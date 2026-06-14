# Test: php-developer/bootstrap writes its architecture fragment safely

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a `docs/architecture/_sections/php-developer.md` fragment that already contains a user-authored "Custom team notes" section with a sentinel line. The php-developer bootstrap skill should detect the existing fragment, append the "PHP Conventions" section (with a merge marker), and leave the user-authored content untouched. It writes only its own fragment — `docs/architecture/CLAUDE.md` is assembled by the coordinator from the fragments in `_sections/`, so this skill never touches it.

The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A `docs/architecture/_sections/php-developer.md` fragment already exists — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.

Read the php-developer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/engineering/php-developer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Do not pause for confirmation — proceed with all defaults.

After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Criteria

- [ ] PASS: After bootstrap, `docs/architecture/_sections/php-developer.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim
- [ ] PASS: After bootstrap, `docs/architecture/_sections/php-developer.md` contains the merge marker `<!-- Added by php-developer bootstrap v3.0.1 -->` — the PHP Conventions section was appended with the correct marker
- [ ] PASS: After bootstrap, `docs/architecture/_sections/php-developer.md` contains a `## PHP Conventions` heading — the conventions block was appended
- [ ] PASS: After bootstrap, `docs/architecture/_sections/php-developer.md` contains the `### Static analysis` subsection naming PHPStan
- [ ] PASS: After bootstrap, `docs/architecture/_sections/php-developer.md` contains the `### Code style` subsection naming PHP-CS-Fixer and PER-CS
- [ ] PASS: After bootstrap, `docs/architecture/_sections/php-developer.md` contains the `### Testing` subsection naming Pest, Behat, and Infection
- [ ] PASS: After bootstrap, `docs/architecture/_sections/php-developer.md` contains the `### Event sourcing` subsection naming EventSauce
- [ ] PASS: The skill did NOT write `docs/architecture/CLAUDE.md` — that file is coordinator-assembled, and the skill writes only its own fragment
- [ ] PASS: Chat output includes a manifest summary listing `docs/architecture/_sections/php-developer.md` as created or merged

## Output expectations

- [ ] PASS: Output names `docs/architecture/_sections/php-developer.md` as the file that was written — a bare "bootstrap complete" without the per-file manifest is not enough
- [ ] PASS: Output does not claim it overwrote or replaced `docs/architecture/_sections/php-developer.md` — the language reflects append or merge, not replacement
- [ ] PARTIAL: Output points the reader at next steps (configuring PHPStan, PHP-CS-Fixer, or using `/php-developer:write-feature-spec`) consistent with the skill's documented manifest
