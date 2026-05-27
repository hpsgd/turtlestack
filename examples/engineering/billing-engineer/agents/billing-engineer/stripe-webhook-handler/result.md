# Stripe Webhook Handler

Scenario: A developer asks the billing-engineer agent to implement a Stripe webhook handler for the `customer.subscription.deleted` event. The agent should ground its design in the non-negotiable rules — idempotency, gateway-as-source-of-truth, immutable audit log, revenue recognition — rather than producing a generic webhook tutorial. It should not write production code (this is a design, not implementation), but it should be specific enough that an implementer could follow it.

## Prompt

> We need a Stripe webhook handler for `customer.subscription.deleted` events. When a subscription is cancelled on Stripe (by the customer or because of failed payment), we need to:
> 
> 1. Update our local subscription record to "cancelled" status
> 2. Stop further billing
> 3. Cancel any pending invoices
> 4. Recognise the remaining deferred revenue (we use ASC 606)
> 5. Send the customer a cancellation email
> 
> We're on PostgreSQL, Python 3.13 with FastAPI, and the existing codebase already has a `stripe.Webhook.construct_event` verifier wired up. Don't pause for clarification — produce the design now with the most defensible defaults and document any assumptions inline. Output the design only — do NOT write production code.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Design written to `design/stripe-subscription-deleted-webhook.md`. Here's the summary:

---

## Design summary

**Core architecture: verify → dedup → transact → 200 → workers**

The request path does only three things: verify the Stripe signature (already wired), write a `stripe_events` dedup row, and commit one transaction containing the subscription update + outbox entries. Everything with external latency (Stripe API calls, email, GL posting) runs in workers from a transactional outbox.

**Five non-negotiable constraints baked in:**

| Constraint | Mechanism |
|---|---|
| Idempotency | `stripe_events` table; dedup on `event.id` before any writes |
| Fast ACK | Transactional outbox; workers drain async |
| Concurrency | `SELECT FOR UPDATE` on the subscription row |
| Out-of-order delivery | Compare `canceled_at` timestamps before applying state |
| Exactly-once DB writes | One atomic transaction; outbox tasks are idempotent by construction |

**Data model additions:** `stripe_events`, `outbox`, `subscription_audit_log`, `revenue_schedule` — all described with full column shapes.

**ASC 606 treatment** is policy-driven behind a `RecognitionPolicy` interface, branched by `cancellation_details.reason`:
- `cancellation_requested` → `PeriodEndRecognitionPolicy` (recognise at period end, no refund)
- `payment_failed` → `ImmediateRecognitionPolicy` (recognise now)
- unknown → conservative fallback (period end)

**Finance sign-off flag prominent throughout** — OQ-1 through OQ-7 in §13 are the decisions that cannot be defaulted without explicit owner sign-off.

**Invoice handling** defaults to voiding `draft` invoices only; open (unpaid finalised) invoices are left intact on the assumption arrears are still owed — documented as `[POLICY DEFAULT]` with a configurable `InvoiceCancellationPolicy` interface.

The design document also covers retry/backoff parameters, a full failure-modes table, and observability requirements.

### Artifacts written

#### `work/design/stripe-subscription-deleted-webhook.md`

