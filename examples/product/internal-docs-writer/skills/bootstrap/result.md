# Bootstrap

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/content/_sections/internal-docs-writer.md` fragment containing a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`. The internal-docs-writer bootstrap skill should preserve that user content while appending the template's internal documentation sections (with a merge marker), and output a manifest listing the fragment and next steps. The skill writes only its own fragment under `docs/content/_sections/` — `docs/content/CLAUDE.md` is assembled later by the coordinator, so the three content writers never collide on it. The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

> The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/content/_sections/internal-docs-writer.md` fragment is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.
> 
> Read the internal-docs-writer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/product/internal-docs-writer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.
> 
> After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Internal Docs Bootstrap Complete

### Files created
- (none)

### Files merged
- `docs/content/_sections/internal-docs-writer.md` — internal-docs-writer's fragment of the content domain doc (assembled into `docs/content/CLAUDE.md` by the coordinator); preserved custom team notes and appended missing template sections

### Next steps
- Write architecture documentation using `/internal-docs-writer:write-architecture-doc`
- Create runbooks for production services using `/internal-docs-writer:write-runbook`
- Set up changelog using `/internal-docs-writer:write-changelog`

### Artifacts written

#### `work/docs/content/_sections/internal-docs-writer.md`

```
## Custom team notes

USER-EDIT-SENTINEL-DO-NOT-STRIP

This section was written by the team and must survive any bootstrap re-run.
It exists to test the safe-merge contract: the bootstrap skill must not
overwrite or remove user-authored content.

<!-- Merged from internal-docs-writer bootstrap v0.1.0 -->

## Internal Documentation

This section covers architecture documentation format, runbook conventions, changelog format, and post-mortem templates.

### What Internal Docs Covers

- **Architecture documentation** — arc42-format system documentation
- **Runbooks** — operational procedures for incident response and maintenance
- **Changelogs** — structured release history
- **Post-mortems** — blameless incident analysis

### Architecture Documentation Format (arc42)

