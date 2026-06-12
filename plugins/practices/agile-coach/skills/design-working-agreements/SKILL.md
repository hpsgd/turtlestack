---
name: design-working-agreements
description: "Facilitate the team to author its own working agreements — team-generated, specific, and testable — with a review cadence. Distinguishes working agreements from the Definition of Done. Produces a working-agreements artifact. Use when a team has no agreements, has vague ones, or needs to revisit them."
argument-hint: "[team name]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Design Working Agreements

Facilitate **$ARGUMENTS** to author its own working agreements. Working agreements are explicit agreements about how
the team operates — meeting norms, communication protocols, how disagreements are handled. They are distinct from
process (Scrum events, Kanban policies) and from the Definition of Done (the quality contract, owned via
`coach-definition-of-done`). The team authors these; you facilitate. An agreement you wrote is your agreement, and
the team won't honour it.

## Step 1: Surface what's actually happening

Before writing agreements, surface the friction. Run a quick round (use silent writing or
[1-2-4-All](https://www.liberatingstructures.com/1-2-4-all/) to get every voice) on: where does the team step on
each other? What unspoken norms cause friction? What do new joiners get wrong because nobody told them?

Output: a list of friction points the team named — in the team's words.

## Step 2: Convert friction into specific, testable agreements

Coach the team to write agreements that are specific and testable, not aspirational. "We will be respectful" is
untestable and therefore useless. "We don't use laptops in retrospectives unless we're the scribe" is specific and
you can tell whether it's being followed.

Test each candidate agreement:

| Test | Pass | Fail |
|------|------|------|
| Specific | "Standup starts at 9:30; we start without latecomers" | "We'll be punctual" |
| Testable | You can observe whether it happened | "We'll communicate well" |
| Team-owned | The team proposed it | You proposed it |
| Behavioural | Names an action | Names a value |

Keep the set small. Ten agreements nobody remembers is worse than four the team lives by.

## Step 3: Distinguish agreements from the Definition of Done

Working agreements govern *how the team behaves together* (social, interpersonal). The Definition of Done governs
*when work is complete* (quality contract). Don't let quality criteria leak into working agreements or vice versa:

- Working agreement: "We pair on anything touching auth."
- Definition of Done: "Auth changes have a security review before merge."

If a candidate item is really a quality gate, route it to `coach-definition-of-done`.

## Step 4: Set a review cadence

Working agreements are living. They belong in the retrospective cycle: created early, reviewed when they stop
working. Agree when the team will revisit them (a standing retro item, or a trigger like a new joiner or a recurring
friction). An agreement nobody reviews becomes invisible wallpaper.

## Step 5: Record the artifact

Write `docs/coaching/working-agreements.md` using the working-agreements template
(`templates/working-agreements.md`). Record who was present (the team authored it) and the review trigger.

## Worked example — vague to specific

The most common failure is agreements that sound good and mean nothing. Coach each candidate from value to behaviour:

| Team said | Too vague because | Coached to |
|-----------|-------------------|-----------|
| "We'll respect each other" | No observable behaviour | "We don't talk over each other in meetings; the facilitator holds the queue" |
| "We'll communicate better" | Can't tell if it happened | "Blockers go in the team channel within the hour, not held until standup" |
| "We'll support each other" | Untestable sentiment | "Anyone stuck for 30 minutes asks for a pair rather than grinding alone" |
| "We'll be on time" | No definition of on-time | "Standup starts at 9:30; we start without latecomers" |

The pattern: name the trigger, the behaviour, and how you'd know it happened. If you can't observe it, it's a value,
not an agreement.

## Rules

- Never write the agreements yourself. Facilitate; the team authors. Your wording, your agreement, their indifference.
- Every agreement must be specific and testable. If you can't observe whether it's being followed, it's a value, not
  an agreement — rewrite it.
- Keep the set small. A short list the team lives by beats a long list it forgot.
- Don't mix working agreements with the Definition of Done. Social behaviour vs quality contract — route quality
  items to `coach-definition-of-done`.
- Set a review trigger. An agreement with no review cadence is dead on arrival.

## Output Format

```markdown
---
title: Working Agreements — [team]
date: YYYY-MM-DD
author: agile-coach
category: Coaching
---

## How these were made
- Authored by: [the team — who was present]
- Friction points surfaced: [...]

## Agreements (team-authored)
1. [Specific, testable, behavioural agreement]
2. [...]

## Review cadence
- Revisited: [when / trigger]

## Routed to Definition of Done
[Any candidate that was really a quality gate.]
```
