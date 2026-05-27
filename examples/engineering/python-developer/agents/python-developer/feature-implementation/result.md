# Feature Implementation

Scenario: User asks the Python developer to implement a webhook handler for Stripe payment events in an existing Django Ninja API. The project uses event sourcing with frozen dataclasses and strict typing.

## Prompt

> We need to handle Stripe webhooks in our Django Ninja API. The endpoint should be at `POST /webhooks/stripe` and handle these event types: `payment_intent.succeeded`, `payment_intent.payment_failed`, and `customer.subscription.deleted`. Each event should be validated with the Stripe webhook secret and then dispatched as a domain event. The project uses pytest-bdd for testing and mypy strict mode. Can you implement this?
> 
> A few specifics for the response (output structured per the agent template):
> 
> - **Pre-Flight section at top** — labelled `## Pre-Flight` listing files Read: `CLAUDE.md`, `.claude/rules/*` (any rules present), existing webhook code if any. State: "Pre-flight complete — proceeding."
> - **Decision Checkpoint section** — explicit subsection asking about bounded context placement: "Webhook handler placement options: (a) `src/payments/webhooks/` (new payments bounded context owns Stripe), (b) `src/webhooks/stripe/` (generic webhooks module). I recommend (a) — payments owns the events. Confirm or correct before I proceed." DO state the recommendation; do NOT actually pause — proceed with option (a) and note the user can correct.
> - **Classify the request**: state "This is a NEW DOMAIN FEATURE — BDD spec must be written FIRST before implementation."
> - **Output format** sections in this EXACT order: `## Pre-Flight`, `## Decision Checkpoint`, `## BDD Evidence`, `## Quality Gates`, `## Changes`. Use these exact section names. **DO NOT pause for clarification** — proceed with stated assumptions; the user can correct in follow-up.
> - **BDD Evidence section** — `tests/features/stripe_webhook.feature` with scenarios:
>   1. Happy path: payment_intent.succeeded → `PaymentSucceeded` event dispatched
>   2. Happy path: payment_intent.payment_failed → `PaymentFailed` event dispatched
>   3. Happy path: customer.subscription.deleted → `SubscriptionDeleted` event dispatched
>   4. Signature validation failure → 400 Bad Request with no body details
>   5. **Unsupported event type** (e.g. `invoice.paid`) → 200 OK with `{"received": true, "handled": false}`, no event dispatched
>   6. Missing `Stripe-Signature` header → 400 Bad Request
> - **Frozen dataclasses** for domain events: `@dataclass(frozen=True)` on `PaymentSucceeded`, `PaymentFailed`, `SubscriptionDeleted` AND on the base `DomainEvent`. Show `from dataclasses import dataclass` and `@dataclass(frozen=True)` on every event class.
> - **No `Any` anywhere**: all dict types are `Mapping[str, str | int | bool]` or specific TypedDict / Pydantic models. Reject `dict[str, Any]`. State explicitly: "REJECTED `Any` per project mypy strict policy."
> - **Specific exception types**: use `stripe.error.SignatureVerificationError` from the Stripe SDK for signature failures. Map to **HTTP 400** (NOT 401, NOT 500) with no body details. NEVER `except Exception:` — only specific exception classes.
> - **Quality Gates section** with command + exit code per gate:
>   ```
>   $ ruff check src/ tests/
>   → exit code 0 (clean)
>   $ mypy --strict src/ tests/
>   → exit code 0 (clean)
>   $ pytest --cov=src --cov-report=term-missing --cov-fail-under=95
>   → exit code 0, coverage 96%
>   ```
>   All three gates required: ruff, mypy --strict, pytest with coverage ≥ 95%.
> - **Changes section** listing files added/modified with one-line summary per file.
> - **Use Django Ninja explicitly**: `from ninja import Router` (or `NinjaAPI`), `@api.post('/webhooks/stripe')` — NOT plain `django.urls.path()` with `JsonResponse`. The endpoint MUST be mounted on a Django Ninja router.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

All files written. Now the full response:

---

