# Coach Flow Metrics

Scenario: A team is drowning in work-in-progress and delivery is unpredictable. The coach must teach the team to read its own flow data — the four measures, the cycle-time scatterplot, the cumulative flow diagram — and justify WIP limits with Little's Law rather than preference, while staying on its side of the delivery-manager boundary.

## Prompt

> Use the agile-coach `coach-flow-metrics` skill to coach the "billing" team on its flow. Context: the team typically has about 20 items in progress at once and completes roughly 4 per week, delivery dates are unpredictable, and several items have been "in progress" for weeks. Teach the team to read its own flow data and produce the flow read and coaching plan in the skill's standard format. Write the output to `docs/coaching/` in the current working directory.
> 
> Proceed without asking — produce the flow coaching output.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Done. I've created the flow coaching document for the billing team at `docs/coaching/flow-coaching-billing.md`.

The coaching teaches the team to read four measures (cycle time, lead time, throughput, work-item age) and applies Little's Law to their situation: 20 WIP ÷ 4/week throughput = 5-week cycle time. The plan walks them through setting up scatterplot and CFD instruments in week 1, reading data as a team in week 2, and negotiating a WIP limit in week 3.

The key move: the team reads its own data, not a report you produce. The document sets clear boundaries — you coach the flow practice; the delivery manager reads numbers for status. This keeps the team on their instruments and prevents creating a metrics-reporting dependency.

### Artifacts written

#### `work/docs/coaching/flow-coaching-billing.md`

