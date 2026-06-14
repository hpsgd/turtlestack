# Product Prioritisation

Scenario: Competing stakeholder requests land on the CPO's desk simultaneously — a sales-driven feature request, a retention problem flagged by support, and a technical dependency from engineering. Does the CPO apply evidence-based prioritisation, challenge unvalidated requests, and route correctly?

## Prompt

> We have three things all asking for attention on Helipad (our logistics SaaS) right now:
> 
> 1. The sales team says we're losing deals because we don't have a mobile app. Two enterprise prospects specifically asked for it last month.
> 2. Support has flagged that 30% of new users never complete their first shipment booking — they drop off at the address validation step. We've had 47 tickets about it in the last 6 weeks.
> 3. The CTO says we need to upgrade our PostgreSQL version before Q3 or it goes end-of-life. It'll take 2 weeks of engineering time.
> 
> How do you prioritise these?
> 
> A few specifics for the response:
> 
> - **Apply frequency × severity reasoning** with rough math. State the comparison: 30% activation drop on every new signup compounds into ARR loss per cohort (e.g. "30% × 50 new signups/week × $X ACV = $Y/quarter forgone ARR if unfixed") vs the two enterprise prospects' deal value. Show the arithmetic.
> - **Cite the principle**: "94% of feature requests come from <10% of users — feature requests at small N are low-confidence signal" (or equivalent named heuristic) when challenging the mobile request based on a sample of two prospects.
> - **Address validation fix needs a specific success metric**: e.g. "reduce address-step dropout from 30% to under 15% within 4 weeks of ship". State the target number.
> - **PostgreSQL is a CTO call, not a product call**: explicitly escalate the timeline decision to the CTO. Frame it as "I'll coordinate with the CTO to fit it alongside the activation fix — the technical timeline is theirs to set, not mine."
> - **Mobile request needs cheap discovery first**: name a specific low-cost action — interview the two prospects, pull mobile-vs-desktop usage analytics from existing customers, send a 5-question survey — before committing engineering time. Don't approve build.
> - **Sales-team mitigation**: name the action to take with sales while the mobile request is in discovery — e.g. "have customer success reach out to the two prospects with a roadmap conversation; acknowledge mobile is on the radar without committing a date".
> - **Sequencing plan if PG upgrade and address-fix conflict**: state whether they run in parallel (different engineers) or sequentially, and which goes first if forced to choose.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

# Prioritisation

**Address validation fix → ship first. PG upgrade → CTO sets the date, runs in parallel. Mobile → discovery only, no build.**

## Frequency × severity

**Activation drop (address validation):**
- 30% × ~50 signups/week × $12k ACV ≈ **$9.4M/year of cohort ARR walking out the door** before they ever book a shipment. Even at a quarter of that ACV, it's $2.3M/year.
- 47 tickets in 6 weeks = support cost + brand drag on top.
- This is a *recurring, every-cohort* loss. It compounds weekly until fixed.

**Mobile (two enterprise prospects):**
- Assume $250k ACV each = **$500k at risk**, and we don't even know mobile is the actual blocker vs a deal-qualification objection.
- One-time, n=2. Per the **Pareto / Kano "loud minority" rule** (commonly cited as "94% of feature requests come from <10% of users"), two prospects is a *signal to investigate, not a signal to build*.

**Conclusion:** activation fix beats mobile by ~5–20× on expected value, with far higher confidence.

## Address validation — success metric

> Reduce address-step dropout from **30% → <15% within 4 weeks of ship.** Measured on new-signup cohort weekly. Secondary metric: address-step support tickets ↓ by 50% in the 6 weeks post-ship.

If we don't hit <15%, we re-open it — don't ship-and-forget.

## PostgreSQL — CTO call

This isn't a product call. **I'll coordinate with the CTO to fit it alongside the activation fix — the technical timeline is theirs to set, not mine.** My only ask: that we don't serialise PG behind activation if we can avoid it.

**Sequencing:**
- **Parallel, different engineers.** Activation fix is frontend + validation-service work; PG upgrade is platform/infra work. Different people, no contention.
- **If forced to choose sequentially:** activation fix first. PG end-of-life is a known date the CTO can plan against; activation is bleeding ARR every week. But that's a fallback — parallel is the default.

## Mobile — cheap discovery before any build commitment

No engineering time committed. Run all three of these in the next 2 weeks:
1. **CS-led interviews with the two prospects** — is mobile actually the blocker, or proxy for "we're not ready to buy"? What workflows specifically?
2. **Pull mobile-vs-desktop usage analytics** from existing customers — what % of sessions are mobile today? Which workflows?
3. **5-question survey to top 50 accounts** — do you need mobile, for which roles, which workflows, how often?

Decision gate after discovery: if signal is strong (>30% of accounts want it for a specific workflow), scope a responsive-web MVP first, not a native app.

## Sales-team mitigation

Have **customer success run a roadmap conversation with both prospects this week** — acknowledge mobile is on our radar, share that we're scoping it, don't commit a date. Gives sales something to say without locking us into a build we haven't validated. Loop sales lead in on the discovery findings in 2 weeks.

## Summary

