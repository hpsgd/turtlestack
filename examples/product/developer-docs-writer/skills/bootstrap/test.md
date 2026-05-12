# Test: developer-docs-writer/bootstrap scaffolds docs/content safely

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/content/CLAUDE.md` containing a user-authored section. The developer-docs-writer bootstrap skill should preserve that user content while appending the template's missing sections (with a merge marker). Unlike the architect bootstrap, this skill creates only one file — the CLAUDE.md domain guide.

The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/content/CLAUDE.md` is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.

Read the developer-docs-writer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/product/developer-docs-writer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.

After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Criteria

- [ ] PASS: After bootstrap, `docs/content/CLAUDE.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim
- [ ] PASS: After bootstrap, `docs/content/CLAUDE.md` contains the safe-merge marker `<!-- Merged from developer-docs-writer bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged
- [ ] PASS: After bootstrap, `docs/content/CLAUDE.md` contains the appended template sections — at minimum the "Diataxis Framework" and "API Documentation Standards" headings now appear alongside the preserved user content
- [ ] PASS: After bootstrap, `docs/content/CLAUDE.md` contains the "Available Developer Docs Skills" section listing at least one `/developer-docs-writer:` skill invocation path
- [ ] PASS: Chat output includes a manifest summary that lists `docs/content/CLAUDE.md` under "Files merged" (not "Files created") since the file already existed

## Output expectations

- [ ] PASS: Output names the merged file individually — a bare "bootstrap complete" without the per-file manifest is not enough
- [ ] PASS: Output does not claim it overwrote or replaced `docs/content/CLAUDE.md` — the language reflects merge, not replacement
- [ ] PARTIAL: Output points the reader at next steps consistent with the skill's documented manifest (writing API docs, SDK guides, or setting up CI doc linting)
