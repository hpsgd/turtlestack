# Bootstrap

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/infrastructure/CLAUDE.md` containing a user-authored section. The devops bootstrap skill should preserve that user content while appending the template's missing sections (with a merge marker), and should create the two files the fixture is missing — `slo-definition.md` and `runbook-template.md`. The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

> The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/infrastructure/CLAUDE.md` is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.
> 
> Read the devops bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/engineering/devops/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.
> 
> After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Infrastructure Bootstrap Complete

### Files created
- `docs/infrastructure/slo-definition.md` — SLO definition template
- `docs/infrastructure/runbook-template.md` — runbook template

### Files merged
- `docs/infrastructure/CLAUDE.md` — merged template sections while preserving user-authored "Custom team notes"

### Next steps
- Create SLO definitions per service using `/devops:write-slo`
- Set up GitHub Actions pipelines using `/devops:write-pipeline`
- Document operational runbooks for known failure modes

### Artifacts written

#### `work/docs/infrastructure/runbook-template.md`

```
# Runbook — [Issue Title]

## Metadata

| Field | Value |
|-------|-------|
| Severity | P1 / P2 / P3 / P4 |
| Last updated | YYYY-MM-DD |
| Author | |
| Service | |

## Symptoms

<!-- How do you know this issue is happening? What alerts fire? What do users report? -->

- Symptom 1
- Symptom 2

## Diagnosis

<!-- Step-by-step commands/checks to confirm the issue -->

1. Check service health:
   ```bash
   curl -s https://[service]/health | jq .
   ```
2. Check logs:
   ```bash
   # Add relevant log query
   ```
3. Check metrics:
   <!-- Link to relevant dashboard -->

## Resolution

<!-- Step-by-step fix procedure -->

1. Step 1
2. Step 2
3. Verify fix:
   ```bash
   # Verification command
   ```

## Escalation

| Condition | Contact | Channel |
|-----------|---------|---------|
| Resolution fails after 30min | [Team lead] | Slack #incidents |
| Data loss suspected | [Engineering manager] | Phone |

## Prevention

<!-- What changes would prevent this from recurring? -->

- [ ] Prevention action 1
- [ ] Prevention action 2

## History

| Date | Occurrence | Resolution Time | Notes |
|------|-----------|-----------------|-------|
| | | | |

```

#### `work/docs/infrastructure/slo-definition.md`

```
# SLO Definition — [Service Name]

> Replace [Service Name] with the actual service name. Create one file per service.

## Service Overview

| Field | Value |
|-------|-------|
| Service | |
| Owner | |
| Dependencies | |
| Tier | Critical / Standard / Best-effort |

## SLIs and SLOs

### Availability

| Field | Value |
|-------|-------|
| SLI | Proportion of successful HTTP requests (non-5xx) |
| Measurement | `count(status < 500) / count(total)` over 5-min windows |
| SLO | >= 99.9% over 30-day rolling window |
| Error budget | 43.2 minutes/month |

### Latency

| Field | Value |
|-------|-------|
| SLI | Response time distribution |
| Measurement | Server-side request duration |
| SLO (p50) | < 100ms |
| SLO (p99) | < 500ms |

### Error Budget Policy

| Budget Remaining | Action |
|-----------------|--------|
| > 50% | Normal development velocity |
| 25–50% | Increased monitoring, cautious deploys |
| 10–25% | Feature freeze, focus on reliability |
| < 10% | Incident response mode, rollback risky changes |

## Alerting

| Alert | Condition | Severity | Channel |
|-------|-----------|----------|---------|
| High burn rate | 14.4x budget consumption over 1h | P1 | PagerDuty |
| Medium burn rate | 6x budget consumption over 6h | P2 | Slack |
| Low burn rate | 3x budget consumption over 3d | P3 | Email |

## Review Schedule

- Monthly: review SLO adherence and error budget
- Quarterly: adjust SLO targets if needed (with ADR)

```

#### `work/docs/infrastructure/CLAUDE.md`

