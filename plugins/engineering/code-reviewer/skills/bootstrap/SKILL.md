---
name: bootstrap
bootstrap-phase: engineering
description: "Bootstrap the code review documentation structure for a project. Creates docs/code-review/, generates initial templates, and writes the code-reviewer fragment of the code-review domain doc (the coordinator assembles docs/code-review/CLAUDE.md). Idempotent — merges missing sections into existing files without overwriting."
argument-hint: "[project name]"
user-invocable: false
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Bootstrap Code Review

Bootstrap the code review documentation for **$ARGUMENTS**.

This skill owns the review process and tooling config. Coding rules and conventions belong to `coding-standards`. The code-reviewer owns how reviews happen, what gets checked, and what tooling runs.

## Process

### Step 1: Detect tech context

If tech context was provided by the coordinator, use it directly.

If running standalone, scan the project:

```bash
# Languages
ls package.json tsconfig.json 2>/dev/null          # TypeScript/JavaScript
ls requirements.txt pyproject.toml setup.py 2>/dev/null  # Python
ls *.csproj *.sln 2>/dev/null                       # .NET

# Linting tools
ls .eslintrc* eslint.config.* 2>/dev/null           # ESLint
ls ruff.toml .ruff.toml pyproject.toml 2>/dev/null  # Ruff (check [tool.ruff] in pyproject.toml)
ls .editorconfig 2>/dev/null                        # EditorConfig

# Existing PR template
ls .github/PULL_REQUEST_TEMPLATE.md 2>/dev/null
```

If the scan is ambiguous (e.g. both `package.json` and `pyproject.toml` exist but you cannot tell which is primary), list findings and ask.

### Step 2: Create docs directory

```bash
mkdir -p docs/code-review docs/code-review/_sections
```

### Step 3: Create or merge files

For each file below, apply the safe merge pattern:

- If file does not exist, create from template
- If file exists, read it, find sections in the template that are missing, append missing sections with `<!-- Merged from code-reviewer bootstrap v0.1.0 -->`

#### Fragment: `docs/code-review/_sections/code-reviewer.md`

`docs/code-review/CLAUDE.md` is **assembled by the coordinator** from the fragments in `_sections/` — no plugin
writes it directly. Write the code-reviewer's contribution as this fragment (adapt linter commands to detected
languages). It starts at H2 (the coordinator generates the `# Code Review Domain` H1 and a one-line intro).
This domain owns *how* reviews are run, not *what* the code should look like — coding rules live in
`coding-standards`. Create it with this content:

```markdown
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

Remove language sections that don't apply to the detected project. If the project uses only Python, delete the TypeScript and C# sections (and vice versa). Keep tooling table rows only for detected languages.

#### File 2: `docs/code-review/review-checklist.md`

```markdown
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

#### File 3: `docs/code-review/pr-template.md`

```markdown
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

### Step 4: Return manifest

After creating/merging all files, output a summary:

```
## Code Review Bootstrap Complete

### Files created
- `docs/code-review/_sections/code-reviewer.md` — code-reviewer fragment (coordinator assembles `docs/code-review/CLAUDE.md` from it)
- `docs/code-review/review-checklist.md` — per-PR checklist
- `docs/code-review/pr-template.md` — suggested PR template

### Files merged
- (list any existing files where sections were appended)

### Detected languages
- (list detected languages/frameworks)

### Existing PR template
- (note whether .github/PULL_REQUEST_TEMPLATE.md exists and what action was taken)

### Next steps
- Remove language sections from the `_sections/code-reviewer.md` fragment and checklist that don't apply
- Review and install the PR template if .github/PULL_REQUEST_TEMPLATE.md doesn't exist
- Configure SonarCloud quality gates to match the scoring thresholds
- Use `/code-reviewer:code-review` during PR reviews
```
