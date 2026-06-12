---
name: assumption-map
description: "Map the assumptions a bet depends on on two axes — how much we know (knowledge) and how much it matters if we're wrong (impact). Produces a prioritised list of which assumptions to test first. Use before committing engineering effort to a solution, to find the riskiest assumptions cheaply."
argument-hint: "[the bet, solution, or business idea to de-risk]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Map the assumptions behind $ARGUMENTS.

Every bet rests on assumptions — about whether customers want it, whether they'll use it, whether the
business case holds. Most "validation" tests the assumptions that are comfortable to test, not the ones
that would sink the idea. This skill applies [David Bland and Alex Osterwalder's assumption mapping](https://www.strategyzer.com/library/testing-business-ideas-book-summary)
(Testing Business Ideas): plot each assumption on knowledge × impact and test the high-impact, low-knowledge
ones first.

Follow every step. The output is a two-axis map and a prioritised test list.

## Step 1: Surface the assumptions

List everything that must be true for the bet to work. Cover the four risk areas so you don't only surface
the comfortable (feasibility) ones:

| Risk area | Assumption prompt |
|-----------|-------------------|
| **Desirability** | Do customers want this? Does it solve a real problem they have? |
| **Viability** | Does the business case work? Will they pay? Does it fit the model? |
| **Feasibility** | Can we build and run it with what we have? |
| **Usability** | Can they figure out how to use it? |

Write each as a falsifiable statement: "Ops managers will switch from their spreadsheet within one billing
cycle", not "the product is good". This step is complete when you have a list of falsifiable assumptions
across all four areas.

## Step 2: Score each assumption on the two axes

For each assumption, score:

- **Knowledge (x-axis):** how much do we actually know about this? Evidence we have → no evidence at all
- **Impact (y-axis):** if we're wrong, how badly does the bet fail? Low → the bet survives; High → the bet
  dies

Use real evidence to place knowledge, not confidence. "We feel sure" is not knowledge — knowledge is data.
This step is complete when every assumption has a knowledge score and an impact score.

## Step 3: Plot the quadrants

Place each assumption in the grid:

| | Low knowledge | High knowledge |
|---|---|---|
| **High impact** | **TEST FIRST** — the bet rests on these and you don't know | Watch — important but established |
| **Low impact** | Defer — uncertain but doesn't matter much | Ignore — known and low-stakes |

The target quadrant is **high impact, low knowledge**: the assumptions the bet depends on that you have no
evidence for. Those are what to test. High-knowledge, low-impact assumptions are established facts — don't
waste an experiment on them. This step is complete when each assumption sits in a named quadrant.

## Step 4: Recommend experiments for the target quadrant

For each high-impact, low-knowledge assumption, recommend the test that would move it. Match evidence
strength to the stakes — and remember the evidence hierarchy: actual behaviour (purchases, usage,
retention) > stated intentions > opinions. Most "validation" collects the weakest type.

- Desirability/value assumptions → a pretotype (`/product-manager:design-pretotype`) — fake door, smoke
  test, concierge
- Behavioural/usage assumptions → a Wizard of Oz or concierge run
- Demand assumptions → a smoke-test landing page with a real call-to-action

This step is complete when every target-quadrant assumption has a recommended experiment.

## Rules

- **Test the riskiest, not the easiest.** Teams default to testing feasibility because engineers are
  comfortable there. The bet usually dies on desirability or viability — map all four areas.
- **Knowledge is evidence, not confidence.** "We're pretty sure" places an assumption in low knowledge,
  not high. Only data earns the high-knowledge column.
- **Don't test what you already know.** High-knowledge, low-impact assumptions are facts. Spend experiments
  on the target quadrant only.
- **Falsifiable statements only.** "The product is valuable" can't be tested. "30% of trial users will
  complete setup unaided" can.
- **Behaviour beats stated intent.** When you recommend a test, prefer one that measures what people do
  over what they say.

## Output Format

Write to `docs/product/assumption-map-[bet-slug].md`:

```markdown
# Assumption map: [bet]

## Assumptions
| # | Assumption (falsifiable) | Risk area | Knowledge (low/high) | Impact (low/high) | Quadrant |
|---|--------------------------|-----------|----------------------|-------------------|----------|
| 1 | ... | Desirability | low | high | TEST FIRST |

## Test first (high impact, low knowledge)
| Assumption | Recommended experiment | Evidence type |
|------------|------------------------|---------------|
| ... | [pretotype / Wizard of Oz / smoke test] | behaviour / intent |

## Deferred / ignored
- [assumption] — [why it doesn't need testing now]
```

## Related Skills

- `/product-manager:design-pretotype` — designs the experiments for the target-quadrant assumptions.
- `/product-manager:write-opportunity-solution-tree` — assumptions hang off solutions on the tree.
- `/product-manager:write-prd` — the riskiest assumption belongs in the PRD's pre-mortem.
