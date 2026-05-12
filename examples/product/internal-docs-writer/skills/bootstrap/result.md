# Bootstrap

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/content/CLAUDE.md` containing a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`. The internal-docs-writer bootstrap skill should preserve that user content while appending the template's internal documentation sections (with a merge marker), and output a manifest listing the merged file and next steps. The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

> The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/content/CLAUDE.md` is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.
> 
> Read the internal-docs-writer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/product/internal-docs-writer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.
> 
> After the bootstrap completes, output the manifest summary the skill defines (files merged, next steps).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Internal Docs Bootstrap Complete

### Files merged
- `docs/content/CLAUDE.md` — appended internal documentation conventions

**Merge details:**
- Existing user-authored "Custom team notes" section preserved intact
- Missing "Internal Documentation" section appended with merge marker
- Safe-merge pattern applied: no user content overwritten

### Next steps
- Write architecture documentation using `/internal-docs-writer:write-architecture-doc`
- Create runbooks for production services using `/internal-docs-writer:write-runbook`
- Set up changelog using `/internal-docs-writer:write-changelog`

### Artifacts written

#### `work/docs/content/CLAUDE.md`

```
# Content Domain

This directory contains documentation conventions and content standards.

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
| Score | 7.5/7.5 (100%) |
| Evaluated | 2026-05-13 |
| Target duration | 29902 ms |
| Target cost | $0.0779 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | After bootstrap, `docs/content/CLAUDE.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim | PASS | Artifact contains the exact line `USER-EDIT-SENTINEL-DO-NOT-STRIP` under the 'Custom team notes' section, with surrounding user-authored text intact. |
| c2 | After bootstrap, `docs/content/CLAUDE.md` contains the safe-merge marker `<!-- Merged from internal-docs-writer bootstrap v0.1.0 -->` — missing sections were appended, not silently merged | PASS | Artifact contains the exact string `<!-- Merged from internal-docs-writer bootstrap v0.1.0 -->` placed between user content and appended template sections. |
| c3 | After bootstrap, `docs/content/CLAUDE.md` contains the appended template sections — at minimum the "Runbook Conventions" and "Post-Mortem Template" headings now appear alongside the preserved user content | PASS | Artifact contains both `### Runbook Conventions` and `### Post-Mortem Template` headings with full content appended after the merge marker. |
| c4 | After bootstrap, `docs/content/CLAUDE.md` contains the "Internal Docs Conventions" section — confirming the full template was appended, not just a partial fragment | PASS | Artifact contains `### Internal Docs Conventions` section near the end with bullet points about doc update policy, runbooks, changelogs, and post-mortems. |
| c5 | Chat output includes a manifest that names `docs/content/CLAUDE.md` as a merged file, consistent with the skill's documented manifest shape | PASS | Chat response has '### Files merged' section listing `- \`docs/content/CLAUDE.md\` — appended internal documentation conventions'. |
| c6 | Output names `docs/content/CLAUDE.md` individually — a bare "bootstrap complete" without the per-file listing is not enough | PASS | The file path `docs/content/CLAUDE.md` is explicitly named in the manifest under 'Files merged', not buried in a generic completion message. |
| c7 | Output does not claim it overwrote or replaced `docs/content/CLAUDE.md` — the language reflects merge or append, not replacement | PASS | Chat says 'appended internal documentation conventions', 'preserved intact', 'appended with merge marker', 'Safe-merge pattern applied: no user content overwritten'. |
| c8 | Output points the reader at next steps referencing at least one `/internal-docs-writer:*` skill, consistent with the skill's documented manifest | PARTIAL | Next steps list three skills: `/internal-docs-writer:write-architecture-doc`, `/internal-docs-writer:write-runbook`, `/internal-docs-writer:write-changelog`. |

### Notes

The skill executed flawlessly: sentinel preserved, merge marker present, full template appended, and manifest correctly structured. All criteria met at ceiling.
