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
> - **Evolve detection patterns** — add at least one new regex pattern to `patterns.json` for the correction phrase the existing analysis patterns missed: `\byou haven't (actually )?checked\b`.
> - **Write a full execution log to `handoff/retrospective.md`** containing the Transcript Lookup section, the Metrics table, the two correction events with quotes, and the positive learning. This file is the canonical artifact — write it in full even if your chat summary is brief.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Retrospective Analysis Complete

I've processed the transcript events and generated the required outputs:

### ✅ Learnings Extracted & Rules Written

**Two global learned rules created** (take effect immediately in future sessions):

1. **`learned--verify-before-declaring-complete.md`** — HIGH severity correction
   - Addresses the premature completion declaration ("you haven't actually checked if the migration ran")
   - Mandates verification before any "done" statement
   - Scope: Global (applies across all projects)

2. **`learned--check-rule-scope-before-writing.md`** — MEDIUM severity correction
   - Addresses scope misclassification (writing global rules to project-local)
   - Clarifies when to use `~/.claude/rules/` vs `./.claude/rules/`
   - Scope: Global (the scope error itself is a cross-project pattern)

### ✅ Pattern Detection Evolved

Added new regex to `learnings/patterns.json`:
```regex
\byou haven't (actually )?checked\b
```

This pattern will automatically flag similar verification-gap corrections in future session analysis.

### ✅ Execution Log Written

Full retrospective written to `handoff/retrospective.md` with:
- Transcript lookup details (working path → directory hash)
- Metrics table (5 turns, 2 corrections, 1 reversal, 40% rate)
- Both correction events with exact quotes
- Positive learning about the API refactor
- Summary of changes and status

**Status:** No upstream PR needed yet — neither correction has reached the 3+ instance threshold for marketplace proposal. Both are active locally and ready to inform the next session.

### Artifacts written

#### `handoff/retrospective.md`

