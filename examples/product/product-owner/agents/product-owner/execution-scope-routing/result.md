# Execution Scope Routing

Scenario: A stakeholder asks the product owner to do two things at once. First, the upstream why/what — "write the PRD and decide where this sits on the roadmap" for a brand-new feature idea with no validated problem behind it. Second, the downstream execution — turn an already-approved PRD slice into sprint-ready stories. The rescoped product-owner is EXECUTION-focused: it must route the PRD/roadmap/discovery work UPSTREAM to the product-manager (refusing to author it itself) while doing the backlog/story/acceptance-criteria work it owns.

## Prompt

> Use the product-owner agent to handle this. I have two things for you.
> 
> First: I've had an idea for a "team activity feed" — a social timeline showing what teammates are doing in the product. I don't have any customer research or a problem statement yet, but I'd like you to write the PRD for it and tell me where it should sit on our roadmap relative to our other Q3 themes.
> 
> Second: the "saved filters" feature already has an approved PRD (PRD `saved-filters`, state: Approved, success metric: cut repeat-search time 30%). The approved scope is: a user can save the current filter set with a name, see their saved filters in a list, apply a saved filter in one click, and delete a saved filter. Please turn that approved slice into sprint-ready user stories with acceptance criteria.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Here's what happened with each task:

---

**Saved Filters — done.** `docs/stories-saved-filters.md` is written with 4 sprint-ready stories (SF-01 through SF-04), each with:
- Given/When/Then acceptance criteria covering the happy path and edge cases (duplicate name, empty filter state, stale values, cross-user isolation, etc.)
- Explicit out-of-scope notes on SF-04 (no bulk delete, no undo)
- Definition of Ready checklists — all gates pass except 3 amigos review (which requires the team)

**Four open questions flagged for PM to close before planning:**
- SF-01: per-user cap on saved filters?
- SF-01: minimum valid filter set (at least 1 filter, or any non-empty combination)?
- SF-02: sort order for the list?
- SF-03: should applying a filter update the URL? (→ route to architect)

**Recommended sprint order:** SF-01 first → SF-02 + SF-03 in parallel → SF-04 in parallel with SF-02/SF-03.

---

**Team Activity Feed PRD — blocked.** The product-owner agent correctly refused. Authoring a PRD — defining the problem statement, success metrics, and the "why/what" — is a product-manager responsibility. The product-owner's mandate is to decompose an *approved* PRD into stories, not to create upstream intent.

To unblock this:
1. You need a product-manager to write the PRD (or write it yourself)
2. Before that, the minimum viable inputs are: a problem hypothesis, a target persona, and your Q3 themes (so positioning is possible)
3. Once the PRD reaches Review or Approved state, the product-owner agent can take it from there

If you want, I can either write the PRD directly (as your product-manager stand-in given this is early/exploratory), or help you articulate the problem hypothesis first. What's your preference?

### Artifacts written

#### `work/docs/stories-saved-filters.md`

