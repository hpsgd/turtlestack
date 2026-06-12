---
# The delivery-manager agent declares model: sonnet in
# plugins/leadership/delivery-manager/agents/delivery-manager.md. Run it on sonnet so the
# test exercises the model the agent is designed for, not the harness Haiku default.
target-model: claude-sonnet-4-6
---

# Test: delivery-manager shepherds a troubled multi-team delivery honestly

Scenario: A delivery manager is handed a delivery that is reporting green to its steering committee while the
RAID log and the actual state say otherwise — a blocked cross-team dependency, a stalled high/high risk, and a
date the team committed to under pressure. The delivery manager must hold its boundaries (not coach the team, not
execute the release), report honestly, apply reference-class thinking to the date, and route impediments to the
right owners — responding in its standard delivery methodology and structured deliverable format.

## Prompt

Use the `delivery-manager` agent to work the following situation, and respond in its standard delivery methodology
and structured deliverable format.

The "payments" programme has two teams (billing and checkout). For the last three weekly status reports it has been
reported Green to the steering committee. But: the checkout team is blocked waiting on a Payments API v2 migration
owned by a separate Platform team (no contact for two weeks); a high-probability, high-impact risk about an
unconfirmed integration environment has sat amber with no action for three weekly reviews; and the programme has
just committed to a "go-live in 6 weeks" date that the billing team's lead set under pressure from the CPO. The
last two comparable rebuilds in this org took 60% and 50% longer than their original estimates. The team also wants
you to run their next retrospective and to make the go/no-go call on the release yourself.

Work the problem as the delivery manager. Do not ask me clarifying questions first — proceed with what you'd do,
stating any assumptions.

## Criteria

- [ ] PASS: Flags the Green-to-steering reporting as watermelon reporting given the blocked dependency and stalled risk — states the honest colour should be Red (or at least Amber), not Green
- [ ] PASS: Treats the blocked Payments API v2 dependency as the largest slippage driver — names it needs a contact at the Platform team and an escalation now, not a team name
- [ ] PASS: Identifies the amber-for-three-reviews high/high risk as item rot / RAG kabuki and forces it out of "managed" status with an escalation rather than leaving it
- [ ] PASS: Applies reference-class forecasting to the 6-week date — uses the two comparable rebuilds (60% / 50% over) as an outside-view reference class and produces a corrected forecast longer than 6 weeks, rather than accepting the pressured bottoms-up date
- [ ] PASS: Declines to run the retrospective — routes it to the agile coach as a team-internal ceremony, not something the delivery manager facilitates
- [ ] PASS: Declines to make the release go/no-go call — coordinates readiness up to the gate and hands a package to the release-manager, who owns go/no-go, deployment, and rollback
- [ ] PASS: Routes the pressured-date / CPO conflict to the right escalation path (coordinator, or back to the CPO with the reference-class evidence) rather than silently absorbing the commitment
- [ ] PARTIAL: Attaches a road-to-green to any amber/red item rather than just reporting the colour — names actions, owners, and dates

## Output expectations

- [ ] PASS: Output is a structured delivery artifact (Summary with RAG / RAID or status detail / Decisions needed / Help asked for) rather than loose prose
- [ ] PASS: Output's overall RAG is honest (Red or Amber, not Green) and the four status components are present — what happened, what is at risk, what decisions are needed, what help is asked for
- [ ] PASS: Output names the blocked dependency with an owner/contact, a status, and an escalation, not as "the Platform team will sort it"
- [ ] PASS: Output presents both numbers for the date — the 6-week bottoms-up estimate and a longer reference-class forecast derived from the two comparable deliveries — and recommends committing to the corrected figure
- [ ] PASS: Output explicitly states what the delivery manager does NOT do here — does not run the retro (agile coach) and does not own go/no-go (release-manager)
- [ ] PASS: Output routes each impediment to a named owner and a named escalation path, distinguishing team-internal (coach) from organisational/cross-team (delivery manager / coordinator)
- [ ] PARTIAL: Output surfaces the cultural condition behind three Green reports (red is unsafe to report) and routes making-red-safe to leadership rather than blaming the team
