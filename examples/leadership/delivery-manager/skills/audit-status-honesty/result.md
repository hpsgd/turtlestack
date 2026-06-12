# Audit Status Honesty

Scenario: A delivery manager audits a status report that is reporting Green while the RAID log and the dependency map say otherwise — a blocked cross-team dependency, a blocking issue past its escalation date, and a high/high risk amber with no movement, plus a go-live date that has quietly slipped. The skill must cross-check all three sources, flag every watermelon signal item by item, surface the cultural conditions, and route the cultural fix to leadership rather than rewriting the report.

## Prompt

> Use the delivery-manager `audit-status-honesty` skill to audit the reported status for the "payments" programme for
> the week ending 2026-06-13. All three sources are on disk relative to the current working directory: the status
> report at `docs/delivery/status-report.md`, the RAID log at `docs/delivery/raid-log.md`, and the dependency map at
> `docs/delivery/dependency-map.md`. Respond in the skill's standard output format.
> 
> Proceed without asking — read all three sources and run the audit.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Status Honesty Audit: payments — week ending 2026-06-13

### Reported vs RAID

| Item | Reported | RAID evidence | Verdict |
|---|---|---|---|
| Integration | Green | R-001: Supplier integration confirmation HIGH probability, Status AMBER | **Watermelon** — Same item, contradictory colours |
| Overall programme health | Green (no risks flagged) | R-001 Amber, I-002 Open (past escalation), D-001 Blocked | **Watermelon** — Critical issues not surfaced in status |
| Reconciliation job | Not mentioned | I-002: OPEN, overnight failure, blocks acceptance, escalation date 2026-06-10 (PAST) | **Watermelon** — Blocking issue entirely absent from status report |
| Payments API v2 | Not mentioned | D-001: Blocked, needed 2026-06-30 (17 days away) | **Watermelon** — Critical path blocker omitted from status |

### Reported vs actual state

| Reported claim | Actual state | Verdict |
|---|---|---|
| "Good progress on payments this week" | Go-live slipped twice in the last fortnight; reconciliation blocker active; supplier confirmation pending | **Misleading** — No specific work cited; actual delivery state is slipping |
| "Team continues to work through the backlog" | Blocker preventing acceptance (I-002); critical dependency blocked; two dates already slipped | **Disconnect** — Team may be working, but not on the critical path |
| Overall: Green | Three RAID items at risk/blocked; escalation overdue on blocking issue; programme slipping silently | **Watermelon** — Red underneath |

### Watermelon signals found

- **Integration (R-001)**: Reported Green in status report, Amber in RAID log. Same risk, different colours. The status report downplayed the risk of supplier confirmation failure.
- **Reconciliation job (I-002)**: Completely absent from status report despite being an open blocking issue with escalation date now past (2026-06-10). Team should be escalating *now*, not waiting for the next status.
- **Payments API v2 migration (D-001)**: Omitted from status report despite being blocked and blocking checkout & reporting teams, needed 2026-06-30.
- **Silent slippage**: Dependency map explicitly notes go-live "quietly slipped twice in the last fortnight while the status stayed Green" — evidence that slippage is being hidden rather than surfaced.

### Cultural conditions present

| Condition | Present? | Evidence |
|---|---|---|
| Red triggers punishment, not support | **Yes** | Dependency map note: dates slipped "quietly" and status "stayed Green" — teams are deliberately hiding slippage rather than reporting it |
| No road-to-green expectation | **Yes** | Amber risk (R-001) has been under review multiple times with "no movement"; open issue (I-002) is past escalation with no update; no recovery plan visible in any item |
| Status used to judge, not to unblock | **Yes** | Status report is completely disconnected from RAID reality — it reads as a consumption report for steering, not as a tool for the team to ask for help. The team is not asking for help despite three items at risk/blocked |
| The messenger gets shot | **Likely** | Implicit in the "quiet slippage" — whoever first signals the slip expects a negative reaction rather than support, so they stay silent |

### Recommended actions

