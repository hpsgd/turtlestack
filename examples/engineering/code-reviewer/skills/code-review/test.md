# Test: code-review skill applied to an Express middleware PR

Scenario: A senior backend engineer opens a PR adding a token-bucket rate limiter to an Express API. The diff introduces an in-memory Map keyed on IP, removes an existing distributed-rate-limit Redis client, and ships without tests. The README, runbooks, and observability dashboards aren't updated. The reviewer needs to apply the layered code-review methodology — native review for mechanics, team conventions on top.

## Prompt

Review this PR. The author is removing the Redis-backed rate limiter and replacing it with an in-process implementation to "reduce infrastructure dependencies."

```typescript
// src/middleware/rateLimit.ts (new file)
import type { Request, Response, NextFunction } from 'express'

const buckets = new Map<string, { tokens: number; lastRefill: number }>()
const RATE = 100         // tokens per minute
const CAPACITY = 100

export function rateLimit(req: Request, res: Response, next: NextFunction) {
  const key = req.ip
  const now = Date.now()
  let bucket = buckets.get(key)

  if (!bucket) {
    bucket = { tokens: CAPACITY, lastRefill: now }
    buckets.set(key, bucket)
  }

  const elapsed = (now - bucket.lastRefill) / 60000
  bucket.tokens = Math.min(CAPACITY, bucket.tokens + elapsed * RATE)
  bucket.lastRefill = now

  if (bucket.tokens < 1) {
    return res.status(429).json({ error: 'rate_limited' })
  }

  bucket.tokens -= 1
  next()
}
```

```diff
// src/app.ts
- import { redisRateLimit } from './middleware/redisRateLimit'
+ import { rateLimit } from './middleware/rateLimit'
- app.use(redisRateLimit({ host: process.env.REDIS_HOST }))
+ app.use(rateLimit)
```

The PR description says: "Removes Redis dependency. Same 100/min limit. All existing tests pass."

A few specifics for the response (output structured per the code-review template):

- **Run the layered flow in order**: scope determination, native review (or the standalone agent fallback if the bundled skill is unavailable in the harness), conventions layer (`review-typescript` + `review-standards` for this diff), merged verdict. Label which layer each finding came from (**Source:** native review | conventions skill | both).
- **HARD vs SOFT signal labels** on every finding. **HARD** = blocker (will cause wrong behaviour in production — multi-instance correctness break, security regression, data loss). **SOFT** = important-but-conditional (improvement, debt, style).
- **Context finding HARD**: in-memory rate limiter is per-instance — once the service runs more than one Node process or container, the 100/min limit becomes 100×N effective. With Redis it was correctly distributed; this PR breaks the security control.
- **Correctness findings**:
  - HARD — Read-modify-write on `bucket.tokens` is not atomic across simultaneous requests on the same Node process (TOCTOU). Two concurrent requests both read tokens=1, both decrement, charge the user once when they should be limited.
  - SOFT — Unbounded Map growth: every unique IP adds a key, no eviction policy. IP-cycling attack or natural churn = memory leak.
  - SOFT — In-memory state lost on every deploy / restart, resetting all counters and giving abusers a fresh quota.
