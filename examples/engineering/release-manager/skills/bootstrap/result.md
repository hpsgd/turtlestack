# Bootstrap

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/release/CLAUDE.md` containing a user-authored section. The release-manager bootstrap skill should preserve that user content while appending the template's missing sections (with a merge marker), and should create the two files the fixture is missing — `CHANGELOG.md` (project root) and `docs/release/release-checklist.md`. The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

> The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/release/CLAUDE.md` is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.
> 
> Read the release-manager bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/engineering/release-manager/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.
> 
> After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Release Bootstrap Complete

### Files created
- `CHANGELOG.md` — Keep a Changelog format (project root)
- `docs/release/release-checklist.md` — release checklist template

### Files merged
- `docs/release/CLAUDE.md` — appended missing sections (What This Domain Covers, Semantic Versioning, Keep a Changelog Format, Release Process, Rollback Procedures, DORA Metrics, Tooling, Available Skills, Conventions). User-authored "Custom team notes" section preserved with safe-merge sentinel intact.

### Next steps
- Use `/release-manager:release-plan` for upcoming releases
- Customise go/no-go participants in the checklist
- Set up GitHub Actions release workflow

### Artifacts written

#### `work/CHANGELOG.md`

```
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

#### `work/docs/release/release-checklist.md`

```
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

#### `work/docs/release/CLAUDE.md`

```
# Release Domain

This directory contains release management documentation: release process, checklists, and versioning conventions.

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

<!-- Merged from release-manager bootstrap v0.1.0 -->

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
| Score | 9.0/9.0 (100%) |
| Evaluated | 2026-05-13 |
| Target duration | 52671 ms |
| Target cost | $0.1550 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | After bootstrap, `docs/release/CLAUDE.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim | PASS | Artifact `work/docs/release/CLAUDE.md` contains `USER-EDIT-SENTINEL-DO-NOT-STRIP` in the '## Custom team notes' section at the bottom of the file. |
| c2 | After bootstrap, `docs/release/CLAUDE.md` contains the safe-merge marker `<!-- Merged from release-manager bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged | PASS | Artifact contains `<!-- Merged from release-manager bootstrap v0.1.0 -->` immediately before the preserved `## Custom team notes` section. |
| c3 | After bootstrap, `docs/release/CLAUDE.md` contains the appended template sections — at minimum the "Semantic Versioning" and "Release Process" headings now appear alongside the preserved user content | PASS | Artifact contains `## Semantic Versioning` and `## Release Process` headings, plus What This Domain Covers, Keep a Changelog Format, Rollback Procedures, DORA Metrics, Tooling, Available Skills, and Conventions. |
| c4 | After bootstrap, `CHANGELOG.md` exists at the project root and was created from the skill's template (contains `## [Unreleased]` and the standard Keep a Changelog categories) | PASS | Artifact `work/CHANGELOG.md` contains `## [Unreleased]` with subsections Added, Changed, Deprecated, Removed, Fixed, Security. |
| c5 | After bootstrap, `docs/release/release-checklist.md` exists and was created from the skill's template (contains a `## Go/No-Go Decision` section and the participant sign-off table) | PASS | Artifact `work/docs/release/release-checklist.md` contains `## Go/No-Go Decision` with a table listing Engineering lead, QA lead, Product owner rows. |
| c6 | Chat output includes a manifest summary that distinguishes files created (`CHANGELOG.md`, `release-checklist.md`) from files merged (`CLAUDE.md`) | PASS | Chat response has separate `### Files created` and `### Files merged` sections, listing CHANGELOG.md and release-checklist.md under created, CLAUDE.md under merged. |
| c7 | Output names each created and merged file individually — a bare "bootstrap complete" without the per-file manifest is not enough | PASS | Each file is individually named with a description: `CHANGELOG.md`, `docs/release/release-checklist.md`, and `docs/release/CLAUDE.md` all listed separately. |
| c8 | Output does not claim it overwrote or replaced `docs/release/CLAUDE.md` — the language reflects merge, not replacement | PASS | Output says 'appended missing sections' and 'User-authored "Custom team notes" section preserved with safe-merge sentinel intact' — no overwrite/replace language. |
| c9 | Output points the reader at next steps (using `/release-manager:release-plan`, customising checklist participants, setting up GitHub Actions release workflow) consistent with the skill's documented manifest | PARTIAL | Next steps section lists all three: `/release-manager:release-plan`, 'Customise go/no-go participants in the checklist', 'Set up GitHub Actions release workflow'. |

### Notes

The skill executed flawlessly across all criteria: user content preserved, merge marker present, template sections appended, both new files created with correct structure, and the manifest summary clearly distinguishes created from merged files. The PARTIAL ceiling on c9 is the only scoring cap applied, and the output fully satisfies even that criterion.
