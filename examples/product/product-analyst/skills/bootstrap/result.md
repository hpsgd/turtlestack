# Bootstrap

Scenario: A contributor sets up product-analytics documentation for a new project. The skill must create `docs/analytics/` with a domain CLAUDE.md, a metric-tree template, and an instrumentation-spec template, leave empty placeholder rows rather than inventing metric values, and return a manifest — without overwriting any existing file.

## Prompt

> Use the product-analyst `bootstrap` skill to set up the product-analytics documentation structure for a project called "Cadence". Create the structure under `docs/analytics/` relative to the current working directory and return the bootstrap manifest in the skill's standard format.
> 
> Proceed without asking — create the files and return the manifest.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Product Analytics Bootstrap Complete

### Files created
- `docs/analytics/CLAUDE.md` — domain conventions and skill reference
- `docs/analytics/metric-tree.md` — North Star and metric-hierarchy template
- `docs/analytics/instrumentation-spec.md` — data-engineer hand-off template

### Files merged
- None (fresh bootstrap)

### Next steps
- Define the North Star with `/product-analyst:define-north-star`
- Build the metric hierarchy with `/product-analyst:design-metric-hierarchy`
- Write the instrumentation spec and hand it to the data-engineer

### Artifacts written

#### `work/docs/analytics/instrumentation-spec.md`

```
# Cadence Instrumentation Specification

Instrumentation specification for the data-engineer. Defines all events, properties, identity model, and attribution logic needed to measure the metrics in `metric-tree.md`.

## Overview

This spec is the hand-off contract between product analytics and the data-engineer. It specifies:
- Every event to be tracked
- Event properties and payload schema
- User identity model (pseudonymous / identified / account-level)
- Session and user ID handling
- Attribution logic (first-touch / last-touch / linear)
- Data quality rules and validation

## Identity Model

- **User ID source**: (how do we identify users?)
- **Session ID**: (how do we identify sessions?)
- **Account ID**: (if applicable)
- **Anonymous handling**: (how do we handle unidentified visitors?)

## Events

Core events to be instrumented. For each event, specify:
- Event name
- Trigger (when is it fired?)
- Properties (data payload)
- Cardinality constraints (how often per user/session?)
- Mandatory fields (user_id, session_id, timestamp, etc.)

| Event Name | Trigger | Key Properties | Cardinality | Notes |
|------------|---------|-----------------|-------------|-------|
| (event name) | (when) | (properties) | (frequency) | (validation rules) |
| (event name) | (when) | (properties) | (frequency) | (validation rules) |

## Property Dictionary

Standard properties sent with every event.

| Property | Type | Description | Example |
|----------|------|-------------|---------|
| `timestamp` | ISO 8601 | Event time (UTC) | `2026-06-13T14:30:00Z` |
| `user_id` | string | Identified user | `user_12345` |
| `session_id` | string | Session token | `sess_abc123` |
| `app_version` | string | Client version | `1.2.3` |
| `platform` | enum | Device platform | `web` / `ios` / `android` |

## Attribution Model

How do we attribute conversions to campaigns, features, or user journeys?

- **Attribution type**: (first-touch / last-touch / linear / time-decay)
- **Touch window**: (how many days between first and conversion?)
- **Channel mapping**: (how do we classify traffic sources?)

## Data Quality

Quality gates and validation rules applied by the data warehouse.

| Rule | Check | Action if Failed |
|------|-------|------------------|
| (rule name) | (validation) | (reject event / flag / alert) |
| (rule name) | (validation) | (reject event / flag / alert) |

## Handoff Checklist

Before handing this spec to the data-engineer:

- [ ] All events in the instrumentation spec are tied to metrics in `metric-tree.md`
- [ ] Identity model is unambiguous (no circular deps between user/session/account)
- [ ] Property dictionary covers all mandatory and optional fields
- [ ] Attribution logic is defined (or documented as "no attribution needed")
- [ ] Data quality rules are explicitly stated
- [ ] The data-engineer has signed off on feasibility and timeline

```

#### `work/docs/analytics/metric-tree.md`

```
# Cadence North Star and Metric Hierarchy

## North Star Metric

The single measure of delivered customer value for Cadence.

| Field | Value |
|-------|-------|
| **Metric** | (to be defined) |
| **Definition** | (precise and unambiguous) |
| **Calculation** | (exact formula or query logic) |
| **Granularity** | (per user / session / account / cohort) |
| **Time window** | (rolling 7d / calendar month / since signup) |
| **Goodhart risk** | (how it could be gamed and who it would hurt) |
| **Owner** | (who approves a definition change) |

## Metric Hierarchy

Input metrics that drive the North Star. Choose HEART or AARRR framework.

### HEART Framework

- **Happiness** — user sentiment and satisfaction
- **Engagement** — interaction frequency and depth
- **Adoption** — new user acquisition and onboarding
- **Retention** — return rates and churn
- **Task success** — completion rates and error frequency

| Input Metric | Definition | Target | Owner |
|--------------|-----------|--------|-------|
| (metric name) | (definition) | (target value) | (owner) |
| (metric name) | (definition) | (target value) | (owner) |
| (metric name) | (definition) | (target value) | (owner) |

### AARRR Framework

- **Awareness** — top-of-funnel discovery
- **Acquisition** — sign-up conversion
- **Activation** — aha-moment completion
- **Revenue** — monetization conversion
- **Retention** — repeat purchase / churn

| Input Metric | Definition | Target | Owner |
|--------------|-----------|--------|-------|
| (metric name) | (definition) | (target value) | (owner) |
| (metric name) | (definition) | (target value) | (owner) |
| (metric name) | (definition) | (target value) | (owner) |

## OKR Alignment

Link each input metric to the OKRs it supports.

| OKR | Supporting Metrics |
|-----|-------------------|
| (OKR statement) | (metric names) |
| (OKR statement) | (metric names) |

## Goodhart Check

For each metric, document the gaming risk:

| Metric | Gaming Risk | Mitigations |
|--------|------------|-------------|
| (metric name) | (how it could be gamed) | (how we'd detect / prevent) |
| (metric name) | (how it could be gamed) | (how we'd detect / prevent) |

```

