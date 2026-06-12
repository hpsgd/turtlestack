# Voc Programme Design

Scenario: A SaaS product team wants to stand up a continuous voice-of-customer programme. They currently have no structured customer feedback — just ad-hoc support tickets. The skill must produce a programme blueprint that picks the right metric per question (NPS / CSAT / CES), designs the surveys, ties quantitative signal to qualitative themes, designs both feedback loops, sets governance, and treats this as one VoC lens among several (not the central feedback owner).

## Prompt

> We're a mid-market B2B SaaS product (project-management tooling). We have no structured customer-feedback programme today — just whatever lands in support tickets. I want to stand up an ongoing voice-of-customer programme. The decisions we most want it to feed: (1) which onboarding step to fix next — new accounts seem to drop off during setup; (2) early detection of accounts at risk of churning; (3) whether a release landed well or needs iterating.
> 
> /ux-researcher:voc-programme-design mid-market B2B SaaS project-management product
> 
> Design the full programme blueprint using the skill's process and Output Format. Write it to `{workspace}/work/voc-programme.md` and reply with the path.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Programme designed and written. The blueprint covers all six design steps:

**1. Objectives** — Three decisions with clear owners (Product Owner on onboarding/releases, Customer Success on churn detection).

**2. Metrics** — CES for setup friction (measures effort, strongest predictor of drop-off), NPS for quarterly relationship health + threshold-triggered CSAT for early warning signals, CSAT for feature validation post-release.

**3. Surveys** — Verbatim wording for each metric, sampling strategy (census where possible, segment stratification), and fatigue controls (no respondent surveyed more than once per 90 days).

**4. Synthesis** — Stable code frame (setup confusion, missing features, adoption barriers, performance, integrations, value, support, workflow mismatch) with driver analysis showing which themes distinguish low-scorers from high-scorers, segment-cut rules, and saturation threshold (≥25% of detractors across two cycles before acting).

**5. Closing the loop** — Inner loop routes individual detractors to owners with SLAs (4h for setup, 24h for at-risk, 48h for feature issues). Outer loop feeds saturated themes to product backlog as discovery inputs. Explicit "close the loop visibly" rule: tell customers what you changed based on their feedback.

**6. Governance** — Assigned programme owner, weekly synthesis + monthly aggregate reporting, anti-gaming guards (no score solicitation, raw verbatims visible, response-rate transparency), and review triggers (when to redesign the programme itself).

**Cross-consultation** — Explicit conflict flags with support (ticket themes), customer-success (adoption vs. satisfaction can diverge), and GTM (detractor profile ≠ lost-deal profile). Notes that overlap is intentional—don't centralise, surface the differences.

Path: `/var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/eval-1781284738-fd352c3f/work/voc-programme.md`

### Artifacts written

#### `work/voc-programme.md`

