---
name: retrospective
description: "Analyse a session transcript for learnings — corrections, reversals, approach changes, and successes. Runs automatically on SessionStart for the previous session. Invoke manually to analyse the current session or review accumulated learnings."
argument-hint: "[session-id, 'current', 'summary', or 'patterns']"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Retrospective

Analyse conversation transcripts to extract learnings. Use `$ARGUMENTS` to control what to do:

- **`current`** — analyse the current session's transcript (Steps 1–3)
- **`latest`** — analyse the most recent completed session (Steps 1–3)
- **`summary`** — show accumulated metrics and trends (runs `generate-metrics.py`)
- **`patterns`** — detect recurring patterns across all sessions (runs `detect-patterns.py`, then Step 4)
- **`full`** — run everything: analyse latest session, detect patterns, generate metrics (Steps 1–5)
- **`{session-id}`** — analyse a specific past session (Steps 1–3)

This skill is also triggered automatically by the SessionStart hook, which runs the analysis scripts on the previous session. Use this skill manually when you want to run analysis mid-session, review metrics, or trigger pattern detection and rule proposals.

## Path resolution

All learnings and rules paths are overridable via environment variables. Test harnesses set these to redirect writes outside permission-gated `.claude/` paths. Users will almost never set them.

```bash
LEARNINGS_DIR="${LEARNINGS_DIR:-.claude/turtlestack/learnings}"
GLOBAL_LEARNINGS_DIR="${GLOBAL_LEARNINGS_DIR:-$HOME/.claude/turtlestack/learnings}"
RULES_DIR="${RULES_DIR:-.claude/rules}"
GLOBAL_RULES_DIR="${GLOBAL_RULES_DIR:-$HOME/.claude/rules}"
```

Run those four lines first in each shell invocation, then use `"$LEARNINGS_DIR"`, `"$GLOBAL_LEARNINGS_DIR"`, `"$RULES_DIR"`, `"$GLOBAL_RULES_DIR"` everywhere that follows.

## Step 1: Locate transcript

Claude stores transcripts at `~/.claude/projects/-{PATH_HASH}/` where PATH_HASH replaces all non-alphanumeric characters with `-`. Worktree sessions get a different hash than the main project, so you need to check all of them, including worktrees that have been removed.

```bash
# Hash: strip leading /, replace non-alphanumeric with -
path_to_hash() { echo "$1" | sed 's|^/||; s|[^a-zA-Z0-9]|-|g'; }

PROJECTS_DIR="$HOME/.claude/projects"
MAIN_HASH_DIR="$PROJECTS_DIR/-$(path_to_hash "$PWD")"

# Write a breadcrumb so future sessions can find this transcript dir
# even after the worktree is removed
[ -d "$MAIN_HASH_DIR" ] && echo "$PWD" > "$MAIN_HASH_DIR/parent-project"

# 1. Active worktrees (git worktree list)
ALL_DIRS=("$MAIN_HASH_DIR")
for wt in $(git worktree list --porcelain 2>/dev/null | sed -n 's/^worktree //p'); do
  wt_dir="$PROJECTS_DIR/-$(path_to_hash "$wt")"
  [ "$wt_dir" != "$MAIN_HASH_DIR" ] && ALL_DIRS+=("$wt_dir")
done

# 2. Removed worktrees (breadcrumb scan)
RESOLVED_PWD=$(pwd -P)
for bc in "$PROJECTS_DIR"/*/parent-project; do
  [ -f "$bc" ] || continue
  bc_dir=$(dirname "$bc")
  bc_project=$(cat "$bc")
  resolved_bc=$(cd "$bc_project" 2>/dev/null && pwd -P || echo "$bc_project")
  [ "$resolved_bc" = "$RESOLVED_PWD" ] && ALL_DIRS+=("$bc_dir")
done

# Filter to existing dirs, deduplicate
TRANSCRIPT_DIRS=()
for d in $(printf '%s\n' "${ALL_DIRS[@]}" | sort -u); do
  [ -d "$d" ] && TRANSCRIPT_DIRS+=("$d")
done
```

For `current`: find the most recently modified `.jsonl` file across all `$TRANSCRIPT_DIRS`.
For a specific session: search all `$TRANSCRIPT_DIRS` for `{session-id}.jsonl`.
For `summary`: skip straight to `generate-metrics.py`. For `patterns`: skip to Step 4.

