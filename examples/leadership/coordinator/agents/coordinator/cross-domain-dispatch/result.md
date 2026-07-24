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

# Team Workspaces — Coordination Dispatch Plan

## Pre-flight

**Files Read**
- `/private/var/folders/.../work/README.md` — single line "# eval workspace". No product code, no existing `CLAUDE.md`, no ADRs, no domain docs.
- `/private/var/folders/.../work/.git/` — repo exists, single commit "initial", branch `main`, clean tree.
- `/var/folders/.../handoff/` — empty. No prior session state.
- `/var/folders/.../learnings/` — only `signals/` scaffold present, no captured patterns yet.
- `/var/folders/.../rules/` — 25 turtlestack rule files installed (v3.6.0). Load-bearing for this plan: `engineering-conventions--spec-first`, `coding-standards--spec-driven-development`, `coding-standards--testing`, `coding-standards--strict-validation`, `coding-standards--review-conventions`, `coding-standards--architecture`, `coding-standards--git-and-ci`, `security-compliance--security-baseline`, `thinking--planning-fallacy`, `thinking--mechanism-design`, `thinking--multi-instance-dispatch`, `writing-style--tone-and-voice`.
- Global learned rules loaded via `~/.claude/rules/` — the ones actually shaping this plan: `learned--dont-minimise-scope`, `learned--proceed-on-unconditional-work`, `learned--evaluate-platforms-as-package`, `learned--walk-variation-history-before-accepting-versioning-adr`, `learned--martin-multi-lens-and-multi-instance-design`, `learned--verify-before-declaring-complete`, `learned--instruct-sub-agents-to-write-incrementally`, `learned--sequential-when-unattended`.

**Marketplace agent inventory consulted** (via the agent registry surfaced this session; installed set from `turtlestack--*` rules v3.6.0). Agents referenced below in fully-qualified form:
`coordinator:coordinator`, `cpo:cpo`, `cto:cto`, `architect:architect`, `security-engineer:security-engineer`, `data-engineer:data-engineer`, `qa-lead:qa-lead`, `qa-engineer:qa-engineer`, `ui-designer:ui-designer`, `frontend-lead:react-developer`, `backend-lead:python-developer`, `devops-lead:devops`, `user-docs-writer:user-docs-writer`, `gtm-lead:gtm`, `support-lead:support`.

**Not consulted / deferred**: no CLAUDE.md exists in-repo, so no project-local conventions layered over turtlestack defaults. If Flowbase has an out-of-repo product wiki, this plan should be reconciled against it before Phase 1 kicks off.

---

## Assumptions / Open Questions

Surfacing the questions I would normally ask before decomposing. **These are assumptions, not decisions** — flag any that are wrong and I'll re-plan the affected phases.

1. **Outcome definition.** "Ship Team Workspaces" is assumed to mean *GA to all paying customers* by quarter-end, not a private beta or feature-flagged pilot. If the real bar is "beta behind flag with 10 design-partner accounts", scope in Phases 3–5 shrinks materially.
2. **Appetite.** Assumed *fixed-time, variable-scope* (Shape Up "appetite" framing) — the deadline is real, and we cut scope rather than slip. Alternative: fixed-scope, variable-time. This determines who owns the trade-off calls in Phase 3.
3. **Deadline meaning.** "End of the quarter" assumed = code-complete + docs live + GTM launched by that date. If it means "merged to main and behind a flag", enablement/GTM work moves out of the critical path.
4. **Commercial signals.** Assumed Team Workspaces is *included in existing paid plans* (no separate SKU, no billing changes). If it's a new upsell tier, add `cpo:cpo` pricing work and a billing/entitlements track in Phase 2.
5. **Existing account model.** Assumed Flowbase currently has single-user accounts and this is the first multi-tenant/collab surface. If workspaces already exist for billing purposes, the schema work is a migration, not a greenfield model.
6. **Auth stack.** Assumed the existing auth provider (SSO/session model) is unchanged — this feature adds authorisation (roles), not authentication.
7. **Invitation delivery.** Assumed transactional email infra already exists. Called out as a build-vs-buy tension below.
8. **Compliance scope.** Assumed SOC 2 / GDPR posture is inherited from the existing product; no new data residency or DPA renegotiation triggered by adding roles. Security review will validate.
9. **Regions & i18n.** Assumed English-only launch, single region. Translations follow post-GA.

