# Test: security-engineer/bootstrap scaffolds docs/security safely

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/security/CLAUDE.md` containing a user-authored section. The security-engineer bootstrap skill should preserve that user content while appending the template's missing sections (with a merge marker), and should create the three files the fixture is missing — `SECURITY.md`, `docs/security/threat-model-template.md`, and `docs/security/security-review-template.md`.

The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/security/CLAUDE.md` is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.

Read the security-engineer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/engineering/security-engineer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.

After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Criteria

- [ ] PASS: After bootstrap, `docs/security/CLAUDE.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim
- [ ] PASS: After bootstrap, `docs/security/CLAUDE.md` contains the safe-merge marker `<!-- Merged from security-engineer bootstrap v0.1.0 -->` and the "STRIDE Threat Modelling" heading was appended
- [ ] PASS: After bootstrap, `SECURITY.md` exists at the project root and contains a "Reporting a Vulnerability" heading
- [ ] PASS: After bootstrap, `docs/security/threat-model-template.md` exists and contains a "STRIDE Analysis" heading
- [ ] PASS: After bootstrap, `docs/security/security-review-template.md` exists and contains a "Checklist" heading

## Output expectations

- [ ] PASS: Chat output individually lists files created and any files merged — a bare "bootstrap complete" without the per-file list is not enough
- [ ] PASS: Output does not claim it overwrote or replaced `docs/security/CLAUDE.md` — the language reflects merge, not replacement
- [ ] PARTIAL: Output points the reader at next steps (updating `SECURITY.md` with a contact email, using `/security-engineer:threat-model`) consistent with the skill's documented manifest