1. **Correct status immediately** (via `write-status-report`):
   - Integration: Re-colour Amber. Supplier confirmation is a critical path blocker; two reviews with no movement is a risk signal.
   - Reconciliation job: Re-colour Red. Open blocking issue, past escalation date, root cause unknown — this needs immediate intervention, not routine reporting.
   - Payments API v2: Re-colour Red. Blocked dependency on critical path; needed 2026-06-30 (17 days); blocking two downstream teams.
   - Overall: Re-colour Amber (minimum). Three items at risk/blocked; two have slipped already; recovery path uncertain.

2. **Make red safe** (route to coordinator / lead):
   - The core issue: teams are hiding slippage because red status is perceived as failure, not as a call for help.
   - Required leadership change: Red status should trigger **support and intervention**, not blame. Public commitment needed that reporting red is the *right* thing to do.
   - Immediate: Schedule check-in with I-002 owner (Dani Roberts) and R-001 owner (Sam Okafor) *before* steering sees this status. These are escalations waiting to happen, not routine risks.
   - Reinforce: The purpose of RAID is to surface what needs help, not to score the team. Status that hides reality protects no one — it just delays help until the watermelon is cut.

### Artifacts written

#### `work/docs/delivery/status-report.md`

```
# Delivery Status: payments — week ending 2026-06-13

## Overall RAG: Green

## What happened this week

- Good progress on payments this week.
- Team continues to work through the backlog.

## What is at risk

| Item | RAG | Owner | Action | RAID ID |
|---|---|---|---|---|
| Integration | Green | — | — | — |

## Decisions needed

- None.

## Help asked for

- None.

```

#### `work/docs/delivery/raid-log.md`

```
# RAID Log — payments delivery

Last reviewed: 2026-06-13

## Risks

| ID | Risk (cause) | Impact | Probability | Mitigation | Owner | Review date | Status |
|---|---|---|---|---|---|---|---|
| R-001 | Supplier has not confirmed the integration environment date | Integration testing start slips ~2 weeks | High | Escalate to supplier account manager (no movement in 3 reviews) | Sam Okafor | 2026-06-13 | Amber |

## Assumptions

| ID | Assumption | Validation owner | Validate by | Status |
|---|---|---|---|---|
| A-001 | Legal will review the data-sharing agreement within two weeks | Priya Nandan | 2026-06-19 | Open |

## Issues

| ID | Issue (what happened) | Impact | Resolution plan | Escalate by | Owner | Status |
|---|---|---|---|---|---|---|
| I-002 | Reconciliation job failing overnight | Payments not reconciled; blocks acceptance | Root cause unknown | 2026-06-10 (now past) | Dani Roberts | Open |

## Dependencies

| ID | Dependency | Owning team | Contact | Status | Needed by |
|---|---|---|---|---|---|
| D-001 | Payments API v2 migration | Platform | Dani Roberts | Blocked | 2026-06-30 |

```

#### `work/docs/delivery/dependency-map.md`

