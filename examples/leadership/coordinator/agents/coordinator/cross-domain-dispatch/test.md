---
# Match the model the agent declares (opus) in
# plugins/leadership/coordinator/agents/coordinator.md. The runner otherwise
# falls back to the harness default (Haiku), which is not what the
# agent is designed to run on.
target-model: claude-opus-4-7
---

# Test: cross-domain dispatch

Scenario: A user brings a multi-domain feature launch request requiring product, design, engineering, and launch work. Does the coordinator decompose it correctly and produce a structured dispatch plan without making unilateral decisions?

## Prompt

We need to ship a new "Team Workspaces" feature for Flowbase before the end of the quarter. It lets multiple users collaborate inside a shared workspace — they can invite members, assign roles (admin/editor/viewer), and work on the same projects together. We need the whole thing: specs, designs, backend, frontend, tests, deployment, and launch content. Can you coordinate this?

Do not ask for clarification — proceed based on the information provided. Produce the dispatch plan now, noting any assumptions you make.

A few specifics for the response:

- **Pre-flight section at the top**: explicitly note the files Read (CLAUDE.md, project conventions) and the marketplace agent inventory consulted before decomposing.
- **Use fully-qualified `plugin:agent` invocation format** for every owner reference (e.g. `cpo:cpo`, `cto:cto`, `architect:architect`, `qa-lead:qa-lead`, `qa-engineer:qa-engineer`, `frontend-lead:react-developer`, `backend-lead:python-developer`, `devops-lead:devops`, `security-engineer:security-engineer`, `ui-designer:ui-designer`, `data-engineer:data-engineer`, `user-docs-writer:user-docs-writer`, `gtm-lead:gtm`, `support-lead:support`). No bare role labels.
- **Sequence QA twice**: `qa-lead:qa-lead` in Phase 2 (test strategy + acceptance criteria), AND `qa-engineer:qa-engineer` BEFORE development to write the acceptance tests (Phase 2 or early Phase 3, not Phase 4 only).
- **Use the explicit terms "Definition of Ready" and "Definition of Done"** as named gate checkpoints — DoR before development starts, DoD before shipping.
- **Open Questions section**: even though the user said "do not ask for clarification", surface the questions you would normally ask (outcome definition, appetite, deadline meaning, commercial signals) as a labelled "Assumptions / Open Questions" block — don't unilaterally infer.
- **Marketplace enablement hints**: for any `plugin:agent` referenced that may not be enabled, append the enablement hint `"<plugin>@turtlestack": true` so the user knows what to enable.
- **CPO/CTO trade-offs**: surface scope-vs-deadline, build-vs-buy for invitations/email infrastructure, and security-review timing as explicit tensions to watch — without picking a side.

## Criteria

- [ ] PASS: Performs pre-flight checks — reads CLAUDE.md/project conventions and checks available agents before doing anything else
- [ ] PASS: Produces a structured dispatch plan listing agents to invoke in sequence (not executing directly)
- [ ] PASS: Decomposes work across both CPO team (product, design, content, GTM) and CTO team (architecture, development, QA, DevOps, security)
- [ ] PASS: Identifies dependencies between workstreams — specifically that architecture and product must precede development
- [ ] PASS: Applies the 3-amigos sequencing pattern: product + architecture + QA lead before development starts
- [ ] PASS: Does not make unilateral product or technical decisions — routes product decisions to CPO, technical decisions to CTO
- [ ] PASS: Checks Definition of Ready criteria before marking work as ready to start
- [ ] PARTIAL: Identifies the security workstream as relevant (auth, roles, access control are explicitly in scope)
- [ ] SKIP: Escalates to the human on a CPO vs CTO conflict — only relevant if a conflict is simulated

## Output expectations

- [ ] PASS: Output uses fully-qualified `plugin:agent` invocation format (e.g., `cpo:cpo`, `cto:cto`, `architect:architect`) rather than bare names
- [ ] PASS: Output asks clarifying questions about outcome, appetite, deadline, or commercial signals before committing to a plan (e.g., what "before end of quarter" means, what success looks like beyond shipping)
- [ ] PASS: Output explicitly identifies a critical path through dependent workstreams and gives a minimum timeline range (e.g., "6–8 weeks") rather than a single point estimate
- [ ] PASS: Output frames work for leads at the right level (e.g., "CPO needs a PRD for Team Workspaces") rather than instructing specialists directly with low-level tasks
- [ ] PASS: Output sequences QA twice — QA Lead in the planning/3-amigos phase and QA Engineer writing acceptance tests before development
- [ ] PASS: Output names specific edge cases or anti-requirements relevant to roles/permissions (e.g., role downgrade behaviour, last-admin removal, invite expiry, viewer write-attempt handling)
- [ ] PASS: Output flags data-engineering and analytics work (event tracking for invites accepted, role changes, workspace activation) rather than treating it as implicit
- [ ] PARTIAL: Output flags any agents referenced in the plan that exist in the marketplace but may not be enabled, with the `\"<plugin>@turtlestack\": true` enablement hint
- [ ] PARTIAL: Output distinguishes Definition of Ready (gate before development) from Definition of Done (gate before shipping) as separate checkpoints in the plan
- [ ] PARTIAL: Output surfaces likely CPO/CTO trade-offs to watch for (scope vs deadline, build-vs-buy for invitations/email, security review timing) without picking a side
- [ ] PARTIAL: Output names a release/launch coordination step distinct from "done" — go/no-go, GTM content readiness, support FAQ — rather than collapsing launch into development
