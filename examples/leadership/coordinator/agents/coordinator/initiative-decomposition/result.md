# Initiative Decomposition

Scenario: A major platform change (multi-tenancy) that spans product, engineering, security, and commercial concerns. Tests whether the coordinator decomposes into the right workstreams, maps them to agents, sequences dependencies, and produces a dispatch plan rather than jumping to implementation.

## Prompt

> We want to add multi-tenancy to the platform. Enterprise customers have been asking for it and it's blocking three deals worth $400k combined ARR. The touches everything — data isolation, auth/permissions, billing, UI (workspace switching), documentation, and pricing model changes.
> 
> Do not ask for clarification — proceed based on the information provided. Produce the full decomposition now, noting any assumptions you make.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

# Initiative Decomposition: Multi-tenancy Platform Support

## Context

| Question | Answer |
|---|---|
| **User problem** | Enterprise customers require isolated workspaces for multiple internal teams/departments. Current single-tenant architecture blocks three deals worth $400k combined ARR. |
| **Target user** | Enterprise buyers (100+ seats) with multiple departments, subsidiaries, or cost centers requiring separate namespaces, billing, and permission hierarchies. |
| **Success criteria** | (1) Three identified deals signed by end of initiative; (2) Platform supports 2+ tenants per customer; (3) Zero data leakage between tenants (security audit passes isolation test); (4) Existing single-tenant deployments continue unaffected; (5) Tenant creation/switching available in UI within 2 weeks of launch. |
| **Appetite** | Quarter-long initiative (10–14 weeks). Multi-tenancy rewires auth, data access, billing, and UI — compressed timeline only if Product and Architecture are in lockstep and parallel work is maximised. |
| **Constraints** | (1) Backwards compatibility required — single-tenant mode must remain operational; (2) Data isolation is non-negotiable (regulatory/trust); (3) Existing customers must not experience disruption during rollout; (4) Billing system integration required for per-tenant usage tracking; (5) API versioning or feature gates needed to avoid breaking single-tenant clients. |

---

## Workstreams

### CPO Team Workstreams

| Workstream | Owner role | Initiative-specific deliverables | Relevant? |
|---|---|---|---|
| **Product** | product-owner | Tenant model spec (org/workspace/account hierarchy), feature boundaries by tier, pricing model (per-tenant add-ons or tier-gating), user stories with acceptance criteria (tenant creation, switching, admin console), spec for backwards compatibility during rollout | **Yes** — foundational |
| **Design** | ui-designer | Workspace switcher UI and interaction model, tenant creation/invitation flow, permission matrix visualization, admin console layouts, responsive design for mobile workspace switching, accessibility audit | **Yes** — blocks development |
| **Content** | user-docs-writer | Multi-tenancy concepts guide, tenant admin how-to, API documentation updates (tenant context headers), migration guide for existing customers, FAQ, known limitations | **Yes** — launch blocker |
| **GTM** | gtm | Positioning (which customer tiers unlock multi-tenancy), messaging for three target deals, case study angles, launch announcement, sales enablement deck, competitive positioning vs. single-tenant alternatives | **Yes** — revenue-blocking dependency |
| **Support** | support | Tenant admin training, common issues and troubleshooting guide, permission troubleshooting playbook, escalation procedures for tenant isolation concerns | **Yes** — post-launch readiness |
| **Research** | ux-researcher | Validate tenant model with 2–3 target customers (do they want org/workspace/account hierarchy?), usability test workspace switcher with 5 power users, interview buyers on pricing expectations for multi-tenancy | **Yes** — risk reduction on model |

### CTO Team Workstreams

