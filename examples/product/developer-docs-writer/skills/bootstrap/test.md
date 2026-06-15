# Test: developer-docs-writer/bootstrap scaffolds its content fragment safely

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/content/_sections/developer-docs-writer.md` fragment containing a user-authored section. The developer-docs-writer bootstrap skill should preserve that user content while appending the template's missing sections (with a merge marker). The skill writes only its own fragment under `docs/content/_sections/` — `docs/content/CLAUDE.md` is assembled later by the coordinator, so the three content writers never collide on it.

The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/content/_sections/developer-docs-writer.md` fragment is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.

Read the developer-docs-writer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/product/developer-docs-writer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.

After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Criteria

- [ ] PASS: After bootstrap, `docs/content/_sections/developer-docs-writer.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim
- [ ] PASS: After bootstrap, `docs/content/_sections/developer-docs-writer.md` contains the safe-merge marker `<!-- Merged from developer-docs-writer bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged
- [ ] PASS: After bootstrap, `docs/content/_sections/developer-docs-writer.md` contains the appended template sections — at minimum the "Diataxis Framework" and "API Documentation Standards" headings now appear alongside the preserved user content
- [ ] PASS: After bootstrap, `docs/content/_sections/developer-docs-writer.md` contains the "Available Developer Docs Skills" section listing at least one `/developer-docs-writer:` skill invocation path
- [ ] PASS: The skill did not create or write `docs/content/CLAUDE.md` — that file is the coordinator's to assemble from the `_sections/` fragments
- [ ] PASS: Chat output includes a manifest summary that lists `docs/content/_sections/developer-docs-writer.md` under "Files merged" (not "Files created") since the fragment already existed

## Output expectations

- [ ] PASS: Output names the merged fragment individually — a bare "bootstrap complete" without the per-file manifest is not enough
- [ ] PASS: Output does not claim it overwrote or replaced the fragment — the language reflects merge, not replacement
- [ ] PARTIAL: Output points the reader at next steps consistent with the skill's documented manifest (writing API docs, SDK guides, or setting up CI doc linting)
