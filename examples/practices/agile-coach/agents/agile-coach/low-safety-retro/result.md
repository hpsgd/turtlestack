# Low Safety Retro

Scenario: A delivery manager asks the coach to help with a team whose retrospectives keep producing the same action items sprint after sprint, and where people seem reluctant to speak openly. The coach must read the situation, hold its facilitation boundary, address safety before format, and route outcomes correctly — responding in its standard coaching methodology and deliverable format.

## Prompt

> Use the `agile-coach` agent to help with the following situation, and respond in its standard coaching methodology and structured deliverable format.
> 
> The "billing" engineering team has run six retrospectives this quarter. The last three all produced the same two action items — "improve test coverage" and "reduce interruptions" — and neither moved. In the last retro, only two of the seven developers spoke; the rest stayed quiet while the tech lead talked. The delivery manager wants you to "just write them a better set of action items and tell them to follow the working agreement."
> 
> Work the problem as the agile coach. Do not ask me clarifying questions first — proceed with what you'd do, stating any assumptions.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

**Assumptions I'm stating upfront** (no prior retrospective docs to read in this environment):
- Safety level assessed from behavioural evidence, not a pre-session poll — treating it as 2/5
- "Improve test coverage" and "reduce interruptions" have appeared verbatim three consecutive times — this isn't a prioritisation problem, it's an insight problem
- The tech lead is not malicious; they fill silence because silence is uncomfortable and nobody else moves
- The delivery manager has good intent but is mis-diagnosing the problem as a documentation/compliance problem

---

## Coaching Assessment: Billing Engineering Retrospectives

### What is actually broken (not what the delivery manager thinks is broken)

Three symptoms are visible. They point to one root cause.

**Symptom 1 — Recycled action items.** "Improve test coverage" and "reduce interruptions" appearing three times unchanged is diagnostic: the team is skipping the Generate Insights phase entirely. They go data → action with no root cause work. The Wheel of Fortune anti-pattern. The action items aren't wrong; they're treating the first-order symptom without ever asking *why coverage degrades sprint after sprint* or *where the interruptions are actually coming from and who has the power to stop them.*

**Symptom 2 — Voice concentration.** Five of seven developers said nothing. This is not a participation style issue. When most of the room goes silent and one voice (a person with positional authority over career outcomes) fills the space, you are seeing psychological safety failure. People have learned that speaking costs more than staying quiet. You don't fix this by enforcing a working agreement — you fix it by changing the conditions that make silence rational.

**Symptom 3 — Zero movement on action items.** Items that don't move are either: (a) not owned by a specific person, (b) not resourced against sprint capacity, (c) not within the team's actual power to fix, or (d) never genuinely committed to in the first place. Given the silence pattern, (d) is the most likely. Nobody objected in the room, but nobody believed it either.

**Root cause hypothesis:** The retrospective format is producing *performance of agreement*, not *genuine reflection and commitment*. The room has a status gradient that suppresses honest signal. The result is a polite ritual that wastes an hour and changes nothing.

---

### Reframing the delivery manager request

> "Just write them a better set of action items and tell them to follow the working agreement."

This request, if executed, will make things worse. Here's why:

Writing action items *for* the team removes the one ingredient that makes action items move: ownership. If the coach writes them, the team didn't commit to them — they were assigned to them. That's a task list, not a retrospective outcome. It also signals that the retrospective is a management compliance exercise, which will further suppress honest participation.

"Tell them to follow the working agreement" treats a safety and facilitation problem as a rule-following problem. You can't mandate psychological safety into existence.

**What I'll tell the delivery manager:**

> "I hear the frustration — three retros, same items, no movement. That's a real signal. But the signal is that the retrospective format is broken, not that the team needs better instructions. If I write their action items for them, I'm training them that the retro is something done *to* them. That makes your problem worse next quarter. Here's what I'm going to do instead, and why I think it'll actually move the items that matter."

The delivery manager's role in the intervention: carry the external blockers (systemic interruptions from outside the team — if that's what "reduce interruptions" actually means) as *their* action items, not the team's.

---

### Pre-session: Conversation with the tech lead

Before redesigning the retro format, I need a private conversation with the tech lead. Not a confrontation — a transparency conversation.

Key points:
- "I noticed you carried most of the conversation in the last retro. I don't think that's your intent, but when you're the most senior voice in the room and fill silences, it becomes hard for others to enter. I want to try a different format that builds in structure so you don't have to carry it — and so you hear things you're probably not hearing right now."
- "There may be things people aren't saying because they're not sure how you'll receive them. That's not a criticism of you — it's a pattern I see in a lot of teams. The goal is to get the room working."
- Ask: "Is there anything you know is not being said in retros? What do you think is actually behind 'reduce interruptions'?"

