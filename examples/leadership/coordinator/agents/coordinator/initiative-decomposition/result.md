# Initiative Decomposition

Scenario: A major platform change (multi-tenancy) that spans product, engineering, security, and commercial concerns. Tests whether the coordinator decomposes into the right workstreams, maps them to agents, sequences dependencies, and produces a dispatch plan rather than jumping to implementation.

## Prompt

> We want to add multi-tenancy to the platform. Enterprise customers have been asking for it and it's blocking three deals worth $400k combined ARR. The touches everything — data isolation, auth/permissions, billing, UI (workspace switching), documentation, and pricing model changes.
> 
> Do not ask for clarification — proceed based on the information provided. Produce the full decomposition now, noting any assumptions you make.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

# Initiative Decomposition: Multi-tenancy for the Platform

## Context

### Initiative context

| Question | Answer |
|---|---|
| **User problem** | Enterprise buyers can't adopt because they need a single account boundary that isolates their org's data, users, billing, and admin controls from other customers — and today the platform is single-tenant per user. Three procurement processes are stalled on this. |
| **Target user** | Enterprise IT/security buyer (approves the purchase) + Workspace Admin (day-to-day owner: invites users, manages roles, sees the invoice) + End users (belong to one or more workspaces and switch between them). |
| **Success criteria** | (1) Three blocked deals ($400k ARR) close within one quarter of GA. (2) Zero cross-tenant data leaks in security review + external pentest. (3) SSO-enabled workspace can be provisioned in <1 business day. (4) ≥90% of existing single-user accounts migrate to a workspace without support intervention. |
| **Appetite** | **One quarter (12 weeks)** to enterprise-ready GA. Beta with the three blocked deals by week 8. Hard stop — this is displacing the next quarter's roadmap, not adding to it. |
| **Constraints** | Deals expected to close within the quarter (revenue pressure). Existing customers must be migrated with zero downtime and no data loss. Security posture cannot regress (SOC 2 in progress). Pricing change needs finance + legal sign-off. Depends on no other in-flight initiatives. |

**Stated assumptions** (proceeding without clarification, per instruction):
- Existing product is a B2B SaaS with per-user accounts and a shared Postgres. No prior tenant abstraction.
- Chosen isolation model: **shared schema, tenant-scoped rows with a `workspace_id` on every business table + row-level enforcement at the ORM/repository layer.** (Cheaper than schema-per-tenant, adequate for the three deals; documented as ADR with the tradeoff noted for future re-evaluation if a regulated customer requires physical isolation.)
- Enterprise tier will bundle multi-tenancy + SSO (SAML/OIDC) + SCIM provisioning + audit log. Pricing shifts from per-seat to per-seat with an enterprise floor.
- Existing users become the sole member of a new personal workspace at migration — no user-facing account change beyond a workspace switcher appearing in the header.

---

## Workstreams

### CPO team workstreams

| Workstream | Owner role | Key deliverables | Relevant? |
|---|---|---|---|
| Product | product-owner | PRD covering workspace lifecycle, roles (Owner/Admin/Member/Guest), invite/join flows, workspace switching, billing model change, migration UX for existing users; acceptance criteria per user story; success metrics | **Yes** — foundational |
| Design | ui-designer | Workspace switcher pattern, workspace settings IA, member management UI, role/permission surfaces, empty-state and first-run for new workspaces, migration prompt UX, accessibility pass | **Yes** — significant surface-area change |
| Content | user-docs-writer | Admin guide (create workspace, invite users, SSO setup, SCIM), end-user guide (switching workspaces, joining), migration FAQ, changelog entry, in-product tooltips/empty states | **Yes** — enterprise buyers evaluate docs during procurement |
| GTM | gtm | Enterprise tier positioning + pricing page changes, sales enablement (deck, security one-pager, competitive angle), launch comms to existing customers about the tier change, three named-account launch plan | **Yes** — pricing change + new tier |
| Support | support | Runbook for workspace/tenancy issues, migration escalation path, known-issues list, training session for CS/support on the new model | **Yes** — migration will drive tickets |
| Research | ux-researcher | Validate workspace switcher and admin flows with 3–5 enterprise design partners (the blocked deals are the sample); post-launch usability check | **Yes** — but scoped: fast validation with the three blocked deals, not net-new persona work |

### CTO team workstreams

