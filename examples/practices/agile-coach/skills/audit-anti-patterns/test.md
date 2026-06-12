# Test: audit-anti-patterns diagnoses Zombie and Dark Scrum and sorts cause

Scenario: Ceremonies look textbook but the team isn't improving or shipping. The coach must run the Zombie Scrum four-symptom check, the Dark Scrum diagnostic, and Aino Corry's retrospective anti-pattern catalogue against the supplied context, then separate team-fixable problems from organisational ones and respect the failure cap.

## Prompt

Use the agile-coach `audit-anti-patterns` skill to diagnose the "billing" team. The team's context dossier is at `docs/coaching/team-context.md` and the latest retrospective is in `docs/coaching/retrospectives/` (relative to the current working directory). On the surface every Scrum event runs on schedule, yet the team isn't shipping or improving. Read the records and produce the anti-pattern audit in the skill's standard format. Write the audit to `docs/coaching/` in the current working directory.

Proceed without asking — read the records and produce the diagnosis.

## Criteria

- [ ] PASS: Runs the Zombie Scrum four-symptom check by name — no working software shipped, no contact with the outside world, no emotional response, no drive to improve — and marks each against the supplied evidence
- [ ] PASS: Names a likely Zombie Scrum cause (cargo-cult adoption, no urgency, or organisational values incompatible with empiricism), not just "Zombie Scrum present"
- [ ] PASS: Runs the Dark Scrum diagnostic, citing the manager-set scope under deadline pressure, the skipped tests/refactoring, the growing technical debt, and the blame-session review
- [ ] PASS: Applies Aino Corry's retrospective anti-pattern catalogue by named items (e.g. Wheel of Fortune, Status theatre, Blame circles) against the retros, not a generic "the retros are bad"
- [ ] PASS: Identifies the missing technical-practice foundation as the Dark Scrum driver and flags it to the team's lead / CTO as an engineering-leadership problem, not a process one
- [ ] PASS: Sorts findings into team-fixable versus organisational, and escalates the organisational ones (incompatible org values, pressure culture, capability gap) to the coordinator/lead rather than coaching the team harder
- [ ] PASS: Cites concrete evidence for each symptom rather than asserting the diagnosis — e.g. "no increment shipped in four sprints, no stakeholder contact, three retros with zero changes"
- [ ] PARTIAL: Invokes the failure cap — the same dysfunction across three retros with no movement means stop coaching harder and escalate

## Output expectations

- [ ] PASS: Output is a structured anti-pattern audit with a Zombie Scrum symptom table, a Dark Scrum section, a retrospective-anti-pattern section, and a team-fixable-vs-organisational split
- [ ] PASS: The Zombie Scrum table marks all four symptoms present with the specific supplied evidence in each row
- [ ] PASS: Output names specific catalogue items from Corry's retrospective anti-patterns (at least Wheel of Fortune and one of Status theatre / Blame circles), not invented labels
- [ ] PASS: Output's Dark Scrum finding ties the dysfunction to a missing technical foundation and routes it to the CTO / engineering leadership
- [ ] PASS: Output clearly separates what the coach can fix at the team level from what must be escalated, and states the escalation target (coordinator / lead)
- [ ] PARTIAL: Output states the failure cap explicitly — three retros, no movement → escalate rather than grind harder
