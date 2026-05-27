---
# Match the model the agent declares (sonnet) in
# plugins/engineering/data-engineer/agents/data-engineer.md. The runner otherwise
# falls back to the harness default (Haiku), which is not what the
# agent is designed to run on.
target-model: claude-sonnet-4-6
---

# Test: Event-sourced user activity pipeline

Scenario: User needs a data pipeline that captures user activity events from the production event stream and makes them available for analytics — specifically to answer retention and feature adoption questions.

## Prompt

We're building out our analytics capability and need a pipeline for user activity data. Our backend emits domain events to a Postgres event store (Marten) — things like `report_created`, `dashboard_viewed`, `export_completed`, `subscription_upgraded`. We want to track retention (did the user come back 7 days after signup?), feature adoption (which features do users engage with in their first 30 days?), and funnel conversion from trial to paid. The events are immutable once written. Can you design the pipeline and data model?

Do not ask for clarification — proceed based on the information provided. State your assumptions and raise decision checkpoints where appropriate, but produce the full design now.

A few specifics for the response (output in this exact section order):

1. **Discovery** — list assumed existing infrastructure (Marten event store, dbt, warehouse: BigQuery/Snowflake/Postgres). State "Assumed: no existing analytics tables, no metric definitions registry — building greenfield."
2. **Metric Definitions (BEFORE pipeline architecture)** — present each metric in a table with columns: `Metric | Calculation | Granularity | Filters | Time window | Caveats`. Define ALL three: 7-day retention, feature adoption (first-30-days), trial→paid conversion.
3. **Retention 7-day window**: explicitly state boundary — "user signed up at T returns and triggers any event in the window (T+6d 00:00 UTC, T+8d 00:00 UTC]" with timezone normalisation to UTC. Discuss point-in-time vs window semantics.
4. **Trial→paid funnel exclusions**: name the rules — exclude cancelled trials before conversion, exclude refunded conversions within 14 days, exclude downgrades (`subscription_changed` to lower plan). Time bound: 30 days from `trial_started_at`.
5. **Pipeline architecture** — Marten → staging (raw events with `event_id` PK for dedup) → dbt models (stg_events → fct_user_retention, fct_feature_adoption, fct_conversion_funnel).
6. **Data Quality Gates (3 checks at each boundary)** — a table: `Stage | Check | Action`. Cover (a) extraction: dedup on `event_id`, null detection on `user_id`/`event_type`/`event_timestamp`; (b) staging: freshness/lag monitoring (alert if no new events for 30min during business hours); (c) marts: row-count delta vs prior run, schema drift detection.
7. **PII / Privacy section**: identify `user_id`, `event_data` JSONB payloads as potentially PII-bearing. State retention policy (e.g. raw events 13 months, aggregated marts indefinite). Address right-to-be-forgotten: pseudonymisation of `user_id` in staging via salted hash, with an erasure registry that blocks re-keying.
8. **Event versioning**: `event_data` JSONB accommodates new fields. Version field on each event (`schema_version` int). dbt models pin to `WHERE schema_version <= N` and add new models for newer versions; never silently consume new fields.
9. **Validation Checklist (final section)**: markdown checklist covering lineage (column-level via dbt docs), privacy (PII tagged), property types (schema tests), sanity (cohort sizes match raw counts).
10. **Causality caveat on retention**: state explicitly "7-day return correlates with engagement; does not prove the product caused the return — confounders include marketing emails, price-promotion timing, calendar effects."

## Criteria

- [ ] PASS: Agent starts by identifying data sources, checking for existing metric definitions and infrastructure, and reviewing what events are already tracked
- [ ] PASS: Agent produces precise metric definitions (with calculation, granularity, filters, time window, and caveats) for retention, feature adoption, and trial conversion before designing the pipeline
- [ ] PASS: Agent applies immutable event sourcing principles — never proposes UPDATE/DELETE patterns on event data, only append-only ingestion
- [ ] PASS: Agent addresses data quality checks at every pipeline boundary (null checks, deduplication, freshness monitoring)
- [ ] PASS: Agent documents data lineage from source (Marten event store) through transformations to the destination (analytics layer)
- [ ] PASS: Agent raises a decision checkpoint before choosing storage technology (architecture commitment)
- [ ] PARTIAL: Agent includes privacy considerations — identifying which properties contain PII and specifying retention/erasure policy
- [ ] PASS: Agent produces a validation checklist covering lineage, privacy, property types, and sanity checks
- [ ] PASS: Agent distinguishes correlation from causation when discussing retention metrics

## Output expectations

- [ ] PASS: Output names the four source events from the prompt (`report_created`, `dashboard_viewed`, `export_completed`, `subscription_upgraded`) and traces each to the analytics use case it supports
- [ ] PASS: Output's retention metric defines the exact 7-day window logic — e.g. "user signed up at T returns and triggers any event in (T+6d, T+8d]" — including boundary handling, not just "did they come back after 7 days"
- [ ] PASS: Output's feature adoption metric specifies first-30-days as a fixed cohort window from signup, lists which events count as "engagement" with which features, and defines the de-duplication rule (one count per user-feature)
- [ ] PASS: Output's funnel metric defines trial-to-paid conversion with explicit start state, terminal state (`subscription_upgraded` event), exclusion rules (cancelled trials, refunds), and time bounds
- [ ] PASS: Output's data flow describes Marten event store → ETL/CDC → analytics layer with explicit append-only semantics — no UPDATE/DELETE patterns on the activity events themselves, even in transformations
- [ ] PASS: Output documents at least three quality checks (null detection on user_id, deduplication of replayed events, freshness/lag monitoring) at named pipeline stages
- [ ] PASS: Output addresses event versioning — what happens if an event schema evolves (new property added to `report_created`) given the events are immutable in Marten
- [ ] PASS: Output raises a decision checkpoint on the analytics destination (warehouse choice — Snowflake / BigQuery / DuckDB / Postgres replica) before committing rather than picking unilaterally
- [ ] PARTIAL: Output identifies the PII and privacy implications — `user_id` linkage, retention period for raw activity, and erasure/right-to-be-forgotten handling for the immutable event store
- [ ] PARTIAL: Output includes a sanity-check on retention causality — flags that "user came back" correlates with engagement but doesn't prove the product caused the return
