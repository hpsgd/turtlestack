# Test: write-status-report builds the four components from evidence with honest RAG

Scenario: A delivery manager writes the weekly status from real evidence — a RAID log with a blocked dependency and
an open blocking issue, plus a dependency map showing the same blocked item gating two teams. The honest read is
not Green. The skill must build the four status components from the evidence (not from a feeling), assign an honest
RAG, and attach a road to green for every amber/red item.

## Prompt

Use the delivery-manager `write-status-report` skill to write the weekly delivery status report for the "payments"
programme for the week ending 2026-06-13. The evidence is on disk: the RAID log at `docs/delivery/raid-log.md` and
the dependency map at `docs/delivery/dependency-map.md`, both relative to the current working directory. Write the
report to `docs/delivery/status-report.md`. Respond in the skill's standard output format.

Proceed without asking — read the evidence, then write the report.

## Criteria

- [ ] PASS: Reads the RAID log and dependency map as evidence before writing — the report is built from the on-disk artifacts, not from a generic sense of progress
- [ ] PASS: Assigns an honest overall RAG that is NOT Green — given a Blocked dependency (D-001) and an open blocking issue (I-002), the colour is Red or Amber with the reasoning stated
- [ ] PASS: Includes all four components — what happened (specific, not "good progress"), what is at risk (named with owner and action, pulled from the RAID), what decisions are needed, what help is asked for
- [ ] PASS: The "what is at risk" section names items with owners and actions and cites RAID IDs (R-001, I-002, D-001) rather than just listing colours
- [ ] PASS: Attaches a road-to-green table for the amber/red items — actions with owners and by-when dates that move the status, not just a diagnosis of the colour
- [ ] PASS: Names at least one decision needed and/or help asked for with a person and a consequence — the report is not passive description only
- [ ] PARTIAL: Flags that reporting Green here would be watermelon reporting given the blocked dependency, reinforcing the honest colour

## Output expectations

- [ ] PASS: A `docs/delivery/status-report.md` file is written with an explicit overall RAG that is Red or Amber (not Green)
- [ ] PASS: The four components are present as distinct sections — what happened / what is at risk / decisions needed / help asked for
- [ ] PASS: The "what is at risk" content references the blocked Payments API v2 dependency and the open reconciliation issue with named owners, not bare colours
- [ ] PASS: A road-to-green section lists at least one action with an owner and a by-when date for an amber/red item
- [ ] PASS: At least one named decision or help-ask appears with a consequence if not actioned — proving the report is not a passive read-out
- [ ] PARTIAL: "What happened this week" is specific (named completed work / findings) rather than "good progress on payments"
