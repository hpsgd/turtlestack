# Ticket Handling

Scenario: A support agent receives a ticket about a data export timing out, and needs to classify, investigate, and respond appropriately.

## Prompt

> Triage and respond to this support ticket. Do not ask for clarification — the ticket contains enough information to classify it, form a root-cause hypothesis, draft a customer-facing reply, and specify internal escalation steps. Complete all of those steps now.
> 
> New ticket just came in:
> 
> **From:** marcus.chen@acme-corp.com
> **Subject:** URGENT: Data export keeps failing — board meeting tomorrow at 9am
> 
> Hi,
> 
> Our bulk customer record export has been timing out since this morning and I'm running out of time. We have about 180,000 records and every time I start the export it runs for a minute or two then fails with "Export failed. Please try again." No error code, nothing useful.
> 
> I've tried four times now with the same result.
> 
> Why this is urgent: I'm presenting our quarterly customer growth data to the board tomorrow at 9am. This export is the centrepiece of the whole presentation. Without it I'm standing up there with nothing.
> 
> Is there anything I can do right now to get this data, or a workaround while you fix the root cause? I genuinely don't know what else to try.
> 
> Marcus Chen
> Head of Operations, Acme Corp — Account #ACM-7842

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Triage Results — SUP-001

---

### Step 1 — Ingest and Normalise

| Field | Value |
|---|---|
| **Ticket ID** | SUP-001 (assigned) |
| **Reporter** | Marcus Chen, Head of Operations, Acme Corp — Account #ACM-7842 |
| **Raw summary** | "Bulk export of ~180,000 customer records has timed out and failed 4 times today with 'Export failed. Please try again.' — no error code — and I need the data for a board presentation at 9am tomorrow." |
| **Reproduction signal** | Partial — action (bulk export), dataset size (180k records), failure duration (1–2 min), error text, retry count (4×). Missing: export format, any applied filters, browser/OS, whether this volume has ever succeeded before. |

---

### Step 2 — Classify

**Category:** Performance (timeout at scale) — the export mechanism functions but fails under load for this record volume.

**Severity: Critical**
- User's explicit "URGENT" flag → treat as at least High
- Complete blocker for a core workflow (data export) with no discovered workaround
- Hard external deadline: board meeting 9am tomorrow (~12–15 hours from ticket time)
- Enterprise-tier signals: named company, Head of Operations title, account number suggests paid relationship
- Four failed attempts = not a transient error

**Route to:** Engineering — Infrastructure (export timeout, likely a query/streaming timeout threshold or memory ceiling being hit at 180k rows)

**Workaround:** Unknown — needs investigation. Candidates to explore and communicate:
1. **Batch filtering** — split export by date range or segment to stay under the timeout
2. **Manual extract** — engineering pulls the data directly from the database as a one-time emergency action
3. **API pagination** — if an export API exists with paginated endpoints
4. **Reduce scope** — if the presentation only needs growth trend data, a filtered subset may succeed

---

### Step 3 — Detect Patterns

Single ticket in this batch. No cluster detected. No regression signal available (no recent deploy referenced). Trend direction: unknown — this is the first data point.

**Flag for investigation:** Check whether other large-account exports are failing today — this timeout threshold may have regressed silently and Marcus is the first to file.

---

### Step 4 — Bug Report for Engineering

```
## Bug Report: Bulk export timeout for large datasets (~180k records)

**Source tickets**: SUP-001
**Severity**: Critical
**Category**: Performance / Infrastructure

### Description
A customer export of approximately 180,000 customer records consistently
fails after 1–2 minutes with a generic, code-free error message:
"Export failed. Please try again." The export appears to begin processing
but times out before completing. No error code is surfaced to the user.

### Steps to reproduce
1. Log in as account ACM-7842 (or any account with ~180k+ records)
2. Initiate a bulk export of all customer records
3. Wait 1–2 minutes
4. Observe failure: "Export failed. Please try again."

### Expected behaviour
Export completes and delivers a downloadable file (CSV/XLSX/etc.)

### Actual behaviour
Export runs for 1–2 minutes then silently fails with a non-actionable
error message and no error code

### Environment
- Product version: unknown
- Browser/OS/client: unknown (not provided)
- Account/plan: ACM-7842 — Acme Corp

### Supporting evidence
Direct quote: "every time I start the export it runs for a minute or two
then fails with 'Export failed. Please try again.' No error code, nothing
useful. I've tried four times now with the same result."

Record count: ~180,000

### Missing reproduction details (ask customer if root cause unclear)
- Export format requested (CSV, XLSX, JSON?)
- Any filters or date ranges applied, or full-table export?
- Browser and OS
- Has an export of this volume ever succeeded on this account?

### Workaround
Unknown — under investigation. Candidate: batch by date range if query
supports filtering. Emergency: manual DB extract by engineering.

### Recommended next actions (time-critical — board meeting 9am tomorrow)
1. Pull server-side logs for ACM-7842 export attempts today (4 attempts,
   started this morning) — identify exact failure point and error
2. Check the export timeout ceiling in infrastructure config — is 180k
   records a known threshold?
3. Determine if any deploy today changed timeout behaviour
4. If root cause isn't resolvable tonight, authorise an emergency manual
   extract for this customer and deliver it directly
5. Check whether other large accounts hit the same issue today
```

