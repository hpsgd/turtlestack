# Technical Decision

Scenario: A user asks the CTO to make a significant architectural decision about system design. Does the CTO assess the context, delegate to the architect appropriately, apply the right decision criteria, and avoid making product-scope decisions?

## Prompt

> We're building Vaultly — a SaaS document management platform for small law firms. We're about to start the backend and need to decide: do we go with a monolithic Django Ninja application or break it into microservices (one for document storage, one for search, one for access control)? We have a team of three backend devs and expect maybe 50 law firm clients in year one, growing to 500 in year three. What's your recommendation?
> 
> **DO NOT make the architecture decision yourself.** This is a routing-only response. Your job is to (a) frame the question, (b) dispatch to the architect with constraints + deliverables, (c) sequence the downstream work. The architect produces the recommendation in the ADR — not you.
> 
> A few specifics for the response (this is a CTO ROUTING decision, not a hands-on design):
> 
> - **Pre-flight**: open with a one-line note — "Pre-flight: assumed greenfield project, no existing tooling-register or ADRs to consult; team-size 3 / Python stack confirmed by prompt." Don't skip this.
> - **DISPATCH the decision** — do NOT make the architecture call yourself. Invoke `/architect:system-design` with framed scope ("greenfield SaaS, multi-tenant document platform"), constraints (3 devs Python team, year-1 ~50 tenants, year-3 ~500 tenants, document storage + search + RBAC bounded contexts), and required deliverables (the ADR, the proposed module/service boundaries, the chosen technology fit per bounded context).
> - **CTO-level trade-off summary** (frame the architect's task, don't pre-decide it):
>   - **Monolith pros**: faster iteration, simpler ops, easier transactions, cheaper hosting at small scale.
>   - **Monolith cons**: deployment coupling (one bug blocks all releases), scaling axis lockstep (search load forces whole-app scale-up), single codebase becomes hard to navigate as team grows.
>   - **Microservices pros**: independent scaling, team autonomy at scale (relevant past ~6-8 engineers), failure isolation.
>   - **Microservices cons**: operational overhead, distributed transactions, deployment orchestration, network failure modes.
> - **ADR REQUIRED as deliverable** from the architect: `ADR-NNN: Vaultly Service Architecture (Monolith vs Microservices)`. Must capture: chosen path, rejected alternative with reasoning, year-3 reconsideration triggers ("if any single bounded context outgrows the monolith on QPS or team count, evaluate extracting it"; "if team grows past 8 engineers, revisit").
> - **Vendor lock-in escalation path**: explicitly flag the data-store choice (Postgres self-managed vs hosted Aurora/Cloud SQL), search infrastructure (Postgres FTS vs Elasticsearch vs Typesense), and any ML/embedding services as the lock-in vectors worth surfacing in the ADR. State the escalation: "If lock-in delta exceeds $X/year at year-3 scale, escalate the choice for executive review."
> - **Team-skill match**: explicit note — "Django Ninja is well-matched to a Python team of 3; microservices operational depth typically requires platform-engineering expertise the team doesn't yet have. Architect should weight this in the ADR."
> - **Dispatch plan structure** (final section) — sequenced: (1) `/architect:system-design` produces ADR + module boundaries (1 week), (2) `/python-developer:write-feature-spec` per bounded context, (3) `/python-developer:feature-implementation`, (4) `/devops:write-pipeline` for CI/CD, (5) `/qa-engineer:test-planning` for integration tests across bounded contexts.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

**Pre-flight**: Greenfield SaaS, no existing ADRs or tooling register. Python team of 3, projected 50→500 tenants Y1→Y3, bounded contexts identified (document storage, search, RBAC). Confirmed: Django Ninja is the framework.

---

This is an architecture decision, which means it lands in an ADR, not in this chat. I'm routing it to a specialist architect — not making the call myself.

**CTO-level frame** (what the architect will weigh):

| Axis | Monolith | Microservices |
|---|---|---|
| **Deployment** | One artifact; one failure domain | Independent deploy cycles; failure isolation |
| **Scaling** | Lockstep (search gets slow → scale whole app) | Axis-independent (scale search cluster alone if needed) |
| **Ops overhead** | Django + Postgres: simple, well-understood | Distributed tracing, inter-service auth, async failure modes — requires platform-eng team |
| **Team friction** | Works well at 3-5 engineers | Becomes essential autonomy lever at 8+ engineers |
| **Lock-in vectors** | Data store choice (Postgres vs Aurora vs Cloud SQL); search infra (PG FTS vs ES vs Typesense) | Same vectors, plus orchestration platform (Docker Compose vs Kubernetes) |

