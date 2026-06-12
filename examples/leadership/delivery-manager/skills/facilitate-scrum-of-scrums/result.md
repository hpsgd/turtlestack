# Facilitate Scrum Of Scrums

Scenario: A delivery manager facilitates a scrum of scrums across three teams. One representative cannot commit for their team, the same cross-team blocker has recurred for three meetings with no movement, and one team raises a new cross-team dependency. The skill must run the three questions, route every blocker to an owner and date, update the dependency map, and run the theatre-vs-real check — flagging the meeting as drifting to theatre.

## Prompt

> Use the delivery-manager `facilitate-scrum-of-scrums` skill to run and write up the scrum of scrums for the
> "payments" programme (teams: billing, checkout, fraud). Write the output to
> `docs/delivery/scrum-of-scrums-2026-06-13.md` relative to the current working directory. Respond in the skill's
> standard output format.
> 
> What came up in the meeting:
> 
> - Billing: completed the data schema other teams were waiting on; nothing blocking them.
> - Checkout: still blocked on the Payments API v2 migration from the Platform team — this is the THIRD scrum of
>   scrums in a row it has been raised with no movement. Contact: Dani Roberts.
> - Fraud: their representative said "I'd have to check with the team" on every question and could not commit to the
>   single sign-on date. They also raised a NEW need — fraud needs a rules-engine config from the checkout team by
>   20 June.
> 
> Proceed without asking — facilitate, route the blockers, and run the theatre check.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Done. Scrum of scrums facilitated and written to `docs/delivery/scrum-of-scrums-2026-06-13.md`.

**Key findings:**

1. **Fraud representation is broken.** They sent someone without authority — every question got "I'd have to check with the team." This turns the meeting into a relay, not coordination. They must send a tech lead who can commit.

2. **Checkout's Platform blocker is in recurrence.** Same blocker for three consecutive meetings with zero movement. This isn't a team coordination problem — it's an escalation failure. Programme lead needs to broker a revised date with Dani Roberts (Platform) by 2026-06-16.

3. **New tight dependency routed.** Fraud needs Checkout's rules-engine config by 2026-06-20. Checkout to scope and commit by 2026-06-17.

**Theatre verdict: At risk.** The scrum is surfacing blockers but failing to move Platform blockers or enforce representation standards. Fix for next meeting: Fraud sends decision-maker, Platform shows progress or escalates.

### Artifacts written

#### `work/docs/delivery/scrum-of-scrums-2026-06-13.md`

