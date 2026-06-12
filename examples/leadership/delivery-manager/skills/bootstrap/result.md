# Bootstrap

Scenario: A delivery manager bootstraps the delivery documentation structure for a new programme. The skill must create `docs/delivery/` with the living artifacts (RAID log, dependency map, status report) from templates, write a domain CLAUDE.md that names the delivery boundaries, detect the delivery shape, and stay idempotent — never overwriting existing living artifacts.

## Prompt

> Use the delivery-manager `bootstrap` skill to set up the delivery documentation structure for the "payments"
> programme. It is a multi-team, continuous-flow product delivery (not GDS-phased). Create everything under
> `docs/delivery/` relative to the current working directory. Respond in the skill's standard output format.
> 
> Proceed without asking — create the structure and report what was created.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Delivery Bootstrap Complete

### Files created
- `docs/delivery/CLAUDE.md` — domain conventions and skill reference (58 lines)
- `docs/delivery/raid-log.md` — RAID log (from template, 39 lines)
- `docs/delivery/dependency-map.md` — dependency map (from template, 28 lines)
- `docs/delivery/status-report.md` — current-week status report (from template, 35 lines)
- `docs/delivery/status/` — directory for weekly status archives

### Files merged
- none

### Delivery shape detected
- **Teams:** Multiple streams
- **Model:** Continuous flow (not GDS-phased)
- **Release cadence:** Rolling releases

### Next steps
- Populate the RAID log with `/delivery-manager:write-raid-log`
- Establish team dependencies with `/delivery-manager:write-dependency-map`
- Run the first weekly status with `/delivery-manager:write-status-report`
- Weekly RAID review cadence begins next week

### Artifacts written

#### `work/docs/delivery/status-report.md`

```
# Delivery Status — payments, week ending [YYYY-MM-DD]

> RAG meanings are fixed: Red = will not meet target without intervention. Amber = at risk, managing it, may need help. Green = on track.
> Amber and red always carry a road to green.

## Overall RAG: [Green / Amber / Red]

## What happened this week

Specific completed work and findings — not "good progress".

- [Specific item: what was completed, what was found]

## What is at risk

Named risks with owners and actions — not a colour.

| Item | RAG | Owner | Action | RAID ID |
|---|---|---|---|---|

## Decisions needed

Each a clear choice with consequences and a recommendation.

| Decision | Options | Recommendation | Owner | By when |
|---|---|---|---|---|

## Help asked for

- [Named ask, named person, consequence if not actioned]

## Road to green (if amber or red)

| Item | Action | Owner | By when | Moves status to |
|---|---|---|---|---|

```

#### `work/docs/delivery/raid-log.md`

```
# RAID Log — payments

> Living governance artifact. Reviewed weekly. Every item has a named owner — never "the team".
> Last reviewed: [pending first review]

## Risks

A risk is a cause, not an outcome. Structure: cause → impact → probability → mitigation.

| ID | Risk (cause) | Impact | Probability | Mitigation | Owner | Review date |
|---|---|---|---|---|---|---|

## Assumptions

Believed true but unconfirmed. Each has a validation owner and a date. Close as Confirmed or Contradicted.

| ID | Assumption | Validation owner | Validate by | Status |
|---|---|---|---|---|

## Issues

Already happening and causing harm. Blocking issues escalate within 48 hours.

| ID | Issue (what happened) | Impact | Resolution plan | Escalate by | Owner | Status |
|---|---|---|---|---|---|---|

## Dependencies

Work or decisions controlled by another team. Each has a named contact and a needed-by date.

| ID | Dependency | Owning team | Contact | Status | Needed by |
|---|---|---|---|---|---|

## Archived

Resolved items, kept for the audit trail.

| ID | Category | Summary | Resolution | Closed |
|---|---|---|---|---|

```

#### `work/docs/delivery/dependency-map.md`

```
# Dependency Map — payments

> Live artifact. Updated weekly and on any status change. Every dependency has a named contact.
> The needed-by date is when this team actually needs it, not when the other team plans to ship it.
> Last updated: [pending first update]

## Team-level view

Both directions: upstream (what this team needs) and downstream (what others need from this team).

| ID | Dependency | Direction | Owning team | Contact | Status | Needed by | Escalation |
|---|---|---|---|---|---|---|---|

## Programme-level view

Cross-team dependency web. Highlight chains where one blocked dependency stalls multiple downstream teams.

| Blocking team | Dependency | Dependent team(s) | Status | Needed by |
|---|---|---|---|---|

## Escalation triggers

| Trigger | Action |
|---|---|
| Status → At risk | Notify the owning-team contact; set an escalation date |
| Status → Blocked | Escalate to coordinator or the relevant lead now |
| Needed-by inside 2 weeks and not On track | Raise in the next scrum of scrums and status report |
| One dependency blocks 2+ downstream teams | Escalate to programme level immediately |

```

#### `work/docs/delivery/CLAUDE.md`

