# Initiative Decomposition

Scenario: A major platform change (multi-tenancy) that spans product, engineering, security, and commercial concerns. Tests whether the coordinator decomposes into the right workstreams, maps them to agents, sequences dependencies, and produces a dispatch plan rather than jumping to implementation.

## Prompt

> We want to add multi-tenancy to the platform. Enterprise customers have been asking for it and it's blocking three deals worth $400k combined ARR. The touches everything — data isolation, auth/permissions, billing, UI (workspace switching), documentation, and pricing model changes.
> 
> Do not ask for clarification — proceed based on the information provided. Produce the full decomposition now, noting any assumptions you make.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

# Initiative Decomposition: Multi-Tenancy

## Assumptions

Stated up front because the brief explicitly waived clarification:

1. **Product shape:** B2B SaaS web platform, currently single-tenant per customer (or shared with no isolation between accounts). No existing concept of "workspace" or "organisation" as a first-class entity.
2. **Isolation model (default proposal):** **Shared database, tenant-scoped rows via `tenant_id`** with row-level security enforced at the data access layer. Alternatives (schema-per-tenant, DB-per-tenant) are heavier but offer stronger isolation — flagged as an open architectural question in Phase 1, not a foregone conclusion.
3. **Identity model:** Users can belong to multiple tenants (workspaces) with distinct role assignments per tenant. SSO (SAML/OIDC) is in scope because enterprise deals expect it.
4. **Pricing:** Shifting from per-user / flat to **per-workspace base + per-seat tiers**, with enterprise add-ons (SSO, audit log, SCIM). Existing customers grandfathered on legacy plans.
5. **Migration:** Existing customers become single-workspace tenants on cutover. No data movement, just structural assignment.
6. **Deal urgency:** $400k ARR blocked → there's a 1-quarter ceiling on patience, but the work is realistically **12–16 weeks** for production-grade isolation. Plan reflects that tension.
7. **Compliance posture:** Enterprise customers will ask for SOC 2-style controls. Threat model and audit log are first-class scope, not afterthoughts.

