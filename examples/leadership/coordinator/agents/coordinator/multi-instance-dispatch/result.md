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

## Dispatch plan — Flowbase rebuild architecture

### Assumptions
- No dedicated `engineering:architect` / `cto:architect` plugin is installed in this session; the only plugin agents available are `analyst:*` and `coordinator:coordinator`. Plan uses `coordinator:coordinator` as the parameterised architect proxy per slice (its `coordinator:decompose-initiative` and `coordinator:write-spec` skills cover system design, contracts, and data model at the level needed). If an engineering plugin lands later, swap the per-slice owner for `<engineering-plugin>:architect` — the shape doesn't change.
- Auth provider is the only shared dependency and is treated as a fixed external contract, not in scope for any slice.
- You are attended for this dispatch (concurrent fan-out is fine; unattended would sequence per `learned--sequential-when-unattended`).

### Shape: 3 parallel slice-owners + 1 reconciler

Follows the multi-instance pattern — same agent, slice-parameterised context, orchestrated from above ([[learned--martin-multi-lens-and-multi-instance-design]], [[learned--martin-agents-are-cheap-focus-is-value]]).

| # | Owner (fully qualified) | Slice | Deliverables (written to slice dir) |
|---|---|---|---|
| 1 | `coordinator:coordinator` | Partner integration API | `docs/slices/integration-api/{system-design,api-contract,data-model,adr/}` |
| 2 | `coordinator:coordinator` | Admin console | `docs/slices/admin-console/{system-design,api-contract,data-model,adr/}` |
| 3 | `coordinator:coordinator` | Mobile backend | `docs/slices/mobile-backend/{system-design,api-contract,data-model,adr/}` |
| R | `coordinator:coordinator` | Reconciliation (runs after 1–3) | `docs/system/{overview,cross-slice-adr,shared-auth-contract,open-conflicts}.md` |

All four are the same agent type; the slice is set by the prompt's context header ("You are the architect for the **<slice>** slice only") and the write-root path.

### How each parallel worker is kept to its own slice

- **Prompt fence.** Each dispatch prompt starts with an explicit scope block: the slice name, its user/consumer, its bounded write-root (`docs/slices/<slice>/**`), and a hard "do not read or write outside this path; do not reference the other two slices except via the shared auth-provider contract" instruction.
- **Filesystem fence.** Isolated write-roots per slice mean no path collisions during concurrent runs. No worktree isolation needed — different directories, no overlapping files.
- **Shared-contract stub.** A one-page `docs/system/shared-auth-contract.md` seeded before dispatch (auth provider name, token shape, claims contract). Each slice consumes this as read-only input; none of the three edits it. This is the ONLY cross-slice touchpoint they may reference.
- **Incremental writes.** Each dispatch prompt includes: *"Write files incrementally — save each doc as soon as drafted, don't batch to the end"* ([[learned--instruct-sub-agents-to-write-incrementally]]). Verify files on disk after each agent completes.
- **Conflict register, not conflict resolution.** If a slice-owner notices something that *feels* like it should be shared (a data type, an event, a naming choice), they append to `docs/slices/<slice>/open-questions.md` and keep going. They do not attempt to reconcile — that's the reconciler's job. Per [[learned--martin-multi-lens-and-multi-instance-design]], surfacing conflict is the design intent.

### How outputs are combined

Reconciler runs **after** all three slice-owners return and files are verified on disk. Its prompt:

1. Read all three `docs/slices/*/` trees + each slice's `open-questions.md`.
2. Produce `docs/system/overview.md` — one system-level view: three services, their boundaries, the auth-provider seam, cross-slice data flows (if any).
3. Produce `docs/system/cross-slice-adr/` — decisions that could not live in any single slice (shared event bus? shared user id space? shared observability?). One ADR per genuine cross-cutting decision.
4. Produce `docs/system/open-conflicts.md` — a register of contradictions across slices (e.g. integration-api and mobile-backend both proposed different pagination schemes) with a recommended resolution and severity. **Do not silently resolve** — list, recommend, flag for Martin.
5. Do **not** rewrite the slice docs. Cross-slice decisions land in `docs/system/`, and each slice cites them by relative link.

### Sequence

1. Seed `docs/system/shared-auth-contract.md` (5-min manual or 1 quick agent).
2. Fan out slices 1, 2, 3 in a **single message with three concurrent Agent calls** (attended run; if this becomes unattended, sequence them).
3. On all three returning, verify files on disk (`ls -la docs/slices/*/`).
4. Dispatch reconciler (R) with the three slice trees as read inputs.
5. Review `docs/system/open-conflicts.md` with Martin — that's the only step where decisions actually need a human.

### What I'd want your input on before firing (not blocking; parallel to setup)