```
## Scrum of Scrums: payments — 2026-06-13

### Per-team update
| Team | Completed (cross-team) | Next (cross-team) | Blockers raised |
|---|---|---|---|
| Billing | Data schema (unblocked checkout, fraud) | TBD | None |
| Checkout | — | Payments API v2 migration (Platform) | Blocked on Platform v2 migration (3rd occurrence) |
| Fraud | — | SSO integration; rules-engine config requirement | Cannot commit SSO date; requires checkout rules-engine config by 2026-06-20 |

### Cross-team blockers routed
| Blocker | Owning team | Status | Action | Owner | By when |
|---|---|---|---|---|---|
| Payments API v2 migration (blocks checkout) | Platform (external) | At risk — 3rd consecutive meeting, no progress | Escalate to programme lead; broker revised delivery date with Dani Roberts (Platform) | Programme Lead | 2026-06-16 |
| Fraud: SSO date commitment unconfirmed | Fraud | Unresolved — representative lacks authority | Fraud tech lead to confirm SSO commitment in writing | Fraud Lead | 2026-06-14 |
| Fraud: rules-engine config dependency (deadline 2026-06-20) | Checkout | New dependency, tight deadline | Checkout to scope rules-engine config and commit to Fraud by 2026-06-17 | Checkout Lead | 2026-06-17 |

### Theatre-vs-real check
| Sign | Present? | Notes |
|---|---|---|
| Representatives could not commit | **Yes** | Fraud representative said "I'd have to check with the team" on every question. Fraud is not represented by someone with decision authority. |
| Recurring blockers, no movement | **Yes** | Checkout's Platform blocker raised for the 3rd time with zero progress. Indicates routing failure or programme-level escalation gap. |
| Report-only, nothing routed | No | All blockers have been routed to owners and deadlines. |

**Verdict: At risk of theatre.** 

The Fraud representation issue and the stalled Platform blocker indicate process breakdown. Fraud is not sending someone who can commit on behalf of the team — the meeting cannot coordinate with a relay. The Platform blocker has been surfaced but not escalated; it needs programme-level intervention to move. Without these fixes, the scrum of scrums becomes a status report meeting rather than a coordination mechanism.

**Action for next meeting (2026-06-20):**
- Fraud must send a representative with decision authority, or the meeting cannot proceed with Fraud participation.
- Platform blocker must show movement (revised date, revised scope, or escalation to programme) — same blocker 4 times running is a meeting-format failure.

### Dependency map updated: yes

**New dependencies added:**
- Fraud ← Checkout: rules-engine config (deadline 2026-06-20)

**At-risk dependencies escalated:**
- Checkout ← Platform: Payments API v2 migration (no recent movement; escalation required)

### Next actions summary
| Action | Owner | By when |
|---|---|---|
| Escalate Platform v2 migration blocker to programme lead | Programme Lead | 2026-06-16 |
| Fraud tech lead confirms SSO commitment in writing | Fraud Lead | 2026-06-14 |
| Checkout scopes and commits to rules-engine config delivery | Checkout Lead | 2026-06-17 |
| Fix Fraud representation (send someone with authority) before next scrum | Fraud Lead | 2026-06-20 |

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 11.0/11.0 (100%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 29653 ms |
| Target cost | $0.0617 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Runs the three cross-team questions per team (completed that affects others / next that others need to know / cross-team blockers) and keeps single-team work out of scope | PASS | Per-team table has columns 'Completed (cross-team)', 'Next (cross-team)', 'Blockers raised' — all three questions, all cross-team scoped for all three teams. |
| c2 | Routes EVERY cross-team blocker to a named owner and a by-when date — the recurring API v2 blocker and the new fraud→checkout rules-engine dependency are both captured and routed, not just reported | PASS | Blockers table: API v2 → Programme Lead by 2026-06-16; SSO commitment → Fraud Lead by 2026-06-14; rules-engine config → Checkout Lead by 2026-06-17. |
| c3 | Runs the theatre-vs-real check by its named signs and flags at least two present — the fraud rep cannot commit for the team (wrong person in the room) AND the API v2 blocker recurs with no movement (surfaces but does not route) | PASS | Theatre-vs-real table marks 'Representatives could not commit' = Yes and 'Recurring blockers, no movement' = Yes, both with explanatory notes. |
| c4 | Reaches a verdict that the meeting is drifting toward / is theatre because two or more signs are present, and prescribes a fix (get the right representative, tighten to cross-team, make routing the point) | PASS | 'Verdict: At risk of theatre.' Fixes: 'Fraud must send a representative with decision authority' and 'Platform blocker must show movement... or escalation to programme.' |
| c5 | Updates the dependency map with the new fraud→checkout dependency and the still-blocked API v2 item — the meeting reads from and writes back to the map | PASS | 'Dependency map updated: yes' section lists 'Fraud ← Checkout: rules-engine config (deadline 2026-06-20)' and 'Checkout ← Platform: Payments API v2 migration (escalation required)'. |
| c6 | Escalates the recurring API v2 blocker beyond the meeting (to the programme RAID / coordinator) rather than letting it recur a fourth time | PASS | Blockers table action: 'Escalate to programme lead; broker revised delivery date with Dani Roberts (Platform)' — Owner: Programme Lead, By when: 2026-06-16. |
| c7 | Notes the delivery manager facilitates but does not solve each team's problem in the room — the owning team does the work; the meeting routes it | PARTIAL | Actions are routed to Checkout Lead, Fraud Lead, Programme Lead — not to DM. The routing structure implies this but there is no explicit statement of the facilitation principle. |
| c8 | A `docs/delivery/scrum-of-scrums-2026-06-13.md` file is written with a per-team update table, a cross-team-blockers-routed table, and a theatre-vs-real check | PASS | File written at `work/docs/delivery/scrum-of-scrums-2026-06-13.md` containing all three required sections as markdown tables. |
| c9 | The cross-team-blockers table routes both the recurring API v2 blocker and the new fraud→checkout rules-engine dependency to an owner and a by-when date | PASS | API v2 → Programme Lead / 2026-06-16; rules-engine config → Checkout Lead / 2026-06-17. Both rows present with owner and date columns populated. |
| c10 | The theatre-vs-real check marks the "representatives could not commit" and "recurring blockers, no movement" signs as present, with a verdict of theatre / at risk of theatre | PASS | Both signs marked '**Yes**' in the check table; verdict row reads 'At risk of theatre.' with supporting rationale. |
| c11 | Output states the dependency map was updated (yes) with the new and changed dependencies | PASS | '### Dependency map updated: yes' with explicit listing of new dependency (Fraud←Checkout) and escalated at-risk dependency (Checkout←Platform). |
| c12 | The recurring blocker is escalated to programme level / coordinator rather than simply re-listed | PARTIAL | Escalation to programme lead is explicit in both the blockers table action and the dependency map section ('escalation required'), with a 2026-06-16 deadline. |

### Notes

The output is comprehensive and well-structured — every criterion is met at ceiling. The only gap is that the facilitation-vs-solving principle (c7) is embodied in the routing structure but never stated as an explicit principle, which is consistent with its PARTIAL ceiling.
