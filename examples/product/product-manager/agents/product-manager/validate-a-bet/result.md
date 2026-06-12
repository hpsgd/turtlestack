# Validate A Bet

Scenario: A founder hands the PM a fully-formed solution ("build an AI assistant that auto-categorises expenses") and asks them to put it on the roadmap and set the Q3 strategy around it. The PM must refuse to roadmap an unvalidated bet, reframe the solution back to a problem, sequence problem-before-solution validation, and decline the strategy-authoring and pricing asks (those belong to the CPO and GTM). There is no separate "product-discoverer" role — the PM owns discovery itself.

## Prompt

> Use the `product-manager` agent to respond to the following, in its standard methodology and deliverable
> format.
> 
> A founder says: "I want you to build an AI assistant that auto-categorises expenses for our accounting app.
> Put it on the roadmap for this quarter, write the company product strategy around it being our flagship
> differentiator, and set the price at $20/user/month. Our biggest competitor just shipped something similar
> so we need to move."
> 
> Respond with how you'd approach this as the product manager — your methodology, what you'd do first, what
> you'd hand off, and where you'd stop.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Here is the PM's response:

---

## PM Response: AI Expense Categorisation Request

**Status:** Pre-discovery — not validated. This is a founder hypothesis, not a confirmed customer problem. Confidence: 0/4.

---

### What I'd do first

Before any roadmap entry, strategy doc, or pricing decision, I need evidence for four questions:

1. **Who specifically** has this problem? Named person, named circumstance.
2. **How do I know?** Support ticket volume, churn interviews, session recordings, sales call notes — not intuition.
3. **How are they solving it today?** Manual rules, a bookkeeper, a competitor? What does their current workaround cost them?
4. **What happens if we don't solve it?** Churn? Lost deals? Or a mild irritant they tolerate?

**This week's discovery work:**
- Pull 90 days of support tickets, tag anything touching categorisation or reconciliation
- Pull churn exit interviews and lost deal notes — did this come up?
- Book 5 customer interviews (power users + recently churned + anyone who mentioned categorisation) in 10 business days, Mom Test format: *"walk me through the last time you had to categorise a batch of expenses"* — not "would you use this feature?"

The output is an **Opportunity Solution Tree** and a **problem validation memo** — not a roadmap item.

---

### What I'm pushing back on, and why

**"Put it on the roadmap this quarter"** — No commitment until problem validation is done. I will commit to a two-week discovery sprint that either confirms the bet or kills it cheaply. If discovery confirms the problem, I'll return with a roadmap proposal and an honest engineering estimate.

**"Write the company strategy around it as our flagship differentiator"** — That's a CPO/founder call, not mine to author. More importantly: if your competitor just shipped it, *AI expense categorisation is already table stakes*, not differentiation. Discovery will surface whether there's a wedge — a segment, integration, or workflow — where you can own a distinct job they haven't nailed. A strategy document written today papers over that question.

**"Set the price at $20/user/month"** — Pricing is a GTM decision. My contribution is a JTBD framing of the value delivered and the cost of the current workaround, so GTM has something concrete to anchor willingness-to-pay research on. I do not decide the number, and neither should you without demand-side data.

---

### What I'll commit to vs. won't

| Will commit to | Won't commit to |
|---|---|
| Two-week discovery sprint | Roadmap slot before validation |
| Opportunity Solution Tree + assumption map | Authoring company/product strategy |
| PRD (if problem confirmed) | Pricing — that goes to GTM |
| JTBD canvas + evidence pack for GTM and CPO | Delivery timeline — engineering estimates against a scoped problem, not before |
| Validated spec handed to product owner | User stories — that's the PO's job |

---

### Handoffs

| What | To whom | When |
|---|---|---|
| JTBD canvas + willingness-to-pay framing | GTM | After problem validation |
| Slice-level evidence pack | You / CPO (strategy input) | After validation confirms differentiation vs. catch-up |
| Validated PRD | CTO/architect (effort estimate) | After spec is written |
| Specced, validated problem | Product owner (backlog, stories) | After PRD is complete |
| Persona depth + usability | UX researcher | Once solution direction is confirmed |

