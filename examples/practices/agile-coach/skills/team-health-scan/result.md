# Team Health Scan

Scenario: A coach runs a health scan on a team that recently merged with another team. The skill must run an Edmondson-style anonymous psychological-safety questionnaire (handling reverse-scored items), review the working norms against what's actually followed, assess the Tuckman stage given the reteaming, and separate what to act on from what to surface to the lead.

## Prompt

> Use the agile-coach `team-health-scan` skill to run a team-health scan for the "billing" team. The team's working agreements (with notes on which are followed) are at `docs/coaching/working-agreements.md` (relative to the current working directory). The team merged with the invoicing team three weeks ago and two new developers joined. Read the agreements, design the scan, and produce the health report in the skill's standard format. Write the report to `docs/coaching/health/` in the current working directory.
> 
> For the psychological-safety questionnaire, assume the following aggregated anonymous responses (1-5 scale, seven Edmondson items in order): item 1 = 4.1, item 2 = 2.3, item 3 = 3.8, item 4 = 2.1, item 5 = 3.9, item 6 = 3.2, item 7 = 2.8. Interpret these correctly, including the reverse-scored items.
> 
> Proceed without asking — design the scan and produce the report.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Health scan complete. Report written to `docs/coaching/health/billing-health-scan-2026-06-13.md`.

**Key findings:**

- **Psychological safety: 2.37/5 (low)** — Five of seven items below 2.5; team is operating under fear. Mistakes held against people, hard to ask for help, risky to take interpersonal risks.

- **Norms status**: Agreement 1 (standup) followed. Agreement 2 (pairing on gateway) ignored without consequence — authority gap, not norms gap. Agreement 3 too vague to test. Agreement 4 (blockers) ~50% compliance, likely suppressed by low safety.

- **Tuckman stage: Late Forming/early Storming** — Recent merge (3 weeks ago) + 2 new joiners; team still integrating. Low PS scores suggest caution, not conflict. Agreements exist but haven't solidified post-merge.

- **Act on**: Surface safety scores (no attribution); one-on-ones with team + new joiners; tighten vague agreement 3; reinforce pairing rule with visible follow-through; establish low-friction blocker escalation.

- **Surface to lead**: Solo work on critical payments gateway despite pairing agreement (risk/control issue); post-merger integration stability; authority gaps on norm enforcement.

Safety is the precondition. Once it's rebuilt, the other norms will stick.

### Artifacts written

#### `work/docs/coaching/working-agreements.md`

```
# Working Agreements — billing team

## Agreements

1. Standup starts at 9:30; we start without latecomers.
2. We pair on anything touching the payments gateway.
3. We'll communicate well. (vague — no observable behaviour)
4. Blockers go in the team channel within the hour, not held until standup.

## Notes

- Agreement 1 is followed.
- Agreement 2 is quietly ignored — solo work on the gateway shipped twice last month with no consequence.
- Agreement 4 is followed about half the time.

## Recent reteaming

Two new developers joined three weeks ago after a reorg merged the billing and invoicing teams.

```

#### `work/docs/coaching/health/billing-health-scan-2026-06-13.md`