That last question is diagnostic. If the tech lead knows — and often they do — it tells me whether this is a safety problem or an insight problem (or both).

---

## Retrospective Plan — Billing Engineering

### Context
- Period: Q3, six retrospectives in; third consecutive retro with recycled action items
- Safety read: **2/5** — assessed from behaviour (5/7 silent, one voice dominating, zero item movement). Not polled; polling a 2/5-safety team about safety is circular. The format must assume low safety without requiring people to declare it.
- Format chosen: **TRIZ + 1-2-4-All** — Liberating Structures combination

---

### Why this format

A standard Start/Stop/Continue or 4Ls round-robin will reproduce the same dynamic: tech lead speaks, others nod, items get written, nothing happens. The format must structurally interrupt that pattern *before* the conversation begins.

**TRIZ** ("What would we have to do to guarantee these problems never get fixed?") is chosen because:
- It's psychologically safer to answer — you're not criticising the team, you're being hypothetically destructive
- It surfaces the real barriers that polite retros skip
- "Improve test coverage" and "reduce interruptions" have been recycled because nobody has said what's *actually stopping them*. TRIZ makes it safe to say it

**1-2-4-All** wraps TRIZ because:
- Ideas form in private (individual write) before any status gradient applies
- Pairs discuss before the full group — two people is low-risk enough that quieter voices speak
- By the time the group hears it, five other people have already heard a version of it, which normalises it

---

### Session design (90 minutes)

#### Phase 1 — Set the Stage (10 min)

Open with Kerth's Prime Directive:

> "Regardless of what we discover, we understand and truly believe that everyone did the best job they could, given what they knew at the time, and given the skills and resources available. We're here to look at the system, not the people."

**Check-in:** One word, round the room, in a random order (not hierarchical). "Describe how you arrived today in one word." No elaboration, no response from others. This gets every voice in the room once before the work starts. Silence before the check-in becomes statistically anomalous after it.

State the timebox and the format. "We're going to do something a bit different today — I'll explain as we go. The only rule is: there are no wrong answers."

---

#### Phase 2 — Gather Data via TRIZ (20 min)

*Facilitator instruction to room:*

> "I want you to think about the two things that have been on our retro list for three sprints: test coverage and interruptions. Instead of asking 'how do we fix them', I want to ask the opposite question."

Write on the board (or virtual equivalent):

> **"What would we have to do — actively and deliberately — to make absolutely sure test coverage never improves and interruptions never decrease?"**

**1-2-4-All structure:**
- **Individual (4 min):** Everyone writes their answers silently. No sharing yet. Stickies or digital equivalent, one idea per note.
- **Pairs (4 min):** Share with one other person. Add to, don't filter. The pair builds a short list.
- **Groups of four (4 min):** Two pairs combine. Identify the 2-3 most powerful sabotage strategies.
- **All (8 min):** Each group of four shares. Facilitator clusters on the board without editorialising.

*What this surfaces that polite retros don't:*
- "We'd make sure the people causing the interruptions never heard about the cost" → who is causing interruptions? From where?
- "We'd never allocate sprint time for test work, just say we'll do it when it's quiet" → capacity is the real constraint
- "We'd make sure the tech lead reviews everything before it goes out, so only they have time to write tests" → knowledge concentration problem
- "We'd make sure nobody felt safe saying the interruptions come from the product manager" → the room will laugh, but it'll be true

The facilitator's job here is to notice what's being *avoided* in the inverses. That's where the root cause lives.

---

#### Phase 3 — Generate Insights (25 min)

Take the sabotage list. Ask the room:

> "Which of these are we actually doing?"

Not hypothetically. Right now, in this team, in this sprint. Dot vote (3 dots each). The highest-voted items are the ones the room believes are real.

For the top 2-3 items, run a lightweight 5 Whys:

*Example (illustrative, not prescriptive):*
- "We never allocate sprint time for test work."
- Why? "Because we're always behind on feature delivery."
- Why? "Because estimates don't include time for test writing."
- Why? "Because the definition of done doesn't include test coverage as a criterion."
- Why? "Because it was never agreed, or it was agreed and not enforced."
- Why? "Because the person who would enforce it doesn't have visibility into coverage numbers before review."

Now you have a specific, actionable insight — *not* "improve test coverage" but "add coverage threshold to the definition of done and route coverage reports to sprint review."

