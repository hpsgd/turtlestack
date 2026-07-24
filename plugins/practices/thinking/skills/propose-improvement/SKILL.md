---
name: propose-improvement
description: "Propose a change to a marketplace repo based on learned patterns — new rules, updated skills, evolved regex patterns. Infers which upstream marketplace the learning belongs to, confirms with the user, then creates a branch, applies changes, shows diff for review, and raises a PR on approval. Use when patterns have enough evidence to share upstream."
argument-hint: "[pattern-id, 'all' to review all pending patterns, or describe the change]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Propose Improvement

Stage a change to a marketplace repo based on $ARGUMENTS. This skill handles the full Path 2 workflow: identify the right upstream, create a branch, apply changes, review with the user, and raise a PR.

## Path resolution

All learnings and rules paths are overridable via environment variables. Test harnesses set these to redirect writes outside permission-gated `.claude/` paths. Users will almost never set them.

```bash
LEARNINGS_DIR="${LEARNINGS_DIR:-.claude/turtlestack/learnings}"
GLOBAL_LEARNINGS_DIR="${GLOBAL_LEARNINGS_DIR:-$HOME/.claude/turtlestack/learnings}"
RULES_DIR="${RULES_DIR:-.claude/rules}"
GLOBAL_RULES_DIR="${GLOBAL_RULES_DIR:-$HOME/.claude/rules}"
```

Run those four lines first in each shell invocation, then use the variables everywhere that follows.

## Step 1: Enumerate known marketplaces

Discover all marketplaces from settings and the current project:

```bash
python3 -c "
import json, os

marketplaces = {}

# Read settings files for extraKnownMarketplaces
for f in [os.path.expanduser('~/.claude/settings.json'), '.claude/settings.json', '.claude/settings.local.json']:
    try:
        d = json.load(open(f))
        mkts = d.get('extraKnownMarketplaces', {})
        for name, cfg in mkts.items():
            src = cfg.get('source', {})
            repo = src.get('repo', '')
            path = src.get('path', '')
            if repo or path:
                marketplaces[name] = {'repo': repo, 'path': path, 'org': repo.split('/')[0] if '/' in repo else ''}
    except: pass

# Read enabledPlugins to map plugin -> marketplace
enabled = {}
for f in [os.path.expanduser('~/.claude/settings.json'), '.claude/settings.json', '.claude/settings.local.json']:
    try:
        d = json.load(open(f))
        for key, val in d.get('enabledPlugins', {}).items():
            if val and '@' in key:
                plugin, mkt = key.rsplit('@', 1)
                enabled[plugin] = mkt
    except: pass

# Also check if current dir is itself a marketplace
mkt_file = '.claude-plugin/marketplace.json'
if os.path.exists(mkt_file):
    try:
        m = json.load(open(mkt_file))
        local_name = m.get('name', '')
        if local_name and local_name not in marketplaces:
            marketplaces[local_name] = {'repo': '', 'path': '.', 'org': ''}
    except: pass

import json as j
print(j.dumps({'marketplaces': marketplaces, 'plugin_sources': enabled}, indent=2))
"
```

This gives you two maps:
- `marketplaces`: name → `{repo, path, org}` for every known marketplace
- `plugin_sources`: plugin name → marketplace name for every enabled plugin

**Output:** All known marketplaces and their plugin mappings.

## Step 2: Infer and confirm the target

Determine which plugin the learning relates to. Sources of signal (check in order):

1. **Explicit in arguments** — the user named a plugin or marketplace
2. **Pattern metadata** — the pattern file may reference specific skills or files
3. **Learned rule filename** — `learned--es-mindset-review.md` relates to event sourcing, likely the `coding-standards` plugin
4. **Session context** — which plugins were active when the correction happened
5. **File paths in evidence** — if the correction involved files under `plugins/practices/coding-standards/`, the target is obvious

Once you have a candidate plugin, resolve its marketplace:

```bash
# Example: plugin "coding-standards" → marketplace "turtlestack" → org "hpsgd"
```

### Org comparison

Compare the target marketplace's GitHub org against the org of the marketplace where this learning skill resides. The learning skill's own marketplace is resolved the same way (from `extraKnownMarketplaces` or the local `marketplace.json` + `git remote`).

```bash
# Resolve this skill's org from the repo it lives in
python3 -c "
import subprocess, re
try:
    remote = subprocess.check_output(['git', 'remote', 'get-url', 'origin'], text=True).strip()
    # Handle both HTTPS and SSH formats
    match = re.search(r'[:/]([^/]+)/[^/]+(?:\.git)?$', remote)
    print(match.group(1) if match else 'UNKNOWN')
except: print('UNKNOWN')
"
```

