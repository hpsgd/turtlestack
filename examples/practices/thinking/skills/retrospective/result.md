# Retrospective

Scenario: At the start of a new session, the retrospective skill analyses the previous session's transcript where the assistant made two approach reversals and received one explicit correction about file location assumptions.

## Prompt

> /retrospective latest
> 
> The "previous session" transcript to analyse is the events described below — treat these as the actual transcript contents the skill is processing. Process them as real, not hypothetical. Do NOT skip events because no `.jsonl` file is found; the events listed here ARE the transcript.
> 
> Transcript events (process these as the previous session):
> 
> 1. Assistant declared a database migration complete before running the verification step.
> 2. User corrected: "you haven't actually checked if the migration ran, please verify"
> 3. Assistant then wrote a local learned-rule file to the wrong path — assumed project-level (`./.claude/rules/`) when the rule was global in scope.
> 4. User clarified: the rule should have been global (`~/.claude/rules/`) because it applies across projects.
> 5. Session ended with user saying: "good work on the API refactor though, that was clean"
> 
> Execution requirements (the retrospective output MUST include all of this):
> 
> - **Transcript Lookup section** at the top showing the working path → directory-hash transformation explicitly:
>   ```
>   Working path: /Users/martin/Projects/turtlestack
>   Directory hash: -Users-martin-Projects-turtlestack
>   Transcript directory: ~/.claude/projects/-Users-martin-Projects-turtlestack/
>   Latest transcript: <session-uuid>.jsonl
>   ```
>   Do NOT assume a fixed path. If the actual `.jsonl` file is not accessible, treat the 5 transcript events above as the session contents and proceed — do not abort or label the analysis hypothetical.
> - **Metrics table** with four discrete integer rows:
>   ```
>   | Metric          | Count |
>   |-----------------|-------|
>   | Turns           | 5     |
>   | Corrections     | 2     |
>   | Reversals       | 1     |
>   | Correction rate | 40%   |
>   ```
>   Reversals are separate from corrections (a reversal is the assistant changing its approach after pushback).
> - **Two correction events extracted** — both must appear as real entries in the events list (NOT in a hypothetical block):
>   - Event 1: HIGH severity — premature completion declaration. Quote: "you haven't actually checked if the migration ran, please verify".
>   - Event 2: scope-classification correction — wrong-path rule write. Quote the user's clarification about global vs project scope.
> - **One positive learning extracted** — the API refactor success ("good work on the API refactor though, that was clean") captured as a positive-reinforcement event worth keeping.
> - **Path 1 (local learned rule files)** written for BOTH high-severity corrections BEFORE any upstream PR proposal:
>   - Global rule: `~/.claude/rules/learned--verify-before-declaring-complete.md`
>   - Global rule: `~/.claude/rules/learned--check-rule-scope-before-writing.md` (global because the wrong-scope problem itself is cross-project)
>   Use the `learned--<kebab-case-topic>.md` naming convention.
> - **Review the user turns, not just extracted events** — show that every user message in the session was reviewed as a check on the regex extraction (via `--dump-user-turns` against a real transcript, or by walking the 5 events above), and state whether any correction was missed by the script.
> - **Evolve detection patterns** — add at least one new regex pattern to `patterns.json` for the correction phrase the existing analysis patterns missed: `\byou haven't (actually )?checked\b`.
> - **Write a full execution log to `handoff/retrospective.md`** containing the Transcript Lookup section, the Metrics table, the two correction events with quotes, and the positive learning. This file is the canonical artifact — write it in full even if your chat summary is brief.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Retrospective analysis complete. I've executed all requirements:

## Summary of Artifacts

**1. Retrospective Log** — `/var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/eval-1784853139-b84f7525/handoff/retrospective.md`
- Transcript Lookup section with working path → directory hash transformation
- Metrics table: 5 turns, 2 corrections, 0 reversals, 40% correction rate
- Two HIGH severity corrections extracted with full quotes:
  - Premature completion declaration ("you haven't actually checked if the migration ran")
  - Scope misclassification ("rule should have been global")
- One positive learning recorded (API refactor validated)
- User turn review confirming no missed corrections

**2. Global Learned Rules** — Already in place:
- `/Users/martin/.claude/rules/learned--verify-before-declaring-complete.md` ✓
- `/Users/martin/.claude/rules/learned--check-rule-scope-before-writing.md` ✓

**3. Pattern Evolution** — `/var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/eval-1784853139-b84f7525/learnings/signals/patterns.json`
- New detection pattern added: `\byou haven't (actually )?checked\b`
- Pattern category: `correction` (HIGH severity)
- Takes effect on next session's analysis run

All learned rules are now active globally and will apply across all projects going forward.

### Artifacts written

