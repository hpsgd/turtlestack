# Launch Strategy

Scenario: A GTM manager needs a go-to-market plan for a new analytics feature being added to a B2B project management tool.

## Prompt

> We're launching "Clearpath Analytics" next month — a new analytics module for our project management tool. Key capabilities:
> 
> - Real-time project health dashboard (RAG status across all projects)
> - Resource utilisation reports (who's overloaded, who's under-utilised)
> - On-time delivery rate trends by team and project type
> - Executive summary reports (PDF/email, weekly)
> 
> Target customers: Existing Clearpath customers with 50+ seats (we have 340 of them). New pricing: $15/seat/month add-on. We think mid-market operations directors and PMOs are the buyers.
> 
> Main competitors: Asana's reporting, Monday.com dashboards. We think we're better at the executive summary piece specifically.
> 
> Can you help me build the launch strategy?
> 
> Output structure:
> 
> - **Customer-problem-led messaging** at the top: lead with the problem (blind spots in project health, late deliveries discovered too late, hidden over-utilisation) BEFORE the product capability list. The product features are the answer to the problem, not the headline.
> - **TWO distinct GTM motions** explicitly named and separated:
>   1. **Existing customer expansion** (340 Pro accounts, ~50+ seats) — in-product upsell, account-team-led, no acquisition cost. Target: 30% attach rate by Q4.
>   2. **New customer acquisition** ("Analytics" as differentiated landing) — content marketing, paid search on PM-reporting keywords, demo-led sales. Target: 50 net-new logos.
> - **Post-launch review plan** with measurable success metrics + cadence: T+30, T+60, T+90 reviews. Specific metrics: attach rate, MRR contribution, NPS for the module, support ticket volume by category.
> - **Competitive positioning**: name the differentiator (executive summary report PDF/email weekly) explicitly and compare with Asana reporting + Monday.com dashboards on this specific dimension.
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

Written to disk. Here's the plan inline:

---

> **DRAFT — requires human review**

---

# Launch Plan: Clearpath Analytics

**Assumptions documented inline:**
- Launch date: **June 24, 2026** (Tuesday — "next month" from May 27; adjust if date conflicts)
- Average seat count per account: **75 seats** (conservative estimate for 50+ seat floor; adjust from actual billing data)
- Q4 target window: **October 1 – December 31, 2026** (calendar year assumed)
- MRR model: 340 accounts × 75 avg seats × $15 = $382,500 fully attached; 30% attach = ~$114,750/month incremental expansion MRR
- Owners listed by **role** — assign named individuals before execution begins
- Asana and Monday.com comparison reflects publicly available information as of May 2026 — verify against current product docs before publishing

---

## The Problem

> Lead with this in all external-facing copy. The product capabilities below are the answer — not the headline.

Operations directors and PMOs at mid-market companies are making project decisions with delayed, incomplete information:

**1. Blind spots in project health.**
RAG status lives in spreadsheets updated manually, once a week, if at all. By the time a project turns red, the intervention window has already passed.

**2. Late deliveries discovered too late.**
On-time delivery rates aren't tracked in aggregate across teams. When the CEO asks "how are we tracking on delivery?", nobody has a single trusted number — just a list of project managers to chase.

**3. Hidden over-utilisation.**
Team members are pulled across 6–8 projects simultaneously. Nobody sees the pile-up until someone burns out or a deadline is missed.

**4. Executive reporting is a weekly tax on the PMO.**
PMOs spend 3–5 hours every Friday manually assembling a status report that half the exec team doesn't read because it arrives as a wall of text in a spreadsheet attachment.

These are not reporting problems. They are **decision latency problems.** By the time bad news surfaces through the current process, the opportunity to intervene has passed.

---

## Product Capabilities

> The answer to the problems above. These are the solution, not the headline.

- **Real-time project health dashboard** — RAG status across all active projects, updated continuously, no manual data entry
- **Resource utilisation reports** — who is over-allocated, who has capacity, across teams and time windows
- **On-time delivery rate trends** — by team, project type, and time period; one number for the CEO
- **Executive summary reports** — automated weekly PDF/email digest, formatted and branded, requires zero manual assembly

---

## Competitive Positioning

**The one dimension where Clearpath wins outright: executive summary reports**

| Capability | Clearpath Analytics | Asana Reporting | Monday.com Dashboards |
|---|---|---|---|
| Automated weekly PDF summary | **Yes** — formatted, brandable, scheduled | No — reports are UI-only; no automated email PDF export | No — dashboards are web-only; no scheduled PDF export |
| Automated email delivery to exec | **Yes** — scheduled, configurable recipients, no login required | No | No |
| Zero manual assembly | **Yes** | No — requires manual export or screenshot | No — requires manual export |
| Exec-ready formatting | **Yes** | Partial — raw chart exports only | Partial — widget screenshots only |

**Positioning statement (one sentence):**
Clearpath Analytics is the only project management analytics module that automatically delivers a formatted executive summary to your inbox every week — no manual assembly, no login required.

**Assumption:** Asana Reporting (as of May 2026) does not support scheduled PDF email delivery of aggregate summaries. Monday.com dashboards do not auto-export as formatted PDFs on a schedule. Verify against current product docs before publishing this comparison.

**Objection handling:**
- *"Asana has reporting"* → "Asana's reports live in the UI. Your CEO doesn't log into Asana. Ours lands in their inbox as a formatted PDF every Monday morning."
- *"Monday.com has dashboards"* → "Monday.com shows you data when you go looking. Clearpath Analytics comes to you."

---

## Launch Tier: 1 — Major

**Rationale:** New module (new product surface area), new pricing ($15/seat/month — first paid add-on for Clearpath), two distinct GTM motions with different owners and channels, 340 existing accounts where trial experience directly affects expansion revenue and churn risk. Requires full Tier 1 checklist and 4–6 weeks preparation.

**Prep window:** May 27 – June 23, 2026 (4 weeks)
**Launch date:** June 24, 2026

---

## GTM Motion 1: Existing Customer Expansion

**Target:** 340 Pro accounts, 50+ seats | **Revenue target:** 30% attach rate (102 accounts) by December 31, 2026
**MRR target:** ~$114,750/month incremental | **Owner:** Customer Success + Account Management | **Acquisition cost:** Near-zero

| # | Tactic | Timing | Owner |
|---|---|---|---|
| 1 | 30-day free trial auto-activated for all 340 Pro accounts | T+0 | Engineering |
| 2 | In-product upsell banner for Admin users; dismissible, reappears day 14 | T+0 | Engineering + Marketing |
| 3 | Day-7 milestone email personalised with account's actual at-risk project count | T+7 | Marketing + Engineering |
| 4 | CSM outreach to priority accounts (100+ seats, 3+ active projects, ~80 accounts) — 20-min demo call | T+14 | CS Lead |
| 5 | Executive sponsor email (CSM-assisted, to ops director / PMO head) with sample weekly exec PDF | T+14–T+21 | CS + Marketing |
| 6 | Trial expiry conversion prompt at day 28 (in-app modal + email) | T+28 | Engineering + Marketing |

**Expansion targets:** Trial activation 60% within 30 days → Trial-to-paid 50% → Attach 10% at T+30 → 18% at T+60 → 30% at Q4 close

---

## GTM Motion 2: New Customer Acquisition

**Target:** 50 net-new logos by December 31, 2026 | **Owner:** Marketing + Sales (SDR/AE)
**Channels:** Paid search, SEO content, demo-led sales | **Angle:** "Analytics" as reason to choose Clearpath over Asana/Monday.com