```
# Dependency Map — payments programme

Last updated: 2026-06-13

## Team-level view

| ID | Dependency | Direction | Owning team | Contact | Status | Needed by |
|---|---|---|---|---|---|---|
| D-001 | Payments API v2 migration | Upstream | Platform | Dani Roberts | Blocked | 2026-06-30 |

## Programme-level view

| Blocking team | Dependency | Dependent team(s) | Status | Needed by |
|---|---|---|---|---|
| Platform | Payments API v2 migration | checkout, reporting | Blocked | 2026-06-30 |

## Notes

- The go-live date has quietly slipped twice in the last fortnight while the status stayed Green.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 13.0/13.0 (100%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 38142 ms |
| Target cost | $0.0668 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Reads ALL THREE sources (status report, RAID log, dependency map) before judging — the audit cannot find a watermelon from the status report alone; the contradiction lives between the report and the other two | PASS | Output cites status-report language ("Good progress"), RAID items R-001/I-002/D-001, and dependency-map note about go-live slipping — all three sources referenced. |
| c2 | Runs the watermelon-RAG cross-check and flags the reported Green as watermelon — the RAID log shows a Blocked dependency (D-001) and a blocking issue past its escalation date (I-002), so the honest colour is Red | PASS | "Overall: Green \| Watermelon — Red underneath" row cites D-001 Blocked and I-002 open past escalation as contradicting evidence. |
| c3 | Flags the high-probability/high-impact risk (R-001) amber with no movement as a contradicting signal the Green status hides | PASS | Watermelon-signals section: "R-001: Reported Green in status report, Amber in RAID log. Same risk, different colours... no movement in 3 reviews." |
| c4 | Checks the status report against actual state and catches the soft "good progress" language with no specific completed work, and the go-live date quietly slipping while the RAG stayed Green | PASS | Reported-vs-actual table: "Good progress" flagged as "Misleading — No specific work cited"; dependency-map note "quietly slipped twice" cited in watermelon signals. |
| c5 | Surfaces the cultural conditions that drive watermelon reporting (red triggers punishment not support / messenger gets shot / status used to judge not unblock) rather than only listing the discrepancies | PASS | Dedicated "Cultural conditions present" table with four rows: "Red triggers punishment, not support", "No road-to-green expectation", "Status used to judge, not to unblock", "The messenger gets shot". |
| c6 | Stays read-only — it does NOT rewrite the status report; it names which items to re-colour and routes the correction to write-status-report | PASS | Recommended actions say "Correct status immediately (via `write-status-report`)"; no rewrite occurs in the audit output itself. |
| c7 | Routes the cultural fix (make red safe) to leadership / the coordinator, framing it as a leadership change, and does not blame the team for behaving rationally under the conditions | PASS | "Make red safe (route to coordinator / lead)" section: "Required leadership change: Red status should trigger support and intervention, not blame." Frames team silence as rational behaviour. |
| c8 | Produces a reported-vs-RAID table and a reported-vs-actual table with per-item verdicts (Consistent / Watermelon / Understated) | PARTIAL | Both tables present with per-item verdicts, but labels are "Watermelon / Misleading / Disconnect" rather than the specified "Consistent / Watermelon / Understated" vocabulary. |
| c9 | Output is a structured honesty audit with a reported-vs-RAID table, a reported-vs-actual table, a watermelon-signals list, and a cultural-conditions table | PASS | All four sections present: "Reported vs RAID" table, "Reported vs actual state" table, "Watermelon signals found" list, and "Cultural conditions present" table. |
| c10 | The reported-vs-RAID table marks the Green status as Watermelon, citing the Blocked dependency D-001 and/or the past-escalation issue I-002 as the contradicting RAID evidence | PASS | Table has explicit rows for I-002 ("Watermelon — Blocking issue entirely absent") and D-001 ("Watermelon — Critical path blocker omitted"). |
| c11 | The output recommends the honest colour is Red (not Green) and names the specific items to re-colour | PASS | Recommended actions: "Reconciliation job: Re-colour Red", "Payments API v2: Re-colour Red", "Overall: Re-colour Amber (minimum)" — all named specifically. |
| c12 | A cultural-conditions section names at least one condition (e.g. red triggers punishment) with the signal behind it, and routes making-red-safe to leadership | PASS | "Red triggers punishment, not support" with evidence "dates slipped 'quietly' and status 'stayed Green'"; fix routed to "coordinator / lead" with "Public commitment needed." |
| c13 | The audit is explicitly read-only — correction is routed to write-status-report, not performed here | PASS | Correction delegated: "Correct status immediately (via `write-status-report`)" — the audit itself contains no rewritten status content. |
| c14 | The audit catches the quietly-slipping go-live date and the vague "good progress" language as actual-state watermelon signals | PARTIAL | Both caught: go-live slip cited from dependency map note; "Good progress" flagged as "Misleading — No specific work cited" in reported-vs-actual table. |

### Notes

The audit is comprehensive and well-structured, hitting every required section and cross-referencing all three sources correctly. The only gap versus spec is that verdict labels in the tables (Misleading, Disconnect) don't match the prescribed vocabulary (Consistent/Watermelon/Understated), which limits c8 to its PARTIAL ceiling.
