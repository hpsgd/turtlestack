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

Good — clean workspace, pure design. Now I'll write the design document.

---

# Stripe `customer.subscription.deleted` Webhook Handler — Design

## Overview

This handler processes Stripe's `customer.subscription.deleted` event through a cascading, event-sourced pipeline. Each step is a separate, idempotent handler that emits the next command. A failure at any step retries from that step only — no prior step needs compensation.

The five requirements map to four cascade handlers:

| Step | Requirement | Handler |
|---|---|---|
| 1 | Update subscription to "cancelled" | `HandleSubscriptionCancellation` |
| 2 | Stop further billing | implicit — Stripe already deleted the subscription; handler marks local record |
| 3 | Cancel pending invoices | `VoidPendingInvoices` |
| 4 | Recognise deferred revenue (ASC 606) | `RecogniseDeferredRevenue` |
| 5 | Send cancellation email | `SendCancellationEmail` |

"Stop further billing" (requirement 2) requires no outbound call: the subscription is already deleted on Stripe's side. The local status update in step 1 is what prevents any retry or re-enqueue of billing logic on our side.

---

## 1. Ingress flow

```
POST /webhooks/stripe
  ↓
construct_event() — already wired, verifies Stripe-Signature header
  ↓
Dedup check: INSERT INTO stripe_webhook_events (event_id) ON CONFLICT DO NOTHING
  → rows_affected == 0 → return HTTP 200 immediately (duplicate delivery)
  ↓
Persist raw event payload to stripe_webhook_events (event_id, type, payload, received_at)
  ↓
Publish SubscriptionCancellationTriggered command onto message bus
  ↓
Return HTTP 200
```

**Assumption A1:** All processing is async after the 200 return. The endpoint must complete in well under Stripe's 30-second timeout. Raw persistence + command publish is the only synchronous work.

**Assumption A2:** `stripe_webhook_events.event_id` has a unique constraint. This is the outer idempotency guard. The aggregate-level guard (§5) handles re-delivery after partial processing.

---

## 2. Domain events lifecycle

The cancellation process follows the `ProcessStarted → Checkpoint → ProcessCompleted` lifecycle from the ES conventions:

```
SubscriptionCancellationStarted          ← outer start
  SubscriptionStatusUpdated              ← step 1 complete
  InvoiceVoidingStarted
    StripeInvoiceVoidInvoked             ← outbound: one per invoice
    StripeInvoiceVoidReplied             ← inbound: result per invoice
  InvoiceVoidingCompleted               ← step 3 complete
  RevenueRecognitionStarted
    DeferredRevenueRecognised            ← OR →
    RevenueRecognitionSkipped            ← if no balance to recognise
  RevenueRecognitionCompleted           ← step 4 complete
  CancellationEmailInvoked              ← outbound: email send
  CancellationEmailReplied              ← inbound: provider ack
SubscriptionCancellationCompleted        ← outer complete
```

Each `Invoked`/`Replied` pair wraps exactly one outbound side-effecting call, per the event semantics rule (`Invoked` = outgoing request, `Replied` = incoming response).

---

## 3. Aggregate model

All state is reconstructed from event history. Frozen dataclasses throughout.

### `SubscriptionAggregate`

| Field | Type | Source |
|---|---|---|
| `subscription_id` | `str` | Stripe `sub_*` ID |
| `customer_id` | `str` | Stripe `cus_*` ID |
| `status` | `SubscriptionStatus` | enum: `active \| past_due \| cancellation_in_progress \| cancelled` |
| `billing_scheme` | `BillingScheme` | enum: `monthly \| annual \| custom` |
| `current_period_start` | `datetime` | from Stripe event payload |
| `current_period_end` | `datetime` | from Stripe event payload |
| `cancelled_at` | `datetime \| None` | populated by `SubscriptionStatusUpdated` event |
| `cancellation_reason` | `CancellationReason \| None` | enum: `customer_requested \| payment_failed \| admin` |
| `cancel_at_period_end` | `bool` | from Stripe event payload |
| `cancellation_process_id` | `str \| None` | FK to the cancellation process aggregate |

### `InvoiceAggregate`

| Field | Type | Notes |
|---|---|---|
| `invoice_id` | `str` | Stripe `in_*` ID |
| `subscription_id` | `str` | — |
| `status` | `InvoiceStatus` | enum: `draft \| open \| paid \| void \| uncollectible` |
| `amount_cents` | `int` | — |
| `billing_period_start` | `datetime` | — |
| `billing_period_end` | `datetime` | — |
| `is_past_due` | `bool` | derived: `status == open AND due_date < now` |

