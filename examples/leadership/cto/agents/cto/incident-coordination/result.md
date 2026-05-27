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

# P0 / SEV-1: Payments Service Down

**Blast radius:** All payment transactions failing → 100% checkout flow blocked, refund/retry obligations accumulating on partial transactions, direct revenue impact at full transaction volume per minute. Customer-facing.

**Timestamp correlation:** Deploy at T-45min, error onset at T-20min — 25-minute lag is consistent with bad code rolling out behind warm caches / in-flight connection pools and poisoning state as they cycled. **Rollback is the right first action** — diagnosis happens in parallel, not before.

---

## Parallel dispatch (NOW, single message)

**`devops-lead` → execute rollback immediately**
- Roll back payments service to the pre-T-45min artefact (platform-appropriate: `kubectl rollout undo deployment/payments` or redeploy previous image tag).
- Time-bound SLAs: rollback executed within **5 min**, error rate trending down within **10 min**, resolution declared only after error rate ≤ baseline for **5 consecutive minutes**.
- Report back: rollback timestamp, current error rate, traffic health on the previous revision.

**`dotnet-developer` (engineer who shipped the order-processing handler) → diagnose in parallel**
- Required evidence to surface:
  - Deployment artefact diff (the handler change + anything else in the bundle).
  - APM error traces with the specific exception + first-occurrence timestamp.
  - Grafana dashboard link, time range **T-50 to now**.
  - Stack trace from the first failing transaction.
- This runs concurrently with the rollback — we do not wait on diagnosis before rolling back.

**`coordinator` → own customer comms and stakeholder broadcast**
- Brief support team within **5 min** (kill speculation — give them the holding line).
- Public status page update within **10 min** of declaration, refreshed every **15 min**.
- Exec notification (CEO/CPO) within **15 min** — revenue-impacting incident threshold tripped.
- I (CTO) am not drafting customer-facing copy. That's coordinator + support.

---

## Communication cadence

| Channel | Audience | Cadence |
|---|---|---|
| `#incident-payments` (Slack) | Internal responders | Every **5 min**, incident commander-driven |
| Status page | Public / customers | Within **10 min**, then every **15 min** |
| Support team brief | CS frontline | Within **5 min** (holding line ready) |
| Exec notification | CEO, CPO | Within **15 min** |

---

## My role (coordinator only)

I am **not** reading the handler code or hypothesising root cause. That's `dotnet-developer`'s job and they have the context. My job is: keep rollback and diagnosis moving in parallel, unblock decisions, own the comms cadence, and escalate if either track slips its time-box.

---

## Post-incident (mandatory, scheduled for after resolution)

1. **Blameless post-mortem** with timestamped timeline from deploy → onset → declaration → rollback → resolution.
2. **Root cause analysis** — what the handler change did, why the 25-min lag, why tests didn't catch it.
3. **ADR / learnings doc** capturing the deployment-process gap: **no canary deploy, no health-check gate, no feature flag** on a payments-path change.
4. **Action item — non-negotiable before the next payments deploy:** add at least one of:
   - Canary rollout (e.g. 5% → 25% → 100% with automated rollback on error budget breach), or
   - Health-check gate that blocks promotion if error rate spikes above baseline, or
   - Feature flag wrapping the handler change so kill-switch ≠ rollback.

