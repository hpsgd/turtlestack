---
name: write-status-report
description: "Write a weekly delivery status report with four components — what happened, what is at risk, what decisions are needed, what help is asked for. Assigns honest RAG (red = won't hit target without intervention) and attaches a road-to-green action plan when amber or red. Use for weekly delivery status, programme updates, or any stakeholder status communication."
argument-hint: "[delivery name and reporting period]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Write a status report

Write the delivery status report for $ARGUMENTS. Status reports are where a delivery-manager earns or loses credibility. This skill builds the report from evidence — the RAID review (`review-raid-log`) and the dependency map (`write-dependency-map`) — not from a sense of how things feel. The current report lives at `docs/delivery/status-report.md`; history is kept under `docs/delivery/status/YYYY-MM-DD.md`. The steering pack (`prepare-steering-pack`) abstracts up from these weekly reports.

The most common failure is watermelon reporting: green outside, red inside. This skill exists to prevent it. Honesty is checked by `audit-status-honesty`; this skill builds the report honestly in the first place.

## Step 1: Gather the evidence

Before writing a word, read:

1. The latest RAID review summary (run `review-raid-log` first if it is stale).
2. The current dependency map — any at-risk or blocked items.
3. The previous status report — what was promised last week, so you can report on it specifically.

A status report written without this evidence is a feeling, not a report.

## Step 2: Write the four components

A credible status report has exactly these four components. Each is specific, not vague.

### What happened this week

Specific facts, not "good progress". Name what was completed and what was found.

Good: "Completed user acceptance testing for the payment journey; 3 issues found, 2 fixed, 1 outstanding and tracked as I-004 in RAID."

Bad: "Good progress on payments this week."

### What is at risk

Named risks with owners and actions — not a colour. Pull these from the RAID log.

Good: "Integration with the legacy system is amber: supplier has not responded to our query about the API timeout. Owner: [name]. Action: escalate to account manager by Friday."

Bad: "Integration: amber."

### What decisions are needed

Many status reports are entirely passive — they describe and make no ask. Name each decision as a clear choice with consequences and your recommendation.

Good: "Decision needed: extend beta by two weeks to fix the accessibility issues found, or launch with a known defect and fix in week one. Recommendation: extend."

### What help is being asked for

If you need senior intervention to unblock something, name it, name the person, and name the consequence.

Good: "We need the CTO's office to authorise the additional cloud spend. Without it, performance testing cannot start and beta is at risk."

## Step 3: Assign RAG honestly

The RAG rubric is only useful if the colours mean something fixed:

| Colour | Meaning |
|---|---|
| Red | Will not meet its target without intervention |
| Amber | At risk; I am managing it but may need help |
| Green | On track |

Assign the colour the evidence supports, not the colour that is comfortable. If the RAID log says red and you are about to write green, stop — that is watermelon reporting. Cross-check with the decision checkpoint: reporting green when the RAID log says otherwise requires confirming the honest colour with the team first.

## Step 4: Attach a road to green

Whenever a status is amber or red, attach a specific recovery plan. A colour without a recovery plan is a diagnosis, not delivery management.

```markdown
### Road to green: [item]
| Action | Owner | By when | Moves status to |
|---|---|---|---|
| Escalate API timeout to supplier account manager | [name] | 2026-06-13 | Amber → Green if response received |
```

## Step 5: Write and archive

Write the report to `docs/delivery/status-report.md` and copy it to `docs/delivery/status/[period-ending].md` for history. The historical series is what `forecast-with-reference-class` later draws on for actuals-vs-estimates.

## Rules

- Never report a colour without the four components behind it. The colour is a summary of the evidence, not a substitute for it.
- Never write green when the RAID log or dependency map says otherwise. Watermelon reporting is the failure this skill exists to prevent.
- Never write a passive report. If a decision is needed, name it with options, consequences, and a recommendation.
- "What happened" is specific or it is noise. "Good progress" tells the reader nothing.
- Amber and red always carry a road to green. No exceptions.
- Produce a report stakeholders actually read. An elegant report nobody reads has missed the point — match the format to the audience.

## Output Format

```markdown
## Delivery Status: [name] — week ending [date]

### Overall RAG: [Green / Amber / Red]

### What happened this week
- [Specific completed work and findings]

### What is at risk
| Item | RAG | Owner | Action | RAID ID |
|---|---|---|---|---|

### Decisions needed
| Decision | Options | Recommendation | Owner | By when |
|---|---|---|---|---|

### Help asked for
- [Named ask, named person, consequence if not actioned]

### Road to green (if amber or red)
| Item | Action | Owner | By when | Moves status to |
|---|---|---|---|---|
```
