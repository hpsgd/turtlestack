---
# Match the model the agent declares (sonnet) in
# plugins/product/product-analyst/agents/product-analyst.md. The runner otherwise
# falls back to the harness default (Haiku), which is not what the agent is
# designed to run on.
target-model: claude-sonnet-4-6
---

# Test: product-analyst rejects a vanity North Star and a correlation-as-causation push

Scenario: Leadership wants a cumulative vanity metric as the North Star and wants to force a product change based on
a correlation treated as cause. The agent must anchor to the customer value moment, reject the vanity metric,
propose a value-based North Star, run a Goodhart check, expose the correlation-not-causation error and demand an
experiment, build a leading/lagging hierarchy, and stay in its lane (hand offs to data-engineer and
product-manager) using its structured deliverable format.

## Prompt

Use the product-analyst agent to handle this, and respond in its standard measurement methodology and deliverable format.

We're the team behind Northstar Notes, a personal note-taking app. Two things came down from leadership this week and we want your read before we commit:

1. The CEO wants to make "total registered users" our official North Star Metric — it only ever goes up and looks great in the board deck.
2. Our data team found that users who join a shared "Spaces" group retain about 3x better than users who don't, so the growth team wants to force every new user into a Spaces group during onboarding to lift retention.

Give us your read on the metrics strategy: what our North Star should be, how to structure the supporting metrics, and what to do about the Spaces finding.

## Criteria

- [ ] PASS: Anchors to the customer value moment before proposing any number — names the observable moment a Northstar Notes user actually gets value (capturing / retrieving a note they rely on)
- [ ] PASS: Rejects "total registered users" as a North Star, explicitly naming it a cumulative vanity metric that rises regardless of product quality
- [ ] PASS: Proposes a North Star that measures delivered customer value (e.g. active users who capture and retrieve notes), not a company-convenience count, and treats revenue as a lagging result rather than the North Star
- [ ] PASS: Runs a Goodhart check on its proposed North Star — names how optimising it could be gamed and whether that would hurt the user
- [ ] PASS: Flags the "Spaces group → 3x retention" finding as correlation, NOT causation — points out those users were likely already more engaged — and recommends an experiment (A/B or holdout) before forcing everyone into Spaces
- [ ] PASS: Builds a metric hierarchy that distinguishes leading/input metrics (controllable this week) from the lagging North Star — not a single number
- [ ] PASS: Distinguishes leading, lagging, and vanity metrics explicitly and keeps vanity metrics out of the tree
- [ ] PASS: Names the hand-offs — data-engineer implements instrumentation, product-manager owns OKRs — and stays within its own remit (does not rewrite OKRs or build pipelines)
- [ ] PARTIAL: Hits a decision checkpoint — flags that changing an established North Star, or shipping an onboarding change that could degrade a segment's experience, needs product-manager / leadership sign-off

## Output expectations

- [ ] PASS: Output uses a structured deliverable format (type, customer question, deliverable, Goodhart/coherence check, hand-off) rather than freeform prose
- [ ] PASS: The Spaces recommendation is "run an experiment to establish causation," not "force everyone into Spaces"
- [ ] PASS: The proposed North Star is expressed as the customer's win as a number, with revenue treated as a downstream/lagging result
- [ ] PARTIAL: A Goodhart / coherence checklist is present and worked through, not just mentioned
