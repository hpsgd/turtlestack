# Test: strategic-voc-synthesis triangulates lenses and surfaces conflict, not consensus

Scenario: A PM pressure-tests a discovery hypothesis against Voice-of-Customer signal from several sources
that disagree. The skill must state the hypothesis as falsifiable, pull each source and tag its lens, weight
behavioural over stated signal and label single-source claims, surface the cross-lens conflict explicitly
(rather than averaging it away), and render a Confirmed / Qualified / Contradicted verdict with a confidence
rating. VoC sources are staged as fixtures.

## Prompt

Use the product-manager `strategic-voc-synthesis` skill to validate this discovery hypothesis against VoC
signal: "Mid-market accounts churn primarily because week-one onboarding is too hard." The VoC sources are
staged at `{workspace}/work/docs/product/voc/` — read all of them (support tickets, churn notes, win/loss,
reviews, survey). Write the synthesis to a file under `docs/product/` in the current working directory, in
the skill's standard format.

Proceed without asking — produce the VoC synthesis.

## Criteria

- [ ] PASS: Restates the hypothesis as a single falsifiable claim before validating it
- [ ] PASS: Pulls each VoC source and tags which lens/owner it comes from (support / customer-success / GTM / reviews / survey)
- [ ] PASS: Weights behavioural signal (what accounts actually did) above stated signal (survey answers), and labels single-source claims as such
- [ ] PASS: SURFACES the cross-lens conflict explicitly — the interviews/onboarding signal vs the sales/price signal — rather than averaging it away or picking the convenient lens
- [ ] PASS: Names which lens it trusts more for THIS hypothesis and why (does not just report that they disagree)
- [ ] PASS: Renders one verdict — Confirmed / Qualified / Contradicted — with a confidence rating (0-4)
- [ ] PASS: If the signal is segment-specific, returns a Qualified verdict stating the segment boundary rather than a forced Confirmed
- [ ] PARTIAL: Recommends consulting other lens-holders (GTM, customer-success, ux-researcher) where the hypothesis touches pricing/churn/positioning

## Output expectations

- [ ] PASS: Output file exists under `docs/product/` with a signal-by-source table tagging each source's lens and tier, and a cross-lens-conflict section
- [ ] PASS: The onboarding-vs-price conflict between the interview/support lens and the sales/win-loss lens is stated plainly, not reconciled into a bland average
- [ ] PASS: The verdict is one of Confirmed / Qualified / Contradicted with a confidence score, and a single-source claim (if any) is labelled
- [ ] PASS: Behavioural signal is weighted above stated survey intent in reaching the verdict
- [ ] PASS: The output names which lens is closer for this hypothesis and gives a reason
- [ ] PARTIAL: Output points to further lens-holders to consult, treating this as the PM's lens rather than the only view
