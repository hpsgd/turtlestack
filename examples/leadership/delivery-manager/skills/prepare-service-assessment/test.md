# Test: prepare-service-assessment compiles evidence, runs the mock, tracks remediation for a beta gate

Scenario: A delivery manager prepares a GDS service for its public-beta assessment. The team is strong on user
research but has a gap (no end-to-end journey across channels) and the beta KPIs are not all tracked. The skill must
compile evidence against the Service Standard, confirm the beta KPIs, run a mock assessment, track remediation for
each gap, and refuse to declare ready while gaps remain on points the panel will test.

## Prompt

Use the delivery-manager `prepare-service-assessment` skill to prepare the "apply-for-a-permit" service for its
public-beta service assessment. Write the assessment-prep evidence to
`docs/delivery/service-assessment/beta/readiness.md` relative to the current working directory. Respond in the
skill's standard output format.

State of play:

- Strong user research: findings, personas, and journey maps exist (Service Standard point 1 is well covered).
- Gap: there is no end-to-end journey across channels — the offline/phone path for users who can't use the digital
  service has not been mapped (point 2).
- Beta KPIs: user satisfaction and completion rate are tracked; cost per transaction and digital take-up are NOT
  tracked yet.
- The team feels confident overall and wants to book the assessment for next week.

Proceed without asking — compile evidence, confirm KPIs, run the mock, and track remediation.

## Criteria

- [ ] PASS: Compiles evidence against the GOV.UK Service Standard points, marking point 1 (understand users) as Ready with concrete evidence and point 2 (solve a whole problem) as a Gap — evidence is concrete artifacts, not assertions
- [ ] PASS: Confirms the beta KPIs are tracked and flags the two that are NOT (cost per transaction, digital take-up) — a beta assessment without these tracked is not ready
- [ ] PASS: Runs a mock assessment — walking the points as the panel would, asking the hard question, and judging whether the evidence stands / is thin / is missing
- [ ] PASS: Every gap (the missing end-to-end journey, the untracked KPIs) becomes a remediation item with a named owner and a by-when date, tracked through to the assessment
- [ ] PASS: Refuses to declare the service ready while unremediated gaps remain on points the panel will test — the readiness verdict is "Not ready — N gaps open", not "ready, book it next week" (decision checkpoint honoured)
- [ ] PASS: Frames the assessment as a whole-team responsibility coordinated by the delivery manager, not a one-person exercise
- [ ] PARTIAL: Distinguishes the beta gate's expectations (production-quality service with measurable KPIs) from an alpha gate's (testing the right things with prototypes)

## Output expectations

- [ ] PASS: A `docs/delivery/service-assessment/beta/readiness.md` file is written with an evidence-against-the-standard table, a beta-KPI table, a mock-assessment findings table, and a remediation tracker
- [ ] PASS: The evidence table marks point 1 Ready and point 2 a Gap, with concrete evidence cited for the Ready point
- [ ] PASS: The KPI table marks cost-per-transaction and digital-take-up as not tracked
- [ ] PASS: The remediation tracker lists each gap with an owner and a by-when date
- [ ] PASS: The readiness verdict is "Not ready — N gaps open" rather than ready-to-book, holding the decision checkpoint
- [ ] PARTIAL: The mock-assessment findings rate at least one point as Thin or Missing rather than asserting everything stands
