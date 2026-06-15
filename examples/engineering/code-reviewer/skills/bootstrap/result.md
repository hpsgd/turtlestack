# Bootstrap

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/code-review/_sections/code-reviewer.md` fragment containing a user-authored section. The code-reviewer bootstrap skill should preserve that user content while appending the template's missing sections (with a merge marker), and should create the two files the fixture is missing — `review-checklist.md` and `pr-template.md`. The code-reviewer never writes `docs/code-review/CLAUDE.md` directly — the coordinator assembles it from the fragments in `_sections/`. The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

> The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/code-review/_sections/code-reviewer.md` fragment is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.
> 
> Read the code-reviewer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/engineering/code-reviewer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.
> 
> After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, detected languages, existing PR template status, next steps).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Code Review Bootstrap Complete

### Files created
- `docs/code-review/_sections/code-reviewer.md` — code-reviewer fragment (coordinator assembles `docs/code-review/CLAUDE.md` from it)
- `docs/code-review/review-checklist.md` — per-PR checklist
- `docs/code-review/pr-template.md` — suggested PR template

### Files merged
- `docs/code-review/_sections/code-reviewer.md` — existing user-authored "Custom team notes" section preserved; bootstrap sections appended with `<!-- Merged from code-reviewer bootstrap v0.1.0 -->`

### Detected languages
- None (minimal project with no tech context files)

### Existing PR template
- `.github/PULL_REQUEST_TEMPLATE.md` does not exist — next step to install the suggested template

### Next steps
- Remove language sections from `docs/code-review/_sections/code-reviewer.md` and `docs/code-review/review-checklist.md` that don't apply to TestProject once languages are detected/added
- Create `.github/PULL_REQUEST_TEMPLATE.md` using the template from `docs/code-review/pr-template.md`
- Configure SonarCloud quality gates to match the scoring thresholds
- Use `/code-reviewer:code-review` during PR reviews

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

## Python

- [ ] Type annotations on all function signatures
- [ ] Pydantic models at API and data boundaries (not raw dicts)
- [ ] No `Any` types — use `unknown` patterns or narrow types
- [ ] `ruff check` and `ruff format` pass cleanly
- [ ] `mypy --strict` passes with no new errors

## TypeScript

- [ ] `strict: true` in `tsconfig.json` — no weakened flags
- [ ] No `any` types — use `unknown` and narrow
- [ ] Zod schemas for runtime validation of external input
- [ ] ESLint and Prettier pass cleanly
- [ ] `tsc --noEmit` passes with no new errors

## C# / .NET

- [ ] Nullable reference types enabled (`<Nullable>enable</Nullable>`)
- [ ] FluentValidation for request models (not manual null checks)
- [ ] `dotnet format --verify-no-changes` passes
- [ ] No new Roslyn analyser warnings
- [ ] CSharpier formatting applied

## Security

- [ ] Input validated at every boundary (API, queue, file, CLI)
- [ ] No SQL/NoSQL injection risks (parameterised queries only)
- [ ] Auth and authz checks present on new endpoints
- [ ] Sensitive data not logged or exposed in error messages
- [ ] CORS, CSP, and security headers reviewed (if applicable)

> Remove language sections that don't apply to this project.

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

#### `work/docs/code-review/_sections/code-reviewer.md`

