# Test: devops/bootstrap scaffolds docs/infrastructure safely

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/infrastructure/_sections/devops.md` fragment containing a user-authored section. The devops bootstrap skill should preserve that user content while appending the template's missing sections (with a merge marker), and should create the two files the fixture is missing — `slo-definition.md` and `runbook-template.md`. The devops skill never writes `docs/infrastructure/CLAUDE.md` directly — the coordinator assembles it from the fragments in `_sections/`.

The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/infrastructure/_sections/devops.md` fragment is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.

Read the devops bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/engineering/devops/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.

After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Criteria

- [ ] PASS: After bootstrap, `docs/infrastructure/_sections/devops.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim
- [ ] PASS: After bootstrap, `docs/infrastructure/_sections/devops.md` contains the safe-merge marker `<!-- Merged from devops bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged
- [ ] PASS: After bootstrap, `docs/infrastructure/_sections/devops.md` contains the appended template sections — at minimum the "SLO/SLI Conventions" and "GitHub Actions Pipeline Standards" headings now appear alongside the preserved user content
- [ ] PASS: The devops fragment is authored at H2 and below — it does not introduce a `# Infrastructure Domain` H1 (the coordinator generates that when it assembles `docs/infrastructure/CLAUDE.md`)
- [ ] PASS: The skill does NOT write `docs/infrastructure/CLAUDE.md` directly — that file is the coordinator's to assemble from `_sections/`
- [ ] PASS: After bootstrap, `docs/infrastructure/slo-definition.md` exists and was created from the skill's template (contains a `## SLIs and SLOs` heading)
- [ ] PASS: After bootstrap, `docs/infrastructure/runbook-template.md` exists and was created from the skill's template (contains a `## Symptoms` heading and a `## Resolution` heading)
- [ ] PASS: Chat output includes a manifest summary that distinguishes files created (`slo-definition.md`, `runbook-template.md`) from files merged (`_sections/devops.md`)

## Output expectations

- [ ] PASS: Output names each created and merged file individually — a bare "bootstrap complete" without the per-file manifest is not enough
- [ ] PASS: Output does not claim it overwrote or replaced `docs/infrastructure/_sections/devops.md` — the language reflects merge, not replacement
- [ ] PARTIAL: Output points the reader at next steps (creating SLO definitions per service using `/devops:write-slo`, setting up pipelines using `/devops:write-pipeline`) consistent with the skill's documented manifest