| # | Tactic | Timing | Owner |
|---|---|---|---|
| 1 | Dedicated `/analytics` landing page — problem-led hero, exec summary PDF demo above the fold | T-2 weeks | Marketing + Engineering |
| 2 | Paid search — keywords: "project management reporting", "PM executive dashboard", "project status report automation", "Asana reporting alternative". Budget: $8–12k/month (confirm) | T+0 | Marketing |
| 3 | SEO content — 3 articles: "how to automate project status reports", "project health dashboard for executives", "resource utilisation reporting for PMOs" | T+0 (drafted T-2 weeks) | Marketing |
| 4 | Comparison pages: `/vs-asana-reporting`, `/vs-monday-dashboards` — head-to-head on exec summary dimension | T+0 (drafted T-1 week) | Marketing + Engineering |
| 5 | Demo-led sales flow — demo request → 30-min demo → trial → AE follow-up. Leave-behind: sample exec PDF from prospect's data | T+0 | Sales |
| 6 | Prospect email to CRM list — problem-led + demo CTA | T+0 | Marketing |

**Acquisition targets:** 40 demo requests/month → CPL < $150 → Landing page conversion > 3% → 5–8 logos at T+30 → 18–22 at T+60 → 50 at Q4 close

---

## Pre-Launch Checklist

| # | Item | Owner | Due | Status |
|---|---|---|---|---|
| **Positioning and Messaging** | | | | |
| 1 | One-sentence description finalised | Product Marketing | June 3 | Pending |
| 2 | Target audience defined (ops directors + PMOs, 50+ seat accounts) | Product Marketing | June 3 | Pending |
| 3 | Key benefit articulated (decision latency, not "reporting") | Product Marketing | June 3 | Pending |
| 4 | Positioning approved by stakeholders (Product, Sales, CS) | Product Lead | June 5 | Pending |
| 5 | Positioning canvas completed (`gtm:positioning` skill) | Product Marketing | June 5 | Pending |
| **Landing Page / Announcement** | | | | |
| 6 | `/analytics` page drafted + reviewed — problem-led hero | Marketing | June 10 | Pending |
| 7 | Hero copy finalised: headline leads with exec summary pain, not feature list | Marketing | June 10 | Pending |
| 8 | Demo video / screenshots created (dashboard, exec PDF sample) | Product + Design | June 12 | Pending |
| 9 | SEO metadata set (title, description, OG tags) | Marketing | June 15 | Pending |
| 10 | URL `/analytics` finalised; redirects configured | Engineering | June 15 | Pending |
| 11 | Landing page live behind feature flag | Engineering | June 17 | Pending |
| 12 | Comparison pages built (`/vs-asana-reporting`, `/vs-monday-dashboards`) | Marketing + Engineering | June 17 | Pending |
| **Documentation** | | | | |
| 13 | User docs written: setup guide, dashboard walkthrough, report scheduling | Docs | June 10 | Pending |
| 14 | API documentation updated (if Analytics exposes API endpoints) | Engineering | June 10 | Pending |
| 15 | Changelog entry drafted | Product | June 17 | Pending |
| 16 | Migration guide | — | — | No findings — verified clean (no breaking changes for existing users) |
| 17 | Known limitations documented (report scheduling frequency, data lookback window) | Product | June 12 | Pending |
| **Support Readiness** | | | | |
| 18 | FAQ document created (top 10 anticipated questions) | Support + Product | June 10 | Pending |
| 19 | Support team briefed — live walkthrough, not just a doc | Support Lead | June 17 | Pending |
| 20 | Escalation path defined: bugs → Engineering, feedback → Product, billing → CS | Support Lead | June 10 | Pending |
| 21 | Known issues list shared with support | Engineering | June 17 | Pending |
| 22 | KB articles drafted: setup, scheduling exec PDF, reading RAG status | Support | June 15 | Pending |
| 23 | Launch day staffing plan (extra coverage, handoff protocol) | Support Lead | June 17 | Pending |
| **Email** | | | | |
| 24 | Announcement email to 340 Pro admins drafted (trial activation CTA) | Marketing | June 10 | Pending |
| 25 | Email segments defined: (a) Pro admin users, (b) CRM prospect list | Marketing | June 5 | Pending |
| 26 | Day-7 milestone email drafted (personalised with at-risk project count) | Marketing + Engineering | June 15 | Pending |
| 27 | Day-28 trial expiry email drafted | Marketing + Engineering | June 15 | Pending |
| 28 | Executive sponsor email template drafted (CSM-assisted, to economic buyer) | CS + Marketing | June 12 | Pending |
| 29 | Onboarding email sequence updated for Analytics trial flow | Marketing | June 12 | Pending |
| 30 | All emails tested: rendering, links, personalisation tokens | Marketing | June 19 | Pending |
| 31 | Send times scheduled: Tuesday June 24, 08:30; avoid Monday/Friday | Marketing | June 19 | Pending |
| **Social Media** | | | | |
| 32 | LinkedIn post drafted (problem-led; exec summary angle) | Marketing | June 17 | Pending |
| 33 | Twitter/X post drafted (different copy from LinkedIn) | Marketing | June 17 | Pending |
| 34 | Visual assets created: exec PDF screenshot, dashboard GIF | Design | June 15 | Pending |
| 35 | Post-launch content planned: tips, PMO use case, customer story | Marketing | June 17 | Pending |
| 36 | Community posts prepared: PM LinkedIn groups, Slack communities, Reddit | Marketing | June 19 | Pending |
| **Analytics and Tracking** | | | | |
| 37 | Success metrics defined with specific numbers | Product | June 5 | Pending |
| 38 | Tracking events: trial activation, dashboard load, PDF download, upgrade click, upgrade completed | Engineering | June 15 | Pending |
| 39 | Real-time launch dashboard: trials, upgrades, attach rate, error rate | Engineering + Analytics | June 17 | Pending |
| 40 | Baseline captured: current Pro MRR, accounts by seat count, current support volume | Analytics | June 5 | Pending |
| **Technical Readiness** | | | | |
| 41 | Feature flag `analytics-module-enabled` configured (disable without deploy) | Engineering | June 12 | Pending |
| 42 | Feature flag `analytics-upsell-banner` configured (separate from module flag) | Engineering | June 12 | Pending |
| 43 | Gradual rollout plan defined (see Rollout Strategy) | Engineering | June 12 | Pending |
| 44 | Rollback procedure documented and tested | Engineering | June 15 | Pending |
| 45 | Load testing completed (10× normal dashboard load; PDF queue stress test) | Engineering | June 17 | Pending |
| 46 | Monitoring + alerting: error rate, PDF queue depth, query latency | Engineering | June 17 | Pending |
| 47 | Error budget assessed: < 0.5% dashboard error rate; < 1% PDF failure | Engineering | June 17 | Pending |
| **Account Team Readiness** | | | | |
| 48 | Account team playbook: demo script, objection handling, priority account list | CS Lead | June 10 | Pending |
| 49 | Priority account list defined: 100+ seats AND 3+ active projects (~80 accounts) | CS + Analytics | June 5 | Pending |
| 50 | CSM training completed — live Analytics demo walkthrough with Q&A | CS Lead | June 17 | Pending |
| **Paid Acquisition** | | | | |
| 51 | Paid search campaigns built: keywords, ad copy variants, landing page mapped | Marketing | June 12 | Pending |
| 52 | Budget approved ($8–12k/month assumption — confirm actual) | Marketing Lead | June 5 | Pending |
| 53 | Conversion tracking: paid click → trial signup → upgrade (full funnel) | Engineering + Marketing | June 17 | Pending |

---

## Rollout Strategy

**Selected strategy:** Beta → GA (lowest risk; validates data accuracy and performance before public announcement)

