# Initiative Decomposition

Scenario: A major platform change (multi-tenancy) that spans product, engineering, security, and commercial concerns. Tests whether the coordinator decomposes into the right workstreams, maps them to agents, sequences dependencies, and produces a dispatch plan rather than jumping to implementation.

## Prompt

> We want to add multi-tenancy to the platform. Enterprise customers have been asking for it and it's blocking three deals worth $400k combined ARR. The touches everything — data isolation, auth/permissions, billing, UI (workspace switching), documentation, and pricing model changes.
> 
> Do not ask for clarification — proceed based on the information provided. Produce the full decomposition now, noting any assumptions you make.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

# Initiative Decomposition: Multi-Tenancy Platform Capability

## Assumptions stated up-front

Since clarification was disallowed, this plan is built on the following assumptions. Any of them flipping changes scope materially — flag them at PRD review.

1. **Current state:** Single-tenant SaaS; users belong to a single global account namespace; no "workspace" or "organisation" abstraction exists today.
2. **Tenancy model:** Pooled (shared DB + per-row `tenant_id` discriminator, enforced at the data-access layer / RLS). Silo-per-tenant DBs and dedicated infra are explicitly rejected as the *default* but allowed as an enterprise-tier upgrade later.
3. **Identity model:** Users can belong to one or more workspaces with workspace-scoped roles. Existing accounts migrate into a personal/legacy workspace 1:1.
4. **Auth scope:** SSO (SAML/OIDC) is in scope as an enterprise prerequisite — at least one of the three blocking deals will require it.
5. **Billing model:** Today is per-seat individual; target is per-workspace subscription with seat counts, invoiced (enterprise) plus self-serve credit-card (SMB).
6. **Commercial pressure:** Three deals worth $400k ARR want this *this quarter*. Appetite is **one quarter (10–13 weeks)** to GA, with an enterprise-pilot milestone at ~week 8.
7. **Library-vs-application:** Platform is an application, not a library — framework coupling is acceptable.
8. **Domain conventions:** hps.gd naming (`Hps\Gd\…` namespace if PHP; `hps-gd/<project>` repo names).

## Context

### Initiative context

| Question | Answer |
|---|---|
| **User problem** | Enterprise buyers cannot adopt the platform because (a) their data co-mingles with other customers in a shared namespace, (b) they cannot map their org structure (departments, business units) onto the product, (c) they cannot administer their own users/roles/SSO, and (d) procurement/billing expects one contract per organisation, not per seat. Their security and compliance reviewers reject the product at the data-isolation gate. |
| **Target user** | Two distinct personas. **Primary:** Enterprise IT administrator at a 200–2000 seat organisation evaluating the platform — needs SSO, workspace-level admin, audit logs, contract billing. **Secondary:** End user inside that enterprise — needs frictionless workspace switching, clear workspace context, no regressions to existing single-tenant UX. **Existing self-serve users** are explicitly an affected persona (migration must be invisible to them). |
| **Success criteria** | **Commercial:** all three blocked deals close within 30 days of GA ($400k ARR booked). **Adoption:** ≥80% of active accounts migrated to workspace model within 4 weeks of GA with <0.5% support-ticket regression rate. **Isolation:** zero cross-tenant data leak incidents in the 90 days post-GA (measured by automated isolation test suite running continuously + zero P0/P1 incidents). **Sales motion:** average enterprise security-review cycle reduced from "blocked" to ≤10 business days. **Self-serve health:** no measurable drop in self-serve activation or D7 retention through the migration window. |
| **Appetite** | **One quarter (10–13 weeks)** to GA. Enterprise-pilot milestone at week 8 (one of the three deals as design-partner customer in production). This is **fixed-time, variable-scope** — features beyond the MVP enterprise checklist defer to a fast-follow. |
| **Constraints** | (a) Migration of existing accounts must be zero-downtime and reversible for at least 14 days. (b) Cannot break public API contracts for existing API consumers without a deprecation window — versioned API or backwards-compatible defaults required. (c) Billing changes touch revenue recognition — finance must sign off on accounting treatment before GA. (d) SOC 2 (or equivalent) controls cannot regress; isolation evidence must be auditable. (e) Pricing model change requires Legal + GTM alignment — existing customers' contracts cannot be unilaterally repriced. (f) Three live enterprise deals = real-customer scrutiny during build; design-partner agreements likely needed. |

