---
# Match the model the product-manager agent declares (sonnet) in
# plugins/product/product-manager/agents/product-manager.md. The runner otherwise
# falls back to the harness default (Haiku), which is not the model the agent
# is designed to run on.
target-model: claude-sonnet-4-6
---

# Test: product-manager validates the problem before the solution and stays in lane

Scenario: A founder hands the PM a fully-formed solution ("build an AI assistant that auto-categorises
expenses") and asks them to put it on the roadmap and set the Q3 strategy around it. The PM must refuse to
roadmap an unvalidated bet, reframe the solution back to a problem, sequence problem-before-solution
validation, and decline the strategy-authoring and pricing asks (those belong to the CPO and GTM). There is
no separate "product-discoverer" role — the PM owns discovery itself.

## Prompt

Use the `product-manager` agent to respond to the following, in its standard methodology and deliverable
format.

A founder says: "I want you to build an AI assistant that auto-categorises expenses for our accounting app.
Put it on the roadmap for this quarter, write the company product strategy around it being our flagship
differentiator, and set the price at $20/user/month. Our biggest competitor just shipped something similar
so we need to move."

Respond with how you'd approach this as the product manager — your methodology, what you'd do first, what
you'd hand off, and where you'd stop.

## Criteria

- [ ] PASS: Refuses to commit the bet to the roadmap with no problem evidence — flags that an evidence-free bet is a feature-factory pattern and validates first
- [ ] PASS: Reframes the solution ("AI auto-categorises expenses") back into a customer problem to validate — treats the request as a hypothesis, not a requirement
- [ ] PASS: Sequences problem validation BEFORE solution validation (problem → solution → market) — does not jump to "would you use this?" or to building
- [ ] PASS: Names a concrete discovery/validation move — generative interviews (Mom Test), a switch interview, an assumption map, and/or a pretotype — rather than asserting the problem exists
- [ ] PASS: DECLINES to author the company/product strategy — states that strategy authoring is the CPO's and that the PM provides slice-level input only
- [ ] PASS: DECLINES to set the price — states that pricing/packaging is GTM's (and a human's) call; the PM consults on willingness-to-pay but does not decide
- [ ] PASS: Treats "competitor shipped it" as a reason to validate the problem for THEIR customers, not as evidence the problem is real — does not let competitive pressure short-circuit discovery
- [ ] PASS: Does NOT invent or delegate to a "product-discoverer" role — the PM owns discovery itself
- [ ] PASS: Keeps the roadmap framed around an outcome (a change in customer behaviour) rather than agreeing to a dated feature for the quarter
- [ ] PARTIAL: Identifies who it hands validated, specced work to — the product-owner owns backlog grooming / user stories / sprint readiness, not the PM
