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

# Prioritisation: address validation > PostgreSQL > mobile discovery

## 1. Address validation fix — ship first

**Frequency × severity:** This bleeds on every cohort. Rough math, plug in your real numbers:

- 30% dropout × 50 signups/week × 13 weeks = **~195 failed activations/quarter**
- At, say, $5K ACV and assume 50% would've converted on a clean funnel = **~$485K/quarter forgone ARR**, recurring every quarter it stays broken
- Plus: 47 support tickets in 6 weeks is ~8/week of direct support load

**Success metric:** reduce address-step dropout from 30% to **under 15% within 4 weeks of ship**, measured on the next full signup cohort post-release. If we don't hit 15%, we haven't fixed the right thing — re-investigate root cause (geocoder coverage? UX? validation strictness?) before moving on.

## 2. Mobile app — discovery only, no build

Two prospects is not a roadmap signal. The named heuristic here is the **vocal minority / Pareto problem**: a small handful of loud requests routinely over-represent themselves relative to the silent majority. ProductPlan's oft-cited version is "less than 10% of users drive the majority of feature requests" — at N=2, we're firmly in low-confidence-signal territory. Build cost is months; discovery cost is days.

**Cheap discovery actions before any engineering commitment:**

- **Interview the two prospects** — what specifically do they need mobile for? Field ops? Tracking? Booking? "Mobile app" can mean five different products.
- **Pull mobile-vs-desktop analytics** from existing customers — what % of sessions are mobile today, what do they do on mobile, where do they bounce?
- **5-question survey** to the existing customer base on mobile use cases and pain.
- **Check the responsive web experience** — is the real ask "native app" or "the web app doesn't work on my phone"? The latter is a fraction of the cost.

**Sales-team mitigation while discovery runs:** ask Customer Success to open a roadmap conversation with the two prospects — acknowledge mobile is on our radar, frame it as "we're scoping it now, want to understand your use case," no date committed. That keeps the deals warm without locking us into a build we haven't validated. Brief sales on the same talking points so they stop treating "no mobile app" as a closed-lost reason without qualifying the actual ask.

## 3. PostgreSQL upgrade — CTO call, not mine

EOL on infra is a technical risk decision and the timeline is the CTO's to set, not product's. **I'll coordinate with the CTO** to slot the 2 weeks of engineering somewhere before Q3, but the sequencing — and whether it's urgent enough to interrupt activation work — is their judgment.

## Sequencing if address-fix and PG upgrade collide

**Default plan: run in parallel.** Address validation is frontend + geocoder work; PG upgrade is backend/infra. Different engineers, minimal contention. CTO assigns the infra engineer(s); I keep frontend on the activation fix.

**If forced to choose one first** (e.g. one team, one engineer): **address validation first, PG upgrade second**, provided the CTO confirms there's slack before Q3 EOL. Reason: address-fix is bleeding revenue *now* on every cohort, PG EOL is a known fixed deadline we can plan to. If the CTO says PG can't wait, it can't wait — that overrides.

## Summary