#### `work/docs/analytics/CLAUDE.md`

```
# Product Analytics Domain

This directory contains product analytics: the North Star Metric, the metric hierarchy,
instrumentation specs, cohort analyses, and experiment designs.

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
| Score | 11.5/11.5 (100%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 40032 ms |
| Target cost | $0.1147 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Creates the `docs/analytics/` directory (the one canonical path — not `docs/product-analytics/` or a variant) | PASS | Artifacts written to `work/docs/analytics/CLAUDE.md`, `work/docs/analytics/metric-tree.md`, `work/docs/analytics/instrumentation-spec.md` — canonical path used. |
| c2 | Writes `docs/analytics/CLAUDE.md` as the domain file | PASS | Artifact `work/docs/analytics/CLAUDE.md` exists and is confirmed written. |
| c3 | Writes `docs/analytics/metric-tree.md` (North Star + metric-hierarchy template) and `docs/analytics/instrumentation-spec.md` (data-engineer hand-off template) | PASS | Both artifact files `work/docs/analytics/metric-tree.md` and `work/docs/analytics/instrumentation-spec.md` are present and written. |
| c4 | The domain CLAUDE.md states the ownership boundary — the product-analyst defines what to measure and why; the data-engineer builds how data flows (pipelines, warehouse, dashboards) | PASS | CLAUDE.md: "The product-analyst defines *what* to measure and *why*. The data-engineer builds *how* data flows (pipelines, warehouse, dashboards)." |
| c5 | The domain CLAUDE.md states the metric-definition standard (question it answers, definition, calculation, granularity, filters, time window, Goodhart risk, owner) | PASS | CLAUDE.md "Metric definition standard" lists all 8 elements: question it answers, definition, calculation, granularity, filters, time window, Goodhart risk, owner. |
| c6 | The domain CLAUDE.md states conventions — North Star measures customer value not company revenue, Goodhart check on every metric, vanity/cumulative totals are never a North Star | PASS | CLAUDE.md Conventions: "North Star measures customer value, never company revenue directly"; "Run the Goodhart check on every metric"; "Vanity metrics (cumulative totals) are never a North Star or an input". |
| c7 | Does not invent metric values during bootstrap — templates ship with empty placeholder rows, not fabricated North Star or input metrics for "Cadence" | PASS | metric-tree.md uses "(to be defined)", "(metric name)", "(target value)"; instrumentation-spec.md uses "(event name)", "(when)". No fabricated Cadence-specific values. |
| c8 | Returns a manifest listing files created, files merged (or "none"), and next steps — not arbitrary prose | PASS | Chat response has structured sections: "Files created" (3 entries), "Files merged" ("None (fresh bootstrap)"), "Next steps" (2 items). |
| c9 | `docs/analytics/CLAUDE.md` exists and lists the available product-analyst skills (define-north-star, design-metric-hierarchy, write-instrumentation-spec, cohort-analysis, design-experiment) | PASS | CLAUDE.md "Available skills" table lists all 5 skills: define-north-star, design-metric-hierarchy, write-instrumentation-spec, cohort-analysis, design-experiment. |
| c10 | `docs/analytics/metric-tree.md` and `docs/analytics/instrumentation-spec.md` exist with template structure and empty placeholder rows, not invented data | PASS | Both files confirmed written with placeholder rows only (e.g., "(metric name)", "(event name)") — no Cadence-specific invented data. |
| c11 | The manifest names the created files and a "Next steps" section pointing at define-north-star and design-metric-hierarchy | PASS | Manifest lists all 3 created files; Next steps: "Define the North Star with `/product-analyst:define-north-star`" and "Build the metric hierarchy with `/product-analyst:design-metric-hierarchy`". |
| c12 | The manifest reports a "Files merged" line as "none" given a clean project (idempotency awareness) | PARTIAL | Manifest has "Files merged: None (fresh bootstrap)" — explicit acknowledgment of idempotency context. |

### Notes

The skill executed flawlessly: all three files written to the canonical path with placeholder-only content, CLAUDE.md covers all required sections (ownership, metric standard, conventions, skills), and the manifest is structured with all required sections. No fabricated Cadence-specific data anywhere.
