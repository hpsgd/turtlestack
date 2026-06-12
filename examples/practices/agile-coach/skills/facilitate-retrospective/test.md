# Test: facilitate-retrospective runs the five phases with a safety frame

Scenario: A coach is asked to design and facilitate a retrospective for a team after a rough sprint that included a production incident. The skill must apply Derby & Larsen's five phases, open with a safety frame, assess psychological safety, pick a fitting format, and produce an output file with action items routed into the next sprint backlog.

## Prompt

Use the agile-coach `facilitate-retrospective` skill to design and facilitate a retrospective for the "billing" team. Context: the sprint just ended with a production incident (a failed payment-reconciliation deploy), morale is low, and a couple of people seem reluctant to speak openly. Write the retrospective output file to `docs/coaching/retrospectives/` in the current working directory. Respond in the skill's standard format — the retro plan plus the output file.

Proceed without asking — design the retro and produce the plan and output artifact.

## Criteria

- [ ] PASS: Applies Esther Derby & Diana Larsen's five phases by name — Set the Stage, Gather Data, Generate Insights, Decide What to Do, Close the Retrospective
- [ ] PASS: Opens Set the Stage with Norm Kerth's Prime Directive (or an explicit safety frame stating everyone did their best given what they knew) as the safety baseline
- [ ] PASS: Assesses psychological safety before choosing the format (e.g. a 1-5 safety read) given the low-morale, reluctant-to-speak context
- [ ] PASS: Selects a specific retrospective format and justifies why it fits this moment (incident + low safety) — not the same format by rote
- [ ] PASS: Includes the Generate Insights phase explicitly and warns that skipping it (data straight to action) is the Wheel of Fortune anti-pattern that fixes symptoms
- [ ] PASS: Produces action items that are routed into the next sprint backlog, each with a named owner and a due sprint — not assigned to "the team" and not left undated
- [ ] PASS: Uses a technique to counter dominance by one voice (silent writing, dot voting, or 1-2-4-All) so the reluctant members contribute
- [ ] PARTIAL: Separates items inside the team's control from items outside it (the "In the Soup" anti-pattern), routing the external ones to the delivery manager

## Output expectations

- [ ] PASS: Output writes a retrospective file under `docs/coaching/retrospectives/` with frontmatter (title, date, author: agile-coach) and a structured body
- [ ] PASS: The output file contains a distinct action-items section formatted as a table with Action / Owner / Due sprint / Backlog item columns — not a flat bullet list with no owners
- [ ] PASS: The five Derby/Larsen phases are visible in the plan or output as named sections, not collapsed into a generic "we'll talk about the sprint"
- [ ] PASS: A safety read (1-5 or equivalent) and the chosen format with its rationale both appear in the output
- [ ] PASS: At least one action item has a concrete owner and a due sprint, demonstrating the route-to-backlog rule rather than a parking lot
- [ ] PARTIAL: Output includes a facilitator note flagging any recurring item carried from a prior retro (the recurring-action watch)
