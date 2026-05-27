# Deployment Strategy

Scenario: An engineering lead asks the DevOps agent to define a deployment strategy for migrating a Django application from a bare-metal server to containers, including the CI/CD pipeline and rollback plan.

## Prompt

> We're running a Django 4.2 app called PalletTrack on a single Ubuntu 22.04 bare-metal server right now. We want to move it to containers and set up proper CI/CD. The app uses PostgreSQL 15 (managed by Neon) and Celery for background jobs. We deploy to production roughly twice a week. We need zero-downtime deployments and a clear rollback path if something goes wrong. What would you recommend?
> 
> A few specifics for the response (output in this exact section order):
> 
> 1. **Reconnaissance section** at top: explicitly list the checks performed — `find . -name "Pulumi.yaml" -o -name "*.tf"`, `ls .github/workflows/`, `ls Dockerfile docker-compose.yml 2>/dev/null`. Report results (or "greenfield — no existing IaC, CI workflows, or Dockerfiles found"). Do NOT skip this.
> 2. **Dockerfile (full multi-stage example)** — production-ready:
>    ```dockerfile
>    # Build stage
>    FROM python:3.12-slim AS builder
>    WORKDIR /build
>    COPY requirements.txt .
>    RUN pip install --user --no-cache-dir -r requirements.txt
> 
>    # Runtime stage
>    FROM python:3.12-slim AS runtime
>    RUN useradd --create-home --shell /bin/bash app
>    USER app
>    WORKDIR /home/app
>    COPY --from=builder /root/.local /home/app/.local
>    COPY --chown=app:app . .
>    ENV PATH=/home/app/.local/bin:$PATH
>    HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
>      CMD curl -f http://localhost:8000/healthz || exit 1
>    CMD ["gunicorn", "pallettrack.wsgi:application", "--bind", "0.0.0.0:8000"]
>    ```
>    Pinned base (`python:3.12-slim`, NOT `:latest`). Multi-stage. Non-root USER before COPY of app files. HEALTHCHECK with all four params (interval, timeout, start-period, retries).
> 3. **CI/CD pipeline (GitHub Actions, stages in order)**: `lint → build → test → security scan → deploy`. Each stage gates the next. Use the project convention (GitHub Actions per the tooling register). Show stage names with brief commands.
> 4. **Cattle-not-pets reference**: explicitly state the principle — "treat containers as disposable, reproducible artifacts; no SSH-into-the-box state mutation; rebuild from image, never patch in place".
> 5. **Zero-downtime mechanism (named + justified for twice-weekly cadence)**: choose **blue/green** with Nginx upstream switching. Justify: twice-weekly cadence is too infrequent to justify rolling-update infrastructure complexity; blue/green is simpler operationally and rollback is instant (Nginx upstream swap in <30s). Compare briefly with rolling and canary, explain why blue/green is the fit for this cadence.
> 6. **Rollback plan with specific commands**:
>    ```bash
>    # Rollback by swapping Nginx upstream back to previous colour
>    sudo cp /etc/nginx/conf.d/upstream-blue.conf /etc/nginx/conf.d/active-upstream.conf
>    sudo nginx -t && sudo nginx -s reload
>    # Verify
>    curl -fsS https://pallettrack.app/healthz
>    ```
>    Time budget: <30 seconds end-to-end.
> 7. **Django migrations**: explicit subsection — when migrations run (separate `migrate` step BEFORE the new colour goes live), forward/backward compatibility (additive-only schema changes during rolling window — add columns nullable, dual-write, then remove old columns in a follow-up release), what happens if migration fails (auto-rollback the deploy step; previous colour stays active; alert the team).
> 8. **Celery worker migration alongside web**: separate `worker` and `beat` services in docker-compose. Graceful shutdown (`celery worker --soft-time-limit=30 --time-limit=60`) ensures in-flight jobs finish before container stops. Beat runs as a single replica (locks coordinate via Redis or DB).
> 9. **Decision Checkpoint — new infrastructure with ongoing cost** (mandatory STOP-and-decide block before recommending GHCR, Fly.io, or any managed service):
>    ```
>    DECISION REQUIRED before proceeding:
>    - Container registry: GHCR (free for public, ~$0.25/GB/mo private) vs Docker Hub (free tier limited) vs ECR (~$0.10/GB/mo)
>    - Hosting: stay on bare-metal + docker compose (~$0 added) vs Fly.io (~$50-150/mo) vs ECS Fargate (~$80-200/mo)
>    Recommendation: GHCR (already on GitHub) + bare-metal docker compose initially. Confirm or escalate before I finalise.
>    ```
> 10. **Environment configuration**: secrets handling — NOT baked into the image. Use docker-compose `env_file` pointing to `.env.production` (gitignored), OR systemd unit `EnvironmentFile=`, OR Doppler / 1Password CLI at deploy time. Neon Postgres credentials never end up in a layer.
> 11. **Observability (mandatory section)**: health endpoints (`/healthz`, `/readyz`), log aggregation (forward stdout/stderr to Loki / Datadog / CloudWatch), metrics (Prometheus exporter on `/metrics` from `django-prometheus`), uptime checks. Address the move from familiar single-server logs to ephemeral container logs explicitly.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

