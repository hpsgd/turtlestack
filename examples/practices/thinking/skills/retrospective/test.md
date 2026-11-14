# Test: retrospective turns session lessons into the right kind of rule

Scenario: At the end of a piece of work, the user runs a retrospective over the session. The session held one cross-project correction, one project-specific correction, a confirmed success, and an iterative re-edit that was not a mistake.

## Prompt

/retrospective current

Treat the events below as the current session's contents. Process them as real, not hypothetical.

1. Assistant declared a database migration complete before running the verification step.
2. User corrected: "you haven't actually checked if the migration ran, please verify"
3. Assistant assumed the app config lived at `config/index.ts`; user corrected: "it's `src/config.ts` in this repo".
4. Assistant edited `docs/plan.md` four times during a planned multi-pass rewrite the user had asked for.
5. Session ended with the user saying: "good work bundling the refactor into one PR, that was the right call"

Sandbox state (substitute for real ls/find results):

```
$GLOBAL_RULES_DIR (~/.claude/rules/)   → learned--verify-before-declaring-complete.md already exists (covers "declare done before verifying")
$RULES_DIR (.claude/rules/)             → no learned rules
Marketplace rules installed             → turtlestack--coding-standards--*--ai-steering.md includes "Never assert without verification"
```

## Criteria

- [ ] PASS: Event 1-2 is classified as a high-severity correction, and the skill finds the existing global learned rule and the marketplace rule rather than writing a duplicate
- [ ] PASS: Event 3 is treated as a project-specific fact (left to auto memory or a project note), not written as a global rule
- [ ] PASS: Event 4 is recognised as planned iteration, not a reversal
- [ ] PASS: Event 5 is recorded as a confirmed non-default success
- [ ] PASS: Output uses the defined format: lessons table with a Home column, rules written or updated, upstream candidates
- [ ] PARTIAL: Skill flags the overlap between the existing learned rule and the marketplace rule as a `/thinking:reconcile-rules` candidate

## Output expectations

- [ ] PASS: No new `learned--*.md` file is created for the verification lesson; the output says the existing rule already covers it
- [ ] PASS: The lessons table has four rows (events 1-2 combined, 3, 4, 5), each with a Home value
- [ ] PASS: Output does not produce session metrics (turn counts, correction rates); this skill no longer computes them
- [ ] PARTIAL: Output names `src/config.ts` as the fact for auto memory rather than inventing a rule like "always check src/ for config"
