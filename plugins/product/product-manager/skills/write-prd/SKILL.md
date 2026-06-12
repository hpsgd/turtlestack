---
name: write-prd
description: Write a Product Requirements Document from rough notes or a feature idea. Produces a structured PRD with problem validation, user definition, RICE prioritisation, acceptance criteria, and scope.
argument-hint: "[feature idea or rough notes]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Write a PRD for $ARGUMENTS.

The PRD is the product manager's artifact for the why and the what — it forces clarity of thought and
communicates intent. It is an alignment document, not a contract. Based on current best practices from
[Marty Cagan (SVPG)](https://www.svpg.com/four-big-risks/), Lenny Rachitsky, Shreyas Doshi, and
[Teresa Torres](https://www.producttalk.org/opportunity-solution-trees/). Write the PRD only for a
problem discovery has validated — if the problem is unconfirmed, run discovery first
(`/product-manager:write-discovery-plan`). Once the PRD is approved, the product-owner owns the how-we-
demonstrate-it-shipped work: backlog grooming, story maps, sprint readiness.

Follow every step below. Do not skip sections. Mark unknowns with `[NEEDS CLARIFICATION: question]` rather than guessing.

### Size the document first

Match PRD weight to decision weight:

| Effort | Format | Sections required |
|---|---|---|
| < 1 week | Ticket with acceptance criteria | Problem + criteria + scope only |
| 1-4 weeks | One-pager | Steps 1-6 below |
| 1+ month | Full PRD | All steps below |
| Quarter+ | Full PRD + strategy context | All steps + link to OKRs and roadmap |

---

## Mandatory Process

### Step 1: Context and Strategic Fit

Before the problem statement, establish WHY this work matters NOW:

- **Strategic alignment** — which company OKR or product goal does this support? If it doesn't connect to a goal, why are we considering it?
- **Why now** — what changed that makes this urgent? Market shift, customer feedback volume, competitive pressure, technical enabler, or contractual obligation?
- **What happens if we don't do this** — the cost of inaction. If the answer is "nothing much changes," question whether this belongs in the roadmap

### Step 2: Problem Validation

Before writing anything, answer these four questions. If you cannot answer them from the input, mark them `[NEEDS CLARIFICATION]` and proceed with assumptions stated explicitly.

1. **What problem are we solving?** State the problem in one sentence. Not the solution, not the feature — the problem.
2. **Who has this problem?** Name the specific user segment. "Everyone" is not an answer. "Mid-market SaaS ops managers handling 50-200 integrations" is.
3. **How do they solve it today?** Describe the current workaround, even if it is "they don't." Include the cost of the current approach (time, money, frustration, risk).
4. **What evidence do we have?** List concrete evidence: support tickets, user interviews, analytics data, churn reasons, competitor adoption. If none exists, state "No direct evidence — this is a hypothesis" and flag it as a risk.

**Anti-patterns to avoid:**
- "Users want X" without evidence of the underlying problem
- Solution-first PRDs that describe a feature without establishing the problem
- Problems that affect a theoretically large audience but have no supporting data
- Conflating "interesting to build" with "valuable to users"

### Step 3: Target User Definition

Define the primary user precisely. Include all of:

- **Role/title**: What they call themselves
- **Context**: When and where they encounter the problem (not just who they are, but what situation they are in)
- **Technical sophistication**: Can they write code? Use APIs? Or do they need a GUI for everything?
- **Frequency**: How often do they encounter this problem? (Daily pain vs. quarterly annoyance determines urgency)
- **Current tools**: What is in their workflow today that this will interact with?

If there is a secondary user (e.g., an admin who configures something that an end-user consumes), define them too, but mark the primary user clearly.

### Step 4: RICE Prioritisation

Score the initiative before investing in detailed requirements. This forces honest assessment of value vs. effort.

| Factor | Score | Reasoning |
|--------|-------|-----------|
| **Reach** | _N users/quarter_ | How many users/accounts will this affect in the next quarter? Use real numbers from analytics, not guesses. If unknown, state the assumption. |
| **Impact** | _3/2/1/0.5/0.25_ | 3 = massive (transforms workflow), 2 = high (significant improvement), 1 = medium (noticeable), 0.5 = low (minor), 0.25 = minimal |
| **Confidence** | _100%/80%/50%_ | 100% = we have data. 80% = strong signals but some assumptions. 50% = educated guess. |
| **Effort** | _person-weeks_ | Total effort across all disciplines (design, eng, QA). Round up, never down. |

**RICE Score** = (Reach x Impact x Confidence) / Effort

State the score. Compare it to other recent initiatives if context is available. A score below 1.0 should trigger a conversation about whether to proceed.

### Step 5: Success Metrics

Define exactly how we will know this succeeded. Every PRD must have at least one leading and one lagging indicator.

**Leading indicators** (measurable within the first week):
- Adoption rate: what percentage of eligible users try the feature?
- Activation rate: what percentage complete the core action?
- Error rate: does usage produce errors or support tickets?

**Lagging indicators** (measurable after 4-8 weeks):
- Retention impact: do users who adopt this feature retain better?
- Task completion: is the underlying job-to-be-done faster/easier to measure?
- Revenue impact: does this affect conversion, expansion, or churn?

**Guardrail metrics** (must NOT get worse):
- Existing feature usage: does this change break or degrade existing workflows?
- Performance: does page load or API latency regress?
- Support volume: does this generate more support tickets than it resolves?

Guardrails protect against second-order effects. A feature that improves adoption but increases support volume by 3x is not a success.

**Failure definition**: State explicitly what failure looks like. "Less than 10% adoption after 4 weeks" or "no measurable change in time-to-complete" — be specific enough that you can make a kill decision.

### Step 6: User Stories with ISC Acceptance Criteria

Write user stories for every behaviour in scope. Each story follows this format:

```
### US-[N]: [Short title]

As a [specific user type], I want [concrete action] so that [measurable outcome].

**Acceptance Criteria:**
- [ ] [I] — Independent: testable without other criteria
- [ ] [S] — Small: one verifiable behaviour
- [ ] [C] — Complete: includes the boundary condition

**Edge cases:**
- What happens when [empty state]?
- What happens when [error condition]?
- What happens when [concurrent access]?
```

**ISC Splitting Test**: Every acceptance criterion must pass all three:
- **Independent**: Can be verified on its own without setting up other criteria first
- **Small**: Tests exactly one behaviour, not a compound "A and B and C"
- **Complete**: Specifies what happens at the boundaries, not just the happy path

If a criterion fails the ISC test, split it until each part passes. The product-owner will break these
stories down further into the backlog — your job is to specify the behaviour, theirs is to make it
sprint-ready.

### Step 7: Scope Definition

**In scope**: List every capability included in this release. Be specific — "user can filter" is vague; "user can filter by date range, status, and assignee" is specific.

**Out of scope**: List what is deliberately excluded AND state why for each item. Common reasons:
- "Deferred to v2 — valuable but not essential for initial validation"
- "Separate initiative — tracked in [reference]"
- "Descoped due to effort — RICE score drops below threshold with this included"

**Anti-requirements**: Things we are explicitly NOT doing, even though someone might expect them. These prevent scope creep by making exclusions visible.

### Step 8: Risks and Pre-Mortem

Imagine the feature shipped and failed. What went wrong? This is a pre-mortem (Shreyas Doshi's emphasis — anticipate failure before it happens).

**Four risk categories** (Marty Cagan's framework):

| Risk type | Question | Assessment |
|---|---|---|
| **Value risk** | Will users actually want this? | [evidence for/against] |
| **Usability risk** | Can they figure out how to use it? | [complexity assessment] |
| **Feasibility risk** | Can we build it with current tech/team/timeline? | [technical assessment] |
| **Business viability risk** | Does this work for the business? (legal, financial, strategic) | [business assessment] |

**Open questions:**

| Question | Impact if wrong | Owner | Due date |
|---|---|---|---|
| _Specific question_ | _What happens if our assumption is incorrect_ | _Who will answer this_ | _When we need the answer by_ |

**Reversibility:** Is this decision easily reversible (feature flag, config change) or hard to reverse (data migration, public API, pricing change)? Reversible decisions can be made faster with less certainty. Irreversible decisions need more evidence.

### Step 9: Launch Plan

How will this reach users?

- **Rollout strategy:** Big bang / percentage rollout / beta → GA / feature flag
- **Rollback criteria:** What signals would trigger a rollback? (error rate, support volume, performance regression)
- **Monitoring:** What dashboards or alerts need to be in place before launch?
- **Communication:** Who needs to know? (support team, sales team, existing customers, marketing)
- **Documentation:** What docs need to be created or updated before launch?

### Step 10: Technical Constraints (if known)

This section is optional but encouraged. Include only hard constraints, not implementation suggestions.

- **Dependencies**: Other systems, teams, or APIs this relies on
- **Performance requirements**: Latency, throughput, or scale expectations
- **Compliance**: Regulatory or security constraints
- **Data requirements**: What data is needed that may not exist yet

Mark any technical suggestions clearly as `[SUGGESTION — not a requirement]` to avoid constraining engineering prematurely.

---

## Quality Checklist

Before finalising the PRD, verify:

- [ ] Strategic fit stated — connects to a company OKR or product goal
- [ ] "Why now" is answered — urgency or timing is clear
- [ ] Problem is stated without referencing the solution
- [ ] Problem is validated by discovery, not assumed
- [ ] Target user is specific enough that you could recruit them for a user test
- [ ] RICE score is calculated with stated assumptions
- [ ] Every acceptance criterion passes the ISC Splitting Test
- [ ] At least one leading, one lagging, and one guardrail metric defined
- [ ] Failure condition is explicitly defined
- [ ] Out-of-scope items include reasoning
- [ ] Four risk categories assessed (value, usability, feasibility, viability)
- [ ] Reversibility assessed
- [ ] Launch plan includes rollback criteria
- [ ] All unknowns are captured with owners and due dates
- [ ] No implementation details masquerading as requirements
- [ ] PRD is understandable by someone who was not in the room when it was discussed

---

## Output Format

Write the PRD to `docs/product/prd-[feature-name].md`. Use the structure above as the document structure. Include the RICE score in the document header as metadata:

```
# PRD: [Feature Name]

| Field | Value |
|-------|-------|
| Author | [name] |
| Status | Draft |
| RICE Score | [N] |
| Target release | [quarter or date] |
| Last updated | [date] |
```

Every `[NEEDS CLARIFICATION]` marker is a follow-up item. List them all in a summary at the end of the document under "## Open Items Requiring Clarification."

## Related Skills

- `/product-manager:write-jtbd` — frame the problem as a customer job before writing the PRD. The core job becomes the problem statement.
- `/product-manager:write-roadmap` — the PRD's outcome should map to a roadmap item.
- `/product-owner:write-user-story` — the product-owner breaks the PRD into implementable, sprint-ready user stories.
- `/product-owner:groom-backlog` — the product-owner prioritises the resulting stories into the backlog.