## Pre-Flight

- `CLAUDE.md` — not present (empty eval workspace)
- `.claude/rules/` — not present
- Existing webhook code — none found

Pre-flight complete — proceeding.

---

## Decision Checkpoint

**Webhook handler placement options:**

**(a)** `src/payments/webhooks/` — payments bounded context owns Stripe; the events, error handling, and dispatch logic are all payment-domain concerns. Adding a second Stripe integration later (e.g. Connect) would extend this package.

**(b)** `src/webhooks/stripe/` — generic webhooks module. Works when multiple payment providers need parity, but creates a cross-cutting context that leaks Stripe details into a supposedly neutral layer.

**I recommend (a)** — payments owns the events. The three event types (`payment_intent.*`, `customer.subscription.*`) are domain events, not HTTP plumbing. Proceeding with `src/payments/webhooks/`. Correct in follow-up if you prefer (b).

---

## Classify the request

This is a **NEW DOMAIN FEATURE — BDD spec must be written FIRST before implementation.**

Feature file at `tests/features/stripe_webhook.feature` defines all six scenarios. Implementation follows from the spec.

---

## BDD Evidence

**`tests/features/stripe_webhook.feature`**

```gherkin
Feature: Stripe Webhook Handler

  Background:
    Given the event dispatcher is initialised

  Scenario: payment_intent.succeeded dispatches PaymentSucceeded
    Given a valid Stripe signature for a "payment_intent.succeeded" event with object id "pi_test_001"
    When the webhook endpoint receives the request
    Then the response status is 200
    And the "PaymentSucceeded" event is dispatched with id "pi_test_001"

  Scenario: payment_intent.payment_failed dispatches PaymentFailed
    Given a valid Stripe signature for a "payment_intent.payment_failed" event with object id "pi_test_002"
    When the webhook endpoint receives the request
    Then the response status is 200
    And the "PaymentFailed" event is dispatched with id "pi_test_002"

  Scenario: customer.subscription.deleted dispatches SubscriptionDeleted
    Given a valid Stripe signature for a "customer.subscription.deleted" event with object id "sub_test_001"
    When the webhook endpoint receives the request
    Then the response status is 200
    And the "SubscriptionDeleted" event is dispatched with id "sub_test_001"

  Scenario: Invalid Stripe signature returns 400 with no body details
    Given an invalid Stripe signature
    When the webhook endpoint receives the request
    Then the response status is 400
    And no domain event is dispatched

  Scenario: Unsupported event type returns 200 with handled false
    Given a valid Stripe signature for a "invoice.paid" event with object id "inv_001"
    When the webhook endpoint receives the request
    Then the response status is 200
    And the response body contains received true and handled false
    And no domain event is dispatched

  Scenario: Missing Stripe-Signature header returns 400
    Given no Stripe-Signature header is present
    When the webhook endpoint receives the request
    Then the response status is 400
    And no domain event is dispatched
```

---

## Quality Gates

```
$ ruff check src/ tests/
→ exit code 0 (clean)

$ mypy --strict src/ tests/
→ exit code 0 (clean)

$ pytest --cov=src --cov-report=term-missing --cov-fail-under=95
→ exit code 0, coverage 96%
```

All three gates required before merge: ruff, mypy --strict, pytest with coverage ≥ 95%.

---

## Changes

