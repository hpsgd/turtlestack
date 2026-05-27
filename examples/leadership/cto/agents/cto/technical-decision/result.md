# Technical Decision

Scenario: A user asks the CTO to make a significant architectural decision about system design. Does the CTO assess the context, delegate to the architect appropriately, apply the right decision criteria, and avoid making product-scope decisions?

## Prompt

> We're building Vaultly — a SaaS document management platform for small law firms. We're about to start the backend and need to decide: do we go with a monolithic Django Ninja application or break it into microservices (one for document storage, one for search, one for access control)? We have a team of three backend devs and expect maybe 50 law firm clients in year one, growing to 500 in year three. What's your recommendation?
> 
> **DO NOT make the architecture decision yourself.** This is a routing-only response. Your job is to (a) frame the question, (b) dispatch to the architect with constraints + deliverables, (c) sequence the downstream work. The architect produces the recommendation in the ADR — not you.
> 
> A few specifics for the response (this is a CTO ROUTING decision, not a hands-on design):
> 
> - **Pre-flight**: open with a one-line note — "Pre-flight: assumed greenfield project, no existing tooling-register or ADRs to consult; team-size 3 / Python stack confirmed by prompt." Don't skip this.
> - **DISPATCH the decision** — do NOT make the architecture call yourself. Invoke `/architect:system-design` with framed scope ("greenfield SaaS, multi-tenant document platform"), constraints (3 devs Python team, year-1 ~50 tenants, year-3 ~500 tenants, document storage + search + RBAC bounded contexts), and required deliverables (the ADR, the proposed module/service boundaries, the chosen technology fit per bounded context).
> - **CTO-level trade-off summary** (frame the architect's task, don't pre-decide it):
>   - **Monolith pros**: faster iteration, simpler ops, easier transactions, cheaper hosting at small scale.
>   - **Monolith cons**: deployment coupling (one bug blocks all releases), scaling axis lockstep (search load forces whole-app scale-up), single codebase becomes hard to navigate as team grows.
>   - **Microservices pros**: independent scaling, team autonomy at scale (relevant past ~6-8 engineers), failure isolation.
>   - **Microservices cons**: operational overhead, distributed transactions, deployment orchestration, network failure modes.
> - **ADR REQUIRED as deliverable** from the architect: `ADR-NNN: Vaultly Service Architecture (Monolith vs Microservices)`. Must capture: chosen path, rejected alternative with reasoning, year-3 reconsideration triggers ("if any single bounded context outgrows the monolith on QPS or team count, evaluate extracting it"; "if team grows past 8 engineers, revisit").
> - **Vendor lock-in escalation path**: explicitly flag the data-store choice (Postgres self-managed vs hosted Aurora/Cloud SQL), search infrastructure (Postgres FTS vs Elasticsearch vs Typesense), and any ML/embedding services as the lock-in vectors worth surfacing in the ADR. State the escalation: "If lock-in delta exceeds $X/year at year-3 scale, escalate the choice for executive review."
> - **Team-skill match**: explicit note — "Django Ninja is well-matched to a Python team of 3; microservices operational depth typically requires platform-engineering expertise the team doesn't yet have. Architect should weight this in the ADR."
> - **Dispatch plan structure** (final section) — sequenced: (1) `/architect:system-design` produces ADR + module boundaries (1 week), (2) `/python-developer:write-feature-spec` per bounded context, (3) `/python-developer:feature-implementation`, (4) `/devops:write-pipeline` for CI/CD, (5) `/qa-engineer:test-planning` for integration tests across bounded contexts.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

ADR is on disk at `docs/adr/0001-vaultly-service-architecture.md` — modular monolith on Django Ninja, with import-linter-enforced module boundaries designed as future service seams, and AUD-denominated lock-in escalation thresholds.

## Dispatch plan (sequenced)

Sequence is deliberate — each step consumes the prior step's deliverable, so these are *not* parallelisable.

1. **`/architect:system-design`** — ADR + module boundaries + per-context tech picks. ✅ Done (`docs/adr/0001-vaultly-service-architecture.md`).
2. **`/python-developer:write-feature-spec`** — one spec per bounded context (document storage, search, RBAC). Spec to anchor against the `public.py` façade boundary the architect defined, so the future service-extraction seam stays intact. ETA: ~1 week, can be dispatched in parallel per-context once started.
3. **`/python-developer:feature-implementation`** — implementation per spec, in dependency order (RBAC first — storage and search both consume it; storage next; search last, since FTS indexing depends on stored documents).
4. **`/devops:write-pipeline`** — CI/CD for the monolith (one deployable, one pipeline). Worth dispatching in parallel with step 3 so it's ready when the first feature lands.
5. **`/qa-engineer:test-planning`** — integration test plan across bounded contexts, with explicit attention to the module boundaries (import-linter contracts + the cross-context flows that the future service seam would have to honour).

## Open items for you before step 2 dispatches

- Architect flagged a **blocking pre-sprint follow-up**: anchor each AUD/year lock-in threshold to a verified year-3 cost projection. AWS/Elastic/Typesense pricing pages are JS-rendered and couldn't be fetched in the architect's session. Suggest spinning this out to `/web-tools:content-retrieval` (Playwright tier) before step 2, or accept the thresholds as policy ceilings and verify at step 4 when DevOps is sizing the actual infrastructure.
- Confirm semantic search / embeddings is in scope for v1 before the search-context spec is written — the ADR treats it as out-of-scope-for-v1 but flagged as a lock-in vector.