**NFR note (Martin-style):** the *tenancy model itself* — pooled vs. silo, RLS vs. app-layer enforcement, single- vs. multi-region — should be **cleanly encoded so it can be changed without invasive rework** ([[learned--martin-nfr-flavour-answers-to-ambiguity]]). The codebase should treat tenant context as a single-source-of-truth value object threaded through every request, not as a tenant_id column added column-by-column. This is an ADR-worthy decision and warrants a historical-variation audit ([[learned--walk-variation-history-before-accepting-versioning-adr]]) — review past data-model migrations to confirm the chosen mechanism can evolve.

**Platform-as-package note:** auth, data isolation, billing, and hosting interact and must be evaluated **together**, not as five independent ADRs ([[learned--evaluate-platforms-as-package]]). A consolidated multi-tenancy ADR is preferable to five sibling ADRs that cascade-rewrite when one changes.

---

## Workstreams

### CPO team workstreams

| Workstream | Owner role | Key deliverables (initiative-specific) | Relevant? |
|---|---|---|---|
| **Product** | product-owner | PRD covering workspace concept, member/role model, invite & onboarding flows, workspace switching UX, admin console scope, migration story for existing users, pricing & packaging decisions, deprecation of legacy single-tenant flows. User stories per persona (enterprise admin, end user, self-serve incumbent). Acceptance criteria including isolation invariants ("user in workspace A must never see object owned by workspace B"). Explicit MVP-vs-fast-follow scope list. | **Yes** — central. The workspace concept is a new primary domain object. |
| **Design** | ui-designer | Workspace switcher pattern (global nav), workspace-scoped settings IA, admin console screens (members, roles, SSO, billing, audit log), workspace creation/invite flows, "you are now in workspace X" affordance, empty/onboarding states for new workspaces, error states (permission denied, workspace deleted). Component spec for workspace context indicator. Accessibility review of all new flows. | **Yes** — workspace switching is a new top-level UX pattern. |
| **Content** | user-docs-writer | New "Workspaces" section in docs; admin guide (SSO setup, role management, billing); end-user guide ("switching workspaces", "what changed"); migration FAQ for existing self-serve users; API docs updates for tenant-scoped endpoints; release notes; in-app onboarding copy. | **Yes** — admin persona has zero existing documentation surface. |
| **GTM** | gtm | Enterprise positioning ("now built for teams"); pricing-page rework (per-workspace + per-seat); sales enablement (security one-pager, isolation architecture diagram, SOC 2 mapping); launch comms (existing customers, prospects, the three blocked deals specifically); pricing-grandfathering policy for existing customers. | **Yes** — pricing model change + enterprise positioning is a launch in itself. |
| **Support** | support | Runbook for workspace/member/role issues; escalation path for suspected cross-tenant leakage (P0 protocol); FAQ on migration; training session for support team; tagging schema in ticketing for tenancy-related issues; pre-launch beta-customer support model. | **Yes** — new failure modes and a P0 incident class (data leak). |
| **Research** | ux-researcher | Validate workspace-switcher pattern with 5–8 enterprise admins (preferably from the three blocked deals); usability test admin console with target persona; journey-map enterprise procurement → activation; post-launch survey instrument. | **Yes** — net-new persona (enterprise admin); existing research likely doesn't cover them. |

### CTO team workstreams