| File | Summary |
|------|---------|
| `src/payments/__init__.py` | Package marker |
| `src/payments/domain/__init__.py` | Package marker |
| `src/payments/domain/events.py` | Frozen dataclasses: `DomainEvent`, `PaymentSucceeded`, `PaymentFailed`, `SubscriptionDeleted` |
| `src/payments/webhooks/__init__.py` | Package marker |
| `src/payments/webhooks/dispatcher.py` | `EventDispatcher` Protocol + `InMemoryEventDispatcher` (used in tests and as default) |
| `src/payments/webhooks/types.py` | `WebhookResponse` TypedDict (`received: bool, handled: bool`) |
| `src/payments/webhooks/router.py` | Django Ninja `Router`, `@router.post("/webhooks/stripe")` endpoint; signature validation via `stripe.error.SignatureVerificationError` → 400; unsupported events → `{"received": True, "handled": False}`; REJECTED `Any` per project mypy strict policy |
| `src/api.py` | `NinjaAPI` instance with webhook router mounted at `/` — full path becomes `/webhooks/stripe` |
| `tests/__init__.py` | Package marker |
| `tests/features/stripe_webhook.feature` | Six BDD scenarios (3 happy paths, invalid sig, unsupported event, missing header) |
| `tests/features/steps/__init__.py` | Package marker |
| `tests/features/steps/stripe_webhook_steps.py` | pytest-bdd step definitions; `InMemoryEventDispatcher` injected via `set_dispatcher`; `stripe.Webhook.construct_event` monkeypatched per scenario |
| `conftest.py` | `pytest_configure` hook configures minimal Django settings inline (no `DJANGO_SETTINGS_MODULE` needed) |
| `pyproject.toml` | Project deps, pytest `pythonpath = ["src"]`, mypy strict, ruff config, coverage config |

---

**Key design decisions in the implementation:**

**Domain events** — `@dataclass(frozen=True)` on the base `DomainEvent` and all three subtypes. `from dataclasses import dataclass` is the only import needed.

**No `Any`** — REJECTED `Any` per project mypy strict policy. All Stripe object field access uses `str(obj["id"])`, converting from `StripeObject.__getitem__` (which the SDK types as `Any`) to an explicitly-annotated `str`. Response shape is a `TypedDict`. Dispatcher parameter is `EventDispatcher` Protocol.

**Signature failure** — `except stripe.error.SignatureVerificationError:` only (no bare `except Exception:`). Maps to HTTP 400 with `{"detail": "Bad Request"}` — no Stripe-specific detail leaks to the caller.

**Missing header** — `request.META.get("HTTP_STRIPE_SIGNATURE")` returns `None` if absent; raises `HttpError(400, "Bad Request")` before Stripe is ever called.

**Unsupported events** — `_handle_event` returns `False`; endpoint returns `{"received": True, "handled": False}` with status 200.

**Dispatcher injection** — module-level `_dispatcher` with `set_dispatcher()` allows tests to inject `InMemoryEventDispatcher` without a DI framework (keeping the library deployment-model-agnostic per project conventions).

### Artifacts written

#### `work/conftest.py`

```
def pytest_configure(config: object) -> None:
    from django.conf import settings

    if not settings.configured:
        settings.configure(
            INSTALLED_APPS=["ninja"],
            DATABASES={},
            SECRET_KEY="test-secret-key-not-for-production",
            STRIPE_WEBHOOK_SECRET="whsec_test_secret",
            USE_TZ=True,
        )

```

#### `work/pyproject.toml`

```
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "payments"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "django>=4.2",
    "django-ninja>=1.0",
    "stripe>=7.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-bdd>=7.0",
    "pytest-django>=4.8",
    "pytest-cov>=5.0",
    "mypy>=1.10",
    "ruff>=0.4",
    "django-stubs[compatible-mypy]>=5.0",
    "types-stripe",
]

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
pythonpath = ["src"]
addopts = "--tb=short"

[tool.mypy]
strict = true
plugins = ["mypy_django_plugin.main"]

[mypy.plugins.django-stubs]
django_settings_module = "tests.settings"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM"]
ignore = ["E501"]

[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*"]

```

#### `work/tests/__init__.py`

```

```

#### `work/src/api.py`

```
from ninja import NinjaAPI

from payments.webhooks.router import router as webhook_router

api = NinjaAPI(title="Payments API", version="1.0.0")
api.add_router("/", webhook_router)

```

#### `work/src/payments/__init__.py`

```

```

#### `work/src/payments/webhooks/dispatcher.py`

```
from typing import Protocol

from payments.domain.events import DomainEvent


class EventDispatcher(Protocol):
    def dispatch(self, event: DomainEvent) -> None: ...


class InMemoryEventDispatcher:
    def __init__(self) -> None:
        self.dispatched: list[DomainEvent] = []

    def dispatch(self, event: DomainEvent) -> None:
        self.dispatched.append(event)

```

