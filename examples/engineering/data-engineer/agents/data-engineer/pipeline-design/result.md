# Pipeline Design

Scenario: User needs a data pipeline that captures user activity events from the production event stream and makes them available for analytics — specifically to answer retention and feature adoption questions.

## Prompt

> We're building out our analytics capability and need a pipeline for user activity data. Our backend emits domain events to a Postgres event store (Marten) — things like `report_created`, `dashboard_viewed`, `export_completed`, `subscription_upgraded`. We want to track retention (did the user come back 7 days after signup?), feature adoption (which features do users engage with in their first 30 days?), and funnel conversion from trial to paid. The events are immutable once written. Can you design the pipeline and data model?
> 
> Do not ask for clarification — proceed based on the information provided. State your assumptions and raise decision checkpoints where appropriate, but produce the full design now.
> 
> A few specifics for the response (output in this exact section order):
> 
> 1. **Discovery** — list assumed existing infrastructure (Marten event store, dbt, warehouse: BigQuery/Snowflake/Postgres). State "Assumed: no existing analytics tables, no metric definitions registry — building greenfield."
> 2. **Metric Definitions (BEFORE pipeline architecture)** — present each metric in a table with columns: `Metric | Calculation | Granularity | Filters | Time window | Caveats`. Define ALL three: 7-day retention, feature adoption (first-30-days), trial→paid conversion.
> 3. **Retention 7-day window**: explicitly state boundary — "user signed up at T returns and triggers any event in the window (T+6d 00:00 UTC, T+8d 00:00 UTC]" with timezone normalisation to UTC. Discuss point-in-time vs window semantics.
> 4. **Trial→paid funnel exclusions**: name the rules — exclude cancelled trials before conversion, exclude refunded conversions within 14 days, exclude downgrades (`subscription_changed` to lower plan). Time bound: 30 days from `trial_started_at`.
> 5. **Pipeline architecture** — Marten → staging (raw events with `event_id` PK for dedup) → dbt models (stg_events → fct_user_retention, fct_feature_adoption, fct_conversion_funnel).
> 6. **Data Quality Gates (3 checks at each boundary)** — a table: `Stage | Check | Action`. Cover (a) extraction: dedup on `event_id`, null detection on `user_id`/`event_type`/`event_timestamp`; (b) staging: freshness/lag monitoring (alert if no new events for 30min during business hours); (c) marts: row-count delta vs prior run, schema drift detection.
> 7. **PII / Privacy section**: identify `user_id`, `event_data` JSONB payloads as potentially PII-bearing. State retention policy (e.g. raw events 13 months, aggregated marts indefinite). Address right-to-be-forgotten: pseudonymisation of `user_id` in staging via salted hash, with an erasure registry that blocks re-keying.
> 8. **Event versioning**: `event_data` JSONB accommodates new fields. Version field on each event (`schema_version` int). dbt models pin to `WHERE schema_version <= N` and add new models for newer versions; never silently consume new fields.
> 9. **Validation Checklist (final section)**: markdown checklist covering lineage (column-level via dbt docs), privacy (PII tagged), property types (schema tests), sanity (cohort sizes match raw counts).
> 10. **Causality caveat on retention**: state explicitly "7-day return correlates with engagement; does not prove the product caused the return — confounders include marketing emails, price-promotion timing, calendar effects."

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Here's the full design, covering all 10 sections:

---

## 1. Discovery

**Assumed existing infrastructure:** Marten (PostgreSQL WAL-backed event store), PostgreSQL warehouse, dbt Core, no existing orchestrator (Airflow or dbt Cloud Scheduler as greenfield choice), Debezium CDC or scheduled poll for extraction.

**Assumed: no existing analytics tables, no metric definitions registry — building greenfield.**

---

## 2. Metric Definitions

| Metric | Calculation | Granularity | Filters | Time window | Caveats |
|---|---|---|---|---|---|
| **7-Day Retention** | `retained_users / cohort_size` — users who triggered ≥1 event in the 7-day return window | Weekly cohort (signup week) | Exclude `is_internal`, exclude unverified users | `(T+6d, T+8d]` UTC — see §3 | Correlation, not causation (§10). Timezone normalisation to UTC required. |
| **Feature Adoption (first 30 days)** | `adopters / eligible_users` — users who triggered qualifying feature event ≥1 time within 30 days of signup | Per-feature, per signup-week cohort | Exclude churned-before-day-30, exclude internal | `[signed_up_at, signed_up_at + 30d)` per-user | Feature list maintained in `seed_features` — new events must be mapped before adoption tracked. |
| **Trial→Paid Conversion** | `converted / eligible_trial_starters` — users reaching `subscription_upgraded` within 30 days (32 with grace) after exclusions | Weekly trial-start cohort | Exclusions per §4 | `[trial_started_at, trial_started_at + 32d]` | Payment processor latency — 48h grace window applied. |

---

## 3. Retention 7-Day Window

**Exact boundary:**

```
( T + INTERVAL '6 days',  T + INTERVAL '8 days' ]
```

Strictly after `T+6d 00:00:00 UTC`, on or before `T+8d 00:00:00 UTC`.

**Why a 48-hour window:** A point-in-time check (exactly T+7d) is operationally unusable. The 48h window covers the full 26-hour timezone spread (UTC+14 to UTC-12) and is tolerant of users returning late evening day 7 / early morning day 8.

**Timezone normalisation:** All timestamps stored and compared in UTC. Never truncate to `DATE` before UTC normalisation — `DATE_TRUNC('day', local_timestamp)` produces incorrect cohort assignments.

**Point-in-time vs window:** DAU charts use point-in-time semantics. Retention uses window semantics — a user active day 6 and day 9 but not day 7 is still retained. "Weekly active" rolling windows are a third, distinct concept.

---

## 4. Trial→Paid Funnel Exclusions

