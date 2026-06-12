# Test: facilitate-sprint-planning coaches the team to author the Sprint Goal

Scenario: A coach facilitates Sprint Planning for a team that has historically over-committed and let the product owner hand out tasks. The skill must run the three Scrum Guide planning topics, coach the team (not write) the Sprint Goal, check capacity, and name the over-commitment and task-assignment anti-patterns.

## Prompt

Use the agile-coach `facilitate-sprint-planning` skill to facilitate Sprint Planning for the "billing" team's next sprint. Context: in the last three sprints the team finished roughly 18 points each but kept pulling in 28+ and carrying work over, and the product owner tends to assign specific tickets to specific people. Two developers are on leave this sprint. Write the planning output to `docs/coaching/` in the current working directory. Respond in the skill's standard format.

Proceed without asking — facilitate the planning and produce the output.

## Criteria

- [ ] PASS: Covers all three Sprint Planning topics from the 2020 Scrum Guide — why this sprint is valuable (the Sprint Goal), what can be done, and how the work gets done
- [ ] PASS: The coach facilitates the team to author the Sprint Goal and explicitly does NOT write the goal itself
- [ ] PASS: Names the over-commitment anti-pattern and coaches against it using the team's own throughput history (≈18 done vs 28+ pulled), not optimism
- [ ] PASS: Names the task-assignment anti-pattern — the product owner owns what/why, the developers own how/how-much — and redirects it
- [ ] PASS: Plans against actual capacity, accounting for the two developers on leave and ceremony overhead, not theoretical full-team capacity
- [ ] PASS: Uses the test that every developer can state the Sprint Goal from memory in their own words as the signal that planning produced a real goal, not a ticket list
- [ ] PARTIAL: Coaches story slicing for items too large to finish in the sprint rather than letting oversized items in

## Output expectations

- [ ] PASS: Output is a structured planning artifact with a team-authored Sprint Goal, a capacity section, the selected scope, and coaching notes — not loose prose
- [ ] PASS: The capacity section reflects the two developers on leave and adjusts the forecast accordingly
- [ ] PASS: The coaching notes name the observed anti-patterns (over-commitment and/or task-assignment) with the throughput evidence
- [ ] PASS: Output frames the Sprint Goal as team-authored and the forecast as developer-owned — it does not present a goal the coach wrote
- [ ] PARTIAL: Output flags the over-commitment risk concretely (e.g. "last three sprints you finished ~18; what makes this one different?") rather than a generic caution
