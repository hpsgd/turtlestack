# Bootstrap

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/data/_sections/data-engineer.md` fragment containing a user-authored section. The data-engineer bootstrap skill should preserve that user content while appending the template's missing sections (with a merge marker), and should create the two files the fixture is missing — `event-tracking-spec.md` and `data-dictionary.md`. The data-engineer never writes `docs/data/CLAUDE.md` directly — the coordinator assembles it from the fragments in `_sections/`. The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

> The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/data/_sections/data-engineer.md` fragment is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.
> 
> Read the data-engineer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/engineering/data-engineer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.
> 
> After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Data Engineer Bootstrap Complete

### Files created
- `docs/data/_sections/data-engineer.md` — data-engineer fragment (coordinator assembles `docs/data/CLAUDE.md` from it)
- `docs/data/event-tracking-spec.md` — event tracking specification template
- `docs/data/data-dictionary.md` — data dictionary template

### Files merged
- `docs/data/_sections/data-engineer.md` — appended missing sections (dbt style guide, event tracking process, data quality, metric definitions, tooling, available skills, conventions) while preserving user-authored "Custom team notes" section with sentinel

### Next steps
- Define initial data models using `/data-engineer:data-model`
- Create event tracking plan using `/data-engineer:event-tracking-plan`
- Populate the data dictionary with core business entities

### Artifacts written

#### `work/docs/data/data-dictionary.md`

```
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

#### `work/docs/data/event-tracking-spec.md`

```
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

#### `work/docs/data/_sections/data-engineer.md`

```
<!-- data-engineer fragment of the data domain doc. Assembled into docs/data/CLAUDE.md by the coordinator. -->

## Custom team notes

USER-EDIT-SENTINEL-DO-NOT-STRIP

This section was written by the team and must survive any bootstrap re-run.
It exists to test the safe-merge contract: the bootstrap skill must not
overwrite or remove user-authored content.

<!-- Merged from data-engineer bootstrap v0.1.0 -->

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

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 10.5/10.5 (100%) |
| Evaluated | 2026-06-15 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 41720 ms |
| Target cost | $0.0867 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | After bootstrap, `docs/data/_sections/data-engineer.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim | PASS | Artifact shows '## Custom team notes\n\nUSER-EDIT-SENTINEL-DO-NOT-STRIP\n\nThis section was written by the team...' intact at top of file. |
| c2 | After bootstrap, `docs/data/_sections/data-engineer.md` contains the safe-merge marker `<!-- Merged from data-engineer bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged | PASS | Artifact contains '<!-- Merged from data-engineer bootstrap v0.1.0 -->' on its own line between user content and appended template sections. |
| c3 | After bootstrap, `docs/data/_sections/data-engineer.md` contains the appended template sections — at minimum the "dbt Style Guide" and "Event Tracking Process" headings now appear alongside the preserved user content | PASS | Artifact contains '## dbt Style Guide' and '## Event Tracking Process' headings alongside the preserved '## Custom team notes' section. |
| c4 | The data-engineer fragment is authored at H2 and below — it does not introduce a `# Data Domain` H1 (the coordinator generates that when it assembles `docs/data/CLAUDE.md`) | PASS | Artifact starts with an HTML comment then '## Custom team notes' — no H1 heading anywhere in the file; all headings are ## or ###. |
| c5 | The skill does NOT write `docs/data/CLAUDE.md` directly — that file is the coordinator's to assemble from `_sections/` | PASS | Artifacts listed are only: data-dictionary.md, event-tracking-spec.md, and _sections/data-engineer.md. No docs/data/CLAUDE.md artifact present. |
| c6 | After bootstrap, `docs/data/event-tracking-spec.md` exists and was created from the skill's template (contains `## Event Catalogue` and `### Naming Rules` sections) | PASS | Artifact work/docs/data/event-tracking-spec.md contains '## Event Catalogue' table and '### Naming Rules' section with snake_case conventions. |
| c7 | After bootstrap, `docs/data/data-dictionary.md` exists and was created from the skill's template (contains `## Entities`, `## Standard Fields`, and `## Business Metrics` sections) | PASS | Artifact work/docs/data/data-dictionary.md contains all three: '## Entities', '## Standard Fields', and '## Business Metrics' sections with tables. |
| c8 | Chat output includes a manifest summary that distinguishes files created (`event-tracking-spec.md`, `data-dictionary.md`) from files merged (`_sections/data-engineer.md`) | PASS | Chat output has distinct '### Files created' and '### Files merged' sections; event-tracking-spec.md and data-dictionary.md under created; _sections/data-engineer.md under merged. |
| c9 | Output names each created and merged file individually — a bare "bootstrap complete" without the per-file manifest is not enough | PASS | Each file is listed individually with a description: 3 files under created, 1 under merged, each on its own bullet with per-file explanation. |
| c10 | Output does not claim it overwrote or replaced `docs/data/_sections/data-engineer.md` — the language reflects merge, not replacement | PASS | Merged entry reads 'appended missing sections... while preserving user-authored "Custom team notes" section with sentinel' — no overwrite/replace language. |
| c11 | Output points the reader at next steps (using `/data-engineer:data-model`, `/data-engineer:event-tracking-plan`, and populating the data dictionary) consistent with the skill's documented manifest | PARTIAL | Next steps section lists all three: '/data-engineer:data-model', '/data-engineer:event-tracking-plan', and 'Populate the data dictionary with core business entities'. |

### Notes

The skill executed flawlessly: sentinel preserved, merge marker present, template sections appended, no H1 introduced, CLAUDE.md not written, both new files created with correct structure, and the manifest correctly distinguishes created from merged files. All ten PASS-ceiling criteria are fully satisfied, and the PARTIAL-ceiling next-steps criterion is maximally satisfied at its 0.5 ceiling.
