# Account Review

Scenario: A CS manager needs to prepare for a QBR with an enterprise customer that has shown a significant usage drop over the past 6 weeks.

## Prompt

> I need to prep for a QBR with Hartwell Manufacturing next week. They're one of our largest accounts — $420k ARR, 3-year contract, renewal comes up in 8 months.
> 
> Here's what I know:
> - They have 340 licensed seats, but only 89 active users in the last 30 days (was 210 six weeks ago)
> - Their champion, Sarah Kowalski (VP of Operations), went on maternity leave 6 weeks ago
> - A new IT director started 2 months ago and has been "reviewing all software spend"
> - They haven't logged a support ticket in 45 days (they used to log 8-12/month)
> - They attended our last QBR but the exec sponsor didn't show up
> 
> What should I be doing, and what should this QBR cover?

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Before writing the QBR document, let me assess this account honestly — the signals here are serious enough that the pre-QBR actions matter as much as the document itself.

---

## Situation Assessment

This account is **Critical**, not At Risk. Here's why:

| Signal | What it means |
|---|---|
| 210 → 89 active users in 6 weeks | Adoption dropped 58% — likely tied directly to Sarah's absence |
| Champion on maternity leave | No internal advocate; no one selling value to the new buyer |
| New IT Director "reviewing spend" | An unfamiliar economic buyer with no relationship and an incentive to cut |
| Zero support tickets for 45 days | Disengagement, not satisfaction |
| Exec sponsor no-show | No executive investment in the relationship |
| Renewal in 8 months | Not enough time to course-correct slowly |

The adoption drop and champion absence are almost certainly correlated — Sarah's team was driving usage, and without her, those users have drifted back to old workflows. The new IT Director is filling the vacuum with a cost lens rather than a value lens.

---

## What You Should Be Doing Right Now (Before the QBR)

These actions need to happen before next week, not at the QBR:

**1. Get to the IT Director before the QBR.**
Don't let their first meaningful interaction with your product be a formal review. Request a 30-minute "context-setting call" framed as "I want to make sure you have a complete picture before we meet with the broader team." The goal is to understand their concerns and introduce yourself — not to pitch. If they're hostile at the QBR and you've never spoken, you've already lost.

**2. Find Sarah's interim.**
Someone is managing Operations while Sarah is on leave. Find out who. That person is your temporary champion candidate. Call them before the QBR — not to sell, but to understand how things are going operationally.

**3. Get the exec sponsor to commit to attending.**
The sponsor no-showed last time. For this QBR, you need them in the room given the renewal timeline. Frame it as: "With renewal coming up in Q1 and some important strategic decisions ahead, I want to make sure we have the right people in the conversation." If they won't attend, that's critical information — escalate internally.

