# Bootstrap

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a root `CLAUDE.md` containing a user-authored section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`, and a `package.json` indicating a TypeScript/JavaScript project. The coding-standards bootstrap skill should preserve user content in root `CLAUDE.md` while appending a "Coding Standards" section, create `docs/tooling-register.md` from the template, detect TypeScript/JavaScript as a language, and output a manifest with the sections the skill defines. Rule installation is the thinking plugin's responsibility (its SessionStart hook) and is explicitly out of scope for this skill. The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

> The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A root `CLAUDE.md` is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`. A `package.json` is also present, indicating a TypeScript/JavaScript project.
> 
> Read the coding-standards bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/practices/coding-standards/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.
> 
> After the bootstrap completes, output the manifest summary the skill defines (Files created, CLAUDE.md updated, Files merged, Detected languages, Next steps).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Coding Standards Bootstrap Complete

### Files created
- `docs/tooling-register.md` — project tooling register

### CLAUDE.md updated
- Appended "Coding Standards" section to root CLAUDE.md (with safe-merge marker)

### Files merged
- (none — tooling register was new)

### Detected languages
- TypeScript / JavaScript (package.json detected)

### Next steps
- Review and customise `docs/tooling-register.md` with project-specific tools
- Configure SonarCloud quality gates
- Ensure the `thinking` plugin is enabled so language-specific rules are installed into `.claude/rules/`
- Use `/coding-standards:review-typescript` for code review

### Artifacts written

#### `work/package.json`

```
{
  "name": "testproject",
  "version": "0.1.0",
  "description": "TestProject — synthetic fixture for coding-standards bootstrap test"
}

```

#### `work/CLAUDE.md`

```
# TestProject

This is the project root CLAUDE.md.

## Custom team notes

USER-EDIT-SENTINEL-DO-NOT-STRIP

This section was written by the team and must survive any bootstrap re-run.
It tests the safe-merge contract: the bootstrap skill must not overwrite or
remove user-authored content when it appends the Coding Standards section.

## Coding Standards

<!-- Merged from coding-standards bootstrap v0.1.0 -->

### Active Standards

| Standard | Enforced By | Scope |
|----------|-------------|-------|
| Linting | CI (GitHub Actions) | All code |
| Formatting | CI + pre-commit hook | All code |
| Type checking | CI | TypeScript / Python (if applicable) |
| Code review | GitHub PR review | All changes |
| Static analysis | SonarCloud | All code |

### Code Review Process

1. Author creates PR with description and linked issue
2. CI runs all quality gates (lint, test, coverage, security)
3. Reviewer checks against coding standards
4. At least one approval required before merge
5. Author merges after approval and green CI

### SonarCloud Integration

- Quality gate runs on every PR
- Coverage threshold: project-specific (see SonarCloud config)
- No new critical or blocker issues allowed
- Technical debt ratio must not increase

### Available Review Skills

| Skill | Purpose |
|-------|---------|
| `/coding-standards:review-standards` | General code standards review |
| `/coding-standards:review-git` | Git commit and branching conventions |
| `/coding-standards:review-typescript` | TypeScript-specific review |
| `/coding-standards:review-python` | Python-specific review |
| `/coding-standards:review-dotnet` | .NET-specific review |

> Only use the review skills matching your project's languages.

```

#### `work/docs/tooling-register.md`

