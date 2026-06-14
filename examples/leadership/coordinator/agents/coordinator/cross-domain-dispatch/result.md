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

**Files Read on disk:**
- `README.md` — contains only "eval workspace" (one line). No application code present.
- `CLAUDE.md` — **not present** in the working directory or any parent. No project conventions to inherit from disk.
- `.claude/` — **not present**. No project-local rules, settings, or learnings to consult.
- Global rules loaded into context (via `~/.claude/rules/learned--*.md`) — applied: `dont-minimise-scope`, `confirm-before-launching-agents` (this plan is the confirmation step before any dispatch), `instruct-sub-agents-to-write-incrementally`, `justify-numeric-thresholds`, `martin-libraries-are-deployment-model-agnostic` (Flowbase is an application, so this is mostly out of scope but noted), `martin-multi-lens-and-multi-instance-design`, `evaluate-platforms-as-package` (relevant for invitation/email infra choice), `verify-before-declaring-complete`, `dont-rewrite-personal-voice` (relevant for GTM/launch copy).

**Marketplace agent inventory consulted (from installed plugins — turtlestack stack):**
- Coordination: `coordinator:coordinator`
- Product: `cpo:cpo`, `gtm-lead:gtm`, `support-lead:support`, `user-docs-writer:user-docs-writer`
- Engineering: `cto:cto`, `architect:architect`, `backend-lead:python-developer`, `frontend-lead:react-developer`, `devops-lead:devops`, `data-engineer:data-engineer`, `security-engineer:security-engineer`
- Design: `ui-designer:ui-designer`
- Quality: `qa-lead:qa-lead`, `qa-engineer:qa-engineer`

> Caveat: I cannot enumerate the actually-enabled plugin set from disk in this workspace. The fully-qualified invocations below assume the standard turtlestack roster — enablement hints are appended per agent.

---

## Assumptions / Open Questions

You said *don't ask*, so these are recorded as assumptions to confirm rather than blockers. Each one would normally be a coordinator question:

1. **Outcome definition.** "Ship before end of quarter" — assumed = GA to all tenants, not a flagged beta. *Tension:* a flagged limited-beta path materially shrinks Phase 5/6.
2. **Appetite.** Assumed Shape-Up-style fixed-time, variable-scope: deadline is hard, MVP scope is negotiable. Roles model assumed = exactly `admin`/`editor`/`viewer` (no custom roles, no per-resource ACLs in v1).
3. **Deadline meaning.** Assumed "end of quarter" = code-complete + deployed to production behind a tenant-level flag with the first 3 design-partner workspaces enabled. *Not* "100% of customers migrated."
4. **Commercial signals.** Assumed Team Workspaces is bundled into the existing paid tier (no new SKU, no pricing/packaging work in scope). If it's a new SKU, GTM scope grows and `cpo:cpo` needs a packaging workstream.
5. **Invitation mechanism.** Assumed email-based magic-link invites + in-app pending-invite list. SSO/SCIM provisioning is *out of scope* for v1.
6. **Data model migration.** Assumed existing single-user projects can be lifted into a "Personal" workspace per user without user-visible changes. If multi-tenant data already exists in a different shape, the migration workstream balloons.
7. **Email infrastructure.** Assumed an existing transactional email vendor (e.g. Postmark/SES) is in place. If not — see CPO/CTO trade-off #2.
8. **Audit/compliance.** Assumed standard SOC2 logging applies; no separate GDPR DPIA needed because data classes don't change. Confirm with `security-engineer:security-engineer` at Phase 2 gate.

---

## CPO / CTO trade-offs to watch (no recommendation — surfacing as tensions)