| Workstream | Owner role | Initiative-specific deliverables | Relevant? |
|---|---|---|---|
| **Architecture** | architect | Tenant context propagation design (context layer approach per event-sourcing rules), data isolation pattern decision (schema separation vs. row-level vs. logical), event model updates (tenant ID in all events), API contract (tenant header/path parameter standard), database schema changes, ADRs for isolation pattern and backwards compatibility strategy | **Yes** — blocks all engineering |
| **Development** | [developer lead] | Auth layer tenant binding, API endpoints for tenant CRUD (create, list, switch, delete), data access layer refactor (tenant filtering in all queries), event sourcing updates (tenant context in aggregate roots), tenant-scoped token generation, workspace switcher implementation, backwards compatibility shims | **Yes** — primary implementation |
| **QA Planning** | qa-lead | Test strategy (isolation matrix: can tenant A read tenant B data?), acceptance criteria from product spec, regression test plan for single-tenant mode, multi-tenant scenario coverage (permission boundaries, billing isolation, event log segregation), performance acceptance criteria (multi-tenant queries latency), security test gates | **Yes** — quality gate |
| **QA Execution** | qa-engineer | Automated integration tests for data isolation (negative tests: verify reads fail across tenants), multi-tenant permission matrix tests, regression suite for single-tenant backwards compatibility, load testing with multiple tenants, manual exploratory testing of edge cases (orphaned tenants, permission inheritance), security-focused testing for isolation leaks | **Yes** — launch gate |
| **DevOps** | devops | Deployment strategy (blue-green, feature-gated rollout by tier), tenant context propagation in observability (logs, traces, metrics tagged by tenant), monitoring dashboards (isolation health, per-tenant query latency, error rates), rollback procedure for tenant isolation bugs, staging environment multi-tenant replica, production deployment runbook | **Yes** — launch gate |
| **Security** | security-engineer | Tenant isolation threat model, isolation pattern review against common bypasses (query parameter injection, permission escalation, event log leakage), audit logging for tenant data access, data residency / compliance implications (GDPR, SOC2), encryption key strategy per tenant vs. shared, security audit acceptance criteria, incident response for suspected isolation breach | **Yes** — non-negotiable |
| **Data** | data-engineer | Event tracking plan (tenant ID in all events), analytics queries scoped to tenant context, per-tenant dashboard setup (usage, API calls, feature adoption), billing data isolation (no cross-tenant revenue leakage), data warehouse modifications for tenant-aware reporting | **Yes** — billing dependency |

---

## Dependencies

| Workstream | Depends on | What it needs before starting | Blocks |
|---|---|---|---|
| **Product** | — | None (can start immediately) | All other workstreams |
| **Research** | Product | Tenant model options to validate with customers | Product refinement (Phase 1 end) |
| **Architecture** | Product | Tenant model definition, API design requirements, isolation risk tolerance | Development, DevOps, Security |
| **Security threat model** | Architecture | Isolation pattern design | Development sign-off, QA test plan |
| **Design** | Product | Tenant model (to inform UI flows), feature tier boundaries | Development |
| **Development** | Architecture + Design + Product | System design docs, API contracts, UI specs, acceptance criteria | QA, DevOps |
| **QA Planning** | Product + Architecture + Security | Acceptance criteria, isolation test matrix, threat model findings | QA Execution (parallel with Dev) |
| **QA Execution** | Development + QA Planning | Working multi-tenant implementation, test plan | Launch gate |
| **DevOps** | Architecture | Infrastructure/deployment strategy decisions | Launch gate |
| **Data** | Product + Development | Tenant model, event model changes, API finalization | Analytics/billing post-launch |
| **Content** | Development (feature freeze) | Working feature screenshots, API documentation, admin console behavior | Launch gate |
| **GTM** | Product + Design | Final positioning, tier definitions, UI screenshots | Launch readiness |
| **Support** | Content + Development | Admin guide, known issues list, permission model documentation | Launch readiness |

---

## Execution Sequence

| Phase | Workstreams (parallel where possible) | Duration | Gate to next phase |
|---|---|---|---|
| **Phase 1 — Define** | Product (tenant model), Architecture (system design), Security (threat model kickoff), Research (customer validation interviews) | 2–3 weeks | PRD approved by leadership, architecture design doc reviewed and signed off by CTO, threat model framework documented |
| **Phase 2 — Specify** | Architecture (API contracts finalized), Design (UX flows and component specs), Security (threat model complete, isolation pattern reviewed), QA Planning (test matrix drafted) | 2 weeks | API contracts frozen, UI specs approved, security review completed with no blockers, test plan ready |
| **Phase 3 — Build** | Development (core isolation layer, auth refactor, API implementation, events), DevOps (infrastructure planning, monitoring setup), Data (event tracking design) | 5–7 weeks | Feature implementation complete, core isolation layer tested locally, API integration tests passing, no known data leakage vectors |
| **Phase 4 — Validate** | QA Execution (isolation tests, regression tests, permission matrix), DevOps (staging deployment, rollback procedures tested), Architecture (code review against design spec) | 2–3 weeks | All QA tests passing, staging multi-tenant environment stable, rollback tested, security review of implementation complete |
| **Phase 5 — Prepare** | Content (documentation complete), GTM (launch plan, sales materials ready), Support (admin training, escalation procedures), Data (billing pipeline tested) | 1–2 weeks | All docs written and reviewed, launch messaging approved, support team trained, billing isolation validated in staging |
| **Phase 6 — Launch** | Coordinated release (feature gate rollout by tier, customer onboarding, GTM announcement) | 1 week | All gates passed, GTM campaign live, first customers onboarded successfully |

