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

Here is the design for the `customer.subscription.deleted` webhook handler.

---

## Design: `customer.subscription.deleted` Webhook Handler

### Scope and constraints

**Assumption A1:** The existing `stripe.Webhook.construct_event` verifier sits in FastAPI middleware or a dependency and raises `400` before the handler runs if the signature is invalid. This design does not re-verify.

**Assumption A2:** The existing database schema includes at minimum:
- `subscriptions(id, stripe_subscription_id, customer_id, status, current_period_start, current_period_end, cancelled_at, plan_id, currency, billing_interval)`
- `invoices(id, stripe_invoice_id, subscription_id, status, amount_due, due_date)`
- `deferred_revenue_ledger(id, subscription_id, period_start, period_end, total_amount, recognized_amount, recognized_at)` — one row per billing period
- `customers(id, email, name)`

**Assumption A3:** Revenue recognition uses a straight-line model across the billing period (daily rate × days remaining). This is the most common ASC 606 pattern for SaaS subscriptions with a single performance obligation (continuous access). If your subscription includes distinct deliverables per period, this needs revisiting.

**Assumption A4:** "Stop further billing" means deactivating any internal scheduled billing jobs or dunning tasks. Stripe itself stops charging on deletion — but local job queues (e.g. Celery tasks, pg-cron jobs, APScheduler) may have pending work.

**Assumption A5:** Email is dispatched asynchronously after the database transaction commits — never inside the transaction. Transactional email failure must not roll back the cancellation.

**Assumption A6:** The event will be delivered at least once. Idempotency is a hard requirement.

---

### Processing sequence

```
1. Receive event
2. Idempotency check
3. Resolve local subscription
4. DB transaction:
   a. Mark subscription cancelled
   b. Cancel pending internal invoices
   c. ASC 606 deferred revenue recognition
   d. Deactivate internal billing tasks
5. Stripe API: void open Stripe invoices
6. Commit
7. Dispatch cancellation email (async)
8. Return 200
```

---

### Step 1 — Receive event

The endpoint accepts `POST /webhooks/stripe`. The event type is asserted to be `customer.subscription.deleted` before any work begins; all other types are acknowledged with `200` and discarded (Stripe retries on non-2xx, so silent discard is correct for unhandled types).

The Stripe `Subscription` object is embedded in `event.data.object`.

---

### Step 2 — Idempotency

**Table:** `processed_webhook_events(stripe_event_id PRIMARY KEY, processed_at, outcome)`

Before doing any work, attempt an INSERT of `stripe_event_id`. If the row already exists (unique constraint violation), return `200` immediately with no further processing. This is a hard requirement because Stripe retries on network errors and may deliver the same event multiple times.

**Why INSERT-then-check rather than SELECT-then-INSERT:** Avoids the TOCTOU race between two concurrent deliveries of the same event. `ON CONFLICT DO NOTHING RETURNING *` is the idiomatic PostgreSQL pattern.

---

### Step 3 — Resolve local subscription

Look up the local subscription row by `stripe_subscription_id = event.data.object.id`. If no matching row exists:

- **Assumption A6a:** Log at WARNING level and return `200`. This can legitimately happen if the subscription was created outside our system (e.g. migrated from a legacy billing provider), or if a test-mode event fires against a production database. Do not return `4xx` — Stripe would retry indefinitely.

---

### Step 4 — Database transaction (`REPEATABLE READ` isolation)

`REPEATABLE READ` is sufficient here: we're updating a single subscription row and related rows, and we want protection against concurrent status changes (e.g. an upgrade/downgrade webhook racing with a deletion). `SERIALIZABLE` would be overly conservative and increases deadlock risk.

#### 4a — Mark subscription cancelled

Set `subscriptions.status = 'cancelled'` and `subscriptions.cancelled_at = event.data.object.canceled_at` (Stripe Unix timestamp, convert to UTC datetime).

**Assumption A7:** `event.data.object.canceled_at` is the canonical cancellation timestamp. Do not use `NOW()` — Stripe's timestamp is what matters for revenue recognition calculations.

Check for idempotency: if `status` is already `cancelled`, exit the transaction early and return `200`. (This is belt-and-suspenders; the webhook idempotency table in Step 2 is the primary guard, but a double-fire within the same DB session window could skip that.)

#### 4b — Cancel pending internal invoices

Query `invoices WHERE subscription_id = ? AND status IN ('draft', 'open', 'pending')`. For each:

- Set `status = 'voided'`
- Set `voided_at = NOW()`
- Set `void_reason = 'subscription_cancelled'`

