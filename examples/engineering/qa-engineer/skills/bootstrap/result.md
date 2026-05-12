# Bootstrap

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a `pyproject.toml` (marking it as a Python project) and a partial `docs/testing/CLAUDE.md` containing a user-authored section. The qa-engineer bootstrap skill should detect Python, preserve the user content while appending missing sections (with a merge marker), and create the two new files — `docs/testing/test-config.md` and `docs/testing/ci-test-jobs.md` — filtered to Python only. The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

> The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A `pyproject.toml` is present at the root. A partial `docs/testing/CLAUDE.md` is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.
> 
> Read the qa-engineer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/engineering/qa-engineer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.
> 
> After the bootstrap completes, output the manifest summary the skill defines (detected languages, files created, files merged, next steps).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Testing Bootstrap Complete

### Detected languages
- **Python** (detected via `pyproject.toml`)

### Files created
- `docs/testing/test-config.md` — pytest configuration template, E2E Playwright config
- `docs/testing/ci-test-jobs.md` — GitHub Actions job templates for Python and E2E testing

### Files merged
- `docs/testing/CLAUDE.md` — appended domain conventions, framework reference, evidence requirements, tooling guidance, and available skills. Existing "Custom team notes" section preserved with USER-EDIT-SENTINEL-DO-NOT-STRIP marker intact.

### Next steps
- Review generated config templates and adjust for your project
- Add CI jobs to your `.github/workflows/ci.yml`
- Generate initial tests with `/qa-engineer:generate-tests`

### Artifacts written

#### `work/pyproject.toml`

```
[project]
name = "testproject"
version = "0.1.0"

```

#### `work/docs/testing/test-config.md`

```
# Test configuration

> Only includes config for languages detected in this project.

## Python (pytest)

### `pyproject.toml`

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks integration tests",
]
strict_markers = true
filterwarnings = ["error"]
addopts = "-v --tb=short"
```

Use factory fixtures in `conftest.py` for domain objects. Run coverage with `pytest --cov=src --cov-report=term-missing --cov-report=xml`.

## E2E (Playwright)

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  timeout: 30_000,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 4 : undefined,
  use: {
    baseURL: process.env.BASE_URL ?? 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
  ],
});
```

```

#### `work/docs/testing/ci-test-jobs.md`

```
# CI test jobs

GitHub Actions job templates. Copy the relevant job into your workflow and adjust paths.

## Python

```yaml
test-python:
  runs-on: ubuntu-latest
  timeout-minutes: 10
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.12'
        cache: 'pip'
    - run: pip install -e ".[test]"
    - run: timeout 120s pytest --cov=src --cov-report=xml -v
    - uses: actions/upload-artifact@v4
      if: failure()
      with:
        name: test-results-python
        path: coverage.xml
```

## E2E (Playwright)

```yaml
test-e2e:
  runs-on: ubuntu-latest
  timeout-minutes: 20
  strategy:
    matrix:
      shard: [1, 2]
      total-shards: [2]
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: '20'
        cache: 'npm'
    - run: npm ci
    - run: npx playwright install --with-deps chromium firefox
    - run: timeout 300s npx playwright test --shard=${{ matrix.shard }}/${{ matrix.total-shards }}
      env:
        BASE_URL: ${{ vars.STAGING_URL }}
    - uses: actions/upload-artifact@v4
      if: failure()
      with:
        name: playwright-report-${{ matrix.shard }}
        path: playwright-report/
```

Add SonarCloud coverage upload after test steps: `SonarSource/sonarcloud-github-action@v3` with `SONAR_TOKEN` secret.

```

#### `work/docs/testing/CLAUDE.md`