| Workstream | Owner role | Key deliverables | Relevant? |
|---|---|---|---|
| Architecture | architect | ADR on isolation model (shared-schema + row scoping), tenant context propagation design (request → repo → query), auth/permission model (workspace-scoped RBAC), SSO/SCIM integration design, migration plan for existing data, billing/entitlement service contract | **Yes** — foundational |
| Development | backend + frontend developers | `workspace_id` schema migration + backfill, tenant-context middleware, repository-layer scoping, RBAC enforcement, invite/SSO/SCIM flows, workspace switcher + settings UI, billing integration changes, feature-flag rollout | **Yes** — the bulk of the work |
| QA Planning | qa-lead | Test strategy focused on **cross-tenant isolation** (the highest-risk failure mode), RBAC matrix tests, migration test plan, regression scope for every touched surface, exit criteria for GA | **Yes** — isolation testing is non-negotiable |
| QA Execution | qa-engineer | Automated isolation test suite (every endpoint × unauthorised tenant), RBAC matrix automation, migration dry-run on production-shaped data, exploratory testing for workspace switching edge cases | **Yes** |
| DevOps | devops | Zero-downtime migration runbook, per-tenant metrics/logging (tenant tag on every log line), tenant-aware rate limits, backup/restore per tenant, staging environment representative of multi-tenant load | **Yes** — migration is the risky step |
| Security | security-engineer | Threat model (STRIDE with focus on tenant-boundary threats), authorisation review, SSO/SAML implementation review, external pentest scoped to isolation, audit log requirements, SOC 2 evidence updates | **Yes** — enterprise buyers will ask for the pentest report |
| Data | data-engineer | Tenant dimension on all analytics events, per-tenant usage dashboards (needed for billing + CS), backfill of tenant on historical events where possible, deprecation of user-scoped dashboards that no longer make sense | **Yes** — billing depends on usage data being tenant-scoped |

**Not included** and why: nothing excluded — the initiative genuinely touches all workstreams. Research is scoped tightly (design partners only, not fresh persona work) to fit the appetite.

---

## Dependencies

### Dependency map

| Workstream | Depends on | What it needs before starting | Blocks |
|---|---|---|---|
| Product | — | Initiative brief + design-partner access | Everything |
| Architecture | Product | Workspace/role/billing requirements + NFRs (isolation guarantee, migration must be zero-downtime) | Development, DevOps, Security, Data |
| Design | Product | PRD with workspace lifecycle, role definitions, and acceptance criteria | Development (frontend), Content |
| Security (threat model) | Architecture | Isolation model + auth/permission design | Development (gates code changes), Pentest scoping |
| Data | Architecture | Schema decision (where `workspace_id` lives) | Billing integration, GTM (usage-based pricing inputs) |
| Development (backend) | Architecture, Security threat model | System design, API contracts, RBAC model, threat-model mitigations agreed | QA execution, DevOps deployment, Frontend (for API contract) |
| Development (frontend) | Design, Backend API contract | Component specs, workspace switcher pattern, API endpoints stable | QA execution, Content (screenshots) |
| QA planning | Product, Architecture | Acceptance criteria + isolation model (drives the isolation test matrix) | QA execution |
| QA execution | Development, QA plan | Working implementation in staging | Pentest, Launch |
| Pentest (external) | Development complete, QA passing | Feature-complete staging environment | GA gate |
| DevOps | Architecture | Migration plan, tenancy model | Beta rollout, GA |
| Content | Development (feature stable enough for screenshots), Design | Working UI, final IA | Launch, Support training |
| Support | Content, QA (known-issues list) | Docs + list of gotchas from QA | Launch |
| GTM | Product (pricing decision), Design (final UX for demos), Legal sign-off on pricing | Enterprise tier definition + pricing model | Launch |
| Research (design-partner validation) | Design (clickable prototype) | Prototype or early build | Product refinement before code-freeze |

**Critical-path dependency to flag:** **Legal + finance sign-off on the pricing model** must happen in parallel with Phase 1. If it slips, GTM cannot launch even if the product is ready. Coordinator to own the escalation.

---

## Execution Sequence

### Phased plan

