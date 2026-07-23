# Multi-instance dispatch

A role is not always singular. When a role's work splits into independent slices that can progress at the
same time — two architects on different subsystems, two delivery managers on different streams, a product
manager per product slice — run several instances of the *same* agent, each scoped to one slice. Same agent
code, slice-parameterised from above. Never ask for a duplicate plugin per slice.

This rule has two halves. If you write dispatch plans (coordinator, CTO, CPO, or any lead), read the first.
If you can be dispatched as an instance (every agent), read the second.

## When you dispatch multiple instances

You produce the plan; the main conversation spawns the instances (you can't — subagents cannot spawn
subagents). Instance identity is the spawn `name` (e.g. `architect-integration-api`), NOT a new invocation
string — the type stays the standard `plugin:agent` (`architect:architect`). Give the executor everything it
needs per instance:

| Field | What you specify |
|---|---|
| Instance name | A distinct, kebab-case label: `<role>-<slice>` (e.g. `delivery-manager-payments`) |
| Agent type | The standard `plugin:agent` reference |
| Slice scope | One sentence: what this instance owns |
| Boundary paths | The dirs/files this instance may write — its slice contract |
| Out of bounds | The sibling slices it must not touch |
| Isolation mode | `slice-scoped dirs` (default) or `worktree` — see below |
| Output location | Where this instance writes its artifacts |

**Choose isolation per dispatch.** When slices write disjoint paths — the common case — slice-scoped output
directories are the whole mechanism; no worktree needed. Declare `isolation: "worktree"` ONLY for instances
that would write the same files on disk. Worktrees cost setup time and disk per instance, so spend them only
when slices genuinely overlap. The plan carries this judgement, so the strategy can change without reworking
the mechanism.

**Vehicle.** Slice instances normally run as plain concurrent `Agent` dispatches. Two native alternatives
exist for the executor: a `Workflow` script when the fan-out is large and mechanical (deterministic
pipelines over many items; needs the user's explicit opt-in to multi-agent orchestration), and an agent
team (experimental) when instances genuinely need to message each other mid-flight. The dispatch plan may
recommend a vehicle; the executor decides.

**Aggregation.** When a higher-order instance rolls up the slices — a programme-level delivery manager
aggregating team RAID, a lead architect reconciling slice ADRs — make it a dependency edge: dispatch the
slice instances first, then dispatch the aggregator with read access to their outputs. State the aggregation
contract (what it consumes, what it produces) in the plan.

Example dispatch-plan fragment:

```
Multi-instance: architect ×2 (disjoint subsystems, run concurrently)
  1. architect:architect  name=architect-integration-api
     slice: partner integration API   boundary: docs/architecture/integration-api/
     out of bounds: docs/architecture/web-app/   isolation: slice-scoped dirs
  2. architect:architect  name=architect-web-app
     slice: end-user web app          boundary: docs/architecture/web-app/
     out of bounds: docs/architecture/integration-api/   isolation: slice-scoped dirs
  Then (depends on 1,2): architect:architect name=architect-lead
     aggregates: reconcile the two slice ADRs into a system-level view
```

## When you are a dispatched instance

If your dispatch context names a slice contract — your slice, your boundary paths, what's out of bounds —
treat it as a hard boundary:

- **Write only inside your boundary.** Create and modify files only within the paths the contract gives you.
- **Don't touch sibling slices.** Another instance is working concurrently in an adjacent scope. Do not read, create, or modify its files. A concurrent read of a sibling mid-write gives you a half-written view; any write collides.
- **Need something outside your slice? Surface it, don't reach for it.** If your slice genuinely depends on another's output, say so in your reply and let the dispatcher sequence it. Reaching across the boundary is how concurrent instances corrupt each other.

Absence of a slice contract means you are the single instance of your role. Nothing changes — work across the project as normal.

## Why convention, not a guard

Boundaries are enforced by discipline plus, when slices share files on disk, the git-worktree isolation the
dispatcher requests per dispatch. Most slices write disjoint paths, so the directory boundary is the whole
mechanism — you pay for a worktree only when two instances would write the same file. Honour the contract and
the cheap path stays safe.
