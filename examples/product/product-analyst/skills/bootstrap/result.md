# Bootstrap

Scenario: A contributor sets up product-analytics documentation for a new project. The skill must create `docs/analytics/` with the product-analyst fragment, a metric-tree template, and an instrumentation-spec template, leave empty placeholder rows rather than inventing metric values, and return a manifest — without overwriting any existing file. The product-analyst never writes `docs/analytics/CLAUDE.md` directly; the coordinator assembles it from the fragments in `_sections/`.

## Prompt

> Use the product-analyst `bootstrap` skill to set up the product-analytics documentation structure for a project called "Cadence". Create the structure under `docs/analytics/` relative to the current working directory and return the bootstrap manifest in the skill's standard format.
> 
> Proceed without asking — create the files and return the manifest.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Product Analytics Bootstrap Complete

### Files created
- `docs/analytics/_sections/product-analyst.md` — product-analyst fragment (coordinator assembles `docs/analytics/CLAUDE.md` from it)
- `docs/analytics/metric-tree.md` — North Star and metric-hierarchy template
- `docs/analytics/instrumentation-spec.md` — data-engineer hand-off template

### Files merged
- (none — this is a fresh bootstrap)

### Next steps
- Define the North Star with `/product-analyst:define-north-star`
- Build the metric hierarchy with `/product-analyst:design-metric-hierarchy`
- Write the instrumentation spec and hand it to the data-engineer

### Artifacts written

#### `work/docs/analytics/instrumentation-spec.md`

```
# Cadence Instrumentation Spec

**Audience:** Data Engineer  
**Owner:** Product Analyst  
**Status:** Draft

## Overview

This spec defines the events, properties, and identity model required to measure Cadence's success metrics (see `metric-tree.md`).

## Identity Model

| Entity | Identifier | Properties |
|--------|-----------|-----------|
| User | | |
| Session | | |
| Account | | |

## Event Taxonomy

### Event Categories

- **User Actions** — Direct user interactions (clicks, submissions, navigations)
- **System Events** — App state changes (errors, feature flags, deployments)
- **Business Events** — Transactions and outcomes (payments, conversions, churn)

## Events Table

| Event Name | Trigger | Properties | Metric(s) Fed |
|------------|---------|-----------|---------------|
| | | | |
| | | | |
| | | | |

## Property Standards

### User Properties

| Property | Type | Values | Use |
|----------|------|--------|-----|
| | | | |
| | | | |

### Session Properties

| Property | Type | Values | Use |
|----------|------|--------|-----|
| | | | |
| | | | |

### Event Properties

| Property | Type | Values | Use |
|----------|------|--------|-----|
| | | | |
| | | | |

## Attribution Model

Describe how events are attributed to users, cohorts, and campaigns:

- **Attribution window:** (e.g., last-click, 30-day lookback)
- **Cohort assignment:** (e.g., by signup date, feature flag cohort)
- **Campaign tagging:** (e.g., utm_source, utm_medium)

## Test Accounts & Filters

List accounts and conditions to exclude from metrics:

- Internal test accounts: `[list IDs or emails]`
- Bot detection rule: 
- Feature flag filters:

## Sampling & Granularity

- **Sampling rate:** (e.g., 100% for all users, 10% for high-volume events)
- **Granularity:** (e.g., per-session vs per-user roll-up)

## Retention & Warehousing

- **Event retention:** (e.g., 13 months)
- **Warehouse destination:** (e.g., Snowflake, BigQuery, Redshift)
- **Partitioning:** (e.g., by date, by user_id)

## Sign-Off

- **Analyst:** _____ (Date: _____)
- **Data Engineer:** _____ (Date: _____)

```

#### `work/docs/analytics/metric-tree.md`

