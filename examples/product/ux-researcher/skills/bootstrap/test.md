# Test: ux-researcher/bootstrap scaffolds docs/design safely

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/design/_sections/ux-researcher.md` fragment containing a user-authored section. The ux-researcher bootstrap skill should preserve that user content while appending the UX research conventions (with a merge marker), and should create the two template files the fixture is missing — `persona-template.md` and `journey-map-template.md`. `docs/design/CLAUDE.md` itself is assembled by the coordinator from the fragments in `_sections/`, so this skill never writes it.

The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/design/_sections/ux-researcher.md` fragment is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.

Read the ux-researcher bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/product/ux-researcher/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.

After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Criteria

- [ ] PASS: After bootstrap, `docs/design/_sections/ux-researcher.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim
- [ ] PASS: After bootstrap, `docs/design/_sections/ux-researcher.md` contains the merge marker `<!-- Merged from ux-researcher bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged
- [ ] PASS: After bootstrap, `docs/design/_sections/ux-researcher.md` contains the appended UX research sections — at minimum the `## UX Research` heading and `### Persona Format` heading now appear alongside the preserved user content
- [ ] PASS: The fragment `docs/design/_sections/ux-researcher.md` starts at an H2 (`##`) heading — it carries no `# Design Domain` H1, since the coordinator generates that when assembling `docs/design/CLAUDE.md`
- [ ] PASS: After bootstrap, `docs/design/persona-template.md` exists and was copied from the plugin template (contains `# Persona Card` heading and `## Evidence base` section)
- [ ] PASS: After bootstrap, `docs/design/journey-map-template.md` exists and was copied from the plugin template (contains `# Journey Map` heading and `## Scope` section)
- [ ] PASS: Chat output includes a manifest summary that distinguishes files created (`persona-template.md`, `journey-map-template.md`, `_sections/ux-researcher.md`) from files merged

## Output expectations

- [ ] PASS: Output names each created and merged file individually — a bare "bootstrap complete" without the per-file manifest is not enough
- [ ] PASS: Output does not claim it overwrote or replaced the `docs/design/_sections/ux-researcher.md` fragment — the language reflects merge or append, not replacement
- [ ] PARTIAL: Output points the reader at next steps (using persona-definition and journey-map skills) consistent with the skill's documented manifest
