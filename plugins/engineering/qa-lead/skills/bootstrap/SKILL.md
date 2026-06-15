---
name: bootstrap
bootstrap-phase: engineering
description: "Bootstrap the quality documentation structure for a project. Creates docs/quality/, generates initial templates, and writes domain CLAUDE.md. Idempotent — merges missing sections into existing files without overwriting."
argument-hint: "[project name]"
user-invocable: false
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Bootstrap Quality Documentation

Bootstrap the quality documentation structure for **$ARGUMENTS**.

## Process

### Step 1: Check and create domain directory

```bash
mkdir -p docs/quality
```

### Step 2: Create or merge files

For each file below, apply the safe merge pattern:
- If file does not exist → create from template
- If file exists → read both, find sections in template missing from file, append missing sections with `<!-- Merged from qa-lead bootstrap v0.1.0 -->`

#### File 1: `docs/quality/CLAUDE.md`

Create with this content (~130 lines):

```markdown
# Quality Domain

This directory contains quality assurance documentation: test strategy, quality gates, and definitions of ready/done.

## What This Domain Covers

- **Test strategy** — overall approach to testing across the project
- **Quality gates** — automated and manual checkpoints before promotion
- **Definitions of Ready/Done** — shared team agreements on work-item lifecycle
- **Acceptance criteria** — BDD-format specifications for features

## Test Pyramid

Follow the test pyramid to balance speed, cost, and confidence:

```
        /  E2E  \          Few — slow, expensive, high confidence
       /----------\
      / Integration \      Some — moderate speed, test boundaries
     /----------------\
    /    Unit Tests     \  Many — fast, cheap, test logic
   /____________________\
```

| Layer | Proportion | Speed | What to Test |
|-------|-----------|-------|--------------|
| Unit | ~70% | < 10ms each | Pure logic, transformations, calculations |
| Integration | ~20% | < 1s each | API boundaries, DB queries, service interactions |
| E2E | ~10% | < 30s each | Critical user journeys only |

### Unit test conventions
- One assertion per test (prefer)
- Arrange-Act-Assert (AAA) pattern
- Test behaviour, not implementation
- Name tests: `should [expected behaviour] when [condition]`

### Integration test conventions
- Use real databases where practical (testcontainers or in-memory)
- Mock only external third-party services
- Test API contracts (request/response shapes)

### E2E test conventions
- Cover the top 5–10 critical user journeys
- Run in CI on every PR (parallelised)
- Use page object pattern for UI tests

## BDD Conventions

Use Given/When/Then format for acceptance criteria:

```gherkin
Feature: [Feature name]

  Scenario: [Scenario description]
    Given [precondition]
    When [action]
    Then [expected outcome]
```

### Writing good scenarios
- One scenario per behaviour
- Keep scenarios independent (no shared state)
- Use domain language, not implementation details
- Avoid over-specifying — test the "what", not the "how"

## Three Amigos Process

Before development begins on any user story:

1. **Product Owner** — clarifies the "why" and acceptance criteria
2. **Developer** — identifies edge cases and technical constraints
3. **QA** — suggests test scenarios and boundary conditions

Timebox to 30 minutes. Output: refined acceptance criteria in Given/When/Then format.

## Quality Gate Definitions

### Gate 1: PR Merge
- [ ] All unit tests pass
- [ ] Integration tests pass
- [ ] Code coverage >= threshold (see SonarCloud)
- [ ] No new critical/blocker issues in SonarCloud
- [ ] Acceptance criteria verified (automated or manual)
- [ ] Peer review approved

### Gate 2: Staging Promotion
- [ ] All Gate 1 criteria met
- [ ] E2E tests pass on staging
- [ ] Performance budget met
- [ ] Security scan clean

### Gate 3: Production Release
- [ ] All Gate 2 criteria met
- [ ] Release checklist completed
- [ ] Rollback plan documented
- [ ] Monitoring dashboards verified

## Definition of Ready

A story is ready for development when:
- [ ] Acceptance criteria written in Given/When/Then format
- [ ] Three Amigos session completed
- [ ] Dependencies identified and available
- [ ] UX designs attached (if applicable)
- [ ] Story is sized (story points assigned)

## Definition of Done

A story is done when:
- [ ] Code implemented and peer-reviewed
- [ ] Unit and integration tests written and passing
- [ ] Acceptance criteria verified
- [ ] Documentation updated (if applicable)
- [ ] No regressions introduced
- [ ] Deployed to staging and verified

## Tooling

| Tool | Purpose |
|------|---------|
| GitHub Actions | CI test gates — runs tests on every PR |
| SonarCloud | Code coverage tracking and quality gate enforcement |

## Available Skills

| Skill | Purpose |
|-------|---------|
| `/qa-lead:test-strategy` | Create or review a test strategy |
| `/qa-lead:write-acceptance-criteria` | Write BDD acceptance criteria for a feature |

## Conventions

- Every user story must have acceptance criteria before development starts
- Test coverage thresholds are enforced in CI — never lower them without an ADR
- Flaky tests are treated as bugs — fix or remove within one sprint
- Test data setup uses factories/builders, not raw fixtures
- QA signs off on acceptance criteria, not just developers
```

#### File 2: `docs/quality/test-strategy.md`

Create with this content:

```markdown
# Test Strategy — [Project Name]

> Replace [Project Name] with the actual project name.

## 1. Scope

### In scope
<!-- Which parts of the system are covered by this strategy -->

### Out of scope
<!-- What is explicitly NOT tested (e.g., third-party SaaS internals) -->

## 2. Test Levels

| Level | Tools | Scope | Run When |
|-------|-------|-------|----------|
| Unit | | Business logic, utilities | Every commit |
| Integration | | API boundaries, DB queries | Every PR |
| E2E | | Critical user journeys | Every PR |
| Performance | | Response times, throughput | Pre-release |

## 3. Test Environments

| Environment | Purpose | Data |
|-------------|---------|------|
| Local | Developer testing | Seed data |
| CI | Automated gates | Ephemeral |
| Staging | Pre-production validation | Anonymised production-like |
| Production | Smoke tests only | Real data |

## 4. Test Data Strategy

<!-- How test data is created, managed, and cleaned up -->

## 5. Defect Management

| Severity | Response Time | Resolution Target |
|----------|--------------|-------------------|
| Critical (P1) | Immediate | Same day |
| Major (P2) | Within 4h | Within sprint |
| Minor (P3) | Next standup | Backlog |
| Trivial (P4) | Triage | Best effort |

## 6. Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Flaky tests erode trust | Medium | Zero-tolerance flaky policy |
| Low coverage areas | High | Coverage tracking per module |
| Slow test suite | Medium | Parallelisation, test pyramid adherence |
```

#### File 3: `docs/quality/definition-of-ready.md`

Create with this content:

```markdown
# Definition of Ready

A user story is **ready** for development when ALL of the following are true:

## Required

- [ ] User story follows the format: "As a [persona], I want [action] so that [benefit]"
- [ ] Acceptance criteria written in Given/When/Then format
- [ ] Three Amigos session completed (PO + Dev + QA)
- [ ] Dependencies identified and available (APIs, designs, data)
- [ ] Story is estimated (story points)
- [ ] Story fits within a single sprint

## Recommended

- [ ] UX designs or wireframes attached (if UI work)
- [ ] API contract defined (if integration work)
- [ ] Edge cases and error scenarios documented
- [ ] Performance expectations stated (if applicable)
```

#### File 4: `docs/quality/definition-of-done.md`

Create with this content:

```markdown
# Definition of Done

A user story is **done** when ALL of the following are true:

## Code

- [ ] Code implemented according to acceptance criteria
- [ ] Code peer-reviewed and approved
- [ ] No TODO/FIXME comments left without a linked issue

## Testing

- [ ] Unit tests written and passing
- [ ] Integration tests written and passing (where applicable)
- [ ] Acceptance criteria verified (automated preferred)
- [ ] No regressions in existing tests
- [ ] Code coverage maintained or improved

## Quality

- [ ] SonarCloud quality gate passes
- [ ] No new critical or blocker issues
- [ ] Linting and formatting checks pass

## Documentation

- [ ] Public API changes documented
- [ ] README updated (if behaviour changes)
- [ ] ADR written (if architectural decision made)

## Deployment

- [ ] Deployed to staging and verified
- [ ] Feature flag configured (if applicable)
- [ ] Monitoring/alerting in place (if new service)
```

#### File 5: `docs/quality/quality-gates.md`

Create with this content:

```markdown
# Quality Gates

Quality gates are automated checkpoints that code must pass before promotion.

## Gate Definitions

### Gate 1: PR Merge

**Enforced by:** GitHub Actions CI pipeline

| Check | Tool | Threshold |
|-------|------|-----------|
| Unit tests | CI runner | 100% pass |
| Integration tests | CI runner | 100% pass |
| Code coverage | SonarCloud | >= project threshold |
| Static analysis | SonarCloud | No new critical/blocker |
| Linting | CI runner | Zero violations |
| Peer review | GitHub | >= 1 approval |

### Gate 2: Staging Promotion

**Enforced by:** GitHub Actions deploy pipeline

| Check | Tool | Threshold |
|-------|------|-----------|
| All Gate 1 checks | CI | Pass |
| E2E tests | CI runner | 100% pass |
| Security scan | SonarCloud / CI | No high/critical |
| Performance budget | CI runner | Within budget |

### Gate 3: Production Release

**Enforced by:** Release checklist + CI

| Check | Tool | Threshold |
|-------|------|-----------|
| All Gate 2 checks | CI | Pass |
| Release checklist | Manual | Complete |
| Rollback plan | Documentation | Documented |
| Smoke tests | Post-deploy CI | Pass |

## Overriding a Gate

Gates should not be bypassed. If a gate must be overridden:
1. Document the reason in the PR/release
2. Get approval from tech lead and QA lead
3. Create a follow-up issue to address the underlying problem
4. Time-bound the override (revert within one sprint)
```

### Step 3: Return manifest

After creating/merging all files, output a summary:

```
## Quality Bootstrap Complete

### Files created
- `docs/quality/CLAUDE.md` — domain conventions and skill reference
- `docs/quality/test-strategy.md` — test strategy template
- `docs/quality/definition-of-ready.md` — Definition of Ready checklist
- `docs/quality/definition-of-done.md` — Definition of Done checklist
- `docs/quality/quality-gates.md` — quality gate definitions

### Files merged
- (list any existing files where sections were appended)

### Next steps
- Fill in `test-strategy.md` with project-specific tools and scope
- Customise coverage thresholds in `quality-gates.md`
- Use `/qa-lead:test-strategy` to elaborate the test strategy
```