**Output:** Path to the transcript file, or list of available sessions.

## Step 2: Run analysis (mandatory for session analysis)

Run the analysis script:

```bash
LEARNINGS_DIR="${LEARNINGS_DIR:-.claude/turtlestack/learnings}"
GLOBAL_LEARNINGS_DIR="${GLOBAL_LEARNINGS_DIR:-$HOME/.claude/turtlestack/learnings}"
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/analyse-session.py <transcript.jsonl> \
    --project-dir "$LEARNINGS_DIR" \
    --global-dir "$GLOBAL_LEARNINGS_DIR" \
    --json
```

The script outputs structured JSON with:
- **metrics**: turns, corrections, reversals, successes, correction rate, tokens
- **events**: each correction, reversal, or success with context and timestamps
- **files_modified**: which files were touched and how many times

Read the JSON output and present the results.

**Output:** Metrics summary table and event list.

## Step 3: Interpret, write learnings, and apply local rules (mandatory)

For each event extracted by the script — plus any correction you spot in the transcript that the script missed — interpret it into a learning:

### For corrections (HIGH severity):

Ask: *What did the assistant do wrong, and what should it do differently?*

```markdown
### Learning: [short title]

**Type:** immediate_correction
**What happened:** [assistant did X]
**What was wrong:** [why X was incorrect — the user's actual intent was Y]
**Rule:** [imperative statement — "Always X" or "Never Y"]
**Scope:** [universal — applies to all projects | project-specific — only this codebase]
```

### For reversals (MEDIUM severity):

Ask: *Was this a genuine mistake that was corrected, or normal iterative refinement?*

Files touched 3+ times are flagged, but not all are problems. A file edited 5 times during a planned multi-pass refactor is normal. A file written then immediately rewritten with a different approach is a reversal.

Check `git log` for the file to distinguish iterative refinement from reversals.

### For successes (POSITIVE):

Ask: *What did the assistant do right that should be reinforced?*

Only record successes that are non-obvious — approaches that worked but might not be the default choice. "Wrote code that compiled" is not worth recording. "Used a single bundled PR instead of splitting, and the user confirmed that was the right call" is.

### Evolve the detection patterns (when the script missed something)

`analyse-session.py` finds events by regex. When your own read of the transcript surfaces a correction or approach change the script did NOT flag, extract a pattern that would catch similar messages in the future and add it to `$LEARNINGS_DIR/signals/patterns.json` (create if missing). The script loads this file on every run, so new patterns take effect from the next analysis.

The patterns file has this structure:

```json
{
  "correction": ["\\bfeels (arbitrary|wrong|off)\\b", "\\bunderestimating\\b"],
  "approach_change": ["\\bi think (we|you) should\\b"],
  "acceptance": []
}
```

For each missed event:

1. Identify the **key phrase** that signals the intent (e.g., "feels arbitrary" → correction)
2. Write a regex pattern that would match it and similar phrasings
3. Test the pattern mentally against a few examples — would it false-positive on normal instructions?
4. If the pattern is safe (low false-positive risk), add it to the appropriate category

**Rules for pattern generation:**
- Patterns must be **general enough** to catch variations but **specific enough** to avoid false positives
- `\bfeels (arbitrary|wrong|off|unnecessary)\b` is good — catches a class of pushback
- `\bfeels\b` alone is too broad — would match "it feels responsive"
- Always use `\b` word boundaries to prevent partial matches
- Test against the original message AND imagine 3 other messages — would they match correctly?

### Path 1: Write local learned rules (immediate effect)

For every HIGH severity correction and every recurring pattern, write a **learned rule** to `$RULES_DIR` so it takes effect immediately (next session, or even mid-session if Claude Code hot-reloads rules).

```bash
RULES_DIR="${RULES_DIR:-.claude/rules}"
GLOBAL_RULES_DIR="${GLOBAL_RULES_DIR:-$HOME/.claude/rules}"

# Check existing learned rules in both locations
find "$RULES_DIR" "$GLOBAL_RULES_DIR" -maxdepth 1 -name 'learned--*.md' -type f 2>/dev/null
```

Write the rule file:

```markdown
---
description: "[one-line description of what this rule prevents]"
alwaysApply: true
---

# Learned: [short title]

[imperative rule statement]

**Why:** [what went wrong without this rule — the specific incident]

**Evidence:** [session ID, date, correction summary]
```

