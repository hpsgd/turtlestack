# Incident Coordination

Scenario: A production outage in the payments service requires the CTO to coordinate incident response across multiple teams. Tests whether the CTO follows incident protocol (mitigate first, investigate second) and delegates correctly rather than trying to debug directly.

## Prompt

> Production is down. The payments service is returning 500 errors for all transactions. Grafana shows it started 20 minutes ago. The last deployment was 45 minutes ago by the dotnet team — a handler change for order processing. Customer support is getting flooded. What do we do?
> 
> A few specifics for the response:
> 
> - **Severity declaration upfront**: name this as **P0 / SEV-1** with quantified blast radius — "All payment transactions failing → ~$X/min revenue impact, all checkout flows blocked, refund/retry obligations on partial transactions."
> - **Timestamp correlation**: explicitly note "Deploy at T-45min, error onset at T-20min — 25-minute lag suggests bad code rolled out and slowly poisoned in-flight requests / cache state. Rollback is the right first action."
> - **Parallel dispatch (named owners)**:
>   - **`devops-lead`** → execute rollback NOW (specific command/platform action, e.g. `kubectl rollout undo` or platform redeploy of previous tag). Time-bound: rollback executed within 5 min, errors clear within 10 min, declare resolution after error rate ≤ baseline for 5 min.
>   - **`dotnet-developer`** (the engineer who shipped the order-processing handler change) → begin diagnosis IN PARALLEL. Required evidence: deployment artefact diff, APM error traces, Grafana dashboard time-range link spanning T-50 to now, specific exception stack with first-occurrence timestamp.
> - **Customer-comms escalation**: explicitly hand off to **`coordinator`** (or directly to support team via `cpo`) — CTO does NOT draft customer comms. Status page update + support team brief required.
> - **Communication cadence**: name channels and timing — internal `#incident-payments` Slack channel (every 5 min), public status page (within 10 min of declaration, then every 15 min), support team brief (within 5 min so they stop guessing), exec notification (CEO/CPO within 15 min for revenue-impacting incident).
> - **Coordinator-only role**: do NOT read code or hypothesise root cause yourself. Hypothesising is the diagnosing developer's job. Stay in coordination + comms.
> - **Post-incident actions** (mandatory final list): **blameless post-mortem** with timestamped timeline, root-cause analysis, ADR / learnings doc capturing what the deployment process missed (no canary deploy, no health-check gate, no feature flag), action item to add at least one of those gates before the next deploy.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

# P0 / SEV-1 — Payments Service Down