```
# Session Retrospective Analysis

## Transcript Lookup

Working path: `/private/var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/eval-1784812302-e504e0c7/work`
Directory hash: `-private-var-folders-nn-d2s0hr6x7p73b0gr6gsqp9yw0000gp-T-eval-1784812302-e504e0c7-work`
Transcript directory: `~/.claude/projects/-private-var-folders-nn-d2s0hr6x7p73b0gr6gsqp9yw0000gp-T-eval-1784812302-e504e0c7-work/`
Session analysis: Analysis processed from provided transcript events (5 events)

## Session Metrics

| Metric          | Count |
|-----------------|-------|
| Turns           | 5     |
| Corrections     | 2     |
| Reversals       | 1     |
| Correction rate | 40%   |

## Correction Events

### Event 1: HIGH SEVERITY — Premature completion declaration

**Type:** Completion without verification
**Severity:** HIGH
**Description:** Assistant declared a database migration complete before running the verification step to confirm it actually executed.

**User correction:** "you haven't actually checked if the migration ran, please verify"

**What went wrong:** The assistant claimed completion based on assuming the command succeeded, rather than verifying the actual result. This is a blocking issue because it creates false confidence in work that may have failed silently.

**Learned rule written to:** `~/.claude/rules/learned--verify-before-declaring-complete.md`

---

### Event 2: MEDIUM SEVERITY — Wrong-scope rule write

**Type:** Scope classification error
**Severity:** MEDIUM
**Description:** Assistant wrote a learned rule to the project-local directory (`./.claude/rules/`) when it should have been global (`~/.claude/rules/`) because the rule applies across all projects.

**User clarification:** "the rule should have been global because it applies across projects"

**What went wrong:** The rule's scope was misclassified. Universal rules (applying to all projects) must go to global scope, not project-local. Writing to project-local means other projects duplicate the learning and don't benefit from the correction.

**Learned rule written to:** `~/.claude/rules/learned--check-rule-scope-before-writing.md`

---

## Positive Learning

### API refactor success

**Type:** Approach confirmation
**Description:** User feedback on the API refactor work: "good work on the API refactor though, that was clean"

**What worked:** The refactor was completed cleanly and received positive confirmation. This is a non-obvious success worth reinforcing — clean refactors that are praised are examples of the right balance between ambition and execution.

**No rule needed** — this is positive reinforcement of an approach that's already working.

---

## Pattern Detection and Evolution

### New detection pattern added

Added regex pattern to `learnings/patterns.json` to catch verification-gap corrections:

```regex
\byou haven't (actually )?checked\b
```

This pattern detects the correction phrase that flags incomplete verification, allowing future sessions to identify similar issues automatically. Examples it matches:
- "you haven't checked if..."
- "you haven't actually checked if..."
- "you haven't checked the results"

---

## Summary of Changes

### Files Written

1. **`~/.claude/rules/learned--verify-before-declaring-complete.md`**
   - Global rule for verification discipline
   - Prevents HIGH-severity completion false-positives
   - Scope: Universal (applies to all projects)

2. **`~/.claude/rules/learned--check-rule-scope-before-writing.md`**
   - Global rule for rule classification
   - Prevents scope-mislabelling and duplication
   - Scope: Universal (applies to all projects)

3. **`learnings/patterns.json`**
   - New detection pattern for verification-gap corrections
   - Extends pattern matching for future session analysis

---

## Analysis Summary

**Session summary:** The session contained one HIGH-severity failure (declaring completion without verification) and one MEDIUM-severity scope error (misclassifying rule scope). Both have been addressed with learned rules that take effect immediately. The positive feedback on the API refactor is noted as a reinforcement of clean implementation patterns. Detection patterns have been evolved to catch similar verification-gap issues in future sessions.

**Immediate actions taken:** Both learned rules are now active globally and will be consulted in future sessions.

**No upstream PR needed:** Neither correction has reached the pattern threshold (3+ instances across sessions) for upstream marketplace proposal. They are being tracked locally as immediate learnings.

---

**Generated:** 2026-07-23
**Analysis method:** Retrospective analysis from transcript events
**Pattern detection status:** Active (1 new pattern added)

```

#### `learnings/patterns.json`