File naming: `$RULES_DIR/learned--{kebab-case-topic}.md` for project-specific, `$GLOBAL_RULES_DIR/learned--{kebab-case-topic}.md` for universal.

Examples (project-specific defaults shown):

- `.claude/rules/learned--verify-before-declaring-complete.md`
- `.claude/rules/learned--route-multi-agent-through-coordinator.md`
- `.claude/rules/learned--check-installed-plugins-not-cache.md`

**Scope determines location:**

- **Project-specific** → `$RULES_DIR/learned--{topic}.md` (default `.claude/rules/`)
- **Universal** → `$GLOBAL_RULES_DIR/learned--{topic}.md` (default `~/.claude/rules/`)

**Rules for writing learned rules:**
- One rule per file. Don't combine multiple learnings into one rule.
- The description must be specific enough that Claude can match it to relevant situations.
- Always include the evidence (session ID + what happened). This helps when reviewing whether the rule is still relevant.
- Check for existing learned rules on the same topic. Update rather than duplicate.
- If a learned rule contradicts a marketplace rule, the learned rule takes precedence locally — but flag it for Path 2 (upstream PR) to resolve the conflict.

**Output:** Classified learnings with rules and scope + list of learned rule files written.

## Step 4: Check for patterns (mandatory for `patterns` mode)

Read all session analysis files from `$LEARNINGS_DIR/sessions/` and `$GLOBAL_LEARNINGS_DIR/sessions/`.

```bash
LEARNINGS_DIR="${LEARNINGS_DIR:-.claude/turtlestack/learnings}"
GLOBAL_LEARNINGS_DIR="${GLOBAL_LEARNINGS_DIR:-$HOME/.claude/turtlestack/learnings}"

# Count learnings by type across all sessions
find "$LEARNINGS_DIR/sessions" "$GLOBAL_LEARNINGS_DIR/sessions" -name '*.json' 2>/dev/null
```

For each learning type, count occurrences across sessions. When the same kind of correction appears 3+ times:

```markdown
### Pattern detected: [name]

**Instances:** [count] across [N] sessions
**First seen:** [date]
**Last seen:** [date]
**Common thread:** [what these corrections have in common]
**Proposed rule:** [imperative statement that would prevent recurrence]
**Target:** [which rule file or agent to update]
**Status:** pending_review
```

Save the pattern to `$LEARNINGS_DIR/patterns/{pattern-id}.json`.

**Output:** Pattern table with proposed changes.

## Step 5: Path 2 — Propose upstream PR (when patterns reach threshold)

When a pattern has 5+ instances, OR the user approves a 3+ instance pattern, OR a learned rule contradicts a marketplace rule — propose a PR against the marketplace repo to share the improvement.

### 5a. Draft the change

Determine what needs to change in the marketplace:

| Learning type | Marketplace change |
|---|---|
| Repeated correction about approach | New rule in the relevant plugin's `rules/` directory |
| Pattern in a specific agent's domain | Update to the agent definition or skill |
| Regex pattern that catches a new class of correction | Update to `scripts/analyse-session.py` seed patterns |
| Learned rule that should be shared | Move from `$RULES_DIR/learned--*.md` to the marketplace plugin's `rules/` |

### 5b. Present to user for approval

```markdown
### Proposed upstream change

**Pattern:** [name] (observed [N] times across [M] sessions)
**Local rule:** `$RULES_DIR/learned--{topic}.md` (already active locally)
**Change type:** [new marketplace rule | skill update | agent update | script update]
**Target file in marketplace:** [path relative to marketplace repo root]
**Evidence:**
- Session [id1] ([date]): [correction summary]
- Session [id2] ([date]): [correction summary]
- Session [id3] ([date]): [correction summary]

**Proposed content:**
[the actual change — full file content or diff]

Submit as PR? (Y/n)
```

### 5c. Create the PR

If approved:

1. Determine the marketplace repo location. Check:
   - The `source` field in `~/.claude/settings.json` under `extraKnownMarketplaces`
   - Fall back to asking the user for the repo path

2. Create a branch and apply the change:
   ```bash
   cd <marketplace-repo>
   git checkout -b learning/learned--{topic}
   # Write or edit the target file
   git add <target-file>
   git commit -m "feat: learned rule — {topic}

   Pattern observed {N} times across {M} sessions.
   Evidence: {session IDs}

   Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
   ```

