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

**Routing decision:** Both. This is an architecture decision AND an implementation task, in that order — but ship a tactical fix Day 0 so the architecture work isn't done under a fire alarm.

**Reasoning:** Cross-service rate limiting touches request routing, multi-tenancy, distributed state, latency budget, and customer commercial tiers. That's architectural — a backend dev implementing in isolation will produce a per-process in-memory limiter that breaks the moment we scale horizontally, and a quota model that customer success has to clean up after. But the bleeding is happening *now*, so a narrow tactical limit on the one offending endpoint must ship in parallel, not be gated on the architecture pass.

---

## Day 0 — Quick mitigation (ships within hours)

**Implement quick fix Day 0 to stop noisy customers degrading service while architecture pass runs in parallel.**

- **Scope:** the bulk-import endpoint only. Not a system-wide limiter.
- **Mechanism:** API gateway / nginx `limit_req` rule keyed on customer/tenant ID, OR a single-endpoint in-memory token bucket in the backend if the gateway can't key on tenant. Pick whichever is faster to ship given current infra.
- **Limit value:** set conservatively from current p95/p99 traffic of the top-3 offenders — enough headroom that legitimate imports complete, low enough that one customer can't saturate a worker pool.
- **Return:** `429 Too Many Requests` with `Retry-After` header. Log every rejection with tenant ID for the architect's traffic analysis.
- **Owner:** backend dev (no design doc needed — this is a known-throwaway).
- **Explicitly flagged as interim.** Will be replaced by the cross-service design. Don't let it ossify.

## Day 0 (parallel) — Customer comms

Coordinate with `cpo:cpo` and customer success **before** the gateway rule lands in prod, even though it's tactical. Noisy bulk-import customers get:
- a heads-up that a temporary throttle is going on,
- the quota number,
- a path to a higher tier if their volume is legitimate.

Do NOT impose unilaterally. The tactical fix is technically reversible; a surprised enterprise customer is not.

---

## Step 1 — Dispatch architect

**Invoke:** `/architect:system-design`

**Frame:**
- **Scope:** cross-service, multi-tenant rate limiting strategy. Applies to every public API surface, not just bulk import.
- **Constraints:**
  - Postgres and Redis both available; pick one (or justify both) on latency and operational grounds.
  - Latency budget: **<5ms per check** at p99.
  - Must work across horizontally-scaled backend instances (distributed counter, not per-process state).
  - Must support per-tenant quotas of varying size (commercial tiering).
- **Anchor case:** *"any solution must allow legitimate bulk imports while preventing them from starving smaller consumers."* This is the design's load-bearing test. A naive global limit fails it.
- **Required deliverables:**
  - `ADR-NNN: Cross-service Rate Limiting Strategy` — chosen approach, rejected alternatives (token bucket vs leaky bucket vs fixed window vs sliding log), and the **future reconsideration trigger** (e.g. "revisit if p99 check latency exceeds 5ms, or if we add a third datacenter").
  - System diagram showing where the limiter sits in the request path (edge gateway? sidecar? in-process middleware with shared store?).
  - Quota model: how tiers map to limits, how bulk-import customers get a dedicated bucket vs sharing a pool.
  - Failure mode: what happens when the counter store is unavailable. Fail open or fail closed? Justified.
  - Migration plan: how the Day 0 tactical limit is retired without a service gap.

**Approval gate:** ADR must be approved before Step 2 starts.

---

## Step 2 — Dispatch backend developer

**Invoke:** `/python-developer:feature-implementation` (or language-equivalent for the service stack).

**Only after ADR approval.** Brief includes:
- The approved ADR as the source of truth.
- Test plan covering the anchor case: simulated bulk-import customer running at quota does not increase p95 latency for a concurrent small-consumer workload.
- Removal of the Day 0 tactical limit as part of the same change.
- Observability: per-tenant rejection counts, latency of the check itself, counter-store health.

---

## Success criteria (measurable)

- **p95 API latency** under representative load returns to baseline of **X ms** (architect to fill X from current SLO doc; if no SLO exists, capture pre-incident baseline as part of the design).
- **No shared-tenant starvation event** in the next **30 days** — defined as: no period >5 min where small consumers see elevated 5xx/latency attributable to bulk-import traffic.
- **Legitimate bulk imports complete within Y minutes** at the assigned quota (architect to define Y per tier, validated with the top-3 affected customers via customer success).

---

## Summary

