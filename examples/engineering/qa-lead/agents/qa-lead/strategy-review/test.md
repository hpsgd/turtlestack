---
# Match the model the agent declares (sonnet) in
# plugins/engineering/qa-lead/agents/qa-lead.md. The runner otherwise
# falls back to the harness default (Haiku), which is not what the
# agent is designed to run on.
target-model: claude-sonnet-4-6
---

# Test: Test strategy for new notifications microservice

Scenario: User asks the QA lead to define a test strategy for a new microservice that sends email, SMS, and push notifications. The service will be called by multiple other services via an internal API.

## Prompt

We're building a new notifications microservice. It receives requests from other internal services (via a REST API), queues them, and delivers via Sendgrid (email), Twilio (SMS), and Firebase (push). There's a preference/opt-out system per user per channel. The service needs to handle ~50,000 notifications/day at launch, growing to ~500,000 within 12 months. Can you define the test strategy before we start development?

## Criteria

- [ ] PASS: Agent operates as the definition of WHAT to test — does not write implementation test code (that is the QA Engineer's job)
- [ ] PASS: Agent assesses the risk profile before defining test levels — identifies financial/reputational risk (sending duplicate notifications, ignoring opt-outs)
- [ ] PASS: Agent defines test levels covering unit, integration (internal API contract, external API boundaries), and E2E
- [ ] PASS: Agent applies the 3 amigos framing — identifies questions the product owner and architect must answer before development starts
- [ ] PASS: Agent identifies edge cases in the edge case checklist: concurrency (duplicate send race condition), opt-out timing, channel fallback when one provider is down
- [ ] PASS: Agent sets specific, measurable quality gates for pre-merge and pre-release
- [ ] PASS: Agent flags testability concerns — e.g. external providers must be fakeable in integration tests, not called live
- [ ] PARTIAL: Agent assigns test levels to specific criteria with rationale (unit vs integration vs E2E reasoning)
- [ ] PASS: Output includes Risk Assessment, Test Levels table, Quality Gates, and at minimum one identified gap

## Output expectations

- [ ] PASS: Output's risk assessment names duplicate-send (financial/reputational), opt-out violations (legal/regulatory — TCPA / GDPR / spam laws), and provider outage as the top risks for a notifications service — not generic "data quality"
- [ ] PASS: Output's test levels table covers unit (logic, preference resolution), integration (internal REST API contract + external Sendgrid/Twilio/Firebase boundaries), and E2E (full request → queue → delivery → callback), with tools/coverage targets per level
- [ ] PASS: Output identifies the integration test pattern — fakes/contract tests at the Sendgrid/Twilio/Firebase boundaries, never live calls in CI — and names this as a testability requirement
- [ ] PASS: Output's edge case checklist covers concurrency (same notification dispatched twice in parallel), opt-out timing (preference change between queue-up and delivery), and channel fallback (one provider down — does the service queue, fail, or skip?)
- [ ] PASS: Output applies the 3 amigos lens — names specific questions for the product owner (what does delivery confirmation mean? what's the SLA on opt-out?) and architect (queue technology, retry strategy)
- [ ] PASS: Output sets specific quality gates pre-merge (coverage threshold, contract tests pass, lint/type clean) and pre-release (load test at 50K/day, opt-out audit query returns zero violations, provider failure simulation)
- [ ] PASS: Output addresses scaling from 50K to 500K notifications/day in the test strategy — load tests must validate the 10x growth path, not just the launch volume
- [ ] PASS: Output stays at strategy level — does NOT include implementation test code or specific test method names, leaving that to the QA Engineer
- [ ] PASS: Output identifies at least one specific gap — e.g. no fake Twilio/Sendgrid available yet, no preference-change-during-flight test scenario in scope, or no contract tests with the calling internal services
- [ ] PARTIAL: Output addresses observability requirements as a testability concern — tests need to assert delivery state, not just request acceptance, which requires hooks into the queue and provider callbacks