```
# Cadence Metric Tree

## North Star Metric

| Field | Value |
|-------|-------|
| **Metric** | |
| **Definition** | |
| **Question it answers** | |
| **Granularity** | |
| **Time window** | |
| **Owner** | |

## Input Metrics (HEART / AARRR)

### Happiness

| Metric | Definition | Owner |
|--------|-----------|-------|
| | | |
| | | |

### Engagement

| Metric | Definition | Owner |
|--------|-----------|-------|
| | | |
| | | |

### Adoption

| Metric | Definition | Owner |
|--------|-----------|-------|
| | | |
| | | |

### Retention

| Metric | Definition | Owner |
|--------|-----------|-------|
| | | |
| | | |

### Task Success

| Metric | Definition | Owner |
|--------|-----------|-------|
| | | |
| | | |

## Metric Relationship Map

```
[North Star]
    |
    +-- [Happiness]
    |       +-- [Sub-metric]
    |       +-- [Sub-metric]
    |
    +-- [Engagement]
    |       +-- [Sub-metric]
    |       +-- [Sub-metric]
    |
    +-- [Retention]
            +-- [Sub-metric]
            +-- [Sub-metric]
```

## Goodhart Checks

For each input metric, document the gaming risk:

| Metric | Goodhart Risk | Mitigation |
|--------|---------------|-----------|
| | | |
| | | |

## Related OKRs

Link to the OKRs this metric tree serves (product-manager domain).

```

#### `work/docs/analytics/_sections/product-analyst.md`

