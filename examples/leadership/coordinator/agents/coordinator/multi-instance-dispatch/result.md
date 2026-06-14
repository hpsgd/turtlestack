# Multi Instance Dispatch

Scenario: An initiative splits into several genuinely independent slices that can progress at the same time, each needing the *same* role. Does the coordinator recognise this and produce a multi-instance dispatch plan — several instances of one agent, each scoped to its slice — rather than a single serial owner or a request to duplicate the plugin?

## Prompt

> We're rebuilding our product Flowbase as three independent services that share
> nothing but the auth provider: a public partner **integration API**, an internal
> **admin console**, and a customer-facing **mobile backend**. Each needs its own
> architecture work — system design, API contracts, data model, ADRs — and the
> three can be designed in parallel because they don't depend on each other. Once
> all three are done we'll need them reconciled into one system-level view.
> 
> Plan how to staff the architecture work. Do not ask for clarification — proceed
> based on the information provided, and produce the dispatch plan now, noting any
> assumptions.
> 
> A few specifics for the response:
> 
> - Treat the three services as independent slices that can be worked concurrently.
> - Use the fully-qualified `plugin:agent` invocation format for every owner.
> - Be explicit about how each parallel worker is kept to its own slice and how their outputs are later combined.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

# Dispatch Plan — Flowbase Three-Service Rebuild Architecture

## Assumptions

