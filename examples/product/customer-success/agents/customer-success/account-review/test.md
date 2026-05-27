---
# Match the model the agent declares (sonnet) in
# plugins/product/customer-success/agents/customer-success.md. The runner otherwise
# falls back to the harness default (Haiku), which is not what the
# agent is designed to run on.
target-model: claude-sonnet-4-6
---

# Test: Account review

Scenario: A CS manager needs to prepare for a QBR with an enterprise customer that has shown a significant usage drop over the past 6 weeks.

## Prompt


I need to prep for a QBR with Hartwell Manufacturing next week. They're one of our largest accounts — $420k ARR, 3-year contract, renewal comes up in 8 months.

Here's what I know:
- They have 340 licensed seats, but only 89 active users in the last 30 days (was 210 six weeks ago)
- Their champion, Sarah Kowalski (VP of Operations), went on maternity leave 6 weeks ago
- A new IT director started 2 months ago and has been "reviewing all software spend"
- They haven't logged a support ticket in 45 days (they used to log 8-12/month)
- They attended our last QBR but the exec sponsor didn't show up

What should I be doing, and what should this QBR cover?

## Criteria


- [ ] PASS: Identifies the health status as red or at-risk based on the signals — 57% usage drop, champion absence, new IT director reviewing spend, exec sponsor no-show
- [ ] PASS: Connects the usage drop to the champion's maternity leave (6 weeks aligns exactly) rather than treating it as a product problem
- [ ] PASS: Flags the new IT director as a risk and recommends a strategy to identify and engage this stakeholder before the QBR
- [ ] PASS: Does NOT recommend an expansion conversation — this account is unhealthy and expansion would be inappropriate per the CS agent's constraints
- [ ] PASS: Recommends specific pre-QBR actions: re-engaging day-to-day users, identifying who has backfilled Sarah's role, getting an exec sponsor confirmed before the meeting
- [ ] PASS: Frames the QBR agenda around value realised and risk mitigation — not a product demo or upsell
- [ ] PARTIAL: Recommends a health score review across all 5 dimensions — partial credit if health is assessed qualitatively but not scored across adoption/engagement/relationship/value/commercial dimensions
- [ ] PASS: Identifies the 8-month renewal timeline as creating urgency and recommends a recovery milestone before the renewal conversation

## Output expectations

- [ ] PASS: Output classifies Hartwell as RED / at-risk — explicitly naming all four signals (57% MAU drop 210→89, champion on leave, new IT director reviewing spend, exec sponsor no-show) as compounding evidence, not just one
- [ ] PASS: Output computes the actual usage drop numerically — "MAU dropped from 210 to 89, a 58% reduction" or similar — and connects the timing to the champion's 6-week leave (the drop and the leave align almost exactly)
- [ ] PASS: Output explicitly does NOT propose expansion or upsell — recognising the account is unhealthy, with the constraint that expansion only follows healthy accounts
- [ ] PASS: Output names the new IT director as a critical risk and proposes a specific pre-QBR action — identifying the IT director by name, requesting a 1:1 introduction before the QBR, demonstrating value to that stakeholder
- [ ] PASS: Output proposes finding Sarah Kowalski's interim coverage — who's running operations in her absence, and getting that person engaged as a temporary champion
- [ ] PASS: Output's pre-QBR action list is concrete with timing — e.g. "this week: identify IT director and request 1:1; week before QBR: confirm exec sponsor attendance; day before: send pre-read with usage analysis"
- [ ] PASS: Output's QBR agenda is structured around value realised + risk mitigation — NOT product demos or new features — with sections like "Value to date" (from the previous 16-month period), "What changed in the last 6 weeks", "Path to renewal in 8 months"
- [ ] PASS: Output addresses the 8-month renewal as creating urgency — proposing a 90-day recovery milestone (e.g. "MAU restored to ~150 by end of Q2") so the renewal conversation in month 8 can happen from a position of strength
- [ ] PASS: Output addresses the dropped support tickets (8-12/month → 0 in 45 days) as a SILENT-departure signal, not "they figured it out" — explaining that customers stop logging tickets when they stop using the product
- [ ] PARTIAL: Output performs a qualitative health assessment across the 5 dimensions (adoption, engagement, relationship, value realisation, commercial) — partial credit if assessed without explicit scoring
