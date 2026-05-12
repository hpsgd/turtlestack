# Bootstrap

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a `docs/architecture/CLAUDE.md` that already contains architecture conventions and a user-authored "Custom team notes" section with a sentinel line. The python-developer bootstrap skill should detect the existing file, append the "Python Conventions" section (with a merge marker), and leave the user-authored content untouched. The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

> The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A `docs/architecture/CLAUDE.md` already exists — it contains architecture conventions from a prior architect bootstrap and a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.
> 
> Read the python-developer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/engineering/python-developer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Do not pause for confirmation — proceed with all defaults.
> 
> After the bootstrap completes, output the manifest summary the skill defines (files updated, files merged, next steps).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Python Developer Bootstrap Complete

### Files merged
- `docs/architecture/CLAUDE.md` — appended Python Conventions section

### Next steps
- Configure mypy strict mode in `pyproject.toml`
- Configure Ruff rules in `pyproject.toml`
- Use `/python-developer:write-feature-spec` for BDD specifications
- Use `/python-developer:write-schema` for Pydantic models

### Artifacts written

#### `work/docs/architecture/CLAUDE.md`

```
# Architecture Domain

This directory contains architecture documentation for the project: decision records, system design artefacts, and API design guidelines.

## What This Domain Covers

- **Architecture Decision Records (ADRs)** — capturing significant technical decisions
- **System design** — C4 model diagrams, arc42 documentation, component relationships
- **API design** — REST/GraphQL/gRPC contract guidelines

## ADR Conventions

We use **MADR** (Markdown Any Decision Records) v3.0 format. Store ADRs in `docs/architecture/adr/`.

<!-- Added by python-developer bootstrap v0.1.0 -->
## Python Conventions

### Typing

- **Strict typing required** — all functions must have type annotations
- Enforce with [mypy](https://mypy-lang.org/) in strict mode (`--strict`)
- Use `from __future__ import annotations` for PEP 604 syntax
- Prefer `TypeAlias` and `TypeVar` for complex types
- No `Any` without an explanatory comment

### Linting and Formatting

- **Ruff** for linting and formatting (replaces flake8, isort, black)
- Rule set: `select = ["E", "F", "I", "N", "UP", "B", "SIM", "C4", "PT"]`
- Line length: 120 characters
- CI gate: zero Ruff violations allowed

### Testing (BDD)

- **pytest-bdd** for acceptance tests (Given/When/Then)
- **pytest** for unit and integration tests
- Feature files in `tests/features/` alongside step definitions
- Use `@pytest.fixture` for test setup — no shared mutable state
- Naming: `test_should_{behaviour}_when_{condition}.py`
- Coverage enforced via SonarCloud (project-specific threshold)

### Pydantic

- Use **Pydantic v2** with `model_config = ConfigDict(strict=True)`
- All API request/response models must be Pydantic `BaseModel`
- Validate at trust boundaries (API handlers, event consumers)
- Use `Field(...)` with descriptions for all public models

### Project Structure

```
src/
├── {package}/
│   ├── __init__.py
│   ├── domain/          # Domain models and business logic
│   ├── application/     # Use cases, commands, queries
│   ├── infrastructure/  # DB, external services, adapters
│   └── api/             # HTTP handlers, serialisation
tests/
├── unit/
├── integration/
├── features/            # BDD feature files
└── conftest.py
```

### Python Tooling

| Tool | Purpose |
|------|---------|
| [SonarCloud](https://sonarcloud.io) | Python code quality and coverage gate |
| [GitHub Actions](https://docs.github.com/en/actions) | `pytest` in CI on every PR |

### Available Python Skills

| Skill | Purpose |
|-------|---------|
| `/python-developer:write-feature-spec` | Write a BDD feature specification |
| `/python-developer:write-schema` | Write a Pydantic schema |

## Custom team notes

USER-EDIT-SENTINEL-DO-NOT-STRIP

This section was written by the team and must survive any bootstrap re-run.
It exists to test the safe-merge contract: the bootstrap skill must not
overwrite or remove user-authored content.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 9.5/9.5 (100%) |
| Evaluated | 2026-05-13 |
| Target duration | 21285 ms |
| Target cost | $0.0724 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | After bootstrap, `docs/architecture/CLAUDE.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim | PASS | Artifact contains 'USER-EDIT-SENTINEL-DO-NOT-STRIP' in the 'Custom team notes' section at the bottom of the file, with surrounding text intact. |
| c2 | After bootstrap, `docs/architecture/CLAUDE.md` contains the merge marker `<!-- Added by python-developer bootstrap v0.1.0 -->` — the Python Conventions section was appended with the correct marker | PASS | Artifact contains exactly '<!-- Added by python-developer bootstrap v0.1.0 -->' immediately before the '## Python Conventions' heading. |
| c3 | After bootstrap, `docs/architecture/CLAUDE.md` contains a `## Python Conventions` heading — the conventions block was appended | PASS | Artifact contains '## Python Conventions' as a second-level heading after the existing architecture content. |
| c4 | After bootstrap, `docs/architecture/CLAUDE.md` contains the `### Typing` subsection — strict typing requirements are present | PASS | Artifact contains '### Typing' subsection with mypy strict mode, type annotations, and 'No `Any`' requirements. |
| c5 | After bootstrap, `docs/architecture/CLAUDE.md` contains the `### Linting and Formatting` subsection — Ruff configuration guidance is present | PASS | Artifact contains '### Linting and Formatting' subsection with Ruff rule set, line length 120, and CI gate requirements. |
| c6 | After bootstrap, `docs/architecture/CLAUDE.md` contains the `### Testing (BDD)` subsection — pytest-bdd test conventions are present | PASS | Artifact contains '### Testing (BDD)' subsection with pytest-bdd, feature files location, fixture conventions, and naming patterns. |
| c7 | Chat output includes a manifest summary listing `docs/architecture/CLAUDE.md` as updated or merged | PASS | Chat output has '### Files merged' section listing '`docs/architecture/CLAUDE.md` — appended Python Conventions section'. |
| c8 | Output names `docs/architecture/CLAUDE.md` as the file that was updated — a bare 'bootstrap complete' without the per-file manifest is not enough | PASS | Output explicitly names '`docs/architecture/CLAUDE.md`' under the 'Files merged' section with specific description of what changed. |
| c9 | Output does not claim it overwrote or replaced `docs/architecture/CLAUDE.md` — the language reflects append or merge, not replacement | PASS | Output uses 'merged' in heading and 'appended Python Conventions section' in the file entry — no overwrite or replacement language. |
| c10 | Output points the reader at next steps (configuring mypy, Ruff, or using `/python-developer:write-feature-spec`) consistent with the skill's documented manifest | PARTIAL | Next steps lists mypy strict mode, Ruff rules, '/python-developer:write-feature-spec', and '/python-developer:write-schema' — all skill-relevant items. |

### Notes

The skill executed flawlessly: user-authored content preserved, merge marker correct, all convention subsections present, and manifest output well-formed. The score is 100% of achievable points with c10 capped at PARTIAL by the test author.