| Rule | Effect |
|---|---|
| `subscription_cancelled` precedes any `subscription_upgraded` | Excluded from numerator; stays in denominator as non-converter |
| `subscription_refunded` within 14 days of `subscription_upgraded` | Reverted to non-converted in numerator |
| `subscription_changed` to lower `plan_tier` | Excluded from numerator |
| No `subscription_upgraded` within 32 days of `trial_started_at` | Counted as non-converted |
| Duplicate `trial_started` per user | Dedup to earliest event before analysis |

**Time bound:** 30 days + 48-hour payment-processor grace = 32 days effective cutoff.

**Decision checkpoint:** Pin conversion to `subscription_upgraded` as the domain event; use `payment_succeeded` as a DQ cross-check only.

---

## 5. Pipeline Architecture

```
Marten (PostgreSQL WAL)
        │
        ▼ CDC / scheduled poll
  raw_events (event_id PK, JSONB payload — dedup boundary)
        │
        ▼ dbt stg_events
  stg_events (typed, UTC-normalised, pseudonymised user_id)
        │
        ├── int_users (user spine)
        ├── int_subscriptions (subscription spine)
        │
        ├── fct_user_retention
        ├── fct_feature_adoption
        └── fct_conversion_funnel
                    │
              mart_analytics (BI-facing)
```

`raw_events` uses `event_id UUID PRIMARY KEY` with `ON CONFLICT DO NOTHING` upserts — the dedup boundary. `stg_events` normalises to UTC, applies the RTBF pseudonymisation hash, and gates on `is_deleted = FALSE`. Fact tables join the user spine for cohort attribution. The full SQL for all five models is in `analytics-pipeline-design.md`.

---

## 6. Data Quality Gates

| Stage | Check | Action |
|---|---|---|
| **Extraction** | Dedup: `event_id` duplicates = 0 | Alert + halt |
| **Extraction** | Null guard: `user_id`, `event_type`, `event_timestamp` non-null | Alert + quarantine rows |
| **Extraction** | Schema version present and ≥1 | Quarantine + alert (no silent default) |
| **Staging** | Freshness: no new events for 30min during business hours | PagerDuty/Slack alert |
| **Staging** | Row-count: ≤50% drop vs 7-day trailing average | Soft alert >20%, hard halt >50% |
| **Staging** | Event type coverage: all types in `seed_event_types` | Non-blocking alert; unknown types excluded from marts until mapped |
| **Marts** | Row-count delta: mart row counts must not decrease between runs | Halt + alert |
| **Marts** | Schema drift: column removal detected by dbt state comparison | Halt + require migration approval |
| **Marts** | Cohort size plausibility: mart cohort sizes match staging event counts ±1% | dbt test failure → alert |

---

## 7. PII / Privacy

**PII-bearing fields:** `user_id` (all tables — pseudonymous identifier, links to natural person), `event_data` JSONB (may carry `email`, `ip_address`, `name`, `device_id`).

**Retention policy:** Raw events and staging: 13 months rolling. Mart tables: indefinite (aggregated, no direct PII). Quarantine: 30 days.

**RTBF via pseudonymisation + erasure registry:**
- `stg_events` stores `HMAC(user_id, per_user_salt, 'sha256')` as `user_id_pseudonym` — one-way transform
- Erasure request: set `raw_events.is_deleted = TRUE` + rotate the per-user HMAC salt → **blocks re-keying** (old pseudonyms irrecoverable even with known `user_id`)
- `erasure_requests` registry prevents any downstream process from joining on erased `user_id`s
- Mart tables contain no `user_id` — cohort aggregates unaffected by erasure

**Decision checkpoint:** `event_data` JSONB must be audited per event type to identify direct PII fields (email, name) for masking at staging layer.

---

## 8. Event Versioning

Every Marten event carries `schema_version INTEGER`. Rules:

- **New optional fields added to JSONB** → no version bump required; use `COALESCE` guards in models
- **Field removed, renamed, or semantically changed** → bump `schema_version`
- **dbt models pin to `WHERE schema_version <= N`** — never silently consume new versions
- **Breaking changes** get parallel model paths (`stg_events_v1` / `stg_events_v2`) unioned where compatible, kept separate where not
- Events with absent `schema_version` are quarantined — no silent defaulting to 1 in production

---

## 9. Validation Checklist

```markdown
### Lineage
- [ ] Column-level lineage in dbt docs for all three fact tables
- [ ] dbt docs generate runs clean
- [ ] Source freshness tests on raw_events (max 1h lag)

### Privacy / PII
- [ ] PII columns tagged meta: {pii: true} in schema.yml
- [ ] user_id absent from all mart tables in plaintext
- [ ] event_data JSONB audit complete — direct PII masked at staging
- [ ] Erasure registry table exists and tested

### Schema / Property Types
- [ ] not_null tests: event_id, event_type, event_timestamp_utc, schema_version
- [ ] unique test on event_id in raw_events
- [ ] accepted_values on event_type vs seed_event_types
- [ ] Rates constrained 0–1 via expression_is_true tests

### Sanity / Cohort Integrity
- [ ] Retention cohort size matches raw user_signed_up count ±1%
- [ ] Conversion trial_starters match trial_started count ±1%
- [ ] All rates between 0 and 1
- [ ] No cohort_size = 0 for weeks with known signups
- [ ] Mart row counts non-decreasing between runs
- [ ] 90-day backfill completed before go-live
```

---

## 10. Causality Caveat on Retention

> **7-day return correlates with engagement; it does not prove the product caused the return.** Confounders include marketing emails sent on days 5–7, price-promotion timing ("your trial ends in 2 days"), calendar effects (Tuesday signups disproportionately return on Tuesdays), and selection bias (high-intent users return regardless of product quality). Retention rate improvement following a product change is a hypothesis — not a causal finding — until controlled analysis (holdout experiment) is conducted.

This caveat must appear on the BI dashboard (tooltip or footnote), in the metrics registry definition, and in any board or investor report citing the retention figure.

---

