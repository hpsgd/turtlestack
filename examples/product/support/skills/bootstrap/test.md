# Test: support/bootstrap scaffolds docs/support safely

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/support/CLAUDE.md` containing a user-authored section. The support bootstrap skill should preserve that user content while appending the template's missing sections (with a merge marker), and should create the two files the fixture is missing — `escalation-playbook.md` and `kb-article-template.md`.

The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/support/CLAUDE.md` is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.

Read the support bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/product/support/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.

After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Criteria

- [ ] PASS: After bootstrap, `docs/support/CLAUDE.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim
- [ ] PASS: After bootstrap, `docs/support/CLAUDE.md` contains the safe-merge marker `<!-- Merged from support bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged
- [ ] PASS: After bootstrap, `docs/support/CLAUDE.md` contains the appended template sections — at minimum the `## Ticket Triage Process` and `## Customer Health Scoring` headings now appear alongside the preserved user content
- [ ] PASS: After bootstrap, `docs/support/escalation-playbook.md` exists and was created from the skill's template (contains `## Escalation Trigger` and `## L2 Investigation` headings)
- [ ] PASS: After bootstrap, `docs/support/kb-article-template.md` exists and was created from the skill's template (contains `## Instructions` and `## Expected Result` headings)
- [ ] PASS: Chat output includes a manifest summary that distinguishes files created (`escalation-playbook.md`, `kb-article-template.md`) from files merged (`CLAUDE.md`)
- [ ] PASS: The manifest output header is `## Support & Customer Success Bootstrap Complete` — the exact heading the skill specifies

## Output expectations

- [ ] PASS: Output names each created and merged file individually — a bare "bootstrap complete" without the per-file manifest is not enough
- [ ] PASS: Output does not claim it overwrote or replaced `docs/support/CLAUDE.md` — the language reflects merge, not replacement
- [ ] PARTIAL: Output points the reader at next steps consistent with the skill's documented manifest (creating escalation playbooks, setting up GitHub Wiki, or using support/CS skills)