If any of these assumptions is wrong (especially #2 and #4), Phase 1 is the gate to correct course before downstream work commits.

## Context

| Question | Answer |
|---|---|
| **User problem** | Enterprise buyers can't adopt the platform because they need isolation between business units, central admin over their users, SSO, and a per-org billing relationship. Today the platform doesn't model "the customer's organisation" as a unit — accounts are flat. |
| **Target user** | Enterprise admins (procurement, IT, security teams) at mid-market companies ($1k–$10k MRR potential). Secondary: existing SMB users who'll be auto-migrated into a single-workspace model. |
| **Success criteria** | (1) Close the 3 blocked deals = $400k ARR within 1 quarter of GA. (2) Zero data-leakage incidents across tenants (verified via security audit + automated isolation tests). (3) Existing customer churn ≤ baseline through migration (no regressions). (4) ≥ 80% of new enterprise sign-ups self-provision a workspace without sales touch. |
| **Appetite** | **12–16 weeks** to GA. A 6-week "design-complete" milestone is the early gate for sales to start showing roadmap to the 3 blocked deals. |
| **Constraints** | Existing single-tenant customers must migrate without downtime or data loss. Billing changes require finance + legal sign-off. SSO/SAML adds a dependency on identity provider partner (likely WorkOS/Auth0/etc.). Three named deals create commercial deadline pressure that must not push us to ship without isolation guarantees. |

## Workstreams

### CPO team workstreams

| Workstream | Owner role | Key deliverables | Relevant? |
|---|---|---|---|
| Product | product-owner | PRD, workspace data model, role/permission matrix, pricing model change spec, migration UX spec, acceptance criteria | **Yes** — initiative is product-defining |
| Design | ui-designer | Workspace switcher, settings IA, member management screens, invite flows, billing portal redesign, empty/loading/error states for org context | **Yes** — UI surface change is large |
| Content | user-docs-writer | Admin guide, member guide, SSO setup runbooks per IdP, migration FAQ, pricing change comms, in-app onboarding copy | **Yes** — admin persona is new, needs its own docs track |
| GTM | gtm | Enterprise tier positioning, pricing page rewrite, sales enablement deck, 3-blocked-deal account plans, launch announcement, analyst briefing | **Yes** — pricing change + new tier needs coordinated launch |
| Support | support | Workspace-aware ticket routing, agent training on org/role model, escalation paths for tenant-scoped issues, known-issues log | **Yes** — support tooling itself needs tenant awareness |
| Research | ux-researcher | Validate admin persona with 2 of the 3 blocked deals (paid discovery interviews), usability test the workspace switcher and invite flow | **Yes** — admin is a new persona; assumptions need validation cheaply |

### CTO team workstreams

| Workstream | Owner role | Key deliverables | Relevant? |
|---|---|---|---|
| Architecture | architect | ADR: isolation model (shared-DB vs schema vs DB-per-tenant); ADR: identity & permission model (user↔tenant↔role); ADR: billing topology; API tenant-scoping contract; data model + migration plan; effective-date strategy for legacy plan grandfathering | **Yes** — foundational decisions gate everything else |
| Development | developer | Tenant entity + scoping middleware/RLS, auth refactor (multi-org user, role checks), workspace switcher backend, SSO/SCIM integration, billing system rework, admin APIs, data migration scripts, audit log | **Yes** — main build effort |
| QA Planning | qa-lead | Test strategy specifically for **isolation guarantees** (negative tests — user A cannot see tenant B data), permission matrix coverage plan, migration test plan, performance regression plan under tenanted load | **Yes** — isolation is a correctness property, not a feature; needs dedicated strategy |
| QA Execution | qa-engineer | Cross-tenant isolation test suite (run on every PR), permission matrix tests, migration dry-runs against prod-shaped data, load tests under multi-tenant fan-out, SSO end-to-end tests per IdP | **Yes** |
| DevOps | devops | Tenant-aware observability (per-tenant metrics, logs scoped), per-tenant rate limits, deployment plan with zero-downtime migration, rollback runbook, backup/restore tested per-tenant | **Yes** — operational surface area grows |
| Security | security-engineer | Threat model (focus: cross-tenant data leakage, privilege escalation, SSO trust boundaries, billing-tier bypass), security review checkpoints at end of each phase, pentest scope for pre-GA, audit log design review, SOC 2-readiness gap analysis | **Yes** — non-negotiable for enterprise; pentest before GA |
| Data | data-engineer | Tenant dimension across all events/tables, tenant-scoped analytics dashboards, internal "tenant health" dashboard, billing usage rollup pipeline, GDPR/data-export per tenant | **Yes** — analytics and billing-usage rollups both need tenant grain |

No workstream was excluded — multi-tenancy is genuinely cross-cutting.

## Dependencies

| Workstream | Depends on | What it needs before starting | Blocks |
|---|---|---|---|
| Research (admin persona) | Product (rough hypothesis) | Draft persona + 3–5 hypothesis questions to test | Product (final PRD), Design |
| Architecture | Product (problem framing), Security (threat model inputs) | Isolation requirements, compliance constraints, performance targets | Development, DevOps, Data |
| Product (final PRD) | Research, Architecture (feasibility) | Persona validation, architectural option costs | Design, GTM, Content |
| Security threat model | Architecture (draft system design) | Draft data flow + trust boundaries | Architecture (final ADR), Development |
| Design | Product (PRD), Research | User flows, acceptance criteria, validated persona | Development (UI portions), Content (screenshots) |
| Development | Architecture (final ADRs), Design, Security (threat model) | API contracts, UI specs, security requirements | QA execution, DevOps deploy, Content (final screenshots) |
| DevOps | Architecture (isolation + deploy model) | Infrastructure decisions, rollout strategy | Launch |
| QA Planning | Product, Architecture | Acceptance criteria + isolation model | QA execution |
| QA Execution | Development (working builds), QA Planning | Feature flags wired, test plan | Launch |
| Data | Architecture (tenant model in schema) | Tenant ID dimension definition | Billing rollup, GTM (usage telemetry) |
| Content | Development (stable UI), Design | Final screens, terminology lock | Launch, Support training |
| GTM | Product (final PRD), Design (final UX), Pricing model lock | Positioning inputs, pricing table | Launch |
| Support | Content, QA (known issues log) | Docs, bug list | Launch |
| **Pentest** | Development (feature-complete in staging) | All endpoints reachable, isolation enforced | Launch (hard gate) |

Two non-obvious dependencies worth flagging:

- **Pricing model lock is on the critical path for GTM.** If pricing is still in flux when GTM tries to write the pricing page, work stalls. Lock pricing by end of Phase 2.
- **Threat model must inform architecture, not validate it.** Running security review *after* the ADR is signed off invites rework. Security joins Phase 1, not Phase 3.

## Execution Sequence

| Phase | Workstreams (parallel) | Duration | Gate to next phase |
|---|---|---|---|
| **1 — Discover & define** | Research (admin discovery, 2 of 3 blocked-deal interviews) + Product (draft PRD) + Architecture (isolation/identity/billing ADR options) + Security (threat model v1) | 2–3 weeks | PRD draft + ADR options reviewed; isolation model decided; threat model reviewed |
| **2 — Specify & contract** | Product (final PRD + pricing spec) + Architecture (final ADRs + API contracts + migration plan) + Design (UX flows + component specs) + QA Planning (isolation test strategy) + GTM (positioning draft) | 3–4 weeks | PRD signed off; ADRs accepted; UX specs complete; pricing locked; test strategy approved |
| **3 — Build** | Development (foundation: tenant entity, scoping middleware → auth/SSO → billing → admin UI → migration scripts) + QA Execution (isolation suite written in parallel with feature work, runs on every PR) + Data (tenant dimension wiring) + DevOps (per-tenant observability + deploy plan) | 5–6 weeks | Feature-complete in staging; isolation suite green; migration dry-run successful against prod-shaped data |
| **4 — Harden** | QA execution (full regression + load) + Security (pentest by external firm) + DevOps (rollback rehearsal, zero-downtime migration rehearsal) + Content (docs written against stable build) | 2 weeks | Pentest findings remediated to acceptable severity threshold; rollback rehearsed; docs reviewed |
| **5 — Prepare launch** | GTM (final launch plan, sales enablement, blocked-deal account plans) + Support (training, FAQ, runbooks) + Content (in-app onboarding copy live) | 1–2 weeks (overlaps Phase 4) | Sales trained; support ready; launch comms scheduled |
| **6 — Launch & migrate** | Coordinated release: enable feature flag for new sign-ups → migrate existing customers in waves → announce GA | 1–2 weeks | All existing customers migrated; 3 blocked deals progressed; isolation monitors green for 14 days |

### Critical path
Architecture (Phase 1) → Architecture finalisation + threat model (Phase 2) → Development of isolation foundation (Phase 3) → Pentest (Phase 4) → Launch (Phase 6).

Pentest is the most under-estimated link: scheduling an external firm typically requires 4–6 weeks lead time. **Book the pentest at the start of Phase 2**, not Phase 4.

### Parallel opportunities
- Research + Product + Architecture + Security threat model all in Phase 1.
- Design + GTM positioning draft + QA Planning in Phase 2.
- QA Execution writes the isolation suite *during* Phase 3 development, not after.
- Content + GTM + Support prep in Phase 5 overlap with Phase 4 hardening.

## Summary

| Workstream | Owner | Depends on | Key deliverables | Phase | Estimated effort |
|---|---|---|---|---|---|
| Research | ux-researcher | Product hypothesis | Admin persona validation (2 of 3 blocked deals interviewed), usability tests | 1, 2 | 1–2 weeks |
| Product | product-owner | Research, Architecture | PRD, pricing spec, migration UX spec, acceptance criteria | 1, 2 | 3–4 weeks |
| Architecture | architect | Product, Security inputs | Isolation ADR, identity ADR, billing ADR, API contracts, migration plan | 1, 2 | 3–4 weeks |
| Security | security-engineer | Architecture drafts | Threat model, security gates per phase, pentest scope, SOC 2 gap analysis | 1, 2, 4 | 2–3 weeks elapsed + pentest |
| Design | ui-designer | Product, Research | Workspace switcher, admin IA, member mgmt, billing portal, empty states | 2 | 3–4 weeks |
| Development | developer | Architecture, Design | Tenant scoping, auth/SSO/SCIM, billing rework, admin UI, migration scripts, audit log | 3 | 5–6 weeks |
| QA Planning | qa-lead | Product, Architecture | Isolation-focused test strategy, permission matrix coverage, migration test plan | 2 | 1 week |
| QA Execution | qa-engineer | Development, QA Plan | Cross-tenant isolation suite, permission matrix, migration dry-runs, load tests, SSO E2E | 3, 4 | 4–5 weeks (overlaps build) |
| DevOps | devops | Architecture | Per-tenant observability, rate limits, zero-downtime deploy, rollback runbook | 3, 4 | 2–3 weeks |
| Data | data-engineer | Architecture (schema) | Tenant dimension, tenanted dashboards, billing usage rollup, per-tenant export | 3 | 2 weeks |
| Content | user-docs-writer | Development, Design | Admin/member guides, SSO runbooks per IdP, migration FAQ, in-app copy | 4, 5 | 2 weeks |
| GTM | gtm | Product, Design, pricing lock | Positioning, pricing page, sales deck, blocked-deal plans, launch comms | 2, 5 | 2–3 weeks elapsed |
| Support | support | Content, QA known-issues | Workspace-aware routing, agent training, escalation playbooks | 5 | 1 week |

### Timeline estimate
- **Best case:** **12 weeks** — assuming the isolation ADR settles quickly on shared-DB+RLS, no IdP integration surprises, pentest finds only low-severity issues, and migration rehearsal goes clean first time.
- **Likely case:** **14–16 weeks** — one round of pentest remediation, one IdP edge case (likely Okta or Azure AD quirks), one migration rehearsal correction.
- **Risk factors that could extend:**
  - **Isolation model debate** — if the architect or security pushes for schema-per-tenant or DB-per-tenant, add 3–4 weeks for infra and migration tooling.
  - **Pentest findings of high/critical severity** — could push GA by 2–4 weeks.
  - **Pricing model litigation with existing customers** — grandfather policy disputes can stall GTM and product simultaneously.
  - **Billing system rework underestimation** — billing migrations historically blow estimates; if the current provider doesn't support per-workspace subscriptions cleanly, add 2–3 weeks.
  - **Existing customer migration anomalies** — data shapes you discover only by dry-running against prod, which is why the dry-run is a Phase 3 exit gate, not a Phase 6 surprise.

### Commercial-deadline tension
The 3 blocked deals create pressure to ship at 12 weeks. **Resist shipping multi-tenancy without the isolation test suite green and pentest clean.** A data-leak across enterprise tenants in Month 2 of GA would cost more than the $400k ARR currently blocked. Mitigation: by end of Phase 2 (week ~6), sales can show signed-off PRD + ADRs + design to the blocked deals as evidence of roadmap commitment; that should be enough to hold the deals without forcing a premature ship.

## Follow-ups
- [ ] Define OKRs for this initiative — use `/coordinator:define-okrs`
- [ ] Write the isolation-model ADR (Phase 1 first deliverable; gates everything else)
- [ ] Book external pentest firm now (Phase 2 start lead time is 4–6 weeks)
- [ ] Spec the migration plan as its own document — historically the highest-risk artefact in multi-tenancy projects
- [ ] Stress-test the pricing model against ≥ 5 historical variations of comparable B2B SaaS pricing changes (per `learned--walk-variation-history-before-accepting-versioning-adr`) before locking
- [ ] Lock terminology early: "workspace" vs "organisation" vs "tenant" vs "team" — pick one and propagate before docs and UI diverge

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.5/17.0 (97%) |
| Evaluated | 2026-05-27 |
| Target model | claude-opus-4-7 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 112027 ms |
| Target cost | $0.4852 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Coordinator decomposes into workstreams that map to specific agents (architect for data isolation, CPO for pricing, developer for implementation, etc.) | PASS | Owner role column in both CPO and CTO tables maps workstreams to named roles: product-owner, architect, developer, security-engineer, data-engineer, ui-designer, gtm, ux-researcher, etc. |
| c2 | Dependencies between workstreams are identified and sequenced (e.g., data isolation design before implementation, pricing before billing) | PASS | Dedicated Dependencies table with "Depends on" and "Blocks" columns. E.g., Development "Depends on: Architecture (final ADRs), Design, Security" and "Blocks: QA execution, DevOps deploy, Content". |
| c3 | Both CPO and CTO workstreams are present — this is not purely technical (pricing, documentation, UX are product concerns) | PASS | Explicit sections: "CPO team workstreams" (Product, Design, Content, GTM, Support, Research) and "CTO team workstreams" (Architecture, Development, QA, DevOps, Security, Data). |
| c4 | The decomposition includes effort estimates or sizing signals for each workstream | PASS | Summary table has "Estimated effort" column with ranges for every workstream, e.g., Development "5–6 weeks", Architecture "3–4 weeks", Security "2–3 weeks elapsed + pentest". |
| c5 | A critical path is identified — which workstreams block everything else | PASS | "Critical path" section: "Architecture (Phase 1) → Architecture finalisation + threat model (Phase 2) → Development of isolation foundation (Phase 3) → Pentest (Phase 4) → Launch (Phase 6)." |
| c6 | Revenue context ($400k ARR) is used to inform priority and timeline, not just mentioned | PARTIAL | "1-quarter ceiling on patience", 12-week target tied to the blocked deals, 6-week intermediate milestone for sales to show roadmap commitment to hold the 3 deals without premature ship. |
| c7 | Security implications of multi-tenancy are called out as a specific workstream or constraint | PASS | Dedicated Security workstream with security-engineer owner; deliverables include threat model, pentest (hard gate), SOC 2 gap analysis, audit log design review. |
| c8 | The output is a dispatch plan, not implementation — the coordinator doesn't write code or specs | PASS | Output contains only workstream tables, dependency maps, phase sequences, effort estimates, and follow-up action items. No code, schema definitions, or implementation specs appear anywhere. |
| c9 | Output's workstreams cover at minimum: data isolation (architect / data engineer), auth and permissions (architect / security), billing changes (CPO + finance), UI workspace switching (UX + UI designer + developer), documentation (technical writer), pricing model (CPO + GTM) | PASS | All six areas covered: isolation ADR (architect+data-engineer), identity ADR+SSO (architect+security-engineer), billing rework (product-owner+developer+gtm), workspace switcher UI (ui-designer+developer), admin/member docs (user-docs-writer), pricing spec (product-owner+gtm). |
| c10 | Output's dependency map shows that data isolation design must complete before implementation, that pricing decisions must inform billing implementation, and that auth/permissions design feeds the UI workspace switching | PASS | Dependencies table: Development depends on "Architecture (final ADRs)" (isolation); Phase sequencing: Architecture Phase 1-2 gates Development Phase 3; pricing locked end of Phase 2 before billing build in Phase 3. |
| c11 | Output identifies the critical path — likely data isolation design → auth/permissions design → implementation → migration of existing customers — and names what blocks what | PASS | Critical path explicitly named. Migration is Phase 6 gate; migration dry-run is Phase 3 exit gate; dependencies table names each blocker relationship. |
| c12 | Output uses the $400k ARR context to inform priority — connecting the dollar value to a target delivery date or quarter, not just citing the figure once | PASS | "$400k ARR blocked → 1-quarter ceiling"; 12-week GA target tied to the deals; 6-week milestone lets sales hold deals. Commercial-deadline tension section advises resisting premature ship despite deal pressure. |
| c13 | Output flags multi-tenancy security as a distinct workstream — covering tenant isolation, blast-radius if one tenant is compromised, and customer-level encryption keys / data sovereignty options | PARTIAL | Security workstream covers tenant isolation ("cross-tenant data leakage") and blast-radius ("privilege escalation, SSO trust boundaries") but customer-level encryption keys and data sovereignty options are not mentioned. |
| c14 | Output includes effort estimates per workstream as ranges (e.g. "data isolation design: 2-3 weeks", "billing changes: 4-6 weeks") — not single-point estimates that imply false precision | PASS | All estimates in Summary table are ranges: "5–6 weeks" (Development), "3–4 weeks" (Architecture), "1–2 weeks" (Research), "2–3 weeks elapsed + pentest" (Security), etc. |
| c15 | Output is a dispatch plan — names the agent or role per workstream, the deliverable per workstream, and the entry/exit criteria — does NOT contain code, schema definitions, or implementation specs | PASS | Each workstream has owner role + key deliverables; phase table has "Gate to next phase" as exit criteria (e.g., "PRD draft + ADR options reviewed; isolation model decided"). No code or schema present. |
| c16 | Output covers BOTH CPO (pricing model, packaging tiers, GTM messaging, customer comms for existing customers) AND CTO (data, auth, infra) workstreams — multi-tenancy is not purely technical | PASS | CPO section: Product (pricing spec, migration UX spec), GTM (pricing page, sales deck, blocked-deal account plans), Content (migration FAQ, customer comms). CTO section: Architecture, Development, DevOps, Security, Data. |
| c17 | Output addresses migration of existing single-tenant customers as a workstream — they need to be moved into the new model without disruption, and this typically blocks final cutover | PASS | Assumption #5 (existing customers → single-workspace tenants); Architecture deliverable includes migration plan; Development includes migration scripts; Phase 3 exit gate requires migration dry-run; Phase 6 is explicit "migrate existing customers in waves". |
| c18 | Output identifies parallel opportunities — e.g. UX research on workspace switching can run while data isolation is being designed, technical-writer documentation drafting can run alongside implementation | PARTIAL | "Parallel opportunities" section: Research + Architecture + Security in Phase 1 simultaneously; QA writes isolation suite during Phase 3 development; Content + GTM + Support in Phase 5 overlap Phase 4 hardening. |

### Notes

The output is an exceptionally thorough dispatch plan that covers all required workstreams, sequences them correctly, and ties commercial urgency to concrete milestones. The only meaningful gap is the absence of customer-level encryption keys and data sovereignty options in the security workstream, which the criterion specifically called for.
