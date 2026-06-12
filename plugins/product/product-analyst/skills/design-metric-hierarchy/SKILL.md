---
name: design-metric-hierarchy
description: "Build a product metric hierarchy using HEART or AARRR depending on product type, decomposing the North Star into actionable input metrics tied to OKRs. Use when structuring product metrics into a tree, choosing between engagement and funnel frameworks, or linking metrics to quarterly goals."
argument-hint: "[product or product area]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Design the Metric Hierarchy

Build the metric hierarchy for **$ARGUMENTS** — the tree that connects the North Star to the input metrics a team can act on, organised by a framework that fits the product. This skill consumes the North Star and inputs from `/product-analyst:define-north-star` and expands them into a structured tree, then ties each branch to the OKRs owned by the product-manager.

## Step 1: Confirm the North Star and product type

Read the existing North Star from `docs/analytics/`. If none exists, run `/product-analyst:define-north-star` first — a hierarchy with no root is just a list. Classify the product type, because it decides the framework in Step 2:

| Product type | Signal |
|---|---|
| Engagement / retention-led SaaS | Value comes from repeated use; success is habit |
| Transactional / funnel-led | Value comes from completing a conversion; success is throughput |
| Marketplace | Two-sided; success is matched transactions |

Verifiable output: the confirmed North Star and a product-type classification with one line of justification.

## Step 2: Choose the framework — HEART or AARRR

Pick by product type. Don't run both; pick the one that matches how the product creates value.

**[HEART](https://research.google/pubs/measuring-the-user-experience-on-a-large-scale-user-centered-metrics-and-the-goals-signals-metrics-process/)** (Google — Rodden, Hutchinson, Fu) for engagement and experience-quality products:

| Dimension | Measures | Example signal |
|---|---|---|
| Happiness | Attitudinal satisfaction | CSAT, in-app survey |
| Engagement | Depth and frequency of use | Actions per active week |
| Adoption | New users reaching value | % new users activating |
| Retention | Users still active over time | 8-week retention |
| Task success | Efficiency and error rate | Completion rate, time-on-task |

HEART pairs with the Goals → Signals → Metrics process: for each dimension state the goal, the behavioural signal, then the metric.

**[AARRR](https://www.500.co/)** (Dave McClure's pirate metrics) for funnel and growth-led products:

| Stage | Question | Example metric |
|---|---|---|
| Acquisition | How do users find us? | New visitors → signups |
| Activation | Do they reach first value? | % completing the aha action |
| Retention | Do they come back? | Day-7 / day-30 return rate |
| Revenue | Do they pay? | Conversion to paid, ARPU |
| Referral | Do they bring others? | Invite rate, k-factor |

Verifiable output: the chosen framework named, with one sentence on why it fits this product over the alternative.

## Step 3: Map the North Star to the framework dimensions

Place the North Star at the root. Under it, map each input metric to a HEART dimension or an AARRR stage. Every dimension or stage that matters for this product gets at least one metric; a dimension with no metric is either irrelevant (say so) or a blind spot (fill it). Each metric carries a definition block.

Verifiable output: a two-level tree (North Star → dimension/stage → metric) with every node defined.

## Step 4: Tie each branch to an OKR

The hierarchy describes the system; OKRs describe this quarter's bet. For each branch, identify which OKR (owned by the product-manager) it serves. A branch with no OKR is being measured but not steered — flag it. An OKR with no branch is a goal with no instrumentation — flag it back to the product-manager. Do not write or change OKRs here; reference them.

Verifiable output: a mapping of branches to OKRs, with orphans flagged in both directions.

## Step 5: Assign ownership and cadence

Each input metric needs a team that owns moving it and a review cadence (weekly for inputs, monthly or quarterly for the North Star). An unowned metric decays into a number nobody acts on.

Verifiable output: owner and cadence on every metric in the tree.

## Step 6: Write the tree

Fill the metric-tree template (`templates/metric-tree.md`) and write it to `docs/analytics/metric-tree.md`. Include the framework choice, the tree, the OKR mapping, and ownership.

## Rules

- Pick one framework — HEART or AARRR — never bolt both onto the same product. The choice is the analysis; running both hides the decision
- Use HEART for engagement/experience products and AARRR for funnel/growth products. If genuinely unsure, the product is probably engagement-led if value comes from repeated use, funnel-led if value comes from a one-time conversion
- Every leaf metric must be an input a team can move, not a lagging outcome. Lagging outcomes belong near the root, not the leaves
- Don't redefine OKRs — they belong to the product-manager. Reference them and flag mismatches
- Don't leave a framework dimension empty without saying whether it's irrelevant or a blind spot — silence hides gaps
- Keep the tree two to three levels deep. A four-level metric tree is a spreadsheet nobody reads

## Output Format

```markdown
## Metric Hierarchy: [product or area]

### Product type & framework
[type] → [HEART | AARRR] because [one sentence]

### Tree
North Star: [metric]
- [Dimension / Stage]
  - [input metric] — owner: [team], cadence: [weekly], definition: [precise]
  - [input metric] — ...
- [Dimension / Stage]
  - ...

### OKR mapping
| Branch | OKR served | Orphan? |
|---|---|---|
| [branch] | [OKR] | [no / metric-without-OKR / OKR-without-metric] |

### Coverage gaps
[dimensions/stages with no metric — irrelevant or blind spot]
```
