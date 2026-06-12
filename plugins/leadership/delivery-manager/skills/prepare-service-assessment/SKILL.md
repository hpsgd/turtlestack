---
name: prepare-service-assessment
description: "Prepare for a GDS service assessment — the alpha/beta/live phase gate. Compiles evidence against the GOV.UK Service Standard, runs a mock assessment, and tracks remediation of gaps. Use when a digital service approaches a phase gate (end of alpha, end of private/public beta) and needs to demonstrate it meets the Service Standard."
argument-hint: "[service name and the phase gate: alpha / beta / live]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Prepare a service assessment

Prepare the service assessment for $ARGUMENTS. Service assessments are panels that check whether a service meets the [GOV.UK Service Standard](https://www.gov.uk/service-manual/service-standard) before it can move from alpha to beta, or beta to live. The panel is independent of the delivery team. The delivery-manager does not sit the assessment alone — everyone in the team is responsible for meeting the standard — but the delivery-manager coordinates the preparation: booking it, compiling evidence, running the mock, and tracking remediation. Evidence is written to `docs/delivery/service-assessment/[phase]/`.

The phase gates control budget and permission to proceed, so a failed assessment is a real delivery blocker. The job is to walk into the assessment with the evidence compiled and the team able to speak to every criterion.

## Step 1: Confirm the phase and the standard

Confirm which gate this is — end of alpha, end of private beta, end of public beta, or the path to live. Read the current [Service Standard](https://www.gov.uk/service-manual/service-standard) (14 points) and the [service assessment guidance](https://www.gov.uk/service-manual/service-assessments). The expectations differ by phase: alpha assessments focus on whether the team has tested the right things with prototypes; beta assessments expect a service built to production quality with measurable KPIs.

## Step 2: Compile evidence against each criterion

For each point of the Service Standard, compile the evidence the team will present:

```markdown
| # | Service Standard point | Evidence | Owner | Status |
|---|---|---|---|---|
| 1 | Understand users and their needs | User research findings, personas, journey maps | UX researcher | Ready |
| 2 | Solve a whole problem for users | End-to-end journey across channels | Product manager | Gap |
```

Evidence is concrete — research outputs, prototypes, KPI dashboards, accessibility audits, architecture decisions — not assertions. A point with no evidence is a gap, regardless of how confident the team feels.

## Step 3: Confirm beta KPIs are tracked (beta and live gates)

For beta and live assessments, the Service Manual requires measurable KPIs. Confirm each is tracked and reported:

| KPI | Tracked? | Current value |
|---|---|---|
| User satisfaction | Yes / No | [value] |
| Completion rate | Yes / No | [value] |
| Cost per transaction | Yes / No | [value] |
| Take-up / digital take-up | Yes / No | [value] |

A beta assessment without these KPIs tracked is not ready. The delivery-manager is typically the person who ensures they are in place.

## Step 4: Run a mock assessment

Run a mock assessment before the real one. Walk each Service Standard point as the panel would: ask the hard question, hear the team's answer, and judge whether the evidence stands. The mock surfaces the gaps while there is still time to close them. Record where the team's answers were thin or the evidence was missing.

## Step 5: Track remediation

Every gap from Steps 2-4 becomes a remediation item with an owner and a date, tracked through to the assessment:

```markdown
| Gap | Service Standard point | Remediation | Owner | By when | Status |
|---|---|---|---|---|---|
| No end-to-end journey across channels | 2 | Map the offline path; add to the prototype | Product manager | 2026-06-25 | Open |
```

Do not declare the assessment ready while unremediated gaps remain on points the panel will test (decision checkpoint). Re-run the relevant part of the mock after remediation.

## Rules

- The delivery-manager coordinates the assessment; the whole team is responsible for meeting the standard. Do not present it as a one-person exercise.
- Evidence is concrete or it is a gap. Confidence is not evidence.
- Beta and live assessments need the KPIs tracked and reported. Without them, the service is not ready for the gate.
- Always run a mock before the real assessment. The mock is where gaps get found cheaply.
- Every gap gets an owner and a date. A gap with no remediation owner will still be open on assessment day.
- Never declare ready with unremediated gaps on points the panel will test. A failed assessment blocks the phase gate and the budget.

## Output Format

```markdown
## Service Assessment Prep: [service] — [phase] gate

### Evidence against the Service Standard
| # | Point | Evidence | Owner | Status (Ready / Gap) |
|---|---|---|---|---|

### Beta KPIs (beta / live gates)
| KPI | Tracked | Value |
|---|---|---|

### Mock assessment findings
| Point | Team's answer | Verdict (Stands / Thin / Missing) |
|---|---|---|

### Remediation tracker
| Gap | Point | Remediation | Owner | By when | Status |
|---|---|---|---|---|---|

### Readiness verdict: [Ready for assessment / Not ready — N gaps open]
```

## Related skills

- `/delivery-manager:write-raid-log` — open remediation gaps that threaten the gate are tracked as risks and issues in the RAID log, not only in the assessment tracker.
- `/delivery-manager:prepare-steering-pack` — a phase gate is a steering-level event. The assessment readiness verdict and any decision to proceed, delay, or remediate belongs in the steering pack.
