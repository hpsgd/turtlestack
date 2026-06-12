# Test: write-dependency-map captures both directions, names contacts, finds critical chains

Scenario: A delivery manager maps the cross-team dependencies for a multi-team programme. The facts include both
upstream and downstream dependencies, one blocked dependency that gates two downstream teams (a critical chain),
and a dependency given only as a team name (must be pushed to a named contact). The skill must build the team-level
and programme-level views, apply escalation triggers, and surface the critical chain.

## Prompt

Use the delivery-manager `write-dependency-map` skill to build the dependency map for the "payments" programme.
Write the map to `docs/delivery/dependency-map.md` relative to the current working directory. Respond in the skill's
standard output format.

Facts:

- The checkout team needs the Payments API v2 migration from the Platform team (contact: Dani Roberts) before it can
  ship. It is currently blocked. Needed by 30 June.
- BOTH the checkout team AND the reporting team depend on that same Payments API v2 migration — if it is late, both
  stall.
- The billing team needs a finalised data schema from the checkout team (downstream of checkout) by 5 July;
  checkout's contact is Sam Okafor. On track.
- The fraud team needs single sign-on from the Identity team. The only detail given is "Identity team will handle
  it" — no named person, due 15 July.

Proceed without asking — map both directions and apply the escalation triggers.

## Criteria

- [ ] PASS: Captures both directions — upstream (what a team needs from others) and downstream (what others need from a team), e.g. the billing team's need from checkout is recorded as a downstream dependency of checkout
- [ ] PASS: Each dependency carries a named contact (a person such as Dani Roberts / Sam Okafor), not just a team name — and the SSO dependency is flagged as needing a named contact because "the Identity team" cannot be chased
- [ ] PASS: The Payments API v2 migration is marked Blocked and the escalation trigger fires — escalate to the coordinator / relevant lead now, not just notify
- [ ] PASS: Identifies the critical chain — the single Payments API v2 dependency blocking BOTH checkout and reporting — and escalates it to programme level because one dependency stalls 2+ downstream teams
- [ ] PASS: Records the needed-by date as when the dependent team actually needs it, and applies the "needed-by inside two weeks and not on track" trigger where relevant
- [ ] PASS: Produces both a team-level view and a programme-level view (which team blocks which) — not a single flat list
- [ ] PARTIAL: Notes the map must stay live (updated weekly / on change) and cross-references the RAID log where the same dependency is governed

## Output expectations

- [ ] PASS: A `docs/delivery/dependency-map.md` file is written with a team-level table and a programme-level table
- [ ] PASS: The Payments API v2 row shows status Blocked, a named contact, the 30 June needed-by date, and an escalation action
- [ ] PASS: A critical-chains section names the Payments API v2 dependency as blocking two downstream teams (checkout and reporting)
- [ ] PASS: The SSO dependency is flagged as missing a named contact — "Identity team" is called out as insufficient
- [ ] PASS: An escalations-triggered section lists the blocked dependency routed to the coordinator / lead with a by-when
- [ ] PARTIAL: Both upstream and downstream directions are visible in the team-level view rather than upstream only