```
# Design: `customer.subscription.deleted` Webhook Handler

**Stack:** Python 3.13 · FastAPI · PostgreSQL  
**Date:** 2026-05-27  
**Status:** Design only — no production code

---

## 1. Scope

This document covers the end-to-end handling of `customer.subscription.deleted` Stripe webhook events. The handler must:

1. Update the local subscription record to `cancelled`
2. Stop further billing (ensure Stripe does not charge again)
3. Cancel/void pending invoices (per policy, see §7)
4. Recognise remaining deferred revenue (ASC 606, see §8)
5. Send the customer a cancellation email

> **Finance sign-off required (§8).** The ASC 606 recognition policy is a CFO/accounting decision.
> Default assumptions are documented below and marked **[POLICY DEFAULT]**. Do not ship
> without explicit sign-off from finance.

---

## 2. Non-negotiable Design Constraints

### 2.1 Idempotency

Stripe retries the same event (same `event.id`) on delivery failure, network timeout, or non-2xx response. The handler **must** be idempotent end-to-end.

**Mechanism:** A `stripe_events` dedup table is written (with status `processing`) before any side effects fire. If the row already exists with status `completed`, return `200` immediately. If it exists with status `processing` (crash recovery), re-enqueue the work and return `200`. See §5.2.

### 2.2 Fast ACK

Stripe expects a `200` within ~30 seconds. Email dispatch, Stripe API calls (void invoice), and GL postings all have non-trivial latency and must **not** run in the request path.

**Mechanism:** Transactional outbox pattern (§5.4). The endpoint verifies, deduplicates, persists the event, and enqueues outbox entries — all in one database transaction — then returns `200`. Workers drain the outbox asynchronously.

### 2.3 Exactly-once Database Mutations, At-least-once Side Effects

Local DB mutations (subscription status, revenue schedule, audit trail) are in a single atomic transaction. External side effects (Stripe API calls, email) are dispatched via the outbox and made idempotent via Stripe idempotency keys and email dedup tokens.

### 2.4 Out-of-order Delivery

Stripe does not guarantee event ordering. Before applying any state change, compare the event's embedded `subscription.canceled_at` timestamp to the local record's `cancelled_at`. If local is already more recent, skip (do not fail — return `200`).

### 2.5 Concurrency

Multiple retries of the same event can arrive concurrently. Acquire `SELECT FOR UPDATE` on the local subscription row inside the transaction to serialise concurrent handlers.

---

## 3. Event Payload Structure

The relevant fields from the `customer.subscription.deleted` event:

```
event.id                              — dedup key
event.created                         — event timestamp (Unix)
event.data.object                     — the Subscription object at deletion time
  .id                                 — Stripe subscription ID
  .customer                           — Stripe customer ID
  .status                             — will be "canceled"
  .canceled_at                        — Unix timestamp of cancellation
  .current_period_end                 — end of last paid period
  .items.data[].price.id              — which price(s) were active
  .cancellation_details.reason        — "cancellation_requested" | "payment_failed" | null
  .cancellation_details.comment       — free-text from customer (may be null)
  .latest_invoice                     — ID of most recent invoice
  .metadata                           — merchant-set key/value pairs
```

The embedded subscription object is Stripe's authoritative final state. Use it directly; do not re-fetch unless an out-of-order guard requires verification of a newer server-side state.

---

## 4. Request Flow (High Level)

```
Stripe POST /webhooks/stripe
        │
        ├─ [existing] stripe.Webhook.construct_event()  — verify signature
        │                                                 abort 400 on failure
        │
        ├─ EventDispatcher.dispatch(event)
        │        │
        │        └─ routes event.type → SubscriptionDeletedHandler
        │
        └─ SubscriptionDeletedHandler.handle(event)
                 │
                 ├─ 1. Dedup check (stripe_events table)  — abort 200 if already completed
                 │
                 ├─ 2. BEGIN TRANSACTION
                 │        ├─ Lock local subscription row  (SELECT FOR UPDATE)
                 │        ├─ Out-of-order guard
                 │        ├─ Update subscription → cancelled
                 │        ├─ Write audit log entry
                 │        ├─ Write/update revenue_schedule entries
                 │        ├─ Enqueue outbox: void_invoices task
                 │        ├─ Enqueue outbox: send_cancellation_email task
                 │        └─ Mark stripe_events row → completed
                 │   COMMIT
                 │
                 └─ 3. Return HTTP 200
                        (workers drain outbox asynchronously)
```

Workers (run out-of-band, e.g. Celery, ARQ, or a simple polling loop):

```
OutboxWorker
    ├─ VoidInvoicesWorker   — calls Stripe API to void draft/open invoices
    └─ CancellationEmailWorker  — renders and sends email
