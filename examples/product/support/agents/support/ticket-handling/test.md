---
# Match the model the agent declares (sonnet) in
# plugins/product/support/agents/support.md. The runner otherwise
# falls back to the harness default (Haiku), which is not what the
# agent is designed to run on.
target-model: claude-sonnet-4-6
---

# Test: Ticket handling

Scenario: A support agent receives a ticket about a data export timing out, and needs to classify, investigate, and respond appropriately.

## Prompt

Triage and respond to this support ticket. Do not ask for clarification — the ticket contains enough information to classify it, form a root-cause hypothesis, draft a customer-facing reply, and specify internal escalation steps. Complete all of those steps now.

New ticket just came in:

**From:** marcus.chen@acme-corp.com
**Subject:** URGENT: Data export keeps failing — board meeting tomorrow at 9am

Hi,

Our bulk customer record export has been timing out since this morning and I'm running out of time. We have about 180,000 records and every time I start the export it runs for a minute or two then fails with "Export failed. Please try again." No error code, nothing useful.

I've tried four times now with the same result.

Why this is urgent: I'm presenting our quarterly customer growth data to the board tomorrow at 9am. This export is the centrepiece of the whole presentation. Without it I'm standing up there with nothing.

Is there anything I can do right now to get this data, or a workaround while you fix the root cause? I genuinely don't know what else to try.

Marcus Chen
Head of Operations, Acme Corp — Account #ACM-7842

## Criteria


- [ ] PASS: Leads with empathy and acknowledgment of urgency before any technical content — the board report deadline is recognised, not ignored
- [ ] PASS: Classifies the ticket across all dimensions: category (bug/data/performance), severity (high — time-sensitive business impact), and routing (likely escalation to engineering given dataset size)
- [ ] PASS: Identifies the likely root cause (180,000 records likely exceeding export timeout threshold) as a hypothesis, not a definitive answer
- [ ] PASS: Provides an immediate workaround or interim path — e.g. date range slicing, filtered export, async export if available — so Marcus can get data before the board meeting
- [ ] PASS: Drafts a customer-facing response that is empathetic, concrete, and does not expose internal technical uncertainty
- [ ] PARTIAL: Flags this ticket for pattern detection — if other customers have hit export timeouts with large datasets, this warrants a bug report or known issue — partial credit if escalation is recommended but pattern check is not mentioned
- [ ] PASS: Specifies next internal steps with owners — who investigates, what they check, by when given the urgency

## Output expectations

- [ ] PASS: Output's customer-facing reply opens with empathy and explicit acknowledgment of the urgency — naming the board meeting deadline, not generic "we understand this is important"
- [ ] PASS: Output's reply provides at least one immediate workaround — date-range slicing the export, filtered subset export, async/queued export if available — so Marcus has a path to get the data BEFORE the board meeting
- [ ] PASS: Output's classification labels the ticket consistently — category (data export / performance issue), severity (high — time-bound business impact), routing (engineering escalation given dataset size of 180K records)
- [ ] PASS: Output's root-cause hypothesis names the specific suspected cause (180,000 records exceeds export timeout window, likely 30-60s) but frames it as a hypothesis to verify, not a definitive answer
- [ ] PASS: Output's reply does NOT expose internal uncertainty or technical-debt admissions — keeps the language confident and customer-facing while acknowledging the issue is real
- [ ] PASS: Output's internal escalation note (separate from the customer reply) names the engineering owner, the specific investigation steps (check export timeout config, recent error logs for this user_id, query the export job table for failed runs), and a target response time given the urgency
- [ ] PASS: Output flags this for pattern detection — recommends searching the ticket queue for "export timeout" or "export failed" tickets in the last 30-60 days to see if Marcus is the canary or the latest of many
- [ ] PASS: Output's customer reply includes a commitment with a time anchor — "we'll have an update for you within 2 hours" or "the workaround above should unblock you immediately; we're investigating the root cause" — not vague "we'll get back to you"
- [ ] PASS: Output addresses follow-up communication — proactive update once root cause is identified, even if Marcus doesn't ask, given the high-stakes context
- [ ] PARTIAL: Output recommends creating a KB article on "exporting large datasets" if pattern detection confirms repeat occurrence — feeding back into self-service deflection
