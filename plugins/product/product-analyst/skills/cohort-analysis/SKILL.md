---
name: cohort-analysis
description: "Analyse retention curves and cohort behaviour, cutting by segment and benchmarking the curve shape against what is healthy for the product type. Use when measuring retention, comparing signup cohorts, diagnosing whether a product has product-market fit, or finding where users drop off."
argument-hint: "[product, cohort dimension, or retention question]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Cohort and Retention Analysis

Analyse cohorts and retention for **$ARGUMENTS**. Aggregate metrics lie — "average retention is 40%" hides that one cohort retains at 60% and another at 20%. This skill groups users by a shared starting characteristic, tracks them over time, and reads the curve shape against a healthy benchmark for the product type. It consumes events defined in `/product-analyst:write-instrumentation-spec` and informs whether the North Star from `/product-analyst:define-north-star` is actually being delivered.

## Step 1: Pick the cohort dimension and the retention event

A cohort is a group sharing a starting characteristic. Choose the dimension that answers the question:

| Dimension | Answers |
|---|---|
| Signup week/month | Is the product getting better over time? |
| Acquisition channel | Which channels bring users who stay? |
| Activation behaviour | Do users who did X retain better? (correlation, not cause) |
| Plan / segment | Do paid users retain differently from free? |

Then define the **retention event** — the action that counts as "still active." This must be the value action, not "opened the app." Returning without getting value is not retention.

Verifiable output: the cohort dimension and the precise retention event, both defined.

## Step 2: Choose the retention definition

There are three, and they answer different questions. State which you're using:

- **N-day retention** — active on exactly day N. Strict; good for daily-use products
- **Unbounded (rolling) retention** — active on day N *or later*. Forgiving; good for less-frequent products
- **Bracket retention** — active within a window (days 7-14). Best for weekly/monthly-use products

Picking the wrong one misreads the product: N-day retention makes a healthy monthly product look dead.

Verifiable output: the retention definition named, with one line on why it fits the product's natural usage frequency.

## Step 3: Build the cohort table and curve

Construct the triangle: rows are cohorts, columns are periods since start, cells are the retained fraction. Plot the retention curve (retention % against period). If you have query access, write the SQL with the business question as a comment and bot/test/internal exclusions explicit; otherwise specify the query for the data-engineer.

Verifiable output: a cohort retention table and the curve for each cohort.

## Step 4: Read the curve shape against the healthy benchmark

The curve shape is the diagnosis. Compare against what's healthy for the product type:

| Curve shape | Meaning |
|---|---|
| Decays to zero | No product-market fit. Users try it and leave. The most important thing to find — acquisition can't fix it |
| Flattens above zero ("smile" or plateau) | Product-market fit. A stable cohort keeps coming back. The plateau height is the fit strength |
| Flattens then rises (smile curve) | Strong fit with resurrection — lapsed users return. Best shape |

Healthy plateau heights differ by product type:

| Product type | A healthy flattening plateau is roughly |
|---|---|
| Daily-use consumer (social, messaging) | High — daily actives a large fraction of signups |
| Weekly SaaS / productivity | Moderate — a meaningful fraction return weekly |
| Transactional / infrequent (travel, events) | Lower absolute, but must still flatten, not hit zero |
| B2B platform | Account-level retention should be high; seat-level varies |

The absolute number matters less than whether the curve **flattens**. A curve still falling at the last period has not proven fit.

Verifiable output: a curve-shape verdict (fit / no fit / improving) with the plateau height and the benchmark it's read against.

## Step 5: Cut by segment to find the pattern

A flat aggregate can hide a great cohort and a dying one cancelling out. Cut the cohorts by a second dimension (channel within signup-month, plan within channel) to find where retention is strong and where it's bleeding. The strong segment shows where fit already exists; the weak segment shows where to focus or stop spending.

Verifiable output: at least one segment cut showing retention divergence, with the strongest and weakest segments named.

## Step 6: Write the analysis

Write the cohort analysis to `docs/analytics/`. Lead with the curve-shape verdict (the answer), then the table, then the segment cuts, then what to investigate next. Flag every causal-sounding finding as correlation unless an experiment backs it.

## Rules

- The retention event is the value action, not "opened the app." Counting returns without value inflates retention into a vanity number
- Match the retention definition (N-day / unbounded / bracket) to the product's natural usage frequency. A monthly product judged on daily retention will always look dead
- The verdict is the curve *shape*, not a single retention number. A flattening curve at 25% beats a still-falling curve at 45%
- A curve that hasn't flattened by the last observed period has not proven product-market fit — say "not yet proven," not "low retention"
- Cohort correlations are not causation. "Users who did X retain better" means those users were probably already more engaged. Flag it and route to `/product-analyst:design-experiment` to test
- Always exclude bots, test, and internal accounts, and state the exclusion. Internal users retain at ~100% and poison every cohort
- Don't report an aggregate without at least one segment cut — the aggregate is where two opposite truths hide

## Output Format

```markdown
## Cohort Analysis: [product / question]

### Verdict
[product-market fit / no fit / fit improving] — curve [flattens at X% / decays to zero / rising]

### Setup
- Cohort dimension: [signup week / channel / ...]
- Retention event: [the value action]
- Retention definition: [N-day / unbounded / bracket] because [usage frequency]
- Exclusions: bots, test accounts, internal users

### Retention table
| Cohort | P0 | P1 | P2 | ... | Plateau |
|---|---|---|---|---|---|
| [cohort] | 100% | x% | y% | ... | z% |

### Curve read against benchmark
[shape] vs healthy [product-type benchmark] → [verdict]

### Segment cut
Strongest: [segment] at [retention]. Weakest: [segment] at [retention].

### Next
[what to investigate; correlations to test via experiment]
```