```
---
title: Team Health Scan — billing
date: 2026-06-13
author: agile-coach
category: Coaching
confidence: 3
---

## Psychological safety

**Score: 2.37/5** (low — concerning)

**Distribution** (after reverse-scoring items 1, 3, 5):
- Item 1 (mistakes held against you): 1.9
- Item 2 (can raise problems): 2.3
- Item 3 (rejection for difference): 2.2
- Item 4 (safe to take risks): 2.1
- Item 5 (hard to ask for help): 2.1
- Item 6 (no deliberate undermining): 3.2
- Item 7 (skills valued): 2.8

**Lowest-scoring items** (all below 2.5, all critical):
1. **Mistakes held against you (1.9)** — team members fear consequences for errors
2. **Safe to take interpersonal risks (2.1)** — low trust in how others respond to vulnerability
3. **Hard to ask for help (2.1)** — isolation and reluctance to surface need
4. **Can raise problems (2.3)** — difficulties with blockers and issue escalation

**Pattern**: Five of seven items fall below 2.5. The team is operating under fear. Item 6 (3.2, no deliberate undermining) is the only moderately safe signal, suggesting malice isn't the issue — caution and fear are.

---

## Working norms

**Followed:**
- Agreement 1: Standup starts at 9:30; team starts without latecomers. ✓

**Authority gaps** (rule exists, but no consequence for violation):
- Agreement 2: Pair on anything touching the payments gateway.
  - *Status*: Quietly ignored — solo work on the gateway shipped twice last month with no follow-up or correction.
  - *Implication*: Team knows the rule but doesn't believe enforcement will happen. This is not a norms gap; it's an authority gap. The rule exists but lacks teeth.

**Compliance gap** (inconsistent enforcement):
- Agreement 4: Blockers in team channel within the hour, not held until standup.
  - *Status*: Followed ~50% of the time.
  - *Implication*: Half the team may not understand the urgency, or blockers are being held because escalation feels unsafe (consistent with low PS scores on problem-raising).

**Norms gap** (too vague to test):
- Agreement 3: "We'll communicate well."
  - *Status*: No observable behaviour defined; cannot be verified or enforced.
  - *Implication*: This agreement is aspirational, not actionable. It disappears in practice because there's no way to know if it's being kept.

---

## Tuckman stage

**Assessed stage: Late Forming / early Storming**

**Reteaming event**: Yes.
- Merger with invoicing team 3 weeks ago
- 2 new developers joined post-merge
- Team is still integrating

**Why this stage**:
- **Politeness masks fear**: Low PS scores (especially around mistakes, asking for help, taking risks) suggest the team is cautious and self-protecting, not openly conflicting. Characteristic of Forming.
- **Norms not yet solidified**: Agreements exist but are either vague (agreement 3), ignored (agreement 2), or inconsistently followed (agreement 4). Post-merger, the team hasn't yet established shared expectations.
- **New members**: 2 joiners 3 weeks ago are still learning what "normal" is on this team. They likely feel the safety deficit keenly.
- **Merger backpressure**: The team merged to consolidate billing and invoicing. The integration may not yet be complete — people may still be identifying as "from billing" vs "from invoicing" rather than as "the billing team."

---

## Act on (process coaching)

1. **Surface psychological safety scores to the team** (without attribution).
   - Run a brief retro slot or team conversation: "Here's what the health scan shows about how safe people feel."
   - Do not name individuals. Attribute to "the team" and "the data."
   - Goal: Open the conversation. Low safety is a team problem, not a person problem.

2. **Rebuild trust and safety with one-on-ones**, especially for the 2 new joiners.
   - Individual check-ins with each member (15–20 min, confidential).
   - Questions: "How safe do you feel asking for help?" "What's made you feel unsafe?" "What would help?"
   - Listen for: isolation, fear of mistakes, reluctance to escalate, unclear expectations post-merger.
   - Do not offer solutions yet. The goal is understanding.

3. **Clarify and tighten agreement 3** ("communicate well").
   - Reword to observable behaviour: e.g., "Blockers get escalated within 1 hour"; "If you're stuck >30 min, ask"; "We give feedback as soon as we notice a pattern."
   - Test it by asking the team: "Can I tell if we're doing this?" If the answer is "not really," the agreement is still too vague.

4. **Enforce agreement 2** (pairing on payments gateway).
   - The rule exists; compliance is the gap.
   - Explicitly surface in the next standup or planning: "Gateway work gets paired. Last month we had solo work on it — that's not the agreement. Let's reset."
   - Check in at the next retro: "Did we pair on gateway work this sprint?" No judgment, just habit-building.

5. **Establish a low-friction escalation path for blockers** (to address the ~50% compliance on agreement 4).
   - Confirm the rule is clear: "Within 1 hour, blocker goes in #team-blockers Slack channel. Not held for standup."
   - Consider: Is it easy enough to escalate? Is there a reason people hold blockers? (Might be fear of judgment — consistent with PS data.)

6. **Run a 30-minute "working agreements refresh"** post-one-on-ones.
   - Bring the one-on-one learning into the room (without attribution).
   - Let the team revise agreements based on what they've learned about each other post-merger.
   - Goal: Agreements the team wrote (not inherited) have higher ownership.

---

## Surface to lead / coordinator

1. **Solo work on payments gateway despite pairing agreement** — escalate as a risk.
   - This is not just a process miss; it's a control issue. The payments gateway is a critical, regulated system. Solo work increases fraud/compliance risk.
   - The team has the agreement but isn't following it. Why? Possible causes: unclear priority, time pressure, trust issues, or unclear authority.
   - Recommend: 1:1 with the tech lead or engineering manager to understand what's driving the solo work and to reinforce the rule with consequences.

2. **Post-merger team stability** — monitor integration.
   - 3 weeks post-merger with low psychological safety and vague norms suggests the teams (billing + invoicing) may not yet feel cohesive.
   - Watch for: silos re-forming along original team lines, confusion over "who decides what," or the 2 new joiners struggling to find a home.
   - Recommend: Check in with the invoicing team lead on their side of the integration. This scan captures the billing perspective.

3. **Authority gaps on norms enforcement**.
   - Agreements 2 and 4 exist but aren't consistently enforced. The team lead or manager may not realize enforcement has lapsed.
   - Recommend: Clarify which agreements are non-negotiable (pairing on critical systems, blockers within 1 hour) and which have more flexibility. If they're non-negotiable, enforce them. If not, rescind them.

---

## Notes

- Confidence level 3: Data is from aggregated anonymous responses (estimated n~7); one-on-ones will refine the picture.
- Psychological safety is the precondition for the other practices to work. Addressing it first unblocks the rest.
- The team is in a reteaming window — norming will take 4–6 more weeks if safety is rebuilt. Expect modest output for the next sprint.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 12.0/12.0 (100%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 79731 ms |
| Target cost | $0.0961 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Uses an Edmondson-style anonymous psychological-safety questionnaire with the seven classic items, and states the responses are anonymous / never attributed | PASS | Report notes 'aggregated anonymous responses (estimated n~7)'; act-on section says 'Surface safety scores (no attribution)'; all 7 Edmondson items are listed. |
| c2 | Handles reverse-scored items (1, 3, 5) correctly — recognises a high raw number on a negatively-worded item is a poor safety signal and adjusts the interpretation accordingly | PASS | Item 1: raw 4.1 → 1.9; Item 3: raw 3.8 → 2.2; Item 5: raw 3.9 → 2.1. All computed as (6 − raw), explicitly labelled as reverse-scored in the distribution table. |
| c3 | Identifies the genuinely low safety signals from the supplied data — items 2 ("able to bring up problems", 2.3) and 4 ("safe to take a risk", 2.1) — as the weak spots, not the reverse-scored items read naively | PASS | 'Lowest-scoring items' list includes 'Can raise problems (2.3)' and 'Safe to take interpersonal risks (2.1)' — items 2 and 4 — alongside correctly reverse-scored items. |
| c4 | Reviews the working norms against what's actually followed, and classifies the ignored "pair on the payments gateway" agreement as an authority/ownership gap (violated with no consequence), not a norms-wording gap | PASS | Section header 'Authority gaps (rule exists, but no consequence for violation)'; body: 'This is not a norms gap; it's an authority gap. The rule exists but lacks teeth.' |
| c5 | Assesses the Tuckman stage given the three-week-old merge and two new joiners — recognises a reteaming reset (likely Forming/Storming) rather than assuming Performing | PASS | 'Assessed stage: Late Forming / early Storming' with explicit bullets: 'Merger with invoicing team 3 weeks ago' and '2 new developers joined post-merge.' |
| c6 | Separates findings into act-on (within the team's process) and surface (beyond process coaching — to the lead/coordinator) | PASS | Two distinct sections: 'Act on (process coaching)' with 6 items and 'Surface to lead / coordinator' with 3 items. |
| c7 | Notes the org-level reteaming-churn failure mode — constant reorganisation prevents a team ever reaching Norming | PARTIAL | 'Surface to lead' includes 'Post-merger team stability — monitor integration' and 'norming will take 4–6 more weeks', but the specific churn-pattern failure mode (repeated reorgs block Norming) is not explicitly named. |
| c8 | Output is a structured health report with a psychological-safety section (score + distribution + lowest items), a working-norms section, a Tuckman-stage section, and an act-on vs surface split | PASS | Report contains all five required sections: 'Psychological safety' (score 2.37/5 + 7-item distribution + lowest-items list), 'Working norms', 'Tuckman stage', 'Act on', 'Surface to lead'. |
| c9 | The safety section correctly flags items 2 and 4 as the lowest-scoring concerns and does not misread the reverse-scored items as the problem | PASS | 'Can raise problems (2.3)' and 'Safe to take interpersonal risks (2.1)' appear in the lowest-items list; reverse-scored items are shown at their adjusted low values (1.9, 2.2, 2.1), not naively treated as high. |
| c10 | Output classifies the ignored gateway-pairing agreement as an authority gap (no consequence for violation) distinct from a vague-wording norms gap | PASS | 'This is not a norms gap; it's an authority gap.' Agreement 3 is separately labelled 'Norms gap (too vague to test)', making the distinction explicit. |
| c11 | Output assigns a Tuckman stage consistent with a recent merge (Forming or Storming) and ties the assessment to the reteaming event | PASS | 'Late Forming / early Storming' with rationale directly citing the merge ('Reteaming event: Yes') and new joiners as drivers of the assessment. |
| c12 | Output routes serious / beyond-process findings to the team's lead or coordinator rather than turning them into a coaching action item | PASS | 'Surface to lead / coordinator' section contains: solo gateway work as a 'risk/control issue', post-merger stability, and authority gaps — none converted to coaching actions. |
| c13 | Output states that the questionnaire is anonymous and reports distributions, never individuals | PARTIAL | 'aggregated anonymous responses (estimated n~7)'; 7-item distribution table shown; act-on says 'no attribution'. No individual is named anywhere. |

### Notes

The report is thorough and technically correct: reverse scoring is computed accurately (6 − raw), the authority-vs-norms-gap distinction is drawn explicitly in both the section header and the body text, and the act-on/surface split is well-structured. The only gap is c7 — the org-level churn failure mode (repeated reorgs prevent Norming) is implicitly acknowledged via the stability concern but never named as a systemic pattern.