### Critical Path

**Product → Architecture → Development → QA Validation → Launch** (10–14 weeks total)

Architecture is the critical bottleneck: any design rework cascades through Dev, QA, and DevOps. Recommend locking architecture by end of Phase 2.

### Parallel Opportunities

- **Product, Architecture, and Security can overlap** (Phases 1–2): Security threat modeling can begin once Architecture sketches isolation pattern, without waiting for full Design.
- **Design and QA Planning can start mid-Phase 2**: Once Product finalizes the model, Design and QA don't need to wait for Architecture API contracts — they can plan in parallel on the UI side.
- **DevOps and Data can start Phase 3**: Infrastructure and analytics planning can proceed alongside Development if Architecture decisions are locked.
- **Content and Support can prep in Phase 4**: No need to wait for full QA sign-off — they can draft docs from the feature spec and refine once QA finds edge cases.

---

## Summary

### Workstream Ownership Table

| Workstream | Owner role | Depends on | Key deliverables | Phase | Estimated effort |
|---|---|---|---|---|---|
| **Product** | product-owner | — | PRD, tenant model spec, user stories, pricing model, acceptance criteria | 1 | 3–4 weeks |
| **Research** | ux-researcher | Product | Customer validation interviews, model feedback, usability findings | 1–2 | 2–3 weeks |
| **Architecture** | architect | Product | System design, API contracts, isolation pattern ADR, event model changes, backwards compatibility strategy | 1–2 | 4–5 weeks |
| **Security** | security-engineer | Architecture | Threat model, isolation review, audit logging spec, incident response plan | 1–2 | 3 weeks |
| **Design** | ui-designer | Product | UX flows, component specs, permission UI, accessibility audit | 2 | 2–3 weeks |
| **Development** | [dev lead] | Architecture + Design | Auth refactor, API implementation, data layer isolation, event sourcing updates, workspace switcher | 3 | 6–8 weeks |
| **QA Planning** | qa-lead | Product + Architecture + Security | Isolation test matrix, acceptance criteria, regression plan, security gates | 2–3 | 1–2 weeks |
| **QA Execution** | qa-engineer | Development + QA Planning | Integration tests, isolation verification, regression testing, security testing | 4 | 2–3 weeks |
| **DevOps** | devops | Architecture | Deployment strategy, monitoring, rollback procedures, staging multi-tenant setup | 3–4 | 2–3 weeks |
| **Data** | data-engineer | Product + Development | Event tracking plan, analytics setup, billing isolation verification | 3–4 | 2–3 weeks |
| **Content** | user-docs-writer | Development | Admin guide, API docs, migration guide, FAQ | 4–5 | 2–3 weeks |
| **GTM** | gtm | Product + Design | Positioning, launch plan, sales enablement, competitive messaging | 4–5 | 2–3 weeks |
| **Support** | support | Content + Development | Admin training, escalation procedures, troubleshooting guides | 5 | 1 week |

### Timeline Estimate

- **Best case:** 10 weeks (no architecture rework, QA passes first round, parallel execution maximized)
- **Likely case:** 12–14 weeks (1 architecture revision cycle, 1 QA iteration, minor DevOps delays, support prep timeline)
- **Risk factors:**
  - Isolation pattern rework (if threat model reveals gaps in Architecture Phase 2) → +2–3 weeks
  - Data layer complexity (if ORM/query refactor is larger than estimated) → +1–2 weeks
  - Third-party integration blocking (e.g., billing system tenant context not supported) → +1–2 weeks
  - Regulatory/compliance discovery mid-build (GDPR, SOC2 multi-tenancy rules) → +1–2 weeks
  - Single-tenant backwards compatibility issues found in QA → +1 week

