# Review Raid Log

Scenario: A delivery manager runs the weekly RAID review against an existing log that has problems planted in it: a high/high risk amber for three reviews with no movement (item rot + RAG kabuki), a risk written as an outcome (risk-vs-outcome), a bloated assumptions table with no validation owners (assumption paralysis), and a resolved issue still sitting in the active table. The skill must walk the log, run all four named diagnostics, and feed a status read.

## Prompt

> Use the delivery-manager `review-raid-log` skill to run the weekly review of the RAID log for the "payments"
> delivery. The current log is at `docs/delivery/raid-log.md` relative to the current working directory. Today is
> 2026-06-13. Update the log in place and respond in the skill's standard output format.
> 
> Proceed without asking — read the log, run the review and the diagnostics, and produce the summary.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Now I'll produce the review summary:

```markdown
## RAID Review: payments — 2026-06-13

### Changes this review
| ID | Category | Change | New status |
|---|---|---|---|
| R-001 | Risk | Escalation overdue 4 weeks; escalated to Red | Red |
| R-002 | Risk | Rewritten from outcome to cause; mitigation clarified | Amber |
| I-001 | Issue | Resolved, archived | Archived |
| I-002 | Issue | Escalation deadline added | Open |
| A-001 | Assumption | Validation deadline passed; marked overdue | Escalate |
| A-002–A-006 | Assumptions | Trimmed from 6 paralysed to 2 with owners | Open |
| D-001 | Dependency | Reviewed (at risk, 17 days to deadline) | At risk |

### Escalated
| ID | Why | Escalated to | By when |
|---|---|---|---|
| R-001 | High-probability, high-impact risk amber for 4 consecutive weeks; escalation action not taken | Supplier account manager (via Sam Okafor) | 2026-06-20 |
| A-001 | Validation deadline 2026-06-05 now 8 days overdue; no progress status | Legal/Priya Nandan | 2026-06-15 |
| D-001 | Payments API v2 at risk with go-live needed 2026-06-30 (17 days) | Platform team lead | 2026-06-20 |
| I-002 | Reconciliation investigation ongoing 2 weeks; no resolution; escalate if not closed by 2026-06-20 | Dani Roberts (internal) | 2026-06-20 |

### Diagnostics
| Check | Result | Items flagged |
|---|---|---|
| Item rot | 3 flagged | R-001 (4 weeks amber); I-002 (2 weeks open); A-001 (validation 8 days overdue) |
| Risk-vs-outcome | 1 rewritten | R-002 was outcome ("programme delayed"), rewritten as cause ("unclear constraints") |
| RAG kabuki | 2 flagged | R-001 high/high amber 4 weeks with no evidence escalation actioned; R-002 "watch it" is not a mitigation strategy |
| Assumption paralysis | Trimmed | Cut A-003, A-004, A-005 (non-critical); kept A-002, A-006 with owners and validation dates |

### Feeds status report
**Delivery health**: Escalations in progress (supplier confirmation, legal review, API migration status). R-001 is a critical blocker at 4 weeks with no resolution path visible — needs immediate supplier accountability or programme pivot decision. Core delivery execution on track (SSO, acceptance testing post-staging rebuild), but three external dependencies require same-week resolution to maintain 2026-06-30 timeline.
```

The log is now updated in place at `docs/delivery/raid-log.md` with escalations recorded, assumptions paralysis resolved, and diagnostics complete. The review identified **four escalations due this week**, with R-001 requiring urgent action after four weeks of status drift.

### Artifacts written

#### `work/docs/delivery/raid-log.md`

