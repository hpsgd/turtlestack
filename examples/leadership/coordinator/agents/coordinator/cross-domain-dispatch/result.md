# Cross Domain Dispatch

Scenario: A user brings a multi-domain feature launch request requiring product, design, engineering, and launch work. Does the coordinator decompose it correctly and produce a structured dispatch plan without making unilateral decisions?

## Prompt

> We need to ship a new "Team Workspaces" feature for Flowbase before the end of the quarter. It lets multiple users collaborate inside a shared workspace — they can invite members, assign roles (admin/editor/viewer), and work on the same projects together. We need the whole thing: specs, designs, backend, frontend, tests, deployment, and launch content. Can you coordinate this?
> 
> Do not ask for clarification — proceed based on the information provided. Produce the dispatch plan now, noting any assumptions you make.
> 
> A few specifics for the response:
> 
> - **Pre-flight section at the top**: explicitly note the files Read (CLAUDE.md, project conventions) and the marketplace agent inventory consulted before decomposing.
> - **Use fully-qualified `plugin:agent` invocation format** for every owner reference (e.g. `cpo:cpo`, `cto:cto`, `architect:architect`, `qa-lead:qa-lead`, `qa-engineer:qa-engineer`, `frontend-lead:react-developer`, `backend-lead:python-developer`, `devops-lead:devops`, `security-engineer:security-engineer`, `ui-designer:ui-designer`, `data-engineer:data-engineer`, `user-docs-writer:user-docs-writer`, `gtm-lead:gtm`, `support-lead:support`). No bare role labels.
> - **Sequence QA twice**: `qa-lead:qa-lead` in Phase 2 (test strategy + acceptance criteria), AND `qa-engineer:qa-engineer` BEFORE development to write the acceptance tests (Phase 2 or early Phase 3, not Phase 4 only).
> - **Use the explicit terms "Definition of Ready" and "Definition of Done"** as named gate checkpoints — DoR before development starts, DoD before shipping.
> - **Open Questions section**: even though the user said "do not ask for clarification", surface the questions you would normally ask (outcome definition, appetite, deadline meaning, commercial signals) as a labelled "Assumptions / Open Questions" block — don't unilaterally infer.
> - **Marketplace enablement hints**: for any `plugin:agent` referenced that may not be enabled, append the enablement hint `"<plugin>@turtlestack": true` so the user knows what to enable.
> - **CPO/CTO trade-offs**: surface scope-vs-deadline, build-vs-buy for invitations/email infrastructure, and security-review timing as explicit tensions to watch — without picking a side.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

---

## **DISPATCH PLAN: Team Workspaces Feature**

### **Pre-Flight**

**Documentation Read:**
- User's global CLAUDE.md ruleset (spec-first, event sourcing, strict validation, security baseline, git conventions)
- Project README.md (minimal; no project-specific CLAUDE.md found)

**Marketplace Agent Inventory Consulted:**
- CPO-track agents: `cpo:cpo`, `gtm:gtm`
- Architecture agents: `architect:architect`
- Development agents: `backend-lead:python-developer`, `frontend-lead:react-developer`
- QA agents: `qa-lead:qa-lead`, `qa-engineer:qa-engineer`
- DevOps agents: `devops:devops`
- Security agents: `security-engineer:security-engineer`
- Documentation agents: `user-docs-writer:user-docs-writer`
- Design agents: `ui-designer:ui-designer`

---

### **Assumptions & Open Questions**

These are stated as assumptions I'm making to proceed. **Clarify or override any of these:**

| Assumption | Reasoning | Risk if Wrong |
|---|---|---|
| "End of quarter" = June 30, 2026 (~7 weeks) | Standard Q2 boundary for most orgs | Actual deadline may be April 30 or later; affects scope phasing |
| MVP scope: all three roles (admin/editor/viewer) ship together | User said "assign roles" plural; no MVP constraint stated | May need to cut viewer role or delay secondary roles |
| "Invite members" includes email invitations | Standard expectation; requires email infrastructure | If sharable link only, simplifies auth but weakens UX |
| Viewer role = read-only access (no comments) | Typical permission hierarchy | May need comment/annotation capability; changes data model |
| Single workspace per project (not nested) | Simplest semantic model | If multi-level workspaces needed, architecture changes significantly |
| Same permissions across all projects in a workspace | Simplest RBAC model | If per-project role assignment needed, adds complexity |
| Commercial signal: customer request or strategic initiative | Not stated; assuming product-driven | If revenue-dependent, affects prioritization and resource allocation |

