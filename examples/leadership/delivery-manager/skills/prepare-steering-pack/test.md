# Test: prepare-steering-pack produces a decision instrument, not a status read-out

Scenario: A delivery manager prepares the fortnightly steering pack for a programme that has been deteriorating
(Amber → Red over two weeks) because of a blocked dependency. The committee can fund a fix or slip the date — a real
steering decision. The skill must abstract up from the weekly status reports, name the decision explicitly with
options/consequences/recommendation, and avoid reproducing the weekly status or presenting an all-green dashboard.

## Prompt

Use the delivery-manager `prepare-steering-pack` skill to prepare the fortnightly programme-steering pack for the
"payments" programme. The recent weekly status reports are on disk under `docs/delivery/status/` relative to the
current working directory. Write the pack to `docs/delivery/steering/2026-06-13.md`. Respond in the skill's standard
output format.

Proceed without asking — read the status history, then prepare the pack.

## Criteria

- [ ] PASS: Abstracts up from the weekly status reports rather than reproducing them — the pack pitches at the steering level (delivery health + decisions), not the issue-by-issue RAID detail
- [ ] PASS: Reports the trajectory honestly as deteriorating (Amber → Red across the two weeks), not a single static colour
- [ ] PASS: Names the steering decision explicitly with the structure: context, genuine options each with their consequence, a recommendation, the decision owner, and the consequence of not deciding
- [ ] PASS: The decision presented is one only the committee can make (fund a second Platform engineer vs slip go-live) — a steering-level mandate, not a delivery-team decision
- [ ] PASS: Surfaces the top risk needing steering attention (the blocked cross-team dependency) with the ask of the committee, not just a colour
- [ ] PASS: Does not present an all-green dashboard — the pack gives the committee something concrete to unblock
- [ ] PARTIAL: States that a steering pack with no decision ask would be theatre, and leaves space to record the committee's decisions for the next pack to report against

## Output expectations

- [ ] PASS: A `docs/delivery/steering/2026-06-13.md` file is written with a delivery-health summary, a decisions-needed section, and a top-risks section
- [ ] PASS: The delivery-health summary states an overall RAG with a one-line why and a trajectory of Deteriorating
- [ ] PASS: At least one decision is presented with options, consequences, a recommendation, and the decision owner — not a vague "we should discuss the API"
- [ ] PASS: The pack does not reproduce the weekly status report verbatim — it summarises health and foregrounds the decision
- [ ] PARTIAL: A space or section exists to record decisions made post-meeting, so the next pack can report against them