```
<!-- code-reviewer fragment of the code-review domain doc. Assembled into docs/code-review/CLAUDE.md by the coordinator. -->

## Custom team notes

USER-EDIT-SENTINEL-DO-NOT-STRIP

This section was written by the team and must survive any bootstrap re-run.
It exists to test the safe-merge contract: the bootstrap skill must not
overwrite or remove user-authored content.

<!-- Merged from code-reviewer bootstrap v0.1.0 -->

## Linter and formatter commands

Run these before opening a PR. CI runs them too, but catching issues locally is faster.

### Python

```bash
ruff check .
ruff format --check .
mypy --strict
```

### TypeScript

```bash
npx eslint .
npx prettier --check .
npx tsc --noEmit
```

### C# / .NET

```bash
dotnet format --verify-no-changes
```

Roslyn analysers run as part of `dotnet build` — check the warnings. CSharpier formatting is enforced in CI.

> Only include sections for languages detected in this project. Delete the rest.

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
| ESLint | TypeScript/JavaScript linting | Per-project config |
| Ruff | Python linting and formatting | Per-project config |
| CSharpier | C# formatting | Per-project config |
| Roslyn analysers | C# static analysis | Per-project config |

> Keep this table in sync with `docs/tooling-register.md`.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 10.5/10.5 (100%) |
| Evaluated | 2026-06-15 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 74308 ms |
| Target cost | $0.1372 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | After bootstrap, `docs/code-review/_sections/code-reviewer.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim | PASS | Artifact shows '## Custom team notes\n\nUSER-EDIT-SENTINEL-DO-NOT-STRIP\n\nThis section was written by the team...' intact at the top of the file. |
| c2 | After bootstrap, `docs/code-review/_sections/code-reviewer.md` contains the safe-merge marker `<!-- Merged from code-reviewer bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged | PASS | Artifact shows '<!-- Merged from code-reviewer bootstrap v0.1.0 -->' on the line directly before '## Linter and formatter commands'. |
| c3 | After bootstrap, `docs/code-review/_sections/code-reviewer.md` contains both the `## Review pass order` and `## Quality scoring` headings — the template's language-independent content was appended | PASS | Artifact contains '## Review pass order' and '## Quality scoring' sections with full content including the 4-pass list and the HARD/SOFT scoring table. |
| c4 | The code-reviewer fragment is authored at H2 and below — it does not introduce a `# Code Review Domain` H1 (the coordinator generates that when it assembles `docs/code-review/CLAUDE.md`) | PASS | Artifact begins with an HTML comment then '## Custom team notes' — no H1 heading anywhere in the file. |
| c5 | The skill does NOT write `docs/code-review/CLAUDE.md` directly — that file is the coordinator's to assemble from `_sections/` | PASS | Artifacts written section lists only three files: review-checklist.md, pr-template.md, and _sections/code-reviewer.md. No CLAUDE.md artifact present. |
| c6 | After bootstrap, `docs/code-review/review-checklist.md` exists and contains the `# Review checklist` heading | PASS | Artifact 'work/docs/code-review/review-checklist.md' exists and starts with '# Review checklist'. |
| c7 | After bootstrap, `docs/code-review/pr-template.md` exists and contains `Suggested content for` — indicating it was created from the skill's template | PASS | Artifact 'work/docs/code-review/pr-template.md' contains 'Suggested content for `.github/PULL_REQUEST_TEMPLATE.md`.' in its body. |
| c8 | Chat output includes a manifest summary that distinguishes files created (`review-checklist.md`, `pr-template.md`) from files merged (`_sections/code-reviewer.md`) | PASS | Chat output has distinct '### Files created' and '### Files merged' sections; review-checklist.md and pr-template.md appear under created; _sections/code-reviewer.md under merged. |
| c9 | Output names each file individually — a bare "bootstrap complete" without the per-file manifest is not enough | PASS | Chat output lists all three files individually with descriptions under separate '### Files created' and '### Files merged' headings. |
| c10 | Output does not claim it overwrote or replaced `docs/code-review/_sections/code-reviewer.md` — the language reflects merge, not replacement | PASS | Under '### Files merged': 'existing user-authored "Custom team notes" section preserved; bootstrap sections appended with...' — explicitly merge language. |
| c11 | Output includes next steps (e.g. removing unused language sections, configuring SonarCloud, using `/code-reviewer:code-review`) consistent with the skill's documented manifest | PARTIAL | '### Next steps' lists removing unused language sections, creating .github/PULL_REQUEST_TEMPLATE.md, configuring SonarCloud gates, and using `/code-reviewer:code-review`. |

### Notes

The skill executed correctly on all dimensions: sentinel preserved, merge marker applied, template sections appended, no H1, no CLAUDE.md written, both new files created with correct content, and manifest output properly structured. The only minor oddity is listing _sections/code-reviewer.md under both 'Files created' and 'Files merged', but the criterion was met since the distinction between created and merged files is clear.
