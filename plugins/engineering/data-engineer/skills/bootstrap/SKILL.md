---
name: bootstrap
bootstrap-phase: stack
description: "Bootstrap the data documentation structure for a project. Creates docs/data/, generates initial templates, and writes the data-engineer fragment of the data domain doc (the coordinator assembles docs/data/CLAUDE.md). Idempotent — merges missing sections into existing files without overwriting."
argument-hint: "[project name]"
user-invocable: false
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Bootstrap Data Documentation

Bootstrap the data documentation structure for **$ARGUMENTS**.

## Process

### Step 1: Check and create domain directory

```bash
mkdir -p docs/data docs/data/_sections
```

### Step 2: Create or merge files

For each file below, apply the safe merge pattern:
- If file does not exist -> create from template
- If file exists -> read both, find sections in template missing from file, append missing sections with `<!-- Merged from data-engineer bootstrap v0.1.0 -->`

#### Fragment: `docs/data/_sections/data-engineer.md`

`docs/data/CLAUDE.md` is **assembled by the coordinator** from the fragments in `_sections/` — no plugin writes
it directly. Write the data-engineer's contribution as this fragment. It starts at H2 (the coordinator generates
the `# Data Domain` H1 and a one-line intro). Create it with this content:

```markdown
## What This Domain Covers

- **Data models** — dbt models, schema design, entity relationships
- **Event tracking** — event taxonomy, tracking plans, schema validation
- **Data dictionary** — canonical definitions for business entities and metrics
- **Data quality** — validation rules, freshness checks, anomaly detection
- **Metric definitions** — single source of truth for business metrics

## dbt Style Guide

### Naming conventions

| Object | Convention | Example |
|--------|-----------|---------|
| Source | `src_{source}` | `src_postgres` |
| Staging | `stg_{source}__{entity}` | `stg_postgres__orders` |
| Intermediate | `int_{entity}_{verb}` | `int_orders_pivoted` |
| Mart | `fct_{entity}` or `dim_{entity}` | `fct_orders`, `dim_customers` |
| Metric | `met_{metric}` | `met_monthly_revenue` |

### Model organisation

```
models/
├── staging/         # 1:1 with source tables, renaming and type casting only
├── intermediate/    # Business logic transformations
├── marts/           # Final fact and dimension tables
└── metrics/         # Metric definitions (dbt metrics or semantic layer)
```

### dbt conventions

- Every model has a `.yml` file with description, column descriptions, and tests
- Use `ref()` and `source()` — never hardcode table names
- Staging models: rename, cast, and deduplicate only — no business logic
- Intermediate models: joins, aggregations, pivots, business logic
- Mart models: final shape for consumption (BI tools, APIs, exports)

## Event Tracking Process

1. **Propose** — define event in tracking plan (see `event-tracking-spec.md`)
2. **Review** — data engineer reviews schema and naming
3. **Implement** — developer instruments the event
4. **Validate** — automated schema validation in CI
5. **Monitor** — track event volume and quality in production

### Event naming

- Format: `{object}_{action}` in snake_case (e.g., `order_placed`, `user_signed_up`)
- Use past tense for completed actions
- Group by domain object, not by page or feature

## Data Quality (Great Expectations)

Enforce data quality with automated checks:

| Check Type | Example | Frequency |
|------------|---------|-----------|
| Schema | Column types match expectation | Every run |
| Completeness | No nulls in required fields | Every run |
| Uniqueness | Primary keys are unique | Every run |
| Freshness | Data updated within SLA | Hourly |
| Volume | Row count within expected range | Daily |
| Custom | Business rule validation | Per-model |

## Metric Definitions

All business metrics must have a single canonical definition:

| Field | Description |
|-------|-------------|
| Name | Metric name (e.g., `monthly_recurring_revenue`) |
| Definition | Plain-English description |
| Formula | SQL or dbt metric definition |
| Grain | Time grain (daily, weekly, monthly) |
| Dimensions | Allowed slice-and-dice dimensions |
| Owner | Team or person responsible |

## Tooling

| Tool | Purpose |
|------|---------|
| [GitHub](https://github.com) | Data model docs versioned in repo |
| [GitHub Actions](https://docs.github.com/en/actions) | `dbt test` in CI on every PR |

## Available Skills

| Skill | Purpose |
|-------|---------|
| `/data-engineer:data-model` | Design a data model |
| `/data-engineer:event-tracking-plan` | Create an event tracking plan |
| `/data-engineer:write-query` | Write an analytical query |

## Conventions

- Every data model must have tests and documentation
- Event schemas are reviewed before implementation
- Metric definitions live in `docs/data/` — not in BI tool configs
- Data quality checks run on every dbt run — failures block deployment
- Staging models never contain business logic
- All queries reference dbt models, not raw source tables
```

#### File 2: `docs/data/event-tracking-spec.md`

Create with this content:

```markdown
# Event Tracking Specification

> Define all tracked events here. Each event must be reviewed by a data engineer before implementation.

## Event Catalogue

| Event Name | Description | Trigger | Owner |
|------------|-------------|---------|-------|
| `example_event` | Example event description | When user does X | Team |

## Event Schema Template

For each event, define the schema:

### `{event_name}`

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `event_name` | string | Yes | Event identifier |
| `timestamp` | ISO 8601 | Yes | When the event occurred |
| `user_id` | string | Yes | Authenticated user ID |
| `session_id` | string | Yes | Browser/app session ID |
| `properties` | object | Yes | Event-specific properties |

### Naming Rules

- Event names: `{object}_{action}` in snake_case
- Property names: snake_case
- Use consistent types across events (e.g., `user_id` is always string)
- Boolean properties prefixed with `is_` or `has_`
```

#### File 3: `docs/data/data-dictionary.md`

Create with this content:

```markdown
# Data Dictionary

> Canonical definitions for business entities, fields, and metrics. Single source of truth.

## Entities

| Entity | Description | Primary Key | Source |
|--------|-------------|-------------|--------|
| | | | |

## Standard Fields

| Field | Type | Description | Used In |
|-------|------|-------------|---------|
| `created_at` | timestamp | Record creation time (UTC) | All entities |
| `updated_at` | timestamp | Last modification time (UTC) | All entities |
| `is_deleted` | boolean | Soft-delete flag | All entities |

## Business Metrics

| Metric | Definition | Formula | Grain | Owner |
|--------|-----------|---------|-------|-------|
| | | | | |

## Enumerations

| Enum | Values | Used In |
|------|--------|---------|
| | | |

> Update this dictionary when new entities, fields, or metrics are introduced.
```

### Step 3: Return manifest

After creating/merging all files, output a summary:

```
## Data Engineer Bootstrap Complete

### Files created
- `docs/data/_sections/data-engineer.md` — data-engineer fragment (coordinator assembles `docs/data/CLAUDE.md` from it)
- `docs/data/event-tracking-spec.md` — event tracking specification template
- `docs/data/data-dictionary.md` — data dictionary template

### Files merged
- (list any existing files where sections were appended)

### Next steps
- Define initial data models using `/data-engineer:data-model`
- Create event tracking plan using `/data-engineer:event-tracking-plan`
- Populate the data dictionary with core business entities
```
