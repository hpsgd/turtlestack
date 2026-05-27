---
# Match the model the agent declares (opus) in
# plugins/leadership/cto/agents/cto.md. The runner otherwise
# falls back to the harness default (Haiku), which is not what the
# agent is designed to run on.
target-model: claude-opus-4-7
---

# Test: Ambiguous routing between architect and developer

Scenario: A request that blurs the line between architecture decision and implementation task. The CTO must decide whether to send this to the architect, a developer, or both, and in what order.

## Prompt

We need to add rate limiting to our API. We're getting hammered by a few customers doing bulk imports and it's degrading performance for everyone else. Not sure if this is an architecture decision about how rate limiting should work across our services, or just an implementation task for the backend developer.

Do not ask for clarification — make the routing decision now, produce the delegation plan, and state your reasoning.

A few specifics for the response (this is a DISPATCH plan, not advisory guidance):

- **Quick mitigation FIRST (interim, before architecture work)** — propose an emergency per-customer or per-endpoint rate limit on the bulk-import endpoint that can ship within hours (e.g. nginx / API gateway rule, or a simple in-memory token bucket on that one endpoint). State explicitly: "Implement quick fix Day 0 to stop noisy customers degrading service while architecture pass runs in parallel."
- **Then dispatch architect**: invoke `/architect:system-design` for the cross-service rate limiting strategy. Frame scope (cross-service, multi-tenant, distributed counter store), constraints (Postgres or Redis available; latency budget <5ms per check), required deliverables, and the **anchor case**: "any solution must allow legitimate bulk imports while preventing them from starving smaller consumers."
- **Then dispatch backend developer**: `/python-developer:feature-implementation` (or equivalent) for implementation, AFTER the architect's design is approved.
- **ADR required**: name the deliverable explicitly — `ADR-NNN: Cross-service Rate Limiting Strategy`, capturing the chosen approach, the rejected alternative (e.g. token bucket vs leaky bucket vs fixed window), and the future reconsideration trigger.
- **Customer communication via CPO/customer-success**: if a hard limit is enforced, coordinate with `cpo:cpo` and customer success — do NOT impose unilaterally. Notify the noisy bulk-import customers with a quota and a higher-tier upgrade path.
- **Success criteria (measurable)**: state explicitly — "p95 API latency under representative load returns to baseline of X ms; no shared-tenant starvation event in the next 30 days; legitimate bulk imports complete within Y minutes."

## Criteria

- [ ] PASS: CTO reads the request fully before classifying — doesn't jump to delegation
- [ ] PASS: CTO produces a trade-off summary before delegating (architecture-level design vs implementation-level fix)
- [ ] PASS: CTO correctly identifies this as needing BOTH — architect for the rate limiting strategy across services, developer for implementation
- [ ] PASS: Delegation to architect specifies the right skill (system-design for cross-service rate limiting strategy)
- [ ] PASS: Delegation sequence is correct — architect first (strategy), then developer (implementation)
- [ ] PARTIAL: CTO identifies that the immediate performance issue may need a quick fix before the architectural solution
- [ ] PASS: Delegation includes clear scope boundaries — what the architect decides vs what the developer decides
- [ ] PASS: ADR is included as a required deliverable for the rate limiting strategy decision

## Output expectations

- [ ] PASS: Output explicitly identifies that the request requires BOTH architecture and implementation work — not just one or the other — and explains why
- [ ] PASS: Output dispatches to the architect first using `/architect:system-design` (or equivalent) for the cross-service rate limiting strategy, then to the backend developer for implementation, in that sequence
- [ ] PASS: Output identifies the immediate problem as a candidate for a quick mitigation (e.g. emergency per-customer limit on the bulk-import endpoint) while the architectural work proceeds, NOT just queueing the proper fix and leaving the noisy customers degrading service for everyone
- [ ] PASS: Output's delegation includes clear scope boundaries — architect decides where rate limiting lives, what dimensions it applies on, and what the response codes / headers are; developer decides how to implement within that contract
- [ ] PASS: Output requires an ADR as a deliverable from the architect — not optional — because rate limiting touches every API consumer and the choice will shape every subsequent service
- [ ] PASS: Output frames the bulk-import scenario explicitly as the anchor case — any solution must allow legitimate bulk imports while preventing them from starving smaller consumers
- [ ] PASS: Output includes communication to the affected customers if a hard limit is enforced — coordinated with CPO / customer success, not unilaterally imposed
- [ ] PARTIAL: Output identifies the success criteria for the rate-limiting work — measurable performance improvement (p95 latency under load returns to baseline X) so the team knows when the fix is verified
