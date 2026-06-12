---
name: audit-ceremonies
description: "Observe a full sprint cycle and name ceremony anti-patterns with evidence — status-theatre standups, secretary Scrum Master, planning-as-task-assignment, retrospectives without action items. Produces an audit with prioritised coaching actions. Use when a team's ceremonies feel hollow or to diagnose ceremony health."
argument-hint: "[team name]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Audit Ceremonies

Observe a full sprint cycle for **$ARGUMENTS** and name ceremony anti-patterns with evidence. This skill diagnoses;
the `facilitate-*` skills fix. For deeper systemic dysfunctions (Zombie Scrum, Dark Scrum), use
`audit-anti-patterns`. Reference: the [2020 Scrum Guide](https://scrumguides.org/scrum-guide.html) defines each
event's purpose, and [Scrum.org's anti-pattern catalogues](https://www.scrum.org/resources/blog) document the
failure modes.

## Step 1: Observe across a full cycle

Anti-patterns only surface across a cycle, not in a single event. Observe (or read records of) each event:
planning, daily scrums, refinement, review, retrospective. Note who runs each event, who talks to whom, and what
the event produces. Don't intervene during observation — you're diagnosing, not coaching, yet.

Output: a one-line note per event on who ran it and what it produced.

## Step 2: Check each event against its anti-patterns

| Event | Anti-pattern | Evidence to look for |
|-------|--------------|---------------------|
| Daily Scrum | Status theatre | Each person reports *at* the coach/PO; questions go round the table toward an authority; no planning happens; blockers named stay blocked |
| Daily Scrum | Secretary coach | The coach runs the standup; the team waits to be called on; can't run the event without the coach |
| Sprint Planning | Task-assignment | The PO hands out tasks; developers don't own the forecast; no memorable Sprint Goal |
| Sprint Planning | No goal | Planning ends with a ticket list nobody can summarise |
| Sprint Review | Demo theatre | One-way presentation to passive recipients; backlog doesn't change |
| Refinement | Absent or batched | Items reach planning unrefined; refinement is a dreaded standalone meeting, not continuous |
| Retrospective | Status theatre | No action items, or items with no owner and no due date |
| Retrospective | Wheel of Fortune | Jumps from data to action with no insight phase; same items recur |

## Step 3: Record the good signals too

An audit that only lists failures gives the team nothing to protect. Note what's working, because those are the
behaviours to reinforce:

| Event | Good coaching signal |
|-------|---------------------|
| Daily Scrum | Developers organise it themselves; the conversation is about the Sprint Goal, not individual tasks; the coach attends but doesn't facilitate |
| Sprint Planning | Every developer can state the Sprint Goal from memory; the plan is the team's, not the PO's or coach's |
| Sprint Review | Stakeholders participate; the backlog changes as a result |
| Retrospective | Action items are owned and routed to the next sprint backlog; formats vary across sprints |

The sharpest self-management test: if the coach went on leave, could the team run every event without them? If yes,
the coach has built capability. If no, the coach has built a dependency.

## Step 4: Distinguish symptom from cause

A secretary-coach standup and a no-goal planning session often share one root: the team has never been coached to
self-manage. Group the observed anti-patterns by likely root cause rather than listing them flat. Recurring action
items across retros are the strongest signal that the insight phase is being skipped.

## Step 5: Prioritise coaching actions

Rank the fixes. Safety and self-management issues come before format polish — a team that can't speak honestly won't
benefit from a nicer retro format. Map each priority to the skill that addresses it.

## Rules

- Always observe a full cycle before naming anti-patterns. A single bad standup isn't a pattern.
- Cite evidence for every anti-pattern — what was observed, in which event. "Status-theatre standup" is not a
  finding; "standup on [date]: each developer reported to the PO, three blockers named, none addressed" is.
- Diagnose the system, not individuals. "The standup is a status report" not "Sam dominates the standup." If an
  individual's behaviour is the issue, raise it privately, not in the audit.
- Don't fix during the audit. Observation and intervention are separate — mixing them contaminates the diagnosis.
- Prioritise self-management and safety over format. Polishing ceremonies on a team that can't self-manage is
  rearranging deck chairs.

## Output Format

```markdown
---
title: Ceremony Audit — [team]
date: YYYY-MM-DD
author: agile-coach
category: Coaching
---

## Cycle observed
[Sprint / period and which events were observed.]

## Anti-patterns found
| Event | Anti-pattern | Evidence | Likely root cause |
|-------|--------------|----------|-------------------|
| [event] | [pattern] | [what was seen, when] | [root] |

## Root-cause grouping
[Anti-patterns grouped by shared cause.]

## Prioritised coaching actions
1. [Highest priority — fix and skill] — addresses [root cause]
2. [Second]
3. [Third]
```