### `RevenueScheduleAggregate`

Tracks the deferred revenue waterfall for a subscription. One aggregate per subscription billing period (or per payment for annual prepay).

| Field | Type | Notes |
|---|---|---|
| `schedule_id` | `str` | `{subscription_id}:{period_start}` |
| `subscription_id` | `str` | — |
| `payment_amount_cents` | `int` | what the customer paid |
| `period_start` | `datetime` | — |
| `period_end` | `datetime` | — |
| `recognized_cents` | `int` | cumulative to date |
| `deferred_cents` | `int` | `payment_amount_cents - recognized_cents` |
| `recognition_entries` | `list[RecognitionEntry]` | dated journal lines |

`RecognitionEntry` = `(date, amount_cents, reason)` where `reason` is `ratable | breakage | skip`.

---

## 4. Cascade handlers

### Handler 1 — `HandleSubscriptionCancellation`

**Triggered by:** `SubscriptionCancellationTriggered` command (published by webhook ingress)

**Idempotency guard:**

```python
# per ES idempotency-guard-on-creation-handler rule
try:
    repo.get(cancellation_process_id)
    return  # already started, skip
except AggregateNotFound:
    pass
```

**Actions:**

1. Emit `SubscriptionCancellationStarted` on the cancellation process aggregate
2. Load `SubscriptionAggregate`; if already `cancelled`, emit `SubscriptionCancellationCompleted` and return (idempotent short-circuit)
3. Emit `SubscriptionStatusUpdated(status=cancellation_in_progress, cancelled_at=event.cancelled_at, reason=derived_from_cancellation_details)`
4. Publish `VoidPendingInvoices` command

**Cancellation reason derivation** (from Stripe `cancellation_details.reason` field):

| Stripe value | Our enum |
|---|---|
| `cancellation_requested` | `customer_requested` |
| `payment_failed` | `payment_failed` |
| `null` / `fraudulent` | `admin` |

---

### Handler 2 — `VoidPendingInvoices`

**Triggered by:** `VoidPendingInvoices` command

**Idempotency guard:** Check `InvoiceVoidingStarted` event on the process aggregate. If present, skip re-querying Stripe and proceed with any un-replied void attempts.

**Actions:**

1. Emit `InvoiceVoidingStarted`
2. Fetch invoices for this subscription from Stripe (filter: `status in [draft, open]`)
3. For each invoice, classify:
   - **Void candidate:** `draft`, or `open` with `billing_period_start > cancelled_at` (future period, not yet due)
   - **Leave open:** `open` with `due_date <= now` — this is a past-due invoice from a failed-payment cycle. **Assumption A3:** We still want to collect past-due amounts; voiding them would write off collectible revenue. Leave these for the dunning/collections flow.
4. For each void candidate:
   - Emit `StripeInvoiceVoidInvoked(invoice_id, idempotency_key=f"void_{event_id}_{invoice_id}")`
   - Call `stripe.Invoice.void_invoice(invoice_id, idempotency_key=...)`
   - Emit `StripeInvoiceVoidReplied(invoice_id, result_status, response_time_ms)`
5. Emit `InvoiceVoidingCompleted(voided_count, skipped_past_due_count)`
6. Publish `RecogniseDeferredRevenue` command

**On Stripe API failure:** The `StripeInvoiceVoidInvoked` event is already persisted. On retry, the handler checks which invoices have a matching `StripeInvoiceVoidReplied` and skips those. It re-sends the Stripe call with the same idempotency key for un-replied ones — Stripe returns the prior result idempotently.

---

### Handler 3 — `RecogniseDeferredRevenue`

**Triggered by:** `RecogniseDeferredRevenue` command

**Idempotency guard:** Check `RevenueRecognitionStarted` event. If present, skip.

**Actions:**

1. Emit `RevenueRecognitionStarted`
2. Apply the ASC 606 decision tree (§6)
3. Emit either `DeferredRevenueRecognised` or `RevenueRecognitionSkipped` with reason
4. Emit `RevenueRecognitionCompleted`
5. Publish `SendCancellationEmail` command

---

### Handler 4 — `SendCancellationEmail`

**Triggered by:** `SendCancellationEmail` command

**Idempotency guard:** Check `CancellationEmailInvoked` event. If present and `CancellationEmailReplied` follows, skip. If `Invoked` exists but no `Replied`, re-send with the same idempotency key.

**Actions:**

