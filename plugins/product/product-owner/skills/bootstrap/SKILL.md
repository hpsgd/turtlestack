---
name: bootstrap
bootstrap-phase: product
description: "Bootstrap the product documentation structure for a project. Creates docs/product/, generates initial templates, and writes the product-owner fragment of the product domain doc. Idempotent — merges missing sections into existing files without overwriting."
argument-hint: "[project name]"
user-invocable: false
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Bootstrap Product Documentation

Bootstrap the product documentation structure for **$ARGUMENTS**.

## Process

### Step 1: Check and create domain directory

```bash
mkdir -p docs/product/_sections
```

### Step 2: Create or merge files

For each file below, apply the safe merge pattern:
- If file does not exist → create from template
- If file exists → read both, find sections in template missing from file, append missing sections with `<!-- Merged from product-owner bootstrap v0.1.0 -->`

#### Fragment: `docs/product/_sections/product-owner.md`

`docs/product/CLAUDE.md` is **assembled by the coordinator** from the fragments in `_sections/` — no plugin
writes it directly, so the product-owner and product-manager never collide on it. Write the product-owner's
contribution as this fragment. It starts at H2 (the coordinator generates the `# Product Domain` H1):

```markdown
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
```

#### File 2: `docs/product/jtbd-canvas.md`

Create with this content:

```markdown
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

### Step 3: Return manifest

After creating/merging all files, output a summary:

```
## Product Bootstrap Complete

### Files created
- `docs/product/_sections/product-owner.md` — product-owner's fragment of the product domain doc (assembled into `docs/product/CLAUDE.md` by the coordinator)
- `docs/product/jtbd-canvas.md` — JTBD canvas template

### Files merged
- (list any existing files where sections were appended)

### Next steps
- Create initial PRDs for planned features using `/product-owner:write-prd`
- Complete JTBD canvases for key user jobs
- Set up backlog in GitHub Issues with labels and milestones
```