Architecture docs follow the [arc42](https://arc42.org/) template:

| Section | Purpose | When to Write |
|---------|---------|---------------|
| 1. Introduction & Goals | Business context, quality goals | Project start |
| 2. Constraints | Technical and organisational limits | Project start |
| 3. Context & Scope | System boundaries and external interfaces | Project start |
| 4. Solution Strategy | Key technology and pattern decisions | After ADRs |
| 5. Building Block View | Component decomposition (C4 levels) | Ongoing |
| 6. Runtime View | Key interaction sequences | As features ship |
| 7. Deployment View | Infrastructure and deployment topology | Before production |
| 8. Crosscutting Concepts | Auth, logging, error handling patterns | Ongoing |
| 9. Architecture Decisions | Link to ADR index | Ongoing |
| 10. Quality Requirements | Quality scenarios and metrics | Project start |
| 11. Risks & Technical Debt | Known risks and debt register | Ongoing |
| 12. Glossary | Domain terms and definitions | Ongoing |

Start with sections 1–5. Add remaining sections as the project matures.

### Runbook Conventions

Runbooks are stored in GitHub Wiki and follow this structure:

| Section | Purpose |
|---------|---------|
| **Title** | System or procedure name |
| **When to use** | Trigger conditions (alert name, symptom, schedule) |
| **Prerequisites** | Required access, tools, permissions |
| **Steps** | Numbered procedure — one action per step |
| **Verification** | How to confirm the procedure succeeded |
| **Rollback** | How to undo if something goes wrong |
| **Escalation** | Who to contact if the runbook doesn't resolve the issue |

### Runbook rules
- Every production alert must have a linked runbook
- Steps must be copy-pasteable — include exact commands, not descriptions
- Runbooks are tested quarterly (dry-run or tabletop exercise)
- Update runbooks immediately after any incident where the runbook was insufficient

### Changelog Format (Keep a Changelog)

Follow [Keep a Changelog](https://keepachangelog.com/) format:

| Category | Description |
|----------|-------------|
| **Added** | New features |
| **Changed** | Changes to existing functionality |
| **Deprecated** | Features that will be removed |
| **Removed** | Features that have been removed |
| **Fixed** | Bug fixes |
| **Security** | Vulnerability fixes |

### Changelog rules
- Changelog is updated in the same PR as the code change
- Entries are written for users, not developers ("Added export to CSV" not "Added ExportService")
- Unreleased changes go under an `[Unreleased]` heading
- Release versions follow Semantic Versioning

### Post-Mortem Template

Post-mortems are blameless and follow this structure:

| Section | Purpose |
|---------|---------|
| **Incident summary** | What happened, duration, impact |
| **Timeline** | Chronological sequence of events (UTC) |
| **Root cause** | Underlying cause (use 5 Whys) |
| **Contributing factors** | Other factors that made the incident worse |
| **What went well** | Things that helped during the response |
| **What went poorly** | Things that hindered the response |
| **Action items** | Specific, assigned, time-bound improvements |

### Post-mortem rules
- Written within 48 hours of incident resolution
- Reviewed in a blameless post-mortem meeting
- Action items tracked in GitHub Issues with `post-mortem` label
- Published to GitHub Wiki for organisational learning

### Internal Docs Tooling

| Tool | Purpose |
|------|---------|
| GitHub Wiki | Runbooks, post-mortems, operational documentation |
| GitHub (in-repo) | Architecture docs in `docs/`, changelogs |

### Available Internal Docs Skills

| Skill | Purpose |
|-------|---------|
| `/internal-docs-writer:write-architecture-doc` | Write arc42 architecture documentation |
| `/internal-docs-writer:write-runbook` | Write an operational runbook |
| `/internal-docs-writer:write-changelog` | Write or update a changelog |

### Internal Docs Conventions

- Architecture docs are updated when the system changes — treat stale docs as bugs
- Every production service has at least one runbook
- Changelogs are maintained per-release, not retroactively
- Post-mortems are blameless — focus on systems, not individuals
- Runbooks are tested regularly — an untested runbook is an unreliable runbook

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 9.5/9.5 (100%) |
| Evaluated | 2026-06-15 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 31506 ms |
| Target cost | $0.0708 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | PASS: After bootstrap, `docs/content/_sections/internal-docs-writer.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim | PASS | Artifact contains 'USER-EDIT-SENTINEL-DO-NOT-STRIP' on its own line, plus the full 'Custom team notes' section text unchanged. |
| c2 | PASS: After bootstrap, `docs/content/_sections/internal-docs-writer.md` contains the safe-merge marker `<!-- Merged from internal-docs-writer bootstrap v0.1.0 -->` — missing sections were appended, not silently merged | PASS | Artifact contains exact marker: '<!-- Merged from internal-docs-writer bootstrap v0.1.0 -->' between the user section and appended template sections. |
| c3 | PASS: After bootstrap, `docs/content/_sections/internal-docs-writer.md` contains the appended template sections — at minimum the "Runbook Conventions" and "Post-Mortem Template" headings now appear alongside the preserved user content | PASS | Artifact contains '### Runbook Conventions' and '### Post-Mortem Template' headings after the merge marker. |
| c4 | PASS: After bootstrap, `docs/content/_sections/internal-docs-writer.md` contains the "Internal Docs Conventions" section — confirming the full template was appended, not just a partial fragment | PASS | Artifact contains '### Internal Docs Conventions' section with multiple bullet points about architecture docs, runbooks, changelogs, post-mortems. |
| c5 | PASS: The skill did not create or write `docs/content/CLAUDE.md` — that file is the coordinator's to assemble from the `_sections/` fragments | PASS | Artifacts only show `work/docs/content/_sections/internal-docs-writer.md`. No `docs/content/CLAUDE.md` artifact appears. |
| c6 | PASS: Chat output includes a manifest that names `docs/content/_sections/internal-docs-writer.md`, consistent with the skill's documented manifest shape | PASS | Chat response 'Files merged' section explicitly names '`docs/content/_sections/internal-docs-writer.md`'. |
| c7 | PASS: Output names `docs/content/_sections/internal-docs-writer.md` individually — a bare "bootstrap complete" without the per-file listing is not enough | PASS | The manifest lists the file individually under 'Files merged' with a description, not just a generic completion notice. |
| c8 | PASS: Output does not claim it overwrote or replaced the fragment — the language reflects merge or append, not replacement | PASS | Chat says 'preserved custom team notes and appended missing template sections' — merge/append language, no overwrite/replace claim. |
| c9 | PARTIAL: Output points the reader at next steps referencing at least one `/internal-docs-writer:*` skill, consistent with the skill's documented manifest | PARTIAL | Next steps list three `/internal-docs-writer:*` skills: write-architecture-doc, write-runbook, write-changelog. |

### Notes

All criteria passed fully. The artifact perfectly demonstrates the safe-merge pattern: sentinel line preserved, merge marker present, full template appended, CLAUDE.md untouched, and the chat manifest accurately reflects the merge operation with correct next-step skill references.