| Workstream | Owner role | Key deliverables (initiative-specific) | Relevant? |
|---|---|---|---|
| **Architecture** | architect | **Consolidated multi-tenancy ADR** (tenancy model, identity model, billing-coupling, hosting impact — evaluated as a package per [[learned--evaluate-platforms-as-package]]). System design covering: tenant context propagation (request → service → data layer), data isolation enforcement (RLS or equivalent), workspace lifecycle (create, suspend, delete, restore), SSO architecture (SAML + OIDC abstractions), audit log architecture, migration strategy for existing data. API contract v2 (tenant-scoped). Threat model interface. Historical-variation audit of past data-model migrations to validate evolvability ([[learned--walk-variation-history-before-accepting-versioning-adr]]). | **Yes** — foundational. |
| **Development** | developer (lead) | Workspace + membership domain model; tenant-context middleware; data-access layer enforcement; admin-console UI; workspace-switcher UI; SSO integration; audit logging; migration scripts (zero-downtime, reversible 14 days); billing integration; API v2 endpoints; deprecation shims for v1. **Streams:** (1) data/isolation, (2) identity/auth/SSO, (3) admin & switcher UX, (4) billing & metering, (5) migration & compatibility. | **Yes** — five parallel sub-streams under one lead. |
| **QA Planning** | qa-lead | Test strategy for isolation invariants (the highest-stakes test class); SSO matrix (IdPs to test: Okta, Azure AD, Google Workspace, generic SAML); migration test plan (production-shaped data, rollback validation); pricing/billing test scenarios; performance test plan (does tenant_id indexing regress hot queries?); regression matrix for existing flows. **Quality gate definitions** per phase. | **Yes** — isolation is a hard correctness gate, not a "we'll find bugs" workstream. |
| **QA Execution** | qa-engineer | Automated isolation test suite (per-endpoint, per-resource, asserting no cross-tenant access; run continuously post-GA); SSO integration tests; migration dry-runs against production-shaped data; performance regression suite; manual exploratory testing of admin console and switcher. | **Yes** — substantial new test surface. |
| **DevOps** | devops | Infrastructure for workspace-scoped resources (object storage prefixing, queue routing if relevant); RLS/policy deployment in DB; rollout plan (feature flag, gradual cohort migration); monitoring dashboards (per-tenant metrics, cross-tenant leak alarms); audit log pipeline; SSO IdP onboarding runbook; rollback plan with 14-day reversibility window. | **Yes** — non-trivial infra and a high-risk rollout. |
| **Security** | security-engineer | Threat model (focus: cross-tenant escape, privilege escalation within workspace, SSO assertion forgery, audit-log tampering); security review at end of Phase 2 and end of Phase 3; SOC 2 controls mapping (or equivalent); penetration test of isolation boundaries pre-GA; incident-response runbook for suspected leakage (P0); review of audit log completeness for compliance evidence. | **Yes** — isolation is the primary security promise of the initiative. |
| **Data** | data-engineer | Event schema additions (`workspace_id` on every event); per-workspace analytics dashboards (for product team + for enterprise admin in-app); migration of historical event data to workspace context; revenue dashboards reflecting new pricing model; data dictionary updates. | **Yes** — every existing event needs tenant context retrofitted; new pricing model needs revenue analytics. |

**Excluded / not-relevant workstreams:** none. Every CPO and CTO workstream is in scope. This is a "touches everything" initiative — that is the user's framing and it survives scrutiny.

---

## Dependencies

### Dependency map

| Workstream | Depends on | What it needs before starting | Blocks |
|---|---|---|---|
| Product | — | Stated assumptions confirmed or revised; access to the three blocked deals for input | Architecture, Design, GTM, Research |
| Architecture | Product (lightweight) | High-level scope, isolation NFR, enterprise checklist; can run in parallel with PRD detailing | Development, DevOps, Security, Data |
| Research | Product (skeleton) | Persona definition and rough flows | Final Design, GTM positioning |
| Design | Product, Research (initial findings) | PRD with flows; preliminary research signal on switcher pattern | Development (UI streams) |
| Security (threat model) | Architecture | Tenancy model + identity model from ADR | Development (gates the isolation enforcement design) |
| Development — data/isolation | Architecture, Security threat model | ADR + threat model | QA isolation tests, all other dev streams (provides tenant context primitive) |
| Development — identity/SSO | Architecture, data/isolation primitive | Tenant-context primitive landed | QA SSO matrix |
| Development — admin & switcher UI | Design, identity primitive | Specs + working membership model | QA UI regression |
| Development — billing | Product (pricing decisions), Architecture | Pricing model finalised; tenant primitive | QA billing scenarios, GTM pricing page |
| Development — migration | All other dev streams (sufficient model to migrate into) | Stable workspace + membership model | DevOps rollout, QA migration tests |
| QA Planning | Product, Architecture | Acceptance criteria + system design | QA Execution |
| QA Execution | Development (per stream as completed) | Buildable feature per stream | Launch gate |
| DevOps | Architecture, Development (migration) | Infra decisions + migration scripts | Launch gate |
| Data | Architecture, Development (event emission) | Tenant-context primitive; event schema decisions | Dashboards used by GTM and Support |
| Content | Design (final UX), Development (stable enough for screenshots) | Working admin console | Support training, Launch |
| Support | Content, QA findings | Docs + known-issues list | Launch gate |
| GTM | Product (pricing), Design (final UX), Research findings | Pricing locked; positioning validated | Launch |

