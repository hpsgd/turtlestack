---
name: write-business-model-canvas
description: "Map and pressure-test a business model using Osterwalder's nine-block Business Model Canvas (customer segments, value propositions, channels, customer relationships, revenue streams, key resources, key activities, key partnerships, cost structure). Use to assess how a product creates, delivers, and captures value, and where the model is most likely to fail. Produces an argued read of viability, not a filled-in grid. CPO-owned artifact."
argument-hint: "[product or business model to map]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Map and pressure-test a business model

Map the business model for $ARGUMENTS using the [Business Model Canvas](https://www.strategyzer.com/library/the-business-model-canvas) (Osterwalder and Pigneur, *Business Model Generation*, 2010) — nine blocks describing how the product creates, delivers, and captures value. The right-side blocks (customer segments, value propositions, channels, customer relationships, revenue streams) are value delivery and capture; the left-side blocks (key resources, key activities, key partnerships, cost structure) are value creation.

The deliverable is **not a completed grid**. A grid with nine filled cells tells you nothing — anyone can write a plausible sentence in each box. The deliverable is an *argued read of the business model*: do the blocks actually hold together, which dependency is load-bearing, where is the riskiest assumption, and what does the canvas reveal about whether this model is viable. If you finish with nine filled cells and no judgment, you've done the wrong job.

This is a CPO-owned artifact. The product manager supplies slice-level input (a segment's economics, a channel's data); the CPO authors the read. The canvas sits alongside the strategy from `/cpo:write-product-strategy` — strategy says which problems you'll solve and how you'll win; the canvas tests whether solving them is a business. For very early-stage products where the customer and problem are unvalidated, the Lean Canvas variant (Step 7) is the better tool — this skill tells you when to switch.

## Step 1: Establish context, then draft the nine blocks as a first pass

Read the vision, strategy, OKRs, pricing notes, and any financial or customer data in the project (`docs/`, research outputs). Note the maturity: existing model being mapped, or a new model being proposed. Maturity changes everything downstream — mapping a running business is an audit; proposing one is a stack of assumptions.

Draft a one-line first pass for each of the nine blocks. This is throat-clearing, not the work — the value comes from the pressure-tests that follow. Keep each line to a phrase. Tag every line `[known]` (you have evidence) or `[assumed]` (you're guessing). The ratio of assumed-to-known is itself a finding: a model that is nine-tenths assumed is a hypothesis, not a business.

Do not polish the grid. Move to the tests.

## Step 2: Pressure-test the right side — does capture follow from value?

The right side is where the business lives or dies. Test the chain, don't just describe it.

1. **Segments → value propositions.** For each customer segment, does the value proposition solve a problem that segment actually has, and would pay to solve? A value proposition that serves no named segment, or a segment with no compelling value proposition, is a broken link — name it. If one value proposition is stretched across several segments, ask whether it genuinely fits all of them or whether you've blurred distinct segments to make the canvas look tidy.
2. **Value propositions → revenue streams.** This is the load-bearing test of the whole canvas. For each revenue stream, trace it back to the value proposition it monetises. Does the money actually follow from the value, or is the revenue model bolted on? Classic failure: the value proposition serves user A (who won't pay) while revenue comes from buyer B (whose interests differ). If user and payer differ, say so explicitly and state whether their interests align or conflict.
3. **Channels and relationships — cost or moat?** Are the channels how this segment actually buys, or how you wish they bought? Is the customer-relationship model (self-serve, high-touch, community) consistent with the price point? A high-touch relationship on a low revenue-per-customer stream is a margin problem hiding in the canvas.

Output of this step: a short argued paragraph per link, ending with the single weakest link on the right side.

## Step 3: Pressure-test the left side — can you actually deliver this?

The left side is what it takes to make the value proposition real. Test feasibility and dependency.

1. **Value propositions → key activities and resources.** What must the business be able to *do* and *have* to deliver the value proposition? Cross-check: a key activity that serves no value proposition is overhead; a value proposition with no supporting activity or resource is a promise you can't keep.
2. **Key partnerships — leverage or single point of failure?** For each partnership, ask what breaks if the partner walks, raises prices, or becomes a competitor. A partnership the model can't survive losing is a concentration risk, not a convenience — flag it.
3. **The critical-resource question.** Which one resource or activity, if removed, collapses the model? Name it. Every viable model has a centre of gravity; if you can't find it, the model may be undifferentiated commodity work.

Output of this step: the load-bearing resource/activity/partnership, and the left-side dependency most likely to fail.

## Step 4: Test the economics — does the model make money?

Revenue streams (right) against cost structure (left) is the viability test. The canvas is not viable just because both boxes are filled.

- **Unit economics direction.** At the level of one customer or one transaction, does revenue plausibly exceed the cost to serve over the relationship? You don't need precise figures to spot a model that loses money on every sale and hopes to make it up on volume — name that pattern if you see it.
- **Cost structure shape.** Is this value-driven (premium, high cost to serve) or cost-driven (efficiency, scale)? A canvas that mixes a premium value proposition with a cost-driven structure, or vice versa, is internally inconsistent. State which shape the model is and whether the blocks agree.
- **Where's the margin?** Point to the block(s) that produce the margin and the block(s) that consume it. If margin depends entirely on an `[assumed]` block, that assumption is now the business.

## Step 5: Find the riskiest assumption

This is the step the canvas exists for. Across all nine blocks, identify the single assumption that, if wrong, breaks the model — usually one of the `[assumed]` tags from Step 1, weighted by how much the rest of the canvas leans on it.

- State the assumption as a falsifiable claim ("Mid-market ops managers will pay $X/month for this", not "there's demand").
- State what evidence would confirm or kill it.
- State the cheapest test that would produce that evidence. If discovery or experimentation skills exist in the marketplace, point to them; otherwise name the test plainly.

A canvas that doesn't surface its riskiest assumption hasn't been pressure-tested — it's been decorated. This step is mandatory and must name exactly one assumption as the top risk, even if several are close.

## Step 6: Write the argued read

Synthesise the tests into a judgment, not a summary. The read answers: is this a coherent business model, where does it bend, and what would have to be true for it to work? Take a position. "The model is viable if and only if the channel assumption holds" is a read; "all nine blocks are populated" is not.

Be willing to conclude the model doesn't hold. If the right-side chain is broken (value that no one pays for) or the economics invert (cost to serve exceeds revenue), say so — that is the most valuable output this skill can produce, and far more useful than a tidy grid.

## Step 7: Decide whether you mapped the wrong canvas

The Business Model Canvas is a snapshot of an operating model — it assumes you broadly know your customer and value proposition. For an early-stage product where the customer, problem, and solution are all unvalidated, most blocks are guesses and the canvas gives false confidence. There, the [Lean Canvas](https://leanstack.com/lean-canvas) (Ash Maurya, *Running Lean*, 2012) is the better tool: it swaps key partnerships, key activities, customer relationships, and key resources for problem, solution, unfair advantage, and key metrics — forcing the team to state the problem before the solution.

Make the call explicitly:

- If Step 1 produced mostly `[known]` tags → the BMC fits; you've done the right work.
- If Step 1 produced mostly `[assumed]` tags, especially on segments and value propositions → recommend switching to a Lean Canvas and flag that the strategic risk is market risk (should we build this?), not operational risk (can we deliver?).

State which canvas this situation actually called for, and why.

## Rules

- **Always produce a judgment, never just a grid.** Nine filled cells with no argument is a failed output. Every block earns its place by surviving a pressure-test, and the artifact ends with a position on viability.
- **Name exactly one riskiest assumption.** Not a list of risks — the single load-bearing assumption that breaks the model if wrong, stated as a falsifiable claim with the cheapest test to settle it.
- **Trace revenue back to value, every time.** A revenue stream that doesn't follow from a value proposition is the most common hidden flaw. If the user and the payer differ, say so and state whether their interests align.
- **Never blur distinct segments to tidy the canvas.** If one value proposition is stretched across several segments, test whether it truly fits each. A clean-looking canvas built on a blurred segment is worse than a messy honest one.
- **Tag every line known or assumed, and honour the ratio.** A mostly-assumed canvas is a hypothesis. Don't present guesses as facts to make the model look further along than it is.
- **Be willing to conclude the model doesn't work.** A broken right-side chain or inverted economics is the finding. Don't rescue a flawed model with optimistic prose.
- **Switch to the Lean Canvas when the model is mostly unvalidated.** Don't apply an operating-model snapshot to a product whose customer and problem are still guesses.
- **The CPO authors; the PM informs.** Take slice-level economic input, but the read is set here.

## Output Format

Write the result to `docs/business-model-canvas-[product-slug].md`. A blank template lives at `plugins/leadership/cpo/templates/business-model-canvas.md`.

```markdown
# Business model canvas — [product or model]

**Maturity:** [operating model audit / proposed model] · **Author:** CPO · **Date:** [YYYY-MM-DD]

**Verdict:** [one line — is this a coherent, viable model, and the single condition it hinges on]

## The nine blocks (first pass)

| Block | Side | One-line | Evidence |
|---|---|---|---|
| Customer segments | Right | [phrase] | `[known\|assumed]` |
| Value propositions | Right | [phrase] | `[known\|assumed]` |
| Channels | Right | [phrase] | `[known\|assumed]` |
| Customer relationships | Right | [phrase] | `[known\|assumed]` |
| Revenue streams | Right | [phrase] | `[known\|assumed]` |
| Key resources | Left | [phrase] | `[known\|assumed]` |
| Key activities | Left | [phrase] | `[known\|assumed]` |
| Key partnerships | Left | [phrase] | `[known\|assumed]` |
| Cost structure | Left | [phrase] | `[known\|assumed]` |

**Known-to-assumed ratio:** [X known / Y assumed — and what that ratio means]

## Right side — does capture follow from value?

[Argued paragraphs: segments→value, value→revenue (incl. user-vs-payer), channels/relationships vs price point.]

**Weakest link on the right:** [the one]

## Left side — can you deliver it?

[Argued paragraphs: value→activities/resources, partnership concentration risk.]

**Load-bearing resource/activity/partnership:** [the one] · **Most likely to fail:** [the one]

## Economics

[Unit-economics direction, cost-structure shape (value- vs cost-driven), where the margin lives.]

## Riskiest assumption

- **Assumption (falsifiable):** [claim]
- **Evidence that would settle it:** [confirm/kill]
- **Cheapest test:** [test, with a pointer to a discovery/experiment skill if one exists]

## Argued read

[The judgment: coherent or not, where it bends, what must be true for it to work. Take a position.]

## Which canvas this called for

[BMC fits / should have been a Lean Canvas — and why, tied to the known-to-assumed ratio.]
```

## Related skills

- `/cpo:write-product-strategy` — strategy says which problems you'll solve and how you'll win; this canvas tests whether solving them is a business.
- `/cpo:write-product-vision` — the vision's business-goals cell should be consistent with the revenue streams and cost structure here.
- `/cpo:diagnose-strategy` — if the canvas reveals the strategy assumed a business model that doesn't hold, run the strategy critique.