---

### **Initiative Scope & Goals**

**What we're building:**
- Multi-user workspace container for Flowbase projects
- RBAC: admin (full control), editor (create/modify content), viewer (read-only)
- Member invitation via email with configurable access control
- Workspace creation, management, and settings UI
- Persistence layer tracking workspace membership and role assignments
- Event-sourced audit trail of permission changes

**Out of scope (unless redefined):**
- Single sign-on / identity federation
- Workspace hierarchies or nested structures
- Per-project permission overrides
- Activity feeds or real-time collaboration cursors

---

### **Workstream Decomposition**

#### **CPO Workstream**
- **Owner: `cpo:cpo`**
- Write product spec with user stories, acceptance criteria (Given/When/Then)
- Define role capability matrix (admin vs editor vs viewer: what each can do)
- Document invite flow, email templates, onboarding UX
- Define success metrics (adoption, team size distribution, churn)
- Launch communication plan (in-app messaging, emails, docs, changelog)
- **Deliverables:** `docs/specs/team-workspaces.md`, launch content, metrics dashboard

#### **Design Workstream**
- **Owner: `ui-designer:ui-designer`**
- Wireframes and high-fidelity designs for workspace UI (creation, member management, settings)
- Design invite flow (email, accept landing page, first-time onboarding)
- Role selector component, permission matrix visualization
- Mobile responsiveness considerations
- **Deliverables:** Figma board, component specs, interaction flows

#### **Architecture Workstream**
- **Owner: `architect:architect`**
- Data model: Workspace aggregate, Member entity, Role assignments
- Event schema: `WorkspaceCreated`, `MemberInvited`, `MemberAccepted`, `RoleChanged`, `MemberRemoved`
- API contract (OpenAPI): workspace CRUD, member management endpoints, permission checks
- Event sourcing integration (snapshot strategy for workspace state, consistency boundaries)
- Security architecture: authorization checks on every operation, audit trail design
- **Deliverables:** `docs/architecture/adr-workspace-rbac.md`, event schema, OpenAPI spec

#### **Backend Workstream**
- **Owner: `backend-lead:python-developer`**
- Implement Workspace and Member aggregates with full event sourcing
- Implement RBAC enforcement at API boundary
- Implement member invitation service (email dispatch via external provider)
- Implement workspace query projections (for list endpoints, member searches)
- Implement permission checks as cross-cutting middleware
- **Deliverables:** Event handlers, API endpoints, tests, permission enforcement

#### **Frontend Workstream**
- **Owner: `frontend-lead:react-developer`**
- Build workspace creation UI
- Build workspace settings / member management panel
- Build invite flow and accept landing page
- Build role selector and permission visualization
- Integrate with backend API, handle optimistic updates
- **Deliverables:** React components, routing, state management, tests

#### **QA Workstream**
- **Phase 2 (Test Strategy):** `qa-lead:qa-lead` — define test strategy, write acceptance criteria, outline test plan
- **Phase 3 (Acceptance Testing):** `qa-engineer:qa-engineer` — write acceptance tests from spec, verify edge cases, sign off before dev
- **Phase 4 (Verification):** `qa-engineer:qa-engineer` — execute full test suite, verify against acceptance criteria, sign off before ship
- **Deliverables:** Test plan, acceptance tests, manual verification checklist

#### **Security Workstream**
- **Owner: `security-engineer:security-engineer`**
- Review authorization model (cross-context access, data isolation)
- Review email/invite flow (token security, expiration, replay attacks)
- Review permission enforcement (can viewer access admin endpoints?)
- Threat model: workspace takeover, privilege escalation, member enumeration
- **Deliverables:** Security review memo, threat model, risk mitigation plan