| Phase | Workstreams (parallel) | Duration | Gate to next phase |
|---|---|---|---|
| **1 — Define** (weeks 1–2) | Product (PRD) ∥ Architecture (isolation ADR + auth model) ∥ Security (initial threat model draft) ∥ Legal/Finance (pricing sign-off — coordinator-led) | 2 weeks | PRD signed off by design partners; ADR on isolation model accepted; threat model draft reviewed; pricing model approved by finance + legal |
| **2 — Design & Contract** (weeks 3–4) | Design (UX flows + component specs) ∥ Architecture (API contracts, migration plan) ∥ Data (event schema) ∥ QA planning (isolation test strategy) ∥ Research (design-partner review of prototype) | 2 weeks | Frontend specs complete; API contracts frozen; migration plan reviewed by DevOps; isolation test matrix drafted |
| **3 — Build** (weeks 5–8) | Backend dev (schema, tenant context, RBAC, SSO/SCIM, billing) ∥ Frontend dev (switcher, settings, invites) ∥ DevOps (staging env, migration tooling) ∥ QA (writing automated isolation + RBAC tests against merged code) ∥ Content (drafting docs against staging build from week 7) | 4 weeks | Feature complete in staging; all isolation tests green; migration dry-run succeeds on prod-shaped data; docs first draft ready |
| **4 — Validate** (weeks 9–10) | QA execution (regression + exploratory) ∥ External pentest ∥ DevOps (production migration rehearsal) ∥ Design-partner beta with the three blocked deals ∥ Support training | 2 weeks | Pentest report clean (or all criticals/highs remediated); beta customers signed off; migration rehearsal successful; support runbook approved |
| **5 — Launch** (weeks 11–12) | GTM launch (pricing page, sales enablement live) ∥ Production migration (staged rollout behind flag) ∥ Content publish ∥ Support live coverage ∥ Data (usage dashboards live) | 2 weeks | GA announced; three named deals contracted; zero P0/P1 incidents in migration; success metrics dashboard live |

### Critical path

**Product → Architecture → Backend dev → QA/Pentest → Launch.** Minimum ~10 weeks if everything runs cleanly. The backend build (Phase 3) is the widest and most compressible-only-by-parallelising-devs point.

### Parallel opportunities

- Phase 1: Legal/finance pricing sign-off runs alongside PRD/ADR work — it has a long lead time and shouldn't serialise behind product.
- Phase 2: Design and Architecture proceed in parallel once the PRD lands; QA planning starts as soon as acceptance criteria and the isolation model are ready.
- Phase 3: Backend and frontend parallelise cleanly given a frozen API contract from Phase 2; QA writes tests against merged code, not at the end.
- Phase 4: External pentest runs concurrently with the design-partner beta — different signals, same feature-complete build.
- Content, GTM, and Support all prepare through Phases 3–4 so Phase 5 is coordination, not authoring.

---

## Summary

### Workstream summary

| Workstream | Owner | Depends on | Key deliverables | Phase | Estimated effort |
|---|---|---|---|---|---|
| Product | product-owner | — | PRD, roles, migration UX, success metrics | 1 | 1.5–2 weeks |
| Architecture | architect | Product | Isolation ADR, auth model, migration plan, API contracts | 1–2 | 2–3 weeks |
| Security (threat model + review) | security-engineer | Architecture | Threat model, auth review, pentest scoping/liaison | 1, 4 | 1.5–2 weeks + pentest window |
| Design | ui-designer | Product | Switcher, settings, invite/admin flows, accessibility | 2 | 2–3 weeks |
| Data | data-engineer | Architecture | Tenant dimension, usage dashboards, billing inputs | 2–5 | 1.5–2 weeks |
| QA planning | qa-lead | Product, Architecture | Isolation test strategy, RBAC matrix, exit criteria | 2 | 1 week |
| Backend development | backend developers | Architecture, Security | Schema + backfill, tenant context, RBAC, SSO/SCIM, billing integration | 3 | 4–5 weeks (2–3 devs) |
| Frontend development | frontend developers | Design, API contract | Switcher, workspace settings, member mgmt, migration prompt | 3 | 3–4 weeks (1–2 devs) |
| DevOps | devops | Architecture | Migration runbook, tenant-tagged obs, backup per tenant, staging | 3–4 | 2–3 weeks |
| QA execution | qa-engineer | Development | Isolation suite, RBAC automation, migration dry-run, exploratory | 3–4 | 3 weeks |
| External pentest | security-engineer (liaison) | Feature-complete build | Report + remediation | 4 | 2 weeks (external) + remediation buffer |
| Content | user-docs-writer | Development, Design | Admin/user guides, migration FAQ, in-product content | 3–5 | 2 weeks |
| Support | support | Content, QA | Runbook, escalation path, CS training | 4–5 | 1 week |
| Research (design-partner val.) | ux-researcher | Design | Prototype validation with 3 blocked deals + post-launch check | 2, 5 | 1 week (split) |
| GTM | gtm | Product (pricing), Design, Legal sign-off | Enterprise tier positioning, sales enablement, launch plan | 2–5 | 2–3 weeks |
| Legal + finance (pricing) | coordinator-led | Product | Pricing model sign-off | 1 | 1–2 weeks (elapsed, low effort) |