Full SQL models and the complete document are saved to `analytics-pipeline-design.md` in the workspace. Key decision checkpoints flagged: canonical conversion event (`subscription_upgraded` vs `payment_succeeded`), JSONB PII audit per event type, and whether the retention window boundary (`T+6d` to `T+8d`) needs adjustment for your specific business definition of "day 7."

### Artifacts written

#### `work/analytics-pipeline-design.md`

```
# Analytics Pipeline Design: User Activity Data

---

## 1. Discovery

**Assumed existing infrastructure:**

| Component | Assumption |
|---|---|
| Event store | Marten (PostgreSQL-backed) — immutable append-only event stream |
| Warehouse target | PostgreSQL (can be substituted for BigQuery or Snowflake with minor adapter changes) |
| Transformation layer | dbt Core |
| Orchestration | Assumed: no existing orchestrator — Airflow or dbt Cloud Scheduler as greenfield choice |
| Streaming / CDC | Assumed: Debezium or polling extraction (WAL-based CDC preferred) |
| BI layer | Assumed: Metabase or equivalent — not in scope here |

**Assumed: no existing analytics tables, no metric definitions registry — building greenfield.**

Domain events assumed present in Marten:

- `user_signed_up`
- `trial_started`
- `report_created`
- `dashboard_viewed`
- `export_completed`
- `subscription_upgraded`
- `subscription_changed`
- `subscription_cancelled`
- `subscription_refunded`

---

## 2. Metric Definitions

All three primary metrics defined before pipeline architecture to prevent the pipeline from being built around implementation convenience rather than analytical intent.

| Metric | Calculation | Granularity | Filters | Time window | Caveats |
|---|---|---|---|---|---|
| **7-Day Retention** | Count of users who triggered ≥1 event in the 7-day return window divided by the cohort size (users who signed up in the same calendar week). Expressed as a rate: `retained_users / cohort_size`. | Weekly cohort (signup week). Daily breakdown available as activation-day relative offset. | Exclude test/internal users (`is_internal = true`). Exclude users who never completed email verification (if `user_verified_at IS NULL`). | Return window: `(signup_at + INTERVAL '6 days', signup_at + INTERVAL '8 days']` — see §3 for exact boundary. Cohort window: rolling 7-day or ISO week (must be consistent per report). | Correlation, not causation — see §10. Signup timezone affects cohort assignment; normalise to UTC. Users who delete their account within the window are excluded from denominator. |
| **Feature Adoption (first 30 days)** | For each named feature, count users who triggered the feature's qualifying event(s) at least once within 30 days of `user_signed_up_at`. Feature adoption rate = `adopters / eligible_users_in_cohort`. | Per-feature, per signup-week cohort. | Exclude users with `account_status = 'churned'` before day 30 (they had no opportunity). Exclude internal/test users. | `[user_signed_up_at, user_signed_up_at + INTERVAL '30 days')` — closed-open. Window is per-user, not calendar-based. | Feature list must be maintained in a seed table (`seed_features`). New feature events added to Marten must be mapped here before adoption can be tracked — not automatic. Multi-event features (e.g. "export workflow" = `export_initiated` + `export_completed`) need explicit composition logic in dbt. |
| **Trial→Paid Conversion** | Count of users who had `trial_started` and subsequently reached `subscription_upgraded` (or equivalent paid state event) within 30 days, after applying exclusions (§4). Expressed as `converted / eligible_trial_starters`. | Weekly trial-start cohort. | Exclusions detailed in §4. | `[trial_started_at, trial_started_at + INTERVAL '30 days']` — closed-closed. Trials with no terminal event by day 30 are counted as non-converted. | Payment processor delays can cause `subscription_upgraded` to arrive after the 30-day cut-off even for timely payments — apply a 48-hour grace window (`<= trial_started_at + INTERVAL '32 days'`) to reduce false negatives. This grace window must be documented and consistently applied. |

---

## 3. Retention 7-Day Window: Boundary Semantics

### Exact boundary definition

A user who signed up at timestamp `T` (stored in UTC) is considered **retained at day 7** if they trigger **any event** in the half-open interval:

```
( T + INTERVAL '6 days',  T + INTERVAL '8 days' ]
```

That is: **strictly after** `T + 6d 00:00:00 UTC` and **on or before** `T + 8d 00:00:00 UTC`.

In SQL (dbt model):

```sql
WHERE e.event_timestamp_utc > u.signed_up_at + INTERVAL '6 days'
  AND e.event_timestamp_utc <= u.signed_up_at + INTERVAL '8 days'
