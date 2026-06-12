# Test: write-raid-log classifies four items correctly and enforces ownership

Scenario: A delivery manager is handed four raw delivery facts that must be classified into the correct RAID
categories and structured for action. One is phrased as an outcome (must be rewritten as a cause), one has no
nameable owner (must be blocked from logging), one is an external dependency, and one is a live issue. The skill
must place each in the right category, apply the per-category shape, and enforce a named owner per item.

## Prompt

Use the delivery-manager `write-raid-log` skill to capture the following four items for the "payments" delivery.
Write the RAID log to `docs/delivery/raid-log.md` relative to the current working directory. Respond in the skill's
standard output format.

1. "The project will be delayed if the supplier doesn't confirm the integration environment date." The supplier is
   chased by Sam Okafor, our integration lead.
2. We believe Legal will sign off the data-sharing agreement within two weeks. Nobody has confirmed this with Legal
   yet; Priya Nandan would be the one to check.
3. The checkout team needs the Payments API v2 migration before it can finish — that work is owned by the separate
   Platform team. Our contact there is Dani Roberts. We need it by 30 June and it is looking shaky.
4. The staging environment has been down for two days and is blocking acceptance testing right now. Owner is Sam
   Okafor; DevOps is rebuilding it.

Proceed without asking — classify, structure, and log each item.

## Criteria

- [ ] PASS: Item 1 is logged as a Risk, and the outcome phrasing ("the project will be delayed") is rewritten as the cause ("supplier has not confirmed the integration environment date") — not logged verbatim as an outcome
- [ ] PASS: The Item 1 risk is structured as cause → impact → probability → mitigation, with probability and impact each rated (High/Medium/Low) and a review date — not a bare sentence
- [ ] PASS: Item 2 is logged as an Assumption with a validation owner (Priya Nandan) and a validate-by date, and is flagged as also a dependency on Legal (cross-reference) since it relies on an external party
- [ ] PASS: Item 3 is logged as a Dependency with the owning team (Platform), a named contact (Dani Roberts, not "the Platform team"), a status (At risk), and the needed-by date (30 June)
- [ ] PASS: Item 4 is logged as an Issue (already happening) with an impact, a resolution plan, and an escalation date within 48 hours — not as a risk
- [ ] PASS: Every logged item carries a named owner (a person), and the skill states that "the team" is not an acceptable owner
- [ ] PASS: IDs follow the per-category sequence (R-, A-, I-, D-) so the log can grow without collisions
- [ ] PARTIAL: The output distinguishes the four categories as genuinely different (risk = not happened yet / issue = already harming / dependency = controlled by another team / assumption = believed unconfirmed) rather than dumping all four into one list

## Output expectations

- [ ] PASS: A `docs/delivery/raid-log.md` file is written with four separate tables (Risks, Assumptions, Issues, Dependencies), each item in its correct table
- [ ] PASS: The risk row shows distinct cause, impact, probability, and mitigation columns — the cause is the unconfirmed environment date, NOT "the project will be delayed"
- [ ] PASS: The dependency row names Dani Roberts as the contact and 30 June as the needed-by date, with status At risk
- [ ] PASS: The issue row carries an escalation date within 48 hours, marking it as a blocking issue
- [ ] PASS: The assumption row has a validation owner and a validate-by date, with a cross-reference noting it is also a Legal dependency
- [ ] PARTIAL: The output summary lists each item with its category, owner, and key date, and flags any item that could not be logged for want of an owner
