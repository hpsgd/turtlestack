# Test: bootstrap scaffolds the coaching documentation structure

Scenario: A coach is onboarding to a new team and needs the `docs/coaching/` structure created from scratch — domain CLAUDE.md, working-agreements starter, and DoD starter — without the skill authoring the team's actual agreements or DoD content.

## Prompt

Use the agile-coach `bootstrap` skill to bootstrap the agile-coaching documentation structure for the "billing" team. Create the structure under `docs/coaching/` in the current working directory (a fresh git repo — nothing exists there yet). Respond in the skill's standard manifest output format.

Proceed without asking — there is no existing coaching documentation; this is a clean bootstrap.

## Criteria

- [ ] PASS: Creates the `docs/coaching/` directory with a `retrospectives/` subdirectory for per-retro outputs
- [ ] PASS: Creates `docs/coaching/CLAUDE.md` as a domain conventions file that names the coach-owns-structure / team-owns-content boundary
- [ ] PASS: The domain CLAUDE.md lists the available agile-coach skills as a reference for a future coach orienting to the repo
- [ ] PASS: Creates a working-agreements starter file and a definition-of-done starter file under `docs/coaching/`
- [ ] PASS: The skill does NOT author actual working agreements or DoD criteria — it creates structure and starter prompts only, leaving the team to fill them in
- [ ] PASS: Output is a bootstrap manifest listing files created (and any merged), plus next steps pointing to design-working-agreements and team-health-scan
- [ ] PARTIAL: The DoD starter and CLAUDE.md note that content is team-owned and specific/testable, not handed down by management

## Output expectations

- [ ] PASS: Output names the files it created at their paths under `docs/coaching/` — CLAUDE.md, working-agreements, definition-of-done — not just a vague "done"
- [ ] PASS: The created `docs/coaching/CLAUDE.md` records the convention that every retro produces action items with an owner and a due sprint
- [ ] PASS: The created files contain placeholder/template content (e.g. bracketed prompts, checkbox stubs) rather than invented team-specific agreements or quality criteria
- [ ] PASS: Output's next-steps point the user at the skills that fill the structure (design-working-agreements, team-health-scan) rather than declaring the team's process complete
- [ ] PARTIAL: Output reflects an idempotent / safe-merge intent — it states it would merge missing sections rather than overwrite if files already existed
