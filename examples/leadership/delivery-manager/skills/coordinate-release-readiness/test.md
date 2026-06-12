# Test: coordinate-release-readiness assembles the package and stops at the gate

Scenario: A delivery manager coordinates the upstream readiness for a release. Some pieces are confirmed, one is an
open gap (no ops runbook), and a gating dependency is still at risk. The skill must work the readiness checklist with
evidence, refuse to present an incomplete package as complete, hand off to the release-manager, and not execute the
release or own the go/no-go.

## Prompt

Use the delivery-manager `coordinate-release-readiness` skill to coordinate readiness for the "payments v2.0"
release. Write the release-readiness package to `docs/delivery/release-readiness.md` relative to the current working
directory. Respond in the skill's standard output format.

State of play:

- Support has been briefed (FAQ + known issues handed over, dated 11 June).
- GTM is aligned — launch announcement drafted, no clash with the deployment window.
- Customer comms are planned (email + in-app, to go out after the release is verified stable).
- Governance: security sign-off is on file.
- The ops runbook for the new reconciliation behaviour does NOT exist yet — nobody has written it.
- A gating dependency, the Payments API v2 migration (D-001), is still At risk.

Proceed without asking — work the checklist, assemble the package, and decide whether it can be handed off.

## Criteria

- [ ] PASS: Works the readiness checklist with evidence per item (support briefed with the 11 June date, GTM with the drafted announcement, security sign-off on file) — confirming each rather than assuming
- [ ] PASS: Identifies the missing ops runbook as an open gap and names an owner (DevOps / ops) and an action/date to close it — not glossed over
- [ ] PASS: Flags the at-risk gating dependency (D-001) as a blocker to a complete package — a release cannot be ready while a gating dependency is at risk, so it is raised in the RAID / status, not buried
- [ ] PASS: Does NOT present the package as complete given the open runbook gap and the at-risk dependency — the package status is Incomplete with the open items listed (decision checkpoint honoured)
- [ ] PASS: Confirms customer comms are planned now but go out only AFTER the release is verified stable, while support is briefed before deployment
- [ ] PASS: Hands the package to the release-manager and explicitly stops at the gate — the release-manager owns go/no-go, deployment, and rollback; this skill does not execute the release
- [ ] PARTIAL: Does not absorb the release-manager's engineering gates (tests, performance, migrations, rollback) into the readiness checklist — keeps the boundary

## Output expectations

- [ ] PASS: A `docs/delivery/release-readiness.md` file is written with a readiness checklist table (item / status / evidence / owner)
- [ ] PASS: The package status is Incomplete (not Complete) with the ops runbook gap and the at-risk dependency listed as open items
- [ ] PASS: A hand-off note routes the package to the release-manager and states the release-manager owns the go/no-go — the delivery manager does not make that call
- [ ] PASS: The confirmed items (support, GTM, security sign-off, customer comms plan) carry evidence rather than bare assertions
- [ ] PARTIAL: Output states the delivery manager coordinates readiness but does not execute the release, holding the boundary explicitly
