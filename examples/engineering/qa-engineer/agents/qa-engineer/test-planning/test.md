---
# Match the model the agent declares (sonnet) in
# plugins/engineering/qa-engineer/agents/qa-engineer.md. The runner otherwise
# falls back to the harness default (Haiku), which is not what the
# agent is designed to run on.
target-model: claude-sonnet-4-6
---

# Test: Payment processing module test suite

Scenario: User asks the QA engineer to write tests for a payment processing module that handles charge creation, refunds, and webhook verification. The module has no existing tests.

## Prompt

We've just finished the payment processing module for our SaaS app. It handles three things: creating Stripe charges (with idempotency keys), processing refunds (full and partial), and verifying incoming Stripe webhooks using signature validation. There are currently zero tests. The module code is provided below as the specification — **treat it as code to implement via TDD, not code already on disk.**

Follow TDD in two phases:
1. **Phase 1 (RED):** Write ALL test files first, then run: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt -q && .venv/bin/pytest tests/ -v 2>&1 | tail -20` — confirm exit code 1 (import errors expected)
2. **Phase 2 (GREEN):** Write ALL source files, then run: `.venv/bin/pytest tests/ -v 2>&1 | tail -30` — confirm exit code 0

Create the project structure (`requirements.txt`, `config.py`, `src/__init__.py`, `src/payments/__init__.py`, `tests/__init__.py`, `tests/payments/__init__.py`) before writing tests.

```
# requirements.txt
stripe>=7.0.0
Django>=5.0.0
django-ninja>=1.3.0
pytest>=8.0.0
pytest-mock>=3.14.0
```

```python
# config.py
class _Settings:
    STRIPE_SECRET_KEY = "sk_test_fake_key_for_testing"
    STRIPE_WEBHOOK_SECRET = "whsec_test_secret_for_testing"

settings = _Settings()
```

Here is the module code to implement (write to disk in Phase 2, AFTER tests are written):

```python
# src/payments/charges.py
from __future__ import annotations

import stripe
from dataclasses import dataclass
from config import settings


@dataclass(frozen=True)
class ChargeResult:
    charge_id: str
    amount: int
    currency: str
    status: str


class ChargeError(Exception):
    pass


def create_charge(
    amount: int,
    currency: str,
    source: str,
    idempotency_key: str,
) -> ChargeResult:
    if amount <= 0:
        raise ChargeError(f"Amount must be positive, got {amount}")
    if not idempotency_key:
        raise ChargeError("idempotency_key is required")

    try:
        charge = stripe.Charge.create(
            amount=amount,
            currency=currency,
            source=source,
            idempotency_key=idempotency_key,
            api_key=settings.STRIPE_SECRET_KEY,
        )
    except stripe.error.CardError as exc:
        raise ChargeError(str(exc)) from exc

    return ChargeResult(
        charge_id=charge["id"],
        amount=charge["amount"],
        currency=charge["currency"],
        status=charge["status"],
    )
```

```python
# src/payments/refunds.py
from __future__ import annotations

import stripe
from dataclasses import dataclass
from config import settings


@dataclass(frozen=True)
class RefundResult:
    refund_id: str
    charge_id: str
    amount: int
    status: str


class RefundError(Exception):
    pass


def create_refund(charge_id: str, amount: int | None = None) -> RefundResult:
    """Create a refund. amount=None means full refund."""
    if amount is not None and amount <= 0:
        raise RefundError(f"Refund amount must be positive, got {amount}")

    params: dict = {"charge": charge_id}
    if amount is not None:
        params["amount"] = amount

    try:
        refund = stripe.Refund.create(
            **params,
            api_key=settings.STRIPE_SECRET_KEY,
        )
    except stripe.error.InvalidRequestError as exc:
        raise RefundError(str(exc)) from exc

    return RefundResult(
        refund_id=refund["id"],
        charge_id=refund["charge"],
        amount=refund["amount"],
        status=refund["status"],
    )
```

```python
# src/payments/webhooks.py
from __future__ import annotations

import stripe
from ninja import Router
from ninja.errors import HttpError
from config import settings

router = Router()


def verify_webhook_signature(payload: bytes, sig_header: str, secret: str) -> dict:
    """Verify Stripe webhook signature and return the event dict."""
    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=secret,
        )
    except stripe.error.SignatureVerificationError as exc:
        raise ValueError("Invalid webhook signature") from exc

    return dict(event)


