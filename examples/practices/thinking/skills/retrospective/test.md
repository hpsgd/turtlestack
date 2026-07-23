# Test: retrospective session analysis with corrections

Scenario: At the start of a new session, the retrospective skill analyses the previous session's transcript where the assistant made two approach reversals and received one explicit correction about file location assumptions.

## Prompt

/retrospective latest

The "previous session" transcript to analyse is the events described below — treat these as the actual transcript contents the skill is processing. Process them as real, not hypothetical. Do NOT skip events because no `.jsonl` file is found; the events listed here ARE the transcript.

Transcript events (process these as the previous session):

1. Assistant declared a database migration complete before running the verification step.
2. User corrected: "you haven't actually checked if the migration ran, please verify"
3. Assistant then wrote a local learned-rule file to the wrong path — assumed project-level (`./.claude/rules/`) when the rule was global in scope.
4. User clarified: the rule should have been global (`~/.claude/rules/`) because it applies across projects.
5. Session ended with user saying: "good work on the API refactor though, that was clean"

Execution requirements (the retrospective output MUST include all of this):

- **Transcript Lookup section** at the top showing the working path → directory-hash transformation explicitly:
  ```
  Working path: /Users/martin/Projects/turtlestack
  Directory hash: -Users-martin-Projects-turtlestack
  Transcript directory: ~/.claude/projects/-Users-martin-Projects-turtlestack/
  Latest transcript: <session-uuid>.jsonl
  ```
  Do NOT assume a fixed path. If the actual `.jsonl` file is not accessible, treat the 5 transcript events above as the session contents and proceed — do not abort or label the analysis hypothetical.
- **Metrics table** with four discrete integer rows:
  ```
  | Metric          | Count |
  |-----------------|-------|
  | Turns           | 5     |
  | Corrections     | 2     |
  | Reversals       | 1     |
  | Correction rate | 40%   |
  ```
  Reversals are separate from corrections (a reversal is the assistant changing its approach after pushback).
- **Two correction events extracted** — both must appear as real entries in the events list (NOT in a hypothetical block):
  - Event 1: HIGH severity — premature completion declaration. Quote: "you haven't actually checked if the migration ran, please verify".
  - Event 2: scope-classification correction — wrong-path rule write. Quote the user's clarification about global vs project scope.
- **One positive learning extracted** — the API refactor success ("good work on the API refactor though, that was clean") captured as a positive-reinforcement event worth keeping.
- **Path 1 (local learned rule files)** written for BOTH high-severity corrections BEFORE any upstream PR proposal:
  - Global rule: `~/.claude/rules/learned--verify-before-declaring-complete.md`
  - Global rule: `~/.claude/rules/learned--check-rule-scope-before-writing.md` (global because the wrong-scope problem itself is cross-project)
  Use the `learned--<kebab-case-topic>.md` naming convention.
- **Evolve detection patterns** — add at least one new regex pattern to `patterns.json` for the correction phrase the existing analysis patterns missed: `\byou haven't (actually )?checked\b`.
- **Write a full execution log to `handoff/retrospective.md`** containing the Transcript Lookup section, the Metrics table, the two correction events with quotes, and the positive learning. This file is the canonical artifact — write it in full even if your chat summary is brief.

## Criteria

- [ ] PASS: Step 1 locates the correct transcript file by computing the directory hash from the working path — does not assume a fixed location
- [ ] PASS: Step 2 runs the analysis script and presents metrics including turns, corrections, reversals, and correction rate
- [ ] PASS: The premature completion declaration is extracted as a correction event and classified as high severity
- [ ] PASS: The wrong-path assumption (project vs global rule location) is extracted as a correction event with scope classification
- [ ] PASS: The API refactor success is captured as a non-obvious positive learning worth reinforcing
- [ ] PASS: Path 1 (local learned rule) is written for every high-severity correction before any upstream PR is considered
- [ ] PASS: Learned rule files use the correct naming convention (`learned--{kebab-case-topic}.md`) and correct scope (global vs project)
- [ ] PARTIAL: Step 3 adds regex patterns to `patterns.json` for any correction phrases the analysis script's existing patterns missed

## Output expectations

- [ ] PASS: Output identifies BOTH correction events from the transcript — premature completion declaration AND wrong-path rule write — with verbatim or near-verbatim user quotes as evidence
- [ ] PASS: Output classifies the premature completion declaration as HIGH severity — verifying-before-declaring-done failures are repeated cause of customer-visible mistakes
- [ ] PASS: Output classifies the wrong-path assumption with explicit scope analysis — the assistant assumed project-level when global was correct, so the resulting learned rule must be scoped correctly (likely a global rule)
- [ ] PASS: Output captures the API refactor success as a positive learning — the user's explicit "good work" is non-obvious and worth reinforcing
- [ ] PASS: Output writes Path 1 (local learned rule) for both high-severity corrections BEFORE any upstream PR proposal — the dual-path rule requires immediate local rules
- [ ] PASS: Output's learned-rule files use the convention `learned--<kebab-case-topic>.md` — e.g. `learned--verify-before-declaring-complete.md` and `learned--check-rule-scope-before-writing.md`
- [ ] PASS: Output places each learned rule in the correct scope — global rules in `~/.claude/rules/`, project rules in `.claude/rules/` — and the wrong-path-correction rule itself is global because it applies across projects
- [ ] PASS: Output presents transcript metrics — turns, corrections, reversals, correction rate — with actual counts derived from the transcript, not estimates
- [ ] PASS: Output's transcript file lookup uses the directory hash (working-path → hash) to locate the correct file in `~/.claude/projects/` — not assuming a fixed path
- [ ] PARTIAL: Output proposes regex patterns for correction phrases the analysis script's existing patterns missed — strengthening future automated detection
