# Bottleneck Investigation

Scenario: User reports that API response times have degraded significantly under load, with P99 climbing from 200ms to 2s, and asks the performance engineer to investigate.

## Prompt

> Our API is getting slow under load. Two weeks ago P99 was around 200ms. Now it's hitting 2 seconds. P50 is still okay at about 180ms — it's the tail latency that's the problem. We're seeing this mostly on `GET /api/reports/{id}` and `POST /api/exports`. Traffic has grown about 30% in the past two weeks but that shouldn't explain a 10x P99 increase. We deploy multiple times a day so it's hard to pinpoint which change caused it. Can you investigate?
> 
> Do not ask for clarification — proceed using the information provided. State your assumptions where relevant.
> 
> A few specifics for the response (output in this exact section order):
> 
> 1. **Baseline section (FIRST, before any fixes)** — explicit table:
>    ```
>    | Metric            | 2 weeks ago | Now    | Delta  |
>    |-------------------|-------------|--------|--------|
>    | P50 latency       | ~180ms      | ~180ms | flat   |
>    | P95 latency       | (estimate)  | (estimate) | (delta) |
>    | P99 latency       | 200ms       | 2000ms | 10×    |
>    | Throughput (req/s)| baseline    | +30%   | +30%   |
>    | Error rate        | (record)    | (record) | (delta) |
>    ```
>    State the disproportionality explicitly: "10× P99 jump on 30% traffic growth is non-linear — suggests resource contention crossing a threshold, NOT linear scaling."
> 2. **Outside-in latency breakdown (BEFORE diving into DB)** — break the request flow into stages: client → load balancer → ingress → application layer → database → external calls → response. Estimate or measure time spent at each stage. Only narrow into the database AFTER you've identified database time as the likely contributor.
> 3. **Stack confirmation** — explicitly note "Assumed Python/Django stack based on common patterns; CONFIRM stack before recommending application profiler. If Python: `py-spy top --pid <pid>`. If Node: `clinic doctor`. If .NET: `dotnet-trace collect`. If JVM: `async-profiler`." Name the stack-appropriate profiler.
> 4. **Two-endpoint analysis** — `GET /api/reports/{id}` (read, sync) vs `POST /api/exports` (write, likely async). Different bottleneck profiles: reports → query/cache, exports → queue depth + lock contention + background-job worker capacity. Address each separately.
> 5. **Deploy bisection (multiple-times-a-day strategy)** — `git log --since="2 weeks ago" --pretty=format:"%h %ai %s"` to enumerate. Use deploy timestamps to bisect: identify the day when P99 crossed a threshold from APM, then bisect commits within that day.
> 6. **One-change-at-a-time discipline** — explicit subsection. Every recommended fix MUST be followed by a re-measurement step at the same load with the same metric BEFORE the next change. State the protocol: "warm-up 60s, sample 10min at fixed RPS, compare P99 with statistical significance (≥30 runs preferred for tight CI)."
> 7. **Decision Checkpoint before infrastructure scaling**: a STOP-and-decide block before any recommendation to add nodes, increase pool size, or upsize the DB. Frame: "Scaling will mask the underlying bottleneck and increase cost ~$X/month. Proceed only if root cause is confirmed and not addressable at the application layer."
> 8. **Findings table** with columns `Component | Impact (HIGH/MEDIUM/LOW) | Hypothesis | Evidence | Recommended Fix | Re-measure Plan`.
> 9. **Before/after measurement requirement** stated explicitly for every fix — same load, same metric, same protocol. No fix is "done" without before/after evidence.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

No application code in the workspace — this is a diagnostic/advisory response. I'll note the stack assumption explicitly as instructed and work from the symptom data provided.

---

## API Tail Latency Investigation: P99 Regression

---

### 1. Baseline

| Metric | 2 weeks ago | Now | Delta |
|---|---|---|---|
| P50 latency | ~180ms | ~180ms | flat |
| P95 latency | ~195ms (est.) | ~600–900ms (est.) | ~4–5× |
| P99 latency | ~200ms | ~2000ms | **10×** |
| Throughput (req/s) | baseline | +30% | +30% |
| Error rate | unknown — **measure now** | unknown — **measure now** | unknown |

