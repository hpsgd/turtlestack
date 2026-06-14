# Test: dotnet-developer/bootstrap writes its architecture fragment safely

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/architecture/_sections/dotnet-developer.md` fragment containing a user-authored section. The dotnet-developer bootstrap skill should preserve that user content while appending the .NET Conventions section (with a merge marker). It writes only its own fragment — `docs/architecture/CLAUDE.md` is assembled by the coordinator from the fragments in `_sections/`, so this skill never touches it.

The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/architecture/_sections/dotnet-developer.md` fragment is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`. There is no `.NET Conventions` section yet.

Read the dotnet-developer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/engineering/dotnet-developer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.

After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Criteria

- [ ] PASS: After bootstrap, `docs/architecture/_sections/dotnet-developer.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim
- [ ] PASS: After bootstrap, `docs/architecture/_sections/dotnet-developer.md` contains the safe-merge marker `<!-- Added by dotnet-developer bootstrap v0.1.0 -->` — the .NET Conventions section was appended with the correct marker
- [ ] PASS: After bootstrap, `docs/architecture/_sections/dotnet-developer.md` contains the `.NET Conventions` heading — the section was appended to the fragment
- [ ] PASS: After bootstrap, `docs/architecture/_sections/dotnet-developer.md` contains sub-sections for Wolverine and Marten conventions — the technology-specific content was included
- [ ] PASS: After bootstrap, `docs/architecture/_sections/dotnet-developer.md` contains a Testing sub-section mentioning Alba and xUnit — the testing conventions were included
- [ ] PASS: After bootstrap, `docs/architecture/_sections/dotnet-developer.md` contains the Available .NET Skills table referencing `/dotnet-developer:write-endpoint` and `/dotnet-developer:write-handler`
- [ ] PASS: Chat output includes a manifest summary with a "Files created" or equivalent section listing `docs/architecture/_sections/dotnet-developer.md`
- [ ] PASS: The skill did NOT write `docs/architecture/CLAUDE.md` and did NOT create any new domain directory — that file is coordinator-assembled, and the skill writes only its own fragment under `_sections/`

## Output expectations

- [ ] PASS: Output names the written fragment explicitly — a bare "bootstrap complete" without listing `docs/architecture/_sections/dotnet-developer.md` is not enough
- [ ] PASS: Output does not claim it overwrote or replaced `docs/architecture/_sections/dotnet-developer.md` — the language reflects append/merge, not replacement
- [ ] PARTIAL: Output points the reader at next steps consistent with the skill's documented manifest — at minimum mentions configuring Wolverine and Marten or using the available skills
