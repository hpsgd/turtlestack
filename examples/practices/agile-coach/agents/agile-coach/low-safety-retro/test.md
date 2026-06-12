---
# The agile-coach agent declares model: sonnet in
# plugins/practices/agile-coach/agents/agile-coach.md. Run it on sonnet so the
# test exercises the model the agent is designed for, not the harness Haiku default.
target-model: claude-sonnet-4-6
---

# Test: agile-coach handles a recurring-action, low-safety team

Scenario: A delivery manager asks the coach to help with a team whose retrospectives keep producing the same action items sprint after sprint, and where people seem reluctant to speak openly. The coach must read the situation, hold its facilitation boundary, address safety before format, and route outcomes correctly — responding in its standard coaching methodology and deliverable format.

## Prompt

Use the `agile-coach` agent to help with the following situation, and respond in its standard coaching methodology and structured deliverable format.

The "billing" engineering team has run six retrospectives this quarter. The last three all produced the same two action items — "improve test coverage" and "reduce interruptions" — and neither moved. In the last retro, only two of the seven developers spoke; the rest stayed quiet while the tech lead talked. The delivery manager wants you to "just write them a better set of action items and tell them to follow the working agreement."

Work the problem as the agile coach. Do not ask me clarifying questions first — proceed with what you'd do, stating any assumptions.

## Criteria

- [ ] PASS: The coach holds its facilitation boundary — it explicitly declines to write the team's action items or working agreement for them, and explains it coaches the team to author its own
- [ ] PASS: The coach pushes back on the delivery manager's "just write them better action items" request rather than complying — naming that authored-for-them content is not coaching
- [ ] PASS: Psychological safety is treated as the priority given only two of seven spoke — the coach addresses safety before retrospective format polish
- [ ] PASS: The recurring identical action items are correctly diagnosed as a skipped insight phase / Wheel of Fortune anti-pattern, not just "the team isn't trying hard enough"
- [ ] PASS: The coach names that a working agreement violated repeatedly with no consequence is an authority/ownership gap, not a facilitation gap — and routes it accordingly
- [ ] PASS: The response distinguishes what the coach facilitates from what the coach actually does (does NOT do delivery, status, or own the content)
- [ ] PASS: Action items / improvements are routed into the next sprint backlog with an owner — not left as a parking lot or assigned to "the team"
- [ ] PARTIAL: The coach references its failure cap — same dysfunction three retros running with no movement signals an organisational cause to escalate, not coaching harder

## Output expectations

- [ ] PASS: Output is structured as a coaching engagement artifact (Context / Observations / Insights / Action items / what-was-coached-vs-done) rather than loose prose
- [ ] PASS: Output includes a safety read or an explicit plan to assess psychological safety before running the next retrospective
- [ ] PASS: Output's observations cite the specific evidence given (two of seven spoke, three retros with the same two stalled actions) rather than generic claims
- [ ] PASS: Output names at least one concrete facilitation technique to counter the loudmouth/HIPPO dominance pattern (e.g. silent writing, 1-2-4-All, dot voting) so the quiet five get heard
- [ ] PASS: Output separates team-fixable problems from organisational ones, and escalates the organisational ones to the lead/coordinator rather than coaching the team harder
- [ ] PASS: Output explicitly refuses to author the team's content (action items, working agreement) on the team's behalf and frames the coach's job as facilitating the team to produce its own
- [ ] PARTIAL: Output routes the recurring "improve test coverage" item toward a likely technical-practice/capability cause (a CTO/engineering-leadership concern) rather than treating it as a pure process item
