# Bootstrap

Scenario: A coach is onboarding to a new team and needs the `docs/coaching/` structure created from scratch — the agile-coach fragment of the coaching domain doc, a working-agreements starter, and a DoD starter — without the skill authoring the team's actual agreements or DoD content. The coach never writes `docs/coaching/CLAUDE.md` directly; the coordinator assembles it from the fragments in `_sections/`.

## Prompt

> Use the agile-coach `bootstrap` skill to bootstrap the agile-coaching documentation structure for the "billing" team. Create the structure under `docs/coaching/` in the current working directory (a fresh git repo — nothing exists there yet). Respond in the skill's standard manifest output format.
> 
> Proceed without asking — there is no existing coaching documentation; this is a clean bootstrap.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Coaching Bootstrap Complete

### Files created
- `docs/coaching/_sections/agile-coach.md` — agile-coach fragment (coordinator assembles `docs/coaching/CLAUDE.md` from it)
- `docs/coaching/working-agreements.md` — working-agreements starter (team-authored template)
- `docs/coaching/definition-of-done.md` — DoD starter (team-authored template)

### Directories created
- `docs/coaching/retrospectives/` — for per-retro output files
- `docs/coaching/health/` — for periodic team-health scans

### Files merged
- (none — clean bootstrap)

### Next steps
- Run `/agile-coach:design-working-agreements` to facilitate the billing team authoring its agreements
- Run `/agile-coach:coach-definition-of-done` to facilitate the billing team authoring its Definition of Done
- Run `/agile-coach:team-health-scan` to establish a psychological-safety baseline
- Record the billing team's method and ceremony cadence in `docs/coaching/_sections/agile-coach.md`

### Artifacts written

#### `work/docs/coaching/working-agreements.md`

```
# Working Agreements — billing

> The team authors this. The coach facilitates. Every agreement is specific, testable, and behavioural — not a value
> statement. Keep the set small: a short list the team lives by beats a long list it forgot.

## How these were made

- Authored by: [the team — who was present]
- Date: [YYYY-MM-DD]
- Friction points that prompted them: [what the team named]

## Agreements

> Each agreement names an observable behaviour. Test: can you tell whether it was followed?

1. [Specific, testable agreement — e.g. "Standup starts at 9:30; we start without latecomers."]
2. [e.g. "We pair on anything touching auth."]
3. [e.g. "No laptops in retrospectives unless you're the scribe."]
4. [...]

## Review cadence

- Revisited: [when — a standing retro item, or a trigger like a new joiner or recurring friction]
- Last reviewed: [YYYY-MM-DD]

## Not in scope here

Quality criteria (what "done" means) live in the Definition of Done, not here. Working agreements govern how the
team behaves together; the DoD governs when work is complete.

```

#### `work/docs/coaching/definition-of-done.md`

```
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

#### `work/docs/coaching/_sections/agile-coach.md`

```
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

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 13.0/13.0 (100%) |
| Evaluated | 2026-06-15 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 35709 ms |
| Target cost | $0.0716 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Creates the `docs/coaching/` directory with a `retrospectives/` subdirectory for per-retro outputs and a `_sections/` subdirectory for the domain fragment | PASS | Chat response: 'Directories created: docs/coaching/retrospectives/' and artifact at work/docs/coaching/_sections/ confirms _sections/ exists. |
| c2 | Creates `docs/coaching/_sections/agile-coach.md` as the agile-coach fragment naming the coach-owns-structure / team-owns-content boundary | PASS | agile-coach.md '## The coach's boundary' section: 'The coach owns the team's internal process... The Definition of Done is owned by the team, not handed down by management.' |
| c3 | The fragment is authored at H2 and below — it does not introduce a `# Coaching Domain` H1 (the coordinator generates that when it assembles `docs/coaching/CLAUDE.md`) | PASS | agile-coach.md starts with '## What this domain covers' — no H1 heading present in the artifact. |
| c4 | The skill does NOT write `docs/coaching/CLAUDE.md` directly — that file is the coordinator's to assemble from `_sections/` | PASS | Only three artifacts written: working-agreements.md, definition-of-done.md, _sections/agile-coach.md. No CLAUDE.md artifact present. |
| c5 | The fragment lists the available agile-coach skills as a reference for a future coach orienting to the repo | PASS | agile-coach.md '## Available skills' table lists 12 skills with purpose column, e.g. '/agile-coach:facilitate-retrospective', '/agile-coach:team-health-scan'. |
| c6 | Creates a working-agreements starter file and a definition-of-done starter file under `docs/coaching/` | PASS | Artifacts confirm work/docs/coaching/working-agreements.md and work/docs/coaching/definition-of-done.md both written. |
| c7 | The skill does NOT author actual working agreements or DoD criteria — it creates structure and starter prompts only, leaving the team to fill them in | PASS | working-agreements.md uses '[Specific, testable agreement — e.g. …]' placeholders; DoD uses '- [ ] [Specific, testable item — e.g. …]' stubs. No actual content invented. |
| c8 | Output is a bootstrap manifest listing files created (and any merged), plus next steps pointing to design-working-agreements and team-health-scan | PASS | Chat response has '### Files created', '### Files merged (none)', '### Next steps' with /agile-coach:design-working-agreements and /agile-coach:team-health-scan. |
| c9 | The DoD starter and the fragment note that content is team-owned and specific/testable, not handed down by management | PARTIAL | DoD: 'The team owns this… Make every item specific and testable.' Fragment: 'The Definition of Done is owned by the team, not handed down by management.' |
| c10 | Output names the files it created at their paths under `docs/coaching/` — `_sections/agile-coach.md`, working-agreements, definition-of-done — not just a vague "done" | PASS | Chat lists exact paths: 'docs/coaching/_sections/agile-coach.md', 'docs/coaching/working-agreements.md', 'docs/coaching/definition-of-done.md'. |
| c11 | The created `docs/coaching/_sections/agile-coach.md` records the convention that every retro produces action items with an owner and a due sprint | PASS | agile-coach.md '## Conventions': 'Every retro produces action items with an owner and a due sprint — no exceptions.' |
| c12 | The created files contain placeholder/template content (e.g. bracketed prompts, checkbox stubs) rather than invented team-specific agreements or quality criteria | PASS | All three artifacts use bracketed prompts '[…]', checkbox stubs '- [ ] [Specific, testable item]', and table placeholders '[Scrum / Kanban / Scrumban]'. |
| c13 | Output's next-steps point the user at the skills that fill the structure (design-working-agreements, team-health-scan) rather than declaring the team's process complete | PASS | Next steps list '/agile-coach:design-working-agreements', '/agile-coach:coach-definition-of-done', '/agile-coach:team-health-scan' — no claim that process is complete. |
| c14 | Output reflects an idempotent / safe-merge intent — it states it would merge missing sections rather than overwrite if files already existed | PARTIAL | '### Files merged: (none — clean bootstrap)' implies merge awareness in the manifest structure, but no explicit statement of overwrite-vs-merge behavior for existing files. |

### Notes

The skill output is comprehensive and well-structured, satisfying all criteria fully within their ceilings. The only nuance is c14, where the 'Files merged: none' section implies idempotent intent but stops short of explicitly describing merge behavior for existing files.
