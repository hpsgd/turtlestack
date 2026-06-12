# Assess Team Topology

Scenario: A team's purpose is muddy and its dependencies are tangled — it owns a layer rather than a slice and is stuck in permanent collaboration with another team. The coach must classify the team against the four Team Topologies types, identify the interaction modes, name the component-team smell, read cognitive load, and keep the recommendation advisory.

## Prompt

> Use the agile-coach `assess-team-topology` skill to assess the "billing-platform" team. Context: this team owns the payments-and-ledger backend layer but no user-facing slice — every customer-facing feature requires it to coordinate constantly with two product teams to ship anything. It is permanently entangled in close back-and-forth with the "checkout" team for almost every release. It also supports five other teams that consume its APIs while still building new ledger features, and nothing seems to finish. Produce the topology assessment in the skill's standard format. Write the output to `docs/coaching/` in the current working directory.
> 
> Proceed without asking — produce the assessment.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Assessment complete. The billing-platform team is a **complicated-subsystem** (owns deep technical infrastructure) being treated as stream-aligned with support obligations — a structural mismatch causing the chronic friction. 

Key findings:
- **Primary problem:** Component-team topology (owning a layer, not a slice) forces permanent collaboration with checkout and other product teams. This isn't a process issue.
- **Cognitive overload:** Supporting 7 downstream teams + building new features simultaneously, with no separation between support and feature work.
- **Interaction-mode failure:** Relationships with checkout and product teams are stuck in expensive collaboration when they should be clean X-as-a-Service (stable APIs, independent consumption).

The assessment recommends the coordinator/leads decide the topology explicitly:
1. **Platform team model:** billing-platform owns the APIs; product teams consume independently (no ongoing collaboration)
2. **Complicated-subsystem model:** a product team owns end-to-end billing and treats billing-platform as a dependency
3. **Reduce cognitive load:** either dedicate support capacity, shift feature development out, or split the team

The assessment is written to `docs/coaching/billing-platform-topology-assessment.md` in the standard format. This is advisory for the leads — the reteaming decision is theirs.

### Artifacts written

#### `work/docs/coaching/billing-platform-topology-assessment.md`