Same pass on interruptions: who is interrupting, what type, what's their expectation, who could change the expectation, what would it take.

**Facilitator discipline during this phase:** Do not let the room generalise. "We just need better discipline" is not an insight. Push: "What does that look like specifically? What would have to be different on Tuesday morning?"

---

#### Phase 4 — Decide What to Do (20 min)

*Rule stated to the room before this phase:*

> "We're going to come out of this with no more than three action items. Not a list of aspirations — three specific things with one owner each that can go into next sprint. If it can't go into next sprint with a real owner, it doesn't leave this room."

Each proposed action goes through a three-question filter (facilitator asks these aloud):
1. Is this within our team's control? (If no → carry to delivery manager)
2. Does one specific person own it? (If no → not an action item yet)
3. Can it go into next sprint's backlog this week? (If no → break it down or defer)

Actions routed as backlog items — not a parking lot, not "the team will look at this." A named person creates the ticket before end of day.

The delivery manager's action items (items outside team control) are written separately and handed over in writing, not just mentioned.

---

#### Phase 5 — Close (15 min)

**Return on Time Invested (ROTI):** Quick show of hands, 1-5. "Did this hour feel worth it?" Not for ego — for calibration. A 2 or 3 tells you the format needs more adjustment. A 4-5 tells you the structure worked.

**Appreciation round (optional, 3 min):** "If you want to name one person who said something useful today, do it now." Not mandatory. Don't force it. But if safety has cracked open even slightly, this cements it.

**Confirm actions aloud:** Read the three items, their owners, their sprint. "Everyone agree this is what we decided?" One final consent check — not consensus, consent.

---

### After the session: What I watch for

**If the sabotage answers are surface-level and safe** ("we'd write bad specs" rather than anything that implicates a person or a system) — safety is lower than 2/5. The next intervention is not another retro format; it's a team health scan and a series of 1:1s before the next retrospective.

**If the tech lead re-enters the conversation during pair work** — gentle redirect: "Let's keep the pairs going for two more minutes." Do it once, calmly. If it happens again, name it after the session in a 1:1, not in the room.

**If the same items appear again next sprint** — the issue is not the retrospective. The issue is sprint planning: test work is not being scheduled as capacity. That's a sprint planning audit, not a retro intervention.

---

### Output file (to be written after the session)

```markdown
---
title: Retrospective — Billing Engineering — 2026-06-13
date: 2026-06-13
author: agile-coach
category: Coaching
---

## Context
- Period: Q3, retro 7 (three consecutive recycled-item retros preceding this)
- Safety read: 2/5 — assessed from prior behaviour; not polled pre-session
- Format used: TRIZ + 1-2-4-All — chosen to break voice-concentration pattern
  and surface root causes polite round-robins have not reached

## What we gathered
[Populated post-session from TRIZ outputs and dot-vote results]

## Insights (root causes)
[Populated post-session in team's own words]

## Action items (routed to next sprint backlog)
| Action | Owner | Due sprint | Backlog item |
|--------|-------|-----------|--------------|
| [specific, not "improve coverage"] | [named dev] | Sprint N+1 | [ticket ID] |

## Carried out of scope (delivery manager action items)
[Items the team cannot control — e.g. cross-team interruption sources]

## Facilitator note
- Format effectiveness: [ROTI score, observed participation]
- Recurring item watch: "improve test coverage" — appeared retros 4, 5, 6.
  If it appears again in retro 8, escalate: sprint planning is not allocating
  capacity for test work. This is a planning problem, not a retro problem.
```

---

### Summary for the delivery manager

Three things to relay:

1. **The action items aren't the problem.** Writing better ones for the team will produce polite compliance and no movement. The team needs to generate their own, from their own root cause analysis.

2. **The retro has a facilitation problem, not a content problem.** Five of seven people were silent. That's a safety signal, not a participation style. The format is being changed to structurally prevent one voice from filling the space.

3. **You have action items too.** If "reduce interruptions" refers to sources outside the team — product, stakeholders, other squads — those are yours to carry. They don't belong on a dev team's retro action list if the dev team can't action them.

