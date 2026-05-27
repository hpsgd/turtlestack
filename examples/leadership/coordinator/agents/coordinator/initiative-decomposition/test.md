---
# Match the model the agent declares (opus) in
# plugins/leadership/coordinator/agents/coordinator.md. The runner otherwise
# falls back to the harness default (Haiku), which is not what the
# agent is designed to run on.
target-model: claude-opus-4-7
---

# Test: Large initiative decomposition across CPO and CTO domains

Scenario: A major platform change (multi-tenancy) that spans product, engineering, security, and commercial concerns. Tests whether the coordinator decomposes into the right workstreams, maps them to agents, sequences dependencies, and produces a dispatch plan rather than jumping to implementation.

## Prompt

We want to add multi-tenancy to the platform. Enterprise customers have been asking for it and it's blocking three deals worth $400k combined ARR. The touches everything — data isolation, auth/permissions, billing, UI (workspace switching), documentation, and pricing model changes.

Do not ask for clarification — proceed based on the information provided. Produce the full decomposition now, noting any assumptions you make.

## Criteria

- [ ] PASS: Coordinator decomposes into workstreams that map to specific agents (architect for data isolation, CPO for pricing, developer for implementation, etc.)
- [ ] PASS: Dependencies between workstreams are identified and sequenced (e.g., data isolation design before implementation, pricing before billing)
- [ ] PASS: Both CPO and CTO workstreams are present — this is not purely technical (pricing, documentation, UX are product concerns)
- [ ] PASS: The decomposition includes effort estimates or sizing signals for each workstream
- [ ] PASS: A critical path is identified — which workstreams block everything else
- [ ] PARTIAL: Revenue context ($400k ARR) is used to inform priority and timeline, not just mentioned
- [ ] PASS: Security implications of multi-tenancy are called out as a specific workstream or constraint
- [ ] PASS: The output is a dispatch plan, not implementation — the coordinator doesn't write code or specs

## Output expectations

- [ ] PASS: Output's workstreams cover at minimum: data isolation (architect / data engineer), auth and permissions (architect / security), billing changes (CPO + finance), UI workspace switching (UX + UI designer + developer), documentation (technical writer), pricing model (CPO + GTM)
- [ ] PASS: Output's dependency map shows that data isolation design must complete before implementation, that pricing decisions must inform billing implementation, and that auth/permissions design feeds the UI workspace switching
- [ ] PASS: Output identifies the critical path — likely data isolation design → auth/permissions design → implementation → migration of existing customers — and names what blocks what
- [ ] PASS: Output uses the $400k ARR context to inform priority — connecting the dollar value to a target delivery date or quarter, not just citing the figure once
- [ ] PASS: Output flags multi-tenancy security as a distinct workstream — covering tenant isolation, blast-radius if one tenant is compromised, and customer-level encryption keys / data sovereignty options
- [ ] PASS: Output includes effort estimates per workstream as ranges (e.g. "data isolation design: 2-3 weeks", "billing changes: 4-6 weeks") — not single-point estimates that imply false precision
- [ ] PASS: Output is a dispatch plan — names the agent or role per workstream, the deliverable per workstream, and the entry/exit criteria — does NOT contain code, schema definitions, or implementation specs
- [ ] PASS: Output covers BOTH CPO (pricing model, packaging tiers, GTM messaging, customer comms for existing customers) AND CTO (data, auth, infra) workstreams — multi-tenancy is not purely technical
- [ ] PASS: Output addresses migration of existing single-tenant customers as a workstream — they need to be moved into the new model without disruption, and this typically blocks final cutover
- [ ] PARTIAL: Output identifies parallel opportunities — e.g. UX research on workspace switching can run while data isolation is being designed, technical-writer documentation drafting can run alongside implementation
