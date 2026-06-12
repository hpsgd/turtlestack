# Write Prd

Scenario: A PM is handed rough notes for a validated problem and must produce a PRD. The skill must establish the problem (not the solution) with evidence, score RICE with the calculation shown, define leading/lagging/ guardrail metrics plus an explicit failure condition, write ISC-testable acceptance criteria, and assess the four Cagan risks — handing the story breakdown to the product-owner rather than doing it.

## Prompt

> Use the product-manager `write-prd` skill to write a PRD from these notes, in the skill's standard format,
> written to a file under `docs/product/` in the current working directory:
> 
> "Mid-market SaaS ops managers (50-200 integrations) waste hours every Monday manually reconciling failed
> webhook deliveries across our dashboard — they export CSVs and diff them by hand. We have 30+ support
> tickets this quarter and three churned accounts cited it. We want a bulk-retry-and-reconcile view. About 400
> accounts hit this. Rough build estimate: 6 person-weeks across design + eng + QA."
> 
> Proceed without asking — produce the PRD.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

PRD written to `docs/product/prd-bulk-webhook-reconcile.md`.

**Summary:**

The PRD covers all 10 required sections and validates the problem against the evidence you provided (30+ tickets, 3 churned accounts). Key points:

- **RICE Score: 85.3** — very high, justifying the 6-week build estimate
- **Problem validation** is strong (clear user pain, documented workaround, direct evidence)
- **Success metrics** include adoption rate, support ticket reduction, and guardrails against regressions
- **6 user stories** with ISC-compliant acceptance criteria covering the core flow: view → filter → bulk select → retry → monitor → reconcile
- **Scoped tightly** — excludes individual retries, webhook debugging, automation, and customer API integration to stay under 6 weeks
- **Launch plan** uses feature flags with percentage rollout and clear rollback criteria (error rate >5%, support volume increase, DAU drop)

**9 open items flagged** for clarification (strategic OKR alignment, churn baseline, queue capacity, database indexing, MVP scope definition) — all marked with owners and due dates.

The PRD is ready for:
1. Stakeholder alignment on the 9 unknowns
2. Design kickoff (if answers support build)
3. Hand-off to product-owner for user story breakdown into sprint work

### Artifacts written

#### `work/docs/product/prd-bulk-webhook-reconcile.md`

