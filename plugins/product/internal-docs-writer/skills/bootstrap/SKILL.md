---
name: bootstrap
description: "Bootstrap the internal documentation conventions for a project. Appends architecture doc, runbook, changelog, and post-mortem conventions to docs/content/CLAUDE.md. Idempotent — merges missing sections into existing files without overwriting."
argument-hint: "[project name]"
user-invocable: false
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Bootstrap Internal Documentation

Bootstrap the internal documentation conventions for **$ARGUMENTS**.

## Process

### Step 1: Check and create domain directory

```bash
mkdir -p docs/content
```

### Step 2: Create or merge files

For each file below, apply the safe merge pattern:
- If file does not exist → create from template
- If file exists → read both, find sections in template missing from file, append missing sections with `<!-- Merged from internal-docs-writer bootstrap v0.1.0 -->`

#### File 1: `docs/content/CLAUDE.md` — APPEND

**Important:** This file may already exist (created by `developer-docs-writer:bootstrap`). If it exists, APPEND the sections below that are missing. If it does not exist, create it with BOTH the header and the content below.

If the file does not exist, start with this header before the content below:

```markdown
# Content Domain

This directory contains documentation conventions and content standards.
```

Append this content (~60 lines):

```markdown
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

### Step 3: Return manifest

After creating/merging all files, output a summary:

```
## Internal Docs Bootstrap Complete

### Files merged
- `docs/content/CLAUDE.md` — appended internal documentation conventions

### Next steps
- Write architecture documentation using `/internal-docs-writer:write-architecture-doc`
- Create runbooks for production services using `/internal-docs-writer:write-runbook`
- Set up changelog using `/internal-docs-writer:write-changelog`
```
