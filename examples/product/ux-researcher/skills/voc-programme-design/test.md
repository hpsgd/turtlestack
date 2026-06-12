# Test: Design a voice-of-customer programme

Scenario: A SaaS product team wants to stand up a continuous voice-of-customer programme. They currently have no structured customer feedback — just ad-hoc support tickets. The skill must produce a programme blueprint that picks the right metric per question (NPS / CSAT / CES), designs the surveys, ties quantitative signal to qualitative themes, designs both feedback loops, sets governance, and treats this as one VoC lens among several (not the central feedback owner).

## Prompt

We're a mid-market B2B SaaS product (project-management tooling). We have no structured customer-feedback programme today — just whatever lands in support tickets. I want to stand up an ongoing voice-of-customer programme. The decisions we most want it to feed: (1) which onboarding step to fix next — new accounts seem to drop off during setup; (2) early detection of accounts at risk of churning; (3) whether a release landed well or needs iterating.

/ux-researcher:voc-programme-design mid-market B2B SaaS project-management product

Design the full programme blueprint using the skill's process and Output Format. Write it to `{workspace}/work/voc-programme.md` and reply with the path.

## Criteria

- [ ] PASS: Every programme objective names a decision it informs AND an owner who acts — no metric collected for its own sake
- [ ] PASS: Selects the right metric per question — CES for the effortful onboarding/setup friction, NPS for relationship/churn-risk trajectory, CSAT or NPS for release perception — not one metric used as a universal thermometer
- [ ] PASS: Justifies CES over CSAT for the onboarding-friction objective (effort predicts disloyalty better than delight for service interactions)
- [ ] PASS: Designs surveys with verbatim question wording AND a paired open-text "why" — a score with no reason is treated as a dead end
- [ ] PASS: Specifies sampling, cadence, and a fatigue cap (no respondent over-surveyed) plus a response-rate floor below which results are flagged insufficient, not reported as fact
- [ ] PASS: Defines a quant-to-qual synthesis method — verbatim coding into a stable code frame, driver analysis tying themes to score movement, and a segment cut
- [ ] PASS: Designs BOTH an inner loop (individual detractor → individual recovery action with owner + SLA) and an outer loop (saturated theme → product/process change) — not just one
- [ ] PASS: Sets governance with anti-gaming guards — no soliciting high scores, report trend not absolute value, raw verbatims visible to those who act
- [ ] PASS: Treats this as the structured-research VoC lens among several — does NOT centralise feedback ownership; cross-consults support, customer-success, and GTM rather than absorbing their feedback streams
- [ ] PARTIAL: Distinguishes this ongoing-programme work from a one-off survey or a persona artifact (does not drift into building a persona)

## Output expectations

- [ ] PASS: Output is written to the given path and follows the skill's Output Format (Objectives, Metric Selection, Survey Design, Quant-to-Qual Synthesis, Closing the Loop, Governance, Cross-Consultation sections)
- [ ] PASS: Output's metric-selection table maps each of the three stated objectives to a specific metric with a trigger point and a rationale — onboarding→CES, churn-risk→NPS (relationship), release→CSAT/NPS
- [ ] PASS: Output includes a Cross-Consultation section naming the other VoC lenses (support, customer-success, GTM) and where their reads may conflict with this programme's — surfacing conflict rather than reconciling it away