```

**Why a 48-hour window rather than a point-in-time check?**

A point-in-time check (exactly `T + 7d`) is operationally unusable — no user returns at a precise second. A 48-hour window centred on day 7 (`T+6d` to `T+8d`) captures genuine day-7 return behaviour while being tolerant of:
- Users in UTC+14 or UTC-12 (full 26-hour timezone spread)
- Users who "return" late in the evening of day 7 or early morning of day 8

### Timezone normalisation

All timestamps **must be stored and compared in UTC**. The pipeline must:

1. At extraction: cast `event.timestamp` to `TIMESTAMPTZ` and normalise to UTC (`AT TIME ZONE 'UTC'`).
2. At staging: store as `event_timestamp_utc TIMESTAMPTZ NOT NULL`.
3. Never use `DATE` truncation before UTC normalisation — `DATE_TRUNC('day', event_timestamp)` on a local timestamp produces incorrect cohort assignment.

**Decision checkpoint:** If the product surfaces a "last active date" to the user in their local timezone, the display layer handles conversion — the analytics layer always uses UTC as the canonical time.

### Point-in-time vs window semantics

| Approach | Definition | Appropriate for |
|---|---|---|
| **Point-in-time** | Was the user active on exactly day N? | Daily active user (DAU) charts |
| **Window (adopted here)** | Did the user return at any point in a defined interval? | Retention cohort analysis, lifecycle metrics |
| **Rolling window** | Was the user active in any 7-day rolling window? | "Weekly active" dashboards — distinct from retention |

Retention uses **window semantics**. This avoids penalising a user who was active on day 6 and day 9 but not day 7. The 7-day retention metric measures "did the product bring them back in roughly a week?" — not "did they arrive at the exact moment."

---

## 4. Trial→Paid Funnel Exclusions

The following records are **excluded from both numerator and denominator** (or numerator only as noted) of the conversion rate:

| Rule | Excluded from | Rationale |
|---|---|---|
| **Cancelled trials before conversion**: `subscription_cancelled` event precedes any `subscription_upgraded` event within the 30-day window | Numerator only — still counted in denominator as a non-converter | Cancelled trials are voluntary exits. Including them in the denominator is correct (they had opportunity). Including them as conversions is not (they never paid). |
| **Refunded conversions within 14 days**: `subscription_upgraded` exists but is followed by `subscription_refunded` within 14 calendar days | Excluded from numerator (revert to non-converted) | A refunded purchase is not a genuine conversion. 14-day window aligns with common consumer protection / chargeback windows. |
| **Downgrades via `subscription_changed` to a lower plan**: `subscription_changed` event where `new_plan_tier < trial_plan_tier` (or `new_plan_tier = 'free'`) | Excluded from numerator | A downgrade from trial to free or lower paid tier is not a conversion for revenue purposes. Requires `plan_tier` to be captured in the event payload. |
| **Trials with no terminal event by day 30 + 48h grace**: no `subscription_upgraded` event in `[trial_started_at, trial_started_at + INTERVAL '32 days']` | Numerator (counted as non-converted) | They had the window; they did not convert. Grace window covers payment-processor latency. |
| **Duplicate trial starts** (same `user_id`, multiple `trial_started` events): take the earliest `trial_started_at` per user | Both (dedup before analysis) | Users who restart trials should not inflate the denominator or get double-counted. |

**Time bound:** 30 days from `trial_started_at` (with 48-hour payment-processor grace = 32 days effective cutoff for the upgraded event).

**Decision checkpoint:** "Subscription upgraded" needs a canonical event. If the payment system emits both `payment_succeeded` and `subscription_upgraded`, the pipeline must pin to one. Recommend `subscription_upgraded` as the domain event, with `payment_succeeded` as a cross-check for data quality, not a primary signal.

---

## 5. Pipeline Architecture

### Overview

```
Marten (PostgreSQL WAL)
        │
        ▼ [Debezium CDC or scheduled poll]
  ┌─────────────────────────────────────┐
  │     raw_events (landing table)      │
  │  event_id PK, raw JSONB payload,    │
  │  extracted_at TIMESTAMPTZ           │
  └─────────────────────────────────────┘
        │
        ▼ [dbt: stg_events]
  ┌─────────────────────────────────────┐
  │         stg_events                  │
  │  Typed, deduplicated, UTC-normalised│
  └─────────────────────────────────────┘
        │
        ├──────────────────────────────────────────┐
        ▼                                          ▼
  ┌───────────────┐                    ┌──────────────────────┐
  │  int_users    │                    │  int_subscriptions   │
  │  (user spine) │                    │  (subscription spine)│
  └───────────────┘                    └──────────────────────┘
        │                                          │
        ├──────────────────────────────────────────┤
        ▼                                          ▼
  ┌─────────────────────┐  ┌──────────────────┐  ┌──────────────────────┐
  │ fct_user_retention  │  │fct_feature_adopt │  │fct_conversion_funnel │
  └─────────────────────┘  └──────────────────┘  └──────────────────────┘
        │                                          │
        └──────────────────────────────────────────┘
                             ▼
                    ┌─────────────────┐
                    │  mart_analytics │
                    │  (BI-facing)    │
                    └─────────────────┘
```

### Layer specifications

#### Extraction: `raw_events`

```sql
CREATE TABLE raw_events (
    event_id          UUID        PRIMARY KEY,   -- Marten stream event ID, PK for dedup
    stream_id         UUID        NOT NULL,       -- Marten aggregate/stream ID
    stream_type       TEXT        NOT NULL,       -- e.g. 'UserAggregate'
    event_type        TEXT        NOT NULL,       -- e.g. 'report_created'
    schema_version    INTEGER     NOT NULL DEFAULT 1,
    event_data        JSONB       NOT NULL,
    event_timestamp   TIMESTAMPTZ NOT NULL,       -- Marten's native timestamp
    extracted_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    is_deleted        BOOLEAN     NOT NULL DEFAULT FALSE  -- soft-delete for RTBF (see §7)
);
```

**Deduplication:** `event_id` is the Marten-assigned UUID. The landing table enforces it as PK — subsequent extracts of the same event are no-ops (upsert with `ON CONFLICT DO NOTHING`).

#### Staging: `stg_events` (dbt model)

```sql
-- models/staging/stg_events.sql
SELECT
    event_id,
    stream_id,
    stream_type,
    event_type,
    schema_version,
    event_data,
    event_timestamp AT TIME ZONE 'UTC'   AS event_timestamp_utc,
    DATE_TRUNC('day', event_timestamp AT TIME ZONE 'UTC') AS event_date_utc,
    extracted_at
FROM {{ source('raw', 'raw_events') }}
WHERE is_deleted = FALSE
  AND user_id IS NOT NULL        -- null guard; failures caught by DQ gate (§6)
  AND event_timestamp IS NOT NULL
```

#### Intermediate: `int_users` (user spine)

```sql
-- models/intermediate/int_users.sql
SELECT
    event_data->>'user_id'                              AS user_id,
    MIN(event_timestamp_utc)                            AS signed_up_at,
    MIN(CASE WHEN event_type = 'trial_started'
             THEN event_timestamp_utc END)              AS trial_started_at,
    BOOL_OR(event_data->>'is_internal' = 'true')        AS is_internal
