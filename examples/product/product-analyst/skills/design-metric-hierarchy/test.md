# Test: design-metric-hierarchy picks the right framework and ties to OKRs

Scenario: An engagement-led SaaS already has a North Star on disk. The skill must confirm that North Star, classify
the product type, choose HEART over AARRR (one framework, not both) with justification, map inputs to dimensions,
tie branches to product-manager OKRs while flagging orphans both ways, and assign an owner and cadence to every
metric — without redefining OKRs or building a four-level tree.

## Prompt

/product-analyst:design-metric-hierarchy Cadence — a team productivity SaaS whose value is a team running a daily async standup habit. The existing North Star is in the file {workspace}/work/docs/analytics/north-star.md — read it first. Write the metric tree to {workspace}/work/docs/analytics/metric-tree.md.

## Criteria

- [ ] PASS: Reads and confirms the existing North Star from the provided file rather than inventing a new one
- [ ] PASS: Classifies Cadence as engagement / retention-led (value comes from repeated habitual use), with a one-line justification
- [ ] PASS: Chooses HEART and justifies it over AARRR for an engagement product — picks ONE framework, does not bolt both onto the product
- [ ] PASS: Maps the North Star to framework dimensions, placing input metrics under the appropriate HEART dimensions (e.g. Engagement, Adoption, Retention)
- [ ] PASS: Ties branches to OKRs owned by the product-manager and flags orphans in both directions (metric-without-OKR and OKR-without-metric) — does NOT rewrite or invent OKRs
- [ ] PASS: Assigns an owning team and a review cadence to each input metric (weekly for inputs, monthly/quarterly for the North Star)
- [ ] PASS: Produces a two-to-three-level tree (North Star → dimension → metric) where every leaf is an input a team can move — not a four-level spreadsheet
- [ ] PARTIAL: Names any empty HEART dimension explicitly as irrelevant or a blind spot rather than leaving it silently blank

## Output expectations

- [ ] PASS: Output is a structured tree with the chosen framework named and a one-sentence justification of HEART over AARRR
- [ ] PASS: Each leaf metric shows an owner and a cadence
- [ ] PASS: Includes an OKR-mapping table with orphan flags
- [ ] PARTIAL: Includes a coverage-gaps section listing any dimension with no metric
