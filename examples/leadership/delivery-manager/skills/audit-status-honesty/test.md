# Test: audit-status-honesty runs the watermelon-RAG diagnostic across three sources

Scenario: A delivery manager audits a status report that is reporting Green while the RAID log and the dependency
map say otherwise — a blocked cross-team dependency, a blocking issue past its escalation date, and a high/high risk
amber with no movement, plus a go-live date that has quietly slipped. The skill must cross-check all three sources,
flag every watermelon signal item by item, surface the cultural conditions, and route the cultural fix to
leadership rather than rewriting the report.

## Prompt

Use the delivery-manager `audit-status-honesty` skill to audit the reported status for the "payments" programme for
the week ending 2026-06-13. All three sources are on disk relative to the current working directory: the status
report at `docs/delivery/status-report.md`, the RAID log at `docs/delivery/raid-log.md`, and the dependency map at
`docs/delivery/dependency-map.md`. Respond in the skill's standard output format.

Proceed without asking — read all three sources and run the audit.

## Criteria

- [ ] PASS: Reads ALL THREE sources (status report, RAID log, dependency map) before judging — the audit cannot find a watermelon from the status report alone; the contradiction lives between the report and the other two
- [ ] PASS: Runs the watermelon-RAG cross-check and flags the reported Green as watermelon — the RAID log shows a Blocked dependency (D-001) and a blocking issue past its escalation date (I-002), so the honest colour is Red
- [ ] PASS: Flags the high-probability/high-impact risk (R-001) amber with no movement as a contradicting signal the Green status hides
- [ ] PASS: Checks the status report against actual state and catches the soft "good progress" language with no specific completed work, and the go-live date quietly slipping while the RAG stayed Green
- [ ] PASS: Surfaces the cultural conditions that drive watermelon reporting (red triggers punishment not support / messenger gets shot / status used to judge not unblock) rather than only listing the discrepancies
- [ ] PASS: Stays read-only — it does NOT rewrite the status report; it names which items to re-colour and routes the correction to write-status-report
- [ ] PASS: Routes the cultural fix (make red safe) to leadership / the coordinator, framing it as a leadership change, and does not blame the team for behaving rationally under the conditions
- [ ] PARTIAL: Produces a reported-vs-RAID table and a reported-vs-actual table with per-item verdicts (Consistent / Watermelon / Understated)

## Output expectations

- [ ] PASS: Output is a structured honesty audit with a reported-vs-RAID table, a reported-vs-actual table, a watermelon-signals list, and a cultural-conditions table
- [ ] PASS: The reported-vs-RAID table marks the Green status as Watermelon, citing the Blocked dependency D-001 and/or the past-escalation issue I-002 as the contradicting RAID evidence
- [ ] PASS: The output recommends the honest colour is Red (not Green) and names the specific items to re-colour
- [ ] PASS: A cultural-conditions section names at least one condition (e.g. red triggers punishment) with the signal behind it, and routes making-red-safe to leadership
- [ ] PASS: The audit is explicitly read-only — correction is routed to write-status-report, not performed here
- [ ] PARTIAL: The audit catches the quietly-slipping go-live date and the vague "good progress" language as actual-state watermelon signals
