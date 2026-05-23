# Test: php-developer/bootstrap appends PHP Conventions safely

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a `docs/architecture/CLAUDE.md` that already contains architecture conventions and a user-authored "Custom team notes" section with a sentinel line. The php-developer bootstrap skill should detect the existing file, append the "PHP Conventions" section (with a merge marker), and leave the user-authored content untouched.

The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A `docs/architecture/CLAUDE.md` already exists — it contains architecture conventions from a prior architect bootstrap and a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.

Read the php-developer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/engineering/php-developer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Do not pause for confirmation — proceed with all defaults.

After the bootstrap completes, output the manifest summary the skill defines (files updated, files merged, next steps).

## Criteria

- [ ] PASS: After bootstrap, `docs/architecture/CLAUDE.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim
- [ ] PASS: After bootstrap, `docs/architecture/CLAUDE.md` contains the merge marker `<!-- Added by php-developer bootstrap v3.0.1 -->` — the PHP Conventions section was appended with the correct marker
- [ ] PASS: After bootstrap, `docs/architecture/CLAUDE.md` contains a `## PHP Conventions` heading — the conventions block was appended
- [ ] PASS: After bootstrap, `docs/architecture/CLAUDE.md` contains the `### Static analysis` subsection naming PHPStan
- [ ] PASS: After bootstrap, `docs/architecture/CLAUDE.md` contains the `### Code style` subsection naming PHP-CS-Fixer and PER-CS
- [ ] PASS: After bootstrap, `docs/architecture/CLAUDE.md` contains the `### Testing` subsection naming Pest, Behat, and Infection
- [ ] PASS: After bootstrap, `docs/architecture/CLAUDE.md` contains the `### Event sourcing` subsection naming EventSauce
- [ ] PASS: Chat output includes a manifest summary listing `docs/architecture/CLAUDE.md` as updated or merged

## Output expectations

- [ ] PASS: Output names `docs/architecture/CLAUDE.md` as the file that was updated — a bare "bootstrap complete" without the per-file manifest is not enough
- [ ] PASS: Output does not claim it overwrote or replaced `docs/architecture/CLAUDE.md` — the language reflects append or merge, not replacement
- [ ] PARTIAL: Output points the reader at next steps (configuring PHPStan, PHP-CS-Fixer, or using `/php-developer:write-feature-spec`) consistent with the skill's documented manifest