**Assumption A8:** "Pending invoices" means invoices in our local system that have not yet been collected. Stripe-side open invoices are handled separately in Step 5 because Stripe is the source of truth for billing state, and voiding locally without voiding on Stripe would leave the customer's Stripe account in an inconsistent state.

#### 4c — ASC 606 deferred revenue recognition

ASC 606 requires recognising revenue as performance obligations are satisfied. For a SaaS subscription, the single performance obligation is providing access; it is satisfied ratably over the subscription period.

**Calculation logic:**

1. Find the active deferred revenue ledger row for the current billing period: `WHERE subscription_id = ? AND period_end >= cancelled_at AND period_start <= cancelled_at`.
2. Days in period = `(period_end - period_start).days`
3. Days elapsed = `(cancelled_at - period_start).days` (floored to 0 minimum)
4. Earned amount = `total_amount × (days_elapsed / days_in_period)`, rounded to 2 decimal places using `ROUND(..., 2)` — **not** Python float arithmetic (use `decimal.Decimal`).
5. Already-recognized amount = `recognized_amount` on the ledger row.
6. Incremental recognition = `earned_amount - already_recognized_amount`.

If `incremental_recognition > 0`:
- Update `deferred_revenue_ledger.recognized_amount += incremental_recognition`
- Update `deferred_revenue_ledger.recognized_at = cancelled_at`
- Insert into `revenue_recognition_journal(subscription_id, amount, recognised_at, reason)` with `reason = 'subscription_cancelled_accelerated'`

If the subscription is cancelled at `period_end` (i.e. end-of-period cancellation), no acceleration is needed; the full amount is already recognized by normal periodic recognition runs.

**Assumption A9:** Refunds are handled by a separate refund flow (triggered by `customer.subscription.deleted` only when `event.data.object.cancellation_details.reason == 'cancellation_requested'` and a proration credit exists). Refund accounting is out of scope here — this design only handles revenue recognition, not cash reimbursement. If your billing model issues prorated refunds, a separate credit memo flow is needed.

**Assumption A10:** The deferred revenue recognition journal entries feed into your accounting system via a nightly export or event stream. This design writes to the journal table; downstream propagation is out of scope.

#### 4d — Deactivate internal billing tasks

Query and soft-delete (or cancel) any scheduled billing tasks tied to this subscription:

- `scheduled_billing_tasks WHERE subscription_id = ? AND status = 'pending'` → set `status = 'cancelled'`, `cancelled_at = NOW()`
- `dunning_tasks WHERE subscription_id = ? AND status IN ('pending', 'scheduled')` → same

**Assumption A11:** If your task queue is external (Celery, RQ, etc.), you cannot reliably cancel in-flight tasks inside a DB transaction. The recommended pattern is: mark as cancelled in the DB, and add an early-exit guard at the top of each task that checks `status == 'cancelled'` before executing. This is the "soft cancel via DB flag" pattern.

---

### Step 5 — Stripe API: void open invoices

After the DB transaction commits, call the Stripe API to void any open invoices on the Stripe side.

```
stripe.Invoice.list(subscription=stripe_subscription_id, status='open')
for each invoice → stripe.Invoice.void_invoice(invoice.id)
```

**Why after the DB commit:** If the Stripe API call fails, we don't want to roll back a valid cancellation. The correct behaviour is: log the failure, emit a metric or alert, and schedule a retry job. A cancelled subscription with an unvoided Stripe invoice is a recoverable inconsistency; a rolled-back cancellation is not.

**Assumption A12:** Stripe automatically voids draft invoices when a subscription is deleted. Open invoices (already finalised) require explicit API calls. If your Stripe account is configured to `cancel_at_period_end`, Stripe may already void these — but defensive voiding is correct regardless.

**Retry policy:** 3 attempts with exponential backoff (1s, 2s, 4s). After exhausting retries, log at ERROR and insert into `failed_stripe_operations(stripe_subscription_id, operation, payload, created_at)` for manual reconciliation.

---

### Step 6 — Commit

Transaction commits in Step 4. Step 5 is outside the transaction. The `processed_webhook_events` row inserted in Step 2 also commits with the transaction — if Step 4 rolls back, the idempotency row is rolled back too, allowing safe redelivery.

**Caveat:** The idempotency row and the business transaction should be in the same transaction for atomicity. If they are in separate transactions (idempotency check → separate transaction → main transaction), there is a narrow window where a rollback leaves the idempotency row committed but no work done. Keep them in one transaction.

---

### Step 7 — Dispatch cancellation email (async)

