# Bootstrap

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/architecture/_sections/architect.md` fragment containing a user-authored section. The architect bootstrap skill should preserve that user content while appending the template's missing sections (with a merge marker), and should create the two files the fixture is missing — `adr/0001-use-adr-process.md` and `system-design.md`. The architect never writes `docs/architecture/CLAUDE.md` directly — the coordinator assembles it from the fragments in `_sections/`. The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

> The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/architecture/_sections/architect.md` fragment is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.
> 
> Read the architect bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/engineering/architect/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.
> 
> After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Architecture Bootstrap Complete

### Files created
- `docs/architecture/adr/0001-use-adr-process.md` — initial ADR establishing the ADR process for TestProject
- `docs/architecture/system-design.md` — system design template with arc42 sections

### Files merged
- `docs/architecture/_sections/architect.md` — appended 11 sections (What This Domain Covers, ADR Conventions, C4 Model Levels, arc42 Structure, API Design Guidelines, Tooling, Available Skills, Conventions) while preserving existing "Custom team notes" section with USER-EDIT-SENTINEL

### Next steps
- Fill in `system-design.md` with TestProject-specific requirements, constraints, and architecture details
- Use `/architect:write-adr` for subsequent architecture decisions
- The `docs/architecture/CLAUDE.md` coordinator will assemble `architect.md` with stack-developer domain fragments when ready

### Artifacts written

#### `work/docs/architecture/system-design.md`

```
# System Design — TestProject

> Replace [Project Name] with the actual project name. Fill in each section as the architecture evolves.

## 1. Introduction and Goals

### Requirements Overview
<!-- Key functional requirements driving the architecture -->

### Quality Goals
<!-- Top 3–5 quality attributes (e.g., performance, security, scalability) -->

| Priority | Quality Attribute | Scenario |
|----------|------------------|----------|
| 1 | | |
| 2 | | |
| 3 | | |

## 2. Constraints

### Technical Constraints
<!-- Technology mandates, existing systems, infrastructure limits -->

### Organisational Constraints
<!-- Team size, budget, timeline, compliance requirements -->

## 3. Context and Scope

### System Context (C4 Level 1)

```mermaid
C4Context
    title System Context Diagram
    Person(user, "User", "Primary user of the system")
    System(system, "System", "The system being designed")
    System_Ext(ext, "External System", "External dependency")
    Rel(user, system, "Uses")
    Rel(system, ext, "Integrates with")
```

## 4. Solution Strategy

<!-- Key technology decisions and architectural patterns chosen -->

## 5. Building Block View

### Container Diagram (C4 Level 2)

<!-- Deployable units: applications, databases, message queues -->

### Component Overview

<!-- Major components within each container -->

## 6. Deployment View

<!-- How containers map to infrastructure -->

## 7. Crosscutting Concepts

### Authentication & Authorisation
<!-- Auth approach -->

### Error Handling
<!-- Error strategy -->

### Logging & Observability
<!-- Logging, tracing, metrics approach -->

## 8. Architecture Decisions

See [ADR index](adr/) for all architecture decision records.

## 9. Risks and Technical Debt

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| | | | |

```

#### `work/docs/architecture/adr/0001-use-adr-process.md`

```
# ADR-0001: Use ADR Process for Architecture Decisions

## Status

Accepted

## Date

2026-06-15

## Context

Architecture decisions are currently made informally and not documented. This leads to repeated discussions, unclear rationale, and difficulty onboarding new team members.

## Decision

We will use Architecture Decision Records (ADRs) following the MADR v3.0 format to document all significant architecture decisions.

ADRs will be:
- Stored in `docs/architecture/adr/`
- Numbered sequentially (`0001`, `0002`, etc.)
- Reviewed via pull requests
- Immutable once accepted (superseded by new ADRs if changed)

## Consequences

### Positive
- Decisions are discoverable and searchable
- New team members can understand historical context
- Decision rationale is preserved even after people leave
- Review process ensures broader input

### Negative
- Small overhead per decision (mitigated by templates)
- Risk of analysis paralysis (mitigated by clear "when to write" guidelines)

## Confirmation

- ADR directory exists and is used for new decisions
- Team references ADRs in pull requests and discussions

```

#### `work/docs/architecture/_sections/architect.md`

