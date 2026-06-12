---
name: write-dependency-map
description: "Create or update the live dependency map — what each team needs from other teams, with owning team, contact, status (on track / at risk / blocked), and resolution date. Produces team-level and programme-level views and flags escalation triggers. Use for tracking cross-team dependencies, preparing a scrum of scrums, or when a dependency turns at-risk or blocked."
argument-hint: "[team or programme name, or the dependency to add]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Write a dependency map

Create or update the dependency map for $ARGUMENTS. The dependency map is a live artifact, not a diagram that gets printed and filed — it changes when reality changes. Dependencies are the greatest source of slippage in multi-team delivery, so this map earns its keep only if it is current. It lives at `docs/delivery/dependency-map.md`. Dependencies also appear in the RAID log (`write-raid-log`); the map is the cross-team coordination view, the RAID log is the governance record.

## Step 1: Read the current map

Read `docs/delivery/dependency-map.md` if it exists. You are updating a living artifact. If it does not exist, copy `templates/dependency-map.md`. Note the last-updated date.

## Step 2: Capture both directions

For the team in scope, map both directions of dependency:

- **Upstream** — what this team needs from others before it can proceed.
- **Downstream** — what other teams need from this team.

A team that tracks only its upstream dependencies blindsides the teams that depend on it. Capture both.

## Step 3: Record each dependency with full detail

```markdown
| ID | Dependency | Direction | Owning team | Contact | Status | Needed by | Escalation |
|---|---|---|---|---|---|---|---|
| D-009 | Payments API v2 migration | Upstream | Payments | [name] | At risk | 2026-06-30 | Owner notified 06-12; escalate to coordinator if not green by 06-20 |
```

Status is one of:

| Status | Meaning |
|---|---|
| On track | Owning team confirms it will land by the needed-by date |
| At risk | Signal that it may slip; you are managing it and may need help |
| Blocked | It will not land without intervention; escalate now |

Every dependency has a named contact at the owning team — not a team name. The needed-by date is the date this team actually needs it, not the date the other team plans to deliver. Ask "when do we actually need this?" before the dependency becomes urgent — that question prevents most slippage.

## Step 4: Build the two views

### Team-level view

The dependencies for a single team, both directions, as above. This is what the team and its delivery-manager work from day to day.

### Programme-level view

When multiple teams are in play, aggregate the cross-team dependencies into a programme view that shows the dependency web — which team blocks which. Highlight any chain where a single blocked dependency stalls multiple downstream teams. This view feeds the scrum of scrums and the programme RAID.

## Step 5: Apply escalation triggers

When a dependency turns at-risk or blocked, it is your job to escalate or broker resolution — not to manage the other team's work. Apply these triggers:

| Trigger | Action |
|---|---|
| Status moves to At risk | Notify the owning-team contact; set an escalation date |
| Status moves to Blocked | Escalate to the coordinator or the relevant lead now |
| Needed-by date inside two weeks and not On track | Raise in the next scrum of scrums and the status report |
| A single dependency blocks 2+ downstream teams | Escalate to programme level immediately |

## Rules

- The map is live or it is useless. Update it weekly and on any status change, not once at the start.
- Always capture both directions. Downstream dependencies you ignore become other teams' surprises.
- Every dependency has a named contact, not a team name. "Payments team" cannot be chased; a person can.
- The needed-by date is when this team needs it, not when the other team plans to ship it. The gap between those two is the risk.
- Never silently manage another team's work to clear a dependency. Escalate or broker — the work stays theirs.
- Don't let the map become a wall of green. If everything is on track but deliveries keep slipping, the map is not being updated honestly — cross-check with `audit-status-honesty`.

## Output Format

```markdown
## Dependency Map: [team / programme] — [updated date]

### Team-level view
| ID | Dependency | Direction | Owning team | Contact | Status | Needed by |
|---|---|---|---|---|---|---|

### Programme-level view (if multi-team)
| Blocking team | Dependency | Dependent team(s) | Status | Needed by |
|---|---|---|---|---|

### Escalations triggered this update
| ID | Status | Escalated to | By when |
|---|---|---|---|

### Critical chains
- [Any single dependency blocking 2+ downstream teams]
```

## Related skills

- `/delivery-manager:write-raid-log` — dependencies appear in both artifacts. The map is the cross-team coordination view; the RAID log is the governance record. Keep the status consistent between them.
- `/delivery-manager:facilitate-scrum-of-scrums` — the dependency map sets the scrum-of-scrums agenda, and blockers routed in that meeting update the map.
- `/delivery-manager:audit-status-honesty` — a map that is all green while deliveries keep slipping is a signal to audit; cross-check there.
