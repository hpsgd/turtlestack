# Bootstrap

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/performance/CLAUDE.md` containing a user-authored section. The performance-engineer bootstrap skill should preserve that user content while appending the template's missing sections (with a merge marker), and should create the file the fixture is missing — `performance-budget.md`. The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

> The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/performance/CLAUDE.md` is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.
> 
> Read the performance-engineer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/engineering/performance-engineer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.
> 
> After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Performance Bootstrap Complete

### Files created
- `docs/performance/performance-budget.md` — performance budget template

### Files merged
- `docs/performance/CLAUDE.md` — merged 8 missing sections (What This Domain Covers, Core Web Vitals, USE Method, RED Method, Performance Budget Enforcement, Load Testing Conventions, Tooling, Available Skills, Conventions) while preserving user-authored Custom team notes section

### Next steps
- Fill in performance budgets based on project requirements
- Set up Lighthouse CI in GitHub Actions
- Use `/performance-engineer:load-test-plan` for load testing

### Artifacts written

#### `work/docs/performance/performance-budget.md`

```
# Performance Budget — TestProject

> Replace [Project Name] with the actual project name.

## Frontend Budget

### Core Web Vitals

| Metric | Target | CI Threshold | Measurement |
|--------|--------|-------------|-------------|
| LCP | <= 2.5s | <= 3.0s | Lighthouse CI |
| INP | <= 200ms | <= 250ms | Real user monitoring |
| CLS | <= 0.1 | <= 0.15 | Lighthouse CI |

### Bundle Size

| Route / Entry | Budget | Current |
|---------------|--------|---------|
| Main bundle | KB | KB |
| Vendor bundle | KB | KB |
| Per-route chunk | KB | KB |
| Total initial load | KB | KB |

### Resource Limits

| Resource | Budget |
|----------|--------|
| Total page weight | KB |
| Images per page | KB |
| Fonts | KB |
| Third-party scripts | KB |

## Backend Budget

### API Response Times

| Endpoint Category | p50 | p95 | p99 |
|-------------------|-----|-----|-----|
| Read (simple) | ms | ms | ms |
| Read (complex/search) | ms | ms | ms |
| Write (create/update) | ms | ms | ms |
| Batch operations | ms | ms | ms |

### Throughput

| Scenario | Target RPS | Current |
|----------|-----------|---------|
| Normal load | | |
| Peak load | | |
| Burst (2x peak) | | |

## Monitoring

| Metric | Tool | Alert Threshold |
|--------|------|-----------------|
| Core Web Vitals | Vercel Analytics | Any metric "Needs Improvement" |
| API latency p99 | Application metrics | > budget by 20% |
| Error rate | Application metrics | > 0.1% |
| Bundle size | CI (GitHub Actions) | > budget |

## Review Schedule

- **Weekly**: check real user Core Web Vitals trends
- **Per release**: validate against budget in staging
- **Quarterly**: review and adjust budgets based on user data

```

#### `work/docs/performance/CLAUDE.md`

