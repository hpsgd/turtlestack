---
# Match the model the agent declares (sonnet) in
# plugins/product/ux-researcher/agents/ux-researcher.md. The runner otherwise
# falls back to the harness default (Haiku), which is not what the
# agent is designed to run on.
target-model: claude-sonnet-4-6
---

# Test: Research plan

Scenario: A product team is seeing high drop-off at checkout and needs a research plan to understand why users abandon the flow.

## Prompt


We're seeing a 68% drop-off rate at our checkout flow. Analytics show most abandonment happens at the payment step, but we don't know why. We have:
- Hotjar session recordings (300+ sessions from last month)
- A Mixpanel funnel showing where in the payment step people drop
- Access to 2,400 customers we could survey or recruit for interviews

We're a 12-person team. No dedicated researcher — I'm a PM doing this myself. Sprint is 2 weeks. Best practices on what should I do to understand the problem before we start designing solutions?

A few specifics for the response:

- **Open with a specific Research Question** at the top, grounded in the available evidence — not the generic "why do users drop off". Something like: "What are users experiencing in the seconds before they abandon the payment step, and what would have to be true for them to complete it?"
- **Reframe block**: after the Mixpanel + Hotjar pass, restate the research question more specifically (e.g. "Now: users who see the address form on mobile are quitting — what's blocking them?").
- **Recruitment criteria** must be explicit: users who attempted checkout in the last 30 days but didn't complete; mix of mobile vs desktop; mix of payment methods attempted (credit card, Apple/Google Pay, BNPL). Include screener questions to confirm fit.
- **Qualitative sample size with rationale**: recommend 5-8 user interviews / unmoderated tests, citing Nielsen's finding that 5 reveals ~80% of usability issues with diminishing returns beyond 8.
- **Discussion guide** with named question themes: (1) what they were trying to do, (2) what they expected at the payment step, (3) what made them hesitate, (4) what they did instead, (5) what would have made them complete it.
- **PM-as-researcher bias guardrails**: a section warning that the PM is the design owner and therefore at risk of confirmation bias and leading questions. Specific guardrails: write open-ended questions only ("tell me about..." not "did you find X confusing?"), have a colleague review the discussion guide for leading framing, record sessions and re-listen for moments where you led the witness.
- **Post-research action**: after analysis, hold a 1-hour synthesis workshop with design + engineering to translate findings into 2-3 hypothesis-driven design experiments — don't wait for a comprehensive research report.

## Criteria


- [ ] PASS: Starts with a clear research question (not "why do users drop off" but a more specific framing grounded in the available evidence)
- [ ] PASS: Prioritises existing data analysis (Hotjar recordings, Mixpanel funnel) before recommending new primary research — evidence before assumption
- [ ] PASS: Recommends a specific number of usability test or interview participants appropriate for the timeline (5-8 for qualitative, not vague "a few users")
- [ ] PASS: Accounts for the PM's resource constraints — 2-week sprint, no researcher — and scopes the plan accordingly rather than recommending a full research programme
- [ ] PASS: Distinguishes between what the quantitative data can answer (where drop-off happens) and what qualitative research is needed for (why it happens)
- [ ] PARTIAL: Includes a recruitment screener or participant criteria for interviews/tests — partial credit if criteria are mentioned but not specified
- [ ] PASS: Produces a plan with sequenced steps and time estimates, not a list of research methods

## Output expectations

- [ ] PASS: Output reframes the research question — instead of "why do users drop off at checkout", it becomes more specific based on the available evidence, e.g. "What are users experiencing in the seconds before they abandon the payment step, and what would have to be true for them to complete it?"
- [ ] PASS: Output sequences existing-data analysis FIRST — Mixpanel funnel deep-dive (which sub-step within payment, which payment methods correlate with drop-off), Hotjar session review (5-10 representative recordings of abandoners) — BEFORE recommending new primary research
- [ ] PASS: Output recommends a specific number of qualitative participants — 5-8 user interviews / unmoderated tests is typical for qualitative — with reasoning that 5 reveals 80%+ of usability issues, more adds diminishing returns
- [ ] PASS: Output scopes the plan to a 2-week sprint with a single PM — does NOT recommend a multi-month research programme; instead picks the highest-leverage methods that fit the constraint
- [ ] PASS: Output distinguishes what the quantitative data CAN answer (where in the funnel, which segment, time-of-day patterns, browser / device patterns) from what only qualitative can answer (why users hesitate, what they expected to see, what would have built confidence)
- [ ] PASS: Output's plan is sequenced with time estimates per step — e.g. "Days 1-2: Mixpanel deep-dive. Days 3-5: Hotjar session review (10 sessions × 30 min). Days 6-7: recruit 6 interview participants. Days 8-10: conduct interviews. Days 11-12: synthesise findings. Days 13-14: write recommendations."
- [ ] PASS: Output's recruitment criteria are specific — "users who attempted checkout in the last 30 days but did not complete; mix of mobile and desktop; mix of payment methods attempted" — not "a few users"
- [ ] PASS: Output suggests an interview discussion guide with named question themes — what they were trying to do, what they expected at the payment step, what made them hesitate, what they did instead
- [ ] PASS: Output addresses the PM-doing-research caveat — provides discussion-guide guardrails to avoid leading questions and confirmation bias (interviewer who is also the design owner is an inherent bias risk)
- [ ] PARTIAL: Output recommends a quick post-research action — a synthesis workshop with the design / engineering team to translate findings into 2-3 hypothesis-driven design experiments rather than waiting for a comprehensive research report
