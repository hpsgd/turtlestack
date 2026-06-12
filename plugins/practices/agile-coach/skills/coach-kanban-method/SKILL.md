---
name: coach-kanban-method
description: "Coach a team on the Kanban Method's six core practices (visualise, limit WIP, manage flow, make policies explicit, feedback loops, evolve experimentally), when Kanban beats Scrum (discovery, ops, irregular arrival), and the Scrumban hybrid. Use when a team's work doesn't fit sprints or to introduce pull-based flow."
argument-hint: "[team name and work type]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Coach the Kanban Method

Coach **$ARGUMENTS** on the [Kanban Method](https://kanban.university/). Kanban is evolutionary: it starts with what
the team already does and improves incrementally, rather than prescribing a framework. It fits work that Scrum
serves poorly. This skill pairs with `coach-flow-metrics` (Kanban's measures) and `audit-scaling-framework`. Source:
David J. Anderson, [*Kanban: Successful Evolutionary Change*](https://djaa.com/).

## Step 1: Confirm Kanban fits the work

Don't introduce Kanban by default — confirm it fits. Kanban beats Scrum when:

| Work type | Why Scrum fits poorly | Why Kanban fits |
|-----------|----------------------|-----------------|
| Discovery / research | Continuous, not sprint-bounded; sprints pressure learning | Pull-based, no artificial cadence on learning |
| Operations / support | Irregular, unpredictable arrival | WIP limits + explicit interrupt policy handle interrupts |
| Maintenance | Mix of planned and unplanned, unpredictable | Pull system absorbs variation |

If the work is sprint-sized complex feature work with meaningful stakeholder feedback, Scrum may fit better — say
so. If the team needs both a cadence and pull, coach Scrumban (Step 5).

Output: a one-line judgement on whether Kanban fits and why.

## Step 2: Coach the six core practices

Coach the team through the practices in order — visualisation first, because everything else depends on seeing the
work:

1. **Visualise** — make invisible work visible. A board with columns for workflow states and cards for work items.
   Problems hide without it.
2. **Limit WIP** — set explicit WIP limits per state. When a column is full, no new work enters until something
   exits. This is the central mechanism: it converts a push system (start work whenever) to a pull system (start
   only when there's capacity).
3. **Manage flow** — monitor speed and smoothness. Track blockages, find bottlenecks, measure cycle time. Aim for
   even flow, not bursts followed by queues.
4. **Make policies explicit** — document the rules: what counts as done per column, what triggers a handoff, how
   blockers escalate, how interrupts are handled. Explicit policies enable rational discussion.
5. **Implement feedback loops** — Anderson's cadences run at different frequencies: daily standup (team),
   replenishment (what enters), service delivery review (metrics/flow), operations review (cross-team). Coach the
   team to run the cadences it needs, not all of them by rote.
6. **Improve collaboratively, evolve experimentally** — change one thing at a time, measure before and after. Use
   models (Theory of Constraints, systems thinking) to guide changes rather than guessing.

## Step 3: Set the first WIP limits

WIP limits are where teams resist most. Coach the why with Little's Law (handled in depth by `coach-flow-metrics`):
less WIP means shorter cycle time without adding people. Start with a limit slightly below current WIP so the team
feels the pull effect, then evolve experimentally. A WIP limit nobody enforces is decoration.

## Step 4: Make the interrupt policy explicit (for ops/support)

For operations and support teams, the interrupt is the defining challenge. Coach the team to write an explicit
policy: what classes of work can jump the queue, who decides, and what WIP is reserved for interrupts. An implicit
interrupt policy means every urgent request wins and planned work never finishes.

## Step 5: Coach Scrumban where the team needs both

Scrumban (Corey Ladas, 2009) is a pragmatic hybrid: keep a cadence for retrospectives and planning checkpoints, but
manage daily work on a Kanban board with WIP limits and drop the sprint commitment. It fits teams transitioning from
Scrum or running mixed planned/unplanned work. Its failure mode: losing the discipline of both methods — name that
risk explicitly.

## Rules

- Don't introduce Kanban by default. Confirm the work doesn't fit Scrum first — the right method matches the work.
- Visualise before limiting. You can't set sensible WIP limits on work you can't see.
- WIP limits must be enforced. An unenforced limit is decoration; the pull effect only happens when "full means
  full."
- Make the interrupt policy explicit for ops/support. Implicit means urgent always wins and planned work starves.
- Evolve experimentally — one change, measured. Don't redesign the whole board at once; you won't know what worked.
- Name the Scrumban risk. A hybrid that drops the discipline of both methods is worse than either alone.

## Output Format

```markdown
---
title: Kanban Coaching — [team]
date: YYYY-MM-DD
author: agile-coach
category: Coaching
---

## Fit judgement
- Kanban fits because: [...] (or: Scrum fits better because [...])

## Six practices — current state and coaching
| Practice | Current | Coaching action |
|----------|---------|-----------------|
| Visualise | [...] | [...] |
| Limit WIP | [...] | [...] |
| Manage flow | [...] | [...] |
| Explicit policies | [...] | [...] |
| Feedback loops | [...] | [...] |
| Evolve experimentally | [...] | [...] |

## WIP limits set
| State | Current WIP | Limit | Rationale |
|-------|-------------|-------|-----------|

## Interrupt policy (ops/support)
[Explicit policy, or N/A.]

## Scrumban
- Recommended: [yes/no — and the risk named]
```
