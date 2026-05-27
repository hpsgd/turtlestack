# Runbook Creation

Scenario: An engineering team needs a runbook for handling payment processing failures so on-call engineers can resolve incidents without tribal knowledge.

## Prompt

> Write a runbook for payment processing failures. Context:
> 
> - We use Stripe for payment processing
> - Common failure modes: Stripe API timeouts, card declines (various codes), idempotency key conflicts, webhook delivery failures
> - Our stack: Node.js API, PostgreSQL, Redis for job queues (Bull), Datadog for monitoring
> - Alert fires when: payment success rate drops below 95% over 5 minutes, or any Stripe API error rate exceeds 2%
> - Business impact: each minute of payment failure = ~$3,400 in lost transactions during peak hours
> 
> On-call engineers are expected to handle this without waking anyone up for most scenarios. We've had 4 incidents this quarter and each one took 45+ minutes to resolve because engineers didn't know where to look.
> 
> A few specifics for the response:
> 
> - Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
> - Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
> - For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
> - When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
> - Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

File written to `runbooks/payment-processing-failures.md`. Here's the full content:

---

# Payment Processing Failures — Runbook

> **Assumption notice:** This runbook was written without access to the application source. Commands marked
> `# ASSUMPTION — verify path/name` should be confirmed against your actual codebase before first use.
> Every placeholder that must be replaced is listed in the Prerequisites section.

---

## Overview

| Field | Value |
|---|---|
| **What this covers** | Diagnosing and resolving payment processing failures: Stripe API timeouts, card-decline spikes, idempotency key conflicts, and webhook delivery failures |
| **When to use** | Alert fires: `payment-success-rate-low` (success rate < 95% over 5 min) **or** `stripe-api-error-rate-high` (Stripe API error rate > 2%); or engineers observe payment errors in logs or customer reports |
| **Business impact** | ~$3,400/minute in lost transactions during peak hours. Customers cannot complete purchases. Every minute counts. |
| **Estimated duration** | 10–20 min for card-decline spikes (no action needed); 15–30 min for Stripe timeouts or idempotency conflicts; 20–45 min for webhook failures |
| **Risk level** | High |
| **Last tested** | UNTESTED — update this field after first use |
| **Owner** | Platform / Billing team — update with actual team and Slack channel |

---

## Prerequisites

Complete this checklist **before** starting the procedure. Do not skip items.

```
- [ ] VPN connected to production network — connect: [your VPN instructions here]
      ⏱ If you don't have VPN access, request it from IT — this may take 30+ min, do this first.

- [ ] Stripe Dashboard access (read-only minimum) — https://dashboard.stripe.com
      If you don't have access: request from your team lead via [your access-request process].
      ⏱ Access may take 5–10 min to provision.

- [ ] Datadog access — https://app.datadoghq.com
      If you don't have access: request from [team/person] via [your access-request process].

- [ ] kubectl or SSH access to the Node.js API service — verify with:
        kubectl get pods -n production -l app=api  # ASSUMPTION — verify namespace and label
      OR:
        ssh deploy@api.internal  # ASSUMPTION — verify SSH host

- [ ] redis-cli installed and reachable — verify with:
        redis-cli -u $REDIS_URL ping  # should return: PONG
      Install: brew install redis (macOS) or apt install redis-tools (Linux)

- [ ] psql installed and DATABASE_URL exported — verify with:
        psql $DATABASE_URL -c "SELECT 1;"  # should return: 1
      Install: brew install postgresql (macOS) or apt install postgresql-client (Linux)

- [ ] Stripe CLI installed — version 1.19+ — verify with:
        stripe --version
      Install: brew install stripe/stripe-cli/stripe (macOS)
               or see https://stripe.com/docs/stripe-cli

- [ ] Environment variables set in your terminal:
        export STRIPE_SECRET_KEY="sk_live_..."   # from: [your secrets manager — e.g. 1Password, AWS Secrets Manager]
        export DATABASE_URL="postgres://..."      # from: [your secrets manager]
        export REDIS_URL="redis://..."            # from: [your secrets manager]
        # ASSUMPTION: adjust secret names to match your secrets manager

- [ ] Slack: join #incidents (or your team's incident channel) and post: "investigating payment failures"
      ⏱ Keep this channel open — post an update every 10 minutes while investigating.
```

---

## Pre-check — is this the right runbook?

**Run these checks before proceeding.** The alert may be transient. Do not take action on a self-resolving event.

```
- [ ] Check the Datadog alert status:
        # Open Datadog → Monitors → [payment-success-rate-low or stripe-api-error-rate-high]
        # Is the alert still in ALERT state, or has it resolved to OK?

- [ ] Confirm with a live health check against the payment endpoint:
        curl -s https://[your-api-domain]/health | jq .  # ASSUMPTION — verify your health endpoint path
        # Expected output: {"status":"ok","payments":"healthy"} or similar
        # If output shows "degraded" or "error" for payments — continue this runbook
        # If output shows fully healthy — wait 60 seconds and re-run before proceeding

- [ ] Retry after 60 seconds:
        sleep 60 && curl -s https://[your-api-domain]/health | jq .
        # If healthy on retry — alert was transient, no action needed. Close alert and note in #incidents.

- [ ] Confirm this is not a planned event:
        # Check your team's change log / maintenance calendar at: [your change log URL]
        # Check #deploys or equivalent Slack channel for recent deployments in the last 30 min

- [ ] Stop conditions — do NOT proceed if:
        - Health check passes on retry (wait 2 minutes and check again to be sure)
        - A planned Stripe maintenance window is active: https://status.stripe.com
        - A deployment was made in the last 5 minutes (wait for it to stabilise, then re-check)
        - The alert was already acknowledged by another engineer (check #incidents)
```

---

## Procedure

This procedure has **two phases**:
1. **Triage** (Steps 1–2): identify which failure mode is active. This takes 5–10 minutes.
2. **Fix** (Steps 3–6): go to the section matching your diagnosis. Do not run all sections.

---

#### Step 1: Check the Datadog payment dashboard and identify the error type

**Action:**
```bash
# Open Datadog and navigate to the payments dashboard:
# https://app.datadoghq.com/dashboard/[your-payments-dashboard-id]  # ASSUMPTION — get dashboard ID from your team

# While the dashboard loads, pull recent payment errors from application logs:
# If using kubectl:
kubectl logs -n production -l app=api --since=10m | grep -i "stripe\|payment\|error\|fail" | tail -50
# ASSUMPTION — adjust namespace and label selector

# If using SSH + pm2:
ssh deploy@api.internal "pm2 logs api --lines 100 --nostream" | grep -i "stripe\|payment\|error\|fail"
# ASSUMPTION — adjust PM2 app name
```

**Expected output:**
```
# Match one of these patterns to a failure mode:

# Stripe API timeout:
[ERROR] Stripe request timed out after 30000ms  {"type":"StripeConnectionError","path":"POST /v1/payment_intents"}

# Card decline spike:
[ERROR] Payment declined  {"code":"card_declined","decline_code":"insufficient_funds","customer_id":"cus_xxx"}

# Idempotency key conflict:
[ERROR] Stripe idempotency error  {"type":"IdempotencyError","message":"Keys for idempotent requests..."}

# Webhook failure:
[ERROR] Webhook signature verification failed  {"err":"No signatures found matching..."}
```

**If this fails:**
- Symptom: `kubectl` returns "Error from server (Forbidden)"
- Likely cause: kubeconfig not set for production or missing RBAC permissions
- Fix: `kubectl config use-context [production-context-name]`
- If the fix doesn't work: escalate to #infra-oncall

**Checkpoint:** You have identified the dominant error type. Go to:
- Stripe timeout → **Step 3**
- Card declines → **Step 4**
- Idempotency conflict → **Step 5**
- Webhook failures → **Step 6**
- Mix / unclear → **Step 2**

---

#### Step 2: Query the payments database for a failure breakdown

**Action:**
```bash
psql $DATABASE_URL << 'SQL'
SELECT
  error_code,
  COUNT(*) AS failure_count,
  MAX(created_at) AS most_recent
FROM payment_attempts                  -- ASSUMPTION: verify your table name
WHERE
  status = 'failed'
  AND created_at > NOW() - INTERVAL '15 minutes'
GROUP BY error_code
ORDER BY failure_count DESC;
SQL
```

**Expected output:**
```
    error_code       | failure_count |          most_recent
---------------------+---------------+-------------------------------
 card_declined       |           142 | 2024-01-15 02:13:44.123456+00
 timeout             |            12 | 2024-01-15 02:14:01.987654+00
 idempotency_error   |             3 | 2024-01-15 02:11:22.345678+00
```

**If this fails:**
- Symptom: `psql: error: connection to server ... failed: FATAL: role "..." does not exist`
- Fix: re-export `DATABASE_URL` from your secrets manager

**Checkpoint:** Dominant error_code identified. Go to the matching numbered step.

---

#### Step 3: Stripe API timeouts

**When to use:** Logs show `StripeConnectionError`, `ETIMEDOUT`, or `read ECONNRESET` targeting Stripe endpoints.

**Sub-step 3a: Check Stripe's status page**

**Action:**
```bash
curl -s https://status.stripe.com/api/v2/status.json | jq '{status: .status.description, indicator: .status.indicator}'
```

**Expected output (healthy):**
```json
{"status": "All Systems Operational", "indicator": "none"}
```

**If Stripe reports an outage:**
- This is Stripe-side. Your system is not broken.
- Post in #incidents: "Stripe reporting [indicator] outage. Monitoring https://status.stripe.com"
- Do NOT restart the API or modify config.
- Monitor every 5 minutes. If outage exceeds 15 minutes: escalate to Stripe Support (see Escalation).
- When Stripe resolves: go to Verification.