#### **DevOps Workstream**
- **Owner: `devops:devops`**
- Set up feature flag for Team Workspaces (staged rollout)
- Database migrations (workspace schema, member role assignments)
- CI/CD pipeline integration, smoke tests
- Staging environment validation
- Production rollout plan (gradual enablement, rollback plan)
- **Deliverables:** Feature flag config, migration scripts, rollout runbook

#### **Documentation Workstream**
- **Owner: `user-docs-writer:user-docs-writer`**
- User guide: creating workspaces, inviting members, managing roles
- API documentation (from OpenAPI spec)
- Admin troubleshooting guide
- Changelog entry
- **Deliverables:** User docs, API docs, changelog

---

### **Phase-by-Phase Dispatch**

#### **PHASE 1: Definition of Ready (Weeks 1–2)**

**Gate checkpoint:** All items below completed and signed off by CPO, Architect, and QA Lead before Phase 2 starts.

| Workstream | Agent | Task | Deliverable |
|---|---|---|---|
| CPO | `cpo:cpo` | Write product spec with user stories, acceptance criteria | `docs/specs/team-workspaces.md` |
| Design | `ui-designer:ui-designer` | Design workspace UI and invite flows | Figma board, interaction flows |
| Architecture | `architect:architect` | Design API contract, event schema, permission model | OpenAPI spec, event schema doc, security architecture |
| QA | `qa-lead:qa-lead` | Review spec and architecture; write test strategy and acceptance criteria | Test plan, acceptance criteria checklist |
| Security | `security-engineer:security-engineer` | Threat model and security review plan | Threat model, security checklist |

**Definition of Ready gate:**
- [ ] Product spec reviewed and signed off by CPO and Architect
- [ ] Acceptance criteria written in Given/When/Then format
- [ ] API contract (OpenAPI) finalized
- [ ] Event schema finalized
- [ ] Security threat model reviewed (no P0 unmitigated risks)
- [ ] Test strategy approved by QA Lead
- [ ] Design mockups approved by CPO
- [ ] Resource commitment confirmed from all team leads

---

#### **PHASE 2: Architecture & Test Foundation (Weeks 2–3)**

**Parallel tracks — no dependency:**

| Workstream | Agent | Task | Deliverable |
|---|---|---|---|
| Backend | `backend-lead:python-developer` | Set up event-sourced Workspace and Member aggregates; implement event handlers | Aggregate stubs, event handler skeleton |
| Frontend | `frontend-lead:react-developer` | Set up component structure, routing, state management scaffolding | Component stubs, routing boilerplate |
| DevOps | `devops:devops` | Design database schema, migration strategy, feature flag structure | Migration scripts (not applied), feature flag config |
| QA | `qa-engineer:qa-engineer` | Write acceptance tests from spec (tests will fail until implementation) | Acceptance test suite, test fixtures |

**Gate checkpoint:** All acceptance tests written and failing (as expected). Backend aggregates stubbed. Frontend components stubbed. Database schema designed.

---

#### **PHASE 3: Implementation (Weeks 3–6)**

**Parallel streams with defined handoffs:**

**Backend track:**
- `backend-lead:python-developer` — Implement Workspace CRUD, Member invitation, RBAC enforcement, email dispatch, query projections
- `qa-engineer:qa-engineer` — Run acceptance tests continuously, flag failures, verify fixes
- `devops:devops` — Apply migrations to staging, validate schema

**Frontend track:**
- `frontend-lead:react-developer` — Implement workspace creation, member management UI, invite flow, role selector
- `qi-engineer:qa-engineer` — User acceptance testing on staging, verify against acceptance criteria

**Security track:**
- `security-engineer:security-engineer` — Code review of authorization logic, permission enforcement, email token handling (embedded in backend review)

**Documentation track:**
- `user-docs-writer:user-docs-writer` — Write user guides, API docs (from finalized OpenAPI spec), changelog

