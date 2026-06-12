# Test: write-business-model-canvas argues viability, not just fills nine boxes

Scenario: The CPO maps a business model where the user and the payer differ — the classic load-bearing
trap. The skill must fill the nine Osterwalder blocks as a first pass, but the quality bar is the ARGUED
READ: it must trace whether revenue actually follows from value (and surface that the people who get the
value are not the people who pay), tag blocks known/assumed and honour the ratio, name exactly ONE riskiest
assumption as a falsifiable claim with the cheapest test to settle it, test the unit economics direction,
and end with a position on viability. A tidy nine-cell grid with no judgment must NOT score well.

## Prompt

Use the cpo `write-business-model-canvas` skill to map and pressure-test the business model for "Roster", a
proposed (not yet built) shift-scheduling app for hospitality venues. The intended model: the app is free
for hourly staff to view and swap shifts (the users), while venue owners/managers pay a per-venue monthly
subscription (the payers). Revenue is assumed to come from venue subscriptions; demand is largely
unvalidated — you are proposing this model, not auditing a running one. Acquisition is assumed to be
word-of-mouth from staff pulling their venue onto the platform.

Write the canvas artifact to `docs/strategy/business-model-canvas-roster.md` (a relative path under the
current working directory). Respond in the skill's standard format. Proceed without asking.

## Criteria

- [ ] PASS: Establishes context and maturity first — recognises this is a PROPOSED model (not an operating-model audit), so most blocks are assumptions
- [ ] PASS: Drafts all nine Osterwalder blocks as a first pass, each tagged `[known]` or `[assumed]`, and reports the known-to-assumed ratio as a finding (a mostly-assumed canvas is a hypothesis, not a business)
- [ ] PASS: Traces revenue back to value and EXPLICITLY surfaces the user-vs-payer split — staff get the value (free shift swapping) while venues pay — and states whether their interests align or conflict
- [ ] PASS: Pressure-tests the right side as a chain (segments→value→revenue, channels/relationships vs price point) with an argued paragraph per link, not a description, ending with the single weakest link on the right
- [ ] PASS: Pressure-tests the left side — value→activities/resources and partnership/concentration risk — and names the load-bearing resource/activity whose removal collapses the model
- [ ] PASS: Tests the economics — unit-economics direction (does revenue plausibly exceed cost to serve) and cost-structure shape (value-driven vs cost-driven), checking the blocks are internally consistent
- [ ] PASS: Names EXACTLY ONE riskiest assumption as a falsifiable claim (e.g. "venue managers will pay $X/month", or "staff word-of-mouth actually pulls venues onto the platform"), NOT a list of risks
- [ ] PASS: For the riskiest assumption, states what evidence would confirm or kill it AND the cheapest test that would produce that evidence
- [ ] PASS: Ends with an argued read that takes a POSITION on viability ("viable if and only if X holds"), willing to conclude the model bends or doesn't hold — not a neutral summary that all nine boxes are filled
- [ ] PASS: Decides whether the BMC was even the right tool — given a mostly-assumed, unvalidated proposed model, recommends switching to a Lean Canvas and names the risk as market risk (should we build this?) not operational risk
- [ ] PASS: Holds CPO ownership — frames the read as CPO-authored with PM supplying slice-level economic input

## Output expectations

- [ ] PASS: Output writes the canvas file to `docs/strategy/business-model-canvas-roster.md` under the working directory, with a one-line viability verdict up top, the nine-block table with known/assumed tags, and a distinct "Riskiest assumption" section
- [ ] PASS: The written file demonstrates the argue-not-box-tick bar — it names exactly one riskiest assumption as a falsifiable claim with a cheapest test, surfaces the user-vs-payer split, and ends with a position on viability rather than restating that all nine blocks are populated
