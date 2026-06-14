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

Pre-flight: assumed greenfield project, no existing tooling-register or ADRs to consult; team-size 3 / Python stack confirmed by prompt.

## Framing — Vaultly backend architecture

This is an architecture decision (monolith vs microservices) for a greenfield multi-tenant SaaS. Per CTO routing, I'm framing the question and dispatching to the architect — the recommendation lives in the ADR, not here.

## Dispatch — `/architect:system-design`

**Scope:** Greenfield SaaS, multi-tenant document management platform for small law firms.

**Constraints:**
- Team: 3 backend developers, Python stack (Django Ninja confirmed as candidate framework).
- Scale trajectory: ~50 tenants year 1 → ~500 tenants year 3.
- Bounded contexts identified: document storage, search, access control (RBAC).
- No existing platform-engineering capability on the team.

**Required deliverables:**
1. `ADR-NNN: Vaultly Service Architecture (Monolith vs Microservices)` capturing chosen path, rejected alternative with reasoning, and year-3 reconsideration triggers.
2. Proposed module/service boundaries per bounded context.
3. Chosen technology fit per bounded context (data store, search infra, auth/RBAC mechanism).

## CTO-level trade-off summary (for the architect to weigh — not pre-decided)

**Monolith**
- Pros: faster iteration, simpler ops, easier transactional integrity, cheaper hosting at small scale.
- Cons: deployment coupling (one bug blocks all releases), scaling axis lockstep (search load forces whole-app scale-up), single codebase navigability degrades as team grows.

**Microservices**
- Pros: independent scaling, team autonomy at scale (typically relevant past ~6–8 engineers), failure isolation per bounded context.
- Cons: operational overhead, distributed-transaction complexity, deployment orchestration burden, additional network failure modes.

**Team-skill match note for the architect:** Django Ninja is well-matched to a Python team of 3. Microservices operational depth typically requires platform-engineering expertise this team doesn't yet have — architect should weight this in the ADR.

## ADR requirements — reconsideration triggers (must be captured)

- "If any single bounded context outgrows the monolith on QPS or team count, evaluate extracting it."
- "If team grows past 8 engineers, revisit the boundary decision."

## Vendor lock-in — escalation path (must be surfaced in the ADR)

Lock-in vectors to flag explicitly:
- **Data store:** Postgres self-managed vs hosted (Aurora / Cloud SQL).
- **Search infrastructure:** Postgres FTS vs Elasticsearch vs Typesense.
- **ML / embedding services** (if any are introduced for semantic search or doc classification).

Escalation rule: **"If lock-in delta exceeds $X/year at year-3 scale, escalate the choice for executive review."** ($X to be set during ADR drafting — recommend a concrete dollar figure tied to year-3 revenue projection.)

## Dispatch plan — sequenced

1. **`/architect:system-design`** — ADR + module boundaries + technology fit per bounded context. *Target: 1 week.*
2. **`/python-developer:write-feature-spec`** — one spec per bounded context (document storage, search, RBAC), driven off the ADR's boundary decisions.
3. **`/python-developer:feature-implementation`** — implement per spec.
4. **`/devops:write-pipeline`** — CI/CD pipeline matched to the chosen deployment model (single artefact vs per-service).
5. **`/qa-engineer:test-planning`** — integration test plan spanning bounded contexts.

