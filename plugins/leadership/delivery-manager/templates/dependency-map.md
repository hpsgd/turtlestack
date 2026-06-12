# Dependency Map — [team / programme]

> Live artifact. Updated weekly and on any status change. Every dependency has a named contact.
> The needed-by date is when this team actually needs it, not when the other team plans to ship it.
> Last updated: [YYYY-MM-DD]

## Team-level view

Both directions: upstream (what this team needs) and downstream (what others need from this team).

| ID | Dependency | Direction | Owning team | Contact | Status | Needed by | Escalation |
|---|---|---|---|---|---|---|---|
| D-001 | [what is needed] | Upstream / Downstream | [team] | [name] | On track / At risk / Blocked | [YYYY-MM-DD] | [trigger + action] |

## Programme-level view

Cross-team dependency web. Highlight chains where one blocked dependency stalls multiple downstream teams.

| Blocking team | Dependency | Dependent team(s) | Status | Needed by |
|---|---|---|---|---|

## Escalation triggers

| Trigger | Action |
|---|---|
| Status → At risk | Notify the owning-team contact; set an escalation date |
| Status → Blocked | Escalate to coordinator or the relevant lead now |
| Needed-by inside 2 weeks and not On track | Raise in the next scrum of scrums and status report |
| One dependency blocks 2+ downstream teams | Escalate to programme level immediately |
