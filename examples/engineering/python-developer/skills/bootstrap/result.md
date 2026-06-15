# Bootstrap

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a `docs/architecture/_sections/python-developer.md` fragment that already contains a user-authored "Custom team notes" section with a sentinel line. The python-developer bootstrap skill should detect the existing fragment, append the "Python Conventions" section (with a merge marker), and leave the user-authored content untouched. It writes only its own fragment — `docs/architecture/CLAUDE.md` is assembled by the coordinator from the fragments in `_sections/`, so this skill never touches it. The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

> The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A `docs/architecture/_sections/python-developer.md` fragment already exists — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.
> 
> Read the python-developer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/engineering/python-developer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Do not pause for confirmation — proceed with all defaults.
> 
> After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Python Developer Bootstrap Complete

### Files created
- None (the fragment already existed)

### Files merged
- `docs/architecture/_sections/python-developer.md` — appended missing Python Conventions sections (Typing, Linting and Formatting, Testing, Pydantic, Project Structure, Python Tooling, Available Skills) while preserving the existing "Custom team notes" user-authored section

### Next steps
- Configure mypy strict mode in `pyproject.toml`
- Configure Ruff rules in `pyproject.toml`
- Use `/python-developer:write-feature-spec` for BDD specifications
- Use `/python-developer:write-schema` for Pydantic models

### Artifacts written

#### `work/docs/architecture/_sections/python-developer.md`

```
<!-- python-developer fragment of the architecture domain doc. Assembled into docs/architecture/CLAUDE.md by the coordinator. -->

## Custom team notes

USER-EDIT-SENTINEL-DO-NOT-STRIP

This section was written by the team and must survive any bootstrap re-run.
It exists to test the safe-merge contract: the bootstrap skill must not
overwrite or remove user-authored content.

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

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 10.5/10.5 (100%) |
| Evaluated | 2026-06-15 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 29726 ms |
| Target cost | $0.0693 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | After bootstrap, `docs/architecture/_sections/python-developer.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim | PASS | Artifact file contains 'USER-EDIT-SENTINEL-DO-NOT-STRIP' in the ## Custom team notes section, verbatim. |
| c2 | After bootstrap, `docs/architecture/_sections/python-developer.md` contains the merge marker `<!-- Added by python-developer bootstrap v0.1.0 -->` — the Python Conventions section was appended with the correct marker | PASS | Artifact contains '<!-- Added by python-developer bootstrap v0.1.0 -->' immediately before '## Python Conventions'. |
| c3 | After bootstrap, `docs/architecture/_sections/python-developer.md` contains a `## Python Conventions` heading — the conventions block was appended | PASS | Artifact contains '## Python Conventions' heading after the user-authored section. |
| c4 | After bootstrap, `docs/architecture/_sections/python-developer.md` contains the `### Typing` subsection — strict typing requirements are present | PASS | Artifact contains '### Typing' with content including 'Strict typing required', mypy strict mode, TypeAlias, and no Any. |
| c5 | After bootstrap, `docs/architecture/_sections/python-developer.md` contains the `### Linting and Formatting` subsection — Ruff configuration guidance is present | PASS | Artifact contains '### Linting and Formatting' with Ruff details including rule set and 120-char line length. |
| c6 | After bootstrap, `docs/architecture/_sections/python-developer.md` contains the `### Testing (BDD)` subsection — pytest-bdd test conventions are present | PASS | Artifact contains '### Testing (BDD)' with pytest-bdd, feature files location, and naming conventions. |
| c7 | The skill did NOT write `docs/architecture/CLAUDE.md` — that file is coordinator-assembled, and the skill writes only its own fragment | PASS | No artifact for docs/architecture/CLAUDE.md is listed; only the _sections/python-developer.md file appears in artifacts written. |
| c8 | Chat output includes a manifest summary listing `docs/architecture/_sections/python-developer.md` as created or merged | PASS | Chat output '### Files merged' section lists 'docs/architecture/_sections/python-developer.md — appended missing Python Conventions sections'. |
| c9 | Output names `docs/architecture/_sections/python-developer.md` as the file that was written — a bare "bootstrap complete" without the per-file manifest is not enough | PASS | Output explicitly names 'docs/architecture/_sections/python-developer.md' in the Files merged section with per-file detail. |
| c10 | Output does not claim it overwrote or replaced `docs/architecture/_sections/python-developer.md` — the language reflects append or merge, not replacement | PASS | Output uses 'appended missing Python Conventions sections... while preserving the existing... user-authored section' — no overwrite/replace language. |
| c11 | Output points the reader at next steps (configuring mypy, Ruff, or using `/python-developer:write-feature-spec`) consistent with the skill's documented manifest | PARTIAL | Chat output '### Next steps' lists mypy strict mode, Ruff config, /python-developer:write-feature-spec and /python-developer:write-schema. |

### Notes

The skill executed correctly across all criteria: sentinel preserved, merge marker present, all subsections appended, CLAUDE.md not touched, manifest complete with append/merge language, and next steps documented. Perfect score.
