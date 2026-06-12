# Test: design-experiment weights weak evidence and sizes the test properly

Scenario: The only evidence for a proposed onboarding checklist is a survey of stated intent. The skill must place
that evidence on the hierarchy and recommend a cheaper test before a full A/B, then still produce a rigorous
design: one primary metric, the correct randomisation unit for a team-based product, a real sample-size
calculation from the four supplied inputs, and a no-peeking stopping rule fixed before launch.

## Prompt

/product-analyst:design-experiment We want to add a guided onboarding checklist to Cadence to lift week-1 activation. The only evidence so far is a survey where 68% of churned users said they "would have stayed if setup were easier." Current week-1 activation is 30%, the product-manager says the smallest lift worth shipping is 3 percentage points, and we get about 400 new teams per week. Write the experiment design to {workspace}/work/docs/analytics/experiment-design.md.

## Criteria

- [ ] PASS: Writes a hypothesis that fills all five slots — reason, change, metric, expected direction and size, and segment
- [ ] PASS: Places the prior evidence (a survey) on the evidence hierarchy and identifies it as stated intent (weak) — recommends a cheaper test (fake door / smoke test) before committing engineering to a full A/B
- [ ] PASS: Chooses an experiment type (A/B) and states the randomisation unit as team/account — and notes that randomising by user or session would leak treatment within a team
- [ ] PASS: Names exactly ONE primary metric (week-1 activation) plus guardrail metrics — not multiple primaries
- [ ] PASS: Calculates the required sample size per variant from the four inputs (baseline 30%, MDE 3 percentage points, α 0.05, power 0.80) and converts it to an expected runtime using ~400 teams/week
- [ ] PASS: Sets a stopping rule that forbids early peeking (fixed horizon or an explicit sequential method) and a minimum runtime of at least one full business cycle
- [ ] PASS: States a ship / kill / inconclusive decision rule fixed before launch
- [ ] PARTIAL: Notes that statistical significance is not the same as worth shipping — confirms the effect must clear the MDE that matters, not merely p < 0.05

## Output expectations

- [ ] PASS: The sample-size section shows the four inputs and a concrete per-variant n plus a runtime in days or weeks
- [ ] PASS: The randomisation unit is team/account with the leakage reason stated
- [ ] PASS: Hands off assignment and logging to the data-engineer
- [ ] PARTIAL: The hypothesis is a single sentence with all five slots visibly filled
