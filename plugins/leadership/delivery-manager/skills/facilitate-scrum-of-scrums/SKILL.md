---
name: facilitate-scrum-of-scrums
description: "Facilitate a scrum of scrums — a 15-30 minute cross-team coordination meeting with one representative per team covering what each team did, what is next, and cross-team blockers. Includes the theatre-vs-real check (representatives who cannot speak for their team make the meeting theatre). Use for multi-team delivery coordination and surfacing cross-team dependencies."
argument-hint: "[programme or set of teams being coordinated]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Facilitate a scrum of scrums

Facilitate the scrum of scrums for $ARGUMENTS. A scrum of scrums is a lightweight cross-team coordination meeting — 15 to 30 minutes, one representative per team, run after each team's own stand-up. The delivery-manager facilitates. Its purpose is to surface and route cross-team blockers and dependencies, not to re-run each team's stand-up. It draws on and updates the dependency map (`write-dependency-map`).

The risk is that the scrum of scrums becomes its own ceremony, disconnected from actual team work. If the representatives cannot speak for their teams, the meeting is theatre — Step 4 checks for this directly.

## Step 1: Confirm the representatives

Each team sends one representative who can speak for the team — commit to dependencies, report real status, and carry actions back. Confirm before the meeting that each team is represented by someone with that authority. A representative who has to "check with the team" on everything turns the meeting into a relay, not coordination.

## Step 2: Run the three questions per team

For each team, the representative answers three questions — kept tight:

1. **What did the team complete since last time** that affects other teams?
2. **What is the team doing next** that other teams need to know about?
3. **What cross-team blockers or dependencies** need attention?

Keep the focus cross-team. Work that affects only the team itself belongs in that team's own stand-up, not here. Cut anything that is not cross-team.

## Step 3: Capture and route cross-team blockers

Every cross-team blocker raised is captured and routed:

```markdown
| Blocker | Raised by | Owning team | Status | Action | Owner | By when |
|---|---|---|---|---|---|---|
| API v2 migration slipping | Payments-dependent team | Payments | At risk | Broker a revised date | [name] | 2026-06-16 |
```

Route each blocker to an owner and a date. A blocker raised and not routed is a blocker the meeting failed to manage. Update the dependency map with anything new or changed.

## Step 4: Run the theatre-vs-real check

After the meeting, check it was real coordination, not theatre. Signs of theatre:

| Sign | What it means |
|---|---|
| Representatives could not commit on behalf of their team | The wrong people are in the room |
| The same blockers recur every meeting with no movement | The meeting surfaces but does not route |
| Nothing was decided or routed — only reported | This is a status read-out, not coordination |
| Teams treat it as a meeting to survive, not use | The meeting has lost its purpose |

If two or more signs are present, the scrum of scrums is theatre. Fix the format: get the right representatives, tighten to cross-team only, and make routing the point. A theatre meeting is worse than no meeting — it consumes time from every team and creates the appearance of coordination without the substance.

## Rules

- One representative per team, and they must be able to speak for the team. A relay is not coordination.
- Keep it cross-team. Single-team work belongs in the team's own stand-up. Cut it ruthlessly.
- Every blocker is routed to an owner and a date, then reflected in the dependency map. Surfacing without routing is half a job.
- 15-30 minutes. If it runs longer, it has drifted into re-running each team's stand-up.
- Run the theatre check every time. The scrum of scrums decays into theatre by default — the check is what keeps it real.
- The delivery-manager facilitates but does not solve each team's problems in the room. Route the blocker; the owning team does the work.

## Output Format

```markdown
## Scrum of Scrums: [programme] — [date]

### Per-team update
| Team | Completed (cross-team) | Next (cross-team) | Blockers raised |
|---|---|---|---|

### Cross-team blockers routed
| Blocker | Owning team | Status | Action | Owner | By when |
|---|---|---|---|---|---|

### Theatre-vs-real check
| Sign | Present? |
|---|---|
| Representatives could not commit | Yes / No |
| Recurring blockers, no movement | Yes / No |
| Report-only, nothing routed | Yes / No |

Verdict: [Real coordination / At risk of theatre / Theatre — fix the format]

### Dependency map updated: [yes / no]
```

## Related skills

- `/delivery-manager:write-dependency-map` — the scrum of scrums reads from and writes back to the dependency map. Blockers routed in the meeting update the map; at-risk dependencies in the map set the agenda.
- `/delivery-manager:review-raid-log` — cross-team blockers that cannot be resolved at team level escalate into the programme RAID. The scrum of scrums is where they surface.