### Timeline estimate

- **Best case:** ~10 weeks — assumes design partners engage quickly, no isolation defects found in pentest, migration rehearsal clean first try.
- **Likely case:** **12 weeks** (matches the appetite) — 1 pentest remediation cycle, one migration dry-run needing a fix, minor scope adjustment after design-partner feedback.
- **Risk factors that could extend:**
  - **Isolation defect found late** — a cross-tenant leak surfaced in pentest is a hard block. Mitigation: isolation testing starts in Phase 3, not Phase 4; treat it as a first-class dev-time concern, not a QA gate.
  - **Pricing sign-off slippage** — legal/finance is external to the delivery team. Mitigation: start in week 1, escalate weekly.
  - **SSO/SCIM per-customer variance** — enterprise IdPs (Okta, Azure AD, Google) each have quirks. Mitigation: pick the top-2 based on the three blocked deals; defer the rest.
  - **Migration goes wrong on prod data shapes not seen in staging.** Mitigation: two rehearsals against a prod snapshot before the real cutover.
  - **Scope creep from GTM** ("we need a self-serve enterprise flow too"). Mitigation: enterprise-tier onboarding is sales-assisted at GA; self-serve is a follow-up.

---

## Follow-ups

- [ ] Define OKRs for this initiative — use `/coordinator:define-okrs` (frame around the three metrics: deals closed, isolation-defect count, migration completion rate).
- [ ] Write the PRD (product-owner) — use `/coordinator:write-spec` once Phase 1 is under way.
- [ ] Kick off legal/finance pricing sign-off in **week 1** — this is the highest-risk parallel dependency.
- [ ] Confirm the isolation-model ADR direction (shared schema + row scoping) with the architect before Phase 1 locks it in — flagged here as an assumption, needs a real decision.
- [ ] Identify the 2 SSO providers to support at GA based on the three named enterprise deals' actual IdPs.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.5/17.0 (97%) |
| Evaluated | 2026-07-24 |
| Target model | claude-opus-4-7 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 108707 ms |
| Target cost | $0.4978 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Coordinator decomposes into workstreams that map to specific agents (architect for data isolation, CPO for pricing, developer for implementation, etc.) | PASS | Explicit role mapping throughout: product-owner, architect, security-engineer, ui-designer, data-engineer, qa-lead, backend developers, frontend developers, devops, user-docs-writer, gtm, ux-researcher. |
| c2 | Dependencies between workstreams are identified and sequenced (e.g., data isolation design before implementation, pricing before billing) | PASS | Dedicated 'Dependency map' table with 'Depends on' and 'Blocks' columns for every workstream. e.g. 'Development (backend) \| Architecture, Security threat model \| ... \| QA execution, DevOps deployment'. |
| c3 | Both CPO and CTO workstreams are present — this is not purely technical (pricing, documentation, UX are product concerns) | PASS | Output explicitly labels 'CPO team workstreams' (Product, Design, Content, GTM, Support, Research) and 'CTO team workstreams' (Architecture, Development, QA, DevOps, Security, Data). |
| c4 | The decomposition includes effort estimates or sizing signals for each workstream | PASS | Summary table 'Estimated effort' column has ranges for every row, e.g. 'Backend development: 4–5 weeks (2–3 devs)', 'Architecture: 2–3 weeks', 'Support: 1 week'. |
| c5 | A critical path is identified — which workstreams block everything else | PASS | 'Critical path: Product → Architecture → Backend dev → QA/Pentest → Launch. Minimum ~10 weeks if everything runs cleanly. The backend build (Phase 3) is the widest … point.' |
| c6 | Revenue context ($400k ARR) is used to inform priority and timeline, not just mentioned | PARTIAL | Appetite set at '12 weeks' driven by the three deals; 'Beta with the three blocked deals by week 8'; SSO provider selection scoped to 'the three blocked deals' actual IdPs'; risk mitigation explicitly tied to keeping the deal timeline. |
| c7 | Security implications of multi-tenancy are called out as a specific workstream or constraint | PASS | Dedicated Security workstream: 'Threat model (STRIDE with focus on tenant-boundary threats), authorisation review, SSO/SAML implementation review, external pentest scoped to isolation, audit log requirements, SOC 2 evidence updates'. |
| c8 | The output is a dispatch plan, not implementation — the coordinator doesn't write code or specs | PASS | No code, schema DDL, or spec prose anywhere. Every section names a role, a deliverable, and a phase/dependency — it delegates implementation to named agents. |
| c9 | Output's workstreams cover at minimum: data isolation (architect / data engineer), auth and permissions (architect / security), billing changes (CPO + finance), UI workspace switching (UX + UI designer + developer), documentation (technical writer), pricing model (CPO + GTM) | PASS | All six areas present: isolation ADR (architect), RBAC/auth (architect + security-engineer), billing integration (backend dev + GTM/legal), switcher UI (ui-designer + frontend), docs (user-docs-writer), pricing (gtm + coordinator-led legal/finance). |
| c10 | Output's dependency map shows that data isolation design must complete before implementation, that pricing decisions must inform billing implementation, and that auth/permissions design feeds the UI workspace switching | PASS | Dependency map: 'Development (backend) depends on Architecture, Security threat model'; 'GTM depends on Product (pricing decision)'; 'Frontend depends on Backend API contract' (which encodes RBAC/auth model). |
| c11 | Output identifies the critical path — likely data isolation design → auth/permissions design → implementation → migration of existing customers — and names what blocks what | PASS | 'Critical path: Product → Architecture → Backend dev → QA/Pentest → Launch.' Dependency map also shows Architecture blocks Development, Security threat model gates Development, DevOps migration gates Launch. |
| c12 | Output uses the $400k ARR context to inform priority — connecting the dollar value to a target delivery date or quarter, not just citing the figure once | PASS | Success criteria: 'Three blocked deals ($400k ARR) close within one quarter of GA'; appetite: 'Hard stop — displacing next quarter's roadmap'; beta with three deals at week 8; scope creep risk mitigated by deal-focus. |
| c13 | Output flags multi-tenancy security as a distinct workstream — covering tenant isolation, blast-radius if one tenant is compromised, and customer-level encryption keys / data sovereignty options | PARTIAL | Tenant isolation and STRIDE threat model are explicit; blast-radius is implied by 'tenant-boundary threats' but not named. Customer-level encryption keys and data sovereignty are entirely absent. |
| c14 | Output includes effort estimates per workstream as ranges (e.g. 'data isolation design: 2-3 weeks', 'billing changes: 4-6 weeks') — not single-point estimates that imply false precision | PASS | Summary table uses ranges throughout: '2–3 weeks', '4–5 weeks (2–3 devs)', '1.5–2 weeks + pentest window', '3–4 weeks (1–2 devs)' — no single-point estimates. |
| c15 | Output is a dispatch plan — names the agent or role per workstream, the deliverable per workstream, and the entry/exit criteria — does NOT contain code, schema definitions, or implementation specs | PASS | Each workstream row has Owner role, Key deliverables, and Depends-on (entry) / Blocks (exit). Phase table has explicit 'Gate to next phase'. No code or schema anywhere. |
| c16 | Output covers BOTH CPO (pricing model, packaging tiers, GTM messaging, customer comms for existing customers) AND CTO (data, auth, infra) workstreams — multi-tenancy is not purely technical | PASS | GTM covers 'Enterprise tier positioning + pricing page changes, sales enablement, launch comms to existing customers about the tier change'. CTO side covers Architecture, Development, Security, Data, DevOps, QA. |
| c17 | Output addresses migration of existing single-tenant customers as a workstream — they need to be moved into the new model without disruption, and this typically blocks final cutover | PASS | DevOps deliverables include 'Zero-downtime migration runbook'; Phase 4 has 'production migration rehearsal'; success criteria: '≥90% of existing single-user accounts migrate without support intervention'; Phase 5 gate: 'zero P0/P1 incidents in migration'. |
| c18 | Output identifies parallel opportunities — e.g. UX research on workspace switching can run while data isolation is being designed, technical-writer documentation drafting can run alongside implementation | PARTIAL | Dedicated 'Parallel opportunities' section lists: Design + Architecture in parallel in Phase 2; 'Content [drafting docs against staging build from week 7]' alongside Phase 3 development; pentest concurrent with beta in Phase 4. |

### Notes

An exceptionally comprehensive decomposition that satisfies nearly all criteria at a high level of specificity — structured tables, explicit dependency maps, phased gates, and per-workstream effort ranges all present. The only meaningful gap is c13: while tenant isolation and STRIDE threat modelling are explicit, blast-radius and data-sovereignty/encryption-key concerns (critical for enterprise procurement) are absent from the security workstream.