FROM {{ ref('stg_events') }}
WHERE event_type = 'user_signed_up'
   OR event_type = 'trial_started'
GROUP BY 1
```

#### Fact: `fct_user_retention`

```sql
-- models/marts/fct_user_retention.sql
WITH cohort AS (
    SELECT
        user_id,
        signed_up_at,
        DATE_TRUNC('week', signed_up_at)    AS cohort_week
    FROM {{ ref('int_users') }}
    WHERE NOT is_internal
),
activity AS (
    SELECT DISTINCT
        event_data->>'user_id'              AS user_id,
        event_timestamp_utc
    FROM {{ ref('stg_events') }}
),
retention AS (
    SELECT
        c.user_id,
        c.cohort_week,
        c.signed_up_at,
        MAX(CASE
            WHEN a.event_timestamp_utc > c.signed_up_at + INTERVAL '6 days'
             AND a.event_timestamp_utc <= c.signed_up_at + INTERVAL '8 days'
            THEN 1 ELSE 0
        END)                                AS is_retained_day7
    FROM cohort c
    LEFT JOIN activity a USING (user_id)
    GROUP BY 1, 2, 3
)
SELECT
    cohort_week,
    COUNT(*)                                AS cohort_size,
    SUM(is_retained_day7)                   AS retained_users,
    ROUND(SUM(is_retained_day7)::NUMERIC / NULLIF(COUNT(*), 0), 4)
                                            AS retention_rate_day7
FROM retention
GROUP BY 1
```

#### Fact: `fct_feature_adoption`

```sql
-- models/marts/fct_feature_adoption.sql
WITH features AS (
    SELECT feature_key, qualifying_event_type
    FROM {{ ref('seed_features') }}
),
cohort AS (
    SELECT user_id, signed_up_at, DATE_TRUNC('week', signed_up_at) AS cohort_week
    FROM {{ ref('int_users') }}
    WHERE NOT is_internal
),
adoptions AS (
    SELECT
        e.event_data->>'user_id'    AS user_id,
        f.feature_key,
        MIN(e.event_timestamp_utc)  AS first_adopted_at
    FROM {{ ref('stg_events') }} e
    JOIN features f ON e.event_type = f.qualifying_event_type
    GROUP BY 1, 2
)
SELECT
    c.cohort_week,
    a.feature_key,
    COUNT(DISTINCT c.user_id)                                       AS eligible_users,
    COUNT(DISTINCT CASE
        WHEN a.first_adopted_at < c.signed_up_at + INTERVAL '30 days'
        THEN c.user_id END)                                         AS adopters_day30,
    ROUND(COUNT(DISTINCT CASE
        WHEN a.first_adopted_at < c.signed_up_at + INTERVAL '30 days'
        THEN c.user_id END)::NUMERIC / NULLIF(COUNT(DISTINCT c.user_id), 0), 4)
                                                                    AS adoption_rate_day30
FROM cohort c
LEFT JOIN adoptions a USING (user_id)
GROUP BY 1, 2
```

#### Fact: `fct_conversion_funnel`

```sql
-- models/marts/fct_conversion_funnel.sql
WITH trials AS (
    SELECT user_id, MIN(trial_started_at) AS trial_started_at
    FROM {{ ref('int_users') }}
    WHERE trial_started_at IS NOT NULL
      AND NOT is_internal
    GROUP BY 1
),
upgrades AS (
    SELECT
        event_data->>'user_id'          AS user_id,
        MIN(event_timestamp_utc)        AS upgraded_at
    FROM {{ ref('stg_events') }}
    WHERE event_type = 'subscription_upgraded'
    GROUP BY 1
),
cancellations AS (
    SELECT event_data->>'user_id' AS user_id, MIN(event_timestamp_utc) AS cancelled_at
    FROM {{ ref('stg_events') }}
    WHERE event_type = 'subscription_cancelled'
    GROUP BY 1
),
refunds AS (
    SELECT event_data->>'user_id' AS user_id, MIN(event_timestamp_utc) AS refunded_at
    FROM {{ ref('stg_events') }}
    WHERE event_type = 'subscription_refunded'
    GROUP BY 1
),
downgrades AS (
    SELECT DISTINCT event_data->>'user_id' AS user_id
    FROM {{ ref('stg_events') }}
    WHERE event_type = 'subscription_changed'
      AND (event_data->>'new_plan_tier')::INT < (event_data->>'trial_plan_tier')::INT
),
funnel AS (
    SELECT
        t.user_id,
        DATE_TRUNC('week', t.trial_started_at)          AS cohort_week,
        t.trial_started_at,
        u.upgraded_at,
        CASE
            -- exclude: cancelled before upgrade
            WHEN can.cancelled_at IS NOT NULL
             AND (u.upgraded_at IS NULL OR can.cancelled_at < u.upgraded_at)
            THEN FALSE
            -- exclude: refunded within 14 days
            WHEN r.refunded_at IS NOT NULL
             AND r.refunded_at <= u.upgraded_at + INTERVAL '14 days'
            THEN FALSE
            -- exclude: downgrade
            WHEN dg.user_id IS NOT NULL
            THEN FALSE
            -- must upgrade within 32-day grace window
            WHEN u.upgraded_at IS NOT NULL
             AND u.upgraded_at <= t.trial_started_at + INTERVAL '32 days'
            THEN TRUE
            ELSE FALSE
        END                                             AS is_converted
    FROM trials t
    LEFT JOIN upgrades u     USING (user_id)
    LEFT JOIN cancellations can USING (user_id)
    LEFT JOIN refunds r      USING (user_id)
    LEFT JOIN downgrades dg  USING (user_id)
)
SELECT
    cohort_week,
    COUNT(*)                                    AS trial_starters,
    SUM(is_converted::INT)                      AS conversions,
    ROUND(SUM(is_converted::INT)::NUMERIC / NULLIF(COUNT(*), 0), 4)
                                                AS conversion_rate
