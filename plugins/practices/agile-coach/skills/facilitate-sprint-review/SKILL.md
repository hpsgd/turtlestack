---
name: facilitate-sprint-review
description: "Coach the sprint review as a collaborative working session that inspects the increment and adapts the backlog — not a demo to management. The product manager runs the review; the coach facilitates the working-session craft. Use when a sprint review has become a passive presentation or to coach review facilitation."
argument-hint: "[team name and review context]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Facilitate the Sprint Review

Coach the sprint review for **$ARGUMENTS** as a working session, not a demo. The
[2020 Scrum Guide](https://scrumguides.org/scrum-guide.html) defines the sprint review as an inspection of the
increment and adaptation of the product backlog — the only event where external stakeholders formally participate.
The product owner / product manager runs the review and owns the backlog conversation; you facilitate the
working-session craft so the conversation stays collaborative rather than performative.

## Step 1: Reframe the review before it starts

The most common failure is the review as a polished presentation to passive recipients — a status update dressed as
a ceremony. The value is in the conversation that changes the backlog, not in the slides. Before the session,
confirm the framing with the product manager: stakeholders are participants, not an audience.

Output: a one-line framing note — is this set up as a working session or a demo?

## Step 2: Inspect the increment against the Definition of Done

Only work that meets the team's Definition of Done is presented. Coach the team to show working software, not
slideware. Inspecting half-done work as if it were complete erodes the meaning of "done" and the trust of
stakeholders.

If items are being presented that don't meet the DoD, that's a signal for `coach-definition-of-done` and a likely
Zombie Scrum symptom — note it.

## Step 3: Facilitate the collaborative conversation

Coach stakeholders into a collaborative posture: what was done, what changed in the market or the business, what
should come next. Use structure to draw out quiet stakeholders — direct questions, round-robin on "what would you
prioritise next?", or dot voting on backlog candidates. The goal is genuine input that adapts the backlog.

Watch for the HIPPO effect (the highest-paid person's opinion dominating). Use structured input so the loudest voice
doesn't set the backlog single-handed.

## Step 4: Capture backlog adaptation

The output of a good review is a changed backlog: new items, reprioritised items, dropped items. The product
manager owns these decisions; you capture that the conversation actually produced adaptation rather than polite
applause.

## Good coaching signals

You'll know the review is working when:

- Stakeholders interrupt with questions and alternatives rather than nodding through slides.
- The team shows working software in a real environment, not screenshots.
- The backlog visibly changes during or right after the session — items added, reordered, or cut.
- Disagreement about priorities surfaces in the room and gets worked through, not deferred to a side channel.

Concrete facilitation moves when the review drifts toward demo theatre:

- Hand the driving to a stakeholder: "Try it yourself — what would you do here?"
- Pause after each increment and ask "what does this change about what's next?" instead of moving to the next item.
- Replace "any questions?" (which gets silence) with a direct prompt: "[name], you own this area — what's your
  reaction?"

## Rules

- Never let the review be a demo to management. If it's a one-way presentation, it failed its purpose — coach toward
  conversation.
- Only DoD-complete work gets presented. Showing half-done work as done corrodes the Definition of Done.
- The product manager runs the review and owns the backlog. You facilitate the craft of the working session; don't
  cross into owning the backlog conversation.
- Draw out quiet stakeholders with structure. Passive stakeholders produce no adaptation, which is the whole point
  of the event.
- Don't measure success by applause. Measure it by whether the backlog changed.
- Don't let the review slide into sprint planning. Inspecting and adapting the backlog is the review's job; deciding
  the next sprint's scope is planning's. Keep the events distinct or both lose their purpose.

## Output Format

```markdown
---
title: Sprint Review — [team] — [sprint]
date: YYYY-MM-DD
author: agile-coach
category: Coaching
---

## Framing
- Set up as: [working session / demo — and what was coached]

## Increment inspected
- DoD-complete items shown: [...]
- Items presented that did NOT meet DoD: [...] (flag for coach-definition-of-done)

## Backlog adaptation (owned by product manager)
[What changed in the backlog as a result of the conversation.]

## Coaching notes
- Stakeholder posture: [collaborative / passive — what was coached]
- HIPPO effect observed: [yes/no — mitigation used]
```