```
# Infrastructure Domain

This directory contains infrastructure and operations documentation: SLO definitions, pipeline standards, runbooks, and deployment conventions.

## What This Domain Covers

- **SLOs/SLIs** — service level objectives and indicators
- **CI/CD pipelines** — GitHub Actions workflow standards
- **Deployment** — Vercel frontend deployment, containerised backend deployment
- **Runbooks** — operational procedures for incident response
- **Infrastructure as Code** — reproducible environment definitions

## SLO/SLI Conventions

### Definitions

- **SLI** (Service Level Indicator) — a quantitative measure of service behaviour (e.g., request latency p99)
- **SLO** (Service Level Objective) — a target value for an SLI (e.g., p99 latency < 200ms)
- **Error budget** — the allowed amount of SLO violation (e.g., 0.1% downtime = 43.8 min/month)

### Standard SLIs

| Category | SLI | Measurement |
|----------|-----|-------------|
| Availability | Success rate | Successful requests / total requests |
| Latency | Response time | p50, p95, p99 response times |
| Throughput | Request rate | Requests per second |
| Error rate | Failure rate | 5xx responses / total responses |

### SLO Template

For each service, define SLOs in `docs/infrastructure/slo-{service}.md`:
- SLI definition and measurement method
- SLO target and evaluation window (30-day rolling)
- Error budget policy (what happens when budget is exhausted)
- Alerting thresholds (burn rate alerts)

## GitHub Actions Pipeline Standards

### Pipeline structure

Every project should have these workflows:

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `ci.yml` | PR, push to main | Build, test, lint, security scan |
| `deploy-staging.yml` | Push to main | Deploy to staging environment |
| `deploy-production.yml` | Release tag / manual | Deploy to production |
| `scheduled-checks.yml` | Cron (weekly) | Dependency audit, security scan |

### Pipeline conventions
- Use pinned action versions (SHA, not `@latest` or `@v3`)
- Cache dependencies (node_modules, pip cache)
- Run jobs in parallel where possible
- Fail fast on lint/type errors before running tests
- Store artifacts for failed test runs
- Use environment secrets (not repository secrets) for deployment credentials

## Deployment Conventions

### Frontend (Vercel)
- Preview deployments on every PR
- Production deploy on merge to main (or release tag)
- Environment variables managed in Vercel dashboard
- Custom domains managed via Gandi DNS

### Backend / Services
- Containerised with Docker (multi-stage builds)
- Images tagged with git SHA and semantic version
- Health check endpoints required (`/health`, `/ready`)
- Graceful shutdown handling (SIGTERM)
- Zero-downtime deployments (rolling update or blue-green)

## Runbook Format

Store runbooks in GitHub Wiki or `docs/infrastructure/runbooks/`.

Every runbook must include:
1. **Title** — clear description of the scenario
2. **Severity** — P1/P2/P3/P4
3. **Symptoms** — how to recognise this issue
4. **Diagnosis** — steps to confirm root cause
5. **Resolution** — step-by-step fix procedure
6. **Escalation** — who to contact if resolution fails
7. **Prevention** — how to stop this recurring

## Tooling

| Tool | Purpose |
|------|---------|
| GitHub Actions | CI/CD pipelines |
| Vercel | Frontend deployment and preview environments |
| Gandi | DNS management |
| SonarCloud | CI quality and security gate |
| Docker | Container builds |

## Available Skills

| Skill | Purpose |
|-------|---------|
| `/devops:write-pipeline` | Create GitHub Actions workflows |
| `/devops:write-dockerfile` | Write optimised Dockerfiles |
| `/devops:write-iac` | Write infrastructure as code |
| `/devops:write-slo` | Define SLOs for a service |
| `/devops:incident-response` | Document incident response procedures |

## Conventions

- Every deployment must be reproducible from a git commit
- No manual changes to production — everything goes through CI/CD
- Secrets are never stored in code or CI config — use environment secrets
- SLOs are reviewed quarterly and adjusted based on actual performance
- Runbooks are tested during game days (at least quarterly)
- Container images are scanned for vulnerabilities before deployment

<!-- Merged from devops bootstrap v0.1.0 -->

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
| Score | 8.5/8.5 (100%) |
| Evaluated | 2026-05-13 |
| Target duration | 50055 ms |
| Target cost | $0.1554 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | After bootstrap, `docs/infrastructure/CLAUDE.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim | PASS | Artifact shows '## Custom team notes\n\nUSER-EDIT-SENTINEL-DO-NOT-STRIP' intact at bottom of CLAUDE.md |
| c2 | After bootstrap, `docs/infrastructure/CLAUDE.md` contains the safe-merge marker `<!-- Merged from devops bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged | PASS | Artifact contains '<!-- Merged from devops bootstrap v0.1.0 -->' directly before the preserved user section |
| c3 | After bootstrap, `docs/infrastructure/CLAUDE.md` contains the appended template sections — at minimum the "SLO/SLI Conventions" and "GitHub Actions Pipeline Standards" headings now appear alongside the preserved user content | PASS | Artifact shows '## SLO/SLI Conventions' and '## GitHub Actions Pipeline Standards' both present in CLAUDE.md alongside user content |
| c4 | After bootstrap, `docs/infrastructure/slo-definition.md` exists and was created from the skill's template (contains a `## SLIs and SLOs` heading) | PASS | Artifact work/docs/infrastructure/slo-definition.md contains '## SLIs and SLOs' heading |
| c5 | After bootstrap, `docs/infrastructure/runbook-template.md` exists and was created from the skill's template (contains a `## Symptoms` heading and a `## Resolution` heading) | PASS | Artifact work/docs/infrastructure/runbook-template.md contains both '## Symptoms' and '## Resolution' headings |
| c6 | Chat output includes a manifest summary that distinguishes files created (`slo-definition.md`, `runbook-template.md`) from files merged (`CLAUDE.md`) | PASS | Chat response has distinct '### Files created' and '### Files merged' sections listing the correct files under each |
| c7 | Output names each created and merged file individually — a bare "bootstrap complete" without the per-file manifest is not enough | PASS | Chat lists slo-definition.md, runbook-template.md under created, and CLAUDE.md under merged — all three files named individually |
| c8 | Output does not claim it overwrote or replaced `docs/infrastructure/CLAUDE.md` — the language reflects merge, not replacement | PASS | Chat says 'merged template sections while preserving user-authored "Custom team notes"' under '### Files merged' — no replacement language |
| c9 | Output points the reader at next steps (creating SLO definitions per service using `/devops:write-slo`, setting up pipelines using `/devops:write-pipeline`) consistent with the skill's documented manifest | PARTIAL | Chat '### Next steps' lists '/devops:write-slo' and '/devops:write-pipeline' explicitly, plus a third item about runbooks |

### Notes

The skill execution was flawless: all three files were correctly produced, the sentinel was preserved, the merge marker was inserted, template sections were appended, and the manifest summary used precise merge/create language. All criteria met at or above threshold.