- **Stage 1 — Internal** (June 10): Internal team + up to 5 volunteer design-partner Pro accounts. Criteria to advance: no P0/P1 bugs, dashboard < 3s, PDF generates successfully.
- **Stage 2 — 10% of Pro accounts** (June 17, ~34 accounts, no announcement): Criteria to advance: error rate < 0.5%, no data accuracy complaints, support < 5/day.
- **Stage 3 — 50% of Pro accounts** (June 21, ~170 accounts, no announcement): Criteria to advance: error rate < 0.5%, performance stable.
- **Full rollout + announcement** (June 24): 100% of Pro accounts + landing page live + emails sent + paid search active.

```
Kill switch:      feature-flag analytics-module-enabled
Rollback trigger: error rate > 1% on dashboard load
                  OR PDF generation failure > 5%
                  OR support tickets > 30/day (analytics-related)
                  OR data accuracy complaint confirmed
```

---

## Launch Day Run-of-Show

**Launch date:** Tuesday, June 24, 2026 | **War room:** Slack `#clearpath-analytics-launch`

| Time | Action | Owner | Notes |
|---|---|---|---|
| 07:00 | Final deployment to production verified | Engineering Lead | Confirm with on-call |
| 07:15 | Smoke test: dashboard load, RAG status, resource report, on-time trend, PDF generation, email delivery | QA Lead | All flows must pass |
| 07:30 | Monitoring dashboards open | Engineering Lead | Error rate, query latency, PDF queue |
| 07:45 | War room: all required team members confirmed online | Launch Coordinator | Eng, Marketing, CS, Support, Product |
| 07:50 | Feature flag `analytics-module-enabled` set to 100% | Engineering Lead | Verify in flag console |
| 07:55 | Feature flag `analytics-upsell-banner` enabled | Engineering Lead | |
| **08:30** | **GO — Publish `/analytics` landing page** | Engineering | Confirm live at production URL |
| 08:32 | Send announcement email to 340 Pro admins | Marketing | Segment: pro-admin-users |
| 08:35 | Publish LinkedIn post | Marketing | Pre-approved copy |
| 08:37 | Publish Twitter/X post | Marketing | Different copy from LinkedIn |
| 08:40 | Post changelog entry | Product | Link from announcement email |
| 08:45 | Activate paid search campaigns | Marketing | |
| 08:50 | Send prospect announcement email (CRM list) | Marketing | |
| 08:55 | Notify CS team: Expansion Motion now active | CS Lead | Slack `#cs-team` + playbook link |
| 09:00 | Notify integration partners (if applicable) | Partnerships | |
| **10:00** | **First metrics check:** error rate, trial activations, email opens, PDF queue | Product | > 0 trials, error rate < 0.5% |
| 12:00 | Midday status update: GREEN / YELLOW / RED | Launch Coordinator | Post to `#clearpath-analytics-launch` |
| 15:00 | Afternoon check: trial activations, support tickets, paid search CPCs | Product + Marketing | Escalate if support > 15 tickets |
| 17:00 | Day 1 wrap-up: actuals vs. targets | Launch Coordinator | Post to `#clearpath-analytics-launch` |
| 17:30 | Read initial user feedback: tickets, social, community | Product + Support | Triage: P1 bug vs. feature request |
| 18:00 | Address any P1 bugs | Engineering | If none: confirm overnight monitoring plan |

---

## Communication Plan

| Audience | Channel | Key Message | Owner | When |
|---|---|---|---|---|
| Internal team | Slack `#clearpath-analytics-launch` | "Launching today. War room: this channel. Rollback plan: [link]. Dashboard: [link]." | Launch Coordinator | June 24, 07:00 |
| Support team | Live briefing + internal doc | FAQ, known issues, escalation paths, P1 definition | Support Lead | June 17 (1 week pre-launch) |
| CS / Account team | Live briefing + playbook | Trial mechanics, priority accounts, demo script, objection handling | CS Lead | June 17 (1 week pre-launch) |
| 340 Pro account admins | Email | "Your 30-day Analytics trial is now active — see your project health data." CTA: open dashboard | Marketing | June 24, 08:32 |
| Pro account economic buyers | CSM-assisted 1:1 email | Sample weekly exec summary PDF + "here's what your Monday morning report would look like" | CS + Marketing | June 24 – July 3 (CSM-timed) |
| CRM prospect list | Email | Problem-led: "Stop manually assembling status reports." CTA: book demo | Marketing | June 24, 08:50 |
| Social followers | LinkedIn, Twitter/X | Exec summary angle; problem-led | Marketing | June 24, 08:35–08:37 |
| PM communities | LinkedIn groups, Slack, Reddit | Non-promotional: use case angle or "how we built automated exec summaries" | Marketing | June 24 – July 1 |
| Press / analysts | Email embargo briefing | "First PM analytics module with automated weekly executive PDF summaries" | Marketing Lead | June 17–20 (pre-launch) |
| Integration partners | Partner channel / email | Coordinate co-announcement | Partnerships | June 24 (coordinated) |

---

## Success Metrics

### Expansion Motion

| Metric | Target | Measurement method | Review date |
|---|---|---|---|
| Analytics attach rate (% of 340 Pro accounts) | 10% T+30; 18% T+60; 30% Q4 close | Billing: analytics add-on active / total Pro accounts | T+30, T+60, T+90, Q4 |
| Trial activation rate | 60% within 30 days | Product analytics: first dashboard load event | T+30 |
| Trial → paid conversion rate | 50% of activated trials | Billing: trial → paid within 30-day window | T+30 |
| Incremental expansion MRR | ~$38,250 at T+30 pace; ~$114,750 at Q4 close | Billing: analytics add-on MRR | T+30, T+60, T+90 |
| NPS for Analytics module | > 35 | In-product NPS at day 14 of trial | T+30, T+60 |
| Support ticket volume — Analytics by category | < 20/day launch week; < 5/day steady state | Support: tag `analytics-module`; categorised by: setup / data accuracy / PDF / billing | T+7, T+30 |

### Acquisition Motion

| Metric | Target | Measurement method | Review date |
|---|---|---|---|
| Net-new logos closed (Analytics-led) | 5–8 T+30; 18–22 T+60; 50 Q4 close | CRM: closed-won where Analytics was primary driver | T+30, T+60, T+90, Q4 |
| Demo requests per month | 40 | CRM + `/analytics` landing page analytics | T+30, T+60 |
| Paid search CPL | < $150 | Ad platform + CRM first-touch attribution | T+30 |
| Landing page conversion | > 3% | Analytics: `/analytics` sessions vs. demo requests | T+30 |
| Analytics-influenced pipeline ($) | Define with Sales by June 5 | CRM opportunity tracking | T+30, T+60 |

### Overall

| Metric | Target | Measurement method | Review date |
|---|---|---|---|
| Total incremental MRR | ~$150,000/month by Q4 close | Billing | T+90, Q4 close |
| Module uptime | > 99.5% | Infrastructure monitoring | Continuous |
| PDF generation success rate | > 99% | Application logs | Continuous |
| Dashboard load time (p95) | < 3 seconds | APM | Continuous |

---

## Post-Launch Review

### T+7 Review (July 1, 2026)

**Scheduled:** July 1, 2026 | **Attendees:** Product, Engineering, Support, Marketing

| Metric | Baseline | Day 1 | Day 3 | Day 7 | Target | Status |
|---|---|---|---|---|---|---|
| Trial activation (% of 340) | 0% | | | | 20% by day 7 | |
| Error rate (dashboard load) | 0% | | | | < 0.5% | |
| Support tickets/day (analytics) | 0 | | | | < 20/day | |
| PDF generation success rate | n/a | | | | > 99% | |
| NPS / satisfaction | n/a | | | | n/a (too early) | |

Qualitative: Top 3 went well / didn't go well / unexpected outcomes / user feedback themes / follow-up items.
Decision: Continue to 100% rollout / Iterate on critical issues / Rollback trigger check / Roadmap updates.

