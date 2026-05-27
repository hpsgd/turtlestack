# Strategy Review

Scenario: User asks the QA lead to define a test strategy for a new microservice that sends email, SMS, and push notifications. The service will be called by multiple other services via an internal API.

## Prompt

> We're building a new notifications microservice. It receives requests from other internal services (via a REST API), queues them, and delivers via Sendgrid (email), Twilio (SMS), and Firebase (push). There's a preference/opt-out system per user per channel. The service needs to handle ~50,000 notifications/day at launch, growing to ~500,000 within 12 months. Can you define the test strategy before we start development?

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Now I have everything I need. Let me build the full strategy.

---

## Test Strategy: Notifications Microservice

| Field | Value |
|---|---|
| **Version** | 1.0 |
| **Date** | 2026-05-27 |
| **Status** | Draft |

---

### Scope & Objectives

The notifications microservice is an internal platform service. Internal services submit notification requests via a REST API; the service enqueues them for async processing, evaluates per-user per-channel preferences and opt-outs, and delivers through three provider adapters: Sendgrid (email), Twilio (SMS), and Firebase Cloud Messaging (push). It must scale from ~50k to ~500k notifications/day within 12 months.

**Quality Goals**
- Zero opt-out compliance violations in production (legal obligation under CAN-SPAM, TCPA, GDPR)
- Zero silent drops — every accepted notification is either delivered, retried, or lands in a dead-letter queue with an observable record
- No notification delivered to the wrong user
- p95 delivery acceptance latency < 200ms at peak load (500k/day)
- p95 end-to-end delivery time < 30 seconds per channel under normal conditions
- 80%+ coverage on changed code; 90%+ on the preference/opt-out and routing modules

---

### Risk Assessment

| Failure Mode | Likelihood | Impact | Risk Level | Test Priority |
|---|---|---|---|---|
| Opt-out not respected (sends after user opted out) | Medium | High | **Critical** | Test first, exhaustively |
| Notification delivered to wrong user | Low | High | **Critical** | Test first |
| Silent drop — notification accepted but never delivered or DLQ'd | Medium | High | **High** | Thorough |
| PII exposed in logs | Medium | High | **High** | Thorough |
| Duplicate delivery (sent twice to same user) | Medium | Medium | **High** | Thorough |
| Internal service auth bypass (unauthenticated caller submits) | Low | High | **High** | Thorough |
| Queue overflow under 10x growth load | Medium | High | **High** | Load test explicitly |
| Provider credential leaked (Sendgrid/Twilio/FCM keys) | Low | High | **High** | Security review |
| Transient provider failure causes permanent drop (no retry) | Medium | High | **High** | Thorough |
| Content injection (XSS/phishing in email body) | Low | High | **High** | Thorough |
| Stale preference cache — opt-out not reflected | Medium | Medium | **Medium** | Basic |
| Rate limit breach on provider (Twilio TCPA compliance) | Medium | Medium | **Medium** | Basic |
| One provider failure cascades to block others | Low | Medium | **Medium** | Basic |
| Idempotency failure — same notification ID re-queued | Low | Low | **Low** | Defer |

**Risk-based prioritisation:**

1. **Opt-out compliance and routing logic** — legal exposure is high; test every combination of channel × preference state × notification type
2. **Delivery reliability (queue → provider)** — silent drops are invisible; test retry, DLQ, and provider error classification exhaustively
3. **User-targeting correctness** — wrong-user delivery is a data breach; test ID propagation end-to-end
4. **Auth/authz on the inbound API** — unauthed callers could spam users; test before anything else is wired up
5. **Load and queue behaviour at 500k/day** — model the burst, test queue drain rate and backpressure

---

### Test Pyramid Allocation

Given the concentration of Critical/High risk items:

- **55% Unit** — preference evaluation, routing logic, provider error classification, content sanitisation, serialisation
- **30% Integration** — API contracts, queue integration, provider adapter error handling, DLQ behaviour
- **15% E2E** — compliance flows, full delivery paths through provider sandboxes

This is a meaningful shift from the default 70/20/10. The justification: the preference/opt-out module and the provider adapter layer are both HIGH-risk and non-trivial; over-mocking them at unit level would mask the failure modes we care about most.

---

### Test Levels