**10× P99 jump on 30% traffic growth is non-linear — suggests resource contention crossing a threshold, NOT linear scaling.**

The P50 being flat is the critical diagnostic signal. If the slowdown were uniform (slow query, bloated payload, slower external call), P50 would have moved too. It hasn't. A flat P50 with a 10× P99 is the textbook signature of one of: connection pool exhaustion, lock contention, or queue saturation — all three are threshold effects. At low load, every request gets the resource immediately. As load climbs past a saturation point, a fraction of requests queue. That fraction sits entirely in the tail.

Establish the error rate baseline now before any changes — a rising P99 sometimes masks 504s being counted as "slow" rather than "failed."

---

### 2. Outside-In Latency Breakdown

Before assuming the database, break the request end-to-end and estimate where time is spent at each stage. Many P99 regressions turn out to be at the load balancer or connection layer, not in SQL.

```
CLIENT
  │  DNS + TLS + TCP: 10–50ms (stable across 2 weeks unless cert changed)
  ▼
LOAD BALANCER
  │  Queue + routing: <5ms (LB logs expose lb_processing_time)
  ▼
INGRESS / REVERSE PROXY (nginx, Caddy, ALB)
  │  Upstream wait time: THIS IS WHERE POOL EXHAUSTION SHOWS FIRST
  │  Check: upstream_response_time in nginx access logs or ALB TargetResponseTime
  │  If upstream_wait >> upstream_response, workers are saturated
  ▼
APPLICATION LAYER
  │  Framework overhead + middleware: 10–30ms
  │  Auth/session checks, rate limiting, request parsing
  │  Profiler target — check for new middleware added in last 2 weeks
  ▼
DATABASE (or ORM layer)
  │  Connection acquisition: 0ms (pool hit) to 2000ms+ (pool exhausted, queued)
  │  Query execution: varies
  │  ORM serialisation overhead
  ▼
EXTERNAL CALLS (S3, email, third-party APIs, caches)
  │  Any synchronous call on the hot path
  │  Even a 50ms P50 external call can be 2000ms P99 if it has a slow tail
  ▼
RESPONSE SERIALISATION + TRANSFER
  │  JSON serialisation: 5–50ms depending on payload size
  └─ If reports payloads have grown with 30% more data, serialisation cost grows too
```

**How to measure each stage without APM:** If you have an APM tool (Datadog, New Relic, Sentry Performance), you already have span-level breakdown — pull the P99 waterfall for a slow trace. Without APM:

```bash
# nginx/ALB: split out upstream_wait vs upstream_response
# In nginx log format, add: $upstream_connect_time $upstream_header_time $upstream_response_time
# Connection time = connect_time; queue wait = response_time - header_time

# Measure connection pool saturation (PostgreSQL example):
SELECT count(*), state, wait_event_type, wait_event
FROM pg_stat_activity
GROUP BY state, wait_event_type, wait_event
ORDER BY count DESC;

# If you see many rows in state='active' with wait_event='Lock' or wait_event_type='Lock',
# lock contention is the culprit.
# If you see many in state='idle in transaction', you have connection leaks.
```

**Narrow into the database only after confirming:** upstream wait time (at the reverse proxy) is elevated for slow requests. If `upstream_connect_time` is near zero but `upstream_response_time` is high, the bottleneck is inside the application or database, not the pool. If `upstream_connect_time` itself is high, you've hit worker saturation before the app even starts.

---

### 3. Stack Confirmation

**Assumed Python/Django (or Django REST Framework) stack based on the endpoint naming conventions (`/api/reports/{id}`, `/api/exports`) and common patterns for this class of API. CONFIRM stack before selecting a profiler.**

| Stack | Profiler |
|---|---|
| **Python (Django/FastAPI/Flask)** | `py-spy top --pid <pid>` (sampling, zero-instrumentation) or `py-spy record -o profile.svg --pid <pid>` for flamegraph |
| Node.js | `clinic doctor -- node server.js` |
| .NET | `dotnet-trace collect --process-id <pid> --profile cpu-sampling` |
| JVM (Spring, etc.) | `async-profiler -d 30 -f flamegraph.html <pid>` |
| Go | Built-in `pprof` endpoint: `import _ "net/http/pprof"` then `go tool pprof http://localhost:6060/debug/pprof/profile` |