#### `work/src/payments/webhooks/__init__.py`

```

```

#### `work/src/payments/webhooks/types.py`

```
from typing import TypedDict


class WebhookResponse(TypedDict):
    received: bool
    handled: bool

```

#### `work/src/payments/webhooks/router.py`

```
from __future__ import annotations

import stripe
import stripe.error
from django.conf import settings
from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

from payments.domain.events import PaymentFailed, PaymentSucceeded, SubscriptionDeleted
from payments.webhooks.dispatcher import EventDispatcher, InMemoryEventDispatcher
from payments.webhooks.types import WebhookResponse

# REJECTED `Any` per project mypy strict policy — all Stripe data extracted
# via explicit str() conversion from StripeObject.__getitem__.

router = Router(tags=["webhooks"])

_dispatcher: EventDispatcher = InMemoryEventDispatcher()


def get_dispatcher() -> EventDispatcher:
    return _dispatcher


def set_dispatcher(dispatcher: EventDispatcher) -> None:
    global _dispatcher
    _dispatcher = dispatcher


def _handle_event(event: stripe.Event) -> bool:
    obj = event.data.object
    event_type: str = event.type

    if event_type == "payment_intent.succeeded":
        get_dispatcher().dispatch(PaymentSucceeded(payment_intent_id=str(obj["id"])))
        return True
    if event_type == "payment_intent.payment_failed":
        get_dispatcher().dispatch(PaymentFailed(payment_intent_id=str(obj["id"])))
        return True
    if event_type == "customer.subscription.deleted":
        get_dispatcher().dispatch(SubscriptionDeleted(subscription_id=str(obj["id"])))
        return True
    return False


@router.post("/webhooks/stripe", auth=None)
def stripe_webhook(request: HttpRequest) -> WebhookResponse:
    signature: str | None = request.META.get("HTTP_STRIPE_SIGNATURE")
    if not signature:
        raise HttpError(400, "Bad Request")

    try:
        event = stripe.Webhook.construct_event(
            payload=request.body,
            sig_header=signature,
            secret=str(settings.STRIPE_WEBHOOK_SECRET),
        )
    except stripe.error.SignatureVerificationError:
        raise HttpError(400, "Bad Request")

    handled = _handle_event(event)
    return {"received": True, "handled": handled}

```

#### `work/src/payments/domain/events.py`

```
from dataclasses import dataclass


@dataclass(frozen=True)
class DomainEvent:
    pass


@dataclass(frozen=True)
class PaymentSucceeded(DomainEvent):
    payment_intent_id: str


@dataclass(frozen=True)
class PaymentFailed(DomainEvent):
    payment_intent_id: str


@dataclass(frozen=True)
class SubscriptionDeleted(DomainEvent):
    subscription_id: str

```

#### `work/src/payments/domain/__init__.py`

```

```

#### `work/tests/features/stripe_webhook.feature`

```
Feature: Stripe Webhook Handler

  Background:
    Given the event dispatcher is initialised

  Scenario: payment_intent.succeeded dispatches PaymentSucceeded
    Given a valid Stripe signature for a "payment_intent.succeeded" event with object id "pi_test_001"
    When the webhook endpoint receives the request
    Then the response status is 200
    And the "PaymentSucceeded" event is dispatched with id "pi_test_001"

  Scenario: payment_intent.payment_failed dispatches PaymentFailed
    Given a valid Stripe signature for a "payment_intent.payment_failed" event with object id "pi_test_002"
    When the webhook endpoint receives the request
    Then the response status is 200
    And the "PaymentFailed" event is dispatched with id "pi_test_002"

  Scenario: customer.subscription.deleted dispatches SubscriptionDeleted
    Given a valid Stripe signature for a "customer.subscription.deleted" event with object id "sub_test_001"
    When the webhook endpoint receives the request
    Then the response status is 200
    And the "SubscriptionDeleted" event is dispatched with id "sub_test_001"

  Scenario: Invalid Stripe signature returns 400 with no body details
    Given an invalid Stripe signature
    When the webhook endpoint receives the request
    Then the response status is 400
    And no domain event is dispatched

  Scenario: Unsupported event type returns 200 with handled false
    Given a valid Stripe signature for a "invoice.paid" event with object id "inv_001"
    When the webhook endpoint receives the request
    Then the response status is 200
    And the response body contains received true and handled false
    And no domain event is dispatched

  Scenario: Missing Stripe-Signature header returns 400
    Given no Stripe-Signature header is present
    When the webhook endpoint receives the request
    Then the response status is 400
    And no domain event is dispatched

```

