---
name: bootstrap
bootstrap-phase: engineering
description: "Bootstrap the infrastructure documentation structure for a project. Creates docs/infrastructure/, generates initial templates, and writes the devops fragment of the infrastructure domain doc (the coordinator assembles docs/infrastructure/CLAUDE.md). Idempotent — merges missing sections into existing files without overwriting."
argument-hint: "[project name]"
user-invocable: false
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Bootstrap Infrastructure Documentation

Bootstrap the infrastructure documentation structure for **$ARGUMENTS**.

## Process

### Step 1: Check and create domain directory

```bash
mkdir -p docs/infrastructure docs/infrastructure/_sections
```

### Step 2: Create or merge files

For each file below, apply the safe merge pattern:
- If file does not exist → create from template
- If file exists → read both, find sections in template missing from file, append missing sections with `<!-- Merged from devops bootstrap v0.1.0 -->`

#### Fragment: `docs/infrastructure/_sections/devops.md`

`docs/infrastructure/CLAUDE.md` is **assembled by the coordinator** from the fragments in `_sections/` — no
plugin writes it directly. Write the devops contribution as this fragment. It starts at H2 (the coordinator
generates the `# Infrastructure Domain` H1 and a one-line intro). Create it with this content:

```markdown
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
```

#### File 2: `docs/infrastructure/slo-definition.md`

Create with this content:

```markdown
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

#### File 3: `docs/infrastructure/runbook-template.md`

Create with this content:

```markdown
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

### Step 3: Return manifest

After creating/merging all files, output a summary:

```
## Infrastructure Bootstrap Complete

### Files created
- `docs/infrastructure/_sections/devops.md` — devops fragment (coordinator assembles `docs/infrastructure/CLAUDE.md` from it)
- `docs/infrastructure/slo-definition.md` — SLO definition template
- `docs/infrastructure/runbook-template.md` — runbook template

### Files merged
- (list any existing files where sections were appended)

### Next steps
- Create SLO definitions per service using `/devops:write-slo`
- Set up GitHub Actions pipelines using `/devops:write-pipeline`
- Document operational runbooks for known failure modes
```