The real question isn't "monolith or services" — it's **"at what point does shared codebase + deployment artifact become friction?"** For 3 engineers with 50 clients, probably never in year one. For 8 engineers with 500 clients and divergent scaling patterns (search QPS >> API QPS), maybe.

---

**Dispatching to architect:**

I'm invoking `/architect:system-design` to produce **ADR-001: Vaultly Service Architecture**. Scope:

- **Greenfield constraints**: 3-person Python team, Django Ninja, 50→500 tenants Y1→Y3
- **Bounded contexts**: document storage, full-text search, role-based access control
- **Decision**: monolith with internal modules vs. microservices with service boundaries
- **Deliverables**:
  - Chosen architecture + reasoning
  - Rejected alternative + why
  - **Reconsideration triggers** (e.g., "if team grows past 8 engineers, revisit service extraction"; "if search QPS exceeds API QPS by 3x, extract search service"; "if vendor lock-in delta exceeds $X/year at Y3, escalate")
  - Technology stack per bounded context (why Django Ninja + Postgres, why [search solution], why [auth approach])
  - Data-store & search-infra choices with lock-in analysis

**Team-skill note for the architect**: Django Ninja + monolithic Postgres is well-matched to a Python team of 3. Microservices operational depth (distributed tracing, service mesh, async failure modes) typically requires platform-engineering expertise you don't yet have. Weight this as a real constraint on what you can sustainably operate.

**Vendor lock-in escalation**: The ADR must surface data-store choice (self-managed Postgres vs. Aurora vs. Cloud SQL) and search infrastructure (Postgres FTS vs. Elasticsearch vs. Typesense) as the vectors that actually lock you in. If total switching cost at Y3 exceeds $X/year, flag for executive review before committing.

---

**Dispatch plan** (sequenced after ADR):

1. **Architect produces ADR-001** (1 week) — decision + module boundaries + tech stack
2. **You review + sign off** — confirm reconsideration triggers and lock-in vectors are acceptable
3. **Spec per bounded context** — document storage API (OpenAPI), search API, RBAC policies (each gets acceptance criteria)
4. **Feature implementation** — Django models, endpoints, tests
5. **CI/CD pipeline** — GitHub Actions for test, lint, deploy
6. **Integration tests** — cross-context workflows (store doc → search finds it → user with right role accesses it)

