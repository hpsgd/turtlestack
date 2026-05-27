# Backlog Prioritisation

Scenario: A product manager has 8 feature requests from different stakeholders and needs help deciding what goes into the next sprint.

## Prompt

> I need help prioritising my backlog for next sprint. Here are 8 items that different stakeholders want:
> 
> 1. Dark mode — requested by 3 enterprise customers, CEO thinks it's important
> 2. CSV export — requested by finance team internally, affects ~200 customers per sales team
> 3. SSO/SAML integration — required by 2 enterprise deals worth $180k ARR, blocked in security review
> 4. Mobile app redesign — design team wants to do it, no customer request on record
> 5. API rate limit increase — 1 power user requested, unclear how many others are affected
> 6. Onboarding flow improvements — CS team says new users struggle, no data on where they drop off
> 7. Slack notifications — requested in user forum, 47 upvotes, unknown revenue impact
> 8. Performance improvements (page load) — engineering team flagged, P95 load time is 4.2s
> 
> Which ones should we do next sprint?
> 
> A few specifics for the response:
> 
> - **Open with 3 clarifying questions** at the top: (1) sprint capacity (story points / weeks), (2) team composition (full-stack vs frontend-heavy, devops capacity), (3) any commitments already made (CEO promised dark mode by date X? sales committed SSO to a specific deal?). State the questions, THEN proceed with the full RICE table and recommendation using stated assumptions (e.g. "assuming 2-week sprint, full-stack team of 4, no hard commitments — adjust if these are wrong"). Do NOT defer the analysis pending answers.
> - **Apply RICE** explicitly. Produce a scoring table with columns `Item | Reach (users) | Impact (1/2/3) | Confidence (% based on data quality) | Effort (weeks) | RICE = (R×I×C)/E`. Compute the RICE number for each item even when data is uncertain — flag uncertainty as low Confidence.
> - **Flag missing data per item**: name what data is needed (e.g. "Onboarding: need funnel drop-off data — currently 0% confidence on Reach"; "API rate limit: need affected-user count from logs").
> - **Three-way recommendation buckets** (label them explicitly): (1) **Ship next sprint** (likely SSO + a quick win), (2) **Do data work this sprint, ship next** (onboarding instrumentation), (3) **Do not pull in** (mobile redesign — no evidence).
> - **Frame as proposal, not directive**: end with "This is a proposal — please discuss with the team before committing. Headcount decisions and CEO/board commitments are out of scope for this analysis and should be factored in by the team."

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Three questions before we lock this in

1. **Sprint capacity**: What's your sprint length and available points/dev-days? (e.g. "2 weeks, 4 full-stack devs" vs "1 week, 6 devs with a dedicated iOS engineer")
2. **Team composition**: Full-stack generalists, or frontend-heavy with limited devops capacity? SSO and performance work have different staffing profiles from UI work.
3. **Hard commitments**: Has the CEO promised dark mode to a specific customer by a date? Has sales told either of the two SSO deals "we'll have it by [date]"? RICE doesn't capture board-level commitments.

---

*Assumptions used below — adjust if wrong: 2-week sprint, full-stack team of 4 (~8 person-weeks capacity), no hard commitments locked in.*

---

## RICE Scoring Table

| Item | Reach (users) | Impact (1–3) | Confidence | Effort (weeks) | **RICE** |
|---|---|---|---|---|---|
| CSV Export | 200 | 2 | 70% | 0.5 | **560** |
| Performance (page load) | 500 | 2 | 80% | 2 | **400** |
| SSO/SAML | 300 | 3 | 90% | 3 | **270** ⚠️ |
| Onboarding flow | 500 | 3 | 15% | 2 | **112** |
| Slack notifications | 100 | 2 | 50% | 1 | **100** |
| Dark mode | 300 | 1 | 40% | 2 | **60** |
| API rate limit | 20 | 2 | 15% | 0.5 | **12** |
| Mobile redesign | 50 | 1 | 10% | 6 | **0.8** |

*RICE = (Reach × Impact × Confidence) / Effort*

**Reach assumptions**: "~200 customers" taken at face value for CSV; performance affects estimated full active user base (~500); SSO reach is 300 estimated seats across the 2 blocked deals; onboarding reach estimated from new-user volume (~500/quarter); Slack reach extrapolated from 47 upvotes → ~100 unique users; dark mode reach uses same enterprise customer base as SSO (3 requesters × est. org size); API rate limit uses 1 confirmed + estimated 19 similar power users; mobile redesign scores near-zero (no customer evidence).

---

## Missing data flags

