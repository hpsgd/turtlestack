# Audit Scaling Framework

Scenario: Leadership is considering adopting SAFe across three teams. The coach must name the coordination problem first, test whether the need can be reduced by restructuring rather than coordinated, map the candidate frameworks to the problem, apply the deliberate-rejection test, and keep the recommendation advisory — resisting "adopt the industry default".

## Prompt

> Use the agile-coach `audit-scaling-framework` skill to advise on a scaling decision. Context: there are three teams (billing, checkout, and accounts). Leadership wants to "adopt SAFe like everyone else." The actual pain is that the three teams keep blocking each other on a shared payments service, and a single shippable increment usually needs coordinated work across all three because the teams are split by component (billing-layer, checkout-layer, accounts-layer) rather than by feature. Produce the scaling assessment in the skill's standard format. Write the output to `docs/coaching/` in the current working directory.
> 
> Proceed without asking — produce the assessment.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Assessment complete. The scaling framework audit has been saved to `docs/coaching/scaling-framework-assessment--payments-teams.md`.

**Core finding:** The three teams don't have a scaling problem—they have a team topology problem. Organizing by component (billing-layer, checkout-layer, accounts-layer) creates unavoidable cross-team dependencies on every meaningful change. SAFe will not solve this; it will institutionalize the dependencies with additional ceremony.

**Recommendation:** Reorganize into feature teams that own end-to-end payment or account slices. This eliminates the systematic blocking. Coordinate lightweight (shared backlog, a weekly sync, clear escalation for emergent blockers) without adopting a framework. If topology change is blocked, stay lightweight rather than adopting SAFe on component teams—adding ceremony without fixing the root cause makes things worse, not better.

The assessment includes the deliberate rejection rationale for each framework and notes the tension for leadership ("everyone uses SAFe") alongside why that's weak reasoning for three teams.

### Artifacts written

#### `work/docs/coaching/scaling-framework-assessment--payments-teams.md`