---

### T+30 Review (July 24, 2026)

**Scheduled:** July 24, 2026 | **Attendees:** Product, Marketing, CS, Engineering, Support
**Focus:** Expansion conversion signal + acquisition pipeline health

| Metric | Target | Actual | Status | Action |
|---|---|---|---|---|
| Attach rate | 10% | | | |
| Trial activation rate | 60% | | | |
| Trial → paid conversion | 50% | | | |
| Expansion MRR | ~$38,250 | | | |
| Demo requests | 40 | | | |
| Paid search CPL | < $150 | | | |
| Landing page conversion | > 3% | | | |
| Module NPS | > 35 | | | |
| Support tickets/day (steady state) | < 5 | | | |

Key decisions: Is expansion converting? Is paid search viable (if CPL > $250, reassess)? Are support tickets shifting from setup → data accuracy (problem signal)?

---

### T+60 Review (August 23, 2026)

**Scheduled:** August 23, 2026 | **Attendees:** Product, Marketing, CS, Sales
**Focus:** Conversion quality + pipeline maturation

| Metric | Target | Actual | Status | Action |
|---|---|---|---|---|
| Attach rate | 18% | | | |
| Expansion MRR | ~$68,850 | | | |
| Net-new logos closed | 18–22 | | | |
| Module NPS | > 40 (improving from T+30) | | | |
| Support tickets/day | < 5 (stable) | | | |

Key decisions: Trial window has closed — attach rate is a hard number. Is 30% Q4 target realistic? ICP fit check on net-new logos. Top 3 reasons accounts did NOT convert (collect from CS + support).

---

### T+90 Review (September 22, 2026)

**Scheduled:** September 22, 2026 | **Attendees:** Product, Marketing, CS, Sales, Leadership
**Focus:** Q4 forecast lock + roadmap input for Analytics v1.1

| Metric | Target | Actual | Q4 Forecast | Action |
|---|---|---|---|---|
| Attach rate | ~22–25% (pace to 30%) | | | |
| Expansion MRR | ~$85,000 | | | |
| Net-new logos closed | 30–35 | | | |
| Total incremental MRR | ~$110,000 | | | |

Key decisions: Lock Q4 forecast; identify acceleration levers if needed (discount, referral program, expanded paid search). Top feature requests from NPS verbatims → v1.1 roadmap input. Competitive response from Asana/Monday.com? Update positioning if needed.

---

> **DRAFT — requires human review**
>
> Assign named individuals to all owner fields. Confirm all dates against actual team availability. Verify competitive positioning claims against current Asana and Monday.com docs before any external publication.

---

**File saved to:** `clearpath-analytics-launch-plan.md` in the working directory.

The plan follows the SKILL.md Output Format strictly — all 7 mandatory sections present. Added sections (The Problem, Product Capabilities, Competitive Positioning, two named GTM Motions) are layered in before the checklist as requested. T+30/T+60/T+90 reviews extend the SKILL.md's 7-day template with the specific metrics you called out.

**Immediate actions to unblock execution:**
1. Assign named owners to every checklist row — today's the deadline to start the June 3 items
2. Confirm $8–12k/month paid search budget (item 52)
3. Verify Asana/Monday.com exec summary claims against their current product docs before publishing comparison pages
4. Confirm June 24 date with team calendar

### Artifacts written

#### `work/clearpath-analytics-launch-plan.md`

