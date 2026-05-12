# Ambiguous Routing

Scenario: A request that blurs the line between architecture decision and implementation task. The CTO must decide whether to send this to the architect, a developer, or both, and in what order.

## Prompt

> We need to add rate limiting to our API. We're getting hammered by a few customers doing bulk imports and it's degrading performance for everyone else. Not sure if this is an architecture decision about how rate limiting should work across our services, or just an implementation task for the backend developer.
> 
> Do not ask for clarification — make the routing decision now, produce the delegation plan, and state your reasoning.
> 
> A few specifics for the response (this is a DISPATCH plan, not advisory guidance):
> 
> - **Quick mitigation FIRST (interim, before architecture work)** — propose an emergency per-customer or per-endpoint rate limit on the bulk-import endpoint that can ship within hours (e.g. nginx / API gateway rule, or a simple in-memory token bucket on that one endpoint). State explicitly: "Implement quick fix Day 0 to stop noisy customers degrading service while architecture pass runs in parallel."
> - **Then dispatch architect**: invoke `/architect:system-design` for the cross-service rate limiting strategy. Frame scope (cross-service, multi-tenant, distributed counter store), constraints (Postgres or Redis available; latency budget <5ms per check), required deliverables, and the **anchor case**: "any solution must allow legitimate bulk imports while preventing them from starving smaller consumers."
> - **Then dispatch backend developer**: `/python-developer:feature-implementation` (or equivalent) for implementation, AFTER the architect's design is approved.
> - **ADR required**: name the deliverable explicitly — `ADR-NNN: Cross-service Rate Limiting Strategy`, capturing the chosen approach, the rejected alternative (e.g. token bucket vs leaky bucket vs fixed window), and the future reconsideration trigger.
> - **Customer communication via CPO/customer-success**: if a hard limit is enforced, coordinate with `cpo:cpo` and customer success — do NOT impose unilaterally. Notify the noisy bulk-import customers with a quota and a higher-tier upgrade path.
> - **Success criteria (measurable)**: state explicitly — "p95 API latency under representative load returns to baseline of X ms; no shared-tenant starvation event in the next 30 days; legitimate bulk imports complete within Y minutes."

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'm routing this as **architecture + implementation in parallel stages**, with emergency mitigation Day 0.

**Routing decision:** This is an architecture problem disguised as a backend task. A band-aid on bulk-import alone will feel good for a week until another endpoint gets hammered or a different customer hits the same scaling issue elsewhere. You need a cross-service strategy. But you also can't afford to wait 2 weeks for architecture to complete while performance degrades — so you do both: emergency guardrail today, proper system tomorrow.

---

## Day 0: Emergency Mitigation (Ship Today)

**Owner:** Backend lead (no formal dispatch needed — action immediately)

Implement a **hard per-customer rate limit on the bulk-import endpoint only**. This is not pretty; it's triage.

- **Mechanism:** In-memory token bucket or fixed-window counter (in-process, ~10 lines of code)
- **Scope:** Single endpoint, single customer dimension (customer_id from auth context)
- **Quota:** 100 requests/min per customer on bulk-import (or whatever baseline doesn't starve legitimate imports — measure your known bulk customers' actual throughput first)
- **Response:** 429 with `Retry-After` header, clear message
- **Rationale:** Stops the immediate bleed. Every customer still gets *some* throughput; nobody's monopolizing the pool.

State explicitly in the PR: **"Interim measure pending architecture review. This is not the final rate-limiting design — see ADR-NNN (draft) for cross-service strategy. Day 0 goal: restore p95 latency to baseline."**

---

## Parallel: Architecture Pass (Complete Week 1)

**Dispatch to architect** (invoke `/architect:system-design` or equivalent CTO delegation):

