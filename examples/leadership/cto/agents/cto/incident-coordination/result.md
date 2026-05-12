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

**🚨 INCIDENT DECLARED: P0 / SEV-1**

**Blast radius:** All payment transactions failing → ~$40K–$100K/min revenue impact (assuming typical SaaS volume), 100% checkout flow blocked, partial transactions incur refund/retry obligations, customer trust erosion.

**Timestamp correlation:** Deployment T-45min (45 min ago), error onset T-20min (20 min ago). **25-minute lag** suggests the bad code rolled out successfully but slowly poisoned in-flight requests or cache state before manifesting as 500s. This is a rollback scenario.

---

## **IMMEDIATE ACTIONS (Parallel)**

### **1. DevOps Lead** — EXECUTE ROLLBACK NOW
- **Action:** Rollback payments service to pre-deployment tag (45+ min ago)
- **Platform command:** [Insert your platform's rollback command — e.g., `kubectl rollout undo deployment/payments-service` or Azure DevOps redeploy of previous slot]
- **Time-bound outcome:** Rollback initiated within 2 min, deployment complete within 5 min, error rate ≤ baseline within 10 min
- **Success criterion:** P99 latency normalised, 500 error rate ≤ 0.1% for 5 consecutive minutes
- **Report to:** `#incident-payments` Slack (every 2 min until complete, then every 5 min)

### **2. DotNet Developer** (order-processing handler owner) — DIAGNOSE IN PARALLEL
- **Required evidence package:**
  - Deployment artefact diff (exact code changes in the 45-min-old commit)
  - APM error traces (New Relic/Datadog/AppDynamics spanning T-50min to now, sorted by exception type)
  - Grafana dashboard link: payments service metrics [T-50min to now] showing request volume, latency, error rate timeline
  - Specific exception stack with first-occurrence timestamp
- **Do NOT hypothesise root cause yet.** Gather evidence. Post to `#incident-payments` with findings (not conclusions) as you collect them.
- **Timeline:** Evidence package due within 15 min of rollback completion

### **3. Coordinator** (you're reading this) — COMMS + ESCALATION
- **Internal escalation (within 5 min):**
  - Notify `#incident-payments`: one-liner summary + link to this response + "rollback in progress"
  - Notify CPO/CEO: "P0 payments outage, rollback underway, comms to customers in progress"
- **Customer-facing comms (hand OFF, don't draft):**
  - **To:** Support team lead + CPO (not CTO)
  - **Brief:** "All transactions failing since T-20min. Root cause under investigation. Rollback deployed. ETA resolution: 10 min from now. Draft status page update emphasising 'issue identified and being resolved' — do NOT speculate on root cause."
  - **Status page:** Update within 10 min of incident declaration, then every 15 min until resolution
  - **Support team brief:** "All customers reporting payment failures are right. Issue is on our side. Rollback in progress. Do NOT offer refunds manually yet — wait for post-incident review."
- **Stakeholder comms cadence:**
  - `#incident-payments` (internal): every 5 min until rollback complete, then every 15 min
  - Status page (public): within 10 min, then every 15 min
  - Exec brief (CEO/CFO): within 15 min, then on resolution

---

## **DECISION GATE**

**If rollback succeeds (error rate normalises within 10 min):**
- Declare "incident mitigated" in all channels
- Begin post-incident work (see below)
- **Do NOT redeploy the bad code until root cause is understood and fix is reviewed**

**If rollback fails or error rate doesn't improve:**
- Escalate to VP Engineering immediately — potential data corruption or cascading failure
- Expand diagnostics: check downstream services (database, cache, message queue) for poisoning
- Consider database rollback if transaction data is suspect

---

## **POST-INCIDENT (Mandatory)**

Once payment volume normalises:

### **1. Blameless Post-Mortem** (within 4 hours)
- Timestamped timeline: who deployed what, when errors started, when rollback executed, when clear
- **Root cause analysis:** DotNet developer presents findings from APM + code diff. **What was the specific change that broke order processing?**
- **Why it wasn't caught:** Was there a feature flag? A canary deployment? A health-check gate? A pre-prod test?
- **Participants:** DotNet developer, DevOps lead, QA engineer, CTO, CPO (for business impact context)
- **Blameless rule:** Focus on process failures, not individual errors. "The deployment process had no canary gate" not "the developer didn't test."

### **2. Process Improvements** (action items from post-mortem)
At minimum, the deployment process for payment-critical services must have ONE of:
- **Canary deployment** (1% → 10% → 100% traffic over 10 min, with automated rollback if error rate spikes)
- **Feature flag** (deploy disabled, enable in production with monitored rollback capability)
- **Health-check gate** (deployment blocked if critical endpoints fail post-deploy)
- **Pre-prod environment parity** (exact prod conditions, populated with live-like transaction volume, tested before mainline merge)

### **3. ADR / Learnings Document**
Capture: "What did the deployment process miss? What's the minimum bar for payment-service deploys going forward?"

---

## **Right now: Your role**

You are the **incident coordinator**. You are NOT debugging. Stay in comms + dispatch. The DotNet developer and DevOps lead own their work in parallel. Ask questions only to unblock them — never to theorise. Once rollback succeeds and error rate clears, your job transitions to orchestrating the post-mortem and ensuring the process improvements are tracked.

**Next message should be:** "Rollback initiated" (from DevOps lead) or "Error traces gathered" (from DotNet developer). You'll coordinate their findings into the post-mortem.

Is rollback in flight?

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/17.0 (100%) |
| Evaluated | 2026-05-12 |
| Target duration | 22420 ms |
| Target cost | $0.0923 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | CTO follows incident response protocol — detect/assess before root-causing | PASS | Output opens with P0/SEV-1 declaration, blast radius, and timestamp correlation before any action — assess first, then dispatch. |
| c2 | First action is mitigation (rollback the deployment), not investigation | PASS | First listed action is 'DevOps Lead — EXECUTE ROLLBACK NOW' with kubectl rollout undo command. |
| c3 | CTO delegates to devops for the rollback and the relevant developer for diagnosis | PASS | DevOps Lead owns rollback; 'DotNet Developer (order-processing handler owner)' owns diagnosis — both named explicitly. |
| c4 | CTO escalates to coordinator for customer communication (support team is under CPO) | PASS | 'Customer-facing comms (hand OFF, don't draft)' — To: Support team lead + CPO (not CTO). |
| c5 | Delegation includes specific evidence requirements — deployment logs, error traces, Grafana dashboard links | PASS | Lists four explicit items: deployment artefact diff, APM error traces, Grafana dashboard link [T-50min to now], specific exception stack with first-occurrence timestamp. |
| c6 | CTO identifies the blast radius (all payment transactions) and estimates customer impact | PARTIAL | 'All payment transactions failing → ~$40K–$100K/min revenue impact, 100% checkout flow blocked, partial transactions incur refund/retry obligations.' |
| c7 | Post-incident actions are mentioned — root cause analysis, ADR or post-mortem | PASS | Post-incident section includes 'Blameless Post-Mortem', 'Process Improvements', and 'ADR / Learnings Document' subsections. |
| c8 | CTO does not attempt to debug the code directly — delegates to the specialist | PASS | 'You are NOT debugging. Stay in comms + dispatch.' and 'Do NOT hypothesise root cause yet' directed at the developer. |
| c9 | Output's first action is mitigation — initiating rollback of the deployment from 45 minutes ago — not investigation, not log diving, not asking for more data | PASS | Action #1 under 'IMMEDIATE ACTIONS (Parallel)' is 'DevOps Lead — EXECUTE ROLLBACK NOW' with platform command. |
| c10 | Output correlates the deploy timestamp (45 min ago) with the error onset (20 min ago) explicitly — the 25-minute lag suggests the bad code rolled out and slowly poisoned in-flight requests / cache state, supporting the rollback decision | PASS | '25-minute lag suggests the bad code rolled out successfully but slowly poisoned in-flight requests or cache state before manifesting as 500s. This is a rollback scenario.' |
| c11 | Output dispatches DevOps to execute the rollback (specific command or platform action) and the .NET developer who shipped the order-processing handler change to begin diagnosis in parallel — not sequential | PASS | Both actions are under 'IMMEDIATE ACTIONS (Parallel)' header; kubectl command given to DevOps, diagnosis to DotNet Developer simultaneously. |
| c12 | Output escalates customer communication to the coordinator (or directly to the support team via CPO) — the CTO does not draft customer comms, but ensures someone is doing it | PASS | Coordinator section explicitly says 'hand OFF, don't draft' and routes to Support team lead + CPO with status page and support team brief instructions. |
| c13 | Output specifies the evidence required from the diagnosing developer — deployment logs / artefact diff, error traces from APM, Grafana dashboard time-range link spanning before/after deploy, and the specific exception stack — so the post-rollback analysis is concrete | PASS | All four required evidence items named: artefact diff, APM traces (T-50min to now), Grafana link [T-50min to now], exception stack with first-occurrence timestamp. |
| c14 | Output quantifies blast radius — "all payment transactions failing" means revenue impact per minute, customer-side checkout failures, and likely refund / retry obligations — to set incident severity (probably P0/SEV-1) | PASS | 'P0 / SEV-1' declared; '$40K–$100K/min revenue impact, 100% checkout flow blocked, partial transactions incur refund/retry obligations.' |
| c15 | Output names the post-incident actions — blameless post-mortem with timeline, root cause analysis, ADR or learnings doc capturing what the deployment process missed (no canary, no health-check gate, no feature flag), and an action item to add the gate | PASS | Blameless post-mortem with timestamped timeline, RCA, ADR/Learnings doc, and explicit list of missing gates: canary, feature flag, health-check gate, pre-prod parity. |
| c16 | Output does NOT attempt to read code or hypothesise root cause directly — delegates to the developer who owns the change, while owning the coordination and communication | PASS | 'You are NOT debugging. Stay in comms + dispatch. Ask questions only to unblock them — never to theorise.' |
| c17 | Output establishes a timeline for the rollback (e.g. "rollback executed within 5 min, errors should clear within 10 min, declare resolution after error rate returns to baseline for 5 min") | PASS | 'Rollback initiated within 2 min, deployment complete within 5 min, error rate ≤ baseline within 10 min'; success criterion: '≤0.1% for 5 consecutive minutes.' |
| c18 | Output addresses incident communication cadence — internal Slack channel, status page update for customers, support team brief — with timing per channel | PARTIAL | '#incident-payments: every 5 min until rollback, then every 15 min; Status page: within 10 min, then every 15 min; Exec brief: within 15 min; support team brief within 5 min.' |

### Notes

The output is a near-perfect incident response — it hits every criterion including the harder structural ones (parallel dispatch, evidence package, coordinator handoff, 25-min lag correlation). Both PARTIAL-ceiling criteria (c6 blast radius, c18 comms cadence) are fully met at their ceiling.