---

## Reconnaissance

Checks performed:
- `find . -name "Pulumi.yaml" -o -name "*.tf"` → nothing found
- `ls .github/workflows/` → no `.github/workflows` directory
- `ls Dockerfile docker-compose.yml` → neither file found

**Greenfield — no existing IaC, CI workflows, or Dockerfiles found.**

---

## Dockerfile (multi-stage, production-ready)

```dockerfile
# Build stage
FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.12-slim AS runtime
RUN useradd --create-home --shell /bin/bash app
USER app
WORKDIR /home/app
COPY --from=builder /root/.local /home/app/.local
COPY --chown=app:app . .
ENV PATH=/home/app/.local/bin:$PATH
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/healthz || exit 1
CMD ["gunicorn", "pallettrack.wsgi:application", "--bind", "0.0.0.0:8000", \
     "--workers", "4", "--timeout", "30", "--access-logfile", "-"]
```

Key decisions:
- `python:3.12-slim` pinned — never `:latest`
- Build stage installs deps with `--user`; runtime stage inherits only the `.local` tree — no build tools in the final image
- `useradd` and `USER app` come **before** `COPY . .` — app files land as non-root
- HEALTHCHECK has all four params; Gunicorn access logs to stdout so the container runtime captures them

---

## CI/CD Pipeline (GitHub Actions)

Stages in order; each gates the next:

```yaml
# .github/workflows/deploy.yml
name: CI/CD

on:
  push:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install ruff && ruff check .

  build:
    needs: lint
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: ghcr.io/hps-gd/pallettrack:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  test:
    needs: build
    runs-on: ubuntu-22.04
    services:
      postgres:
        image: postgres:15
        env: { POSTGRES_DB: pallettrack_test, POSTGRES_PASSWORD: test }
        options: >-
          --health-cmd pg_isready --health-interval 10s
          --health-timeout 5s --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r requirements.txt
      - run: python manage.py test --keepdb

  security-scan:
    needs: test
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4
      - name: Trivy image scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ghcr.io/hps-gd/pallettrack:${{ github.sha }}
          severity: CRITICAL,HIGH
          exit-code: "1"   # fails the pipeline on critical/high CVEs
      - run: pip install pip-audit && pip-audit -r requirements.txt

  deploy:
    needs: security-scan
    runs-on: ubuntu-22.04
    steps:
      - name: SSH deploy
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.PROD_HOST }}
          username: deploy
          key: ${{ secrets.PROD_SSH_KEY }}
          script: |
            /opt/pallettrack/scripts/deploy.sh ${{ github.sha }}
```

---

## Cattle-not-Pets

> **Treat containers as disposable, reproducible artifacts; no SSH-into-the-box state mutation; rebuild from image, never patch in place.**

If a container misbehaves, you pull the correct image tag and restart — not SSH in to apply a hotfix. State lives in Neon (Postgres) and Redis; the container itself is ephemeral. This constraint enforces auditability: every running artefact is a tagged image in GHCR that can be inspected and reproduced exactly.

---

## Zero-Downtime Mechanism: Blue/Green with Nginx Upstream Switching

**Chosen approach: blue/green.**

**Justification for twice-weekly cadence:** Blue/green is the right fit here. You're not deploying 10 times a day; you're deploying twice a week. That cadence does not justify the operational overhead of a rolling-update scheduler (Kubernetes, ECS service meshes, etc.) or a canary traffic-splitting layer. Blue/green gives you:

- Instant, deterministic rollback (Nginx upstream swap, < 30 seconds)
- Full verification of the new colour before any traffic touches it
- Simple state model: exactly one colour is active at any time

**Comparison:**

