# Research Plan

Scenario: A product team is seeing high drop-off at checkout and needs a research plan to understand why users abandon the flow.

## Prompt

> We're seeing a 68% drop-off rate at our checkout flow. Analytics show most abandonment happens at the payment step, but we don't know why. We have:
> - Hotjar session recordings (300+ sessions from last month)
> - A Mixpanel funnel showing where in the payment step people drop
> - Access to 2,400 customers we could survey or recruit for interviews
> 
> We're a 12-person team. No dedicated researcher — I'm a PM doing this myself. Sprint is 2 weeks. Best practices on what should I do to understand the problem before we start designing solutions?
> 
> A few specifics for the response:
> 
> - **Open with a specific Research Question** at the top, grounded in the available evidence — not the generic "why do users drop off". Something like: "What are users experiencing in the seconds before they abandon the payment step, and what would have to be true for them to complete it?"
> - **Reframe block**: after the Mixpanel + Hotjar pass, restate the research question more specifically (e.g. "Now: users who see the address form on mobile are quitting — what's blocking them?").
> - **Recruitment criteria** must be explicit: users who attempted checkout in the last 30 days but didn't complete; mix of mobile vs desktop; mix of payment methods attempted (credit card, Apple/Google Pay, BNPL). Include screener questions to confirm fit.
> - **Qualitative sample size with rationale**: recommend 5-8 user interviews / unmoderated tests, citing Nielsen's finding that 5 reveals ~80% of usability issues with diminishing returns beyond 8.
> - **Discussion guide** with named question themes: (1) what they were trying to do, (2) what they expected at the payment step, (3) what made them hesitate, (4) what they did instead, (5) what would have made them complete it.
> - **PM-as-researcher bias guardrails**: a section warning that the PM is the design owner and therefore at risk of confirmation bias and leading questions. Specific guardrails: write open-ended questions only ("tell me about..." not "did you find X confusing?"), have a colleague review the discussion guide for leading framing, record sessions and re-listen for moments where you led the witness.
> - **Post-research action**: after analysis, hold a 1-hour synthesis workshop with design + engineering to translate findings into 2-3 hypothesis-driven design experiments — don't wait for a comprehensive research report.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Research Question

**"What are users experiencing in the 30 seconds before they abandon the payment step — and what belief, friction, or missing condition would have to change for them to complete the purchase?"**

This is more useful than "why do users drop off" because it focuses on the moment and the reversibility: it's asking what's in the way, not just that something is.

---

## Phase 1: Desk Work (Days 1–2)

Before recruiting anyone, exhaust what you already have.

**Mixpanel funnel — what to look for:**
- Where exactly within the payment step does volume drop (address entry → card entry → submit → error state → abandon)?
- Segment by device (mobile vs desktop) — checkout friction is often device-specific
- Segment by payment method attempted — Apple/Google Pay flows have different failure modes than card entry
- Look at time-on-step: are people spending 4+ minutes on a field that should take 30 seconds?
- Check error event rates — are there validation errors or API failures that correlate with the drop?

**Hotjar session recordings — what to watch for:**
- Rage clicks on specific fields or buttons
- Scroll depth: do people see the CTA?
- Form field focus/blur patterns — which fields do people abandon mid-form?
- Mobile keyboard behavior pushing elements off-screen
- Trust signals: do people scroll up to re-read product/shipping info before abandoning?

Watch 30–40 recordings. Tag each with: device, payment method, where they stopped, and one observation about what they were doing in the 20 seconds before leaving.

---

## Reframe Block

After the Mixpanel + Hotjar pass, you'll have a more specific problem to investigate. A likely reframe looks like one of these:

> "Mobile users on the card entry form are rage-clicking the CVV field and then abandoning — is it a UI issue, a keyboard-overlap issue, or a trust issue?"

> "Users who start with Apple Pay but fall back to card entry are dropping at 2x the rate — what breaks in the fallback experience?"

> "Users who see an address validation error don't retry — are they confused by the error message, or is the error itself a surprise?"

Restate the research question here with the specific friction point named. The interviews should test that hypothesis, not re-discover the whole funnel from scratch.

---

## Recruitment Criteria

**Who you want:**
- Attempted checkout on your site in the last 30 days
- Did not complete purchase (confirmed by your order data, not self-report)
- Mix: 50% mobile, 50% desktop
- Mix: credit/debit card users, Apple/Google Pay users, BNPL users (roughly proportional to your attempted payment method split from Mixpanel)
- Age range: don't over-filter — broad is better for a payment flow

**Who to exclude:**
- People who abandoned before reaching the payment step (they have a different problem)
- Existing loyal customers who have completed purchases many times (they may not represent the friction)

**Screener questions (email or Typeform, keep it short):**

1. "In the last 30 days, did you add items to your cart on [site] and start the checkout process?" (Must say yes)
2. "Did you complete your purchase?" (Must say no)
3. "Which device were you using when you tried to check out?" (Capture for quota)
4. "Which payment method did you try to use?" (Capture for quota)
5. "Are you available for a 30-minute video call in the next two weeks?" (Scheduling filter)