3. Push and create the PR:
   ```bash
   git push -u origin learning/learned--{topic}
   gh pr create --title "Learning: {topic}" --body "$(cat <<'PREOF'
   ## Summary

   This change was proposed by the learning system based on observed patterns.

   **Pattern:** {description}
   **Instances:** {N} across {M} sessions (first seen: {date}, last seen: {date})
   **Local rule:** Has been active locally as `$RULES_DIR/learned--{topic}.md`

   ## Evidence

   {table of session IDs, dates, and correction summaries}

   ## Change

   {description of what changed and why}

   ---
   Generated by `/thinking:retrospective` — the marketplace learning system.
   PREOF
   )"
   ```

4. Update the pattern status in `$LEARNINGS_DIR/patterns/{pattern-id}.json`:
   - Set `"status": "pr_submitted"`
   - Record the PR URL

5. Optionally remove the local learned rule if the PR is merged (the marketplace rule supersedes it).

**Output:** PR URL + updated pattern status.

## Rules

- **The script does extraction, you do interpretation.** The Python script (`analyse-session.py`) handles JSONL parsing and pattern matching. This skill reads the structured output and applies judgment — classifying scope, filtering noise, detecting patterns.
- **Not every reversal is a mistake.** Files touched 3+ times during a planned multi-pass operation are normal iterative refinement. Check the context before flagging.
- **Not every correction is a learning.** "No, use tabs not spaces" in a project with a `.editorconfig` is a config issue, not a learning. Only record corrections that reveal a gap in understanding or process.
- **Universal vs project-specific.** "Don't declare completion without running the audit" is universal. "The config file is at `src/config.ts` not `config/index.ts`" is project-specific. Classify correctly — universal learnings go to `$GLOBAL_LEARNINGS_DIR` (default `~/.claude/turtlestack/learnings/`), project-specific to `$LEARNINGS_DIR` (default `.claude/turtlestack/learnings/`).
- **Patterns are more valuable than incidents.** One correction is an event. Three corrections about the same thing are a pattern. Patterns become rules.
- **Never record user-specific information.** Learnings capture what went wrong and how to fix it, not personal details about the user.
- **The 1-hour rule.** The SessionStart hook analyses the previous session, which gives at least a session-gap delay. This is intentional — it allows delayed corrections (where the user realises later something was wrong) to be captured in the same transcript.
- **Path 1 is immediate, Path 2 is shared.** Always write a local learned rule first (Path 1) so it takes effect immediately. Only propose an upstream PR (Path 2) when the pattern has enough evidence to justify sharing it. A learned rule that works locally for one session is not ready for the marketplace.
- **Local rules take precedence.** If a learned rule contradicts a marketplace rule, the local rule wins. But flag the conflict for Path 2 resolution — either the marketplace rule is wrong (PR to fix) or the local context is special (keep local only).
- **Clean up after merge.** When a Path 2 PR is merged, the corresponding local learned rule becomes redundant. Remove it — the marketplace rule now handles it for everyone.

## Output Format

### Session analysis:
```markdown
## Retrospective: [session-id]

### Metrics
| Metric | Value |
|---|---|
| Duration | [N] minutes |
| Turns | [N] user / [N] assistant |
| Corrections | [N] immediate, [N] approach changes, [N] reversals |
| Successes | [N] |
| Correction rate | [N]% |

### Learnings
| # | Type | Severity | Rule | Scope |
|---|---|---|---|---|
| 1 | [type] | [sev] | [rule] | [scope] |

### Patterns
[Any patterns detected from accumulated data]
```

### Summary mode:
```markdown
## Learning Summary

### Totals (across [N] sessions)
| Metric | Value |
|---|---|
| Sessions analysed | [N] |
| Total corrections | [N] |
| Total successes | [N] |
| Active patterns | [N] |
| Pending proposals | [N] |

### Top patterns
| Pattern | Count | Proposed change | Status |
|---|---|---|---|
```

## Related Skills

- `/thinking:learning` — capture individual learnings in the moment. Retrospective analyses transcripts after the fact.
- `/thinking:wisdom` — when patterns crystallise (85%+ confidence), promote them to wisdom frames.
- `/thinking:health-check` — audits the learning system's coverage as part of project health.
