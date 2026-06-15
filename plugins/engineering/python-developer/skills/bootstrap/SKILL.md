---
name: bootstrap
bootstrap-phase: stack
description: "Bootstrap Python conventions into the architecture documentation. Writes the python-developer fragment of the architecture domain doc. Idempotent — merges missing sections into existing files without overwriting."
argument-hint: "[project name]"
user-invocable: false
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Bootstrap Python Conventions

Bootstrap Python development conventions for **$ARGUMENTS**.

This skill writes only its own fragment — `docs/architecture/_sections/python-developer.md`. The architecture domain `CLAUDE.md` is assembled by the coordinator from every fragment in `_sections/`, so this skill never collides with the architect or the other stack developers.

## Process

### Step 1: Create the sections directory

```bash
mkdir -p docs/architecture/_sections
```

### Step 2: Write the Python fragment

`docs/architecture/CLAUDE.md` is **assembled by the coordinator** from the fragments in `_sections/` — no plugin writes it directly, so this skill and the architect never collide on it. Write the Python contribution as `docs/architecture/_sections/python-developer.md`. It starts at H2 (the coordinator generates the `# Architecture Domain` H1).

Apply the safe merge pattern:

- If the fragment does not exist → create it from the template below
- If the fragment exists → read both, find sections in the template missing from the file, append only the missing sections with the marker `<!-- Added by python-developer bootstrap v0.1.0 -->`

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

### Files created
- `docs/architecture/_sections/python-developer.md` — python-developer's fragment of the architecture domain doc (assembled into `docs/architecture/CLAUDE.md` by the coordinator)

### Files merged
- (list the fragment here if it already existed and missing sections were appended, or "none")

### Next steps
- Configure mypy strict mode in `pyproject.toml`
- Configure Ruff rules in `pyproject.toml`
- Use `/python-developer:write-feature-spec` for BDD specifications
- Use `/python-developer:write-schema` for Pydantic models
```

## Rules

- **Write only your own fragment.** `docs/architecture/CLAUDE.md` is assembled by the coordinator; this skill writes `docs/architecture/_sections/python-developer.md` and nothing else. The architect and the other stack developers write their own fragments — there is no shared file to clobber.
- **Safe-merge the fragment, idempotent by design.** If the fragment exists, preserve user-authored content and append only missing template sections with the marker — never overwrite. Running twice produces no duplicate sections.
