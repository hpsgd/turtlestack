# Audit Ceremonies

Scenario: A coach is asked to audit a team's ceremonies after a full sprint cycle. Observation notes and the last two retrospective outputs are on disk. The skill must observe across the cycle, name specific ceremony anti-patterns with cited evidence, record good signals too, distinguish symptom from cause, and prioritise coaching actions.

## Prompt

> Use the agile-coach `audit-ceremonies` skill to audit the "billing" team's ceremonies. The observation notes for one full sprint cycle are at `docs/coaching/ceremony-notes.md` and the last two retrospective outputs are in `docs/coaching/retrospectives/` (relative to the current working directory). Read them and produce the ceremony audit in the skill's standard format. Write the audit to `docs/coaching/` in the current working directory.
> 
> Proceed without asking — read the records and produce the audit.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Audit complete. I've produced the ceremony audit for the billing team based on sprint 14 observations and the two retrospective outputs (2026-05-15, 2026-05-29).

**Key findings:**

- **Secretary coach + status theatre standup**: Team can't run the standup without the SM (skipped when absent Wed). Blockers are named but not owned ("staging credentials" repeated Tue/Thu, never picked up).

- **Task-assignment planning**: PO walks in with pre-assigned tickets; developers don't negotiate. No Sprint Goal written; when asked, team gives three different answers.

- **Broken retrospective**: Jumps from "what went wrong" to actions with no insight phase. Same two items ("improve test coverage", "reduce interruptions") recur identically across both retros with no owner or due date.

- **Absent refinement**: Ad hoc, incomplete. Items reach planning unrefined (two had no acceptance criteria).

**Root cause:** The team has not been coached to self-manage. They're waiting to be told what to do and by whom, rather than owning the plan, the goal, and the blockers.

**Recommended coaching path:** Start with the retrospective (to close the feedback loop and establish ownership norms), then design working agreements (standup ownership, blocker escalation, action item routing), then move to planning and refinement. The standup will self-repair once the team owns their blockers.

The audit is written to `docs/coaching/audit-ceremonies-billing-sprint14.md`.

### Artifacts written

#### `work/docs/coaching/ceremony-notes.md`

```
# Billing team — ceremony observation notes (sprint 14)

Observer notes captured across one full sprint cycle. Raw, unanalysed.

## Daily Scrum

- Held daily at 9:30, 15 min, run by the Scrum Master every day.
- Each developer speaks in turn, addressing their update to the Scrum Master and the product owner who both attend.
- The Scrum Master calls on each person by name: "Priya, you're next."
- On Tue and Thu a developer said "still blocked on the staging credentials" — the same blocker, named both days, not picked up by anyone.
- No re-planning of the sprint happens in the standup; it's a round of status.
- When the Scrum Master was away on Wed, the team milled about for ten minutes and skipped the standup.

## Sprint Planning (sprint 14)

- Product owner walked in with tickets pre-assigned: "Sam takes the refund endpoint, Priya takes the reconciliation job."
- Developers did not push back on the assignment or the volume.
- No Sprint Goal was written. Asked at the end "what's the goal this sprint?", three of six developers gave different answers; two shrugged.
- 28 points pulled in; the team finished 17 last sprint and 19 the sprint before.

## Refinement

- No standing refinement. Items are refined ad hoc the day before planning, often incompletely.
- Two items reached planning with no acceptance criteria.

## Sprint Review

- 18-slide deck presented to the head of product, who did most of the talking.
- Team showed screenshots, not running software, for the reconciliation feature.
- The product backlog was not changed during or after the review.

## Retrospective

- Format: Start/Stop/Continue, same as the last five sprints.
- Jumped straight from "what went wrong" to "let's do X" with no discussion of why.
- Two action items produced: "improve test coverage" and "reduce interruptions" — identical to the previous two retros.
- Neither action item had an owner or a due date.

```

#### `work/docs/coaching/audit-ceremonies-billing-sprint14.md`

