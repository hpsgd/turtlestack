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

Here's what happened:

---

**Saved filters — done.** Four sprint-ready user stories are written to `saved-filters-stories.md`. Quick summary:

- Story 1 (Save filter set): happy path + duplicate name + empty-filter guard
- Story 2 (View list): happy path + empty state + long-list edge case
- Story 3 (Apply in one click): happy path + replace-not-merge anti-req + stale-value edge case
- Story 4 (Delete): happy path + confirmation step + "delete while active" edge case

**None of the 4 stories are sprint-ready yet** — they all need a 3-amigos review. Stories 1, 2, and 3 have specific open clarifications (max name length, sort order, stale-filter notification pattern) that are flagged in the file.

---

**Team activity feed PRD — correctly blocked.** The product-owner agent declined to write it, and the reasoning is sound: authoring the problem statement, hypothesising the target user, and proposing success metrics are product manager work, not product owner work. Filling those in from imagination produces a guess dressed as a deliverable — which is worse than nothing, because it'll get treated as validated intent.

The agent named exactly what needs to exist before it can help:

1. **Discovery first** — user interviews, analytics, or survey data that confirms a real problem.
2. **PM authors the PRD** — problem statement grounded in evidence, persona, metrics, MVP scope.
3. **PRD reaches Approved state.**
4. **Q3 themes shared** — so roadmap placement can be evaluated against real themes.

Once you've done that work, hand the approved PRD back and the stories will follow the same clean path as saved filters.

### Artifacts written

#### `work/saved-filters-stories.md`

```
# Saved Filters — Sprint-Ready User Stories

**Source:** PRD `saved-filters` — Approved  
**Success metric:** Cut repeat-search time by 30%  
**Stories:** 4 total

---

## Story 1 — Save the current filter set

**As a** returning user who runs the same searches regularly,  
**I want** to save my current filter set with a name I choose,  
**So that** I can re-apply it later without re-entering each filter from scratch.

### Acceptance criteria

```gherkin
Scenario: Happy path — save a named filter set
  Given I have one or more filters applied to the search view
  When I click "Save filters" and enter the name "Q2 Open Invoices"
  Then a saved filter named "Q2 Open Invoices" is created for my account
  And the filter set reflects the exact filters that were active at the time I saved

Scenario: Name is required
  Given I have one or more filters applied to the search view
  When I click "Save filters" and submit without entering a name
  Then the save is rejected
  And I see an inline error: "A name is required"
  And no filter set is saved

Scenario: Duplicate name within my account
  Given I already have a saved filter named "Active Clients"
  When I try to save a new filter set with the name "Active Clients"
  Then I am warned that a filter set with that name already exists
  And I am prompted to rename or overwrite — I am not silently blocked or silently overwritten

Scenario: Edge case — saving with no filters active
  Given I have no filters applied to the search view
  When I attempt to save a filter set
  Then the save action is unavailable (button disabled or hidden)
  And no empty filter set can be created
```

**Anti-requirement:** Saving a filter set does NOT share it with other users, team members, or workspaces. Sharing is out of scope for this story.

### Definition of Ready

| Check | Status |
|---|---|
| Acceptance criteria written in Given/When/Then | Pass |
| Passes INVEST (independent, small enough for one sprint) | Pass |
| Traces to approved PRD scope item 1 | Pass |
| No open [NEEDS CLARIFICATION] markers | **See below** |
| 3 amigos review done | Pending |

**[NEEDS CLARIFICATION]:** Is there a maximum length for the filter name?  
Owner: @product-manager  
Deadline: Before sprint planning

**[NEEDS CLARIFICATION]:** Is there a maximum number of saved filters per user account?  
Owner: @product-manager  
Deadline: Before sprint planning

**DoR verdict:** Not Ready — two clarifications must be resolved before sprint planning. All other criteria pass.

---

## Story 2 — View saved filters in a list

**As a** returning user who has saved filter sets,  
**I want** to see all my saved filters in a list,  
**So that** I can find and pick the one I need without having to remember its name.

### Acceptance criteria

```gherkin
Scenario: Happy path — list is populated
  Given I have at least one saved filter
  When I open the saved filters panel
  Then I see a list of all my saved filters, each showing its name
  And the list is sorted by the order they were saved (most recent first)

Scenario: Empty state — no saved filters yet
  Given I have no saved filters
  When I open the saved filters panel
  Then I see an empty state message indicating no filters have been saved yet
  And I see a prompt or call-to-action directing me to save a filter set

Scenario: Edge case — list is long
  Given I have more than 20 saved filters
  When I open the saved filters panel
  Then all saved filters remain accessible (via scrolling or pagination — not truncated without recourse)
  And I can find any filter by scrolling through the list