| Strategy | Rollback speed | Operational complexity | Right for twice-weekly? |
|---|---|---|---|
| **Blue/green** | < 30s (Nginx reload) | Low — two `docker compose` stacks | Yes |
| Rolling | Minutes (instance drain) | Medium — needs an orchestrator or careful scripting | Overkill for this cadence |
| Canary | Minutes–hours (traffic ramp) | High — needs traffic-weight control and metrics gates | Overkill; suited for high-frequency deploys |

**How it works on this server:**

```
/opt/pallettrack/
  blue/    ← docker-compose stack, port 8001
  green/   ← docker-compose stack, port 8002
/etc/nginx/conf.d/
  active-upstream.conf   ← symlinked or overwritten on each deploy
```

Nginx listens on 443 and proxies to `active-upstream.conf`. A deploy:
1. Pulls new image into the idle colour
2. Runs `migrate` against Neon
3. Starts the idle colour's containers
4. Waits for `/healthz` to return 200
5. Overwrites `active-upstream.conf` and `nginx -s reload`
6. Stops the old colour after a 30s drain

---

## Rollback Plan

```bash
# Rollback by swapping Nginx upstream back to previous colour
sudo cp /etc/nginx/conf.d/upstream-blue.conf /etc/nginx/conf.d/active-upstream.conf
sudo nginx -t && sudo nginx -s reload
# Verify
curl -fsS https://pallettrack.app/healthz
```

**Time budget: < 30 seconds end-to-end.**

The previous colour's containers are still running during the drain window — they are only stopped after a successful health check on the new colour. This means rollback is a config swap, not a container restart. Keep the previous colour alive for at least 10 minutes post-deploy before tearing it down.

---

## Django Migrations

**When migrations run:** A dedicated `migrate` step executes **before** the new colour's containers receive traffic. In `deploy.sh`:

```bash
docker compose -f /opt/pallettrack/${NEW_COLOUR}/docker-compose.yml \
  run --rm web python manage.py migrate --check   # dry-run first
docker compose -f /opt/pallettrack/${NEW_COLOUR}/docker-compose.yml \
  run --rm web python manage.py migrate
```

**Forward/backward compatibility (dual-write pattern):**
- Add columns as `NULL` or with a default — never `NOT NULL` without a default in the same release
- During the deploy window both colours point at the same Neon database; the old colour must tolerate the new schema
- Remove old columns only in a **follow-up release**, after the column has been unused for one full deploy cycle

**If migration fails:**
- The `migrate` step returns non-zero → `deploy.sh` exits before touching `active-upstream.conf`
- The old colour remains active; no traffic disruption
- CI marks the deploy job failed; alert fires via GitHub Actions notification / PagerDuty webhook
- The failed colour's containers are stopped and the image is quarantined for debugging

---

## Celery Workers

```yaml
# docker-compose.yml (excerpt — same image, different CMD)
services:
  web:
    image: ghcr.io/hps-gd/pallettrack:${IMAGE_TAG}
    command: gunicorn pallettrack.wsgi:application --bind 0.0.0.0:8000

  worker:
    image: ghcr.io/hps-gd/pallettrack:${IMAGE_TAG}
    command: >
      celery -A pallettrack worker
        --loglevel=info
        --soft-time-limit=30
        --time-limit=60
        --concurrency=4

  beat:
    image: ghcr.io/hps-gd/pallettrack:${IMAGE_TAG}
    command: celery -A pallettrack beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
    deploy:
      replicas: 1   # beat must be a singleton — never scale this
```

**Graceful shutdown:** `--soft-time-limit=30` raises `SoftTimeLimitExceeded` in the task (catchable for cleanup); `--time-limit=60` sends `SIGKILL` as a hard backstop. Docker's `stop_grace_period` should be set to `70s` to give tasks the full window.

**Beat singleton:** Beat must run as exactly one replica. Coordination is via `django-celery-beat`'s database-backed scheduler — the DB lock prevents duplicate firings if you ever temporarily run two replicas. Do not put beat behind a load balancer.

---

## Decision Checkpoint — New Infrastructure with Ongoing Cost

```
DECISION REQUIRED before proceeding:

Container registry:
  - GHCR (free for public repos; ~$0.25/GB/mo for private) — already on GitHub, zero new accounts
  - Docker Hub (free tier: 1 private repo, rate-limited pulls) — gets painful fast
  - ECR (~$0.10/GB/mo + data transfer) — adds AWS dependency

Hosting:
  - Stay on bare-metal + docker compose (~$0 added cost) — lowest complexity, matches current ops model
  - Fly.io (~$50–150/mo depending on sizing) — managed, but adds a new vendor and egress costs
  - ECS Fargate (~$80–200/mo) — fully managed, but significant AWS surface area for a twice-weekly deploy cadence

Recommendation: GHCR (already on GitHub, GITHUB_TOKEN auth is automatic in Actions) +
bare-metal docker compose (zero added cost, you own the server, blue/green is trivial to
implement with two compose stacks). Confirm or escalate before I finalise registry and
hosting configuration.
```