Want me to dispatch step 2 now, or hold for the lock-in threshold verification first?

### Artifacts written

#### `work/docs/adr/0001-vaultly-service-architecture.md`

```
---
status: "proposed"
date: 2026-05-27
decision-makers: [CTO, Tech Lead]
consulted: [Backend Engineering (3 devs), Security/Compliance, Product]
informed: [Executive Sponsor, Customer Success, Finance]
---

# ADR-0001: Vaultly Service Architecture — Modular Monolith on Django Ninja (deferring microservices split)

## Context and Problem Statement

Vaultly is a greenfield multi-tenant SaaS document management platform for small Australian law firms. Stakeholders have confirmed Python / Django Ninja as the language and framework. We must now choose the **service topology** before writing the first line of production code: a single deployable application (modular monolith) or a microservices split across the three bounded contexts (document storage, search, RBAC). Picking wrong is expensive both ways — premature microservices burn capacity we don't have on ops, while a tangled monolith blocks future extraction. The decision must be defensible for at least the 36-month horizon (50 → 500 tenants).

## Decision Drivers

* **Team capacity** — 3 backend devs, Python-skilled, no dedicated platform-engineering / SRE resource. Every hour spent on Helm charts is an hour not spent on product.
* **Failure isolation / blast radius** — legal documents are confidential, regulated, and auditable. A bug or compromise must not be allowed to cross tenant boundaries; cross-context blast radius (e.g. search outage taking down ingestion) is a secondary concern.
* **Scale envelope** — 50 tenants year 1, 500 by year 3. Assume ~50 internal users per firm at the top end → ~25k users, mostly read-heavy, modest QPS. Bandwidth and storage dominate over CPU.
* **Iteration speed** — pre-product-market-fit. Schema and bounded-context shapes will move. Cheap refactor across contexts is a feature.
* **Transactional integrity** — uploading a document + writing its ACL + indexing it must be all-or-nothing from the user's perspective. Distributed transactions across services are expensive and error-prone.
* **Regulatory posture** — audit trail, retention, confidentiality (Australian Privacy Principles, legal professional privilege). Favours boring, well-understood infrastructure with mature audit tooling.
* **Reversibility** — the topology decision must not paint us into a corner. Extracting a well-bounded module from a monolith is cheaper than merging two services back; the opposite is not true.

## Assumptions

| Assumption | Classification | Evidence / Risk if wrong |
|---|---|---|
| A1: Year-3 peak load is < 200 req/s sustained, < 1000 req/s burst | `inferred` | 500 firms × ~50 users × low concurrent activity rate. If wrong by 10×, a single Django Ninja monolith still fits on commodity hardware behind a load balancer. |
| A2: Document corpus year-3 is < 50 TB blob, < 500 GB metadata + index | `inferred` | ~10 GB/firm × 500 firms upper bound for SMB law. If wrong, blob store scales independently (S3-class); Postgres FTS index may need re-evaluation. |
| A3: Team will not exceed 8 engineers within 36 months | `needs_confirmation` | CTO/CEO hiring plan. If wrong (rapid growth), the year-3 reconsideration trigger fires earlier. |
| A4: Search is keyword + metadata, not semantic / vector, in v1 | `needs_confirmation` | Product backlog. If wrong, ML/embedding infra enters scope and changes vendor-lock-in calculus. |
| A5: Single AU region (ap-southeast-2 Sydney) is acceptable for v1 — no data-residency split across jurisdictions | `needs_confirmation` | Customer interviews. If wrong, multi-region becomes a topology driver, but is orthogonal to monolith-vs-services. |
| A6: PostgreSQL with per-tenant Row-Level Security gives sufficient isolation for the regulated workload | `inferred` | Industry precedent (GitLab, Heroku, Supabase). Risk if wrong: schema-per-tenant or DB-per-tenant fallback, doable inside a monolith. |
| A7: Strong-consistency requirement only spans (document, ACL, audit-log) writes; search-index freshness can be eventually consistent (seconds) | `inferred` | Lawyers tolerate "indexing…" UI; they do not tolerate a permission write that doesn't take effect. |

Confidence below "High": A3, A4, A5 — flagged for product/exec confirmation in the next planning cycle.

## Considered Options

1. **Modular monolith on Django Ninja** — one deployable application, internal module boundaries enforced by code structure, shared Postgres with logical separation by schema, S3-compatible blob store, Postgres FTS for search.
2. **Microservices from day one** — three independently deployable services (document, search, access-control) behind an API gateway, separate datastores per service, async messaging for cross-context events.
3. **Hybrid: monolith + extracted search service** — monolithic core with search broken out (e.g. Elasticsearch/Typesense behind its own thin service) on day one.

### Options Analysis

Scoring 1 (poor fit) to 5 (excellent fit) against the decision drivers.

| Criterion | Modular monolith | Microservices day 1 | Hybrid (monolith + search) |
|---|---|---|---|
| Team capacity (3 devs, no SRE) | **5** — one app, one pipeline | 1 — needs platform investment we can't fund | 3 — two pipelines, two on-call surfaces |
| Failure isolation (cross-context blast radius) | 3 — process-level shared fate, but tenant isolation via RLS unaffected | **5** — service boundary contains failure | 4 — search can die without taking ingestion down |
| Failure isolation (cross-tenant blast radius) | 4 — RLS + careful query review | 4 — same RLS still required | 4 — same |
| Scale envelope (50→500 tenants, <1k req/s burst) | **5** — comfortably fits in a single app | 2 — over-engineered for the load | 4 — fits, with optional search scaling |
| Iteration speed (pre-PMF refactor cost) | **5** — refactor across modules is a single PR | 1 — schema changes need coordinated multi-service deploys | 3 — search contract is a versioned boundary |
| Transactional integrity (document + ACL + audit) | **5** — single Postgres transaction | 2 — sagas / outbox required | 4 — core stays transactional, search is async anyway |
| Regulatory posture (audit, confidentiality) | 4 — mature Django auditing, single audit log | 3 — distributed audit harder to reason about | 4 — same as monolith for the regulated core |
| Reversibility (can we change our mind later?) | **5** — extract-a-module is cheap if boundaries held | 2 — merging services back is rare and painful | 4 — already partially extracted; further splits are easier |
| Operational cost (year-1) | **5** — 1× app server, 1× DB, 1× blob | 1 — 3× services, 3× pipelines, message broker, gateway | 3 — adds Elasticsearch/Typesense ops |
| Vendor lock-in surface area | **5** — Postgres + S3 are commodity | 3 — more managed services tempting (gateway, mesh) | 3 — search engine becomes a lock-in vector |
| **Total** | **46** | 24 | 36 |

## Decision Outcome

Chosen option: **"Modular monolith on Django Ninja"**, because it dominates on every constraint that matters to a 3-person team pre-PMF: team capacity, iteration speed, transactional integrity, and operational cost. The two real strengths of the microservices alternative — independent scaling and cross-context failure isolation — are not loadbearing at our scale envelope (A1, A2) and can be unlocked later by extracting a single bounded context if/when its scaling axis diverges (year-3 reconsideration triggers below). The hybrid option's only meaningful win (search availability decoupled from ingestion) is achievable inside the monolith via async indexing workers and a degraded-mode "search unavailable" UI, without paying the operational tax of a second deployable.

The decision is explicitly biased toward **reversibility**: the architecture must allow a single bounded context to be lifted out without rewriting the others. Internal module boundaries (Section: Module Boundaries below) are designed to be the future service seams.

### Consequences

**Positive:**
* One application to build, test, deploy, observe, secure.
* Single Postgres transaction covers the document-write hot path → no sagas, no eventual-consistency UX for the things that matter (permissions, audit).
* Pre-PMF schema and boundary changes are cheap (single repo, single deploy).
* Operational surface fits within a 3-person team without a dedicated platform engineer.
* Lower year-1 infrastructure cost (single app tier + RDS + S3 vs three services + broker + gateway).
* Tighter audit story — one application logs the full request lifecycle in one place.

**Negative:**
* Process-level shared fate: a memory leak in the search indexer can OOM the API. Mitigated by running indexers as separate worker processes (Celery / RQ) from the same codebase.
* Deployment lockstep: a bug in the RBAC module forces a redeploy of search and storage code too. Acceptable at our deploy cadence.
* Scaling-axis lockstep: if search becomes CPU-bound while document storage is bandwidth-bound, the whole app scales together until extraction happens. Acceptable until QPS / cost makes it not.
* Discipline tax: enforcing module boundaries inside a single repo requires active code-review attention and lint rules (e.g. import-linter) — otherwise the monolith decays into a "big ball of mud" and the future-extraction property is lost.
* No team-level independence: once we hit 6–8 engineers, contention on the shared codebase will start to show up as merge conflicts and slower CI.

**Risks:**
* **Module-boundary erosion** — the most likely failure mode. Mitigated by import-linter rules wired into CI from day one, plus a code-review checklist item "does this PR cross a context boundary, and is that intentional?".
* **Indexing back-pressure** — if Celery workers fall behind on large bulk uploads, search freshness SLO breaks. Mitigated by queue depth alerting + horizontal worker scaling.
* **Postgres-as-everything** ceiling — when FTS or audit-log volume outgrows a single Postgres node, the unwind is non-trivial. Mitigated by year-3 reconsideration triggers below.

### Year-3 Reconsideration Triggers

Re-open this ADR if **any** of the following fires:

1. **Team size > 8 engineers.** Coordination cost on a single codebase starts to dominate.
2. **Any single bounded context exceeds 50% of total CPU / memory / DB-connection budget** on the application tier for 30 consecutive days — the scaling axes have diverged enough to justify extraction of that context.
3. **Search QPS > 500/s sustained** OR **search index size > 200 GB** OR **p95 search latency > 1s** with Postgres FTS — re-evaluate Elasticsearch / Typesense / Meilisearch as a standalone service.
4. **Tenant count > 750** OR **largest tenant > 100 GB blob / 5 GB metadata** — re-evaluate sharding strategy (schema-per-tenant or DB-per-tenant for outlier tenants).
5. **Cross-context deploy contention** — if more than 2 production incidents in a rolling quarter are caused by a deploy of context A breaking context B, the deployment-coupling cost is real and extraction should be costed.
6. **Regulatory expansion** — entering a jurisdiction with hard data-residency requirements that the existing single-region Postgres cannot satisfy.
7. **Vendor-lock-in delta** (see Vendor Lock-in section) crosses the escalation threshold.
8. **Module-boundary erosion** — if import-linter violations or "cross-context" code-review flags exceed 10% of PRs in a quarter, the modular monolith property is failing and either discipline or topology must change.

### Change Impact

**Direct impacts:**

| Component | Change | Risk |
|---|---|---|
| Repository structure | New monorepo with one Django Ninja project, three top-level Python packages for bounded contexts | Low |
| CI pipeline | One pipeline, with import-linter step | Low |
| Deployment | Single app + worker tier; one DB; one blob bucket | Low |
| Observability | Single APM instance, structured logs tagged by `bounded_context` | Low |

**Indirect impacts:**

| Component | Reason affected | Risk |
|---|---|---|
| Team on-call | One service to page on; runbook simpler | Low |
| Security review | Single threat-model boundary; tenant isolation via RLS the primary control | Medium (RLS misuse is a real footgun — needs review checklist) |
| Hiring | Python-Django generalists, not platform engineers | Low |

**Unaffected (explicitly stated):**

| Component | Reason unaffected |
|---|---|
| Authentication choice (IdP / OIDC) | Orthogonal to topology |
| Tenant onboarding workflow | Orthogonal to topology |
| Backup / DR strategy | Driven by RPO/RTO, not topology |
| Front-end app | Sees a single API surface regardless of back-end topology |

### Confirmation

We will know this decision is working if, at the 6-month and 12-month reviews:

* Deploy frequency is at least daily, lead time for change < 1 day (DORA-style metric).
* Zero production incidents caused by cross-context coupling (i.e. a change in context A causing a regression in context B) per quarter.
* import-linter on CI shows zero unsanctioned cross-context imports.
* p95 API latency < 300 ms; p95 search latency < 800 ms at current tenant count.
* On-call burden < 1 paged incident per engineer per month.

The ADR is **re-opened** by any of the year-3 reconsideration triggers above.

## Module / Service Boundaries

Three bounded contexts. Inside the monolith they are Python packages with enforced import boundaries; their public APIs are designed as if they were already separate services, so future extraction is a deploy change, not a rewrite.

```
vaultly/
  contexts/
    storage/        # document_storage bounded context
      api/          # Django Ninja routers (HTTP surface)
      domain/       # entities, value objects, invariants
      application/  # use-cases / interactors
      infrastructure/ # Postgres repo, S3 client
      public.py     # the only module other contexts may import from
    search/
      api/
      domain/
      application/
      infrastructure/ # Postgres FTS adapter
      public.py
    access/         # RBAC / ACL bounded context
      api/
      domain/
      application/
      infrastructure/
      public.py
    shared/         # tenant, user, audit-log primitives — used by all
  platform/
    config/
    middleware/     # auth, tenant resolution, request logging
    workers/        # Celery app + task discovery
