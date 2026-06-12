# Test: write-opportunity-solution-tree roots on outcome, sources opportunities from research

Scenario: A PM maps a problem space after several interviews. The skill must build a Torres OST: one desired
outcome at the root, opportunities sourced from actual interviews (each citing its interview, not
brainstormed), multiple solutions for ONE target opportunity, and the riskiest assumption with an experiment
attached — plus an update rhythm. Interview notes are staged as a fixture.

## Prompt

Use the product-manager `write-opportunity-solution-tree` skill to build an opportunity solution tree for the
"activation" slice. The desired outcome is to lift week-one activation from 30% to 55%. Interview synthesis
notes are at `{workspace}/work/docs/product/discovery-log.md` — read them first and source the opportunities
from those interviews. Write the tree to a file under `docs/product/` in the current working directory, in
the skill's standard format.

Proceed without asking — produce the opportunity solution tree.

## Criteria

- [ ] PASS: Sets one measurable desired outcome at the root (week-one activation 30% → 55%) — one root per tree
- [ ] PASS: Maps opportunities (customer needs/pains) that, if addressed, would move the root metric
- [ ] PASS: Sources opportunities from the supplied interviews and cites the interview each came from — NOT brainstormed problems
- [ ] PASS: Opportunities are specific enough to act on ("freelancers on mobile can't connect a bank feed in week one") — not "users are frustrated"
- [ ] PASS: Picks ONE target opportunity and brainstorms multiple (≥3) distinct solutions under it — does not generate solutions across the whole space at once
- [ ] PASS: Attaches the riskiest assumption and an experiment to the leading solution (the experiment is a leaf under the solution)
- [ ] PASS: Every solution traces to an opportunity and every opportunity traces to the outcome — no floating nodes
- [ ] PARTIAL: Records an update rhythm / next-review date (the tree is a living artifact, monthly minimum)

## Output expectations

- [ ] PASS: Output tree file exists under `docs/product/` with the desired outcome as the single root and a nested opportunity → solution → assumption/experiment structure
- [ ] PASS: Each opportunity node cites the interview it came from (drawn from the fixture), demonstrating research-sourced rather than brainstormed opportunities
- [ ] PASS: Exactly one target opportunity carries multiple candidate solutions; the rest are not pre-loaded with solutions
- [ ] PASS: The leading solution has its riskiest assumption named with an attached experiment/test
- [ ] PASS: No floating nodes — every solution hangs off an opportunity, every opportunity off the outcome
- [ ] PARTIAL: A next-review date or update cadence is recorded
