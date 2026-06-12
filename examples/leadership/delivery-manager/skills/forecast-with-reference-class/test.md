# Test: forecast-with-reference-class uses an outside-view reference class, not a padded estimate

Scenario: A team has produced an optimistic bottoms-up estimate under stakeholder pressure. The delivery manager
must build an outside-view reference class from comparable past deliveries, derive the median correction factor,
apply it, and recommend committing to the reference-class forecast rather than the pressured number — presenting
both figures and the gap between them.

## Prompt

Use the delivery-manager `forecast-with-reference-class` skill to forecast the "payments rebuild". Write the
forecast to `docs/delivery/forecast-payments-rebuild.md` relative to the current working directory. Respond in the
skill's standard output format.

Facts:

- The team's bottoms-up estimate, given under pressure from the CPO to "hit 8 weeks", is 8 weeks.
- Three comparable past rebuilds in this org, with their original estimates and actuals:
  - Billing migration: estimated 8 weeks, actually took 13 weeks.
  - Search rebuild: estimated 6 weeks, actually took 9 weeks.
  - Notifications service: estimated 10 weeks, actually took 14 weeks.

Proceed without asking — build the reference class and produce the forecast.

## Criteria

- [ ] PASS: Builds an outside-view reference class from the three comparable past deliveries — pulling each one's original estimate and actual outcome, not reasoning only from the current team's inside-view estimate
- [ ] PASS: Computes the actual/estimate ratio for each past delivery (≈1.63, 1.50, 1.40) and derives a correction factor — preferring the MEDIAN (≈1.50) for the small class rather than padding the estimate by an arbitrary buffer
- [ ] PASS: Applies the correction factor to the 8-week bottoms-up estimate to produce a reference-class forecast of roughly 12 weeks — derived from history, not from inflating the team number by a gut feel
- [ ] PASS: Presents BOTH numbers — the 8-week bottoms-up estimate and the ~12-week reference-class forecast — and names the gap between them as the planning-fallacy correction
- [ ] PASS: Recommends committing to the reference-class forecast (~12 weeks), not the pressured 8-week number, with the reasoning visible — naming that committing to the optimistic figure embeds the planning fallacy
- [ ] PASS: Names the method as reference-class forecasting / the planning-fallacy correction (Kahneman/Lovallo via Flyvbjerg) rather than presenting it as a generic "add contingency"
- [ ] PARTIAL: Notes that a reference class needs comparable deliveries (three to five is usable; one is an anecdote) and does not fabricate data to fill it

## Output expectations

- [ ] PASS: A `docs/delivery/forecast-payments-rebuild.md` file is written with a reference-class table (past delivery / estimate / actual / ratio), a derived correction factor, and a recommendation
- [ ] PASS: The reference-class table shows all three past deliveries with their estimate, actual, and computed ratio
- [ ] PASS: The median ratio (≈1.50) is stated and used, with a note that median is preferred over mean for the small class
- [ ] PASS: Both the 8-week bottoms-up estimate and the ~12-week reference-class forecast appear, and the recommendation is to commit to ~12 weeks
- [ ] PASS: The recommendation explains the gap as the planning-fallacy correction and flags the optimism risk of using the 8-week estimate instead
- [ ] PARTIAL: The forecast is grounded in the outside-view history rather than an arbitrary buffer added to the team's number