| Org match? | Classification | Action |
|---|---|---|
| Same org | **Owned upstream** | Full PR flow (Step 3 onwards) |
| Different org | **Third-party** | Local rule only + advisory (see below) |
| Can't resolve | **Unknown** | Ask the user |

### Third-party handling

If the target marketplace belongs to a different GitHub org:

```markdown
### Third-party plugin: {plugin}@{marketplace}

This learning relates to **{plugin}**, which comes from **{marketplace}** (`{org}/{repo}`).
That's a third-party marketplace — I can't raise a PR there directly.

**Options:**
1. Save as a local learned rule only (immediate effect, no upstream)
2. Open an issue on `{org}/{repo}` describing the finding
3. Fork the repo and raise a PR from the fork

**Recommendation:** Option 1 is safest. The local rule protects you now.
If this is a bug or outdated dependency that affects other users, option 2 is worth doing.
```

Wait for the user's choice before proceeding. If they choose option 1, write the local rule and stop. If option 2 or 3, proceed with that path.

### Confirmation (mandatory for all targets)

Before proceeding, confirm:

```markdown
This learning relates to **{plugin}** from **{marketplace}** (`{org}/{repo}`).
I'll create a PR against that repo. Correct? (Y/n/change target)
```

If the user says **change target**, let them specify the correct marketplace and plugin, then re-confirm.

**Output:** Confirmed target marketplace, repo, org, and plugin.

## Step 3: Identify what to propose

### From a pattern ID

Read the pattern file from `$LEARNINGS_DIR/patterns/{pattern-id}.json` or `$GLOBAL_LEARNINGS_DIR/patterns/`.

Check:
- `count` >= 3 (minimum for a proposal)
- `status` is `detected` or `pending_review` (not already submitted)
- Evidence is sufficient (multiple sessions, clear common thread)

### From a learned rule

If the user has a local learned rule (`$RULES_DIR/learned--{topic}.md`) that they want to upstream:
- Read the rule content
- The target plugin was already resolved in Step 2

### From a direct description

If the user describes the change directly, skip the pattern lookup and proceed to Step 4.

**Output:** The proposed change: what, where, why, and evidence.

## Step 4: Determine the target file

Map the learning to a file in the target marketplace repo:

| Learning type | Target in marketplace |
|---|---|
| New rule (process/convention) | `plugins/{category}/{plugin}/rules/{topic}.md` |
| Skill update (methodology change) | `plugins/{category}/{plugin}/skills/{skill}/SKILL.md` |
| Agent update (responsibility change) | `plugins/{category}/{plugin}/agents/{agent}.md` |
| Regex pattern evolution | `scripts/analyse-session.py` |
| Template improvement | `plugins/{category}/{plugin}/templates/{template}.md` |
| Cross-cutting rule | `plugins/practices/coding-standards/rules/{topic}.md` |

If the target repo is not the current working directory, clone or locate it first:

```bash
# Check if we have a local path for this marketplace
# If not, clone to a temp location
TARGET_REPO="<resolved-path-or-clone>"
cd "$TARGET_REPO"
```

Read the current version of the target file to understand what exists.

**Output:** Target file path + current content summary.

## Step 5: Create branch and apply changes

```bash
cd "$TARGET_REPO"

# Ensure we're on a clean main branch
git fetch origin
git checkout main
git pull --ff-only

# Create the proposal branch
BRANCH="learning/$(echo '{topic}' | tr ' ' '-' | tr '[:upper:]' '[:lower:]')"
git checkout -b "$BRANCH"
```

Apply the change. Depending on type:

### New rule file

Write the complete rule file using `Write`. Follow the existing rule format (YAML frontmatter with `description`, markdown body with imperatives).

### Skill/agent edit

Use `Edit` to modify the specific section. Keep changes minimal — only add what the learning requires.

### Regex pattern update

Read the current seed patterns in the script, add the new patterns to the appropriate list. Use `Edit`.

**Output:** Files modified on the branch.

## Step 6: Show diff for review (mandatory — never skip)

```bash
cd "$TARGET_REPO"
git diff --stat
git diff
```

Present the diff to the user with context:

```markdown
### Proposed change: [title]

**Target:** `{org}/{repo}` ({marketplace name})
**Branch:** `learning/{topic}`
**Pattern:** [pattern-id] — [N] instances across [M] sessions
**Evidence:**
- [session date]: [correction summary]
- [session date]: [correction summary]

**Files changed:**
[git diff --stat output]

**Diff:**
[git diff output — or summarise if large]

**Local rule:** `$RULES_DIR/learned--{topic}.md` has been active since [date]

Approve and create PR? (Y/n/edit)
```