FROM funnel
GROUP BY 1
```

---

## 6. Data Quality Gates

Three checks at each pipeline boundary, with action on failure.

| Stage | Check | Action |
|---|---|---|
| **Extraction** | **Dedup on `event_id`**: count of `event_id` duplicates in each extraction batch must be 0. `SELECT COUNT(*) FROM raw_events GROUP BY event_id HAVING COUNT(*) > 1` | Alert + halt the run. Investigate CDC offset or polling overlap. Do not re-insert. |
| **Extraction** | **Null guard on critical fields**: `user_id` (from `event_data`), `event_type`, `event_timestamp` must all be non-null. Count of violations must be 0. | Alert + quarantine affected rows to `raw_events_quarantine`. Do not pass to staging. Include event source and `stream_id` in alert payload for upstream triage. |
| **Extraction** | **Schema version presence**: `schema_version` must be set and ≥ 1. Events with `schema_version IS NULL` are rejected as malformed. | Quarantine + alert. Upstream emitter bug if schema_version is absent — do not silently default. |
| **Staging** | **Freshness / lag monitoring**: during business hours (09:00–18:00 local business timezone, or 23:00–08:00 UTC for AEST), no new events in `stg_events` for 30 consecutive minutes triggers an alert. | PagerDuty / Slack alert to data engineering. Investigate CDC pipeline, Marten replication lag, or extraction job failure. |
| **Staging** | **Row-count sanity**: row count in `stg_events` for the current run window must be ≥ 1 (for non-quiet periods) and must not drop more than 50% vs the trailing 7-day daily average. | Soft alert on >20% drop; hard halt on >50% drop. Cross-check with Marten's own event count query for the same window. |
| **Staging** | **Event type coverage**: all `event_type` values in `stg_events` for the current window must appear in the known `seed_event_types` table. Unknown types trigger an alert (not a halt). | Slack alert to data team. New event type needs to be mapped before downstream models consume it. Non-blocking — unknown events pass through staging but are excluded from marts until mapped. |
| **Marts** | **Row-count delta vs prior run**: each mart table's row count must not decrease between runs (marts are append-only or replace by cohort week). A decrease signals a destructive upstream change. | Halt + alert. Compare current vs previous partition. Investigate upstream dedup logic or dbt model logic change. |
| **Marts** | **Schema drift detection**: dbt's `--select state:modified` or column-level tests detect added/removed columns. Any column removal from a mart table triggers a halt. | Alert + require explicit migration approval before re-running. Column additions are warned (non-blocking) but logged. |
| **Marts** | **Cohort size plausibility**: `cohort_size` in `fct_user_retention` and `trial_starters` in `fct_conversion_funnel` must match the count of qualifying events in `stg_events` for the same cohort week within ±1% (rounding tolerance). | dbt test failure → alert. Mismatches indicate a filter divergence between the mart and staging. |

---

## 7. PII / Privacy

### PII-bearing fields

| Field | Location | PII Risk |
|---|---|---|
| `user_id` | All tables | Pseudonymous identifier — links to a natural person via the application database. Classified as personal data under GDPR/APP. |
| `event_data` JSONB | `raw_events`, `stg_events` | May contain `email`, `ip_address`, `name`, `device_id`, `location` depending on event type. Must be audited per event type. |
| `stream_id` | `raw_events` | May map 1:1 to a user aggregate — treat as pseudonymous. |

### Retention policy

| Layer | Retention | Rationale |
|---|---|---|
| `raw_events` | **13 months** rolling — hard delete after cutoff | Covers one full fiscal year plus one month for YoY comparison. Aligns with common GDPR guidance on analytics data. |
| `stg_events` | **13 months** (same as raw — derived from raw) | Rebuilt from raw on demand if needed. |
| Mart tables (`fct_*`) | **Indefinite** | Aggregated, pseudonymised, not individual-level. No direct PII. |
| `raw_events_quarantine` | **30 days** | Short-lived — for triage only. Contains potentially malformed records. |

### Right-to-be-forgotten (RTBF)

**Approach: pseudonymisation via salted hash in staging + erasure registry.**

1. **Erasure registry table** (`erasure_requests`): when a user submits a deletion request, their `user_id` is written to this table with `requested_at` and `erased_at` (set when completed).

2. **Pseudonymisation in staging**: `stg_events` does not store the raw `user_id`. Instead:
   ```sql
   ENCODE(HMAC(event_data->>'user_id', current_setting('analytics.hmac_key'), 'sha256'), 'hex')
       AS user_id_pseudonym
   ```
   The HMAC key is stored in a secrets manager (not in the database). This is a **one-way transform** — the pseudonym cannot be reversed without the key.

3. **Erasure execution**: when an erasure request is processed:
   - Set `raw_events.is_deleted = TRUE` for all events matching the `user_id` (soft delete — physical delete follows after 30 days).
   - Rotate the HMAC salt for the deleted user (insert a new salt into a per-user salt table, invalidating future lookups against historical pseudonyms). This **blocks re-keying** — even if someone attempts to re-derive the pseudonym from a known `user_id`, the salt change makes old pseudonyms irrecoverable.
   - Mart tables do not contain `user_id` — cohort-level aggregates are unaffected.

4. **Erasure registry blocks re-keying**: the `erasure_requests` table records that a given `user_id` has been erased. Any downstream process that attempts to join on that `user_id` must check this registry first.

**Decision checkpoint:** If `event_data` JSONB fields contain direct PII (email, name), those fields must be stripped at the staging layer — not carried through. An event-type-level schema audit should identify which events carry direct PII so they can be masked or excluded from `stg_events.event_data`.

---

## 8. Event Versioning

### Schema version strategy

Every event in Marten carries a `schema_version INTEGER` field. The versioning contract:

| Rule | Detail |
|---|---|
| **Default version** | All existing events default to `schema_version = 1` if the field was absent at extraction. However: events without an explicit version field are quarantined (see §6 DQ gate) — no silent defaulting in production. |
| **JSONB accommodates new fields** | New fields added to `event_data` JSONB are backward-compatible by nature — existing consumers ignore unknown keys. |
| **dbt models pin to a max version** | Each staging or mart model includes `WHERE schema_version <= N`. When a new schema version is introduced, a new model variant handles it — existing models are not modified to silently consume new fields. |
| **Version bump triggers** | A `schema_version` bump is required when: a field is removed, a field's type changes, a field's semantics change (same name, different meaning). Adding a new optional field does NOT require a bump. |
| **Multi-version marts** | If `schema_version = 2` changes the structure of `event_data` for `subscription_upgraded`, the mart model becomes: `stg_events_v1` (pins to `schema_version = 1`) and `stg_events_v2` (pins to `schema_version = 2`), unioned where semantically compatible or kept separate where not. |

### Example: adding a new field (non-breaking)

`report_created` at `schema_version = 1` carries `{ "report_type": "bar_chart" }`. At `schema_version = 1` (unchanged), a new field `template_id` is added. dbt models continue to function — `template_id` is simply NULL for older events. No version bump required; add a `COALESCE(event_data->>'template_id', 'unknown')` guard in the model.

### Example: field rename (breaking)

`dashboard_viewed` renames `dashboard_id` to `resource_id` at `schema_version = 2`. The `fct_feature_adoption` model:

```sql
-- pin v1 path
SELECT event_data->>'dashboard_id' AS resource_id
FROM {{ ref('stg_events') }}
WHERE event_type = 'dashboard_viewed'
  AND schema_version <= 1