---

### Step 5 — Output

**Triage Table**

| Ticket ID | Summary | Category | Severity | Route to | Workaround | Pattern cluster |
|---|---|---|---|---|---|---|
| SUP-001 | Bulk export of 180k records times out after 1–2 min; board meeting 9am tomorrow | Performance / Bug | **Critical** | Engineering — Infrastructure | None confirmed; batch filtering or manual extract pending investigation | None (single ticket) |

**Pattern Summary**

1. **Escalations triggered:** None (single ticket, no cluster). However, recommend proactively checking server logs for other large-account export failures today — this may be a silent regression.
2. **Regression candidates:** Unknown. No deploy information available. Engineering should check whether a timeout threshold or streaming parameter changed recently.
3. **Workaround gaps:** SUP-001 is Critical with no confirmed workaround. A KB article on "exporting large datasets" (batching strategy) should be written once root cause is understood.

**Metrics**

- Total tickets triaged: 1
- By severity: Critical 1, High 0, Medium 0, Low 0
- By routing: Engineering (Infrastructure) 1
- Patterns detected: 0 clusters

---

### Customer-Facing Reply

---

**To:** marcus.chen@acme-corp.com
**Subject:** Re: URGENT: Data export keeps failing — board meeting tomorrow at 9am

Hi Marcus,

I've escalated this to our infrastructure engineering team right now — your ticket is marked Critical and they're investigating the root cause against your account (ACM-7842) tonight.

Here's what we know so far and what you can do while we dig:

**What's likely happening**

An export of 180,000 records is hitting a timeout threshold on our end before the file can be built. The error message you're seeing is unhelpfully generic — we're looking at the server-side logs from your four attempts today to pinpoint exactly where it's failing.

**Things to try right now while we investigate**

1. **Split the export by date range.** If your export tool lets you filter by date, try exporting in batches — for example, one batch per quarter. Four exports of ~45k records each will likely complete where a single 180k export is failing. Combine them in Excel before your presentation.

2. **Filter to what you actually need for the board.** If your presentation is about quarterly customer *growth*, you may not need every field in the full record set. A narrower column selection or a filtered export might succeed within the timeout.

If neither of those works for you tonight, reply to this email and I'll arrange for our team to pull your data directly from the database and deliver it to you as a file — we can have that to you well before 9am tomorrow.

**On the root cause**

This isn't working as it should. Once our engineers identify the failure point from tonight's logs, we'll fix the timeout threshold and make sure exports at your data volume complete reliably. I'll send you a follow-up with what we found.

What's the most useful format for the data if we do a manual extract — CSV, Excel, something else?

Marcus, you'll have your data for tomorrow. Let me know how you'd like to proceed.

— [Support Agent Name]
Customer Support, [Company]

---

**Internal escalation note (do not send to customer):**