---

## Environment Configuration

Secrets are **never baked into the image**. Neon credentials, `DJANGO_SECRET_KEY`, Redis URL — none of these appear in a layer.

**Options (pick one):**

```bash
# Option A — docker-compose env_file (simplest)
# docker-compose.yml:
env_file: /opt/pallettrack/.env.production   # gitignored, owned by deploy user, chmod 600

# Option B — systemd EnvironmentFile (if running compose as a systemd unit)
# /etc/systemd/system/pallettrack-blue.service:
EnvironmentFile=/opt/pallettrack/blue/.env.production

# Option C — Doppler or 1Password CLI at deploy time
doppler run -- docker compose up -d
# or
op run --env-file=.env.template -- docker compose up -d
```

`.env.production` is on the server only, chmod 600, owned by the `deploy` user. It is never committed to git. The CI pipeline injects only non-secret build-time args (e.g. `IMAGE_TAG`).

---

## Observability

**The key shift:** you're moving from `tail -f /var/log/pallettrack/app.log` on one box to ephemeral containers that write to stdout/stderr. Plan for this explicitly.

**Health endpoints** (add these to Django before the first deploy):
```python
# pallettrack/urls.py
path("healthz", views.healthz),   # liveness — returns 200 if process is up
path("readyz", views.readyz),      # readiness — returns 200 only when DB + Redis are reachable
```
Nginx uses `healthz`; the blue/green deploy script polls `readyz` before switching upstream.

**Log aggregation:** configure Docker's logging driver to ship stdout/stderr:
```json
// /etc/docker/daemon.json
{
  "log-driver": "loki",
  "log-opts": {
    "loki-url": "http://localhost:3100/loki/api/v1/push",
    "loki-pipeline-stages": "..."
  }
}
```
Alternatives: Datadog agent sidecar, Fluentd → CloudWatch. The key constraint: **no local log files** — containers are ephemeral. Logs must leave the host.

**Metrics:** add `django-prometheus` to `requirements.txt`:
```python
# settings.py
INSTALLED_APPS += ["django_prometheus"]
# urls.py
path("metrics", include("django_prometheus.urls"))
```
Prometheus scrapes `/metrics`; Grafana visualises. Default exporters cover request latency, DB query counts, cache hits — enough to diagnose the most common regressions post-deploy.

**Uptime checks:** external probe (UptimeRobot free tier, or Grafana Cloud synthetic monitoring) hitting `https://pallettrack.app/healthz` every 60 seconds. Alerts on 2 consecutive failures. This is your canary for the Nginx swap — if it goes red post-deploy, rollback immediately.

---