@router.post("/webhooks/stripe")
def stripe_webhook(request) -> dict:
    payload = request.body
    sig_header = request.headers.get("Stripe-Signature", "")

    try:
        event = verify_webhook_signature(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HttpError(400, "Invalid signature")

    event_type = event.get("type", "")
    if event_type == "charge.succeeded":
        pass  # TODO: handle
    elif event_type == "charge.refunded":
        pass  # TODO: handle

    return {"received": True}
```

A few specifics for the response:

- **TDD with both exit codes shown**: run `.venv/bin/pytest tests/ -v 2>&1` BEFORE implementing — show the actual output ending with **`exit code 1`** (RED phase, expected import errors). Then implement, run again — show output ending with **`exit code 0`** (GREEN). Both runs must appear in DELIVERY.md.
- **Single-assertion-per-test discipline**: each `def test_*` asserts ONE behaviour. If you need to assert that a charge was created with the right amount AND currency AND the Stripe API was called once, that's THREE separate tests, not one with three asserts. Apply this consistently.
- **Mock at external boundary ONLY**: never mock `src.payments.webhooks.verify_webhook_signature` (internal). Mock `stripe.Webhook.construct_event` (external SDK boundary) in the verify-signature unit tests. Endpoint integration tests should call the real `verify_webhook_signature` with a mocked `stripe.Webhook.construct_event`.
- **Idempotency contract tests (2)**: (1) same idempotency key twice with same params → returns same charge, no duplicate stripe call; (2) same idempotency key with different params → raises `stripe.error.IdempotencyError`. Both required.
- **Refund tests (3 distinct)**: full refund (amount=None), partial refund (amount<original), AND **over-refund** (amount > remaining balance) raising `stripe.error.InvalidRequestError`. Plus refund-of-already-refunded charge.
- **Webhook signature tests (4)**: valid, missing `Stripe-Signature` header, invalid signature (tampered body), AND **replayed timestamp** outside Stripe's tolerance window (Stripe rejects events older than 5 minutes by default).
- **Use pytest fixtures / factories** for mock charge/refund/webhook objects in `conftest.py` — never inline dict construction repeated across tests. Define `charge_factory(amount=1000, currency="usd")` and reuse.
- **Evidence table** with columns: `Test name | Command | Exit code | Result (PASS/FAIL)`. List every test individually — not just category counts. Include both RED and GREEN runs.

## Criteria

- [ ] PASS: Agent reads existing code before writing any tests — inspects the module's public API surface, inputs, outputs, and error paths
- [ ] PASS: Agent follows TDD Iron Law — writes failing tests first (RED), confirms exit code 1, then implements to make them pass (GREEN)
- [ ] PASS: Agent identifies test cases across all required categories: happy path, edge cases (zero amounts, duplicate idempotency keys, expired cards), and error cases (network failures, invalid signatures)
- [ ] PASS: Agent runs tests in run mode (`pytest`, not watch mode) and reports exact command and exit code
- [ ] PASS: Agent mocks only at external boundaries (Stripe API) — does not mock internal payment module classes
- [ ] PASS: Agent identifies security-relevant test cases: signature validation bypass attempts, negative refund amounts, over-refund attempts
- [ ] PASS: Agent produces an evidence table with test name, command, exit code, and result
- [ ] PARTIAL: Agent covers both unit tests (pure logic) and integration-style tests for the webhook endpoint
- [ ] PASS: Agent applies one assertion per test — flags any test that would assert multiple unrelated things

## Output expectations

- [ ] PASS: Output groups test cases under all three named module functions — charge creation (with idempotency keys), refunds (full and partial), webhook signature verification — not generic "payment tests"
- [ ] PASS: Output's idempotency tests cover both happy path (same key → same charge, no duplicate) and edge case (same key with different amount → error / explicit handling), with the deterministic Stripe idempotency contract
- [ ] PASS: Output's refund tests separate full refund (amount = original charge) from partial refund (amount < original) and over-refund attempt (amount > remaining), each as a distinct test
- [ ] PASS: Output's webhook signature tests cover valid signature, missing signature header, invalid signature (tampered body), and replayed timestamp (Stripe tolerance window), with verbatim Stripe library exception types asserted
- [ ] PASS: Output mocks at the Stripe API boundary only (e.g. `stripe.Charge.create`, `stripe.Webhook.construct_event`) — no mocking of the project's own `payments.charges` or `payments.refunds` internal classes
- [ ] PASS: Output writes tests in TDD order — RED first (`pytest -v` shows the failing tests with exit code 1) — then implementation, then GREEN (exit code 0), with both commands and exit codes shown as evidence
- [ ] PASS: Output covers security-relevant adversarial tests — signature bypass attempts, negative refund amounts, refund of already-refunded charge, charge with negative amount — as required failures (the function rejects them)
- [ ] PASS: Output's evidence table has columns for test name, exact command, exit code, and PASS/FAIL — and lists every test, not just a summary count
- [ ] PASS: Output uses pytest fixtures and factories for charge/refund/webhook event objects rather than inline dict construction repeated across tests
- [ ] PARTIAL: Output covers integration-style tests for the webhook endpoint (POSTing a signed body to the Django Ninja route) separate from the unit tests on `verify_webhook_signature`
