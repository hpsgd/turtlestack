# Test: write-roadmap is outcome-shaped Now/Next/Later, not a feature timeline

Scenario: A stakeholder hands the PM a dated feature list ("bulk import in Q2, SSO in Q3, mobile app in Q4")
and asks for a roadmap. The skill must refuse the date-feature shape, anchor on desired outcomes with
baseline → target, place items by how much is known (Now/Next/Later) with confidence decreasing left to
right, keep solution ideas off the roadmap (they belong on the OST), and derive proposed product-level OKR
input for the CPO/coordinator rather than authoring the OKR set.

## Prompt

Use the product-manager `write-roadmap` skill to build a roadmap for the "onboarding" slice of an accounting
SaaS. A stakeholder has asked for: "bulk import in Q2, SSO in Q3, a mobile app in Q4." Current data: 30% of
new accounts import data in week one; week-one churn is 22%. Write the roadmap to a file under
`docs/product/` in the current working directory, in the skill's standard format.

Proceed without asking — produce the roadmap.

## Criteria

- [ ] PASS: Refuses to produce a dated feature timeline — does NOT render "bulk import, Q2 / SSO, Q3 / mobile app, Q4" as the roadmap
- [ ] PASS: Anchors on one to three desired outcomes expressed as a metric moving from a baseline to a target (e.g. week-one import 30% → 60%), not as features
- [ ] PASS: Uses Now / Next / Later (or GIST) horizons placed by how much is known, not by calendar date
- [ ] PASS: Confidence decreases left to right — Later items are explicit bets that may never happen, not certainties
- [ ] PASS: Keeps solution ideas (e.g. "bulk import", "onboarding wizard") OFF the roadmap — roadmap items are outcomes/opportunities; solutions belong on the opportunity solution tree
- [ ] PASS: Derives proposed product-level OKR input (Objective + KRs with baselines) marked as INPUT for the CPO/coordinator — does not author the company OKR set
- [ ] PASS: Flags any item lacking a baseline or evidence as a discovery gap rather than placing it in Now
- [ ] PARTIAL: Does not smuggle sprint-level backlog stories onto the roadmap — backlog is the product-owner's

## Output expectations

- [ ] PASS: Output roadmap file exists under `docs/product/` with a desired-outcomes table (baseline → target) at the top, not a list of features with quarters
- [ ] PASS: The Now / Next / Later sections contain outcomes/opportunities, each tied to a desired outcome — "bulk import in Q2" is reshaped into the behaviour-change it would drive
- [ ] PASS: Output explicitly notes that confidence decreases across the horizons and that Later items are bets allowed to die
- [ ] PASS: Output includes a proposed product-level OKR block (Objective + KRs with baselines) explicitly labelled as input for the CPO / coordinator, not an authored OKR set
- [ ] PASS: Solution-shaped items are redirected to the opportunity solution tree rather than placed on the roadmap
- [ ] PARTIAL: Output flags the requested "mobile app" (no baseline/evidence) as a Later bet or a discovery gap, not a committed Now item
