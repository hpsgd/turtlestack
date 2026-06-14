---
name: bootstrap
bootstrap-phase: foundations
description: "Bootstrap the coding standards documentation for a project. Creates docs/tooling-register.md and appends coding conventions to root CLAUDE.md. Idempotent — merges missing sections into existing files without overwriting. Rule installation is handled separately by the thinking plugin's SessionStart hook."
argument-hint: "[project name]"
user-invocable: false
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Bootstrap Coding Standards

Bootstrap the coding standards documentation for **$ARGUMENTS**.

This skill operates at the `docs/` root level rather than creating its own domain directory.

## Process

### Step 1: Detect project languages and frameworks

Scan the project to determine which languages and frameworks are in use:

```bash
# Check for language indicators
ls package.json tsconfig.json 2>/dev/null          # TypeScript/JavaScript
ls requirements.txt pyproject.toml setup.py 2>/dev/null  # Python
ls *.csproj *.sln 2>/dev/null                       # .NET
ls go.mod 2>/dev/null                                # Go
ls Cargo.toml 2>/dev/null                            # Rust
```

Record which languages are detected — this determines which rules to install and which review skills to reference.

### Step 2: Create docs directory

```bash
mkdir -p docs
```

### Step 3: Create or merge files

For each file below, apply the safe merge pattern:
- If file does not exist → create from template
- If file exists → read both, find sections in template missing from file, append missing sections with `<!-- Merged from coding-standards bootstrap v0.1.0 -->`

#### File 1: `docs/tooling-register.md`

Create with this content:

```markdown
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

Rule installation is NOT this skill's responsibility — the thinking plugin's `install-rules.sh` SessionStart hook installs rules from every enabled plugin into `.claude/rules/` automatically. Do not copy rule files here.

### Step 4: Append coding conventions to root CLAUDE.md

Check if the project root `CLAUDE.md` already has a "Coding Standards" section. If not, append the following:

```markdown

## Coding Standards

### Active Standards

<!-- Updated by coding-standards bootstrap — list detected language standards -->

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

If the section already exists, find and append any missing subsections.

### Step 5: Return manifest

After creating/merging all files, output a summary:

```
## Coding Standards Bootstrap Complete

### Files created
- `docs/tooling-register.md` — project tooling register

### CLAUDE.md updated
- Appended "Coding Standards" section to root CLAUDE.md

### Files merged
- (list any existing files where sections were appended)

### Detected languages
- (list detected languages/frameworks)

### Next steps
- Review and customise `docs/tooling-register.md` with project-specific tools
- Configure SonarCloud quality gates
- Ensure the `thinking` plugin is enabled so language-specific rules are installed into `.claude/rules/`
- Use `/coding-standards:review-*` skills during code review
```
