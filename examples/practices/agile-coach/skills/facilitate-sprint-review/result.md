# Facilitate Sprint Review

Scenario: A coach is asked to fix a sprint review that has become a polished slideshow to management. The skill must reframe it as a working session that inspects the increment against the DoD and adapts the backlog, draw out passive stakeholders, watch for the HIPPO effect, and keep the product manager owning the backlog.

## Prompt

> Use the agile-coach `facilitate-sprint-review` skill to coach the "billing" team's sprint review. Context: the review has turned into a 30-slide presentation to the head of product, who does most of the talking; other stakeholders sit silent and nod; the team often shows screenshots rather than running software, and the backlog never actually changes as a result. Write the review coaching output to `docs/coaching/` in the current working directory. Respond in the skill's standard format.
> 
> Proceed without asking — coach the review and produce the output.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Done. I've written coaching output for the billing team's sprint review to `docs/coaching/billing-sprint-review-coaching.md`.

The document diagnoses the core anti-pattern: the review has become a broadcast ceremony (30-slide presentation to an executive audience) with zero backlog adaptation — the entire point of the event. It then provides four concrete shifts:

1. **Reframe with the product manager** — this is a working session, not a status demo
2. **Show running software** — let stakeholders explore live, not watch screenshots
3. **Structure participation** — use round-robin or dot voting to draw out quiet stakeholders and counter the HIPPO effect
4. **Adapt the backlog visibly** — the only success metric is whether the backlog actually changes

The document includes red flags to watch, a concrete next-sprint agenda (45–60 min structure), and success metrics so the team can measure whether the coaching took. The first moves are explicit: product manager reframes, team prepares one item to run live, and the group plans the prioritisation structure.

The backlog won't change as long as the ceremony stays performative. That reframe is the lever.

### Artifacts written

#### `work/docs/coaching/billing-sprint-review-coaching.md`