```
## What this domain covers

- **North Star Metric** — the single number capturing delivered customer value
- **Metric hierarchy** — input metrics that drive the North Star (HEART or AARRR)
- **Instrumentation specs** — events, properties, identity model, attribution (handed to data-engineer)
- **Cohort and retention analysis** — retention curves and segment cuts
- **Experiment design** — A/B and holdout tests with sample-size calculations

## Ownership boundary

The product-analyst defines *what* to measure and *why*. The data-engineer builds *how* data
flows (pipelines, warehouse, dashboards). Instrumentation specs are written here and handed off
for implementation. OKRs live with the product-manager; metrics here serve those OKRs.

## Metric definition standard

Every metric carries a definition block before implementation:

- **Question it answers** — the decision the number informs
- **Definition** — precise and unambiguous
- **Calculation** — exact formula or query logic
- **Granularity** — per user / session / account / cohort
- **Filters** — bots, test accounts, internal users (explicit)
- **Time window** — rolling 7d / calendar month / since signup
- **Goodhart risk** — how it could be gamed and who it would hurt
- **Owner** — who approves a definition change

## Conventions

- The North Star measures customer value, never company revenue directly
- Run the Goodhart check on every metric before promoting it
- Vanity metrics (cumulative totals) are never a North Star or an input
- Correlation is the default; causation requires an experiment
- Evidence hierarchy: observed behaviour > stated intent > opinion
- One file per artifact under `docs/analytics/`

## Available skills

| Skill | Purpose |
|-------|---------|
| `/product-analyst:define-north-star` | Define the North Star Metric and its input metrics |
| `/product-analyst:design-metric-hierarchy` | Build a HEART or AARRR metric tree tied to OKRs |
| `/product-analyst:write-instrumentation-spec` | Specify events for the data-engineer to implement |
| `/product-analyst:cohort-analysis` | Analyse retention curves and segment cuts |
| `/product-analyst:design-experiment` | Design an A/B or holdout experiment |

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 13.5/13.5 (100%) |
| Evaluated | 2026-06-15 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 48213 ms |
| Target cost | $0.0967 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Creates the `docs/analytics/` directory (the one canonical path — not `docs/product-analytics/` or a variant) with a `_sections/` subdirectory for the domain fragment | PASS | Artifacts at `work/docs/analytics/_sections/product-analyst.md`, `work/docs/analytics/metric-tree.md`, `work/docs/analytics/instrumentation-spec.md` confirm canonical path. |
| c2 | Writes `docs/analytics/_sections/product-analyst.md` as the domain fragment | PASS | Artifact `work/docs/analytics/_sections/product-analyst.md` is present and contains the full domain fragment. |
| c3 | The fragment is authored at H2 and below — it does not introduce a `# Analytics Domain` H1 (the coordinator generates that when it assembles `docs/analytics/CLAUDE.md`) | PASS | Fragment starts with `## What this domain covers` — no H1 present anywhere in the file. |
| c4 | The skill does NOT write `docs/analytics/CLAUDE.md` directly — that file is the coordinator's to assemble from `_sections/` | PASS | No `CLAUDE.md` appears in the artifacts. Chat response explicitly notes "coordinator assembles `docs/analytics/CLAUDE.md` from it". |
| c5 | Writes `docs/analytics/metric-tree.md` (North Star + metric-hierarchy template) and `docs/analytics/instrumentation-spec.md` (data-engineer hand-off template) | PASS | Both `work/docs/analytics/metric-tree.md` and `work/docs/analytics/instrumentation-spec.md` are present in artifacts. |
| c6 | The fragment states the ownership boundary — the product-analyst defines what to measure and why; the data-engineer builds how data flows (pipelines, warehouse, dashboards) | PASS | "## Ownership boundary" section: "The product-analyst defines *what* to measure and *why*. The data-engineer builds *how* data flows (pipelines, warehouse, dashboards)." |
| c7 | The fragment states the metric-definition standard (question it answers, definition, calculation, granularity, filters, time window, Goodhart risk, owner) | PASS | "## Metric definition standard" lists all 8 required fields: question it answers, definition, calculation, granularity, filters, time window, Goodhart risk, owner. |
| c8 | The fragment states conventions — North Star measures customer value not company revenue, Goodhart check on every metric, vanity/cumulative totals are never a North Star | PASS | "## Conventions": "North Star measures customer value, never company revenue directly", "Run the Goodhart check on every metric", "Vanity metrics (cumulative totals) are never a North Star or an input". |
| c9 | Does not invent metric values during bootstrap — templates ship with empty placeholder rows, not fabricated North Star or input metrics for "Cadence" | PASS | `metric-tree.md` North Star table has empty Value cells; HEART tables have empty rows. `instrumentation-spec.md` Events Table and Property tables all contain empty rows. |
| c10 | Returns a manifest listing files created, files merged (or "none"), and next steps — not arbitrary prose | PASS | Chat response has structured sections: "### Files created", "### Files merged" (with "none — fresh bootstrap"), "### Next steps". |
| c11 | `docs/analytics/_sections/product-analyst.md` exists and lists the available product-analyst skills (define-north-star, design-metric-hierarchy, write-instrumentation-spec, cohort-analysis, design-experiment) | PASS | "## Available skills" table lists all 5 skills: define-north-star, design-metric-hierarchy, write-instrumentation-spec, cohort-analysis, design-experiment. |
| c12 | `docs/analytics/metric-tree.md` and `docs/analytics/instrumentation-spec.md` exist with template structure and empty placeholder rows, not invented data | PASS | Both files present with full template structure (headers, tables, sections) and empty rows — no fabricated metric names or values for "Cadence". |
| c13 | The manifest names the created files and a "Next steps" section pointing at define-north-star and design-metric-hierarchy | PASS | Manifest lists 3 files created; "### Next steps" cites "/product-analyst:define-north-star" and "/product-analyst:design-metric-hierarchy" explicitly. |
| c14 | The manifest reports a "Files merged" line as "none" given a clean project (idempotency awareness) | PARTIAL | "### Files merged" section present with "(none — this is a fresh bootstrap)" — explicit idempotency awareness shown. |

### Notes

The skill produced a perfect bootstrap: all three files created at correct canonical paths, fragment correctly scoped to H2+, CLAUDE.md not written directly, all template content uses empty placeholder rows, and the manifest is properly structured. No gaps found across any criterion.
