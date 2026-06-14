---
name: bootstrap
bootstrap-phase: engineering
description: "Bootstrap the testing documentation structure for a project. Creates docs/testing/, generates initial templates, and writes domain CLAUDE.md. Idempotent — merges missing sections into existing files without overwriting."
argument-hint: "[project name]"
user-invocable: false
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Bootstrap Testing Documentation

Bootstrap the testing documentation structure for **$ARGUMENTS**.

## Process

### Step 0: Detect tech context

If tech context was provided by the coordinator bootstrap, use it. Otherwise, scan the project:

```bash
ls package.json tsconfig.json 2>/dev/null                     # TypeScript
ls pyproject.toml requirements.txt setup.py 2>/dev/null       # Python
find . -maxdepth 3 \( -name '*.csproj' -o -name '*.sln' \) 2>/dev/null | head -5  # C#
```

If ambiguous, list what was found and ask the user. Set `$LANGS` to detected languages. Only include config and CI sections for those languages.

### Step 1: Create domain directory

```bash
mkdir -p docs/testing
```

### Step 2: Create or merge files

For each file, apply the safe merge pattern:

- If file does not exist -> create from template
- If file exists -> read both, find missing sections, append with `<!-- Merged from qa-engineer bootstrap v0.1.0 -->`

#### File 1: `docs/testing/CLAUDE.md`

```markdown
# Testing Domain

This directory covers test infrastructure, framework configuration, and CI test integration. Test strategy, quality gates, DoR, and DoD live in `docs/quality/` (owned by qa-lead).

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

#### File 2: `docs/testing/test-config.md`

Only include sections for detected languages. Create with relevant sections from below:

```markdown
# Test configuration

> Only includes config for languages detected in this project.

<!-- PYTHON — include if python in $LANGS -->

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

<!-- TYPESCRIPT — include if typescript in $LANGS -->

## TypeScript (vitest)

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    // Only add environment: 'jsdom' if testing browser code.
    include: ['src/**/*.test.ts', 'tests/**/*.test.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'lcov'],
      exclude: ['node_modules/', 'tests/fixtures/'],
    },
  },
});
```

<!-- CSHARP — include if csharp in $LANGS -->

## C# (xUnit)

Use xUnit + NSubstitute + Shouldly + coverlet. Add a `.runsettings` file for coverage:

```xml
<?xml version="1.0" encoding="utf-8"?>
<RunSettings>
  <DataCollectionRunSettings>
    <DataCollectors>
      <DataCollector friendlyName="XPlat Code Coverage">
        <Configuration>
          <Format>opencover</Format>
          <ExcludeByFile>**/Migrations/**</ExcludeByFile>
        </Configuration>
      </DataCollector>
    </DataCollectors>
  </DataCollectionRunSettings>
</RunSettings>
```

<!-- E2E — include if any language detected -->

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

#### File 3: `docs/testing/ci-test-jobs.md`

Only include sections for detected languages. Create with relevant sections from below:

```markdown
# CI test jobs

GitHub Actions job templates. Copy the relevant job into your workflow and adjust paths.

<!-- PYTHON — include if python in $LANGS -->

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

<!-- TYPESCRIPT — include if typescript in $LANGS -->

## TypeScript

```yaml
test-typescript:
  runs-on: ubuntu-latest
  timeout-minutes: 10
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: '20'
        cache: 'npm'
    - run: npm ci
    - run: timeout 120s npx vitest run --coverage
      env:
        CI: true
    - uses: actions/upload-artifact@v4
      if: failure()
      with:
        name: test-results-typescript
        path: coverage/
```

<!-- CSHARP — include if csharp in $LANGS -->

## C#

```yaml
test-dotnet:
  runs-on: ubuntu-latest
  timeout-minutes: 15
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-dotnet@v4
      with:
        dotnet-version: '8.0.x'
    - run: dotnet restore
    - run: >-
        timeout 120s dotnet test --no-restore --verbosity normal
        --collect:"XPlat Code Coverage" --settings .runsettings
    - uses: actions/upload-artifact@v4
      if: failure()
      with:
        name: test-results-dotnet
        path: '**/TestResults/'
```

<!-- E2E — include if any frontend detected -->

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

### Step 3: Return manifest

After creating/merging all files, output a summary:

```
## Testing Bootstrap Complete

### Detected languages
- (list detected languages and how they were detected)

### Files created
- `docs/testing/CLAUDE.md` — domain conventions, framework reference, evidence requirements
- `docs/testing/test-config.md` — framework config templates (filtered to detected languages)
- `docs/testing/ci-test-jobs.md` — GitHub Actions job templates (filtered to detected languages)

### Files merged
- (list any existing files where sections were appended)

### Next steps
- Review generated config templates and adjust for your project
- Add CI jobs to your `.github/workflows/ci.yml`
- Generate initial tests with `/qa-engineer:generate-tests`
```
