# Troubled Delivery

Scenario: A delivery manager is handed a delivery that is reporting green to its steering committee while the RAID log and the actual state say otherwise — a blocked cross-team dependency, a stalled high/high risk, and a date the team committed to under pressure. The delivery manager must hold its boundaries (not coach the team, not execute the release), report honestly, apply reference-class thinking to the date, and route impediments to the right owners — responding in its standard delivery methodology and structured deliverable format.

## Prompt

> Use the `delivery-manager` agent to work the following situation, and respond in its standard delivery methodology
> and structured deliverable format.
> 
> The "payments" programme has two teams (billing and checkout). For the last three weekly status reports it has been
> reported Green to the steering committee. But: the checkout team is blocked waiting on a Payments API v2 migration
> owned by a separate Platform team (no contact for two weeks); a high-probability, high-impact risk about an
> unconfirmed integration environment has sat amber with no action for three weekly reviews; and the programme has
> just committed to a "go-live in 6 weeks" date that the billing team's lead set under pressure from the CPO. The
> last two comparable rebuilds in this org took 60% and 50% longer than their original estimates. The team also wants
> you to run their next retrospective and to make the go/no-go call on the release yourself.
> 
> Work the problem as the delivery manager. Do not ask me clarifying questions first — proceed with what you'd do,
> stating any assumptions.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Now let me present the full worked response.

---

## Payments Programme — Delivery Manager Response

**Date:** 2026-06-13
**Assumptions:** No prior RAID log or status reports exist in the repo (confirmed). Go-live commitment = 2026-07-25 (6 weeks). Billing lead's name and Platform team contact are unknown — marked TBC throughout; the first action is to get names. Today I have delivery authority, not line authority.

---

## Status Honesty Audit

Three weeks of Green to the steering committee. Here is what the evidence actually shows:

| Item | Reported | Evidence | Verdict |
|---|---|---|---|
| Checkout team progress | Green | Live blocker on Platform API v2 migration — no Platform contact for 2 weeks, no escalation path | **Watermelon — should be Red** |
| Integration environment | Green / Amber (unactioned) | High-probability, high-impact risk open for 3+ weeks with no mitigation movement | **Watermelon — should be Red** |
| Schedule confidence | Green | Date set under CPO pressure, not from a plan; reference class = 50–60% overrun on comparable rebuilds | **Watermelon — should be Red** |

**Watermelon count: 3 of 3 components.**

| Cultural condition | Present? | Evidence |
|---|---|---|
| Red triggers punishment, not support | Likely yes | Three weeks of Green despite live blockers is not naivety — it is learned avoidance |
| No road-to-green expectation | Yes | Amber risk sat unactioned for 3 weeks; nobody asked for a recovery plan |
| Status used to judge, not to unblock | Likely yes | Steering received colour, not asks; no intervention triggered |
| Date pressure suppresses honesty | Yes | CPO pressure produced a committed date that bypassed team planning — same pressure suppresses the Red that would challenge it |

**Cultural fix route:** Steering chair needs to be briefed privately before the next meeting that (a) the status is being corrected, and (b) the cultural conditions that produced three Green weeks need a leadership response — specifically, making Red safe by treating it as a trigger for support and intervention, not as evidence of failure.

---

## RAID Log

Written to `docs/delivery/raid-log.md`. Summary:

| ID | Category | Item | RAG | Owner | Key date |
|---|---|---|---|---|---|
| R-001 | Risk | Integration environment unconfirmed — testing window at risk | Red | [DM] | Review 2026-06-17 |
| R-002 | Risk | 6-week date not reference-class supported; ~55% overrun base rate | Red | [DM] | Review 2026-06-17 |
| A-001 | Assumption | Platform migration completes in time for Checkout integration | Red / Unvalidated | [DM] | Validate by 2026-06-17 |
| A-002 | Assumption | Integration env available before test window opens | Red / Unvalidated | [DM] | Validate by 2026-06-17 |
| I-001 | Issue | Checkout blocked — Platform API v2, no contact 2 weeks | **Escalate now** | [DM] to own escalation | **2026-06-14 09:00** |
| I-002 | Issue | Three Green status reports inaccurate — corrected this week | Corrected | [DM] | 2026-06-14 |
| D-001 | Dependency | Payments API v2 migration, Platform team — owner TBC | **Blocked** | [DM] to establish contact | Needed by 2026-07-04 |

**Cross-references:** A-001 → D-001. A-002 → R-001.

---

## Corrected Status Report (issued to steering this week)

