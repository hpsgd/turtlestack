---
name: competitor-price-benchmark
description: "Build structured pricing intelligence across the competitive set — list prices, packaging, tiering, add-ons, discounting signals, and the value metric each competitor charges on. Use when you need a clear picture of how the market prices and packages before a pricing or positioning decision. GTM owns pricing; the product-manager consults on packaging; a human approves price changes."
argument-hint: "[product category or named competitors to benchmark]"
user-invocable: true
allowed-tools: Read, Write, Bash, Glob, Grep, WebSearch, WebFetch
---

# Competitor price benchmark

Build a structured pricing benchmark across the competitive set for $ARGUMENTS. The output is a like-for-like comparison of how each competitor prices, packages, and tiers — and what value metric they charge on — so a pricing or positioning decision rests on the actual market shape rather than a vague sense of "they're cheaper."

**Ownership boundary:** GTM owns pricing intelligence and the pricing recommendation. The product-manager **consults** on packaging and tier composition but does not own price. Any price or packaging change is a commercial decision **a human approves**. This skill produces the market picture the human and the product-manager reason with.

Pair this with `/gtm:competitive-analysis` (the broader sales-enablement competitive view) and `/gtm:design-pricing-study` (this benchmark sets the realistic price ranges a willingness-to-pay study should test).

## Step 1 — Define the competitive set and value metric

List the competitors to benchmark, by type, and name the value metric each charges on. The value metric — what they meter and bill against (per seat, per usage unit, per outcome, flat) — is the single most important pricing fact, because two products can look the same price but be radically different at scale.

| Competitor | Type (direct / indirect / substitute) | Value metric | Why this metric matters |
|---|---|---|---|
| [name] | [type] | per seat / usage / flat / tiered / outcome | [how it scales for the buyer] |

Include at least 3 direct competitors and the "manual / spreadsheet / do-nothing" substitute where relevant — its implicit cost is a real anchor in deals.

## Step 2 — Capture published pricing

For each competitor, record what is publicly published. Cite the URL and the date you checked — pricing pages change and stale data is worse than none.

```
## [Competitor]
- Pricing page: [URL] (checked [date])
- Model: [per seat / usage / flat / freemium / enterprise-only]
- Free tier: [what's included, limits]
- Entry tier: [name, price, what's included, key limits]
- Mid tier: [name, price, what's included]
- Top published tier: [name, price, what's included]
- Enterprise: [custom / "contact us" — note if no public price]
- Annual vs monthly: [discount for annual commit]
- Value-metric thresholds: [where the price steps up — seats, usage caps]
```

Rules:

- Record "contact us / no public price" as a finding, not a gap. Hidden enterprise pricing is itself a signal.
- Capture the limits, not just the price. A $20 tier capped at 3 users is not comparable to a $20 tier with 10.
- Date every capture. Mark anything you can't verify "unverified."

## Step 3 — Normalise to a like-for-like comparison

Raw prices are not comparable across different value metrics and tier shapes. Normalise to a common scenario the buyer would recognise — for example, "team of 10 users, moderate usage, annual billing." Compute the effective cost per competitor for 2-3 representative scenarios (small, typical, at-scale).

| Competitor | Small (e.g. 3 users) | Typical (e.g. 10 users) | At scale (e.g. 50 users) | Value metric driving cost |
|---|---|---|---|---|
| Us | [$] | [$] | [$] | [metric] |
| [competitor] | [$] | [$] | [$] | [metric] |

Rules:

- State the scenario assumptions explicitly. The comparison is only honest if the scenarios are named.
- Show where the crossover happens — a competitor cheaper at 3 users may be far more expensive at 50. The crossover point is a selling and positioning insight.
- Include "us" as a row. The benchmark is useless without our own position in it.

## Step 4 — Analyse packaging and tiering

Look past price to packaging structure — what is bundled, gated, and sold as add-ons. This reveals the market's mental model of "good / better / best" and where there is whitespace.

| Capability | Us | Comp A | Comp B | Comp C | Pattern |
|---|---|---|---|---|---|
| [feature] | core / add-on / top-tier / absent | ... | ... | ... | [what the market treats as premium] |

Identify:

- **Standard gating** — features the whole market puts behind the top tier (e.g. SSO, audit logs). These are tier-anchoring conventions; deviating from them is a deliberate choice.
- **Add-on patterns** — what gets unbundled and sold separately.
- **Packaging whitespace** — a tier shape or bundle nobody offers that a segment wants.

## Step 5 — Read the discounting and motion signals

Published price is rarely the transacted price. Capture signals on real discounting and the sales motion:

- Annual-commit discount depth.
- Public promotions, startup/non-profit/education programmes.
- Self-serve vs sales-assisted threshold (where "contact us" kicks in).
- Review-site and forum mentions of negotiated discounts ([G2](https://www.g2.com), [Capterra](https://www.capterra.com), Reddit) — label these as anecdotal.

## Step 6 — Synthesise findings

Pull it together into the market shape and the implications for our pricing and positioning. State what is evidence and what is inference.

Stop at the market picture and the implications. Do **not** propose our own tier prices or a recommended price band — not even labelled "for human approval". Proposing a price is `/gtm:design-pricing-study`'s job (a willingness-to-pay study) and ultimately the human's decision; a benchmark that ends in "we should charge $X" has crossed the boundary. Describe where we *sit* relative to the market and where the whitespace is; let the human and the pricing study set the number.

## Rules

- Normalise before comparing. Raw tier prices across different value metrics are not a benchmark — they're a list. The like-for-like scenario is the deliverable.
- Always include "us" in every table. A competitor benchmark that omits our own position answers nothing.
- The value metric is the headline. Capture what each competitor meters on before you capture the numbers.
- Date and cite every price. Mark unverifiable figures "unverified"; record hidden enterprise pricing as a finding.
- Discounting signals are anecdotal unless sourced from a primary record. Label them so.
- Recommend the market picture, not the price. Never output our own tier prices or a recommended price band — labelling a proposed price "for human approval" does not make it allowed. The number comes from a willingness-to-pay study and the human's decision, not from this benchmark.
- **All output is DRAFT until human-reviewed.** Label every output "DRAFT — requires human review" at the top and bottom.

## Output Format

```markdown
# Competitor price benchmark — [category] (DRAFT — requires human review)

**Ownership:** GTM owns this benchmark. Product-manager consults on packaging. Price changes approved by a human.
**Date checked:** [date]

## Competitive set and value metrics
| Competitor | Type | Value metric | Why it matters |
|---|---|---|---|

## Published pricing
[Per-competitor capture with URLs and dates]

## Like-for-like comparison
**Scenario assumptions:** [stated explicitly]
| Competitor | Small | Typical | At scale | Metric |
|---|---|---|---|---|

## Packaging and tiering
| Capability | Us | A | B | C | Pattern |
|---|---|---|---|---|---|
**Standard gating:** [conventions]
**Add-on patterns:** [...]
**Packaging whitespace:** [...]

## Discounting and motion signals
[Annual discount, programmes, self-serve threshold, anecdotal negotiation signals]

## Synthesis
- Where we sit: [cheap / mid / premium, and at which scale]
- Crossover points: [where competitors flip from cheaper to dearer]
- Implications for pricing: [evidence] / [inference]
- Implications for positioning: [...]

DRAFT — requires human review
```

## Related Skills

- `/gtm:design-pricing-study` — this benchmark sets the realistic price ranges a willingness-to-pay study should test.
- `/gtm:competitive-analysis` — broader sales-enablement competitive view; pricing is one dimension within it.
- `/gtm:positioning` — price position is part of market position; benchmark informs the value framing.