If the user says **edit**: let them modify the changes, then re-show the diff.
If the user says **no**: discard the branch (`git checkout main && git branch -D learning/{topic}`).
If the user says **yes**: proceed to Step 7.

**Output:** Diff presented, user decision captured.

## Step 7: Commit, push, and create PR

```bash
cd "$TARGET_REPO"

# Stage and commit
git add <changed-files>
git commit -m "$(cat <<'COMMITEOF'
feat: learned rule — {topic}

Pattern observed {N} times across {M} sessions.
Local rule has been active since {date}.

Evidence:
- {session1}: {summary}
- {session2}: {summary}

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
COMMITEOF
)"

# Push
git push -u origin "learning/{topic}"

# Create PR
gh pr create \
  --title "Learning: {topic}" \
  --body "$(cat <<'PREOF'
## Summary

Proposed by the learning system based on observed patterns.

**Source project:** {project where the learning was captured}
**Pattern:** {description}
**Instances:** {N} across {M} sessions
**First seen:** {date} | **Last seen:** {date}
**Local rule:** Active as `$RULES_DIR/learned--{topic}.md` since {date}

## Evidence

| Session | Date | Correction |
|---|---|---|
| {id} | {date} | {summary} |

## Change

{what changed and why}

---
🤖 Generated by `/thinking:propose-improvement`
PREOF
)"

# Return to main
git checkout main
```

**Output:** PR URL.

## Step 8: Update tracking

After the PR is created:

1. Update the pattern file (`$LEARNINGS_DIR/patterns/{pattern-id}.json`):
   ```json
   {
     "status": "pr_submitted",
     "pr_url": "https://github.com/...",
     "pr_submitted_at": "2026-04-03T...",
     "target_marketplace": "{marketplace-name}",
     "target_repo": "{org}/{repo}"
   }
   ```

2. Add a note to the local learned rule:
   ```markdown
   <!-- Upstream PR: {pr_url} ({org}/{repo}) — remove this rule after PR is merged -->
   ```

3. Log the proposal in `$LEARNINGS_DIR/proposals/`:
   ```json
   {
     "pattern_id": "pat-...",
     "pr_url": "...",
     "target_marketplace": "...",
     "target_repo": "...",
     "branch": "learning/...",
     "files_changed": [...],
     "submitted_at": "...",
     "status": "open"
   }
   ```

**Output:** Tracking updated, PR URL confirmed.

## Rules

- **Never push without user approval.** Step 6 (diff review) is mandatory. The user must see exactly what will be proposed before anything is pushed.
- **Always confirm the target.** Step 2 confirmation is mandatory. The user must agree with the inferred target marketplace before any changes are made.
- **One change per PR.** Each pattern or learned rule gets its own branch and PR. Don't bundle unrelated changes.
- **Evidence is mandatory.** Every PR must include the session IDs and correction summaries that justify the change. A rule without evidence is an opinion.
- **Minimal changes.** Only modify what the learning requires. Don't refactor surrounding code or "improve" adjacent content.
- **Clean branch hygiene.** Always branch from a fresh `main`. Delete the branch locally after PR creation. If the PR is rejected, note the reason in the pattern file.
- **Local rule stays until merge.** The `$RULES_DIR/learned--*.md` file (default `.claude/rules/`) remains active locally until the upstream PR is merged. Don't remove it prematurely.
- **Return to main.** Always `git checkout main` at the end, regardless of outcome. Never leave a repo on a feature branch.
- **Same org = owned, different org = third-party.** Org comparison uses the GitHub org of the repo where this skill resides vs the target marketplace's repo. No config flags needed.
- **Third-party learnings stay local by default.** Don't raise PRs against repos you don't own without explicit user instruction.

## Output Format

```markdown
## Improvement Proposed: [title]

**Target:** `{org}/{repo}` ({marketplace name})
**PR:** [url]
**Branch:** `learning/{topic}`
**Pattern:** {N} instances across {M} sessions
**Files changed:** [count]
**Status:** PR submitted — awaiting review

### Next steps
1. Review the PR on GitHub
2. If merged, run `/thinking:reconcile-rules` to clean up the local learned rule
3. The marketplace update will take effect on next plugin cache refresh
```

## Related Skills

- `/thinking:retrospective` — identifies patterns and proposes changes. This skill executes the proposal.
- `/thinking:learning` — captures individual learnings. Patterns emerge from accumulated learnings.
- `/thinking:reconcile-rules` — cleans up local rules after upstream PRs are merged.
