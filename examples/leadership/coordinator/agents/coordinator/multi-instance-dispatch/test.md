---
# Match the model the agent declares (opus) in
# plugins/leadership/coordinator/agents/coordinator.md, consistent with the
# other coordinator agent tests. The runner otherwise falls back to Haiku.
target-model: claude-opus-4-7
---

# Test: multi-instance dispatch

Scenario: An initiative splits into several genuinely independent slices that can
progress at the same time, each needing the *same* role. Does the coordinator
recognise this and produce a multi-instance dispatch plan — several instances of
one agent, each scoped to its slice — rather than a single serial owner or a
request to duplicate the plugin?

## Prompt

We're rebuilding our product Flowbase as three independent services that share
nothing but the auth provider: a public partner **integration API**, an internal
**admin console**, and a customer-facing **mobile backend**. Each needs its own
architecture work — system design, API contracts, data model, ADRs — and the
three can be designed in parallel because they don't depend on each other. Once
all three are done we'll need them reconciled into one system-level view.

Plan how to staff the architecture work. Do not ask for clarification — proceed
based on the information provided, and produce the dispatch plan now, noting any
assumptions.

A few specifics for the response:

- Treat the three services as independent slices that can be worked concurrently.
- Use the fully-qualified `plugin:agent` invocation format for every owner.
- Be explicit about how each parallel worker is kept to its own slice and how their outputs are later combined.

## Criteria

- [ ] PASS: Recognises the work splits into independent slices that can run concurrently, rather than serialising it under one owner
- [ ] PASS: Proposes multiple instances of the SAME agent (the architect) — one per slice — not three different agents and not one architect doing all three in sequence
- [ ] PASS: Gives each instance a distinct identity/name tied to its slice (e.g. an integration-API architect, an admin-console architect, a mobile-backend architect)
- [ ] PASS: Defines a bounded scope per instance — what each one owns and what it must not touch — so concurrent work doesn't collide
- [ ] PASS: Does NOT propose duplicating or forking the plugin per slice — it's the same agent, slice-parameterised
- [ ] PASS: Sequences an aggregation/reconciliation step that combines the three slices' outputs into a system-level view, as a dependent step after the parallel work
- [ ] PARTIAL: Addresses how concurrent writes are kept isolated (slice-scoped output locations by default; heavier isolation only if slices would write the same files) rather than leaving collision unaddressed
- [ ] PARTIAL: Uses the fully-qualified `plugin:agent` format (`architect:architect`) rather than bare role labels
- [ ] SKIP: Escalates a CPO vs CTO conflict — not relevant to this scenario

## Output expectations

- [ ] PASS: Output presents the three architecture workstreams as concurrent, not as a serial chain
- [ ] PASS: Output names or labels each architect instance per its slice so the executor can dispatch them distinctly
- [ ] PASS: Output states a per-instance boundary (which service/paths are in scope for each) so the slices don't overlap
- [ ] PASS: Output includes a distinct reconciliation/aggregation step that depends on the three parallel workstreams completing
- [ ] PARTIAL: Output notes the isolation approach for parallel writers (disjoint output locations by default; worktree-style isolation only if they'd touch the same files)
- [ ] PARTIAL: Output keeps the coordinator in its lane — produces a dispatch plan for the main conversation to execute rather than claiming to spawn the instances itself
