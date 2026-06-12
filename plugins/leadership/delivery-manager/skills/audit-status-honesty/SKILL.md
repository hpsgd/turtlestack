---
name: audit-status-honesty
description: "Audit delivery status for watermelon reporting — green outside, red inside. Cross-checks status reports against the RAID log against the actual delivery state, and surfaces the cultural conditions that drive watermelon reporting (red triggers punishment rather than support). Use to validate status honesty before a steering meeting, or when reported status and reality seem to diverge."
argument-hint: "[delivery name or reporting period to audit]"
user-invocable: true
allowed-tools: Read, Glob, Grep
---

# Audit status honesty

Audit the delivery status for $ARGUMENTS for watermelon reporting — green on the outside, red on the inside. This is a read-only audit: it cross-checks the status reports (`write-status-report`) against the RAID log (`review-raid-log`) against the actual delivery state, and surfaces both the discrepancies and the cultural conditions that produce them. It does not rewrite the reports — it tells the delivery-manager and the team where status and reality have diverged.

Watermelon reporting is the most common and most damaging status failure. The mechanism: when an organisation treats red status as evidence of failure, honesty feels unsafe. Teams learn to avoid red — they skip amber, where action could still help, and stay green until the problem is undeniable. By the time the watermelon is cut open, it is too late to act.

## Step 1: Read all three sources

Read in order:

1. The latest status report(s) for the period — the reported RAG and the four components.
2. The current RAID log — the open risks, issues, and at-risk or blocked dependencies.
3. Any signal of actual delivery state — the dependency map, recent slippage, the scrum-of-scrums blockers, missed dates.

You are looking for the gap between what was reported and what the other two sources say is true.

## Step 2: Cross-check reported status against the RAID log

For each item reported green or amber, check the RAID log for contradicting evidence:

| Reported | RAID says | Verdict |
|---|---|---|
| Green | High-probability, high-impact risk open with no mitigation moving | Watermelon — should be amber or red |
| Green | Blocking issue past its 48hr escalation, unresolved | Watermelon — should be red |
| Amber | Blocked dependency with no road to green | Understated — should be red |
| Green | Clean RAID, dependencies on track | Consistent |

A status colour that the RAID log contradicts is the core watermelon signal. Flag every one.

## Step 3: Check the status report against actual delivery state

Compare what was reported as "happened" against what actually moved. Signs of watermelon at this layer:

- Dates quietly slipping while the RAG stays green.
- "Good progress" language with no specific completed work behind it.
- Risks described as "being managed" for weeks with no change in the RAID log.
- Decisions that needed asking never named in the report.

## Step 4: Surface the cultural conditions

Watermelon reporting is a symptom; the cause is usually cultural. Surface the conditions, because fixing the report without fixing the culture just produces the next watermelon:

| Condition | Signal | Consequence |
|---|---|---|
| Red triggers punishment, not support | People describe red as "admitting failure" | Teams stay green until undeniable |
| No road-to-green expectation | Amber/red reported without recovery plans | Red feels like surrender, so it is avoided |
| Status used to judge, not to unblock | Steering reacts to colour, not to the ask | Honesty has no upside, so it stops |
| The messenger gets shot | The last person to report red was blamed | Everyone learned the lesson |

Name which conditions are present. The fix is to make red safe — red should trigger support and intervention, not blame. That is a leadership change, not a reporting change, so route it to the coordinator or the relevant lead.

## Step 5: Report the findings

Report the discrepancies and the conditions. This is a diagnostic for the delivery-manager and the team, not a rewrite of the status. The delivery-manager uses it to correct the status honestly (via `write-status-report`) and to raise the cultural conditions with leadership.

## Rules

- This is a read-only audit. It does not rewrite status reports — it surfaces where they diverge from reality. Correction happens in `write-status-report`.
- A status colour the RAID log contradicts is a watermelon signal. Flag every one, by item.
- Always check all three sources. Status alone cannot reveal a watermelon — the contradiction lives between the report and the RAID log and the actual state.
- Surface the cultural conditions, not just the discrepancies. Fixing the report without making red safe produces the next watermelon.
- Route the cultural fix to leadership. Making red safe is a leadership change; the delivery-manager surfaces it but cannot mandate it alone.
- Never blame the team for watermelon reporting. The behaviour is rational under the conditions — change the conditions, not the people.

## Output Format

```markdown
## Status Honesty Audit: [delivery] — [period]

### Reported vs RAID
| Item | Reported | RAID evidence | Verdict (Consistent / Watermelon / Understated) |
|---|---|---|---|

### Reported vs actual state
| Reported claim | Actual state | Verdict |
|---|---|---|

### Watermelon signals found
- [Item-by-item list of green/amber statuses contradicted by evidence]

### Cultural conditions present
| Condition | Present? | Evidence |
|---|---|---|

### Recommended actions
1. Correct status: [which items to re-colour, via write-status-report]
2. Make red safe: [the cultural change, routed to coordinator / lead]
```

## Related skills

- `/delivery-manager:write-status-report` — this audit is read-only; correction happens there. Items the audit flags as watermelon get re-coloured honestly in the next status report.
- `/delivery-manager:review-raid-log` — the reviewed RAID is the evidence base for the cross-check. A stale RAID makes the audit unreliable, so review it first.
- `/delivery-manager:prepare-steering-pack` — run this audit before a steering meeting so the pack's health summary is honest rather than watermelon.