Day 0: gateway limit on bulk-import endpoint + CPO/CS comms. Day 1+: architect drafts ADR-NNN for cross-service strategy. Post-approval: backend implements, retires the tactical limit. Quick fix lets the architecture be designed deliberately rather than under fire.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.5/16.0 (97%) |
| Evaluated | 2026-06-13 |
| Target model | claude-opus-4-7 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 34060 ms |
| Target cost | $0.5386 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | CTO reads the request fully before classifying — doesn't jump to delegation | PASS | Output opens with 'Routing decision: Both' and provides a full reasoning paragraph covering cross-service concerns, horizontal scaling, and customer tiers before any delegation. |
| c2 | CTO produces a trade-off summary before delegating (architecture-level design vs implementation-level fix) | PASS | Reasoning section: 'a backend dev implementing in isolation will produce a per-process in-memory limiter that breaks the moment we scale horizontally' — explicit arch vs impl trade-off. |
| c3 | CTO correctly identifies this as needing BOTH — architect for the rate limiting strategy across services, developer for implementation | PASS | 'Routing decision: Both. This is an architecture decision AND an implementation task, in that order' |
| c4 | Delegation to architect specifies the right skill (system-design for cross-service rate limiting strategy) | PASS | Step 1 explicitly states 'Invoke: /architect:system-design' with scope framed as 'cross-service, multi-tenant rate limiting strategy' |
| c5 | Delegation sequence is correct — architect first (strategy), then developer (implementation) | PASS | Step 2 opens with 'Only after ADR approval.' and Step 1 precedes Step 2 in the plan with an explicit approval gate. |
| c6 | CTO identifies that the immediate performance issue may need a quick fix before the architectural solution | PARTIAL | Day 0 section: 'Implement quick fix Day 0 to stop noisy customers degrading service while architecture pass runs in parallel' — fully addressed. |
| c7 | Delegation includes clear scope boundaries — what the architect decides vs what the developer decides | PASS | Architect deliverables include ADR, quota model, failure mode, migration plan. Developer brief: 'The approved ADR as the source of truth' with removal of Day 0 limit and observability. |
| c8 | ADR is included as a required deliverable for the rate limiting strategy decision | PASS | 'ADR-NNN: Cross-service Rate Limiting Strategy — chosen approach, rejected alternatives... and the future reconsideration trigger' listed under Required deliverables. |
| c9 | Output explicitly identifies that the request requires BOTH architecture and implementation work — not just one or the other — and explains why | PASS | 'This is an architecture decision AND an implementation task' with reasoning on horizontal scaling breakage and commercial tier quota model as justification. |
| c10 | Output dispatches to the architect first using `/architect:system-design` (or equivalent) for the cross-service rate limiting strategy, then to the backend developer for implementation, in that sequence | PASS | Step 1 invokes `/architect:system-design`, Step 2 invokes `/python-developer:feature-implementation`, with explicit sequencing and approval gate between them. |
| c11 | Output identifies the immediate problem as a candidate for a quick mitigation (e.g. emergency per-customer limit on the bulk-import endpoint) while the architectural work proceeds, NOT just queueing the proper fix and leaving the noisy customers degrading service for everyone | PASS | Day 0 section specifies nginx `limit_req` or in-memory token bucket on bulk-import endpoint, 429 with Retry-After, 'Explicitly flagged as interim. Will be replaced by the cross-service design.' |
| c12 | Output's delegation includes clear scope boundaries — architect decides where rate limiting lives, what dimensions it applies on, and what the response codes / headers are; developer decides how to implement within that contract | PASS | Architect scope includes 'where the limiter sits in the request path', quota model, failure mode. Developer brief: implement per approved ADR, remove Day 0 limit, add observability. |
| c13 | Output requires an ADR as a deliverable from the architect — not optional — because rate limiting touches every API consumer and the choice will shape every subsequent service | PASS | ADR listed under 'Required deliverables' (not suggested). 'Approval gate: ADR must be approved before Step 2 starts' makes it mandatory. |
| c14 | Output frames the bulk-import scenario explicitly as the anchor case — any solution must allow legitimate bulk imports while preventing them from starving smaller consumers | PASS | 'Anchor case: any solution must allow legitimate bulk imports while preventing them from starving smaller consumers. This is the design's load-bearing test.' |
| c15 | Output includes communication to the affected customers if a hard limit is enforced — coordinated with CPO / customer success, not unilaterally imposed | PASS | Day 0 parallel section: 'Coordinate with cpo:cpo and customer success before the gateway rule lands in prod... Do NOT impose unilaterally.' |
| c16 | Output identifies the success criteria for the rate-limiting work — measurable performance improvement (p95 latency under load returns to baseline X) so the team knows when the fix is verified | PARTIAL | Success criteria section lists p95 latency, 30-day starvation-free window, and bulk import completion time Y — all three measurable, with X deferred to architect from SLO doc. |

### Notes

The output is comprehensive and well-structured, hitting every criterion including the anchor case, ADR as mandatory deliverable, CPO coordination, and Day 0 tactical fix. The only minor gap is that success criteria placeholder values (X ms, Y minutes) are deferred to the architect rather than providing even rough estimates, but this is reasonable given the stated absence of an SLO doc.