---

## CPO/CTO trade-offs to watch (do not resolve here)

Per [[learned--martin-multi-lens-and-multi-instance-design]] — surface the tensions, let the responsible leads take conflicting positions, don't pre-reconcile.

- **Scope vs deadline.** Full RBAC + invitations + shared projects + audit log + billing seat management is unlikely to fit end-of-quarter at quality bar. `cpo:cpo` will push for the customer-visible surface; `cto:cto` will push for a defensible core. Explicit MoSCoW cut needed at Phase 2 gate.
- **Build vs buy — invitations + email.** Options: (a) build in-house against existing transactional email provider, (b) adopt an auth/permissions SaaS (WorkOS, Clerk Orgs, Auth0 Organizations, Frontegg) that ships invite flows out of the box, (c) hybrid — buy the invite/RBAC primitives, own the workspace domain model. Cost signal: (b)/(c) shave weeks off the deadline; (a) preserves data-model control and avoids per-seat vendor pricing. Owner: `cto:cto` with `cpo:cpo` on pricing exposure, `security-engineer:security-engineer` on data-residency implications. Per [[learned--evaluate-platforms-as-package]], evaluate as one package, not three ADRs.
- **Security review timing.** Options: (a) `security-engineer:security-engineer` review at design (Phase 2) *and* pre-merge (Phase 4), (b) design-only, (c) pre-merge-only. Multi-tenant authorisation is a class of feature where late-stage review routinely finds architectural issues that are expensive to fix — but early review can stall design. Recommend (a); flagging so `cto:cto` can decide.

---

## Phase 0 — Frame (½ day)

Owner: `coordinator:coordinator`.

- Resolve the assumptions block above with the sponsor. Every "assumed X" either becomes a decision or gets an explicit "still-open, deciding by <date>".
- Confirm quarter-end date and freeze it. Convert "end of quarter" to a concrete calendar date (per [[learned--martin-nfr-flavour-answers-to-ambiguity]] style, capture as a single-source-of-truth constant referenced everywhere downstream).
- Pick the build-vs-buy path for invitations/email so Phase 1 architecture isn't done twice.

**Exit gate:** assumptions resolved or explicitly deferred with owners.

---

## Phase 1 — Discovery & Framing (days 1–3)

Parallel, independent lenses. Dispatch concurrently.

| Owner | Deliverable |
|---|---|
| `cpo:cpo` | Product brief: problem, target user, success metrics, MoSCoW scope for Team Workspaces v1, competitive scan of collab/RBAC patterns (Notion, Linear, Figma). |
| `cto:cto` | Technical constraints memo: current auth/session model, existing tenancy assumptions, integration surface, build-vs-buy recommendation for invitations/email (per trade-off above). |
| `architect:architect` | High-level solution options (2–3), each with data model sketch, authorisation model (RBAC vs ReBAC), and migration story from single-user → workspaced accounts. |
| `security-engineer:security-engineer` | Threat model draft: tenant-isolation risks, invitation-abuse vectors, role-escalation paths, audit-log requirements, data-residency implications of any SaaS in the build-vs-buy shortlist. |
| `ui-designer:ui-designer` | Discovery sketches: workspace switcher, member management, invite flow, role-picker affordances; audit against existing Flowbase design system. |
| `gtm-lead:gtm` | Positioning brief: who this unlocks, message pillars, competitive framing, pricing/packaging implications flagged back to `cpo:cpo`. |

