# Test: review-raid-log runs the four diagnostics against a rotting log

Scenario: A delivery manager runs the weekly RAID review against an existing log that has problems planted in it: a
high/high risk amber for three reviews with no movement (item rot + RAG kabuki), a risk written as an outcome
(risk-vs-outcome), a bloated assumptions table with no validation owners (assumption paralysis), and a resolved
issue still sitting in the active table. The skill must walk the log, run all four named diagnostics, and feed a
status read.

## Prompt

Use the delivery-manager `review-raid-log` skill to run the weekly review of the RAID log for the "payments"
delivery. The current log is at `docs/delivery/raid-log.md` relative to the current working directory. Today is
2026-06-13. Update the log in place and respond in the skill's standard output format.

Proceed without asking — read the log, run the review and the diagnostics, and produce the summary.

## Criteria

- [ ] PASS: Runs the item-rot diagnostic and flags R-001 — High/High, amber, unchanged across three consecutive weekly reviews — as item rot, and notes three consecutive weeks is the failure cap that forces escalation
- [ ] PASS: Runs the RAG-kabuki diagnostic and flags R-001 specifically as a high-probability/high-impact risk sitting amber with no action moving — naming it as RAG kabuki, not just "a risk"
- [ ] PASS: Runs the risk-vs-outcome diagnostic and flags R-002 ("the payments programme will be delayed") as an outcome dressed as a risk, and rewrites it as the cause that would produce it
- [ ] PASS: Runs the assumption-paralysis diagnostic and flags the bloated assumptions table (A-002 to A-006 with no validation owners or dates) — trimming or assigning owners rather than leaving every conceivable assumption logged
- [ ] PASS: Closes the resolved issue (I-001, staging restored) by moving it to an Archived section with a resolution note and date — not deleting it and not leaving it in the active table
- [ ] PASS: Records today (2026-06-13) as the new review date so the next review can check item rot against it
- [ ] PASS: Produces a feeds-status-report read — a one-line honest delivery-health summary that the weekly status report can consume
- [ ] PARTIAL: Escalates R-001 explicitly given it has hit the three-review failure cap, rather than confirming it as "still being managed"

## Output expectations

- [ ] PASS: Output is a structured RAID review with a Changes table, an Escalated table, and a Diagnostics table covering all four checks (item rot, risk-vs-outcome, RAG kabuki, assumption paralysis)
- [ ] PASS: The Diagnostics table names the specific item IDs flagged by each check (R-001 for rot and kabuki, R-002 for risk-vs-outcome, the A-00x assumptions for paralysis) — not generic "clean / not clean"
- [ ] PASS: R-002 is identified as an outcome and a corrected cause-form rewrite is given
- [ ] PASS: The resolved issue I-001 is archived with a date rather than left active or deleted, and the log file reflects the new review date 2026-06-13
- [ ] PASS: The review surfaces R-001 as needing escalation (failure cap reached) rather than reporting the log as healthy
- [ ] PARTIAL: Output's feeds-status-report line gives an honest delivery-health read rather than an all-clear