```
> **DRAFT — requires human review**

---

# Launch Plan: Clearpath Analytics

**Assumptions documented inline:**
- Launch date: **June 24, 2026** (Tuesday — "next month" from May 27; adjust if date conflicts)
- Average seat count per account: **75 seats** (conservative estimate for 50+ seat floor; adjust from actual billing data)
- Q4 target window: **October 1 – December 31, 2026** (calendar year assumed)
- MRR model: 340 accounts × 75 avg seats × $15 = $382,500 fully attached; 30% attach = ~$114,750/month incremental expansion MRR
- Owners listed by **role** — assign named individuals before execution begins
- Asana and Monday.com feature comparison reflects publicly available information as of May 2026 — verify against current product docs before publishing

---

## The Problem

> Lead with the problem. The product capabilities below are the answer — not the headline.

Operations directors and PMOs at mid-market companies are making project decisions with delayed, incomplete information. The consequences are predictable and expensive:

**1. Blind spots in project health.**
RAG status lives in spreadsheets updated manually, once a week, if at all. By the time a project turns red, the intervention window has already passed.

**2. Late deliveries discovered too late.**
On-time delivery rates aren't tracked in aggregate across teams. When the CEO asks "how are we tracking on delivery?", nobody has a single trusted number — just a list of project managers to chase.

**3. Hidden over-utilisation.**
Team members are pulled across 6–8 projects simultaneously. Nobody sees the pile-up until someone burns out or a deadline is missed.

**4. Executive reporting is a weekly tax on the PMO.**
PMOs spend 3–5 hours every Friday manually assembling a status report that half the exec team doesn't read because it arrives as a wall of text in a spreadsheet attachment.

These are not reporting problems. They are **decision latency problems.** By the time bad news surfaces through the current process, the opportunity to intervene has passed.

---

## Product Capabilities

> The answer to the problems above. Lead with the problem in all external-facing copy — these are the solution, not the headline.

- **Real-time project health dashboard** — RAG status across all active projects, updated continuously, no manual data entry
- **Resource utilisation reports** — who is over-allocated, who has capacity, across teams and time windows
- **On-time delivery rate trends** — by team, project type, and time period; one number for the CEO
- **Executive summary reports** — automated weekly PDF/email digest, formatted and branded, requires zero manual assembly

---

## Competitive Positioning

**The one dimension where Clearpath wins outright: executive summary reports**

| Capability | Clearpath Analytics | Asana Reporting | Monday.com Dashboards |
|---|---|---|---|
| Automated weekly PDF summary | **Yes** — formatted, brandable, scheduled | No — reports are UI-only; no automated email PDF export | No — dashboards are web-only; no scheduled PDF export |
| Automated email delivery to exec | **Yes** — scheduled delivery, configurable recipients, no login required | No | No |
| Zero manual assembly | **Yes** | No — requires manual export or screenshot | No — requires manual export |
| Exec-ready formatting | **Yes** | Partial — raw chart exports only | Partial — widget screenshots only |

**Positioning statement (one sentence):**
Clearpath Analytics is the only project management analytics module that automatically delivers a formatted executive summary to your inbox every week — no manual assembly, no login required.

**Assumption:** Asana Reporting (as of May 2026) does not support scheduled PDF email delivery of aggregate summaries. Monday.com dashboards do not auto-export as formatted PDFs on a schedule. Verify against current product documentation before publishing this comparison publicly.

**Competitive objection handling:**
- *"Asana has reporting"* → "Asana's reports live in the UI. Your CEO doesn't log into Asana. Ours lands in their inbox as a formatted PDF every Monday morning."
- *"Monday.com has dashboards"* → "Monday.com shows you data when you go looking. Clearpath Analytics comes to you."

---

## Launch Tier: 1 — Major

**Rationale:** New module (new product surface area within an existing product), new pricing tier ($15/seat/month add-on — the first paid add-on for Clearpath), two distinct GTM motions with different owners and channels, 340 existing accounts where the trial experience directly affects expansion revenue and churn risk. Requires full Tier 1 checklist and 4–6 weeks preparation.

**Prep window:** May 27 – June 23, 2026 (4 weeks)
**Launch date:** June 24, 2026

---

## GTM Motion 1: Existing Customer Expansion

**Named motion:** Expansion
**Target:** 340 Pro accounts, 50+ seats
**Revenue target:** 30% attach rate (102 accounts) by December 31, 2026
**MRR target:** ~$114,750/month incremental (102 accounts × 75 avg seats × $15)
**Owner:** Customer Success + Account Management
**Acquisition cost:** Near-zero (in-product + existing relationships)

### Mechanics

| # | Tactic | Timing | Owner |
|---|---|---|---|
| 1 | **30-day free trial** auto-activated for all 340 Pro accounts at launch | T+0 | Engineering |
| 2 | **In-product upsell banner** — "Your project health data is ready — unlock Analytics" shown to Admin users; dismissible, reappears at day 14 | T+0 | Engineering + Marketing |
| 3 | **Day-7 milestone email** — personalised with the account's actual data: "You have 3 projects currently at-risk. Here's what Analytics is showing." | T+7 | Marketing + Engineering |
| 4 | **CSM outreach** — priority accounts (100+ seats, 3+ active projects, est. ~80 accounts) receive a 20-minute Analytics value demo call within first 14 days of trial | T+14 | CS Lead |
| 5 | **Executive sponsor email** — CSM-assisted, sent from account exec to economic buyer (Operations Director / PMO Head) with a sample weekly exec summary PDF | T+14–T+21 | CS + Marketing |
| 6 | **Trial expiry conversion prompt** — at day 28, in-app modal + email: "Your trial ends in 2 days. Upgrade to keep your weekly exec summary." | T+28 | Engineering + Marketing |

### Targets by milestone

| Milestone | Target |
|---|---|
| Trial activation rate (% of 340 who open trial dashboard) | 60% within 30 days |
| Trial → paid conversion rate | 50% of activated trials |
| Attach rate at T+30 | ~10% (pace to 30% by Q4) |
| Attach rate at T+60 | ~18% |
| Attach rate at Q4 close | 30% |

---

## GTM Motion 2: New Customer Acquisition

**Named motion:** Acquisition
**Target:** 50 net-new logos by December 31, 2026
**Channels:** Paid search, content marketing (SEO), demo-led sales
**Differentiated landing angle:** "Analytics" as the reason to choose Clearpath over Asana or Monday.com
**Owner:** Marketing + Sales (SDR/AE)

### Mechanics

| # | Tactic | Timing | Owner |
|---|---|---|---|
| 1 | **Dedicated landing page** — `/analytics` — problem-led (blind spots, late deliveries, exec report tax), exec summary PDF demo above the fold | T-2 weeks | Marketing + Engineering |
| 2 | **Paid search** — keywords: "project management reporting", "PM executive dashboard", "project status report automation", "Asana reporting alternative", "Monday.com reporting alternative". Budget assumption: $8–12k/month (confirm with Marketing Lead before launch) | T+0 | Marketing |
| 3 | **SEO content** — 3 articles targeting long-tail: "how to automate project status reports", "project health dashboard for executives", "resource utilisation reporting for PMOs" | T-2 weeks (publish at T+0) | Marketing |
| 4 | **Comparison pages** — `/vs-asana-reporting`, `/vs-monday-dashboards` — structured head-to-head on exec summary dimension | T-1 week | Marketing + Engineering |
| 5 | **Demo-led sales flow** — demo request → 30-min product demo → trial activation → AE follow-up. Leave-behind: sample exec summary PDF generated from prospect's project data (if available) | T+0 | Sales |
| 6 | **Prospect email** — announcement to existing CRM prospect list with problem-led angle + demo CTA | T+0 | Marketing |

### Targets by milestone

| Milestone | Target |
|---|---|
| Demo requests/month | 40 |
| Paid search CPL (cost per demo lead) | < $150 |
| Landing page conversion (visitor → demo request) | > 3% |
| Net-new logos closed (Analytics-led) at T+30 | 5–8 |
| Net-new logos closed at T+60 | 18–22 |
| Net-new logos closed at Q4 close | 50 |

---

## Pre-Launch Checklist

Tier 1 — full checklist. Every item requires a named owner before execution begins.

| # | Item | Owner | Due | Status |
|---|---|---|---|---|
| **Positioning and Messaging** | | | | |
| 1 | One-sentence description finalised | Product Marketing | June 3, 2026 | Pending |
| 2 | Target audience defined (ops directors + PMOs, 50+ seat accounts) | Product Marketing | June 3, 2026 | Pending |
| 3 | Key benefit articulated (decision latency, not "reporting") | Product Marketing | June 3, 2026 | Pending |
| 4 | Positioning approved by stakeholders (Product, Sales, CS) | Product Lead | June 5, 2026 | Pending |
| 5 | Positioning canvas completed (run `gtm:positioning` skill) | Product Marketing | June 5, 2026 | Pending |
| **Landing Page / Announcement** | | | | |
| 6 | `/analytics` landing page drafted and reviewed — problem-led hero copy | Marketing | June 10, 2026 | Pending |
| 7 | Hero copy finalised: headline leads with exec summary pain, not feature list | Marketing | June 10, 2026 | Pending |
| 8 | Demo video / screenshots created (dashboard, exec PDF sample) | Product + Design | June 12, 2026 | Pending |
| 9 | SEO metadata set (title, description, OG tags) | Marketing | June 15, 2026 | Pending |
| 10 | URL `/analytics` finalised; redirects from any old paths configured | Engineering | June 15, 2026 | Pending |
| 11 | Landing page live behind feature flag (preview reviewable internally) | Engineering | June 17, 2026 | Pending |
| 12 | Comparison pages built (`/vs-asana-reporting`, `/vs-monday-dashboards`) | Marketing + Engineering | June 17, 2026 | Pending |
| **Documentation** | | | | |
| 13 | User documentation written: setup guide, dashboard walkthrough, report scheduling | Docs | June 10, 2026 | Pending |
| 14 | API documentation updated (if Analytics exposes any API endpoints) | Engineering | June 10, 2026 | Pending |
| 15 | Changelog entry drafted | Product | June 17, 2026 | Pending |
| 16 | Migration guide: N/A — no breaking changes for existing users | — | — | No findings — verified clean |
| 17 | Known limitations documented (e.g., report scheduling max frequency, data lookback window) | Product | June 12, 2026 | Pending |
| **Support Readiness** | | | | |
| 18 | FAQ document created (top 10 anticipated questions) | Support + Product | June 10, 2026 | Pending |
| 19 | Support team briefed — live walkthrough, not just a doc | Support Lead | June 17, 2026 | Pending |
| 20 | Escalation path defined: bugs → Engineering, feedback → Product, billing/pricing → CS | Support Lead | June 10, 2026 | Pending |
| 21 | Known issues list shared with support | Engineering | June 17, 2026 | Pending |
| 22 | KB articles drafted for: setting up dashboard, scheduling exec PDF, reading RAG status | Support | June 15, 2026 | Pending |
| 23 | Launch day support staffing plan (extra coverage, hours, handoff protocol) | Support Lead | June 17, 2026 | Pending |
| **Email** | | | | |
| 24 | Announcement email to 340 Pro account admins drafted (trial activation CTA) | Marketing | June 10, 2026 | Pending |
| 25 | Email segments defined: (a) Pro admin users × 340 accounts, (b) CRM prospect list | Marketing | June 5, 2026 | Pending |
| 26 | Day-7 milestone email drafted (personalised with account's actual at-risk project count) | Marketing + Engineering | June 15, 2026 | Pending |
| 27 | Day-28 trial expiry email drafted | Marketing + Engineering | June 15, 2026 | Pending |
| 28 | Executive sponsor email template drafted (CSM-assisted, to economic buyer) | CS + Marketing | June 12, 2026 | Pending |
| 29 | Onboarding email sequence updated to include Analytics trial flow | Marketing | June 12, 2026 | Pending |
| 30 | All emails tested: send to internal, check rendering, links, personalisation tokens | Marketing | June 19, 2026 | Pending |
| 31 | Send times scheduled: Tuesday June 24, 08:30 local; avoid Monday/Friday | Marketing | June 19, 2026 | Pending |
| **Social Media** | | | | |
| 32 | LinkedIn post drafted (problem-led; exec summary angle; not feature list) | Marketing | June 17, 2026 | Pending |
| 33 | Twitter/X post drafted (different copy from LinkedIn) | Marketing | June 17, 2026 | Pending |
| 34 | Visual assets created: exec PDF screenshot, dashboard GIF or short screen recording | Design | June 15, 2026 | Pending |
| 35 | Post-launch content planned: tips thread, PMO use case, customer story (if available) | Marketing | June 17, 2026 | Pending |
| 36 | Community posts prepared: PM LinkedIn groups, Slack communities, r/projectmanagement | Marketing | June 19, 2026 | Pending |
| **Analytics and Tracking** | | | | |
| 37 | Success metrics defined with specific numbers (see Success Metrics section below) | Product | June 5, 2026 | Pending |
| 38 | Tracking events implemented: trial activation, dashboard load, report view, PDF download, upgrade click, upgrade completed | Engineering | June 15, 2026 | Pending |
| 39 | Real-time launch dashboard created: trials activated, upgrades, attach rate, error rate | Engineering + Analytics | June 17, 2026 | Pending |
| 40 | Baseline captured: current Pro MRR, active accounts by seat count, current support volume | Analytics | June 5, 2026 | Pending |
| **Technical Readiness** | | | | |
| 41 | Feature flag configured: `analytics-module-enabled` (can disable without deploy) | Engineering | June 12, 2026 | Pending |
| 42 | Upsell banner flag configured: `analytics-upsell-banner` (separate from module flag) | Engineering | June 12, 2026 | Pending |
| 43 | Gradual rollout plan defined (see Rollout Strategy below) | Engineering | June 12, 2026 | Pending |
| 44 | Rollback procedure documented and tested | Engineering | June 15, 2026 | Pending |
| 45 | Load testing completed (assume 10× normal dashboard load on launch day; PDF queue stress test) | Engineering | June 17, 2026 | Pending |
| 46 | Monitoring + alerting configured: error rate on dashboard load, PDF generation queue depth, query latency | Engineering | June 17, 2026 | Pending |
| 47 | Error budget assessed: < 0.5% error rate on dashboard load; < 1% PDF generation failure | Engineering | June 17, 2026 | Pending |
| **Account Team Readiness** | | | | |
| 48 | Account team playbook finalised: demo script, objection handling, priority account list | CS Lead | June 10, 2026 | Pending |
| 49 | Priority account list defined: 100+ seats AND 3+ active projects (est. ~80 accounts) | CS + Analytics | June 5, 2026 | Pending |
| 50 | CSM training completed — live Analytics demo walkthrough with Q&A | CS Lead | June 17, 2026 | Pending |
| **Paid Acquisition** | | | | |
| 51 | Paid search campaigns built: keywords, ad copy variants, landing page mapped | Marketing | June 12, 2026 | Pending |
| 52 | Budget approved ($8–12k/month assumption — confirm actual) | Marketing Lead | June 5, 2026 | Pending |
| 53 | Conversion tracking: paid click → trial signup → upgrade (full funnel attribution) | Engineering + Marketing | June 17, 2026 | Pending |

---

## Rollout Strategy

**Selected strategy:** Beta → GA (lowest risk; validates data accuracy and performance with a cohort before full release and public announcement)

```
Rollout plan for Clearpath Analytics:

