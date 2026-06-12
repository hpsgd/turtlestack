# Test: Accept readiness package

Scenario: A delivery-manager hands the release-manager two release-readiness packages. One (Billing v2.4) is complete with evidence on every coordination item; the other (Search v3.0) has a missing ops runbook and a bare "Confirmed" on Support briefed with no evidence. The skill must gate the first to a GO input and return the second to sender as a NO-GO with the specific gaps named.

## Prompt

Two release-readiness packages have been handed over by the delivery-manager. They are on disk at:

- `{workspace}/work/release-readiness/billing-v2.4-package.md` — Billing v2.4
- `{workspace}/work/release-readiness/search-v3.0-package.md` — Search v3.0

Read both packages.

/release-manager:accept-readiness-package Billing v2.4 and Search v3.0 — packages at the paths above

Process BOTH packages. For each one, run the full skill: validate the package is complete, map each coordination item to a release-plan readiness gate, run the readiness assessment over the combined engineering + coordination picture, and produce a go/no-go input with explicit blockers. Use the Output Format from the skill for each. Treat a bare "Confirmed" with no evidence (a link, a date, a reference) as an open/unconfirmed item, exactly as the skill's rules require.

## Criteria

- [ ] PASS: Billing v2.4 is validated as a complete package — all six coordination items present with evidence (link/date/reference), so it proceeds to assessment
- [ ] PASS: Search v3.0 is returned-to-sender / NO-GO — the missing ops runbook is named as a gap, not downgraded to a warning
- [ ] PASS: Search v3.0's "Support briefed: Confirmed" with no evidence is treated as an open/unconfirmed item — a bare status is not acceptance
- [ ] PASS: Billing v2.4 produces a GO input; Search v3.0 produces a NO-GO input — the two verdicts are distinct and justified
- [ ] PASS: The engineering gates (Definition of Done, verification tests, open bugs, migrations, performance) are assessed directly by the release-manager — not assumed satisfied by the package
- [ ] PASS: The skill does not re-coordinate the missing items itself (does not quietly draft the runbook or brief support) — it returns the gap to the delivery-manager
- [ ] PARTIAL: Output uses the skill's structured Output Format — package-validation table, gate-mapping/combined-assessment table, and go/no-go input with a blockers table

## Output expectations

- [ ] PASS: Output contains two separate assessments (Billing v2.4 and Search v3.0), each with its own package-validation result and go/no-go verdict — not a single merged verdict
- [ ] PASS: Search v3.0's validation table marks the Ops runbook as a Gap (MISSING) and the result is "Returned-to-sender" → NO-GO
- [ ] PASS: The combined assessment table fills the engineering gates from each package's engineering evidence (test exit codes, migration logs, performance numbers) and the operational/communication gates from the coordination items
- [ ] PASS: Search v3.0's NO-GO lists blockers in a table with Blocker | Gate | Owner | Action to clear — naming the runbook (DevOps) and the unconfirmed support briefing
- [ ] PASS: Output does not propose a conditional go for Search v3.0's missing package items (a missing package item is never a conditional go per the skill)
