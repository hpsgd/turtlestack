# Test: coach-kanban-method coaches the six practices for an ops team

Scenario: A support/operations team is being forced into two-week sprints that don't fit its irregular, interrupt-driven work. The coach must confirm Kanban fits the work, coach the six Kanban practices in the right order, set first WIP limits below current, make the interrupt policy explicit, and name the Scrumban hybrid and its risk where relevant.

## Prompt

Use the agile-coach `coach-kanban-method` skill to coach the "billing-support" team. Context: this team handles incoming production support and billing-incident tickets — work arrives irregularly and unpredictably, and urgent issues constantly preempt planned work. They've been told to run two-week Scrum sprints, which keep getting blown up by interrupts. Coach them on the right method and produce the output in the skill's standard format. Write the output to `docs/coaching/` in the current working directory.

Proceed without asking — produce the Kanban coaching output.

## Criteria

- [ ] PASS: Confirms Kanban fits this work and explains why Scrum fits poorly for irregular, interrupt-driven operations/support work — rather than introducing Kanban by default
- [ ] PASS: Coaches all six Kanban Method practices by name — visualise, limit WIP, manage flow, make policies explicit, implement feedback loops, improve/evolve experimentally
- [ ] PASS: Coaches visualisation first and explains everything else depends on seeing the work
- [ ] PASS: Sets first WIP limits slightly below current WIP so the team feels the pull effect, and states that an unenforced WIP limit is decoration
- [ ] PASS: Makes the interrupt policy explicit — what classes of work jump the queue, who decides, what WIP is reserved for interrupts — given this is an ops/support team
- [ ] PASS: Explains the pull-system mechanism — limiting WIP converts a push system (start work whenever) to a pull system (start only when there's capacity)
- [ ] PARTIAL: Names Scrumban and its risk (losing the discipline of both methods) where the team needs both a cadence and pull

## Output expectations

- [ ] PASS: Output is a structured Kanban-coaching artifact with a fit judgement, the six practices with current-state and coaching action, the WIP limits set, and the interrupt policy
- [ ] PASS: The fit judgement explicitly says Kanban fits because the work is irregular/interrupt-driven and Scrum's fixed sprint pressures this work, not a generic "Kanban is good"
- [ ] PASS: The six-practices section addresses all six, with visualisation coached before WIP limits
- [ ] PASS: Output includes a concrete interrupt policy section (not N/A) appropriate to a support team
- [ ] PASS: The WIP-limits section sets initial limits below current WIP and notes enforcement is what makes the pull effect real
- [ ] PARTIAL: Output evolves experimentally — recommends changing one thing at a time and measuring, rather than redesigning the whole board at once
