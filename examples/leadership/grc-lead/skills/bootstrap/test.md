# Test: grc-lead/bootstrap scaffolds docs/governance safely

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/governance/_sections/grc-lead.md` fragment containing a user-authored section. The grc-lead bootstrap skill should preserve that user content while appending the template's missing sections (with a merge marker), and should create the three files the fixture is missing — `risk-register.md`, `compliance-checklist.md`, and `ai-governance-policy.md`. The grc-lead never writes `docs/governance/CLAUDE.md` directly — the coordinator assembles it from the fragments in `_sections/`.

The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/governance/_sections/grc-lead.md` fragment is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.

Read the grc-lead bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/leadership/grc-lead/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.

After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Criteria

- [ ] PASS: After bootstrap, `docs/governance/_sections/grc-lead.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim
- [ ] PASS: After bootstrap, `docs/governance/_sections/grc-lead.md` contains the safe-merge marker `<!-- Merged from grc-lead bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged
- [ ] PASS: After bootstrap, `docs/governance/_sections/grc-lead.md` contains the appended template sections — at minimum the "Risk Management (ISO 31000)" and "Compliance Frameworks" headings now appear alongside the preserved user content
- [ ] PASS: The grc-lead fragment is authored at H2 and below — it does not introduce a `# Governance Domain` H1 (the coordinator generates that when it assembles `docs/governance/CLAUDE.md`)
- [ ] PASS: The skill does NOT write `docs/governance/CLAUDE.md` directly — that file is the coordinator's to assemble from `_sections/`
- [ ] PASS: After bootstrap, `docs/governance/risk-register.md` exists and was created from the skill's template (contains an "Active Risks" table with column headers)
- [ ] PASS: After bootstrap, `docs/governance/compliance-checklist.md` exists and was created from the skill's template (contains a "Framework Applicability" table)
- [ ] PASS: After bootstrap, `docs/governance/ai-governance-policy.md` exists and was created from the skill's template (contains an "AI System Inventory" table and "Principles" section)
- [ ] PASS: Chat output includes a manifest summary headed `## GRC Lead Bootstrap Complete` that distinguishes files created from files merged

## Output expectations

- [ ] PASS: Output names each created and merged file individually — a bare "bootstrap complete" without the per-file manifest is not enough
- [ ] PASS: Output does not claim it overwrote or replaced `docs/governance/_sections/grc-lead.md` — the language reflects merge, not replacement
- [ ] PARTIAL: Output points the reader at next steps (conducting a risk assessment, determining applicable compliance frameworks, classifying AI systems) consistent with the skill's documented manifest
