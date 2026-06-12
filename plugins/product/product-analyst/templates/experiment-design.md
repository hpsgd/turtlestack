# Experiment Design — [change]

> Produced by `/product-analyst:design-experiment`. All sections fixed before launch — no post-hoc edits to metrics or stopping rules.

## Hypothesis

> Because [evidence/reason], we believe [change] will [increase/decrease] [primary metric]
> by [amount] for [segment].

| Slot | Value |
|---|---|
| Reason / evidence | |
| Change | |
| Primary metric | |
| Direction & size (MDE) | |
| Segment | |

## Prior evidence

| Field | Value |
|---|---|
| Evidence type | observed behaviour / stated intent / opinion |
| Strength | strong / weak / weakest |
| Recommendation | run full experiment now / run a cheaper test (fake door, smoke test) first |

## Design

| Field | Value |
|---|---|
| Experiment type | A/B / holdout / A/B/n / switchback / geo |
| Randomisation unit | user / session / account |
| Why this type & unit | |

## Metrics

| Role | Metric | Definition |
|---|---|---|
| Primary (OEC) | one only | |
| Guardrail | must not regress | |
| Guardrail | | |
| Secondary | context only | |

## Power

| Input | Value |
|---|---|
| Baseline rate | |
| Minimum detectable effect (MDE) | smallest lift worth shipping (set by product-manager) |
| Significance level (α) | 0.05 |
| Power (1−β) | 0.80 |
| Sample size per variant | |
| Traffic per day | |
| Expected runtime | days |

## Stopping & decision rules

| Field | Value |
|---|---|
| Minimum runtime | ≥ one full business cycle |
| Read method | fixed horizon / sequential (peeking allowed only if sequential) |
| Ship if | primary-metric result that ships the change |
| Kill if | result that kills it |
| Inconclusive if | result that decides nothing |

## Hand-off

| Item | Detail |
|---|---|
| data-engineer implements | assignment, logging, metric pipeline |
| Needs sign-off | product-manager (MDE, segment exposure) |
