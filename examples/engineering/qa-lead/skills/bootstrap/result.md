# Bootstrap

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/quality/_sections/qa-lead.md` fragment containing a user-authored section. The qa-lead bootstrap skill should preserve that user content while appending the template's missing sections (with a merge marker), and should create the four files the fixture is missing — `test-strategy.md`, `definition-of-ready.md`, `definition-of-done.md`, and `quality-gates.md`. The qa-lead never writes `docs/quality/CLAUDE.md` directly — the coordinator assembles it from the fragments in `_sections/`. The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

> The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/quality/_sections/qa-lead.md` fragment is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.
> 
> Read the qa-lead bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/engineering/qa-lead/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.
> 
> After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Quality Bootstrap Complete

### Files created
- `docs/quality/test-strategy.md` — test strategy template
- `docs/quality/definition-of-ready.md` — Definition of Ready checklist
- `docs/quality/definition-of-done.md` — Definition of Done checklist
- `docs/quality/quality-gates.md` — quality gate definitions

### Files merged
- `docs/quality/_sections/qa-lead.md` — qa-lead fragment (sections appended via safe-merge pattern, user-authored "Custom team notes" section preserved)

### Next steps
- Fill in `test-strategy.md` with TestProject-specific tools and scope
- Customise coverage thresholds in `quality-gates.md`
- Use `/qa-lead:test-strategy` to elaborate the test strategy
- The coordinator will assemble `docs/quality/CLAUDE.md` from the `_sections/qa-lead.md` fragment

### Artifacts written

#### `work/docs/quality/quality-gates.md`

```
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

#### `work/docs/quality/test-strategy.md`

```
# Test Strategy — TestProject

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

#### `work/docs/quality/definition-of-ready.md`

```
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

#### `work/docs/quality/definition-of-done.md`

```
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

#### `work/docs/quality/_sections/qa-lead.md`

```
<!-- qa-lead fragment of the quality domain doc. Assembled into docs/quality/CLAUDE.md by the coordinator. -->

## Custom team notes

USER-EDIT-SENTINEL-DO-NOT-STRIP

This section was written by the team and must survive any bootstrap re-run.
It exists to test the safe-merge contract: the bootstrap skill must not
overwrite or remove user-authored content.

<!-- Merged from qa-lead bootstrap v0.1.0 -->

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

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 11.5/11.5 (100%) |
| Evaluated | 2026-06-15 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 54306 ms |
| Target cost | $0.0987 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | After bootstrap, `docs/quality/_sections/qa-lead.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim | PASS | Artifact `work/docs/quality/_sections/qa-lead.md` contains the line `USER-EDIT-SENTINEL-DO-NOT-STRIP` under the `## Custom team notes` section. |
| c2 | After bootstrap, `docs/quality/_sections/qa-lead.md` contains the safe-merge marker `<!-- Merged from qa-lead bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged | PASS | Artifact contains the exact line `<!-- Merged from qa-lead bootstrap v0.1.0 -->` immediately after the user-authored section. |
| c3 | After bootstrap, `docs/quality/_sections/qa-lead.md` contains the appended template sections — at minimum the "Test Pyramid" and "BDD Conventions" headings now appear alongside the preserved user content | PASS | Artifact contains `## Test Pyramid` and `## BDD Conventions` headings alongside the preserved `## Custom team notes` section. |
| c4 | The qa-lead fragment is authored at H2 and below — it does not introduce a `# Quality Domain` H1 (the coordinator generates that when it assembles `docs/quality/CLAUDE.md`) | PASS | All headings in `_sections/qa-lead.md` artifact are `##` level (`## Custom team notes`, `## Test Pyramid`, `## BDD Conventions`, etc.). No H1 present. |
| c5 | The skill does NOT write `docs/quality/CLAUDE.md` directly — that file is the coordinator's to assemble from `_sections/` | PASS | No `docs/quality/CLAUDE.md` artifact is listed. Chat output states "The coordinator will assemble `docs/quality/CLAUDE.md` from the `_sections/qa-lead.md` fragment". |
| c6 | After bootstrap, all four template files exist: `docs/quality/test-strategy.md`, `docs/quality/definition-of-ready.md`, `docs/quality/definition-of-done.md`, and `docs/quality/quality-gates.md` | PASS | All four artifacts are present: `work/docs/quality/test-strategy.md`, `definition-of-ready.md`, `definition-of-done.md`, and `quality-gates.md`. |
| c7 | The created `docs/quality/test-strategy.md` contains the `## 2. Test Levels` heading and references "TestProject" in its title (placeholder was substituted) | PASS | Artifact title is `# Test Strategy — TestProject` and contains `## 2. Test Levels` heading with a populated table. |
| c8 | The created `docs/quality/quality-gates.md` contains gate definitions — at minimum the "Gate 1: PR Merge" section heading | PASS | Artifact `quality-gates.md` contains `### Gate 1: PR Merge` with a full table of checks. |
| c9 | Chat output includes a manifest summary that distinguishes files created (the four templates) from files merged (`_sections/qa-lead.md`) | PASS | Chat output has separate `### Files created` and `### Files merged` sections, clearly distinguishing the four templates from the merged fragment. |
| c10 | Output names each created and merged file individually — a bare "bootstrap complete" without the per-file manifest is not enough | PASS | Chat output lists all four created files by path and `docs/quality/_sections/qa-lead.md` as the merged file, each on its own bullet. |
| c11 | Output does not claim it overwrote or replaced `docs/quality/_sections/qa-lead.md` — the language reflects merge, not replacement | PASS | Chat output says "sections appended via safe-merge pattern, user-authored 'Custom team notes' section preserved" — no replacement language. |
| c12 | Output points the reader at next steps (filling in `test-strategy.md`, customising thresholds in `quality-gates.md`, or using `/qa-lead:test-strategy`) consistent with the skill's documented manifest | PARTIAL | Chat output `### Next steps` lists all three: fill in `test-strategy.md`, customise `quality-gates.md` thresholds, and use `/qa-lead:test-strategy`. |

### Notes

The skill executed flawlessly across all dimensions: sentinel preservation, merge marker placement, correct heading level, no CLAUDE.md write, all four files created with proper content, and a well-structured manifest. Perfect score constrained only by the PARTIAL ceiling on c12.