---

## Execution sequence

| Phase | Workstreams (parallel) | Duration | Gate to next phase |
|---|---|---|---|
| **1 — Define** | Product (PRD draft), Architecture (consolidated multi-tenancy ADR draft + variation audit), Research (enterprise-admin interviews, ideally with the three deals), Security (initial threat-model framing) | 2 weeks | **Gate G1:** PRD approved by CPO + CTO; multi-tenancy ADR accepted (variation audit attached); pricing model decision locked with Finance + GTM sign-off; design-partner agreement with at least one blocked deal. |
| **2 — Design & Foundation** | Design (admin console + switcher specs), Security (threat model finalised), Development — data/isolation primitive (tenant context, RLS enforcement, test harness), QA Planning (strategy + isolation test framework), DevOps (RLS/policy infra spike, feature-flag plumbing), Data (event schema decisions) | 2–3 weeks | **Gate G2:** Tenant-context primitive merged behind flag; isolation test framework demonstrably catches a planted leak; UX specs accepted; threat model signed off; pricing page wireframes accepted. |
| **3 — Build** | Dev streams in parallel: identity/SSO, admin & switcher UI, billing, migration; QA Execution (isolation suite, SSO matrix, migration dry-runs running continuously); Content (drafting alongside stable specs); Data (dashboards as events land) | 4–5 weeks | **Gate G3:** Feature-complete behind flag; isolation suite green on every PR; SSO matrix green for at least Okta + Azure AD + generic SAML; migration dry-run on production-shaped data passes + rollback verified; performance regression within budget; pen-test scheduled. |
| **4 — Validate & Pilot** | QA Execution (full regression + exploratory), DevOps (staging-prod parity, monitoring dashboards live, rollback rehearsed), Security (pen test), Support (training + runbooks), GTM (sales enablement assets), enterprise-pilot customer onboarded in production behind flag | 2 weeks | **Gate G4:** Pen test passed (no high/critical open); pilot customer in production with green metrics for ≥5 business days; finance sign-off on revenue recognition; support team trained; rollback rehearsal successful. |
| **5 — Prepare launch** | GTM (launch comms scheduled, pricing page staged), Content (docs published in staging), Support (on-call schedule, P0 protocol live), Product (existing-customer migration comms), legal review of grandfathering policy | 1 week (overlaps end of Phase 4) | **Gate G5:** Launch checklist 100%; existing-customer migration plan signed off; on-call rota confirmed; rollback authority and criteria documented. |
| **6 — GA & migrate** | Coordinated release; staged rollout (internal → design partner → 10% → 50% → 100%); existing-customer migration in cohorts; close the three deals | 1–2 weeks to 100%, with 4-week migration tail | Initiative success criteria met (see Context). |

### Critical path

**Product (PRD) → Architecture (ADR) → Dev: data/isolation primitive → Dev: identity/SSO → QA (isolation + SSO) → Pilot → GA.**

The tenant-context primitive in Phase 2 is the single most important deliverable — every other dev stream consumes it. **It must be merged by end of week 4** or the whole timeline slips.

### Parallel opportunities

- Research interviews and PRD authoring run in parallel during Phase 1; research informs Design directly without serialising through Product.
- Within Phase 3, the four dev sub-streams (identity, admin UI, billing, migration) all consume the Phase-2 isolation primitive and proceed independently.
- Content and Data dashboards begin in Phase 3 against the stabilising feature, not waiting for code-complete.
- GTM enablement assets are drafted in Phase 3 in parallel with development, finalised after Gate G3.
- The pilot in Phase 4 runs in production behind a flag while regression QA continues — pilot is *not* a separate gated wait.

---

## Summary

### Workstream summary