For Python specifically: `py-spy top --pid <pid>` will show which functions are consuming CPU in real time. Run it against a worker during a load spike. If the top entries are database-related (e.g. `execute`, `fetchall`, `_execute_query`), DB is confirmed as the hot path.

---

### 4. Two-Endpoint Analysis

These two endpoints have fundamentally different bottleneck profiles and must be investigated separately.

#### `GET /api/reports/{id}` — Read, synchronous

**Characteristics:** Synchronous, returns immediately, P99 is directly user-visible.

**Likely bottleneck candidates (ordered by prior probability):**

1. **DB connection pool exhaustion** — at 30% more traffic, if pool is fixed-size, the fraction of requests that queue for a connection lands entirely in P99. Check `CONN_MAX_AGE` in Django settings and the pool size. If Django's connection-per-thread model is in use (no pooling), each gunicorn worker holds one connection; at max workers the pool is full.

2. **N+1 query regression** — a recently added `related_name` field, serialiser change, or ORM relation without `select_related`/`prefetch_related` turns one query into N+1. P50 looks fine because small reports hit cache; large reports or cache misses expose N queries. Check: `django-debug-toolbar` query count on slow requests, or enable `LOGGING` for `django.db.backends` and count queries per request.

3. **Cache invalidation / eviction** — if report results are cached and the 30% traffic increase pushed the cache hit rate down (more unique report IDs in flight), the cold-path is now hit more often. A cache miss on a slow query at P99 is invisible at P50. Check cache hit rate metric directly.

4. **Report payload growth** — if reports now contain more data (more rows, more relations) due to accumulated data over 2 weeks, serialisation time and DB scan time both grow. This would show as a gradual drift rather than a step-change.

**Immediate diagnostic:**
```sql
-- PostgreSQL: find the slow query
SELECT query, calls, mean_exec_time, max_exec_time, stddev_exec_time,
       total_exec_time / calls AS avg_total
FROM pg_stat_statements
WHERE query ILIKE '%report%'
ORDER BY max_exec_time DESC
LIMIT 10;
```

#### `POST /api/exports` — Write, likely async

**Characteristics:** Enqueues a job (or triggers a background task). The HTTP response time may be fast (200ms to acknowledge) but the actual export work runs async. However, P99 being 2 seconds here suggests the POST itself is blocking — either synchronous processing, or waiting for worker acknowledgment / task ID.

**Likely bottleneck candidates:**

1. **Job queue depth / worker backlog** — at 30% more exports, if workers are at capacity, new jobs queue. If the POST waits for the job to be accepted by a worker (rather than just enqueued), queue depth directly adds to P99. Check Celery/RQ/SQS queue depth metrics. A queue depth that was near zero two weeks ago and is now 50–200 items is the smoking gun.

2. **DB row-level lock contention** — exports often write an "export record" and may SELECT FOR UPDATE on related records to prevent duplicates. At higher concurrency, lock wait time spikes. This appears only in P99 because most requests get the lock immediately, but under load, the occasional collision cascades.

3. **Blocking on a shared resource during export initiation** — if the POST synchronously calls S3, triggers a file creation, or acquires a semaphore, any slowness in that resource shows directly in the response time.

4. **Background worker starvation causing queue-full backpressure** — if the queue is bounded and workers can't drain it fast enough, the POST itself may block waiting for a slot.

**Immediate diagnostic for exports:**
```bash
# Celery queue depth (if using Redis broker):
redis-cli LLEN celery

# If using RQ:
rq info --url redis://localhost:6379

# Check worker concurrency vs arrival rate:
# If exports are arriving at 10/s and workers process at 7/s, queue grows indefinitely
```

**Key difference:** For reports, the fix is query/cache-level. For exports, the fix is likely worker concurrency or queue configuration — but confirm before scaling workers, because adding workers increases DB connection pressure.

---

### 5. Deploy Bisection Strategy

With multiple deploys per day over two weeks, you may have 50–200 commits. Don't bisect commits blindly — bisect days first using APM data, then bisect commits within the day.