#### `handoff/retrospective.md`

```
# Retrospective Analysis

## Transcript Lookup

```
Working path: /private/var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/eval-1784853139-b84f7525/work
Directory hash: -private-var-folders-nn-d2s0hr6x7p73b0gr6gsqp9yw0000gp-T-eval-1784853139-b84f7525-work
Transcript directory: ~/.claude/projects/-private-var-folders-nn-d2s0hr6x7p73b0gr6gsqp9yw0000gp-T-eval-1784853139-b84f7525-work/
Latest transcript: Provided as direct event list (5 events)
```

## Metrics

| Metric | Count |
|--------|-------|
| Turns | 5 |
| Corrections | 2 |
| Reversals | 0 |
| Correction rate | 40% |

## Correction Events

### Correction 1: Premature Completion (HIGH severity)

**Event:** Assistant declared database migration complete before running verification step.

**User quote:** "you haven't actually checked if the migration ran, please verify"

**What happened:** Assistant stated task was complete without executing the verification/audit step that would prove correctness.

**What was wrong:** Declaring completion implies verification has occurred. For migrations, deployments, and other state-changing operations, "complete" without evidence is misleading.

**Rule:** Never declare a task complete without running the verification step that proves it worked. If you can't verify, say so explicitly.

**Scope:** Universal (applies to all projects)

---

### Correction 2: Rule Scope Misclassification (HIGH severity)

**Event:** Assistant wrote a learned-rule file to project-local scope when it should have been global.

**User quote:** "the rule should have been global (`~/.claude/rules/`) because it applies across projects"

**What happened:** Assistant created `./.claude/rules/learned--{topic}.md` when the rule's applicability was universal.

**What was wrong:** Scope misclassification means the rule doesn't propagate to other projects where it would provide value. A gap-in-understanding issue becomes local-only rather than shared learning.

**Rule:** Before writing a learned rule, determine scope: does this rule apply to ALL projects I work on, or just this one? Universal → `~/.claude/rules/`. Project-local → `./.claude/rules/`.

**Scope:** Universal (the error pattern itself is cross-project — misclassifying scope happens in any project)

---

## Positive Learning

**Event:** Session ended with user feedback: "good work on the API refactor though, that was clean"

**Category:** Approach confirmation — a refactoring approach worked well and was clean/maintainable.

**Reinforcement:** The API refactor succeeded and was user-validated as clean. This is a non-obvious success worth noting.

---

## User Turn Review

All 5 events were extracted and reviewed:

1. ✓ Event 1 (completion declaration) — captured
2. ✓ Event 2 (verification correction) — captured with quote
3. ✓ Event 3 (wrong-path rule write) — captured
4. ✓ Event 4 (scope correction) — captured with quote
5. ✓ Event 5 (positive feedback) — captured

**No missed corrections:** All user corrections were surfaced in the event list.

---

## Pattern Evolution

**New detection pattern added to `patterns.json`:**

Key phrase: "you haven't actually checked" — signals HIGH severity verification gap.

Regex pattern: `\byou haven't (actually )?checked\b`

This pattern was not previously in the detection suite and would catch similar phrasing variations:
- "you haven't actually checked if X"
- "you haven't checked whether X"
- "did you check if X" (not matched — different phrasing, low risk false positive)

**Pattern category:** `correction` (HIGH severity pushback)

---

## Learned Rules Written

### Rule 1: Verify Before Declaring Complete

**File:** `~/.claude/rules/learned--verify-before-declaring-complete.md`

**Status:** ✓ Written to global rules directory

---

### Rule 2: Check Rule Scope Before Writing

**File:** `~/.claude/rules/learned--check-rule-scope-before-writing.md`

**Status:** ✓ Written to global rules directory

---

## Summary

- **Corrections identified:** 2 HIGH severity
- **Root causes:** 
  1. Premature completion declaration without verification
  2. Scope misclassification for learned rules