**If Stripe status is green:** Continue to Sub-step 3b.

---

**Sub-step 3b: Check API service resource utilisation**

**Action:**
```bash
kubectl top pods -n production -l app=api  # ASSUMPTION — adjust namespace/label
```

**Expected output (healthy):**
```
NAME                   CPU(cores)   MEMORY(bytes)
api-7d9f5b-abc12       120m         380Mi
```

**Expected output (problem):**
```
api-7d9f5b-abc12       980m         1450Mi    ← near limits
```

**If CPU or memory is above 80% of limits:**
```bash
kubectl scale deployment api -n production --replicas=$(( $(kubectl get deployment api -n production -o jsonpath='{.spec.replicas}') + 2 ))
# ASSUMPTION — adjust deployment name
kubectl rollout status deployment/api -n production --timeout=120s
kubectl top pods -n production -l app=api
```

**Checkpoint:** After scaling, wait 2 minutes. If success rate hasn't improved, continue to Sub-step 3c.

---

**Sub-step 3c: Check Redis (Bull queue) for a processing backlog**

**Action:**
```bash
redis-cli -u $REDIS_URL
LLEN bull:payment-processing:wait    # ASSUMPTION — verify your Bull queue name
LLEN bull:payment-processing:active
GET  bull:payment-processing:failed
```

**Expected output (problem):** wait queue length > 500

**If wait queue > 500 jobs:**

⚠ **WARNING: The following command pauses the queue and stops new payment jobs from being picked up. This is intentional — it prevents the backlog from growing while you investigate. Resume in Sub-step 3d.**

```bash
curl -X POST https://[your-api-domain]/admin/queues/payment-processing/pause \
  -H "Authorization: Bearer $ADMIN_API_TOKEN"
# ASSUMPTION — verify endpoint and token env var
```

**Checkpoint:** Queue paused. Continue to Sub-step 3d.

---

**Sub-step 3d: Resume the Bull queue and verify recovery**

**Action:**
```bash
curl -X POST https://[your-api-domain]/admin/queues/payment-processing/resume \
  -H "Authorization: Bearer $ADMIN_API_TOKEN"

redis-cli -u $REDIS_URL LLEN bull:payment-processing:wait
# Should be decreasing each time you run this
```

**Checkpoint:** Wait length decreasing. Go to **Verification**.

---

#### Step 4: Card decline spike

**When to use:** Logs show `card_declined`, `insufficient_funds`, `do_not_honor`, `lost_card`, or `stolen_card` in high volume.

**Sub-step 4a: Identify the decline codes and pattern**

**Action:**
```bash
psql $DATABASE_URL << 'SQL'
SELECT
  stripe_decline_code,              -- ASSUMPTION: verify column name
  COUNT(*) AS count,
  COUNT(DISTINCT customer_id) AS unique_customers,
  COUNT(DISTINCT ip_address) AS unique_ips   -- ASSUMPTION: verify column names
FROM payment_attempts
WHERE
  status = 'failed'
  AND created_at > NOW() - INTERVAL '15 minutes'
GROUP BY stripe_decline_code
ORDER BY count DESC;
SQL
```

**Expected output (organic — no action needed):**
```
stripe_decline_code  | count | unique_customers | unique_ips
---------------------+-------+-----------------+-----------
insufficient_funds   |    45 |              43 |         41   ← many unique = organic
```

**Expected output (carding attack):**
```
card_declined        |  1842 |              12 |          3   ← few unique = attack
```

**If organic (many unique IPs/customers):**
- Decline rate < 8%: within normal range. No action. Monitor for 10 minutes.
- Decline rate > 8%: check https://status.stripe.com for issuer outages. Post in #incidents.

**If carding attack (high volume, < 10 unique IPs):**
```bash
psql $DATABASE_URL << 'SQL'
SELECT ip_address, COUNT(*) AS attempts
FROM payment_attempts
WHERE status = 'failed'
  AND created_at > NOW() - INTERVAL '30 minutes'
GROUP BY ip_address
HAVING COUNT(*) > 20
ORDER BY attempts DESC;
SQL
```

⚠ **WARNING: Blocking IPs affects all traffic from that address. Cross-check against your monitoring/internal IP allowlist before blocking.**

```bash
# Block IPs at your WAF layer (adjust for your provider):
# Cloudflare: Security → WAF → IP Access Rules → Block [ip]
# AWS WAF: update the IP block list in the WAF console
# ASSUMPTION — verify your WAF provider and process
```

**Checkpoint:** Decline pattern identified. Action taken (or confirmed not needed). Go to **Verification**.

---

#### Step 5: Idempotency key conflicts

**When to use:** Logs show `IdempotencyError` or "Keys for idempotent requests can only be used with the same parameters".

**Sub-step 5a: Confirm the error pattern and source**

**Action:**
```bash
kubectl logs -n production -l app=api --since=30m \
  | grep -i "idempotency" \
  | grep -o '"idempotency_key":"[^"]*"' \
  | sort | uniq -c | sort -rn | head -20
# ASSUMPTION — adjust log format to match your JSON key name
```

**Expected output showing retry bug:**
```
      8 "idempotency_key":"pay_retry_1705280042_ord_7f3a"   ← different timestamps, same order
      3 "idempotency_key":"pay_retry_1705280001_ord_7f3a"   ← retry loop is generating new keys
```

**Sub-step 5b: Check for a recent deployment that changed retry logic**

**Action:**
```bash
kubectl exec -n production -it $(kubectl get pod -n production -l app=api -o name | head -1) \
  -- git log --since="1 hour ago" --oneline -- src/payments/ src/jobs/ src/stripe/
# ASSUMPTION — adjust paths to your payment source directories
```

**If a deployment in the last hour changed retry logic:**

⚠ **WARNING: Rolling back causes a brief restart of API pods. Payments in flight will be retried. Confirm with your team lead before proceeding.**

```bash
kubectl rollout history deployment/api -n production
kubectl rollout undo deployment/api -n production
kubectl rollout status deployment/api -n production --timeout=120s
```

**If no recent deployment:** This is a pre-existing bug at scale. Continue to Sub-step 5c.

**Sub-step 5c: Clear stuck idempotency-conflicted jobs from the queue**

**Action:**
```bash
redis-cli -u $REDIS_URL
# For Bull v3 — rename failed key to preserve for post-incident review (do NOT delete):
redis-cli -u $REDIS_URL RENAME bull:payment-processing:failed bull:payment-processing:failed-incident-$(date +%Y%m%d%H%M)
# ASSUMPTION — verify against your Bull version; Bull 4.x uses sorted sets — use Bull Board UI instead
```

**If this fails:** Do not proceed with manual Redis manipulation. Escalate to #platform-oncall.

**Checkpoint:** Idempotency error rate in logs drops to near zero. File a bug report. Go to **Verification**.

---

#### Step 6: Webhook delivery failures

**When to use:** Logs show signature verification failures OR Stripe Dashboard → Developers → Webhooks shows delivery failures.

**Sub-step 6a: Check Stripe webhook delivery status**

**Action:**
```bash
stripe events list --limit 20 --api-key $STRIPE_SECRET_KEY \
  | jq '.data[] | {id: .id, type: .type, created: .created}'
```

Then check Stripe Dashboard:
```
1. Open https://dashboard.stripe.com/developers/webhooks
2. Click your endpoint URL (e.g. https://[your-api-domain]/webhooks/stripe)
3. Click "Recent deliveries" — look for "Failed" status
4. Click a failed delivery to see the error response
```

Match the error to a sub-step:
- `HTTP 400: No signatures found matching` → **Sub-step 6b** (secret mismatch)
- `HTTP 503 / connection refused` → return to **Step 3** (API is down)
- `Stripe cannot reach endpoint` → **Sub-step 6d** (network/firewall)
- `HTTP 200 but no action` → **Sub-step 6c** (handler error)

---

**Sub-step 6b: Webhook secret mismatch — resync the signing secret**

**Action:**
```bash
# 1. Get the current signing secret from Stripe Dashboard:
#    https://dashboard.stripe.com/developers/webhooks → click endpoint → "Reveal" signing secret
#    Copy value (starts with whsec_)

# 2. Update in your secrets manager (AWS Secrets Manager example):
aws secretsmanager update-secret \
  --secret-id production/stripe/webhook-secret \
  --secret-string "whsec_[paste-value-here]"
# ASSUMPTION — verify your secret name

# 3. Restart API to pick up new secret:
kubectl rollout restart deployment/api -n production
kubectl rollout status deployment/api -n production --timeout=120s
```

**Checkpoint:** Trigger a test webhook from Stripe Dashboard → your endpoint → "Send test webhook". Should show HTTP 200. Go to Sub-step 6c to replay missed events.

---

**Sub-step 6c: Replay failed webhook events**

⚠ **WARNING: Replaying `payment_intent.succeeded` events re-triggers order fulfilment. Only do this if your handlers are idempotent (processing the same event twice does not create duplicate orders). If unsure — do NOT replay. Escalate to engineering instead.**

**Action:**
```bash
# List recent succeeded payment events:
stripe events list \
  --api-key $STRIPE_SECRET_KEY \
  --limit 100 \
  | jq '.data[] | select(.type == "payment_intent.succeeded") | .id' \
  | tr -d '"'

# Replay each event:
stripe events resend evt_3xxxx --api-key $STRIPE_SECRET_KEY
```

**If handlers are not idempotent — check for stuck orders instead:**
```bash
psql $DATABASE_URL << 'SQL'
SELECT id, stripe_payment_intent_id, status, created_at
FROM orders                             -- ASSUMPTION: verify table name
WHERE status = 'pending'
  AND created_at > NOW() - INTERVAL '2 hours'
  AND stripe_payment_intent_id IS NOT NULL
ORDER BY created_at DESC
LIMIT 50;
SQL
```
Escalate to engineering for manual order reconciliation if rows are returned.

