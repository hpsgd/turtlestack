---
name: bootstrap
bootstrap-phase: engineering
description: "Bootstrap the release documentation structure for a project. Creates docs/release/, generates initial templates and root CHANGELOG.md, and writes the release-manager fragment of the release domain doc (the coordinator assembles docs/release/CLAUDE.md). Idempotent — merges missing sections into existing files without overwriting."
argument-hint: "[project name]"
user-invocable: false
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Bootstrap Release Documentation

Bootstrap the release documentation structure for **$ARGUMENTS**.

## Process

### Step 1: Check and create domain directory

```bash
mkdir -p docs/release docs/release/_sections
```

### Step 2: Create or merge files

For each file below, apply the safe merge pattern:
- If file does not exist → create from template
- If file exists → read both, find sections in template missing from file, append missing sections with `<!-- Merged from release-manager bootstrap v0.1.0 -->`

#### File 1: `CHANGELOG.md` (project root)

Create with this content:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security
```

#### Fragment: `docs/release/_sections/release-manager.md`

`docs/release/CLAUDE.md` is **assembled by the coordinator** from the fragments in `_sections/` — no plugin
writes it directly. Write the release-manager's contribution as this fragment. It starts at H2 (the coordinator
generates the `# Release Domain` H1 and a one-line intro). Create it with this content:

```markdown
## What This Domain Covers

- **Release process** — how code moves from development to production
- **Versioning** — Semantic Versioning conventions
- **Changelog** — Keep a Changelog format
- **Release checklists** — go/no-go gates and verification steps
- **Rollback procedures** — how to safely revert a release
- **DORA metrics** — deployment frequency, lead time, change failure rate, MTTR

## Semantic Versioning

Follow [SemVer 2.0.0](https://semver.org/):

| Change Type | Version Bump | Example |
|-------------|-------------|---------|
| Breaking API change | MAJOR | 1.0.0 → 2.0.0 |
| New feature (backward compatible) | MINOR | 1.0.0 → 1.1.0 |
| Bug fix (backward compatible) | PATCH | 1.0.0 → 1.0.1 |
| Pre-release | PRERELEASE | 1.0.0-beta.1 |

### Rules
- Once released, the contents of a version MUST NOT be modified
- Pre-release versions (e.g., `1.0.0-rc.1`) may be unstable
- Build metadata (e.g., `1.0.0+build.123`) does not affect versioning

## Keep a Changelog Format

Maintain `CHANGELOG.md` at the project root using these categories:

| Category | Use For |
|----------|---------|
| **Added** | New features |
| **Changed** | Changes to existing functionality |
| **Deprecated** | Features that will be removed |
| **Removed** | Features that have been removed |
| **Fixed** | Bug fixes |
| **Security** | Vulnerability fixes |

### Conventions
- Most recent version at the top
- `[Unreleased]` section always present for in-progress changes
- Each version has a date in `YYYY-MM-DD` format
- Link version headers to diff comparisons on GitHub

## Release Process

### Standard release flow

1. **Feature freeze** — branch cut or code freeze
2. **Release candidate** — tag `vX.Y.Z-rc.1`, deploy to staging
3. **Verification** — run full test suite, E2E tests, manual smoke tests
4. **Go/No-go** — release checklist review (see `release-checklist.md`)
5. **Release** — tag `vX.Y.Z`, deploy to production
6. **Announce** — update changelog, notify stakeholders
7. **Monitor** — watch error rates and SLOs for 24 hours

### Go/No-Go Gates

A release proceeds only when ALL gates pass:
- [ ] All quality gates green (see `docs/quality/quality-gates.md`)
- [ ] No critical/blocker bugs open
- [ ] Changelog updated
- [ ] Rollback plan documented
- [ ] Stakeholders notified

## Rollback Procedures

### When to rollback
- Error rate exceeds SLO error budget burn rate
- Critical functionality broken
- Data integrity issues detected

### How to rollback
1. Deploy previous known-good version (re-deploy previous tag)
2. Verify rollback success (health checks, smoke tests)
3. Notify stakeholders
4. Create incident report
5. Fix forward — do NOT re-release the broken version

## DORA Metrics

Track these four key metrics:

| Metric | Elite | High | Medium | Low |
|--------|-------|------|--------|-----|
| Deployment frequency | On-demand (multiple/day) | Weekly–monthly | Monthly–6 monthly | < 6 monthly |
| Lead time for changes | < 1 hour | 1 day–1 week | 1 week–1 month | > 1 month |
| Change failure rate | 0–15% | 16–30% | 31–45% | > 45% |
| Mean time to recovery | < 1 hour | < 1 day | < 1 week | > 1 week |

## Tooling

| Tool | Purpose |
|------|---------|
| GitHub Actions | Deployment pipelines |
| Vercel | Frontend releases |
| GitHub Issues | Release tracking and go/no-go |
| GitHub Releases | Release notes and artifacts |

## Available Skills

| Skill | Purpose |
|-------|---------|
| `/release-manager:release-plan` | Create a release plan |
| `/release-manager:rollback-assessment` | Assess rollback risk and procedure |

## Conventions

- Every release gets a changelog entry — no exceptions
- Releases are tagged in git (`vX.Y.Z`) and create a GitHub Release
- Hotfixes follow the same process but with expedited gates
- Release branches (if used) are named `release/vX.Y.Z`
- Post-release monitoring period is 24 hours minimum
```

#### File 3: `docs/release/release-checklist.md`

Create with this content:

```markdown
# Release Checklist — vX.Y.Z

> Copy this template for each release. Fill in the version number above.

## Pre-release

- [ ] All planned items merged to main
- [ ] CHANGELOG.md updated with all changes
- [ ] Version bumped in package files
- [ ] Release candidate tagged (`vX.Y.Z-rc.1`)
- [ ] RC deployed to staging

## Verification

- [ ] Full test suite passes on staging
- [ ] E2E tests pass on staging
- [ ] Performance budget met on staging
- [ ] Security scan clean
- [ ] Manual smoke test completed
- [ ] No critical/blocker bugs open

## Go/No-Go Decision

| Participant | Decision | Notes |
|-------------|----------|-------|
| Engineering lead | Go / No-go | |
| QA lead | Go / No-go | |
| Product owner | Go / No-go | |

**Decision:** Go / No-go
**Date:** YYYY-MM-DD

## Release

- [ ] Production tag created (`vX.Y.Z`)
- [ ] Production deployment triggered
- [ ] Health checks pass
- [ ] Smoke tests pass in production
- [ ] GitHub Release created with notes

## Post-release

- [ ] Stakeholders notified
- [ ] Monitoring dashboards checked (error rate, latency)
- [ ] 24-hour monitoring period started
- [ ] Retrospective scheduled (if issues found)

## Rollback Plan

**Rollback trigger:** [Define specific conditions]
**Rollback version:** vX.Y.(Z-1)
**Rollback procedure:**
1. Re-deploy previous tag via GitHub Actions
2. Verify health checks
3. Notify stakeholders
4. Create incident report
```

### Step 3: Return manifest

After creating/merging all files, output a summary:

```
## Release Bootstrap Complete

### Files created
- `CHANGELOG.md` — Keep a Changelog format (project root)
- `docs/release/_sections/release-manager.md` — release-manager fragment (coordinator assembles `docs/release/CLAUDE.md` from it)
- `docs/release/release-checklist.md` — release checklist template

### Files merged
- (list any existing files where sections were appended)

### Next steps
- Use `/release-manager:release-plan` for upcoming releases
- Customise go/no-go participants in the checklist
- Set up GitHub Actions release workflow
```