The goal isn't a better-formatted retro document. The goal is a room where people say what's actually true, find the actual cause, and commit to something they actually believe they'll do.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 13.5/14.0 (96%) |
| Evaluated | 2026-06-13 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 105433 ms |
| Target cost | $0.2882 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | The coach holds its facilitation boundary — it explicitly declines to write the team's action items or working agreement for them, and explains it coaches the team to author its own | PASS | "Writing action items *for* the team removes the one ingredient that makes action items move: ownership. If the coach writes them, the team didn't commit to them — they were assigned to them." |
| c2 | The coach pushes back on the delivery manager's "just write them better action items" request rather than complying — naming that authored-for-them content is not coaching | PASS | Dedicated section 'Reframing the delivery manager request' opens with: "This request, if executed, will make things worse." |
| c3 | Psychological safety is treated as the priority given only two of seven spoke — the coach addresses safety before retrospective format polish | PASS | Safety read 2/5 stated upfront in assumptions; Symptom 2 identifies "psychological safety failure" before any format discussion; TRIZ+1-2-4-All chosen explicitly to address safety. |
| c4 | The recurring identical action items are correctly diagnosed as a skipped insight phase / Wheel of Fortune anti-pattern, not just "the team isn't trying hard enough" | PASS | "the team is skipping the Generate Insights phase entirely. They go data → action with no root cause work. The Wheel of Fortune anti-pattern." |
| c5 | The coach names that a working agreement violated repeatedly with no consequence is an authority/ownership gap, not a facilitation gap — and routes it accordingly | PARTIAL | Output rejects the DM's working-agreement mandate as "treats a safety and facilitation problem as a rule-following problem" — but never names the authority/ownership gap specifically. |
| c6 | The response distinguishes what the coach facilitates from what the coach actually does (does NOT do delivery, status, or own the content) | PASS | Pre-session conversation is coaching; team generates content through TRIZ; DM carries organisational items; coach role is strictly facilitation throughout. |
| c7 | Action items / improvements are routed into the next sprint backlog with an owner — not left as a parking lot or assigned to "the team" | PASS | "Actions routed as backlog items — not a parking lot, not 'the team will look at this.' A named person creates the ticket before end of day." |
| c8 | The coach references its failure cap — same dysfunction three retros running with no movement signals an organisational cause to escalate, not coaching harder | PARTIAL | "If it appears again in retro 8, escalate: sprint planning is not allocating capacity for test work. This is a planning problem, not a retro problem." |
| c9 | Output is structured as a coaching engagement artifact (Context / Observations / Insights / Action items / what-was-coached-vs-done) rather than loose prose | PASS | Structured with named sections: Coaching Assessment, What is actually broken, Root cause hypothesis, Retrospective Plan with Context/Safety read, Session phases, Output file template, Summary for DM. |
| c10 | Output includes a safety read or an explicit plan to assess psychological safety before running the next retrospective | PASS | "Safety read: 2/5 — assessed from behaviour (5/7 silent, one voice dominating, zero item movement). Not polled; polling a 2/5-safety team about safety is circular." |
| c11 | Output's observations cite the specific evidence given (two of seven spoke, three retros with the same two stalled actions) rather than generic claims | PASS | "Five of seven developers said nothing" and "'Improve test coverage' and 'reduce interruptions' appearing three times unchanged" — both drawn directly from the prompt's specifics. |
| c12 | Output names at least one concrete facilitation technique to counter the loudmouth/HIPPO dominance pattern (e.g. silent writing, 1-2-4-All, dot voting) so the quiet five get heard | PASS | 1-2-4-All named and fully explained; "Ideas form in private (individual write) before any status gradient applies"; dot voting used in Phase 3. |
| c13 | Output separates team-fixable problems from organisational ones, and escalates the organisational ones to the lead/coordinator rather than coaching the team harder | PASS | "Is this within our team's control? (If no → carry to delivery manager)" and "You have action items too. If 'reduce interruptions' refers to sources outside the team — those are yours to carry." |
| c14 | Output explicitly refuses to author the team's content (action items, working agreement) on the team's behalf and frames the coach's job as facilitating the team to produce its own | PASS | "Writing action items *for* the team removes the one ingredient that makes action items move: ownership... That's a task list, not a retrospective outcome." |
| c15 | Output routes the recurring "improve test coverage" item toward a likely technical-practice/capability cause (a CTO/engineering-leadership concern) rather than treating it as a pure process item | PARTIAL | 5 Whys example traces coverage → DoD missing threshold → sprint capacity not allocated. Routes to planning/DoD, not explicitly to CTO/engineering-leadership. |

### Notes

The output is exceptional in breadth and depth — it correctly names the Wheel of Fortune anti-pattern, runs a full TRIZ+1-2-4-All design, separates organisational from team-owned blockers, and explicitly rejects writing content for the team. The only gaps are that it never names the working-agreement problem as an authority/ownership gap (c5) and the test-coverage escalation path points to sprint planning rather than engineering-leadership capability (c15).