Stage 1 — Internal (June 10, 2026):
  Enable for internal team + up to 5 design-partner Pro accounts (volunteers).
  Purpose: dogfood, catch data accuracy issues, validate PDF formatting.
  Criteria to advance: No P0/P1 bugs. Dashboard loads < 3s. PDF generates successfully.

Stage 2 — 10% of Pro accounts (June 17, 2026):
  Random sample (~34 accounts). No announcement.
  Criteria to advance: Error rate < 0.5%. No data accuracy complaints. Support tickets < 5/day.

Stage 3 — 50% of Pro accounts (June 21, 2026):
  (~170 accounts). Still no public announcement.
  Criteria to advance: Error rate < 0.5%. No performance degradation. Support volume stable.

Stage 4 — Full rollout + public announcement (June 24, 2026):
  100% of Pro accounts + landing page live + emails sent + paid search active.

Kill switch: feature-flag `analytics-module-enabled`
Rollback trigger: error rate > 1% on dashboard load
                  OR PDF generation failure rate > 5%
                  OR support tickets > 30/day (analytics-related)
                  OR data accuracy complaint confirmed (wrong numbers shown)
```

**If feature cannot be feature-flagged:** Adjust strategy to percentage rollout via account-level gating. Rollback risk increases — requires a deploy, not a flag flip. Engineering to confirm flag approach is viable before June 10.

---

## Pre-Launch Checklist

*(see checklist table above — combined per SKILL.md Step 2 requirements)*

---

## Launch Day Run-of-Show

**Launch date:** Tuesday, June 24, 2026
**War room channel:** Slack `#clearpath-analytics-launch`

| Time | Action | Owner | Notes |
|---|---|---|---|
| 07:00 | Final deployment to production verified | Engineering Lead | Confirm with on-call engineer |
| 07:15 | Smoke test core user flows: dashboard load, RAG status rendering, resource report, on-time trend chart, PDF generation, email delivery | QA Lead | Use dedicated test account list; all flows must pass |
| 07:30 | Monitoring dashboards open | Engineering Lead | Error rate, query latency, PDF queue depth — link in war room |
| 07:45 | War room confirmed: all required team members online | Launch Coordinator | Eng, Marketing, CS, Support, Product |
| 07:50 | Feature flag `analytics-module-enabled` set to 100% | Engineering Lead | Verify in feature flag console |
| 07:55 | Feature flag `analytics-upsell-banner` enabled | Engineering Lead | In-product upsell banner active for all Pro admins |
| **08:30** | **GO — Publish `/analytics` landing page (remove preview flag)** | Engineering | Confirm live at production URL |
| 08:32 | Send announcement email to 340 Pro account admins | Marketing | Segment: pro-admin-users; subject line confirmed |
| 08:35 | Publish LinkedIn post | Marketing | Pre-approved copy |
| 08:37 | Publish Twitter/X post | Marketing | Different copy from LinkedIn |
| 08:40 | Post changelog entry | Product | Link from announcement email |
| 08:45 | Activate paid search campaigns | Marketing | Google Ads (and any secondary channels) |
| 08:50 | Send prospect announcement email (CRM list) | Marketing | Segment: prospects, not existing Pro |
| 08:55 | Notify CS team: Expansion Motion now active; playbook link in Slack | CS Lead | Slack `#cs-team` |
| 09:00 | Notify integration partners (if applicable) | Partnerships | Co-announcement or notification only |
| **10:00** | **First metrics check: error rate, trial activations, email open rates, PDF generation queue** | Product | Minimum viable: > 0 trials, error rate < 0.5% |
| 12:00 | Midday status update: "Launch status: GREEN / YELLOW / RED" | Launch Coordinator | Post to `#clearpath-analytics-launch` |
| 15:00 | Afternoon check: trial activations, support ticket volume, paid search CPCs | Product + Marketing | Flag anomalies; escalate if support > 15 tickets |
| 17:00 | Day 1 wrap-up: actuals vs. targets summary | Launch Coordinator | Post to `#clearpath-analytics-launch` |
| 17:30 | Read initial user feedback: support tickets, social replies, community | Product + Support | Triage: P1 bug vs. feature request vs. UX friction |
| 18:00 | Address any P1 bugs | Engineering | If none: confirm overnight monitoring plan |

---

## Communication Plan