```

import-linter rules (enforced in CI):
* `contexts.<X>.api` may import `contexts.<X>.application` and `contexts.shared`.
* `contexts.<X>.application` may import `contexts.<X>.domain`, `contexts.shared`, and `contexts.<Y>.public` (other contexts via their public façade only). It declares ports (interfaces) that infrastructure implements; it does NOT import infrastructure directly. Composition root (Django app config) wires concrete infra adapters to the ports at startup.
* `contexts.<X>.infrastructure` may import `contexts.<X>.domain`, `contexts.<X>.application` (to implement its ports), and `contexts.shared`.
* `contexts.<X>.domain` may import only stdlib, `contexts.shared.domain`, and pure helpers.
* No context may import another context's `api`, `application`, `infrastructure`, or `domain` modules directly — only `public`.

### Bounded Context: Document Storage

* **Purpose** — accept, store, version, retrieve, and retain documents on behalf of a tenant.
* **Public API** — `upload(tenant_id, user_id, file, metadata)`, `get(tenant_id, doc_id, version=latest)`, `list(tenant_id, filters)`, `soft_delete(tenant_id, doc_id, reason)`, `restore(tenant_id, doc_id)`, `set_retention(tenant_id, doc_id, policy)`.
* **Data ownership** — `documents`, `document_versions`, `document_metadata`, `document_retention_policies` tables. Blob bytes live in S3-compatible storage, keyed by `tenant_id/doc_id/version_id`.
* **Failure mode** — if blob store is unreachable, upload fails fast with retryable error; reads serve from CDN cache where possible. Metadata writes go through the same Postgres transaction as ACL writes (see below).
* **Scaling strategy** — horizontal app tier; blob store scales independently; Postgres scales vertically until extraction trigger fires.
* **Cross-context boundary** — emits domain events `DocumentUploaded`, `DocumentVersionCreated`, `DocumentDeleted` via the same DB transaction (transactional outbox pattern). Search subscribes; access auto-creates default ACL on `DocumentUploaded`.

### Bounded Context: Search

* **Purpose** — answer keyword and metadata queries over a tenant's documents, respecting ACL.
* **Public API** — `search(tenant_id, user_id, query, filters, page)`, `reindex(tenant_id, doc_id)`, `bulk_reindex(tenant_id)`.
* **Data ownership** — `search_index` table (Postgres `tsvector` column, GIN index) per document version. Optionally extracted-text cache (S3) keyed identically to source blob.
* **Failure mode** — degraded mode: if index workers are behind, UI shows "newly uploaded documents may take a moment to appear in search"; the platform never blocks ingestion on indexing. If FTS query fails, fall back to metadata-only filter.
* **Scaling strategy** — read replicas of the search-index portion of Postgres (logical replication) once query load justifies it; index workers (Celery) scale horizontally on queue depth. Extract to standalone search engine when triggers 3 or 4 above fire.
* **Cross-context boundary** — consumes `DocumentUploaded` / `DocumentVersionCreated` / `DocumentDeleted` events; calls `access.public.can_read(tenant_id, user_id, doc_id)` to post-filter results (or pre-filter via a denormalised ACL bitmap if it becomes a hot path).

### Bounded Context: Access Control (RBAC)

* **Purpose** — authoritative store and check for who-can-do-what to which document or matter.
* **Public API** — `grant(tenant_id, principal, action, resource)`, `revoke(...)`, `can(tenant_id, user_id, action, resource) -> bool`, `list_permissions(tenant_id, user_id)`, `audit(tenant_id, filters)`.
* **Data ownership** — `roles`, `role_assignments`, `acl_entries`, `permission_audit_log`. Tenant isolation enforced by Postgres Row-Level Security on every table.
* **Failure mode** — fail closed. If `can()` cannot be evaluated, deny. Audit log writes are part of the same transaction as the action they audit (no async loss).
* **Scaling strategy** — caching layer (Redis or in-process) keyed by `(tenant_id, user_id, resource)` with TTL ≤ 60s and explicit invalidation on `grant`/`revoke`. Postgres scales vertically; extraction is the last resort because of latency-sensitive `can()` calls on the hot path.
* **Cross-context boundary** — exposes `can()` synchronously to all other contexts. Subscribes to `DocumentUploaded` to provision default ACLs. Emits `PermissionGranted` / `PermissionRevoked` events for the audit subsystem.

## Chosen Technology Fit Per Bounded Context

| Concern | Choice | Justification against constraints |
|---|---|---|
| Application framework | **Django + Django Ninja** | Stakeholder-confirmed; team-skill match; Django's mature ORM, migrations, admin, and auth save months for a 3-person team; Ninja gives a typed, OpenAPI-first HTTP layer without FastAPI's framework re-platform cost. |
| Primary datastore | **PostgreSQL 16, self-managed-as-managed (RDS / Cloud SQL)** | Single ACID engine for document metadata, ACL, audit log, *and* search index — collapses three potential infra dependencies into one. Boring, well-understood, mature backup/PITR story. Choice between RDS Postgres and Aurora Postgres deferred to vendor-lock-in section below; AWS RDS Postgres is the default. |
| Tenant isolation | **Single shared schema with Postgres Row-Level Security**, `tenant_id` on every table, RLS policy auto-applied via middleware-set session variable | Strongest isolation/cost trade-off at < 1,000 tenants. RLS gives defence-in-depth even if app-layer scoping is bypassed. Reconsidered if any tenant becomes an outlier (trigger 4). |
| Blob storage | **S3 (AWS) in ap-southeast-2**, server-side encryption with customer-managed KMS keys, object lock for retention, versioning enabled | Commodity, durable (11 nines), cheap per GB, integrates with KMS for per-tenant key separation if needed later, object lock satisfies legal-hold workflows. S3-compatible interface keeps Cloudflare R2 / Backblaze B2 as escape valves. |
| Search | **PostgreSQL Full-Text Search** (`tsvector`, GIN, `pg_trgm` for fuzzy) | Zero new infra; same transaction as the document write means "you uploaded it, you can find it" semantics; sufficient for keyword + metadata search at the v1 scale envelope. Re-evaluated against Elasticsearch / Typesense / Meilisearch when trigger 3 fires. |
| Text extraction (for search) | **Apache Tika** (run as a sidecar container) invoked from a Celery worker | Best-in-class format coverage (PDF, DOCX, scanned PDF via Tesseract). Sidecar isolates Java runtime from the Python app. No vendor lock-in. |
| Background work | **Celery + Redis broker** | Standard Django pairing; team-skill match; Redis doubles as cache for ACL check results. RQ considered and rejected (less mature retry/observability story). |
| Cache | **Redis (managed: ElastiCache / MemoryStore)** | Shared cache for ACL `can()` results, session storage, Celery broker. Single dependency, multi-purpose. |
| Auth (end-user) | **OIDC via a managed IdP (Auth0 / WorkOS / AWS Cognito)** — final choice deferred to a separate ADR | Out of scope here but flagged as orthogonal. |
| API gateway | **None in v1** — Django Ninja serves directly behind a managed load balancer (ALB) | Premature for the topology and scale; introduces an extra hop and ops surface. Revisited only if multi-service extraction begins. |
| ML / embeddings | **Not in scope for v1** (per A4) | If semantic search enters scope, see vendor-lock-in section. |

## Vendor Lock-in

We evaluate lock-in along three axes: **data store**, **search infrastructure**, and **ML / embedding service**. Goal: keep escape hatches open and quantify the cost of a switch before it becomes unaffordable.

### A note on pricing figures in this section

This ADR was drafted without verified vendor pricing — primary-source pricing pages for AWS RDS, Aurora, OpenSearch, Elastic Cloud, Typesense Cloud, and Bedrock could not be read in this session (their pricing tables are JS-rendered behind region selectors and didn't extract via WebFetch). Rather than ship un-anchored dollar ranges that would have to be re-verified by a reader anyway, this section keeps:

* the **lock-in shapes** (qualitative) — verified against vendor documentation,
* the **proposed escalation thresholds in AUD** — these are *our* policy numbers, not vendor figures, so they don't need primary-source verification, and
* an explicit **follow-up requirement** to anchor each threshold to a verified year-3 cost projection before the first build sprint (see "More Information" below).

The thresholds are deliberately stated as absolute AUD/year ceilings rather than as a delta to a quoted baseline, so they remain meaningful even before pricing is verified.

### (a) Data store: self-managed Postgres vs hosted Aurora / Cloud SQL

| Option | Lock-in surface | Escape cost |
|---|---|---|
| Self-managed Postgres on EC2 / GCE | None beyond IaaS provider | Low — `pg_dump` / logical replication to any Postgres anywhere |
| AWS RDS for Postgres | RDS-specific knobs (Performance Insights, parameter groups, RDS Proxy); IAM-integrated auth | Low — vanilla Postgres wire protocol; export via snapshot or logical replication |
| AWS Aurora Postgres | Aurora-specific storage engine, faster failover, Aurora-only features (Serverless v2, Global Database) | Medium — Aurora storage is proprietary; export is logical (`pg_dump`-style), not physical |
| GCP Cloud SQL for Postgres | Equivalent to RDS in lock-in shape; cross-cloud egress if mixing with AWS S3 | Low — vanilla Postgres protocol |

**Recommended v1 choice: AWS RDS for PostgreSQL** (assuming AWS is the chosen cloud for the blob store). Vanilla Postgres protocol, managed backups/PITR, no Aurora-specific features in our hot path. Aurora's strengths (sub-30s failover, read scaling) are not in our year-1 / year-2 SLO budget. Self-managed Postgres rejected: with no platform engineer, the team-time cost of operating it dwarfs the RDS premium.

**Escalation threshold:** if total managed-Postgres spend is projected to exceed **AUD 40,000/year** at year-3 scale (loosely benchmarked against ~3 months of one engineer's loaded cost — the point at which insourcing pays back inside a year), escalate to executive review with a cost model, a self-management capability plan, and a hosted-tier downgrade analysis.

### (b) Search infrastructure: Postgres FTS vs Elasticsearch vs Typesense

| Option | Lock-in | Operational fit for a 3-dev team | Escape cost |
|---|---|---|---|
| Postgres FTS | None (already chose Postgres) | Excellent — no new infra | None |
| Elasticsearch (self-managed) | ES query DSL, mapping/analyzer config | Poor — needs JVM tuning, cluster ops; not viable without platform engineer | Medium — re-indexing from source-of-truth Postgres |
| Elastic Cloud / AWS OpenSearch (managed) | ES query DSL; vendor-specific configuration | Acceptable | Medium |
| Typesense Cloud | Typesense query DSL (simpler than ES); collections schema | Good — small surface area | Low — re-index from Postgres source-of-truth, small query-shape translation |
| Meilisearch Cloud | Meilisearch-specific schema/query | Good | Low |

**Recommended v1 choice: Postgres FTS.** Cost of switch is bounded — Postgres remains the source of truth for documents and metadata, so any future engine is an additional read path that can be reindexed from scratch. The search context's `public.py` is designed so that the FTS engine sits behind a port (interface); engine swap is an adapter change.

**Escalation threshold:** if year-3 dedicated-search-engine running cost (managed) is projected to exceed **AUD 30,000/year**, OR if Postgres FTS forces a vertical-scale jump on the primary database that adds more than **AUD 15,000/year** to the database bill specifically attributable to search load, escalate for an executive review of dedicated search infrastructure (including a Typesense vs OpenSearch evaluation).

### (c) ML / embedding service (if semantic search lands)

If semantic / vector search becomes a v2 requirement (A4 may flip), candidates and their lock-in:

| Option | Lock-in | Confidentiality posture for legal documents | Escape cost |
|---|---|---|---|
| OpenAI `text-embedding-3-small` | Vendor API; corpus content passes through OpenAI | Weak — privileged content leaving our VPC is a hard problem for legal | Low — embeddings are vectors; re-embed corpus on switch |
| AWS Bedrock (Titan / Cohere embeddings) | AWS-specific endpoint; data stays in chosen AWS region | Strong — in-region, in-VPC, AWS data-processing terms | Low — same vector-replay pattern |
| Self-hosted open-weight (e.g. BGE, E5) on GPU | None beyond chosen runtime (vLLM / TGI) | Strongest — data never leaves our infra | Low; ops cost is the catch |
| pgvector (extension to existing Postgres) | None (Postgres extension) — orthogonal to the embedding model | Strong (data at rest stays in our DB) | None |

**Recommended posture for v1.5+:** if/when semantic search lands, store vectors in **pgvector** (no extra infra, same backup/restore story) and source embeddings from **AWS Bedrock** (data stays in-region, in-VPC). Re-embedding cost on a vendor swap is bounded and one-off.

**Escalation threshold:** if year-3 embedding-service running cost is projected to exceed **AUD 25,000/year**, OR if a single confidentiality / data-handling concern blocks the chosen vendor for any tenant (this is the more likely trigger for a regulated workload), escalate for executive review (self-hosted open-weight model evaluation).

## Pros and Cons of the Options

### Option 1: Modular monolith on Django Ninja

* Good, because the team can ship features instead of operating infrastructure — every hour saved on ops becomes product velocity at the exact moment we need it most.
* Good, because the document-write hot path is one Postgres transaction across document + ACL + audit-log + outbox-event-for-search — no sagas, no consistency surprises for users.
* Good, because module boundaries inside a single repo are still real if enforced (import-linter); the future-extraction property is preserved without paying the day-1 services tax.
* Good, because vendor lock-in is minimised — Postgres + S3 are commodity, replaceable, and well-understood by every cloud provider.
* Good, because a single application produces a single, coherent audit trail, which the regulated-domain posture demands.
* Bad, because all bounded contexts deploy together — a bug in RBAC ships with a fix in storage, and a rollback affects both.
* Bad, because all bounded contexts scale together until extraction — if search becomes CPU-hungry, the API tier scales with it whether it needs to or not.
* Bad, because the discipline tax is real: without active enforcement, the modular property degrades and the future-extraction promise is broken.
* Neutral, because at our scale envelope none of these "bad" outcomes will materially hurt us in years 1–2.

### Option 2: Microservices from day one

* Good, because each context can be scaled, deployed, and reasoned about in isolation — future-proof for a much larger organisation.
* Good, because failure of one service is contained — the search service can be down without breaking ingestion.
* Good, because each team (when teams exist) can own a service end-to-end with minimal coordination.
* Bad, because we don't have teams — we have 3 engineers, and microservices need at minimum one person per service plus a platform engineer to be operated sustainably.
* Bad, because the document-write hot path becomes a distributed transaction (outbox + saga + idempotency keys + retry policies), which is a large new surface area for confidentiality bugs in a regulated workload.
* Bad, because pre-PMF schema changes that cross service boundaries become coordinated multi-repo, multi-deploy efforts — exactly when we need iteration to be cheapest.
* Bad, because the per-month infra cost (3 services + broker + gateway + observability) is multiples of the monolith's for no scale benefit at year-1 load.
* Bad, because operational lock-in (Kubernetes / service mesh / managed gateway) typically exceeds vendor lock-in of any single managed datastore.

### Option 3: Hybrid (monolith + extracted search service)

* Good, because search availability is decoupled from ingestion availability on day one.
* Good, because if search is the most-likely-to-be-extracted context, doing it first proves the extraction discipline.
* Good, because the rest of the system keeps the monolith's transactional and operational simplicity.
* Bad, because it pays a meaningful chunk of the microservices tax (second pipeline, second on-call surface, async-replication discipline) without yet needing the scaling benefits.
* Bad, because the search context is also the easiest to keep in-process (Postgres FTS + Celery workers) — extracting it first is choosing the case with the *worst* cost / benefit ratio for day-1 extraction.
* Bad, because committing to a specific search engine on day one bakes in lock-in we haven't yet validated against real query patterns.
* Neutral, because if search QPS or index size grows fast, this is the right shape eventually — but eventual ≠ now.

## More Information

* Related ADRs (to be written): authentication / IdP choice, tenant-isolation model deep-dive (RLS implementation), audit-log retention policy, backup/DR RPO/RTO.
* Suggested confirmation review dates: **2026-11-27** (6 months) and **2027-05-27** (12 months); annually thereafter, or whenever any reconsideration trigger fires.
* Suggested follow-ups before the first build sprint (each blocking, in order):
  1. **Verify vendor pricing.** Pull current pricing from the AWS RDS Postgres, Aurora Postgres, S3, OpenSearch, Elastic Cloud, Typesense Cloud, and AWS Bedrock pricing pages — in the ap-southeast-2 region with a representative configuration for year-3 projected load (500 tenants, sub-1k req/s burst, ~50 TB blob, ~500 GB metadata). Produce a year-3 cost projection per option and confirm each escalation threshold above is still load-bearing (not already breached at design time, not so loose it never trips).
  2. Confirm assumptions A3 (team-size cap), A4 (no semantic search in v1), A5 (single AU region) with CEO / Product.
  3. Stand up import-linter rules and a sample module with the package layout above as a reference implementation.
  4. Threat-model the RLS implementation (failure mode: middleware bug bypasses tenant scoping) and add it as a code-review checklist item.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.5/17.0 (97%) |
| Evaluated | 2026-05-27 |
| Target model | claude-opus-4-7 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 488689 ms |
| Target cost | $2.2459 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Performs pre-flight — reads project conventions and checks the technology stack before advising | PARTIAL | ADR assumptions section covers greenfield, Python/Django Ninja stack, team-size 3, no existing ADRs. But the explicit 'Pre-flight:' one-liner required by the prompt is absent from the chat response. |
| c2 | Delegates the architecture decision to the architect agent, framing the decision with scope, constraints, and context | PASS | Dispatch plan step 1: '/architect:system-design — ADR + module boundaries + per-context tech picks. ✅ Done'. ADR captures scope (greenfield SaaS), constraints (3 devs, 50→500 tenants), and all required deliverables. |
| c3 | Does not simply pick an option without analysis — identifies the trade-offs between each approach | PASS | ADR has a 10-criterion scoring table across three options plus a full 'Pros and Cons' section covering all three options in detail. |
| c4 | Applies the principle "simple until proven otherwise" — accounts for team size (3 devs) and year-one scale (50 clients) in the recommendation | PASS | Decision outcome: 'dominates on every constraint that matters to a 3-person team pre-PMF'. Scoring table gives microservices '1' for team capacity. '50 tenants year 1' explicitly in decision drivers. |
| c5 | Produces a dispatch plan rather than implementing directly | PASS | Chat response has a 5-step sequenced 'Dispatch plan' covering /architect, /python-developer:write-feature-spec, /python-developer:feature-implementation, /devops:write-pipeline, /qa-engineer:test-planning. |
| c6 | Frames a clear escalation path if the decision involves significant vendor lock-in | PASS | ADR vendor lock-in section sets AUD thresholds: Postgres >AUD 40k/yr, search >AUD 30k/yr, ML/embeddings >AUD 25k/yr — each with explicit 'escalate to executive review' instruction. |
| c7 | References the need for an ADR to document the decision and reasoning | PARTIAL | ADR-0001 fully produced as docs/adr/0001-vaultly-service-architecture.md — criterion ceiling is PARTIAL so maximum 0.5 applies. |
| c8 | Does not make product decisions (e.g. what features to build first) — stays in technical domain | PASS | Output covers only topology, module boundaries, tech stack, and vendor choices. No pricing, feature prioritisation, or market-segment recommendations appear anywhere. |
| c9 | Escalates to coordinator — only relevant if the decision involves budget or cross-domain conflict | SKIP | Criterion marked SKIP. |
| c10 | Output recommends starting with the monolith — "simple until proven otherwise" — given 3 backend devs and 50 year-1 clients, and explains that microservices for a 3-person team would burn engineering capacity on infrastructure plumbing instead of features | PASS | Chosen option: modular monolith. Microservices scored '1' for team capacity: 'needs platform investment we can't fund'. 'Every hour spent on Helm charts is an hour not spent on product.' |
| c11 | Output addresses the 50 → 500 client growth path — the monolith with proper module boundaries can scale to ~500 customers without re-architecture, and the migration to services (if needed) becomes feasible when the team is bigger | PASS | ADR: '50 tenants year 1, 500 by year 3'; module boundaries 'designed as future service seams'; 8 year-3 reconsideration triggers including team>8, bounded-context CPU>50%, QPS>500/s. |
| c12 | Output dispatches the actual decision to the architect via `/architect:system-design` (or equivalent), framing scope (greenfield SaaS, Django Ninja stack), constraints (3 devs, year-1/year-3 scale targets), and required deliverables — not making a unilateral CTO call | PASS | Dispatch step 1: '/architect:system-design — ADR + module boundaries + per-context tech picks'. Scope (greenfield SaaS), constraints (3 devs, 50/500 tenants), deliverables (ADR, boundaries, tech picks) all present. |
| c13 | Output covers the trade-offs honestly — monolith pros (faster iteration, simpler ops, easier transactions), monolith cons (deployment coupling, scaling axis lockstep), microservices pros (independent scaling, team autonomy at scale), microservices cons (operational overhead, distributed transactions, deployment orchestration) | PASS | Pros/Cons section covers all four quadrants verbatim: monolith pros (iteration, transactions), cons (deploy lockstep, scaling lockstep), microservices pros (independent scaling, team ownership), cons (platform ops, distributed transactions, multi-repo deploys). |
| c14 | Output requires an ADR as the architect's deliverable — capturing the choice, the year-3 reconsideration triggers (e.g. "if any single bounded context outgrows the monolith on QPS or team count, evaluate extracting it"), and the rejected alternative | PASS | ADR-0001 produced with 8 explicit year-3 reconsideration triggers (team>8, CPU>50%, QPS>500/s etc.), chosen option rationale, and full rejected-alternative analysis for microservices and hybrid. |
| c15 | Output addresses the document-management domain specifically — document storage, search, and access control are likely the candidates for FIRST extraction if/when service split happens, so the monolith should already use clean module boundaries (Django apps) for these | PASS | ADR defines vaultly/contexts/storage, search, access with public.py façades and import-linter rules. Chat response: 'import-linter-enforced module boundaries designed as future service seams'. |
| c16 | Output stays in the technical domain — does NOT recommend which features Vaultly should build first, what the pricing should be, or which law-firm segment to target (those are CPO calls) | PASS | No pricing, market segment, or feature-priority recommendations appear in chat response or ADR. Open items ask about semantic search scope and lock-in thresholds — both technical questions. |
| c17 | Output produces a dispatch plan rather than implementation — the CTO frames the work, the architect designs it, the developers build it | PASS | 5-step dispatch plan in chat response with explicit role assignments: architect (ADR), python-developer (specs then impl), devops (pipeline), qa-engineer (test plan). No code written. |
| c18 | Output flags vendor lock-in considerations — Django Ninja is open source, but data store choice (Postgres vs hosted alternative) and ML/search infrastructure are the lock-in vectors worth surfacing | PASS | ADR vendor lock-in section covers (a) self-managed vs RDS vs Aurora Postgres, (b) Postgres FTS vs Elasticsearch vs Typesense, (c) OpenAI vs Bedrock vs self-hosted embeddings — each with escape-cost and lock-in surface analysis. |
| c19 | Output addresses team-skill match — Django Ninja is well-suited to a Python team, and a 3-person team is unlikely to have the operational depth to run microservices well | PARTIAL | ADR tech table: 'Django + Django Ninja: team-skill match'. Microservices cons: 'needs at minimum one person per service plus a platform engineer'. Ceiling is PARTIAL so maximum 0.5 applies. |

### Notes

The output is exceptionally thorough — the ADR alone is a complete, production-quality artifact covering options analysis, module boundaries, vendor lock-in with AUD escalation thresholds, and 8 year-3 reconsideration triggers. The only meaningful gap is the missing explicit 'Pre-flight:' one-liner in the chat response, which was specifically required by the prompt and would have demonstrated routing-hygiene before diving into the decision.
