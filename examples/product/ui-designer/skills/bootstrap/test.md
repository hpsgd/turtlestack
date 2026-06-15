# Test: ui-designer/bootstrap scaffolds docs/design safely

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/design/_sections/ui-designer.md` fragment containing a user-authored section. The ui-designer bootstrap skill should preserve that user content while appending the template's missing sections (with a merge marker), and should create the file the fixture is missing — `docs/design/design-tokens.md` — copied from the plugin template. `docs/design/CLAUDE.md` itself is assembled by the coordinator from the fragments in `_sections/`, so this skill never writes it.

The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/design/_sections/ui-designer.md` fragment is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.

Read the ui-designer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/product/ui-designer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.

After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Criteria

- [ ] PASS: After bootstrap, `docs/design/_sections/ui-designer.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim
- [ ] PASS: After bootstrap, `docs/design/_sections/ui-designer.md` contains the safe-merge marker `<!-- Merged from ui-designer bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged
- [ ] PASS: After bootstrap, `docs/design/_sections/ui-designer.md` contains the appended template sections — at minimum the "Design Token Architecture" and "WCAG 2.2 Accessibility Requirements" headings now appear alongside the preserved user content
- [ ] PASS: The fragment `docs/design/_sections/ui-designer.md` starts at an H2 (`##`) heading — it carries no `# Design Domain` H1, since the coordinator generates that when assembling `docs/design/CLAUDE.md`
- [ ] PASS: After bootstrap, `docs/design/design-tokens.md` exists and was created from the plugin template (contains `## Colour Primitives` and `## Semantic Colour Tokens` headings)
- [ ] PASS: Chat output includes a manifest summary that distinguishes files created (`design-tokens.md`) from files merged (`_sections/ui-designer.md`)

## Output expectations

- [ ] PASS: Output names each created and merged file individually — a bare "bootstrap complete" without the per-file manifest is not enough
- [ ] PASS: Output does not claim it overwrote or replaced the `docs/design/_sections/ui-designer.md` fragment — the language reflects merge, not replacement
- [ ] PARTIAL: Output points the reader at next steps (populating `design-tokens.md`, using `/ui-designer:component-spec`) consistent with the skill's documented manifest