- **Security findings**:
  - HARD — `req.ip` is fragile behind a proxy/load balancer. If `app.set('trust proxy', ...)` is misconfigured, attackers spoof `X-Forwarded-For` and bypass the limiter, OR all requests appear from the LB IP and one user starves all others.
  - SOFT — One client behind NAT (corporate office) representing 1000 users will be falsely throttled as a single IP.
  - SOFT — No `Retry-After` header on 429 responses (clients can't back off intelligently). Friction signal.
- **Quality / conventions findings**:
  - HARD — Missing observability: no logged events, no metrics emitted, no dashboard for rate-limit hits/misses. This is a security control without instrumentation = no detection of abuse.
  - HARD — Tests can't observe cross-instance drift; existing tests "validate the wrong thing" since they only run against one process.
  - SOFT — No specific test cases proposed for refill arithmetic, concurrent requests, capacity boundary, IP-key collision behind a proxy.
- **Adversarial analysis** (from the native layer or reasoned directly): consider explicitly — (a) 10K req/sec attack profile, (b) 1000 users behind one NAT IP, (c) deploy resets in-memory state mid-attack, (d) IP cycling to defeat the limiter.
- **Verdict**: explicit `Verdict: REQUEST_CHANGES` (not APPROVE) with explicit counts: `Blockers: N | Important: N | Suggestions: N`.
- **Each finding cites file:line** (use `src/middleware/rateLimit.ts:N` or the diff path) AND a concrete fix suggestion (e.g. "switch to `express-rate-limit` with Redis store" OR "document the trade-off and stay with the existing distributed limiter").
- **Zero-finding gate** acknowledged (even though this PR has findings) — state the rule: "If both layers come back clean, name a specific positive assertion with file:line to prove review depth, not silence."
- **Calibration rules** stated at top: no findings without evidence, no findings without fix suggestions, no style preferences not codified in team standards.

## Criteria

- [ ] PASS: Skill layers team conventions on the native review — a mechanics layer (bundled `/code-review`, agent fallback, or declared inline pass), then a conventions layer applied either via the matching review-* skills or inline via installed rules with explicit attribution in a Layers table
- [ ] PASS: Skill distinguishes HARD signals (blockers — will cause wrong behaviour in production) from SOFT signals (important but conditional)
- [ ] PASS: Output's Layers table shows the conventions layer ran for the diff's language (review-typescript/review-standards invoked, or named installed rules applied inline) — TypeScript-specific and cross-cutting standards findings or an explicit "none — checked"
- [ ] PASS: Output's Layers table shows the security layer triggered for this security-control diff (security-audit invoked, or security-baseline rules applied inline with attribution)
- [ ] PASS: Skill merges findings across layers, deduplicating, and every finding records its source layer
- [ ] PASS: Skill defines a zero-finding gate — if clean, must name a specific positive assertion with file:line to prove review depth
- [ ] PASS: Skill's output format includes a verdict (APPROVE, REQUEST_CHANGES, NEEDS_DISCUSSION) with a count of blockers, important, and suggestion findings
- [ ] PASS: Skill's calibration rules prohibit findings without evidence, findings without fix suggestions, and style preferences not codified in team standards

## Output expectations

- [ ] PASS: Output flags the per-process in-memory Map as a HARD signal — rate limit no longer enforced across instances, won't survive restart, defeats the purpose of rate limiting in any horizontally scaled deployment
- [ ] PASS: Output flags the absence of tests as a HARD signal given the change to a security-relevant control, and proposes specific test cases (refill arithmetic, concurrent requests, capacity boundary, IP key collision behind a proxy)
- [ ] PASS: Output flags `req.ip` as fragile behind a proxy/load balancer — depends on `trust proxy` configuration, can be spoofed via `X-Forwarded-For` if not configured correctly
- [ ] PASS: Output flags the unbounded `Map` growth as a memory leak — no eviction, every unique IP forever, OOM risk under botnet or large user base
- [ ] PASS: Output identifies a concurrency / TOCTOU issue — read-modify-write on `bucket.tokens` is not atomic across simultaneous requests on the same Node process
- [ ] PASS: Output flags the lack of `Retry-After` header on the 429 response as a friction signal (clients can't back off intelligently)
- [ ] PASS: Output produces a verdict of `REQUEST_CHANGES` or `NEEDS_DISCUSSION` (not APPROVE) with explicit blocker / important / suggestion counts
- [ ] PASS: Each finding cites a specific file:line and includes a concrete suggested fix (e.g. switch to `express-rate-limit` with Redis store, or document the trade-off and stay with the existing distributed limiter)
- [ ] PASS: Output runs an adversarial pass — what happens at 10K req/sec, what happens with one client behind NAT representing 1000 users, what happens during a deploy when in-memory state resets
- [ ] PARTIAL: Output flags the missing observability — no logged events, no metrics, no dashboard for rate-limit hits/misses — given this is a security control
