# Test: qa-lead/bootstrap scaffolds docs/quality safely

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/quality/_sections/qa-lead.md` fragment containing a user-authored section. The qa-lead bootstrap skill should preserve that user content while appending the template's missing sections (with a merge marker), and should create the four files the fixture is missing — `test-strategy.md`, `definition-of-ready.md`, `definition-of-done.md`, and `quality-gates.md`. The qa-lead never writes `docs/quality/CLAUDE.md` directly — the coordinator assembles it from the fragments in `_sections/`.

The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/quality/_sections/qa-lead.md` fragment is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.

Read the qa-lead bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/engineering/qa-lead/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.

After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Criteria

- [ ] PASS: After bootstrap, `docs/quality/_sections/qa-lead.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim
- [ ] PASS: After bootstrap, `docs/quality/_sections/qa-lead.md` contains the safe-merge marker `<!-- Merged from qa-lead bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged
- [ ] PASS: After bootstrap, `docs/quality/_sections/qa-lead.md` contains the appended template sections — at minimum the "Test Pyramid" and "BDD Conventions" headings now appear alongside the preserved user content
- [ ] PASS: The qa-lead fragment is authored at H2 and below — it does not introduce a `# Quality Domain` H1 (the coordinator generates that when it assembles `docs/quality/CLAUDE.md`)
- [ ] PASS: The skill does NOT write `docs/quality/CLAUDE.md` directly — that file is the coordinator's to assemble from `_sections/`
- [ ] PASS: After bootstrap, all four template files exist: `docs/quality/test-strategy.md`, `docs/quality/definition-of-ready.md`, `docs/quality/definition-of-done.md`, and `docs/quality/quality-gates.md`
- [ ] PASS: The created `docs/quality/test-strategy.md` contains the `## 2. Test Levels` heading and references "TestProject" in its title (placeholder was substituted)
- [ ] PASS: The created `docs/quality/quality-gates.md` contains gate definitions — at minimum the "Gate 1: PR Merge" section heading
- [ ] PASS: Chat output includes a manifest summary that distinguishes files created (the four templates) from files merged (`_sections/qa-lead.md`)

## Output expectations

- [ ] PASS: Output names each created and merged file individually — a bare "bootstrap complete" without the per-file manifest is not enough
- [ ] PASS: Output does not claim it overwrote or replaced `docs/quality/_sections/qa-lead.md` — the language reflects merge, not replacement
- [ ] PARTIAL: Output points the reader at next steps (filling in `test-strategy.md`, customising thresholds in `quality-gates.md`, or using `/qa-lead:test-strategy`) consistent with the skill's documented manifest