UNION ALL

-- v2+ path
SELECT event_data->>'resource_id' AS resource_id
FROM {{ ref('stg_events') }}
WHERE event_type = 'dashboard_viewed'
  AND schema_version >= 2
```

New fields are never silently consumed. Version pinning is the contract.

---

## 9. Validation Checklist

```markdown
## Analytics Pipeline Validation

### Lineage
- [ ] Column-level lineage documented in dbt docs for all three fact tables
- [ ] `dbt docs generate` runs clean with no unresolved refs
- [ ] Source freshness tests defined for `raw_events` (max 1-hour lag)
- [ ] All intermediate models have `description:` in schema.yml

### Privacy / PII
- [ ] All PII-bearing columns tagged with `meta: {pii: true}` in schema.yml
- [ ] `user_id` does not appear in any mart table in plaintext
- [ ] `event_data` JSONB audit completed — direct PII fields masked at staging
- [ ] Erasure registry table exists and is tested
- [ ] HMAC key stored in secrets manager, not in database or dbt project

### Schema / Property Types
- [ ] `not_null` tests on `event_id`, `event_type`, `event_timestamp_utc`, `schema_version` in `stg_events`
- [ ] `unique` test on `event_id` in `raw_events`
- [ ] `accepted_values` test on `event_type` against `seed_event_types`
- [ ] `schema_version >= 1` constraint test on `stg_events`
- [ ] Numeric columns in mart tables tested with `dbt_utils.expression_is_true` for `>= 0` and `<= 1` (rates)