**4. Pull your usage data by team/department.**
You need to know whether the adoption drop is uniform (everyone stopped) or concentrated (Sarah's direct team stopped). If it's concentrated, you can show the IT Director that 89 active users are getting value — and that the path to more is a people problem, not a product problem.

**5. Prepare a concise business case.**
The IT Director needs a one-page answer to "why are we paying $420k for this?" before they walk into a QBR. Have it ready to send as pre-read.

---

## QBR Document

```markdown
# Quarterly Business Review: Hartwell Manufacturing

**Quarter:** Q2 2026
**Prepared by:** [CSM Name]
**Date:** June 2026
**Renewal date:** January 2027 (8 months)
**Next QBR:** September 2026

---

## Executive Summary

Hartwell Manufacturing's account is at a critical juncture. During the first half of the quarter,
active usage was strong — 210 users engaged monthly, demonstrating meaningful adoption across
Operations. Over the past six weeks, active usage has declined to 89 users, a drop that coincides
with Sarah Kowalski's maternity leave and indicates that adoption was concentrated in her team
rather than embedded across the organisation.

With renewal eight months away and a new IT Director reviewing software spend, we are prioritising
stabilisation: re-establishing an internal champion, re-engaging the teams that have gone quiet,
and building a clear value case for the renewal conversation. This QBR is the starting point for
that work — not the end of it.

We are not here to declare success. We are here to be transparent about where we are, commit to
specific actions, and ask for your partnership in making this investment work for Hartwell.

---

## Health Overview

| Dimension | Status | Signal |
|---|---|---|
| Product Adoption | Critical | 89 active / 340 licensed (26%); down from 210 six weeks ago |
| Relationship | At Risk | Champion on leave; exec sponsor engagement low |
| Support | At Risk | Zero tickets in 45 days; disengagement pattern, not resolution |
| Commercial | At Risk | $420k ARR; renewal January 2027; new economic buyer unfamiliar with value |
| Strategic Alignment | At Risk | No exec sponsor at last QBR; no interim champion identified |

**Composite: Critical. Trend: Declining.**

---

## Value Delivered This Quarter

### What Worked (When We Were at Full Adoption)

At peak adoption — 210 active users in March and April — [insert your product's core value here,
translated into Hartwell's operational outcomes]:

- **[Metric 1]:** [e.g., "Operations teams processed X% more work orders per week using the
  automated routing workflows — approximately [N] hours per week recovered across the team"]
- **[Metric 2]:** [e.g., "Reporting that previously required [N] hours of manual Excel work is
  now generated in under 10 minutes by 3 users"]
- **[Metric 3]:** [specific outcome tied to their operational goals]

> **Note:** Insert your actual product metrics here. The goal is to show what 210 active users
> were achieving — this becomes the "what we're leaving on the table" argument for the IT Director.

### Goals Scorecard

| Goal (from last QBR) | Target | Actual | Status | Notes |
|---|---|---|---|---|
| [Goal 1 from last QBR] | [target] | [actual] | Met / Partial / Missed | [context] |
| [Goal 2 from last QBR] | [target] | [actual] | Met / Partial / Missed | [context] |
| Expand active users to [N] | [target] | 89 active (from 210 peak) | Missed | Sarah's leave removed primary adoption driver |

### Usage Trends

| Metric | 8 weeks ago | Today | Change |
|---|---|---|---|
| Monthly active users | 210 | 89 | -58% |
| Seat utilisation | 62% | 26% | -36pp |
| Support tickets/month | 8–12 | 0 (45 days) | Disengaged |
| [Feature X usage] | [value] | [value] | [delta] |
| [Feature Y usage] | [value] | [value] | [delta] |

---

## Honest Assessment: What Happened

The adoption decline over the past six weeks is real, and we want to address it directly rather
than present a number that looks better than the underlying situation.

**The champion dependency:** Sarah Kowalski was the primary driver of adoption within Operations.
Her team was the most active cohort, and her advocacy created the conditions for users to engage.
With her on leave, that driving force went with her — and users drifted back to prior workflows.
This tells us adoption was not yet self-sustaining. That is our problem to solve, not Sarah's.

**The engagement silence:** The drop in support tickets looks like good news on a dashboard. It
is not. When engaged users encounter problems, they raise them. When disengaged users encounter
problems, they stop using the product. Forty-five days of silence is a disengagement signal.

**What we should have done:** We should have identified a backup champion before Sarah's leave,
and we should have proactively reached out when usage began declining rather than waiting for
this QBR. We didn't do that. We're doing it now.

---

## Risks and Mitigation Plan

| Risk | Severity | Evidence | Action |
|---|---|---|---|
| No internal champion | Critical | Sarah on leave; no identified interim; usage freefall | Identify and onboard interim champion with [CSM name] by [date] |
| New IT Director unfamiliar with value | Critical | "Reviewing all software spend" with no prior relationship | [CSM name] to meet with IT Director before QBR; deliver one-page ROI summary |
| Adoption not self-sustaining | High | 58% drop tied to single champion | Structured re-engagement: team-by-team usage audit, workflow reanchoring sessions |
| Renewal risk | High | 8 months to renewal; current health Critical | Stabilisation must begin now; renewal readiness review in September |
| Exec sponsor disengagement | Medium | No-show at last QBR | Request exec sponsor commitment to September QBR; identify escalation path |

---

## Recommendations for Next Quarter

These are specific commitments — from us and from Hartwell:

| Action | Owner | Timeline | Success metric |
|---|---|---|---|
| Identify interim Operations champion to work with CSM while Sarah is on leave | Hartwell (IT Director or COO) | By June 15 | Named individual confirmed |
| Usage audit: map active vs. inactive users by department; identify drop-off reasons | [CSM name] | By June 20 | Audit delivered to Hartwell sponsor |
| Re-engagement sessions: 90-min working sessions with each inactive team lead | Joint (CSM + interim champion) | July–August | 3 sessions completed; baseline usage per team established |
| Renewal readiness review (internal) | [CSM name] + [AE name] | July | Go/no-go on renewal strategy |
| Exec QBR (September) with exec sponsor confirmed | [CSM name] to confirm with Hartwell | By July 1 | Sponsor confirmed on calendar |
| Deliver ROI summary for IT Director | [CSM name] | Before this QBR | Document delivered; meeting held |

**Target for September QBR:** Active users back above 150 (44% utilisation) with a named interim
champion driving adoption independently.

---

## What We Are Not Recommending

Given Hartwell's current health, we are not proposing any expansion, upsell, or additional
seat purchase at this time. Our focus is entirely on demonstrating and rebuilding the value of
the existing investment. Expansion conversations belong in September — if we have delivered on
the commitments above.

---

## For the Renewal Conversation (January 2027)

We have eight months. The renewal conversation should be a formality, not a fire drill — but
only if we act now. Here is what success looks like by the time we reach January:

- Active utilisation above 60% (200+ of 340 seats engaged)
- At least two internal champions — not one — who can advocate for renewal independently
- A documented ROI case that the IT Director can present to their leadership
- Exec sponsor actively engaged and present at the September QBR

If we are not on track by September, we will tell you that in September — not in December.

---

## Appendix

### Support Ticket History

| Period | Volume | Avg resolution time | Notable issues |
|---|---|---|---|
| Q4 2025 | 8–12/month | [time] | [themes] |
| Q1 2026 | [volume] | [time] | [themes] |
| Q2 2026 (last 45 days) | 0 | N/A | No tickets lodged |

### Feature Adoption Breakdown

| Feature | Adoption rate | Active users | Trend |
|---|---|---|---|
| [Feature 1] | [%] | [N] | [up/down/flat] |
| [Feature 2] | [%] | [N] | [up/down/flat] |
| [Feature 3 — low adoption] | [%] | [N] | [opportunity/risk] |

### Seat Utilisation by Department (if available)

| Department | Licensed | Active | Utilisation |
|---|---|---|---|
| Operations (Sarah's team) | [N] | [N] | [%] — primary drop-off |
| [Department 2] | [N] | [N] | [%] |
| [Department 3] | [N] | [N] | [%] |
```

---

## The Conversation That Actually Matters

The QBR document is the frame. The conversation you need to have is this:

**To the IT Director:** "You're reviewing software spend — that's exactly the right question to ask. I want to give you the full picture: adoption was strong at 210 users, it dropped when Sarah went on leave, and I didn't catch it fast enough. Here's what it was delivering when it was working, here's what recovering that looks like, and here's what I'm asking from your team to make that happen."

**To whoever shows up in the exec chair:** "We need you to help us identify who owns Operations while Sarah is away. Without an internal champion, we can't rebuild adoption — that's not a product problem, it's a people problem, and you're the person who can solve it."

**Do not** walk into this QBR with a deck that makes it look like everything is fine. The IT Director will have already pulled the seat utilisation report. If your narrative doesn't match their data, you lose all credibility for the renewal conversation.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/17.0 (100%) |
| Evaluated | 2026-05-27 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 99573 ms |
| Target cost | $0.2037 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Identifies the health status as red or at-risk based on the signals — 57% usage drop, champion absence, new IT director reviewing spend, exec sponsor no-show | PASS | Situation Assessment table lists all four signals; output states 'This account is **Critical**, not At Risk' with explicit reasoning. |
| c2 | Connects the usage drop to the champion's maternity leave (6 weeks aligns exactly) rather than treating it as a product problem | PASS | 'The adoption drop and champion absence are almost certainly correlated' and 'adoption was concentrated in her team rather than embedded across the organisation.' |
| c3 | Flags the new IT director as a risk and recommends a strategy to identify and engage this stakeholder before the QBR | PASS | Pre-QBR action #1: 'Get to the IT Director before the QBR' with a 30-min context-setting call; Risk table rates this 'Critical' with 'meet with IT Director before QBR; deliver one-page ROI summary.' |
| c4 | Does NOT recommend an expansion conversation — this account is unhealthy and expansion would be inappropriate per the CS agent's constraints | PASS | Explicit section 'What We Are Not Recommending': 'we are not proposing any expansion, upsell, or additional seat purchase at this time.' |
| c5 | Recommends specific pre-QBR actions: re-engaging day-to-day users, identifying who has backfilled Sarah's role, getting an exec sponsor confirmed before the meeting | PASS | Five numbered pre-QBR actions: IT Director outreach, Find Sarah's interim, exec sponsor commitment, usage data by team, and business case preparation. |
| c6 | Frames the QBR agenda around value realised and risk mitigation — not a product demo or upsell | PASS | QBR sections: Value Delivered This Quarter, Honest Assessment: What Happened, Risks and Mitigation Plan — no product demo or new feature sections. |
| c7 | Recommends a health score review across all 5 dimensions — partial credit if health is assessed qualitatively but not scored across adoption/engagement/relationship/value/commercial dimensions | PARTIAL | Health Overview table covers Product Adoption, Relationship, Support, Commercial, Strategic Alignment with Critical/At Risk labels — qualitative, no numeric scores. |
| c8 | Identifies the 8-month renewal timeline as creating urgency and recommends a recovery milestone before the renewal conversation | PASS | 'Target for September QBR: Active users back above 150 (44% utilisation)'; 'renewal eight months away...prioritising stabilisation.' |
| c9 | Output classifies Hartwell as RED / at-risk — explicitly naming all four signals (57% MAU drop 210→89, champion on leave, new IT director reviewing spend, exec sponsor no-show) as compounding evidence, not just one | PASS | Situation Assessment table explicitly lists all four signals; classified as 'Critical'; framing is 'compounding' not isolated. |
| c10 | Output computes the actual usage drop numerically — "MAU dropped from 210 to 89, a 58% reduction" or similar — and connects the timing to the champion's 6-week leave (the drop and the leave align almost exactly) | PASS | '210 → 89 active users in 6 weeks \| Adoption dropped 58% — likely tied directly to Sarah's absence' in the table. |
| c11 | Output explicitly does NOT propose expansion or upsell — recognising the account is unhealthy, with the constraint that expansion only follows healthy accounts | PASS | 'What We Are Not Recommending': 'not proposing any expansion, upsell, or additional seat purchase at this time. Our focus is entirely on demonstrating and rebuilding the value of the existing investment.' |
| c12 | Output names the new IT director as a critical risk and proposes a specific pre-QBR action — identifying the IT director by name, requesting a 1:1 introduction before the QBR, demonstrating value to that stakeholder | PASS | Risk table: 'New IT Director unfamiliar with value \| Critical'; pre-QBR action: 30-min context-setting call + one-page ROI summary before QBR. |
| c13 | Output proposes finding Sarah Kowalski's interim coverage — who's running operations in her absence, and getting that person engaged as a temporary champion | PASS | Pre-QBR action #2: 'Find Sarah's interim. Someone is managing Operations while Sarah is on leave. Find out who. That person is your temporary champion candidate.' |
| c14 | Output's pre-QBR action list is concrete with timing — e.g. "this week: identify IT director and request 1:1; week before QBR: confirm exec sponsor attendance; day before: send pre-read with usage analysis" | PASS | Recommendations table has dates: 'By June 15', 'By June 20', 'Before this QBR'; pre-QBR section says 'These actions need to happen before next week, not at the QBR.' |
| c15 | Output's QBR agenda is structured around value realised + risk mitigation — NOT product demos or new features — with sections like "Value to date" (from the previous 16-month period), "What changed in the last 6 weeks", "Path to renewal in 8 months" | PASS | QBR doc sections: Value Delivered This Quarter, Honest Assessment: What Happened, Risks and Mitigation Plan, For the Renewal Conversation — no demos or feature sections. |
| c16 | Output addresses the 8-month renewal as creating urgency — proposing a 90-day recovery milestone (e.g. "MAU restored to ~150 by end of Q2") so the renewal conversation in month 8 can happen from a position of strength | PASS | 'Target for September QBR: Active users back above 150'; July-August re-engagement sessions; 'If we are not on track by September, we will tell you that in September — not in December.' |
| c17 | Output addresses the dropped support tickets (8-12/month → 0 in 45 days) as a SILENT-departure signal, not "they figured it out" — explaining that customers stop logging tickets when they stop using the product | PASS | 'The drop in support tickets looks like good news on a dashboard. It is not... When disengaged users encounter problems, they stop using the product. Forty-five days of silence is a disengagement signal.' |
| c18 | Output performs a qualitative health assessment across the 5 dimensions (adoption, engagement, relationship, value realisation, commercial) — partial credit if assessed without explicit scoring | PARTIAL | Health Overview table: Product Adoption, Relationship, Support, Commercial, Strategic Alignment — qualitative Critical/At Risk labels, no numeric scoring. |

### Notes

The output is exceptionally thorough, covering every criterion with specific evidence. Both partial-ceiling criteria (c7, c18) correctly receive partial credit as the health assessment is qualitative without explicit numeric scoring across dimensions.