After the full transaction commits and Stripe invoices are handled, enqueue the cancellation email. Do not send inline — email delivery can be slow (100-500ms+) and must not block the webhook response.

**Email content (minimum):**
- Customer name and email resolved from `customers` table
- Subscription plan name
- Effective cancellation date (`cancelled_at`)
- Any access remaining until `current_period_end` (if `cancel_at_period_end` was set — **Assumption A13:** if `cancel_at_period_end = false`, access ends immediately; if `true`, access continues to `current_period_end`)

**Queue mechanism:** Use your existing async queue (Celery task, FastAPI `BackgroundTasks`, or an outbox pattern). The outbox pattern (write email job to `outbox_emails` table inside the main transaction, poll and send separately) is the most reliable if your email queue is external — it prevents losing the email job if the process crashes between commit and enqueue.

---

### Error handling and rollback

| Failure point | Behaviour |
|---|---|
| Idempotency INSERT conflict | Return `200`, no work done |
| Subscription not found locally | Log WARNING, return `200` |
| DB transaction failure (deadlock, constraint) | Rollback, return `500` → Stripe retries |
| Stripe invoice void API failure | Log ERROR, write to `failed_stripe_operations`, return `200` (don't re-raise) |
| Email enqueue failure | Log ERROR, return `200` (email failure must not affect billing state) |

Return `500` only when you want Stripe to retry. Return `200` for terminal conditions (not found, already processed) — `500` on permanent failures will cause Stripe to retry up to 72 hours, generating noise and duplicate attempts.

---

### Assumptions summary (consolidated)

| ID | Assumption |
|---|---|
| A1 | Signature verification is upstream of this handler |
| A2 | Schema as described above exists |
| A3 | Straight-line revenue recognition, single performance obligation |
| A4 | Internal billing jobs may be in a local queue (Celery, pg-cron, etc.) |
| A5 | Email is async, outside the transaction |
| A6 | At-least-once delivery; idempotency required |
| A6a | Unknown subscription → log + 200, not an error |
| A7 | `event.data.object.canceled_at` is canonical, not `NOW()` |
| A8 | Local invoices and Stripe invoices are voided independently |
| A9 | Prorated refunds are a separate flow; not in scope here |
| A10 | Journal entries feed accounting via a separate export |
| A11 | Async task cancellation uses soft-cancel via DB flag |
| A12 | Only open Stripe invoices need explicit void; drafts auto-void |
| A13 | `cancel_at_period_end = false` means immediate access termination |

## Evaluation

| Field | Value |
|---|---|
| Verdict | PARTIAL |
| Score | 11.5/16.5 (70%) |
| Evaluated | 2026-05-27 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 85052 ms |
| Target cost | $0.1931 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent reads the project conventions (Pre-Flight Step 1) and references the language stack (Python 3.13, FastAPI) and the existing webhook verifier setup before designing | PASS | Assumption A1 references 'stripe.Webhook.construct_event verifier sits in FastAPI middleware'; design mentions 'decimal.Decimal' (Python), FastAPI endpoint POST /webhooks/stripe. |
| c2 | Agent classifies the work (Pre-Flight Step 3) — this is a "Payment flow (webhook)" task, not a subscription lifecycle change or a reporting task | FAIL | No explicit Pre-Flight classification step present. Design jumps directly to 'Scope and constraints' with no formal task-type classification statement. |
| c3 | Design treats the Stripe gateway as the authoritative source of truth — local state reconciles to Stripe, not the other way around | PASS | A7: 'event.data.object.canceled_at is canonical. Do not use NOW().' Step 5 notes 'Stripe is the source of truth for billing state.' A8 states local/Stripe invoices voided independently. |
| c4 | Design uses an idempotency key derived from the Stripe event ID (`evt_*`) so duplicate webhooks produce the same outcome | PASS | Step 2: 'Table: processed_webhook_events(stripe_event_id PRIMARY KEY, processed_at, outcome)' — INSERT of stripe_event_id; conflict → return 200 immediately. |
| c5 | Design persists the intended operation (event ID + intended action) before dispatching downstream side effects (email, revenue recognition entry) — never fire-and-forget | PASS | Idempotency INSERT committed atomically with business transaction (Step 6). Email dispatched only after commit (Step 7). Outbox pattern recommended to prevent lost email jobs. |
| c6 | Design includes a reconciliation step — query Stripe to confirm the subscription state before treating the event as authoritative, since webhooks can arrive out of order or be replayed | FAIL | No stripe.Subscription.retrieve() call or equivalent state-verification step exists anywhere in the processing sequence. Event data is used directly without cross-checking Stripe's current state. |
| c7 | Design addresses ASC 606 revenue recognition explicitly — names which performance obligation is being settled, how deferred revenue is moved to recognised revenue, and whether a credit memo is needed | PASS | Step 4c: 'single performance obligation is providing access; satisfied ratably.' Details deferred_revenue_ledger → revenue_recognition_journal. A9 explicitly addresses credit memos as a separate flow. |
| c8 | Design includes an immutable audit log entry for the cancellation event — what was received, when, who acted on it, the resulting state change | PARTIAL | processed_webhook_events captures event_id/processed_at/outcome; revenue_recognition_journal and failed_stripe_operations exist. No single unified audit log captures 'who acted on it' + full state transition. |
| c9 | Design names a decision checkpoint that should pause for human input (e.g. before changing refund policy for pro-rated cancellations, or before adopting a new revenue recognition treatment) | PARTIAL | A3: 'If subscription includes distinct deliverables per period, this needs revisiting.' A9: 'If billing model issues prorated refunds, a separate credit memo flow is needed.' Framed as assumptions, not explicit human-review checkpoints. |
| c10 | Design addresses race conditions — concurrent webhooks for the same subscription (cancel + reactivate landing close together) — and how the handler is serialised or made commutative | PARTIAL | Step 4: 'REPEATABLE READ... protection against concurrent status changes (e.g. upgrade/downgrade racing with deletion).' Belt-and-suspenders check in 4a. Cancel+reactivate ordering not explicitly resolved. |
| c11 | Output is a design, not production code — no full FastAPI route implementation, no SQL DDL, no Python class definitions beyond signature-level pseudo-code | PASS | Schema described in prose (Assumption A2). Only a 2-line Stripe API pseudo-snippet appears. No FastAPI decorators, no SQL DDL, no class definitions. |
| c12 | Output's idempotency mechanism is named concretely (event ID stored in a unique-constrained table, with a `processed_at` timestamp) rather than "use idempotency keys" | PASS | Step 2: 'processed_webhook_events(stripe_event_id PRIMARY KEY, processed_at, outcome)' — PRIMARY KEY enforces uniqueness; processed_at timestamp explicitly named. |
| c13 | Output's reconciliation step specifies which Stripe API call to make (`stripe.Subscription.retrieve(subscription_id)`) and what state to compare against | FAIL | No reconciliation step exists in the design. stripe.Subscription.retrieve() is never mentioned. Only Stripe API calls are Invoice.list() and Invoice.void_invoice() in Step 5. |
| c14 | Output's revenue-recognition treatment cites ASC 606 — names performance obligation, deferred revenue account, and the journal-entry shape (debit deferred revenue, credit recognised revenue) without dictating an exact dollar figure | PARTIAL | ASC 606 cited; performance obligation named; deferred_revenue_ledger and revenue_recognition_journal named. Debit/credit accounting terminology (DR deferred revenue, CR recognised revenue) is absent. |
| c15 | Output's webhook signature verification is acknowledged (the prompt says the verifier is wired up, so the design references it rather than duplicating it) | PASS | A1: 'The existing stripe.Webhook.construct_event verifier sits in FastAPI middleware... raises 400 before the handler runs if the signature is invalid. This design does not re-verify.' |
| c16 | Output lists the failure modes — duplicate event, out-of-order event, signature failure, downstream email send failure — and how each is handled (retry, dead-letter, alert) | PARTIAL | Table covers duplicate event, missing subscription, DB failure, Stripe API failure, email failure. Out-of-order event and signature failure not in the table (A1 covers signature implicitly). No dead-letter queue named. |
| c17 | Output addresses observability — what gets logged, what gets emitted as a metric (e.g. `stripe.webhook.subscription_deleted.received`, `.processed`, `.failed`), so the system is debuggable in production | PARTIAL | Logging levels mentioned (WARNING, ERROR) in multiple places; Step 5 mentions 'emit a metric or alert.' No metric names defined; no structured logging schema; no tracing references. |
| c18 | Output flags whether the customer email send is a separate concern (queue + worker) or inline — and which is more defensible given idempotency requirements | PARTIAL | Step 7: 'Do not send inline... enqueue the cancellation email.' Outbox pattern recommended as 'most reliable.' Idempotency of email itself (duplicate sends on retry) not explicitly addressed. |

### Notes

The design is thorough on idempotency, ASC 606, and the no-production-code constraint, and its assumption documentation is well-structured. The two significant gaps are the missing Stripe reconciliation step (c6, c13) and the absent Pre-Flight task classification (c2), which together account for most of the score deficit.
