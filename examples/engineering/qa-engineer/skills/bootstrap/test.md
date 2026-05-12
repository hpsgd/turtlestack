# Test: qa-engineer/bootstrap scaffolds docs/testing safely

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a `pyproject.toml` (marking it as a Python project) and a partial `docs/testing/CLAUDE.md` containing a user-authored section. The qa-engineer bootstrap skill should detect Python, preserve the user content while appending missing sections (with a merge marker), and create the two new files — `docs/testing/test-config.md` and `docs/testing/ci-test-jobs.md` — filtered to Python only.

The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A `pyproject.toml` is present at the root. A partial `docs/testing/CLAUDE.md` is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.

Read the qa-engineer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/engineering/qa-engineer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.

After the bootstrap completes, output the manifest summary the skill defines (detected languages, files created, files merged, next steps).

## Criteria

- [ ] PASS: After bootstrap, `docs/testing/CLAUDE.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim
- [ ] PASS: After bootstrap, `docs/testing/CLAUDE.md` contains the safe-merge marker `<!-- Merged from qa-engineer bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged
- [ ] PASS: After bootstrap, `docs/testing/CLAUDE.md` contains the appended template sections — at minimum the "Runner commands" and "Evidence requirements" headings now appear alongside the preserved user content
- [ ] PASS: After bootstrap, `docs/testing/test-config.md` exists and contains the `## Python (pytest)` section (language filtering matched `pyproject.toml`)
- [ ] PASS: After bootstrap, `docs/testing/test-config.md` does NOT contain `## C# (xUnit)` — language filtering excluded C# because no `.csproj` or `.sln` was detected
- [ ] PASS: After bootstrap, `docs/testing/ci-test-jobs.md` exists and contains the `## Python` CI job
- [ ] PASS: Chat output's manifest summary includes a "Detected languages" section naming Python

## Output expectations

- [ ] PASS: Output names each created and merged file individually — a bare "bootstrap complete" without the per-file manifest is not enough
- [ ] PASS: Output does not claim it overwrote or replaced `docs/testing/CLAUDE.md` — the language reflects merge, not replacement
- [ ] PARTIAL: Output points the reader at next steps consistent with the skill's documented manifest (reviewing config templates, adding CI jobs, using `/qa-engineer:generate-tests`)
