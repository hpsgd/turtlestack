---
name: bootstrap
description: "Bootstrap Python conventions into the architecture documentation. Appends Python-specific sections to docs/architecture/CLAUDE.md. Idempotent — merges missing sections into existing files without overwriting."
argument-hint: "[project name]"
user-invocable: false
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Bootstrap Python Conventions

Bootstrap Python development conventions for **$ARGUMENTS**.

This skill does NOT create its own domain directory. It appends Python-specific sections to `docs/architecture/CLAUDE.md`.

## Process

### Step 1: Verify architecture domain exists

```bash
mkdir -p docs/architecture
```

If `docs/architecture/CLAUDE.md` does not exist, stop and report that the architect bootstrap should run first.

### Step 2: Append Python conventions to `docs/architecture/CLAUDE.md`

Check if `docs/architecture/CLAUDE.md` already contains a "Python Conventions" section. If not, append the following:

```markdown

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

### Step 3: Return manifest

After creating/merging all files, output a summary:

```
## Python Developer Bootstrap Complete

### Files merged
- `docs/architecture/CLAUDE.md` — appended Python Conventions section

### Next steps
- Configure mypy strict mode in `pyproject.toml`
- Configure Ruff rules in `pyproject.toml`
- Use `/python-developer:write-feature-spec` for BDD specifications
- Use `/python-developer:write-schema` for Pydantic models
```