```
---
title: Sprint Review Coaching — Billing Team
date: 2026-06-12
author: agile-coach
category: Coaching
---

## Current State (Anti-Pattern)

Your sprint review has drifted into a **broadcast ceremony** rather than a collaborative working session:

- **30-slide presentation** to the head of product
- **Head of product dominates** the speaking time; other stakeholders sit silent
- **Screenshots** shown instead of running software live
- **Backlog never changes** — no new items added, no reprioritisation, no dropped work

This is **Zombie Scrum**: the ceremony has the form but has lost its function. The Scrum Guide defines the sprint review as an **inspection of the increment AND adaptation of the product backlog**. Right now you're doing inspection (one-way, to an executive audience) with zero adaptation. The backlog is a passenger in your process, not the output.

---

## What Must Change

### 1. Reframe: This is a working session, not a demo

**Before your next review, the product manager must reset expectations with the head of product.** The review exists to change the backlog in response to what stakeholders learn by inspecting the increment. Executives participate to provide input, not to applaud the team.

**Coaching move:** Have the product manager send a 2-sentence note 24 hours before the review:
> "The sprint review is a working session where we inspect what we shipped and adapt the backlog based on what we learn. This is collaborative — stakeholders will have live running software to explore and decisions to make about priorities. It's not a status presentation."

This reframe is non-negotiable. If the head of product expects slides and applause, the session will default back to broadcast mode.

### 2. Show working software; invite stakeholders to use it

**Replace screenshots with a live, explorable system.** Stakeholders learn by doing, not by watching a curated demo.

**Concrete move:** Start each backlog item with "Here's what we built — go try it" and hand the keyboard to a stakeholder for 2–3 minutes. Let them poke at it, ask questions, discover edge cases. Let them feel friction. If a stakeholder finds a problem, that's a new backlog item in the room.

This serves three purposes:
- You surface real issues (that screenshots hide)
- Stakeholders become collaborators instead of observers
- You get authentic feedback, not polite nods

### 3. Structure the conversation to draw out quiet stakeholders

The **HIPPO effect** (Highest-Paid Person's Opinion) is why your backlog doesn't change. The head of product fills the silence, and everyone else defers. Silence is a failure mode — it means you're not getting real input.

**Concrete moves:**
- After each item, don't ask "Any questions?" (which gets silence). Instead: name a stakeholder and ask directly: "[name], you own this area — what's your reaction? Would you prioritise this next or something else?"
- Use **round-robin prioritisation**: go around the table and ask each stakeholder what ONE item from the backlog they'd pull into the next sprint. Capture the votes.
- Use **dot voting** on candidates: give each stakeholder 3 dots to put on backlog items they think matter most. No talking, just dots. It surfaces disagreement without the loudest voice winning.

These structures work because they force participation instead of defaulting to silence.

### 4. Own the backlog adaptation

**The backlog must visibly change during or immediately after the review.** This is the only measure of success.

**What changed looks like:**
- New items added (from stakeholder input, from issues discovered in live demo)
- Items reordered (based on stakeholder priorities revealed in round-robin or dot voting)
- Items dropped (because the market moved, or stakeholders discovered the problem is already solved)
- Clarifications added to scope or acceptance criteria (because stakeholders asked hard questions)

**Coaching move for the product manager:** After the collaborative conversation, write the changes to the backlog *in the room*. Don't defer to a spreadsheet later. Let stakeholders see the backlog shift in response to their input. This closes the loop and proves the session wasn't performative.

---

## Red Flags to Watch

- **Slides outnumber conversation.** If you're showing more than 5 slides total (one per item max), you're drifting toward a presentation.
- **Stakeholders don't interrupt.** If no one asks a question, challenges a decision, or suggests a different priority, the session isn't collaborative.
- **No one asks "what should we do next?"** The review should end with stakeholder input on what's next. If that question never surfaces, the backlog won't change.
- **Screenshots instead of live software.** Pixels are safe; live software reveals friction. Friction creates decisions.
- **The head of product leaves having said 80% of the words.** The team and other stakeholders should be talking more.

---

## Your Next Sprint Review: Concrete Agenda

**9:00–9:05** — Framing (product manager)  
> "We've shipped X, Y, Z this sprint. Today we're here to understand how these land with you and what should come next. We'll show you working software, get your input, and the backlog will change based on what we learn."

**9:05–9:35** — Inspect increment (one item per ~10 min)  
> Team shows working software (live, not slides). Hands keyboard to a stakeholder for 2–3 min to explore. Stakeholder asks questions. Issues/ideas are noted as backlog candidates.

**9:35–9:45** — Collaborative prioritisation  
> Round-robin: each stakeholder names one thing from the backlog they'd prioritise next. OR dot voting on 5 backlog candidates. Capture input.

**9:45–9:55** — Backlog adaptation  
> Product manager rewrites the backlog in the room (move items, add new ones, drop old ones) based on the conversation. Stakeholders see their input become visible work.

**9:55–10:00** — Close  
> Product manager: "Here's what changed. Here's what we're taking into planning next sprint."

---

## Success Metrics

You'll know this is working when:

- [ ] Backlog has 3+ items reordered or added after the review (not zero)
- [ ] Stakeholders ask at least 5 substantive questions during increment inspection
- [ ] At least one new item is added to the backlog as a result of live demo exploration
- [ ] The product manager spends less than 20% of the air time talking (team and stakeholders fill the rest)
- [ ] The review takes 45–60 minutes, not 90+ (fewer slides = faster)
- [ ] Someone disagrees about priorities in the room and it gets worked through (not deferred)

---

## Your First Move

1. **Product manager**: Reframe the sprint review with the head of product. Send the 2-sentence note. Confirm this is a working session, not a status presentation.
2. **Team**: Pick one item for your next review and prepare it to run live, not as screenshots.
3. **All**: Plan for the round-robin prioritisation move. Have 5 backlog candidates ready to vote on.

The backlog won't change if the ceremony stays performative. This reframe is the lever.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 9.5/11.0 (86%) |
| Evaluated | 2026-06-12 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 44113 ms |
| Target cost | $0.0682 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Reframes the review as a collaborative working session that inspects the increment and adapts the backlog — explicitly not a demo or status update to management | PASS | Section 1 heading: 'Reframe: This is a working session, not a demo'; body: 'broadcast ceremony rather than a collaborative working session' |
| c2 | States that only Definition-of-Done-complete work should be presented and flags the screenshot-instead-of-running-software problem | PARTIAL | Screenshots flagged explicitly ('Replace screenshots with a live, explorable system') but no explicit statement that only DoD-complete work should be shown. |
| c3 | Names the HIPPO effect (the head of product dominating) and gives a concrete move to counter it so quiet stakeholders contribute | PASS | Section 3: 'The HIPPO effect (Highest-Paid Person's Opinion) is why your backlog doesn't change'; concrete moves: round-robin, dot voting, direct named prompts. |
| c4 | Keeps the product manager / product owner owning the backlog conversation — the coach facilitates the working-session craft, does not take over the backlog | PASS | Section 4: 'Coaching move for the product manager: After the collaborative conversation, write the changes to the backlog *in the room*.' |
| c5 | Defines review success as the backlog visibly changing (items added, reordered, dropped), not as applause or a clean presentation | PASS | Success Metrics: 'Backlog has 3+ items reordered or added after the review (not zero)'; Section 4 lists added, reordered, dropped items as what success looks like. |
| c6 | Gives at least one concrete facilitation move to convert passive stakeholders into participants (hand driving to a stakeholder, direct named prompts, dot voting on next priorities) | PASS | 'hand the keyboard to a stakeholder for 2–3 minutes'; 'don't ask Any questions? Instead: name a stakeholder and ask directly'; dot voting described explicitly. |
| c7 | Keeps the review distinct from sprint planning — inspecting/adapting the backlog is the review's job, not deciding the next sprint's scope | PARTIAL | Agenda close: 'Here's what we're taking into planning next sprint' implies handoff to planning, but no explicit statement distinguishing review from sprint planning. |
| c8 | Output is a structured review-coaching artifact with a framing note (working session vs demo), the increment inspection against DoD, backlog adaptation, and coaching notes | PASS | Document has clearly labelled sections: framing (Section 1), increment inspection (Section 2), backlog adaptation (Section 4), red flags, concrete agenda, and success metrics. |
| c9 | Output records whether items not meeting the DoD were presented and flags that for coach-definition-of-done | FAIL | No section or flag in the artifact records whether DoD-incomplete items were shown; screenshots are flagged as anti-pattern but DoD compliance of presented items is not assessed. |
| c10 | Output names the HIPPO/dominance issue with the specific stakeholder (head of product) and a mitigation | PASS | Red Flags: 'The head of product leaves having said 80% of the words'; Section 3 names HIPPO with the head of product specifically and provides round-robin/dot voting mitigations. |
| c11 | Output frames the measure of success as backlog change, and assigns backlog ownership to the product manager, not the coach | PASS | Success Metrics lead with backlog items changed; Section 4 coaching move explicitly directs the product manager to write backlog changes in the room. |
| c12 | Output offers concrete drift-correction moves (hand driving to a stakeholder, replace "any questions?" with a direct named prompt) rather than a generic "make it collaborative" | PARTIAL | Exact matches: 'hand the keyboard to a stakeholder' and 'don't ask Any questions? Instead: name a stakeholder and ask directly' — both verbatim examples from the criterion. |

### Notes

Strong output that hits all major themes — HIPPO framing, running software, PM ownership, backlog-change as the success metric. The only meaningful gap is c9: the artifact never records or flags whether DoD-incomplete items were actually presented, which was a specific coaching-output requirement.