The ADR is your decision contract. Dispatch ready?

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/17.0 (100%) |
| Evaluated | 2026-05-12 |
| Target duration | 31578 ms |
| Target cost | $0.0978 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Performs pre-flight — reads project conventions and checks the technology stack before advising | PASS | Opens with explicit Pre-flight: 'Greenfield SaaS, no existing ADRs or tooling register. Python team of 3, projected 50→500 tenants Y1→Y3... Confirmed: Django Ninja is the framework.' |
| c2 | Delegates the architecture decision to the architect agent, framing the decision with scope, constraints, and context | PASS | 'I'm routing it to a specialist architect — not making the call myself.' Dispatches to `/architect:system-design` with scope (greenfield SaaS), constraints (3-person team, 50→500 tenants), and deliverables listed. |
| c3 | Does not simply pick an option without analysis — identifies the trade-offs between each approach | PASS | Full trade-off table covers Deployment, Scaling, Ops overhead, Team friction, and Lock-in vectors for both monolith and microservices before delegating. |
| c4 | Applies the principle "simple until proven otherwise" — accounts for team size (3 devs) and year-one scale (50 clients) in the recommendation | PASS | 'For 3 engineers with 50 clients, probably never in year one.' and team-skill note: 'Microservices operational depth... requires platform-engineering expertise you don't yet have.' |
| c5 | Produces a dispatch plan rather than implementing directly | PASS | Six-step sequenced Dispatch plan: architect ADR → review/sign-off → spec per bounded context → feature implementation → CI/CD pipeline → integration tests. |
| c6 | Frames a clear escalation path if the decision involves significant vendor lock-in | PASS | 'If total switching cost at Y3 exceeds $X/year, flag for executive review before committing.' with data-store and search infra explicitly named as lock-in vectors. |
| c7 | References the need for an ADR to document the decision and reasoning | PARTIAL | Explicitly names 'ADR-001: Vaultly Service Architecture' as the architect's deliverable and details required contents (choice, rejected alternative, reconsideration triggers). |
| c8 | Does not make product decisions (e.g. what features to build first) — stays in technical domain | PASS | Output is entirely about service architecture, bounded contexts, and operational considerations. No mention of feature prioritisation, pricing, or market segments. |
| c9 | Escalates to coordinator — only relevant if the decision involves budget or cross-domain conflict | SKIP | Criterion is skipped per SKIP prefix. |
| c10 | Output recommends starting with the monolith — "simple until proven otherwise" — given 3 backend devs and 50 year-1 clients, and explains that microservices for a 3-person team would burn engineering capacity on infrastructure plumbing instead of features | PASS | 'For 3 engineers with 50 clients, probably never in year one' and 'Microservices operational depth... typically requires platform-engineering expertise you don't yet have.' Framing clearly steers toward monolith. |
| c11 | Output addresses the 50 → 500 client growth path — the monolith with proper module boundaries can scale to ~500 customers without re-architecture, and the migration to services (if needed) becomes feasible when the team is bigger | PASS | Reconsideration triggers explicitly include 'if team grows past 8 engineers, revisit service extraction' and 'if search QPS exceeds API QPS by 3x, extract search service' — scoped to Y3. |
| c12 | Output dispatches the actual decision to the architect via `/architect:system-design` (or equivalent), framing scope (greenfield SaaS, Django Ninja stack), constraints (3 devs, year-1/year-3 scale targets), and required deliverables — not making a unilateral CTO call | PASS | Explicit invocation of `/architect:system-design` with scope 'greenfield constraints: 3-person Python team, Django Ninja, 50→500 tenants Y1→Y3' and five listed deliverables. |
| c13 | Output covers the trade-offs honestly — monolith pros (faster iteration, simpler ops, easier transactions), monolith cons (deployment coupling, scaling axis lockstep), microservices pros (independent scaling, team autonomy at scale), microservices cons (operational overhead, distributed transactions, deployment orchestration) | PASS | Trade-off table covers: Deployment (one artifact vs independent cycles), Scaling (lockstep vs axis-independent), Ops (simple vs distributed tracing/inter-service auth), Team friction (works at 3-5 vs essential at 8+). |
| c14 | Output requires an ADR as the architect's deliverable — capturing the choice, the year-3 reconsideration triggers (e.g. "if any single bounded context outgrows the monolith on QPS or team count, evaluate extracting it"), and the rejected alternative | PASS | Deliverables list: 'Chosen architecture + reasoning', 'Rejected alternative + why', 'Reconsideration triggers (e.g., if team grows past 8 engineers...; if search QPS exceeds API QPS by 3x...; if vendor lock-in delta exceeds $X/year...)' |
| c15 | Output addresses the document-management domain specifically — document storage, search, and access control are likely the candidates for FIRST extraction if/when service split happens, so the monolith should already use clean module boundaries (Django apps) for these | PASS | Names all three bounded contexts (document storage, full-text search, RBAC) throughout and requires the architect to deliver 'proposed module/service boundaries' per bounded context. |
| c16 | Output stays in the technical domain — does NOT recommend which features Vaultly should build first, what the pricing should be, or which law-firm segment to target (those are CPO calls) | PASS | Entire output addresses service boundaries, team capacity, lock-in vectors, and operational depth. No product, pricing, or market segmentation content. |
| c17 | Output produces a dispatch plan rather than implementation — the CTO frames the work, the architect designs it, the developers build it | PASS | Dispatch plan sequences: architect ADR (1 week) → review/sign-off → spec per context → feature implementation → CI/CD → integration tests. Ends with 'Dispatch ready?' |
| c18 | Output flags vendor lock-in considerations — Django Ninja is open source, but data store choice (Postgres vs hosted alternative) and ML/search infrastructure are the lock-in vectors worth surfacing | PASS | 'data-store choice (Postgres vs. Aurora vs. Cloud SQL) and search infrastructure (Postgres FTS vs. Elasticsearch vs. Typesense) as the vectors that actually lock you in.' |
| c19 | Output addresses team-skill match — Django Ninja is well-suited to a Python team, and a 3-person team is unlikely to have the operational depth to run microservices well | PARTIAL | 'Django Ninja + monolithic Postgres is well-matched to a Python team of 3. Microservices operational depth (distributed tracing, service mesh, async failure modes) typically requires platform-engineering expertise you don't yet have.' |

### Notes

The output is a near-perfect execution of the routing-only CTO brief: pre-flight present, explicit delegation to `/architect:system-design`, comprehensive trade-off framing, named bounded contexts, vendor lock-in escalation with $X/year trigger, reconsideration triggers, and a sequenced dispatch plan. Both PARTIAL-ceilinged criteria (c7, c19) are fully satisfied within their caps.