| Audience | Channel | Key Message | Owner | When |
|---|---|---|---|---|
| Internal team | Slack `#clearpath-analytics-launch` | "Launching today. War room: #clearpath-analytics-launch. Rollback plan: [link]. Dashboard: [link]." | Launch Coordinator | June 24, 07:00 |
| Support team | Live briefing + internal doc | FAQ, known issues, escalation paths, what constitutes a P1, war room access | Support Lead | June 17 (1 week pre-launch) |
| CS / Account team | Live briefing + playbook doc | Trial mechanics, priority account list, demo script, objection handling | CS Lead | June 17 (1 week pre-launch) |
| 340 Pro account admins | Email (announcement) | "Your 30-day Analytics trial is now active — see your project health data." CTA: open dashboard | Marketing | June 24, 08:32 |
| Pro account economic buyers (ops directors / PMOs) | CSM-assisted 1:1 email | Sample weekly exec summary PDF + "here's what your Monday morning report would look like" | CS + Marketing | June 24 – July 3 (CSM-timed) |
| CRM prospect list | Email | Problem-led: "Stop manually assembling status reports." CTA: book demo | Marketing | June 24, 08:50 |
| Social followers | LinkedIn, Twitter/X | Exec summary angle; problem-led; not a feature list | Marketing | June 24, 08:35–08:37 |
| PM communities | LinkedIn groups, Slack, Reddit | Non-promotional angle: "how we built automated exec summaries" or use case story | Marketing | June 24 – July 1 |
| Press / analysts (if Tier 1 warrants outreach) | Email embargo briefing | "First PM analytics module with automated weekly executive PDF summaries" | Marketing Lead | June 17–20 (pre-launch embargo) |
| Integration partners | Email / partner channel | Coordinate co-announcement or joint mention | Partnerships | June 24 (coordinated) |

---

## Success Metrics

### Expansion Motion (existing customers)

| Metric | Target | Measurement method | Review date |
|---|---|---|---|
| Analytics attach rate (% of 340 Pro accounts) | 10% at T+30; 18% at T+60; 30% at Q4 close | Billing system: analytics add-on active / total Pro accounts | T+30, T+60, T+90, Q4 close |
| Trial activation rate (% of 340 who open trial dashboard) | 60% within 30 days | Product analytics: first dashboard load event | T+30 |
| Trial → paid conversion rate | 50% of activated trials | Billing: trial → paid within 30-day window | T+30 |
| Incremental expansion MRR | ~$38,250 at T+30 pace; ~$114,750 at Q4 close | Billing system: analytics add-on MRR | T+30, T+60, T+90 |
| NPS for Analytics module | > 35 | In-product NPS survey triggered at day 14 of trial | T+30, T+60 |
| Support ticket volume — Analytics (by category) | < 20/day in launch week; < 5/day steady state | Support system: tag = `analytics-module`; report by category (setup / data accuracy / PDF / billing) | T+7, T+30 |

### Acquisition Motion (new customers)

| Metric | Target | Measurement method | Review date |
|---|---|---|---|
| Net-new logos closed (Analytics-led) | 5–8 at T+30; 18–22 at T+60; 50 at Q4 close | CRM: closed-won where Analytics was primary driver | T+30, T+60, T+90, Q4 close |
| Demo requests per month | 40 | CRM + `/analytics` landing page analytics | T+30, T+60 |
| Paid search CPL (cost per demo lead) | < $150 | Ad platform + CRM first-touch attribution | T+30 |
| Landing page conversion rate (visitor → demo) | > 3% | Analytics: `/analytics` sessions vs. demo requests | T+30 |
| Analytics-influenced pipeline ($) | Define with Sales by June 5 | CRM opportunity: Analytics noted as trigger | T+30, T+60 |

### Overall

| Metric | Target | Measurement method | Review date |
|---|---|---|---|
| Total incremental MRR (expansion + acquisition) | ~$150,000/month by Q4 close | Billing system | T+90, Q4 close |
| Analytics module uptime | > 99.5% | Infrastructure monitoring | Continuous |
| PDF generation success rate | > 99% | Application logs: PDF job success/fail | Continuous |
| Dashboard load time (p95) | < 3 seconds | APM / application monitoring | Continuous |

---

## Post-Launch Review

The skill's 7-day review (Step 6) is preserved below and extended to T+30/T+60/T+90 per the launch requirements.

### T+7 Review (July 1, 2026)

**Scheduled:** July 1, 2026
**Attendees:** Product Lead, Engineering Lead, Support Lead, Marketing Lead
**Focus:** Technical health + early signals

| Metric | Baseline | Day 1 | Day 3 | Day 7 | Target | Status |
|---|---|---|---|---|---|---|
| Trial activation (% of 340) | 0% | | | | 20% by day 7 | |
| Error rate (dashboard load) | 0% | | | | < 0.5% | |
| Support ticket volume (analytics-related) | 0 | | | | < 20/day launch week | |
| PDF generation success rate | 0 (no baseline) | | | | > 99% | |
| NPS / satisfaction | n/a | | | | n/a (too early) | |

**Qualitative review:**
- Top 3 things that went well
- Top 3 things that didn't go well
- Unexpected outcomes
- User feedback themes (support tickets, social, community)
- Follow-up items: P1/P2 bugs, quick wins, doc gaps

**Decision:**
- [ ] Continue rollout to 100% if not already complete
- [ ] Iterate on any critical UX or data accuracy issues surfaced
- [ ] Rollback: triggered if error rate > 1% or data accuracy issue confirmed
- [ ] Update roadmap: note any quick-win features to prioritise for v1.1

---

### T+30 Review (July 24, 2026)

**Scheduled:** July 24, 2026
**Attendees:** Product Lead, Marketing Lead, CS Lead, Engineering Lead, Support Lead
**Focus:** Expansion conversion signal + acquisition pipeline health

| Metric | Target | Actual T+30 | Status | Action |
|---|---|---|---|---|
| Attach rate (% of 340) | 10% | | | |
| Trial activation rate | 60% | | | |
| Trial → paid conversion | 50% | | | |
| Expansion MRR | ~$38,250 | | | |
| Demo requests | 40 | | | |
| Paid search CPL | < $150 | | | |
| Landing page conversion | > 3% | | | |
| Module NPS | > 35 | | | |
| Support tickets/day (steady state) | < 5 | | | |

**Key decisions at T+30:**
- Is expansion motion converting? If trial activation < 40%, investigate in-product discovery. If trial → paid < 30%, investigate pricing or value perception.
- Is paid search viable? If CPL > $250 at T+30, reassess budget allocation vs. SEO/content.
- Are support ticket categories shifting from setup (expected) to data accuracy (problem)?

---

### T+60 Review (August 23, 2026)

**Scheduled:** August 23, 2026
**Attendees:** Product Lead, Marketing Lead, CS Lead, Sales Lead
**Focus:** Conversion quality + pipeline maturation

| Metric | Target | Actual T+60 | Status | Action |
|---|---|---|---|---|
| Attach rate | 18% | | | |
| Expansion MRR | ~$68,850 | | | |
| Net-new logos closed | 18–22 | | | |
| Module NPS (second cohort) | > 40 (improving from T+30) | | | |
| Support tickets/day | < 5 (stable) | | | |

**Key decisions at T+60:**
- Trial window has closed for T+0 activations — attach rate is now a hard number. Is 30% Q4 target realistic? Adjust forecast if < 15% at T+60.
- Are net-new logos the right profile (50+ seats, ops director buyer)? Check ICP fit.
- Is NPS improving as users become familiar? If flat or declining, investigate onboarding.
- Top 3 reasons accounts did NOT convert from trial — collect from CS and support.

---

### T+90 Review (September 22, 2026)