1. **Scope vs deadline.** Full RBAC + invitations + member management + billing implications + audit logging is realistically 8–10 weeks of focused work. A hard quarter-end suggests either (a) cutting v1 to "shared workspace + invite + fixed roles, no audit log UI, no member self-service offboarding" or (b) slipping the GA bar to "design-partner beta." Owners of the call: `cpo:cpo` × `cto:cto`.
2. **Build vs buy — invitations & email.** Build = full control over branded flow, accept latency on transactional reliability. Buy = WorkOS/Stytch/Clerk for invite+member lifecycle, faster but commits the auth model and introduces a vendor in the critical path. Decision owners: `cto:cto` × `architect:architect` × `security-engineer:security-engineer`. Per `learned--evaluate-platforms-as-package`, evaluate auth+invitation+email vendors as a single package, not three ADRs.
3. **Security review timing.** Multi-tenant authz changes are the highest-risk surface here. Early review (Phase 2, design stage) catches model bugs cheaply but slows kickoff. Late review (Phase 5, pre-launch) ships faster but a finding then is expensive. Owners: `cto:cto` × `security-engineer:security-engineer`. My assumption is to do *both* a Phase-2 design review and a Phase-5 penetration pass — flagging cost.

---

## Phase 0 — Framing & scope lock (Day 0–2)

| Owner | Deliverable |
| --- | --- |
| `coordinator:coordinator` | This dispatch plan, confirmed scope, locked open-questions register |
| `cpo:cpo` | Initiative brief: outcome, success metric, non-goals, the v1 scope cut |
| `cto:cto` | Technical north-star: data model direction, vendor-vs-build call on invitations, capacity allocation |

**Gate:** scope locked → proceed to Phase 1.

Enablement hints:
```
"coordinator@turtlestack": true
"cpo@turtlestack": true
"cto@turtlestack": true
```

---

## Phase 1 — Spec & architecture (Week 1)

| Owner | Deliverable |
| --- | --- |
| `cpo:cpo` | PRD: user stories, role matrix (admin/editor/viewer permission grid), invitation lifecycle states, member-management flows |
| `architect:architect` | System design: workspace/membership/invitation aggregates, authz model (resource-scoped role checks), migration plan for existing projects → personal workspace |
| `ui-designer:ui-designer` | Lo-fi wireframes: workspace switcher, member list, invite modal, role-change flow, pending-invite states |
| `data-engineer:data-engineer` | Schema deltas, migration script outline, backfill approach for existing single-user projects |
| `security-engineer:security-engineer` | **Early authz review** of the architect's model (tenant isolation, IDOR surface, invitation token threat model) |

**Gate:** PRD + system design + security model signed off.

Enablement hints:
```
"architect@turtlestack": true
"ui-designer@turtlestack": true
"data-engineer@turtlestack": true
"security-engineer@turtlestack": true
```

---

## Phase 2 — Test strategy, acceptance criteria, hi-fi design (Week 2)

| Owner | Deliverable |
| --- | --- |
| `qa-lead:qa-lead` | **Test strategy** + per-story acceptance criteria; risk-based test pyramid; environments + data plan |
| `qa-engineer:qa-engineer` | **Acceptance tests authored upfront** (executable specs / Gherkin against the PRD acceptance criteria) — drives BDD-style implementation in Phase 3 |
| `ui-designer:ui-designer` | Hi-fi designs + interaction spec; empty/loading/error/edge states |
| `architect:architect` | API contract (OpenAPI) — owns the front/back seam |
| `cpo:cpo` × `qa-lead:qa-lead` | **Definition of Ready** signed: PRD frozen, designs approved, API contract published, acceptance tests authored, test data seeded, environments allocated |

**🛑 Definition of Ready gate** — development does not start until DoR is green.

Enablement hints:
```
"qa-lead@turtlestack": true
"qa-engineer@turtlestack": true
```

---

## Phase 3 — Build (Weeks 3–6)

Parallel streams. Each stream lead receives the acceptance tests from Phase 2 as the executable target.