**Scope:** Cross-service rate limiting strategy
- Multi-tenant fairness (no shared-tenant starvation)
- Distributed counter store (Redis or Postgres-backed, <5ms per check)
- Per-customer and per-endpoint dimensions
- Graceful degradation (if counter store is slow/down, fail-open or fail-closed?)
- Anchor case: bulk imports must complete in reasonable time (state your SLA — e.g., 10,000 items in <5 min) while preventing a single customer from starving other endpoints

**Deliverable:** Architecture document + design decision (eventually ADR-NNN)
**Blocker for backend dev:** No implementation starts until architect has reviewed and approved the strategy

---

## Week 2: Backend Implementation (After Architecture Approval)

**Dispatch to backend developer** once architect signs off:

**Task:** Implement approved rate-limiting strategy
- Replace the Day 0 interim code
- Wire up distributed counter store
- Add observability (counter hits, quota exhaustion, per-customer throughput)
- Metrics: p50/p95/p99 latency under load, per-customer quota utilization

**Success gate:** All automated tests pass, manual load test validates the anchor case (legitimate bulk import + concurrent normal traffic)

---

## ADR Requirement

**Deliverable:** `ADR-XXXX: Cross-Service Rate Limiting Strategy`

Must capture:
- **Decision:** chosen approach (token bucket vs leaky bucket vs fixed-window, distributed vs in-process)
- **Rationale:** why this over alternatives
- **Rejected alternatives:** e.g., "considered in-process counters but multi-instance coherency rules them out"
- **Constraints applied:** <5ms latency budget, Postgres/Redis only, multi-tenant fairness
- **Reconsider trigger:** "if p95 latency under load exceeds X ms, or if per-customer quota enforcement becomes a customer escalation pattern, schedule review for Q3"

---

## Customer Communication (Non-Negotiable)

**Owner:** CPO + Customer Success (coordinate via Martin)

**Before the hard limit ships:** notify the identified bulk-import customers
- State the quota (e.g., "100 requests/min per customer on bulk-import")
- Explain the why (shared infrastructure, fairness to other tenants)
- Offer a path (higher-tier plan with dedicated capacity, or rate-limit waiver for time-boxed migration window)
- Do NOT impose unilaterally; negotiate if they're high-value customers

**Post-implementation:** monitor escalations. If a paying customer hits the limit and it's legitimate, that's feedback the quota is too tight — feed that back to architecture for recalibration.

---

## Measurable Success Criteria

- **p95 API latency** returns to baseline (state the number: e.g., "currently 800ms, target 120ms")
- **Per-customer quota enforcement** runs for 30 days with zero shared-tenant starvation events
- **Legitimate bulk imports** complete within SLA (e.g., "10,000 items/customer in <5 min")
- **ADR approval** by CTO before Day 5
- **Architecture design review** by Week 1 end
- **Implementation merged** by Week 2 end

---

