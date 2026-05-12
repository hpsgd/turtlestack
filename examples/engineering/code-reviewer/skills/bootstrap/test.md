# Test: code-reviewer/bootstrap scaffolds docs/code-review safely

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/code-review/CLAUDE.md` containing a user-authored section. The code-reviewer bootstrap skill should preserve that user content while appending the template's missing sections (with a merge marker), and should create the two files the fixture is missing — `review-checklist.md` and `pr-template.md`.

The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/code-review/CLAUDE.md` is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.

Read the code-reviewer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/engineering/code-reviewer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.

After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, detected languages, existing PR template status, next steps).

## Criteria

- [ ] PASS: After bootstrap, `docs/code-review/CLAUDE.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim
- [ ] PASS: After bootstrap, `docs/code-review/CLAUDE.md` contains the safe-merge marker `<!-- Merged from code-reviewer bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged
- [ ] PASS: After bootstrap, `docs/code-review/CLAUDE.md` contains both the `## Review pass order` and `## Quality scoring` headings — the template's language-independent content was appended
- [ ] PASS: After bootstrap, `docs/code-review/review-checklist.md` exists and contains the `# Review checklist` heading
- [ ] PASS: After bootstrap, `docs/code-review/pr-template.md` exists and contains `Suggested content for` — indicating it was created from the skill's template
- [ ] PASS: Chat output includes a manifest summary that distinguishes files created (`review-checklist.md`, `pr-template.md`) from files merged (`CLAUDE.md`)
- [ ] PASS: Output names each file individually — a bare "bootstrap complete" without the per-file manifest is not enough
- [ ] PASS: Output does not claim it overwrote or replaced `docs/code-review/CLAUDE.md` — the language reflects merge, not replacement

## Output expectations

- [ ] PARTIAL: Output includes next steps (e.g. removing unused language sections, configuring SonarCloud, using `/code-reviewer:code-review`) consistent with the skill's documented manifest
