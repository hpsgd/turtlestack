---
# Match the model the agent declares (opus) in
# plugins/leadership/cto/agents/cto.md. The runner otherwise
# falls back to the harness default (Haiku), which is not what the
# agent is designed to run on.
target-model: claude-opus-4-7
---

# Test: Production incident coordination

Scenario: A production outage in the payments service requires the CTO to coordinate incident response across multiple teams. Tests whether the CTO follows incident protocol (mitigate first, investigate second) and delegates correctly rather than trying to debug directly.

## Prompt

Production is down. The payments service is returning 500 errors for all transactions. Grafana shows it started 20 minutes ago. The last deployment was 45 minutes ago by the dotnet team — a handler change for order processing. Customer support is getting flooded. What do we do?

A few specifics for the response:

- **Severity declaration upfront**: name this as **P0 / SEV-1** with quantified blast radius — "All payment transactions failing → ~$X/min revenue impact, all checkout flows blocked, refund/retry obligations on partial transactions."
- **Timestamp correlation**: explicitly note "Deploy at T-45min, error onset at T-20min — 25-minute lag suggests bad code rolled out and slowly poisoned in-flight requests / cache state. Rollback is the right first action."
- **Parallel dispatch (named owners)**:
  - **`devops-lead`** → execute rollback NOW (specific command/platform action, e.g. `kubectl rollout undo` or platform redeploy of previous tag). Time-bound: rollback executed within 5 min, errors clear within 10 min, declare resolution after error rate ≤ baseline for 5 min.
  - **`dotnet-developer`** (the engineer who shipped the order-processing handler change) → begin diagnosis IN PARALLEL. Required evidence: deployment artefact diff, APM error traces, Grafana dashboard time-range link spanning T-50 to now, specific exception stack with first-occurrence timestamp.
- **Customer-comms escalation**: explicitly hand off to **`coordinator`** (or directly to support team via `cpo`) — CTO does NOT draft customer comms. Status page update + support team brief required.
- **Communication cadence**: name channels and timing — internal `#incident-payments` Slack channel (every 5 min), public status page (within 10 min of declaration, then every 15 min), support team brief (within 5 min so they stop guessing), exec notification (CEO/CPO within 15 min for revenue-impacting incident).
- **Coordinator-only role**: do NOT read code or hypothesise root cause yourself. Hypothesising is the diagnosing developer's job. Stay in coordination + comms.
- **Post-incident actions** (mandatory final list): **blameless post-mortem** with timestamped timeline, root-cause analysis, ADR / learnings doc capturing what the deployment process missed (no canary deploy, no health-check gate, no feature flag), action item to add at least one of those gates before the next deploy.

## Criteria

- [ ] PASS: CTO follows incident response protocol — detect/assess before root-causing
- [ ] PASS: First action is mitigation (rollback the deployment), not investigation
- [ ] PASS: CTO delegates to devops for the rollback and the relevant developer for diagnosis
- [ ] PASS: CTO escalates to coordinator for customer communication (support team is under CPO)
- [ ] PASS: Delegation includes specific evidence requirements — deployment logs, error traces, Grafana dashboard links
- [ ] PARTIAL: CTO identifies the blast radius (all payment transactions) and estimates customer impact
- [ ] PASS: Post-incident actions are mentioned — root cause analysis, ADR or post-mortem
- [ ] PASS: CTO does not attempt to debug the code directly — delegates to the specialist

## Output expectations

- [ ] PASS: Output's first action is mitigation — initiating rollback of the deployment from 45 minutes ago — not investigation, not log diving, not asking for more data
- [ ] PASS: Output correlates the deploy timestamp (45 min ago) with the error onset (20 min ago) explicitly — the 25-minute lag suggests the bad code rolled out and slowly poisoned in-flight requests / cache state, supporting the rollback decision
- [ ] PASS: Output dispatches DevOps to execute the rollback (specific command or platform action) and the .NET developer who shipped the order-processing handler change to begin diagnosis in parallel — not sequential
- [ ] PASS: Output escalates customer communication to the coordinator (or directly to the support team via CPO) — the CTO does not draft customer comms, but ensures someone is doing it
- [ ] PASS: Output specifies the evidence required from the diagnosing developer — deployment logs / artefact diff, error traces from APM, Grafana dashboard time-range link spanning before/after deploy, and the specific exception stack — so the post-rollback analysis is concrete
- [ ] PASS: Output quantifies blast radius — "all payment transactions failing" means revenue impact per minute, customer-side checkout failures, and likely refund / retry obligations — to set incident severity (probably P0/SEV-1)
- [ ] PASS: Output names the post-incident actions — blameless post-mortem with timeline, root cause analysis, ADR or learnings doc capturing what the deployment process missed (no canary, no health-check gate, no feature flag), and an action item to add the gate
- [ ] PASS: Output does NOT attempt to read code or hypothesise root cause directly — delegates to the developer who owns the change, while owning the coordination and communication
- [ ] PASS: Output establishes a timeline for the rollback (e.g. "rollback executed within 5 min, errors should clear within 10 min, declare resolution after error rate returns to baseline for 5 min")
- [ ] PARTIAL: Output addresses incident communication cadence — internal Slack channel, status page update for customers, support team brief — with timing per channel