```
---
title: Flow Coaching — Billing Team
date: 2026-06-12
author: agile-coach
category: Coaching
---

## Current flow read

| Measure | Value | Read |
|---------|-------|------|
| WIP (current) | 20 items | Elevated; Little's Law predicts 5-week cycle time |
| Throughput | 4 items/week | Stable, but constrained by WIP |
| Cycle time (implied) | ~5 weeks | Calculated: 20 WIP ÷ 4 throughput = 5 weeks average |
| Aging items | Several (weeks+) | Items above 5-week mark indicate bottleneck or size variation |
| Delivery predictability | Low | Symptom: cycle time variability + queue depth |

## The flow problem in one sentence

**Your team is accumulating work faster than it's completing it, creating a backlog inside the workflow.** Twenty items in progress means each item waits 4–5 weeks on average before touching your hands. Unpredictable delivery follows from unpredictable wait time.

## Little's Law: the why behind WIP limits

This is physics, not preference:

```
Average Cycle Time = Average WIP / Average Throughput
```

**Your numbers:**
- Current: 20 WIP ÷ 4/week = **5-week cycle time**
- If you cut WIP to 10: 10 ÷ 4 = **2.5-week cycle time** (no staff changes, no process changes)
- If you cut to 6: 6 ÷ 4 = **1.5-week cycle time**

The implication: **halving WIP halves how long work sits waiting**. Your unpredictable delivery isn't a person problem — it's a congestion problem.

## What the team needs to read itself

You're going to stop reporting "status" and start reading your own instruments. Here are the four measures and what each one tells you:

### 1. Cycle Time: Start to Done
- **Definition:** How long from when someone picks up work until it's complete?
- **Why it matters:** This is *active* time on the team. It shows whether your process is efficient.
- **How to read it:** Plot each completed item on an X/Y scatterplot — X is completion date, Y is how long it sat in progress. The spread shows variability. If most items cluster at 1 week and one at 8 weeks, something broke on that item — investigate it.
- **Your target:** Reduce variability first, then push the 50th percentile down.

### 2. Lead Time: Requested to Done
- **Definition:** How long from when work is *requested* (entered the system) until it's *done*?
- **Why it matters:** This is what a stakeholder experiences. It includes queue time — work waiting to be started.
- **How to read it:** Lead time = queue time + cycle time. If lead time is 8 weeks but cycle time is 2, you're spending 6 weeks *waiting* to start.
- **Your target:** Reduce queue time by limiting WIP.

### 3. Throughput: Items Completed per Week
- **Definition:** How many items finish each week? Track the trend.
- **Why it matters:** Shows team capacity and whether you're improving or degrading.
- **How to read it:** A flat 4/week is stable but gives you no slack for emergency work. If it's dropping (4 → 3 → 2), you have a blocker.
- **Your target:** Stabilize it, then increase it by removing the constraint.

### 4. Work-Item Age: "How long has this been in progress?"
- **Definition:** For items *currently* in your workflow, how long since they started?
- **Why it matters:** Shows which item needs attention *right now* — before it becomes a crisis.
- **How to read it:** Every standup, call out items older than 2 weeks (your implied 85th percentile). Ask: "What's blocking this?" If you can't name the blocker in 30 seconds, it needs triage.
- **Your target:** Nothing older than 3 weeks without explicit escalation.

## CFD: System-level picture

A Cumulative Flow Diagram charts how many items live in each workflow state (To Do → In Progress → In Review → Done) over time. The team reads the *band widths*:

- **Even-width bands rising steadily → Healthy.** Work flows through consistently.
- **Widening "In Progress" band → Bottleneck.** Items entering faster than leaving. This is your current state.
- **Flat top line → No throughput.** Nothing is completing.
- **Steep jump at end → Batch release.** Work piles up, then dumps all at once. Unpredictable to stakeholders.

**Your CFD likely shows:** In Progress band widening (20 items), queue building, sporadic releases. The widening band is your diagnosis — work enters faster than it leaves.

## Coaching plan: What you'll do starting this week

### Week 1: Establish the instruments
1. **Set up the scatterplot** in your board tool (Jira, Linear, Azure DevOps — most have flow reports built in).
   - X-axis: completion date
   - Y-axis: cycle time (days from start to done)
   - Add percentile lines: 50th, 85th, 95th
   - This is your primary diagnostic. You'll read it every standup.

2. **Set up the CFD** (same tool). Ensure it shows: To Do, In Progress, Review, Done.
   - Read the band widths. If In Progress is widening, name why.

3. **Post both charts in your standup space** (Slack, wiki, whatever you use). Make them visible — not in a report you pull once a month.

### Week 2: Read the data as a team
1. **In standup,** spend 2 minutes reading the scatterplot:
   - What's the 50th and 85th cycle time?
   - Are there outliers above 85th? If yes, say the item name and what it's stuck on.
   - Is variability going up or down?

2. **Read the CFD:**
   - Is In Progress widening, stable, or shrinking?
   - If widening, where in the workflow is work piling up? (Entry? Review? Handoff?)

3. **Call out work-item age:**
   - Every item in progress >2 weeks gets named. What's the blocker?

### Week 3: WIP negotiation
By now you'll see the In Progress band clearly. Bring the leadership team and this proposal:

> "We currently complete 4 items/week with 20 in progress. Little's Law predicts 5-week cycle time. To halve it to 2.5 weeks (and predictability), we'd limit WIP to 10. That means saying 'no' to new work entering until we finish items. Are we willing to do that?"

Frame it as: *"More predictable delivery, not fewer features — just different rhythm."*

### Cadence
- **Daily standup:** 2 minutes reading scatterplot + CFD + aging items. Name one thing to unblock.
- **Weekly:** Trend check. Is cycle time improving? Throughput stable?
- **Monthly:** Review with leadership. Propose WIP adjustment if needed.

## Boundary: Your role vs. delivery manager's

- **You read:** scatterplot, CFD, aging items, trends. You coach the team on *what they mean*.
- **Delivery manager reads:** the same numbers for *status* — "are we on track?" That's different from coaching.
- **You don't do:** produce status reports, track individual item percentages, become the metrics service.

The team reads its own data. You teach the team what to look for. The delivery manager glances at the dashboard for status. Clear roles.

## Success criteria

You'll know this is working when:

1. **The team brings the scatterplot to standup, not the other way around.** You're not pulling it for them.
2. **Someone says,** "Item X is aging; we need to unblock it" — without being asked.
3. **WIP drops intentionally.** "We're saying no to new work this week because we're at our limit."
4. **Cycle time improves.** 5 weeks → 3 weeks → 2 weeks, with variability shrinking.
5. **Stakeholder satisfaction increases.** Predictable delivery beats surprising delivery.

---

## Next step: Schedule the coaching session

We'll walk through your board tool together, set up the charts, and run through one standup reading cycle. After that, it's your practice — you read, you act, we check in monthly.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 12.0/13.0 (92%) |
| Evaluated | 2026-06-12 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 42695 ms |
| Target cost | $0.0682 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Establishes the four measures by name — cycle time, lead time, throughput, work-item age — with what each one answers | PASS | Four numbered sections: '1. Cycle Time: Start to Done', '2. Lead Time: Requested to Done', '3. Throughput: Items Completed per Week', '4. Work-Item Age', each with a 'Why it matters' explanation. |
| c2 | Correctly distinguishes cycle time (start-to-done, active time) from lead time (requested-to-done, includes queue time) rather than conflating them | PASS | Cycle time: 'active time on the team'; Lead time: 'lead time = queue time + cycle time. If lead time is 8 weeks but cycle time is 2, you're spending 6 weeks *waiting* to start.' |
| c3 | Explains the cycle-time scatterplot as the primary diagnostic, including percentile lines and that an item above the 85th percentile is aging and needs attention now | PASS | 'This is your primary diagnostic.' Week 1 setup: 'Add percentile lines: 50th, 85th, 95th'. Standup: 'Are there outliers above 85th? If yes, say the item name and what it's stuck on.' |
| c4 | Explains how to read the cumulative flow diagram — widening band = WIP accumulating / bottleneck, flat top line = nothing completing | PASS | 'Widening "In Progress" band → Bottleneck. Items entering faster than leaving.' and 'Flat top line → No throughput. Nothing is completing.' |
| c5 | Applies Little's Law correctly to the supplied numbers — 20 WIP ÷ 4 per week ≈ 5-week cycle time — and shows that halving WIP to 10 halves cycle time without adding people | PASS | '20 WIP ÷ 4/week = 5-week cycle time' and 'If you cut WIP to 10: 10 ÷ 4 = 2.5-week cycle time (no staff changes, no process changes)' |
| c6 | Justifies WIP limits with Little's Law as physics, not preference, and notes the law's conditions (stable flow, no wild item-size variation) | PARTIAL | 'This is physics, not preference' is explicit. However, conditions for the law to hold (stable flow, no wild item-size variation) are never stated as conditions on Little's Law itself. |
| c7 | Hands the instruments to the team — sets the team up to read its own scatterplot/CFD rather than the coach becoming the flow-report service | PASS | 'You're going to stop reporting "status" and start reading your own instruments.' and 'The team reads its own data. You teach the team what to look for.' |
| c8 | Holds the boundary — the coach coaches the flow practice; the delivery manager only reads the numbers for status | PARTIAL | Explicit 'Boundary: Your role vs. delivery manager's' section: 'Delivery manager reads: the same numbers for *status* — "are we on track?" That's different from coaching.' |
| c9 | Output is a structured flow-coaching artifact with a current flow read, a CFD read, a Little's Law application, and a coaching plan | PASS | Document contains: 'Current flow read' table, 'CFD: System-level picture' section, 'Little's Law: the why behind WIP limits' section, and 'Coaching plan: What you'll do starting this week' section. |
| c10 | The Little's Law section shows the concrete calculation (≈5-week current cycle time from 20 WIP / 4 throughput, halving to ≈2.5 weeks at WIP 10), not just the formula | PASS | Three bullet calculations shown: current '20 WIP ÷ 4/week = 5-week cycle time', WIP 10: '10 ÷ 4 = 2.5-week cycle time', WIP 6: '6 ÷ 4 = 1.5-week cycle time'. |
| c11 | Output distinguishes cycle time from lead time explicitly and ties the difference to queue time | PASS | Lead Time section: 'lead time = queue time + cycle time. If lead time is 8 weeks but cycle time is 2, you're spending 6 weeks *waiting* to start.' |
| c12 | Output flags the long-running in-progress items as aging items needing attention now (above the typical percentile), not just "some items are slow" | PASS | Work-Item Age: 'call out items older than 2 weeks (your implied 85th percentile). Ask: "What's blocking this?"' and 'Every item in progress >2 weeks gets named.' |
| c13 | Output's coaching plan sets up the team to read its own data on its own cadence rather than positioning the coach as the report producer | PASS | Week 2: 'In standup, spend 2 minutes reading the scatterplot' — team reads, not coach. Cadence section: daily/weekly/monthly team-owned reading rituals. |
| c14 | Output notes a condition or caveat on Little's Law (e.g. wildly varying item sizes break the averages) rather than presenting it as unconditional | FAIL | Little's Law is presented without explicit caveats. 'Size variation' is mentioned in the aging-items table row but not framed as a condition on Little's Law applicability. |

### Notes

The artifact is strong across the board — all four flow measures, correct cycle/lead distinction, concrete Little's Law arithmetic, and clear team-owns-the-instruments framing. The only gaps are that Little's Law conditions (stable flow, item-size variation caveat) are never explicitly stated, which causes c6 to land at PARTIAL and c14 to fail.
