---
name: review-raid-log
description: "Run the weekly RAID log review — scan for status changes, close resolved items, escalate overdue ones, and run the item-rot, risk-vs-outcome, RAG-kabuki, and assumption-paralysis diagnostics. Use for the weekly delivery review or whenever the RAID log needs a health check before a status report or steering pack."
argument-hint: "[delivery name, or the RAID log path]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Review a RAID log

Run the weekly review of the RAID log for $ARGUMENTS. New items are captured with `write-raid-log`; this skill keeps the log honest and moving. A well-maintained log reviews in under 15 minutes. The log lives at `docs/delivery/raid-log.md`. The output of this review feeds `write-status-report` and `audit-status-honesty`.

The log is not a history document. The discipline of review is: scan for items changing status, close items that are resolved, escalate items overdue on their action. A stale RAID log is worse than no log — it manufactures false confidence in front of senior stakeholders.

## Step 1: Read the full log

Read `docs/delivery/raid-log.md`. Note the last review date (recorded at the top of the file). Anything not touched since the last review is a candidate for the item-rot check in Step 4.

## Step 2: Walk every open item

For each open risk, assumption, issue, and dependency, decide one of:

| Decision | Action |
|---|---|
| Resolved | Move to the archived section with a resolution note and date |
| Status changed | Update the status and the relevant date |
| Action overdue | Escalate per the item's escalation path; raise it in the status report |
| Materialised | A risk that has happened becomes an issue — re-log it as I-, link the risk ID |
| No change | Confirm it is still genuinely being managed, not just sitting |

## Step 3: Update dates and statuses

Apply every decision from Step 2 to the log. Record today as the new review date at the top. Move resolved items to `## Archived` rather than deleting them — the audit trail matters.

## Step 4: Run the four diagnostics

### Item rot

Any item unchanged across this review and the previous one (two consecutive weeks at the same status) is flagged as item rot. Item rot means the log is drifting from reality. Force a decision: either the item is genuinely static (rare) or it is being ignored. Three consecutive weeks at the same status is a failure cap — escalate it.

### Risk-vs-outcome

Scan every risk. If it reads as an outcome ("the project will slip", "we might miss the date"), it is malformed. Rewrite it as the cause that would produce that outcome, structured cause → impact → probability → mitigation. An outcome dressed as a risk cannot be mitigated because there is no cause to act on.

### RAG kabuki

Check whether any high-probability, high-impact risk has been sitting amber for weeks with no action taken. RAG kabuki is using the log as evidence that risks are managed when nothing is moving. A tidy list in front of a stakeholder while the team knows none of it is progressing is the failure. Flag every stalled high/high item by name.

### Assumption paralysis

Check the assumptions table for bloat. If it lists every conceivable assumption with no validation plan, that is assumption paralysis. Assumptions should be proportionate — the ones that, if wrong, would change a significant delivery decision. Cut or merge the rest; ensure each survivor has a validation owner and date.

## Step 5: Produce the review summary

Summarise what changed, what was escalated, and what the diagnostics found. This summary is the delivery-manager's input to the weekly status report.

## Rules

- Always record the review date. A review with no date cannot be checked against the next one for item rot.
- Never leave a resolved item in the active tables — archive it. Never delete it — keep the trail.
- Never let a high-probability, high-impact risk sit amber for three reviews without escalation (failure cap).
- A risk that has materialised is re-logged as an issue, not edited in place — the history of "this was a risk we saw coming" is worth keeping.
- The review takes 15 minutes on a healthy log. If it takes much longer, the log has rotted and needs a cleanup pass, not just a review.

## Output Format

```markdown
## RAID Review: [delivery name] — [review date]

### Changes this review
| ID | Category | Change | New status |
|---|---|---|---|
| I-002 | Issue | Staging restored | Resolved → Archived |
| D-009 | Dependency | Slipped to At risk | At risk |

### Escalated
| ID | Why | Escalated to | By when |
|---|---|---|---|

### Diagnostics
| Check | Result | Items flagged |
|---|---|---|
| Item rot | [clean / N flagged] | [IDs unchanged 2+ reviews] |
| Risk-vs-outcome | [clean / N rewritten] | [IDs that were outcomes] |
| RAG kabuki | [clean / N flagged] | [high/high items stalled amber] |
| Assumption paralysis | [clean / trimmed] | [assumptions cut or given owners] |

### Feeds status report
- [The one-line delivery-health read this review produces]
```

## Related skills

- `/delivery-manager:write-raid-log` — captures and structures new items. This skill closes, escalates, and diagnoses them. Run the write skill to add; run this one weekly to keep the log honest.
- `/delivery-manager:write-status-report` — the review summary is the delivery-manager's input to the weekly status. Review the RAID before writing status, never after.
- `/delivery-manager:audit-status-honesty` — uses the reviewed RAID as the evidence base to check reported status against reality.
