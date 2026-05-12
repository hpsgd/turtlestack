# Test: user-docs-writer/bootstrap scaffolds docs/content safely

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/content/CLAUDE.md` containing a user-authored section. The user-docs-writer bootstrap skill should preserve that user content while appending the missing user-documentation sections (with a merge marker). Unlike the architect bootstrap, this skill manages only one file — `docs/content/CLAUDE.md` — so the test focuses on the safe-merge contract and the manifest output.

The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/content/CLAUDE.md` is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.

Read the user-docs-writer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/product/user-docs-writer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.

After the bootstrap completes, output the manifest summary the skill defines (files merged, next steps).

## Criteria

- [ ] PASS: After bootstrap, `docs/content/CLAUDE.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim
- [ ] PASS: After bootstrap, `docs/content/CLAUDE.md` contains the safe-merge marker `<!-- Merged from user-docs-writer bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged
- [ ] PASS: After bootstrap, `docs/content/CLAUDE.md` contains the appended user-docs sections — at minimum the `## User Documentation` heading and the `### User Guide Conventions` heading now appear alongside the preserved user content
- [ ] PASS: After bootstrap, `docs/content/CLAUDE.md` contains the `### KB Article Structure` section, which defines the KB article template
- [ ] PASS: After bootstrap, `docs/content/CLAUDE.md` contains the `### Available User Docs Skills` section listing the four skill slash commands

## Output expectations

- [ ] PASS: Output includes a manifest summary with a "Files merged" section naming `docs/content/CLAUDE.md`
- [ ] PASS: Output does not claim it overwrote or replaced `docs/content/CLAUDE.md` — the language reflects merge or append, not replacement
- [ ] PARTIAL: Output points the reader at next steps referencing at least two of the three skills (`write-onboarding`, `write-kb-article`, `content-strategy`) consistent with the skill's documented manifest