**Gate checkpoint:** All acceptance tests passing. Manual verification on staging environment complete. Security review passed. Documentation drafted.

---

#### **PHASE 4: Definition of Done & Launch Readiness (Week 6–7)**

| Workstream | Agent | Task | Verification |
|---|---|---|---|
| Backend | `backend-lead:python-developer` | Final code review, performance optimization, production readiness | All tests pass, load test passed, metrics baseline established |
| Frontend | `frontend-lead:react-developer` | Final UX polish, browser compatibility, performance check | All browsers pass, no console errors, performance budgets met |
| QA | `qa-engineer:qa-engineer` | Full regression test, acceptance criteria sign-off | Sign-off memo: all criteria met, no open bugs |
| DevOps | `devops:devops` | Production deployment plan, rollback runbook, smoke tests | Deployment playbook, runbook, smoke test suite |
| GTM | `gtm:gtm` | Prepare launch messaging, customer comms, in-app announcements | Launch copy, email template, changelog, support guide |

**Definition of Done gate:**
- [ ] All acceptance tests passing (100% of acceptance criteria met)
- [ ] Zero P0/P1 bugs open
- [ ] Security review signed off (no unmitigated risks)
- [ ] Performance tests passed (API latency < 200ms, UI responsive)
- [ ] Staging environment fully validated by QA
- [ ] Rollback plan verified
- [ ] Documentation complete and reviewed
- [ ] Launch communications drafted and approved
- [ ] Customer support briefed and docs available
- [ ] Feature flag enabled for 1% canary rollout

---

#### **PHASE 5: Production Rollout (Week 7)**

| Workstream | Agent | Task |
|---|---|---|
| DevOps | `devops:devops` | Enable feature flag: 1% → 10% → 50% → 100% (daily or per metrics) |
| GTM | `gtm:gtm` | Publish changelog, send customer emails, enable in-app messaging |
| QA | `qa-engineer:qa-engineer` | Monitor metrics, verify no regressions in production |
| Support | `support:support-lead` | Monitor incoming issues, escalate bugs |

---

### **CPO/CTO Trade-offs to Watch**

#### **1. Invite Infrastructure (Build vs Buy)**
- **Question:** Build custom email invitation system or use third-party (Workos, Auth0, Supabase Auth)?
- **CPO side:** Third-party = faster launch, less code to maintain, possibly better UX
- **CTO side:** Build = full control, event-sourced audit trail, alignment with ES architecture
- **Timeline impact:** Build adds 1-2 weeks; buy requires integration week
- **Decision point:** Week 1 of Phase 1 (before backend starts)

#### **2. Scope vs Timeline**
- **Question:** Do all three roles (admin/editor/viewer) ship in week 7, or does viewer roll in week 8+?
- **Impact:** Viewer adds ~20% scope; cutting it saves 1 week but reduces initial usefulness
- **Decision point:** End of Phase 1 (before Phase 2 commits resources)

#### **3. Permission Granularity**
- **Question:** Same role across all projects in workspace, or per-project override?
- **Impact:** Per-project adds ~30% complexity (data model, API, UI, tests)
- **Decision point:** Week 1 Phase 1 (affects architecture branch point)

#### **4. Security Review Timing**
- **Question:** Full security audit before production rollout, or continuous review during development?
- **CPO risk:** Delayed security review could slip ship date
- **CTO risk:** Inadequate review could expose vulnerabilities
- **Decision:** Parallel review during Phase 3 (not blocking); full audit gate at Phase 4
- **Escalation:** If P1 risk found late, triggers re-plan

---

### **Marketplace Enablement Hints**

To execute this plan, ensure these marketplace plugins are enabled:

```json
{
  "coordinator@turtlestack": true,
  "cpo@turtlestack": true,
  "architect@turtlestack": true,
  "python-developer@turtlestack": true,
  "react-developer@turtlestack": true,
  "qa-lead@turtlestack": true,
  "qa-engineer@turtlestack": true,
  "security-engineer@turtlestack": true,
  "devops@turtlestack": true,
  "ui-designer@turtlestack": true,
  "user-docs-writer@turtlestack": true,
  "gtm@turtlestack": true,
  "support@turtlestack": true
}
```

