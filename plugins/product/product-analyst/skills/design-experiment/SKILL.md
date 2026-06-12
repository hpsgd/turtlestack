---
name: design-experiment
description: "Design an A/B test or holdout experiment to establish causation, including hypothesis, sample-size calculation, and the evidence hierarchy that weights observed behaviour over stated intent over opinion. Use when designing an A/B test, sizing an experiment, planning a holdout, or deciding whether a change actually caused an outcome."
argument-hint: "[change or hypothesis to test]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Design an Experiment

Design an experiment to test **$ARGUMENTS**. Correlation is the default; causation must be earned. This skill produces a controlled experiment — A/B or holdout — that can credibly claim a change caused an outcome, with a sample-size calculation so the result is readable. It tests the causal claims that `/product-analyst:cohort-analysis` surfaces and measures whether a change moves the North Star from `/product-analyst:define-north-star`.

## Step 1: Write the hypothesis

A testable hypothesis names the change, the metric, the expected direction and size, and the reason:

> Because [evidence/reason], we believe [change] will [increase/decrease] [metric] by [amount] for [segment].

If you can't fill every slot, you're not ready. "We think this will be better" is not a hypothesis — better at what, by how much, for whom, and why do you believe it?

Verifiable output: a hypothesis with all five slots filled.

## Step 2: Place the evidence on the hierarchy

Before running anything, weight your prior evidence using the hierarchy from David Bland and Alex Osterwalder's *Testing Business Ideas*: **observed behaviour > stated intent > opinion.**

| Evidence strength | Example | Weight |
|---|---|---|
| Observed behaviour | Users already do the workaround the change automates | Strong — worth a full experiment |
| Stated intent | Users said in a survey they'd use it | Weak — they often don't |
| Opinion | A stakeholder is confident it'll work | Weakest — test cheaply first |

If your only evidence is opinion or stated intent, run a cheaper test (fake door, smoke test) before committing engineering to a full A/B. Don't spend a four-week experiment validating a hunch a one-week fake-door could kill.

Verifiable output: the prior evidence classified, with a recommendation on whether to run the full experiment now or a cheaper test first.

## Step 3: Choose the experiment type

| Type | Use when |
|---|---|
| **A/B test** | You can randomly split traffic and show variants concurrently. The default for UI/flow changes |
| **Holdout** | You're rolling out broadly but keep a randomly-held-back control to measure long-run, cumulative impact (good for retention/revenue effects that take weeks) |
| **A/B/n** | Testing several variants — needs more traffic and a multiple-comparisons correction |
| **Switchback / geo** | Marketplace or network effects where users can't be independently split (treatment leaks between users) |

State the randomisation unit (user, session, account) — for B2B, randomise by account or treatment leaks across a team.

Verifiable output: the experiment type and randomisation unit, with the reason.

## Step 4: Define the metrics — primary, guardrail, secondary

- **Primary metric (OEC)** — the one metric the decision rests on. One, not three. Multiple primaries invite cherry-picking
- **Guardrail metrics** — things the change must not harm (latency, error rate, the North Star's counter-metric). A win on the primary that breaks a guardrail is not a win
- **Secondary metrics** — context, not decision criteria

Verifiable output: one primary metric, named guardrails, and secondary metrics, each defined precisely.

## Step 5: Calculate the sample size

The experiment must be large enough to detect the effect you hypothesised. Compute the required sample per variant from four inputs:

- **Baseline rate** — current value of the primary metric
- **Minimum detectable effect (MDE)** — the smallest lift worth shipping (set by the product-manager, not by what's convenient)
- **Significance level (α)** — conventionally 0.05
- **Power (1−β)** — conventionally 0.80

Compute the sample size (use a standard power calculation; for a proportion, `n ≈ 16 × p(1−p) / MDE²` per variant as a rule-of-thumb sanity check, then a proper calculator for the real number). Divide by traffic/day to get the runtime. State the runtime explicitly and never call a result before it ends — early peeking inflates false positives.

Verifiable output: required sample per variant, expected runtime in days, and the four inputs used.

## Step 6: Set the stopping and analysis rules upfront

Decide before launch, to avoid p-hacking:

- **Fixed horizon** — run for the calculated duration, then read once. Or use a sequential-testing method that explicitly allows peeking
- **Minimum runtime** — at least one full business cycle (usually a week) to cover day-of-week effects, even if significance comes early
- **Decision rule** — what primary-metric result ships the change, what kills it, and what counts as inconclusive

Verifiable output: the stopping rule, minimum runtime, and the ship/kill/inconclusive decision rule, all fixed before launch.

## Step 7: Write the design doc

Fill the experiment-design template (`templates/experiment-design.md`): hypothesis, evidence placement, type and randomisation, metrics, sample size and runtime, stopping rules. Write it to `docs/analytics/`. Name the data-engineer as the implementer of assignment and logging.

## Rules

- One primary metric. Multiple primaries let you find a "win" somewhere after the fact — that's p-hacking with extra steps
- Calculate sample size and runtime before launching. An underpowered test that shows "no significant difference" tells you nothing — you couldn't have detected the effect either way
- Never call a result early. Peeking and stopping when significance appears inflates the false-positive rate well above the stated α. Fix the horizon or use a sequential method
- Run for at least one full business cycle. Tuesday's users differ from Saturday's; a three-day test reads the wrong week
- Weight prior evidence by the hierarchy (behaviour > intent > opinion). Don't spend a full experiment on something a cheaper fake-door test would refute
- A guardrail breach overrides a primary-metric win. Shipping a conversion lift that doubles error rate is a loss
- Significant is not the same as worth shipping. State the MDE and confirm the observed effect clears the bar that matters, not just p < 0.05
- Randomise by the right unit. Splitting by session when behaviour is per-user, or by user in a marketplace, leaks treatment and biases the result

## Output Format

```markdown
## Experiment Design: [change]

### Hypothesis
Because [reason], we believe [change] will [direction] [primary metric] by [MDE] for [segment].

### Prior evidence
[observed behaviour / stated intent / opinion] → [run full experiment / run cheaper test first]

### Design
- Type: [A/B / holdout / A/B/n / switchback]
- Randomisation unit: [user / session / account]
- Primary metric (OEC): [definition]
- Guardrails: [metrics that must not regress]
- Secondary: [context metrics]

### Power
- Baseline: [rate] | MDE: [smallest worthwhile lift] | α: 0.05 | power: 0.80
- Sample per variant: [n] | Expected runtime: [days]

### Stopping & decision rules
- Minimum runtime: [≥ one business cycle]
- Read: [fixed horizon / sequential]
- Ship if: [result] | Kill if: [result] | Inconclusive if: [result]

### Hand-off
- data-engineer implements: assignment, logging, metric pipeline
```