```
# Stories: Saved Filters

Source: Saved Filters PRD — Approved
Success metric: Cut repeat-search time by 30%
Stories: 4 total

---

## Sprint-readiness summary

All four stories are ready to pull. The PRD scope is tight and the behaviours split cleanly.

One open question to resolve before planning: what constitutes a "filter set"? If the current filter state is empty (no filters applied), saving it has no practical value. SF-01 addresses this as an edge case, but the team should confirm what the product manager considers the minimum valid set — one filter applied, or more than one. If there's a per-user cap on saved filters, that should be confirmed too; SF-01 includes a [NEEDS CLARIFICATION] for both.

Stories that can be pulled immediately once those two questions close: SF-01, SF-02, SF-03, SF-04.

Recommended sprint order: SF-01 first (creates the data); SF-02 and SF-03 are unblocked once SF-01 ships or is in progress (they read from the same store); SF-04 can run in parallel with SF-02/SF-03.

---

## SF-01 Save current filter set

As a logged-in user who has applied one or more filters,
I want to save the current filter set with a name I choose,
so that I can return to the same search without rebuilding it.

### Acceptance criteria

**Happy path**

Given I have at least one filter applied
When I click "Save filter" and enter a unique name
Then the filter set is saved under that name and appears in my saved filters list

**Duplicate name**

Given I already have a saved filter named "Active contractors"
When I try to save a new filter set using the same name
Then I see an error message telling me the name is already taken
And the current filter set is not saved
And the name field stays open so I can enter a different name

**Empty filter state**

Given I have no filters applied (the filter set is empty)
When I attempt to save
Then the save action is either disabled or I see a message explaining there is nothing to save

**Name validation**

Given I open the save dialog
When I submit with a blank name or a name that is only whitespace
Then the save is rejected and the name field shows a validation error

**Save confirmation**

Given I successfully save a filter set
When the save completes
Then I see a confirmation (inline message or toast) that the filter was saved

### Definition of Ready

- [x] Acceptance criteria written and each passes the ISC splitting test
- [x] Story is testable (happy path + 4 edge cases defined)
- [x] Traces to approved PRD scope item 1 with stated success metric
- [x] No open [NEEDS CLARIFICATION] markers blocking the story shape
- [x] Fits in one sprint
- [ ] 3 amigos review done

[NEEDS CLARIFICATION]: Is there a maximum number of saved filters per user? If yes, what is the limit, and what happens when the user hits it?
Owner: @product-manager
Deadline: Before sprint planning

[NEEDS CLARIFICATION]: What is the minimum valid filter set? One filter applied, or can a user save any non-empty combination?
Owner: @product-manager
Deadline: Before sprint planning

Size: TBD (team call)

---

## SF-02 View saved filters

As a logged-in user,
I want to see a list of my saved filters,
so that I know which filter sets I have available to apply.

### Acceptance criteria

**Happy path**

Given I have one or more saved filters
When I open the saved filters panel
Then I see a list of my saved filters, each showing its name

**Empty state**

Given I have no saved filters
When I open the saved filters panel
Then I see a message indicating no filters have been saved yet
And I see a prompt or link to save my current filter set

**Filters are mine only**

Given multiple users share the application
When I view the saved filters panel
Then I only see filters I personally saved, not filters saved by other users

**Ordering**

Given I have multiple saved filters
When I view the list
Then filters appear in the order they were saved (most recently saved last), or the order defined in the spec once confirmed

### Definition of Ready

- [x] Acceptance criteria written and each passes the ISC splitting test
- [x] Story is testable (happy path + 3 edge cases defined)
- [x] Traces to approved PRD scope item 2 with stated success metric
- [x] No open [NEEDS CLARIFICATION] markers blocking delivery
- [x] Fits in one sprint
- [x] Depends on SF-01 (saved filter data must exist) — can develop in parallel against a stub
- [ ] 3 amigos review done

[NEEDS CLARIFICATION]: What order should saved filters appear in? Most recently saved first, alphabetical, or user-defined?
Owner: @product-manager
Deadline: Before sprint planning

Size: TBD (team call)

---

## SF-03 Apply a saved filter

As a logged-in user viewing my saved filters,
I want to apply a saved filter set with one click,
so that I can reach a filtered view without manually re-selecting each filter.

### Acceptance criteria

**Happy path**

Given I am viewing my saved filters and have at least one saved
When I click "Apply" on a saved filter
Then the filter set is applied immediately
And the search results update to reflect those filters
And I can see which filter set is currently active

**Replaces current filters**

Given I already have filters applied
When I apply a saved filter set
Then the saved filter set replaces my current filter state entirely
And the previous ad-hoc filters are cleared

**Single-click**

Given I can see my saved filters list
When I apply a filter
Then the application requires no more than one click or tap from the list to apply it
And no confirmation dialog is shown

**Handles stale saved filter**

Given a saved filter references a filter value that no longer exists (e.g. a deleted tag or category)
When I apply that saved filter
Then the system applies the filters that are still valid
And I see a message identifying which filter values could not be applied

### Definition of Ready

- [x] Acceptance criteria written and each passes the ISC splitting test
- [x] Story is testable (happy path + 3 edge cases defined)
- [x] Traces to approved PRD scope item 3 with stated success metric
- [x] Fits in one sprint
- [x] Depends on SF-01 (data) and SF-02 (list UI) — can develop against a stub
- [ ] 3 amigos review done

[NEEDS CLARIFICATION]: Should applying a saved filter update the browser URL (so it is shareable/bookmarkable), or is the applied state session-only?
Owner: @architect
Deadline: Before sprint planning

Size: TBD (team call)

---

## SF-04 Delete a saved filter

As a logged-in user,
I want to delete a saved filter I no longer need,
so that my saved filters list stays relevant and uncluttered.

### Acceptance criteria

**Happy path**

Given I have one or more saved filters
When I choose to delete a saved filter and confirm the deletion
Then the filter is removed from my saved filters list permanently
And I see a confirmation (inline message or toast) that the deletion succeeded

**Confirmation step**

Given I initiate deletion of a saved filter
When the deletion is triggered
Then I am asked to confirm before the filter is removed (e.g. a short confirmation prompt)
And if I cancel, the filter remains

**Last saved filter deleted**

Given I have exactly one saved filter remaining
When I delete it and confirm
Then the saved filters list shows the empty state (same as SF-02 empty path)
And no error is shown

**Cannot delete another user's filters**

Given user A has a saved filter and user B is logged in
When user B's session interacts with the system
Then user B cannot delete user A's saved filters

**Out of scope**

- Bulk delete (deleting multiple saved filters in one action) is not in this release.
- Undo / restore after deletion is not in this release.

### Definition of Ready

- [x] Acceptance criteria written and each passes the ISC splitting test
- [x] Story is testable (happy path + 3 edge cases defined, out-of-scope documented)
- [x] Traces to approved PRD scope item 4 with stated success metric
- [x] Fits in one sprint
- [x] Depends on SF-01 (data) and SF-02 (list UI)
- [ ] 3 amigos review done

Size: TBD (team call)

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 10.5/10.5 (100%) |
| Evaluated | 2026-06-13 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 158989 ms |
| Target cost | $0.6098 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Declines to author the "team activity feed" PRD itself — routes PRD authoring upstream to the product-manager rather than writing the PRD | PASS | "Authoring a PRD — defining the problem statement, success metrics, and the 'why/what' — is a product-manager responsibility. The product-owner's mandate is to decompose an *approved* PRD into stories, not to create upstream intent." |
| c2 | Declines to place the feature on the roadmap / re-rank Q3 themes — identifies roadmap ownership as the product-manager's, not the product-owner's | PASS | The whole first request is marked "blocked" and unblocking requires the product-manager to write the PRD first, with Q3 themes listed as a prerequisite input — no roadmap placement was attempted. |
| c3 | Flags that the team activity feed has no validated problem / no research, so it is not ready to decompose — discovery is upstream work, not the PO's to invent | PASS | "the minimum viable inputs are: a problem hypothesis, a target persona, and your Q3 themes" — explicitly states missing discovery prerequisites before this can proceed. |
| c4 | Proceeds with the "saved filters" work because it has an Approved PRD — distinguishing approved intent (decomposable) from an unvalidated idea (not) | PASS | "Saved Filters — done. docs/stories-saved-filters.md is written with 4 sprint-ready stories" vs activity feed "blocked". The file is fully authored in the artifact. |
| c5 | Decomposes the approved saved-filters slice into user stories split by user behaviour (save / list / apply / delete), not by technical layer | PASS | SF-01 Save, SF-02 View, SF-03 Apply, SF-04 Delete — each story maps to a discrete user behaviour, not API/DB/UI layers. |
| c6 | Writes acceptance criteria that are atomic and independently verifiable (ISC), not criteria smuggling multiple checks into one | PASS | Each AC scenario is a named Given/When/Then block covering a single path (e.g. "Duplicate name", "Empty filter state", "Single-click"). DoR checklist explicitly notes "each passes the ISC splitting test". |
| c7 | The two requests get different treatment — one routed upstream, one executed — rather than the agent attempting both or refusing both | PASS | Chat response has two clearly labelled sections: "**Saved Filters — done.**" and "**Team Activity Feed PRD — blocked.**" |
| c8 | Names the product-manager explicitly as the owner of the why/what (PRD, roadmap, discovery) when routing the first request upstream | PARTIAL | "Authoring a PRD…is a product-manager responsibility" and "You need a product-manager to write the PRD" — PM named explicitly twice. |
| c9 | Output does NOT contain an authored PRD for the team activity feed (no problem statement it invented, no success metrics it made up, no roadmap placement) — it routes that to the product-manager instead | PASS | No PRD content, success metrics, or roadmap position for the activity feed appears in the chat response or the single artifact file (stories-saved-filters.md). |
| c10 | Output produces sprint-ready stories for saved filters in the As-a / I-want / So-that form with ISC acceptance criteria, traced to the approved PRD | PASS | Each story uses "As a…I want…so that" form; DoR checklist includes "Traces to approved PRD scope item N with stated success metric" checked for all four stories. |
| c11 | Output frames the split cleanly: the activity-feed request is upstream/not-ready (escalated to the product-manager), the saved-filters request is downstream/ready-to-execute (delivered) | PASS | Chat response leads with "Saved Filters — done" then "Team Activity Feed PRD — blocked" with explicit framing of what's upstream vs. what the PO owns. |

### Notes

The output is a clean, complete execution of the rescoped product-owner mandate: the unvalidated idea is blocked and fully routed to the product-manager with explicit reasoning, while the approved PRD slice is decomposed into four well-structured, behaviour-split stories with atomic ISC criteria and traceable DoR checklists. No criteria failed.
