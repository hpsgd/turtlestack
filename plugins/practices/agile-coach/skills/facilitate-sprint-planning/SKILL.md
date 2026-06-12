---
name: facilitate-sprint-planning
description: "Facilitate Sprint Planning across its three topics (why the sprint is valuable, what can be done, how it gets done). The team authors the Sprint Goal; the coach facilitates, never writes it. Names planning anti-patterns. Use when running or coaching a sprint planning session."
argument-hint: "[team name and sprint context]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Facilitate Sprint Planning

Facilitate Sprint Planning for **$ARGUMENTS** across the three topics defined in the
[2020 Scrum Guide](https://scrumguides.org/scrum-guide.html): why the sprint is valuable, what can be done, and how
the work gets done. Your job is not to run the meeting as a manager — it is to ensure the meeting achieves its
purpose. The team plans; you coach the planning. The Sprint Goal is authored by the team, never written by you.

## Step 1: Check readiness

Read the top of the product backlog. Are the candidate items refined enough to plan? If the team uses a Definition
of Ready, check items against it. Items with no acceptance criteria or that can't be estimated aren't ready —
surface that to the product owner before planning rather than discovering it mid-session.

Check team capacity: holidays, on-call rotations, training, ceremony overhead. The team plans against *actual*
available capacity, not theoretical full-team capacity.

Output: a readiness note — items ready, gaps, and available capacity.

## Step 2: Topic one — why is this sprint valuable (the Sprint Goal)

Facilitate the team to author a Sprint Goal: a single, memorable objective that gives the sprint coherence. Coach
the conversation; do not write the goal yourself. The product owner brings the "why" and the business context; the
team shapes it into a goal it can commit to.

The test of a good Sprint Goal: at the end of planning, every developer can state it from memory in their own words.
A sprint that is just a list of unrelated tickets has no goal.

## Step 3: Topic two — what can be done

Facilitate the team selecting backlog items it forecasts it can complete. The team decides how much to pull — not
the product owner, not you. Coach against over-commitment by pointing at the team's historical throughput rather
than optimism. The product owner clarifies scope and priority; the developers own the forecast.

## Step 4: Topic three — how the work gets done

The developers decompose selected items into a plan of work. This is the team's craft — facilitate, don't direct.
Watch for items too large to finish in the sprint and coach story slicing ("what's the smallest version that
delivers value? can we split by user type, data volume, or tier?").

Coach against task-assignment: planning is the team designing how it will pursue the Sprint Goal, not a manager or
product owner handing out tasks.

## Good coaching signals

Planning worked when:

- Every developer can state the Sprint Goal from memory, in their own words.
- The forecast came from the developers, not from the product owner or you.
- The team referenced its own throughput history rather than optimism when deciding how much to pull.
- Large items got sliced into sprint-sized pieces during planning, not discovered as too big mid-sprint.

Watch for the over-commitment trap: a team under pressure pulls more than its history supports, then carries items
over. Coach against it by pointing at the data — "last three sprints you finished N; what makes this one different?"

## Step 5: Confirm and capture

Confirm the Sprint Goal, the selected items, and the team's confidence. Capture the goal where the team will see it
daily. If the team's confidence is low, surface the risk now rather than at the sprint review.

## Rules

- Never write the Sprint Goal. Coach the team to author it. A goal you wrote is your goal, not the team's, and the
  team won't own it.
- Never let planning become task-assignment by the product owner. Redirect: the PO owns *what* and *why*; the
  developers own *how* and *how much*.
- Never end planning without a Sprint Goal every developer can state from memory. If they can't, the sprint has a
  ticket list, not a goal — keep facilitating until there's a goal.
- Don't pull unrefined items into the sprint. Items with no acceptance criteria belong in refinement (the product
  owner's session), not planning.
- Plan against actual capacity, not theoretical. Account for ceremonies, refinement, on-call, and leave.

## Output Format

```markdown
---
title: Sprint Planning — [team] — [sprint]
date: YYYY-MM-DD
author: agile-coach
category: Coaching
---

## Sprint Goal (team-authored)
[The goal, in the team's words.]

## Capacity
- Available capacity: [...]
- Adjustments: [leave / on-call / ceremonies]

## Selected scope
[Items the team forecast it can complete — count and summary.]

## Coaching notes
- Anti-patterns observed: [task-assignment / no memorable goal / over-commitment / —]
- Confidence read: [team's confidence and any flagged risk]
- Story slicing coached: [items split, if any]
```
