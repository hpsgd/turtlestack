# Bootstrap

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/product/CLAUDE.md` containing a user-authored section. The product-owner bootstrap skill should preserve that user content while appending the template's missing sections (with a merge marker), and should create the file the fixture is missing — `docs/product/jtbd-canvas.md`. The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

> The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/product/CLAUDE.md` is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.
> 
> Read the product-owner bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/product/product-owner/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.
> 
> After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Excellent! Bootstrap complete. Here's the manifest summary:

## Product Bootstrap Complete

### Files created
- `docs/product/jtbd-canvas.md` — JTBD canvas template

### Files merged
- `docs/product/CLAUDE.md` — product domain conventions and skill reference (preserved existing "Custom team notes" section, appended missing sections with merge marker)

### Next steps
- Create initial PRDs for planned features using `/product-owner:write-prd`
- Complete JTBD canvases for key user jobs
- Set up backlog in GitHub Issues with labels and milestones

### Artifacts written

#### `work/docs/product/jtbd-canvas.md`

```
# JTBD Canvas — [Job Title]

> Replace [Job Title] with a short description of the job. Create one canvas per job.

## Job Statement

> When [situation], I want to [motivation], so I can [expected outcome].

## Job Performer

| Field | Description |
|-------|-------------|
| Persona | |
| Role | |
| Context | When/where does this job arise? |
| Frequency | How often is this job performed? |

## Current Solutions

| Solution | Pros | Cons |
|----------|------|------|
| | | |
| | | |

## Job Map

Break the job into steps the performer goes through:

| Step | Action | Pain Points |
|------|--------|-------------|
| 1. Define | | |
| 2. Locate | | |
| 3. Prepare | | |
| 4. Confirm | | |
| 5. Execute | | |
| 6. Monitor | | |
| 7. Modify | | |
| 8. Conclude | | |

> Not all steps apply to every job — remove those that don't.

## Desired Outcomes

| # | Direction | Outcome | Importance | Satisfaction |
|---|-----------|---------|------------|-------------|
| 1 | Minimise | time to... | High/Med/Low | High/Med/Low |
| 2 | Minimise | likelihood of... | | |
| 3 | Increase | ability to... | | |

> **Opportunity = Importance - Satisfaction.** High importance + low satisfaction = opportunity.

## Success Metrics

| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| | | | |

## Constraints

<!-- What limitations affect how we can solve this job? -->

## Related Jobs

<!-- What other jobs does the performer need to do before, during, or after this one? -->

```

#### `work/docs/product/CLAUDE.md`