| Workstream | Owner | Depends on | Key deliverables | Phase(s) | Estimated effort |
|---|---|---|---|---|---|
| Product | product-owner | — | PRD, pricing decisions, MVP scope, migration story | 1, ongoing | 2–3 weeks lead + 0.3 FTE through GA |
| Architecture | architect | Product (light) | Consolidated multi-tenancy ADR + variation audit, system design, API v2 contract | 1–2 | 2–3 weeks lead + 0.3 FTE through GA |
| Research | ux-researcher | Product (skeleton) | Enterprise admin interviews, switcher usability, post-launch instrument | 1, 4 | 1.5–2.5 weeks total |
| Design | ui-designer | Product, Research (initial) | Admin console, switcher, settings IA, accessibility review | 2 | 2–3 weeks |
| Security | security-engineer | Architecture | Threat model, security gates, pen test, SOC 2 mapping | 1, 2, 4 | 2–3 weeks dispersed |
| Dev — data/isolation | developer | Architecture, Security | Tenant context primitive, RLS, isolation test harness | 2 | 2–3 weeks (critical path) |
| Dev — identity/SSO | developer | Isolation primitive, Architecture | Membership model, SAML + OIDC, audit log | 3 | 3–4 weeks |
| Dev — admin & switcher | developer | Design, identity primitive | Admin console, workspace switcher | 3 | 3–4 weeks |
| Dev — billing | developer | Product (pricing), Architecture | Per-workspace subscription, seat counting, invoicing integration | 3 | 2–3 weeks |
| Dev — migration | developer | Other dev streams (stable model) | Zero-downtime migration scripts, 14-day reversibility | 3, 6 | 2–3 weeks build + execution tail |
| QA Planning | qa-lead | Product, Architecture | Test strategy, isolation framework, SSO matrix, gate definitions | 2 | 1.5–2 weeks lead + ongoing |
| QA Execution | qa-engineer | Development (per stream) | Automated isolation suite, SSO tests, regression, manual exploratory | 3–4 | 4–5 weeks across phases |
| DevOps | devops | Architecture | Infra, feature flags, monitoring, rollout plan, rollback | 2–4 | 2.5–3.5 weeks dispersed |
| Data | data-engineer | Architecture, Dev (events) | Event schema, dashboards, historical retrofit, revenue analytics | 2–3 | 2 weeks |
| Content | user-docs-writer | Design (final), Development (stable) | Workspaces docs, admin guide, migration FAQ, API v2 docs | 3–5 | 2 weeks |
| GTM | gtm | Product (pricing), Design, Research | Positioning, pricing page, enablement, launch comms, grandfathering policy | 3–5 | 2 weeks |
| Support | support | Content, QA findings | Runbooks, P0 protocol, training, ticket schema | 4–5 | 1 week |

### Timeline estimate

- **Best case:** **10 weeks** to GA — PRD/ADR land cleanly in Phase 1, no surprise in SSO IdP integration, migration dry-runs pass first time, pen test clean.
- **Likely case:** **12–13 weeks** to GA — typical friction on SSO matrix (one IdP misbehaves), one migration rework cycle, one round of pen-test findings to remediate.
- **Worst credible case:** **16+ weeks** — isolation primitive needs rework after threat model (the ADR was wrong), billing accounting treatment blocks finance sign-off, or pen-test surfaces an architectural flaw.

### Risk factors

1. **Isolation primitive ships late or wrong.** Single biggest schedule risk. Mitigation: start Architecture in Phase 1 (not Phase 2); land the primitive behind a flag *before* identity/UI/billing streams begin; isolation test harness must catch planted leaks at Gate G2.
2. **Migration of existing customers.** Reversibility window + zero downtime is genuinely hard. Mitigation: full production-shape dry-runs in Phase 3; staged cohort rollout in Phase 6; rollback rehearsal at Gate G4.
3. **Pricing model change angers existing customers.** Grandfathering policy must be signed off by Legal + GTM + Finance before launch comms. Mitigation: Phase 1 pricing lock; explicit grandfathering plan in Gate G5.
4. **SSO IdP variability.** SAML in practice is not SAML in spec. Mitigation: matrix-test against real IdPs in Phase 3; design partner from the blocked deals provides at least one real-world test target.
5. **Cross-tenant leak post-GA.** P0 incident class with reputational stakes. Mitigation: continuous isolation suite in CI + production; explicit P0 protocol live before Gate G5; audit log completeness verified by Security.
6. **Three deals churn while waiting.** Commercial risk. Mitigation: design-partner agreement at Gate G1 with at least one of the three; transparent timeline to Sales; pilot milestone at week 8 demonstrable to the other two.
7. **Conflating "workspace" and "tenant".** Vocabulary drift causes contract bugs. Mitigation: PRD names the concept once and the ADR aligns; code uses one term throughout.