```
---
title: Ceremony Audit — billing team
date: 2026-06-12
author: agile-coach
category: Coaching
---

## Cycle observed

Sprint 14 (one full cycle). All ceremonies observed: Daily Scrum (daily, 9:30am, 15 min), Sprint Planning (pre-sprint), Refinement (ad hoc), Sprint Review (post-sprint, 18-slide deck), Retrospective (post-sprint, Start/Stop/Continue format). Retrospective outputs from Sprint 13 and 14 reviewed.

## Anti-patterns found

| Event | Anti-pattern | Evidence | Likely root cause |
|-------|--------------|----------|-------------------|
| Daily Scrum | Secretary coach | SM calls on people by name; team milled about and skipped standup when SM absent on Wed (sprint 14:Wed). Team cannot self-run the event. | Team has not been coached to self-manage. |
| Daily Scrum | Status theatre | Developers report to SM and PO (addressees, not peers). Same blocker ("staging credentials") named Tue/Thu, not picked up by team. No replanning happens; it's a round-robin status report. | Team has not been coached to own blockers or drive towards the Sprint Goal. |
| Sprint Planning | Task-assignment | PO walked in with pre-assigned tickets ("Sam takes the refund endpoint, Priya takes the reconciliation job"). Developers did not push back on assignment or volume (sprint 14). | Team has not been coached to own the forecast or negotiate scope. |
| Sprint Planning | No goal | No Sprint Goal written. When asked "what's the goal this sprint?", three of six developers gave different answers; two shrugged (sprint 14). | Team has not been coached to generate and internalise the Sprint Goal. |
| Refinement | Absent or batched | No standing refinement. Items are refined ad hoc the day before planning, often incompletely. Two items reached planning with no acceptance criteria (sprint 14). | Refinement is not treated as a continuous discipline; team has not established working agreements around readiness. |
| Sprint Review | Demo theatre | One-way presentation (18-slide deck) to head of product, who did most of the talking. Team showed screenshots, not running software. Product backlog was not changed during or after the review (sprint 14). | Sprint Review is treated as a reporting ceremony, not a feedback/adaptation opportunity. |
| Retrospective | Wheel of Fortune | Jumps from "what went wrong" to "let's do X" with no discussion of why or insight phase. Same two action items recur: "improve test coverage" and "reduce interruptions" appear in both sprint 13 (2026-05-15) and sprint 14 (2026-05-29) retros. | Insight phase is being skipped; action items are not being followed through or completed. |
| Retrospective | Status theatre (action items) | Two action items produced each retro, but neither has an owner or a due date. (Sprint 13: 2026-05-15 and sprint 14: 2026-05-29). | Team has not been coached to own action items; accountability and follow-through are absent. |

## Root-cause grouping

**Root cause 1: Team has not been coached to self-manage**
- Secretary coach (standup can't run without SM)
- Status theatre (blockers named, not owned; developers report to authority, not to each other)
- Task-assignment (developers accept PO's plan, don't negotiate)
- No goal (team can't articulate or own the Sprint Goal)

This is the deepest issue. The team is waiting to be told what to do and by whom, rather than self-organising around a shared outcome.

**Root cause 2: Refinement discipline is absent**
- No standing refinement; ad hoc, incomplete
- Items reach planning unrefined
- Compounds task-assignment anti-pattern: unrefined backlog → PO assigns tasks → team accepts

**Root cause 3: Action items are ghosted**
- No owner or due date assigned
- Same items recur across two consecutive retros (identical language in both retros)
- Indicates the insight phase is being skipped (jumping from problem to action without understanding why or who will own the fix)

**Root cause 4: Retrospective format has decayed**
- Wheel of Fortune (data → action, no insight)
- Format has been the same for five consecutive sprints with no variance or adaptation
- Signals that the retro is not delivering value and the team has stopped investing in it

## Prioritised coaching actions

1. **Facilitate retrospective** (use `agile-coach:facilitate-retrospective`) — addresses root causes 3 and 4. The retro is broken: the team is jumping from problem to action without insight, and action items are ghosted (no owner, no due date). The recurrence of identical items across two sprints is the loudest signal that the feedback loop is not closing. A retro that doesn't produce owned, routed action items is just venting. **This is safety-critical**: until the team can surface and own what's not working, self-management cannot start.

2. **Design working agreements** (use `agile-coach:design-working-agreements`) — addresses root cause 1 (self-management). Focus on:
   - Who runs the standup (should be the team, not the SM)
   - How blockers are owned (named in standup → owned in standup, not escalated)
   - How the Sprint Goal is generated and owned (team's goal, not PO's assignment)
   - How action items are routed (owner + due date, tracked in the sprint backlog, not ghosted)

3. **Coach continuous refinement** (use `agile-coach:coach-definition-of-done` to establish refinement DoD, or `agile-coach:design-working-agreements` to cover refinement discipline) — addresses root cause 2. Establish that items must reach planning with acceptance criteria and technical unknowns surfaced. Refinement should be continuous, not a dreaded standalone meeting; working agreement: "no item is ready for planning until [criteria met]".

4. **Facilitate sprint planning** (use `agile-coach:facilitate-sprint-planning`) — addresses root cause 1 (task-assignment anti-pattern). Once working agreements are in place, help the team generate and internalise their own Sprint Goal, negotiate scope themselves, and produce a plan they own (not accept).

## Safety note

The team is showing signs of learned helplessness (blockers named but not owned, retro items recur, actions don't complete). The ceremonies are symptomatic — the real issue is autonomy. Until the team is coached to self-manage, polishing the format won't help. Start with the retrospective (to close the feedback loop and establish ownership norms), then move to working agreements and planning. The standup will self-repair once the team owns blockers.

```

#### `work/docs/coaching/retrospectives/2026-05-29.md`

```
---
title: Retrospective — billing — 2026-05-29
date: 2026-05-29
author: agile-coach
category: Coaching
---

## What we gathered

Sprint 14. Production incident on the reconciliation deploy. Tired team.

## Insights

(none recorded — went straight to actions again)

## Action items

- Improve test coverage
- Reduce interruptions

```

#### `work/docs/coaching/retrospectives/2026-05-15.md`

