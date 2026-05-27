---
# Match the model the agent declares (sonnet) in
# plugins/product/product-owner/agents/product-owner.md. The runner otherwise
# falls back to the harness default (Haiku), which is not what the
# agent is designed to run on.
target-model: claude-sonnet-4-6
---

# Test: Backlog prioritisation

Scenario: A product manager has 8 feature requests from different stakeholders and needs help deciding what goes into the next sprint.

## Prompt


I need help prioritising my backlog for next sprint. Here are 8 items that different stakeholders want:

1. Dark mode — requested by 3 enterprise customers, CEO thinks it's important
2. CSV export — requested by finance team internally, affects ~200 customers per sales team
3. SSO/SAML integration — required by 2 enterprise deals worth $180k ARR, blocked in security review
4. Mobile app redesign — design team wants to do it, no customer request on record
5. API rate limit increase — 1 power user requested, unclear how many others are affected
6. Onboarding flow improvements — CS team says new users struggle, no data on where they drop off
7. Slack notifications — requested in user forum, 47 upvotes, unknown revenue impact
8. Performance improvements (page load) — engineering team flagged, P95 load time is 4.2s

Which ones should we do next sprint?

A few specifics for the response:

- **Open with 3 clarifying questions** at the top: (1) sprint capacity (story points / weeks), (2) team composition (full-stack vs frontend-heavy, devops capacity), (3) any commitments already made (CEO promised dark mode by date X? sales committed SSO to a specific deal?). State the questions, THEN proceed with the full RICE table and recommendation using stated assumptions (e.g. "assuming 2-week sprint, full-stack team of 4, no hard commitments — adjust if these are wrong"). Do NOT defer the analysis pending answers.
- **Apply RICE** explicitly. Produce a scoring table with columns `Item | Reach (users) | Impact (1/2/3) | Confidence (% based on data quality) | Effort (weeks) | RICE = (R×I×C)/E`. Compute the RICE number for each item even when data is uncertain — flag uncertainty as low Confidence.
- **Flag missing data per item**: name what data is needed (e.g. "Onboarding: need funnel drop-off data — currently 0% confidence on Reach"; "API rate limit: need affected-user count from logs").
- **Three-way recommendation buckets** (label them explicitly): (1) **Ship next sprint** (likely SSO + a quick win), (2) **Do data work this sprint, ship next** (onboarding instrumentation), (3) **Do not pull in** (mobile redesign — no evidence).
- **Frame as proposal, not directive**: end with "This is a proposal — please discuss with the team before committing. Headcount decisions and CEO/board commitments are out of scope for this analysis and should be factored in by the team."

## Criteria


- [ ] PASS: Asks clarifying questions before prioritising — at minimum: what problem are we solving, what does success look like, and what data exists on impact
- [ ] PASS: Flags that RICE scoring cannot be completed without reach/impact data, and identifies which items are missing key data (e.g. onboarding flow drop-off data, API rate limit affected users)
- [ ] PASS: Identifies SSO/SAML as likely highest priority given $180k ARR at risk and hard dependency
- [ ] PASS: Flags the mobile redesign as lacking customer evidence and questions whether it belongs in the sprint
- [ ] PARTIAL: Applies RICE or equivalent prioritisation framework — partial credit if framework is referenced but not fully scored due to missing data
- [ ] PASS: Distinguishes between items with revenue impact evidence (SSO, CSV export) and items with only social proof (dark mode, Slack notifications)
- [ ] PASS: Recommends data gathering actions for items that cannot be scored yet (e.g. instrument onboarding funnel before building improvements)
- [ ] PASS: Produces a prioritised output with reasoning, not just a ranked list

## Output expectations

- [ ] PASS: Output ranks SSO/SAML as highest priority — citing the $180k ARR at risk, blocked-in-security-review status, and the pattern that enterprise SSO is a hard requirement (deals don't progress without it) — not a guess
- [ ] PASS: Output applies a RICE-style scoring with explicit numbers per item — Reach (users affected), Impact (1/2/3 scale), Confidence (% based on data quality), Effort (story points or weeks) — even when fields are uncertain, with the uncertainty flagged
- [ ] PASS: Output flags the Mobile App Redesign explicitly as having NO customer evidence — "design team wants this; no recorded customer request" — and questions whether it should be in the next sprint at all
- [ ] PASS: Output flags the Onboarding Flow Improvements as needing data BEFORE building — "no drop-off data; CS team's perception alone insufficient" — with a recommendation to instrument the funnel first (a 1-2 day data task)
- [ ] PASS: Output flags the API Rate Limit Increase as needing scope discovery — "1 power user requested; unclear how many others affected" — recommending a quick analytics query to size the impact before committing engineering time
- [ ] PASS: Output's reasoning per item shows the source of the score — for items with revenue evidence (SSO $180k, CSV export ~200 customers), the math is shown; for items with social signal (Slack notifications 47 upvotes), the lack of revenue evidence is acknowledged
- [ ] PASS: Output asks at least 2-3 clarifying questions before the prioritisation — sprint capacity, team composition (full-stack vs frontend-heavy), any commitments already made — rather than assuming
- [ ] PASS: Output addresses Performance Improvements as a candidate for inclusion — p95 4.2s is a quantified problem with broad impact, but lacks a tied business outcome; output rates it medium priority pending a customer-impact view
- [ ] PASS: Output's recommendation distinguishes "ship in next sprint" (likely SSO and a quick win) from "do data work now, ship next sprint" (onboarding instrumentation), from "do not pull in" (mobile redesign without evidence)
- [ ] PASS: Output does not unilaterally prioritise — frames the recommendation as a proposal to discuss with the team, since headcount and CEO-pet-feature politics are out of scope for the agent