```
# Testing Domain

This directory covers test infrastructure, framework configuration, and CI test integration. Test strategy, quality gates, DoR, and DoD live in `docs/quality/` (owned by qa-lead).

## Custom team notes

USER-EDIT-SENTINEL-DO-NOT-STRIP

This section was written by the team and must survive any bootstrap re-run.
It exists to test the safe-merge contract: the bootstrap skill must not
overwrite or remove user-authored content.

<!-- Merged from qa-engineer bootstrap v0.1.0 -->

## What this domain covers

- Test framework setup and configuration per language
- Test directory structure and naming conventions
- CI job definitions for running tests
- Evidence format for test results
- E2E and integration test infrastructure

## Runner commands

| Stack | Command | Notes |
|-------|---------|-------|
| Python | `CI=true pytest --strict-markers -v` | Local: `pytest -v` |
| TypeScript | `CI=true npx vitest run` | Fallback: `CI=true npx jest`. NEVER watch mode in CI |
| C# | `dotnet test --verbosity normal` | N/A |
| E2E | `npx playwright test` | Debug locally with `--ui` |

## Test directory structure

```
tests/
├── e2e/
│   ├── smoke/           # Fast post-deployment checks
│   ├── acceptance/      # Full acceptance test suite
│   └── fixtures/        # Page objects, test data
├── unit/                # Or co-located: src/**/*.test.ts
└── integration/
```

Co-located unit tests (`src/**/*.test.ts`, `src/**/test_*.py`) are fine for smaller projects.

## Evidence requirements

Every test result must include: exact command (copy-pasteable), exit code, test count (passed/failed/skipped), duration. No vague "tests pass" claims. Show the output.

## Rules

- No `sleep()` — use `waitFor` (Playwright), `eventually` (pytest), `vi.advanceTimersByTime` (vitest)
- Timeout guards in CI: `timeout 120s` prefix
- Deterministic only. Flaky tests get quarantined or fixed, not re-run
- Each test file runnable in isolation

## Tooling

| Tool | Purpose |
|------|---------|
| GitHub Actions | CI test execution |
| SonarCloud | Coverage reporting and quality gate |
| Playwright | E2E browser testing |

## Available skills

| Skill | Purpose |
|-------|---------|
| `/qa-engineer:generate-tests` | Generate test files from specs or source code |
| `/qa-engineer:write-bug-report` | Write a structured bug report |

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 9.5/10.0 (95%) |
| Evaluated | 2026-05-13 |
| Target duration | 51801 ms |
| Target cost | $0.1757 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | After bootstrap, `docs/testing/CLAUDE.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim | PASS | CLAUDE.md artifact contains 'USER-EDIT-SENTINEL-DO-NOT-STRIP' on its own line inside the 'Custom team notes' section. |
| c2 | After bootstrap, `docs/testing/CLAUDE.md` contains the safe-merge marker `<!-- Merged from qa-engineer bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged | PASS | CLAUDE.md artifact contains the exact line '<!-- Merged from qa-engineer bootstrap v0.1.0 -->' between the user section and the appended content. |
| c3 | After bootstrap, `docs/testing/CLAUDE.md` contains the appended template sections — at minimum the "Runner commands" and "Evidence requirements" headings now appear alongside the preserved user content | PASS | CLAUDE.md artifact contains '## Runner commands' (with full table) and '## Evidence requirements' headings after the merge marker. |
| c4 | After bootstrap, `docs/testing/test-config.md` exists and contains the `## Python (pytest)` section (language filtering matched `pyproject.toml`) | PASS | test-config.md artifact exists and contains '## Python (pytest)' heading with full pyproject.toml pytest config block. |
| c5 | After bootstrap, `docs/testing/test-config.md` does NOT contain `## C# (xUnit)` — language filtering excluded C# because no `.csproj` or `.sln` was detected | PASS | test-config.md contains only '## Python (pytest)' and '## E2E (Playwright)' sections — no C# section present. |
| c6 | After bootstrap, `docs/testing/ci-test-jobs.md` exists and contains the `## Python` CI job | PASS | ci-test-jobs.md artifact exists and contains '## Python' heading with a full GitHub Actions job using actions/setup-python@v5 and pytest. |
| c7 | Chat output's manifest summary includes a "Detected languages" section naming Python | PASS | Chat output has '### Detected languages' with '- **Python** (detected via `pyproject.toml`)'. |
| c8 | Output names each created and merged file individually — a bare "bootstrap complete" without the per-file manifest is not enough | PASS | Chat output has '### Files created' listing test-config.md and ci-test-jobs.md, and '### Files merged' listing CLAUDE.md with per-file descriptions. |
| c9 | Output does not claim it overwrote or replaced `docs/testing/CLAUDE.md` — the language reflects merge, not replacement | PASS | Chat says 'appended domain conventions... Existing "Custom team notes" section preserved with USER-EDIT-SENTINEL-DO-NOT-STRIP marker intact.' No overwrite language. |
| c10 | Output points the reader at next steps consistent with the skill's documented manifest (reviewing config templates, adding CI jobs, using `/qa-engineer:generate-tests`) | PARTIAL | Next steps list all three: 'Review generated config templates', 'Add CI jobs to your `.github/workflows/ci.yml`', 'Generate initial tests with `/qa-engineer:generate-tests`'. |

### Notes

All ten criteria are met cleanly. The artifacts confirm the safe-merge contract was honoured (sentinel preserved, marker inserted, new sections appended), language filtering excluded C#, and the chat manifest accurately describes each file outcome. c10 is capped at PARTIAL by the test author.