---

### The honest read on competitive pressure

The specific risk here is building a catch-up feature at speed and calling it a differentiator. Your competitor's customers are still figuring out whether it actually solves their problem. You have a narrow window — probably 6–8 weeks — to understand the job they tried to do and find the angle they missed, rather than shipping an identical feature two months later.

**Discovery is the competitive move, not the delay.**

If validation confirms the problem, you'll have a specced, prioritised bet, a strategy input memo identifying where the genuine differentiation opportunity sits, and a GTM-ready canvas for pricing research. That is a better starting position than a roadmap slot you haven't earned yet.

---

**First question back to the founder:** Do you have existing interview notes, VoC data, or support ticket access I should read before running new interviews — or do we start fresh with the data pull?

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 9.5/9.5 (100%) |
| Evaluated | 2026-06-13 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 88700 ms |
| Target cost | $0.2307 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | PASS: Refuses to commit the bet to the roadmap with no problem evidence — flags that an evidence-free bet is a feature-factory pattern and validates first | PASS | "No commitment until problem validation is done. I will commit to a two-week discovery sprint that either confirms the bet or kills it cheaply." |
| c2 | PASS: Reframes the solution ("AI auto-categorises expenses") back into a customer problem to validate — treats the request as a hypothesis, not a requirement | PASS | "Status: Pre-discovery — not validated. This is a founder hypothesis, not a confirmed customer problem." Four named questions about who has the problem and how we know. |
| c3 | PASS: Sequences problem validation BEFORE solution validation (problem → solution → market) — does not jump to "would you use this?" or to building | PASS | Interview format specified as Mom Test: "walk me through the last time you had to categorise a batch of expenses" — explicitly not "would you use this feature?" |
| c4 | PASS: Names a concrete discovery/validation move — generative interviews (Mom Test), a switch interview, an assumption map, and/or a pretotype — rather than asserting the problem exists | PASS | "Book 5 customer interviews... Mom Test format"; "Pull 90 days of support tickets"; "Opportunity Solution Tree and a problem validation memo" named as outputs. |
| c5 | PASS: DECLINES to author the company/product strategy — states that strategy authoring is the CPO's and that the PM provides slice-level input only | PASS | "That's a CPO/founder call, not mine to author." Handoffs table shows "Slice-level evidence pack" goes to "You / CPO (strategy input)" after validation. |
| c6 | PASS: DECLINES to set the price — states that pricing/packaging is GTM's (and a human's) call; the PM consults on willingness-to-pay but does not decide | PASS | "Pricing is a GTM decision... I do not decide the number, and neither should you without demand-side data." JTBD framing handed to GTM. |
| c7 | PASS: Treats "competitor shipped it" as a reason to validate the problem for THEIR customers, not as evidence the problem is real — does not let competitive pressure short-circuit discovery | PASS | "Your competitor's customers are still figuring out whether it actually solves their problem... Discovery is the competitive move, not the delay." |
| c8 | PASS: Does NOT invent or delegate to a "product-discoverer" role — the PM owns discovery itself | PASS | All discovery work (support ticket pull, churn interviews, customer interviews, OST, validation memo) is described in first person with no delegation to a separate discoverer role. |
| c9 | PASS: Keeps the roadmap framed around an outcome (a change in customer behaviour) rather than agreeing to a dated feature for the quarter | PASS | Commits only to "a two-week discovery sprint" and a "roadmap proposal" contingent on validation — no Q3 feature slot, framed around confirming "the bet" not shipping a feature. |
| c10 | PARTIAL: Identifies who it hands validated, specced work to — the product-owner owns backlog grooming / user stories / sprint readiness, not the PM | PARTIAL | Handoffs table: "Specced, validated problem" → "Product owner (backlog, stories)" and won't-commit list: "User stories — that's the PO's job." |

### Notes

The output is a clean, comprehensive pass across all criteria with no gaps. Every decline is explicit and attributed, discovery sequencing is correct, and the PM/PO boundary is clearly drawn in both the won't-commit table and the handoffs section.