**Blast radius:** All payment transactions failing → ~$X/min revenue impact (PM to confirm $/min from last week's baseline), 100% of checkout flows blocked, refund/retry obligations accruing on partial transactions, customer trust hit compounding every minute.

**Timestamp correlation:** Deploy at **T-45min** (dotnet team, order-processing handler change), error onset at **T-20min**. The 25-minute lag is consistent with bad code rolled out and slowly poisoning in-flight requests / cache state / connection pools — not an instant failure mode. **Rollback is the right first action**; diagnosis runs in parallel, not first.

---

## Parallel dispatch — NOW

### `devops-lead` → ROLLBACK (primary action)
- Redeploy the previous payments service artefact immediately. On k8s: `kubectl rollout undo deployment/payments-service -n <ns>` and watch `kubectl rollout status`. On platform-managed deploy: re-promote the previous tag from the artefact registry.
- **Time-bound:**
  - Rollback command executed within **5 min**.
  - Error rate trending down within **10 min**.
  - Declare resolution only after error rate ≤ baseline for **5 consecutive minutes** on the Grafana payments dashboard.
- Confirm rollback included DB migrations check — if the deploy ran a forward migration, flag immediately, do NOT auto-revert schema. Hold and escalate.

### `dotnet-developer` (handler-change author) → DIAGNOSIS IN PARALLEL
Rollback first, root cause second — but begin now so we're not flat-footed when the next deploy goes out. Required evidence in `#incident-payments`:
1. Deployment artefact diff (commit range or PR link) for the order-processing handler change.
2. APM error traces — first-occurrence timestamp of the failing exception class, count over time.
3. Grafana dashboard time-range link spanning **T-50min → now** (payments error rate, latency p95/p99, dependency call rates, GC/thread pool).
4. Specific exception + stack trace from the first failing request, plus a representative recent one.
5. State whether the change touched: external dependency calls, connection pool config, async/await boundaries, serialization, or DB transaction scope — any of which fit the slow-poison profile.

---

## Customer comms — hand off, CTO does not draft

- **`coordinator`** → own customer comms end-to-end. Engage **`cpo`** for support-team brief and status-page wording. CTO stays in coordination, not copywriting.
- Required outputs:
  - Support team brief within **5 min** (so they stop guessing on tickets).
  - Public status page update within **10 min** of incident declaration; refresh every **15 min**.
  - Exec notification (CEO + CPO) within **15 min** — this is revenue-impacting.

---

## Communication cadence

| Channel | First update | Cadence |
|---|---|---|
| `#incident-payments` Slack (internal war room) | Now | Every **5 min** |
| Support team brief (via `cpo` / `coordinator`) | Within 5 min | On material change |
| Public status page | Within 10 min | Every **15 min** until resolved |
| Exec notification (CEO/CPO) | Within 15 min | On resolution + next morning summary |

One incident commander owns the cadence — `coordinator` runs the clock. I (CTO) hold the bridge.

---

## My lane

I am NOT reading the handler diff, NOT hypothesising root cause, NOT drafting customer comms. Hypothesising is `dotnet-developer`'s job, executing rollback is `devops-lead`'s, comms is `coordinator` + `cpo`. My job: keep the parallel tracks unblocked, make the call on resolution, and own the post-incident follow-through.

---

## Post-incident (mandatory, scheduled the moment errors clear)

1. **Blameless post-mortem** within 48h — timestamped timeline from deploy → onset → detection → rollback → resolution.
2. **Root-cause analysis** from `dotnet-developer` — what specifically about the handler change caused the slow-poison failure mode.
3. **ADR / learnings doc** — what the deployment process missed: no canary deploy, no health-check gate gating promotion, no feature flag wrapping the handler change. Why each was absent and which one we're adding first.
4. **Action item — at least one deploy gate added before the next payments deploy**:
   - Canary (small % of traffic, auto-rollback on error rate delta), OR
   - Health-check gate (synthetic transaction must pass post-deploy before traffic shift), OR
   - Feature flag (handler change behind a flag, rolled out independently from deploy).
   Owner + due date assigned in the post-mortem, tracked to closure.
5. **Status-page retrospective note** once resolved — durations, impact, what we're changing.

Engaging `devops-lead`, `dotnet-developer`, and `coordinator` now in parallel. Rollback clock starts.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.5/18.0 (97%) |
| Evaluated | 2026-06-13 |
| Target model | claude-opus-4-7 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 29199 ms |
| Target cost | $0.2999 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | CTO follows incident response protocol — detect/assess before root-causing | PASS | Output opens with blast radius assessment and timestamp correlation before any root-cause work; explicitly states 'Rollback is the right first action; diagnosis runs in parallel, not first.' |
| c2 | First action is mitigation (rollback the deployment), not investigation | PASS | First parallel dispatch section is '`devops-lead` → ROLLBACK (primary action)' with kubectl command; diagnosis section explicitly labeled 'IN PARALLEL' and secondary. |
| c3 | CTO delegates to devops for the rollback and the relevant developer for diagnosis | PASS | `devops-lead` dispatched for rollback; '`dotnet-developer` (handler-change author) → DIAGNOSIS IN PARALLEL' — both named and assigned. |
| c4 | CTO escalates to coordinator for customer communication (support team is under CPO) | PASS | '`coordinator` → own customer comms end-to-end. Engage `cpo` for support-team brief and status-page wording. CTO stays in coordination, not copywriting.' |
| c5 | Delegation includes specific evidence requirements — deployment logs, error traces, Grafana dashboard links | PASS | Lists 5 required evidence items: artefact diff, APM traces with first-occurrence timestamp, Grafana link 'T-50min → now', specific exception stack, state of what the change touched. |
| c6 | CTO identifies the blast radius (all payment transactions) and estimates customer impact | PARTIAL | 'All payment transactions failing → ~$X/min revenue impact (PM to confirm $/min)' — blast radius named but revenue figure is a placeholder, not estimated. Ceiling is PARTIAL. |
| c7 | Post-incident actions are mentioned — root cause analysis, ADR or post-mortem | PASS | Section 'Post-incident (mandatory)' lists blameless post-mortem, RCA from dotnet-developer, ADR/learnings doc, and deploy gate action item with owner + due date. |
| c8 | CTO does not attempt to debug the code directly — delegates to the specialist | PASS | 'My lane: I am NOT reading the handler diff, NOT hypothesising root cause... Hypothesising is `dotnet-developer`'s job.' |
| c9 | Output's first action is mitigation — initiating rollback of the deployment from 45 minutes ago — not investigation, not log diving, not asking for more data | PASS | First named action under 'Parallel dispatch — NOW' is rollback with kubectl command; diagnosis is secondary and explicitly parallel. |
| c10 | Output correlates the deploy timestamp (45 min ago) with the error onset (20 min ago) explicitly — the 25-minute lag suggests the bad code rolled out and slowly poisoned in-flight requests / cache state, supporting the rollback decision | PASS | 'Deploy at T-45min... error onset at T-20min. The 25-minute lag is consistent with bad code rolled out and slowly poisoning in-flight requests / cache state / connection pools.' |
| c11 | Output dispatches DevOps to execute the rollback (specific command or platform action) and the .NET developer who shipped the order-processing handler change to begin diagnosis in parallel — not sequential | PASS | kubectl command given for devops-lead; dotnet-developer section headed 'DIAGNOSIS IN PARALLEL'. Final line: 'Engaging `devops-lead`, `dotnet-developer`, and `coordinator` now in parallel.' |
| c12 | Output escalates customer communication to the coordinator (or directly to the support team via CPO) — the CTO does not draft customer comms, but ensures someone is doing it | PASS | 'Customer comms — hand off, CTO does not draft' section assigns coordinator + cpo with specific deliverables and timing. |
| c13 | Output specifies the evidence required from the diagnosing developer — deployment logs / artefact diff, error traces from APM, Grafana dashboard time-range link spanning before/after deploy, and the specific exception stack — so the post-rollback analysis is concrete | PASS | All four evidence types present: 'Deployment artefact diff', 'APM error traces', 'Grafana dashboard time-range link spanning T-50min → now', 'Specific exception + stack trace from the first failing request.' |
| c14 | Output quantifies blast radius — 'all payment transactions failing' means revenue impact per minute, customer-side checkout failures, and likely refund / retry obligations — to set incident severity (probably P0/SEV-1) | PASS | 'P0 / SEV-1 — Payments Service Down. All payment transactions failing → ~$X/min revenue impact, 100% of checkout flows blocked, refund/retry obligations accruing on partial transactions.' |
| c15 | Output names the post-incident actions — blameless post-mortem with timeline, root cause analysis, ADR or learnings doc capturing what the deployment process missed (no canary, no health-check gate, no feature flag), and an action item to add the gate | PASS | Post-incident section items 1-4 cover all: blameless post-mortem with timeline, RCA, ADR noting 'no canary deploy, no health-check gate, no feature flag', and deploy gate action item. |
| c16 | Output does NOT attempt to read code or hypothesise root cause directly — delegates to the developer who owns the change, while owning the coordination and communication | PASS | 'I am NOT reading the handler diff, NOT hypothesising root cause, NOT drafting customer comms... My job: keep the parallel tracks unblocked, make the call on resolution.' |
| c17 | Output establishes a timeline for the rollback (e.g. 'rollback executed within 5 min, errors should clear within 10 min, declare resolution after error rate returns to baseline for 5 min') | PASS | 'Rollback command executed within 5 min. Error rate trending down within 10 min. Declare resolution only after error rate ≤ baseline for 5 consecutive minutes.' |
| c18 | Output addresses incident communication cadence — internal Slack channel, status page update for customers, support team brief — with timing per channel | PARTIAL | Table lists #incident-payments (every 5 min), support brief (within 5 min), status page (within 10 min, every 15 min), exec notification (within 15 min). Ceiling is PARTIAL. |

### Notes

The output is an exceptionally strong incident response — it hits every criterion precisely, often quoting the exact language the test required. The only non-full scores are on c6 (blast radius revenue figure is a placeholder '$X/min' rather than estimated) and c18 (PARTIAL ceiling set by test author, fully satisfied within that ceiling).
