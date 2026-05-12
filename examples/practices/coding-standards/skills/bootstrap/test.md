# Test: coding-standards/bootstrap scaffolds docs/ root safely

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a root `CLAUDE.md` containing a user-authored section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`, and a `package.json` indicating a TypeScript/JavaScript project. The coding-standards bootstrap skill should preserve user content in root `CLAUDE.md` while appending a "Coding Standards" section, create `docs/tooling-register.md` from the template, detect TypeScript/JavaScript as a language, and output a manifest with the sections the skill defines. Rule installation is the thinking plugin's responsibility (its SessionStart hook) and is explicitly out of scope for this skill.

The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A root `CLAUDE.md` is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`. A `package.json` is also present, indicating a TypeScript/JavaScript project.

Read the coding-standards bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/practices/coding-standards/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.

After the bootstrap completes, output the manifest summary the skill defines (Files created, CLAUDE.md updated, Files merged, Detected languages, Next steps).

## Criteria

- [ ] PASS: After bootstrap, root `CLAUDE.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim
- [ ] PASS: After bootstrap, root `CLAUDE.md` contains a `## Coding Standards` heading — the conventions section was appended without replacing the existing content
- [ ] PASS: After bootstrap, `docs/tooling-register.md` exists and contains a `# Tooling Register` heading and at least one table (the "Development Tools" table from the template)
- [ ] PASS: The manifest output includes a "Files created" section listing `docs/tooling-register.md`
- [ ] PASS: The manifest output includes a "CLAUDE.md updated" section — distinct from "Files created" or "Files merged"
- [ ] PASS: The manifest output includes a "Detected languages" section that names TypeScript, JavaScript, or Node — confirming `package.json` was used for language detection
- [ ] PASS: The output does not claim rule files were copied to `.claude/rules/` — rule installation is the thinking plugin's responsibility, not this skill's

## Output expectations

- [ ] PASS: Output names `docs/tooling-register.md` as a created file — a bare "bootstrap complete" without per-file detail is not enough
- [ ] PASS: Output does not claim it overwrote or replaced the root `CLAUDE.md` — the language reflects append or merge, not replacement
- [ ] PARTIAL: Output points the reader at next steps consistent with the skill's documented manifest (customising `docs/tooling-register.md`, configuring SonarCloud, ensuring the thinking plugin is enabled, or using `/coding-standards:review-*` skills)
