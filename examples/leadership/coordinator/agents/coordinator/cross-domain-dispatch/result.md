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

# Team Workspaces — Dispatch Plan

## Pre-flight

**Files Read:**
- `./README.md` — empty eval workspace (single line: "eval workspace").
- `./CLAUDE.md` — **not present**. No project conventions, stack hints, ADRs, or domain memory available.
- `./.claude/` — **not present**. No project-local rules, agents, or settings.
- Global learned rules (`~/.claude/rules/learned--*.md`) — applied; notable: library-vs-application distinction, NFR-flavour answers to ambiguity, verify-before-declaring-complete, instruct sub-agents to write incrementally, hps.gd naming conventions.

**Marketplace agent inventory consulted** (from the agent table supplied by the runtime):
- Leadership: `coordinator:coordinator`, `cpo:cpo`, `cto:cto`.
- Engineering: `architect:architect` (assumed available via `architect@turtlestack`), `qa-lead:qa-lead`, `qa-engineer:qa-engineer`, `react-developer` (frontend), `python-developer` (backend), `devops:devops`, `security-engineer:security-engineer`, `data-engineer:data-engineer`, `code-reviewer:code-reviewer`, `release-manager:release-manager`, `performance-engineer:performance-engineer`.
- Product: `product-owner:product-owner`, `ui-designer:designer` (note: the marketplace inventory exposes this as `ui-designer:designer`, but the user's brief uses `ui-designer:ui-designer` — I will use the user's form and flag the discrepancy below), `ux-researcher:ux-researcher`, `gtm:gtm`, `support:support`, `user-docs-writer:user-docs-writer`, `developer-docs-writer:developer-docs-writer`, `internal-docs-writer:internal-docs-writer`, `customer-success:customer-success`.