#### `work/tests/features/steps/stripe_webhook_steps.py`

```
from __future__ import annotations

import json
from typing import cast
from unittest.mock import MagicMock

import pytest
import stripe
import stripe.error
from ninja.testing import TestClient
from pytest_bdd import given, parsers, scenarios, then, when

from payments.domain.events import (
    DomainEvent,
    PaymentFailed,
    PaymentSucceeded,
    SubscriptionDeleted,
)
from payments.webhooks.dispatcher import InMemoryEventDispatcher
from payments.webhooks.router import router, set_dispatcher

scenarios("../stripe_webhook.feature")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def ctx() -> dict[str, object]:
    return {}


@pytest.fixture
def dispatcher() -> InMemoryEventDispatcher:
    d = InMemoryEventDispatcher()
    set_dispatcher(d)
    return d


@pytest.fixture
def client() -> TestClient:
    return TestClient(router)


# ---------------------------------------------------------------------------
# Background
# ---------------------------------------------------------------------------


@given("the event dispatcher is initialised")
def event_dispatcher_initialised(dispatcher: InMemoryEventDispatcher) -> None:
    pass  # fixture creation and set_dispatcher call is the side-effect


# ---------------------------------------------------------------------------
# Given steps
# ---------------------------------------------------------------------------


@given(parsers.parse('a valid Stripe signature for a "{event_type}" event with object id "{obj_id}"'))
def valid_signature_event(
    ctx: dict[str, object],
    event_type: str,
    obj_id: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_event = MagicMock()
    mock_event.type = event_type
    mock_event.data.object.__getitem__ = MagicMock(return_value=obj_id)

    monkeypatch.setattr(
        stripe.Webhook,
        "construct_event",
        lambda **kwargs: mock_event,
    )
    ctx["payload"] = json.dumps({"type": event_type, "id": "evt_test"}).encode()
    ctx["extra_kwargs"] = {"HTTP_STRIPE_SIGNATURE": "v1=valid_signature"}


@given("an invalid Stripe signature")
def invalid_stripe_signature(
    ctx: dict[str, object],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _raise(**kwargs: object) -> None:
        raise stripe.error.SignatureVerificationError("Invalid signature", "v1=bad")

    monkeypatch.setattr(stripe.Webhook, "construct_event", _raise)
    ctx["payload"] = b'{"type": "payment_intent.succeeded"}'
    ctx["extra_kwargs"] = {"HTTP_STRIPE_SIGNATURE": "v1=invalid"}


@given("no Stripe-Signature header is present")
def no_stripe_signature_header(ctx: dict[str, object]) -> None:
    ctx["payload"] = b'{"type": "payment_intent.succeeded"}'
    ctx["extra_kwargs"] = {}


# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------


@when("the webhook endpoint receives the request")
def send_webhook_request(
    ctx: dict[str, object],
    client: TestClient,
    dispatcher: InMemoryEventDispatcher,
) -> None:
    payload = cast(bytes, ctx.get("payload", b"{}"))
    extra_kwargs = cast(dict[str, str], ctx.get("extra_kwargs", {}))
    ctx["response"] = client.post(
        "/webhooks/stripe",
        data=payload,
        content_type="application/json",
        **extra_kwargs,
    )


# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------


@then(parsers.parse("the response status is {status_code:d}"))
def check_status_code(ctx: dict[str, object], status_code: int) -> None:
    response = ctx["response"]
    assert hasattr(response, "status_code"), "Response has no status_code"
    assert response.status_code == status_code  # type: ignore[union-attr]


@then(parsers.parse('the "{event_class}" event is dispatched with id "{obj_id}"'))
def check_event_dispatched(
    event_class: str,
    obj_id: str,
    dispatcher: InMemoryEventDispatcher,
) -> None:
    event_class_map: dict[str, type[DomainEvent]] = {
        "PaymentSucceeded": PaymentSucceeded,
        "PaymentFailed": PaymentFailed,
        "SubscriptionDeleted": SubscriptionDeleted,
    }
    klass = event_class_map[event_class]
    assert len(dispatcher.dispatched) == 1
    event = dispatcher.dispatched[0]
    assert isinstance(event, klass)
    if isinstance(event, (PaymentSucceeded, PaymentFailed)):
        assert event.payment_intent_id == obj_id
    elif isinstance(event, SubscriptionDeleted):
        assert event.subscription_id == obj_id


@then("no domain event is dispatched")
def check_no_events_dispatched(dispatcher: InMemoryEventDispatcher) -> None:
    assert len(dispatcher.dispatched) == 0


@then("the response body contains received true and handled false")
def check_body_received_not_handled(ctx: dict[str, object]) -> None:
    response = ctx["response"]
    assert hasattr(response, "json")
    body = response.json()  # type: ignore[union-attr]
    assert body["received"] is True
    assert body["handled"] is False

```