**Next step is your call on the Decision Checkpoint** — confirm GHCR + bare-metal and I'll produce the full `deploy.sh` script and the two `docker-compose.yml` files (blue/green) ready to drop onto the server.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/16.0 (100%) |
| Evaluated | 2026-05-27 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 93685 ms |
| Target cost | $0.3030 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent checks for existing IaC (Pulumi.yaml, .tf files), existing CI workflows, and existing Dockerfiles before proposing anything new | PASS | Reconnaissance section lists all three checks verbatim and reports 'Greenfield — no existing IaC, CI workflows, or Dockerfiles found.' |
| c2 | Agent produces a Dockerfile that uses multi-stage builds, a non-root user, pinned base image versions, and a HEALTHCHECK instruction | PASS | Dockerfile has builder+runtime stages, `useradd`+`USER app`, `python:3.12-slim` pinned, and HEALTHCHECK with all four params (interval/timeout/start-period/retries). |
| c3 | Agent defines a CI/CD pipeline with stages in the correct order: lint → build → test → security scan → deploy | PASS | GitHub Actions YAML shows jobs lint → build (needs: lint) → test (needs: build) → security-scan (needs: test) → deploy (needs: security-scan). |
| c4 | Agent addresses zero-downtime deployments explicitly — describes a mechanism (blue/green, rolling update, or health-check-gated) with reasoning | PASS | Dedicated section 'Zero-Downtime Mechanism: Blue/Green with Nginx Upstream Switching' with justification for twice-weekly cadence and comparison table. |
| c5 | Agent defines a rollback plan with specific commands or steps, not just 'roll back the deployment' | PASS | Rollback section contains exact bash commands: `sudo cp ... && sudo nginx -t && sudo nginx -s reload` + `curl -fsS https://pallettrack.app/healthz`, with '<30 seconds' budget. |
| c6 | Agent stops and asks before recommending new cloud resources with ongoing cost (as required by the decision checkpoints) | PASS | Decision Checkpoint section explicitly states 'DECISION REQUIRED before proceeding' with cost figures per option and 'Confirm or escalate before I finalise'. |
| c7 | Agent addresses the Celery worker migration alongside the web server — not just the Django app in isolation | PARTIAL | Dedicated 'Celery Workers' section with docker-compose excerpt for worker+beat, graceful shutdown flags (--soft-time-limit/--time-limit), and beat singleton constraint. |
| c8 | Agent references the cattle-not-pets principle and ensures the deployment design treats containers as disposable/reproducible | PASS | Dedicated 'Cattle-not-Pets' section quotes verbatim: 'Treat containers as disposable, reproducible artifacts; no SSH-into-the-box state mutation; rebuild from image, never patch in place.' |
| c9 | Output's Dockerfile (or container build description) is a multi-stage build with a non-root user, a pinned base image version (e.g. `python:3.12-slim` not `python:latest`), and an explicit HEALTHCHECK | PASS | Dockerfile: builder/runtime stages, `python:3.12-slim` pinned, `USER app`, HEALTHCHECK `--interval=30s --timeout=5s --start-period=10s --retries=3`. |
| c10 | Output addresses the two distinct workloads — the Django web app and the Celery workers — as separate container images or processes, not bundled into one image | PASS | docker-compose excerpt shows web, worker, and beat as separate services with distinct `command:` entries, all using the same image tag. |
| c11 | Output's CI/CD pipeline orders stages as lint → build → test → security scan → deploy, with each stage gating the next, and names the tool (GitHub Actions / GitLab CI / Jenkins) consistent with the project conventions | PASS | File named `.github/workflows/deploy.yml`, tool is GitHub Actions, `needs:` gates enforce lint→build→test→security-scan→deploy order. |
| c12 | Output's zero-downtime mechanism is named explicitly (rolling update, blue/green, or canary) with reasoning for the choice given the twice-weekly deploy cadence — not just 'we'll do zero-downtime' | PASS | 'Blue/green' named; comparison table contrasts rolling and canary; 'twice a week…does not justify the operational overhead' explicitly stated. |
| c13 | Output's rollback plan includes specific commands or steps (kubectl rollout undo, fly deploy --image previous_tag, swap traffic back to old colour) with a stated time budget — not 'redeploy the previous version' | PASS | Bash commands `sudo cp upstream-blue.conf ... && nginx -s reload` + healthz curl check, time budget explicitly '< 30 seconds end-to-end'. |
| c14 | Output addresses Django migrations explicitly — when migrations run in the deployment, how forward/backward compatibility is preserved across the rolling update, and what happens if a migration fails | PASS | 'Django Migrations' section covers: migrate runs before colour switch, additive-only/dual-write pattern, and migration failure path (deploy.sh exits, old colour stays live, CI alert). |
| c15 | Output stops and asks before recommending new infrastructure with ongoing cost (e.g. Kubernetes cluster, container registry, managed Redis for Celery broker), framing the cost trade-offs | PASS | Decision Checkpoint block lists GHCR/Docker Hub/ECR with $/GB figures, bare-metal/Fly.io/Fargate with $/mo ranges, ends with 'Confirm or escalate before I finalise'. |
| c16 | Output addresses environment configuration — secrets handling (not baked into the image), env var injection at runtime, and how Neon Postgres credentials reach the container without ending up in a layer | PASS | 'Environment Configuration' section states 'never baked into the image', offers three injection options (env_file, systemd EnvironmentFile, Doppler/1Password), explicitly mentions Neon credentials. |
| c17 | Output addresses observability for the new deployment — health endpoints, log aggregation, metrics — given the move from a single bare-metal server with familiar logs to ephemeral containers | PARTIAL | 'Observability' section covers /healthz+/readyz endpoints, Loki/Datadog log aggregation, django-prometheus /metrics, uptime checks, and explicitly flags the shift from `tail -f` to ephemeral container stdout. |

### Notes

The output is a comprehensive, well-structured response that satisfies every criterion at or above threshold. Both PARTIAL-capped criteria (Celery workers and observability) were actually addressed more thoroughly than required, but the ceilings hold them at 0.5 each.