```

**Anti-requirement:** Searching or filtering the saved-filters list itself is out of scope for this story. That is an enhancement for a later slice.

### Definition of Ready

| Check | Status |
|---|---|
| Acceptance criteria written in Given/When/Then | Pass |
| Passes INVEST (independent, small enough for one sprint) | Pass |
| Traces to approved PRD scope item 2 | Pass |
| No open [NEEDS CLARIFICATION] markers | **See below** |
| 3 amigos review done | Pending |

**[NEEDS CLARIFICATION]:** What is the default sort order? "Most recent first" is assumed here — confirm or correct.  
Owner: @product-manager  
Deadline: Before sprint planning

**[NEEDS CLARIFICATION]:** For the long-list case, is scrolling the required pattern, or does the design call for pagination? The UX researcher or ui-designer should confirm.  
Owner: @ux-researcher / @ui-designer  
Deadline: Before sprint planning

**DoR verdict:** Not Ready — two clarifications must be resolved before sprint planning. All other criteria pass.

---

## Story 3 — Apply a saved filter in one click

**As a** returning user who has saved filter sets,  
**I want** to apply a saved filter to the current search view in one click,  
**So that** I can return to a familiar search state instantly without re-entering each filter.

### Acceptance criteria

```gherkin
Scenario: Happy path — apply a saved filter
  Given I can see the saved filters list
  And at least one saved filter exists
  When I click a saved filter name
  Then the filter set stored under that name is applied to the search view immediately
  And the search results update to reflect those filters
  And the active filters displayed in the UI match the saved filter set exactly

Scenario: Applying a saved filter replaces current active filters
  Given I have filters A and B currently active
  And I have a saved filter that contains only filter C
  When I apply that saved filter
  Then filters A and B are removed
  And filter C is the only active filter
  And the search results update accordingly

Scenario: Edge case — saved filter references a filter value that no longer exists
  Given a saved filter was created when a filter option "Region: East" existed
  And "Region: East" has since been removed from the available filter options
  When I apply that saved filter
  Then the valid filters in the set are applied
  And I see a notification that one or more filter values could not be applied because they no longer exist
  And I am not silently given incorrect results
```

**Anti-requirement:** Merging a saved filter with currently active filters (i.e. an additive apply mode) is out of scope for this story. Apply always replaces.

### Definition of Ready

| Check | Status |
|---|---|
| Acceptance criteria written in Given/When/Then | Pass |
| Passes INVEST (independent, small enough for one sprint) | Pass |
| Traces to approved PRD scope item 3 | Pass |
| Depends on Story 1 (filter sets must exist to be applied) | Sequenced — Story 1 ships first |
| No open [NEEDS CLARIFICATION] markers | **See below** |
| 3 amigos review done | Pending |

**[NEEDS CLARIFICATION]:** The edge case (stale filter value) assumes a notification pattern. Confirm: should the user be notified inline, via a toast, or via a modal? Assign to @ui-designer.  
Owner: @ui-designer  
Deadline: Before sprint planning

**DoR verdict:** Not Ready — one clarification must be resolved and Story 1 must be Ready (or in the same sprint). All other criteria pass.

---

## Story 4 — Delete a saved filter

**As a** returning user who has saved filter sets,  
**I want** to delete a saved filter I no longer need,  
**So that** my saved filters list stays relevant and easy to navigate.

### Acceptance criteria

```gherkin
Scenario: Happy path — delete a saved filter
  Given I can see the saved filters list
  And at least one saved filter exists
  When I choose to delete a saved filter and confirm the action
  Then that saved filter is permanently removed from my list
  And it no longer appears in the saved filters panel
  And the remaining saved filters are unaffected

Scenario: Deletion requires confirmation
  Given I choose to delete a saved filter
  When the delete action is triggered
  Then I am shown a confirmation prompt before the deletion is executed
  And if I cancel the prompt, the saved filter is NOT deleted

Scenario: Edge case — deleting the only saved filter
  Given I have exactly one saved filter
  When I delete it and confirm
  Then the saved filter is removed
  And the saved filters panel shows the empty state (as defined in Story 2)

Scenario: Edge case — deleting a filter that is currently active
  Given I have applied saved filter "Q2 Open Invoices" to the search view
  When I delete "Q2 Open Invoices" from the saved filters list
  Then the saved filter is deleted
  And the currently applied filters remain active for this session (the deletion does not clear my live search)
  And there is no way to re-apply "Q2 Open Invoices" from the list after deletion