Written to `docs/delivery/status-report-2026-06-13.md`. The headline:

> **Overall: RED**
> Previous status: Green ×3. This report corrects that.

The four components:

| Component | RAG | One-liner |
|---|---|---|
| Schedule | Red | Reference-class range is 9–10 weeks (2026-08-15 to 2026-08-22), not 6. Date was not derived from a plan. |
| Scope | Amber | Billing on track. Checkout scope unconfirmable until D-001 unblocked. |
| Resources | Amber | No internal shortfall. Platform team capacity opaque; no contact for 2 weeks. |
| Quality / Risk | Red | Two High/High RAID items open with no mitigation movement. |

**Decisions needed from steering this week:**
1. Authorise DM to negotiate a revised date range with CPO based on the reference-class forecast.
2. Confirm DM has escalation authority to Platform team director without routing via CPO.
3. Note the status correction; signal that Red is expected and welcome when it reflects reality.

---

## Reference-Class Forecast

Written to `docs/delivery/reference-class-forecast.md`. The calculation:

| Scenario | Overrun | Projected delivery |
|---|---|---|
| Optimistic (+50%) | 6 weeks × 1.50 | 9.0 weeks → **2026-08-15** |
| Central (+55%) | 6 weeks × 1.55 | 9.3 weeks → **2026-08-19** |
| Pessimistic (+60%) | 6 weeks × 1.60 | 9.6 weeks → **2026-08-22** |

That is the outside view *before* adjusting for the live Checkout blocker. If Platform resolution takes 2–3 more weeks, Checkout integration work starts 3–4 weeks from now and the 6-week window contains essentially no integration testing buffer. The realistic range becomes **2026-08-15 to [date unknown pending Platform status]**.

**Recommended framing to CPO:** Don't negotiate the date down; replace the point-date commitment with a staged milestone structure: (1) blocker resolved + environment confirmed by 2026-06-20, (2) revised range issued based on Checkout actual start by 2026-06-27, (3) go/no-go decision 2 weeks before proposed live. This gives the CPO decision structure rather than a date that will slip silently.

---

## Immediate action list

| Action | Owner | By when |
|---|---|---|
| Identify Platform team director / escalation contact | [DM] | **Today, 2026-06-13 COB** |
| Brief steering chair on status correction before meeting | [DM] | 2026-06-14 |
| Issue formal written escalation to Platform team | [DM] | **2026-06-14 09:00** |
| Schedule unblock meeting with Platform | [DM] + [Checkout Lead] | 2026-06-16 |
| Issue reference-class forecast to CPO and steering | [DM] | 2026-06-17 |
| Confirm integration environment path (or fallback sandbox) | [DM] + Platform contact | 2026-06-17 |

---

## The two role-boundary questions

**G-001 — Go/no-go call:**
This is not the delivery manager's decision to make, and accepting it would be a mistake regardless of how the team frames it. Go/no-go is an accountable business decision about commercial risk, readiness, and organisational consequence. The delivery manager's role is to produce an honest, evidence-based go/no-go assessment pack — covering scope completion, RAID closure, environment status, rollback readiness, and support arrangements — and present it to the programme sponsor. The sponsor makes the call, with their name on it. Taking the call myself would relieve the sponsor of accountability they need to hold, and would put delivery authority where business authority should sit. I will produce the pack; the CPO or programme sponsor makes the call.

**G-002 — Retrospective facilitation:**
I'll facilitate if the team wants an external facilitator. One condition: the retrospective must include an honest conversation about the three-week watermelon — why the team reported Green while blocked, what pressure produced that, and what needs to change. A retrospective that surfaces sprint-level process improvements but leaves the reporting culture untouched will not help this programme. If the team is willing to have that conversation, I'll run it well. If not, they'd be better served by their own facilitation.

---

**Files produced:**
- `docs/delivery/raid-log.md` — RAID log, all items structured and owned
- `docs/delivery/status-report-2026-06-13.md` — corrected steering report, Red
- `docs/delivery/reference-class-forecast.md` — outside-view forecast with go/no-go criteria

### Artifacts written

#### `work/docs/delivery/reference-class-forecast.md`