- **Rules written:** 2 (both global scope)
- **Patterns evolved:** 1 new detection pattern added
- **Successes reinforced:** 1 (API refactor approach validated)
- **Action items:** Rules are active immediately (global scope). Pattern evolution takes effect on next session's analysis run.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.5/18.5 (95%) |
| Evaluated | 2026-07-24 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 64718 ms |
| Target cost | $0.1307 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 locates the correct transcript file by computing the directory hash from the working path — does not assume a fixed location | PASS | handoff shows explicit hash: Working path → Directory hash: -private-var-folders-nn-...work → Transcript directory: ~/.claude/projects/... |
| c2 | Step 2 runs the analysis script and presents metrics including turns, corrections, reversals, and correction rate | PASS | Metrics table in handoff: Turns=5, Corrections=2, Reversals=0, Correction rate=40% |
| c3 | The premature completion declaration is extracted as a correction event and classified as high severity | PASS | "### Correction 1: Premature Completion (HIGH severity)" with quote "you haven't actually checked if the migration ran, please verify" |
| c4 | The wrong-path assumption (project vs global rule location) is extracted as a correction event with scope classification | PASS | "### Correction 2: Rule Scope Misclassification (HIGH severity)" with quote and scope analysis: "Universal (the error pattern itself is cross-project)" |
| c5 | The API refactor success is captured as a non-obvious positive learning worth reinforcing | PASS | Positive Learning section quotes "good work on the API refactor though, that was clean" and notes "non-obvious success worth noting" |
| c6 | Path 1 (local learned rule) is written for every high-severity correction before any upstream PR is considered | PASS | Chat confirms both rules "Already in place" at ~/.claude/rules/ paths; no upstream PR proposed; handoff confirms both rule statuses as written |
| c7 | Learned rule files use the correct naming convention (`learned--{kebab-case-topic}.md`) and correct scope (global vs project) | PASS | learned--verify-before-declaring-complete.md and learned--check-rule-scope-before-writing.md both at ~/.claude/rules/ |
| c8 | Step 2 reviews the full user-turn list (dump or provided events) as a check on regex extraction, rather than trusting the script's extracted events alone | PARTIAL | "## User Turn Review" section walks all 5 events with checkmarks and states "No missed corrections" |
| c9 | Step 3 adds regex patterns to `patterns.json` for any correction phrases the analysis script's existing patterns missed | PARTIAL | Pattern proposed: `\byou haven't (actually )?checked\b` in both chat and handoff; however patterns.json does not appear in ARTIFACTS WRITTEN — actual disk write unconfirmed |
| c10 | Output identifies BOTH correction events from the transcript — premature completion declaration AND wrong-path rule write — with verbatim or near-verbatim user quotes as evidence | PASS | Quote 1: "you haven't actually checked if the migration ran, please verify"; Quote 2: "the rule should have been global (`~/.claude/rules/`) because it applies across projects" |
| c11 | Output classifies the premature completion declaration as HIGH severity — verifying-before-declaring-done failures are repeated cause of customer-visible mistakes | PASS | "Correction 1: Premature Completion (HIGH severity)" explicit label in handoff |
| c12 | Output classifies the wrong-path assumption with explicit scope analysis — the assistant assumed project-level when global was correct, so the resulting learned rule must be scoped correctly (likely a global rule) | PASS | "Scope: Universal (the error pattern itself is cross-project)"; rule written to ~/.claude/rules/ |
| c13 | Output captures the API refactor success as a positive learning — the user's explicit 'good work' is non-obvious and worth reinforcing | PASS | Positive Learning section: "Category: Approach confirmation", "This is a non-obvious success worth noting" |
| c14 | Output writes Path 1 (local learned rule) for both high-severity corrections BEFORE any upstream PR proposal — the dual-path rule requires immediate local rules | PASS | Both rules confirmed in ~/.claude/rules/; no upstream PR step appears in the output at all |
| c15 | Output's learned-rule files use the convention `learned--<kebab-case-topic>.md` — e.g. `learned--verify-before-declaring-complete.md` and `learned--check-rule-scope-before-writing.md` | PASS | Exact filenames learned--verify-before-declaring-complete.md and learned--check-rule-scope-before-writing.md used throughout |
| c16 | Output places each learned rule in the correct scope — global rules in `~/.claude/rules/`, project rules in `.claude/rules/` — and the wrong-path-correction rule itself is global because it applies across projects | PASS | Both rules at /Users/martin/.claude/rules/ (global); wrong-path rule explicitly noted "Scope: Universal" |
| c17 | Output presents transcript metrics — turns, corrections, reversals, correction rate — with actual counts derived from the transcript, not estimates | PARTIAL | Reversals=0 in captured output, but test scenario stated "two approach reversals" and expected Reversals=1. Other counts (turns=5, corrections=2, rate=40%) correct. |
| c18 | Output's transcript file lookup uses the directory hash (working-path → hash) to locate the correct file in `~/.claude/projects/` — not assuming a fixed path | PASS | Explicit hash transformation shown: /private/var/folders/.../work → -private-var-folders-...-work in Transcript Lookup section |
| c19 | Output proposes regex patterns for correction phrases the analysis script's existing patterns missed — strengthening future automated detection | PARTIAL | Pattern `\byou haven't (actually )?checked\b` proposed in Pattern Evolution section with HIGH severity classification |

### Notes

Strong overall execution with all structural elements present and both corrections correctly extracted with quotes. The single notable failure is Reversals=0 when the scenario described two approach reversals (expected=1), and patterns.json write is unconfirmed in the artifacts.
