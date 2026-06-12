---
name: coach-refinement
description: "Run a backlog refinement event — facilitate the team through INVEST checks, a capacity budget, dependency surfacing, and a Definition of Ready gate so items leave the session sprint-ready. Use to prepare and run a live refinement ceremony, not a solo backlog audit."
argument-hint: "[path to the backlog/candidate items, or 'next-sprint' to pull the top of the ready queue]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Coach a backlog refinement event

Facilitate a live backlog refinement session for the items at $ARGUMENTS. This is the team-event run of refinement: the product owner walks the team through a small set of candidate items, checks each against [INVEST](https://www.agilealliance.org/glossary/invest/), surfaces dependencies, and gates each item against the Definition of Ready so it leaves the session sprint-ready.

This skill complements `groom-backlog`. They are not the same activity and have a genuine workflow dependency:

- `groom-backlog` is the **solo audit pass** — the product owner classifies the whole backlog (ready / needs-refinement / stale / blocked), RICE-scores, and produces the ordered queue. Run it first.
- `coach-refinement` is the **live team event** — you take the top of that groomed queue and run the team through it together to reach Ready.

Run `groom-backlog` before this skill so you walk into the event with a pre-classified queue, not a raw backlog. The [agile-coach](https://www.scrum.org/resources/what-is-scrum) observes this event for INVEST and capacity discipline; you run the content, they keep the ceremony healthy.

## Step 1: Set the capacity budget

Refinement is timeboxed against team capacity, not open-ended. The [Scrum Guide](https://scrumguides.org/scrum-guide.html) treats Product Backlog refinement as an ongoing activity that should consume no more than about **10% of the team's capacity**. Budget the session before it starts.

1. Establish the team's sprint capacity in hours (developer-hours available this sprint)
2. The refinement budget is ~10% of that capacity across the sprint. A two-week sprint for five developers is roughly 400 hours; the refinement budget is roughly 40 hours total, of which a single event is a slice
3. From the per-event time, derive how many items can realistically be refined. A rule of thumb: 10-15 minutes per item for discussion plus INVEST and DoR checks

State the budget explicitly at the top of the output: total capacity, refinement budget, items in scope for this event. If the candidate list exceeds the budget, trim to the highest-priority items from the groomed queue — do not run over.

**Verifiable output:** a stated budget line and a trimmed candidate list that fits inside it.

## Step 2: INVEST-check every candidate item

For each item in scope, walk the team through the six INVEST criteria. Mark each criterion pass or fail with a one-line reason:

- **I**ndependent — can be delivered without waiting on another item in this batch
- **N**egotiable — the approach is open; only the outcome is fixed
- **V**aluable — delivers user-visible value on its own
- **E**stimable — the team can size it with reasonable confidence
- **S**mall — fits comfortably in one sprint
- **T**estable — has acceptance criteria a tester could verify

Any item that fails **Small** or **Independent** must be split during the event. Split by user behaviour, never by technical layer — "user can export to CSV" and "user can export to PDF", not "build export backend" and "build export frontend". Each child item re-enters the INVEST check.

**Anti-pattern:** do not wave an item through INVEST because the team is impatient to fill the sprint. An item that fails a criterion and is not split or fixed leaves the event as "needs refinement", not "ready". Recording a fake pass is worse than recording an honest fail.

**Verifiable output:** an INVEST table per item with explicit pass/fail and reasons; any split items shown with their children.

## Step 3: Surface dependencies and blockers

For each surviving item, ask the team three questions and record the answers:

1. **Prerequisite** — what must exist before this can start? (another story, an API, a design, a data migration)
2. **Related** — what other in-flight or batched item touches the same code or contract?
3. **External** — what other team, vendor, or stakeholder decision does this wait on?

Map the dependencies plainly:

```
[Item A] --depends on--> [Item B]
[Item C] --blocked by--> [external: legal sign-off]
[Item D] (no dependencies — can start immediately)
```

Flag any dependency cycle — it signals a scoping problem to resolve before either item is Ready. An item with an unresolved external blocker leaves the event as **Blocked**, not Ready, with the blocker, the owner, and the impact of delay named.

**Verifiable output:** a dependency map and a list of any items reclassified to Blocked.

## Step 4: Run the Definition of Ready gate

Each item that survived INVEST and has no open blocker faces the Definition of Ready. An item passes only when every box is ticked:

- [ ] Acceptance criteria written, each passing the ISC Splitting Test (atomic, independently verifiable, no "and"/"all"/"complete" smuggling two criteria into one)
- [ ] Passes INVEST (from Step 2)
- [ ] Dependencies identified and resolved or sequenced (from Step 3)
- [ ] Traces to a PRD or roadmap item with success metrics (the why is on the card, not just the what)
- [ ] No open `[NEEDS CLARIFICATION]` markers
- [ ] 3 amigos perspective present — product owner, an engineer, and QA have all weighed in during the event

An item that fails any box goes back to the refinement queue with the specific gap named. Only items that pass every box are declared Ready and eligible for sprint planning.

**Verifiable output:** a DoR checklist result per item; a clean split between Ready and back-to-refinement.

## Step 5: Close the event and hand off

Summarise what the event produced and what happens next:

1. Items now **Ready** for planning, in priority order from the groomed queue
2. Items returned to **refinement** with the specific question or split each needs
3. Items reclassified **Blocked**, with owner and escalation
4. Any items deferred because the capacity budget ran out

Write the summary to the backlog file if the input was file-based; otherwise present it directly. Note for the agile-coach any INVEST or capacity discipline issues observed during the event (items that kept failing Small, a session that ran over budget, dependencies discovered late) so the ceremony itself can improve.

## Rules

- Always run `groom-backlog` first. Walking into a refinement event with an unclassified backlog wastes the team's timebox on triage that should already be done.
- Always state the capacity budget before refining. Never run refinement open-ended — an unbudgeted event is the most common way refinement eats sprint capacity.
- Never declare an item Ready that fails a DoR box. "Mostly ready" is not Ready. The gate is the whole point of the event.
- Split failing items by user behaviour, never by technical layer. A layer-split child delivers no value alone and fails INVEST's Valuable on its own.
- Never silently absorb a discovered dependency. If an item turns out to depend on unbuilt work, reclassify it Blocked or sequence it — don't pass it as Ready and hope.
- Don't re-prioritise against the roadmap during the event. The product owner sequences within the priority the product-manager set; refinement is about readiness, not re-ranking.
- Keep the agile-coach's lens distinct from yours. You own whether items are Ready; the coach owns whether the ceremony is healthy. Don't conflate the two in the output.

## Output Format

```markdown
# Refinement Event — [date]

## Capacity budget
- Team sprint capacity: [N developer-hours]
- Refinement budget (~10%): [M hours]
- Items in scope this event: [K]

## Item results

| Item | INVEST (I/N/V/E/S/T) | Dependencies | DoR | Outcome |
|------|----------------------|--------------|-----|---------|
| [title] | ✅✅✅✅✅✅ | None | 6/6 | Ready |
| [title] | ✅✅✅❌✅✅ | depends on [item] | 4/6 | Back to refinement — not estimable until API contract set |
| [title] | ✅✅✅✅✅✅ | blocked by [external] | — | Blocked — legal sign-off (owner: GRC lead) |

## Split items
- [parent] → [child A], [child B] (split by behaviour because parent failed Small)

## Dependency map
[A --depends on--> B, etc. Flag cycles.]

## Ready for planning (priority order)
1. [item] — [size]
2. [item] — [size]

## Returned to refinement
- [item] — [specific question or split needed]

## Blocked — escalation
- [item] — [blocker, owner, impact of delay]

## Deferred (over budget)
- [item] — carried to next event

## Notes for the agile-coach
- [ceremony-health observations: items repeatedly failing Small, late-surfacing dependencies, over-budget run]
```

## Related skills

- `/product-owner:groom-backlog` — the solo audit pass that classifies and RICE-orders the whole backlog. Run it before this skill so the event starts from a groomed queue.
- `/product-owner:write-user-story` — expand or rewrite an item that fails the Testable or Small INVEST check into a properly-sliced story with ISC criteria.
- `/product-owner:write-story-map` — when a batch of items reveals a missing end-to-end slice, map the release to find the walking skeleton before refining further.