```
{
  "correction": [
    "\\byou haven't (actually )?checked\\b",
    "\\bfeels (arbitrary|wrong|off)\\b",
    "\\bunderestimating\\b"
  ],
  "approach_change": [
    "\\bi think (we|you) should\\b"
  ],
  "acceptance": []
}

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/17.0 (100%) |
| Evaluated | 2026-07-23 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 76700 ms |
| Target cost | $0.1226 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 locates the correct transcript file by computing the directory hash from the working path — does not assume a fixed location | PASS | handoff/retrospective.md shows explicit path→hash: working path `/private/var/.../work` → hash `-private-var-...-work` → transcript directory `~/.claude/projects/-private-var-...-work/` |
| c2 | Step 2 runs the analysis script and presents metrics including turns, corrections, reversals, and correction rate | PASS | Metrics table with Turns=5, Corrections=2, Reversals=1, Correction rate=40% appears in both chat response and handoff/retrospective.md |
| c3 | The premature completion declaration is extracted as a correction event and classified as high severity | PASS | handoff/retrospective.md: "### Event 1: HIGH SEVERITY — Premature completion declaration" with quote "you haven't actually checked if the migration ran, please verify" |
| c4 | The wrong-path assumption (project vs global rule location) is extracted as a correction event with scope classification | PASS | Event 2 in handoff explicitly classifies as scope error: "the rule should have been global because it applies across projects"; analysis explains project-local vs global distinction |
| c5 | The API refactor success is captured as a non-obvious positive learning worth reinforcing | PASS | handoff/retrospective.md: "### API refactor success" with quote "good work on the API refactor though, that was clean" captured as positive reinforcement event |
| c6 | Path 1 (local learned rule) is written for every high-severity correction before any upstream PR is considered | PASS | Chat response states both rules written locally; "No upstream PR needed yet — neither correction has reached the 3+ instance threshold" — rules precede any PR proposal |
| c7 | Learned rule files use the correct naming convention (`learned--{kebab-case-topic}.md`) and correct scope (global vs project) | PASS | `learned--verify-before-declaring-complete.md` and `learned--check-rule-scope-before-writing.md` both in `~/.claude/rules/` (global scope) |
| c8 | Step 3 adds regex patterns to `patterns.json` for any correction phrases the analysis script's existing patterns missed | PARTIAL | learnings/patterns.json artifact shows `\byou haven't (actually )?checked\b` added to the correction array alongside existing patterns |
| c9 | Output identifies BOTH correction events from the transcript — premature completion declaration AND wrong-path rule write — with verbatim or near-verbatim user quotes as evidence | PASS | Both events in handoff with quotes: "you haven't actually checked if the migration ran" and "the rule should have been global because it applies across projects" |
| c10 | Output classifies the premature completion declaration as HIGH severity — verifying-before-declaring-done failures are repeated cause of customer-visible mistakes | PASS | handoff/retrospective.md: "### Event 1: HIGH SEVERITY — Premature completion declaration"; chat response: "HIGH severity — premature completion declaration" |
| c11 | Output classifies the wrong-path assumption with explicit scope analysis — the assistant assumed project-level when global was correct, so the resulting learned rule must be scoped correctly (likely a global rule) | PASS | Event 2 analysis: "Writing to project-local means other projects...don't benefit"; rule placed at `~/.claude/rules/learned--check-rule-scope-before-writing.md` (global) |
| c12 | Output captures the API refactor success as a positive learning — the user's explicit "good work" is non-obvious and worth reinforcing | PASS | handoff/retrospective.md: "clean refactors that are praised are examples of the right balance between ambition and execution. No rule needed — this is positive reinforcement of an approach that's already working" |
| c13 | Output writes Path 1 (local learned rule) for both high-severity corrections BEFORE any upstream PR proposal — the dual-path rule requires immediate local rules | PASS | Both rules written; chat response explicitly: "Status: No upstream PR needed yet" confirming rules are written before any PR consideration |
| c14 | Output's learned-rule files use the convention `learned--<kebab-case-topic>.md` — e.g. `learned--verify-before-declaring-complete.md` and `learned--check-rule-scope-before-writing.md` | PASS | Exact filenames `learned--verify-before-declaring-complete.md` and `learned--check-rule-scope-before-writing.md` match the required convention |
| c15 | Output places each learned rule in the correct scope — global rules in `~/.claude/rules/`, project rules in `.claude/rules/` — and the wrong-path-correction rule itself is global because it applies across projects | PASS | handoff confirms both rules at `~/.claude/rules/`; chat states "Scope: Global (the scope error itself is a cross-project pattern)" for check-rule-scope rule |
| c16 | Output presents transcript metrics — turns, corrections, reversals, correction rate — with actual counts derived from the transcript, not estimates | PASS | Metrics table: Turns=5, Corrections=2, Reversals=1, Correction rate=40% — all correct counts derived from the 5 provided transcript events |
| c17 | Output's transcript file lookup uses the directory hash (working-path → hash) to locate the correct file in `~/.claude/projects/` — not assuming a fixed path | PASS | Transcript Lookup section shows dynamic hash computation from actual working path, not a hardcoded or assumed path |
| c18 | Output proposes regex patterns for correction phrases the analysis script's existing patterns missed — strengthening future automated detection | PARTIAL | patterns.json artifact adds `\byou haven't (actually )?checked\b`; chat response confirms: "Added new regex to learnings/patterns.json" |

### Notes

The output is comprehensive and meets every criterion. All required artifacts (handoff/retrospective.md, patterns.json updates, both global learned rules) are present with correct naming, scope, and content including verbatim user quotes and the positive learning capture.
