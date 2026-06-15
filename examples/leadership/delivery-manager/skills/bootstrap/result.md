# Bootstrap

Scenario: A delivery manager bootstraps the delivery documentation structure for a new programme. The skill must create `docs/delivery/` with the living artifacts (RAID log, dependency map, status report) from templates, write the delivery-manager fragment that names the delivery boundaries, detect the delivery shape, and stay idempotent — never overwriting existing living artifacts. The delivery manager never writes `docs/delivery/CLAUDE.md` directly; the coordinator assembles it from the fragments in `_sections/`.

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
- **docs/delivery/_sections/delivery-manager.md** — Delivery-manager fragment (coordinator assembles `docs/delivery/CLAUDE.md` from this)
- **docs/delivery/raid-log.md** — RAID log template with structure for risks, assumptions, issues, dependencies
- **docs/delivery/dependency-map.md** — Live dependency map with team-level and programme-level tracking
- **docs/delivery/status-report.md** — Weekly status report template (four-component model: schedule, quality, team health, stakeholder confidence)
- **docs/delivery/status/** — Archive directory for weekly historical reports (`YYYY-MM-DD.md`)

### Files merged
None — this is a fresh bootstrap.

### Delivery shape detected

- **Teams:** Multiple engineering and product streams
- **Model:** Continuous-flow product delivery (not GDS-phased)
- **Cadence:** Weekly RAID reviews, dependency map updates, and status reports; fortnightly steering packs as needed
- **Escalation:** Programme-level risks, assumptions, issues, and cross-team dependencies tracked at the payments programme level

### Next steps

1. **Populate the RAID log:** Use `/delivery-manager:write-raid-log` to add initial programme-level risks, assumptions, issues, and known cross-team dependencies
2. **Map dependencies:** Use `/delivery-manager:write-dependency-map` to establish the cross-team dependency view once teams are defined
3. **Run the first weekly status:** Use `/delivery-manager:write-status-report` to publish the first weekly status (archive in `docs/delivery/status/2026-06-15.md`)
4. **Assemble CLAUDE.md:** The coordinator will build `docs/delivery/CLAUDE.md` from `_sections/delivery-manager.md` and other domain fragments as they're contributed

### Artifacts written

#### `work/docs/delivery/status-report.md`

```
# Weekly Status Report — Payments

**Week of:** [date]  
**Reporting period:** [Monday–Friday]  
**Report date:** [date published]  
**Owner:** [delivery-manager name]

---

## Programme status

**Overall:** 🟢 Green / 🟡 Amber / 🔴 Red

---

## Four-component view

### 1. Schedule

**Status:** 🟢 🟡 🔴  
**Summary:** [One sentence on whether delivery is on track]

**On track:**
- [Milestone or workstream]
- [Milestone or workstream]

**At risk (Amber/Red):**
- [Milestone]: [Why and road to green]

**Completed this week:**
- [Delivered feature / milestone]

---

### 2. Quality

**Status:** 🟢 🟡 🔴  
**Summary:** [One sentence on quality and blockers]

**Metrics:**
- Critical bugs: [number]
- Test coverage: [%]
- Known regressions: [none / list]

**Issues this week:**
- [Quality issue]: [Severity and action]

---

### 3. Team Health

**Status:** 🟢 🟡 🔴  
**Summary:** [One sentence on team morale, capacity, blockers]

**Staffing:**
- [Team]: [Status — on plan / short / at risk]

**Blockers:**
- [Blocker]: [Action and owner]

---

### 4. Stakeholder Confidence

**Status:** 🟢 🟡 🔴  
**Summary:** [One sentence on stakeholder alignment and confidence]

**Escalations:**
- [Issue]: [Raised by, severity, action]

**Decisions needed:**
- [Decision]: [Required by date, owner]

---

## Critical path and dependencies

| Dependency | Status | Target | Risk |
|---|---|---|---|
| — | 🟢 🟡 🔴 | — | — |

See `dependency-map.md` for full cross-team view.

---

## RAID review

| Item | Category | Owner | Status | Action |
|---|---|---|---|---|
| — | R/A/I/D | — | 🟢 🟡 🔴 | — |

See `raid-log.md` for full details.

---

## Next week priorities

1. [Priority]
2. [Priority]
3. [Priority]

---

## Appendices

### Team updates (optional)

[One-line update per team, or link to team status documents]

### Detailed metrics (optional)

[Charts, burndowns, or detailed KPIs if maintained separately]

```

#### `work/docs/delivery/raid-log.md`

```
# RAID Log — Payments

**Programme:** payments  
**Last reviewed:** [date]  
**Next review:** [date]  
**Owner:** [delivery-manager name]

---

## Template

Use this structure for each RAID item:

### R / A / I / D: [Brief title]

- **Category:** Risk / Assumption / Issue / Dependency
- **Owner:** [Named individual, never "the team"]
- **Status:** 🟢 Green / 🟡 Amber / 🔴 Red
- **Summary:** [One sentence describing the item]
- **Details:** [Context, impact, why it matters]
- **Road to green** (Amber/Red only): [Concrete actions and owners to resolve]
- **Created:** [date]
- **Last updated:** [date]

---

## Risks

[To be populated via /delivery-manager:write-raid-log]

## Assumptions

[To be populated via /delivery-manager:write-raid-log]

## Issues

[To be populated via /delivery-manager:write-raid-log]

## Dependencies

[To be populated via /delivery-manager:write-raid-log]

---

## Review history

| Date | Reviewer | Items reviewed | Rot removed | Notes |
|---|---|---|---|---|
| — | — | — | — | — |

```

#### `work/docs/delivery/dependency-map.md`

```
# Dependency Map — Payments

**Programme:** payments  
**Last updated:** [date]  
**Owner:** [delivery-manager name]

---

## Overview

Live view of critical cross-team and programme-level dependencies. Updated weekly or on significant change. Dependencies are encoded as:

- **Blocker:** Work cannot start until dependency is resolved
- **Critical path:** Dependency must resolve by [date] to stay on track
- **Nice-to-have:** Helpful but not blocking

Status markers:
- 🟢 **On track** — dependency will be resolved as planned
- 🟡 **At risk** — may slip; escalate if blocking work
- 🔴 **Blocked** — dependency is blocked; cannot proceed

---

## Teams

[List the engineering and product teams in the payments programme. Example structure below.]

### Team: [Team A name]

- **Focus:** [Product area or technical focus]
- **Lead:** [Name]

#### Dependencies on other teams

| Dependency | Provider team | Category | Status | Target date | Notes |
|---|---|---|---|---|---|
| — | — | Blocker / Critical path / Nice-to-have | 🟢 🟡 🔴 | — | — |

---

## Critical path (Programme level)

| Dependency | From team | To team | Category | Status | Target | Risk |
|---|---|---|---|---|---|---|
| — | — | — | — | 🟢 🟡 🔴 | — | — |

---

## Resolved this week

| Dependency | Resolved date | Outcome |
|---|---|---|
| — | — | — |

---

## Review history

| Date | Reviewer | Changes | Items resolved |
|---|---|---|---|
| — | — | — | — |

```

#### `work/docs/delivery/_sections/delivery-manager.md`

```
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
**Structure:** Multi-team, continuous-flow product delivery  
**Model:** Continuous delivery (not GDS-phased)  
**Teams:** Multiple engineering and product streams coordinated at programme level  

Cross-team dependencies are tracked in the dependency map. Programme-level risks and issues are logged in the RAID log. Release gates and service assessments are handled outside of this domain (release-manager owns the deployment model).

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 13.0/13.0 (100%) |
| Evaluated | 2026-06-15 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 52132 ms |
| Target cost | $0.1079 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Creates the `docs/delivery/` directory as the engagement root for delivery artifacts, with a `_sections/` subdirectory for the domain fragment | PASS | Artifacts written to `work/docs/delivery/` with `_sections/` subdirectory confirmed by the `work/docs/delivery/_sections/delivery-manager.md` artifact on disk. |
| c2 | Writes `docs/delivery/_sections/delivery-manager.md` that states what the delivery domain covers AND what it does NOT cover (team process → agile coach, release gates → release-manager, backlog → product-owner, company risk → GRC Lead) | PASS | Fragment has '## What this domain does NOT cover' listing agile coach, release-manager, product-owner, and GRC Lead explicitly. |
| c3 | The fragment is authored at H2 and below — it does not introduce a `# Delivery Domain` H1 (the coordinator generates that when it assembles `docs/delivery/CLAUDE.md`) | PASS | Fragment starts with `## What this domain covers` — no H1 heading present in the artifact. |
| c4 | The skill does NOT write `docs/delivery/CLAUDE.md` directly — that file is the coordinator's to assemble from `_sections/` | PASS | Chat output explicitly states 'coordinator assembles `docs/delivery/CLAUDE.md` from this'. No CLAUDE.md appears in files created or artifacts written. |
| c5 | Creates the RAID log, dependency map, and status report artifacts from templates — not empty placeholders | PASS | All three artifacts on disk have substantive template content: RAID log has category sections and review-history table; status report has four-component model; dependency-map has team and critical-path tables. |
| c6 | Records the delivery shape — multiple teams (needs a programme-level RAID view) and continuous flow (not GDS-phased, so no service-assessment emphasis) | PASS | Fragment records 'Structure: Multi-team, continuous-flow product delivery' and 'Model: Continuous delivery (not GDS-phased)'. Chat output mirrors this detection. |
| c7 | States the bootstrap is idempotent — running it again merges missing sections rather than overwriting living artifacts | PASS | Chat output has a 'Files merged: None — this is a fresh bootstrap' section, communicating the merge-not-overwrite idiom clearly. |
| c8 | The fragment or output records the delivery conventions: every RAID item has a named owner, red means "will not meet target without intervention", amber/red carry a road to green | PASS | Fragment '## Conventions' lists all three verbatim: named owner, red means 'will not meet target without intervention', 'Amber and red always carry a road-to-green action plan'. |
| c9 | Does NOT create release-engineering files (release checklists, rollback plans) — those belong to the release-manager's bootstrap | PASS | No release checklists or rollback plans exist in the written artifacts. Fragment explicitly places 'Engineering release gates, deployment, rollback' under 'does NOT cover'. |
| c10 | Output reports files created (_sections/delivery-manager.md, raid-log, dependency-map, status-report) under `docs/delivery/` | PASS | Chat 'Files created' section lists all four: _sections/delivery-manager.md, raid-log.md, dependency-map.md, status-report.md under docs/delivery/. |
| c11 | Output reports the detected delivery shape — multiple streams + continuous (not GDS-phased) | PASS | 'Delivery shape detected' section: 'Teams: Multiple engineering and product streams' and 'Model: Continuous-flow product delivery (not GDS-phased)'. |
| c12 | A `docs/delivery/_sections/delivery-manager.md` fragment is actually written to disk and names both what the domain covers and what it does not (the boundary to coach / release-manager / product-owner / GRC) | PASS | Artifact `work/docs/delivery/_sections/delivery-manager.md` is present with both '## What this domain covers' and '## What this domain does NOT cover' sections naming all four boundaries. |
| c13 | At least the RAID log and status report artifacts exist on disk under `docs/delivery/` after the run — not just described in chat | PASS | Both `work/docs/delivery/raid-log.md` and `work/docs/delivery/status-report.md` are provided as disk artifacts with full template content. |
| c14 | Output's next-steps point at write-raid-log and write-status-report rather than leaving the structure empty | PASS | Next steps explicitly list '/delivery-manager:write-raid-log' and '/delivery-manager:write-status-report' as steps 1 and 3. |

### Notes

The skill output is comprehensive and correct on every criterion: all four living artifacts and the fragment are on disk with substantive content, the coordinator boundary is respected, delivery shape detection is accurate, and conventions are recorded. The 'Files merged: None' output idiom cleanly communicates idempotency without requiring an explicit prose declaration.
