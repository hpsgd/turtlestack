# Test: assess-team-topology classifies type, interaction modes, and cognitive load

Scenario: A team's purpose is muddy and its dependencies are tangled — it owns a layer rather than a slice and is stuck in permanent collaboration with another team. The coach must classify the team against the four Team Topologies types, identify the interaction modes, name the component-team smell, read cognitive load, and keep the recommendation advisory.

## Prompt

Use the agile-coach `assess-team-topology` skill to assess the "billing-platform" team. Context: this team owns the payments-and-ledger backend layer but no user-facing slice — every customer-facing feature requires it to coordinate constantly with two product teams to ship anything. It is permanently entangled in close back-and-forth with the "checkout" team for almost every release. It also supports five other teams that consume its APIs while still building new ledger features, and nothing seems to finish. Produce the topology assessment in the skill's standard format. Write the output to `docs/coaching/` in the current working directory.

Proceed without asking — produce the assessment.

## Criteria

- [ ] PASS: Classifies the team against the four Team Topologies types by name (stream-aligned, platform, enabling, complicated-subsystem) and reaches a defensible primary type
- [ ] PASS: Names the component-team-masquerading-as-stream-aligned smell — owning a layer not a slice, forcing cross-team coordination to ship anything user-facing
- [ ] PASS: Classifies the interaction modes by name (collaboration, X-as-a-Service, facilitating) for the team's significant relationships
- [ ] PASS: Identifies the permanent collaboration with the checkout team as the wrong mode — collaboration is expensive and time-bounded; this relationship should likely be X-as-a-Service
- [ ] PASS: Reads cognitive load explicitly and flags the team as overloaded (five consumers plus new feature work, nothing finishing) with the supplied evidence
- [ ] PASS: Keeps the recommendation advisory — the topology/restructuring decision belongs to the coordinator and leads, not the coach
- [ ] PARTIAL: Notes when this lens does NOT apply — a process/safety problem is not a topology problem — to avoid misdiagnosing

## Output expectations

- [ ] PASS: Output is a structured topology assessment with the team type, the interaction-mode table, a cognitive-load read, and advisory recommendations
- [ ] PASS: Output names the component-team smell with the layer-not-a-slice evidence rather than accepting the "platform" or "stream-aligned" label at face value
- [ ] PASS: The interaction-mode table flags the checkout-team collaboration as a mode that should change (toward X-as-a-Service) with the friction noted
- [ ] PASS: Output's cognitive-load read concludes overloaded and cites the five consumers plus concurrent feature work
- [ ] PASS: Output frames every recommendation as advisory to the coordinator/leads, not as a restructuring the coach will perform
- [ ] PARTIAL: Output reads as genuinely using the Team Topologies model (correct vocabulary and the collaboration-is-expensive insight), not a generic team review