```
<!-- architect fragment of the architecture domain doc. Assembled into docs/architecture/CLAUDE.md by the coordinator. -->

## Custom team notes

USER-EDIT-SENTINEL-DO-NOT-STRIP

This section was written by the team and must survive any bootstrap re-run.
It exists to test the safe-merge contract: the bootstrap skill must not
overwrite or remove user-authored content.

<!-- Merged from architect bootstrap v0.1.0 -->

## What This Domain Covers

- **Architecture Decision Records (ADRs)** — capturing significant technical decisions
- **System design** — C4 model diagrams, arc42 documentation, component relationships
- **API design** — REST/GraphQL/gRPC contract guidelines
- **Technology evaluation** — structured assessments of technology choices

## ADR Conventions

We use **MADR** (Markdown Any Decision Records) v3.0 format.

### ADR numbering

- Sequential four-digit numbers: `0001`, `0002`, etc.
- Store in `docs/architecture/adr/`
- File naming: `NNNN-kebab-case-title.md`

### ADR statuses

| Status | Meaning |
|--------|---------|
| Proposed | Under discussion — not yet decided |
| Accepted | Decision made and active |
| Deprecated | Superseded by a later ADR |
| Superseded | Replaced — link to replacement ADR |

### When to write an ADR

Write an ADR when the decision:
- Affects the system's structure (service boundaries, data flow, API contracts)
- Is expensive to reverse (technology choices, database schema, authentication)
- Will be questioned later ("why did we do it this way?")
- Affects multiple teams or domains

Do NOT write an ADR for trivial choices, decisions already covered by conventions, or temporary decisions revisited within a sprint.

## C4 Model Levels

Use the C4 model for structural documentation:

| Level | Name | Shows | Audience |
|-------|------|-------|----------|
| 1 | System Context | System + external actors | Everyone |
| 2 | Container | Deployable units (apps, DBs, queues) | Technical staff |
| 3 | Component | Major components within a container | Developers |
| 4 | Code | Class/module detail (rarely needed) | Developers |

Prefer Mermaid for diagrams. Keep Level 4 diagrams only where truly necessary.

## arc42 Structure

For full system documentation, follow the arc42 template sections:
1. Introduction and Goals
2. Constraints
3. Context and Scope
4. Solution Strategy
5. Building Block View
6. Runtime View
7. Deployment View
8. Crosscutting Concepts
9. Architecture Decisions (→ link to ADRs)
10. Quality Requirements
11. Risks and Technical Debt
12. Glossary

Not every project needs all 12 sections. Start with sections 1–5 and expand as needed.

## API Design Guidelines

- Use OpenAPI 3.1 for REST API specifications
- Follow resource-oriented design: nouns for resources, HTTP verbs for actions
- Version APIs via URL path (`/v1/`) for breaking changes
- Use consistent error response format with `code`, `message`, and `details`
- Document all endpoints before implementation (spec-driven development)

## Tooling

| Tool | Purpose |
|------|---------|
| GitHub Discussions | RFCs and architecture proposals |
| GitHub Pull Requests | ADR review and approval |
| Mermaid | Diagrams (embedded in Markdown) |

## Available Skills

| Skill | Purpose |
|-------|---------|
| `/architect:write-adr` | Write an Architecture Decision Record |
| `/architect:system-design` | Create system design documentation |
| `/architect:api-design` | Design API contracts |
| `/architect:evaluate-technology` | Structured technology evaluation |

## Conventions

- Every significant decision gets an ADR — no exceptions
- ADRs are immutable once accepted; create a new ADR to supersede
- System design docs live in `docs/architecture/`
- Link ADRs from relevant code via comments where the decision applies
- Review ADRs in PRs with at least one architect or tech lead approval

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 10.5/10.5 (100%) |
| Evaluated | 2026-06-15 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 56869 ms |
| Target cost | $0.1023 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | After bootstrap, `docs/architecture/_sections/architect.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim | PASS | The artifact `work/docs/architecture/_sections/architect.md` contains `USER-EDIT-SENTINEL-DO-NOT-STRIP` under the `## Custom team notes` section. |
| c2 | After bootstrap, `docs/architecture/_sections/architect.md` contains the safe-merge marker `<!-- Merged from architect bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged | PASS | The artifact contains `<!-- Merged from architect bootstrap v0.1.0 -->` immediately after the user section and before the appended template sections. |
| c3 | After bootstrap, `docs/architecture/_sections/architect.md` contains the appended template sections — at minimum the "ADR Conventions" and "C4 Model Levels" headings now appear alongside the preserved user content | PASS | The artifact contains both `## ADR Conventions` and `## C4 Model Levels` headings alongside the preserved `## Custom team notes` section. |
| c4 | The architect fragment is authored at H2 and below — it does not introduce a `# Architecture Domain` H1 (the coordinator generates that when it assembles `docs/architecture/CLAUDE.md`) | PASS | The artifact `_sections/architect.md` only contains H2-level headings (`##`). No H1 (`#`) heading is present in the file. |
| c5 | After bootstrap, `docs/architecture/adr/0001-use-adr-process.md` exists and was created from the skill's template | PASS | The artifact `work/docs/architecture/adr/0001-use-adr-process.md` exists with content matching an ADR template including Status, Date, Context, Decision, and Consequences sections. |
| c6 | The created `adr/0001-use-adr-process.md` has a real ISO date in its `Date` section, not the literal placeholder `{CURRENT_DATE}` | PASS | The ADR artifact contains `## Date  2026-06-15` — a real ISO date, not a placeholder. |
| c7 | After bootstrap, `docs/architecture/system-design.md` exists and was created from the skill's template (contains a `## 1. Introduction and Goals` heading and a Mermaid C4Context block) | PASS | The artifact `work/docs/architecture/system-design.md` contains `## 1. Introduction and Goals` and a `C4Context` Mermaid block in section 3. |
| c8 | Chat output includes a manifest summary that distinguishes files created (`adr/0001-use-adr-process.md`, `system-design.md`) from files merged (`_sections/architect.md`) | PASS | Chat output has separate `### Files created` (listing ADR and system-design.md) and `### Files merged` (listing _sections/architect.md) sections. |
| c9 | Output names each created and merged file individually — a bare "bootstrap complete" without the per-file manifest is not enough | PASS | Each file is individually named: `docs/architecture/adr/0001-use-adr-process.md`, `docs/architecture/system-design.md`, and `docs/architecture/_sections/architect.md`. |
| c10 | Output does not claim it overwrote or replaced `docs/architecture/_sections/architect.md` — the language reflects merge, not replacement | PASS | Chat output says `architect.md — appended 11 sections... while preserving existing "Custom team notes" section` — merge language, not overwrite. |
| c11 | Output points the reader at next steps (filling in `system-design.md`, using `/architect:write-adr` for further decisions) consistent with the skill's documented manifest | PARTIAL | Chat output `### Next steps` section mentions filling in `system-design.md` and using `/architect:write-adr` for subsequent decisions. |

### Notes

The skill executed flawlessly: sentinel preserved, merge marker present, all template sections appended, both missing files created with correct content, and the manifest summary is complete and accurate. All criteria met at ceiling.
