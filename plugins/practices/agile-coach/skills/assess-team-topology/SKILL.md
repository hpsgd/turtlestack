---
name: assess-team-topology
description: "Assess a team against the Team Topologies four team types (stream-aligned, enabling, platform, complicated-subsystem) and three interaction modes (collaboration, X-as-a-service, facilitating). Produces a topology read and recommendations on team type and interactions. Use when a team's purpose is unclear, dependencies are tangled, or interactions are friction-heavy."
argument-hint: "[team name]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Assess Team Topology

Assess **$ARGUMENTS** using [Team Topologies](https://teamtopologies.com/key-concepts) (Matthew Skelton and Manuel
Pais, 2019). The model gives a vocabulary for what kind of team this is and how it should interact with others — a
useful lens when a team's purpose is muddy or its dependencies are tangled. This is an advisory assessment: the
org-structural call belongs to the coordinator and leads (a coach decision checkpoint), not to you.

## Step 1: Identify the team's primary type

Classify the team against the four types. Most teams should be stream-aligned; the others exist to support them.

| Type | Purpose | Signal |
|------|---------|--------|
| Stream-aligned | Owns a flow of work for a product/service slice end-to-end | Delivers user value directly; the default and most common type |
| Platform | Provides internal services that reduce other teams' cognitive load | Other teams consume its services to go faster |
| Enabling | Carries deep expertise; helps stream-aligned teams acquire new capability | Specialist knowledge other teams temporarily need |
| Complicated-subsystem | Owns a part requiring rare specialist knowledge | A subsystem too complex for a stream-aligned team to own part-time |

A common smell: a "stream-aligned" team that's actually a component team (owns a layer, not a slice), forcing
constant cross-team coordination to ship anything user-facing. Name it.

## Step 2: Classify the current interaction modes

For each significant relationship with another team, identify which of the three interaction modes is in play:

| Mode | What it is | When it's right |
|------|------------|-----------------|
| Collaboration | Two teams work closely together for a period | Discovery, novel problems, high uncertainty — but costly, keep it bounded |
| X-as-a-Service | One team consumes another's service with minimal interaction | Well-understood, stable interfaces — the goal for most platform relationships |
| Facilitating | One team helps another improve or learn | Enabling-team work; temporary capability transfer |

The model's insight: collaboration is expensive (two teams' cognitive load entangled) and should be deliberate and
time-bounded, not the permanent default. A relationship stuck in collaboration that should be X-as-a-Service is a
source of chronic friction.

## Step 3: Read cognitive load

A team owning more than it can hold loses flow. Assess whether the team's responsibilities exceed its cognitive
capacity — too many domains, too much of the stack, too many consumers to support. Excessive cognitive load shows up
as slow flow, constant context-switching, and nothing finishing. The fix is usually a topology change (a platform
or complicated-subsystem team absorbing part of the load), which is a recommendation to the leads, not a coaching
action.

## Step 4: Recommend (advisory only)

Produce a topology read and recommendations: the team's actual type vs how it's being treated, the interaction modes
that should change, and any cognitive-load problem. Frame these as advice for the coordinator and leads — the
restructuring decision is theirs.

## When this lens helps — and when it doesn't

Reach for a topology assessment when a team's purpose is muddy, dependencies are tangled, or interactions generate
chronic friction. It's the right tool when the problem is *structural* — the team is shaped wrong for the work.

Don't reach for it when the problem is process or safety. A team with a clear stream-aligned purpose that runs bad
retrospectives doesn't have a topology problem; it has a facilitation problem (`audit-ceremonies`,
`facilitate-retrospective`). Misdiagnosing a process problem as a structural one sends a restructuring recommendation
to the leads when a coaching conversation would have fixed it.

## Rules

- Most teams should be stream-aligned. If you're classifying many teams as platform or complicated-subsystem,
  re-examine — the default is stream-aligned.
- Name component teams masquerading as stream-aligned. A team that owns a layer, not a slice, generates the
  coordination overhead the model exists to remove.
- Treat collaboration as expensive and time-bounded. A permanent collaboration relationship that should be
  X-as-a-Service is chronic friction, not teamwork.
- This is advisory. The topology and reteaming decisions belong to the coordinator and leads — you assess and
  recommend, you don't restructure.
- Read cognitive load explicitly. A team drowning in scope won't flow no matter how good its ceremonies are.

## Output Format

```markdown
---
title: Team Topology Assessment — [team]
date: YYYY-MM-DD
author: agile-coach
category: Coaching
---

## Team type
- Actual type: [stream-aligned / platform / enabling / complicated-subsystem]
- Treated as: [...]
- Component-team smell: [yes/no — evidence]

## Interaction modes
| Relationship | Current mode | Should be | Friction? |
|--------------|--------------|-----------|-----------|

## Cognitive load
- Assessment: [within capacity / overloaded]
- Evidence: [...]

## Recommendations (advisory to coordinator / leads)
1. [...]
```
