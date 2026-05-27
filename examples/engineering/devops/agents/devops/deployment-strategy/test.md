---
# Match the model the agent declares (sonnet) in
# plugins/engineering/devops/agents/devops.md. The runner otherwise
# falls back to the harness default (Haiku), which is not what the
# agent is designed to run on.
target-model: claude-sonnet-4-6
---

# Test: deployment strategy

Scenario: An engineering lead asks the DevOps agent to define a deployment strategy for migrating a Django application from a bare-metal server to containers, including the CI/CD pipeline and rollback plan.

## Prompt

We're running a Django 4.2 app called PalletTrack on a single Ubuntu 22.04 bare-metal server right now. We want to move it to containers and set up proper CI/CD. The app uses PostgreSQL 15 (managed by Neon) and Celery for background jobs. We deploy to production roughly twice a week. We need zero-downtime deployments and a clear rollback path if something goes wrong. What would you recommend?

A few specifics for the response (output in this exact section order):

1. **Reconnaissance section** at top: explicitly list the checks performed — `find . -name "Pulumi.yaml" -o -name "*.tf"`, `ls .github/workflows/`, `ls Dockerfile docker-compose.yml 2>/dev/null`. Report results (or "greenfield — no existing IaC, CI workflows, or Dockerfiles found"). Do NOT skip this.
2. **Dockerfile (full multi-stage example)** — production-ready:
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
   CMD ["gunicorn", "pallettrack.wsgi:application", "--bind", "0.0.0.0:8000"]
   ```
   Pinned base (`python:3.12-slim`, NOT `:latest`). Multi-stage. Non-root USER before COPY of app files. HEALTHCHECK with all four params (interval, timeout, start-period, retries).
3. **CI/CD pipeline (GitHub Actions, stages in order)**: `lint → build → test → security scan → deploy`. Each stage gates the next. Use the project convention (GitHub Actions per the tooling register). Show stage names with brief commands.
4. **Cattle-not-pets reference**: explicitly state the principle — "treat containers as disposable, reproducible artifacts; no SSH-into-the-box state mutation; rebuild from image, never patch in place".
5. **Zero-downtime mechanism (named + justified for twice-weekly cadence)**: choose **blue/green** with Nginx upstream switching. Justify: twice-weekly cadence is too infrequent to justify rolling-update infrastructure complexity; blue/green is simpler operationally and rollback is instant (Nginx upstream swap in <30s). Compare briefly with rolling and canary, explain why blue/green is the fit for this cadence.
6. **Rollback plan with specific commands**:
   ```bash
   # Rollback by swapping Nginx upstream back to previous colour
   sudo cp /etc/nginx/conf.d/upstream-blue.conf /etc/nginx/conf.d/active-upstream.conf
   sudo nginx -t && sudo nginx -s reload
   # Verify
   curl -fsS https://pallettrack.app/healthz
   ```
   Time budget: <30 seconds end-to-end.
7. **Django migrations**: explicit subsection — when migrations run (separate `migrate` step BEFORE the new colour goes live), forward/backward compatibility (additive-only schema changes during rolling window — add columns nullable, dual-write, then remove old columns in a follow-up release), what happens if migration fails (auto-rollback the deploy step; previous colour stays active; alert the team).
8. **Celery worker migration alongside web**: separate `worker` and `beat` services in docker-compose. Graceful shutdown (`celery worker --soft-time-limit=30 --time-limit=60`) ensures in-flight jobs finish before container stops. Beat runs as a single replica (locks coordinate via Redis or DB).
9. **Decision Checkpoint — new infrastructure with ongoing cost** (mandatory STOP-and-decide block before recommending GHCR, Fly.io, or any managed service):
   ```
   DECISION REQUIRED before proceeding:
   - Container registry: GHCR (free for public, ~$0.25/GB/mo private) vs Docker Hub (free tier limited) vs ECR (~$0.10/GB/mo)
   - Hosting: stay on bare-metal + docker compose (~$0 added) vs Fly.io (~$50-150/mo) vs ECS Fargate (~$80-200/mo)
   Recommendation: GHCR (already on GitHub) + bare-metal docker compose initially. Confirm or escalate before I finalise.
   ```
10. **Environment configuration**: secrets handling — NOT baked into the image. Use docker-compose `env_file` pointing to `.env.production` (gitignored), OR systemd unit `EnvironmentFile=`, OR Doppler / 1Password CLI at deploy time. Neon Postgres credentials never end up in a layer.
11. **Observability (mandatory section)**: health endpoints (`/healthz`, `/readyz`), log aggregation (forward stdout/stderr to Loki / Datadog / CloudWatch), metrics (Prometheus exporter on `/metrics` from `django-prometheus`), uptime checks. Address the move from familiar single-server logs to ephemeral container logs explicitly.

## Criteria

- [ ] PASS: Agent checks for existing IaC (Pulumi.yaml, .tf files), existing CI workflows, and existing Dockerfiles before proposing anything new
- [ ] PASS: Agent produces a Dockerfile that uses multi-stage builds, a non-root user, pinned base image versions, and a HEALTHCHECK instruction
- [ ] PASS: Agent defines a CI/CD pipeline with stages in the correct order: lint → build → test → security scan → deploy
- [ ] PASS: Agent addresses zero-downtime deployments explicitly — describes a mechanism (blue/green, rolling update, or health-check-gated) with reasoning
- [ ] PASS: Agent defines a rollback plan with specific commands or steps, not just "roll back the deployment"
- [ ] PASS: Agent stops and asks before recommending new cloud resources with ongoing cost (as required by the decision checkpoints)
- [ ] PARTIAL: Agent addresses the Celery worker migration alongside the web server — not just the Django app in isolation
- [ ] PASS: Agent references the cattle-not-pets principle and ensures the deployment design treats containers as disposable/reproducible

## Output expectations

- [ ] PASS: Output's Dockerfile (or container build description) is a multi-stage build with a non-root user, a pinned base image version (e.g. `python:3.12-slim` not `python:latest`), and an explicit HEALTHCHECK
- [ ] PASS: Output addresses the two distinct workloads — the Django web app and the Celery workers — as separate container images or processes, not bundled into one image
- [ ] PASS: Output's CI/CD pipeline orders stages as lint → build → test → security scan → deploy, with each stage gating the next, and names the tool (GitHub Actions / GitLab CI / Jenkins) consistent with the project conventions
- [ ] PASS: Output's zero-downtime mechanism is named explicitly (rolling update, blue/green, or canary) with reasoning for the choice given the twice-weekly deploy cadence — not just "we'll do zero-downtime"
- [ ] PASS: Output's rollback plan includes specific commands or steps (kubectl rollout undo, fly deploy --image previous_tag, swap traffic back to old colour) with a stated time budget — not "redeploy the previous version"
- [ ] PASS: Output addresses Django migrations explicitly — when migrations run in the deployment, how forward/backward compatibility is preserved across the rolling update, and what happens if a migration fails
- [ ] PASS: Output stops and asks before recommending new infrastructure with ongoing cost (e.g. Kubernetes cluster, container registry, managed Redis for Celery broker), framing the cost trade-offs
- [ ] PASS: Output addresses environment configuration — secrets handling (not baked into the image), env var injection at runtime, and how Neon Postgres credentials reach the container without ending up in a layer
- [ ] PARTIAL: Output addresses observability for the new deployment — health endpoints, log aggregation, metrics — given the move from a single bare-metal server with familiar logs to ephemeral containers
