# Test: write-product-strategy takes a position with Cagan focus, not a generic plan

Scenario: The CPO is asked to write a product strategy for a single product with one broadly understood
market. The skill must pick a format and justify the choice — defaulting to Cagan/SVPG for a single product
rather than reaching for the Playing-to-Win cascade — and then take a real position: name the few specific
problems it will solve, AND write the deliberate "not doing" list (the hardest, most valuable section),
drive each bet from an insight rather than opinion, and avoid producing a roadmap or an aspiration dressed
as a strategy. A generic "improve onboarding, grow revenue, delight users" plan must not score well.

## Prompt

Use the cpo `write-product-strategy` skill to write a product strategy for "Tideline", an existing
appointment-and-records product for solo and very small allied-health clinics. It is one product in one
broadly understood market (Australian allied-health micro-practices). The vision already exists: help these
clinics run without a back office. Today the product handles bookings well but clinicians still chase
no-shows manually and do their compliance notes in a separate tool. Discovery shows no-shows are the number
one cause of lost revenue for these practices, and that switching cost from their current spreadsheet is the
biggest barrier to adoption.

Write the strategy artifact to `docs/strategy/product-strategy-tideline.md` (a relative path under the
current working directory). Respond in the skill's standard format. Proceed without asking.

## Criteria

- [ ] PASS: Picks a format explicitly and justifies it in one sentence — defaults to Cagan/SVPG for this single product / single market, and does NOT reach for the Playing-to-Win cascade where "where to play" is not open
- [ ] PASS: Reads/links the existing vision and frames the strategy as the plan to close the gap between today and the vision, not a blank-slate plan
- [ ] PASS: Names a few specific problems to solve (typically two to four) — each a customer or business problem (e.g. no-shows, compliance-notes friction), NOT a feature or initiative
- [ ] PASS: Each chosen problem is driven from the supplied insight/evidence (no-shows = #1 revenue loss; switching cost = top adoption barrier), not from opinion or gut feel
- [ ] PASS: Writes an explicit "what we are deliberately NOT doing" section listing tempting problems being said no to this period, with reasons — present and substantive, not an afterthought
- [ ] PASS: Provides a focus rationale explaining why these problems, in this order, this period — tied to discovery/market/technology, not just listed
- [ ] PASS: States a refresh cadence (no less than quarterly) and what would trigger an earlier refresh
- [ ] PASS: Takes a real position — the strategy is opinionated and specific to Tideline's situation, not a generic "improve onboarding / grow revenue / delight customers" plan applicable to any product
- [ ] PASS: Does NOT produce a roadmap or dated feature/sprint list in place of strategy, and does not let an aspiration ("become the market leader", "reach $X") pose as the strategy
- [ ] PASS: Runs the bad-strategy self-check (fluff / facing the challenge / goals-as-strategy / disconnected objectives) and points to `/cpo:diagnose-strategy` as the mandatory follow-up
- [ ] PASS: Connects to execution — names downstream owners (PM → PRD/roadmap, engineering → delivery) and ties bets to OKRs

## Output expectations

- [ ] PASS: Output writes the strategy file to `docs/strategy/product-strategy-tideline.md` under the working directory, with the chosen format declared and the "deliberately not doing" section present as a named heading
- [ ] PASS: The written strategy is concrete to Tideline (no-shows, compliance notes, switching cost) and reads as a set of focused bets with rationale — demonstrating the take-a-position bar rather than a generic template fill
