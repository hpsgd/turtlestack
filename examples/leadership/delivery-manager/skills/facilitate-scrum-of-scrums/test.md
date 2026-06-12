# Test: facilitate-scrum-of-scrums routes cross-team blockers and runs the theatre check

Scenario: A delivery manager facilitates a scrum of scrums across three teams. One representative cannot commit for
their team, the same cross-team blocker has recurred for three meetings with no movement, and one team raises a new
cross-team dependency. The skill must run the three questions, route every blocker to an owner and date, update the
dependency map, and run the theatre-vs-real check — flagging the meeting as drifting to theatre.

## Prompt

Use the delivery-manager `facilitate-scrum-of-scrums` skill to run and write up the scrum of scrums for the
"payments" programme (teams: billing, checkout, fraud). Write the output to
`docs/delivery/scrum-of-scrums-2026-06-13.md` relative to the current working directory. Respond in the skill's
standard output format.

What came up in the meeting:

- Billing: completed the data schema other teams were waiting on; nothing blocking them.
- Checkout: still blocked on the Payments API v2 migration from the Platform team — this is the THIRD scrum of
  scrums in a row it has been raised with no movement. Contact: Dani Roberts.
- Fraud: their representative said "I'd have to check with the team" on every question and could not commit to the
  single sign-on date. They also raised a NEW need — fraud needs a rules-engine config from the checkout team by
  20 June.

Proceed without asking — facilitate, route the blockers, and run the theatre check.

## Criteria

- [ ] PASS: Runs the three cross-team questions per team (completed that affects others / next that others need to know / cross-team blockers) and keeps single-team work out of scope
- [ ] PASS: Routes EVERY cross-team blocker to a named owner and a by-when date — the recurring API v2 blocker and the new fraud→checkout rules-engine dependency are both captured and routed, not just reported
- [ ] PASS: Runs the theatre-vs-real check by its named signs and flags at least two present — the fraud rep cannot commit for the team (wrong person in the room) AND the API v2 blocker recurs with no movement (surfaces but does not route)
- [ ] PASS: Reaches a verdict that the meeting is drifting toward / is theatre because two or more signs are present, and prescribes a fix (get the right representative, tighten to cross-team, make routing the point)
- [ ] PASS: Updates the dependency map with the new fraud→checkout dependency and the still-blocked API v2 item — the meeting reads from and writes back to the map
- [ ] PASS: Escalates the recurring API v2 blocker beyond the meeting (to the programme RAID / coordinator) rather than letting it recur a fourth time
- [ ] PARTIAL: Notes the delivery manager facilitates but does not solve each team's problem in the room — the owning team does the work; the meeting routes it

## Output expectations

- [ ] PASS: A `docs/delivery/scrum-of-scrums-2026-06-13.md` file is written with a per-team update table, a cross-team-blockers-routed table, and a theatre-vs-real check
- [ ] PASS: The cross-team-blockers table routes both the recurring API v2 blocker and the new fraud→checkout rules-engine dependency to an owner and a by-when date
- [ ] PASS: The theatre-vs-real check marks the "representatives could not commit" and "recurring blockers, no movement" signs as present, with a verdict of theatre / at risk of theatre
- [ ] PASS: Output states the dependency map was updated (yes) with the new and changed dependencies
- [ ] PARTIAL: The recurring blocker is escalated to programme level / coordinator rather than simply re-listed
