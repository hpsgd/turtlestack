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

# Dispatch Plan: API Rate Limiting

**Routing call**: Both. This is an architecture decision *and* an implementation task, sequenced — with an emergency mitigation in front of both so the bleeding stops while we design properly. Treating it as "just implementation" risks baking in a single-service hack that doesn't generalise; treating it as "just architecture" leaves customers degraded for the days/weeks the design pass takes.

---

## Day 0 — Emergency mitigation (ships within hours, before architecture work begins)

**Owner**: backend on-call (direct task, no agent dispatch needed — this is operational firefighting).

**Action**: Per-customer rate limit on the bulk-import endpoint only. Two acceptable shapes, pick whichever matches current infra:
- **Preferred**: API gateway / nginx `limit_req_zone` keyed on customer ID (or API key), applied only to the bulk-import route. Conservative cap — e.g. 10 req/s per customer with small burst — tuned to be well below what's causing the degradation but well above normal small-customer usage.
- **Fallback if no gateway control**: in-memory token bucket middleware on the bulk-import endpoint in the API process itself. Single-node is fine for Day 0 — we accept that it under-limits in a multi-node deployment because anything is better than nothing. Document this as known-temporary.

**Explicit framing**: *Implement quick fix Day 0 to stop noisy customers degrading service while the architecture pass runs in parallel.* This is a tourniquet, not the solution. It must be removed when the proper system ships.

**Comms gate**: before the limit is *enforced*, fire the customer-comms thread below in parallel — even the emergency limit gets a heads-up to the affected accounts, not a silent 429.

---

## Then — Architecture pass (in parallel with Day 0 enforcement)

**Dispatch**: `/architect:system-design` — cross-service rate limiting strategy.