**Exit gate:** written specs/briefs on disk (per [[learned--instruct-sub-agents-to-write-incrementally]] — each agent instructed to save incrementally). `coordinator:coordinator` synthesises tensions surfaced by the lenses without collapsing them.

---

## Phase 2 — Design, Spec, and Test Strategy (days 3–7)

Sequential dependencies inside this phase; cross-owner reviews are parallel.

1. `cpo:cpo` — v1 spec: user stories, acceptance criteria per story, out-of-scope list, success metrics with baselines. Per `turtlestack--engineering-conventions--spec-first`, this is the contract for everything downstream.
2. `architect:architect` — ADR set (one per decision, not bundled): tenancy model, authorisation model, invitation lifecycle, data migration, API shape. Per [[learned--evaluate-platforms-as-package]], platform choices co-evaluated in one ADR.
3. `data-engineer:data-engineer` — schema design: `workspaces`, `workspace_members`, `roles`, `invitations`, audit-log table; migration plan from current single-user shape; backfill strategy for existing accounts.
4. `ui-designer:ui-designer` — hi-fi flows for invite, accept, role change, remove member, empty states, error states (expired invite, seat cap hit, etc.). Handed to `frontend-lead:react-developer` as design-system-conformant components.
5. `security-engineer:security-engineer` — design review of ADRs + threat model finalised. Approvals block Phase 3 start.
6. **`qa-lead:qa-lead` — test strategy** (Phase 2 QA seat #1): risk-based test plan across unit / integration / E2E / security / a11y / perf; environment strategy; acceptance-criteria review against `cpo:cpo`'s spec; enumerates gaps before dev starts.
7. **`qa-engineer:qa-engineer` — acceptance tests authored ahead of dev** (Phase 2 QA seat #2, spanning into early Phase 3): executable acceptance tests derived from the spec — red by design, will go green as `frontend-lead:react-developer` and `backend-lead:python-developer` implement. Per `turtlestack--coding-standards--spec-driven-development`.
8. `gtm-lead:gtm` + `user-docs-writer:user-docs-writer` — launch and docs plan skeletons drafted against the spec so they're not scrambling in Phase 5.

**Definition of Ready gate (blocks Phase 3):**

- [ ] Spec merged and signed off by `cpo:cpo`.
- [ ] ADRs merged and signed off by `cto:cto` and `architect:architect`.
- [ ] Threat model signed off by `security-engineer:security-engineer`.
- [ ] Schema + migration reviewed by `data-engineer:data-engineer` and `backend-lead:python-developer`.
- [ ] Test strategy signed off by `qa-lead:qa-lead`; executable acceptance tests committed (red) by `qa-engineer:qa-engineer`.
- [ ] Designs handed off, tokens/components identified by `ui-designer:ui-designer` and `frontend-lead:react-developer`.
- [ ] Build-vs-buy decision on invitations/email locked; if "buy", contract/DPA in flight owned by `cto:cto`.

Do not open a Phase 3 PR before every DoR box is ticked.

---

## Phase 3 — Build (days 7–18)

Parallel tracks; per [[learned--sequential-when-unattended]], if any dispatch runs unattended, batch per-track rather than firing all developers at once.

| Track | Owner | Scope |
|---|---|---|
| Data & migrations | `data-engineer:data-engineer` + `backend-lead:python-developer` | Schema migrations, backfill, seed fixtures, migration rehearsal on staging. |
| Backend API | `backend-lead:python-developer` | Workspace CRUD, membership, roles/permissions middleware, invitation issue/accept/revoke, audit-log writes, seat-cap enforcement. Contract-tested against `qa-engineer:qa-engineer`'s acceptance tests. |
| Frontend | `frontend-lead:react-developer` | Workspace switcher, members page, invite modal, role picker, empty/error states, accept-invite landing. |
| Auth/permissions integration | `backend-lead:python-developer` + `security-engineer:security-engineer` consulting | Authorisation middleware, tenant-isolation guards on every workspace-scoped endpoint. |
| Infra prep | `devops-lead:devops` | Feature flag wiring, staging seed data, email provider config (or SaaS vendor config if "buy" won), observability hooks (metrics, structured logs, traces on invite lifecycle), migration runbook. |
| Docs draft | `user-docs-writer:user-docs-writer` | User-facing docs drafted against the shipping UI (screenshots deferred to Phase 4). |

`qa-engineer:qa-engineer` runs the acceptance suite continuously; tickets filed against `backend-lead:python-developer` / `frontend-lead:react-developer` as tests flip.

---

## Phase 4 — Harden (days 18–22)

- `qa-lead:qa-lead` + `qa-engineer:qa-engineer` — full regression pass; exploratory testing on invite abuse (expired, replayed, revoked-mid-accept, cross-tenant leak attempts); a11y audit; perf smoke on member-list at 500/5k members.
- `security-engineer:security-engineer` — pre-merge security review: authorisation on every new endpoint, tenant isolation, invite-token entropy and expiry, audit-log completeness, secrets handling. Per the trade-off above, this is the second security touchpoint.
- `devops-lead:devops` — staging load test; production migration dry-run; rollback plan validated.
- `architect:architect` — cross-cutting review: does the shipped shape match the ADRs? Any drift documented or reverted.

---

## Phase 5 — Launch (days 22–end of quarter)

- `user-docs-writer:user-docs-writer` — final docs with real screenshots, in-app help strings, changelog entry.
- `gtm-lead:gtm` — launch content: announcement post, sales enablement, in-app announcement copy, launch-day social. Per [[learned--dont-rewrite-personal-voice]], if the sponsor is drafting the announcement themselves, `gtm-lead:gtm` edits rather than rewrites.
- `support-lead:support` — support runbook: known limitations, common issues, escalation paths, macros for the top 5 expected tickets, on-call briefed.
- `devops-lead:devops` — flagged rollout (internal → beta cohort → 10% → 100%), with dashboards + alerts pre-wired.
- `cpo:cpo` — success metrics baselined; post-launch review scheduled T+14.

**Definition of Done gate (blocks announcing the launch):**

- [ ] All spec acceptance criteria pass in production behind the flag.
- [ ] `qa-lead:qa-lead` sign-off: regression + a11y + perf targets met.
- [ ] `security-engineer:security-engineer` sign-off: pre-merge review closed, no unmitigated highs.
- [ ] `devops-lead:devops` sign-off: migration executed, rollback validated, dashboards live, alerts firing on synthetic failures.
- [ ] `user-docs-writer:user-docs-writer` sign-off: docs live, in-app strings shipped, changelog published.
- [ ] `support-lead:support` sign-off: runbook merged, on-call briefed, macros loaded.
- [ ] `gtm-lead:gtm` sign-off: launch content published, sales enabled.
- [ ] `cpo:cpo` sign-off: success metrics instrumented and reading from prod.
- [ ] `coordinator:coordinator` verification pass per [[learned--verify-before-declaring-complete]] — every checkbox above verified, not assumed.

Only after every DoD box is ticked does "Team Workspaces has shipped" get said out loud.

---

## Marketplace enablement hints

Append to project settings so any not-yet-enabled plugins can be turned on:

```json
{
  "coordinator@turtlestack": true,
  "cpo@turtlestack": true,
  "cto@turtlestack": true,
  "architect@turtlestack": true,
  "security-engineer@turtlestack": true,
  "data-engineer@turtlestack": true,
  "qa-lead@turtlestack": true,
  "qa-engineer@turtlestack": true,
  "ui-designer@turtlestack": true,
  "frontend-lead@turtlestack": true,
  "backend-lead@turtlestack": true,
  "devops-lead@turtlestack": true,
  "user-docs-writer@turtlestack": true,
  "gtm-lead@turtlestack": true,
  "support-lead@turtlestack": true
}
```

---

## What I need from you to kick off Phase 1

Confirm (or correct) the assumptions block, resolve the three CPO/CTO tensions or delegate them, and I'll dispatch Phase 1's six lenses in parallel with incremental-write instructions and background execution.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/16.5 (97%) |
| Evaluated | 2026-07-23 |
| Target model | claude-opus-4-7 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 116239 ms |
| Target cost | $0.7889 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Performs pre-flight checks — reads CLAUDE.md/project conventions and checks available agents before doing anything else | PASS | Dedicated 'Pre-flight' section lists files read (README.md, .git/, handoff, learnings, rules) and explicitly notes 'no CLAUDE.md exists in-repo'. Marketplace agent inventory listed by fully-qualified name. |
| c2 | Produces a structured dispatch plan listing agents to invoke in sequence (not executing directly) | PASS | Six named phases (0–5) with table-formatted agent owners and deliverables. Closes with 'What I need from you to kick off Phase 1' — dispatch is conditional on confirmation, not executed. |
| c3 | Decomposes work across both CPO team (product, design, content, GTM) and CTO team (architecture, development, QA, DevOps, security) | PASS | CPO side: cpo:cpo, ui-designer:ui-designer, gtm-lead:gtm, user-docs-writer:user-docs-writer. CTO side: cto:cto, architect:architect, backend-lead:python-developer, frontend-lead:react-developer, devops-lead:devops, security-engineer:security-engineer, qa-lead:qa-lead, qa-engineer:qa-engineer, data-engineer:data-engineer. |
| c4 | Identifies dependencies between workstreams — specifically that architecture and product must precede development | PASS | DoR gate explicitly: 'Spec merged and signed off by cpo:cpo. ADRs merged and signed off by cto:cto and architect:architect... Do not open a Phase 3 PR before every DoR box is ticked.' |
| c5 | Applies the 3-amigos sequencing pattern: product + architecture + QA lead before development starts | PASS | Phase 2 includes cpo:cpo (spec), architect:architect (ADRs), and qa-lead:qa-lead (test strategy) all gated before Phase 3 Build. DoR requires all three signed off. |
| c6 | Does not make unilateral product or technical decisions — routes product decisions to CPO, technical decisions to CTO | PASS | 'CPO/CTO trade-offs to watch (do not resolve here)' section surfaces three tensions without resolving them. Assumptions block explicitly labelled 'These are assumptions, not decisions'. |
| c7 | Checks Definition of Ready criteria before marking work as ready to start | PASS | Phase 2 closes with 'Definition of Ready gate (blocks Phase 3)' containing 7 explicit checkboxes across spec, ADRs, threat model, schema, test strategy, designs, and build-vs-buy decision. |
| c8 | Identifies the security workstream as relevant (auth, roles, access control are explicitly in scope) | PARTIAL | security-engineer:security-engineer appears in Phase 1 (threat model), Phase 2 (design review), Phase 3 (auth/permissions integration), and Phase 4 (pre-merge review). Ceiling capped at PARTIAL. |
| c9 | Escalates to the human on a CPO vs CTO conflict — only relevant if a conflict is simulated | SKIP | Not applicable — no conflict simulation in the test scenario. |
| c10 | Output uses fully-qualified `plugin:agent` invocation format (e.g., `cpo:cpo`, `cto:cto`, `architect:architect`) rather than bare names | PASS | Every agent reference uses plugin:agent form throughout: cpo:cpo, cto:cto, architect:architect, qa-lead:qa-lead, qa-engineer:qa-engineer, backend-lead:python-developer, frontend-lead:react-developer, devops-lead:devops, etc. |
| c11 | Output asks clarifying questions about outcome, appetite, deadline, or commercial signals before committing to a plan (e.g., what 'before end of quarter' means, what success looks like beyond shipping) | PASS | 'Assumptions / Open Questions' block has 9 items covering: outcome (GA vs beta), appetite (fixed-time vs fixed-scope), deadline meaning, commercial signals (pricing/SKU), existing account model, auth stack, invite infra, compliance, i18n. |
| c12 | Output explicitly identifies a critical path through dependent workstreams and gives a minimum timeline range (e.g., '6–8 weeks') rather than a single point estimate | PARTIAL | Phases are numbered with specific day ranges (Phase 3: days 7-18, Phase 4: days 18-22, Phase 5: days 22-end of quarter) showing a critical path, but no explicit range statement like '5-8 weeks minimum' is given. |
| c13 | Output frames work for leads at the right level (e.g., 'CPO needs a PRD for Team Workspaces') rather than instructing specialists directly with low-level tasks | PASS | Phase 1 cpo:cpo: 'Product brief: problem, target user, success metrics, MoSCoW scope...'; cto:cto: 'Technical constraints memo'; architect:architect: 'High-level solution options (2-3)'. |
| c14 | Output sequences QA twice — QA Lead in the planning/3-amigos phase and QA Engineer writing acceptance tests before development | PASS | Phase 2 item 6: 'qa-lead:qa-lead — test strategy (Phase 2 QA seat #1)'; item 7: 'qa-engineer:qa-engineer — acceptance tests authored ahead of dev (Phase 2 QA seat #2, spanning into early Phase 3)'. |
| c15 | Output names specific edge cases or anti-requirements relevant to roles/permissions (e.g., role downgrade behaviour, last-admin removal, invite expiry, viewer write-attempt handling) | PASS | Phase 4 QA: 'exploratory testing on invite abuse (expired, replayed, revoked-mid-accept, cross-tenant leak attempts)'; Phase 1 security: 'role-escalation paths'; Phase 2 UI: 'expired invite, seat cap hit' edge states. |
| c16 | Output flags data-engineering and analytics work (event tracking for invites accepted, role changes, workspace activation) rather than treating it as implicit | PASS | data-engineer:data-engineer explicitly in Phase 2 (schema + audit-log table) and Phase 3 (migrations track). devops: 'observability hooks (metrics, structured logs, traces on invite lifecycle)'. CPO DoD: 'success metrics instrumented and reading from prod'. |
| c17 | Output flags any agents referenced in the plan that exist in the marketplace but may not be enabled, with the `"<plugin>@turtlestack": true` enablement hint | PARTIAL | 'Marketplace enablement hints' section provides JSON with all 15 plugins in exact `"<plugin>@turtlestack": true` format (e.g., `"coordinator@turtlestack": true`, `"cpo@turtlestack": true`). |
| c18 | Output distinguishes Definition of Ready (gate before development) from Definition of Done (gate before shipping) as separate checkpoints in the plan | PARTIAL | Phase 2 has 'Definition of Ready gate (blocks Phase 3)' with 7 checkboxes; Phase 5 has 'Definition of Done gate (blocks announcing the launch)' with 9 checkboxes. Both use exact named terms. |
| c19 | Output surfaces likely CPO/CTO trade-offs to watch for (scope vs deadline, build-vs-buy for invitations/email, security review timing) without picking a side | PARTIAL | 'CPO/CTO trade-offs to watch (do not resolve here)' section covers all three: scope vs deadline, build vs buy for invitations/email (three options listed), and security review timing (three options a/b/c listed). |
| c20 | Output names a release/launch coordination step distinct from 'done' — go/no-go, GTM content readiness, support FAQ — rather than collapsing launch into development | PARTIAL | Phase 5 'Launch' is entirely separate from Phase 3 Build and Phase 4 Harden, with distinct owners (gtm-lead:gtm, support-lead:support, user-docs-writer) and a DoD gate blocking announcement. |

### Notes

An exceptionally complete response that satisfies virtually every criterion, including the dual QA sequencing, named DoR/DoD gates, fully-qualified plugin:agent format, enablement hints, and the CPO/CTO tensions block. The only material gap is c12: the plan presents a detailed phased day schedule rather than an explicit uncertainty-bounded range (e.g., '5–8 weeks minimum'), so the 'minimum timeline range' requirement is only partially met.