```
# Tooling Register

This document tracks all tools, services, and platforms used by the project.

## Development Tools

| Tool | Purpose | Owner | URL |
|------|---------|-------|-----|
| GitHub | Source control, issues, PRs | Engineering | https://github.com |
| GitHub Actions | CI/CD pipelines | DevOps | https://github.com/features/actions |
| SonarCloud | Code quality and security analysis | Engineering | https://sonarcloud.io |
| Vercel | Frontend deployment | DevOps | https://vercel.com |

## Communication & Collaboration

| Tool | Purpose | Owner | URL |
|------|---------|-------|-----|
| GitHub Discussions | Technical RFCs, architecture proposals | Engineering | |
| GitHub Issues | Work tracking, bug reports | Product | |
| GitHub Wiki | Operational runbooks | DevOps | |

## Infrastructure

| Tool | Purpose | Owner | URL |
|------|---------|-------|-----|
| Gandi | DNS management | DevOps | https://gandi.net |
| Docker | Container builds | DevOps | https://docker.com |

## Monitoring & Analytics

| Tool | Purpose | Owner | URL |
|------|---------|-------|-----|
| Vercel Analytics | Frontend performance (Core Web Vitals) | Engineering | |
| SonarCloud | SAST, coverage tracking | Engineering | |

## Productivity

| Tool | Purpose | Owner | URL |
|------|---------|-------|-----|
| useMotion | Sprint planning, task management | Product | https://usemotion.com |
| MS 365 | Documents, presentations, stakeholder comms | All | |

> Update this register when tools are added or removed. Each tool should have a clear owner.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 9.5/9.5 (100%) |
| Evaluated | 2026-05-13 |
| Target duration | 28144 ms |
| Target cost | $0.0984 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | After bootstrap, root `CLAUDE.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim | PASS | work/CLAUDE.md artifact contains `USER-EDIT-SENTINEL-DO-NOT-STRIP` inside the preserved '## Custom team notes' section. |
| c2 | After bootstrap, root `CLAUDE.md` contains a `## Coding Standards` heading — the conventions section was appended without replacing the existing content | PASS | work/CLAUDE.md artifact has `## Coding Standards` appended after the existing user content, both sections coexist. |
| c3 | After bootstrap, `docs/tooling-register.md` exists and contains a `# Tooling Register` heading and at least one table (the "Development Tools" table from the template) | PASS | work/docs/tooling-register.md artifact has `# Tooling Register` heading and a full '## Development Tools' table with GitHub, Actions, SonarCloud rows. |
| c4 | The manifest output includes a "Files created" section listing `docs/tooling-register.md` | PASS | Chat response: '### Files created\n- `docs/tooling-register.md` — project tooling register' |
| c5 | The manifest output includes a "CLAUDE.md updated" section — distinct from "Files created" or "Files merged" | PASS | Chat response has a standalone '### CLAUDE.md updated' heading separate from 'Files created' and 'Files merged'. |
| c6 | The manifest output includes a "Detected languages" section that names TypeScript, JavaScript, or Node — confirming `package.json` was used for language detection | PASS | '### Detected languages\n- TypeScript / JavaScript (package.json detected)' |
| c7 | The output does not claim rule files were copied to `.claude/rules/` — rule installation is the thinking plugin's responsibility, not this skill's | PASS | Next steps say 'Ensure the `thinking` plugin is enabled so language-specific rules are installed' — correctly attributing rule installation to the plugin, not the skill. |
| c8 | Output names `docs/tooling-register.md` as a created file — a bare "bootstrap complete" without per-file detail is not enough | PASS | '### Files created\n- `docs/tooling-register.md` — project tooling register' explicitly names the file. |
| c9 | Output does not claim it overwrote or replaced the root `CLAUDE.md` — the language reflects append or merge, not replacement | PASS | 'Appended "Coding Standards" section to root CLAUDE.md (with safe-merge marker)' — uses append language throughout. |
| c10 | Output points the reader at next steps consistent with the skill's documented manifest (customising `docs/tooling-register.md`, configuring SonarCloud, ensuring the thinking plugin is enabled, or using `/coding-standards:review-*` skills) | PARTIAL | All four expected next-step categories present: customise tooling-register, configure SonarCloud, enable thinking plugin, use /coding-standards:review-typescript. |

### Notes

The skill executed flawlessly: sentinel preserved, section appended, tooling register created with correct structure, manifest sections all present, and rule-installation correctly delegated to the thinking plugin. No gaps found across any criterion.
