# Test: coach-flow-metrics teaches the four measures and Little's Law

Scenario: A team is drowning in work-in-progress and delivery is unpredictable. The coach must teach the team to read its own flow data — the four measures, the cycle-time scatterplot, the cumulative flow diagram — and justify WIP limits with Little's Law rather than preference, while staying on its side of the delivery-manager boundary.

## Prompt

Use the agile-coach `coach-flow-metrics` skill to coach the "billing" team on its flow. Context: the team typically has about 20 items in progress at once and completes roughly 4 per week, delivery dates are unpredictable, and several items have been "in progress" for weeks. Teach the team to read its own flow data and produce the flow read and coaching plan in the skill's standard format. Write the output to `docs/coaching/` in the current working directory.

Proceed without asking — produce the flow coaching output.

## Criteria

- [ ] PASS: Establishes the four measures by name — cycle time, lead time, throughput, work-item age — with what each one answers
- [ ] PASS: Correctly distinguishes cycle time (start-to-done, active time) from lead time (requested-to-done, includes queue time) rather than conflating them
- [ ] PASS: Explains the cycle-time scatterplot as the primary diagnostic, including percentile lines and that an item above the 85th percentile is aging and needs attention now
- [ ] PASS: Explains how to read the cumulative flow diagram — widening band = WIP accumulating / bottleneck, flat top line = nothing completing
- [ ] PASS: Applies Little's Law correctly to the supplied numbers — 20 WIP ÷ 4 per week ≈ 5-week cycle time — and shows that halving WIP to 10 halves cycle time without adding people
- [ ] PASS: Justifies WIP limits with Little's Law as physics, not preference, and notes the law's conditions (stable flow, no wild item-size variation)
- [ ] PASS: Hands the instruments to the team — sets the team up to read its own scatterplot/CFD rather than the coach becoming the flow-report service
- [ ] PARTIAL: Holds the boundary — the coach coaches the flow practice; the delivery manager only reads the numbers for status

## Output expectations

- [ ] PASS: Output is a structured flow-coaching artifact with a current flow read, a CFD read, a Little's Law application, and a coaching plan
- [ ] PASS: The Little's Law section shows the concrete calculation (≈5-week current cycle time from 20 WIP / 4 throughput, halving to ≈2.5 weeks at WIP 10), not just the formula
- [ ] PASS: Output distinguishes cycle time from lead time explicitly and ties the difference to queue time
- [ ] PASS: Output flags the long-running in-progress items as aging items needing attention now (above the typical percentile), not just "some items are slow"
- [ ] PASS: Output's coaching plan sets up the team to read its own data on its own cadence rather than positioning the coach as the report producer
- [ ] PARTIAL: Output notes a condition or caveat on Little's Law (e.g. wildly varying item sizes break the averages) rather than presenting it as unconditional