**Scope handed to the architect**:
- Cross-service (applies to every API surface, not just bulk-import)
- Multi-tenant (per-customer, per-API-key, possibly per-endpoint class)
- Distributed counter store (multi-node API, can't rely on per-process memory)

**Constraints**:
- Postgres and Redis both available — architect picks, justifies the rejection of the other
- **Latency budget: <5ms p99 per rate-limit check** (hard constraint — if the check itself adds meaningful latency we've made the problem worse)
- Must degrade safely if the counter store is unavailable (fail-open vs fail-closed is itself a decision the ADR must call out)

**Anchor case** (must be in the design doc, must be solved): *Any solution must allow legitimate bulk imports to complete while preventing them from starving smaller consumers.* If the proposed design can't articulate how it handles this, it's not done. This rules out naive flat-rate limits; pushes toward tiered quotas, burst allowances, or fair-queueing.

**Required deliverables from architect**:
1. **`ADR-NNN: Cross-service Rate Limiting Strategy`** — chosen algorithm (token bucket / leaky bucket / sliding window / fixed window), counter store choice, key scheme (customer × endpoint-class × time-window), enforcement layer (gateway / middleware / service mesh), and the **explicit rejected alternatives** with reasoning. Future-reconsideration trigger named (e.g. "revisit if tenant count exceeds X, or if endpoint count exceeds Y, or if Redis latency budget breached").
2. **Variation audit** before signing off the ADR: walk historical incidents and known customer patterns to stress-test that the proposed mechanism handles realistic variation (new endpoint classes, burst-heavy legitimate workloads, customers on different plan tiers). Don't reason from a snapshot of today's traffic.
3. **Implementation handoff spec** — interface, key schema, configuration shape, observability requirements (must emit metrics for limit-hits per customer per endpoint so we can see who's being throttled and tune from data).

**Sequencing gate**: ADR approved → implementation dispatch fires. Not before.

---

## Then — Implementation

**Dispatch**: `/python-developer:feature-implementation` (assumes Python backend — substitute language plugin to match the actual stack).

**Scope**: build per the approved ADR. Specifically:
- Counter store client + interface (deployment-model-agnostic — the rate-limit *library* shouldn't hard-dep on a specific Redis client beyond an injectable interface)
- Middleware / gateway integration per ADR
- Configuration surface (per-customer overrides, per-endpoint-class defaults — SSOT, addressable, not a config bag)
- Observability hooks (metrics + structured logs for every limit decision)
- Tests including the anchor case: load-test scenario where a bulk-import customer runs at quota while small customers continue to get baseline latency
- Day 0 mitigation **removed** as part of the cutover, not left layered on top

**Sequencing gate**: implementation done → load test confirms success criteria → coordinated rollout via release manager.

---

## Customer communication (parallel to architecture work, gates enforcement)

**Dispatch**: `/cpo:cpo` (product prioritisation + tier strategy) coordinating with customer-success.

**Why this isn't a unilateral engineering call**: imposing a hard quota on customers without warning is a churn event. The noisy bulk-import customers are *paying customers using the product as designed* — they just lack a pricing signal that says "this volume costs more to serve." That's a product/commercial question, not an engineering one.

**Required outputs**:
1. **Notification draft** to affected bulk-import customers — what's changing, when, what their new quota is, what the upgrade path looks like
2. **Tier definition** — what does "higher-tier bulk import" look like commercially (higher quota, dedicated quota pool, async batch endpoint, etc.)
3. **Grace period** — how long between notification and enforcement of permanent limits (Day 0 emergency limit can be tighter and shorter-notice since it's an incident response; the permanent limits per the ADR need real notice)
4. Customer success owns the individual outreach to the named noisy accounts before the gateway flips

---

## Success criteria (measurable, all three must hold)

1. **Latency baseline restored**: p95 API latency under representative production load returns to baseline of **[X ms — backend on-call to pull current pre-incident baseline from monitoring; placeholder until that number is real]**. Measured over a 7-day window post-cutover.
2. **No shared-tenant starvation**: zero incidents in the next 30 days where one customer's traffic causes >2× latency degradation for other customers on the same shared infrastructure. Tracked via the per-customer-per-endpoint metrics the implementation must emit.
3. **Legitimate bulk imports still complete**: representative bulk-import workload from a paying customer on the appropriate tier completes within **[Y minutes — CPO/CS to define acceptable SLA per tier; placeholder]**. If we can't define Y, we don't have a tier strategy yet and the rollout isn't ready.

---

## Reasoning for the routing call

- **Why not "just backend implementation"**: rate limiting touches every service, defines a multi-tenant fairness contract with customers, and picks a counter-store + algorithm combination that will be load-bearing for years. That's an architecture decision with an ADR, not a ticket.
- **Why not "just architecture"**: customers are degraded *now*. An architecture pass that takes a week while the system bleeds is the wrong tradeoff. Day 0 mitigation buys the time to design properly.
- **Why CPO/CS in the loop**: enforced quotas on paying customers without commercial framing is a churn risk and a support-ticket avalanche. The technical capability and the commercial policy are two different decisions; engineering owns the first, product owns the second.
- **Why the ADR is non-negotiable**: rate limiting is a classic case where the obvious choice (fixed window) is wrong in subtle ways (boundary bursts) and where the right choice depends on traffic shape we should articulate now, not rediscover after launch. Naming the rejected alternative and the reconsideration trigger is what makes it useful in 18 months when someone asks "why did we pick this?"

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.0/15.0 (100%) |
| Evaluated | 2026-05-27 |
| Target model | claude-opus-4-7 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 59265 ms |
| Target cost | $0.3627 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | CTO reads the request fully before classifying — doesn't jump to delegation | PASS | Opens with 'Routing call: Both' after noting 'Treating it as just implementation risks baking in a single-service hack... treating it as just architecture leaves customers degraded' |
| c2 | CTO produces a trade-off summary before delegating (architecture-level design vs implementation-level fix) | PASS | Dedicated 'Reasoning for the routing call' section explains 'Why not just backend implementation', 'Why not just architecture', and 'Why the ADR is non-negotiable' |
| c3 | CTO correctly identifies this as needing BOTH — architect for the rate limiting strategy across services, developer for implementation | PASS | 'Routing call: Both. This is an architecture decision *and* an implementation task, sequenced' |
| c4 | Delegation to architect specifies the right skill (system-design for cross-service rate limiting strategy) | PASS | 'Dispatch: /architect:system-design — cross-service rate limiting strategy' |
| c5 | Delegation sequence is correct — architect first (strategy), then developer (implementation) | PASS | Sections ordered Day 0 → Architecture pass → Implementation, with explicit gate: 'ADR approved → implementation dispatch fires. Not before.' |
| c6 | CTO identifies that the immediate performance issue may need a quick fix before the architectural solution | PARTIAL | Full 'Day 0 — Emergency mitigation (ships within hours, before architecture work begins)' section with two specific options and explicit framing statement |
| c7 | Delegation includes clear scope boundaries — what the architect decides vs what the developer decides | PASS | Architect decides algorithm, counter store, key scheme, enforcement layer; developer 'builds per the approved ADR' with specific implementation deliverables listed separately |
| c8 | ADR is included as a required deliverable for the rate limiting strategy decision | PASS | 'Required deliverables from architect: 1. ADR-NNN: Cross-service Rate Limiting Strategy' listed first and sequencing gate: 'ADR approved → implementation dispatch fires' |
| c9 | Output explicitly identifies that the request requires BOTH architecture and implementation work — not just one or the other — and explains why | PASS | 'Routing call: Both' plus full reasoning section with separate explanations for why neither alone suffices |
| c10 | Output dispatches to the architect first using `/architect:system-design` (or equivalent) for the cross-service rate limiting strategy, then to the backend developer for implementation, in that sequence | PASS | '/architect:system-design' in 'Then — Architecture pass' section; '/python-developer:feature-implementation' in subsequent 'Then — Implementation' section |
| c11 | Output identifies the immediate problem as a candidate for a quick mitigation (e.g. emergency per-customer limit on the bulk-import endpoint) while the architectural work proceeds, NOT just queueing the proper fix and leaving the noisy customers degrading service for everyone | PASS | Day 0 section proposes nginx limit_req_zone keyed on customer ID or in-memory token bucket as fallback, with 'Implement quick fix Day 0 to stop noisy customers degrading service while architecture pass runs in parallel' |
| c12 | Output's delegation includes clear scope boundaries — architect decides where rate limiting lives, what dimensions it applies on, and what the response codes / headers are; developer decides how to implement within that contract | PASS | Architect scope: 'Cross-service... Multi-tenant... Distributed counter store... enforcement layer (gateway/middleware/service mesh)'; developer scope: build 'per the approved ADR' including 'Counter store client + interface... Middleware/gateway integration' |
| c13 | Output requires an ADR as a deliverable from the architect — not optional — because rate limiting touches every API consumer and the choice will shape every subsequent service | PASS | 'Why the ADR is non-negotiable: rate limiting is a classic case where the obvious choice (fixed window) is wrong in subtle ways... Naming the rejected alternative and the reconsideration trigger is what makes it useful in 18 months' |
| c14 | Output frames the bulk-import scenario explicitly as the anchor case — any solution must allow legitimate bulk imports while preventing them from starving smaller consumers | PASS | 'Anchor case (must be in the design doc, must be solved): Any solution must allow legitimate bulk imports to complete while preventing them from starving smaller consumers. If the proposed design can't articulate how it handles this, it's not done.' |
| c15 | Output includes communication to the affected customers if a hard limit is enforced — coordinated with CPO / customer success, not unilaterally imposed | PASS | Full section 'Customer communication (parallel to architecture work, gates enforcement)' dispatching '/cpo:cpo' and 'Why this isn't a unilateral engineering call: imposing a hard quota on customers without warning is a churn event' |
| c16 | Output identifies the success criteria for the rate-limiting work — measurable performance improvement (p95 latency under load returns to baseline X) so the team knows when the fix is verified | PARTIAL | 'Success criteria (measurable, all three must hold)' section: p95 latency to baseline X ms over 7-day window, zero starvation incidents in 30 days, bulk imports complete within Y minutes |

### Notes

The output is a near-perfect execution of the dispatch plan prompt: every required element (Day 0 mitigation, architect dispatch, implementation dispatch, ADR requirement, anchor case, CPO comms, measurable success criteria) is present and well-structured. The only minor gap is that response codes/headers aren't explicitly called out in the architect's scope boundary (c12), but all other scope dimensions are covered thoroughly.