```
---
title: Team Topology Assessment — billing-platform
date: 2026-06-12
author: agile-coach
category: Coaching
---

## Team type

- **Actual type:** Complicated-subsystem (payments and ledger backend) — specialized, technically deep work
- **Treated as:** Stream-aligned with support obligations
- **Component-team smell:** Yes. The team owns a technical layer (backend payment/ledger infrastructure) rather than an end-to-end user-facing product slice. Every customer-facing feature requires coordination across teams because the team's output is a dependency, not a complete flow.

## Interaction modes

| Relationship | Current mode | Should be | Friction |
|--------------|--------------|-----------|----------|
| Checkout team | Collaboration (close back-and-forth on almost every release) | X-as-a-Service (checkout consumes ledger APIs) | High — permanent entanglement, nothing finishes cleanly |
| Other product team | Collaboration (constant coordination for feature shipping) | X-as-a-Service (stable API contracts) | High — same entanglement pattern |
| 5 API-consuming teams | X-as-a-Service (nominal) | X-as-a-Service (with capacity to support) | Medium — support obligations compete with new feature work; teams may be blocked waiting for ledger API improvements |

## Cognitive load

- **Assessment:** Severely overloaded
- **Evidence:**
  - Supporting 7 downstream teams (checkout + 1 product team + 5 API consumers) while simultaneously building new ledger features
  - No clear separation between support obligations and new work — team context-switches constantly
  - Chronic inability to finish work ("nothing seems to finish")
  - Permanently entangled in close back-and-forth with checkout team — a collaboration relationship that should be transactional
  - Team is a dependency bottleneck for two product teams' release cycles

## Root cause

The topology mismatch: billing-platform is structured as a **component team** (owns a layer) but is being asked to behave as a **stream-aligned team** (ships features end-to-end). Component teams should not own support obligations — they should provide a clean, stable interface that other teams consume independently.

The permanent collaboration with checkout is a symptom. When a team owns a layer rather than a slice, every feature that crosses the boundary requires that two-team back-and-forth. This isn't a process problem; it's a structural one.

## Recommendations (advisory to coordinator / leads)

1. **Reclassify the team explicitly.** Decide: is billing-platform a **platform team** (providing payments/ledger infrastructure as a service to product teams) or a **complicated-subsystem team** (owning the deep technical work while a product team owns the customer interface)? The current state — neither clear structure, both expectations — is generating the friction.

   - If **platform team:** billing-platform owns the ledger and payment APIs; checkout and other product teams consume them independently via X-as-a-Service relationships. Team stops being involved in release cycles of downstream teams.
   - If **complicated-subsystem team:** a product team (e.g., checkout team or a dedicated billing product team) owns the end-to-end billing experience and treats billing-platform as a specialized subsystem they integrate. Billing-platform is not a peer; it's a dependency they own.

2. **Stabilize the API boundary.** The permanent collaboration with checkout suggests the APIs are either unclear, unstable, or insufficient for checkout to ship independently. Invest in clarifying and hardening the contract:
   - Document the ledger API surface clearly (what checkout can do without asking)
   - Establish a deprecation policy for API changes
   - Make API changes time-bounded and predictable (not ad-hoc, mid-release coordination)

3. **Reduce cognitive load by separating concerns.** If the team keeps the current shape (owning new ledger features + supporting 7 teams), it will continue to drown. Options:
   - Assign a dedicated support person (or pair) to handle API-consumer requests — let them interrupt and unblock; the rest of the team builds features
   - Or: move new feature development out and make billing-platform purely a platform team (no new ledger development — that becomes the checkout or product team's responsibility to request)
   - Or: split the team — a complicated-subsystem core (payments experts) and a platform overlay (API/support)

4. **Measure the coordination cost.** Before the reteam: audit how much of billing-platform's sprint time is spent in synchronous coordination (Slack, meetings, code reviews with checkout/product teams) vs. autonomous feature work. If it's >40% coordination, you have data for the leads that the topology is broken.

## What to do next

This assessment is a checkpoint for the coordinator and leads — they own the reteaming decision. A coach can:
- Help the team clarify its purpose and constraints within whatever structure is chosen
- Facilitate a working-agreement conversation with checkout and other product teams (once the topology is decided)
- Monitor whether the interaction modes (X-as-a-Service, collaboration, facilitation) are actually happening as redesigned

This is not a process problem. Fixing ceremonies, retros, or standups won't move the needle while the team is structured to require constant cross-team coordination.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 11.5/12.0 (96%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 42601 ms |
| Target cost | $0.0687 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Classifies the team against the four Team Topologies types by name (stream-aligned, platform, enabling, complicated-subsystem) and reaches a defensible primary type | PASS | Artifact: 'Actual type: Complicated-subsystem' and 'Treated as: Stream-aligned'. Recommendations name 'platform team' and 'complicated-subsystem team'. Three of four types named; enabling absent but inapplicable. |
| c2 | Names the component-team-masquerading-as-stream-aligned smell — owning a layer not a slice, forcing cross-team coordination to ship anything user-facing | PASS | 'Component-team smell: Yes. The team owns a technical layer... rather than an end-to-end user-facing product slice. Every customer-facing feature requires coordination across teams.' |
| c3 | Classifies the interaction modes by name (collaboration, X-as-a-Service, facilitating) for the team's significant relationships | PASS | Interaction-mode table uses 'Collaboration' and 'X-as-a-Service' for all three relationship rows. 'Facilitating' not named but inapplicable to these relationships. |
| c4 | Identifies the permanent collaboration with the checkout team as the wrong mode — collaboration is expensive and time-bounded; this relationship should likely be X-as-a-Service | PASS | Table row: 'Checkout team \| Collaboration (close back-and-forth) \| Should be: X-as-a-Service \| Friction: High — permanent entanglement, nothing finishes cleanly.' |
| c5 | Reads cognitive load explicitly and flags the team as overloaded (five consumers plus new feature work, nothing finishing) with the supplied evidence | PASS | 'Assessment: Severely overloaded. Supporting 7 downstream teams... while simultaneously building new ledger features' and 'Chronic inability to finish work ("nothing seems to finish")' |
| c6 | Keeps the recommendation advisory — the topology/restructuring decision belongs to the coordinator and leads, not the coach | PASS | 'This assessment is a checkpoint for the coordinator and leads — they own the reteaming decision.' Recommendations use 'Decide:', 'Options:', 'If X then...' framing throughout. |
| c7 | Notes when this lens does NOT apply — a process/safety problem is not a topology problem — to avoid misdiagnosing | PARTIAL | 'This is not a process problem. Fixing ceremonies, retros, or standups won't move the needle...' Process exclusion noted; safety dimension not mentioned. |
| c8 | Output is a structured topology assessment with the team type, the interaction-mode table, a cognitive-load read, and advisory recommendations | PASS | Artifact has distinct sections: Team type, Interaction modes (table), Cognitive load, Root cause, Recommendations (advisory), What to do next — all present. |
| c9 | Output names the component-team smell with the layer-not-a-slice evidence rather than accepting the 'platform' or 'stream-aligned' label at face value | PASS | Root cause section: 'billing-platform is structured as a component team (owns a layer) but is being asked to behave as a stream-aligned team (ships features end-to-end).' |
| c10 | The interaction-mode table flags the checkout-team collaboration as a mode that should change (toward X-as-a-Service) with the friction noted | PASS | Table row: Checkout team \| Collaboration \| Should be: X-as-a-Service \| Friction: High — permanent entanglement, nothing finishes cleanly. |
| c11 | Output's cognitive-load read concludes overloaded and cites the five consumers plus concurrent feature work | PASS | 'Supporting 7 downstream teams (checkout + 1 product team + 5 API consumers) while simultaneously building new ledger features' under 'Severely overloaded.' |
| c12 | Output frames every recommendation as advisory to the coordinator/leads, not as a restructuring the coach will perform | PASS | All four recommendations use 'Decide:', 'Options:', or conditional 'If X then' framing. 'What to do next' section explicitly names coordinator/leads as decision owners. |
| c13 | Output reads as genuinely using the Team Topologies model (correct vocabulary and the collaboration-is-expensive insight), not a generic team review | PARTIAL | Correct TT vocabulary throughout (stream-aligned, complicated-subsystem, X-as-a-Service, collaboration). 'Collaboration is expensive and time-bounded' not stated explicitly — only 'permanent entanglement' noted. |

### Notes

The assessment is thorough and accurate — component-team smell named, interaction modes correctly applied, cognitive load explicitly called 'severely overloaded', and advisory framing maintained throughout. Minor gaps: the enabling team type is never named, the 'facilitating' interaction mode is absent (though inapplicable here), and the canonical Team Topologies insight that collaboration is intentionally expensive and time-bounded isn't stated as a principle.
