---
name: bootstrap
description: "Bootstrap the agile-coaching documentation structure for a project. Creates docs/coaching/, generates initial working-agreements and retrospective templates, and writes a domain CLAUDE.md. Idempotent — merges missing sections into existing files without overwriting."
argument-hint: "[team or project name]"
user-invocable: false
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Bootstrap Coaching Documentation

Bootstrap the agile-coaching documentation structure for **$ARGUMENTS**.

## Step 1: Check and create domain directory

```bash
mkdir -p docs/coaching/retrospectives
mkdir -p docs/coaching/health
```

`docs/coaching/` holds the team's process artifacts: working agreements, Definition of Done, retrospective
outputs, and team-health scans. `retrospectives/` holds one file per retro; `health/` holds periodic scans.

## Step 2: Create or merge files

For each file below, apply the safe merge pattern:

- If the file does not exist → create from the template.
- If the file exists → read both, find sections in the template missing from the file, append the missing
  sections with a `<!-- Merged from agile-coach bootstrap v0.1.0 -->` marker. Never overwrite existing content.

### File 1: `docs/coaching/CLAUDE.md`

Create with this content:

```markdown
# Coaching Domain

This directory holds the team's process artifacts: working agreements, Definition of Done, retrospective
outputs, and team-health scans. The agile coach owns the structure; the team owns the content.

## What this domain covers

- **Working agreements** — how the team operates (norms, communication, meeting behaviour)
- **Definition of Done** — the team's quality contract for any increment
- **Retrospectives** — one output file per retro, with action items routed to the next sprint backlog
- **Team-health scans** — periodic psychological-safety and norms reviews
- **Flow metrics** — the team reads its own cycle time, throughput, and work-item age

## Method in use

State the team's method here: Scrum, Kanban, Scrumban, or ad hoc. Record the ceremony cadence and board
configuration so a new coach can orient quickly.

| Aspect | Value |
|--------|-------|
| Method | [Scrum / Kanban / Scrumban] |
| Sprint length | [if Scrum/Scrumban] |
| WIP limits | [if Kanban/Scrumban] |
| Ceremonies | [list with cadence] |

## Conventions

- One retrospective output file per retro, named `retrospectives/YYYY-MM-DD.md`
- Every retro produces action items with an owner and a due sprint — no exceptions
- Working agreements are team-generated, specific, and testable — reviewed when they stop working
- The Definition of Done is owned by the team, not handed down by management
- Team-health scans are anonymous; raw responses are never attributed

## The coach's boundary

The coach owns the team's internal process. The delivery manager owns delivery (external coordination, RAID,
status). The coach facilitates retrospectives, planning, and working agreements; the product owner runs
refinement and the sprint review. The coach coaches flow metrics; the delivery manager only reads them.

## Available skills

| Skill | Purpose |
|-------|---------|
| `/agile-coach:facilitate-retrospective` | Run a Derby/Larsen five-phase retrospective |
| `/agile-coach:facilitate-sprint-planning` | Facilitate Sprint Planning's three topics |
| `/agile-coach:facilitate-sprint-review` | Facilitate the sprint review as a working session |
| `/agile-coach:audit-ceremonies` | Observe a cycle and name ceremony anti-patterns |
| `/agile-coach:team-health-scan` | Run a psychological-safety and norms scan |
| `/agile-coach:design-working-agreements` | Facilitate the team to author working agreements |
| `/agile-coach:coach-flow-metrics` | Teach the team to read its own flow data |
| `/agile-coach:audit-anti-patterns` | Diagnose retro, Zombie, and Dark Scrum anti-patterns |
| `/agile-coach:coach-definition-of-done` | Facilitate the team to author its own DoD |
| `/agile-coach:coach-kanban-method` | Coach the six Kanban practices |
| `/agile-coach:assess-team-topology` | Assess team type and interaction modes |
| `/agile-coach:audit-scaling-framework` | Help a team pick or reject a scaling framework |
```

### File 2: `docs/coaching/working-agreements.md`

Create from the working-agreements template at `templates/working-agreements.md` in this plugin.

### File 3: `docs/coaching/definition-of-done.md`

Create with this starter content:

```markdown
# Definition of Done

> The team owns this. It is the team's quality contract for any increment. Make every item specific and testable.

## Applies to

[State the work types this DoD covers — e.g. user-facing features, API changes, infrastructure.]

## Done means

- [ ] [Specific, testable item — e.g. "unit tests written, line coverage >= 80%"]
- [ ] [Specific, testable item — e.g. "merged to main behind a feature flag"]
- [ ] [Specific, testable item]

## Review cadence

Reviewed in the retrospective when an item proves vague or is repeatedly skipped.
```

## Step 3: Return manifest

After creating or merging all files, output a summary:

```
## Coaching Bootstrap Complete

### Files created
- `docs/coaching/CLAUDE.md` — domain conventions and skill reference
- `docs/coaching/working-agreements.md` — working-agreements starter
- `docs/coaching/definition-of-done.md` — DoD starter

### Files merged
- (list any existing files where sections were appended)

### Next steps
- Run `/agile-coach:design-working-agreements` to facilitate the team authoring its agreements
- Run `/agile-coach:team-health-scan` to establish a safety baseline
- Record the team's method in `docs/coaching/CLAUDE.md`
```

## Rules

- Always merge, never overwrite. Existing team content is the source of truth — append missing sections with the
  merge marker, don't replace.
- Never author the working agreements or DoD content yourself. Bootstrap creates the *structure* and starter
  prompts; the team fills them in via the `design-working-agreements` and `coach-definition-of-done` skills.
- Don't create a directory tree deeper than needed. If `docs/coaching/` already exists with a richer structure,
  respect it.

## Output Format

The manifest in Step 3 is the output. List files created, files merged, and next steps. No prose summary beyond it.
