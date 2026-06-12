# Test: write-prd validates the problem, scores RICE, and defines failure

Scenario: A PM is handed rough notes for a validated problem and must produce a PRD. The skill must establish
the problem (not the solution) with evidence, score RICE with the calculation shown, define leading/lagging/
guardrail metrics plus an explicit failure condition, write ISC-testable acceptance criteria, and assess the
four Cagan risks — handing the story breakdown to the product-owner rather than doing it.

## Prompt

Use the product-manager `write-prd` skill to write a PRD from these notes, in the skill's standard format,
written to a file under `docs/product/` in the current working directory:

"Mid-market SaaS ops managers (50-200 integrations) waste hours every Monday manually reconciling failed
webhook deliveries across our dashboard — they export CSVs and diff them by hand. We have 30+ support
tickets this quarter and three churned accounts cited it. We want a bulk-retry-and-reconcile view. About 400
accounts hit this. Rough build estimate: 6 person-weeks across design + eng + QA."

Proceed without asking — produce the PRD.

## Criteria

- [ ] PASS: States the problem in one sentence WITHOUT referencing the solution — the problem is the manual reconciliation pain, not "build a bulk-retry view"
- [ ] PASS: Cites the concrete evidence (30+ tickets, three churned accounts) as problem validation rather than asserting "users want it"
- [ ] PASS: Defines the target user precisely (mid-market ops managers, 50-200 integrations, weekly frequency) — specific enough to recruit for a test
- [ ] PASS: Calculates a RICE score showing the formula (Reach × Impact × Confidence) / Effort with the numbers — does not just assert "high priority"
- [ ] PASS: Defines at least one leading, one lagging, AND one guardrail metric — and an explicit failure condition (e.g. "<10% adoption after 4 weeks")
- [ ] PASS: Writes acceptance criteria that are Independent / Small / Complete (ISC) — including a boundary/edge case, not just the happy path
- [ ] PASS: Assesses all four Cagan risks (value, usability, feasibility, viability) in a pre-mortem
- [ ] PARTIAL: Defines scope with in-scope, out-of-scope (with reasons), and anti-requirements — and hands story breakdown to the product-owner rather than grooming the backlog itself

## Output expectations

- [ ] PASS: Output PRD file exists under `docs/product/` with a header carrying the RICE score, and the problem stated independently of the solution
- [ ] PASS: The RICE section shows the actual arithmetic (Reach, Impact, Confidence, Effort values and the resulting score), not a bare "high"
- [ ] PASS: Success metrics include leading + lagging + guardrail, and the PRD names a specific, falsifiable failure condition that supports a kill decision
- [ ] PASS: At least one acceptance criterion specifies a boundary/error condition (empty state, error, concurrency), demonstrating the "Complete" part of ISC
- [ ] PASS: The four risk categories (value, usability, feasibility, viability) are each assessed, not just listed
- [ ] PASS: Output marks genuine unknowns with `[NEEDS CLARIFICATION: ...]` rather than silently inventing missing facts
- [ ] PARTIAL: Output states that the product-owner breaks the stories down into the sprint-ready backlog — the PRD specifies behaviour, not backlog grooming
