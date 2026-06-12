---
name: facilitate-retrospective
description: "Design and facilitate a team retrospective using Derby & Larsen's five phases, with a format catalogue (Start/Stop/Continue, 4Ls, Sailboat, Mad/Sad/Glad, 5 Whys, Lean Coffee) and Liberating Structures. Produces a retro plan and an output file with action items routed to the next sprint backlog. Use when running or designing a retrospective."
argument-hint: "[team name and any focus, e.g. 'billing team, recent incident']"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Facilitate a Retrospective

Design and run a retrospective for **$ARGUMENTS** using the five-phase structure from Esther Derby and Diana
Larsen's [*Agile Retrospectives*](https://pragprog.com/titles/dlret/agile-retrospectives/). This skill produces a
retro plan before the session and an output file after, with action items routed into the next sprint backlog (a
[Scrum Guide](https://scrumguides.org/scrum-guide.html) requirement). For diagnosing why retros aren't working, use
`audit-anti-patterns` first.

## Step 1: Read context and the safety level

Read the last 2-3 retrospective outputs in `docs/coaching/retrospectives/`. Look for recurring action items — a
signal the team fixes symptoms, not causes. Check the most recent team-health scan if one exists.

Assess psychological safety before designing the format. A quick anonymous 1-5 check on "how comfortable do you feel
sharing honestly today?" tells you how much is being withheld. Low safety changes the format choice: pick
Mad/Sad/Glad or a silent-writing structure over an open round-robin.

Output: a one-line context note and a safety read (1-5, how assessed).

## Step 2: Pick the format to match the moment

Don't run the same format every sprint — teams habituate and disengage. Match the format to what the team needs:

| Format | Best for | Failure mode |
|--------|----------|--------------|
| Start / Stop / Continue | Fast, familiar, low overhead | Long "start" list with no prioritisation |
| 4Ls (Liked, Learned, Lacked, Longed For) | More nuance; surfaces forward wishes | Can sprawl without timeboxing |
| Sailboat / Speedboat | Visual, accessible, mixed-discipline teams | Metaphor reduces specificity |
| Mad / Sad / Glad | Low-safety teams; emotional temperature | Stays at feelings without root cause |
| 5 Whys | Root-cause on one specific problem | Stops at first plausible answer |
| Lean Coffee | Team-owned agenda, dot-voted | Misses systemic issues in team blind spots |

For stuck or low-safety groups, layer in [Liberating Structures](https://www.liberatingstructures.com/):

- [1-2-4-All](https://www.liberatingstructures.com/1-2-4-all/) — individual → pair → quartet → whole group. Ideas
  form in private before group pressure. ~15 min.
- [TRIZ](https://www.liberatingstructures.com/9-triz/) — "how would we guarantee the worst possible outcome?" then
  invert. Surfaces dysfunctions polite retros skip.
- What, So What, Now What — separate observation from interpretation from action. Good after incidents.

Output: the chosen format and why it fits this moment.

## Step 3: Run the five phases

Facilitate, don't dominate. You serve the process; the team owns the outcome. Hold neutrality — if you have a view,
declare it ("stepping out of facilitator mode for a moment") and step back in.

1. **Set the stage.** Open with [Kerth's Prime Directive](https://retrospectivewiki.org/index.php?title=The_Prime_Directive)
   as the safety frame: "everyone did the best job they could, given what they knew at the time." Confirm the
   timebox and the format. Get everyone speaking once early (a check-in word) so silence isn't the default.
2. **Gather data.** Collect what actually happened — events, facts, feelings. Use the chosen format. Use silent
   writing or dot voting to counter the Loudmouth pattern (one voice shaping conclusions).
3. **Generate insights.** This is the phase teams skip — going straight from data to action is the "Wheel of
   Fortune" anti-pattern and fixes symptoms. Use 5 Whys or What/So What/Now What to find root causes.
4. **Decide what to do.** Convert insights into a small number of specific action items. Fewer, owned, and done
   beats a long list nobody picks up. Each action gets an owner and a due sprint.
5. **Close the retrospective.** Confirm the action items and where they're going. A quick appreciation or a
   return-on-time-invested check closes the loop and gives you a signal on the session itself.

## Step 4: Route action items and write the output

Write `docs/coaching/retrospectives/YYYY-MM-DD.md`. Every action item goes into the next sprint backlog with an
owner — not a parking lot, not "the team." A retro that ends without action items routed into the backlog was status
theatre.

## Rules

- Always open Set the Stage with the Prime Directive. Reciting it doesn't substitute for believing it — if blame
  surfaces, redirect to systemic conditions, not the person.
- Never skip Generate Insights. Data → action with no insight phase fixes symptoms and the problem returns next
  sprint.
- Never let the retro discuss only things outside the team's control ("In the Soup"). Redirect to what the team
  *can* change; note the external item for the delivery manager to carry.
- Vary the format across sprints, but don't change it for novelty alone — change it to match what the team needs.
- Don't assign action items to "the team" or leave them undated. No owner and no due sprint means it won't happen.
- Never facilitate as a participant with a stake in the outcome without declaring it. Undeclared steering corrodes
  trust faster than an honest opinion.

## Output Format

```markdown
---
title: Retrospective — [team] — [date]
date: YYYY-MM-DD
author: agile-coach
category: Coaching
---

## Context
- Sprint / period: [...]
- Safety read: [1-5, how assessed]
- Format used: [name] — chosen because [...]

## What we gathered
[Events, facts, feelings from the data phase.]

## Insights (root causes)
[What the team discovered — in the team's words, not yours.]

## Action items (routed to next sprint backlog)
| Action | Owner | Due sprint | Backlog item |
|--------|-------|-----------|--------------|
| [action] | [member] | [sprint] | [id/link] |

## Carried out of scope
[Items outside the team's control — handed to the delivery manager.]

## Facilitator note
- Format effectiveness: [...]
- Recurring item watch: [any action item recycled from a prior retro]
```