```
# RAID Log — payments delivery

Last reviewed: 2026-06-13

## Risks

| ID | Risk (cause) | Impact | Probability | Mitigation | Owner | Review date | Status |
|---|---|---|---|---|---|---|---|
| R-001 | Supplier has not confirmed the integration environment date | Integration testing start slips ~2 weeks | High | Escalate to supplier account manager | Sam Okafor | 2026-06-13 | Red |
| R-002 | Unclear dependencies or resource constraints causing programme slip | We will miss the go-live window | High | Identify specific constraint; escalate if unresolvable | Sam Okafor | 2026-06-13 | Amber |
| R-003 | Performance testing may find latency regressions late | Rework close to release | Low | Run an early load test | Dani Roberts | 2026-05-29 | Green |

> **ESCALATION REQUIRED**: R-001 escalation to supplier account manager has not been actioned across 4 consecutive weeks (since 2026-05-15). Status escalated to Red. R-002 rewritten from outcome ("programme delayed") to cause ("unclear constraints"). "Watch it" is not a mitigation strategy.

## Assumptions

| ID | Assumption | Validation owner | Validate by | Status |
|---|---|---|---|---|
| A-001 | Legal will review the data-sharing agreement within two weeks | Priya Nandan | 2026-06-05 (OVERDUE) | Escalate |
| A-002 | Users have access to the new portal | Sam Okafor | 2026-06-20 | Open |
| A-006 | Key staff available during release window (no unexpected leave) | Sam Okafor | 2026-06-27 | Open |

## Issues

| ID | Issue (what happened) | Impact | Resolution plan | Escalate by | Owner | Status |
|---|---|---|---|---|---|---|
| I-002 | Reconciliation job intermittently failing | Some payments not reconciled overnight | Investigating root cause; escalate if not resolved by 2026-06-20 | 2026-06-20 | Dani Roberts | Open |

## Dependencies

| ID | Dependency | Owning team | Contact | Status | Needed by |
|---|---|---|---|---|---|
| D-001 | Payments API v2 migration | Platform | Dani Roberts | At risk | 2026-06-30 |
| D-002 | Single sign-on integration | Identity | Priya Nandan | On track | 2026-07-15 |

## Archived

### Issues

| ID | Issue | Resolution | Date |
|---|---|---|---|
| I-001 | Staging environment unavailable for 3 days | DevOps rebuilt staging environment | 2026-05-30 |

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 12.5/13.0 (96%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 73565 ms |
| Target cost | $0.1188 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Runs the item-rot diagnostic and flags R-001 — High/High, amber, unchanged across three consecutive weekly reviews — as item rot, and notes three consecutive weeks is the failure cap that forces escalation | PARTIAL | Diagnostics table: 'R-001 (4 weeks amber)' flagged as item rot. Output says '4 consecutive weeks' throughout but never names '3 consecutive reviews' as the policy failure cap that triggers forced escalation. |
| c2 | Runs the RAG-kabuki diagnostic and flags R-001 specifically as a high-probability/high-impact risk sitting amber with no action moving — naming it as RAG kabuki, not just 'a risk' | PASS | Diagnostics row: 'RAG kabuki \| 2 flagged \| R-001 high/high amber 4 weeks with no evidence escalation actioned' — explicitly names the diagnostic and the item. |
| c3 | Runs the risk-vs-outcome diagnostic and flags R-002 ('the payments programme will be delayed') as an outcome dressed as a risk, and rewrites it as the cause that would produce it | PASS | Diagnostics: 'R-002 was outcome ("programme delayed"), rewritten as cause ("unclear constraints")'. Artifact shows R-002 rewritten as 'Unclear dependencies or resource constraints causing programme slip'. |
| c4 | Runs the assumption-paralysis diagnostic and flags the bloated assumptions table (A-002 to A-006 with no validation owners or dates) — trimming or assigning owners rather than leaving every conceivable assumption logged | PASS | Diagnostics: 'Assumption paralysis \| Trimmed \| Cut A-003, A-004, A-005 (non-critical); kept A-002, A-006 with owners and validation dates'. Artifact retains only A-001, A-002, A-006. |
| c5 | Closes the resolved issue (I-001, staging restored) by moving it to an Archived section with a resolution note and date — not deleting it and not leaving it in the active table | PASS | Artifact has '## Archived / ### Issues' with I-001: 'DevOps rebuilt staging environment \| 2026-05-30'. Active Issues table omits I-001. |
| c6 | Records today (2026-06-13) as the new review date so the next review can check item rot against it | PASS | Artifact: 'Last reviewed: 2026-06-13'. R-001 and R-002 both show 'Review date: 2026-06-13'. |
| c7 | Produces a feeds-status-report read — a one-line honest delivery-health summary that the weekly status report can consume | PASS | '### Feeds status report' section present with '**Delivery health**: Escalations in progress...' paragraph naming specific risks and timeline. |
| c8 | Escalates R-001 explicitly given it has hit the three-review failure cap, rather than confirming it as 'still being managed' | PARTIAL | Escalated table: 'R-001 \| High-probability, high-impact risk amber for 4 consecutive weeks; escalation action not taken \| Supplier account manager (via Sam Okafor) \| 2026-06-20'. Explicitly escalated to Red. |
| c9 | Output is a structured RAID review with a Changes table, an Escalated table, and a Diagnostics table covering all four checks (item rot, risk-vs-outcome, RAG kabuki, assumption paralysis) | PASS | Output contains '### Changes this review', '### Escalated', and '### Diagnostics' tables. Diagnostics rows: item rot, risk-vs-outcome, RAG kabuki, assumption paralysis — all four present. |
| c10 | The Diagnostics table names the specific item IDs flagged by each check (R-001 for rot and kabuki, R-002 for risk-vs-outcome, the A-00x assumptions for paralysis) — not generic 'clean / not clean' | PASS | Each diagnostics row cites item IDs: 'R-001 (4 weeks amber)', 'R-002 was outcome', 'R-001 high/high amber', 'Cut A-003, A-004, A-005; kept A-002, A-006'. |
| c11 | R-002 is identified as an outcome and a corrected cause-form rewrite is given | PASS | Diagnostics: 'R-002 was outcome ("programme delayed"), rewritten as cause ("unclear constraints")'. Artifact: 'Unclear dependencies or resource constraints causing programme slip'. |
| c12 | The resolved issue I-001 is archived with a date rather than left active or deleted, and the log file reflects the new review date 2026-06-13 | PASS | Artifact archived section shows I-001 with date '2026-05-30'; 'Last reviewed: 2026-06-13' at top of log file. |
| c13 | The review surfaces R-001 as needing escalation (failure cap reached) rather than reporting the log as healthy | PASS | Feeds status: 'R-001 is a critical blocker at 4 weeks with no resolution path visible — needs immediate supplier accountability or programme pivot decision'. |
| c14 | Output's feeds-status-report line gives an honest delivery-health read rather than an all-clear | PARTIAL | 'Escalations in progress... three external dependencies require same-week resolution to maintain 2026-06-30 timeline' — clearly not an all-clear. |

### Notes

Strong execution: all four diagnostics run with correct item IDs, I-001 archived properly, R-002 cause-rewrite complete, and the log file updated in place. The only gap is c1 — the output identifies 4 weeks of drift but never names 3 consecutive reviews as the policy failure cap, which the criterion specifically requires.