| Item | Action this week | Owner | Decision |
|---|---|---|---|
| Address validation | Start build; define <15% dropout target | Product + frontend | **Approved** |
| PostgreSQL upgrade | Confirm timeline & resourcing | CTO | **Escalated to CTO** |
| Mobile app | Run discovery (interviews + analytics + survey); CS roadmap convo with prospects | Product + CS | **Not approved — discovery only** |

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/17.0 (100%) |
| Evaluated | 2026-05-27 |
| Target model | claude-opus-4-7 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 37352 ms |
| Target cost | $0.3295 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Challenges the mobile app request as a solution rather than a validated problem — asks for evidence beyond two anecdotal prospects | PASS | "Two prospects is not a roadmap signal" and "Interview the two prospects — what specifically do they need mobile for?" |
| c2 | Identifies the address validation dropout as the highest-priority item due to quantified frequency (47 tickets, 30% dropoff) and direct impact on activation | PASS | Placed #1, cites "47 support tickets in 6 weeks is ~8/week" and "30% dropout × 50 signups/week × 13 weeks = ~195 failed activations/quarter" |
| c3 | Applies problem frequency and severity weighting — does not treat all three requests as equal | PASS | Three distinct outcomes: address fix Approved, PG Escalated to CTO, mobile Not approved — discovery only. ARR math shown only for activation fix. |
| c4 | Escalates the PostgreSQL upgrade to the CTO rather than making a technical timeline decision | PASS | "EOL on infra is a technical risk decision and the timeline is the CTO's to set, not product's. I'll coordinate with the CTO to slot the 2 weeks..." |
| c5 | Does not approve the mobile app without evidence of user need at scale — cites the 94% low-engagement principle or equivalent | PASS | Cites "vocal minority / Pareto problem" and "less than 10% of users drive the majority of feature requests — at N=2, we're firmly in low-confidence-signal territory" |
| c6 | Produces a clear prioritisation with reasoning, not just a ranked list | PASS | Three full sections with ARR math, named heuristics, discovery steps, sequencing plan, and a summary table with owner and decision columns. |
| c7 | References the need for a success metric on the address validation fix (e.g. target dropout rate) | PARTIAL | "Success metric: reduce address-step dropout from 30% to under 15% within 4 weeks of ship, measured on the next full signup cohort post-release." |
| c8 | Does not make the business priority call unilaterally on scope conflicts — presents trade-offs clearly | PASS | PG timeline deferred to CTO; forced-choice sequencing explicitly conditioned on "provided the CTO confirms there's slack before Q3 EOL." |
| c9 | Output explicitly challenges the mobile app request as a solution-not-problem — asks for evidence that mobile (vs responsive web) is the actual blocker, not assumes the two anecdotal prospects represent the wider market | PASS | "Check the responsive web experience — is the real ask 'native app' or 'the web app doesn't work on my phone'? The latter is a fraction of the cost." |
| c10 | Output prioritises the address-validation drop-off as #1 due to quantified impact — 30% of new users dropping off plus 47 tickets in 6 weeks = direct, measurable activation problem with revenue and churn impact | PASS | "~$485K/quarter forgone ARR, recurring every quarter it stays broken" plus "47 support tickets in 6 weeks is ~8/week of direct support load" |
| c11 | Output applies frequency × severity reasoning — does NOT treat the three requests as equal weight, and shows the math (rough) that retention/activation problems compound into ARR loss faster than missing a feature for two prospects | PASS | Full ARR calculation shown for activation fix; mobile dismissed as N=2 low-confidence signal with no comparable math — explicit contrast in weighting. |
| c12 | Output escalates the PostgreSQL upgrade to the CTO — recognising it's a technical timeline call, not a product priority call — and proposes coordinating to fit it into the schedule alongside the activation fix | PASS | "I'll coordinate with the CTO to slot the 2 weeks of engineering somewhere before Q3, but the sequencing... is their judgment." |
| c13 | Output does NOT approve the mobile app build without further evidence — references something like "94% of feature requests are low-engagement" or "we need quantified user research before building a major platform" before committing | PASS | "Build cost is months; discovery cost is days." Summary table shows "Not approved — discovery only" for mobile. |
| c14 | Output's prioritisation is presented with reasoning per item — not a bare ranked list — covering the user-pain rationale and the evidence weight per request | PASS | Three dedicated sections with ARR math, heuristic citation, discovery steps, escalation rationale, and a sequencing plan — not a bullet list. |
| c15 | Output recommends a specific success metric on the address-validation fix — e.g. "reduce address-step dropoff from 30% to under 15%" — so the team knows when the fix is good enough to declare done | PASS | "reduce address-step dropout from 30% to under 15% within 4 weeks of ship, measured on the next full signup cohort post-release" |
| c16 | Output proposes a cheap discovery action on the mobile request — e.g. interview the two prospects, look at usage analytics from existing customers (mobile vs desktop), survey customers — before committing engineering time | PASS | Four specific actions: interview two prospects, pull mobile-vs-desktop analytics, 5-question survey, check responsive web experience. |
| c17 | Output presents the trade-off honestly to stakeholders — naming who is unhappy with the recommended sequence (sales team) and how to mitigate (customer-relations action while the dropoff fix ships) | PASS | "Sales-team mitigation while discovery runs" section: CS roadmap conversation with prospects, brief sales on talking points to stop treating it as closed-lost. |
| c18 | Output addresses what happens if the PostgreSQL upgrade and the address-validation fix conflict for engineering time — proposing a sequencing or parallelisation plan rather than leaving the conflict unresolved | PARTIAL | Full "Sequencing if address-fix and PG upgrade collide" section: default parallel plan with different engineers, forced-choice fallback with address fix first if CTO confirms Q3 slack. |

### Notes

The output is a near-perfect match against all criteria: it shows the ARR arithmetic, cites the vocal-minority heuristic, names a specific 15% dropout target, defers PG timeline to the CTO, and lists four concrete mobile discovery steps. Both PARTIAL-ceiling criteria (c7, c18) are actually fully addressed in the output — they are capped at PARTIAL by the test author's ceiling, not by any deficiency in the response.
