---
name: handoff
description: "Write or resume a session handoff doc. Use when ending a session with in-flight work that another session will pick up, or starting a session to continue prior work. Captures state explicitly so the next session doesn't have to reconstruct it from chat scrollback."
argument-hint: "[write <topic> | resume | list]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Write a handoff doc when in-flight work needs to cross sessions, or read one to pick work back up. Optional, never automatic — invoke when you know you need it.

Filename: `<YYYY-MM-DD-HHMM>-<slug>.md`. Slug is a short kebab-case description of the topic.

## Path resolution

The handoff directory is `.claude/turtlestack/handoff/` by default. Test harnesses and other tooling may override it via the `HANDOFF_DIR` environment variable.

Every bash command in this skill uses the resolved path:

```bash
HANDOFF_DIR="${HANDOFF_DIR:-.claude/turtlestack/handoff}"
```

Run that line first in each shell invocation, then use `"$HANDOFF_DIR"` everywhere that follows. Users will almost never set the override — it exists so automated tests can redirect writes outside `.claude/`, which is permission-gated.

## Modes

`$ARGUMENTS` selects mode:

| Mode | Trigger | Action |
|---|---|---|
| `write <topic>` | "write a handoff", "we'll need to pick this up later" | Capture current state to a new handoff doc |
| `resume` | "resume", "pick up handoff", "continue where we left off" | Read newest handoff doc, apply it as task context |
| `list` | "show handoffs", "any handoffs?" | List handoff docs with dates and topics |

If `$ARGUMENTS` is empty, default to `list`.

## Mode: write

Goal: capture enough state that a fresh session can continue without scrollback. Not a status report — a continuation contract.

### Step 1: Ensure the handoff directory exists

```bash
HANDOFF_DIR="${HANDOFF_DIR:-.claude/turtlestack/handoff}"
mkdir -p "$HANDOFF_DIR"
```

### Step 2: Gather state

Run in parallel:

- `git status` — dirty files, untracked
- `git log --oneline -5` — recent commits
- `git rev-parse --abbrev-ref HEAD` — current branch
- Any in-flight commands or tasks (check TaskList if available)

### Step 3: Pick a slug

Short kebab-case, derived from `<topic>` argument or the work focus. Examples: `rule-install-fix`, `release-pipeline-cutover`, `auth-middleware-refactor`. Avoid timestamps in the slug — the filename already has one.

### Step 4: Write the doc

Filename: `${HANDOFF_DIR}/<YYYY-MM-DD-HHMM>-<slug>.md`. Use the local date and 24h time.

Template:

```markdown
# Handoff: <one-line description>

## Context

Why this work exists. What problem it solves. One paragraph.

## What changed

What the current session did. List commits if any. Note files touched.

## State at handoff

Concrete facts the next session needs:

- Current branch: `<branch>`
- Dirty files: `<files or "none">`
- Last commit: `<sha> <subject>`
- In-flight: `<what's running, what's waiting>`
- Other relevant state: <env, config, external systems>

## Verify in new session

Numbered steps to confirm prior work landed and decide what's next. Each step
should be runnable without context from the prior session.

1. <Specific check, with the exact command>
2. <Next check>
3. ...

## Failure modes to watch

What might be wrong if a verify step doesn't behave. How to diagnose.

## Files of interest

Bulleted list of paths the next session will likely need to read.
```

### Step 5: Confirm path

Output the absolute path to the new handoff doc. Don't summarise the contents — they're in the file.

## Mode: resume

### Step 1: Locate the handoff

```bash
HANDOFF_DIR="${HANDOFF_DIR:-.claude/turtlestack/handoff}"
find "$HANDOFF_DIR" -maxdepth 1 -name '*.md' -type f 2>/dev/null | sort -r
```

This handles a missing handoff directory cleanly. Do not use bare globs like `ls $HANDOFF_DIR/*.md` — under `set -e` or zsh's default no-match behaviour, an empty directory raises an error instead of returning nothing.

If multiple unresumed handoffs exist, list them and ask which to pick up. Don't assume newest is correct.

If none exist, say so and stop.

### Step 2: Read and apply

Read the chosen handoff doc. Then:

- Verify the **State at handoff** section against current state (branch, dirty files, last commit). Flag drift if reality has moved on.
- Run the **Verify in new session** steps in order. Report results.
- If verification reveals the work is already complete, archive the handoff (see Step 3).
- Otherwise, continue from where the prior session stopped, using **Files of interest** as the starting context.

### Step 3: Archive when done

Once the handoff work is complete and verified, move the doc to the `resumed/` subdirectory:

```bash
HANDOFF_DIR="${HANDOFF_DIR:-.claude/turtlestack/handoff}"
mkdir -p "$HANDOFF_DIR/resumed"
mv "$HANDOFF_DIR/<file>.md" "$HANDOFF_DIR/resumed/"
```

This keeps the handoff directory as the live queue. Resumed docs persist for audit but stay out of the way.

## Mode: list

```bash
HANDOFF_DIR="${HANDOFF_DIR:-.claude/turtlestack/handoff}"
find "$HANDOFF_DIR" -maxdepth 1 -name '*.md' -type f 2>/dev/null | sort -r
```

For each, print: filename, date, first heading line (read with `head -1`). If `$HANDOFF_DIR/resumed/` exists and `--all` is in `$ARGUMENTS`, include those too with a `(resumed)` marker:

```bash
find "$HANDOFF_DIR/resumed" -maxdepth 1 -name '*.md' -type f 2>/dev/null | sort -r
```

If nothing exists, say so plainly.

## Rules

- **Optional, never mandatory.** This is a tool you reach for, not a hook that fires automatically. If the user finishes a session cleanly, no handoff is needed.
- **Write at the moment of stopping**, not retroactively. A handoff written from memory after a context flush is fiction.
- **Concrete state over narrative.** "Branch `main` at `fc47c42`, marketplace.json bumped to 1.9.2, 1.9.3 tag pending workflow run `25148762702`" beats "we made some changes and a release is happening."
- **Verify steps must be self-contained.** Each step runnable cold by a fresh session. No "remember from earlier."
- **Don't bury secrets.** Treat handoff docs like any other repo file — no tokens, no credentials. If the project commits them, they're visible to teammates; if it ignores them via `.gitignore`, they're local-only. Either way, no secrets.
- **One handoff per topic.** Don't pile multiple in-flight threads into one doc — that's drift, not handoff. If two unrelated streams need handoff, write two docs.

## Output

### When writing:

```markdown
## Handoff written

**Path:** `.claude/turtlestack/handoff/<file>.md`
**Topic:** <topic>
**Branch at handoff:** <branch>
**Resume with:** `/handoff resume`
```

### When resuming:

```markdown
## Resuming: <topic>

**Source:** `.claude/turtlestack/handoff/<file>.md`
**State drift:** <none / list of differences>
**Verify results:**
1. <step> — <pass/fail/result>
2. ...

<then continue with the actual work>
```

### When listing:

```markdown
## Handoffs

| # | Date | Topic | File |
|---|---|---|---|
| 1 | 2026-04-30 14:23 | rule-install-fix | .claude/turtlestack/handoff/2026-04-30-1423-rule-install-fix.md |
```

## Related skills

- `/learning` — capture lessons from the work after resuming. Handoffs are continuation; learnings are extraction.
- `/retrospective` — analyse a session for patterns. Use after resuming a complex handoff to capture what made it hard or smooth.
