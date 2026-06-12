# Test: audit-ceremonies names ceremony anti-patterns with evidence

Scenario: A coach is asked to audit a team's ceremonies after a full sprint cycle. Observation notes and the last two retrospective outputs are on disk. The skill must observe across the cycle, name specific ceremony anti-patterns with cited evidence, record good signals too, distinguish symptom from cause, and prioritise coaching actions.

## Prompt

Use the agile-coach `audit-ceremonies` skill to audit the "billing" team's ceremonies. The observation notes for one full sprint cycle are at `docs/coaching/ceremony-notes.md` and the last two retrospective outputs are in `docs/coaching/retrospectives/` (relative to the current working directory). Read them and produce the ceremony audit in the skill's standard format. Write the audit to `docs/coaching/` in the current working directory.

Proceed without asking — read the records and produce the audit.

## Criteria

- [ ] PASS: Reads the supplied observation notes and retrospective records before naming anti-patterns — diagnoses from a full cycle, not a single event
- [ ] PASS: Names the status-theatre Daily Scrum anti-pattern, citing the evidence (each developer reports to the Scrum Master/PO, the repeated unaddressed staging-credentials blocker)
- [ ] PASS: Names the secretary-coach anti-pattern, citing that the team could not run the standup when the Scrum Master was away
- [ ] PASS: Names the task-assignment and no-Sprint-Goal planning anti-patterns, citing the pre-assigned tickets and the three different answers to "what's the goal?"
- [ ] PASS: Names the demo-theatre review anti-pattern, citing screenshots-not-running-software and the unchanged backlog
- [ ] PASS: Names the retrospective Wheel-of-Fortune / status-theatre anti-patterns, citing the data-straight-to-action jump and the identical ownerless action items across retros
- [ ] PASS: Records at least one good signal as well as the failures (what to reinforce), not a failures-only list
- [ ] PASS: Distinguishes symptom from cause — groups the anti-patterns under a likely shared root (the team has never been coached to self-manage) rather than listing them flat
- [ ] PARTIAL: Prioritises coaching actions with self-management and safety before format polish, mapping each priority to a skill

## Output expectations

- [ ] PASS: Output is a structured ceremony-audit artifact with an anti-patterns table (event / anti-pattern / evidence / likely root cause), a root-cause grouping, and prioritised coaching actions
- [ ] PASS: Every named anti-pattern cites concrete evidence from the supplied records (which event, what was observed) — no bare "status-theatre standup" without the supporting observation
- [ ] PASS: Output applies the self-management test — would the team run every event if the coach went on leave — and answers it using the standup-skipped-when-SM-away evidence
- [ ] PASS: Output diagnoses the system, not individuals — "the standup is a status report" rather than naming a person as the problem
- [ ] PASS: Output's prioritised actions map each fix to the skill that addresses it (e.g. facilitate-retrospective, facilitate-sprint-planning) and put self-management/safety ahead of format
- [ ] PARTIAL: Output flags the recurring identical action items across retros as the strongest evidence the insight phase is being skipped