Reach out to your 2,400-person pool via email. Expect 5–10% response rate on screener, 40–60% conversion to booked sessions. Send to 200–300 people to get 8 sessions confirmed.

---

## Qualitative Sample Size

**Recommend 6–8 moderated user interviews.**

Nielsen's research (1993, replicated multiple times) shows that 5 users reveal approximately 80% of usability issues, with each additional user delivering sharply diminishing returns. With a checkout flow — a relatively constrained task with one success state — the problem space is bounded enough that 6 gets you strong signal. Go to 8 if your Mixpanel data shows two clearly distinct failure patterns (e.g., mobile card entry vs. BNPL fallback), since you're effectively running two mini-studies.

Do not run 20 interviews. You'll spend two weeks collecting data, then run out of sprint to act on it.

---

## Discussion Guide

**Session structure: 30 minutes per participant**

Intro (3 min): "I'm going to ask you about a recent experience. There are no right or wrong answers — we want to understand what happened from your perspective, not evaluate your choices. It's fine to say you don't remember."

**Theme 1 — Context: what they were trying to do**
- "Tell me about what brought you to [site] that day. What were you looking for?"
- "Walk me through what happened from when you landed on the site to when you left."

**Theme 2 — Expectations at the payment step**
- "When you got to the payment page, what were you expecting to see or do?"
- "Was there anything on that page that surprised you?"

**Theme 3 — The moment of hesitation**
- "Was there a specific moment where you paused or felt unsure? Tell me about that."
- "What were you thinking at that point?"
- "What were you looking at when you decided to stop?"

**Theme 4 — What they did instead**
- "After you left the site, what did you do? Did you buy somewhere else? Look for more information?"
- "Did you come back and try again?"

**Theme 5 — What would have made them complete**
- "If you could change one thing about that experience that would have made you go through with the purchase, what would it be?"
- "What would need to be true for you to feel confident completing that checkout?"

Close (2 min): "Is there anything else about that experience that felt off, or that I didn't ask about that you want to share?"

---

## PM-as-Researcher Bias Guardrails

You own the design decisions on this flow. That makes you the most dangerous possible person to run these interviews without safeguards.

**The risks:**
- You have a hypothesis about what's broken (you've looked at Hotjar). You will unconsciously guide participants toward confirming it.
- You may skip probing when a participant says something that contradicts your hypothesis, and lean in when they confirm it.
- Your tone of voice changes when you hear the answer you expected — participants pick this up and start telling you what you want to hear.

**Specific guardrails:**

**Write open-ended questions only.** Every question in your guide should start with "tell me about," "walk me through," or "what." Never: "Did you find the CVV field confusing?" Never: "Was the page too busy?" Those are leading — you've named the hypothesis in the question. If you want to know about the CVV field, ask "was there any part of the form that you had trouble with?" and wait.

**Have a colleague review the guide for leading framing.** Before you run session 1, share the guide with someone on the team who doesn't know what your Hotjar analysis found. Ask them: "Do any of these questions tell the participant what answer I'm looking for?" Revise anything they flag.

**Record every session and re-listen.** During the call you're focused on the next question. Re-listening surfaces the moments where you steered — where you said "so it sounds like X was the problem?" or moved on too quickly when a participant said something unexpected. Those are the most important moments.

**Separate note-taking.** Don't take notes live while moderating — you'll miss cues. Have a colleague join as a silent observer and note-taker, or use Otter/Grain to transcribe. Review the transcript against your notes before synthesizing.

---

## Post-Research Action

Do not write a research report. Reports get read once and filed.

After analysis, hold a **1-hour synthesis workshop** with design and engineering (aim for day after your last session):

- **30 min:** share raw observations, not conclusions. Walk the team through 3–4 session clips. Let the team see what you saw.
- **15 min:** group observations into themes on a shared board (FigJam, Miro, sticky notes).
- **15 min:** write 2–3 "How might we" statements, each in the form: "Users who [experience X] are [doing Y] because [belief/friction Z] — if we [change C] we expect [outcome O]."

