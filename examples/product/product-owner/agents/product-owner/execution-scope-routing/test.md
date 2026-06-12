---
# The product-owner agent declares model: sonnet in
# plugins/product/product-owner/agents/product-owner.md. Pin it so the runner
# doesn't fall back to the harness default (Haiku).
target-model: claude-sonnet-4-6
---

# Test: Execution scope and upstream routing

Scenario: A stakeholder asks the product owner to do two things at once. First, the upstream why/what — "write the PRD and decide where this sits on the roadmap" for a brand-new feature idea with no validated problem behind it. Second, the downstream execution — turn an already-approved PRD slice into sprint-ready stories. The rescoped product-owner is EXECUTION-focused: it must route the PRD/roadmap/discovery work UPSTREAM to the product-manager (refusing to author it itself) while doing the backlog/story/acceptance-criteria work it owns.

## Prompt

Use the product-owner agent to handle this. I have two things for you.

First: I've had an idea for a "team activity feed" — a social timeline showing what teammates are doing in the product. I don't have any customer research or a problem statement yet, but I'd like you to write the PRD for it and tell me where it should sit on our roadmap relative to our other Q3 themes.

Second: the "saved filters" feature already has an approved PRD (PRD `saved-filters`, state: Approved, success metric: cut repeat-search time 30%). The approved scope is: a user can save the current filter set with a name, see their saved filters in a list, apply a saved filter in one click, and delete a saved filter. Please turn that approved slice into sprint-ready user stories with acceptance criteria.

## Criteria

- [ ] PASS: Declines to author the "team activity feed" PRD itself — routes PRD authoring upstream to the product-manager rather than writing the PRD
- [ ] PASS: Declines to place the feature on the roadmap / re-rank Q3 themes — identifies roadmap ownership as the product-manager's, not the product-owner's
- [ ] PASS: Flags that the team activity feed has no validated problem / no research, so it is not ready to decompose — discovery is upstream work, not the PO's to invent
- [ ] PASS: Proceeds with the "saved filters" work because it has an Approved PRD — distinguishing approved intent (decomposable) from an unvalidated idea (not)
- [ ] PASS: Decomposes the approved saved-filters slice into user stories split by user behaviour (save / list / apply / delete), not by technical layer
- [ ] PASS: Writes acceptance criteria that are atomic and independently verifiable (ISC), not criteria smuggling multiple checks into one
- [ ] PASS: The two requests get different treatment — one routed upstream, one executed — rather than the agent attempting both or refusing both
- [ ] PARTIAL: Names the product-manager explicitly as the owner of the why/what (PRD, roadmap, discovery) when routing the first request upstream

## Output expectations

- [ ] PASS: Output does NOT contain an authored PRD for the team activity feed (no problem statement it invented, no success metrics it made up, no roadmap placement) — it routes that to the product-manager instead
- [ ] PASS: Output produces sprint-ready stories for saved filters in the As-a / I-want / So-that form with ISC acceptance criteria, traced to the approved PRD
- [ ] PASS: Output frames the split cleanly: the activity-feed request is upstream/not-ready (escalated to the product-manager), the saved-filters request is downstream/ready-to-execute (delivered)
