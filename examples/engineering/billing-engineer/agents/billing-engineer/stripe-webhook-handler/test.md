# Test: billing-engineer designs a Stripe subscription-cancellation webhook handler

Scenario: A developer asks the billing-engineer agent to implement a Stripe webhook handler for the `customer.subscription.deleted` event. The agent should ground its design in the non-negotiable rules — idempotency, gateway-as-source-of-truth, immutable audit log, revenue recognition — rather than producing a generic webhook tutorial. It should not write production code (this is a design, not implementation), but it should be specific enough that an implementer could follow it.

## Prompt

We need a Stripe webhook handler for `customer.subscription.deleted` events. When a subscription is cancelled on Stripe (by the customer or because of failed payment), we need to:

1. Update our local subscription record to "cancelled" status
2. Stop further billing
3. Cancel any pending invoices
4. Recognise the remaining deferred revenue (we use ASC 606)
5. Send the customer a cancellation email

We're on PostgreSQL, Python 3.13 with FastAPI, and the existing codebase already has a `stripe.Webhook.construct_event` verifier wired up. Don't pause for clarification — produce the design now with the most defensible defaults and document any assumptions inline. Output the design only — do NOT write production code.

## Criteria

- [ ] PASS: Agent reads the project conventions (Pre-Flight Step 1) and references the language stack (Python 3.13, FastAPI) and the existing webhook verifier setup before designing
- [ ] PASS: Agent classifies the work (Pre-Flight Step 3) — this is a "Payment flow (webhook)" task, not a subscription lifecycle change or a reporting task
- [ ] PASS: Design treats the Stripe gateway as the authoritative source of truth — local state reconciles to Stripe, not the other way around
- [ ] PASS: Design uses an idempotency key derived from the Stripe event ID (`evt_*`) so duplicate webhooks produce the same outcome
- [ ] PASS: Design persists the intended operation (event ID + intended action) before dispatching downstream side effects (email, revenue recognition entry) — never fire-and-forget
- [ ] PASS: Design includes a reconciliation step — query Stripe to confirm the subscription state before treating the event as authoritative, since webhooks can arrive out of order or be replayed
- [ ] PASS: Design addresses ASC 606 revenue recognition explicitly — names which performance obligation is being settled, how deferred revenue is moved to recognised revenue, and whether a credit memo is needed
- [ ] PASS: Design includes an immutable audit log entry for the cancellation event — what was received, when, who acted on it, the resulting state change
- [ ] PASS: Design names a decision checkpoint that should pause for human input (e.g. before changing refund policy for pro-rated cancellations, or before adopting a new revenue recognition treatment)
- [ ] PARTIAL: Design addresses race conditions — concurrent webhooks for the same subscription (cancel + reactivate landing close together) — and how the handler is serialised or made commutative
- [ ] PASS: Output is a design, not production code — no full FastAPI route implementation, no SQL DDL, no Python class definitions beyond signature-level pseudo-code

## Output expectations

- [ ] PASS: Output's idempotency mechanism is named concretely (event ID stored in a unique-constrained table, with a `processed_at` timestamp) rather than "use idempotency keys"
- [ ] PASS: Output's reconciliation step specifies which Stripe API call to make (`stripe.Subscription.retrieve(subscription_id)`) and what state to compare against
- [ ] PASS: Output's revenue-recognition treatment cites ASC 606 — names performance obligation, deferred revenue account, and the journal-entry shape (debit deferred revenue, credit recognised revenue) without dictating an exact dollar figure
- [ ] PASS: Output's webhook signature verification is acknowledged (the prompt says the verifier is wired up, so the design references it rather than duplicating it)
- [ ] PASS: Output lists the failure modes — duplicate event, out-of-order event, signature failure, downstream email send failure — and how each is handled (retry, dead-letter, alert)
- [ ] PARTIAL: Output addresses observability — what gets logged, what gets emitted as a metric (e.g. `stripe.webhook.subscription_deleted.received`, `.processed`, `.failed`), so the system is debuggable in production
- [ ] PARTIAL: Output flags whether the customer email send is a separate concern (queue + worker) or inline — and which is more defensible given idempotency requirements