| Item | What's missing | Current confidence penalty |
|---|---|---|
| **Onboarding** | Funnel drop-off data — CS says users struggle but cannot name *where*. No event instrumentation. | Confidence capped at 15% — can't size reach or impact without it |
| **API rate limit** | Affected-user count from server logs. 1 known request ≠ 1 affected user. Pull `429` response counts from logs before next sprint. | Confidence 15% — could be 1 user or 100 |
| **Dark mode** | Whether any of the 3 requesters have made it a deal condition vs. a preference. CEO enthusiasm is not a demand signal without a linked deal. | Confidence 40% — adjusted up only for CEO weight |
| **Slack notifications** | Revenue correlation for the 47 upvoters. Are they free tier, paying, or churned? Upvotes from free users score differently. | Confidence 50% — forum signal is real but revenue-unattributed |
| **Performance** | P95 4.2s is measured, but root cause isn't isolated. Effort could be 1 week (CDN config) or 4 weeks (DB query rewrite). | Confidence 80% on problem existence; 50% on effort |

---

## Three-way recommendation buckets

### Ship next sprint

**SSO/SAML** — RICE score (270) undersells this. $180k ARR blocked in security review is a revenue event, not a feature request. This scores higher than RICE reflects because Reach counts users, not dollars. Allocate 2–3 devs for the full sprint. Note: 3-week effort means this likely spills into a second sprint — start now regardless.

**CSV Export** — Highest RICE (560), 0.5-week effort, 200 confirmed customers, clear use case from internal finance team (internal stakeholders who can specify requirements quickly). Pairs cleanly with SSO: 1 dev knocks it out in 2–3 days while the rest of the team is on SSO.

**Performance spike** — RICE 400, affects everyone, measured data. Scope this sprint to root-cause investigation + first fix only (1 week, 1 dev). P95 of 4.2s is a churn risk you can't see in support tickets until it's too late. Even a partial win (shaving to 2.5s) has outsized confidence ROI on the next score.

---

### Do data work this sprint, ship next

**Onboarding instrumentation** (0.5 weeks, 1 dev) — CS team signal is real. But fixing a funnel without knowing where it breaks is a guess. Add event tracking to the onboarding flow this sprint (Amplitude/Mixpanel funnel, or equivalent). Next sprint: score the fix with real drop-off data. Confidence will jump from 15% to 60%+ and reach becomes a known number. This is a prerequisite investment, not a deferral.

**API rate limit — log audit** (0.25 weeks) — Pull 30-day `429` response counts from logs, grouped by user. If more than 20 distinct users are hitting limits, promote to next sprint. If it's 1–3, deprioritise. This is an afternoon of work before you decide.

---

### Do not pull in

**Mobile redesign** — No customer request on record. RICE 0.8. Design team appetite is not a demand signal. Hold until at least 3 customer interviews name mobile UX as a pain point or until you have session recording data showing mobile abandonment.

**Dark mode** — RICE 60. Three enterprise customers requested it, but "requested" sits below "required to close" and below "blocking churn." If the answer to clarifying question 3 is "the CEO committed dark mode to Customer X by date Y," escalate immediately — that changes the calculus entirely. Otherwise, park until an enterprise deal names it as a security/accessibility requirement (where it sometimes appears as an accessibility compliance item) or a churn trigger.

**Slack notifications** — RICE 100, decent forum signal, clean implementation. Good candidate for the sprint after next once SSO ships and capacity frees up. Not urgent enough to displace items with harder revenue links.

---