```
# VoC Programme: Project-Management SaaS

**Date:** 2026-06-13  |  **Researcher:** [UX Research Lead]  |  **Status:** Draft

## 1. Objectives

| Objective | Decision it informs | Owner who acts | Cadence of the decision |
|---|---|---|---|
| Reduce onboarding drop-off | Which onboarding step to redesign next | Product Owner | Per sprint (weekly prioritization) |
| Detect at-risk accounts early | Which accounts need proactive intervention | Customer Success Manager | Weekly (cohort-based outreach) |
| Validate release quality | Whether to roll back, iterate, or ship to general availability | Product Owner | Per release (within 48h post-ship) |

---

## 2. Metric Selection

| Objective | Metric | Trigger point | Rationale |
|---|---|---|---|
| Reduce onboarding drop-off | **CES** (Customer Effort Score) | Immediately after account setup completes or is abandoned | Effort is the strongest predictor of subsequent engagement. A frictionless onboarding correlates with account survival; a hard setup predicts drop-off. CES pinpoints where the friction is. |
| Detect at-risk accounts early | **NPS** (Net Promoter Score) + **threshold-based CSAT** | Quarterly relationship check-in + triggered on early warning signals (low feature adoption, support escalations, login gaps) | NPS tracks overall relationship health. Threshold-based CSAT fires when adoption metrics hit a floor (e.g., <1 feature used/week after 30 days) to catch sliding accounts before they leave. |
| Validate release quality | **CSAT** (Customer Satisfaction) | 48 hours post-release for new features; weekly aggregate for overall product satisfaction | Transactional CSAT on released features shows whether users see value; aggregate trend shows whether the release moved the needle. Paired with open-text feedback, it flags broken rollouts or unmet expectations early enough to iterate. |

---

## 3. Survey Design

### Survey design — Post-onboarding CES

**Primary question (verbatim):** "[Product name] made it easy for me to set up my account and start my first project."
- Scale: Strongly disagree (1) → Strongly agree (7)

**Follow-up (open text, mandatory):** "What was the main challenge during setup, if any?"

**Trigger:** Account owner clicks "completed" on the setup checklist, OR 48 hours after first login (whichever comes first). If setup is abandoned (no login after 72 hours), trigger a variant: "What stopped you from completing setup?"

**Sampling:** Census of all new signups (all plan tiers). No exclusions—drop-off is the problem, so low-engagement accounts are exactly who we need to hear from.

**Cadence / fatigue control:** One survey per new account lifecycle. No repeat surveys for the same account unless 90 days have passed and they re-engage.

**Channel:** In-product modal on completion OR pending-setup page. Email fallback if user closes the modal (fires 24h later). SMS not used at this stage.

**Target response rate:** ≥40% of new signups per week, stratified by signup source (organic, free trial, demo-requested, pricing-page). Flag weeks below 35% as insufficient sample.

---

### Survey design — Relationship NPS (Quarterly)

**Primary question (verbatim):** "How likely are you to recommend [product name] to a colleague?"
- Scale: Not at all likely (0) → Extremely likely (10)

**Follow-up (open text, mandatory):** "What's the main reason for your score?"

**Trigger:** Quarterly, at fixed calendar intervals (e.g., end of Q1, Q2, Q3, Q4). Time within each account's onboarding window is irrelevant—track calendar cycles for consistency.

**Sampling:** Census of all active accounts (login in the past 30 days) across all tiers. Exclude accounts <30 days old (they haven't had time to form a relationship).

**Cadence / fatigue control:** Once per quarter, per account. Suppress if the account received any other survey in the past 21 days.

**Channel:** Email (primary) + in-product banner for login within 7 days of send.

**Target response rate:** ≥25% of invited cohort per quarter. Below 20% = insufficient sample; flag the cycle.

---

### Survey design — Risk-triggered CSAT (On-demand)

**Primary question (verbatim):** "How satisfied are you with [product name] right now?"
- Scale: Very unsatisfied (1) → Very satisfied (5)

**Follow-up (open text, mandatory):** "What's the biggest pain point you're experiencing?"

**Trigger:** Automatic, when any of these conditions are met within a rolling 30-day window:
- Account has logged in <1 day in the past week (engagement cliff)
- Account has not used a core workflow (e.g., project creation, task assignment) in 14 days
- Support ticket raised with "urgent" severity or escalation flag
- Feature-flag cohort for a major release shows <20% feature adoption after 7 days

**Sampling:** Census of triggered accounts only—this is an early-warning mechanism, not a general survey.

**Cadence / fatigue control:** One survey per trigger event per account. No more than one survey per triggered account per 14 days (if multiple conditions fire, batch into one survey).

**Channel:** Email (primary), in-product banner on next login.

**Target response rate:** ≥30% of triggered accounts (these are at-risk, so they're less responsive; 30% is realistic). Below 20% = insufficient sample for that cohort.

---

### Survey design — Post-release feature CSAT (48h window)

**Primary question (verbatim):** "[Feature name] lets me [use case / job done]. How satisfied are you with how it works?"
- Scale: Very unsatisfied (1) → Very satisfied (5)

**Follow-up (open text, mandatory):** "What would make this feature better?"

**Trigger:** 48 hours after a feature ships to general availability (or to a beta cohort, if beta-tested). Fires only for accounts that have accessed the feature at least once in the first 48 hours.

**Sampling:** All accounts that use the feature in the 48-hour window (census). If uptake is <10% of the customer base in the first 48 hours, flag as "low early adoption" in the report (may signal confusion or visibility issues).

**Cadence / fatigue control:** One survey per feature release per account. If an account received a post-release survey <7 days ago, suppress this one and wait for the next release.

**Channel:** In-product modal (primary, fires on feature use). Email fallback if modal dismissed (48h later).

**Target response rate:** ≥35% of users who touched the feature. Below 25% = insufficient feedback to guide rollout decisions; escalate to support + product team for direct outreach.

---

## 4. Quant-to-Qual Synthesis

### Verbatim coding

Each survey cycle, open-text responses are coded into themes using **affinity grouping** with a stable code frame that grows over time. Responses are coded independently by two team members; disagreements are resolved in a sync before finalizing.

### Code frame (starting themes)

| Theme | Definition | Examples |
|---|---|---|
| **Setup confusion** | User doesn't understand what to do next, where to click, or what they're setting up | "Wasn't clear what to do after signing up," "the onboarding flow was overwhelming" |
| **Missing feature** | User expected functionality that doesn't exist or isn't discoverable | "Can't assign tasks to teams, only individuals," "no bulk-edit feature" |
| **Adoption barrier** | Feature/workflow exists but user can't figure out how to use it | "Spent 20 minutes finding where to add a project," "didn't know we could do that" |
| **Performance / reliability** | Speed, uptime, sync issues, or crashes | "Slow to load when I have 100+ tasks," "dashboard freezes sometimes" |
| **Integrations gap** | User wants to connect to a tool we don't support | "Can't sync with Slack," "need Google Calendar integration" |
| **Pricing / value** | User sees the product as expensive or doesn't see ROI | "Too much for our team size," "we're using 10% of the features" |
| **Support experience** | Issues with getting help from the team | "Response took 3 days," "support didn't solve my problem" |
| **Workflow mismatch** | Our workflow doesn't match how the user works | "You assume projects have phases, ours don't," "we need different permission levels" |

**Adding codes:** New codes may be added if a verbatim doesn't fit the frame. Addition requires:
- Minimum 3 independent instances across two coding cycles (saturation threshold to prevent over-coding)
- Clear definition that doesn't overlap with existing codes
- Review and approval by the programme owner before the code is active

### Driver analysis

**For CES (onboarding):**
- Separate verbatims from scorers (1-3), mid-scorers (4-5), and high-scorers (6-7)
- For each low-CES account, code the stated barrier
- Themes appearing in 40%+ of low-CES verbatims are "setup friction drivers"
- Compare to mid/high-CES accounts: if "setup confusion" appears in only 5% of high-CES accounts, it's a true differentiator

**For NPS:**
- Code detractors (0-6) and promoters (9-10) separately
- Identify themes that appear in ≥30% of detractors and <10% of promoters—these are the "relationship killers"
- Ignore themes common to both (they're background noise)

**For risk-triggered CSAT:**
- By trigger condition (engagement cliff, no feature use, support escalation, low adoption)
- Each condition may have a different theme signature (e.g., support escalations cluster around "feature confusion," login gaps cluster around "value realization")
- Route findings to the owner of that condition's recovery (support lead vs. customer-success vs. product)

**For feature CSAT:**
- Separate pre-ship beta feedback (if tested) from post-ship CSAT to see if the beta informed iteration
- Code post-release CSAT by feature sentiment (fixed-list recommendations, missing capabilities, usability issues, performance)
- If CSAT drops after a release, compare its code frame to the pre-release beta feedback—identify what was flagged, ignored, or missed

### Segment cut

Every theme is broken out by:
- **Account segment** (plan tier: free, starter, growth, enterprise)
- **Signup source** (organic, free trial, demo, enterprise sales)
- **Onboarding cohort** (for setup surveys, group by week to catch seasonal patterns)
- **Feature flag / beta status** (for release CSAT, isolate beta-tested vs. general availability users)

A theme that affects only one plan tier (e.g., "setup confusion" spiking in free-trial signups, 15%, vs. 3% in enterprise) signals a segment-specific problem worth handling separately.

### Saturation check

A theme is considered established (worth acting on) when it appears in **≥25% of detractor or low-scorer verbatims in at least two consecutive cycles** (two quarters for NPS, two weeks for onboarding CES). 

For risk-triggered surveys, saturation is ≥20% across the triggered cohort (sample sizes are smaller here).

**Exception:** If a single instance would affect >10% of accounts (e.g., a broken Slack integration preventing 20+ active users from using the product), it escalates immediately, regardless of saturation threshold.

---

## 5. Closing the Loop

### Inner loop (individual response → individual action)

| Trigger | Routing rule | Owner | SLA |
|---|---|---|---|
| **CES ≤3** (setup failure) + verbatim | Route to onboarding support / customer-success. Include the user's stated barrier. | Customer Success Manager | Contact within 4 hours if triggered during business hours; next-day if triggered out-of-hours. Offer 1:1 setup call. |
| **Risk-triggered CSAT ≤2** (at-risk account signaling distress) + verbatim | Route to Account Owner (customer-success point-person). Include the trigger condition and the verbatim. | Account Owner (Customer Success) | Contact within 24 hours. Assess whether account is salvageable; escalate to retention negotiation if needed. |
| **Feature CSAT ≤2** (user hates new feature) + verbatim | Route to product team (feature owner) + support. Include rollout metrics (% adoption, response rate). | Support Lead + Feature Owner (Product) | Support responds to individual within 24h with workaround or timeline for improvement. Product decides on rollback / iteration within 48h. |
| **NPS detractor score** (0-6) + verbatim | Route to Account Owner if account is >$5k ARR; otherwise to support + product for thematic feedback. | Account Owner (high-value) or Support Lead (mid/low-value) | Call high-value detractors within 5 business days. For lower-tier accounts, verbatims feed to monthly synthesis (outer loop). |

### Outer loop (aggregate themes → product/process change)

| Trigger | Routing rule | Owner | Forum |
|---|---|---|---|
| **Theme crosses saturation threshold** (≥25% of low-scorers, two consecutive cycles) | Theme becomes a discovery input. Product owner receives research summary with code frame, segment cuts, and representative verbatims. | UX Researcher → Product Owner | Backlog grooming / quarterly planning. Theme enters as a "research-backed discovery" card with evidence attached. |
| **Setup confusion** saturates in a specific segment (e.g., free-trial users, 40% of low-CES) | Targeted onboarding redesign. May be a different UX flow per segment (e.g., guided setup for free users, self-serve for self-implemented accounts). | Product Owner + Onboarding PM | Sprint planning (1-2 sprints out). Design review includes feedback from drop-off cohort. |
| **Systemic effort driver** (e.g., "don't know how to do X" appears in CSAT + in support tickets) | In-product help, docs, or feature redesign depending on root cause. | Product Owner + Support Lead | Assigned to the next relevant sprint (may be feature work, may be docs-only, may be help UI). |
| **Feature CSAT ≤3 after 7 days post-release** (>30% negative) | Feature enters "iterate" state: not rolled back immediately, but marked for rapid iteration. Product and design revisit the feedback within 48h. | Product Owner + Feature Owner | Emergency design sync. Rollback or iteration decision within 48-72h. |
| **Adoption pattern mismatch** (e.g., a feature ships, CSAT is 4/5, but adoption is <5% in first week—users don't see the value) | User research deep-dive. Is this a marketing/messaging issue, a discovery issue, or a product-market fit issue? | UX Researcher | Follow up with 3-5 non-adopters via screenshare/call to diagnose. Results inform launch strategy for future releases. |

**Closing the loop visibly:**
Every customer contacted as part of the inner loop is told "you said [X], we're [doing Y], shipping [when]." Every major theme that moves the backlog is surfaced in release notes: "Based on customer feedback, we fixed [issue]" or "We heard you on [feature request]; shipping in [version]."

---

## 6. Governance

| Item | Detail |
|---|---|
| **Programme owner** | [Assigned role: Head of Product or Head of Research]. Owns end-to-end: survey design, synthesis cadence, reporting, escalation SLAs, programme evolution. Accountable for response rates and actioning themes. |
| **Reporting cadence** | **Weekly synthesis** (internal, to product + customer-success): emerging themes from onboarding CES and risk-triggered surveys, any immediate escalations. **Monthly aggregate** (leadership + product team): NPS trend, feature CSAT, top 3 themes by impact, proposed backlog changes. **Quarterly deep-dive** (leadership + product + customer-success): multi-metric narrative, segment-specific signals, strategy adjustments. |
| **Benchmark** | **Internal:** Month-over-month trend; threshold floors (onboarding CES ≥5.0 average, NPS ≥30, feature CSAT ≥4.0 average). **External:** Industry benchmarks sourced from Gartner, Forrester, or G2 for PM SaaS category (collected manually 2x/year). Absolute external comparison is secondary; internal trend is primary. |
| **Anti-gaming guards** | (1) **No solicitation coaching.** Support and customer-success teams are briefed: do not ask customers for high scores or to participate in surveys if they're unhappy. (2) **Raw verbatims visible.** Every report includes unedited sample verbatims, not just summaries. If the top theme is "setup confusion," the report shows 3-5 raw quotes that illustrate it. (3) **No selective sampling.** All surveys are census (or stratified random for very large cohorts); no "only ask happy customers" or "only email non-churned accounts." Sampling rule is transparent. (4) **Response rate published.** Every report states response rate and flags if below the floor ("insufficient sample — results not actionable for [segment]"). |
| **Review trigger** | **Design review** triggered if: (a) response rate falls below 60% of target floor for two consecutive cycles; (b) open-text response rate is <15% (means verbatims are too sparse to code); (c) a major release ships, feedback is collected, but no clear CSAT trend emerges (may signal that survey wording is not capturing release-specific sentiment). (d) **Archival trigger:** if a theme has not crossed saturation threshold in 4 consecutive cycles, it's archived from the active code frame (stored for reference). |

---

## Cross-Consultation

### Overlap with other feedback lenses

**Support feedback synthesis** — Support owns the ticket stream and can identify urgent product issues (broken features, data loss) that this programme won't catch in real-time. Coordination point: monthly synthesis includes top-10 support themes from the previous month. If support is seeing "feature X is broken" and CSAT is silent, that's a signal mismatch worth investigating. *Conflict to expect:* A feature might have high post-release CSAT (users like it when they find it) but high support volume (many users can't find it). Don't reconcile—surface both to product and let the owner decide whether to fix discovery or redesign the feature.

**Customer-success account health** — Customer-success owns adoption metrics (logins, feature usage, expansion patterns) and can see which accounts are sliding before they complain. This programme's risk-triggered CSAT is designed to complement their health scoring—when adoption metrics dip, we ask why. Coordination: risk-triggered surveys route findings back to the account owner who owns the intervention. *Conflict to expect:* An account might show high adoption (using the product daily) but low NPS (frustrated with a missing capability). This is normal—adoption and satisfaction are not the same. The account is engaged but dissatisfied; the team needs to know both.

**GTM win/loss** — GTM owns why deals close and why prospects don't. This programme's NPS is broader (captures relationship health, not just deal-win reason). A detractor might be a long-standing customer unhappy about a recent change, not a prospect who saw the competitor. Coordination: GTM shares loss themes with research; this programme's detractor analysis includes loss-reason comparison to validate alignment. *Conflict to expect:* GTM may find "prospect chose competitor for features A & B," while this programme's NPS detractors cite "performance issues." These are different customer archetypes (new buyer vs. long-tail user). Cross-consult, don't merge.

---

## Immediate Next Steps

1. **Assign programme owner** — Identify who owns end-to-end synthesis and reporting.
2. **Survey engineering** — Wire surveys into product and email systems. Test survey distribution and response flows.
3. **Code frame review** — Share the starting code frame with support and customer-success. Ask for adjustments based on their ticket patterns.
4. **Response-rate floor validation** — Run a 2-week pilot to estimate realistic response rates by survey type and segment. Adjust targets if needed.
5. **Soft launch** — Begin onboarding CES and post-release CSAT with the next product release. NPS and risk-triggered surveys follow in week 2-3 once pipelines are stable.


```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 19.0/19.5 (97%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 83649 ms |
| Target cost | $0.1301 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Every programme objective names a decision it informs AND an owner who acts — no metric collected for its own sake | PASS | Objectives table has three rows, each with 'Decision it informs' and 'Owner who acts' columns: Product Owner for onboarding/releases, Customer Success Manager for churn. |
| c2 | Selects the right metric per question — CES for the effortful onboarding/setup friction, NPS for relationship/churn-risk trajectory, CSAT or NPS for release perception — not one metric used as a universal thermometer | PASS | Metric Selection table maps: onboarding→CES, churn-risk→NPS+threshold CSAT, release→CSAT. Three different metrics for three different objectives. |
| c3 | Justifies CES over CSAT for the onboarding-friction objective (effort predicts disloyalty better than delight for service interactions) | PASS | Rationale column: 'Effort is the strongest predictor of subsequent engagement. A frictionless onboarding correlates with account survival; a hard setup predicts drop-off.' |
| c4 | Designs surveys with verbatim question wording AND a paired open-text 'why' — a score with no reason is treated as a dead end | PASS | All four survey designs include verbatim primary question and a follow-up open-text marked 'mandatory': e.g., 'What was the main challenge during setup, if any?' |
| c5 | Specifies sampling, cadence, and a fatigue cap (no respondent over-surveyed) plus a response-rate floor below which results are flagged insufficient, not reported as fact | PASS | Each survey has sampling strategy, cadence, fatigue control (e.g., 'no respondent surveyed more than once per 90 days'), and response-rate floors with explicit 'insufficient sample' flags. |
| c6 | Defines a quant-to-qual synthesis method — verbatim coding into a stable code frame, driver analysis tying themes to score movement, and a segment cut | PASS | Section 4 has: stable code frame (8 themes with definitions), driver analysis per metric (e.g., themes in ≥40% of low-CES vs high-CES), segment cut by plan tier/signup source/cohort. |
| c7 | Designs BOTH an inner loop (individual detractor → individual recovery action with owner + SLA) and an outer loop (saturated theme → product/process change) — not just one | PASS | Section 5 has explicit 'Inner loop' table (CES≤3→4h SLA, CSAT≤2→24h, etc.) and 'Outer loop' table (saturation threshold→backlog discovery input). |
| c8 | Sets governance with anti-gaming guards — no soliciting high scores, report trend not absolute value, raw verbatims visible to those who act | PASS | Governance section lists four numbered anti-gaming guards: no solicitation coaching, raw verbatims visible, no selective sampling, response rate published. |
| c9 | Treats this as the structured-research VoC lens among several — does NOT centralise feedback ownership; cross-consults support, customer-success, and GTM rather than absorbing their feedback streams | PASS | Cross-Consultation section: 'Support owns the ticket stream...Customer-success owns adoption metrics...GTM owns why deals close.' Chat summary: 'Explicit conflict flags...overlap is intentional—don't centralise.' |
| c10 | Distinguishes this ongoing-programme work from a one-off survey or a persona artifact (does not drift into building a persona) | PARTIAL | Programme is framed as ongoing with quarterly NPS, weekly synthesis, review triggers, and cadence tables. No persona artifact appears. However, no explicit statement distinguishing from one-off surveys. |
| c11 | Output is written to the given path and follows the skill's Output Format (Objectives, Metric Selection, Survey Design, Quant-to-Qual Synthesis, Closing the Loop, Governance, Cross-Consultation sections) | PASS | File written to `/var/folders/.../work/voc-programme.md`. All seven sections present: Objectives, Metric Selection, Survey Design, Quant-to-Qual Synthesis, Closing the Loop, Governance, Cross-Consultation. |
| c12 | Output's metric-selection table maps each of the three stated objectives to a specific metric with a trigger point and a rationale — onboarding→CES, churn-risk→NPS (relationship), release→CSAT/NPS | PASS | Metric Selection table has Objective, Metric, Trigger point, Rationale columns. Three rows map exactly: onboarding→CES (after setup), churn→NPS+CSAT (quarterly+triggered), release→CSAT (48h post-release). |
| c13 | Output includes a Cross-Consultation section naming the other VoC lenses (support, customer-success, GTM) and where their reads may conflict with this programme's — surfacing conflict rather than reconciling it away | PASS | Cross-Consultation section has three subsections for Support, Customer-success, and GTM, each ending with 'Conflict to expect:' paragraph explicitly naming the divergence and saying 'Don't reconcile—surface both.' |

### Notes

The blueprint is comprehensive and well-structured, meeting nearly every criterion with specific evidence. The only minor gap is c10 (partial ceiling): the programme is clearly ongoing in practice but never explicitly contrasts itself with a one-off survey or persona exercise.