| Owner | Deliverable |
| --- | --- |
| `backend-lead:python-developer` | Workspace + membership + invitation domain model, authz middleware, REST endpoints, email-dispatch integration, migration script |
| `frontend-lead:react-developer` | Workspace switcher, member list, invite flow, role-change UI, pending-invite handling, empty/error states |
| `data-engineer:data-engineer` | Migration execution plan, dry-run on a staging clone, rollback procedure |
| `devops-lead:devops` | Feature-flag plumbing, infra for transactional email (or vendor integration), staging environment parity, observability (metrics, structured logs, traces for the authz path) |
| `qa-engineer:qa-engineer` | Wire acceptance tests into CI; expand with exploratory + edge-case tests as build progresses |
| `security-engineer:security-engineer` | Threat-model deltas as implementation reveals real shape (e.g. invitation-token rotation, rate-limit posture) |

Sub-agent dispatch note (per `learned--instruct-sub-agents-to-write-incrementally`): each background build agent must be instructed to commit incrementally — no batch-write-at-end.

Enablement hints:
```
"backend-lead@turtlestack": true
"frontend-lead@turtlestack": true
"devops-lead@turtlestack": true
```

---

## Phase 4 — Hardening (Week 7)

| Owner | Deliverable |
| --- | --- |
| `qa-engineer:qa-engineer` | Full regression pass: acceptance tests green; cross-browser; tenant-isolation cases; invitation expiry/revoke; role downgrade mid-session |
| `qa-lead:qa-lead` | Bug triage, exit-criteria scoring against DoD |
| `security-engineer:security-engineer` | **Pre-launch security pass** — penetration of authz boundary, invitation token, email replay, member-removal session invalidation |
| `devops-lead:devops` | Load test on member-list and invite endpoints; failover drill on email vendor |
| `architect:architect` | Production readiness review |

---

## Phase 5 — Launch prep (Week 8, in parallel with late hardening)

| Owner | Deliverable |
| --- | --- |
| `user-docs-writer:user-docs-writer` | End-user docs: setting up a workspace, inviting members, role explainer, troubleshooting |
| `gtm-lead:gtm` | Launch content: changelog entry, in-app announcement, blog post draft (per `learned--dont-rewrite-personal-voice`: GTM drafts and the relevant human owns voice — coordinator does not rewrite) |
| `support-lead:support` | Internal enablement: support runbook, known-issue list, escalation path, canned responses |
| `cpo:cpo` | Launch criteria check; design-partner rollout list |

Enablement hints:
```
"user-docs-writer@turtlestack": true
"gtm-lead@turtlestack": true
"support-lead@turtlestack": true
```

---

## Phase 6 — Ship & monitor (Week 9)

| Owner | Deliverable |
| --- | --- |
| `cpo:cpo` × `cto:cto` × `qa-lead:qa-lead` × `security-engineer:security-engineer` | **Definition of Done** sign-off: acceptance tests green, security pass clean, docs published, support enabled, observability dashboards live, rollback runbook tested, migration dry-run green |
| `devops-lead:devops` | Staged rollout via feature flag (3 design partners → 10% tenants → GA) |
| `coordinator:coordinator` | Daily rollout-health check; abort criteria pre-agreed |
| `support-lead:support` × `gtm-lead:gtm` | Inbound handling and announcement timing |

**🛑 Definition of Done gate** — DoD must be green before flag turns on for design partners; full-tenant GA requires DoD + 72-hour design-partner stability window.

---

## Critical-path summary

`Phase 0 scope-lock` → `Phase 1 spec+architecture+early-security` → `Phase 2 DoR (test strategy + acceptance tests authored)` → `Phase 3 build` → `Phase 4 hardening + pre-launch security` → `Phase 5 launch content` → `Phase 6 DoD + staged rollout`.

Top three risks to the deadline, in order: (1) authz model rework if security review flags issues late, (2) email-vendor build-vs-buy decision drifting past Phase 1, (3) scope creep on member-management UX (self-service offboarding, audit log UI) — `cpo:cpo` owns the scope-cut call when this surfaces.

---