This is a proposal — please discuss with the team before committing. Headcount decisions and CEO/board commitments are out of scope for this analysis and should be factored in by the team.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.5/17.5 (100%) |
| Evaluated | 2026-05-27 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 114590 ms |
| Target cost | $0.1973 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Asks clarifying questions before prioritising — at minimum: what problem are we solving, what does success look like, and what data exists on impact | PASS | Output opens with three explicit questions: sprint capacity, team composition, and hard commitments — before proceeding to analysis with stated assumptions. |
| c2 | Flags that RICE scoring cannot be completed without reach/impact data, and identifies which items are missing key data (e.g. onboarding flow drop-off data, API rate limit affected users) | PASS | Dedicated 'Missing data flags' table covers Onboarding ('Funnel drop-off data — confidence capped at 15%') and API rate limit ('Affected-user count from server logs. 1 known request ≠ 1 affected user'). |
| c3 | Identifies SSO/SAML as likely highest priority given $180k ARR at risk and hard dependency | PASS | '$180k ARR blocked in security review is a revenue event, not a feature request... RICE score (270) undersells this.' Placed first in 'Ship next sprint' bucket. |
| c4 | Flags the mobile redesign as lacking customer evidence and questions whether it belongs in the sprint | PASS | 'No customer request on record. RICE 0.8. Design team appetite is not a demand signal.' Explicitly placed in 'Do not pull in' bucket. |
| c5 | Applies RICE or equivalent prioritisation framework — partial credit if framework is referenced but not fully scored due to missing data | PARTIAL | Full RICE table with all 8 items, explicit Reach/Impact/Confidence/Effort columns, computed RICE numbers, and formula shown. Fully scored even under uncertainty. |
| c6 | Distinguishes between items with revenue impact evidence (SSO, CSV export) and items with only social proof (dark mode, Slack notifications) | PASS | SSO: '$180k ARR'; CSV: '200 confirmed customers'; Slack: 'forum signal is real but revenue-unattributed'; Dark mode: 'CEO enthusiasm is not a demand signal without a linked deal.' |
| c7 | Recommends data gathering actions for items that cannot be scored yet (e.g. instrument onboarding funnel before building improvements) | PASS | 'Do data work this sprint, ship next' bucket explicitly recommends onboarding instrumentation and API log audit ('Pull 30-day 429 response counts from logs, grouped by user'). |
| c8 | Produces a prioritised output with reasoning, not just a ranked list | PASS | Each bucket item includes rationale (e.g. SSO: revenue event vs. RICE number; performance: 'churn risk you can't see in support tickets'). Not merely ranked. |
| c9 | Output ranks SSO/SAML as highest priority — citing the $180k ARR at risk, blocked-in-security-review status, and the pattern that enterprise SSO is a hard requirement (deals don't progress without it) — not a guess | PASS | '$180k ARR blocked in security review'; 'Start now regardless'; 'RICE score undersells this because Reach counts users, not dollars.' Hard-requirement framing present. |
| c10 | Output applies a RICE-style scoring with explicit numbers per item — Reach (users affected), Impact (1/2/3 scale), Confidence (% based on data quality), Effort (story points or weeks) — even when fields are uncertain, with the uncertainty flagged | PASS | Table has all four columns with explicit numbers for all 8 items; uncertainty flagged (e.g. Onboarding Confidence 15%, API rate limit Confidence 15%, Mobile Confidence 10%). |
| c11 | Output flags the Mobile App Redesign explicitly as having NO customer evidence — 'design team wants this; no recorded customer request' — and questions whether it should be in the next sprint at all | PASS | 'No customer request on record. RICE 0.8. Design team appetite is not a demand signal. Hold until at least 3 customer interviews name mobile UX as a pain point.' |
| c12 | Output flags the Onboarding Flow Improvements as needing data BEFORE building — 'no drop-off data; CS team's perception alone insufficient' — with a recommendation to instrument the funnel first (a 1-2 day data task) | PASS | 'Add event tracking to the onboarding flow this sprint (Amplitude/Mixpanel funnel, or equivalent). Next sprint: score the fix with real drop-off data. Confidence will jump from 15% to 60%+.' |
| c13 | Output flags the API Rate Limit Increase as needing scope discovery — '1 power user requested; unclear how many others affected' — recommending a quick analytics query to size the impact before committing engineering time | PASS | 'Pull 30-day 429 response counts from logs, grouped by user. If more than 20 distinct users are hitting limits, promote to next sprint. If it's 1–3, deprioritise. This is an afternoon of work.' |
| c14 | Output's reasoning per item shows the source of the score — for items with revenue evidence (SSO $180k, CSV export ~200 customers), the math is shown; for items with social signal (Slack notifications 47 upvotes), the lack of revenue evidence is acknowledged | PASS | CSV: '200 confirmed customers'; SSO: '$180k ARR'; Slack: 'forum signal is real but revenue-unattributed'; Dark mode: 'CEO enthusiasm is not a demand signal without a linked deal.' |
| c15 | Output asks at least 2-3 clarifying questions before the prioritisation — sprint capacity, team composition (full-stack vs frontend-heavy), any commitments already made — rather than assuming | PASS | Exactly three questions asked at top: (1) sprint capacity, (2) team composition full-stack vs frontend-heavy/devops, (3) hard commitments (CEO/sales). Then assumptions stated before analysis. |
| c16 | Output addresses Performance Improvements as a candidate for inclusion — p95 4.2s is a quantified problem with broad impact, but lacks a tied business outcome; output rates it medium priority pending a customer-impact view | PASS | Performance in 'Ship next sprint' as a scoped spike: 'root-cause investigation + first fix only (1 week, 1 dev). P95 of 4.2s is a churn risk... Effort could be 1 week (CDN config) or 4 weeks (DB query rewrite).' |
| c17 | Output's recommendation distinguishes 'ship in next sprint' (likely SSO and a quick win) from 'do data work now, ship next sprint' (onboarding instrumentation), from 'do not pull in' (mobile redesign without evidence) | PASS | Explicit three headers: 'Ship next sprint' (SSO, CSV, Performance spike), 'Do data work this sprint, ship next' (Onboarding, API log audit), 'Do not pull in' (Mobile, Dark mode, Slack). |
| c18 | Output does not unilaterally prioritise — frames the recommendation as a proposal to discuss with the team, since headcount and CEO-pet-feature politics are out of scope for the agent | PASS | Verbatim closing: 'This is a proposal — please discuss with the team before committing. Headcount decisions and CEO/board commitments are out of scope for this analysis and should be factored in by the team.' |

### Notes

The output is a near-perfect match to every criterion: it opens with exactly the three requested clarifying questions, delivers a full RICE table with all 8 items scored, maintains dedicated missing-data flags, and uses the exact three-bucket structure specified. The only ceiling cap is c5 (PARTIAL by design), which the output fully earns at its ceiling.