**Lead-role mapping** (per the brief's naming):
- `frontend-lead:react-developer`
- `backend-lead:python-developer`
- `devops-lead:devops`
- `gtm-lead:gtm`
- `support-lead:support`

---

## Assumptions / Open Questions

The brief said "do not ask for clarification", so these are *labelled* and proceeding under the stated assumption. Each should be confirmed before Phase 1 closes.

| # | Question | Assumed answer (proceeding on this basis) |
|---|---|---|
| OQ-1 | **Outcome definition** — what does "shipped" mean? GA to all customers, opt-in beta, or dark launch behind a flag? | **Opt-in beta behind a feature flag**, GA gated on Phase 5 success criteria. |
| OQ-2 | **Appetite** — fixed scope / flexible date, or fixed date / flexible scope? | **Fixed date, flexible scope.** "Before end of quarter" reads as a hard deadline; non-core scope (e.g. audit log UI, advanced role policies) is the variable. |
| OQ-3 | **Deadline meaning** — code-complete, in-prod-for-customers, or marketing-launched by EOQ? | **In-prod for opt-in customers by EOQ**, marketing launch may trail by ≤ 2 weeks. |
| OQ-4 | **Commercial signals** — is this a paid SKU, a packaging change, or a free expansion? Does it gate a deal / renewal? | **Free expansion in current tier for beta**, monetisation deferred — but `cpo:cpo` to confirm with finance/sales. |
| OQ-5 | **Stack assumption** — Python/React inferred from the lead-role mapping in the brief. No CLAUDE.md to confirm. | **Python backend + React frontend** confirmed via brief's lead naming. |
| OQ-6 | **Existing tenancy model** — does Flowbase already have an "account" or "org" entity, or is workspace the first multi-user primitive? | **Workspace is new tenancy primitive.** `architect:architect` to validate against current data model in Phase 1. |
| OQ-7 | **Invitation transport** — transactional email provider in use? | **Unknown — see build-vs-buy below.** |
| OQ-8 | **Marketplace plugin name discrepancy** — brief says `ui-designer:ui-designer`, inventory lists `ui-designer:designer`. | Using brief's form; flagging for the user to reconcile. |

---

## CPO/CTO Trade-offs to Watch (surfaced, not resolved)

1. **Scope vs deadline.** Roles (admin/editor/viewer) × invitations × shared projects × permissions enforcement × audit is a lot for one quarter. Tension: every cut hurts the launch narrative; every keep hurts the date. `cpo:cpo` and `cto:cto` must jointly agree the MVP cut at the Phase 1 → 2 gate.
2. **Build vs buy — invitations & email.** Options: (a) build SMTP/SES integration in-house, (b) use a transactional provider (Postmark/SendGrid/Resend), (c) leverage an auth platform with team-invite primitives (WorkOS, Auth0 Organizations, Clerk). Trade-off: (c) is fastest to ship but creates platform lock-in for a core primitive; (a) is slowest but owns the surface. **No default chosen** — `cto:cto` + `cpo:cpo` decision in Phase 1.
3. **Security-review timing.** A multi-tenant permissions feature has a large blast radius (cross-workspace data leaks, privilege escalation, invitation-link abuse). Tension: doing `security-engineer:security-engineer` review *only* at the end risks a late "no-ship" finding; doing it too early reviews a design that will change. **Recommendation to discuss:** threat-model in Phase 2 (cheap, design-stage), vulnerability assessment in Phase 4 (pre-DoD, real code).

---

## Phased Dispatch

### Phase 1 — Framing & Decomposition (Days 0–3)

| Step | Owner | Deliverable |
|---|---|---|
| 1.1 | `cpo:cpo` | Product brief: problem statement, target users, success metrics, commercial framing (resolves OQ-4). Confirms MVP cut. |
| 1.2 | `cto:cto` | Technical framing: tenancy approach, build-vs-buy stance on invitations/email (resolves OQ-7), risk register. |
| 1.3 | `coordinator:coordinator` | Workstream decomposition (uses `coordinator:decompose-initiative` skill) — workstreams, dependencies, owners, effort estimates. |
| 1.4 | `ux-researcher:ux-researcher` | Lightweight user-needs validation (existing-customer signals, competitive snapshot of team/workspace patterns). |
| 1.5 | `architect:architect` | High-level architecture sketch + data-model impact assessment (resolves OQ-6). Identifies migration risk. |

**Gate:** `cpo:cpo` + `cto:cto` joint sign-off on MVP scope cut + build-vs-buy decision.

### Phase 2 — Specification, Design & Test Strategy (Days 3–10)

| Step | Owner | Deliverable |
|---|---|---|
| 2.1 | `cpo:cpo` (via `coordinator:write-spec`) | Spec: user stories, acceptance criteria, API contracts, data model. |
| 2.2 | `product-owner:product-owner` | Backlog: prioritised, sized, ready for development. |
| 2.3 | `ui-designer:ui-designer` | Component designs: invite flow, member list, role assignment, workspace switcher. *(Enablement hint below — discrepancy noted in OQ-8.)* |
| 2.4 | `architect:architect` | System design doc: workspace as tenancy boundary, permissions model (RBAC vs ABAC), invitation token design, audit log shape. |
| 2.5 | `data-engineer:data-engineer` | Migration plan from existing single-user model to workspace-scoped data. Backfill strategy. |
| 2.6 | **`qa-lead:qa-lead`** | **Test strategy + acceptance criteria review.** Risk-based test plan: tenancy isolation, role enforcement, invitation flows, migration. Defines what "tested" means. |
| 2.7 | **`qa-engineer:qa-engineer`** | **Acceptance tests written from spec — BEFORE development begins.** Executable specs (failing) covering each user story's acceptance criteria. Lives in the repo as the DoR gate. |
| 2.8 | `security-engineer:security-engineer` | **Design-stage threat model** (STRIDE on the proposed architecture). Cheap to fix at this stage. |

**Gate — Definition of Ready (DoR):** Spec exists. Designs approved. Acceptance tests committed and failing. Threat model surfaced top risks. Migration plan reviewed. `product-owner:product-owner` confirms backlog is ready.

### Phase 3 — Build (Days 10–35)

Parallel tracks; `coordinator:coordinator` reconciles via `coordinator:cross-domain-dispatch`.

| Track | Owner | Scope |
|---|---|---|
| 3.1 Backend | `backend-lead:python-developer` | Workspace model, membership, roles, invitation tokens, permissions middleware, audit log writes. |
| 3.2 Frontend | `frontend-lead:react-developer` | Workspace switcher, member management UI, invite flow, role-gated UI affordances. |
| 3.3 Data | `data-engineer:data-engineer` | Migration scripts, backfill, rollback plan. |
| 3.4 DevOps | `devops-lead:devops` | Feature-flag wiring, observability (metrics for invites sent/accepted, permission denials), DB migration runbook. |
| 3.5 Continuous QA | `qa-engineer:qa-engineer` | Acceptance tests must go green as features land. New tests for edge cases found during build. |
| 3.6 Code review | `code-reviewer:code-reviewer` | Every PR. |

### Phase 4 — Hardening (Days 35–45)

| Step | Owner | Deliverable |
|---|---|---|
| 4.1 | `security-engineer:security-engineer` | **Vulnerability assessment on the built code** (cross-workspace data access, IDOR, invitation token entropy, role-escalation paths). |
| 4.2 | `performance-engineer:performance-engineer` | Permission-check hot-path perf, query plans on workspace-scoped lookups. |
| 4.3 | `qa-lead:qa-lead` | Final test-strategy sign-off; confirms coverage of risk register from 2.6. |
| 4.4 | `developer-docs-writer:developer-docs-writer` | API docs for workspace endpoints. |
| 4.5 | `user-docs-writer:user-docs-writer` | Help-centre articles (invite flow, role definitions, common questions). |
| 4.6 | `internal-docs-writer:internal-docs-writer` | Internal runbook for support — common ticket patterns, escalation paths. |

**Gate — Definition of Done (DoD):** All acceptance tests green. Security findings remediated or accepted with `cto:cto` sign-off. Migration tested in staging with prod-shaped data. Docs published. Runbook delivered. Feature flag wired and off by default.

### Phase 5 — Launch (Days 45–60)

| Step | Owner | Deliverable |
|---|---|---|
| 5.1 | `release-manager:release-manager` | Release coordination: cut, deploy, flag rollout plan (cohort %, escalation triggers). |
| 5.2 | `devops-lead:devops` | Deployment + migration execution; monitoring dashboards live. |
| 5.3 | `gtm-lead:gtm` | Launch strategy: beta enrolment, comms calendar, positioning, in-app announcements. |
| 5.4 | `support-lead:support` | Support readiness: train team on runbook from 4.6, staffing for invite-flow tickets. |
| 5.5 | `customer-success:customer-success` | Beta-cohort selection & white-glove onboarding for top-N accounts. |
| 5.6 | `coordinator:coordinator` | Post-launch retro after 2 weeks of beta traffic. |

---

## Marketplace Enablement Hints

Append to `settings.json` `enabledPlugins` (or equivalent) any not currently enabled:

```json
{
  "coordinator@turtlestack": true,
  "cpo@turtlestack": true,
  "cto@turtlestack": true,
  "architect@turtlestack": true,
  "product-owner@turtlestack": true,
  "ux-researcher@turtlestack": true,
  "ui-designer@turtlestack": true,
  "qa-lead@turtlestack": true,
  "qa-engineer@turtlestack": true,
  "react-developer@turtlestack": true,
  "python-developer@turtlestack": true,
  "devops@turtlestack": true,
  "data-engineer@turtlestack": true,
  "security-engineer@turtlestack": true,
  "performance-engineer@turtlestack": true,
  "code-reviewer@turtlestack": true,
  "release-manager@turtlestack": true,
  "developer-docs-writer@turtlestack": true,
  "user-docs-writer@turtlestack": true,
  "internal-docs-writer@turtlestack": true,
  "gtm@turtlestack": true,
  "support@turtlestack": true,
  "customer-success@turtlestack": true
}
```

Note on OQ-8: the inventory exposes the UI designer as `ui-designer:designer` (agent name `designer`), but the brief specifies `ui-designer:ui-designer`. Reconcile before dispatch — likely a marketplace naming change.

---

## Next Step

Confirm OQ-1 through OQ-7 (especially OQ-2 deadline meaning and OQ-7 build-vs-buy on invitations/email), and the marketplace enablement set above. On confirmation, dispatch Phase 1 (`cpo:cpo`, `cto:cto`, `coordinator:coordinator`, `ux-researcher:ux-researcher`, `architect:architect` in parallel).

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.5/16.5 (94%) |
| Evaluated | 2026-05-27 |
| Target model | claude-opus-4-7 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 93608 ms |
| Target cost | $0.3659 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | PASS: Performs pre-flight checks — reads CLAUDE.md/project conventions and checks available agents before doing anything else | PASS | Dedicated 'Pre-flight' section lists files read (README.md, CLAUDE.md noted absent, .claude/ noted absent, global learned rules) and full marketplace agent inventory consulted before any decomposition. |
| c2 | PASS: Produces a structured dispatch plan listing agents to invoke in sequence (not executing directly) | PASS | Five-phase 'Phased Dispatch' table lists agents and deliverables in sequence. No agents are actually invoked; the plan ends with 'On confirmation, dispatch Phase 1.' |
| c3 | PASS: Decomposes work across both CPO team (product, design, content, GTM) and CTO team (architecture, development, QA, DevOps, security) | PASS | CPO side: cpo:cpo, product-owner:product-owner, ui-designer:ui-designer, gtm-lead:gtm, ux-researcher:ux-researcher, user-docs-writer:user-docs-writer. CTO side: architect:architect, backend-lead:python-developer, frontend-lead:react-developer, devops-lead:devops, qa-lead, qa-engineer, security-engineer, data-engineer. |
| c4 | PASS: Identifies dependencies between workstreams — specifically that architecture and product must precede development | PASS | DoR gate at Phase 2 end requires 'Spec exists. Designs approved. Acceptance tests committed.' Phase 3 (Build) only starts after Phase 2 completes. architect:architect delivers system design in Phase 2 before backend/frontend build in Phase 3. |
| c5 | PASS: Applies the 3-amigos sequencing pattern: product + architecture + QA lead before development starts | PASS | Phase 2 includes 2.1 (cpo:cpo spec), 2.4 (architect:architect system design), and 2.6 (qa-lead:qa-lead test strategy) — all three before Phase 3 Build. |
| c6 | PASS: Does not make unilateral product or technical decisions — routes product decisions to CPO, technical decisions to CTO | PASS | Trade-offs section explicitly says 'No default chosen — cto:cto + cpo:cpo decision in Phase 1' for build-vs-buy; scope/deadline tension assigned to joint cpo:cpo + cto:cto agreement. OQ table labels assumptions without resolving them. |
| c7 | PASS: Checks Definition of Ready criteria before marking work as ready to start | PASS | Explicit 'Gate — Definition of Ready (DoR)' at Phase 2 end: 'Spec exists. Designs approved. Acceptance tests committed and failing. Threat model surfaced top risks. Migration plan reviewed.' |
| c8 | PARTIAL: Identifies the security workstream as relevant (auth, roles, access control are explicitly in scope) | PARTIAL | security-engineer:security-engineer appears in Phase 2 (design-stage threat model, STRIDE) and Phase 4 (vulnerability assessment: cross-workspace data access, IDOR, invitation token entropy, role-escalation paths). |
| c9 | SKIP: Escalates to the human on a CPO vs CTO conflict — only relevant if a conflict is simulated | SKIP | Not applicable — no CPO/CTO conflict was simulated in the prompt. |
| c10 | PASS: Output uses fully-qualified `plugin:agent` invocation format (e.g., `cpo:cpo`, `cto:cto`, `architect:architect`) rather than bare names | PASS | All 23 agent references use plugin:agent format throughout: cpo:cpo, cto:cto, architect:architect, qa-lead:qa-lead, qa-engineer:qa-engineer, frontend-lead:react-developer, backend-lead:python-developer, devops-lead:devops, etc. |
| c11 | PASS: Output asks clarifying questions about outcome, appetite, deadline, or commercial signals before committing to a plan (e.g., what "before end of quarter" means, what success looks like beyond shipping) | PASS | 8-row 'Assumptions / Open Questions' table covers OQ-1 (outcome/shipped meaning), OQ-2 (appetite: fixed scope vs date), OQ-3 (deadline meaning: code-complete vs in-prod vs marketing-launched), OQ-4 (commercial signals: paid SKU or free). |
| c12 | PASS: Output explicitly identifies a critical path through dependent workstreams and gives a minimum timeline range (e.g., "6–8 weeks") rather than a single point estimate | PARTIAL | Critical path is identified via sequential phases with dependencies. However, the timeline is expressed as a fixed 60-day endpoint (Days 0-3, 3-10, 10-35, 35-45, 45-60) rather than a range like '8-12 weeks' acknowledging schedule uncertainty. |
| c13 | PASS: Output frames work for leads at the right level (e.g., "CPO needs a PRD for Team Workspaces") rather than instructing specialists directly with low-level tasks | PASS | Phase 1.1: 'cpo:cpo — Product brief: problem statement, target users, success metrics'; 1.2: 'cto:cto — Technical framing: tenancy approach, build-vs-buy stance'. Leads receive outcome framing, not step-by-step instructions. |
| c14 | PASS: Output sequences QA twice — QA Lead in the planning/3-amigos phase and QA Engineer writing acceptance tests before development | PASS | Phase 2.6: qa-lead:qa-lead 'Test strategy + acceptance criteria review' bold-labeled. Phase 2.7: qa-engineer:qa-engineer 'Acceptance tests written from spec — BEFORE development begins' bold-labeled. Both precede Phase 3. |
| c15 | PASS: Output names specific edge cases or anti-requirements relevant to roles/permissions (e.g., role downgrade behaviour, last-admin removal, invite expiry, viewer write-attempt handling) | PARTIAL | Phase 4.1 names 'role-escalation paths, IDOR, invitation token entropy, cross-workspace data access'; trade-offs mention 'invitation-link abuse'. Missing: last-admin removal guard, invite expiry, viewer write-attempt handling, role downgrade behavior. |
| c16 | PASS: Output flags data-engineering and analytics work (event tracking for invites accepted, role changes, workspace activation) rather than treating it as implicit | PASS | data-engineer:data-engineer is a named workstream in Phases 2.5 and 3.3. Phase 3.4 devops-lead:devops explicitly lists 'observability (metrics for invites sent/accepted, permission denials)' as a deliverable. |
| c17 | PARTIAL: Output flags any agents referenced in the plan that exist in the marketplace but may not be enabled, with the `"<plugin>@turtlestack": true` enablement hint | PARTIAL | Dedicated 'Marketplace Enablement Hints' section provides a JSON block with 23 entries in exact '"<plugin>@turtlestack": true' format covering all referenced agents. |
| c18 | PARTIAL: Output distinguishes Definition of Ready (gate before development) from Definition of Done (gate before shipping) as separate checkpoints in the plan | PARTIAL | 'Gate — Definition of Ready (DoR)' at Phase 2 end and 'Gate — Definition of Done (DoD)' at Phase 4 end are explicitly named as separate, distinct checkpoints using those exact terms. |
| c19 | PARTIAL: Output surfaces likely CPO/CTO trade-offs to watch for (scope vs deadline, build-vs-buy for invitations/email, security review timing) without picking a side | PARTIAL | Explicit 'CPO/CTO Trade-offs to Watch (surfaced, not resolved)' section covers all three: scope vs deadline, build-vs-buy (explicitly 'No default chosen'), and security timing (framed as 'Recommendation to discuss' not a decision). |
| c20 | PARTIAL: Output names a release/launch coordination step distinct from "done" — go/no-go, GTM content readiness, support FAQ — rather than collapsing launch into development | PARTIAL | Phase 5 (Days 45-60) is a dedicated launch phase separate from Phase 4 (DoD). Includes release-manager:release-manager (rollout plan), gtm-lead:gtm (launch strategy), support-lead:support (readiness), customer-success:customer-success (beta cohort). |

### Notes

An exceptionally thorough dispatch plan that satisfies nearly every criterion. The only notable gap is c12 (timeline expressed as a fixed 60-day endpoint rather than a range acknowledging uncertainty) and c15 (security edge cases are named but the UX anti-requirements like last-admin removal and viewer write-attempt handling are absent).