Each HMW becomes a design experiment to prototype in the next sprint. You've gone from 68% drop-off to three testable hypotheses in two weeks, without a research report and without waiting for the perfect dataset.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.5/16.0 (97%) |
| Evaluated | 2026-05-27 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 66164 ms |
| Target cost | $0.1492 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Starts with a clear research question (not 'why do users drop off' but a more specific framing grounded in the available evidence) | PASS | Opens with: 'What are users experiencing in the 30 seconds before they abandon the payment step — and what belief, friction, or missing condition would have to change for them to complete the purchase?' |
| c2 | Prioritises existing data analysis (Hotjar recordings, Mixpanel funnel) before recommending new primary research — evidence before assumption | PASS | 'Phase 1: Desk Work (Days 1–2) — Before recruiting anyone, exhaust what you already have.' Mixpanel and Hotjar analysis explicitly precede recruitment. |
| c3 | Recommends a specific number of usability test or interview participants appropriate for the timeline (5-8 for qualitative, not vague 'a few users') | PASS | 'Recommend 6–8 moderated user interviews.' Nielsen's 1993 finding cited: 5 users reveal ~80% of usability issues; go to 8 if two distinct failure patterns. |
| c4 | Accounts for the PM's resource constraints — 2-week sprint, no researcher — and scopes the plan accordingly rather than recommending a full research programme | PASS | 'Do not run 20 interviews. You'll spend two weeks collecting data, then run out of sprint to act on it.' Post-research section says skip the report, go straight to 1-hour workshop. |
| c5 | Distinguishes between what the quantitative data can answer (where drop-off happens) and what qualitative research is needed for (why it happens) | PASS | Mixpanel/Hotjar sections frame WHERE questions; Reframe Block says 'interviews should test that hypothesis, not re-discover the whole funnel from scratch.' Quant/qual roles are explicit. |
| c6 | Includes a recruitment screener or participant criteria for interviews/tests — partial credit if criteria are mentioned but not specified | PARTIAL | Full screener with 5 numbered questions (confirmed checkout attempt, non-completion, device, payment method, availability) plus explicit inclusion/exclusion criteria. Ceiling is PARTIAL. |
| c7 | Produces a plan with sequenced steps and time estimates, not a list of research methods | PASS | Plan flows: Phase 1 Desk Work (Days 1-2) → Recruitment → Interviews (30 min each) → Synthesis workshop (day after last session). Ordered phases, not a methods menu. |
| c8 | Output reframes the research question — instead of 'why do users drop off at checkout', it becomes more specific based on the available evidence | PASS | Dedicated 'Reframe Block' section with three example reframes, e.g., 'Mobile users on the card entry form are rage-clicking the CVV field and then abandoning — is it a UI issue, a keyboard-overlap issue, or a trust issue?' |
| c9 | Output sequences existing-data analysis FIRST — Mixpanel funnel deep-dive, Hotjar session review — BEFORE recommending new primary research | PASS | Phase 1 (Days 1-2) covers Mixpanel then Hotjar with specific watch-list items before any mention of recruitment or interviews. |
| c10 | Output recommends a specific number of qualitative participants — 5-8 user interviews / unmoderated tests — with reasoning that 5 reveals 80%+ of usability issues, more adds diminishing returns | PASS | 'Recommend 6–8 moderated user interviews. Nielsen's research (1993, replicated multiple times) shows that 5 users reveal approximately 80% of usability issues, with each additional user delivering sharply diminishing returns.' |
| c11 | Output scopes the plan to a 2-week sprint with a single PM — does NOT recommend a multi-month research programme | PASS | Explicitly: 'Do not run 20 interviews. You'll spend two weeks collecting data, then run out of sprint to act on it.' Synthesis workshop replaces comprehensive report. |
| c12 | Output distinguishes what the quantitative data CAN answer (where in the funnel, which segment, device patterns) from what only qualitative can answer (why users hesitate, what they expected) | PASS | Mixpanel section lists sub-step drop, device segment, payment method, time-on-step. Hotjar lists rage clicks, field abandonment. Interviews cover hesitation, expectations, alternatives. |
| c13 | Output's plan is sequenced with time estimates per step — e.g. 'Days 1-2: Mixpanel deep-dive. Days 3-5: Hotjar session review. Days 6-7: recruit...' | PARTIAL | Only Phase 1 has explicit day labeling ('Days 1–2'). Subsequent phases (Hotjar watch, recruitment, interviews, synthesis) lack day-range estimates; 'day after last session' is relative, not sprint-anchored. |
| c14 | Output's recruitment criteria are specific — 'users who attempted checkout in the last 30 days but did not complete; mix of mobile and desktop; mix of payment methods attempted' | PASS | 'Attempted checkout on your site in the last 30 days... did not complete... Mix: 50% mobile, 50% desktop... credit/debit card users, Apple/Google Pay users, BNPL users.' Exact match on all three dimensions. |
| c15 | Output suggests an interview discussion guide with named question themes — what they were trying to do, what they expected at the payment step, what made them hesitate, what they did instead | PASS | Five named themes: (1) Context/what they were trying to do, (2) Expectations at the payment step, (3) The moment of hesitation, (4) What they did instead, (5) What would have made them complete. |
| c16 | Output addresses the PM-doing-research caveat — provides discussion-guide guardrails to avoid leading questions and confirmation bias | PASS | Full 'PM-as-Researcher Bias Guardrails' section: open-ended questions only, colleague guide review, record and re-listen, separate note-taker. Explicitly names confirmation bias risk. |
| c17 | Output recommends a quick post-research action — a synthesis workshop with the design / engineering team to translate findings into 2-3 hypothesis-driven design experiments | PARTIAL | 'Post-Research Action: Do not write a research report...hold a 1-hour synthesis workshop...write 2–3 HMW statements...Each HMW becomes a design experiment to prototype in the next sprint.' Ceiling is PARTIAL. |

### Notes

The output is exceptionally strong — it satisfies nearly every criterion fully, including the Reframe Block, bias guardrails, Nielsen-cited sample size rationale, and complete screener questions. The only gap is c13: beyond 'Days 1–2' for Phase 1, the remaining sprint phases lack explicit day-range anchors, making the timeline only partially scheduled.