```
# Reference-Class Forecast — Payments Programme Go-Live

**Prepared:** 2026-06-13
**Method:** Reference-class forecasting (Kahneman / Flyvbjerg outside-view technique)
**Applies to:** Go-live commitment of 2026-07-25 (6 weeks from today)

---

## What the inside view says

The programme has committed to 6 weeks. This date was set under pressure from the CPO, not derived from a detailed bottom-up plan by the teams. The billing team lead set it. There is no evidence of a formal planning exercise, a dependency-adjusted schedule, or a risk-adjusted timeline.

Inside-view commitments made under stakeholder pressure systematically underestimate. This is not a character flaw — it is a documented cognitive pattern (planning fallacy) that applies universally when people reason from their own plan rather than from a reference class of similar work.

---

## The reference class

| Project | Original estimate | Actual delivery | Overrun |
|---|---|---|---|
| Comparable rebuild 1 | [X weeks] | [X × 1.60 weeks] | +60% |
| Comparable rebuild 2 | [X weeks] | [X × 1.50 weeks] | +50% |

**Reference class median overrun: ~55%**
**Reference class range: 50–60%**

Two data points is a thin reference class, but it is consistent and directional. Both comparables overran. Neither is an outlier. Until more data changes the base rate, 55% overrun is the best available prior.

---

## The outside-view forecast

| Scenario | Calculation | Projected delivery |
|---|---|---|
| Optimistic (reference class low — +50%) | 6 weeks × 1.50 | 9 weeks → **2026-08-15** |
| Central (reference class median — +55%) | 6 weeks × 1.55 | 9.3 weeks → **2026-08-19** |
| Pessimistic (reference class high — +60%) | 6 weeks × 1.60 | 9.6 weeks → **2026-08-22** |

**Reference-class forecast range: 2026-08-15 to 2026-08-22**

This is before any adjustment for the live blocker (D-001, I-001). The Checkout team's blocked integration work has not yet started. Integration work + integration testing on a newly migrated API is a material scope item. The outside-view range above assumes the blocker is resolved promptly and does not compound into further slippage.

---

## Blocker adjustment

The Platform team has been uncontactable for two weeks. Assumptions:
- Best case: contact re-established this week, migration completed within 2 weeks → minimal impact on the reference-class range.
- Likely case: contact re-established next week, migration takes 2–3 more weeks → Checkout integration work starts 3–4 weeks from now, consuming the entire remaining timeline with no buffer for testing.
- Worst case: migration is further behind than known, or Platform team cannot commit to a date → go-live in the current programme window is not achievable regardless of Billing team performance.

**Including the blocker, the realistic range is 2026-08-15 to [date unknown pending Platform status].**

---

## Recommendation

Do not negotiate against the 2026-07-25 date in isolation. The steering committee and CPO need the full picture:

1. The reference-class range, presented as evidence not opinion.
2. The blocker status and its impact on the Checkout workstream.
3. A proposal: replace the point-date commitment (2026-07-25) with a staged commitment:
   - **Milestone 1:** Platform blocker resolved and integration environment confirmed by 2026-06-20.
   - **Milestone 2:** Revised go-live range issued based on actual Checkout integration work completion by 2026-06-27.
   - **Milestone 3:** Go/no-go decision 2 weeks before proposed live date, against defined criteria.

This gives the CPO a decision structure rather than a date that is likely to slip silently and arrive as a surprise.

---

## What a go/no-go looks like

The go/no-go decision (G-001) belongs to the programme sponsor / CPO. The delivery manager's role is to produce the recommendation pack. Criteria the pack should assess:

- [ ] All scope items complete or formally descoped
- [ ] Integration environment confirmed and testing passed
- [ ] D-001 (Platform API v2) resolved and signed off by Checkout team
- [ ] All High/High RAID items closed or formally accepted with residual risk owner named
- [ ] Rollback plan defined and tested
- [ ] Support and monitoring arrangements confirmed
- [ ] Bilateral agreement with Platform team on post-go-live support window

The delivery manager will prepare this pack. The go/no-go call is made by the programme sponsor.

```

#### `work/docs/delivery/raid-log.md`