---

## Follow-ups

- [ ] **Confirm or revise the 8 stated assumptions** before Gate G1 — especially tenancy model (pooled vs. silo) and pricing model. Any reversal here is a re-decomposition.
- [ ] **Define OKRs** for this initiative — run `/coordinator:define-okrs` against the success criteria above (close-rate, isolation incident count, self-serve retention, security-review cycle time).
- [ ] **Write the consolidated multi-tenancy ADR** as a *single package decision* covering tenancy + identity + billing + hosting interactions ([[learned--evaluate-platforms-as-package]]). Attach the historical-variation audit ([[learned--walk-variation-history-before-accepting-versioning-adr]]).
- [ ] **Lock the design-partner agreement** with one of the three blocked deals before end of Phase 1.
- [ ] **Spec each workstream** — run `/coordinator:write-spec` per major workstream (PRD, system design, test strategy, GTM plan) so each owner has a contract before Phase 2 begins.
- [ ] **Finance sign-off path** for revenue recognition under the new pricing model — initiate in Phase 1, gate at Phase 4.
- [ ] **Schedule the pen test** in Phase 1 (lead time is real) for execution in Phase 4.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 19.5/20.0 (98%) |
| Evaluated | 2026-06-13 |
| Target model | claude-opus-4-7 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 152856 ms |
| Target cost | $0.5493 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Coordinator decomposes into workstreams that map to specific agents (architect for data isolation, CPO for pricing, developer for implementation, etc.) | PASS | Workstream table explicitly maps: architect → multi-tenancy ADR, product-owner → PRD, developer → 5 sub-streams, security-engineer → threat model, gtm → pricing page. |
| c2 | Dependencies between workstreams are identified and sequenced (e.g., data isolation design before implementation, pricing before billing) | PASS | Full dependency table lists 'Dev — data/isolation' depends on Architecture + Security threat model; 'Dev — billing' depends on 'Product (pricing decisions), Architecture'. |
| c3 | Both CPO and CTO workstreams are present — this is not purely technical (pricing, documentation, UX are product concerns) | PASS | Separate 'CPO team workstreams' section covers product-owner, ui-designer, user-docs-writer, gtm, support, ux-researcher; 'CTO team workstreams' covers architect, developer, qa, devops, security, data. |
| c4 | The decomposition includes effort estimates or sizing signals for each workstream | PASS | Summary table includes 'Estimated effort' column with range estimates per workstream, e.g. 'Dev — data/isolation: 2–3 weeks (critical path)', 'QA Execution: 4–5 weeks across phases'. |
| c5 | A critical path is identified — which workstreams block everything else | PASS | 'Critical path' section: 'Product (PRD) → Architecture (ADR) → Dev: data/isolation primitive → Dev: identity/SSO → QA → Pilot → GA.' with explicit 'must be merged by end of week 4' statement. |
| c6 | Revenue context ($400k ARR) is used to inform priority and timeline, not just mentioned | PARTIAL | Assumption 6 sets 'one quarter (10–13 weeks) to GA' driven by '3 deals worth $400k ARR'; Risk 6 explicitly names 'three deals churn while waiting' with mitigation. Used to anchor timeline and risk. |
| c7 | Security implications of multi-tenancy are called out as a specific workstream or constraint | PASS | Security workstream lists: threat model (cross-tenant escape, privilege escalation, SSO forgery, audit-log tampering), pen test, SOC 2 mapping, P0 incident-response runbook, gates at G2 and G4. |
| c8 | The output is a dispatch plan, not implementation — the coordinator doesn't write code or specs | PASS | No code, schema, or implementation spec appears. Output consists of workstream tables, dependency map, phase sequence, gate criteria, and follow-up action items delegating spec-writing to sub-agents. |
| c9 | Output's workstreams cover at minimum: data isolation (architect / data engineer), auth and permissions (architect / security), billing changes (CPO + finance), UI workspace switching (UX + UI designer + developer), documentation (technical writer), pricing model (CPO + GTM) | PASS | All six areas explicitly covered: data isolation (architect ADR + dev isolation stream), auth/SSO (dev identity stream + security), billing (dev billing stream + finance sign-off), workspace switcher UI (ui-designer + dev admin/switcher), content/docs (user-docs-writer), pricing (product-owner + gtm). |
| c10 | Output's dependency map shows that data isolation design must complete before implementation, that pricing decisions must inform billing implementation, and that auth/permissions design feeds the UI workspace switching | PASS | Dependency table: 'Dev — data/isolation' needs Architecture + Security first; 'Dev — billing' needs 'pricing model finalised'; 'Dev — admin & switcher UI' needs 'identity primitive' landed. |
| c11 | Output identifies the critical path — likely data isolation design → auth/permissions design → implementation → migration of existing customers — and names what blocks what | PASS | Critical path section names exact chain; also notes 'Dev — migration' depends on 'stable workspace + membership model' from other streams; migration blocks 'DevOps rollout, QA migration tests'. |
| c12 | Output uses the $400k ARR context to inform priority — connecting the dollar value to a target delivery date or quarter, not just citing the figure once | PASS | Assumption 6 connects $400k + 'this quarter' → fixed 10–13 week appetite; Risk 6 ties deal-churn to mitigation (design-partner at G1, pilot at week 8 demonstrable to other two deals). |
| c13 | Output flags multi-tenancy security as a distinct workstream — covering tenant isolation, blast-radius if one tenant is compromised, and customer-level encryption keys / data sovereignty options | PARTIAL | Security workstream covers isolation and SSO forgery; threat model mentions 'cross-tenant escape'. Customer-level encryption keys and data sovereignty are not explicitly addressed. |
| c14 | Output includes effort estimates per workstream as ranges (e.g. 'data isolation design: 2-3 weeks', 'billing changes: 4-6 weeks') — not single-point estimates that imply false precision | PASS | Every row in the summary table uses ranges: 'Dev — data/isolation: 2–3 weeks', 'Dev — billing: 2–3 weeks', 'QA Execution: 4–5 weeks across phases', etc. No single-point estimates. |
| c15 | Output is a dispatch plan — names the agent or role per workstream, the deliverable per workstream, and the entry/exit criteria — does NOT contain code, schema definitions, or implementation specs | PASS | Each workstream row names role, key deliverables, and phase gate criteria (G1–G5). No code or schema present. Follow-ups delegate spec writing via '/coordinator:write-spec per major workstream'. |
| c16 | Output covers BOTH CPO (pricing model, packaging tiers, GTM messaging, customer comms for existing customers) AND CTO (data, auth, infra) workstreams — multi-tenancy is not purely technical | PASS | Dedicated 'CPO team workstreams' section covers pricing, GTM, support, docs, research. 'CTO team workstreams' covers architecture through data engineering. Both fully populated. |
| c17 | Output addresses migration of existing single-tenant customers as a workstream — they need to be moved into the new model without disruption, and this typically blocks final cutover | PASS | 'Dev — migration' is a named workstream: 'zero-downtime migration scripts, 14-day reversibility'; dependency table shows it blocks DevOps rollout and QA migration tests; Phase 6 includes 'existing-customer migration in cohorts'. |
| c18 | Output identifies parallel opportunities — e.g. UX research on workspace switching can run while data isolation is being designed, technical-writer documentation drafting can run alongside implementation | PARTIAL | 'Parallel opportunities' section explicitly lists: research + PRD in parallel in Phase 1; four dev sub-streams parallel in Phase 3; content + dashboards begin in Phase 3 against stabilising feature; GTM assets drafted in Phase 3 parallel with development. |

### Notes

The output is an exceptionally thorough dispatch plan that covers all required workstreams, dependency sequencing, phased execution with named gates, and explicit parallel opportunities. The only minor gap is c13 — customer-level encryption keys and data sovereignty options are not addressed in the security workstream, though blast-radius and isolation are.