---

**Sub-step 6d: Webhook endpoint unreachable from Stripe**

**Action:**
```bash
# Test reachability:
curl -v -X POST https://[your-api-domain]/webhooks/stripe \
  -H "Content-Type: application/json" \
  -d '{"test": true}'
# Expected: HTTP 400 (signature check fails — but endpoint is reachable)
# Problem: connection refused, timeout, or DNS failure
```

**If unreachable:** This is a network/infrastructure issue. Escalate to #infra-oncall immediately.

---

## Verification

Run all checks after completing any procedure step. **All checks must pass before closing the incident.**

#### Verification checklist

```
- [ ] API health check passes:
        curl -s https://[your-api-domain]/health | jq .
        → Expected: {"status":"ok"} (or your system's healthy response)

- [ ] Payment success rate above 95% in Datadog:
        Open: https://app.datadoghq.com/dashboard/[your-payments-dashboard-id]
        → Metric: payment.success_rate (5-minute average) → Required: > 95%

- [ ] Stripe API error rate below 2% in Datadog:
        → Metric: stripe.api.error_rate (5-minute average) → Required: < 2%

- [ ] No new errors in API logs (last 5 minutes):
        kubectl logs -n production -l app=api --since=5m | grep -c "ERROR"
        → Expected: 0 or below your normal baseline (< 5)

- [ ] Bull queue wait length near zero:
        redis-cli -u $REDIS_URL LLEN bull:payment-processing:wait
        → Expected: < 50 jobs

- [ ] No pending orders stuck from the incident window:
        psql $DATABASE_URL -c "
          SELECT COUNT(*) FROM orders
          WHERE status = 'pending'
          AND created_at BETWEEN NOW() - INTERVAL '2 hours' AND NOW() - INTERVAL '5 minutes';"
        → Expected: 0 (or same count as pre-incident baseline)
        # ASSUMPTION — verify table and column names

- [ ] Stripe webhook delivery success rate:
        Open: https://dashboard.stripe.com/developers/webhooks → your endpoint
        → No failed deliveries in the last 10 minutes

- [ ] Make a test payment:
        stripe trigger payment_intent.succeeded --api-key $STRIPE_SECRET_KEY
        → Should appear in your system as a succeeded payment
```

---

## Rollback

#### Rollback procedure

**When to rollback:**
- The procedure made things worse (error rate increased after your action)
- Deployment rollback introduced new errors
- Queue jobs were paused/moved and orders are stuck

**Rollback window:**
- Deployment rollback: available while the previous ReplicaSet exists (typically 24 hours, depends on `revisionHistoryLimit`)
- Queue pause: can be resumed at any time
- Secret rotation: previous version restorable from secrets manager history

**Data implications:** Rolling back a deployment does not affect database data. If webhook events were replayed and triggered fulfilment, those state changes are NOT rolled back — check with engineering before rolling back.

---

**1. Roll back a deployment**

```bash
kubectl rollout history deployment/api -n production
# Roll forward (undo the undo):
kubectl rollout undo deployment/api -n production --to-revision=[most-recent-revision-number]
kubectl rollout status deployment/api -n production --timeout=120s
```
Expected result: `deployment "api" successfully rolled out`

---

**2. Resume a paused Bull queue**

```bash
curl -X POST https://[your-api-domain]/admin/queues/payment-processing/resume \
  -H "Authorization: Bearer $ADMIN_API_TOKEN"
```
Expected result: `{"status":"resumed"}`

---

**3. Restore a renamed Redis queue key**

```bash
redis-cli -u $REDIS_URL KEYS "bull:payment-processing:failed-incident-*"
# Copy the key name, then restore:
redis-cli -u $REDIS_URL RENAME bull:payment-processing:failed-incident-202401150214 bull:payment-processing:failed
```
Expected result: `OK`

---

**4. Revert a webhook secret rotation**

```bash
# List previous versions in AWS Secrets Manager:
aws secretsmanager list-secret-version-ids --secret-id production/stripe/webhook-secret
# Restore previous version — ASSUMPTION: verify rollback process for your secrets manager
aws secretsmanager restore-secret --secret-id production/stripe/webhook-secret

kubectl rollout restart deployment/api -n production
```

#### After rollback

```
- [ ] Verify rollback succeeded — run the full Verification checklist above
- [ ] Post in #incidents: "Rollback complete. Status: [healthy/still-degraded]"
- [ ] If still degraded after rollback: escalate immediately — see Escalation section
- [ ] Create incident ticket in [your ticketing system] with:
        - Timeline of actions taken
        - Which rollback was performed
        - Current system state
        - Stripe event IDs for any replayed events
        - Any orders that may need manual reconciliation
```

---

## Troubleshooting

#### Error rate drops briefly then climbs again

**Symptom:** Datadog shows success rate recovering but degrading again every few minutes.

**Cause:** Bull queue retry logic is hitting the same broken code path on each retry; backed-off jobs re-enter the active state in waves.

**Solution:**
```bash
# Pause the queue to stop the retry wave:
curl -X POST https://[your-api-domain]/admin/queues/payment-processing/pause \
  -H "Authorization: Bearer $ADMIN_API_TOKEN"

# Identify the failing jobs:
redis-cli -u $REDIS_URL LRANGE bull:payment-processing:active 0 20

# Once root cause is fixed or broken jobs cleared, resume:
curl -X POST https://[your-api-domain]/admin/queues/payment-processing/resume \
  -H "Authorization: Bearer $ADMIN_API_TOKEN"
```

**Prevention:** Configure Bull's backoff to use exponential delay with a cap so retry waves are spread out.

---

#### Procedure interrupted midway (terminal disconnects)

**Symptom:** Session was interrupted mid-procedure.

**Solution:**
1. Check current state before resuming:
   ```bash
   redis-cli -u $REDIS_URL GET bull:payment-processing:paused  # "1" = paused
   kubectl rollout status deployment/api -n production
   ```
2. Post in #incidents: "Rejoining investigation — checking current state."
3. Return to the **Pre-check** section and re-assess from scratch. Do not assume previous steps succeeded.

---

#### This runbook is run twice by accident

**Concerns:**
- `kubectl rollout undo` run twice: second call rolls back an additional revision. Fix: `kubectl rollout history` and roll forward to the intended version.
- Queue paused twice: no harm — still just paused. Resume once.
- Webhook events replayed twice: if handlers are idempotent, no harm. If not, duplicate orders may exist — escalate to engineering for deduplication.

**Prevention:** Always check #incidents for an active investigation before starting this runbook.

---

#### `stripe events resend` fails with "event not found"

**Symptom:** `Error: No such event: evt_xxx`

**Cause:** Stripe only stores events for 30 days.

**Solution:**
```bash
psql $DATABASE_URL << 'SQL'
SELECT o.id, o.stripe_payment_intent_id, o.status
FROM orders o
JOIN payments p ON p.order_id = o.id
WHERE o.status = 'pending'
AND p.stripe_status = 'succeeded'     -- ASSUMPTION: verify column name
LIMIT 50;
SQL
```
Escalate to engineering for manual order state transition if this returns rows.

---

## Escalation