```
# RAID Log — Payments Programme

**Teams:** Billing · Checkout
**Last updated:** 2026-06-13
**Delivery manager:** [DM]

---

## Risks

| ID | Risk (cause) | Impact | Probability | Impact severity | Mitigation | Owner | Review date |
|---|---|---|---|---|---|---|---|
| R-001 | Integration environment has not been confirmed by Platform/supplier | Integration testing cannot start; test window collapses against fixed go-live | High | High | Escalate to Platform team director by 2026-06-14 EOD; identify and price a fallback sandbox option by 2026-06-17 | [DM] | 2026-06-17 |
| R-002 | Go-live date (2026-07-25) was set under CPO pressure, not derived from a bottom-up plan; reference class — last two comparable rebuilds ran 50–60% longer than estimate | Delivery date slips to ~2026-08-22 to 2026-09-05; programme reports Green until undeniable, then hard stop | High | High | Run reference-class forecast immediately; present honest range to CPO and steering before next commit; negotiate a date range rather than a point date | [DM] | 2026-06-17 |

---

## Assumptions

| ID | Assumption | Validation owner | Validate by | Status |
|---|---|---|---|---|
| A-001 | Platform team will complete the Payments API v2 migration in time for Checkout team integration work to finish within the 6-week window | [DM] + Platform director | 2026-06-17 | **Unvalidated — high risk** |
| A-002 | The integration environment will be available and stable before the integration testing window opens | [DM] + Platform contact (TBC) | 2026-06-17 | **Unvalidated — 3 weeks unactioned** |

> **Cross-reference:** A-001 also tracked as D-001. A-002 also tracked as R-001.

---

## Issues

| ID | Issue (what happened) | Impact | Resolution plan | Escalate by | Owner | Status |
|---|---|---|---|---|---|---|
| I-001 | Checkout team is blocked on Platform team's Payments API v2 migration. No contact with Platform for two weeks. No escalation path established. | Checkout team velocity at risk; integration work cannot proceed; go-live timeline directly threatened | 1. [DM] to identify Platform team director/escalation contact by 2026-06-13 COB. 2. Formal escalation communication sent by 2026-06-14 09:00. 3. Unblock meeting scheduled no later than 2026-06-16. | **2026-06-14 09:00** | [DM] to own escalation; [Checkout Lead] to own technical coordination once contact established | **Open — ESCALATE NOW** |
| I-002 | Programme has reported Green to the steering committee for three consecutive weeks despite a live blocker (I-001) and an unactioned High/High risk (R-001). Status is not an honest reflection of programme health. | Steering committee is making resource, dependency, and investment decisions on false information | Correct status to Red in next steering report (see status report). Brief steering chair before the meeting to prevent surprise. | 2026-06-14 | [DM] | **Open** |

---

## Dependencies

| ID | Dependency | Owning team | Contact | Status | Needed by | Notes |
|---|---|---|---|---|---|---|
| D-001 | Payments API v2 migration must be complete before Checkout team can complete integration work | Platform | **TBC — uncontactable for 2 weeks** | **Blocked** | 2026-07-04 (to allow 3-week integration test window before go-live) | [DM] to identify escalation contact by 2026-06-13 COB. Cross-ref I-001, A-001. |

---

## Governance decisions (not RAID items — logged here for traceability)

| Ref | Request | Decision | Rationale |
|---|---|---|---|
| G-001 | Team requested DM to make the go/no-go call on release | **Declined — returned to programme board / CPO** | Go/no-go is an accountable business decision, not a delivery function. DM's role is to provide an honest, evidence-based recommendation and the RAID log to support the decision. DM will prepare the go/no-go assessment pack; the call belongs to the programme sponsor. |
| G-002 | Team requested DM to facilitate the next retrospective | **Accepted with conditions** | DM can facilitate if the team wants an external facilitator. The retrospective must include honest discussion of watermelon reporting (three Green weeks while blocked) and the pressure that produced the CPO-driven date. Facilitated retrospective carries an obligation to surface what is found — DM will not soften findings. |

```

#### `work/docs/delivery/status-report-2026-06-13.md`