```
# Performance Domain

This directory contains performance documentation for the project.

## Custom team notes

USER-EDIT-SENTINEL-DO-NOT-STRIP

This section was written by the team and must survive any bootstrap re-run.
It exists to test the safe-merge contract: the bootstrap skill must not
overwrite or remove user-authored content.

<!-- Merged from performance-engineer bootstrap v0.1.0 -->

## What This Domain Covers

- **Performance budgets** — thresholds for Core Web Vitals and API response times
- **Load testing** — methodology, scenarios, and results
- **Profiling** — CPU, memory, and I/O analysis
- **Capacity planning** — growth projections and scaling strategies

## Core Web Vitals

Google's Core Web Vitals are the primary frontend performance metrics:

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| **LCP** (Largest Contentful Paint) | <= 2.5s | 2.5–4.0s | > 4.0s |
| **INP** (Interaction to Next Paint) | <= 200ms | 200–500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | <= 0.1 | 0.1–0.25 | > 0.25 |

### Targets
- All pages must score "Good" on all three Core Web Vitals
- Measured at the 75th percentile of real user data
- Enforced in CI via Lighthouse or equivalent

## USE Method (Infrastructure)

For backend/infrastructure performance, apply the USE method per resource:

| Component | Utilisation | Saturation | Errors |
|-----------|-------------|------------|--------|
| CPU | % busy | Run queue length | Hardware errors |
| Memory | % used | Swap usage | OOM kills |
| Disk I/O | % busy | Wait queue | Read/write errors |
| Network | Bandwidth % | Dropped packets | Connection errors |

## RED Method (Services)

For microservice performance, track:

| Metric | Description | Target |
|--------|-------------|--------|
| **R**ate | Requests per second | Baseline + growth margin |
| **E**rrors | Error rate (%) | < 0.1% for critical paths |
| **D**uration | Latency (p50, p95, p99) | See performance budget |

## Performance Budget Enforcement

Performance budgets are enforced as CI gates:

1. **Build-time** — bundle size limits (webpack/vite budget)
2. **Synthetic** — Lighthouse score thresholds in CI
3. **Real user** — Core Web Vitals monitoring in production

### Budget violations
- Blocking: budget exceeded by > 10% → PR cannot merge
- Warning: budget exceeded by 1–10% → PR flagged for review
- Tracking: all metrics logged for trend analysis

## Load Testing Conventions

### When to load test
- Before major releases
- After significant architecture changes
- When onboarding high-traffic clients
- Quarterly baseline tests

### Load test types

| Type | Purpose | Duration |
|------|---------|----------|
| Smoke | Verify system works under minimal load | 1–2 min |
| Load | Validate performance under expected load | 10–30 min |
| Stress | Find breaking point | 15–30 min |
| Soak | Detect memory leaks, resource exhaustion | 1–4 hours |

## Tooling

| Tool | Purpose |
|------|---------|
| GitHub Actions | Performance CI gate (Lighthouse, bundle analysis) |
| Vercel Analytics | Real user Core Web Vitals monitoring |

## Available Skills

| Skill | Purpose |
|-------|---------|
| `/performance-engineer:load-test-plan` | Create a load testing plan |
| `/performance-engineer:performance-profile` | Profile and analyse performance |
| `/performance-engineer:capacity-plan` | Plan capacity for growth |

## Conventions

- Performance budgets are set early and only relaxed with an ADR
- Every API endpoint has a p99 latency target
- Bundle size is tracked per-route for frontend applications
- Load test results are stored in `docs/performance/results/` for comparison
- Performance regressions are treated as bugs — fix within the sprint

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 9.5/9.5 (100%) |
| Evaluated | 2026-05-13 |
| Target duration | 50477 ms |
| Target cost | $0.1444 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | After bootstrap, `docs/performance/CLAUDE.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim | PASS | Artifact `work/docs/performance/CLAUDE.md` contains the exact line `USER-EDIT-SENTINEL-DO-NOT-STRIP` within the preserved 'Custom team notes' section. |
| c2 | After bootstrap, `docs/performance/CLAUDE.md` contains the safe-merge marker `<!-- Merged from performance-engineer bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged | PASS | Artifact contains `<!-- Merged from performance-engineer bootstrap v0.1.0 -->` on a line immediately after the user-authored section. |
| c3 | After bootstrap, `docs/performance/CLAUDE.md` contains the appended template sections — at minimum the "Core Web Vitals" and "USE Method (Infrastructure)" headings now appear alongside the preserved user content | PASS | Artifact contains both `## Core Web Vitals` and `## USE Method (Infrastructure)` headings after the safe-merge marker, alongside the preserved user content. |
| c4 | After bootstrap, `docs/performance/performance-budget.md` exists and was created from the skill's template | PASS | Artifact `work/docs/performance/performance-budget.md` is present and contains `# Performance Budget — TestProject` from the skill's template. |
| c5 | The created `performance-budget.md` contains a "## Frontend Budget" section and a "## Backend Budget" section | PASS | Artifact contains both `## Frontend Budget` with Core Web Vitals/Bundle Size tables and `## Backend Budget` with API Response Times/Throughput tables. |
| c6 | Chat output includes a manifest summary (`## Performance Bootstrap Complete`) that lists files created and files merged | PASS | Chat response opens with `## Performance Bootstrap Complete` followed by `### Files created` and `### Files merged` subsections. |
| c7 | Chat output includes a `### Next steps` section pointing to relevant next actions (e.g. filling in budgets, setting up Lighthouse CI, or using `/performance-engineer:load-test-plan`) | PASS | `### Next steps` lists: fill in performance budgets, set up Lighthouse CI in GitHub Actions, use `/performance-engineer:load-test-plan`. |
| c8 | Output names each created and merged file individually — a bare "bootstrap complete" without the per-file manifest is not enough | PASS | Output names `docs/performance/performance-budget.md` under Files created and `docs/performance/CLAUDE.md` under Files merged, each with a description. |
| c9 | Output does not claim it overwrote or replaced `docs/performance/CLAUDE.md` — the language reflects merge, not replacement | PASS | Output states 'merged 8 missing sections … while preserving user-authored Custom team notes section' — explicit merge language, no overwrite claim. |
| c10 | Output points the reader at next steps consistent with the skill's documented manifest (Lighthouse CI setup, load test plan skill) | PARTIAL | Next steps explicitly mention 'Set up Lighthouse CI in GitHub Actions' and 'Use `/performance-engineer:load-test-plan` for load testing' — both documented manifest items present. |

### Notes

The skill executed flawlessly: the sentinel was preserved, the merge marker applied, all template sections appended, and the missing file created. The manifest summary in chat was well-structured and accurate.
