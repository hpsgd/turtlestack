# Test: internal-docs-writer/bootstrap merges docs/content/CLAUDE.md safely

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/content/CLAUDE.md` containing a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`. The internal-docs-writer bootstrap skill should preserve that user content while appending the template's internal documentation sections (with a merge marker), and output a manifest listing the merged file and next steps.

The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/content/CLAUDE.md` is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.

Read the internal-docs-writer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/product/internal-docs-writer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.

After the bootstrap completes, output the manifest summary the skill defines (files merged, next steps).

## Criteria

- [ ] PASS: After bootstrap, `docs/content/CLAUDE.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim
- [ ] PASS: After bootstrap, `docs/content/CLAUDE.md` contains the safe-merge marker `<!-- Merged from internal-docs-writer bootstrap v0.1.0 -->` — missing sections were appended, not silently merged
- [ ] PASS: After bootstrap, `docs/content/CLAUDE.md` contains the appended template sections — at minimum the "Runbook Conventions" and "Post-Mortem Template" headings now appear alongside the preserved user content
- [ ] PASS: After bootstrap, `docs/content/CLAUDE.md` contains the "Internal Docs Conventions" section — confirming the full template was appended, not just a partial fragment
- [ ] PASS: Chat output includes a manifest that names `docs/content/CLAUDE.md` as a merged file, consistent with the skill's documented manifest shape

## Output expectations

- [ ] PASS: Output names `docs/content/CLAUDE.md` individually — a bare "bootstrap complete" without the per-file listing is not enough
- [ ] PASS: Output does not claim it overwrote or replaced `docs/content/CLAUDE.md` — the language reflects merge or append, not replacement
- [ ] PARTIAL: Output points the reader at next steps referencing at least one `/internal-docs-writer:*` skill, consistent with the skill's documented manifest