```
---
title: Retrospective — billing — 2026-05-15
date: 2026-05-15
author: agile-coach
category: Coaching
---

## What we gathered

Sprint 13. Bumpy. Reconciliation work slipped again.

## Insights

(none recorded — went straight to actions)

## Action items

- Improve test coverage
- Reduce interruptions

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 13.0/14.0 (93%) |
| Evaluated | 2026-06-12 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 55039 ms |
| Target cost | $0.0850 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Reads the supplied observation notes and retrospective records before naming anti-patterns — diagnoses from a full cycle, not a single event | PASS | "Cycle observed" section: "All ceremonies observed... Retrospective outputs from Sprint 13 and 14 reviewed." Anti-patterns table covers all five ceremony types. |
| c2 | Names the status-theatre Daily Scrum anti-pattern, citing the evidence (each developer reports to the Scrum Master/PO, the repeated unaddressed staging-credentials blocker) | PASS | Table row: "Developers report to SM and PO (addressees, not peers). Same blocker ('staging credentials') named Tue/Thu, not picked up by team." |
| c3 | Names the secretary-coach anti-pattern, citing that the team could not run the standup when the Scrum Master was away | PASS | Table row: "SM calls on people by name; team milled about and skipped standup when SM absent on Wed (sprint 14:Wed). Team cannot self-run the event." |
| c4 | Names the task-assignment and no-Sprint-Goal planning anti-patterns, citing the pre-assigned tickets and the three different answers to "what's the goal?" | PASS | Two table rows: pre-assigned tickets quoted verbatim; "three of six developers gave different answers; two shrugged (sprint 14)" cited for No goal row. |
| c5 | Names the demo-theatre review anti-pattern, citing screenshots-not-running-software and the unchanged backlog | PASS | Table row: "Team showed screenshots, not running software. Product backlog was not changed during or after the review (sprint 14)." |
| c6 | Names the retrospective Wheel-of-Fortune / status-theatre anti-patterns, citing the data-straight-to-action jump and the identical ownerless action items across retros | PASS | Two table rows: "Jumps from 'what went wrong' to 'let's do X' with no insight phase" and "neither has an owner or a due date" citing both sprint 13 and 14 retros. |
| c7 | Records at least one good signal as well as the failures (what to reinforce), not a failures-only list | FAIL | No good-signals section exists in the artifact or chat response. The audit is entirely failure-oriented with no positive observations (e.g. consistent 9:30 daily cadence) recorded. |
| c8 | Distinguishes symptom from cause — groups the anti-patterns under a likely shared root (the team has never been coached to self-manage) rather than listing them flat | PASS | Root-cause grouping section: "Root cause 1: Team has not been coached to self-manage... This is the deepest issue." Four root causes named and anti-patterns mapped to each. |
| c9 | Prioritises coaching actions with self-management and safety before format polish, mapping each priority to a skill | PARTIAL | Actions 1–4 map to named skills (facilitate-retrospective, design-working-agreements, coach-definition-of-done, facilitate-sprint-planning). Safety note: "Start with the retrospective... The standup will self-repair once the team owns blockers." |
| c10 | Output is a structured ceremony-audit artifact with an anti-patterns table (event / anti-pattern / evidence / likely root cause), a root-cause grouping, and prioritised coaching actions | PASS | Artifact contains table with columns Event\|Anti-pattern\|Evidence\|Likely root cause, plus "Root-cause grouping" and "Prioritised coaching actions" sections. |
| c11 | Every named anti-pattern cites concrete evidence from the supplied records (which event, what was observed) — no bare "status-theatre standup" without the supporting observation | PASS | Every table row includes sprint-specific evidence: day references (Tue/Thu, Wed), direct quotes from notes ("Sam takes the refund endpoint"), and retrospective dates (2026-05-15, 2026-05-29). |
| c12 | Output applies the self-management test — would the team run every event if the coach went on leave — and answers it using the standup-skipped-when-SM-absent evidence | PASS | Secretary coach row: "Team cannot self-run the event." Safety note: "until the team is coached to self-manage... The standup will self-repair once the team owns blockers." |
| c13 | Output diagnoses the system, not individuals — "the standup is a status report" rather than naming a person as the problem | PASS | All root causes attributed to "team has not been coached to self-manage" or systemic gaps. No individual named as the problem. |
| c14 | Output's prioritised actions map each fix to the skill that addresses it (e.g. facilitate-retrospective, facilitate-sprint-planning) and put self-management/safety ahead of format | PASS | All four actions cite specific skills with backtick notation. Self-management (working agreements #2) and safety (retro #1) precede format polish. Format not mentioned as a standalone action. |
| c15 | Output flags the recurring identical action items across retros as the strongest evidence the insight phase is being skipped | PARTIAL | Coaching action 1: "The recurrence of identical items across two sprints is the loudest signal that the feedback loop is not closing." Root cause 3 also flags identical language across both retros. |

### Notes

The audit is thorough and well-structured, covering all five ceremonies with specific citations, a four-root-cause grouping, and skill-mapped coaching actions. The only clear miss is c7: no good signals are recorded anywhere in the artifact, making it a failures-only list.
