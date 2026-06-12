---
name: write-opportunity-solution-tree
description: "Build or update a Teresa Torres Opportunity Solution Tree — desired outcome at the root, opportunity space from real interviews, solutions per opportunity, and assumption tests. Produces a visual artifact that makes discovery decisions explicit. Use when mapping a problem space or keeping discovery legible as interviews accumulate."
argument-hint: "[desired outcome and the interview evidence to map]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Build or update an Opportunity Solution Tree for $ARGUMENTS.

The [Opportunity Solution Tree (Teresa Torres)](https://www.producttalk.org/opportunity-solution-trees/) is
a visual artifact that makes the team's discovery work legible and decision-making explicit. It connects a
desired outcome to the customer opportunities that would move it, the solutions that might address them,
and the experiments that test those solutions. The tree is only as good as its inputs — opportunities come
from interviews, not brainstorming.

Follow every step. The output is a tree (rendered as a nested markdown structure or Mermaid diagram) that
the trio uses to decide where to invest.

## Step 1: Set the desired outcome (root)

Agree the desired outcome with your product leader before touching the tree — a business metric the team
is trying to move (increase weekly active users, reduce churn). One root per tree. If the slice already
has a roadmap, the desired outcome is the roadmap root. This step is complete when one measurable outcome
sits at the root.

## Step 2: Map the opportunity space from research

Opportunities are customer needs, pain points, and desires that — if addressed — would drive the outcome.
They come from interviews (`/product-manager:write-interview-guide`,
`/product-manager:synthesise-interviews`), never from assumption. Start by running three to four
story-based interviews, then map what you heard.

**What earns a branch.** An opportunity belongs on the tree only if it is:

1. **Connected to the desired outcome** — addressing it would plausibly move the root metric
2. **Surfaced by actual customer research** — not team brainstorming
3. **Specific enough to act on** — "users are frustrated" fails; "freelancers on mobile can't track hours
   against multiple clients simultaneously" passes

Group related opportunities into a hierarchy (parent needs, child sub-needs). This step is complete when
every opportunity node cites the interview it came from.

## Step 3: Brainstorm solutions for the target opportunity

Choose one opportunity to focus on — don't generate solutions for the whole space at once. For that
opportunity, brainstorm multiple distinct solutions; don't jump to the obvious one. Each solution is a
child of its opportunity, never floating free. This step is complete when the target opportunity has at
least three candidate solutions.

## Step 4: Identify assumptions and design experiments

Before building any solution, identify the assumptions it relies on and design experiments to test the
riskiest ones (`/product-manager:assumption-map`, `/product-manager:design-pretotype`). Each experiment is
a leaf under its solution. This step is complete when the leading solution has its riskiest assumption
named and an experiment attached.

## Step 5: Set the update rhythm

The tree is a living artifact, not a one-time deliverable. Revisit the opportunity space every three to
four additional interviews (roughly monthly for weekly interviewers). A tree that doesn't update is a
static decision tree, not a discovery tool. This step is complete when the next review date is recorded.

## Rules

- **Opportunities come from research, not assumption.** A tree built from brainstormed problems is just a
  decision tree. The customer-evidence requirement is what makes it a discovery tool.
- **One opportunity at a time for solutions.** Don't brainstorm solutions across the whole opportunity
  space — choose a target opportunity, then ideate.
- **Don't add solutions before selecting a target opportunity.** Jumping to solutions for everything is the
  most common OST failure mode.
- **Every solution traces to an opportunity; every opportunity traces to the outcome.** No floating nodes.
- **The tree updates continuously.** Monthly is the minimum. A static tree is stale within weeks of active
  discovery.
- **Specific opportunities only.** "Users want it faster" is not actionable. Name the person, the context,
  and the friction.

## Output Format

Write to `docs/product/ost-[slice].md`. Use a nested structure or a Mermaid tree:

```markdown
# Opportunity Solution Tree: [slice]

**Desired outcome (root):** [metric, baseline → target]
**Last updated:** [date] · **Next review:** [date]

## Tree

- **Outcome:** [root metric]
  - **Opportunity:** [specific need] — _source: [interview ref]_
    - **Solution:** [idea]
      - **Assumption:** [riskiest] → **Experiment:** [test] — _status: [untested / running / result]_
    - **Solution:** [idea]
  - **Opportunity:** [specific need] — _source: [interview ref]_

## Target opportunity this cycle
[which opportunity the team is focused on, and why]

## Open assumptions to test
| Solution | Riskiest assumption | Experiment | Status |
|----------|---------------------|------------|--------|
| ... | ... | ... | ... |
```

Optionally render the tree as a Mermaid `graph TD` diagram for stakeholder communication.

## Related Skills

- `/product-manager:write-discovery-plan` — the cadence that feeds the tree.
- `/product-manager:synthesise-interviews` — turns an interview window into opportunity nodes.
- `/product-manager:assumption-map` — picks which assumptions under a solution to test first.
- `/product-manager:design-pretotype` — designs the experiments that hang off solutions.
