# Test: write-narrative builds a Raskin change / enemy / promised-land / magic / proof arc from positioning

Scenario: GTM is given an existing positioning (staged on disk) and asked to write the strategic narrative.
The skill must ground in that positioning and build the five Andy Raskin moves IN ORDER — name the big
external change, name the stakes (the enemy = the old way, never a named competitor), paint the promised
land as the buyer's future, then and only then introduce the product as the magic with proof. The product
must arrive late, the protagonist must be the buyer, and the skill must pressure-test the arc. A template
fill that names a change nobody feels, or pitches the product up front, must not score well.

## Prompt

A positioning document already exists at `docs/gtm/positioning.md` (relative to your current working
directory) — read it first. Then use the gtm `write-narrative` skill to write the strategic narrative for
"Tideline" from that positioning, for use as the opening of a launch keynote.

Write the narrative artifact to `docs/gtm/narrative-tideline.md` (a relative path under the current working
directory). Respond in the skill's standard format. Proceed without asking.

## Criteria

- [ ] PASS: Grounds the narrative in the staged positioning (reads `docs/gtm/positioning.md`) — draws the change, old world, magic, and promised land from it rather than inventing differentiation
- [ ] PASS: Names a big, external, undeniable change as the opening move (rising allied-health demand vs flat clinician supply / rising regulatory admin floor / patient expectations of frictionless booking) — NOT a product announcement
- [ ] PASS: The change move does not mention the product — the product does not appear in move one
- [ ] PASS: Names the stakes / enemy as the OLD WAY (manual admin, the evenings lost, the spreadsheet juggle), explicitly NOT a named competitor — and makes the stakes concrete and asymmetric (winners pull ahead, laggards bleed no-shows)
- [ ] PASS: Paints a promised land described as the buyer's future outcomes (clinician spends the day on patients, evenings handed back, clinic runs itself), not a feature list, and hard enough to reach that help is needed
- [ ] PASS: Introduces the product LATE — only after change, stakes, and promised land — as the magic / capabilities that make the promised land reachable
- [ ] PASS: Maps each capability (one-login, no-show recovery, compliance-at-point-of-care, clinician-run) to a promised-land outcome and attaches proof (e.g. ~3 no-shows recovered/week, ~5 hours/week reclaimed)
- [ ] PASS: Makes the buyer (the solo practitioner) the protagonist of the story — it is their story, not the company's
- [ ] PASS: Writes the five moves as one continuous, speakable narrative in order — deliverable from a stage, not a bulleted essay
- [ ] PASS: Runs the pressure-test (change / enemy / promised-land / earned-product / ownership) and reports pass/fail per test rather than skipping it
- [ ] PASS: Labels the output DRAFT — requires human review and applies writing-style discipline (no obvious AI tells in the keynote prose)
- [ ] PASS: Has valid YAML frontmatter (name, description, argument-hint)

## Output expectations

- [ ] PASS: Output writes the narrative to `docs/gtm/narrative-tideline.md` under the working directory and restates the positioning root
- [ ] PASS: Output's first move is an external change with NO product mention; the product is introduced only after the promised land
- [ ] PASS: Output's enemy is the old way of operating (manual admin / the juggle), not a named rival company
- [ ] PASS: Output contains a continuous, speakable narrative section delivering the five moves in order, with the buyer as protagonist
- [ ] PASS: Output's magic+proof section maps capabilities to promised-land outcomes with specific proof, and the pressure-test table reports per-test results
