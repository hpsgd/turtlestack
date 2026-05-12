# Bootstrap

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/code-review/CLAUDE.md` containing a user-authored section. The code-reviewer bootstrap skill should preserve that user content while appending the template's missing sections (with a merge marker), and should create the two files the fixture is missing — `review-checklist.md` and `pr-template.md`. The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

> The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/code-review/CLAUDE.md` is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.
> 
> Read the code-reviewer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/engineering/code-reviewer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.
> 
> After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, detected languages, existing PR template status, next steps).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Code Review Bootstrap Complete

### Files created
- `docs/code-review/review-checklist.md` — per-PR checklist with language-agnostic and security sections
- `docs/code-review/pr-template.md` — suggested PR template for `.github/PULL_REQUEST_TEMPLATE.md`

### Files merged
- `docs/code-review/CLAUDE.md` — review process, quality scoring, available skills, and tooling table appended while preserving existing "Custom team notes" section (USER-EDIT-SENTINEL-DO-NOT-STRIP)

### Detected languages
- None detected (project has no package.json, tsconfig.json, pyproject.toml, requirements.txt, *.csproj, or *.sln)

### Existing PR template
- `.github/PULL_REQUEST_TEMPLATE.md` does not exist — ready for creation when configured

### Next steps
- Add language-specific linter/formatter commands and checklist sections once primary language(s) are configured
- Create `.github/PULL_REQUEST_TEMPLATE.md` from the suggested template in `docs/code-review/pr-template.md`
- Configure SonarCloud quality gates to match the HARD/SOFT signal thresholds
- Update tooling table in CLAUDE.md to reflect tools integrated with this project
- Use `/code-reviewer:code-review` during PR reviews and `/code-reviewer:pr-create` for new PRs

### Artifacts written

#### `work/docs/code-review/review-checklist.md`

```
# Review checklist

Use this checklist per PR. Not every item applies to every change — skip items that genuinely don't apply, but read through the full list before deciding.

## All languages

- [ ] Read the full file, not just the diff — context matters
- [ ] Check for logic errors, off-by-one, null/undefined handling
- [ ] Verify error handling covers all paths (not just the happy path)
- [ ] Check for secrets, keys, or credentials in code or config
- [ ] Verify test coverage of changed code paths
- [ ] Confirm the PR description matches what the code actually does
- [ ] Check that new dependencies are justified and pinned

## Security

- [ ] Input validated at every boundary (API, queue, file, CLI)
- [ ] No SQL/NoSQL injection risks (parameterised queries only)
- [ ] Auth and authz checks present on new endpoints
- [ ] Sensitive data not logged or exposed in error messages
- [ ] CORS, CSP, and security headers reviewed (if applicable)

> Add language-specific sections here once your project languages are configured (Python, TypeScript, C# / .NET).

```

#### `work/docs/code-review/CLAUDE.md`

```
# Code Review

This directory contains code review documentation for the project.

## Custom team notes

USER-EDIT-SENTINEL-DO-NOT-STRIP

This section was written by the team and must survive any bootstrap re-run.
It exists to test the safe-merge contract: the bootstrap skill must not
overwrite or remove user-authored content.

<!-- Merged from code-reviewer bootstrap v0.1.0 -->

## Linter and formatter commands

Run these before opening a PR. CI runs them too, but catching issues locally is faster.

> No languages detected in this project. Add sections here for your primary language(s) once configured (Python, TypeScript, C# / .NET).

## Review pass order

Reviews follow four passes in this order. Do not skip ahead.

1. **Context** — read the linked issue, understand *why* this change exists, check the PR description matches the diff
2. **Correctness** — logic errors, edge cases, off-by-one, null/undefined handling, error paths
3. **Security** — input validation, injection risks, secrets in code, auth/authz gaps, data exposure
4. **Quality** — readability, naming, duplication, test coverage, performance

## Quality scoring

Each dimension scores 0-100. HARD signals block merge. SOFT signals are advisory.

| Signal | Type | 0 = | 100 = |
|---|---|---|---|
| Security | HARD | Vulnerability found | Clean |
| Correctness | HARD | Logic error found | Sound |
| Data integrity | HARD | Data loss possible | Safe |
| Performance | SOFT | Unnecessary complexity | Optimised |
| Maintainability | SOFT | Tight coupling, unclear intent | Clear |
| Test coverage | SOFT | Changed paths untested | Covered |

A PR with any HARD signal below 70 should not merge without explicit justification.

## Available skills

| Skill | When to use |
|-------|-------------|
| `/code-reviewer:code-review` | Run a full multi-pass review on a PR or diff |
| `/code-reviewer:pr-create` | Create a PR with the standard template and checks |

## Tooling

| Tool | Purpose | Owner |
|------|---------|-------|
| GitHub PRs | Code review workflow | Engineering |
| SonarCloud | Static analysis, coverage gates | Engineering |

> Keep this table in sync with `docs/tooling-register.md`.

```

