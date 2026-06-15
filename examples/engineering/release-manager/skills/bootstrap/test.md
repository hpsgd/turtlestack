# Test: release-manager/bootstrap scaffolds docs/release safely

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/release/_sections/release-manager.md` fragment containing a user-authored section. The release-manager bootstrap skill should preserve that user content while appending the template's missing sections (with a merge marker), and should create the two files the fixture is missing — `CHANGELOG.md` (project root) and `docs/release/release-checklist.md`. The release-manager never writes `docs/release/CLAUDE.md` directly — the coordinator assembles it from the fragments in `_sections/`.

The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/release/_sections/release-manager.md` fragment is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.

Read the release-manager bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/engineering/release-manager/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.

After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Criteria

- [ ] PASS: After bootstrap, `docs/release/_sections/release-manager.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim
- [ ] PASS: After bootstrap, `docs/release/_sections/release-manager.md` contains the safe-merge marker `<!-- Merged from release-manager bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged
- [ ] PASS: After bootstrap, `docs/release/_sections/release-manager.md` contains the appended template sections — at minimum the "Semantic Versioning" and "Release Process" headings now appear alongside the preserved user content
- [ ] PASS: The release-manager fragment is authored at H2 and below — it does not introduce a `# Release Domain` H1 (the coordinator generates that when it assembles `docs/release/CLAUDE.md`)
- [ ] PASS: The skill does NOT write `docs/release/CLAUDE.md` directly — that file is the coordinator's to assemble from `_sections/`
- [ ] PASS: After bootstrap, `CHANGELOG.md` exists at the project root and was created from the skill's template (contains `## [Unreleased]` and the standard Keep a Changelog categories)
- [ ] PASS: After bootstrap, `docs/release/release-checklist.md` exists and was created from the skill's template (contains a `## Go/No-Go Decision` section and the participant sign-off table)
- [ ] PASS: Chat output includes a manifest summary that distinguishes files created (`CHANGELOG.md`, `release-checklist.md`) from files merged (`_sections/release-manager.md`)

## Output expectations

- [ ] PASS: Output names each created and merged file individually — a bare "bootstrap complete" without the per-file manifest is not enough
- [ ] PASS: Output does not claim it overwrote or replaced `docs/release/_sections/release-manager.md` — the language reflects merge, not replacement
- [ ] PARTIAL: Output points the reader at next steps (using `/release-manager:release-plan`, customising checklist participants, setting up GitHub Actions release workflow) consistent with the skill's documented manifest
