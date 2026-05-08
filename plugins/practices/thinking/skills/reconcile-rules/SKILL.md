---
name: reconcile-rules
description: "Review learned rules against marketplace rules for overlap. Identifies learned rules that have been superseded by upstream changes and recommends cleanup. Use periodically to reduce context bloat from duplicate rules."
argument-hint: "['global' to check ~/.claude/rules/, 'project' for .claude/rules/, or 'all']"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

# Reconcile Rules

Compare learned rules against marketplace rules to find overlap and recommend cleanup. Learned rules are created by the retrospective system when corrections are detected. Marketplace rules are installed by plugins. Over time, learnings get folded into the marketplace — but the local learned rules stick around, doubling up in context.

## Path resolution

All rules and learnings paths are overridable via environment variables. Test harnesses set these to redirect writes outside permission-gated `.claude/` paths. Users will almost never set them.

```bash
RULES_DIR="${RULES_DIR:-.claude/rules}"
GLOBAL_RULES_DIR="${GLOBAL_RULES_DIR:-$HOME/.claude/rules}"
LEARNINGS_DIR="${LEARNINGS_DIR:-.claude/turtlestack/learnings}"
GLOBAL_LEARNINGS_DIR="${GLOBAL_LEARNINGS_DIR:-$HOME/.claude/turtlestack/learnings}"
```

Run those four lines first in each shell invocation, then use the variables everywhere that follows.

## Step 1: Inventory rules

Scan both locations based on `$ARGUMENTS`:

```bash
RULES_DIR="${RULES_DIR:-.claude/rules}"
GLOBAL_RULES_DIR="${GLOBAL_RULES_DIR:-$HOME/.claude/rules}"

# Global learned rules
find "$GLOBAL_RULES_DIR" -maxdepth 1 -name 'learned--*.md' -type f 2>/dev/null

# Project learned rules
find "$RULES_DIR" -maxdepth 1 -name 'learned--*.md' -type f 2>/dev/null

# Marketplace rules (installed by plugins)
find "$RULES_DIR" "$GLOBAL_RULES_DIR" -maxdepth 1 -name '*.md' -type f 2>/dev/null | grep -v '/learned--'
```

Read every rule file — both learned and marketplace. For each, extract:
- The `description` from frontmatter
- The core imperative (the actual rule statement)
- The evidence/source

**Output:** Table of all rules with source (learned vs marketplace plugin).

## Step 2: Compare for overlap

For each learned rule, compare it against every marketplace rule. You are looking for:

**Full supersession:** The marketplace rule covers the same ground as the learned rule. The learned rule adds nothing beyond what the marketplace now enforces.

Example: `learned--evaluate-platforms-as-package.md` says "evaluate infrastructure decisions together." If the architect plugin's architecture rule now says the same thing, the learned rule is superseded.

**Partial overlap:** The marketplace rule covers part of the learned rule, but the learned rule has additional specifics not in the marketplace.

Example: `learned--no-code-without-spec.md` says "never code without a spec." The marketplace has `spec-first.md` in all implementation agents. If the content is the same, it's superseded. If the learned rule has project-specific detail (like a specific `docs/quality/specs/` path), it's partial.

**No overlap:** The learned rule covers something the marketplace doesn't address at all. Keep it.

**Output:** Classification table.

## Step 3: Present recommendations

```markdown
## Rule Reconciliation

### Superseded (safe to remove)

| Learned rule | Superseded by | Confidence | Reason |
|---|---|---|---|
| `learned--{topic}.md` | `{plugin}--{rule}.md` | High/Medium | [why they overlap] |

### Partial overlap (review needed)

| Learned rule | Overlaps with | What's extra in learned | Recommendation |
|---|---|---|---|
| `learned--{topic}.md` | `{plugin}--{rule}.md` | [specific additional content] | Keep / Merge / Remove |

### No overlap (keep)

| Learned rule | Covers |
|---|---|
| `learned--{topic}.md` | [what it covers that no marketplace rule addresses] |

### Summary
- Total learned rules: [N]
- Superseded (remove): [N]
- Partial overlap (review): [N]
- Unique (keep): [N]
- Context tokens saved if cleaned up: ~[estimate based on file sizes]
```

Wait for the user to approve removals before deleting anything.

## Step 4: Apply cleanup (only with user approval)

For each rule the user approves for removal:

```bash
RULES_DIR="${RULES_DIR:-.claude/rules}"
GLOBAL_RULES_DIR="${GLOBAL_RULES_DIR:-$HOME/.claude/rules}"

rm "$GLOBAL_RULES_DIR/learned--{topic}.md"
# or
rm "$RULES_DIR/learned--{topic}.md"
```

Report what was removed.

After cleanup, update the reconciliation snapshot so the SessionStart hook won't nudge again until plugins change:

```bash
RULES_DIR="${RULES_DIR:-.claude/rules}"
GLOBAL_RULES_DIR="${GLOBAL_RULES_DIR:-$HOME/.claude/rules}"
GLOBAL_LEARNINGS_DIR="${GLOBAL_LEARNINGS_DIR:-$HOME/.claude/turtlestack/learnings}"

RULES_DIR="$RULES_DIR" GLOBAL_RULES_DIR="$GLOBAL_RULES_DIR" GLOBAL_LEARNINGS_DIR="$GLOBAL_LEARNINGS_DIR" \
python3 -c "
import json, os, glob, datetime
plugins = set()
for d in [os.environ['GLOBAL_RULES_DIR'], os.environ['RULES_DIR']]:
    for f in glob.glob(os.path.join(d, '*.md')):
        basename = os.path.basename(f)
        if not basename.startswith('learned--'):
            parts = basename.split('--', 1)
            if len(parts) == 2:
                plugins.add(parts[0])
snapshot = {'marketplace_plugins': sorted(plugins), 'reconciled_at': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')}
os.makedirs(os.environ['GLOBAL_LEARNINGS_DIR'], exist_ok=True)
with open(os.path.join(os.environ['GLOBAL_LEARNINGS_DIR'], 'reconcile-snapshot.json'), 'w') as f:
    json.dump(snapshot, f, indent=2)
"
```

**Do NOT remove rules the user hasn't explicitly approved.** Present the list, wait for confirmation, then act.

## Rules

- **Never auto-delete.** This skill recommends. The user decides. Present the evidence and wait.
- **Err toward keeping.** If you're unsure whether a marketplace rule fully covers a learned rule, classify as "partial overlap" not "superseded." False removal is worse than slight duplication.
- **Context cost matters.** Each rule loaded into context costs tokens. 6 learned rules at ~15 lines each is ~90 lines of context. If 3 are superseded, removing them saves ~45 lines per session, every session.
- **Check both locations.** Global (`$GLOBAL_RULES_DIR`, default `~/.claude/rules/`) and project (`$RULES_DIR`, default `.claude/rules/`). A global learned rule might be superseded by a project-installed marketplace rule.
- **Learned rules with evidence are more valuable.** A learned rule with "Session 681945ff, user corrected 3 times" carries more weight than a generic marketplace rule. If the marketplace rule is weaker, flag it — maybe the marketplace needs updating instead.

## Related Skills

- `/thinking:retrospective` — creates learned rules. This skill cleans them up when the marketplace catches up.
- `/thinking:propose-improvement` — proposes PRs to upstream learned rules into the marketplace. After merge, run reconcile to clean up.