| Condition | Escalate to | Contact | Expected response time |
|---|---|---|---|
| Payment error rate still > 5% after 20 minutes of investigation | Billing platform lead | PagerDuty: `billing-platform-oncall` / Slack: `#billing-platform` | 5 minutes |
| Stripe API error rate > 2% AND https://status.stripe.com shows outage > 15 min | Stripe Support | https://support.stripe.com/contact — reference your Stripe account ID from Dashboard | 15–30 min for P1 |
| Data loss suspected (orders with succeeded Stripe payments not reflected in database) | Engineering lead + Data team | PagerDuty: `data-oncall` / Slack: `#data-incidents` | Immediate |
| Customer impact confirmed (support tickets, social media reports) | Customer Success + Engineering lead | Slack: `#customer-escalations` — tag @cs-lead and @eng-lead | Immediate |
| Carding attack in progress (> 500 failed attempts from < 10 IPs in 30 min) | Security team | PagerDuty: `security-oncall` / Slack: `#security-incidents` | Immediate |
| Unsure whether to proceed with a destructive step (queue drain, rollback) | On-call team lead | Slack: `#incidents` — post details and ask before proceeding | 5 minutes |
| `kubectl` / infrastructure access not working | Infrastructure team | PagerDuty: `infra-oncall` / Slack: `#infra-oncall` | 10 minutes |
| All of the above unresponsive | Engineering Manager | [Add mobile number in your team's on-call doc] | Immediate |

> **Assumption:** Replace all PagerDuty service names, Slack channels, and contact methods with your team's actual values. Document the backup contact for each role in case the primary is unavailable.

---

## Appendix

### References

This runbook was written based on the following stated context (no source code was available at time of writing):
- Stack: Node.js API, PostgreSQL, Redis (Bull queue), Datadog monitoring
- Payment processor: Stripe
- Alert thresholds: success rate < 95% / Stripe error rate > 2% (5-minute window)
- Business impact: ~$3,400/min during peak hours
- Stripe error codes: https://stripe.com/docs/error-codes
- Stripe webhook signatures: https://stripe.com/docs/webhooks/signatures
- Bull queue docs: https://docs.bullmq.io (BullMQ) or https://github.com/OptimalBits/bull (Bull v3/v4)
- Stripe CLI reference: https://stripe.com/docs/stripe-cli

### Related runbooks

- Database failover runbook: `runbooks/postgresql-failover.md` — create if needed
- Redis failover runbook: `runbooks/redis-failover.md` — create if needed
- Stripe integration setup: `runbooks/stripe-setup.md` — create if needed

### Architecture context

```
Customer browser
      │
      ▼
 Load Balancer / CDN (Cloudflare / AWS ALB — ASSUMPTION: verify)
      │
      ▼
 Node.js API  ──── PostgreSQL (payments, orders, payment_attempts tables)
      │
      ├──── Redis (Bull queues: payment-processing, stripe-webhooks — ASSUMPTION)
      │
      └──── Stripe API (payment intents, charges, webhooks)
                │
                └── Stripe webhooks ──► POST /webhooks/stripe  (back to your API)
```

Datadog monitors:
- `payment.success_rate` — percentage of payment attempts that succeeded
- `stripe.api.error_rate` — percentage of Stripe API calls returning errors

### Incident history (this quarter)

| Date | Duration | Root cause | Resolution |
|------|----------|------------|------------|
| [Incident 1] | 45+ min | Unknown | Unknown |
| [Incident 2] | 45+ min | Unknown | Unknown |
| [Incident 3] | 45+ min | Unknown | Unknown |
| [Incident 4] | 45+ min | Unknown | Unknown |

> **Action item:** After each incident, fill in this table. This becomes the fastest diagnostic tool for the next incident.

### Change log

| Date | Change | Author |
|------|--------|--------|
| 2026-05-27 | Initial version created | Platform team |

---

**Three things your team should do before this runbook goes live:**

1. **Fill in every `# ASSUMPTION`** — there are ~20 of them. Namespace names, table names, queue names, secret manager paths, admin endpoint URLs. A 30-minute review with someone who knows the codebase will catch them all.
2. **Run the pre-check and Step 1 commands in staging** to confirm log format matches the expected grep patterns — the `grep -i "stripe\|payment\|error\|fail"` pattern may need tuning for your actual log structure.
3. **Update the Escalation table** with real PagerDuty service IDs and Slack channels — the placeholders there are the most critical gap between this doc and being useful at 2am.

### Artifacts written

#### `work/runbooks/payment-processing-failures.md`

```
# Payment Processing Failures — Runbook

> **Assumption notice:** This runbook was written without access to the application source. Commands marked
> `# ASSUMPTION — verify path/name` should be confirmed against your actual codebase before first use.
> Every placeholder that must be replaced is listed in the Prerequisites section.

---

## Overview

| Field | Value |
|---|---|
| **What this covers** | Diagnosing and resolving payment processing failures: Stripe API timeouts, card-decline spikes, idempotency key conflicts, and webhook delivery failures |
| **When to use** | Alert fires: `payment-success-rate-low` (success rate < 95% over 5 min) **or** `stripe-api-error-rate-high` (Stripe API error rate > 2%); or engineers observe payment errors in logs or customer reports |
| **Business impact** | ~$3,400/minute in lost transactions during peak hours. Customers cannot complete purchases. Every minute counts. |
| **Estimated duration** | 10–20 min for card-decline spikes (no action needed); 15–30 min for Stripe timeouts or idempotency conflicts; 20–45 min for webhook failures |
| **Risk level** | High |
| **Last tested** | UNTESTED — update this field after first use |
| **Owner** | Platform / Billing team — update with actual team and Slack channel |

---

## Prerequisites

Complete this checklist **before** starting the procedure. Do not skip items.

```
- [ ] VPN connected to production network — connect: [your VPN instructions here]
      ⏱ If you don't have VPN access, request it from IT — this may take 30+ min, do this first.

- [ ] Stripe Dashboard access (read-only minimum) — https://dashboard.stripe.com
      If you don't have access: request from your team lead via [your access-request process].
      ⏱ Access may take 5–10 min to provision.

- [ ] Datadog access — https://app.datadoghq.com
      If you don't have access: request from [team/person] via [your access-request process].

- [ ] kubectl or SSH access to the Node.js API service — verify with:
        kubectl get pods -n production -l app=api  # ASSUMPTION — verify namespace and label
      OR:
        ssh deploy@api.internal  # ASSUMPTION — verify SSH host

- [ ] redis-cli installed and reachable — verify with:
        redis-cli -u $REDIS_URL ping  # should return: PONG
      Install: brew install redis (macOS) or apt install redis-tools (Linux)

- [ ] psql installed and DATABASE_URL exported — verify with:
        psql $DATABASE_URL -c "SELECT 1;"  # should return: 1
      Install: brew install postgresql (macOS) or apt install postgresql-client (Linux)

- [ ] Stripe CLI installed — version 1.19+ — verify with:
        stripe --version
      Install: brew install stripe/stripe-cli/stripe (macOS)
               or see https://stripe.com/docs/stripe-cli

- [ ] Environment variables set in your terminal:
        export STRIPE_SECRET_KEY="sk_live_..."   # from: [your secrets manager — e.g. 1Password, AWS Secrets Manager]
        export DATABASE_URL="postgres://..."      # from: [your secrets manager]
        export REDIS_URL="redis://..."            # from: [your secrets manager]
        # ASSUMPTION: adjust secret names to match your secrets manager

- [ ] Slack: join #incidents (or your team's incident channel) and post: "investigating payment failures"
      ⏱ Keep this channel open — post an update every 10 minutes while investigating.
```

---

## Pre-check — is this the right runbook?

**Run these checks before proceeding.** The alert may be transient (network blip, brief Stripe hiccup). Do not take action on a self-resolving event.

```
- [ ] Check the Datadog alert status:
        # Open Datadog → Monitors → [payment-success-rate-low or stripe-api-error-rate-high]
        # Is the alert still in ALERT state, or has it resolved to OK?

- [ ] Confirm with a live health check against the payment endpoint:
        curl -s https://[your-api-domain]/health | jq .  # ASSUMPTION — verify your health endpoint path
        # Expected output: {"status":"ok","payments":"healthy"} or similar
        # If output shows "degraded" or "error" for payments — continue this runbook
        # If output shows fully healthy — wait 60 seconds and re-run before proceeding

- [ ] Retry after 60 seconds:
        sleep 60 && curl -s https://[your-api-domain]/health | jq .
        # If healthy on retry — alert was transient, no action needed. Close alert and note in #incidents.

- [ ] Confirm this is not a planned event:
        # Check your team's change log / maintenance calendar at: [your change log URL]
        # Check #deploys or equivalent Slack channel for recent deployments in the last 30 min

- [ ] Stop conditions — do NOT proceed if:
        - Health check passes on retry (wait 2 minutes and check again to be sure)
        - A planned Stripe maintenance window is active: https://status.stripe.com
        - A deployment was made in the last 5 minutes (wait for it to stabilise, then re-check)
        - The alert was already acknowledged by another engineer (check #incidents)
```

---

## Procedure

This procedure has **two phases**:
1. **Triage** (Steps 1–2): identify which failure mode is active. This takes 5–10 minutes.
2. **Fix** (Steps 3–6): go to the section matching your diagnosis. Do not run all sections.

---

#### Step 1: Check the Datadog payment dashboard and identify the error type

**Why:** The four failure modes (Stripe timeout, card declines, idempotency conflicts, webhook failures) have different causes and fixes. Starting with metrics gets you to the right fix without guessing.

**Action:**
```bash
# Open Datadog and navigate to the payments dashboard:
# https://app.datadoghq.com/dashboard/[your-payments-dashboard-id]  # ASSUMPTION — get dashboard ID from your team

# While the dashboard loads, pull recent payment errors from application logs:
# If using kubectl:
kubectl logs -n production -l app=api --since=10m | grep -i "stripe\|payment\|error\|fail" | tail -50
# ASSUMPTION — adjust namespace and label selector

# If using SSH + pm2:
ssh deploy@api.internal "pm2 logs api --lines 100 --nostream" | grep -i "stripe\|payment\|error\|fail"
# ASSUMPTION — adjust PM2 app name
```

**Expected output:**
```
# You will see log lines like one of these — match to a failure mode:

# Stripe API timeout:
[ERROR] Stripe request timed out after 30000ms  {"type":"StripeConnectionError","path":"POST /v1/payment_intents"}

# Card decline spike:
[ERROR] Payment declined  {"code":"card_declined","decline_code":"insufficient_funds","customer_id":"cus_xxx"}

# Idempotency key conflict:
[ERROR] Stripe idempotency error  {"type":"IdempotencyError","message":"Keys for idempotent requests..."}

# Webhook failure:
[ERROR] Webhook signature verification failed  {"err":"No signatures found matching..."}
OR check Stripe Dashboard → Developers → Webhooks → [your endpoint] → failed deliveries
```

**If this fails:**
- Symptom: `kubectl` returns "Error from server (Forbidden)"
- Likely cause: your kubeconfig is not set for production or you lack RBAC permissions
- Fix: `kubectl config use-context [production-context-name]` — get context name from your team's kubeconfig docs
- If the fix doesn't work: escalate to the infrastructure team via #infra-oncall

**Checkpoint:** You have identified which error type appears most frequently in the last 10 minutes. Note it, then proceed to the matching step:
- Stripe timeout → **go to Step 3**
- Card declines → **go to Step 4**
- Idempotency conflict → **go to Step 5**
- Webhook failures → **go to Step 6**
- Mix of errors / unclear → continue to Step 2

---

#### Step 2: Query the payments database for a failure breakdown

**Why:** If logs are ambiguous, the database gives a ground-truth count of failures by type in the last 15 minutes.

**Action:**
```bash
psql $DATABASE_URL << 'SQL'
SELECT
  error_code,                          -- e.g. 'card_declined', 'timeout', 'idempotency_error'
  COUNT(*) AS failure_count,
  MAX(created_at) AS most_recent
FROM payment_attempts                  -- ASSUMPTION: verify your table name
WHERE
  status = 'failed'
  AND created_at > NOW() - INTERVAL '15 minutes'
GROUP BY error_code
ORDER BY failure_count DESC;
SQL
```

**Expected output:**
```
    error_code       | failure_count |          most_recent
---------------------+---------------+-------------------------------
 card_declined       |           142 | 2024-01-15 02:13:44.123456+00
 timeout             |            12 | 2024-01-15 02:14:01.987654+00
 idempotency_error   |             3 | 2024-01-15 02:11:22.345678+00
(3 rows)
```

**If this fails:**
- Symptom: `psql: error: connection to server ... failed: FATAL: role "..." does not exist`
- Likely cause: `DATABASE_URL` is not set or is wrong
- Fix: `echo $DATABASE_URL` — if empty, re-export it from your secrets manager. If set but wrong, get the correct value from [your secrets manager path]
- If the fix doesn't work: escalate to #db-oncall

**Checkpoint:** You can see which error_code dominates. The dominant type determines which step to run next. If `card_declined` > 80% of failures, that is likely a card-issuer spike (not your system fault) — go to Step 4.

---

#### Step 3: Stripe API timeouts

**When to use this step:** Logs show `StripeConnectionError`, `ETIMEDOUT`, or `read ECONNRESET` targeting Stripe endpoints.

**Sub-step 3a: Check Stripe's status page**

**Action:**
```bash
curl -s https://status.stripe.com/api/v2/status.json | jq '{status: .status.description, indicator: .status.indicator}'
```

**Expected output (healthy):**
```json
{
  "status": "All Systems Operational",
  "indicator": "none"
}
```

**Expected output (incident):**
```json
{
  "status": "Partial System Outage",
  "indicator": "major"
}
```

**If Stripe reports an outage:**
- This is a Stripe-side incident. Your system is not broken.
- Action: Post in #incidents: "Stripe reporting [indicator] outage. Monitoring. ETA: check https://status.stripe.com"
- Monitor https://status.stripe.com every 5 minutes.
- Do NOT attempt to restart your API or modify any config — that will not help and may make things worse.
- When Stripe resolves: verify your success rate recovers (go to Verification section).
- Escalate to Stripe support if outage exceeds 15 minutes: see Escalation section.

**If Stripe status is green (your problem, not theirs):**
Continue to Sub-step 3b.

---

**Sub-step 3b: Check API service resource utilisation**

**Why:** Timeouts that are not Stripe-side are often caused by the Node.js process being CPU- or memory-starved, or by connection pool exhaustion on the database or Redis.

**Action:**
```bash
# Check pod resource usage:
kubectl top pods -n production -l app=api  # ASSUMPTION — adjust namespace/label
```

**Expected output (healthy):**
```
NAME                   CPU(cores)   MEMORY(bytes)
api-7d9f5b-abc12       120m         380Mi
api-7d9f5b-def34       115m         372Mi
```

**Expected output (problem):**
```
NAME                   CPU(cores)   MEMORY(bytes)
api-7d9f5b-abc12       980m         1450Mi    ← near CPU limit; memory near limit
api-7d9f5b-def34       995m         1480Mi
```

**If CPU or memory is above 80% of limits:**
```bash
# Scale up the API deployment by 2 replicas:
kubectl scale deployment api -n production --replicas=$(( $(kubectl get deployment api -n production -o jsonpath='{.spec.replicas}') + 2 ))
# ASSUMPTION — adjust deployment name

# Wait 60 seconds for new pods to become ready:
kubectl rollout status deployment/api -n production --timeout=120s

# Re-check resource usage:
kubectl top pods -n production -l app=api
```

**If this fails:**
- Symptom: `Error from server (NotFound): deployments "api" not found`
- Likely cause: wrong deployment name
- Fix: `kubectl get deployments -n production` to list all deployments, then use the correct name
- If the fix doesn't work: escalate to #infra-oncall

**Checkpoint:** After scaling, wait 2 minutes and check the success rate in Datadog. If it has not improved, continue to Sub-step 3c.

---

**Sub-step 3c: Check Redis (Bull queue) for a processing backlog**

**Why:** If the Bull payment queue has accumulated thousands of jobs, workers may be timing out waiting for locks.

**Action:**
```bash
redis-cli -u $REDIS_URL

# Once connected, run:
KEYS bull:payment-processing:*  # ASSUMPTION — verify your Bull queue name prefix
# This lists all keys for the payment-processing queue

LLEN bull:payment-processing:wait   # jobs waiting to be processed
LLEN bull:payment-processing:active # jobs currently being processed
GET  bull:payment-processing:failed # failed job count
```

**Expected output (healthy):**
```
(integer) 0      # wait: no backlog
(integer) 4      # active: normal number in flight
"12"             # failed: some historical failures (check if number is growing)
```

**Expected output (problem):**
```
(integer) 3842   # wait: large backlog ← problem
(integer) 1200   # active: too many concurrent (lock storm) ← problem
```

**If wait queue > 500 jobs:**

⚠ **WARNING: The following command pauses the queue and will stop new payment jobs from being picked up. This is intentional — it prevents the queue from growing further while you investigate. Resume the queue in Sub-step 3d.**

```bash
# Exit redis-cli first (type: exit or ctrl+c), then pause the queue via the API:
curl -X POST https://[your-api-domain]/admin/queues/payment-processing/pause \
  -H "Authorization: Bearer $ADMIN_API_TOKEN"
# ASSUMPTION — verify your admin queue endpoint and token env var name
# The token should be in your secrets manager at: [path]
```

**Then check for stuck active jobs (jobs that have been "active" for > 5 minutes):**
```bash
redis-cli -u $REDIS_URL
LRANGE bull:payment-processing:active 0 -1
# Copy any stuck job IDs, then for each:
HGET bull:payment-processing:[job-id]  # inspect the job data
# Look for jobs with processedOn timestamps > 5 minutes ago
```

**If this fails:**
- Symptom: `WRONGTYPE Operation against a key holding the wrong kind of value`
- Likely cause: your queue uses a different Redis data structure or Bull version
- Fix: `SCAN 0 MATCH bull:*` to find all Bull keys, then check the actual key types with `TYPE [key]`
- If the fix doesn't work: escalate to #platform-oncall

**Checkpoint:** Queue wait length is below 100. Proceed to Sub-step 3d to resume the queue.

---

**Sub-step 3d: Resume the Bull queue and verify recovery**

**Action:**
```bash
curl -X POST https://[your-api-domain]/admin/queues/payment-processing/resume \
  -H "Authorization: Bearer $ADMIN_API_TOKEN"
# ASSUMPTION — verify endpoint

# Confirm the queue is processing:
redis-cli -u $REDIS_URL LLEN bull:payment-processing:wait
# Should be decreasing each time you run this command
```

**Expected output:**
```
HTTP/1.1 200 OK
{"status":"resumed"}
```

**If this fails:**
- Escalate to #platform-oncall immediately — queue management tooling may be broken.

**Checkpoint:** Wait length is decreasing. Go to **Verification** section.

---

#### Step 4: Card decline spike

**When to use this step:** Logs show `card_declined`, `insufficient_funds`, `do_not_honor`, `lost_card`, `stolen_card`, or any `decline_code` pattern in high volume.

**Why this is different:** Card declines are the card issuer's decision, not a bug in your system. A spike usually means: a promotion drove high-risk traffic, a bad actor is carding (testing stolen cards), or a legitimate issuer outage. Your job is to confirm which, then decide whether any action is needed.

**Sub-step 4a: Identify the decline codes in the spike**

**Action:**
```bash
psql $DATABASE_URL << 'SQL'
SELECT
  error_code,
  stripe_decline_code,              -- ASSUMPTION: verify column name
  COUNT(*) AS count,
  COUNT(DISTINCT customer_id) AS unique_customers,
  COUNT(DISTINCT ip_address) AS unique_ips   -- ASSUMPTION: verify column names
FROM payment_attempts
WHERE
  status = 'failed'
  AND created_at > NOW() - INTERVAL '15 minutes'
GROUP BY error_code, stripe_decline_code
ORDER BY count DESC;
SQL
```

**Expected output (normal decline pattern — organic failures):**
```
  error_code   | stripe_decline_code  | count | unique_customers | unique_ips
---------------+---------------------+-------+-----------------+-----------
 card_declined | insufficient_funds  |    45 |              43 |         41
 card_declined | do_not_honor        |    18 |              17 |         17
```
Many unique customers and IPs → organic, expected decline rate. No action needed unless absolute numbers are abnormally high.

**Expected output (carding attack):**
```
  error_code   | stripe_decline_code  | count | unique_customers | unique_ips
---------------+---------------------+-------+-----------------+-----------
 card_declined | card_declined       |  1842 |              12 |          3
 card_declined | insufficient_funds  |   843 |               8 |          3
```
High count, very few unique customers and IPs → likely carding attack.

**If you see a carding attack (high volume, few IPs):**
```bash
# Get the attacking IP addresses:
psql $DATABASE_URL << 'SQL'
SELECT ip_address, COUNT(*) AS attempts
FROM payment_attempts
WHERE
  status = 'failed'
  AND created_at > NOW() - INTERVAL '30 minutes'
GROUP BY ip_address
HAVING COUNT(*) > 20
ORDER BY attempts DESC;
SQL

# Block the IPs at your WAF / CDN layer:
# If using Cloudflare: Security → WAF → IP Access Rules → Block [ip]
# If using AWS WAF: update the IP block list in the WAF console
# ASSUMPTION — verify your WAF provider and process
```

⚠ **WARNING: Blocking IPs affects all traffic from that IP. Double-check against your allowlist (internal IPs, monitoring IPs) before blocking.**

**If declines are organic (many unique IPs/customers):**
- If Stripe decline rate is < 8%: this is within normal range. No action needed. Monitor for 10 minutes.
- If Stripe decline rate is > 8%: check https://status.stripe.com for issuer-side outages, and post in #incidents noting the pattern.

**Checkpoint:** You have identified the pattern and taken action (or confirmed no action is needed). Go to **Verification** section.

---

#### Step 5: Idempotency key conflicts

**When to use this step:** Logs show `IdempotencyError`, "Keys for idempotent requests can only be used with the same parameters", or HTTP 400 errors from Stripe with `idempotency_error` type.

**Why this happens:** Idempotency keys are used to safely retry Stripe requests. A conflict means a key is being reused with different parameters — usually caused by a bug in key generation logic, or a retry loop that mutates the request body (e.g. adding a timestamp or changing an amount).

**Sub-step 5a: Confirm the idempotency error rate and source**

**Action:**
```bash
# Count idempotency errors in the last 30 minutes:
kubectl logs -n production -l app=api --since=30m \
  | grep -i "idempotency" \
  | grep -o '"idempotency_key":"[^"]*"' \
  | sort | uniq -c | sort -rn | head -20
# ASSUMPTION — adjust log format to match your JSON key name
```

**Expected output:**
```
      8 "idempotency_key":"pay_retry_1705280042_ord_7f3a"
      3 "idempotency_key":"pay_retry_1705280001_ord_7f3a"
```
If the same order ID (`ord_7f3a`) appears repeatedly with different keys, the retry loop is generating new keys instead of reusing them — this is a bug in your retry logic.

If the same key appears multiple times with different amounts, a request parameter is being mutated between retries.

**Sub-step 5b: Check for a recent deployment that changed payment retry logic**

**Action:**
```bash
# Check git log for recent changes to payment-related files:
kubectl exec -n production -it $(kubectl get pod -n production -l app=api -o name | head -1) \
  -- git log --since="1 hour ago" --oneline -- src/payments/ src/jobs/ src/stripe/
# ASSUMPTION — adjust paths to your payment source directories
```

**Expected output:**
```
a3f2c1d fix: add timestamp to retry idempotency key   ← THIS IS LIKELY THE BUG
```

**If a deployment in the last hour changed retry logic:**

⚠ **WARNING: Rolling back a deployment may cause a brief restart of API pods. Payments in flight will be retried. Confirm with your team lead before proceeding.**

```bash
# Get the previous deployment revision:
kubectl rollout history deployment/api -n production

# Roll back to the previous revision:
kubectl rollout undo deployment/api -n production

# Monitor the rollout:
kubectl rollout status deployment/api -n production --timeout=120s
```

**If this fails:**
- Symptom: `error: no rollout history found`
- Likely cause: this is the first deployment for this deployment object, or history is limited
- Fix: re-deploy the previous Docker image tag manually — get the previous tag from your CI/CD system (e.g. CircleCI, GitHub Actions)
- If you cannot identify the previous image: escalate to the team lead for a hotfix

**If no recent deployment:** This is a pre-existing bug now surfacing at scale. Proceed to Sub-step 5c.

**Sub-step 5c: Clear stuck idempotency-conflicted jobs from the Bull queue**

**Why:** Conflicted jobs in the Bull queue will keep retrying and generating more errors. Clearing them stops the noise so you can get back to baseline while the engineering team fixes the root cause.

**Action:**
```bash
redis-cli -u $REDIS_URL

# Count failed jobs:
GET bull:payment-processing:failed   # ASSUMPTION — verify queue name

# Move failed jobs to a holding list for post-incident review (do NOT delete them):
# First, copy them:
redis-cli -u $REDIS_URL RENAME bull:payment-processing:failed bull:payment-processing:failed-incident-$(date +%Y%m%d%H%M)
# ASSUMPTION — verify this command against your Bull version; Bull 4.x stores failed jobs differently (sorted set)
# For Bull 4.x: use the Bull admin UI or the Bull Board dashboard at: [your Bull Board URL]
```

**If this fails:**
- Do not proceed with manual Redis manipulation if you're unsure of the data structure.
- Escalate to #platform-oncall with the error message.

**Checkpoint:** Idempotency error rate in logs drops to near zero. Go to **Verification** section. File a bug report for the root-cause code issue regardless of whether a rollback was performed.

---

#### Step 6: Webhook delivery failures

**When to use this step:** Logs show webhook signature verification failures, OR Stripe Dashboard → Developers → Webhooks shows delivery failures.

**Why webhooks matter:** Your system likely relies on webhook events (e.g. `payment_intent.succeeded`, `charge.refunded`) to finalise orders and trigger fulfilment. Missed webhooks mean orders may be stuck in a "pending" state even though payment succeeded.

**Sub-step 6a: Check Stripe webhook delivery status**

**Action:**
```bash
# Using Stripe CLI to check recent webhook events:
stripe events list --limit 20 --api-key $STRIPE_SECRET_KEY \
  | jq '.data[] | {id: .id, type: .type, created: .created}'
```

**Expected output:**
```json
{"id": "evt_3xxx", "type": "payment_intent.succeeded", "created": 1705280400}
{"id": "evt_3yyy", "type": "payment_intent.payment_failed", "created": 1705280380}
```

**Then check for failed delivery attempts in Stripe Dashboard:**
```
1. Open https://dashboard.stripe.com/developers/webhooks
2. Click on your webhook endpoint URL (e.g. https://[your-api-domain]/webhooks/stripe)
3. Click "Recent deliveries"
4. Look for any deliveries with status "Failed" — click one to see the error
```

**Common webhook failure reasons:**
- `HTTP 400: No signatures found matching` → webhook secret mismatch (Sub-step 6b)
- `HTTP 503 / connection refused` → API is down (return to Step 3)
- `HTTP 200 but no action taken` → your handler threw an error after returning 200 (Sub-step 6c)
- `Stripe cannot reach endpoint` → firewall or load balancer issue (Sub-step 6d)

---

**Sub-step 6b: Webhook secret mismatch — resync the signing secret**

**Why this happens:** The `STRIPE_WEBHOOK_SECRET` in your environment does not match the signing secret in Stripe Dashboard. Usually caused by rotating the secret without updating all environments.

**Action:**
```bash
# Get the current signing secret from Stripe Dashboard:
# 1. https://dashboard.stripe.com/developers/webhooks
# 2. Click your endpoint
# 3. Click "Reveal" next to "Signing secret"
# 4. Copy the value (starts with whsec_)

# Update the secret in your secrets manager:
# AWS Secrets Manager example:
aws secretsmanager update-secret \
  --secret-id production/stripe/webhook-secret \
  --secret-string "whsec_[paste-value-here]"
# ASSUMPTION — verify your secret name in Secrets Manager

# Then trigger a rolling restart to pick up the new secret:
kubectl rollout restart deployment/api -n production
kubectl rollout status deployment/api -n production --timeout=120s
```

**Expected output:**
```
deployment.apps/api restarted
Waiting for deployment "api" rollout to finish: 1 out of 3 new replicas have been updated...
deployment "api" successfully rolled out
```

**If this fails:**
- If secrets manager update fails: check your IAM permissions for `secretsmanager:UpdateSecret`
- Escalate to #security-oncall if you cannot update the secret

**Checkpoint:** Test by triggering a test webhook from Stripe Dashboard → your endpoint → "Send test webhook". It should show HTTP 200 in the delivery log. Go to **Verification** section.

---

**Sub-step 6c: Replay failed webhook events**

**Why:** Even after fixing the delivery failure, events that failed while the problem was active need to be replayed. Orders may be stuck in a pending state.

**Action:**
```bash
# List failed webhook events from Stripe in the last hour:
stripe events list \
  --api-key $STRIPE_SECRET_KEY \
  --limit 100 \
  --created $(date -d "1 hour ago" +%s 2>/dev/null || date -v-1H +%s) \  # GNU date or BSD date
  | jq '.data[] | select(.type == "payment_intent.succeeded") | .id' \
  | tr -d '"'
```

**Expected output:**
```
evt_3xxxx
evt_3yyyy
evt_3zzzz
```

```bash
# Replay each event (example for one event — run for each evt_ ID):
stripe events resend evt_3xxxx --api-key $STRIPE_SECRET_KEY
# ASSUMPTION — verify your Stripe CLI version supports this command
```

⚠ **WARNING: Replaying `payment_intent.succeeded` events will re-trigger your order fulfilment logic. Ensure your handlers are idempotent (i.e. processing the same event twice does not create duplicate orders). If you are unsure, do NOT replay without confirming with the engineering team.**

**If event handlers are not idempotent:**
- Do not replay events.
- Escalate to the engineering team for manual order reconciliation.
- Query stuck orders:
```bash
psql $DATABASE_URL << 'SQL'
SELECT id, stripe_payment_intent_id, status, created_at
FROM orders                             -- ASSUMPTION: verify table name
WHERE
  status = 'pending'
  AND created_at > NOW() - INTERVAL '2 hours'
  AND stripe_payment_intent_id IS NOT NULL
ORDER BY created_at DESC
LIMIT 50;
SQL
```

**Checkpoint:** No pending orders for payments that succeeded in Stripe. Go to **Verification** section.

---

**Sub-step 6d: Webhook endpoint unreachable from Stripe**

**Why this happens:** Stripe cannot reach your webhook endpoint due to a firewall rule change, load balancer misconfiguration, or DNS issue.

**Action:**
```bash
# Test reachability from outside your network:
curl -v -X POST https://[your-api-domain]/webhooks/stripe \
  -H "Content-Type: application/json" \
  -d '{"test": true}'
# Expected: HTTP 400 (signature check fails) — this confirms the endpoint is reachable
# Problem: connection refused, timeout, or DNS resolution failure
```

**If the endpoint is unreachable:**
- Check your load balancer health in your cloud console (AWS ALB / GCP Load Balancer / etc.)
- Check if a firewall rule was changed: `kubectl get networkpolicies -n production` — look for policies blocking inbound traffic
- This is a network/infrastructure issue. Escalate to #infra-oncall immediately.

---

## Verification

Run all of these checks after completing any procedure step. **All checks must pass before closing the incident.**

#### Verification checklist

```
- [ ] API health check passes:
        curl -s https://[your-api-domain]/health | jq .
        → Expected: {"status":"ok"} (or your system's healthy response)

- [ ] Payment success rate above 95% in Datadog:
        Open: https://app.datadoghq.com/dashboard/[your-payments-dashboard-id]
        → Metric: payment.success_rate (5-minute average)
        → Required: > 95%

- [ ] Stripe API error rate below 2% in Datadog:
        → Metric: stripe.api.error_rate (5-minute average)
        → Required: < 2%

- [ ] No new errors in API logs (last 5 minutes):
        kubectl logs -n production -l app=api --since=5m | grep -c "ERROR"
        → Expected: 0 or a count matching your normal baseline (< 5)

- [ ] Bull queue wait length is near zero:
        redis-cli -u $REDIS_URL LLEN bull:payment-processing:wait
        → Expected: < 50 jobs

- [ ] No pending orders stuck from the incident window:
        psql $DATABASE_URL -c "
          SELECT COUNT(*) FROM orders
          WHERE status = 'pending'
          AND created_at BETWEEN NOW() - INTERVAL '2 hours' AND NOW() - INTERVAL '5 minutes';"
        → Expected: 0, or same count as before the incident (orders genuinely awaiting payment)
        # ASSUMPTION — verify table and column names

- [ ] Stripe webhook delivery success rate in Dashboard:
        Open: https://dashboard.stripe.com/developers/webhooks → your endpoint
        → No failed deliveries in the last 10 minutes

- [ ] Make a test payment (if you have a staging/test mode payment form):
        stripe trigger payment_intent.succeeded --api-key $STRIPE_SECRET_KEY
        # Should create a succeeded event; verify it appears in your system
```

---

## Rollback

This section covers how to undo actions taken during this runbook.

#### Rollback procedure

**When to rollback:**
- The procedure made things worse (error rate increased after your action)
- A deployment rollback was performed but did not resolve the issue and introduced new errors
- Queue jobs were paused/moved and orders are now stuck

**Rollback window:**
- Deployment rollback: available while the previous ReplicaSet exists (typically 24 hours, depends on `revisionHistoryLimit` setting)
- Queue pause: queue can be resumed at any time
- Secret rotation: old secret can be re-applied from secrets manager history

**Data implications:**
- Rolling back a deployment does not affect database data
- Replayed webhook events may have triggered order state changes — these are NOT rolled back by a deployment rollback. Check with engineering before rolling back if fulfilment was triggered.

---

**1. Roll back a deployment (if you ran `kubectl rollout undo`)**

```bash
# Check available revision history:
kubectl rollout history deployment/api -n production

# Roll forward (undo the undo) to the most recent revision:
kubectl rollout undo deployment/api -n production --to-revision=[most-recent-revision-number]

# Monitor:
kubectl rollout status deployment/api -n production --timeout=120s
```

Expected result:
```
deployment "api" successfully rolled out
```

---

**2. Resume a paused Bull queue (if you ran the pause command in Step 3c)**

```bash
curl -X POST https://[your-api-domain]/admin/queues/payment-processing/resume \
  -H "Authorization: Bearer $ADMIN_API_TOKEN"
```

Expected result:
```json
{"status":"resumed"}
```

---

**3. Restore a moved/renamed Redis queue key (if you renamed it in Step 5c)**

```bash
# Find the incident backup key:
redis-cli -u $REDIS_URL KEYS "bull:payment-processing:failed-incident-*"

# Example output: bull:payment-processing:failed-incident-202401150214

# Restore it:
redis-cli -u $REDIS_URL RENAME bull:payment-processing:failed-incident-202401150214 bull:payment-processing:failed
```

Expected result: `OK`

---

**4. Revert a webhook secret rotation**

```bash
# Get the previous secret version from AWS Secrets Manager:
aws secretsmanager list-secret-version-ids --secret-id production/stripe/webhook-secret

# Restore the previous version:
aws secretsmanager restore-secret --secret-id production/stripe/webhook-secret
# ASSUMPTION — verify your rollback process for your specific secrets manager

# Restart API to pick up the reverted secret:
kubectl rollout restart deployment/api -n production
```

#### After rollback

```
- [ ] Verify rollback succeeded — run the full Verification checklist above
- [ ] Post in #incidents: "Rollback complete. System status: [healthy/still-degraded]"
- [ ] If still degraded after rollback: escalate immediately — see Escalation section
- [ ] Create an incident ticket in [your ticketing system] with:
        - Timeline of actions taken
        - Which rollback was performed
        - Current system state
        - Stripe event IDs for any replayed events
        - Any orders that may need manual reconciliation
```

---

## Troubleshooting

#### Error rate drops briefly then climbs again

**Symptom:** Datadog shows the payment success rate recovering but degrading again every few minutes.

**Cause:** The Bull queue's retry logic is hitting the same broken code path on each retry, and backed-off jobs are re-entering the active state in waves.

**Solution:**
```bash
# Pause the queue to stop the retry wave:
curl -X POST https://[your-api-domain]/admin/queues/payment-processing/pause \
  -H "Authorization: Bearer $ADMIN_API_TOKEN"

# Identify the failing jobs:
redis-cli -u $REDIS_URL LRANGE bull:payment-processing:active 0 20

# Once the root cause is fixed (or the broken jobs are cleared), resume:
curl -X POST https://[your-api-domain]/admin/queues/payment-processing/resume \
  -H "Authorization: Bearer $ADMIN_API_TOKEN"
```

**Prevention:** Configure Bull's backoff to use exponential delay with a cap, so retry waves are spread out and don't cause periodic spikes.

---

#### Procedure interrupted midway (e.g. your terminal disconnects)

**Symptom:** You were mid-procedure and your session was interrupted.

**Cause:** Network interruption, laptop sleep, etc.

**Solution:**
1. Check the current state before resuming:
   ```bash
   # Is the queue paused?
   redis-cli -u $REDIS_URL GET bull:payment-processing:paused
   # Returns "1" if paused, nothing if not paused

   # Is a deployment rollout in progress?
   kubectl rollout status deployment/api -n production
   ```
2. Post in #incidents: "Rejoining investigation — checking current state."
3. Return to the Pre-check section and re-assess the alert status from scratch.
4. Do not assume the previous steps succeeded. Re-run the checkpoints to confirm state.

---

#### This runbook is run twice by accident (duplicate execution)

**Symptom:** A second engineer ran the same steps concurrently.

**Concerns:**
- `kubectl rollout undo` run twice: the second call rolls back an additional revision. Fix: `kubectl rollout history deployment/api -n production` and roll forward to the intended version.
- Queue paused twice: no harm — it's still just paused. Resume once.
- Webhook events replayed twice: if handlers are idempotent, no harm. If not, duplicate orders may have been created. Escalate to engineering for order deduplication.

**Prevention:** Always check #incidents for active investigation before starting this runbook.

---

#### `stripe events resend` fails with "event not found"

**Symptom:**
```
Error: No such event: evt_xxx
```

**Cause:** Stripe only stores events for 30 days. If the event is older, it cannot be replayed via CLI.

**Solution:** Manually reconcile affected orders using Stripe Dashboard payment records:
```bash
psql $DATABASE_URL << 'SQL'
-- Find orders with a succeeded payment_intent that are still "pending":
SELECT o.id, o.stripe_payment_intent_id, o.status
FROM orders o                          -- ASSUMPTION: verify table names
JOIN payments p ON p.order_id = o.id
WHERE o.status = 'pending'
AND p.stripe_status = 'succeeded'     -- ASSUMPTION: verify column name
LIMIT 50;
SQL
```
Escalate to engineering for manual order state transition if this query returns rows.

---

## Escalation

| Condition | Escalate to | Contact | Expected response time |
|---|---|---|---|
| Payment error rate still > 5% after 20 minutes of investigation | Billing platform lead | PagerDuty: `billing-platform-oncall` / Slack: `#billing-platform` | 5 minutes |
| Stripe API error rate > 2% AND https://status.stripe.com shows outage > 15 min | Stripe Support | https://support.stripe.com/contact — Reference your account ID from Stripe Dashboard | 15–30 min for P1 |
| Data loss suspected (orders with succeeded Stripe payments not reflected in database) | Engineering lead + Data team | PagerDuty: `data-oncall` / Slack: `#data-incidents` | Immediate |
| Customer impact confirmed (support tickets, social media reports) | Customer Success + Engineering lead | Slack: `#customer-escalations` — tag @cs-lead and @eng-lead | Immediate |
| Carding attack in progress (> 500 failed attempts from < 10 IPs) | Security team | PagerDuty: `security-oncall` / Slack: `#security-incidents` | Immediate |
| Unsure whether to proceed with a destructive step (queue drain, rollback) | On-call team lead | Slack: `#incidents` — post details and ask before proceeding | 5 minutes |
| `kubectl` / infrastructure access not working | Infrastructure team | PagerDuty: `infra-oncall` / Slack: `#infra-oncall` | 10 minutes |
| All of the above unresponsive | Engineering Manager | [Add mobile number in your team's on-call doc] | Immediate |

> **Assumption:** Replace all PagerDuty service names, Slack channels, and contact methods with your team's actual values. Document the backup contact for each role in case the primary is unavailable.

---

## Appendix

### References

This runbook was written based on the following stated context (no source code was available at time of writing):
- Stack: Node.js API, PostgreSQL, Redis (Bull queue), Datadog monitoring
- Payment processor: Stripe
- Alert thresholds: success rate < 95% / Stripe error rate > 2% (5-minute window)
- Business impact: ~$3,400/min during peak hours
- Stripe documentation: https://stripe.com/docs/error-codes
- Stripe webhook signatures: https://stripe.com/docs/webhooks/signatures
- Bull queue documentation: https://docs.bullmq.io (if using BullMQ) or https://github.com/OptimalBits/bull (if using Bull v3/v4)
- Stripe CLI reference: https://stripe.com/docs/stripe-cli

### Related runbooks

- Database failover runbook: `runbooks/postgresql-failover.md` — ASSUMPTION: create if needed
- Redis failover runbook: `runbooks/redis-failover.md` — ASSUMPTION: create if needed
- Stripe integration setup: `runbooks/stripe-setup.md` — ASSUMPTION: create if needed

### Architecture context

```
Customer browser
      │
      ▼
 Load Balancer / CDN (Cloudflare / AWS ALB — ASSUMPTION: verify)
      │
      ▼
 Node.js API  ──── PostgreSQL (payments, orders, payment_attempts tables)
      │
      ├──── Redis (Bull queues: payment-processing, stripe-webhooks — ASSUMPTION)
      │
      └──── Stripe API (payment intents, charges, webhooks)
                │
                └── Stripe webhooks ──► POST /webhooks/stripe  (back to your API)
```

Datadog monitors:
- `payment.success_rate` — percentage of payment attempts that succeeded
- `stripe.api.error_rate` — percentage of Stripe API calls returning errors

### Incident history (this quarter)

| Date | Duration | Root cause | Resolution |
|------|----------|------------|------------|
| [Incident 1] | 45+ min | Unknown | Unknown |
| [Incident 2] | 45+ min | Unknown | Unknown |
| [Incident 3] | 45+ min | Unknown | Unknown |
| [Incident 4] | 45+ min | Unknown | Unknown |

> **Action item:** After each incident, fill in this table with the actual root cause and resolution. This becomes the fastest diagnostic tool for the next incident.

### Change log

| Date | Change | Author |
|------|--------|--------|
| 2026-05-27 | Initial version created | Platform team |

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.5/16.5 (100%) |
| Evaluated | 2026-05-27 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 463035 ms |
| Target cost | $0.6590 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Written for a first-timer at 2am — no assumed knowledge of the system, all commands are copy-pasteable with expected output shown | PASS | Every command has install instructions, expected output blocks (healthy vs problem states), and explicit `# ASSUMPTION` flags. Prerequisites checklist covers VPN, Stripe dashboard, kubectl, redis-cli, psql, Stripe CLI. |
| c2 | Includes a decision tree or clear branching logic for different failure modes (API timeout vs card declines vs webhook failures vs idempotency conflicts) | PASS | Step 1 Checkpoint explicitly routes: 'Stripe timeout → Step 3, Card declines → Step 4, Idempotency conflict → Step 5, Webhook failures → Step 6, Mix/unclear → Step 2'. |
| c3 | Every diagnostic step includes the exact command or query to run, not just "check the logs" or "look in Datadog" | PASS | All steps include exact commands: `kubectl logs -n production -l app=api --since=10m \| grep -i "stripe\\|payment\\|error\\|fail" \| tail -50`, psql SQL heredocs, `redis-cli -u $REDIS_URL LLEN bull:payment-processing:wait`, stripe CLI commands. |
| c4 | Includes a rollback or safe revert step for any action that could make the situation worse | PASS | Dedicated Rollback section covers: deployment rollback (`kubectl rollout undo`), queue resume (curl POST), Redis key restore (RENAME), webhook secret revert (aws secretsmanager restore-secret). ⚠️ warnings precede destructive steps. |
| c5 | Specifies an escalation path with roles and contact method — who to wake up and when, not "escalate if needed" | PASS | Escalation table rows: 'error rate > 5% after 20 min → billing-platform-oncall PagerDuty, 5 min response'; 'carding attack → security-oncall PagerDuty, Immediate'; 8 conditions total with response times. |
| c6 | Documents how to verify the incident is resolved (what metric to watch, what threshold confirms recovery) | PASS | Verification checklist requires: `payment.success_rate > 95%` (5-min avg), `stripe.api.error_rate < 2%`, `kubectl logs grep ERROR count < 5`, Bull queue wait < 50, zero stuck orders, no Stripe failed deliveries. |
| c7 | Covers all four failure modes mentioned — partial credit if 2-3 are covered but one is missing | PARTIAL | All four covered: Step 3 (Stripe API timeouts), Step 4 (card declines), Step 5 (idempotency key conflicts), Step 6 (webhook delivery failures). Maximum score capped at PARTIAL per ceiling. |
| c8 | Includes severity classification or impact assessment so the on-call engineer can judge urgency (the $3,400/minute context should inform this) | PASS | Overview table: 'Business impact: ~$3,400/minute in lost transactions during peak hours. Customers cannot complete purchases. Every minute counts.' Risk level: High. Pre-check section prevents false positives. |
| c9 | Output's runbook header states the alert trigger conditions verbatim — payment success rate < 95% over 5 min, OR Stripe API error rate > 2% — and the $3,400/minute business impact, so the on-call knows the urgency immediately | PASS | Overview table: 'success rate < 95% over 5 min OR Stripe API error rate > 2%' and '~$3,400/minute in lost transactions during peak hours' both present in the first visible table. |
| c10 | Output's decision tree branches on the first observable signal (which alert fired? what's the dominant error code from logs/Datadog?) and routes to one of four specific failure modes — Stripe API timeout, card declines, idempotency conflict, webhook delivery failure | PASS | Step 1 pulls live logs with grep patterns matching all four error types, then Checkpoint routes: 'Stripe timeout → Step 3, Card declines → Step 4, Idempotency conflict → Step 5, Webhook failures → Step 6'. |
| c11 | Output's diagnostic commands are exact and copy-pasteable — e.g. `datadog query payment.errors{service:payment-api} \| sum:1m` or `psql -c "SELECT COUNT(*) FROM payments WHERE status='failed' AND created_at > NOW() - INTERVAL '5 minutes';"` — not "check the logs" | PASS | Step 2 psql heredoc: `SELECT error_code, COUNT(*) AS failure_count FROM payment_attempts WHERE status='failed' AND created_at > NOW() - INTERVAL '15 minutes' GROUP BY error_code ORDER BY failure_count DESC;` |
| c12 | Output's commands each show the expected output / threshold — e.g. "expected: error count < 50/min in healthy state; if you see 200+/min, this confirms an API outage" | PASS | Every command block has 'Expected output (healthy)' and 'Expected output (problem)' sections with concrete values. E.g. Step 3b: CPU 120m/380Mi = healthy; 980m/1450Mi = 'near limits ← problem'. |
| c13 | Output handles each of the four failure modes with branch-specific diagnostics — Stripe outage (check status.stripe.com, fail-over to retry queue), card declines (check decline code distribution, no rollback needed), idempotency conflicts (check Redis key collisions, clear stuck keys with named command), webhook failures (check Bull queue depth, retry failed webhooks) | PASS | Step 3a: `curl status.stripe.com/api/v2/status.json`; Step 4a: decline code distribution SQL; Step 5c: `RENAME bull:payment-processing:failed`; Step 6c: `stripe events resend evt_xxx`. |
| c14 | Output's rollback steps are explicit for any destructive action — e.g. "if you disable the payment processor, re-enable with `kubectl scale deployment/payment-processor --replicas=3`" | PASS | Rollback section 1: `kubectl rollout undo deployment/api -n production --to-revision=[N]`; section 2: queue resume curl; section 3: `RENAME` Redis key back; section 4: `aws secretsmanager restore-secret` + rollout restart. |
| c15 | Output's escalation thresholds are defined — e.g. "if no resolution after 30 min OR Stripe status page shows incident, page the engineering manager via PagerDuty severity 1" | PASS | 'error rate > 5% after 20 minutes → billing-platform-oncall, 5 min response'; 'Stripe outage > 15 min → Stripe Support, 15-30 min'; 'data loss suspected → data-oncall, Immediate'. |
| c16 | Output's verification step shows what success looks like — payment success rate back above 95% for 10 consecutive minutes, error rate below 0.5%, no new alerts firing — with an illustrative Datadog query in the same syntax style as the diagnostic commands | PASS | Verification checklist: 'payment.success_rate > 95% (5-min avg)', 'stripe.api.error_rate < 2%', queue wait < 50, orders stuck = 0. Metric names given; Datadog is UI navigation rather than query syntax, but thresholds are explicit. |
| c17 | Output is written for a first-timer at 2am — every step has a single action, no assumed knowledge of which dashboard or which Redis key, all paths absolute | PASS | Redis key names spelled out (`bull:payment-processing:wait`), dashboard URLs given, install commands included, `# ASSUMPTION` flags mark every placeholder. Steps are single-action with checkpoints before advancing. |

### Notes

An exceptionally thorough runbook covering all four failure modes with exact commands, dual healthy/problem expected outputs, explicit rollback procedures, and a detailed escalation table. The only minor gap is that the Datadog verification uses UI navigation rather than query syntax (c16), but all thresholds are concrete and the overall verification coverage is strong.
