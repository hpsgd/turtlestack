---
# Match the model the agent declares (opus) in
# plugins/leadership/cto/agents/cto.md. The runner otherwise
# falls back to the harness default (Haiku), which is not what the
# agent is designed to run on.
target-model: claude-opus-4-7
---

# Test: technical decision

Scenario: A user asks the CTO to make a significant architectural decision about system design. Does the CTO assess the context, delegate to the architect appropriately, apply the right decision criteria, and avoid making product-scope decisions?

## Prompt

We're building Vaultly — a SaaS document management platform for small law firms. We're about to start the backend and need to decide: do we go with a monolithic Django Ninja application or break it into microservices (one for document storage, one for search, one for access control)? We have a team of three backend devs and expect maybe 50 law firm clients in year one, growing to 500 in year three. What's your recommendation?

**DO NOT make the architecture decision yourself.** This is a routing-only response. Your job is to (a) frame the question, (b) dispatch to the architect with constraints + deliverables, (c) sequence the downstream work. The architect produces the recommendation in the ADR — not you.

A few specifics for the response (this is a CTO ROUTING decision, not a hands-on design):

- **Pre-flight**: open with a one-line note — "Pre-flight: assumed greenfield project, no existing tooling-register or ADRs to consult; team-size 3 / Python stack confirmed by prompt." Don't skip this.
- **DISPATCH the decision** — do NOT make the architecture call yourself. Invoke `/architect:system-design` with framed scope ("greenfield SaaS, multi-tenant document platform"), constraints (3 devs Python team, year-1 ~50 tenants, year-3 ~500 tenants, document storage + search + RBAC bounded contexts), and required deliverables (the ADR, the proposed module/service boundaries, the chosen technology fit per bounded context).
- **CTO-level trade-off summary** (frame the architect's task, don't pre-decide it):
  - **Monolith pros**: faster iteration, simpler ops, easier transactions, cheaper hosting at small scale.
  - **Monolith cons**: deployment coupling (one bug blocks all releases), scaling axis lockstep (search load forces whole-app scale-up), single codebase becomes hard to navigate as team grows.
  - **Microservices pros**: independent scaling, team autonomy at scale (relevant past ~6-8 engineers), failure isolation.
  - **Microservices cons**: operational overhead, distributed transactions, deployment orchestration, network failure modes.
- **ADR REQUIRED as deliverable** from the architect: `ADR-NNN: Vaultly Service Architecture (Monolith vs Microservices)`. Must capture: chosen path, rejected alternative with reasoning, year-3 reconsideration triggers ("if any single bounded context outgrows the monolith on QPS or team count, evaluate extracting it"; "if team grows past 8 engineers, revisit").
- **Vendor lock-in escalation path**: explicitly flag the data-store choice (Postgres self-managed vs hosted Aurora/Cloud SQL), search infrastructure (Postgres FTS vs Elasticsearch vs Typesense), and any ML/embedding services as the lock-in vectors worth surfacing in the ADR. State the escalation: "If lock-in delta exceeds $X/year at year-3 scale, escalate the choice for executive review."
- **Team-skill match**: explicit note — "Django Ninja is well-matched to a Python team of 3; microservices operational depth typically requires platform-engineering expertise the team doesn't yet have. Architect should weight this in the ADR."
- **Dispatch plan structure** (final section) — sequenced: (1) `/architect:system-design` produces ADR + module boundaries (1 week), (2) `/python-developer:write-feature-spec` per bounded context, (3) `/python-developer:feature-implementation`, (4) `/devops:write-pipeline` for CI/CD, (5) `/qa-engineer:test-planning` for integration tests across bounded contexts.

## Criteria

- [ ] PASS: Performs pre-flight — reads project conventions and checks the technology stack before advising
- [ ] PASS: Delegates the architecture decision to the architect agent, framing the decision with scope, constraints, and context
- [ ] PASS: Does not simply pick an option without analysis — identifies the trade-offs between each approach
- [ ] PASS: Applies the principle "simple until proven otherwise" — accounts for team size (3 devs) and year-one scale (50 clients) in the recommendation
- [ ] PASS: Produces a dispatch plan rather than implementing directly
- [ ] PASS: Frames a clear escalation path if the decision involves significant vendor lock-in
- [ ] PARTIAL: References the need for an ADR to document the decision and reasoning
- [ ] PASS: Does not make product decisions (e.g. what features to build first) — stays in technical domain
- [ ] SKIP: Escalates to coordinator — only relevant if the decision involves budget or cross-domain conflict

## Output expectations

- [ ] PASS: Output recommends starting with the monolith — "simple until proven otherwise" — given 3 backend devs and 50 year-1 clients, and explains that microservices for a 3-person team would burn engineering capacity on infrastructure plumbing instead of features
- [ ] PASS: Output addresses the 50 → 500 client growth path — the monolith with proper module boundaries can scale to ~500 customers without re-architecture, and the migration to services (if needed) becomes feasible when the team is bigger
- [ ] PASS: Output dispatches the actual decision to the architect via `/architect:system-design` (or equivalent), framing scope (greenfield SaaS, Django Ninja stack), constraints (3 devs, year-1/year-3 scale targets), and required deliverables — not making a unilateral CTO call
- [ ] PASS: Output covers the trade-offs honestly — monolith pros (faster iteration, simpler ops, easier transactions), monolith cons (deployment coupling, scaling axis lockstep), microservices pros (independent scaling, team autonomy at scale), microservices cons (operational overhead, distributed transactions, deployment orchestration)
- [ ] PASS: Output requires an ADR as the architect's deliverable — capturing the choice, the year-3 reconsideration triggers (e.g. "if any single bounded context outgrows the monolith on QPS or team count, evaluate extracting it"), and the rejected alternative
- [ ] PASS: Output addresses the document-management domain specifically — document storage, search, and access control are likely the candidates for FIRST extraction if/when service split happens, so the monolith should already use clean module boundaries (Django apps) for these
- [ ] PASS: Output stays in the technical domain — does NOT recommend which features Vaultly should build first, what the pricing should be, or which law-firm segment to target (those are CPO calls)
- [ ] PASS: Output produces a dispatch plan rather than implementation — the CTO frames the work, the architect designs it, the developers build it
- [ ] PASS: Output flags vendor lock-in considerations — Django Ninja is open source, but data store choice (Postgres vs hosted alternative) and ML/search infrastructure are the lock-in vectors worth surfacing
- [ ] PARTIAL: Output addresses team-skill match — Django Ninja is well-suited to a Python team, and a 3-person team is unlikely to have the operational depth to run microservices well
