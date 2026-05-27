---
# Match the model the agent declares (sonnet) in
# plugins/product/internal-docs-writer/agents/internal-docs-writer.md. The runner otherwise
# falls back to the harness default (Haiku), which is not what the
# agent is designed to run on.
target-model: claude-sonnet-4-6
---

# Test: Runbook creation

Scenario: An engineering team needs a runbook for handling payment processing failures so on-call engineers can resolve incidents without tribal knowledge.

## Prompt


Write a runbook for payment processing failures. Context:

- We use Stripe for payment processing
- Common failure modes: Stripe API timeouts, card declines (various codes), idempotency key conflicts, webhook delivery failures
- Our stack: Node.js API, PostgreSQL, Redis for job queues (Bull), Datadog for monitoring
- Alert fires when: payment success rate drops below 95% over 5 minutes, or any Stripe API error rate exceeds 2%
- Business impact: each minute of payment failure = ~$3,400 in lost transactions during peak hours

On-call engineers are expected to handle this without waking anyone up for most scenarios. We've had 4 incidents this quarter and each one took 45+ minutes to resolve because engineers didn't know where to look.

A few specifics for the response:

- Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
- Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
- For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
- When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
- Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Criteria


- [ ] PASS: Written for a first-timer at 2am — no assumed knowledge of the system, all commands are copy-pasteable with expected output shown
- [ ] PASS: Includes a decision tree or clear branching logic for different failure modes (API timeout vs card declines vs webhook failures vs idempotency conflicts)
- [ ] PASS: Every diagnostic step includes the exact command or query to run, not just "check the logs" or "look in Datadog"
- [ ] PASS: Includes a rollback or safe revert step for any action that could make the situation worse
- [ ] PASS: Specifies an escalation path with roles and contact method — who to wake up and when, not "escalate if needed"
- [ ] PASS: Documents how to verify the incident is resolved (what metric to watch, what threshold confirms recovery)
- [ ] PARTIAL: Covers all four failure modes mentioned — partial credit if 2-3 are covered but one is missing
- [ ] PASS: Includes severity classification or impact assessment so the on-call engineer can judge urgency (the $3,400/minute context should inform this)

## Output expectations

- [ ] PASS: Output's runbook header states the alert trigger conditions verbatim — payment success rate < 95% over 5 min, OR Stripe API error rate > 2% — and the $3,400/minute business impact, so the on-call knows the urgency immediately
- [ ] PASS: Output's decision tree branches on the first observable signal (which alert fired? what's the dominant error code from logs/Datadog?) and routes to one of four specific failure modes — Stripe API timeout, card declines, idempotency conflict, webhook delivery failure
- [ ] PASS: Output's diagnostic commands are exact and copy-pasteable — e.g. `datadog query payment.errors{service:payment-api} | sum:1m` or `psql -c "SELECT COUNT(*) FROM payments WHERE status='failed' AND created_at > NOW() - INTERVAL '5 minutes';"` — not "check the logs"
- [ ] PASS: Output's commands each show the expected output / threshold — e.g. "expected: error count < 50/min in healthy state; if you see 200+/min, this confirms an API outage"
- [ ] PASS: Output handles each of the four failure modes with branch-specific diagnostics — Stripe outage (check status.stripe.com, fail-over to retry queue), card declines (check decline code distribution, no rollback needed), idempotency conflicts (check Redis key collisions, clear stuck keys with named command), webhook failures (check Bull queue depth, retry failed webhooks)
- [ ] PASS: Output's rollback steps are explicit for any destructive action — e.g. "if you disable the payment processor, re-enable with `kubectl scale deployment/payment-processor --replicas=3`"
- [ ] PASS: Output's escalation thresholds are defined — e.g. "if no resolution after 30 min OR Stripe status page shows incident, page the engineering manager via PagerDuty severity 1"
- [ ] PASS: Output's verification step shows what success looks like — payment success rate back above 95% for 10 consecutive minutes, error rate below 0.5%, no new alerts firing — with an illustrative Datadog query in the same syntax style as the diagnostic commands
- [ ] PASS: Output is written for a first-timer at 2am — every step has a single action, no assumed knowledge of which dashboard or which Redis key, all paths absolute
