---
name: write-product-strategy
description: "Write a product strategy as the plan to reach the product vision. Primary format is Cagan/SVPG-style (specific problems to solve, ruthless focus, quarterly refresh); the Lafley/Martin Playing-to-Win cascade is documented as an alternative for portfolio or market-entry decisions. Use when you have a vision and need the plan to get there. CPO-owned artifact."
argument-hint: "[product or product area to write a strategy for]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Write a product strategy

Write a product strategy for $ARGUMENTS — the plan to get from where the product is today to where the vision says it should be. The strategy is not a roadmap and not a backlog: it is the small set of bets, with focus and rationale, that will move the product toward the vision.

Two formats are supported. The **primary** format is the Cagan/[SVPG](https://www.svpg.com/) style — strategy as the specific problems you choose to solve, with ruthless focus and a quarterly refresh. The **alternative** is the [Playing to Win](https://rogermartin.medium.com/decoding-the-strategy-choice-cascade-475d40555eb1) Strategy Choice Cascade (Lafley and Martin) — five interlocked choices, better suited to portfolio or market-entry decisions. Step 1 picks the format; be opinionated about the fit.

This is CPO-owned. The product manager supplies slice-level input (a segment's problems, a feature area's evidence); the CPO authors the strategy. The vision comes from `/cpo:write-product-vision`; once the strategy exists, run `/cpo:diagnose-strategy` over it before it ships.

## Step 1: Pick the format (and justify it)

Choose Cagan or the cascade. Don't default — decide on the situation.

**Use the Cagan/SVPG format (primary, the default for a single product) when:**

- You have one product and one broadly understood market.
- The strategic question is "which problems do we solve next, and which do we deliberately ignore?"
- You want a living document refreshed quarterly as discovery, technology, and market conditions change.
- The team is empowered and needs strategic context to make autonomous decisions, not a feature factory waiting on approvals.

**Use the Playing-to-Win cascade (alternative) when:**

- The decision spans a portfolio, a new market entry, or a "where do we even compete?" question.
- "Where to play" is genuinely open — multiple segments, channels, or geographies are on the table.
- You need a shared language to stop a team debating tactics before agreeing on the arena.
- The competitive-advantage question ("how do we win here?") is unresolved and contested.

State the chosen format and one sentence of justification. If both seem to fit, default to Cagan for a single product; reach for the cascade only when "where to play" is a live, open question. A cascade applied to a one-market product mostly produces obvious answers.

## Step 2: Read the vision and the evidence

The strategy descends from the vision. Before writing:

1. **Read the product vision** (`docs/product-vision-*.md` or the Vision Board). The strategy's job is to close the gap between today and that vision. No vision on file → write one first with `/cpo:write-product-vision`, or state explicitly that you're working from an implicit vision and capture it.
2. **Gather the evidence** — discovery findings, customer research, usage data, support themes, competitive intelligence, OKR results. Cagan's strategy is driven by insight; the cascade's "how to win" needs competitive evidence. Pull slice-level input from the PM here.
3. **Note the current state** — what's the product today, what's working, what's stuck. Strategy is a path from a real starting point, not a blank slate.

## Step 3a: Write the strategy — Cagan/SVPG format

If you chose Cagan in Step 1, produce these sections:

1. **The few problems we will solve.** Name the specific, important problems — typically two to four — whose solution moves the product toward the vision. Each is a customer or business problem, not a feature or initiative. State why each one matters now (the insight behind the bet).
2. **What we are deliberately not doing.** Strategy is choosing. List the tempting problems you are saying no to this period, and why. A strategy with no explicit "not now" list isn't focused — it's a wish list. This is the hardest and most valuable section.
3. **Focus rationale.** Why these problems, in this order, for this period? Tie each to discovery insight, enabling technology, market condition, or learning. "Picking your battles" — make the picking visible.
4. **Refresh cadence.** State when this strategy is reviewed (no less than quarterly) and what would trigger an earlier refresh (a discovery finding, a market move, a failed bet).

The test for this format: could an empowered team read this and make good autonomous decisions about what to build, without coming back for approval on every call? If not, the strategy isn't providing context — it's a to-do list.

## Step 3b: Write the strategy — Playing-to-Win cascade (alternative)

If you chose the cascade in Step 1, answer all five questions. A cascade missing any answer is hopes, not strategy.

1. **Winning aspiration** — what does winning look like? What is the product/organisation trying to achieve? (This connects to the vision; it's narrower and more competitive.)
2. **Where to play** — which segments, channels, geographies, and use cases? And, by implication, where you will *not* play. This and the next question are the strategic core.
3. **How to win** — what is the competitive advantage in those arenas? Why will the target group choose you over the alternatives, durably?
4. **Must-have capabilities** — what must the organisation be able to do to deliver the how-to-win? Capabilities a competitor can't easily copy.
5. **Enabling management systems** — what processes, metrics, and structures sustain those capabilities?

The reality check (Martin's "18-month test"): if a competitor could replicate your where-to-play and how-to-win within 18 months, it isn't a real strategy. State whether it passes. The cascade is iterative — revisiting "how to win" will often force a change to "where to play". Note any such loops.

## Step 4: Self-check against bad-strategy hallmarks

Before declaring the strategy done, run a quick pass against Rumelt's four hallmarks of bad strategy (the full critique is `/cpo:diagnose-strategy`):

- **Fluff** — any inflated language standing in for content? ("leverage synergies", "world-class platform") Cut it.
- **Failure to face the challenge** — is the core obstacle named plainly? If there's no clear problem, there's nothing to evaluate against.
- **Goals mistaken for strategy** — is "grow to $X" or "be the leader" masquerading as a plan? An aspiration is not a strategy.
- **Disconnected objectives** — are the chosen problems coherent and reinforcing, or a scattered grab-bag?

This is a pre-flight, not the full diagnostic. Always hand the finished strategy to `/cpo:diagnose-strategy` for the proper critique.

## Step 5: Connect to execution

A strategy that doesn't reach execution is shelfware. Close the loop:

- Each problem/bet should be traceable to forthcoming OKRs (`/coordinator:define-okrs`) — the strategy says *what* and *why*; OKRs say *how we'll measure progress*.
- Name the downstream owners: the PM translates chosen problems into PRDs and roadmap; engineering delivers. State the handoff explicitly.
- Set the review date. Cagan's quarterly refresh is a commitment, not a suggestion.

## Rules

- **Always write the "not doing" section.** Strategy is choice. A strategy that says yes to everything has decided nothing. The deliberate no-list is the most valuable part of the document.
- **Never confuse the strategy with a roadmap.** No dated feature lists, no sprint plans. The strategy is the small set of problems and the rationale; the roadmap is the PM's downstream artifact.
- **Never let an aspiration pose as a strategy.** "Become the market leader" / "reach $1B" is a goal. The strategy is *how* — the bets that get you there.
- **Pick one format per artifact and justify it.** Don't blend Cagan and the cascade into a mush. If a single product, default to Cagan; reach for the cascade only when "where to play" is genuinely open.
- **Drive from insight, not opinion.** Every chosen problem cites the discovery finding, data, or market condition behind it. Gut feel at strategy scale is the enemy.
- **The CPO authors; the PM informs.** Take slice-level input, but the strategy is set here. Don't delegate authoring to the product manager.
- **Refresh quarterly at minimum.** A strategy written once and never revisited becomes fiction as the market moves. State the cadence in the document.

## Output Format

Write the result to `docs/product-strategy-[product-slug].md`. A blank template lives at `plugins/leadership/cpo/templates/product-strategy.md`.

```markdown
# Product strategy — [product or area]

**Format:** [Cagan/SVPG | Playing-to-Win cascade] · **Author:** CPO · **Date:** [YYYY-MM-DD] · **Next review:** [date]

**Vision link:** [path to the vision this strategy serves]

**Format justification:** [one sentence on why this format fits the situation]

---

<!-- If Cagan/SVPG format: -->

## The problems we will solve

1. **[Problem 1]** — [why it matters now; the insight behind the bet]
2. **[Problem 2]** — [insight]
3. **[Problem 3]** — [insight]

## What we are deliberately not doing

- [Tempting problem we're saying no to this period] — [why not now]
- [Another]

## Focus rationale

[Why these problems, in this order, this period — tied to discovery, technology, market, or learning.]

## Refresh cadence

[Review date and the triggers for an earlier refresh.]

---

<!-- If Playing-to-Win cascade: -->

## Winning aspiration

[What winning looks like.]

## Where to play

[Segments, channels, geographies, use cases — and where we won't play.]

## How to win

[The durable competitive advantage in those arenas.]

## Must-have capabilities

[Capabilities required to deliver the how-to-win.]

## Enabling management systems

[Processes, metrics, structures that sustain the capabilities.]

## 18-month test

[Could a competitor replicate WTP + HTW within 18 months? Pass/fail and why.]

---

## Bad-strategy self-check

- [ ] No fluff
- [ ] Core challenge faced plainly
- [ ] No aspiration posing as strategy
- [ ] Objectives coherent, not scattered

## Execution handoff

- **OKRs:** [link or "to be defined via /coordinator:define-okrs"]
- **Downstream owners:** [PM → PRD/roadmap; engineering → delivery]
```

## Related skills

- `/cpo:write-product-vision` — write the vision first; the strategy is the plan to reach it.
- `/cpo:diagnose-strategy` — run Rumelt's good-vs-bad diagnostic over this strategy before it ships. Mandatory follow-up.
- `/coordinator:define-okrs` — turn the chosen problems/bets into measurable OKRs.