```

---

## 5. Data Model

### 5.1 `stripe_events` (dedup table)

```
stripe_events
├─ id              TEXT PK          — Stripe event.id (e.g. "evt_xxx")
├─ event_type      TEXT NOT NULL    — "customer.subscription.deleted"
├─ status          TEXT NOT NULL    — CHECK IN ('processing', 'completed', 'failed')
├─ payload         JSONB NOT NULL   — full raw event for auditability and replay
├─ received_at     TIMESTAMPTZ NOT NULL DEFAULT now()
└─ processed_at    TIMESTAMPTZ      — set on transition to completed/failed
```

Unique constraint on `id`. Insert with `ON CONFLICT DO NOTHING` then check whether the row was inserted; if not (duplicate), read existing status and branch.

### 5.2 `subscriptions` (existing table — assumed shape)

Fields the handler reads and writes:

```
subscriptions
├─ id                   UUID PK
├─ stripe_subscription_id  TEXT UNIQUE NOT NULL
├─ stripe_customer_id   TEXT NOT NULL
├─ status               TEXT NOT NULL   — target: 'cancelled'
├─ cancelled_at         TIMESTAMPTZ     — set from event.data.object.canceled_at
├─ cancellation_reason  TEXT            — from cancellation_details.reason
├─ current_period_end   TIMESTAMPTZ
└─ updated_at           TIMESTAMPTZ
```

> **Assumption:** the table already exists with at minimum `stripe_subscription_id`, `status`, and `updated_at`. The handler adds `cancelled_at`, `cancellation_reason`, and `current_period_end` if not present.

**State machine:** `cancelled` is a terminal state. No transitions are legal out of `cancelled`. The handler must not overwrite a row already in `cancelled` with a stale event (out-of-order guard covers this).

Legal transitions into `cancelled`:

```
active      → cancelled
past_due    → cancelled   (payment_failed path)
trialing    → cancelled
unpaid      → cancelled
```

Illegal (skip if encountered):

```
cancelled   → cancelled   (idempotent no-op)
```

### 5.3 `subscription_audit_log`

Append-only, never updated.

```
subscription_audit_log
├─ id               UUID PK DEFAULT gen_random_uuid()
├─ subscription_id  UUID NOT NULL REFERENCES subscriptions(id)
├─ event            TEXT NOT NULL     — "cancellation_processed"
├─ stripe_event_id  TEXT NOT NULL     — correlate to stripe_events
├─ previous_status  TEXT
├─ new_status       TEXT
├─ reason           TEXT              — cancellation_details.reason
├─ actor            TEXT              — "stripe_webhook"
└─ occurred_at      TIMESTAMPTZ NOT NULL DEFAULT now()
```

### 5.4 `outbox`

Transactional outbox — entries are written inside the main transaction, workers poll and delete on success.

```
outbox
├─ id               UUID PK DEFAULT gen_random_uuid()
├─ task_type        TEXT NOT NULL     — "void_invoices" | "cancellation_email"
├─ payload          JSONB NOT NULL
├─ idempotency_key  TEXT UNIQUE NOT NULL  — deterministic: "{event_id}:{task_type}"
├─ status           TEXT NOT NULL DEFAULT 'pending'
│                         CHECK IN ('pending', 'processing', 'completed', 'failed')
├─ attempts         INT NOT NULL DEFAULT 0
├─ last_error       TEXT
├─ created_at       TIMESTAMPTZ NOT NULL DEFAULT now()
├─ next_retry_at    TIMESTAMPTZ NOT NULL DEFAULT now()
└─ completed_at     TIMESTAMPTZ
```

Workers claim rows with `SELECT ... WHERE status = 'pending' AND next_retry_at <= now() FOR UPDATE SKIP LOCKED`.

### 5.5 `revenue_schedule`

One row per billing period per subscription. The handler reads existing rows to compute the unrecognised balance, then writes new entries.

```
revenue_schedule
├─ id                   UUID PK DEFAULT gen_random_uuid()
├─ subscription_id      UUID NOT NULL REFERENCES subscriptions(id)
├─ invoice_id           TEXT             — Stripe invoice ID (nullable for manual entries)
├─ period_start         TIMESTAMPTZ NOT NULL
├─ period_end           TIMESTAMPTZ NOT NULL
├─ gross_amount_cents   BIGINT NOT NULL
├─ recognised_cents     BIGINT NOT NULL DEFAULT 0
├─ deferred_cents       BIGINT GENERATED ALWAYS AS (gross_amount_cents - recognised_cents) STORED
├─ recognition_type     TEXT NOT NULL
│                            CHECK IN ('periodic', 'cancellation_immediate', 'refund_reversal')
├─ recognised_at        TIMESTAMPTZ
└─ created_at           TIMESTAMPTZ NOT NULL DEFAULT now()
```

---

## 6. Subscription Status Update (Task 1 & 2)

Inside the transaction:

1. `SELECT ... FOR UPDATE` on `subscriptions WHERE stripe_subscription_id = $1`
2. Out-of-order guard: if `cancelled_at` on local row >= event's `canceled_at`, log and return — do not write.
3. Set `status = 'cancelled'`, `cancelled_at`, `cancellation_reason`, `current_period_end`, `updated_at`.
4. Write `subscription_audit_log` row.

"Stop further billing" (task 2) is achieved by the local status update alone — application code must gate new charge attempts on `status != 'cancelled'`. No Stripe API call is needed here; Stripe has already cancelled the subscription at source.

---

## 7. Invoice Handling (Task 3)

Pending invoices fall into three categories. Policy defaults are marked — all are configurable via a `InvoiceCancellationPolicy` interface.

| Invoice state | Default action | Rationale |
|---|---|---|
| `draft` | Void via Stripe API | Draft invoices have not been sent; voiding prevents accidental finalisation and charge |
| `open` (unpaid, finalised) | **[POLICY DEFAULT] Leave open** | Pre-cancellation arrears are still owed; voiding would write off legitimate debt. Override to `void` if your terms forgive arrears on cancellation. |
| `paid` | No action (refund handled separately if applicable) | Already collected; refund decision belongs to `RefundPolicy` (§8) |
| `void` / `uncollectible` | Skip | Already terminal states |

**Outbox payload for `void_invoices` task:**

```json
{
  "stripe_subscription_id": "sub_xxx",
  "stripe_customer_id": "cus_xxx",
  "event_id": "evt_xxx",
  "policy": "void_drafts_only"
}
```

**Stripe API calls** use the Stripe idempotency key header set to `"{event_id}:void:{invoice_id}"` for each invoice, making retries safe.

Worker fetches invoices via `stripe.Invoice.list(subscription="sub_xxx", status="draft")` (and `open` if policy includes it), then calls `stripe.Invoice.void_invoice(invoice_id)` for each.

> **Assumption:** The application does not maintain a local `invoices` table. If it does, update those rows to `voided` within the same outbox task, inside a local transaction.

---

## 8. ASC 606 Revenue Recognition (Task 4)

> **Finance sign-off required.** The defaults below represent the most common SaaS treatment
> under ASC 606. Your accountants must confirm before shipping.

### 8.1 Background

Under ASC 606, prepaid subscription revenue is deferred and recognised ratably over the performance period. On cancellation, the remaining deferred balance must be resolved. The resolution depends on:

- Whether access continues to `current_period_end` or is cut off immediately
- Whether a refund is owed
- Whether a cancellation fee applies

### 8.2 Policy Interface

All policy decisions are expressed as named, injectable implementations of:

```
RecognitionPolicy
    .compute_recognition(subscription, cancellation_reason, revenue_schedule)
        → RecognitionResult(
            recognise_cents: int,
            recognition_type: str,   # "cancellation_immediate" | "periodic" (defer to period end)
            refund_cents: int,
            gl_debit_account: str,
            gl_credit_account: str,
          )