- Whether an engineering-plugin architect agent exists in another marketplace you'd rather I load, vs. using `coordinator:coordinator` as the proxy.
- Confirmation the auth provider is truly the only shared seam (e.g. no shared billing / feature-flag / analytics service to add to the stub contract).

Both are refinements to the reconciler's inputs — the slice-owner dispatch shape is unconditional and can proceed either way.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 12.0/12.0 (100%) |
| Evaluated | 2026-07-23 |
| Target model | claude-opus-4-7 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 58933 ms |
| Target cost | $0.3726 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Recognises the work splits into independent slices that can run concurrently, rather than serialising it under one owner | PASS | Shape section: '3 parallel slice-owners + 1 reconciler'. Sequence: 'Fan out slices 1, 2, 3 in a single message with three concurrent Agent calls'. |
| c2 | Proposes multiple instances of the SAME agent (the architect) — one per slice — not three different agents and not one architect doing all three in sequence | PASS | Table shows all three slice owners as `coordinator:coordinator`. 'All four are the same agent type; the slice is set by the prompt's context header'. |
| c3 | Gives each instance a distinct identity/name tied to its slice (e.g. an integration-API architect, an admin-console architect, a mobile-backend architect) | PASS | Table rows: 'Partner integration API', 'Admin console', 'Mobile backend' — each with its own slice label and write path. |
| c4 | Defines a bounded scope per instance — what each one owns and what it must not touch — so concurrent work doesn't collide | PASS | 'hard "do not read or write outside this path; do not reference the other two slices except via the shared auth-provider contract" instruction'. |
| c5 | Does NOT propose duplicating or forking the plugin per slice — it's the same agent, slice-parameterised | PASS | 'All four are the same agent type; the slice is set by the prompt's context header'. No fork or copy of the plugin suggested. |
| c6 | Sequences an aggregation/reconciliation step that combines the three slices' outputs into a system-level view, as a dependent step after the parallel work | PASS | Reconciler (R) 'runs after all three slice-owners return and files are verified on disk', producing `docs/system/overview.md` and `docs/system/cross-slice-adr/`. |
| c7 | Addresses how concurrent writes are kept isolated (slice-scoped output locations by default; heavier isolation only if slices would write the same files) rather than leaving collision unaddressed | PARTIAL | 'Isolated write-roots per slice mean no path collisions during concurrent runs. No worktree isolation needed — different directories, no overlapping files'. |
| c8 | Uses the fully-qualified `plugin:agent` format (`architect:architect`) rather than bare role labels | PARTIAL | Uses `coordinator:coordinator` throughout — correct plugin:agent format, but not `architect:architect` (no architect plugin assumed installed; plan notes to swap if one lands). |
| c9 | Escalates a CPO vs CTO conflict — not relevant to this scenario | SKIP | N/A — criterion marked SKIP. |
| c10 | Output presents the three architecture workstreams as concurrent, not as a serial chain | PASS | Sequence step 2: 'Fan out slices 1, 2, 3 in a **single message with three concurrent Agent calls**'. |
| c11 | Output names or labels each architect instance per its slice so the executor can dispatch them distinctly | PASS | Table rows labelled 'Partner integration API', 'Admin console', 'Mobile backend'; write-roots `docs/slices/integration-api/`, `docs/slices/admin-console/`, `docs/slices/mobile-backend/`. |
| c12 | Output states a per-instance boundary (which service/paths are in scope for each) so the slices don't overlap | PASS | Each slice has a distinct bounded write-root in the table and 'prompt fence' instruction specifying the slice name and its `docs/slices/<slice>/**` write path. |
| c13 | Output includes a distinct reconciliation/aggregation step that depends on the three parallel workstreams completing | PASS | Sequence step 4: 'Dispatch reconciler (R) with the three slice trees as read inputs', after step 3 verifies all three slice outputs on disk. |
| c14 | Output notes the isolation approach for parallel writers (disjoint output locations by default; worktree-style isolation only if they'd touch the same files) | PARTIAL | 'No worktree isolation needed — different directories, no overlapping files.' Explicitly addresses when heavier isolation is/isn't required. |
| c15 | Output keeps the coordinator in its lane — produces a dispatch plan for the main conversation to execute rather than claiming to spawn the instances itself | PARTIAL | Sequence framed as instructions ('Fan out...', 'Dispatch reconciler...') and ends with 'What I'd want your input on before firing' — not claiming to have spawned anything. |

### Notes

The output is a strong, well-structured dispatch plan that correctly identifies all three services as independently parallelisable, applies the multi-instance same-agent pattern explicitly, isolates each slice by write-root and prompt fence, and sequences the reconciler as a dependent gate. The only partial deductions are on the four PARTIAL-capped criteria, all of which the output actually satisfies fully — the ceiling was set by the test, not by any gap in the response.