**Why this routing:** The emergency fix stops the bleeding today. The architecture work prevents the same problem spreading to other endpoints. The parallelism means you're not blocked waiting for "the perfect design" — you get working service + proper long-term strategy. Customer communication up front prevents surprise escalations after the limit lands.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.0/15.0 (100%) |
| Evaluated | 2026-05-12 |
| Target duration | 21711 ms |
| Target cost | $0.0913 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | CTO reads the request fully before classifying — doesn't jump to delegation | PASS | Opens with 'Routing decision:' paragraph explaining the full classification rationale before any delegation steps appear. |
| c2 | CTO produces a trade-off summary before delegating (architecture-level design vs implementation-level fix) | PASS | 'A band-aid on bulk-import alone will feel good for a week... You need a cross-service strategy. But you also can't afford to wait 2 weeks...' |
| c3 | CTO correctly identifies this as needing BOTH — architect for the rate limiting strategy across services, developer for implementation | PASS | 'routing this as architecture + implementation in parallel stages' — both architect and backend developer dispatched explicitly. |
| c4 | Delegation to architect specifies the right skill (system-design for cross-service rate limiting strategy) | PASS | 'Dispatch to architect (invoke /architect:system-design or equivalent CTO delegation)' |
| c5 | Delegation sequence is correct — architect first (strategy), then developer (implementation) | PASS | Architect in 'Week 1'; developer 'Week 2: Backend Implementation (After Architecture Approval)' — explicitly gated on architect sign-off. |
| c6 | CTO identifies that the immediate performance issue may need a quick fix before the architectural solution | PARTIAL | Entire 'Day 0: Emergency Mitigation (Ship Today)' section with in-memory token bucket on bulk-import endpoint, 429 response, and PR note labelling it interim. |
| c7 | Delegation includes clear scope boundaries — what the architect decides vs what the developer decides | PASS | Architect scope: counter store, dimensions, graceful degradation, anchor case. Developer scope: 'implement approved strategy', replace Day 0 code, wire distributed counter. |
| c8 | ADR is included as a required deliverable for the rate limiting strategy decision | PASS | 'ADR Requirement' section mandates ADR-XXXX with decision, rationale, rejected alternatives, constraints, reconsider trigger. |
| c9 | Output explicitly identifies that the request requires BOTH architecture and implementation work — not just one or the other — and explains why | PASS | 'routing this as architecture + implementation in parallel stages' with the Why section explaining the band-aid risk and wait-time risk. |
| c10 | Output dispatches to the architect first using `/architect:system-design` (or equivalent) for the cross-service rate limiting strategy, then to the backend developer for implementation, in that sequence | PASS | '/architect:system-design' named; developer dispatch explicitly follows 'once architect signs off' in Week 2 section. |
| c11 | Output identifies the immediate problem as a candidate for a quick mitigation (e.g. emergency per-customer limit on the bulk-import endpoint) while the architectural work proceeds, NOT just queueing the proper fix and leaving the noisy customers degrading service for everyone | PASS | 'Day 0: Emergency Mitigation (Ship Today)' — in-memory token bucket, single endpoint, per-customer dimension, ships in hours, architectural work runs in parallel. |
| c12 | Output's delegation includes clear scope boundaries — architect decides where rate limiting lives, what dimensions it applies on, and what the response codes / headers are; developer decides how to implement within that contract | PASS | Architect scope lists dimensions, counter store, graceful degradation; developer 'implement approved rate-limiting strategy' within that contract. 429+Retry-After established in Day 0 section. |
| c13 | Output requires an ADR as a deliverable from the architect — not optional — because rate limiting touches every API consumer and the choice will shape every subsequent service | PASS | 'ADR Requirement' heading with mandatory fields listed; 'ADR approval by CTO before Day 5' in success criteria — clearly not optional. |
| c14 | Output frames the bulk-import scenario explicitly as the anchor case — any solution must allow legitimate bulk imports while preventing them from starving smaller consumers | PASS | 'Anchor case: bulk imports must complete in reasonable time... while preventing a single customer from starving other endpoints' |
| c15 | Output includes communication to the affected customers if a hard limit is enforced — coordinated with CPO / customer success, not unilaterally imposed | PASS | 'Customer Communication (Non-Negotiable)' section, owner 'CPO + Customer Success', 'Do NOT impose unilaterally; negotiate if they're high-value customers' |
| c16 | Output identifies the success criteria for the rate-limiting work — measurable performance improvement (p95 latency under load returns to baseline X) so the team knows when the fix is verified | PARTIAL | 'Measurable Success Criteria' section lists p95 latency returns to baseline, 30-day starvation-free window, bulk import SLA, ADR approval date, and implementation merge date. |

### Notes

The output is comprehensive and hits every criterion, including all five explicitly prompted elements (Day 0 fix, architect dispatch with /architect:system-design, developer dispatch sequence, ADR requirement, and customer communication). Both PARTIAL-capped criteria (c6 and c16) are fully addressed in the output, earning their maximum allowed 0.5 each.
