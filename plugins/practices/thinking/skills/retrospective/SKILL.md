---
name: retrospective
description: "Look back over a session (or a window of sessions) for lessons — corrections, reversals, approach changes, confirmed successes — and turn the ones that should apply everywhere into learned rules. Use at the end of a piece of work, when something went wrong and the cause only became clear later, or when asked to capture a lesson as a rule."
argument-hint: "['current', a session id, or 'last N' sessions]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Retrospective

Review work after the fact and extract lessons. Looking back beats catching mistakes live: often nobody knows what good looks like until further along.

## Where this sits next to native memory

Claude Code's auto memory already captures in-session facts, preferences and corrections for the current project, and loads them each session. Don't duplicate it. This skill covers what auto memory doesn't:

- **Cross-project lessons.** Auto memory is per-project. A lesson that should hold in every project becomes a global learned rule.
- **Project rules everyone on the repo should get.** A project learned rule in `.claude/rules/` is visible to the whole team; auto memory is per-user.
- **Sharing upstream.** A learned rule with enough evidence can become a marketplace change via `/thinking:propose-improvement`.

## Path resolution

Test harnesses override these; users rarely will.

```bash
CONFIG_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
RULES_DIR="${RULES_DIR:-.claude/rules}"
GLOBAL_RULES_DIR="${GLOBAL_RULES_DIR:-$CONFIG_DIR/rules}"
```

## Step 1: Gather the session

- **`current`** (default): use the conversation in context.
- **A session id or `last N`**: read transcripts directly. They live at `$CONFIG_DIR/projects/-<hash>/<session-id>.jsonl`, where `<hash>` is the absolute project path with every non-alphanumeric character replaced by `-`. Worktree sessions have their own hash, so check `git worktree list` paths too. Pull the user turns, which carry the corrections (tool results are skipped):

```bash
jq -r 'select(.type=="user") | .message.content | if type=="string" then . else (map(select(.type=="text") | .text) | join("\n")) end | select(length>0)' "$TRANSCRIPT" | head -c 20000
```

## Step 2: Find the lessons

Read for:

- **Corrections** (high): the user said the approach was wrong. Ask what was done, what was wrong, and what to do instead.
- **Reversals** (medium): work redone with a different approach. Check `git log` to tell a genuine reversal from planned iteration.
- **Approach changes**: the user redirected the plan.
- **Confirmed successes**: a non-default choice the user confirmed was right. Skip the obvious.

Not every correction is a lesson. "Use tabs" in a repo with `.editorconfig` is config, not a gap in understanding. Never record personal details about the user.

## Step 3: Decide where each lesson goes

| Lesson | Home |
|---|---|
| A fact or preference for this project only | Leave it to auto memory (or write a memory if it was missed) |
| A rule for this repo that teammates should share | `$RULES_DIR/learned--{topic}.md` |
| A rule for every project | `$GLOBAL_RULES_DIR/learned--{topic}.md` |
| A gap in a marketplace rule, skill or agent | Learned rule now, then `/thinking:propose-improvement` |

Ask "does this apply to every project, or just this one?" "Always X" / "Never X" usually means global; "in this repo, X lives at Y" means project.

## Step 4: Write the learned rule (Path 1: immediate effect)

Learned rules are always-on and count against Claude Code's 150k-character instruction budget, so earn the space:

1. Look for an existing rule on the same topic and update it rather than adding a new one:
   ```bash
   find "$RULES_DIR" "$GLOBAL_RULES_DIR" -maxdepth 1 -name 'learned--*.md' -type f 2>/dev/null
   ```
2. Check whether a marketplace rule or skill already says it. If it does, don't write a rule; if the marketplace version is weaker, go to Step 5.
3. Keep it short. The rule, why, how to apply, evidence. Aim for under 2k characters.

```markdown
# Learned: [short title]

[imperative rule statement]

**Why:** [the specific incident, with the user's words where they matter]

**How to apply:** [when it fires, what to do]

**Evidence:** [session id, date, project]
```

If the same rule must exist in more than one Claude config directory (several profiles), say so, so the user can keep the copies in step.

## Step 5: Share it (Path 2)

When a learned rule has held up across sessions, or contradicts a marketplace rule, offer `/thinking:propose-improvement` to move it upstream. The local rule stays until the upstream change is merged and installed; then `/thinking:reconcile-rules` removes it.

## Output

```markdown
## Retrospective: [session or window]

### Lessons
| # | Type | Lesson | Home |
|---|---|---|---|

### Rules written or updated
- [path]: [one line]

### Upstream candidates
- [rule]: [why it's ready, or what evidence is missing]
```

## Related skills

- `/thinking:reconcile-rules` — removes learned rules once the marketplace covers them.
- `/thinking:propose-improvement` — raises the upstream PR for a learned rule.
- `/thinking:health-check` — reports rule counts and the instruction budget.
