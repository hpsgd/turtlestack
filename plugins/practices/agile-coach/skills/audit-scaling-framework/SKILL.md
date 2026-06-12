---
name: audit-scaling-framework
description: "Help a multi-team setup pick or deliberately reject a scaling framework — where LeSS, Nexus, Scrum@Scale, and SAFe fit and where they don't. Produces a recommendation grounded in the coordination problem, not framework fashion. Use when leadership is considering a scaling framework or a team is being forced into one."
argument-hint: "[context — number of teams, the coordination problem]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Audit a Scaling Framework

Help **$ARGUMENTS** pick or deliberately reject a scaling framework. The [Scrum Guide](https://scrumguides.org/scrum-guide.html)
addresses only single-team Scrum; scaling frameworks address multi-team delivery. This is an advisory assessment —
adopting a scaling framework is an org-structural decision for the coordinator and leads (a coach decision
checkpoint). Your job is to ground the choice in the actual coordination problem rather than framework fashion.

## Step 1: Name the coordination problem first

Don't start from the framework — start from the problem. What specifically is hard? Common multi-team problems:

- A single shippable increment needs coordinated work across many teams.
- Teams keep blocking each other on shared components.
- Dependencies aren't visible until they bite at integration.
- Priorities conflict across teams with no resolution mechanism.

The most important question: can the coordination *need* be reduced rather than coordinated? The strongest critique
of scaling frameworks (and LeSS's whole premise) is that many solve coordination by adding structure when the real
fix is reorganising so teams are less interdependent (feature teams, not component teams — ties to
`assess-team-topology`). If you can remove the dependency, you may not need a framework at all.

Output: the coordination problem stated concretely, and whether it can be reduced instead.

## Step 2: Map the candidates to the problem

| Framework | Shape | Fits when | Caution |
|-----------|-------|-----------|---------|
| [LeSS](https://less.works/) | Minimalist; single-team Scrum extended to 2-8 teams with few new roles | You want minimal added structure and can restructure into feature teams | Requires genuine reorganisation; not a bolt-on |
| [Nexus](https://www.scrum.org/resources/scaling-scrum) | Adds a Nexus Integration Team for 3-9 teams on one Integrated Increment | You want Scrum Guide vocabulary and a clear integration owner | Adds a coordination team |
| [Scrum@Scale](https://www.scrumatscale.com/) | Network of teams with a Scrum-of-Scrums layer | You need flexible scaling that can extend organisation-wide | Coordination overhead grows with the network |
| [SAFe](https://scaledagileframework.com/) | Most prescriptive; team/program/solution/portfolio layers, PI planning, ARTs | A large enterprise needs heavy structure and alignment ceremonies | Widely criticised for institutionalising bureaucracy; heaviest option |

## Step 3: Apply the deliberate-rejection test

Picking no framework is a legitimate outcome. Reject a framework deliberately when:

- The coordination need can be reduced by restructuring teams instead.
- There are few enough teams (2-3) that lightweight coordination (a regular sync, shared backlog visibility) suffices.
- The framework would add more ceremony than the problem warrants — SAFe on three teams is overkill.

A deliberate "no, and here's the lightweight coordination we'll use instead" is a better answer than adopting a
framework because it's the industry default.

## Step 4: Recommend (advisory only)

Produce a recommendation tied to the coordination problem: reduce-the-need first, then the lightest framework that
fits if coordination genuinely can't be reduced, with the rejection rationale for the ones that don't fit. Frame it
for the coordinator and leads — the adoption decision is theirs.

## The common critique to keep in mind

Scaling frameworks attract sharp criticism, and the criticism is useful signal. The recurring charge — levelled at
SAFe most often, by practitioners including Ron Jeffries and Allen Holub — is that they solve coordination by adding
structure rather than by reducing the coordination need. LeSS takes the opposite stance: reorganise into feature
teams so there's less to coordinate, then add as little new structure as possible.

Carry that lens into every assessment. Before recommending any framework, ask whether the coordination problem is
real and irreducible, or whether it's an artefact of how teams are currently split (component teams forcing
cross-team handoffs to ship anything). A framework that institutionalises a dependency you could have removed is
worse than no framework. This is also why "adopt the industry default because everyone uses it" is the weakest
possible rationale — it optimises for looking standard, not for solving the team's actual problem.

## Rules

- Start from the coordination problem, never from the framework. "We should do SAFe" is fashion; "teams block each
  other on the shared payments service" is a problem you can solve.
- Always test reduce-the-need before adopting structure. The best scaling decision is often a topology change that
  removes the dependency, not a framework that coordinates it.
- Prefer the lightest framework that fits. Added structure is a cost; don't pay for more than the problem requires.
- Treat "no framework" as a valid recommendation. Lightweight coordination on a few teams beats a heavyweight
  framework adopted by default.
- This is advisory. Adopting a scaling framework is an org-structural decision for the coordinator and leads — you
  ground the choice, you don't make it.

## Output Format

```markdown
---
title: Scaling Framework Assessment — [context]
date: YYYY-MM-DD
author: agile-coach
category: Coaching
confidence: [0-4]
---

## Coordination problem
- Stated concretely: [...]
- Can the need be reduced (topology change)? [yes/no — how]

## Candidate fit
| Framework | Fits? | Rationale |
|-----------|-------|-----------|
| LeSS | [...] | [...] |
| Nexus | [...] | [...] |
| Scrum@Scale | [...] | [...] |
| SAFe | [...] | [...] |

## Recommendation (advisory to coordinator / leads)
- Primary: [reduce-the-need / framework / no framework + lightweight coordination]
- Rationale: [...]
- Rejected and why: [...]
```