1. Emit `CancellationEmailInvoked(to=customer_email, idempotency_key=f"{subscription_id}:cancellation:{cancelled_at_iso}")`
2. Call email provider with idempotency key
3. Emit `CancellationEmailReplied(provider_message_id, delivery_status)`
4. Emit `SubscriptionCancellationCompleted`

**Email failure policy — Assumption A4:** Email is non-critical path. Retry up to 3 times with exponential backoff. After 3 failures, emit `CancellationEmailFailed` with alert metadata and still emit `SubscriptionCancellationCompleted`. The subscription cancellation is complete regardless of email delivery. A separate alerting handler monitors for `CancellationEmailFailed` events.

---

## 5. Idempotency — three levels

| Level | Mechanism | Scope |
|---|---|---|
| Webhook dedup | `stripe_webhook_events.event_id` UNIQUE + `ON CONFLICT DO NOTHING` | Outer gate; handles Stripe re-delivery |
| Aggregate version | ES idempotency guard (`try: get; return except AggregateNotFound: pass`) per handler | Per-process-aggregate step |
| Side-effect dedup | Stripe `Idempotency-Key` header; email provider idempotency key derived from `{subscription_id}:{action}:{timestamp}` | Per outbound call |

---

## 6. ASC 606 deferred revenue decision tree

**Background:** Revenue is recognised when performance obligations are satisfied (ASC 606-10-25). For SaaS, the performance obligation is continuous access to the service. Prepaid amounts sit in deferred revenue until earned ratabaly. On cancellation, treatment depends on refund policy and when the cancellation takes effect.

```
Is billing_scheme == monthly (in-arrears)?
  → No prepaid balance exists by definition
  → Emit RevenueRecognitionSkipped(reason="monthly_billing_no_deferred_balance")
  → DONE

Is cancel_at_period_end == True?
  → Subscription ran to period end; service fully delivered; all revenue already recognised ratably
  → Emit RevenueRecognitionSkipped(reason="cancelled_at_period_end_fully_earned")
  → DONE

Is cancelled_at >= current_period_end?
  → Same as above — no unearned days
  → Emit RevenueRecognitionSkipped(reason="no_unearned_days")
  → DONE

Was a refund issued on the originating charge?
  (check: stripe.Charge.retrieve(charge_id).refunds.data is non-empty)
  → YES: Emit ManualRevenueReviewRequired(subscription_id, refund_amount_cents)
       → HALT automatic recognition. Flag for finance team.
       → Assumption A5: Refund-offset recognition requires human review because the
         deferred balance must be reduced by the refund amount before recognising
         breakage, and the netting treatment varies by jurisdiction.
  → NO: continue ↓

Calculate unearned balance:
  days_remaining  = (current_period_end - cancelled_at).days
  days_in_period  = (current_period_end - current_period_start).days
  deferred_to_recognise_cents = round(payment_amount_cents * days_remaining / days_in_period)

  # Assumption A6: No-refund policy means the remaining obligation is extinguished
  # at cancellation. Per ASC 606-10-55-49 (breakage), deferred balance is recognised
  # as revenue when the customer forfeits the remaining service entitlement.

  Journal entry:
    DR  Deferred Revenue          deferred_to_recognise_cents
    CR  Subscription Revenue      deferred_to_recognise_cents

  Emit DeferredRevenueRecognised(
    subscription_id,
    days_remaining,
    days_in_period,
    recognised_cents=deferred_to_recognise_cents,
    recognition_basis="breakage_no_refund_obligation"
  )
```

**Assumption A7:** The `RevenueScheduleAggregate` for this subscription already has a record of `payment_amount_cents` and `period_start/end`, populated when the original payment was processed. This handler reads from that aggregate; it does not re-derive amounts from Stripe.

---

## 7. Out-of-order event handling

Stripe does not guarantee event ordering. Possible races:

| Race | Handling |
|---|---|
| `invoice.payment_failed` arrives after `subscription.deleted` | Invoice aggregate processes independently. No dependency on subscription status for invoice updates. |
| `customer.subscription.updated` arrives after `subscription.deleted` | Subscription aggregate checks terminal state. If `status == cancelled`, update events are ignored. |
| Duplicate `subscription.deleted` for same subscription | Webhook dedup (level 1) catches exact duplicates. Aggregate idempotency guard (level 2) catches re-processed events with different `event_id` (e.g., test vs. live mode mixup). |
| `subscription.deleted` arrives before related invoices are fetched | Handler 2 fetches live from Stripe at execution time, not from cached state. Race window is narrow. |

The subscription aggregate's state machine enforces valid transitions only:

```
active → cancellation_in_progress → cancelled
past_due → cancellation_in_progress → cancelled
```

