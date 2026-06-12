---
name: prepare-steering-pack
description: "Prepare a steering-committee pack — a fortnightly or monthly governance pack pitched at the right level of abstraction, with decision asks named explicitly. Not a status read-out. Use for steering-committee meetings, executive updates, or any governance forum that exists to make decisions rather than receive status."
argument-hint: "[delivery or programme name and the steering cadence]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Prepare a steering pack

Prepare the steering-committee pack for $ARGUMENTS. A steering pack is not a weekly status report scaled up — it is a decision instrument. It abstracts up from the weekly status reports (`write-status-report`) to the level a steering committee needs, and its whole purpose is to surface the decisions that need a steering-level mandate. The pack is written to `docs/delivery/steering/[period-ending].md`.

The failure mode is status theatre: an hour-long meeting, a deck per person, an all-amber-and-green dashboard, and nobody learns anything they did not already know or makes a decision they could not have made by email. This skill exists to produce a pack that earns the meeting.

## Step 1: Pick the audience and abstraction level

Each governance audience needs a different level of abstraction:

| Audience | Cadence | Abstraction |
|---|---|---|
| Programme steering | Fortnightly | Delivery health across teams, cross-team risks, decisions needing programme mandate |
| Executive / board | Monthly | Outcomes against goals, top risks, funding and scope decisions |

Pitch the pack at the audience. A steering committee does not need the issue-by-issue RAID detail; it needs the two or three things that need its decision and the delivery health that frames them.

## Step 2: Summarise delivery health

Roll up the weekly status reports for the period into a short health summary: overall RAG with one line of why, the trajectory (improving / steady / deteriorating), and the two or three things that most shape the outcome. This is context for the decisions, not the point of the pack.

## Step 3: Name the decisions explicitly

This is the core of the pack. For each decision the committee needs to make:

```markdown
### Decision [N]: [the decision]
- **Context:** [why this is on the table now]
- **Options:** [the genuine alternatives, each with its consequence]
- **Recommendation:** [your recommendation and why]
- **Decision owner:** [who in the room can make this call]
- **Consequence of not deciding:** [what happens if the committee defers]
```

A steering pack with no decision asks is a status read-out wearing a governance costume. If there is genuinely nothing to decide, the meeting probably should not happen — say so.

## Step 4: Surface the top risks needing steering attention

Pull from the programme RAID the risks that need a steering-level intervention — the ones the delivery team cannot mitigate alone (funding, scope, cross-organisation dependencies, governance blockers). Present them with the ask, not just the colour.

## Step 5: Record decisions and actions

Leave space for the committee's decisions and the actions arising, and after the meeting record them. The decision log is what the next pack reports against — "at the last steering, the committee decided X; here is where that landed."

## Rules

- A steering pack exists to make decisions, not to report status. If it has no decision asks, it is theatre.
- Pitch at the audience's level. Steering does not need issue-level RAID detail; it needs the decisions and the health that frames them.
- Every decision ask names the options, the consequences, the recommendation, and who can decide. A vague "we should discuss X" wastes the meeting.
- Never present an all-green dashboard to avoid hard conversations. The committee's value is in unblocking the hard things — give them something to unblock.
- Record decisions after the meeting. A decision made in the room and lost by the next pack will be re-litigated.
- Don't reproduce the weekly status report. If the steering pack and the status report say the same thing, one of them is redundant.

## Output Format

```markdown
## Steering Pack: [programme] — [period ending]

### Delivery health
| Field | Value |
|---|---|
| Overall RAG | [colour + one-line why] |
| Trajectory | Improving / Steady / Deteriorating |
| Shaping the outcome | [the 2-3 things that matter most] |

### Decisions needed
### Decision 1: [decision]
- Context / Options / Recommendation / Decision owner / Consequence of not deciding

### Top risks needing steering attention
| Risk | Impact | Ask of the committee | Owner |
|---|---|---|---|

### Decisions made (recorded post-meeting)
| Decision | Outcome | Action | Owner | By when |
|---|---|---|---|---|
```

## Related skills

- `/delivery-manager:write-status-report` — the steering pack abstracts up from the weekly status reports. Do not reproduce them; pull the health summary and the decisions that need a steering mandate.
- `/delivery-manager:review-raid-log` — the top risks needing steering attention come from the programme RAID. Run the review first so the risks presented are current.
- `/delivery-manager:audit-status-honesty` — run before a steering meeting to confirm the health summary is not watermelon. Presenting an all-green pack that the RAID contradicts is theatre.