- Each referenced plugin exposes one agent (same slug as the plugin's leaf), so invocation is e.g. `leadership/cto:cto`. Slice scoping is via prompt parameterisation, not via separate plugins (per the multi-instance design pattern).
- The shared auth provider is a given — not in scope for redesign by any slice.
- "ADRs" land per-slice in Phase 1; only cross-slice ADRs emerge in Phase 2.
- No external/customer research is in scope here, so the `analyst:*` plugins aren't dispatched.

## Phase 0 — Decompose (single owner, sequential, runs first)

| Step | Owner | Output |
|---|---|---|
| Split the rebuild into three slice charters; name the cross-slice contracts (auth integration, shared identifiers, eventing conventions if any) and pin them as "interfaces to honour, not to redesign". | `leadership/coordinator:coordinator` | Slice charters A/B/C + cross-slice contract list + a sealed "out-of-scope" boundary per slice |

Each slice charter explicitly lists the **other two slices as out-of-scope** so the Phase 1 workers can't drift sideways.

## Phase 1 — Parallel slice architecture (three concurrent slices)

Same agent code, three parameterised instances per role — one pinned to each slice. None of these instances can see the other slices' outputs during this phase.

**Slice A — Partner Integration API**
- `leadership/cto:cto` (instance "cto/integration-api") — system design, public API contracts, data model, slice-local ADRs
- `product/product-owner:product-owner` (instance "po/integration-api") — partner-developer-facing contract, acceptance criteria, slice scope guardrails

**Slice B — Internal Admin Console**
- `leadership/cto:cto` (instance "cto/admin-console") — same brief, scoped to admin console
- `product/product-owner:product-owner` (instance "po/admin-console") — internal-operator-facing contract & acceptance criteria

**Slice C — Customer-facing Mobile Backend**
- `leadership/cto:cto` (instance "cto/mobile-backend") — same brief, scoped to mobile backend
- `product/product-owner:product-owner` (instance "po/mobile-backend") — end-customer-facing contract & acceptance criteria

**Cross-slice supports running alongside Phase 1** (not slice-pinned, deliberately):
- `product/product-manager:product-manager` — validate-a-bet across the three-slice split itself (is "three independent services sharing only auth" still the right bet given what each slice is uncovering?)
- `product/product-analyst:product-analyst` — metrics-strategy across all three (success metrics per slice + system-level)

### How slice workers stay in their lane

1. Each prompt opens with the slice charter from Phase 0 and the sealed out-of-scope list. The "you are designing the X slice only; the other two slices are someone else's job and your design must not assume anything about their internals beyond the cross-slice contracts" framing is explicit.
2. Phase 1 instances are dispatched in parallel with no shared workspace — each writes to its own slice directory (e.g. `docs/architecture/integration-api/`, `…/admin-console/`, `…/mobile-backend/`).
3. The slice CTO and slice PO for one slice **can** consult each other (same slice); they cannot consult other-slice agents.
4. Any temptation to design a cross-slice mechanism gets logged as a Phase 2 input ("flag for reconciliation"), not resolved inline.

## Phase 2 — Reconciliation into a system-level view

Runs after all three slices' Phase 1 outputs are on disk. Multi-lens by design — conflict is surfaced, not pre-resolved.

| Step | Owner | Job |
|---|---|---|
| 1. Diff the three slices for conflicting/overlapping decisions (auth usage, identifier shapes, terminology, eventing assumptions, ops/observability conventions). Produce a reconciliation log. | `leadership/coordinator:coordinator` (cross-domain-conflict mode) | Conflict log + reconciliation candidates |
| 2. Arbitrate technical conflicts surfaced above; ratify or rewrite cross-slice ADRs. This is a **fresh system-level CTO instance**, distinct from the three slice CTOs, so it isn't anchored to one slice's prior commitments. | `leadership/cto:cto` (instance "cto/system") | Cross-slice ADRs + system technical view |
| 3. Sequence the three slices for build order, factoring dependencies, value, and risk. | `leadership/cpo:cpo` | Build sequence + go/no-go on the bet |
| 4. Final system-level dispatch: assemble the three slice docs + cross-slice ADRs into one navigable system view; assign follow-ups. | `leadership/coordinator:coordinator` (cross-domain-dispatch mode) | System-level architecture index, follow-up backlog |

## Conflict policy

Cross-slice disagreements are **surfaced as conflicts in the Phase 2 reconciliation log, not silently merged** — the system CTO and coordinator decide what wins, which keeps slice-local reasoning intact and visible after reconciliation.

## What's deliberately not staffed

- No `practices/agile-coach` or `leadership/delivery-manager` — this is architecture planning, not in-flight delivery; pull them in once Phase 2 hands off to build.
- No standalone analyst plugins — assuming the customer/partner understanding underlying the bet is already in hand.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 12.0/13.0 (92%) |
| Evaluated | 2026-06-13 |
| Target model | claude-opus-4-7 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 60306 ms |
| Target cost | $0.5973 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Recognises the work splits into independent slices that can run concurrently, rather than serialising it under one owner | PASS | Phase 1 is titled 'Parallel slice architecture (three concurrent slices)' and states 'None of these instances can see the other slices' outputs during this phase.' |
| c2 | Proposes multiple instances of the SAME agent (the architect) — one per slice — not three different agents and not one architect doing all three in sequence | PASS | 'Same agent code, three parameterised instances per role' — all three use `leadership/cto:cto` with distinct instance labels. |
| c3 | Gives each instance a distinct identity/name tied to its slice (e.g. an integration-API architect, an admin-console architect, a mobile-backend architect) | PASS | Instances labelled 'cto/integration-api', 'cto/admin-console', 'cto/mobile-backend' in the Phase 1 table. |
| c4 | Defines a bounded scope per instance — what each one owns and what it must not touch — so concurrent work doesn't collide | PASS | 'Each slice charter explicitly lists the other two slices as out-of-scope' and 'your design must not assume anything about their internals beyond the cross-slice contracts.' |
| c5 | Does NOT propose duplicating or forking the plugin per slice — it's the same agent, slice-parameterised | PASS | Assumptions section: 'Slice scoping is via prompt parameterisation, not via separate plugins (per the multi-instance design pattern).' |
| c6 | Sequences an aggregation/reconciliation step that combines the three slices' outputs into a system-level view, as a dependent step after the parallel work | PASS | Phase 2 'Reconciliation into a system-level view' explicitly 'Runs after all three slices' Phase 1 outputs are on disk' with a 4-step reconciliation process. |
| c7 | Addresses how concurrent writes are kept isolated (slice-scoped output locations by default; heavier isolation only if slices would write the same files) rather than leaving collision unaddressed | PARTIAL | 'each writes to its own slice directory (e.g. docs/architecture/integration-api/, …/admin-console/, …/mobile-backend/)' — disjoint locations addressed; no mention of heavier worktree-style escalation. |
| c8 | Uses the fully-qualified `plugin:agent` format (`architect:architect`) rather than bare role labels | PARTIAL | Uses `leadership/cto:cto`, `product/product-owner:product-owner`, `leadership/coordinator:coordinator` — fully-qualified but in a deeper `plugin/subplugin:agent` hierarchy, matching criterion intent. |
| c9 | Escalates a CPO vs CTO conflict — not relevant to this scenario | SKIP | Not applicable. |
| c10 | Output presents the three architecture workstreams as concurrent, not as a serial chain | PASS | Phase 1 header: 'Parallel slice architecture (three concurrent slices)' with all three slices shown side-by-side, not sequenced. |
| c11 | Output names or labels each architect instance per its slice so the executor can dispatch them distinctly | PASS | Instance labels 'cto/integration-api', 'cto/admin-console', 'cto/mobile-backend' appear explicitly in the Phase 1 section. |
| c12 | Output states a per-instance boundary (which service/paths are in scope for each) so the slices don't overlap | PASS | Each slice CTO entry lists its deliverables (e.g. 'system design, public API contracts, data model, slice-local ADRs') and Phase 0 charters seal out-of-scope boundaries. |
| c13 | Output includes a distinct reconciliation/aggregation step that depends on the three parallel workstreams completing | PASS | Phase 2 'Runs after all three slices' Phase 1 outputs are on disk' and contains four sequential steps assembling a system-level view. |
| c14 | Output notes the isolation approach for parallel writers (disjoint output locations by default; worktree-style isolation only if they'd touch the same files) | PARTIAL | Disjoint slice directories specified; worktree-style escalation for collision not mentioned — partial coverage matching the criterion's ceiling. |
| c15 | Output keeps the coordinator in its lane — produces a dispatch plan for the main conversation to execute rather than claiming to spawn the instances itself | PARTIAL | The output is a structured dispatch plan (tables, phases, ownership) presented as instructions for execution, not a claim of having spawned agents. |

### Notes

The output is a strong multi-instance dispatch plan that correctly parameterises one agent across three slice instances, enforces boundaries via Phase 0 charters, and sequences a dependent reconciliation phase. The only gaps are the absence of a worktree-style escalation path for concurrent writers and no explicit mention that disjoint directories are only the default tier.
