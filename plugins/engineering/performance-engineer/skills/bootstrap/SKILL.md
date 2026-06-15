---
name: bootstrap
bootstrap-phase: engineering
description: "Bootstrap the performance documentation structure for a project. Creates docs/performance/, generates initial templates, and writes the performance-engineer fragment of the performance domain doc (the coordinator assembles docs/performance/CLAUDE.md). Idempotent — merges missing sections into existing files without overwriting."
argument-hint: "[project name]"
user-invocable: false
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Bootstrap Performance Documentation

Bootstrap the performance documentation structure for **$ARGUMENTS**.

## Process

### Step 1: Check and create domain directory

```bash
mkdir -p docs/performance docs/performance/_sections
```

### Step 2: Create or merge files

For each file below, apply the safe merge pattern:
- If file does not exist → create from template
- If file exists → read both, find sections in template missing from file, append missing sections with `<!-- Merged from performance-engineer bootstrap v0.1.0 -->`

#### Fragment: `docs/performance/_sections/performance-engineer.md`

`docs/performance/CLAUDE.md` is **assembled by the coordinator** from the fragments in `_sections/` — no plugin
writes it directly. Write the performance-engineer's contribution as this fragment. It starts at H2 (the
coordinator generates the `# Performance Domain` H1 and a one-line intro). Create it with this content:

```markdown
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

#### File 2: `docs/performance/performance-budget.md`

Create with this content:

```markdown
# Performance Budget — [Project Name]

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

### Step 3: Return manifest

After creating/merging all files, output a summary:

```
## Performance Bootstrap Complete

### Files created
- `docs/performance/_sections/performance-engineer.md` — performance-engineer fragment (coordinator assembles `docs/performance/CLAUDE.md` from it)
- `docs/performance/performance-budget.md` — performance budget template

### Files merged
- (list any existing files where sections were appended)

### Next steps
- Fill in performance budgets based on project requirements
- Set up Lighthouse CI in GitHub Actions
- Use `/performance-engineer:load-test-plan` for load testing
```