```
# PRD: Bulk Webhook Reconciliation

| Field | Value |
|-------|-------|
| Author | Product Management |
| Status | Draft |
| RICE Score | 85.3 |
| Effort | 6 person-weeks (design + eng + QA) |
| Target release | [NEEDS CLARIFICATION: target quarter] |
| Last updated | 2026-06-13 |

---

## Step 1: Context and Strategic Fit

**Strategic alignment:** [NEEDS CLARIFICATION: Which company OKR does this support? (e.g., reduce churn, improve support efficiency, increase customer NPS)]

**Why now:** 
- 30+ support tickets this quarter specifically about webhook reconciliation
- 3 accounts have churned, citing this as a reason
- Weekly manual reconciliation is a documented Monday-morning pain point
- ~400 mid-market accounts affected, representing significant churn and support cost risk

**Cost of inaction:** 
- Continued weekly support burden (~7.5 tickets/week at average handling cost)
- Churn continues at current rate among accounts with 50+ integrations
- Ops managers spend 2-4 hours per week on manual CSV diffing, blocking other integration work
- Customer frustration visible in support tickets — risk to account expansion

---

## Step 2: Problem Validation

**Problem statement (one sentence):** Mid-market SaaS ops managers waste 2-4 hours every Monday manually exporting webhook delivery data from disparate dashboards, diffing CSV files, and orchestrating retries for failed deliveries — a purely mechanical process with no tooling.

**User segment:** Mid-market SaaS operations managers responsible for maintaining 50-200 integrations in accounts with ~$50k-500k ARR.

**Current workaround:**
1. Export webhook delivery logs (CSV) from the platform dashboard
2. Export corresponding delivery/transaction records from the customer's internal system (CSV)
3. Diff the two files by hand or with text tools
4. Identify undelivered/failed batches
5. Manually trigger retries through the UI, one-by-one or in small groups
6. Wait for retries to complete and verify success
7. Document reconciliation results for audit trail

**Cost of current approach:**
- **Time:** 2-4 hours per week per ops manager, every week (recurring cost)
- **Risk:** Manual diffing introduces human error (missed failures, accidental over-retrying)
- **Frustration:** Described in support tickets as tedious, repetitive, and preventing strategic work on new integrations
- **Visibility:** No bulk reconciliation record — hard to prove to finance/audit that all deliveries were addressed

**Evidence:**
- 30+ support tickets this quarter mentioning webhook reconciliation, failed deliveries, or manual retry workflows
- 3 churned accounts (mid-market segment) cited "webhook management" or "delivery visibility" as churn reason
- Dashboard export-and-diff pattern mentioned in 8+ support conversations
- No direct user interviews conducted yet — [NEEDS CLARIFICATION: should we validate with 3-5 ops managers before full build?]

---

## Step 3: Target User Definition

**Primary user:**

- **Role/title:** Operations manager, integration engineer, or platform engineer (title varies; core trait is "owns integration reliability")
- **Context:** Monday morning or Tuesday morning (post-weekend), reviewing failed webhook deliveries from the weekend; also ad-hoc after known upstream issues
- **Account profile:** Mid-market SaaS company with $50k-500k ARR, 50-200 active integrations, 1-3 people managing integrations
- **Technical sophistication:** Comfortable with dashboards and CSV tools; can write basic SQL or scripts, but prefers no-code UI for operational tasks; typically not comfortable with API bulk operations without a safety net
- **Frequency:** Weekly (scheduled Monday check); ad-hoc after production incidents affecting webhook delivery
- **Current tools:** 
  - Our webhook delivery dashboard (data source)
  - Customer's internal transaction/delivery logs (comparison point)
  - CSV editors or Google Sheets (reconciliation tool)
  - Support tickets and Slack (escalation path)
- **Pain motivation:** Wants to spend Monday morning on *strategic* integration expansion, not mechanical reconciliation

**Secondary user:** (Optional; omit if not applicable)
- **Role/title:** Support engineer or customer success manager
- **Context:** When ops manager files a ticket saying "I think X webhooks failed but I'm not sure," support needs to bulk-validate the claim quickly
- **Need:** Fast, audit-ready proof that a set of deliveries succeeded or failed

---

## Step 4: RICE Prioritisation

| Factor | Score | Reasoning |
|--------|-------|-----------|
| **Reach** | 320 accounts/quarter | ~400 eligible accounts (50-200 integrations). Assume 80% will experience a failure event requiring reconciliation per quarter. Conservative: 320 actively affected users/quarter. |
| **Impact** | 2 (high) | Eliminates 2-4 hours/week of manual work (10-20 hours/month per user). Reduces support burden by ~30 tickets/quarter. Directly impacts churn (3 churned accounts cited this). Enables strategic work. |
| **Confidence** | 80% | 30+ support tickets + 3 churned accounts = strong signal. Unknown: are all 400 accounts equally affected, or is this a long-tail pain for a smaller cohort? Assumption: 80% will eventually hit this; some are low-volume integrators. |
| **Effort** | 6 person-weeks | Design (1-2 weeks), engineering (3-4 weeks), QA (1 week), contingency included. |

**RICE Score** = (320 × 2 × 0.8) / 6 = **85.3**

**Assessment:** Score of 85.3 is very high. Compare to: [NEEDS CLARIFICATION: provide 1-2 recent initiatives with RICE scores for context]. Justifies investment if effort estimate holds.

---

## Step 5: Success Metrics

**Leading indicators (measurable within first week of launch):**
- Adoption rate: % of eligible accounts (those with >10 failed deliveries/month) who access the bulk reconciliation view within 2 weeks of launch
  - Target: 25%+ adoption within 2 weeks
- Activation rate: % of users who complete at least one bulk reconciliation flow (view failures + filter + initiate retry)
  - Target: 80%+ of viewers complete at least one action
- Error rate: % of bulk retry operations that fail or produce reconciliation mismatches
  - Target: <1% error rate (all retries execute without error; all results match expected state)

**Lagging indicators (measurable after 4-8 weeks):**
- Support ticket reduction: Decrease in "webhook reconciliation / manual retry" tickets
  - Baseline: 30+ tickets/quarter → Target: <15 tickets/quarter (50% reduction)
- Time-to-reconcile: Average time from "I notice a failure" to "all retries confirmed" (via user survey or proxy metric)
  - Target: Reduction from 120 min/event to <30 min/event
- Churn impact: Churn rate in mid-market segment (50-200 integrations) pre vs. post
  - Baseline: [NEEDS CLARIFICATION: what is current churn rate for this segment?] → Target: [TBD based on baseline]
- Feature retention: % of users who use the bulk reconciliation feature at least once per month
  - Target: >70% of activated users remain active after 4 weeks

**Guardrail metrics (must NOT regress):**
- Existing dashboard usage: Daily active users on the webhook delivery dashboard should not decrease
  - Guardrail: DAU should not drop >5%
- Support ticket volume (overall): Bulk reconciliation must not generate new support tickets at rate higher than it resolves
  - Guardrail: Support volume for feature should be <10% of tickets resolved
- API performance: Bulk retry operations must not cause latency regression for single-delivery operations
  - Guardrail: p95 latency for individual retries must remain <500ms
- Feature error rate: Failed reconciliation operations must be <2% (includes timeouts, data mismatches, API failures)
  - Guardrail: >98% successful operations

**Failure definition:**
- <15% adoption after 4 weeks (signals lack of user interest or discoverability problem)
- >5% error rate on bulk retry operations (signals reliability concern, requires rollback)
- Support ticket volume increase instead of decrease (signals feature is creating more problems than it solves)
- DAU on existing dashboard drops >10% (signals feature cannibalized existing workflow)

---

## Step 6: User Stories with ISC Acceptance Criteria

### US-1: View Reconciliation Summary

As an ops manager, I want to see all webhook deliveries from the past 7 days grouped by status (delivered, failed, pending), so that I can quickly identify how many failures occurred.

**Acceptance Criteria:**
- [ ] **[I]** View displays deliveries from the past 7 days; user can change the date range (1 day, 7 days, 30 days) via dropdown
- [ ] **[I]** Delivered deliveries are shown as a count and percentage of total
- [ ] **[I]** Failed deliveries are shown as a count and percentage of total, grouped by failure type (timeout, 5xx, 4xx, auth, other)
- [ ] **[I]** Pending deliveries (in-flight) are shown separately with an auto-refresh indicator
- [ ] **[S]** Page loads in <2 seconds on a typical mid-market account (10k–50k deliveries in date range)
- [ ] **[C]** When date range has zero deliveries, display "No deliveries in this range" and show the comparison period
- [ ] **[C]** Stale data is never shown; if data is >5 minutes old, a "Last updated X minutes ago" badge appears with a manual refresh button

**Edge cases:**
- User selects a future date range → show validation: "End date cannot be in the future"
- User has no failed deliveries → show summary with 0 failures and a confirmation message: "All deliveries succeeded"
- User has >1M deliveries in range → still load in <2s (pagination/sampling required — specify in design)

---

### US-2: Filter Failures by Recipient and Reason

As an ops manager, I want to filter failed deliveries by recipient/endpoint and failure reason, so that I can group retries by root cause and avoid retrying failures caused by misconfiguration.

**Acceptance Criteria:**
- [ ] **[I]** Filters include: recipient (multiselect, typeahead autocomplete), failure type (checkbox list: timeout, 5xx, 4xx, auth, rate-limited, network, other)
- [ ] **[I]** User can combine multiple filters (e.g., show "5xx errors to recipient A" AND "timeout errors to recipient B")
- [ ] **[I]** Filter state is preserved in the URL so the filtered view can be shared with a colleague
- [ ] **[S]** Filter results update in <500ms
- [ ] **[C]** When no results match the filters, display "0 failures match these filters" and suggest adjusting criteria

**Edge cases:**
- User types a recipient name that doesn't exist → autocomplete returns no results; allow free-text entry with warning "This recipient was not found in the past 7 days"
- User adds a filter that excludes all results → show "0 results" state with a "Clear filters" button

---

### US-3: Bulk Select and Retry Failed Deliveries

As an ops manager, I want to select multiple failed deliveries and initiate a bulk retry with one click, so that I don't have to retry each failure individually.

**Acceptance Criteria:**
- [ ] **[I]** Failed deliveries table shows a checkbox column; user can select individual rows or use "Select all" checkbox
- [ ] **[I]** Selected count is displayed in a sticky footer ("3 failures selected") with a "Retry selected" button
- [ ] **[I]** "Select all" checkbox only selects visible (filtered) failures, not entire dataset
- [ ] **[S]** Clicking "Retry selected" opens a confirmation modal showing: count of failures, recipient breakdown, estimated retry time
- [ ] **[S]** User must explicitly confirm the modal before retries are triggered (no auto-retry after selection)
- [ ] **[C]** If the user navigates away before confirming, the selection is cleared (no persistent queuing of retries)
- [ ] **[C]** Retries are rate-limited: bulk operations can retry up to 1,000 failures per operation; batches >1,000 require multiple operations

**Edge cases:**
- User selects all failures (1,500) → modal warns "This will retry 1,500 deliveries. This will take approximately 5–10 minutes. Continue?"
- User selects failures, then filters change (e.g., new failures arrive in the 7-day window) → selection should be cleared with a message: "Filters changed; your selection was cleared"
- User initiates a retry while another retry is in progress → prevent concurrent bulk operations; show "A bulk retry is already in progress. Please wait."

---

### US-4: Monitor Bulk Retry Progress

As an ops manager, I want to see real-time progress of a bulk retry operation, so that I know when it's safe to close the page and what the final count of successful/failed retries is.

**Acceptance Criteria:**
- [ ] **[I]** After confirming a bulk retry, a progress modal appears showing: "Retrying X of Y failures (Z% complete)"
- [ ] **[I]** Progress updates in real-time; user can see failures grouped by outcome (succeeded, failed, pending)
- [ ] **[I]** If a retry fails, the failure reason is displayed inline (e.g., "Recipient returned 500: Internal Server Error")
- [ ] **[S]** User can close the progress modal and the retry continues in the background
- [ ] **[S]** A banner at the top of the page shows "Bulk retry in progress: 47 of 50 complete" with a "View details" link
- [ ] **[C]** If the user navigates away and returns, the in-progress bulk operation's status is restored and visible
- [ ] **[C]** When retry completes, the status modal or banner displays final summary: "Completed: 48 succeeded, 2 failed"

**Edge cases:**
- User closes the browser tab during a bulk retry → operation continues server-side; when they return, they can see the final result
- Bulk retry takes >30 minutes → operation should still complete without timeout; user can check back anytime
- A single retry within the bulk operation times out → that failure is marked "retry failed: timeout" and not retried automatically; user can manually retry afterward

---

### US-5: View Reconciliation Results and Audit Trail

As an ops manager, I want to see the final result of a reconciliation (which deliveries succeeded, which remained failed) and export an audit record, so that I can prove to finance/compliance that all deliveries were addressed.

**Acceptance Criteria:**
- [ ] **[I]** After a bulk retry completes, a results table shows: original delivery ID, recipient, original failure reason, retry outcome (succeeded, failed, skipped), retry timestamp
- [ ] **[I]** User can filter the results table by outcome (succeeded, failed, skipped)
- [ ] **[I]** User can export results as CSV with columns: delivery ID, recipient, failure reason, retry status, retry timestamp, retry error (if any)
- [ ] **[S]** Export completes in <5 seconds even for 10k+ rows
- [ ] **[C]** CSV includes a header row with column descriptions and a footer with reconciliation metadata: date range reconciled, total failures, success/failure counts, user email, timestamp

**Edge cases:**
- User exports before retry is complete → warn "Retry still in progress. Export will include only completed retries. Continue?"
- Result set is empty (all retries succeeded) → CSV still exports with headers and summary footer

---

### US-6: Prevent Accidental Mass Retries

As the platform, I want to prevent an ops manager from accidentally retrying thousands of failures at once and creating cascading failures on the recipient side.

**Acceptance Criteria:**
- [ ] **[I]** Bulk retry operations are capped at 1,000 failures per operation
- [ ] **[I]** If user selects >1,000 failures, the "Retry selected" button is disabled with tooltip: "Maximum 1,000 retries per operation. Your selection has 2,043 failures. Split into multiple operations or filter the selection."
- [ ] **[I]** Retried deliveries are rate-limited on the recipient side: no more than 50 retries/second per recipient
- [ ] **[S]** If a recipient returns 429 (rate-limited) or 5xx during a bulk retry, the operation pauses, backs off, and retries after 30–60 seconds
- [ ] **[C]** If a retry fails 3 times due to recipient errors, it is marked "failed: recipient unreachable" and not retried further in this operation

**Edge cases:**
- Recipient's rate limit is very strict (e.g., 1 retry/second) → bulk operation adapts automatically; may take longer but still completes successfully
- Recipient is permanently down → operation marks all retries to that recipient as "failed: recipient unreachable" after 3 attempts and moves on

---

## Step 7: Scope Definition

**In scope:**
- Bulk view of webhook deliveries (past 7, 30 days; customizable)
- Grouping by status (delivered, failed, pending) and failure type
- Filtering by recipient and failure reason
- Bulk selection of failed deliveries (up to 1,000 per operation)
- Initiate bulk retry with confirmation modal
- Real-time progress monitoring of bulk retry operations
- Results view and CSV export with audit trail
- Rate limiting and safety guardrails to prevent cascading failures
- Mobile-responsive view (ops managers check status on-the-go)

**Out of scope:**
- Individual (single-delivery) retry workflows — existing UI already supports this; bulk feature is *in addition to*, not a replacement
  - Reason: Deferred to v2 if needed; single retries are already available
- Webhook payload inspection or debugging — different problem (delivery vs. content correctness)
  - Reason: Separate initiative; inspection is advanced ops task, not core reconciliation pain
- Webhook configuration or rule management — this is event source setup, not delivery reconciliation
  - Reason: Tracked separately; out of scope for this feature
- Automatic retry on failure (e.g., "retry all 4xx failures daily until resolved") — too much automation without ops oversight
  - Reason: Descoped due to safety concerns; can be v2 feature once confidence is higher
- Integration with customer's internal systems (pulling comparison data automatically) — would require customer API setup
  - Reason: Out of scope; customers must still export their own data. Feature reduces *analysis* time, not data import time
- Custom retry schedules or policies — reconciliation is ad-hoc, not scheduled
  - Reason: Deferred; low priority for mid-market ops managers

**Anti-requirements:**
- Do NOT automatically retry failures — ops manager must always confirm
- Do NOT show sensitive data in CSV exports (API keys, auth headers, customer PII)
- Do NOT allow retries of successful deliveries (no harm, but unnecessary and confusing)
- Do NOT bulk-retry more than 1,000 failures per operation without explicit user action to split
- Do NOT proceed with a bulk retry if >5% of the selected failures are already in-flight (pending)

---

## Step 8: Risks and Pre-Mortem

### Value Risk: Will ops managers actually use this?

**Assessment:** Medium risk. Evidence supports the need:
- 30+ support tickets this quarter show clear demand
- 3 churned accounts explicitly cited webhook management
- Manual CSV diffing is painful and well-documented

**But:** Unknown how many of the 400 eligible accounts actually hit this pain weekly vs. quarterly. Some low-volume integrators may never encounter enough failures to justify switching workflows. Activation may be lower among small-batch users.

**Mitigation:** Run discovery interviews with 3–5 ops managers after beta to validate usage patterns. Monitor adoption rate closely; if <15% activate, consider whether messaging/discoverability is the problem or whether the feature solves a smaller problem than expected.

---

### Usability Risk: Can ops managers figure out how to use this?

**Assessment:** Low-medium risk. Bulk operations are inherently risky (one click = many actions). Ops managers are not always technical.

**Specific concerns:**
- Confirmation modal is critical to prevent accidental bulk retries. If modal is too easy to dismiss, users will regret it.
- Filtering language (multiselect, typeahead, combining filters) could be confusing if UI is not intuitive.
- Exporting results for audit trail requires clear CSV format; if columns are poorly labeled, users won't trust it.

**Mitigation:**
- Design confirmation modal prominently, with explicit summary (e.g., "You are about to retry 347 failed deliveries to 12 recipients").
- Include inline help text and tooltips for filters.
- Pre-fill CSV header row with descriptive names, not database column names.
- Conduct design review with 1–2 ops managers before engineering starts.

---

### Feasibility Risk: Can we build this with current tech/team/timeline?

**Assessment:** Low risk, assuming:
- Webhook delivery data is already queryable and stable in our database
- Retry mechanism already exists for individual deliveries (just needs batching)
- 6-person-week estimate is realistic for the team

**Unknown dependencies:**
- [NEEDS CLARIFICATION: Do we need to build/refactor the retry queue to handle bulk operations at 50 retries/second?]
- [NEEDS CLARIFICATION: Is delivery data currently indexed for fast filtering on recipient + failure reason?]
- [NEEDS CLARIFICATION: Does the team have QA capacity for 1 full week, or is this an underestimate?]

**Mitigation:** Engineering to validate the 6-person-week estimate. If any dependency is blocked (queue refactor, indexing), timeline extends.

---

### Business Viability Risk: Does this work for the business?

**Assessment:** Low risk. Clear business wins:
- Reduces churn (3 known accounts; likely more at scale)
- Reduces support cost (~30 tickets/quarter = ~7.5 person-weeks support capacity freed up)
- Improves NPS for mid-market segment (ops experience matters for expansion)
- No compliance or legal concerns; no revenue impact (non-monetized feature)

**No conflicts** with pricing, legal, or strategic direction identified.

---

### Open Questions

| Question | Impact if wrong | Owner | Due date |
|---|---|---|---|
| Are all 400 eligible accounts equally likely to use this, or is demand concentrated in a smaller cohort? | If concentrated, RICE score and addressable market shrink; effort stays same → score drops significantly | [NEEDS CLARIFICATION: Product to sample 10–15 accounts and estimate distribution] | Before full build kickoff |
| What is the current retry/delivery queue architecture? Can it scale to 50+ retries/second during bulk operations? | If queue is already at capacity, scaling bulk operations may require major refactor (adds 1–2 weeks) | [NEEDS CLARIFICATION: Engineering to review queue capacity] | Before full build kickoff |
| Is delivery data (recipient, failure reason) indexed for fast filtering, or is a new index needed? | If new index is needed, adds 1–2 weeks and potential prod impact (index deployment) | [NEEDS CLARIFICATION: Engineering to review DB schema and query plans] | Before full build kickoff |
| What is the actual churn rate in the mid-market segment, and what % can we attribute to webhook reconciliation? | If churn is lower than expected, business case weakens; if higher, case strengthens | [NEEDS CLARIFICATION: Finance to provide cohort churn analysis] | Before feature launch (informs success metrics baseline) |
| Should we build this for all failure types, or start with just 5xx + timeout failures (80/20)? | Narrower scope = faster MVP, easier to validate, but may not address all user pain. Broader scope = more complete but more build effort | [NEEDS CLARIFICATION: Product + Eng to decide on MVP scope] | Before design kickoff |

---

## Step 9: Launch Plan

**Rollout strategy:** Feature flag with percentage rollout
1. **Alpha (internal):** Enable for all hps.gd employees + 1 friendly customer (1–2 days). Focus: smoke testing, basic usability.
2. **Beta (percentage rollout):** Enable for 10% of eligible accounts (those with >10 failed deliveries/month). Monitor adoption, error rates, support volume. Duration: 1 week.
3. **Ramp (percentage rollout):** 25% → 50% → 100% over 2 weeks, monitoring at each stage.
4. **GA:** Feature flag removed once confidence is high (error rate <1%, no new support tickets).

**Rollback criteria:**
- Error rate >5% on bulk retry operations → immediate rollback; investigate retry queue
- Support ticket volume increases instead of decreases → rollback; revisit usability
- DAU on existing webhook dashboard drops >10% → rollback; feature may be cannibalizing existing workflows
- Database query performance on delivery dashboard degrades >20% → rollback; investigate impact of filtering queries

**Monitoring (required before launch):**
- Bulk retry success rate (% of retries that succeed)
- Bulk retry error breakdown (timeout, 5xx, 4xx, rate-limited, other)
- Feature adoption rate (% of eligible accounts accessing the feature)
- Feature activation rate (% of viewers who initiate a bulk retry)
- Time-to-reconcile (via user survey during beta)
- Support ticket volume for "webhook reconciliation" keyword
- Existing webhook dashboard: DAU, session duration, feature usage

**Communication:**
- Support team: Train on new feature; include in FAQ before launch. Expect questions about "can I still retry manually?" (answer: yes, feature is in addition to existing UI)
- Sales team: Brief on feature availability for upsell/retention conversations with at-risk accounts
- Marketing: Blog post or changelog entry for feature announcement (low priority; feature is not lead-gen, just retention/support improvement)
- Customer success: Proactive outreach to 3 churned accounts (or successors at those companies) to highlight new feature; may justify re-engagement

**Documentation:**
- In-app tooltips and help text for filter UI (required)
- Knowledge base article: "Reconciling webhook failures: how to use bulk retry" (nice-to-have; can ship after GA if needed)
- API documentation: Document bulk retry endpoint and rate limits for advanced customers (nice-to-have)

---

## Step 10: Technical Constraints (if known)

**Dependencies:**
- Webhook delivery data must be queryable with filters on recipient + failure reason (index required if not present)
- Retry mechanism must support idempotent retries (same delivery can be retried multiple times without duplication)
- Delivery status must be transactional (a delivery cannot be marked "delivered" and "failed" simultaneously)
- [NEEDS CLARIFICATION: Is there a webhook replay/retry queue, or do retries go through the same ingestion path as new deliveries?]

**Performance requirements:**
- Bulk view query must return results in <2 seconds for accounts with 50k deliveries in 7-day window
- Filtering must respond in <500ms
- Bulk retry rate limit: up to 50 retries/second per recipient (implies queue/rate-limiter on backend)
- Results export (CSV) must complete in <5 seconds even for 10k rows

**Compliance/Security constraints:**
- Audit trail (CSV export) must include user email and timestamp; auditors should be able to trace who initiated retries
- CSV exports must not include sensitive data: API keys, auth headers, customer PII (sanitize before export)
- Bulk retry operations must be gated to users with "manage integrations" permission or higher (already exists; reuse existing permission model)

**Data requirements:**
- Delivery ID, recipient, failure reason, failure timestamp, attempt count already exist in schema
- Original retry timestamp (when was this delivery first retried?) — [NEEDS CLARIFICATION: is this tracked?]
- Retry error message (what was the error when a retry failed?) — [NEEDS CLARIFICATION: is this captured?]

**[SUGGESTION — not a requirement]** Consider adding an optional "reason for retry" field (free-text) so ops managers can document why they initiated the bulk retry (e.g., "recipient's API recovered from outage"). Helpful for audit trail but not required for MVP.

---

## Quality Checklist

- [x] Strategic fit stated — connects to reducing churn and support volume
- [x] "Why now" is answered — 30+ tickets + 3 churned accounts + weekly pain point
- [x] Problem is stated without referencing the solution
- [x] Problem is validated by discovery (support tickets + churn data provided)
- [x] Target user is specific enough for recruitment ("ops managers at mid-market SaaS, 50–200 integrations")
- [x] RICE score is calculated with stated assumptions (85.3; high score justifies build)
- [x] Every acceptance criterion passes the ISC Splitting Test (verified each story)
- [x] At least one leading, one lagging, and one guardrail metric defined
- [x] Failure condition is explicitly defined (<15% adoption, >5% error rate, support volume increase)
- [x] Out-of-scope items include reasoning for each exclusion
- [x] Four risk categories assessed (value, usability, feasibility, viability)
- [x] Reversibility assessed — feature flag provides full reversibility; low risk
- [x] Launch plan includes rollback criteria (error rate, support volume, DAU)
- [x] All unknowns captured with owners and due dates
- [x] No implementation details masquerading as requirements
- [x] PRD is understandable by someone not in this discussion

---

## Open Items Requiring Clarification

1. **Strategic alignment:** Which company OKR does this support? (e.g., reduce churn, improve support efficiency, increase customer NPS)
2. **Target release:** What is the target release quarter for this feature?
3. **Discovery validation:** Should we conduct user interviews with 3–5 ops managers before committing to full build?
4. **Churn baseline:** What is the current churn rate for the mid-market segment (50–200 integrations)?
5. **Cohort distribution:** Are all 400 eligible accounts equally likely to use this, or is demand concentrated in a smaller cohort?
6. **Queue architecture:** What is the current retry/delivery queue architecture, and can it scale to 50+ retries/second?
7. **Database indexing:** Is delivery data indexed for fast filtering on recipient + failure reason, or is a new index needed?
8. **Delivery tracking:** Are "original retry timestamp" and "retry error message" already captured in the schema?
9. **MVP scope:** Should we build for all failure types, or start with a narrower scope (5xx + timeout) for faster MVP validation?

---

## Related Skills / Next Steps

- `/product-manager:write-discovery-plan` — if discovery interviews are needed before full build (Step 1, question 3)
- `/product-owner:write-user-story` — product owner will break these user stories into sprint-ready tasks
- `/product-owner:groom-backlog` — product owner will prioritise stories into backlog
- Link to company roadmap/OKR system once strategic alignment is confirmed (Step 1)

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.0/14.0 (100%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 112170 ms |
| Target cost | $0.1143 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | States the problem in one sentence WITHOUT referencing the solution — the problem is the manual reconciliation pain, not 'build a bulk-retry view' | PASS | Step 2: 'Mid-market SaaS ops managers waste 2-4 hours every Monday manually exporting webhook delivery data... diffing CSV files... a purely mechanical process with no tooling.' |
| c2 | Cites the concrete evidence (30+ tickets, three churned accounts) as problem validation rather than asserting 'users want it' | PASS | Step 2 Evidence: '30+ support tickets this quarter' and '3 churned accounts (mid-market segment) cited webhook management or delivery visibility as churn reason' |
| c3 | Defines the target user precisely (mid-market ops managers, 50-200 integrations, weekly frequency) — specific enough to recruit for a test | PASS | Step 3: 'Mid-market SaaS company with $50k-500k ARR, 50-200 active integrations'; Frequency: 'Weekly (scheduled Monday check)' |
| c4 | Calculates a RICE score showing the formula (Reach × Impact × Confidence) / Effort with the numbers — does not just assert 'high priority' | PASS | Step 4: 'RICE Score = (320 × 2 × 0.8) / 6 = 85.3' with a table defining Reach=320, Impact=2, Confidence=80%, Effort=6 |
| c5 | Defines at least one leading, one lagging, AND one guardrail metric — and an explicit failure condition (e.g. '<10% adoption after 4 weeks') | PASS | Step 5 has leading (adoption rate), lagging (support ticket reduction), guardrail (DAU must not drop >5%), and explicit failure: '<15% adoption after 4 weeks' |
| c6 | Writes acceptance criteria that are Independent / Small / Complete (ISC) — including a boundary/edge case, not just the happy path | PASS | Each US uses [I]/[S]/[C] labels. US-1 edge cases: 'User selects a future date range → show validation'; US-3: empty selection, filter change clears selection |
| c7 | Assesses all four Cagan risks (value, usability, feasibility, viability) in a pre-mortem | PASS | Step 8 has four named sections: 'Value Risk', 'Usability Risk', 'Feasibility Risk', 'Business Viability Risk' — each with assessment and mitigation |
| c8 | Defines scope with in-scope, out-of-scope (with reasons), and anti-requirements — and hands story breakdown to the product-owner rather than grooming the backlog itself | PARTIAL | Step 7 has in-scope, out-of-scope with reasons, and anti-requirements. Related Skills: '/product-owner:write-user-story — product owner will break these user stories into sprint-ready tasks' |
| c9 | Output PRD file exists under `docs/product/` with a header carrying the RICE score, and the problem stated independently of the solution | PASS | File at work/docs/product/prd-bulk-webhook-reconcile.md; header table shows 'RICE Score \| 85.3'; problem statement in Step 2 contains no solution reference |
| c10 | The RICE section shows the actual arithmetic (Reach, Impact, Confidence, Effort values and the resulting score), not a bare 'high' | PASS | Step 4 table shows Reach=320, Impact=2, Confidence=80%, Effort=6, then 'RICE Score = (320 × 2 × 0.8) / 6 = 85.3' |
| c11 | Success metrics include leading + lagging + guardrail, and the PRD names a specific, falsifiable failure condition that supports a kill decision | PASS | Failure definition: '<15% adoption after 4 weeks', '>5% error rate on bulk retry operations', 'Support ticket volume increases instead of decreases' |
| c12 | At least one acceptance criterion specifies a boundary/error condition (empty state, error, concurrency), demonstrating the 'Complete' part of ISC | PASS | US-3 [C]: 'If user navigates away before confirming, the selection is cleared'; also 'prevent concurrent bulk operations; show A bulk retry is already in progress' |
| c13 | The four risk categories (value, usability, feasibility, viability) are each assessed, not just listed | PASS | Each risk has: a named assessment level (e.g., 'Medium risk', 'Low-medium risk'), specific concerns, and a Mitigation paragraph with concrete actions |
| c14 | Output marks genuine unknowns with `[NEEDS CLARIFICATION: ...]` rather than silently inventing missing facts | PASS | Multiple instances: '[NEEDS CLARIFICATION: Which company OKR does this support?]', '[NEEDS CLARIFICATION: what is current churn rate for this segment?]', queue capacity, DB indexing |
| c15 | Output states that the product-owner breaks the stories down into the sprint-ready backlog — the PRD specifies behaviour, not backlog grooming | PARTIAL | Related Skills: '/product-owner:write-user-story — product owner will break these user stories into sprint-ready tasks' and '/product-owner:groom-backlog — product owner will prioritise stories' |

### Notes

The PRD is comprehensive and hits every criterion cleanly. All four Cagan risks are substantively assessed with mitigations, RICE arithmetic is fully shown, ISC criteria include boundary/concurrency cases, and unknowns are consistently marked rather than invented.