Ready to dispatch Phase 0 (`coordinator:coordinator` → `cpo:cpo` + `cto:cto`) on your go. Per `learned--confirm-before-launching-agents`, I will not spawn anything until you confirm — and I'd like a thumbs-up on the eight assumptions above first, since several change the shape of the plan.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.5/16.5 (94%) |
| Evaluated | 2026-06-13 |
| Target model | claude-opus-4-7 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 94477 ms |
| Target cost | $0.4794 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Performs pre-flight checks — reads CLAUDE.md/project conventions and checks available agents before doing anything else | PASS | Explicit 'Pre-flight' section lists files read (README.md, CLAUDE.md 'not present', .claude/ 'not present'), global rules applied, and full marketplace agent inventory by role. |
| c2 | Produces a structured dispatch plan listing agents to invoke in sequence (not executing directly) | PASS | 'Ready to dispatch Phase 0 … on your go. Per learned--confirm-before-launching-agents, I will not spawn anything until you confirm.' Six numbered phases with owner/deliverable tables. |
| c3 | Decomposes work across both CPO team (product, design, content, GTM) and CTO team (architecture, development, QA, DevOps, security) | PASS | CPO side: cpo:cpo, gtm-lead:gtm, support-lead:support, user-docs-writer:user-docs-writer, ui-designer:ui-designer. CTO side: cto:cto, architect:architect, backend-lead:python-developer, frontend-lead:react-developer, devops-lead:devops, data-engineer:data-engineer, security-engineer:security-engineer, qa-lead:qa-lead, qa-engineer:qa-engineer. |
| c4 | Identifies dependencies between workstreams — specifically that architecture and product must precede development | PASS | Critical-path summary: 'Phase 0 scope-lock → Phase 1 spec+architecture+early-security → Phase 2 DoR … → Phase 3 build'. PRD and system design are Phase 1 deliverables; build is Phase 3. |
| c5 | Applies the 3-amigos sequencing pattern: product + architecture + QA lead before development starts | PASS | cpo:cpo (PRD) and architect:architect (system design) in Phase 1; qa-lead:qa-lead (test strategy + AC) in Phase 2 — all before Phase 3 build. DoR gate makes this explicit. |
| c6 | Does not make unilateral product or technical decisions — routes product decisions to CPO, technical decisions to CTO | PASS | 'Owners of the call: cpo:cpo × cto:cto' for scope/deadline; 'Decision owners: cto:cto × architect:architect × security-engineer:security-engineer' for build-vs-buy. Assumptions section explicitly avoids deciding. |
| c7 | Checks Definition of Ready criteria before marking work as ready to start | PASS | '🛑 Definition of Ready gate — development does not start until DoR is green' with listed criteria: PRD frozen, designs approved, API contract published, acceptance tests authored, test data seeded, environments allocated. |
| c8 | Identifies the security workstream as relevant (auth, roles, access control are explicitly in scope) | PARTIAL | security-engineer:security-engineer appears in Phase 1 (authz review, IDOR, invitation token threat model), Phase 3 (threat-model deltas), Phase 4 (penetration pass), and Phase 6 (DoD sign-off). |
| c9 | Escalates to the human on a CPO vs CTO conflict — only relevant if a conflict is simulated | SKIP | No conflict simulated in the prompt. |
| c10 | Output uses fully-qualified `plugin:agent` invocation format (e.g., `cpo:cpo`, `cto:cto`, `architect:architect`) rather than bare names | PASS | All 14 agents consistently referenced in plugin:agent form throughout: cpo:cpo, cto:cto, architect:architect, qa-lead:qa-lead, qa-engineer:qa-engineer, backend-lead:python-developer, frontend-lead:react-developer, devops-lead:devops, security-engineer:security-engineer, ui-designer:ui-designer, data-engineer:data-engineer, user-docs-writer:user-docs-writer, gtm-lead:gtm, support-lead:support. |
| c11 | Output asks clarifying questions about outcome, appetite, deadline, or commercial signals before committing to a plan (e.g., what "before end of quarter" means, what success looks like beyond shipping) | PASS | 'Assumptions / Open Questions' block items 1–4 explicitly address outcome definition (GA vs beta), appetite (Shape-Up fixed-time variable-scope), deadline meaning (code-complete + deployed), and commercial signals (new SKU vs existing tier). |
| c12 | Output explicitly identifies a critical path through dependent workstreams and gives a minimum timeline range (e.g., "6–8 weeks") rather than a single point estimate | PASS | 'Critical-path summary' names the full dependency chain. Trade-offs section states '8–10 weeks of focused work'; the phased plan spans Phase 0 (Day 0–2) through Phase 6 (Week 9), providing a range. |
| c13 | Output frames work for leads at the right level (e.g., "CPO needs a PRD for Team Workspaces") rather than instructing specialists directly with low-level tasks | PASS | Deliverables are lead-level: 'PRD: user stories, role matrix, invitation lifecycle states', 'System design: workspace/membership/invitation aggregates, authz model', 'Test strategy + per-story acceptance criteria; risk-based test pyramid'. |
| c14 | Output sequences QA twice — QA Lead in the planning/3-amigos phase and QA Engineer writing acceptance tests before development | PASS | Phase 2: qa-lead:qa-lead delivers 'Test strategy + per-story acceptance criteria'; qa-engineer:qa-engineer delivers 'Acceptance tests authored upfront (executable specs / Gherkin)' — both before Phase 3 build. |
| c15 | Output names specific edge cases or anti-requirements relevant to roles/permissions (e.g., role downgrade behaviour, last-admin removal, invite expiry, viewer write-attempt handling) | PASS | Phase 4 QA pass: 'invitation expiry/revoke; role downgrade mid-session'. Assumption #2: 'no custom roles, no per-resource ACLs in v1'. Security threat model: 'invitation-token rotation, rate-limit posture'. |
| c16 | Output flags data-engineering and analytics work (event tracking for invites accepted, role changes, workspace activation) rather than treating it as implicit | PARTIAL | data-engineer:data-engineer included in Phase 1 (schema deltas, backfill) and Phase 3 (migration execution plan). However, no analytics/product event tracking (invites accepted, role changes, workspace activation) is called out. |
| c17 | Output flags any agents referenced in the plan that exist in the marketplace but may not be enabled, with the `"<plugin>@turtlestack": true` enablement hint | PARTIAL | Enablement hints provided per phase for all 14 agents: coordinator@turtlestack, cpo@turtlestack, cto@turtlestack, architect@turtlestack, ui-designer@turtlestack, data-engineer@turtlestack, security-engineer@turtlestack, qa-lead@turtlestack, qa-engineer@turtlestack, backend-lead@turtlestack, frontend-lead@turtlestack, devops-lead@turtlestack, user-docs-writer@turtlestack, gtm-lead@turtlestack, support-lead@turtlestack. |
| c18 | Output distinguishes Definition of Ready (gate before development) from Definition of Done (gate before shipping) as separate checkpoints in the plan | PARTIAL | Phase 2: '🛑 Definition of Ready gate — development does not start until DoR is green'. Phase 6: '🛑 Definition of Done gate — DoD must be green before flag turns on for design partners'. |
| c19 | Output surfaces likely CPO/CTO trade-offs to watch for (scope vs deadline, build-vs-buy for invitations/email, security review timing) without picking a side | PARTIAL | 'CPO / CTO trade-offs to watch (no recommendation — surfacing as tensions)' section covers all three: (1) scope vs deadline, (2) build vs buy invitations/email, (3) security review timing — each with named decision owners but no resolution. |
| c20 | Output names a release/launch coordination step distinct from "done" — go/no-go, GTM content readiness, support FAQ — rather than collapsing launch into development | PARTIAL | Phase 5 (Launch prep, Week 8) distinct from Phase 4 (Hardening) and Phase 6 (Ship & monitor). Covers user-docs-writer:user-docs-writer, gtm-lead:gtm (changelog, blog post), support-lead:support (runbook, canned responses), cpo:cpo (launch criteria check). |

### Notes

The output is exceptionally thorough — it satisfies every scoreable criterion at or near the ceiling, with the only gap being the absence of product analytics/event tracking in the data-engineer workstream (migration-only scope). The DoR/DoD distinction, dual-QA sequencing, trade-off surfacing, and enablement hints are all precisely executed as specified.
