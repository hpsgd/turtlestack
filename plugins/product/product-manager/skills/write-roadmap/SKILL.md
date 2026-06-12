---
name: write-roadmap
description: "Build an outcome-shaped product roadmap using Now/Next/Later or GIST. Produces a roadmap that promises changes in customer behaviour, not a feature timeline with dates. Use when communicating product direction, planning a quarter, or replacing a date-based feature roadmap."
argument-hint: "[product slice, time horizon, or existing roadmap to reshape]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Build an outcome-shaped roadmap for $ARGUMENTS.

A roadmap states the change in customer behaviour you expect, not a list of features with dates against
them. The further out an item sits, the less you know about it — so committing to dated features is
asserting a certainty you don't have. This skill produces a [Now/Next/Later roadmap (Janna Bastow /
ProdPad)](https://www.prodpad.com/blog/invented-now-next-later-roadmap/) or a
[GIST plan (Itamar Gilad)](https://itamargilad.com/gist-framework/), grounded in the outcome roadmap
critique from Melissa Perri's *Escaping the Build Trap*. Product-level OKR input is produced here and fed
up to the CPO and coordinator.

Follow every step. The output is a roadmap a stakeholder can read without mistaking it for a delivery
commitment.

## Step 1: Anchor on the desired outcome

Before any roadmap item, state the outcome the roadmap drives. An outcome is a change in customer
behaviour, expressed as a metric moving from a baseline to a target:

- Bad (output): "Ship the bulk-import feature in Q2"
- Good (outcome): "Increase the share of new accounts that import data in week one from 30% to 60%"

Write one to three desired outcomes for the slice. Each must have a baseline and a target. If you can't
state a baseline, that is a discovery gap — flag it and run discovery first
(`/product-manager:write-discovery-plan`). This step is complete when every outcome has baseline → target.

## Step 2: Choose the roadmap shape

Pick one shape and state why:

| Shape | Use when | Structure |
|-------|----------|-----------|
| **Now / Next / Later** | Communicating direction to stakeholders who expect a roadmap | Three time-horizon columns, confidence decreasing left to right |
| **GIST** | The org tolerates uncertainty and treats experiments as learning | Goals → Ideas → Step-projects → Tasks, each at a different cadence |

Default to Now/Next/Later for stakeholder communication. Use GIST when the team is running a
discovery-heavy, experiment-driven motion and needs the idea bank and step-project layers.

## Step 3: Populate the horizons

For Now/Next/Later, place each item by how much you know, not by a date:

- **Now** — in active discovery or delivery. You know the problem, you have evidence, work is moving
- **Next** — validated enough to commit to soon. Discovery has confirmed the problem; solution is forming
- **Later** — directionally important, not yet validated. A bet, not a promise. May never happen

Each item is an outcome or an opportunity, not a feature. "Reduce time-to-first-value" belongs on the
roadmap; "add an onboarding wizard" is a solution hypothesis that belongs on the opportunity solution
tree (`/product-manager:write-opportunity-solution-tree`), not the roadmap.

For GIST, populate the four layers: Goals (the outcomes from Step 1), Ideas (a prioritised bank of bets),
Step-projects (the experiments and MVPs in flight, typically ≤ 10 weeks), Tasks (the current work).

This step is complete when every item ties to a desired outcome from Step 1.

## Step 4: Attach confidence and evidence

For each Now and Next item, record the evidence behind it and a confidence rating (0-4). Items with no
evidence cannot sit in Now — they belong in Later as an explicit bet, or in discovery. This is what stops
the roadmap from becoming a wish list.

## Step 5: Derive product-level OKR input

The roadmap's desired outcomes become proposed product-level OKRs. Express them as Objective + Key
Results with baselines, and mark this as **input for the CPO and coordinator**, not an authored OKR set:

```
Objective: [the qualitative direction]
  KR1: [outcome metric] from [baseline] to [target]
  KR2: [outcome metric] from [baseline] to [target]
```

You propose; the coordinator owns the company OKR set and the CPO owns product strategy. This step is
complete when each desired outcome has a corresponding proposed KR with a baseline.

## Rules

- **Never put dated features on the roadmap.** "Bulk import, Q2" is a timeline commitment masquerading as a roadmap. State the outcome and let discovery decide the feature.
- **Every item ties to an outcome.** If you can't name the customer-behaviour change an item drives, it doesn't belong on the roadmap — it belongs on the OST as a solution idea.
- **Confidence decreases left to right.** Don't pretend Later items have the certainty of Now items. The honesty is the point.
- **Don't smuggle the backlog onto the roadmap.** Sprint-level stories are the product-owner's backlog, not roadmap items. The roadmap is the why; the backlog is the how.
- **OKR input, not OKR authorship.** Propose product-level outcomes; the coordinator authors the company OKR set.
- **A Later item is allowed to die.** The roadmap is a set of bets, not promises. Killing a Later item after discovery contradicts it is success, not failure.

## Output Format

Write the roadmap to `docs/product/roadmap-[slice].md` using the `templates/roadmap.md` template:

```markdown
# Roadmap: [slice]

## Desired outcomes

| Outcome | Baseline | Target | Confidence (0-4) |
|---------|----------|--------|------------------|
| ... | ... | ... | ... |

## Now / Next / Later

### Now (active)
- [outcome/opportunity] — drives [desired outcome] — evidence: [...] — confidence: [0-4]

### Next (committing soon)
- [outcome/opportunity] — drives [desired outcome] — evidence: [...] — confidence: [0-4]

### Later (directional bets)
- [outcome/opportunity] — drives [desired outcome] — bet, not yet validated

## Proposed product-level OKRs (input for CPO / coordinator)

Objective: [...]
  KR1: [metric] from [baseline] to [target]
  KR2: [metric] from [baseline] to [target]
```

## Related Skills

- `/product-manager:write-opportunity-solution-tree` — solution ideas live on the OST; outcomes live on the roadmap.
- `/product-manager:write-prd` — a Now item that's ready for delivery gets a PRD.
- `/product-manager:write-discovery-plan` — items with no baseline or evidence go to discovery before the roadmap.