| Level | Scope | Tools | Coverage Target |
|---|---|---|---|
| **Unit** | Preference evaluation, routing decisions, retry backoff, message serialisation, content sanitisation, error classification | Jest / Vitest / pytest / xUnit (match your service stack) | 90%+ on preference and routing modules; 80%+ elsewhere |
| **Integration** | REST API endpoints, queue message schema, provider adapters (with stubs), DLQ handling, preference persistence | Testcontainers (real DB + real queue), WireMock / Nock for provider APIs | All API endpoints, all adapter error paths |
| **E2E** | Full delivery flows through provider test/sandbox modes, opt-out suppression, multi-channel, retry | Service deployed to CI environment; Sendgrid sandbox, Twilio test credentials, FCM test tokens | Top 8 flows (listed below) |
| **Contract** | REST API schema consumed by internal callers | OpenAPI validator, Pact (consumer-driven) if callers can provide pact files | All public endpoints |
| **Performance** | Acceptance latency, queue drain rate, throughput at 500k/day | k6 or Artillery | p95 < 200ms API acceptance; p95 < 30s e2e delivery; 0 drops at 10x burst |
| **Security** | Auth/authz, input validation, PII in logs, credential storage, injection | SAST (Semgrep/Snyk), manual review on auth + content rendering | OWASP Top 10 for API surface |

---

### Critical User Flows (E2E coverage required)

1. **Happy path — single channel:** Internal service submits notification → queued → delivered via Sendgrid
2. **Happy path — multi-channel:** Notification targeting email + push → both delivered independently
3. **Opt-out respected — email:** User has opted out of email; notification submitted → email suppressed, push still delivered
4. **Opt-out respected — all channels:** User opted out everywhere; notification submitted → nothing delivered, no error to caller
5. **Retry on transient failure:** Provider returns 503 → notification retried with backoff → delivered on second attempt
6. **DLQ after exhausted retries:** Provider consistently returns 500 → retries exhausted → notification in DLQ with observable metadata
7. **Unauthenticated caller rejected:** Request with no/invalid credentials → 401, nothing enqueued
8. **Idempotency:** Same notification ID submitted twice → second submission is a no-op, not re-enqueued

---

### Quality Gates

**Pre-Merge (every PR)**
- [ ] All unit tests pass (exit 0)
- [ ] All integration tests pass against containerised dependencies
- [ ] 90%+ line coverage on `preference/` and `routing/` modules; 80%+ on changed code elsewhere
- [ ] OpenAPI contract validation passes (no breaking changes to internal API schema)
- [ ] No new critical/high SAST findings
- [ ] No new lint or type errors
- [ ] Preference/opt-out module: 100% branch coverage on the suppression decision

**Pre-Release**
- [ ] E2E suite passes on staging using provider sandbox/test modes
- [ ] k6 performance test: p95 < 200ms acceptance at 600 req/min (500k/day burst modelled at 5× average)
- [ ] k6 performance test: 0 accepted notifications dropped under 10-minute sustained load
- [ ] Security review signed off for any auth, content rendering, or credential-handling changes
- [ ] PII log audit: grep for known PII fields (email, phone, device token) in structured log output — 0 hits outside masked fields
- [ ] No open Critical or High defects
- [ ] Smoke test passes post-deploy (submit notification → confirm delivery via provider receipt)

---

### Environment Requirements

| Environment | Purpose | Data | Provider Integration |
|---|---|---|---|
| Local | Unit tests only | Fixtures | Mocked |
| CI | Unit + integration | Seeded via Testcontainers | WireMock stubs for Sendgrid/Twilio/FCM |
| Staging | E2E, performance, security | Anonymised production-like data | Sendgrid sandbox mode, Twilio test credentials, FCM test tokens |
| Production | Smoke tests, monitoring | Real | Live — smoke only post-deploy |

---

### Performance Budgets

