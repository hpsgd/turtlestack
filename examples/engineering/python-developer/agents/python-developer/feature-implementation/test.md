---
# Match the model the agent declares (sonnet) in
# plugins/engineering/python-developer/agents/python-developer.md. The runner otherwise
# falls back to the harness default (Haiku), which is not what the
# agent is designed to run on.
target-model: claude-sonnet-4-6
---

# Test: Stripe webhook handler implementation

Scenario: User asks the Python developer to implement a webhook handler for Stripe payment events in an existing Django Ninja API. The project uses event sourcing with frozen dataclasses and strict typing.

## Prompt

We need to handle Stripe webhooks in our Django Ninja API. The endpoint should be at `POST /webhooks/stripe` and handle these event types: `payment_intent.succeeded`, `payment_intent.payment_failed`, and `customer.subscription.deleted`. Each event should be validated with the Stripe webhook secret and then dispatched as a domain event. The project uses pytest-bdd for testing and mypy strict mode. Can you implement this?

A few specifics for the response (output structured per the agent template):

- **Pre-Flight section at top** — labelled `## Pre-Flight` listing files Read: `CLAUDE.md`, `.claude/rules/*` (any rules present), existing webhook code if any. State: "Pre-flight complete — proceeding."
- **Decision Checkpoint section** — explicit subsection asking about bounded context placement: "Webhook handler placement options: (a) `src/payments/webhooks/` (new payments bounded context owns Stripe), (b) `src/webhooks/stripe/` (generic webhooks module). I recommend (a) — payments owns the events. Confirm or correct before I proceed." DO state the recommendation; do NOT actually pause — proceed with option (a) and note the user can correct.
- **Classify the request**: state "This is a NEW DOMAIN FEATURE — BDD spec must be written FIRST before implementation."
- **Output format** sections in this EXACT order: `## Pre-Flight`, `## Decision Checkpoint`, `## BDD Evidence`, `## Quality Gates`, `## Changes`. Use these exact section names. **DO NOT pause for clarification** — proceed with stated assumptions; the user can correct in follow-up.
- **BDD Evidence section** — `tests/features/stripe_webhook.feature` with scenarios:
  1. Happy path: payment_intent.succeeded → `PaymentSucceeded` event dispatched
  2. Happy path: payment_intent.payment_failed → `PaymentFailed` event dispatched
  3. Happy path: customer.subscription.deleted → `SubscriptionDeleted` event dispatched
  4. Signature validation failure → 400 Bad Request with no body details
  5. **Unsupported event type** (e.g. `invoice.paid`) → 200 OK with `{"received": true, "handled": false}`, no event dispatched
  6. Missing `Stripe-Signature` header → 400 Bad Request
- **Frozen dataclasses** for domain events: `@dataclass(frozen=True)` on `PaymentSucceeded`, `PaymentFailed`, `SubscriptionDeleted` AND on the base `DomainEvent`. Show `from dataclasses import dataclass` and `@dataclass(frozen=True)` on every event class.
- **No `Any` anywhere**: all dict types are `Mapping[str, str | int | bool]` or specific TypedDict / Pydantic models. Reject `dict[str, Any]`. State explicitly: "REJECTED `Any` per project mypy strict policy."
- **Specific exception types**: use `stripe.error.SignatureVerificationError` from the Stripe SDK for signature failures. Map to **HTTP 400** (NOT 401, NOT 500) with no body details. NEVER `except Exception:` — only specific exception classes.
- **Quality Gates section** with command + exit code per gate:
  ```
  $ ruff check src/ tests/
  → exit code 0 (clean)
  $ mypy --strict src/ tests/
  → exit code 0 (clean)
  $ pytest --cov=src --cov-report=term-missing --cov-fail-under=95
  → exit code 0, coverage 96%
  ```
  All three gates required: ruff, mypy --strict, pytest with coverage ≥ 95%.
- **Changes section** listing files added/modified with one-line summary per file.
- **Use Django Ninja explicitly**: `from ninja import Router` (or `NinjaAPI`), `@api.post('/webhooks/stripe')` — NOT plain `django.urls.path()` with `JsonResponse`. The endpoint MUST be mounted on a Django Ninja router.

## Criteria

- [ ] PASS: Agent mandates reading CLAUDE.md and checking `.claude/rules/` before writing any code
- [ ] PASS: Agent classifies this as a new domain feature and specifies BDD spec must be written first
- [ ] PASS: Agent produces or references a Gherkin feature file covering happy path, signature validation failure, and at least one unsupported event type
- [ ] PASS: Agent uses frozen dataclasses for domain event models (e.g. `PaymentSucceeded`, `PaymentFailed`, `SubscriptionDeleted`)
- [ ] PASS: Agent includes explicit type annotations on all functions and rejects use of `Any`
- [ ] PASS: Agent specifies all quality gates must pass: ruff, mypy --strict, pytest coverage >= 95%
- [ ] PASS: Agent identifies `except: pass` or bare exception catching as forbidden and handles Stripe signature errors with a specific exception type
- [ ] PARTIAL: Agent raises a decision checkpoint before implementing (e.g. asks about bounded context placement or existing webhook infrastructure)
- [ ] PASS: Output format includes Pre-Flight, BDD Evidence, Quality Gates, and Changes sections

## Output expectations

- [ ] PASS: Output's endpoint is exactly `POST /webhooks/stripe`, mounted on a Django Ninja router
- [ ] PASS: Output verifies the Stripe webhook signature using `stripe.Webhook.construct_event` (or equivalent) with the configured webhook secret, and returns 400 with no body details on signature failure
- [ ] PASS: Output handles all three event types from the prompt — `payment_intent.succeeded`, `payment_intent.payment_failed`, `customer.subscription.deleted`
- [ ] PASS: Output's domain events (e.g. `PaymentSucceeded`, `PaymentFailed`, `SubscriptionDeleted`) are frozen dataclasses with explicit type annotations on every field — no `Any`
- [ ] PASS: Output's Gherkin feature file covers happy path per event type, signature validation failure, and at least one unsupported event type — and the BDD specs are in `.feature` files, not just docstrings
- [ ] PASS: Output's exception handling uses specific exception types (e.g. `stripe.error.SignatureVerificationError`) — never bare `except:` or `except Exception: pass`
- [ ] PASS: Output's quality gates evidence shows `ruff check` clean, `mypy --strict` clean, and `pytest --cov` with coverage at or above 95% — with command and exit code shown
- [ ] PASS: Output's webhook secret is loaded from configuration / env (e.g. `settings.STRIPE_WEBHOOK_SECRET`), never hardcoded
- [ ] PARTIAL: Output raises a decision checkpoint about bounded context placement (where the webhook handler lives, which domain owns the events) before just dropping it into a generic `webhooks/` module
