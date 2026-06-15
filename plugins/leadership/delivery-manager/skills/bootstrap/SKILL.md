---
name: bootstrap
bootstrap-phase: delivery
description: "Bootstrap the delivery documentation structure for a project. Creates docs/delivery/, generates initial RAID log, dependency map, status report and steering pack templates, and writes the delivery-manager fragment of the delivery domain doc (the coordinator assembles docs/delivery/CLAUDE.md). Idempotent — merges missing sections into existing files without overwriting."
argument-hint: "[project name]"
user-invocable: false
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Bootstrap Delivery Documentation

Bootstrap the delivery documentation structure for **$ARGUMENTS**. This sets up the living artifacts the delivery-manager maintains: the RAID log (`write-raid-log`), the dependency map (`write-dependency-map`), the weekly status report (`write-status-report`), and the steering pack (`prepare-steering-pack`). The structure is created once; the skills above keep it alive.

## Step 1: Create the domain directory

```bash
mkdir -p docs/delivery
mkdir -p docs/delivery/_sections
```

Confirm the directory exists before continuing. This is the engagement root for all delivery artifacts.

## Step 2: Create or merge files

For each file below, apply the safe merge pattern:

- If the file does not exist → create it from the template.
- If the file exists → read both, find sections in the template missing from the file, and append only the missing sections with a marker comment `<!-- Merged from delivery-manager bootstrap v0.1.0 -->`. Never overwrite existing content.

### File 1: `docs/delivery/_sections/delivery-manager.md`

`docs/delivery/CLAUDE.md` is **assembled by the coordinator** from the fragments in `_sections/` — no plugin
writes it directly. Write the delivery-manager's contribution as this fragment. It starts at H2 (the coordinator
generates the `# Delivery Domain` H1 and a one-line intro). Create it with this content:

```markdown
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
```

### File 2: `docs/delivery/raid-log.md`

Copy the template from `templates/raid-log.md`. If the file already exists, leave it — the RAID log is a living document and must not be reset.

### File 3: `docs/delivery/dependency-map.md`

Copy the template from `templates/dependency-map.md`. Leave it if it already exists.

### File 4: `docs/delivery/status-report.md`

Copy the template from `templates/status-report.md`. This is the current-week report; history is kept under `docs/delivery/status/YYYY-MM-DD.md`.

```bash
mkdir -p docs/delivery/status
```

## Step 3: Detect the delivery shape

Before finishing, record the delivery shape in `docs/delivery/_sections/delivery-manager.md` under a `## This project` heading:

1. Single team or multiple streams? Multiple streams need a programme-level RAID view.
2. GDS-phased (discovery / alpha / beta / live) or continuous product flow? Phased delivery needs `prepare-service-assessment`.
3. Which tools track work and host reports? Match the tooling-conventions rule if one is installed.

## Rules

- Never overwrite an existing RAID log, dependency map, or status report — these are living artifacts. Merge missing sections only.
- Never create empty placeholder files. If a template has no content yet, do not create the file.
- Idempotent: running bootstrap twice produces no duplicate sections and no lost content.
- Do not create release-engineering files (release checklists, rollback plans) — those belong to the release-manager's bootstrap.

## Output Format

```markdown
## Delivery Bootstrap Complete

### Files created
- docs/delivery/_sections/delivery-manager.md — delivery-manager fragment (coordinator assembles docs/delivery/CLAUDE.md from it)
- docs/delivery/raid-log.md — RAID log (from template)
- docs/delivery/dependency-map.md — dependency map (from template)
- docs/delivery/status-report.md — current-week status report (from template)

### Files merged
- [list any existing files where sections were appended, or "none"]

### Delivery shape detected
- Teams: [single / multiple streams]
- Model: [GDS-phased / continuous]
- Tooling: [work tracking + reporting tools]

### Next steps
- Populate the RAID log with /delivery-manager:write-raid-log
- Run the first weekly status with /delivery-manager:write-status-report
```
