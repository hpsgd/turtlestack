# Test: switch-interview reconstructs the timeline and codes the Moesta four forces

Scenario: A PM wants to understand a real B2B purchase. The skill must run a Moesta switch interview: pick a
real recent switch, reconstruct the timeline as a documentary (first thought → passive looking → active
looking → decision) with specifics, code the four forces (push, pull, anxiety, habit) from quotes, and
extract the demand-side insight including the real competition — not run an evaluative feature-feedback
interview.

## Prompt

Use the product-manager `switch-interview` skill to design a switch interview for "Dana, an ops lead at a
mid-market logistics firm who switched from a spreadsheet to our reconciliation product six weeks ago". Write
the interview design and force-coding structure to a file under `docs/product/` in the current working
directory, in the skill's standard format. Use plausible illustrative quotes to populate the timeline and
force coding.

Proceed without asking — produce the switch interview.

## Criteria

- [ ] PASS: Frames a real, recent, specific switch (Dana, spreadsheet → product, ~6 weeks ago) — not a hypothetical "people who might buy"
- [ ] PASS: Reconstructs the timeline as a documentary across the four moments: first thought, passive looking, active looking, the event/decision — with specifics (when, where, who else)
- [ ] PASS: Codes ALL FOUR Moesta forces by name — Push and Pull (drive the switch), Anxiety and Habit (resist it)
- [ ] PASS: Notes that the switch happens only when push + pull outweigh anxiety + habit
- [ ] PASS: Codes forces from quotes (the customer's words), not from the interviewer's interpretation/inference
- [ ] PASS: Reconstructs the decision moment with documentary specifics (what tipped them, what happened right before) rather than abstract feature evaluation
- [ ] PASS: Extracts the demand-side insight — the job hired for, the decisive anxiety, the habit overcome, and the real competition (often "do nothing" / the spreadsheet)
- [ ] PARTIAL: Distinguishes the switch interview (retrospective, post-purchase) from generative discovery (prospective)

## Output expectations

- [ ] PASS: Output file exists under `docs/product/` with a timeline table (first thought → passive → active → decision) and a four-force coding table
- [ ] PASS: All four forces (push, pull, anxiety, habit) are present and correctly classified as drivers vs resistors
- [ ] PASS: The force coding cites quotes rather than interviewer interpretation
- [ ] PASS: The demand-side insight names the job hired for, the decisive anxiety, and the real competition (e.g. the spreadsheet / status quo)
- [ ] PARTIAL: Output states the switch interview is retrospective, distinct from prospective generative discovery