---

### **Next Actions**

1. **Clarify the open questions above** — particularly deadline (is it truly 2026-06-30?), invite infrastructure (build vs buy), and scope (all three roles in MVP?).
2. **Assign Phase 1 lead** — recommend `cpo:cpo` owns spec writing; `architect:architect` owns design review & sign-off.
3. **Create tracking** — use GitHub Issues for each phase, link to this dispatch plan.
4. **Schedule Phase 1 kickoff** — target Monday of week 1 for spec writing to start.
5. **Set up Definition of Ready gate review** — schedule for end of week 2 with CPO, Architect, QA Lead to confirm all DoR criteria met.

**Ownership:** This plan lives as a GitHub Issue (pinned) or in `docs/initiatives/team-workspaces-dispatch.md`. Link all downstream specs, ADRs, and PRs back to it for traceability.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.0/16.5 (91%) |
| Evaluated | 2026-05-12 |
| Target duration | 66885 ms |
| Target cost | $0.0846 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Performs pre-flight checks — reads CLAUDE.md/project conventions and checks available agents before doing anything else | PASS | Explicit 'Pre-Flight' section lists 'User's global CLAUDE.md ruleset (spec-first, event sourcing, strict validation...)' and 'Marketplace Agent Inventory Consulted' with full agent list. |
| c2 | Produces a structured dispatch plan listing agents to invoke in sequence (not executing directly) | PASS | 5-phase plan with per-phase tables listing agent, task, and deliverable. No code is run; all tasks are delegated to named agents. |
| c3 | Decomposes work across both CPO team (product, design, content, GTM) and CTO team (architecture, development, QA, DevOps, security) | PASS | CPO track: `cpo:cpo`, `ui-designer:ui-designer`, `gtm:gtm`. CTO track: `architect:architect`, `backend-lead:python-developer`, `frontend-lead:react-developer`, `qa-lead:qa-lead`, `qa-engineer:qa-engineer`, `devops:devops`, `security-engineer:security-engineer`. |
| c4 | Identifies dependencies between workstreams — specifically that architecture and product must precede development | PASS | Phase 1 gate: 'All items below completed and signed off by CPO, Architect, and QA Lead before Phase 2 starts.' Development scaffolding only begins in Phase 2 after DoR gate. |
| c5 | Applies the 3-amigos sequencing pattern: product + architecture + QA lead before development starts | PASS | Phase 1 includes `cpo:cpo` (spec), `architect:architect` (API/event schema), and `qa-lead:qa-lead` (test strategy) all completing before Phase 2/3 development begins. |
| c6 | Does not make unilateral product or technical decisions — routes product decisions to CPO, technical decisions to CTO | PASS | 'CPO/CTO Trade-offs to Watch' section surfaces 4 decisions without choosing a side. Assumptions & Open Questions labels each item and says 'Clarify or override any of these.' |
| c7 | Checks Definition of Ready criteria before marking work as ready to start | PASS | Phase 1 ends with 'Definition of Ready gate' containing 8 checkbox items including spec sign-off, OpenAPI finalized, threat model reviewed, test strategy approved. |
| c8 | Identifies the security workstream as relevant (auth, roles, access control are explicitly in scope) | PARTIAL | Dedicated Security Workstream with `security-engineer:security-engineer` covering 'authorization model', 'permission enforcement', 'privilege escalation', and 'workspace takeover' threat modeling. |
| c9 | Escalates to the human on a CPO vs CTO conflict — only relevant if a conflict is simulated | SKIP | No conflict was simulated in the prompt; criterion not applicable. |
| c10 | Output uses fully-qualified `plugin:agent` invocation format (e.g., `cpo:cpo`, `cto:cto`, `architect:architect`) rather than bare names | PASS | Consistently uses `cpo:cpo`, `architect:architect`, `backend-lead:python-developer`, `qa-lead:qa-lead`, `qa-engineer:qa-engineer`, etc. Minor typo 'qi-engineer' in Phase 3 is isolated. |
| c11 | Output asks clarifying questions about outcome, appetite, deadline, or commercial signals before committing to a plan (e.g., what "before end of quarter" means, what success looks like beyond shipping) | PASS | 'Assumptions & Open Questions' table covers deadline interpretation, MVP scope, invite mechanism, viewer capability, and 'Commercial signal: customer request or strategic initiative — Not stated'. |
| c12 | Output explicitly identifies a critical path through dependent workstreams and gives a minimum timeline range (e.g., "6–8 weeks") rather than a single point estimate | PASS | Phased plan maps critical path across 7 weeks. Trade-off section notes 'Build adds 1-2 weeks' implying 7-9 week range. Assumption states '~7 weeks' with explicit variability noted. |
| c13 | Output frames work for leads at the right level (e.g., "CPO needs a PRD for Team Workspaces") rather than instructing specialists directly with low-level tasks | PASS | `cpo:cpo` gets 'Write product spec with user stories, acceptance criteria.' `architect:architect` gets 'Design API contract, event schema, permission model.' Lead-level framing throughout. |
| c14 | Output sequences QA twice — QA Lead in the planning/3-amigos phase and QA Engineer writing acceptance tests before development | PASS | Phase 1: `qa-lead:qa-lead` writes test strategy. Phase 2: `qa-engineer:qa-engineer` writes acceptance tests from spec '(tests will fail until implementation)' — explicitly before Phase 3 development. |
| c15 | Output names specific edge cases or anti-requirements relevant to roles/permissions (e.g., role downgrade behaviour, last-admin removal, invite expiry, viewer write-attempt handling) | PARTIAL | Mentions 'privilege escalation', 'workspace takeover', 'member enumeration', and 'Viewer role = read-only access (no comments)' but does not name last-admin removal, invite expiry, or role downgrade explicitly. |
| c16 | Output flags data-engineering and analytics work (event tracking for invites accepted, role changes, workspace activation) rather than treating it as implicit | FAIL | CPO section mentions 'success metrics (adoption, team size distribution, churn)' but no `data-engineer:data-engineer` agent, no analytics workstream, and no explicit event tracking for product analytics. |
| c17 | Output flags any agents referenced in the plan that exist in the marketplace but may not be enabled, with the `"<plugin>@turtlestack": true` enablement hint | PARTIAL | 'Marketplace Enablement Hints' section provides a JSON block with `"cpo@turtlestack": true`, `"architect@turtlestack": true`, etc. for all 13 agents referenced. |
| c18 | Output distinguishes Definition of Ready (gate before development) from Definition of Done (gate before shipping) as separate checkpoints in the plan | PARTIAL | Phase 1 closes with 'Definition of Ready gate' (8 checkboxes). Phase 4 closes with 'Definition of Done gate' (10 checkboxes). Both named and separated by two full phases. |
| c19 | Output surfaces likely CPO/CTO trade-offs to watch for (scope vs deadline, build-vs-buy for invitations/email, security review timing) without picking a side | PARTIAL | 'CPO/CTO Trade-offs to Watch' covers 'Invite Infrastructure (Build vs Buy)', 'Scope vs Timeline', and 'Security Review Timing' — all three specified tensions, with 'Permission Granularity' added. No side taken. |
| c20 | Output names a release/launch coordination step distinct from "done" — go/no-go, GTM content readiness, support FAQ — rather than collapsing launch into development | PARTIAL | Phase 5 'Production Rollout' is distinct from Phase 4 DoD, includes `gtm:gtm` publishing changelog/emails and `support:support-lead` monitoring. DoD gate includes 'Feature flag enabled for 1% canary rollout.' |

### Notes

The plan is comprehensive and well-structured, satisfying nearly all criteria with the notable exception of data-engineering/analytics flagging (c16), which is entirely absent despite the event-sourced architecture making it a natural fit. The edge-case handling (c15) is present but insufficiently specific — 'privilege escalation' and 'workspace takeover' gesture at the concern without naming canonical cases like last-admin removal or invite expiry.
