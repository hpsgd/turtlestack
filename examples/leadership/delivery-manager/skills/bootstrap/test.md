# Test: bootstrap creates the delivery documentation structure idempotently

Scenario: A delivery manager bootstraps the delivery documentation structure for a new programme. The skill must
create `docs/delivery/` with the living artifacts (RAID log, dependency map, status report) from templates, write the
delivery-manager fragment that names the delivery boundaries, detect the delivery shape, and stay idempotent — never
overwriting existing living artifacts. The delivery manager never writes `docs/delivery/CLAUDE.md` directly; the
coordinator assembles it from the fragments in `_sections/`.

## Prompt

Use the delivery-manager `bootstrap` skill to set up the delivery documentation structure for the "payments"
programme. It is a multi-team, continuous-flow product delivery (not GDS-phased). Create everything under
`docs/delivery/` relative to the current working directory. Respond in the skill's standard output format.

Proceed without asking — create the structure and report what was created.

## Criteria

- [ ] PASS: Creates the `docs/delivery/` directory as the engagement root for delivery artifacts, with a `_sections/` subdirectory for the domain fragment
- [ ] PASS: Writes `docs/delivery/_sections/delivery-manager.md` that states what the delivery domain covers AND what it does NOT cover (team process → agile coach, release gates → release-manager, backlog → product-owner, company risk → GRC Lead)
- [ ] PASS: The fragment is authored at H2 and below — it does not introduce a `# Delivery Domain` H1 (the coordinator generates that when it assembles `docs/delivery/CLAUDE.md`)
- [ ] PASS: The skill does NOT write `docs/delivery/CLAUDE.md` directly — that file is the coordinator's to assemble from `_sections/`
- [ ] PASS: Creates the RAID log, dependency map, and status report artifacts from templates — not empty placeholders
- [ ] PASS: Records the delivery shape — multiple teams (needs a programme-level RAID view) and continuous flow (not GDS-phased, so no service-assessment emphasis)
- [ ] PASS: States the bootstrap is idempotent — running it again merges missing sections rather than overwriting living artifacts
- [ ] PASS: The fragment or output records the delivery conventions: every RAID item has a named owner, red means "will not meet target without intervention", amber/red carry a road to green
- [ ] PARTIAL: Does NOT create release-engineering files (release checklists, rollback plans) — those belong to the release-manager's bootstrap

## Output expectations

- [ ] PASS: Output reports files created (_sections/delivery-manager.md, raid-log, dependency-map, status-report) under `docs/delivery/`
- [ ] PASS: Output reports the detected delivery shape — multiple streams + continuous (not GDS-phased)
- [ ] PASS: A `docs/delivery/_sections/delivery-manager.md` fragment is actually written to disk and names both what the domain covers and what it does not (the boundary to coach / release-manager / product-owner / GRC)
- [ ] PASS: At least the RAID log and status report artifacts exist on disk under `docs/delivery/` after the run — not just described in chat
- [ ] PARTIAL: Output's next-steps point at write-raid-log and write-status-report rather than leaving the structure empty
