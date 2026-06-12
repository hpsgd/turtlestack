# Test: Coach a backlog refinement event

Scenario: A product owner runs a live refinement event over a groomed candidate queue for a 5-developer two-week sprint. The queue contains a clean story, an over-large story that must be split by behaviour, a story that depends on the over-large one, a story with a non-atomic acceptance criterion and an external legal blocker, and a second clean story. The skill must set a 10% capacity budget, INVEST-check each item, surface dependencies, gate against the Definition of Ready, and produce a clean Ready / back-to-refinement / Blocked split.

## Prompt

The groomed candidate queue for the Sprint 14 refinement event is on disk at `{workspace}/work/groomed-queue.md`. Read it.

/product-owner:coach-refinement {workspace}/work/groomed-queue.md

Run the full refinement event. Set the capacity budget first (the team is 5 developers on a two-week sprint), INVEST-check every candidate, surface dependencies, run the Definition of Ready gate on each, and produce the event summary using the skill's Output Format. Write the summary back to the backlog file at the path above and reply with that path.

## Criteria

- [ ] PASS: Sets a capacity budget before refining — states team sprint capacity in developer-hours and a refinement budget of ~10% of that capacity, with items-in-scope derived from it
- [ ] PASS: INVEST-checks every candidate item with explicit pass/fail per criterion (I/N/V/E/S/T) and a one-line reason, not a blanket "looks fine"
- [ ] PASS: Flags the "Account settings overhaul" item as failing Small and splits it by user behaviour (e.g. profile / notifications / billing / security as separate stories), never by technical layer
- [ ] PASS: Surfaces that "Show last-login timestamp" depends on the security tab from the overhaul item — and sequences or reclassifies it rather than passing it as Ready
- [ ] PASS: Reclassifies the "Export account data" item as Blocked (external legal sign-off on the field list) — not Ready — with owner and impact named
- [ ] PASS: Runs a Definition of Ready gate per item and only declares Ready the items that pass every box — "mostly ready" is not Ready
- [ ] PASS: Catches the non-atomic acceptance criterion on the export item ("PDF AND CSV AND email" smuggles multiple criteria into one) against the ISC splitting test
- [ ] PASS: The two clean stories (password reset, TOTP 2FA) pass INVEST and DoR and leave the event Ready for planning
- [ ] PASS: Does not re-prioritise the items against the roadmap during the event — readiness only, not re-ranking
- [ ] PARTIAL: Keeps the agile-coach's ceremony-health lens distinct from the PO's readiness call — notes ceremony observations separately rather than conflating them

## Output expectations

- [ ] PASS: Output writes the refinement summary to the backlog file at the given path and reports that path — not only an inline chat answer
- [ ] PASS: Output's item-results table follows the skill format (Item | INVEST | Dependencies | DoR | Outcome) and assigns every candidate a clear Outcome (Ready / back to refinement / Blocked)
- [ ] PASS: Output produces a dependency map showing the last-login → security-tab/overhaul relationship and the export → legal-sign-off blocker, with any unblocked items marked as startable immediately