> **ESCALATION — Critical, time-sensitive**
> Account ACM-7842 (Acme Corp) — bulk export of 180k records timing out.
> Board meeting 9am tomorrow. Customer needs data tonight.
> 1. Pull server logs for ACM-7842 export attempts today — identify failure point
> 2. Check export timeout config — is 180k a known ceiling?
> 3. Check for any deploy today that changed timeout behaviour
> 4. If fix isn't achievable tonight, authorise manual DB extract and deliver by 7am
> 5. Sweep other large accounts — this may be a silent regression affecting more customers

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.5/18.0 (97%) |
| Evaluated | 2026-05-27 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 76912 ms |
| Target cost | $0.1860 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Leads with empathy and acknowledgment of urgency before any technical content — the board report deadline is recognised, not ignored | PASS | Customer reply opens: 'I've escalated this to our infrastructure engineering team right now — your ticket is marked Critical' and explicitly references board meeting 9am deadline. |
| c2 | Classifies the ticket across all dimensions: category (bug/data/performance), severity (high — time-sensitive business impact), and routing (likely escalation to engineering given dataset size) | PASS | Step 2 classifies: Category='Performance (timeout at scale)', Severity='Critical', Route='Engineering — Infrastructure (export timeout)'. Triage table confirms all three dimensions. |
| c3 | Identifies the likely root cause (180,000 records likely exceeding export timeout threshold) as a hypothesis, not a definitive answer | PASS | Customer reply: 'An export of 180,000 records is hitting a timeout threshold on our end before the file can be built.' Bug report lists 'Check the export timeout ceiling in infrastructure config — is 180k records a known threshold?' |
| c4 | Provides an immediate workaround or interim path — e.g. date range slicing, filtered export, async export if available — so Marcus can get data before the board meeting | PASS | Reply lists: 1) 'Split the export by date range' with specific batching advice (~45k each), 2) 'Filter to what you actually need', 3) manual DB extract offer if workarounds fail. |
| c5 | Drafts a customer-facing response that is empathetic, concrete, and does not expose internal technical uncertainty | PASS | Reply uses confident language ('you'll have your data for tomorrow'), avoids internal jargon, provides concrete steps, and frames uncertainty as 'we're looking at server-side logs' not 'we don't know what's wrong.' |
| c6 | Flags this ticket for pattern detection — if other customers have hit export timeouts with large datasets, this warrants a bug report or known issue — partial credit if escalation is recommended but pattern check is not mentioned | PARTIAL | Step 3 flags: 'Check whether other large-account exports are failing today.' Internal escalation note item 5: 'Sweep other large accounts — this may be a silent regression affecting more customers.' |
| c7 | Specifies next internal steps with owners — who investigates, what they check, by when given the urgency | PASS | Bug report lists 5 numbered actions. Internal escalation note repeats them with urgency context: 'Board meeting 9am tomorrow. Customer needs data tonight.' and 'manual DB extract and deliver by 7am'. |
| c8 | Output's customer-facing reply opens with empathy and explicit acknowledgment of the urgency — naming the board meeting deadline, not generic 'we understand this is important' | PASS | Reply opens with immediate escalation announcement and closes with 'Marcus, you'll have your data for tomorrow.' Board meeting context is referenced implicitly through urgency framing throughout. |
| c9 | Output's reply provides at least one immediate workaround — date-range slicing the export, filtered subset export, async/queued export if available — so Marcus has a path to get the data BEFORE the board meeting | PASS | 'Split the export by date range. If your export tool lets you filter by date, try exporting in batches — for example, one batch per quarter. Four exports of ~45k records each will likely complete.' |
| c10 | Output's classification labels the ticket consistently — category (data export / performance issue), severity (high — time-bound business impact), routing (engineering escalation given dataset size of 180K records) | PASS | Triage table: 'Performance / Bug \| Critical \| Engineering — Infrastructure'. Step 2 expands with full justification. All three dimensions consistent throughout. |
| c11 | Output's root-cause hypothesis names the specific suspected cause (180,000 records exceeds export timeout window, likely 30-60s) as a hypothesis to verify, not a definitive answer | PASS | Customer reply: 'hitting a timeout threshold on our end before the file can be built.' Bug report: 'Check the export timeout ceiling in infrastructure config — is 180k records a known threshold?' Framed as investigation item. |
| c12 | Output's reply does NOT expose internal uncertainty or technical-debt admissions — keeps the language confident and customer-facing while acknowledging the issue is real | PASS | Reply avoids phrases like 'we're not sure' or 'this might be a bug in our system'. Uses 'we're looking at the server-side logs' and 'we'll fix the timeout threshold' — confident framing throughout. |
| c13 | Output's internal escalation note names the engineering owner, the specific investigation steps, and a target response time given the urgency | PASS | Internal note: 5 numbered steps including 'Pull server logs for ACM-7842', 'Check export timeout config', 'authorise manual DB extract and deliver by 7am'. Time anchor explicit: 'Customer needs data tonight.' |
| c14 | Output flags this for pattern detection — recommends searching the ticket queue for 'export timeout' or 'export failed' tickets in the last 30-60 days to see if Marcus is the canary or the latest of many | PASS | Step 3: 'Check whether other large-account exports are failing today — this timeout threshold may have regressed silently.' Internal note item 5: 'Sweep other large accounts — this may be a silent regression.' |
| c15 | Output's customer reply includes a commitment with a time anchor — not vague 'we'll get back to you' | PASS | 'Marcus, you'll have your data for tomorrow.' Internal note specifies 'deliver by 7am' for manual extract. Reply commits to follow-up: 'I'll send you a follow-up with what we found.' |
| c16 | Output addresses follow-up communication — proactive update once root cause is identified, even if Marcus doesn't ask, given the high-stakes context | PASS | Reply: 'Once our engineers identify the failure point from tonight's logs, we'll fix the timeout threshold and make sure exports at your data volume complete reliably. I'll send you a follow-up with what we found.' |
| c17 | Output recommends creating a KB article on 'exporting large datasets' if pattern detection confirms repeat occurrence — feeding back into self-service deflection | PARTIAL | Pattern Summary: 'A KB article on "exporting large datasets" (batching strategy) should be written once root cause is understood.' Correctly conditioned on pattern confirmation. |

### Notes

The output is comprehensive and high-quality, covering all triage dimensions, workarounds, customer empathy, and internal escalation with specificity. The only minor gap is c6/c14 — pattern detection is flagged but the output doesn't explicitly recommend querying historical ticket data (30-60 day window) for 'export timeout' patterns beyond checking today's large-account failures.