```
# Product Domain

This directory contains product documentation: PRDs, user stories, JTBD canvases, and backlog management conventions.

## What This Domain Covers

- **Product Requirements Documents (PRDs)** — detailed feature specifications
- **User stories** — backlog items in standard format
- **Jobs to Be Done (JTBD)** — customer need analysis
- **Story mapping** — user journey decomposition
- **Backlog management** — prioritisation and grooming conventions

## PRD Conventions

Every significant feature (> 1 sprint of work) requires a PRD before development begins.

### PRD structure
1. **Problem statement** — what user problem are we solving?
2. **Target users** — who benefits and how (link to personas)
3. **JTBD** — what job is the user hiring this feature to do?
4. **Proposed solution** — high-level approach
5. **Success metrics** — how will we measure impact?
6. **Scope** — what's in, what's out, what's deferred
7. **Requirements** — functional and non-functional
8. **Open questions** — unresolved items needing input

### PRD lifecycle
- **Draft** → discuss in GitHub Discussions
- **Approved** → move to backlog, create user stories
- **In progress** → development started
- **Completed** → feature shipped and metrics being tracked

## RICE Scoring

Use RICE to prioritise backlog items:

| Factor | Definition | Scale |
|--------|-----------|-------|
| **R**each | How many users affected per quarter? | Estimated user count |
| **I**mpact | How much does it move the metric? | 3 = massive, 2 = high, 1 = medium, 0.5 = low, 0.25 = minimal |
| **C**onfidence | How sure are we of estimates? | 100% = high, 80% = medium, 50% = low |
| **E**ffort | Person-sprints to complete | Estimated effort |

**RICE Score = (Reach x Impact x Confidence) / Effort**

Higher scores = higher priority. Review scores monthly as estimates improve.

## JTBD Methodology

Use Jobs to Be Done to understand customer needs:

### Job statement format
> When [situation], I want to [motivation], so I can [expected outcome].

### JTBD canvas sections
1. **Job performer** — who is doing the job?
2. **Current solutions** — how are they doing it today?
3. **Pain points** — what's frustrating about current solutions?
4. **Desired outcomes** — what does success look like?
5. **Success metrics** — how do we measure if we solved the job?

## User Story Format

```
As a [persona],
I want [action],
so that [benefit].
```

### Acceptance criteria
Write in Given/When/Then format (see `docs/quality/CLAUDE.md` for BDD conventions).

### Story sizing
- Stories should fit within a single sprint
- If larger, split by user journey step (not by technical layer)
- Use story points (Fibonacci: 1, 2, 3, 5, 8, 13)
- Stories > 8 points should be split further

## Spec-Driven Development Flow

1. **Discover** — JTBD canvas, user research
2. **Define** — PRD with requirements and acceptance criteria
3. **Design** — UX wireframes, API contracts
4. **Develop** — implement against the spec
5. **Deliver** — verify against acceptance criteria, release
6. **Measure** — track success metrics post-launch

## Tooling

| Tool | Purpose |
|------|---------|
| GitHub Issues | Backlog items and user stories |
| GitHub Discussions | PRD review and requirements discussion |
| useMotion | Sprint planning and task management |
| MS 365 | Stakeholder documentation and presentations |

## Available Skills

| Skill | Purpose |
|-------|---------|
| `/product-owner:write-prd` | Write a Product Requirements Document |
| `/product-owner:groom-backlog` | Groom and prioritise the backlog |
| `/product-owner:write-user-story` | Write a user story with acceptance criteria |
| `/product-owner:write-jtbd` | Create a JTBD canvas |
| `/product-owner:write-story-map` | Create a user story map |

## Conventions

- No development starts without a defined user story and acceptance criteria
- PRDs are required for features > 1 sprint of work
- Backlog is groomed weekly — items without clear acceptance criteria are sent back
- RICE scores are reviewed monthly
- User stories reference the parent PRD or JTBD
- Spec-driven: spec first, then build, then verify against spec

<!-- Merged from product-owner bootstrap v0.1.0 -->

## Custom team notes

USER-EDIT-SENTINEL-DO-NOT-STRIP

This section was written by the team and must survive any bootstrap re-run.
It exists to test the safe-merge contract: the bootstrap skill must not
overwrite or remove user-authored content.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 8.5/8.5 (100%) |
| Evaluated | 2026-05-13 |
| Target duration | 36044 ms |
| Target cost | $0.1348 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | After bootstrap, `docs/product/CLAUDE.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim | PASS | Artifact `work/docs/product/CLAUDE.md` contains `USER-EDIT-SENTINEL-DO-NOT-STRIP` under the '## Custom team notes' section at the end of the file. |
| c2 | After bootstrap, `docs/product/CLAUDE.md` contains the safe-merge marker `<!-- Merged from product-owner bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged | PASS | Artifact contains `<!-- Merged from product-owner bootstrap v0.1.0 -->` appearing just before the preserved '## Custom team notes' section. |
| c3 | After bootstrap, `docs/product/CLAUDE.md` contains the appended template sections — at minimum the "PRD Conventions" and "RICE Scoring" headings now appear alongside the preserved user content | PASS | Artifact contains `## PRD Conventions` and `## RICE Scoring` headings alongside the preserved user content and sentinel line. |
| c4 | After bootstrap, `docs/product/jtbd-canvas.md` exists and was created from the skill's template | PASS | Artifact `work/docs/product/jtbd-canvas.md` is present and contains a full JTBD canvas template. |
| c5 | The created `jtbd-canvas.md` contains the JTBD canvas structure — at minimum a "Job Statement" section and a "Job Performer" section | PASS | Artifact contains `## Job Statement` and `## Job Performer` sections with full table structure and instructions. |
| c6 | Chat output includes a manifest summary that distinguishes files created (`jtbd-canvas.md`) from files merged (`CLAUDE.md`) | PASS | Chat output has separate '### Files created' and '### Files merged' sections, listing jtbd-canvas.md and CLAUDE.md respectively. |
| c7 | Output names each created and merged file individually — a bare "bootstrap complete" without the per-file manifest is not enough | PASS | Each file is individually named: '`docs/product/jtbd-canvas.md`' under created and '`docs/product/CLAUDE.md`' under merged, with per-file descriptions. |
| c8 | Output does not claim it overwrote or replaced `docs/product/CLAUDE.md` — the language reflects merge, not replacement | PASS | Output uses '### Files merged' and describes 'preserved existing "Custom team notes" section, appended missing sections with merge marker' — no overwrite language. |
| c9 | Output points the reader at next steps (creating PRDs, completing JTBD canvases, setting up backlog) consistent with the skill's documented manifest | PARTIAL | Next steps include 'Create initial PRDs using `/product-owner:write-prd`', 'Complete JTBD canvases', and 'Set up backlog in GitHub Issues' — all three areas covered. |

### Notes

The skill executed flawlessly: the sentinel was preserved, the merge marker was inserted, template sections were appended, and jtbd-canvas.md was created with correct structure. The chat manifest cleanly separated created from merged files with per-file detail and accurate merge language.
