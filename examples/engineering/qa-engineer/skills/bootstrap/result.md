# Bootstrap

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a `pyproject.toml` (marking it as a Python project) and a partial `docs/testing/_sections/qa-engineer.md` fragment containing a user-authored section. The qa-engineer bootstrap skill should detect Python, preserve the user content while appending missing sections (with a merge marker), and create the two new files — `docs/testing/test-config.md` and `docs/testing/ci-test-jobs.md` — filtered to Python only. The qa-engineer never writes `docs/testing/CLAUDE.md` directly — the coordinator assembles it from the fragments in `_sections/`. The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

> The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A `pyproject.toml` is present at the root. A partial `docs/testing/_sections/qa-engineer.md` fragment is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.
> 
> Read the qa-engineer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/engineering/qa-engineer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.
> 
> After the bootstrap completes, output the manifest summary the skill defines (detected languages, files created, files merged, next steps).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

---

## Testing Bootstrap Complete

### Detected languages
- **Python** — detected from `pyproject.toml` presence at project root

### Files created
- `docs/testing/test-config.md` — framework config templates (Python + E2E Playwright)
- `docs/testing/ci-test-jobs.md` — GitHub Actions job templates (Python + E2E Playwright)

### Files merged
- `docs/testing/_sections/qa-engineer.md` — existing file with user-authored "Custom team notes" preserved; template sections (What this domain covers, Runner commands, Test directory structure, Evidence requirements, Rules, Tooling, Available skills) inserted before custom section with merge marker `<!-- Merged from qa-engineer bootstrap v0.1.0 -->`

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

#### `work/docs/testing/_sections/qa-engineer.md`

```
<!-- qa-engineer fragment of the testing domain doc. Assembled into docs/testing/CLAUDE.md by the coordinator. -->

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
| Score | 11.5/11.5 (100%) |
| Evaluated | 2026-06-15 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 57183 ms |
| Target cost | $0.1110 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | After bootstrap, `docs/testing/_sections/qa-engineer.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim | PASS | Artifact shows '## Custom team notes' section with 'USER-EDIT-SENTINEL-DO-NOT-STRIP' intact on its own line. |
| c2 | After bootstrap, `docs/testing/_sections/qa-engineer.md` contains the safe-merge marker `<!-- Merged from qa-engineer bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged | PASS | Artifact line 3: '<!-- Merged from qa-engineer bootstrap v0.1.0 -->' present near top of file. |
| c3 | After bootstrap, `docs/testing/_sections/qa-engineer.md` contains the appended template sections — at minimum the "Runner commands" and "Evidence requirements" headings now appear alongside the preserved user content | PASS | Artifact contains '## Runner commands' table and '## Evidence requirements' section both present before the preserved custom section. |
| c4 | The qa-engineer fragment is authored at H2 and below — it does not introduce a `# Testing Domain` H1 (the coordinator generates that when it assembles `docs/testing/CLAUDE.md`) | PASS | Artifact opens with HTML comment and merge marker; first heading is '## What this domain covers' (H2). No H1 present. |
| c5 | The skill does NOT write `docs/testing/CLAUDE.md` directly — that file is the coordinator's to assemble from `_sections/` | PASS | Artifacts list only: pyproject.toml, test-config.md, ci-test-jobs.md, _sections/qa-engineer.md. No docs/testing/CLAUDE.md written. |
| c6 | After bootstrap, `docs/testing/test-config.md` exists and contains the `## Python (pytest)` section (language filtering matched `pyproject.toml`) | PASS | Artifact work/docs/testing/test-config.md contains '## Python (pytest)' heading with full pytest config block. |
| c7 | After bootstrap, `docs/testing/test-config.md` does NOT contain `## C# (xUnit)` — language filtering excluded C# because no `.csproj` or `.sln` was detected | PASS | Artifact test-config.md has only '## Python (pytest)' and '## E2E (Playwright)' sections; no C# section present. |
| c8 | After bootstrap, `docs/testing/ci-test-jobs.md` exists and contains the `## Python` CI job | PASS | Artifact work/docs/testing/ci-test-jobs.md contains '## Python' with full GitHub Actions yaml job 'test-python'. |
| c9 | Chat output's manifest summary includes a "Detected languages" section naming Python | PASS | Chat response section '### Detected languages' lists '**Python** — detected from `pyproject.toml` presence at project root'. |
| c10 | Output names each created and merged file individually — a bare "bootstrap complete" without the per-file manifest is not enough | PASS | '### Files created' lists both test-config.md and ci-test-jobs.md; '### Files merged' names qa-engineer.md individually. |
| c11 | Output does not claim it overwrote or replaced `docs/testing/_sections/qa-engineer.md` — the language reflects merge, not replacement | PASS | Chat says 'existing file with user-authored "Custom team notes" preserved; template sections … inserted before custom section with merge marker'. |
| c12 | Output points the reader at next steps consistent with the skill's documented manifest (reviewing config templates, adding CI jobs, using `/qa-engineer:generate-tests`) | PARTIAL | '### Next steps' lists: review config templates, add CI jobs to .github/workflows/ci.yml, and '/qa-engineer:generate-tests' — all three match. |

### Notes

The skill executed flawlessly across all criteria: safe-merge preserved user content and sentinel, language filtering excluded C#, the coordinator boundary (no CLAUDE.md written) was respected, and the manifest summary was complete and accurate. No gaps found.