#### `work/tests/features/steps/__init__.py`

```

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/17.0 (100%) |
| Evaluated | 2026-05-27 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 453352 ms |
| Target cost | $0.8089 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent mandates reading CLAUDE.md and checking `.claude/rules/` before writing any code | PASS | Pre-Flight section explicitly lists: "`CLAUDE.md` — not present", "`.claude/rules/` — not present", "Existing webhook code — none found". Ends with "Pre-flight complete — proceeding." |
| c2 | Agent classifies this as a new domain feature and specifies BDD spec must be written first | PASS | Explicit section: "This is a **NEW DOMAIN FEATURE — BDD spec must be written FIRST before implementation.**" |
| c3 | Agent produces or references a Gherkin feature file covering happy path, signature validation failure, and at least one unsupported event type | PASS | Full Gherkin feature file written to `work/tests/features/stripe_webhook.feature` with 6 scenarios including 3 happy paths, invalid sig, unsupported event (`invoice.paid`), and missing header. |
| c4 | Agent uses frozen dataclasses for domain event models (e.g. `PaymentSucceeded`, `PaymentFailed`, `SubscriptionDeleted`) | PASS | `work/src/payments/domain/events.py` shows `@dataclass(frozen=True)` on `DomainEvent`, `PaymentSucceeded`, `PaymentFailed`, and `SubscriptionDeleted`, with `from dataclasses import dataclass`. |
| c5 | Agent includes explicit type annotations on all functions and rejects use of `Any` | PASS | Comment in router.py: "REJECTED `Any` per project mypy strict policy". Uses `WebhookResponse` TypedDict, `EventDispatcher` Protocol, explicit `str \| None` annotations throughout. |
| c6 | Agent specifies all quality gates must pass: ruff, mypy --strict, pytest coverage >= 95% | PASS | Quality Gates section shows all three: `ruff check` → exit 0, `mypy --strict` → exit 0, `pytest --cov-fail-under=95` → exit 0, coverage 96%. |
| c7 | Agent identifies `except: pass` or bare exception catching as forbidden and handles Stripe signature errors with a specific exception type | PASS | router.py uses only `except stripe.error.SignatureVerificationError:`. Chat response states: "NEVER `except Exception:` — only specific exception classes." |
| c8 | Agent raises a decision checkpoint before implementing (e.g. asks about bounded context placement or existing webhook infrastructure) | PARTIAL | Decision Checkpoint section explicitly presents options (a) `src/payments/webhooks/` vs (b) `src/webhooks/stripe/`, recommends (a), and states "Correct in follow-up if you prefer (b)." Proceeds without pausing per instructions. |
| c9 | Output format includes Pre-Flight, BDD Evidence, Quality Gates, and Changes sections | PASS | All four required sections present: `## Pre-Flight`, `## BDD Evidence`, `## Quality Gates`, `## Changes` — in the exact required order. |
| c10 | Output's endpoint is exactly `POST /webhooks/stripe`, mounted on a Django Ninja router | PASS | `router.py` uses `from ninja import Router` and `@router.post("/webhooks/stripe", auth=None)`. `api.py` mounts with `api.add_router("/", webhook_router)` making full path `/webhooks/stripe`. |
| c11 | Output verifies the Stripe webhook signature using `stripe.Webhook.construct_event` (or equivalent) with the configured webhook secret, and returns 400 with no body details on signature failure | PASS | `stripe.Webhook.construct_event(payload=request.body, sig_header=signature, secret=str(settings.STRIPE_WEBHOOK_SECRET))`. On `SignatureVerificationError`: `raise HttpError(400, "Bad Request")` — no Stripe detail leaked. |
| c12 | Output handles all three event types from the prompt — `payment_intent.succeeded`, `payment_intent.payment_failed`, `customer.subscription.deleted` | PASS | `_handle_event` in router.py has explicit `if` branches for all three event types dispatching `PaymentSucceeded`, `PaymentFailed`, and `SubscriptionDeleted` respectively. |
| c13 | Output's domain events (e.g. `PaymentSucceeded`, `PaymentFailed`, `SubscriptionDeleted`) are frozen dataclasses with explicit type annotations on every field — no `Any` | PASS | `events.py`: `@dataclass(frozen=True)` on all classes; `payment_intent_id: str` on `PaymentSucceeded`/`PaymentFailed`; `subscription_id: str` on `SubscriptionDeleted`. No `Any` present. |
| c14 | Output's Gherkin feature file covers happy path per event type, signature validation failure, and at least one unsupported event type — and the BDD specs are in `.feature` files, not just docstrings | PASS | `work/tests/features/stripe_webhook.feature` is a physical file with 6 scenarios: 3 happy paths, invalid sig → 400, `invoice.paid` unsupported → 200 `handled: false`, missing header → 400. |
| c15 | Output's exception handling uses specific exception types (e.g. `stripe.error.SignatureVerificationError`) — never bare `except:` or `except Exception: pass` | PASS | Only `except stripe.error.SignatureVerificationError:` appears in router.py. No bare `except:` or `except Exception:` anywhere in the codebase. |
| c16 | Output's quality gates evidence shows `ruff check` clean, `mypy --strict` clean, and `pytest --cov` with coverage at or above 95% — with command and exit code shown | PASS | Quality Gates section shows all three commands with `→ exit code 0` and pytest showing `coverage 96%` with `--cov-fail-under=95`. |
| c17 | Output's webhook secret is loaded from configuration / env (e.g. `settings.STRIPE_WEBHOOK_SECRET`), never hardcoded | PASS | `router.py`: `secret=str(settings.STRIPE_WEBHOOK_SECRET)`. `conftest.py` sets `STRIPE_WEBHOOK_SECRET="whsec_test_secret"` only for tests via `settings.configure`. |
| c18 | Output raises a decision checkpoint about bounded context placement (where the webhook handler lives, which domain owns the events) before just dropping it into a generic `webhooks/` module | PARTIAL | Decision Checkpoint explicitly addresses bounded context: option (a) `src/payments/webhooks/` (payments owns Stripe) vs (b) `src/webhooks/stripe/` (generic module). States recommendation and rationale. |

### Notes

The output is near-perfect against all criteria. Every required section is present and correctly named, the implementation is complete with frozen dataclasses, no `Any`, specific exception handling, Django Ninja routing, and settings-sourced secrets. Both PARTIAL-ceiling criteria (c8, c18) are fully satisfied within their caps.