Any event attempting to move from `cancelled` to another state is rejected and logged.

---

## 8. Observability

Every outbound call emits a paired `Invoked`/`Replied` event on the process aggregate's stream. This gives a complete, queryable trace of what happened and when.

Additional projection: a `SubscriptionCancellationSummaryProjection` (inline, synchronous) builds a read model keyed by `subscription_id` with:

- `cancellation_process_id`
- `cancelled_at`
- `invoices_voided_count`
- `past_due_invoices_skipped_count`
- `revenue_recognised_cents`
- `email_delivered`
- `completed_at`

This projection is the dashboard-visible record of each cancellation. Disposable — can be rebuilt from events.

---

## 9. Assumptions summary

| ID | Assumption | Impact if wrong |
|---|---|---|
| A1 | All processing is async after HTTP 200 return | If processing must be synchronous, the handler needs to complete within 30s — likely too slow for multi-step cascade |
| A2 | `stripe_webhook_events.event_id` unique constraint exists | Without it, duplicate deliveries run the full pipeline multiple times |
| A3 | Past-due open invoices from failed-payment cancellations are left open for collection | If the business policy is to write them off, Handler 2 voids all open invoices regardless of due date |
| A4 | Email failure is non-critical; cancellation completes without email ack | If email confirmation is legally required (e.g., consumer protection regulation), email failure must block `SubscriptionCancellationCompleted` |
| A5 | Refund-offset ASC 606 recognition requires manual finance review | If refunds are rare or absent, this path never fires; if common, the manual review creates operational load |
| A6 | No-refund policy: cancelled mid-period, no refund issued, remaining deferred balance recognised as breakage revenue immediately | If refunds are possible, the recognition must be offset by refund amount (separate flow, out of scope here) |
| A7 | `RevenueScheduleAggregate` is populated at payment time, not at cancellation time | If not built yet, Handler 3 must derive amounts from Stripe charge history — increases Stripe API calls and failure surface |

**Deferred scope (not designed here):**