**Step 1: Pull the commit log**
```bash
git log --since="2 weeks ago" --pretty=format:"%h %ai %s" > /tmp/deploy-log.txt
# Also capture deploy timestamps if separate from commits:
# Heroku: heroku releases --num 100
# AWS CodeDeploy / ECS: check deployment history in console
```

**Step 2: Identify the P99 inflection point from APM**

In your APM tool (Datadog, New Relic, Grafana), pull the P99 for `GET /api/reports/{id}` as a time series over 14 days. Find the first timestamp where P99 crossed 500ms (or whichever threshold marks the inflection). You are looking for a step-change (a deploy) not a gradual drift (data growth or traffic growth).

- **Step-change** at a specific deploy timestamp → a code change is the cause. Bisect to that deploy.
- **Gradual drift** tracking traffic growth → likely a capacity/resource ceiling (pool exhaustion). Still check deploys but also look at resource utilisation trends.
- **Step-change that's also the day traffic grew** → you may have a configuration change that moved the saturation knee (e.g., pool size reduced, cache TTL shortened, new index dropped).

**Step 3: Bisect within the day**
```bash
# Filter commits to the suspect day (e.g., 2026-05-20):
git log --after="2026-05-19T23:59:59" --before="2026-05-21T00:00:00" \
  --pretty=format:"%h %ai %s"

# For each deploy in that day, compare the P99 window before and after the deploy.
# Match deploy timestamps from your CI/CD system to the commit hashes.
```

**Step 4: Inspect the suspect commit range**
```bash
# diff the likely culprit files:
git diff <hash-before> <hash-after> -- '**/models.py' '**/serializers.py' \
  '**/views.py' '**/settings*.py' '**/migrations/'

# Pay attention to:
# - New migrations (added/removed indexes, schema changes)
# - serializer field additions (new related fields = potential N+1)
# - settings changes (CONN_MAX_AGE, CACHES, database pool config)
# - New middleware or decorator added to the slow endpoints
# - Changes to Celery/worker concurrency config
```

---

### 6. One-Change-at-a-Time Discipline

**Every fix must be followed by a re-measurement step before the next change is applied.**

Rationale: with multiple hypotheses in play (connection pool, N+1, cache, locks), applying two fixes simultaneously makes it impossible to attribute the improvement — or to detect when a "fix" made things worse. At tail latencies, interactions between changes are common and non-obvious.

**Protocol:**

```
1. Document the current P99 baseline (10-minute sample at fixed RPS)
2. Apply exactly ONE change
3. Deploy to a load-test environment (or canary if no staging)
4. Warm-up: 60 seconds at target RPS (to fill connection pools, warm caches)
5. Sample: 10 minutes at the SAME fixed RPS used for baseline
6. Collect: P50, P95, P99, error rate, throughput
7. Compare: use the same tool/query as the baseline measurement
8. Statistical gate: ≥30 complete request samples in the P99 bucket preferred
   (at 100 req/s over 10min = 60,000 requests; the top 1% = 600 samples — sufficient)
9. Decision: improvement confirmed → commit the change, proceed to next hypothesis
            no improvement → revert, move to next hypothesis
            regression → revert immediately, investigate interaction
```

Do not rely on production P99 as your signal unless you have a canary deployment with isolated metrics. Production signals are noisy and confounded by concurrent traffic changes.

---

### 7. Decision Checkpoint Before Infrastructure Scaling

---

**STOP. Read before adding nodes, increasing DB instance size, or expanding the connection pool.**

Scaling will mask the underlying bottleneck. It will also add cost. If the root cause is a missing index, N+1 query, or connection leak, scaling the database instance buys you weeks at 3–5× the cost before P99 degrades again — and the next threshold crossing happens at higher traffic, higher urgency, and more load on an already-stressed system.

**Proceed with scaling only when:**
- [ ] Root cause is confirmed (not just hypothesised) via before/after measurement
- [ ] The root cause is a genuine capacity limit (e.g., CPU-bound query that has been optimised as far as possible, or legitimate traffic exceeding single-node write capacity)
- [ ] Application-layer fixes have been exhausted or ruled out
- [ ] Cost impact is accepted: rough estimates for common scaling moves:

| Scaling action | Typical cost increase | Masks what |
|---|---|---|
| Add 2 more app servers | ~$200–400/month | Worker exhaustion, connection pressure |
| Upgrade DB instance (e.g., db.t3.medium → db.t3.large) | ~$150–300/month | Memory pressure, buffer cache misses |
| Increase connection pool size | $0 (config) | Connection queuing — but check max_connections on DB first |
| Add read replica | ~$200–400/month | Read-heavy query load |

**Increasing the connection pool without increasing `max_connections` on the database will cause "FATAL: sorry, too many clients" errors — a hard regression, not an improvement.**

---

### 8. Findings Table

| Component | Impact | Hypothesis | Evidence to Collect | Recommended Fix | Re-measure Plan |
|---|---|---|---|---|---|
| **DB connection pool** | HIGH | 30% traffic increase pushed pool utilisation past saturation; requests queue for a connection | Check `pg_stat_activity` for `idle in transaction` or `active` count vs configured pool size; check `upstream_connect_time` spike in LB logs | Increase `CONN_MAX_AGE` (Django) or switch to PgBouncer transaction-mode pooling; tune pool min/max to match worker count | Baseline P99 → adjust pool → 60s warm-up → 10min at fixed RPS → compare P99 |
| **N+1 query (reports endpoint)** | HIGH | Recent serialiser or model change introduced unguarded `related_name` access | Enable `django.db.backends` logging, count queries per request for a report fetch; compare count between fast and slow requests | Add `select_related()` / `prefetch_related()` on the offending ORM call | Query count per request drops to expected; P99 follows |
| **Missing or dropped index** | HIGH | A migration in the past 2 weeks dropped an index or added a column that changed the query plan | `EXPLAIN ANALYZE` on the slow query; check `pg_stat_statements` for `max_exec_time` jump; review migration files in the suspect commit range | Re-add index on the filtered/joined column | `EXPLAIN ANALYZE` shows index scan not seq scan; P99 drops |
| **Job queue depth / worker backlog (exports)** | HIGH | Workers can't drain the export queue at 30% higher throughput; POST blocks on queue acceptance | Check queue depth metric (Celery inspect, RQ info, SQS ApproximateNumberOfMessages); plot queue depth vs time against P99 time series | Increase worker concurrency or add workers (after confirming DB connection headroom); alternatively make POST non-blocking (fire-and-forget enqueue) | Queue depth returns to near-zero; P99 for POST /api/exports drops |
| **Row-level lock contention (exports)** | MEDIUM | Concurrent export creation `SELECT FOR UPDATE` on shared record; high concurrency → lock queue | `pg_stat_activity` with `wait_event = 'Lock'` during load; `pg_locks` joined to `pg_stat_activity` | Add `NOWAIT` or `SKIP LOCKED`; redesign to avoid shared-row updates at insert time | Lock wait count drops to near-zero; P99 improves under concurrent load |
| **Cache miss rate increase** | MEDIUM | 30% more unique report IDs in flight; cache eviction or TTL expiry causing more cold-path DB hits | Cache hit rate metric (Redis `INFO stats` → `keyspace_hits / (keyspace_hits + keyspace_misses)`); compare to 2-week-ago baseline | Increase cache size; tune TTL for report results; pre-warm cache for hot reports | Cache hit rate returns to baseline percentage; DB query rate drops proportionally |
| **Synchronous external call on reports hot path** | MEDIUM | A new integration (logging, audit trail, analytics event) was added to the reports view and calls an external service synchronously | Trace the view code for any HTTP calls, SDK calls, or `requests.get()`; check if new middleware was added to the endpoint | Move to async (background task) or add circuit breaker + timeout | External call no longer on critical path; P99 no longer correlated with external service latency |
| **Response payload size growth** | LOW | 30% more data in DB means reports return larger payloads; serialisation time grows | Compare average response Content-Length now vs 2 weeks ago; profile serialiser with `cProfile` or `py-spy` | Pagination, field filtering (`?fields=`), or lazy-loading expensive nested relations | Mean payload size drops; P99 improves proportional to serialisation savings |

---

### 9. Before/After Measurement Requirement

**No fix is "done" without before/after evidence collected under identical conditions.**

For every fix in the findings table above, the following is required before marking it resolved:

