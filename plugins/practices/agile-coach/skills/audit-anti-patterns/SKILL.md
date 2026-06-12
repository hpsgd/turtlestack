---
name: audit-anti-patterns
description: "Diagnose deep agile dysfunction using Aino Corry's retrospective anti-pattern catalogue, the Zombie Scrum four-symptom check, and Ron Jeffries' Dark Scrum diagnostic. Distinguishes team-fixable problems from organisational ones. Use when ceremonies look fine on the surface but the team isn't really improving or shipping."
argument-hint: "[team name]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Audit Anti-Patterns

Diagnose deep dysfunction in **$ARGUMENTS**. Where `audit-ceremonies` checks whether the events run correctly, this
skill checks whether Scrum has a beating heart at all. Some dysfunctions are team-fixable; many are organisational,
and coaching the team harder won't fix them. Reference:
[Aino Corry's retrospective anti-patterns](https://martinfowler.com/articles/retrospective-antipatterns.html),
[Zombie Scrum](https://zombiescrum.org/), and [Ron Jeffries' Dark Scrum](https://ronjeffries.com/articles/016-09ff/defense/).

## Step 1: Run the Zombie Scrum four-symptom check

Zombie Scrum is "Scrum on the surface, except there's no beating heart." Check all four symptoms:

| Symptom | Evidence |
|---------|----------|
| No working software shipped | The shippable increment is treated as optional; nothing reaches users |
| No contact with the outside world | The team operates in isolation from stakeholders and customers |
| No emotional response | Items carry over sprint after sprint with no concern; outcomes feel irrelevant |
| No drive to improve | Retrospectives happen but nothing ever changes |

Zombie Scrum has three usual causes: cargo-cult adoption (ceremonies without values), no urgency (no real goal or
consequence for not shipping), and organisational values incompatible with empiricism. Name the likely cause.

## Step 2: Run the Dark Scrum diagnostic

Dark Scrum is Scrum that oppresses developers — mechanics adopted without values, where power holders use sprint
boundaries to increase pressure. Check for:

- Developers committing to unrealistic sprint goals under pressure.
- Quality practices (TDD, CI, refactoring) skipped to hit the sprint.
- Technical debt accumulating sprint over sprint.
- The sprint review used as a blame session.

Jeffries' core point: "When a team does not have the necessary technical skills to produce a shippable Increment
week in and week out, the Scrum process almost inevitably goes dark." Pressure without technical capability produces
Dark Scrum. The fix is often a missing technical-practice foundation, not more process coaching — flag that to the
team's lead (CTO).

## Step 3: Map retrospective anti-patterns

Check the last few retros against Corry's catalogue:

| Anti-pattern | Signal |
|--------------|--------|
| Wheel of Fortune | Data straight to action, no insight phase; symptoms fixed, problem returns |
| In the Soup | Retro spends its time on things outside the team's control |
| Loudmouth | One voice shapes every conclusion |
| Status theatre | No action items, or items with no owner and no date |
| Blame circles | Focus on who did wrong, not on systemic conditions |
| Same format forever | Team habituated and disengaged |

## Step 4: Sort team-fixable from organisational

This is the decisive step. Many of these dysfunctions cannot be coached away at the team level:

- **Team-fixable** — retrospective format issues, insight-phase skipping, working-norm gaps. Coach directly.
- **Organisational** — Zombie Scrum from incompatible org values, Dark Scrum from a pressure culture, a missing
  technical foundation. Surviving these requires changing organisational conditions, not coaching the team harder.
  Escalate to the coordinator and the team's lead with evidence.

If you've surfaced the same dysfunction three retrospectives running with no movement, that's your failure cap —
stop coaching harder and escalate.

## Rules

- Distinguish team-fixable from organisational. Coaching a team harder through Zombie or Dark Scrum is cruelty
  disguised as diligence — the cause is upstream.
- Cite evidence for every symptom. "Zombie Scrum" is not a diagnosis; "no increment shipped in four sprints, no
  stakeholder contact, three retros with zero changes" is.
- Flag missing technical practices to the CTO. Dark Scrum from a capability gap is an engineering-leadership problem,
  not a process one.
- Don't recite the Prime Directive as a substitute for fixing blame culture. Blame circles need the underlying
  safety addressed, not a ritual.
- Respect the failure cap. Same dysfunction, three retros, no movement → escalate, don't grind.

## Output Format

```markdown
---
title: Anti-Pattern Audit — [team]
date: YYYY-MM-DD
author: agile-coach
category: Coaching
confidence: [0-4]
---

## Zombie Scrum check
| Symptom | Present? | Evidence |
|---------|----------|----------|
| No working software | [y/n] | [...] |
| No outside contact | [y/n] | [...] |
| No emotional response | [y/n] | [...] |
| No drive to improve | [y/n] | [...] |
- Likely cause: [cargo-cult / no urgency / incompatible values]

## Dark Scrum check
[Findings on pressure, skipped practices, technical debt, blame.]

## Retrospective anti-patterns
[Corry catalogue matches with evidence.]

## Team-fixable
1. [coach directly — skill]

## Organisational (escalate to coordinator / lead)
1. [evidence and why it's not team-fixable]
```
