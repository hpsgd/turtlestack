# Test: ai-engineer/bootstrap scaffolds docs/ai safely

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/ai/CLAUDE.md` containing a user-authored section. The ai-engineer bootstrap skill should preserve that user content while appending the template's missing sections (with a merge marker), and should create the two files the fixture is missing — `prompt-library.md` and `eval-suite-template.md`.

The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/ai/CLAUDE.md` is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.

Read the ai-engineer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/engineering/ai-engineer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.

After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Criteria

- [ ] PASS: After bootstrap, `docs/ai/CLAUDE.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim
- [ ] PASS: After bootstrap, `docs/ai/CLAUDE.md` contains the safe-merge marker `<!-- Merged from ai-engineer bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged
- [ ] PASS: After bootstrap, `docs/ai/CLAUDE.md` contains the appended template sections — at minimum the "Prompt Engineering Conventions" and "Model Evaluation" headings now appear alongside the preserved user content
- [ ] PASS: After bootstrap, `docs/ai/prompt-library.md` exists and contains a `## Prompt Registry` heading
- [ ] PASS: After bootstrap, `docs/ai/eval-suite-template.md` exists and contains a `## Metrics` heading
- [ ] PASS: The created `eval-suite-template.md` contains an AI-specific metrics row referencing RAGAS (e.g. `Faithfulness (RAGAS)`) or `## Failure Analysis`
- [ ] PASS: Chat output includes a manifest summary that distinguishes files created (`prompt-library.md`, `eval-suite-template.md`) from files merged (`CLAUDE.md`)

## Output expectations

- [ ] PASS: Output names each created and merged file individually — a bare "bootstrap complete" without the per-file manifest is not enough
- [ ] PASS: Output does not claim it overwrote or replaced `docs/ai/CLAUDE.md` — the language reflects merge, not replacement
- [ ] PARTIAL: Output points the reader at next steps (using `/ai-engineer:model-evaluation` or `/ai-engineer:rag-pipeline`) consistent with the skill's documented manifest