Dispatching `devops-lead`, `dotnet-developer`, and `coordinator` now.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/17.0 (100%) |
| Evaluated | 2026-05-27 |
| Target model | claude-opus-4-7 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 23968 ms |
| Target cost | $0.2067 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | CTO follows incident response protocol — detect/assess before root-causing | PASS | Output opens with P0/SEV-1 declaration and blast-radius assessment, then timestamp correlation, before any investigation — assess then act structure maintained throughout. |
| c2 | First action is mitigation (rollback the deployment), not investigation | PASS | Parallel dispatch section leads with 'devops-lead → execute rollback immediately' as the first named action before any diagnosis step. |
| c3 | CTO delegates to devops for the rollback and the relevant developer for diagnosis | PASS | Explicitly dispatches 'devops-lead' for rollback and 'dotnet-developer (engineer who shipped the order-processing handler)' for diagnosis. |
| c4 | CTO escalates to coordinator for customer communication (support team is under CPO) | PASS | 'coordinator → own customer comms and stakeholder broadcast'; 'I (CTO) am not drafting customer-facing copy. That's coordinator + support.' |
| c5 | Delegation includes specific evidence requirements — deployment logs, error traces, Grafana dashboard links | PASS | dotnet-developer section lists: deployment artefact diff, APM error traces + first-occurrence timestamp, Grafana link T-50 to now, stack trace from first failing transaction. |
| c6 | CTO identifies the blast radius (all payment transactions) and estimates customer impact | PARTIAL | 'All payment transactions failing → 100% checkout flow blocked, refund/retry obligations accumulating, direct revenue impact at full transaction volume per minute' — no specific $X/min figure. |
| c7 | Post-incident actions are mentioned — root cause analysis, ADR or post-mortem | PASS | Post-incident section explicitly lists blameless post-mortem, root cause analysis, and 'ADR / learnings doc capturing the deployment-process gap.' |
| c8 | CTO does not attempt to debug the code directly — delegates to the specialist | PASS | 'My role (coordinator only): I am not reading the handler code or hypothesising root cause. That's dotnet-developer's job.' |
| c9 | Output's first action is mitigation — initiating rollback of the deployment from 45 minutes ago — not investigation, not log diving, not asking for more data | PASS | First dispatched action is 'devops-lead → execute rollback immediately' with kubectl command, before any diagnostic steps. |
| c10 | Output correlates the deploy timestamp (45 min ago) with the error onset (20 min ago) explicitly — the 25-minute lag suggests the bad code rolled out and slowly poisoned in-flight requests / cache state, supporting the rollback decision | PASS | 'Deploy at T-45min, error onset at T-20min — 25-minute lag is consistent with bad code rolling out behind warm caches / in-flight connection pools and poisoning state as they cycled.' |
| c11 | Output dispatches DevOps to execute the rollback (specific command or platform action) and the .NET developer who shipped the order-processing handler change to begin diagnosis in parallel — not sequential | PASS | Provides 'kubectl rollout undo deployment/payments'; 'This runs concurrently with the rollback — we do not wait on diagnosis before rolling back.' |
| c12 | Output escalates customer communication to the coordinator (or directly to the support team via CPO) — the CTO does not draft customer comms, but ensures someone is doing it | PASS | coordinator assigned to 'own customer comms and stakeholder broadcast' with specific deliverables; CTO explicitly disavows drafting comms. |
| c13 | Output specifies the evidence required from the diagnosing developer — deployment logs / artefact diff, error traces from APM, Grafana dashboard time-range link spanning before/after deploy, and the specific exception stack — so the post-rollback analysis is concrete | PASS | All four evidence types listed under dotnet-developer: artefact diff, APM error traces, Grafana link T-50 to now, stack trace from first failing transaction. |
| c14 | Output quantifies blast radius — "all payment transactions failing" means revenue impact per minute, customer-side checkout failures, and likely refund / retry obligations — to set incident severity (probably P0/SEV-1) | PASS | 'P0 / SEV-1: All payment transactions failing → 100% checkout flow blocked, refund/retry obligations accumulating, direct revenue impact at full transaction volume per minute.' |
| c15 | Output names the post-incident actions — blameless post-mortem with timeline, root cause analysis, ADR or learnings doc capturing what the deployment process missed (no canary, no health-check gate, no feature flag), and an action item to add the gate | PASS | Post-incident section items 1–4: blameless post-mortem with timestamped timeline, RCA, ADR capturing 'no canary deploy, no health-check gate, no feature flag', action item to add at least one gate. |
| c16 | Output does NOT attempt to read code or hypothesise root cause directly — delegates to the developer who owns the change, while owning the coordination and communication | PASS | 'I am not reading the handler code or hypothesising root cause. That's dotnet-developer's job and they have the context. My job is: keep rollback and diagnosis moving in parallel...' |
| c17 | Output establishes a timeline for the rollback (e.g. "rollback executed within 5 min, errors should clear within 10 min, declare resolution after error rate returns to baseline for 5 min") | PASS | 'rollback executed within 5 min, error rate trending down within 10 min, resolution declared only after error rate ≤ baseline for 5 consecutive minutes.' |
| c18 | Output addresses incident communication cadence — internal Slack channel, status page update for customers, support team brief — with timing per channel | PARTIAL | Table covers #incident-payments every 5 min, status page within 10 min then every 15 min, support team brief within 5 min, exec within 15 min — comprehensive but ceiling is PARTIAL. |

### Notes

The output is a near-perfect match for all 18 criteria, correctly structuring the response around mitigation-first, parallel delegation with named owners, explicit evidence requirements, and full post-incident actions. The only gap is c6's missing dollar-per-minute quantification, but that criterion's ceiling was already capped at PARTIAL.
