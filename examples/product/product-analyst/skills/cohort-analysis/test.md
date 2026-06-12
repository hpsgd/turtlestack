# Test: cohort-analysis reads curve shape and finds the hidden dying segment

Scenario: A retention table is provided where the blended curve flattens (looks like product-market fit) but one
channel decays to near zero while another flattens high. The retention event in the data is the weak "opened the
app," and no bot/internal exclusions have been applied. The skill must read the curve SHAPE as the verdict,
benchmark it for a weekly SaaS, cut by channel to expose the divergence, flag the value-action problem, flag a
correlation as not-causation, and require the missing exclusions.

## Prompt

/product-analyst:cohort-analysis Cadence retention. A cohort retention table for the last six monthly signup cohorts, plus a breakout by acquisition channel, is in the file {workspace}/work/docs/analytics/retention-data.md — read it. Diagnose whether Cadence has product-market fit and where retention is strong versus bleeding. Write the analysis to {workspace}/work/docs/analytics/cohort-analysis.md.

## Criteria

- [ ] PASS: Flags that the retention event should be the value action (a standup posted), and that the provided "opened the app" definition overstates retention — returning without getting value is not retention
- [ ] PASS: States which retention definition (N-day / unbounded / bracket) fits Cadence's natural usage frequency, with a one-line reason
- [ ] PASS: Reads the curve SHAPE as the verdict (flattens above zero = fit vs decays to zero = no fit) rather than reporting a single average retention number
- [ ] PASS: Benchmarks the plateau against what is healthy for the product type (weekly SaaS) rather than an absolute target pulled from nowhere
- [ ] PASS: Cuts the cohorts by channel and names the strongest and weakest segments — surfacing the divergence the blended aggregate hides (referral flattens high; paid social decays to ~2%)
- [ ] PASS: Flags the "calendar integration in week 1 → 2x retention" finding as correlation, NOT causation, and routes it to an experiment to test
- [ ] PASS: Calls out that bots, test, and internal accounts have not been excluded and states they must be, since internal users retain near 100% and poison cohorts
- [ ] PARTIAL: Leads the write-up with the curve-shape verdict (the answer) before presenting the table

## Output expectations

- [ ] PASS: Output opens with a verdict line stating product-market fit / no fit / improving, tied to the curve shape — not to a single number
- [ ] PASS: Output includes a retention table or curve plus at least one segment cut
- [ ] PASS: Output names the strongest and weakest channel segments with their retention figures
- [ ] PARTIAL: Output includes a "next" section listing the correlations to test via experiment
