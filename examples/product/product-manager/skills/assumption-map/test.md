# Test: assumption-map plots knowledge × impact and tests the riskiest first

Scenario: A PM must de-risk a bet before committing engineering effort. The skill must surface falsifiable
assumptions across all four risk areas (not just feasibility), score each on knowledge × impact, place them
in the four quadrants, identify the high-impact/low-knowledge "test first" quadrant, and recommend a
behaviour-measuring experiment for each target assumption — knowledge meaning evidence, not confidence.

## Prompt

Use the product-manager `assumption-map` skill to map the assumptions behind this bet: "We'll add a guided
onboarding checklist to lift week-one activation, because ops managers who don't finish setup churn." Write
the assumption map to a file under `docs/product/` in the current working directory, in the skill's standard
format.

Proceed without asking — produce the assumption map.

## Criteria

- [ ] PASS: Surfaces assumptions across all four risk areas — desirability, viability, feasibility, usability — not just the comfortable feasibility ones
- [ ] PASS: Writes each assumption as a falsifiable statement ("30% of trial users complete setup unaided") — not "the product is good"
- [ ] PASS: Scores each assumption on two axes: knowledge (evidence we have → none) and impact (bet survives → bet dies)
- [ ] PASS: Treats knowledge as evidence, NOT confidence — "we're pretty sure" places an assumption in LOW knowledge, not high
- [ ] PASS: Places assumptions in the four quadrants and identifies the high-impact / low-knowledge quadrant as TEST FIRST
- [ ] PASS: Recommends an experiment for each target-quadrant assumption that measures behaviour over stated intent (pretotype / Wizard of Oz / smoke test)
- [ ] PASS: Defers or ignores high-knowledge / low-impact assumptions rather than spending experiments on established facts
- [ ] PARTIAL: Notes the team-defaults-to-feasibility trap — the bet usually dies on desirability or viability

## Output expectations

- [ ] PASS: Output file exists under `docs/product/` with an assumptions table tagged by risk area and a two-axis (knowledge × impact) placement
- [ ] PASS: The high-impact / low-knowledge assumptions are explicitly flagged as the ones to TEST FIRST
- [ ] PASS: Each test-first assumption has a recommended experiment, and the recommended evidence type is behaviour rather than opinion/intent
- [ ] PASS: At least one assumption is correctly deferred/ignored as high-knowledge or low-impact — not everything is "test it"
- [ ] PASS: Assumptions are falsifiable statements, and knowledge is scored on evidence rather than confidence
- [ ] PARTIAL: All four risk areas appear, demonstrating the map didn't collapse to feasibility-only