---

## Assumptions

1. **Tenant model is org-level** (one customer org can have multiple workspaces/teams). Adjust if a different hierarchy is desired.
2. **Data isolation is row-level or logical** (shared schema, tenant filters on all queries). If schema-level separation is required, add 2–3 weeks to Architecture and Development.
3. **Backwards compatibility required during rollout** — implies feature gates and API versioning. Single-tenant deployments must continue working.
4. **No change to event sourcing principles** — tenant context flows as context layer through all aggregates and events per existing event-sourcing rules.
5. **Billing integration exists** and can be extended for per-tenant metering. If billing system rewrites is needed, add 2–3 weeks to Phase 3.
6. **Security audit expected** before launch — allocate 1 week for external review if not included in Security workstream.
7. **Three target deals are warm and waiting** — GTM timeline assumes sales cycle is just waiting for feature availability, not discovery/negotiation.

---

## Follow-ups

- [ ] Validate tenant model and hierarchy with Research workstream (Phase 1 customer interviews)
- [ ] Define OKRs for this initiative — use `/coordinator:define-okrs` after this decomposition is approved
- [ ] Create detailed specs for Product PRD, Architecture ADRs, and API contract — assign to respective owners at Phase 1 end
- [ ] Schedule weekly cross-team syncs (Product, Architecture, Development leads) to unblock dependencies in real-time
- [ ] Identify and reserve one senior developer and one architect for full-time dedication (multi-tenancy is too cross-cutting for part-time work)
- [ ] Establish a "isolation incident protocol" — how Security and DevOps escalate suspected data leakage issues during and after launch

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/17.0 (94%) |
| Evaluated | 2026-05-12 |
| Target duration | 53810 ms |
| Target cost | $0.0724 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Coordinator decomposes into workstreams that map to specific agents (architect for data isolation, CPO for pricing, developer for implementation, etc.) | PASS | Summary table lists owner roles per workstream: product-owner, architect, security-engineer, ui-designer, qa-lead, qa-engineer, devops, data-engineer, user-docs-writer, gtm, support, ux-researcher. |
| c2 | Dependencies between workstreams are identified and sequenced (e.g., data isolation design before implementation, pricing before billing) | PASS | Dedicated 'Dependencies' table lists each workstream, what it depends on, what it needs before starting, and what it blocks (e.g., Architecture depends on Product, blocks Development). |
| c3 | Both CPO and CTO workstreams are present — this is not purely technical (pricing, documentation, UX are product concerns) | PASS | Output explicitly separates 'CPO Team Workstreams' (Product, Design, Content, GTM, Support, Research) and 'CTO Team Workstreams' (Architecture, Development, QA, DevOps, Security, Data). |
| c4 | The decomposition includes effort estimates or sizing signals for each workstream | PASS | Summary table includes 'Estimated effort' column with ranges for every workstream, e.g. 'Development: 6–8 weeks', 'Architecture: 4–5 weeks', 'Security: 3 weeks'. |
| c5 | A critical path is identified — which workstreams block everything else | PASS | 'Critical Path' section states: 'Product → Architecture → Development → QA Validation → Launch' and 'Architecture is the critical bottleneck: any design rework cascades through Dev, QA, and DevOps.' |
| c6 | Revenue context ($400k ARR) is used to inform priority and timeline, not just mentioned | PARTIAL | $400k ARR noted in context table; success criteria links to 'Three identified deals signed by end of initiative'; assumption notes 'deals are warm and waiting.' Used to justify urgency but not deeply tied to timeline compression. |
| c7 | Security implications of multi-tenancy are called out as a specific workstream or constraint | PASS | Dedicated Security workstream with deliverables: 'Tenant isolation threat model, isolation pattern review against common bypasses, audit logging, encryption key strategy per tenant vs. shared, incident response for isolation breach.' |
| c8 | The output is a dispatch plan, not implementation — the coordinator doesn't write code or specs | PASS | Output contains only workstream tables, dependency maps, phase sequences, effort ranges, and role assignments — no code, schema definitions, or implementation specs anywhere in the document. |
| c9 | Output's workstreams cover at minimum: data isolation (architect / data engineer), auth and permissions (architect / security), billing changes (CPO + finance), UI workspace switching (UX + UI designer + developer), documentation (technical writer), pricing model (CPO + GTM) | PASS | All six areas present: Architecture covers data isolation and auth; Security covers permissions; GTM+Product cover pricing; Design+Development cover workspace switcher UI; user-docs-writer covers documentation. |
| c10 | Output's dependency map shows that data isolation design must complete before implementation, that pricing decisions must inform billing implementation, and that auth/permissions design feeds the UI workspace switching | PASS | Dependencies table: 'Development depends on Architecture + Design + Product'; 'Architecture depends on Product (isolation risk tolerance)'; 'GTM depends on Product + Design (tier definitions)' mapping all three required chains. |
| c11 | Output identifies the critical path — likely data isolation design → auth/permissions design → implementation → migration of existing customers — and names what blocks what | PASS | 'Critical Path: Product → Architecture → Development → QA Validation → Launch'; Dependencies table explicitly states each workstream's blockers and blocked workstreams. |
| c12 | Output uses the $400k ARR context to inform priority — connecting the dollar value to a target delivery date or quarter, not just citing the figure once | PARTIAL | $400k cited in context table; success criteria references deal closure; 'Quarter-long initiative (10–14 weeks)' appetite set. No explicit statement connecting the dollar amount to a specific delivery deadline or quarter. |
| c13 | Output flags multi-tenancy security as a distinct workstream — covering tenant isolation, blast-radius if one tenant is compromised, and customer-level encryption keys / data sovereignty options | PASS | Security workstream explicitly covers: tenant isolation threat model, 'encryption key strategy per tenant vs. shared', 'incident response for suspected isolation breach' (blast-radius), and 'data residency / compliance (GDPR, SOC2)'. |
| c14 | Output includes effort estimates per workstream as ranges (e.g. "data isolation design: 2-3 weeks", "billing changes: 4-6 weeks") — not single-point estimates that imply false precision | PASS | Every workstream in the Summary table has range estimates: 'Architecture: 4–5 weeks', 'Development: 6–8 weeks', 'Security: 3 weeks', 'QA Execution: 2–3 weeks', etc. |
| c15 | Output is a dispatch plan — names the agent or role per workstream, the deliverable per workstream, and the entry/exit criteria — does NOT contain code, schema definitions, or implementation specs | PASS | Summary table has owner role and key deliverables columns; Execution Sequence table lists 'Gate to next phase' criteria per phase; no code or schema present anywhere. |
| c16 | Output covers BOTH CPO (pricing model, packaging tiers, GTM messaging, customer comms for existing customers) AND CTO (data, auth, infra) workstreams — multi-tenancy is not purely technical | PASS | CPO section includes Product (pricing model, tier boundaries), GTM (positioning, sales enablement), Content (migration guide for existing customers); CTO section includes Architecture, Development, DevOps, Security, Data. |
| c17 | Output addresses migration of existing single-tenant customers as a workstream — they need to be moved into the new model without disruption, and this typically blocks final cutover | PARTIAL | Backwards compatibility addressed in Architecture ('backwards compatibility strategy'), DevOps ('feature-gated rollout'), Content ('migration guide for existing customers'), and Assumptions. No dedicated migration workstream or explicit statement it blocks final cutover. |
| c18 | Output identifies parallel opportunities — e.g. UX research on workspace switching can run while data isolation is being designed, technical-writer documentation drafting can run alongside implementation | PARTIAL | Dedicated 'Parallel Opportunities' section: 'Design and QA Planning can start mid-Phase 2', 'Content and Support can prep in Phase 4' alongside QA, 'DevOps and Data can start Phase 3' alongside Development. |

### Notes

The output is a strong, comprehensive dispatch plan that correctly separates CPO and CTO concerns, maps all workstreams to roles, and provides explicit dependency tables and phase gates. The two main gaps are: the $400k ARR is acknowledged but never explicitly drives a deadline or timeline compression decision, and existing single-tenant customer migration is distributed across workstreams rather than called out as a blocking workstream in its own right.