```
# Delivery Domain

This directory holds delivery-management artifacts: the RAID log, dependency map, status reports, steering packs, and service-assessment evidence. These are living documents — the delivery-manager maintains them on a weekly cadence, not once.

## What this domain covers

- RAID log — risks, assumptions, issues, dependencies (governance artifact)
- Dependency map — live team-level and programme-level dependency status
- Status reports — weekly four-component delivery status with honest RAG
- Steering packs — fortnightly or monthly decision-focused governance packs
- Release-readiness packages — handed to the release-manager at the gate
- Service-assessment evidence — GDS alpha/beta/live phase-gate readiness

## What this domain does NOT cover

- Team process, ceremonies, retrospectives, flow coaching — agile coach
- Engineering release gates, deployment, rollback — release-manager
- Backlog, priority, what ships — product-owner / product manager
- Company risk register and compliance frameworks — GRC Lead

## Cadence

| Artifact | Cadence |
|---|---|
| RAID review | Weekly |
| Dependency map | Weekly, or on change |
| Status report | Weekly |
| Steering pack | Fortnightly or monthly |
| Service assessment | At each phase gate |

## Available skills

| Skill | Purpose |
|---|---|
| /delivery-manager:write-raid-log | Create or add to the RAID log |
| /delivery-manager:review-raid-log | Weekly RAID review and rot diagnostic |
| /delivery-manager:write-dependency-map | Maintain the live dependency map |
| /delivery-manager:write-status-report | Weekly delivery status report |
| /delivery-manager:prepare-steering-pack | Steering-committee decision pack |
| /delivery-manager:coordinate-release-readiness | Assemble the release-readiness package |
| /delivery-manager:facilitate-scrum-of-scrums | Run cross-team coordination |
| /delivery-manager:prepare-service-assessment | GDS phase-gate readiness |
| /delivery-manager:forecast-with-reference-class | Reference-class forecasting |
| /delivery-manager:audit-status-honesty | Watermelon-RAG honesty audit |

## Conventions

- Every RAID item has a named owner — never "the team"
- Red status means "will not meet target without intervention"
- Amber and red always carry a road-to-green action plan
- The delivery-manager coordinates release readiness but never executes the release

## This project

**Programme:** payments  
**Delivery model:** Continuous flow (multi-team)  
**Teams:** Multiple streams  
**Phase gate:** Not GDS-phased; continuous product delivery with rolling releases

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 11.0/11.0 (100%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 38414 ms |
| Target cost | $0.1242 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Creates the `docs/delivery/` directory as the engagement root for delivery artifacts | PASS | All four artifact files are listed under `docs/delivery/` in the chat output and artifacts section confirms files written at `work/docs/delivery/`. |
| c2 | Writes `docs/delivery/CLAUDE.md` that states what the delivery domain covers AND what it does NOT cover (team process → agile coach, release gates → release-manager, backlog → product-owner, company risk → GRC Lead) | PASS | CLAUDE.md 'What this domain does NOT cover' names all four: agile coach, release-manager, product-owner/PM, GRC Lead. |
| c3 | Creates the RAID log, dependency map, and status report artifacts from templates — not empty placeholders | PASS | All three files have structured template content: RAID log has five labelled table sections; dependency map has team/programme views + escalation triggers; status report has six named sections. |
| c4 | Records the delivery shape — multiple teams (needs a programme-level RAID view) and continuous flow (not GDS-phased, so no service-assessment emphasis) | PASS | Chat output: 'Teams: Multiple streams', 'Model: Continuous flow (not GDS-phased)'. CLAUDE.md: 'Phase gate: Not GDS-phased'. Dependency map includes 'Programme-level view' section. |
| c5 | States the bootstrap is idempotent — running it again merges missing sections rather than overwriting living artifacts | PASS | Output explicitly includes a 'Files merged: none' section as a distinct category from 'Files created', communicating merge-not-overwrite behavior. |
| c6 | The domain CLAUDE.md or output records the delivery conventions: every RAID item has a named owner, red means "will not meet target without intervention", amber/red carry a road to green | PASS | CLAUDE.md Conventions: 'Every RAID item has a named owner — never "the team"'; 'Red status means "will not meet target without intervention"'; 'Amber and red always carry a road-to-green action plan'. |
| c7 | Does NOT create release-engineering files (release checklists, rollback plans) — those belong to the release-manager's bootstrap | PARTIAL | No release checklists or rollback plans created. CLAUDE.md explicitly excludes 'Engineering release gates, deployment, rollback — release-manager' from domain scope. |
| c8 | Output reports files created (CLAUDE.md, raid-log, dependency-map, status-report) under `docs/delivery/` | PASS | 'Files created' section lists all four: docs/delivery/CLAUDE.md, docs/delivery/raid-log.md, docs/delivery/dependency-map.md, docs/delivery/status-report.md. |
| c9 | Output reports the detected delivery shape — multiple streams + continuous (not GDS-phased) | PASS | 'Delivery shape detected' section: 'Teams: Multiple streams', 'Model: Continuous flow (not GDS-phased)', 'Release cadence: Rolling releases'. |
| c10 | A `docs/delivery/CLAUDE.md` file is actually written to disk and names both what the domain covers and what it does not (the boundary to coach / release-manager / product-owner / GRC) | PASS | Artifact at work/docs/delivery/CLAUDE.md on disk with 'What this domain covers' and 'What this domain does NOT cover' sections naming all four boundary roles. |
| c11 | At least the RAID log and status report artifacts exist on disk under `docs/delivery/` after the run — not just described in chat | PASS | Artifacts section confirms both work/docs/delivery/raid-log.md and work/docs/delivery/status-report.md written to disk with full template content. |
| c12 | Output's next-steps point at write-raid-log and write-status-report rather than leaving the structure empty | PARTIAL | Next steps list: 'Populate the RAID log with /delivery-manager:write-raid-log' and 'Run the first weekly status with /delivery-manager:write-status-report'. |

### Notes

The bootstrap output is comprehensive and correct on all dimensions: all four artifacts written to disk with templated content, CLAUDE.md captures domain boundaries and conventions precisely, delivery shape detected and recorded, and idempotency communicated via the 'Files merged' output section. The skill stays firmly within its lane (no release-engineering files created), earning both PARTIAL-ceiling criteria at their maximum.