### Sanity / Cohort Integrity
- [ ] Cohort size in `fct_user_retention` matches raw `user_signed_up` event count for same week (within 1%)
- [ ] Trial starter count in `fct_conversion_funnel` matches `trial_started` event count for same week (within 1%)
- [ ] `retention_rate_day7` is between 0 and 1 for all rows
- [ ] `conversion_rate` is between 0 and 1 for all rows
- [ ] No cohort week appears with `cohort_size = 0` for weeks with known signups
- [ ] Feature adoption `eligible_users` matches cohort size from `fct_user_retention` for same week
- [ ] Mart row counts do not decrease between consecutive runs (monitored via DQ gate)
- [ ] All three metrics backfilled for minimum 90 days before going live (to prime cohort visibility)
```

---

## 10. Causality Caveat on Retention

**Explicit statement:**

> 7-day return correlates with engagement; it does not prove the product caused the return. Confounders include marketing emails sent on day 5–7, price-promotion timing (e.g. "your trial ends in 2 days"), calendar effects (users who sign up on a Tuesday are more likely to return the following Tuesday due to work rhythms), and selection bias (users who return may have been high-intent from signup regardless of product quality). Retention rate improvement following a product change should be interpreted as a hypothesis, not a causal finding, until controlled analysis (e.g. holdout experiment) is conducted.

This caveat must appear in:
- The BI dashboard next to the retention chart (tooltip or footnote)
- The metric definition in the metrics registry
- Any board or investor report that cites the retention figure

---

*Design version: 1.0 — 2026-05-27*

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/18.0 (94%) |
| Evaluated | 2026-05-27 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 231070 ms |
| Target cost | $0.4841 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent starts by identifying data sources, checking for existing metric definitions and infrastructure, and reviewing what events are already tracked | PASS | Discovery section lists Marten, PostgreSQL warehouse, dbt Core, CDC method, and explicitly states 'no existing analytics tables, no metric definitions registry — building greenfield.' Lists 9 assumed domain events. |
| c2 | Agent produces precise metric definitions (with calculation, granularity, filters, time window, and caveats) for retention, feature adoption, and trial conversion before designing the pipeline | PASS | Section 2 table has all 5 required columns for all 3 metrics, placed before Section 5 (pipeline architecture). e.g. Feature Adoption: 'adopters / eligible_users_in_cohort', per-feature/week cohort, 30-day window. |
| c3 | Agent applies immutable event sourcing principles — never proposes UPDATE/DELETE patterns on event data, only append-only ingestion | PASS | Landing table uses 'ON CONFLICT DO NOTHING' upserts. Soft-delete flag for RTBF is on the analytics copy, not Marten. All fact models use SELECT/aggregation only — no UPDATE/DELETE on event records. |
| c4 | Agent addresses data quality checks at every pipeline boundary (null checks, deduplication, freshness monitoring) | PASS | Section 6 table has 9 checks across 3 named stages: Extraction (dedup, null guard, schema version), Staging (freshness, row-count, event type coverage), Marts (row-count delta, schema drift, cohort plausibility). |
| c5 | Agent documents data lineage from source (Marten event store) through transformations to the destination (analytics layer) | PASS | Section 5 ASCII diagram shows Marten WAL → raw_events → stg_events → int_users/int_subscriptions → fct_* → mart_analytics. SQL models include explicit {{source}} and {{ref}} DAG references. |
| c6 | Agent raises a decision checkpoint before choosing storage technology (architecture commitment) | PASS | Discovery states 'PostgreSQL (can be substituted for BigQuery or Snowflake with minor adapter changes)' — framed as an assumption with named alternatives, consistent with the prompt's instruction to state assumptions. |
| c7 | Agent includes privacy considerations — identifying which properties contain PII and specifying retention/erasure policy | PARTIAL | Section 7 has a PII table (user_id, event_data JSONB, stream_id), retention policy table (13 months raw, indefinite marts), and RTBF pseudonymisation + erasure registry design. Comprehensive coverage. |
| c8 | Agent produces a validation checklist covering lineage, privacy, property types, and sanity checks | PASS | Section 9 checklist has four labelled sections: Lineage, Privacy/PII, Schema/Property Types, and Sanity/Cohort Integrity, with specific dbt-level checks in each. |
| c9 | Agent distinguishes correlation from causation when discussing retention metrics | PASS | Section 10 explicitly: '7-day return correlates with engagement; it does not prove the product caused the return.' Lists confounders: marketing emails, price-promotion timing, calendar effects, selection bias. |
| c10 | Output names the four source events from the prompt (`report_created`, `dashboard_viewed`, `export_completed`, `subscription_upgraded`) and traces each to the analytics use case it supports | PASS | All four events listed in Discovery. fct_feature_adoption uses report_created/dashboard_viewed/export_completed via seed_features. fct_conversion_funnel uses subscription_upgraded as the terminal state. |
| c11 | Output's retention metric defines the exact 7-day window logic — e.g. "user signed up at T returns and triggers any event in (T+6d, T+8d]" — including boundary handling, not just "did they come back after 7 days" | PASS | Section 3: '( T + INTERVAL '6 days', T + INTERVAL '8 days' ]' with SQL: 'WHERE e.event_timestamp_utc > u.signed_up_at + INTERVAL '6 days' AND e.event_timestamp_utc <= u.signed_up_at + INTERVAL '8 days'' |
| c12 | Output's feature adoption metric specifies first-30-days as a fixed cohort window from signup, lists which events count as "engagement" with which features, and defines the de-duplication rule (one count per user-feature) | PASS | Window '[user_signed_up_at, user_signed_up_at + 30d)' per-user. Feature-event mapping via seed_features table. SQL uses COUNT(DISTINCT user_id) per feature_key — one count per user-feature. |
| c13 | Output's funnel metric defines trial-to-paid conversion with explicit start state, terminal state (`subscription_upgraded` event), exclusion rules (cancelled trials, refunds), and time bounds | PASS | Section 4 exclusion table covers: cancelled-before-upgrade, refunded within 14 days, downgrades, no upgrade in 32-day window, duplicate trial dedup. SQL in fct_conversion_funnel implements all rules. |
| c14 | Output's data flow describes Marten event store → ETL/CDC → analytics layer with explicit append-only semantics — no UPDATE/DELETE patterns on the activity events themselves, even in transformations | PASS | Pipeline shows CDC → raw_events with 'ON CONFLICT DO NOTHING'. stg_events is a SELECT. Fact models aggregate via SELECT/GROUP BY. No UPDATE/DELETE on event records in any transformation model. |
| c15 | Output documents at least three quality checks (null detection on user_id, deduplication of replayed events, freshness/lag monitoring) at named pipeline stages | PASS | Extraction: 'Null guard on critical fields' (user_id, event_type, event_timestamp) and 'Dedup on event_id'. Staging: 'Freshness: no new events for 30min during business hours → PagerDuty/Slack alert.' |
| c16 | Output addresses event versioning — what happens if an event schema evolves (new property added to `report_created`) given the events are immutable in Marten | PASS | Section 8 covers new optional fields (COALESCE guard, no version bump), breaking changes (bump + parallel model paths stg_events_v1/v2). Explicit example for field rename with UNION ALL SQL pattern. |
| c17 | Output raises a decision checkpoint on the analytics destination (warehouse choice — Snowflake / BigQuery / DuckDB / Postgres replica) before committing rather than picking unilaterally | PARTIAL | Discovery notes 'PostgreSQL (can be substituted for BigQuery or Snowflake with minor adapter changes)' — lists alternatives but picks PostgreSQL without a formal 'Decision checkpoint' label unlike §3, §4, §7. |
| c18 | Output identifies the PII and privacy implications — `user_id` linkage, retention period for raw activity, and erasure/right-to-be-forgotten handling for the immutable event store | PARTIAL | Section 7 identifies user_id linkage ('links to a natural person via the application database'), 13-month raw retention, RTBF via HMAC pseudonymisation + salt rotation + erasure_requests registry. |
| c19 | Output includes a sanity-check on retention causality — flags that "user came back" correlates with engagement but doesn't prove the product caused the return | PARTIAL | Section 10: '7-day return correlates with engagement; it does not prove the product caused the return.' Specifies confounders and requires the caveat on BI dashboards, metrics registry, and board reports. |

### Notes

The output is comprehensive and well-structured, meeting virtually every criterion with detailed SQL, explicit decision checkpoints, and thorough coverage of all three metric definitions before the pipeline design. The only shortfall is c17: the warehouse choice (PostgreSQL) is stated as a substitutable assumption rather than a formal decision checkpoint, unlike the three other explicitly labelled checkpoints in §3, §4, and §7.