#### `work/docs/code-review/pr-template.md`

```
# PR template

Suggested content for `.github/PULL_REQUEST_TEMPLATE.md`.

> **If `.github/PULL_REQUEST_TEMPLATE.md` already exists**, review it against this template and merge any missing sections rather than replacing. Append merged sections with `<!-- Merged from code-reviewer bootstrap v0.1.0 -->`.

## Template

```markdown
## What changed

<!-- Brief description of the change -->

## Why

<!-- Link to issue, context for the change -->
Closes #

## How to test

<!-- Steps to verify this change works -->

## Checklist

- [ ] Tests added/updated
- [ ] No new lint warnings
- [ ] Documentation updated (if needed)
- [ ] Self-reviewed for security concerns
```

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 9.5/10.0 (95%) |
| Evaluated | 2026-05-13 |
| Target duration | 47582 ms |
| Target cost | $0.1294 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | After bootstrap, `docs/code-review/CLAUDE.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim | PASS | Artifact shows `USER-EDIT-SENTINEL-DO-NOT-STRIP` on its own line under `## Custom team notes`, with surrounding user content intact. |
| c2 | After bootstrap, `docs/code-review/CLAUDE.md` contains the safe-merge marker `<!-- Merged from code-reviewer bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged | PASS | Artifact contains `<!-- Merged from code-reviewer bootstrap v0.1.0 -->` immediately before the appended template sections. |
| c3 | After bootstrap, `docs/code-review/CLAUDE.md` contains both the `## Review pass order` and `## Quality scoring` headings — the template's language-independent content was appended | PASS | Artifact contains both `## Review pass order` and `## Quality scoring` headings in the appended section after the merge marker. |
| c4 | After bootstrap, `docs/code-review/review-checklist.md` exists and contains the `# Review checklist` heading | PASS | Artifact `work/docs/code-review/review-checklist.md` opens with `# Review checklist`. |
| c5 | After bootstrap, `docs/code-review/pr-template.md` exists and contains `Suggested content for` — indicating it was created from the skill's template | PASS | Artifact `work/docs/code-review/pr-template.md` contains "Suggested content for `.github/PULL_REQUEST_TEMPLATE.md`". |
| c6 | Chat output includes a manifest summary that distinguishes files created (`review-checklist.md`, `pr-template.md`) from files merged (`CLAUDE.md`) | PASS | Chat response has separate `### Files created` and `### Files merged` sections, listing the two new files vs. the merged CLAUDE.md. |
| c7 | Output names each file individually — a bare 'bootstrap complete' without the per-file manifest is not enough | PASS | All three files are named individually with descriptions: `review-checklist.md`, `pr-template.md`, and `CLAUDE.md` each on their own bullet. |
| c8 | Output does not claim it overwrote or replaced `docs/code-review/CLAUDE.md` — the language reflects merge, not replacement | PASS | Chat says "appended while preserving existing 'Custom team notes' section (USER-EDIT-SENTINEL-DO-NOT-STRIP)" — clearly merge language, not replacement. |
| c9 | Output includes next steps (e.g. removing unused language sections, configuring SonarCloud, using `/code-reviewer:code-review`) consistent with the skill's documented manifest | PARTIAL | Chat lists 5 next steps including SonarCloud configuration and `/code-reviewer:code-review` usage, but does not mention removing unused language placeholder sections. |

### Notes

All file content criteria pass cleanly — sentinel preserved, merge marker present, template headings appended, both new files created correctly. The only minor gap is c9 (capped PARTIAL): next steps cover SonarCloud and skill usage but omit the 'remove unused language placeholder sections' item the criterion hints at.
