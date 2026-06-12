---
name: define-north-star
description: "Define a product's North Star Metric and its supporting input metrics, with explicit checks against Goodhart's Law and multi-customer-type incoherence. Use when establishing the single metric that captures delivered customer value, or auditing an existing North Star for gaming risk."
argument-hint: "[product or product area]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Define the North Star Metric

Define the North Star Metric (NSM) and input metrics for **$ARGUMENTS**. The North Star is the single number that captures the value a customer gets from the product — not revenue, not a vanity count. This skill produces the North Star and the 3-5 input metrics that drive it, then stress-tests both against gaming and segment incoherence. It feeds `/product-analyst:design-metric-hierarchy` (which expands the inputs into a full tree) and the OKRs owned by the product-manager.

## Step 1: State the customer value moment

Before naming a metric, name the moment a customer gets value. Spotify: a song played. Slack: a message sent in an active channel. Airbnb: a night booked and stayed. Write one sentence: "A customer of [product] gets value when [observable event]." If you can't write it, stop — the product's value is unclear and that's a discovery question, not a metrics question. Escalate to the product-manager.

Verifiable output: a single value-moment sentence anchored to an observable event.

## Step 2: Draft the North Star candidate

The North Star expresses the value moment at the right scale and cadence. Choose the shape that matches the product:

| Product type | North Star shape | Example |
|---|---|---|
| Engagement / SaaS | Frequency of the value action by active users | Weekly active users completing the core action |
| Transactional | Volume of completed value exchanges | Nights booked and stayed |
| Marketplace | Matched transactions (both sides win) | Successful matches per week |
| Content / media | Time or depth of genuine consumption | Hours of content consumed (not started) |
| B2B platform | Accounts reaching activated, repeated use | Accounts with 3+ weekly active seats |

Reject any candidate that is cumulative (only goes up), counts starts not completions, or measures company benefit instead of customer benefit.

Verifiable output: one North Star candidate with its definition block (question, definition, calculation, granularity, filters, time window, owner).

## Step 3: Run the Goodhart check

[Goodhart's Law](https://en.wikipedia.org/wiki/Goodhart%27s_law): "When a measure becomes a target, it ceases to be a good measure." For the candidate, ask: if a team optimised this number ruthlessly, what would they do, and would it hurt the customer?

- "Hours consumed" → optimise via dark patterns and autoplay traps. Hurts the customer
- "Messages sent" → optimise via notification spam. Hurts the customer
- "Nights booked and stayed" → hard to game without delivering real stays. Survives

If the candidate fails, add a counter-metric (a guardrail the team must not harm while moving the North Star) or pick a harder-to-game candidate. Document the failure and the fix.

Verifiable output: a Goodhart verdict (survives / needs counter-metric / reject) with the gaming scenario written out.

## Step 4: Run the multi-customer-type coherence check

A North Star must mean the same thing — good — for every customer type the product serves. On a two-sided marketplace, "listings created" is good for sellers and irrelevant to buyers. On a creator platform, "content posted" is good for creators but says nothing about consumers.

List each customer type. For each, state whether the candidate North Star going up is good, bad, or neutral for them. If it's not unambiguously good across all types, the metric is incoherent — either pick a metric that captures the shared value exchange (the match, the transaction, the consumed value) or split into per-side North Stars with a primary.

Verifiable output: a coherence table (customer type × is-up-good?) and a verdict.

## Step 5: Derive the input metrics

The North Star moves slowly and indirectly. Derive 3-5 input metrics the team can move this week. Each input must be **leading** (moves before the North Star) and **controllable** (a team can change it). The classic decomposition: breadth (how many customers), depth (how much each does the action), frequency (how often), efficiency (how easily). An input nobody can influence is a reporting line — drop it.

Verifiable output: 3-5 input metrics, each with a definition block and the team that owns it.

## Step 6: Assemble the canvas

Fill the North Star canvas (`templates/north-star-canvas.md`): value moment, North Star with definition, Goodhart verdict and counter-metric, coherence table, input metrics, and the link to the product-manager's OKRs. Write it to `docs/analytics/`.

## Rules

- Never propose a cumulative metric (total signups, total revenue-to-date) as a North Star — it rises regardless of product quality and is the canonical vanity metric
- Never let revenue be the North Star directly. Revenue is what you get *because* you delivered customer value; measure the value
- Always run both the Goodhart check (Step 3) and the coherence check (Step 4) — skipping either ships a metric that will mislead the team
- Don't count starts when you mean completions. "Onboarding started" is not value; "onboarding completed and first action taken" is
- Don't invent the value moment. If discovery hasn't established it, that's a blocking gap — escalate, don't guess
- Every input metric must be a lever a team can pull this quarter. If it can't, it's not an input

## Output Format

```markdown
## North Star: [product or area]

### Customer value moment
[one sentence anchored to an observable event]

### North Star Metric
[definition block: question, definition, calculation, granularity, filters, time window, owner]

### Goodhart check
- Gaming scenario: [how a team could game it]
- Verdict: [survives / counter-metric added / rejected and replaced]
- Counter-metric (if any): [guardrail that must not be harmed]

### Coherence across customer types
| Customer type | Is North-Star-up good? |
|---|---|
| [type] | [good / bad / neutral] |

Verdict: [coherent / incoherent — resolution applied]

### Input metrics
| Input | Definition | Leading? | Owner |
|---|---|---|---|
| [name] | [precise] | [yes] | [team] |

### Link to OKRs
[which product-manager OKR this North Star serves]
```