**Scheduled:** September 22, 2026
**Attendees:** Product Lead, Marketing Lead, CS Lead, Sales Lead, Leadership
**Focus:** Q4 forecast lock + roadmap input for Analytics v1.1

| Metric | Target | Actual T+90 | Q4 Forecast | Action |
|---|---|---|---|---|
| Attach rate | ~22–25% (pace to Q4 30%) | | | |
| Expansion MRR | ~$85,000 | | | |
| Net-new logos closed | 30–35 | | | |
| Total incremental MRR | ~$110,000 | | | |

**Key decisions at T+90:**
- Is Q4 target (30% attach, 50 net-new logos) achievable? Lock forecast; adjust if needed.
- What Q4 acceleration is needed? (Discount offer, referral program, expanded paid search)
- What are the top 3 feature requests from NPS verbatims and support tickets? → Roadmap input for v1.1.
- Any competitive response from Asana or Monday.com? Update positioning if needed.
- What did we learn about the acquisition ICP that changes our targeting?

---

> **DRAFT — requires human review**
>
> This plan must be reviewed and approved by the launch owner before any execution begins. Assign named individuals to all owner fields. Confirm all dates against the team's actual availability calendar. Verify competitive positioning claims against current Asana and Monday.com product documentation before any external publication.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.5/16.0 (97%) |
| Evaluated | 2026-05-27 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 519338 ms |
| Target cost | $0.6361 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | All marketing copy, messaging, and campaign content is labelled DRAFT and flagged for human review before use | PASS | Document opens and closes with '**DRAFT — requires human review**'. Competitive claims include 'Verify against current product documentation before any external publication.' |
| c2 | Applies positioning work before tactics — identifies the competitive alternative (Asana/Monday reporting), differentiator (executive summaries), and target segment (operations directors/PMOs at 50+ seat accounts) before writing messages | PASS | '## Competitive Positioning' section names Asana Reporting + Monday.com Dashboards, exec summary as differentiator, ops directors/PMOs as buyers — all appear before any tactical GTM motion sections. |
| c3 | Leads messaging with the customer problem (e.g. blind spots in project health, lack of exec visibility) rather than feature descriptions | PASS | '## The Problem' is the first content section with four named pains including 'Blind spots in project health' and 'Executive reporting is a weekly tax on the PMO.' Product capabilities follow in a separate section. |
| c4 | Recommends a launch tier (given 340 existing customers and $15/seat add-on, this is likely a Tier 2 or Tier 1 launch — not a silent rollout) | PASS | '## Launch Tier: 1 — Major' with explicit rationale: new module, new pricing tier, two GTM motions, 340 accounts at risk. |
| c5 | Distinguishes between the existing customer expansion play (340 accounts) and any net-new motion — these require different approaches | PASS | Two explicitly named and separated sections: '## GTM Motion 1: Existing Customer Expansion' and '## GTM Motion 2: New Customer Acquisition' with different channels, owners, and mechanics. |
| c6 | Includes a post-launch review plan with success metrics — partial credit if metrics are named but no review timeline or owner is specified | PARTIAL | T+7/T+30/T+60/T+90 reviews with dates (e.g. July 24, Aug 23, Sept 22), named attendees by role, and metric tables with targets. Ceiling is PARTIAL regardless. |
| c7 | Produces a structured launch plan with phases and owners, not a list of marketing ideas | PASS | 53-item pre-launch checklist with Owner/Due columns, 4-stage rollout strategy, timestamped launch-day run-of-show, communication plan table, and post-launch review tables all with owners. |
| c8 | Output sizes the existing-customer revenue opportunity — 340 accounts × 50+ seats × $15/seat/month — yielding the upper-bound ARR (~$3M+) and a realistic conversion target (e.g. "30% adoption in year 1 → ~$900K ARR uplift") | PASS | Assumptions section: '340 accounts × 75 avg seats × $15 = $382,500 fully attached; 30% attach = ~$114,750/month incremental expansion MRR.' Math is explicit; MRR rather than ARR labeling is the only gap. |
| c9 | Output's positioning anchors against Asana / Monday native reporting as the competitive alternatives, with the executive summary as the named differentiator — not a generic feature list | PASS | Comparison table rows include 'Automated weekly PDF summary' showing Clearpath=Yes, Asana='No — reports are UI-only', Monday.com='No — dashboards are web-only.' Positioning statement calls out 'automatically delivers a formatted executive summary to your inbox every week.' |
| c10 | Output's customer-problem framing leads with the operations director / PMO pain — e.g. "execs ask 'how are projects tracking?' and you spend half a day pulling a manual report" — not "we have a new analytics module" | PASS | 'Operations directors and PMOs at mid-market companies are making project decisions with delayed, incomplete information.' Point 4: 'PMOs spend 3–5 hours every Friday manually assembling a status report.' |
| c11 | Output classifies this as Tier 1 or Tier 2 launch given 340 existing customers, $15/seat ARR uplift, and a 3-year-customer-base activation event — explicitly NOT a silent rollout | PASS | '## Launch Tier: 1 — Major' with rationale citing new product surface area, first paid add-on, two GTM motions, and 340 existing accounts at stake. |
| c12 | Output separates the existing-customer expansion motion (CSM-led, in-product upsell, QBR conversations) from any net-new acquisition motion — different channels, different messaging, different sales process | PASS | Motion 1: in-product banner, CSM outreach, exec sponsor email, near-zero acquisition cost. Motion 2: paid search ($8-12k/month), SEO content, comparison pages, demo-led sales, CRM prospect email. |
| c13 | Output's launch plan has phases with owners and dates — Pre-launch (weeks -4 to 0): readiness checklist, sales enablement, beta close-out; Launch week: announcements, in-product, customer comms; Post-launch (weeks 1-12): adoption tracking, expansion plays, feedback loops | PASS | 4-stage rollout (June 10→17→21→24), 53-item pre-launch checklist with due dates June 3–19, timestamped launch day run-of-show, T+7/T+30/T+60/T+90 post-launch phases. |
| c14 | Output's marketing copy and messaging examples are labelled DRAFT — explicitly flagged for human review before publication | PASS | Document opens and closes with '**DRAFT — requires human review**'. Final note: 'This plan must be reviewed and approved by the launch owner before any execution begins.' |
| c15 | Output's post-launch review plan names success metrics (e.g. trial signups, paid conversions, % of 340-base activated, $ ARR uplift), a review date (e.g. "Day 30, Day 60, Day 90 reviews"), and a review owner | PASS | T+30 (July 24): attendees listed, attach rate 10%, trial activation 60%, MRR ~$38,250 targets. T+60 (Aug 23), T+90 (Sept 22) similarly structured with named attendees and metric tables. |
| c16 | Output addresses internal readiness alongside external launch — sales enablement (battle cards, demo scripts), CSM enablement (expansion playbooks), support training, docs ready before announce | PASS | Pre-launch checklist items 48-50: account team playbook, priority account list, CSM training. Items 18-23: Support Readiness. Items 13-17: Documentation. Communication plan includes CS/Support live briefings on June 17. |
| c17 | Output addresses pricing communication carefully — $15/seat add-on for existing customers may need grandfathering for early adopters or volume discounting at the 340 mid-market scale | FAIL | No discussion of grandfathering, volume discounting, loyalty pricing, or pricing sensitivity for the existing 340-account base. $15/seat is stated flatly with no communication nuance. |

### Notes

The output is a comprehensive, well-structured GTM plan that satisfies nearly every criterion — problem-led messaging, explicit tier classification, two named and separated motions, phases with owners/dates, DRAFT labeling, and detailed T+30/T+60/T+90 reviews. The only gap is c17: pricing communication for existing customers (grandfathering, volume discounting) is entirely absent despite the 340-account base representing a meaningful loyalty pricing consideration.