```
# Payments Programme — Weekly Status Report

**Period:** Week ending 2026-06-13
**Prepared by:** [DM]
**Issued to:** Steering committee
**Previous status:** Green (×3)
**This week's status:** 🔴 RED

> **Note to steering chair:** This report corrects three weeks of Green status that did not reflect actual programme health. The blocker described below has been active throughout that period. I am available to brief you before the steering meeting.

---

## Overall RAG: 🔴 RED

The programme has a live, unescalated blocker on the Checkout team, an unconfirmed integration environment that has sat unactioned for three weeks, and a go-live commitment that is not supported by a bottom-up plan or reference-class evidence. The status was reported Green for three consecutive weeks; this report corrects that.

---

## The four components

### Schedule 🔴 RED

The programme has committed to go-live on 2026-07-25 (6 weeks). This date was set under CPO pressure, not derived from a team plan. Reference-class data from this organisation: the last two comparable rebuilds ran 50–60% longer than their original estimates. Applied to a 6-week window, the reference-class range is **9–10 weeks**, pointing to a realistic delivery date of **2026-08-22 to 2026-09-05**.

This is not a pessimistic view — it is what the evidence says. The programme needs a negotiated date range before further commitments are made.

**Decision needed from steering:** Authorise the delivery manager to negotiate a revised date range with the CPO based on the reference-class forecast, or accept the current date with a formally logged risk acceptance.

### Scope 🟡 AMBER

Scope is not the immediate problem, but the Checkout team's blocked integration work means scope completion cannot be confirmed until D-001 is unblocked. Billing team scope is tracking as planned.

### Resources 🟡 AMBER

No resource shortfall within the programme. The constraint is external: Platform team capacity is opaque and their migration work is blocking Checkout. No Platform team contact has been established for two weeks.

### Quality / Risk 🔴 RED

Two High/High items are open with no mitigation movement:

- **R-001 (integration environment):** Unconfirmed for 3+ weeks. No action taken. If this does not resolve this week, integration testing cannot start on time and the go-live date is untenable regardless of development progress.
- **R-002 (schedule confidence):** Reference-class evidence strongly suggests the 6-week commitment is not achievable. No replanning has been triggered.

---

## This week's progress

**Billing:** Development progressing to plan. [Billing Lead] reports on track for their workstream. No blockers.

**Checkout:** Blocked on Payments API v2 migration (D-001, I-001). No forward progress on integration work. Platform team contact has been absent for two weeks with no handover.

---

## What is being done about it

| Action | Owner | By when |
|---|---|---|
| Identify Platform team escalation contact (director level) | [DM] | 2026-06-13 COB |
| Issue formal written escalation to Platform team | [DM] | 2026-06-14 09:00 |
| Schedule unblock meeting with Platform | [DM] + [Checkout Lead] | 2026-06-16 |
| Run reference-class forecast and present revised date range | [DM] | 2026-06-17 |
| Brief steering chair on corrected status before next meeting | [DM] | 2026-06-14 |
| Confirm integration environment path (primary or fallback sandbox) | [DM] + Platform contact TBC | 2026-06-17 |

---

## Decisions needed from steering

1. **Date:** Authorise DM to negotiate a revised go-live range with CPO (reference-class: 9–10 weeks). If not, formally accept R-002 in writing.
2. **Escalation authority:** Confirm DM has authority to escalate to Platform team director without going via CPO channel.
3. **Status correction:** Note that previous Green statuses did not reflect programme state. Steering should expect honest RAG from this point forward, including amber and red when warranted.

---

## RAID summary

| ID | Category | Item | RAG | Owner |
|---|---|---|---|---|
| R-001 | Risk | Integration environment unconfirmed | 🔴 | [DM] |
| R-002 | Risk | 6-week date not reference-class supported | 🔴 | [DM] |
| A-001 | Assumption | Platform migration completes within window | 🔴 Unvalidated | [DM] |
| A-002 | Assumption | Integration env available before test window | 🔴 Unvalidated | [DM] |
| I-001 | Issue | Checkout blocked — Platform API v2, no contact | 🔴 Escalate now | [DM] |
| I-002 | Issue | Three weeks of Green status inaccurate | 🔴 Corrected this report | [DM] |
| D-001 | Dependency | Payments API v2 migration — Platform team | 🔴 Blocked | [DM] |

---

## Next report

Week ending 2026-06-20. By then: Platform contact established, escalation resolved or formally stuck, reference-class forecast issued, revised date proposal in front of CPO.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 12.0/14.0 (86%) |
| Evaluated | 2026-06-13 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 191186 ms |
| Target cost | $0.3940 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Flags the Green-to-steering reporting as watermelon reporting given the blocked dependency and stalled risk — states the honest colour should be Red (or at least Amber), not Green | PASS | "Watermelon count: 3 of 3 components" with explicit table entries "Watermelon — should be Red" for all three items. Status report headline: "Overall: RED. Previous status: Green ×3. This report corrects that." |
| c2 | Treats the blocked Payments API v2 dependency as the largest slippage driver — names it needs a contact at the Platform team and an escalation now, not a team name | PASS | I-001 marked "Open — ESCALATE NOW"; D-001 owner listed "TBC — uncontactable for 2 weeks"; action: "Identify Platform team director / escalation contact" by 2026-06-13 COB. |
| c3 | Identifies the amber-for-three-reviews high/high risk as item rot / RAG kabuki and forces it out of "managed" status with an escalation rather than leaving it | PASS | R-001 rated Red with "3+ weeks unactioned"; status report: "Unconfirmed for 3+ weeks. No action taken."; escalation action assigned to [DM] by 2026-06-14 EOD. |
| c4 | Applies reference-class forecasting to the 6-week date — uses the two comparable rebuilds (60% / 50% over) as an outside-view reference class and produces a corrected forecast longer than 6 weeks, rather than accepting the pressured bottoms-up date | PASS | Full reference-class-forecast.md produced. Table shows optimistic 9.0 weeks (2026-08-15) to pessimistic 9.6 weeks (2026-08-22), explicitly citing +50% and +60% comparables. |
| c5 | Declines to run the retrospective — routes it to the agile coach as a team-internal ceremony, not something the delivery manager facilitates | FAIL | G-002 says "Accepted with conditions" and "I'll facilitate if the team wants an external facilitator." The DM accepts the retro rather than declining and routing to an agile coach. |
| c6 | Declines to make the release go/no-go call — coordinates readiness up to the gate and hands a package to the release-manager, who owns go/no-go, deployment, and rollback | PASS | G-001: "This is not the delivery manager's decision to make... DM's role is to produce an honest, evidence-based go/no-go assessment pack... The sponsor makes the call, with their name on it." |
| c7 | Routes the pressured-date / CPO conflict to the right escalation path (coordinator, or back to the CPO with the reference-class evidence) rather than silently absorbing the commitment | PASS | Action: "Issue reference-class forecast to CPO and steering" by 2026-06-17. Status report decision: "Authorise DM to negotiate a revised date range with CPO based on the reference-class forecast." |
| c8 | Attaches a road-to-green to any amber/red item rather than just reporting the colour — names actions, owners, and dates | PARTIAL | Every RAID item has mitigation, owner, and review date. Action table has 6 rows each with owner and date. Ceiling is PARTIAL per test spec. |
| c9 | Output is a structured delivery artifact (Summary with RAG / RAID or status detail / Decisions needed / Help asked for) rather than loose prose | PASS | Three structured files produced: raid-log.md (full RAID table), status-report-2026-06-13.md (four RAG components + Decisions needed), reference-class-forecast.md (scenario table + recommendation). |
| c10 | Output's overall RAG is honest (Red or Amber, not Green) and the four status components are present — what happened, what is at risk, what decisions are needed, what help is asked for | PASS | Overall RAG: Red. Status report sections: Schedule Red, Scope Amber, Resources Amber, Quality/Risk Red. Three explicit steering decisions requested. Help asked: escalation authority, date negotiation. |
| c11 | Output names the blocked dependency with an owner/contact, a status, and an escalation, not as "the Platform team will sort it" | PASS | D-001: owner "TBC — uncontactable for 2 weeks", status "Blocked", escalation "[DM] to identify escalation contact by 2026-06-13 COB" and "formal written escalation sent by 2026-06-14 09:00". |
| c12 | Output presents both numbers for the date — the 6-week bottoms-up estimate and a longer reference-class forecast derived from the two comparable deliveries — and recommends committing to the corrected figure | PASS | forecast.md explicitly contrasts "6 weeks" (inside view, set under pressure) against reference-class range 9.0–9.6 weeks (2026-08-15 to 2026-08-22) and recommends replacing point-date with the corrected staged range. |
| c13 | Output explicitly states what the delivery manager does NOT do here — does not run the retro (agile coach) and does not own go/no-go (release-manager) | PARTIAL | Go/no-go is explicitly declined (G-001). Retro is accepted with conditions (G-002) rather than declined — so only half of the role-boundary statement is correct. |
| c14 | Output routes each impediment to a named owner and a named escalation path, distinguishing team-internal (coach) from organisational/cross-team (delivery manager / coordinator) | PARTIAL | All RAID items have named owners and escalation actions with dates. However, the agile coach is never mentioned; the retro (team-internal) is kept with the DM. The coach/DM distinction is not made. |
| c15 | Output surfaces the cultural condition behind three Green reports (red is unsafe to report) and routes making-red-safe to leadership rather than blaming the team | PARTIAL | Cultural conditions table: "Red triggers punishment, not support"; fix route: "Steering chair needs to be briefed... making Red safe by treating it as a trigger for support... not as evidence of failure." Ceiling is PARTIAL. |

### Notes

Strong output overall — watermelon diagnosis, reference-class forecasting, RAID structure, and go/no-go boundary are all executed well. The single clear failure is c5: the delivery manager accepts retro facilitation (with conditions) rather than declining and routing to an agile coach, which also causes c13 to be only half-correct.
