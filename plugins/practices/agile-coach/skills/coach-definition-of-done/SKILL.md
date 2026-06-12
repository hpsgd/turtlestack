---
name: coach-definition-of-done
description: "Facilitate the team to author its own Definition of Done — specific, testable, collectively owned, not a management wish list. Runs a specificity test and ties the DoD to the release-manager's gates. Use when a team has no DoD, a vague one, or is presenting half-done work as complete."
argument-hint: "[team name]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Coach the Definition of Done

Facilitate **$ARGUMENTS** to author its own Definition of Done. The DoD is the team's quality contract with itself
and the organisation: per the [2020 Scrum Guide](https://scrumguides.org/scrum-guide.html), "if a Product Backlog
item does not meet the Definition of Done, it cannot be released or even presented at the Sprint Review." The team
authors it; you facilitate. A DoD handed down by management is a wish list the team won't own. This skill pairs with
`design-working-agreements` (the DoD is the quality contract; agreements are social behaviour) and feeds the
release-manager's go/no-go gates.

## Step 1: Establish what the DoD applies to

A team often needs more than one DoD — a user-facing feature, an API change, and an infrastructure change have
different completeness criteria. Facilitate the team to name the work types its DoD must cover before drafting
criteria.

Output: the list of work types in scope.

## Step 2: Facilitate the team drafting criteria

Coach the team to draft completeness criteria for each work type. Prompt with the dimensions, but let the team write
the content:

- Code: reviewed, merged, behind a flag if needed.
- Tests: which kinds, what coverage threshold.
- Quality: lint, typecheck, security review for auth/data changes.
- Docs: what must be updated.
- Deployment: does "done" include deployed to production? (A DoD that says "deployed to production" commits the team
  to continuous delivery — a real choice to make consciously.)

## Step 3: Run the specificity test

The most common DoD failure is vagueness. Test every criterion: can you objectively tell whether it's met?

| Vague | Specific |
|-------|----------|
| "Unit tests written" | "Unit tests written; line coverage >= 80%" |
| "Code reviewed" | "Reviewed and approved by one engineer not the author" |
| "Documented" | "Public API changes reflected in the API docs" |
| "Tested" | "Acceptance tests pass; manual smoke test recorded" |

Any criterion that can't be objectively checked gets rewritten or dropped. A DoD you can argue about at the sprint
review isn't a contract.

## Step 4: Tie the DoD to the release gates

The DoD feeds the [release-manager's](https://scrumguides.org/scrum-guide.html) go/no-go gates — "all items meet
Definition of Done" is a release gate. Coach the team to keep its DoD coherent with the release gates: if the
release gate requires a security review for auth changes, the DoD should too. Where a DoD change would alter a
release gate, route it through the release manager (a decision checkpoint for the coach).

## Step 5: Record and set a review trigger

Write `docs/coaching/definition-of-done.md` (the bootstrap skill creates the starter). Set a review trigger: revisit
the DoD in the retrospective when an item proves vague or is repeatedly skipped. A DoD nobody revisits drifts from
reality.

## Rules

- The team authors the DoD; you facilitate. A management-authored DoD is a wish list, not a contract the team owns.
- Every criterion must be objectively testable. If you can argue at the review about whether it's met, it's too
  vague — rewrite it.
- Keep the DoD coherent with the release gates. A DoD that contradicts go/no-go gates creates a dispute at release
  time. Route gate-affecting changes through the release manager.
- "Deployed to production" in a DoD is a real commitment to continuous delivery — make sure the team chooses it
  consciously, not by accident.
- Don't let quality criteria leak into working agreements or vice versa. The DoD is the quality contract; agreements
  are social behaviour.

## Output Format

```markdown
---
title: Definition of Done — [team]
date: YYYY-MM-DD
author: agile-coach
category: Coaching
---

## Authored by
- The team — [who was present]

## Scope
[Work types this DoD covers.]

## Definition of Done (team-authored)
### [Work type]
- [ ] [Specific, testable criterion]
- [ ] [...]

## Specificity check
[Any criterion rewritten from vague to testable.]

## Release-gate coherence
- Aligned with release gates: [...]
- Gate-affecting changes routed to release manager: [...]

## Review trigger
- Revisited when: [...]
```