```
BEFORE measurement:
  - Load: fixed RPS matching current production peak (e.g., 500 req/s)
  - Warm-up: 60 seconds (connection pools, caches at steady state)
  - Sample window: 10 minutes
  - Record: P50, P95, P99, error rate, throughput
  - Tool: same tool used for baseline (wrk, k6, Locust, or APM percentiles)

APPLY the fix.

AFTER measurement (same environment, same load, same tool, same window):
  - Load: same fixed RPS
  - Warm-up: 60 seconds
  - Sample window: 10 minutes
  - Record: same metrics

COMPARE:
  - P99 improvement ≥ 20% from before → fix is confirmed effective
  - P99 unchanged → fix did not address this bottleneck; revert and move on
  - P99 regression → revert immediately; fix introduced a new problem

DOCUMENT the result (a table row: Fix | P99 Before | P99 After | Delta | Conclusion).
```

The goal is a chain of evidence, not a bag of changes. When the incident is closed, you should be able to point to a single commit (or at most two) and show the P99 drop in the data.

---

**Recommended starting point:** Pull `pg_stat_activity` and `pg_stat_statements` right now under live load, before any changes. If you see connection queuing or a single query dominating `max_exec_time`, that's your root cause and the rest of the investigation is confirmation. If both look clean, move to the LB upstream wait time — the bottleneck is above the database.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 18.5/18.5 (100%) |
| Evaluated | 2026-05-27 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 209383 ms |
| Target cost | $0.2745 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent establishes a baseline measurement before recommending any fixes — records the exact current metrics (P50, P95, P99, throughput, error rate) | PASS | Section 1 'Baseline' is the first section, with an explicit table recording P50, P95, P99, throughput (+30%), and error rate ('unknown — measure now') before any fixes. |
| c2 | Agent follows the outside-in bottleneck identification: end-to-end timing breakdown before diving into database or code | PASS | Section 2 traces CLIENT→LB→INGRESS→APPLICATION→DATABASE→EXTERNAL CALLS→RESPONSE with estimates, and ends: 'Narrow into the database only after confirming upstream wait time is elevated.' |
| c3 | Agent checks for database-level issues: N+1 queries, missing indexes, full table scans, and lock contention | PASS | Findings table rows: N+1 query (HIGH), Missing/dropped index (HIGH), Row-level lock contention (MEDIUM); tools pg_stat_statements, EXPLAIN ANALYZE, pg_locks, pg_stat_activity all named. |
| c4 | Agent applies the one-change-at-a-time rule — does not recommend changing multiple things simultaneously | PASS | Section 6 protocol step 2: 'Apply exactly ONE change'; findings table has separate re-measure plan per row; rationale given: 'applying two fixes simultaneously makes it impossible to attribute the improvement.' |
| c5 | Agent recommends profiling tools appropriate to the likely stack before proposing optimisations | PASS | Section 3 table lists py-spy (Python), clinic doctor (Node), dotnet-trace (.NET), async-profiler (JVM), pprof (Go) — appears before code-level recommendations in section order. |
| c6 | Agent raises a decision checkpoint before recommending infrastructure scaling changes (cost and architecture implications) | PASS | Section 7 is a bolded 'STOP' block: 'Scaling will mask the underlying bottleneck' with cost table (add 2 app servers ~$200–400/month, upgrade DB ~$150–300/month, etc.) and conditions checklist. |
| c7 | Agent notes that P50 vs P99 divergence is a tail latency signal — suggests investigating resource contention and connection pool exhaustion under concurrency rather than average-case code paths | PASS | 'A flat P50 with a 10× P99 is the textbook signature of one of: connection pool exhaustion, lock contention, or queue saturation — all three are threshold effects.' |
| c8 | Agent produces a prioritised findings table with impact (HIGH/MEDIUM/LOW), component, and recommended fix | PARTIAL | Section 8 findings table contains all required columns (Component, Impact, Hypothesis, Evidence, Recommended Fix, Re-measure Plan) with HIGH/MEDIUM/LOW impact ratings across 8 rows. |
| c9 | Agent specifies that every optimisation must have a before/after measurement using the same load and same metric | PASS | Section 9: 'No fix is done without before/after evidence collected under identical conditions' with full BEFORE/APPLY/AFTER/COMPARE protocol including warm-up and statistical gate. |
| c10 | Output's baseline section reproduces the exact metrics from the prompt — P50 ~180ms (still healthy), P99 was 200ms two weeks ago, P99 now 2s, 30% traffic growth — and notes the 10x P99 jump is disproportionate to traffic | PASS | Baseline table: P50 ~180ms flat, P99 200ms→2000ms (10×), throughput +30%; followed by '10× P99 jump on 30% traffic growth is non-linear — suggests resource contention crossing a threshold, NOT linear scaling.' |
| c11 | Output explicitly identifies the P50-stable / P99-degraded pattern as a tail-latency / contention signal rather than an across-the-board slowdown, and lists candidate causes (connection pool exhaustion, lock contention, GC pauses, cold cache, queueing under load) | PASS | 'flat P50 with a 10× P99 is the textbook signature of one of: connection pool exhaustion, lock contention, or queue saturation — all three are threshold effects. At low load, every request gets the resource immediately.' |
| c12 | Output's investigation plan addresses the two named endpoints (`GET /api/reports/{id}` and `POST /api/exports`) specifically — looking at their distinct workloads (read vs write, sync vs async) | PASS | Section 4 has two subsections: 'GET /api/reports/{id} — Read, synchronous' (cache/query focus) and 'POST /api/exports — Write, likely async' (queue depth/lock focus), each with separate diagnostic commands. |
| c13 | Output proposes correlating the regression with the deployment history — using deploy timestamps to bisect the change set, since 'we deploy multiple times a day' makes single-commit blame infeasible | PASS | Section 5 four-step bisection: pull commit log with git log --since, identify P99 inflection from APM, filter commits to the suspect day, diff suspect commit range with git diff <hash-before> <hash-after>. |
| c14 | Output's database checks include N+1 detection, missing indexes, full table scans, and lock contention, with named tools or queries (`pg_stat_statements`, `EXPLAIN ANALYZE`, `pg_locks`) where applicable | PASS | pg_stat_statements query in Section 4, pg_stat_activity for lock contention in Sections 2 and 4, pg_locks in findings table, EXPLAIN ANALYZE in findings table; Django query logging for N+1 detection. |
| c15 | Output applies the one-change-at-a-time discipline — any recommended fix is followed by a re-measurement step before the next change, not a batch of optimisations | PASS | Section 6 protocol: 'Decision: improvement confirmed → commit the change, proceed to next hypothesis / no improvement → revert, move to next hypothesis'; each findings table row has its own Re-measure Plan. |
| c16 | Output names a profiling tool appropriate to the inferred stack (e.g. py-spy, async-profiler, dotnet-trace, Node clinic) before proposing code-level changes — and asks for stack confirmation if not stated | PASS | Section 3: 'Assumed Python/Django... CONFIRM stack before selecting a profiler' with table of py-spy, clinic doctor, dotnet-trace, async-profiler, pprof — placed before section 4 code-level recommendations. |
| c17 | Output stops and asks before recommending infrastructure scaling (more nodes, larger pool, bigger DB), framing the cost/architecture implications | PASS | Section 7 bold 'STOP': checklist of conditions before scaling, cost table per action, warning: 'Increasing the connection pool without increasing max_connections...will cause FATAL errors — a hard regression.' |
| c18 | Output's findings table is prioritised by likely impact (HIGH/MEDIUM/LOW) with component and recommended fix per row, not a flat unranked list | PASS | Section 8 findings table orders rows HIGH (DB connection pool, N+1, missing index, job queue) then MEDIUM (lock contention, cache miss rate, external call) then LOW (payload size) — explicitly ranked. |
| c19 | Output requires before/after measurement at the same load and same metric for every change, with the measurement protocol stated (warm-up, sample size, statistical significance) | PASS | Section 9: 'warm-up: 60 seconds', 'sample: 10 minutes at SAME fixed RPS', '≥30 complete request samples in the P99 bucket preferred (at 100 req/s over 10min = 60,000 requests; top 1% = 600 samples — sufficient).' |

### Notes

The output is a comprehensive, well-structured response that addresses every criterion fully. The only ceiling limitation is c8 (PARTIAL), where the findings table is present and complete but the test author capped it at 0.5 by design.