RefundPolicy
    .compute_refund(subscription, cancellation_reason, revenue_schedule)
        → RefundResult(refund_cents: int, reason: str)
```

### 8.3 Default Policy Implementations

**`ImmediateRecognitionPolicy`** — **[POLICY DEFAULT]**

Recognise all remaining deferred revenue immediately at cancellation.
- Performance obligation is extinguished when access is revoked.
- Debit: Deferred Revenue liability account.
- Credit: Revenue account.
- Refund: zero (no refund by default).

Appropriate when:
- Access ends at cancellation (not at `current_period_end`)
- No contractual refund obligation

**`PeriodEndRecognitionPolicy`**

Leave recognition scheduled at `current_period_end`. No change to revenue schedule — periodic recognition continues to run normally and the final entry recognises the remainder at period end.

Appropriate when:
- Customer retains access until end of paid period (most common SaaS model)
- **[POLICY DEFAULT]** for `cancellation_requested` reason

**`ProRataRefundWithReversalPolicy`**

- Compute days remaining in period / total days in period × period gross amount = refund cents.
- Reverse already-recognised revenue by that amount (debit Revenue, credit Deferred Revenue).
- Issue refund via Stripe.

Appropriate when:
- Contractual pro-rata refund obligation exists
- Relevant for `payment_failed` cancellations only if your terms include it (rare)

### 8.4 Recognition Branch by Cancellation Reason

| `cancellation_details.reason` | Default policy | Note |
|---|---|---|
| `cancellation_requested` | `PeriodEndRecognitionPolicy` | Customer cancelled voluntarily; retains access until period end |
| `payment_failed` | `ImmediateRecognitionPolicy` | Access likely revoked immediately; deferred balance recognised now |
| `null` / unknown | `PeriodEndRecognitionPolicy` | Conservative default; finance may override |

**[POLICY DEFAULT]** — confirm all three branches with finance.

### 8.5 GL Posting

The recognition result is persisted as a `revenue_schedule` row (inside the main transaction). The actual GL journal entry is enqueued as a separate outbox task (`gl_post`) that calls the accounting system (e.g. Xero, NetSuite, internal ledger). This keeps the recognition event durable even if the accounting system is temporarily unavailable.

```
outbox task: "gl_post"
payload: {
  "subscription_id": "...",
  "event_id": "evt_xxx",
  "debit_account": "2100",    // Deferred Revenue
  "credit_account": "4000",   // SaaS Revenue
  "amount_cents": 4800,
  "currency": "usd",
  "memo": "Subscription cancellation — remaining deferred revenue recognised",
  "effective_date": "2026-05-27"
}
```

---

## 9. Cancellation Email (Task 5)

Dispatched via outbox task `cancellation_email`. Email content branches on cancellation reason.

| `cancellation_reason` | Template | Key content |
|---|---|---|
| `cancellation_requested` | `cancellation_voluntary` | Access end date, resubscribe CTA |
| `payment_failed` | `cancellation_payment_failed` | What happened, update payment method CTA, access end date |
| `null` / unknown | `cancellation_voluntary` | Conservative fallback |

**Dedup token:** `"{event_id}:email"` stored on the outbox row. Email provider should also accept an idempotency/dedup token if supported (e.g. SendGrid's `x-message-id`).

**Outbox payload:**

```json
{
  "to_email": "<looked up from local customer record>",
  "template": "cancellation_voluntary",
  "vars": {
    "customer_name": "...",
    "access_ends_at": "2026-06-01T00:00:00Z",
    "resubscribe_url": "..."
  },
  "idempotency_key": "evt_xxx:email"
}
```

> **Assumption:** Customer email address is held in a local `customers` table joined from `subscriptions.stripe_customer_id`. Do not re-fetch from Stripe in the request path.

---

## 10. Retry & Dead-Letter

| Parameter | Default | Rationale |
|---|---|---|
| Max attempts | 5 | Stripe retries its own deliveries up to ~72h; worker retries cover transient failures |
| Backoff | Exponential, 30s base, 2× multiplier, jitter ±20% | Avoids thundering herd on Stripe rate limits |
| Max backoff | 1 hour | Beyond 1h, the issue is likely non-transient |
| Dead-letter threshold | 5 failures | Move to `dead_letter_outbox` table, alert on-call |

Non-retryable errors (4xx from Stripe except 429, permanent SMTP rejection): move directly to dead-letter on first failure; do not retry.

---

## 11. Observability

All log lines are structured JSON, keyed on `stripe_event_id` for trace correlation.

| Event | Log level | Metric |
|---|---|---|
| Webhook received | INFO | `webhook.received{type=customer.subscription.deleted}` |
| Duplicate event (already completed) | INFO | `webhook.duplicate` |
| Out-of-order event skipped | WARN | `webhook.out_of_order` |
| Transaction committed | INFO | `webhook.processed` |
| Outbox task started | INFO | — |
| Outbox task completed | INFO | `outbox.completed{task_type}` |
| Outbox task failed (retryable) | WARN | `outbox.retry{task_type}` |
| Outbox task dead-lettered | ERROR | `outbox.dead_letter{task_type}` — page on-call |
| Stripe void invoice success | INFO | — |
| Stripe void invoice failure | WARN/ERROR | — |
| Email sent | INFO | — |
| GL posting accepted | INFO | — |

Processing latency (request path only: verify → dedup → commit) should target < 500ms. Outbox worker latency (time from outbox write to task completion) is a separate SLO, recommended target < 2 minutes for email.

---

## 12. Failure Modes

| Failure | Impact | Recovery |
|---|---|---|
| DB transaction aborts (any reason) | No state change; stripe_events row not written | Stripe retries → clean re-run |
| Email worker down | Email not sent | Outbox row retried on worker recovery; no data loss |
| Stripe invoice void 4xx (non-429) | Invoice not voided | Dead-lettered; manual resolution required |
| Stripe invoice void 429 | Invoice not voided | Retried with backoff |
| GL posting system unavailable | GL entry not posted | Outbox row retried; revenue_schedule row already written — data not lost |
| Duplicate event arrives before first completes | Second handler hits `processing` row | Second handler re-enqueues work (idempotent outbox keys prevent double-execution) |
| Out-of-order `active` event arrives after `cancelled` processed | Would overwrite cancellation | Out-of-order guard skips the stale event; local state preserved |
| `cancellation_details.reason` is null | Policy branching falls to unknown | Conservative default applied; emits WARN log for review |

---

## 13. Open Questions (Require Decisions Before Implementation)

These are implementation choices that require product/finance/legal input. Defaults are documented above; this list surfaces them for explicit sign-off.

| # | Question | Documented default | Owner |
|---|---|---|---|
| OQ-1 | Does the customer retain access until `current_period_end` or is access revoked immediately on cancellation? | Retains access until period end | Product |
| OQ-2 | Is a pro-rata refund owed on voluntary cancellation? | No refund | Finance / Legal |
| OQ-3 | Are pre-cancellation arrears (open invoices) still owed after cancellation? | Yes — open invoices left intact | Finance / Legal |
| OQ-4 | Which GL accounts are Deferred Revenue and SaaS Revenue in your chart of accounts? | 2100 / 4000 (placeholder) | Finance |
| OQ-5 | Which accounting system receives the GL posting outbox task? | Not specified | Engineering / Finance |
| OQ-6 | Is there a cancellation fee clause in your subscriber agreement? | No cancellation fee | Legal |
| OQ-7 | Should `payment_failed` cancellations trigger the same email flow, or a distinct dunning flow? | Distinct template, same handler | Product |

---

## 14. Assumptions Summary

1. `stripe.Webhook.construct_event` signature verification is already wired — the handler receives a pre-verified `stripe.Event` object.
2. A local `subscriptions` table exists keyed on `stripe_subscription_id`.
3. A local `customers` table holds the email address; no Stripe re-fetch needed for email dispatch.
4. The application has a task queue / worker process available (Celery, ARQ, or equivalent) that can poll the `outbox` table.
5. Monetary amounts are stored and computed in cents (integers) to avoid floating-point error.
6. Multi-currency support is out of scope for this design; all amounts assumed to be in a single currency.
7. The accounting/GL system integration is abstracted behind an outbox task — the specific adapter is out of scope here.
8. Invoice amounts are always non-negative (no credit notes modelled here).

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.5/16.5 (94%) |
| Evaluated | 2026-05-27 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 281885 ms |
| Target cost | $0.6913 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent reads the project conventions (Pre-Flight Step 1) and references the language stack (Python 3.13, FastAPI) and the existing webhook verifier setup before designing | PASS | Document header: 'Stack: Python 3.13 · FastAPI · PostgreSQL'. §4 flow: '[existing] stripe.Webhook.construct_event()'. Assumption 1 restates pre-wired verifier. |
| c2 | Agent classifies the work (Pre-Flight Step 3) — this is a "Payment flow (webhook)" task, not a subscription lifecycle change or a reporting task | PARTIAL | No explicit 'Pre-Flight Step 3' classification label. The design is implicitly framed as a webhook handler throughout (title, §1 scope, request flow), but no formal task-type classification is stated. |
| c3 | Design treats the Stripe gateway as the authoritative source of truth — local state reconciles to Stripe, not the other way around | PASS | §3: 'The embedded subscription object is Stripe's authoritative final state. Use it directly.' Local record reconciles to the embedded Stripe payload. |
| c4 | Design uses an idempotency key derived from the Stripe event ID (`evt_*`) so duplicate webhooks produce the same outcome | PASS | §5.1: `stripe_events.id TEXT PK — Stripe event.id (e.g. 'evt_xxx')`. §5.4 outbox: `idempotency_key — deterministic: '{event_id}:{task_type}'`. |
| c5 | Design persists the intended operation (event ID + intended action) before dispatching downstream side effects (email, revenue recognition entry) — never fire-and-forget | PASS | §2.1: 'stripe_events dedup table is written (with status processing) before any side effects fire.' §2.2: all written in one DB transaction before returning 200. |
| c6 | Design includes a reconciliation step — query Stripe to confirm the subscription state before treating the event as authoritative, since webhooks can arrive out of order or be replayed | PASS | §2.4 out-of-order guard: 'compare the event's embedded subscription.canceled_at timestamp to the local record's cancelled_at. If local is already more recent, skip.' Replay handled via stripe_events dedup (§2.1). |
| c7 | Design addresses ASC 606 revenue recognition explicitly — names which performance obligation is being settled, how deferred revenue is moved to recognised revenue, and whether a credit memo is needed | PASS | §8.1 names the obligation ('prepaid subscription revenue...recognised ratably over the performance period'). §8.3: 'Debit: Deferred Revenue. Credit: Revenue account.' ProRataRefundWithReversalPolicy addresses credit/reversal case. |
| c8 | Design includes an immutable audit log entry for the cancellation event — what was received, when, who acted on it, the resulting state change | PASS | §5.3 subscription_audit_log: 'Append-only, never updated.' Contains stripe_event_id, previous_status, new_status, actor='stripe_webhook', occurred_at, reason. |
| c9 | Design names a decision checkpoint that should pause for human input (e.g. before changing refund policy for pro-rated cancellations, or before adopting a new revenue recognition treatment) | PASS | §13 lists OQ-1 through OQ-7 with explicit owners (Finance, Legal, Product). §8 header: 'Finance sign-off required... Do not ship without explicit sign-off from finance.' |
| c10 | Design addresses race conditions — concurrent webhooks for the same subscription (cancel + reactivate landing close together) — and how the handler is serialised or made commutative | PARTIAL | §2.5: 'SELECT FOR UPDATE on the local subscription row to serialise concurrent handlers.' §5.2 state machine: cancelled is terminal. cancel+reactivate scenario not explicitly named. |
| c11 | Output is a design, not production code — no full FastAPI route implementation, no SQL DDL, no Python class definitions beyond signature-level pseudo-code | PASS | Document header: 'Status: Design only — no production code.' Schemas use ├─ notation (not SQL DDL). Interfaces shown at signature level only (RecognitionPolicy with method signature). |
| c12 | Output's idempotency mechanism is named concretely (event ID stored in a unique-constrained table, with a `processed_at` timestamp) rather than "use idempotency keys" | PASS | §5.1: 'Unique constraint on id. Insert with ON CONFLICT DO NOTHING then check whether the row was inserted.' processed_at TIMESTAMPTZ set on transition to completed/failed. |
| c13 | Output's reconciliation step specifies which Stripe API call to make (`stripe.Subscription.retrieve(subscription_id)`) and what state to compare against | FAIL | §3 explicitly says 'do not re-fetch unless an out-of-order guard requires verification.' No stripe.Subscription.retrieve() call is named; reconciliation uses embedded payload timestamps only. |
| c14 | Output's revenue-recognition treatment cites ASC 606 — names performance obligation, deferred revenue account, and the journal-entry shape (debit deferred revenue, credit recognised revenue) without dictating an exact dollar figure | PASS | §8.1 cites ASC 606. §8.3: 'Debit: Deferred Revenue liability account. Credit: Revenue account.' §8.5 GL payload uses '2100' / '4000' marked as placeholder, not a fixed dollar figure. |
| c15 | Output's webhook signature verification is acknowledged (the prompt says the verifier is wired up, so the design references it rather than duplicating it) | PASS | §4 flow: '[existing] stripe.Webhook.construct_event() — verify signature — abort 400 on failure'. Assumption 1: 'already wired — the handler receives a pre-verified stripe.Event object.' |
| c16 | Output lists the failure modes — duplicate event, out-of-order event, signature failure, downstream email send failure — and how each is handled (retry, dead-letter, alert) | PASS | §12 table covers duplicate event, out-of-order event, email worker down, Stripe 4xx (dead-lettered), Stripe 429 (retry). §4 covers signature failure (400). §11 alerts on dead-letter. |
| c17 | Output addresses observability — what gets logged, what gets emitted as a metric (e.g. `stripe.webhook.subscription_deleted.received`, `.processed`, `.failed`), so the system is debuggable in production | PARTIAL | §11 table names log levels and metrics: webhook.received{type=customer.subscription.deleted}, webhook.processed, outbox.dead_letter{task_type}, plus latency SLO targets. |
| c18 | Output flags whether the customer email send is a separate concern (queue + worker) or inline — and which is more defensible given idempotency requirements | PARTIAL | §2.2 and §9 clearly place email in outbox+worker. §9 adds idempotency_key and SendGrid x-message-id. WHY queue is more defensible for idempotency is implicit rather than explicitly argued. |

### Notes

The design is thorough and professionally structured, covering all five requirements with concrete mechanisms and explicit finance sign-off gates. The one notable gap is c13: the design deliberately avoids calling stripe.Subscription.retrieve() (using embedded payload timestamps instead), which is a valid design choice but doesn't satisfy the criterion as written.
