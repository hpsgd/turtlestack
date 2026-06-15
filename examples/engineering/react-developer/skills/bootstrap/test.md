# Test: react-developer/bootstrap writes its architecture fragment safely

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/architecture/_sections/react-developer.md` fragment containing a user-authored section. The react-developer bootstrap skill should preserve that user content while appending the React/Next.js Conventions section (with a merge marker). It writes only its own fragment — `docs/architecture/CLAUDE.md` is assembled by the coordinator from the fragments in `_sections/`, so this skill never touches it.

The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/architecture/_sections/react-developer.md` fragment is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.

Read the react-developer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/engineering/react-developer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.

After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Criteria

- [ ] PASS: After bootstrap, `docs/architecture/_sections/react-developer.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim
- [ ] PASS: After bootstrap, `docs/architecture/_sections/react-developer.md` contains the merge marker `<!-- Added by react-developer bootstrap v0.1.0 -->` — the React conventions section was appended with the correct marker, not silently dropped
- [ ] PASS: After bootstrap, `docs/architecture/_sections/react-developer.md` contains a `## React/Next.js Conventions` heading — the top-level section was appended
- [ ] PASS: After bootstrap, `docs/architecture/_sections/react-developer.md` contains at least two of the subsection headings from the template (`### TypeScript`, `### Styling`, `### Component Patterns`, `### Testing`, `### Project Structure`, `### Deployment`) — proving the template body was appended, not just the heading
- [ ] PASS: The skill did NOT write `docs/architecture/CLAUDE.md` — that file is coordinator-assembled, and the skill writes only its own fragment
- [ ] PASS: Chat output includes a manifest summary that names `docs/architecture/_sections/react-developer.md` and uses append or update language (not "overwrote" or "replaced")

## Output expectations

- [ ] PASS: Output names `docs/architecture/_sections/react-developer.md` individually in the manifest — a bare "bootstrap complete" without listing the file is not enough
- [ ] PASS: Output does not claim it overwrote or replaced `docs/architecture/_sections/react-developer.md` — the language reflects append/merge, not replacement
- [ ] PARTIAL: Output points the reader at next steps consistent with the skill's documented manifest (mentions Tailwind, Vitest, or `/react-developer:component-from-spec`)