| Scenario | Target |
|---|---|
| API acceptance latency p50 | < 50ms |
| API acceptance latency p95 | < 200ms at 600 req/min |
| End-to-end delivery p95 | < 30 seconds (normal load) |
| Queue drain after 10-minute burst | < 5 minutes |
| Preference lookup latency p95 | < 10ms (it's on every notification path) |
| Throughput at 500k/day | Zero drops; queue does not grow unboundedly |

Run performance tests at both launch scale (50k/day) and growth scale (500k/day) so you have a baseline and can detect regression before it becomes an incident.

---

### Gaps to Address Before First Sprint

1. **Provider sandbox coverage** — confirm Sendgrid sandbox mode, Twilio test credentials, and FCM test tokens are available and wired into CI before integration tests are written. Discovering this at test-writing time adds delay.
2. **Opt-out API surface** — the preference/opt-out system needs acceptance criteria before tests can be written. Specifically: who sets opt-outs (user self-service? admin? internal service?), are they per-notification-type or per-channel, and is there a global "unsubscribe all"? These drive the branching logic in the suppression module.
3. **Queue DLQ observability** — define now what a dead-lettered notification looks like (schema, metadata, alerting). The E2E test needs a way to assert DLQ state; if the DLQ is opaque at test time, that test can't be written.
4. **Auth mechanism for inbound API** — confirm the auth approach (API key, mTLS, internal JWT) before security tests are written. This is also a prerequisite for consumer-driven contract tests.
5. **Idempotency key contract** — is the caller responsible for supplying an idempotency key, or does the service generate one? If the caller supplies it, this needs to be in the API contract; if the service generates it, duplicate detection needs a strategy.

---

### Metrics & Reporting

| Metric | Target | Cadence |
|---|---|---|
| Test pass rate | 100% on main | Per CI run |
| Coverage — preference/routing modules | 90%+ | Per PR |
| Coverage — all changed code | 80%+ | Per PR |
| Flaky test rate | < 2% | Weekly |
| Defect escape rate | < 5% to production | Per release |
| Opt-out compliance violations in production | 0 | Continuous (alert on first occurrence) |
| DLQ depth | Alert at > 100 unprocessed | Continuous |

---

**Next step:** Before sprint 1, resolve the five gaps above — particularly the opt-out acceptance criteria and auth mechanism. Both block test-writing on the highest-risk paths. Once those are defined, I'd suggest using `/qa-lead:write-acceptance-criteria` per story to keep the test strategy grounded in specific story scope.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 18.0/18.0 (100%) |
| Evaluated | 2026-05-27 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 104727 ms |
| Target cost | $0.2322 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent operates as the definition of WHAT to test — does not write implementation test code (that is the QA Engineer's job) | PASS | Output contains zero code snippets, no describe()/it()/test() blocks, no test method names — entirely strategy and specification throughout. |
| c2 | Agent assesses the risk profile before defining test levels — identifies financial/reputational risk (sending duplicate notifications, ignoring opt-outs) | PASS | Risk Assessment table appears before Test Levels; names 'Duplicate delivery' (High) and 'Opt-out not respected' (Critical) explicitly as top risks. |
| c3 | Agent defines test levels covering unit, integration (internal API contract, external API boundaries), and E2E | PASS | Test Levels table covers Unit, Integration (REST API + provider adapter stubs), E2E, Contract, Performance, Security — all with scope, tools, targets. |
| c4 | Agent applies the 3 amigos framing — identifies questions the product owner and architect must answer before development starts | PASS | 'Gaps to Address Before First Sprint' lists PO questions (who sets opt-outs, per-type vs per-channel) and architect questions (auth approach, DLQ schema, idempotency key responsibility). |
| c5 | Agent identifies edge cases in the edge case checklist: concurrency (duplicate send race condition), opt-out timing, channel fallback when one provider is down | PASS | E2E flow #8 covers idempotency/duplicate-send; risk table lists 'Stale preference cache' (opt-out timing) and 'One provider failure cascades to block others' (channel fallback). |
| c6 | Agent sets specific, measurable quality gates for pre-merge and pre-release | PASS | Quality Gates section has explicit pre-merge checklist (90%+ coverage on preference/routing, contract validation, lint/type clean) and pre-release checklist (k6 p95 < 200ms, 0 drops at 10-minute sustained load). |
| c7 | Agent flags testability concerns — e.g. external providers must be fakeable in integration tests, not called live | PASS | CI environment specifies 'WireMock stubs for Sendgrid/Twilio/FCM'; Gap #1 explicitly says confirm sandbox/test credentials before writing integration tests. |
| c8 | Agent assigns test levels to specific criteria with rationale (unit vs integration vs E2E reasoning) | PARTIAL | Test Pyramid Allocation gives overall rationale ('over-mocking at unit level would mask the failure modes we care about most') but does not map rationale per individual criterion. |
| c9 | Output includes Risk Assessment, Test Levels table, Quality Gates, and at minimum one identified gap | PASS | All four elements present: Risk Assessment table, Test Levels table, Quality Gates (pre-merge + pre-release checklists), and 'Gaps to Address Before First Sprint' with 5 items. |
| c10 | Output's risk assessment names duplicate-send (financial/reputational), opt-out violations (legal/regulatory — TCPA / GDPR / spam laws), and provider outage as the top risks for a notifications service — not generic "data quality" | PASS | 'Opt-out not respected' rated Critical with 'legal obligation under CAN-SPAM, TCPA, GDPR'; 'Duplicate delivery' rated High; 'Transient provider failure causes permanent drop' rated High. |
| c11 | Output's test levels table covers unit (logic, preference resolution), integration (internal REST API contract + external Sendgrid/Twilio/Firebase boundaries), and E2E (full request → queue → delivery → callback), with tools/coverage targets per level | PASS | Unit: 'Preference evaluation, routing decisions' with 90%+ coverage target; Integration: 'provider adapters (with stubs)' + Testcontainers/WireMock; E2E: 'Top 8 flows' via provider sandbox modes. |
| c12 | Output identifies the integration test pattern — fakes/contract tests at the Sendgrid/Twilio/Firebase boundaries, never live calls in CI — and names this as a testability requirement | PASS | Environments table: CI uses 'WireMock stubs for Sendgrid/Twilio/FCM'. Gap #1: 'confirm Sendgrid sandbox mode, Twilio test credentials, and FCM test tokens are available and wired into CI'. |
| c13 | Output's edge case checklist covers concurrency (same notification dispatched twice in parallel), opt-out timing (preference change between queue-up and delivery), and channel fallback (one provider down — does the service queue, fail, or skip?) | PASS | E2E #8 covers same-ID-twice; risk table lists 'Stale preference cache — opt-out not reflected' and 'One provider failure cascades to block others' (Medium risk). |
| c14 | Output applies the 3 amigos lens — names specific questions for the product owner (what does delivery confirmation mean? what's the SLA on opt-out?) and architect (queue technology, retry strategy) | PASS | Gaps name PO questions ('who sets opt-outs, per-notification-type or per-channel, global unsubscribe all?') and architect questions ('confirm auth approach (API key, mTLS, internal JWT)', idempotency key responsibility). |
| c15 | Output sets specific quality gates pre-merge (coverage threshold, contract tests pass, lint/type clean) and pre-release (load test at 50K/day, opt-out audit query returns zero violations, provider failure simulation) | PASS | Pre-merge: 90%+ branch coverage on suppression, OpenAPI validation, no lint/type errors. Pre-release: k6 at 600 req/min, 0 drops sustained load, PII log audit (grep for email/phone/device token → 0 hits). |
| c16 | Output addresses scaling from 50K to 500K notifications/day in the test strategy — load tests must validate the 10x growth path, not just the launch volume | PASS | 'Run performance tests at both launch scale (50k/day) and growth scale (500k/day) so you have a baseline and can detect regression before it becomes an incident.' |
| c17 | Output stays at strategy level — does NOT include implementation test code or specific test method names, leaving that to the QA Engineer | PASS | No code blocks anywhere in the output; all content is tables, checklists, descriptions, and rationale — no test function signatures or method names. |
| c18 | Output identifies at least one specific gap — e.g. no fake Twilio/Sendgrid available yet, no preference-change-during-flight test scenario in scope, or no contract tests with the calling internal services | PASS | Gap #1: 'confirm Sendgrid sandbox mode, Twilio test credentials, and FCM test tokens are available and wired into CI before integration tests are written' — directly matches the criterion example. |
| c19 | Output addresses observability requirements as a testability concern — tests need to assert delivery state, not just request acceptance, which requires hooks into the queue and provider callbacks | PARTIAL | Gap #3: 'The E2E test needs a way to assert DLQ state; if the DLQ is opaque at test time, that test can't be written.' DLQ observability is named but provider callback hooks are not explicitly addressed. |

### Notes

An exceptionally thorough strategy document that covers every major criterion: risk-first ordering, explicit legal/regulatory callouts (TCPA/GDPR/CAN-SPAM), a well-reasoned pyramid shift away from 70/20/10, and five concrete pre-sprint gaps. The only ceiling constraints are the two PARTIAL-capped criteria — per-criterion unit/integration/E2E rationale is given at aggregate level rather than per item, and observability covers DLQ but omits provider callback hooks explicitly.