```
---
title: Scaling Framework Assessment — Billing / Checkout / Accounts Coordination
date: 2026-06-13
author: agile-coach
category: Coaching
confidence: 4
---

## Coordination problem

**Stated concretely:** Three teams split by technical layer/component (billing-layer, checkout-layer, accounts-layer) block each other on a shared payments service. Every shippable user-facing increment in payments requires coordinated work across all three teams. Teams cannot ship independently because no single layer owns a complete feature.

**Can the need be reduced (topology change)?** **Yes.** The coordination problem is not inherent to payments complexity—it is created by the team structure. Reorganizing into feature teams (e.g., "subscription billing," "one-time payment checkout," "account authentication") where each team owns an end-to-end user-facing slice would eliminate most cross-team dependencies. Teams could then coordinate on shared infrastructure and emergent dependencies, rather than on every feature.

This is the core insight: **the pain is not that scaling is needed; the pain is that the team topology creates unnecessary dependencies.**

---

## Candidate fit

| Framework | Fits? | Rationale |
|-----------|-------|-----------|
| **LeSS** | Conditional—only if topology changes first | LeSS's philosophy is "remove dependencies, don't coordinate them." It requires feature teams as a prerequisite. If billing/checkout/accounts reorganize into feature teams owning slices of payment flows, LeSS's minimal structure (daily standup, shared backlog, one definition of done) works well. But LeSS doesn't help if teams stay component-organized. |
| **Nexus** | Weak fit | Nexus adds a Nexus Integration Team to coordinate the three teams' sprints. This creates a new bottleneck: the integration team becomes the single point where shared-payments decisions get made. For 3 teams and a known shared dependency, a dedicated coordination team is overkill and slows decision-making. |
| **Scrum@Scale** | Poor fit | Designed for organisation-wide scaling (8+ teams, multiple programs). Three teams is below the scale where Scrum@Scale's network structure adds value. Adds ceremony without addressing the topology problem. |
| **SAFe** | Poor fit / reject | SAFe is the heaviest framework (team / program / solution / portfolio layers, PI planning, ARTs, multiple ceremonies). It is designed for large enterprises with rigid structure and heavy alignment needs. Three teams is far below SAFe's design point. More critically, SAFe will institutionalize the component-based coordination problem—adding PI planning and ART ceremonies to component teams just means component teams meet more often, not that dependencies vanish. "Adopt SAFe like everyone else" is fashion-driven adoption, not problem-driven. |

---

## Recommendation (advisory to coordinator / leads)

**Primary path: Reorganize into feature teams. Coordinate lightweight, no framework.**

- **Rationale:** The root cause is team topology, not scaling complexity. Three feature teams (each owning an end-to-end payment flow or account feature) eliminate the systematic cross-team blocking. Teams remain small (Dunbar-sized), so lightweight coordination suffices: shared backlog visibility, a 30-min weekly sync for dependency raises, clear escalation when an unexpected cross-team dependency appears.

- **Why not SAFe:** SAFe is being considered because it is the industry default, not because it solves this problem. Adopting SAFe on three component-organized teams will add PI planning, ART ceremonies, and program-level coordination—but it won't fix the fact that every change still requires all three teams. You will have the same dependencies plus ceremony overhead. SAFe is appropriate for large enterprises (20+ teams, multiple business units, portfolio-level prioritization conflicts). Three teams is an order of magnitude too small.

- **Why not Nexus:** Nexus adds a Nexus Integration Team. For teams with a known shared dependency (the payments service), this creates a bottleneck: the integration team becomes the decision-maker on shared-service changes. Better to have the three teams sync directly and raise blockers in real time, rather than funnel through a coordination team.

- **If topology change is blocked:** If leadership won't reorganize into feature teams, the next-best choice is lightweight coordination without a framework. Use a shared backlog, visibility into cross-team dependencies (a dependency matrix or simple "who's blocked on whom" conversation in standup), and a low-ceremony weekly sync. Do not adopt SAFe or Nexus on a component-organized structure—it will institutionalize the dependencies rather than resolve them.

---

## Key tensions for the coordinator

1. **"Everyone is adopting SAFe."** True, but SAFe is designed for large enterprises (100+ people, multiple programs, portfolio-level conflicts). Three teams is not "everyone." Industry fashion is a weak basis for org design. Ground the choice in the actual problem.

2. **Topology change is hard.** Reorganizing from component teams to feature teams requires reskilling (billing engineers learning checkout flows, etc.) and may feel risky. But it's the only move that permanently reduces the coordination need. Adding ceremony (SAFe, Nexus) without topology change is a tax on speed without a benefit.

3. **The payments service is shared.** This is real, and it's not going away. Feature teams still need to coordinate on shared infrastructure. The difference: instead of "every feature requires all three component teams," you have "feature-specific teams + a small shared-infra sync." Much smaller coordination surface.

---

## Confidence: High (4/4)

The diagnosis (component-organized teams create systematic dependencies) is clear, and the solution (reorganize into feature teams) is well-established in the literature and practice (cross-functional feature teams, product slicing, [LeSS](https://less.works/), Team Topologies). The recommendation to reject SAFe on three teams is well-grounded in both framework design intent and practitioner experience (Ron Jeffries, Allen Holub, and others on SAFe's heavyweight-on-small-teams risk).

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 13.0/13.0 (100%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 42029 ms |
| Target cost | $0.0668 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Names the coordination problem concretely first (teams blocking each other on the shared payments service; component-split teams forcing cross-team work to ship) — does not start from the framework | PASS | "Three teams split by technical layer/component...block each other on a shared payments service. Every shippable user-facing increment in payments requires coordinated work across all three teams." |
| c2 | Tests whether the coordination need can be reduced by restructuring into feature teams rather than coordinated by a framework — the reduce-the-need-first move | PASS | "Can the need be reduced (topology change)? Yes." followed by explicit discussion of reorganizing into feature teams owning end-to-end slices. |
| c3 | Maps the candidate frameworks (LeSS, Nexus, Scrum@Scale, SAFe) to this specific problem with where each fits and its caution, rather than a generic framework summary | PASS | Candidate fit table covers all four frameworks with verdicts (Conditional/Weak/Poor/Poor-reject) and rationale tied to the three-team component-split scenario. |
| c4 | Applies the deliberate-rejection test — picking no framework is a legitimate outcome; with only three teams, lightweight coordination may suffice and SAFe is likely overkill | PASS | Primary recommendation: "Reorganize into feature teams. Coordinate lightweight, no framework." No framework is the explicit primary path. |
| c5 | Pushes back on "adopt SAFe because everyone uses it" — naming that the industry-default rationale optimises for looking standard, not for solving the actual problem | PASS | "'Adopt SAFe like everyone else' is fashion-driven adoption, not problem-driven." Tensions section: "Industry fashion is a weak basis for org design." |
| c6 | Connects the recommendation to team topology — the component-team split is the real driver, and reorganising into feature teams may remove the dependency entirely | PASS | "The root cause is team topology, not scaling complexity." and "the pain is not that scaling is needed; the pain is that the team topology creates unnecessary dependencies." |
| c7 | Keeps the recommendation advisory — adopting a scaling framework is an org-structural decision for the coordinator and leads | PASS | Section heading: "## Recommendation (advisory to coordinator / leads)" — explicit advisory framing. |
| c8 | If a framework is recommended at all, prefers the lightest that fits rather than the heaviest | PARTIAL | No framework is the primary recommendation. LeSS is listed as "Conditional" (lightest option), clearly ranked above SAFe. Ceiling is PARTIAL. |
| c9 | Output is a structured scaling assessment stating the coordination problem, whether it can be reduced, a candidate-fit table, and an advisory recommendation | PASS | File contains all four required sections: Coordination problem, topology-change test, Candidate fit table, and Recommendation (advisory to coordinator/leads). |
| c10 | The recommendation leads with reduce-the-need (restructure toward feature teams) before any framework, given the component-split root cause | PASS | "Primary path: Reorganize into feature teams. Coordinate lightweight, no framework." — topology fix comes before any framework discussion. |
| c11 | The candidate-fit table covers LeSS, Nexus, Scrum@Scale, and SAFe with a fit verdict and rationale tied to three teams blocking on a shared service | PASS | Table rows: LeSS (Conditional), Nexus (Weak fit), Scrum@Scale (Poor fit), SAFe (Poor fit/reject) — all with rationale referencing the three-team shared-payments scenario. |
| c12 | Output explicitly rejects "adopt SAFe by default" and explains why the industry-default rationale is the weakest one | PASS | Tensions section: "'Everyone is adopting SAFe.' True, but...Three teams is not 'everyone.' Industry fashion is a weak basis for org design. Ground the choice in the actual problem." |
| c13 | Output frames the decision as advisory to the coordinator/leads, not a call the coach makes | PASS | "## Recommendation (advisory to coordinator / leads)" — the section heading explicitly scopes the decision to coordinators and leads. |
| c14 | If suggesting any framework, output prefers the lightest that fits (e.g. LeSS over SAFe for three teams) and flags SAFe as overkill here | PARTIAL | LeSS rated Conditional (lightest), SAFe explicitly called overkill: "Three teams is far below SAFe's design point." Ceiling is PARTIAL. |

### Notes

The assessment is comprehensive and well-structured, hitting every criterion including the deliberate-rejection test, topology-first framing, advisory tone, and explicit pushback on industry-default reasoning. Both the chat summary and the written artifact are fully aligned, with the file containing all required structural elements.