- Refund flow — requires its own `RefundProcessed` event chain and revenue reversal
- Reactivation after cancellation — new subscription, new aggregate, no state reuse
- Prorated credit handling for mid-period cancellations with credit notes
- Dunning state machine — upstream of this handler

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.0/16.5 (85%) |
| Evaluated | 2026-05-12 |
| Target duration | 229864 ms |
| Target cost | $0.7727 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent reads the project conventions (Pre-Flight Step 1) and references the language stack (Python 3.13, FastAPI) and the existing webhook verifier setup before designing | PASS | Ingress flow: 'construct_event() — already wired, verifies Stripe-Signature header'; frozen dataclasses and Python-style pseudo-code used throughout; async HTTP 200 pattern matches FastAPI idioms. |
| c2 | Agent classifies the work (Pre-Flight Step 3) — this is a "Payment flow (webhook)" task, not a subscription lifecycle change or a reporting task | FAIL | Output opens with 'Good — clean workspace, pure design. Now I'll write the design document.' No explicit classification step naming this as a payment flow / webhook task. |
| c3 | Design treats the Stripe gateway as the authoritative source of truth — local state reconciles to Stripe, not the other way around | PASS | Handler 2 'Fetch invoices for this subscription from Stripe'; 'subscription is already deleted on Stripe's side'; Handler 2 'fetches live from Stripe at execution time, not from cached state'. |
| c4 | Design uses an idempotency key derived from the Stripe event ID (`evt_*`) so duplicate webhooks produce the same outcome | PASS | 'INSERT INTO stripe_webhook_events (event_id) ON CONFLICT DO NOTHING'; void idempotency key: 'f"void_{event_id}_{invoice_id}"'; Assumption A2 confirms unique constraint on event_id. |
| c5 | Design persists the intended operation (event ID + intended action) before dispatching downstream side effects (email, revenue recognition entry) — never fire-and-forget | PASS | Ingress flow: 'Persist raw event payload to stripe_webhook_events' then 'Publish SubscriptionCancellationTriggered command'; each handler emits Invoked event before outbound call. |
| c6 | Design includes a reconciliation step — query Stripe to confirm the subscription state before treating the event as authoritative, since webhooks can arrive out of order or be replayed | PARTIAL | Handler 2 fetches live invoice state from Stripe; charge refund check via 'stripe.Charge.retrieve(charge_id)'. No explicit stripe.Subscription.retrieve() to verify subscription deletion state before proceeding. |
| c7 | Design addresses ASC 606 revenue recognition explicitly — names which performance obligation is being settled, how deferred revenue is moved to recognised revenue, and whether a credit memo is needed | PASS | §6 cites ASC 606-10-25 and 606-10-55-49 (breakage); 'performance obligation is continuous access to the service'; 'DR Deferred Revenue / CR Subscription Revenue'; ManualRevenueReviewRequired for refund offsets. |
| c8 | Design includes an immutable audit log entry for the cancellation event — what was received, when, who acted on it, the resulting state change | PASS | 'Persist raw event payload to stripe_webhook_events (event_id, type, payload, received_at)'; §2 full event lifecycle with timestamped Invoked/Replied pairs; SubscriptionCancellationSummaryProjection with completed_at. |
| c9 | Design names a decision checkpoint that should pause for human input (e.g. before changing refund policy for pro-rated cancellations, or before adopting a new revenue recognition treatment) | PASS | ASC 606 tree: 'Emit ManualRevenueReviewRequired → HALT automatic recognition. Flag for finance team.' Assumption A5: 'Refund-offset ASC 606 recognition requires manual finance review'. |
| c10 | Design addresses race conditions — concurrent webhooks for the same subscription (cancel + reactivate landing close together) — and how the handler is serialised or made commutative | PARTIAL | §7 covers out-of-order events; state machine 'active → cancellation_in_progress → cancelled' enforces valid transitions; no mention of serialisation mechanism (locks, optimistic concurrency) for concurrent processing. |
| c11 | Output is a design, not production code — no full FastAPI route implementation, no SQL DDL, no Python class definitions beyond signature-level pseudo-code | PASS | Output is entirely prose, tables, flow diagrams, and signature-level pseudo-code. No class definitions, no SQL DDL, no route decorators, no import statements. |
| c12 | Output's idempotency mechanism is named concretely (event ID stored in a unique-constrained table, with a `processed_at` timestamp) rather than "use idempotency keys" | PASS | 'INSERT INTO stripe_webhook_events (event_id) ON CONFLICT DO NOTHING'; table schema: '(event_id, type, payload, received_at)'; 'Assumption A2: stripe_webhook_events.event_id has a unique constraint'. |
| c13 | Output's reconciliation step specifies which Stripe API call to make (`stripe.Subscription.retrieve(subscription_id)`) and what state to compare against | FAIL | No stripe.Subscription.retrieve() call appears anywhere. Live Stripe calls are limited to invoice listing and stripe.Charge.retrieve() for refund checking. Subscription state is taken from the event payload. |
| c14 | Output's revenue-recognition treatment cites ASC 606 — names performance obligation, deferred revenue account, and the journal-entry shape (debit deferred revenue, credit recognised revenue) without dictating an exact dollar figure | PASS | §6: cites ASC 606-10-25; 'performance obligation is continuous access to the service'; 'DR Deferred Revenue deferred_to_recognise_cents / CR Subscription Revenue deferred_to_recognise_cents'; amount expressed as formula. |
| c15 | Output's webhook signature verification is acknowledged (the prompt says the verifier is wired up, so the design references it rather than duplicating it) | PASS | Ingress flow step: 'construct_event() — already wired, verifies Stripe-Signature header'. References without reproducing implementation. |
| c16 | Output lists the failure modes — duplicate event, out-of-order event, signature failure, downstream email send failure — and how each is handled (retry, dead-letter, alert) | PASS | §7 out-of-order table; §5 three-level idempotency; Handler 4 email retry with 'CancellationEmailFailed with alert metadata'; Stripe API failure recovery in Handler 2 via Invoked/Replied pattern. |
| c17 | Output addresses observability — what gets logged, what gets emitted as a metric (e.g. `stripe.webhook.subscription_deleted.received`, `.processed`, `.failed`), so the system is debuggable in production | PARTIAL | §8 Observability section names SubscriptionCancellationSummaryProjection with enumerated fields; 'every outbound call emits Invoked/Replied events'. No named metrics (e.g. stripe.webhook.*.received) or structured log fields. |
| c18 | Output flags whether the customer email send is a separate concern (queue + worker) or inline — and which is more defensible given idempotency requirements | PARTIAL | Handler 4 and Assumption A4 state email is non-critical, retried 3x with backoff, and cancellation completes regardless. Async after HTTP 200 is clear. 'Queue + worker vs inline' framing is not explicitly named. |

### Notes

The output is an exceptionally thorough event-sourced design that handles idempotency, ASC 606, audit logging, and failure modes with precision. The two main gaps are: no explicit pre-flight classification (c2) and no Stripe subscription state reconciliation call (c6 partial, c13 fail), which means the design trusts the event payload without independently verifying the subscription's current state on Stripe.