Next step: confirm and I'll invoke `/architect:system-design` with the framing above.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.5/17.0 (91%) |
| Evaluated | 2026-06-13 |
| Target model | claude-opus-4-7 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 19421 ms |
| Target cost | $0.2957 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Performs pre-flight — reads project conventions and checks the technology stack before advising | PASS | Opens verbatim: "Pre-flight: assumed greenfield project, no existing tooling-register or ADRs to consult; team-size 3 / Python stack confirmed by prompt." |
| c2 | Delegates the architecture decision to the architect agent, framing the decision with scope, constraints, and context | PASS | "Dispatch — `/architect:system-design`" section provides scope ("Greenfield SaaS, multi-tenant..."), constraints (team, scale, bounded contexts), and required deliverables. |
| c3 | Does not simply pick an option without analysis — identifies the trade-offs between each approach | PASS | "CTO-level trade-off summary" lists monolith pros/cons and microservices pros/cons explicitly with "not pre-decided" framing. |
| c4 | Applies the principle "simple until proven otherwise" — accounts for team size (3 devs) and year-one scale (50 clients) in the recommendation | PASS | Constraints list "3 backend developers" and "~50 tenants year 1"; team-skill note says "Microservices operational depth typically requires platform-engineering expertise this team doesn't yet have." |
| c5 | Produces a dispatch plan rather than implementing directly | PASS | "Dispatch plan — sequenced" section lists 5 numbered steps from architect through QA, explicitly sequenced with no implementation by the CTO. |
| c6 | Frames a clear escalation path if the decision involves significant vendor lock-in | PASS | "Escalation rule: 'If lock-in delta exceeds $X/year at year-3 scale, escalate the choice for executive review.'" with three lock-in vectors named. |
| c7 | References the need for an ADR to document the decision and reasoning | PARTIAL | ADR-NNN required as deliverable #1; separate "ADR requirements" section specifies reconsideration triggers and rejected alternative capture. |
| c8 | Does not make product decisions (e.g. what features to build first) — stays in technical domain | PASS | Output contains only architectural framing, dispatch plan, trade-off analysis, and vendor lock-in — no feature prioritisation, pricing, or market-segment decisions. |
| c9 | Escalates to coordinator — only relevant if the decision involves budget or cross-domain conflict | SKIP | Criterion marked SKIP — not evaluated. |
| c10 | Output recommends starting with the monolith — "simple until proven otherwise" — given 3 backend devs and 50 year-1 clients, and explains that microservices for a 3-person team would burn engineering capacity on infrastructure plumbing instead of features | PARTIAL | Team-skill note strongly implies monolith preference: "Microservices operational depth typically requires platform-engineering expertise this team doesn't yet have." But explicit recommendation is deliberately deferred to architect per routing instruction. |
| c11 | Output addresses the 50 → 500 client growth path — the monolith with proper module boundaries can scale to ~500 customers without re-architecture, and the migration to services (if needed) becomes feasible when the team is bigger | PARTIAL | Scale trajectory "~50 tenants year 1 → ~500 tenants year 3" in constraints; reconsideration triggers cover extraction conditions. Does not explicitly state monolith can scale to 500 without re-arch. |
| c12 | Output dispatches the actual decision to the architect via `/architect:system-design` (or equivalent), framing scope (greenfield SaaS, Django Ninja stack), constraints (3 devs, year-1/year-3 scale targets), and required deliverables — not making a unilateral CTO call | PASS | Dispatch section invokes "`/architect:system-design`" with scope, constraints (team, scale, bounded contexts), and three numbered deliverables. Explicitly states "recommendation lives in the ADR, not here." |
| c13 | Output covers the trade-offs honestly — monolith pros (faster iteration, simpler ops, easier transactions), monolith cons (deployment coupling, scaling axis lockstep), microservices pros (independent scaling, team autonomy at scale), microservices cons (operational overhead, distributed transactions, deployment orchestration) | PASS | All four trade-off quadrants covered verbatim: monolith pros include "faster iteration, simpler ops, easier transactional integrity"; cons include "deployment coupling"; microservices pros include "independent scaling"; cons include "operational overhead, distributed-transaction complexity." |
| c14 | Output requires an ADR as the architect's deliverable — capturing the choice, the year-3 reconsideration triggers (e.g. "if any single bounded context outgrows the monolith on QPS or team count, evaluate extracting it"), and the rejected alternative | PASS | Required deliverable #1 is ADR capturing "chosen path, rejected alternative with reasoning, and year-3 reconsideration triggers"; triggers quoted verbatim match the criterion. |
| c15 | Output addresses the document-management domain specifically — document storage, search, and access control are likely the candidates for FIRST extraction if/when service split happens, so the monolith should already use clean module boundaries (Django apps) for these | PARTIAL | "Bounded contexts identified: document storage, search, access control (RBAC)" named; "Proposed module/service boundaries per bounded context" required. No explicit "first extraction candidates" or "Django apps" framing. |
| c16 | Output stays in the technical domain — does NOT recommend which features Vaultly should build first, what the pricing should be, or which law-firm segment to target (those are CPO calls) | PASS | Entire output covers architecture, dispatch plan, vendor lock-in, and technology fit. No features, pricing, or market-segment content anywhere. |
| c17 | Output produces a dispatch plan rather than implementation — the CTO frames the work, the architect designs it, the developers build it | PASS | Five-step sequenced plan: architect → python-developer (spec) → python-developer (impl) → devops → qa-engineer. CTO produces no implementation. |
| c18 | Output flags vendor lock-in considerations — Django Ninja is open source, but data store choice (Postgres vs hosted alternative) and ML/search infrastructure are the lock-in vectors worth surfacing | PASS | "Lock-in vectors to flag explicitly: Data store: Postgres self-managed vs hosted (Aurora / Cloud SQL). Search infrastructure: Postgres FTS vs Elasticsearch vs Typesense. ML / embedding services." |
| c19 | Output addresses team-skill match — Django Ninja is well-suited to a Python team, and a 3-person team is unlikely to have the operational depth to run microservices well | PARTIAL | "Team-skill match note for the architect: Django Ninja is well-matched to a Python team of 3. Microservices operational depth typically requires platform-engineering expertise this team doesn't yet have." |

### Notes

The output is a near-textbook CTO routing response — pre-flight, trade-off framing, dispatch, ADR requirement, vendor lock-in escalation, and dispatch plan all present and well-formed. The only consistent gap is that criteria requiring an explicit monolith recommendation (c10, c11, c15) are only partially met because the output correctly defers the recommendation to the architect per the routing instruction, creating a tension between those criteria and the routing-only constraint.
