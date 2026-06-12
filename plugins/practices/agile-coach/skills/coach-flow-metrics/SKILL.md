---
name: coach-flow-metrics
description: "Teach the team to read its own flow data — cycle-time scatterplot, throughput, work-item age, and cumulative flow diagram — with Little's Law as the why behind WIP limits. Produces a flow read and coaching plan. Use when a team is drowning in WIP, has unpredictable delivery, or needs to understand its own flow."
argument-hint: "[team name and any flow data location]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Coach Flow Metrics

Teach **$ARGUMENTS** to read its own flow data. The goal is the team self-correcting from its own instruments, not
you reporting numbers at it. You coach the practice; the delivery manager only reads the data for status — the
boundary matters. Reference: Daniel Vacanti's
[*Actionable Agile Metrics for Predictability*](https://actionableagile.com/) and Little's Law.

## Step 1: Establish the four measures

Teach the team what each measure is and what it answers:

| Measure | Definition | Answers |
|---------|------------|---------|
| Cycle time | Elapsed time from work *started* to *done* | How long does our work actually take? |
| Lead time | Elapsed time from *requested* to *done* (includes queue) | What does a customer experience? |
| Throughput | Items completed per unit time | How much do we finish, and the trend? |
| Work-item age | Time since a *currently-active* item started | Which in-progress item is aging and needs attention now? |

The distinction that trips teams up: cycle time measures *active* time (start to done); lead time includes queue
time (requested to done). Cycle time is more actionable for the team; lead time is what stakeholders feel.

## Step 2: Read the cycle-time scatterplot

The scatterplot — each completed item plotted by completion date (X) against its cycle time (Y) — is the primary
diagnostic. Teach the team to read it: the spread shows variability; percentile lines (50th, 85th, 95th) show
typical and worst-case behaviour. An item sitting above the 85th percentile is "aging in progress" and warrants
attention *now*, before it's late.

## Step 3: Read the cumulative flow diagram

A CFD charts how many items are in each workflow state over time. Teach the team to read the bands:

- Even-width bands rising steadily → healthy flow.
- A widening band → WIP accumulating, a bottleneck forming.
- A flat top line → nothing is completing (no throughput).
- Steepening after flatness → batch releases, not continuous flow.

The CFD gives the system-level picture; the scatterplot gives the item-level picture. The team needs both.

## Step 4: Teach Little's Law as the why behind WIP limits

WIP limits aren't preference — they're physics. Little's Law:

```
Average Cycle Time = Average WIP / Average Throughput
```

Concretely: 20 items in progress, completing 4 per week → 5-week cycle time. Drop WIP to 10 and cycle time halves —
without adding a person or changing the process. This is the mathematical justification for limiting WIP, and it's
what converts a team from "we're busy" to "we finish things." Note the law's conditions: stable flow, consistent
measurement, no wild work-item-size variation confounding the averages.

## Step 5: Hand the instruments to the team

The point isn't a report you produce — it's the team reading its own data and acting. Set up the team to pull these
views itself (in its board tool) and to look at them in its own cadence. If only you can read the scatterplot,
you've built a dependency, not a capability.

## Rules

- Teach the team to read its own data — don't become the flow-report service. The instruments belong to the team.
- Cycle time is start-to-done; lead time is requested-to-done. Don't conflate them — the difference is queue time and
  it matters to the conversation.
- Justify WIP limits with Little's Law, not preference. "Limit WIP because it feels tidy" doesn't land; "halve WIP,
  halve cycle time" does.
- Watch the conditions on Little's Law. Wildly varying item sizes break the averages — surface that rather than
  reporting a meaningless mean.
- Stay on your side of the boundary. You coach the flow practice; the delivery manager reads the numbers for status.
  Don't drift into producing status reports.

## Output Format

```markdown
---
title: Flow Coaching — [team]
date: YYYY-MM-DD
author: agile-coach
category: Coaching
---

## Current flow read
| Measure | Value | Read |
|---------|-------|------|
| Cycle time (50th / 85th) | [...] | [...] |
| Throughput | [...] | [...] |
| WIP | [...] | [...] |
| Aging items (>85th pctile) | [...] | [needs attention now] |

## CFD read
[Band shape and what it indicates — flow / bottleneck / batching.]

## Little's Law applied
- Current: WIP [x] / throughput [y] → cycle time [z]
- If WIP → [target]: cycle time → [projected]

## Coaching plan
- What the team will now read itself: [...]
- Cadence: [...]
```
