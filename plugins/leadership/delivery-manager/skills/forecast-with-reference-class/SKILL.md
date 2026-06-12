---
name: forecast-with-reference-class
description: "Forecast a delivery using reference-class forecasting — historical actuals-vs-estimates from similar past deliveries rather than bottoms-up team estimates under pressure. Corrects the planning fallacy (Kahneman/Lovallo, via Flyvbjerg). Use when a date or commitment is being set, when a team estimate looks optimistic, or when stakeholders are pushing for a number."
argument-hint: "[the delivery or commitment being forecast]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Forecast with a reference class

Produce a reference-class forecast for $ARGUMENTS. Bottoms-up team estimates made under stakeholder pressure are systematically optimistic — this is the planning fallacy ([Kahneman and Lovallo](https://thedecisionlab.com/biases/planning-fallacy), operationalised for delivery by Bent Flyvbjerg's reference-class forecasting). The correction is to forecast from what actually happened on similar past deliveries, not from a fresh estimate of how this one will go. A delivery-manager who only ever presents what the team says will consistently over-promise.

This skill is the antidote to the planning-fallacy dysfunction. It draws on the historical status reports (`write-status-report`) the delivery-manager has been keeping — the actuals-vs-estimates record.

## Step 1: Define the thing being forecast

State precisely what is being forecast: a delivery date, a phase duration, an effort estimate, a throughput. Reference-class forecasting works on a comparable unit — "when will the payments rebuild be done" is forecastable; "when will the product be finished" is not. Narrow it until it has a comparable reference class.

## Step 2: Build the reference class

Identify past deliveries similar enough to this one to be comparable. For each, pull the original estimate and the actual outcome:

```markdown
| Past delivery | Original estimate | Actual | Ratio (actual / estimate) |
|---|---|---|---|
| Billing migration | 8 weeks | 13 weeks | 1.63 |
| Search rebuild | 6 weeks | 9 weeks | 1.50 |
| Notifications service | 10 weeks | 14 weeks | 1.40 |
```

Draw these from the historical status reports and delivery records. The more comparable deliveries in the class, the stronger the forecast. Three to five is a usable minimum; one is an anecdote, not a reference class. If no historical data exists, say so explicitly — a reference-class forecast without a reference class is just a guess wearing a label (this is a decision checkpoint, not something to fabricate).

## Step 3: Derive the correction factor

From the reference class, derive the typical ratio of actual to estimate. The median ratio is usually more robust than the mean for small classes (it resists the one runaway delivery). In the example above the median ratio is 1.50 — past deliveries took, on average, 50% longer than estimated.

## Step 4: Apply the correction to the bottoms-up estimate

Take the team's bottoms-up estimate and apply the correction:

```markdown
- Team's bottoms-up estimate: 8 weeks
- Reference-class median ratio: 1.50
- Reference-class forecast: 12 weeks
```

Present both numbers. The bottoms-up estimate is what the team believes; the reference-class forecast is what history suggests. The gap between them is the planning-fallacy correction. Where they diverge sharply, the divergence itself is the finding — surface it rather than silently picking one.

## Step 5: Recommend the commitment

Recommend what to commit to, with the reasoning visible. Under stakeholder pressure the temptation is to commit to the bottoms-up number; the discipline is to commit to the reference-class forecast and explain why. If the team's estimate must be used (no reference class exists, or this delivery is genuinely novel), say so and flag the optimism risk explicitly.

## Rules

- Forecast from history, not from a fresh estimate under pressure. The fresh estimate is exactly what the planning fallacy corrupts.
- A reference class needs comparable deliveries. One past delivery is an anecdote; three to five is a usable class.
- Never fabricate historical data to fill a reference class. If the actuals do not exist, say so and flag that the forecast is weak.
- Present both numbers — the bottoms-up estimate and the reference-class forecast. The gap is the finding, not noise to hide.
- Prefer the median ratio for small classes; it resists a single runaway outlier distorting the correction.
- Don't commit to the optimistic number just because stakeholders want it. Committing to a date the reference class contradicts embeds the planning fallacy into the commitment (decision checkpoint).

## Output Format

```markdown
## Reference-Class Forecast: [delivery]

### Forecasting
| Field | Value |
|---|---|
| What is forecast | [date / duration / effort] |
| Team bottoms-up estimate | [value] |

### Reference class
| Past delivery | Estimate | Actual | Ratio |
|---|---|---|---|

- Median ratio: [value]
- Reference-class forecast: [corrected value]

### Recommendation
- Commit to: [value]
- Reasoning: [why this number, citing the reference class]
- Optimism risk if the team estimate is used instead: [low / medium / high]
```

## Related skills

- `/delivery-manager:write-status-report` — the historical status reports are the actuals-vs-estimates source this forecast draws on. The discipline of recording real outcomes weekly is what makes a reference class possible later.
- `/delivery-manager:prepare-steering-pack` — when a commitment goes to a steering committee, present the reference-class forecast, not the bottoms-up estimate. The gap between them is the planning-fallacy correction the committee needs to see.