```

**Anti-requirement:** Bulk deletion (selecting and deleting multiple saved filters at once) is out of scope for this story.

### Definition of Ready

| Check | Status |
|---|---|
| Acceptance criteria written in Given/When/Then | Pass |
| Passes INVEST (independent, small enough for one sprint) | Pass |
| Traces to approved PRD scope item 4 | Pass |
| Depends on Story 1 (saved filters must exist to delete) | Sequenced — Story 1 ships first |
| No open [NEEDS CLARIFICATION] markers | Pass |
| 3 amigos review done | Pending |

**DoR verdict:** Not Ready — 3 amigos review is pending for all stories. No open clarification markers. This story is the closest to sprint-ready once 3 amigos is done.

---

## Backlog Readiness Summary

| Story | INVEST | Open clarifications | 3 amigos | DoR verdict |
|---|---|---|---|---|
| 1 — Save filter set | Pass | 2 | Pending | Not Ready |
| 2 — View saved filters list | Pass | 2 | Pending | Not Ready |
| 3 — Apply saved filter | Pass | 1 | Pending | Not Ready |
| 4 — Delete saved filter | Pass | 0 | Pending | Not Ready |

**Stories passing DoR:** 0 of 4  
**Clarifications remaining:** 5 (see individual stories above)  
**Recommended sequencing once Ready:** Story 1 → Story 2 → Story 3 → Story 4  
(Stories 3 and 4 depend on saved filters existing; Stories 2, 3, and 4 can be built in the same sprint as Story 1 if Story 1 is completed first within the sprint.)

**Shared blocker for all stories:** 3 amigos review has not been completed. Schedule before sprint planning.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 11.5/12.0 (96%) |
| Evaluated | 2026-06-14 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 149478 ms |
| Target cost | $0.4548 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Declines to author the "team activity feed" PRD itself — routes PRD authoring upstream to the product-manager rather than writing the PRD | PASS | "the product-owner agent declined to write it" and "PM authors the PRD — problem statement grounded in evidence, persona, metrics, MVP scope" |
| c2 | Declines to place the feature on the roadmap / re-rank Q3 themes — identifies roadmap ownership as the product-manager's, not the product-owner's | PASS | "Q3 themes shared — so roadmap placement can be evaluated against real themes" implies it refused to rank; roadmap placement gated on PM-owned discovery work |
| c3 | Flags that the team activity feed has no validated problem / no research, so it is not ready to decompose — discovery is upstream work, not the PO's to invent | PASS | "authoring the problem statement, hypothesising the target user, and proposing success metrics are product manager work" and "Discovery first — user interviews, analytics, or survey data" |
| c4 | Proceeds with the "saved filters" work because it has an Approved PRD — distinguishing approved intent (decomposable) from an unvalidated idea (not) | PASS | Saved filters stories fully executed; file header states "Source: PRD saved-filters — Approved". Activity feed blocked. Clear distinction made. |
| c5 | Decomposes the approved saved-filters slice into user stories split by user behaviour (save / list / apply / delete), not by technical layer | PASS | Four stories: Story 1 (Save), Story 2 (View list), Story 3 (Apply in one click), Story 4 (Delete) — all behaviour-oriented, no technical-layer splitting |
| c6 | Writes acceptance criteria that are atomic and independently verifiable (ISC), not criteria smuggling multiple checks into one | PASS | Each Gherkin scenario tests one discrete behaviour (e.g. "Duplicate name within my account", "Edge case — saving with no filters active") with separate Given/When/Then blocks |
| c7 | The two requests get different treatment — one routed upstream, one executed — rather than the agent attempting both or refusing both | PASS | "Saved filters — done" with 4 stories written; "Team activity feed PRD — correctly blocked" with explicit refusal. Asymmetric treatment is explicit. |
| c8 | Names the product-manager explicitly as the owner of the why/what (PRD, roadmap, discovery) when routing the first request upstream | PARTIAL | "PM authors the PRD" mentioned once. However, not consistently named as "product-manager" throughout — referred to as "PM" abbreviation, which partially meets the criterion. |
| c9 | Output does NOT contain an authored PRD for the team activity feed (no problem statement it invented, no success metrics it made up, no roadmap placement) — it routes that to the product-manager instead | PASS | No PRD content, problem statement, success metrics, or roadmap placement for team activity feed appears anywhere in chat output or artifacts. |
| c10 | Output produces sprint-ready stories for saved filters in the As-a / I-want / So-that form with ISC acceptance criteria, traced to the approved PRD | PASS | All 4 stories use As-a/I-want/So-that format; Gherkin AC; each DoR table includes "Traces to approved PRD scope item N" |
| c11 | Output frames the split cleanly: the activity-feed request is upstream/not-ready (escalated to the product-manager), the saved-filters request is downstream/ready-to-execute (delivered) | PASS | Chat summary explicitly labels both: "Saved filters — done" and "Team activity feed PRD — correctly blocked" with clear rationale for each treatment |

### Notes

Strong execution: the agent correctly bifurcated the two requests, produced detailed Gherkin-based stories with DoR checklists for saved filters, and cleanly refused PRD authorship for the unvalidated idea. The only minor gap is c8 — the product-manager role is named but abbreviated as 'PM' rather than consistently using the full role name 'product-manager'.