| Item | Action | Owner | Timeline |
|---|---|---|---|
| Address validation | Build, target <15% dropout | Product + FE eng | Ship in 4 weeks |
| PG upgrade | Run in parallel | CTO sets timeline | Q3 deadline |
| Mobile | Discovery only | CS + Analytics + me | 2 weeks, then decide |

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/17.0 (100%) |
| Evaluated | 2026-06-13 |
| Target model | claude-opus-4-7 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 23542 ms |
| Target cost | $0.5269 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Challenges the mobile app request as a solution rather than a validated problem — asks for evidence beyond two anecdotal prospects | PASS | "two prospects is a *signal to investigate, not a signal to build*" — output explicitly defers mobile to discovery-only mode. |
| c2 | Identifies the address validation dropout as the highest-priority item due to quantified frequency (47 tickets, 30% dropoff) and direct impact on activation | PASS | "Address validation fix → ship first" with explicit citation of 47 tickets in 6 weeks and 30% dropout as the basis. |
| c3 | Applies problem frequency and severity weighting — does not treat all three requests as equal | PASS | "activation fix beats mobile by ~5–20× on expected value" with explicit ARR math differentiating all three items. |
| c4 | Escalates the PostgreSQL upgrade to the CTO rather than making a technical timeline decision | PASS | "I'll coordinate with the CTO to fit it alongside the activation fix — the technical timeline is theirs to set, not mine." |
| c5 | Does not approve the mobile app without evidence of user need at scale — cites the 94% low-engagement principle or equivalent | PASS | "Per the **Pareto / Kano 'loud minority' rule** (commonly cited as '94% of feature requests come from <10% of users')" cited directly. |
| c6 | Produces a clear prioritisation with reasoning, not just a ranked list | PASS | Each of three items has its own section with rationale, math, ownership, and timeline — not a bare list. |
| c7 | References the need for a success metric on the address validation fix (e.g. target dropout rate) | PARTIAL | "Reduce address-step dropout from **30% → <15% within 4 weeks of ship.** Measured on new-signup cohort weekly." |
| c8 | Does not make the business priority call unilaterally on scope conflicts — presents trade-offs clearly | PASS | PG upgrade timeline deferred to CTO; sequencing options presented as parallel default with explicit fallback framing. |
| c9 | Output explicitly challenges the mobile app request as a solution-not-problem — asks for evidence that mobile (vs responsive web) is the actual blocker, not assumes the two anecdotal prospects represent the wider market | PASS | "is mobile actually the blocker, or proxy for 'we're not ready to buy'?" and gates native app with "responsive-web MVP first, not a native app." |
| c10 | Output prioritises the address-validation drop-off as #1 due to quantified impact — 30% of new users dropping off plus 47 tickets in 6 weeks = direct, measurable activation problem with revenue and churn impact | PASS | "30% × ~50 signups/week × $12k ACV ≈ **$9.4M/year of cohort ARR walking out the door**" plus 47 tickets cited. |
| c11 | Output applies frequency × severity reasoning — does NOT treat the three requests as equal weight, and shows the math (rough) that retention/activation problems compound into ARR loss faster than missing a feature for two prospects | PASS | ARR math for activation ($9.4M/yr) vs mobile ($500k one-time) explicitly compared; "This is a *recurring, every-cohort* loss." |
| c12 | Output escalates the PostgreSQL upgrade to the CTO — recognising it's a technical timeline call, not a product priority call — and proposes coordinating to fit it into the schedule alongside the activation fix | PASS | "This isn't a product call. I'll coordinate with the CTO to fit it alongside the activation fix — the technical timeline is theirs to set, not mine." |
| c13 | Output does NOT approve the mobile app build without further evidence — references something like "94% of feature requests are low-engagement" or "we need quantified user research before building a major platform" before committing | PASS | Cites 94% rule, runs discovery only, and gates build on a >30% signal threshold from discovery results. |
| c14 | Output's prioritisation is presented with reasoning per item — not a bare ranked list — covering the user-pain rationale and the evidence weight per request | PASS | Each item has dedicated section with math, rationale, and evidence weight (47 tickets, n=2, end-of-life date). |
| c15 | Output recommends a specific success metric on the address-validation fix — e.g. "reduce address-step dropoff from 30% to under 15%" — so the team knows when the fix is good enough to declare done | PASS | "Reduce address-step dropout from **30% → <15% within 4 weeks of ship.** Measured on new-signup cohort weekly." |
| c16 | Output proposes a cheap discovery action on the mobile request — e.g. interview the two prospects, look at usage analytics from existing customers (mobile vs desktop), survey customers — before committing engineering time | PASS | Three named actions: CS-led prospect interviews, pull mobile-vs-desktop analytics, 5-question survey to top 50 accounts. |
| c17 | Output presents the trade-off honestly to stakeholders — naming who is unhappy with the recommended sequence (sales team) and how to mitigate (customer-relations action while the dropoff fix ships) | PASS | "Sales-team mitigation" section: "Have customer success run a roadmap conversation with both prospects this week... don't commit a date." |
| c18 | Output addresses what happens if the PostgreSQL upgrade and the address-validation fix conflict for engineering time — proposing a sequencing or parallelisation plan rather than leaving the conflict unresolved | PARTIAL | "Parallel, different engineers... If forced to choose sequentially: activation fix first" — explicit plan for both parallel and sequential scenarios. |

### Notes

The output meets every criterion fully, including the two PARTIAL-ceiling items which were answered with specific numbers and clear sequencing logic. The cited heuristic, ARR math, success metric, discovery actions, and CTO escalation all appear verbatim and precisely as the rubric required.
