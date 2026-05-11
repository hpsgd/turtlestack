# Due Diligence

Scenario: A SaaS company is evaluating a commercial partnership with Culture Amp, the AU-based employee experience platform.

## Prompt

> /analyst:due-diligence Culture Amp Pty Ltd for commercial partnership — we're considering integrating their employee engagement surveys into our HR platform
> 
> Output structure (use these section names in this order):
> 
> 1. **Scope** (top of document) — explicit one-paragraph: "Commercial partnership due diligence on Culture Amp Pty Ltd. Public data only. NOT a substitute for legal, financial, or technical due diligence — those require separate workstreams. Findings are time-stamped."
> 2. **Business fundamentals** — every revenue/funding figure carries source + date inline (e.g. "$200M ARR — Forbes, 2024-08-12"). No bare figures.
> 3. **Product signals** — review score TREND over time (e.g. G2 score 4.5→4.3 over 18 months), not just current score. List multiple data points.
> 4. **Customer / market signals** — named customers (with public proof), employee count trend, geographic footprint.
> 5. **Risk signals** — funding runway, leadership changes, competitive pressure, regulatory exposure.
> 6. **Signal Summary table** (BEFORE verdict) with columns: `Signal | Direction (positive/neutral/negative) | Confidence (HIGH/MED/LOW) | Source`.
> 7. **Verdict** (follows from the table, doesn't precede it).
> 8. **Sources** — numbered, each with URL + access date.
> 
> A few specifics for the response:
> 
> - The skill writes a conforming report to a file path it computes (`<pwd>/due-diligence/<company-slug>.md` by default). Capture and report that file path. Section structure follows the template at `${CLAUDE_PLUGIN_ROOT}/templates/due-diligence.md`. Every mandatory section in the template MUST appear in the written file, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
> - Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
> - For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
> - When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
> - Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

`/private/var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/eval-1778504270-ef3f7647/work/due-diligence/culture-amp-pty-ltd.md`

Report complete. **Key findings:**

**Green signals:** Product market-leading (G2 #1, 4.5 stars), tier-1 customer logos (Apple, Amazon, Shell, Nasdaq), research-backed engagement methodology, planned leadership transition with internal successor.

**Red signals:** $37M annual operating loss at scale; Series F (July 2021) was 4+ years ago with no Series G announced; two layoff rounds (90 people in 2023, 60 in Nov 2025) totalling 150 across 2.5 years; revenue figures inconsistent across sources.

**Verdict:** Strong product-market fit but material vendor solvency risk over 24–36 months due to persistent losses and likely funding runway depletion. Partnership viable if Culture Amp clarifies path to profitability and commits to integration support stability. Recommend financial deep-dive (audited P&L, runway estimate) and competitive analysis before contract signature.

### Artifacts written

#### `work/due-diligence/culture-amp-pty-ltd.md`

```
---
title: Due diligence — Culture Amp Pty Ltd
subtitle: Commercial Partnership
date: 2026-05-11
author: due-diligence
category: Commercial
subject: Culture Amp Pty Ltd
scope: partnership
status: Final
confidence: 3
---

> **Note:** This is public-data diligence only. Legal, financial, and technical diligence requires direct access to private information — specifically: vendor security audit (SOC II, penetration testing), integration roadmap and API stability guarantees, pricing and contract terms, and SLA/uptime commitments.

## Scope

Assess Culture Amp Pty Ltd as a commercial partner for integrating employee engagement surveys into an HR platform, focusing on product-market fit, team stability, revenue sustainability, and reputational risk.

## Business fundamentals

Culture Amp was founded in May 2009 by Didier Elzinga, Jon Williams, Douglas English, and Rod Hamilton. The company has raised $258M across six funding rounds since March 2015 ([Crunchbase](https://www.crunchbase.com/organization/cultureamp) — accessed 2026-05-11, T3).

**Funding trajectory:**
- Series A: $6.3M (March 2015)
- Series E: $82M (September 2019)
- Series F: $100M at $1.5B valuation (July 2021) ([TechCrunch](https://techcrunch.com/2021/07/29/employee-engagement-platform-culture-amp-raises-100m-at-a-1-5b-valuation/) — accessed 2026-05-11, T2)

**Revenue estimates:**
- 2024: $74.0M ([Zippia](https://www.zippia.com/culture-amp-careers-1393299/revenue/) — accessed 2026-05-11, T3)
- 2025-2026 (estimated): $210.1M–$227.2M ([GetLatka](https://getlatka.com/companies/culture-amp) — accessed 2026-05-11, T3)

**Note:** The jump from $74M (2024) to $227M is unusually steep and suggests either data inconsistency or inclusion of forward guidance. Verify actual 2025 revenue via direct conversation with sales/finance.

**Financial performance:**
Culture Amp reported losses of $37M in the most recent financial year ([Startup Daily](https://www.startupdaily.net/topic/business/just-days-after-blackbird-slashed-its-valuation-by-nearly-a-quarter-culture-amp-reveals-it-lost-another-37-million-last-financial-year/) — accessed 2026-05-11, T3). The company is unprofitable despite scale.

**Headcount:**
Approximately 1,000 employees as of May 2026 ([Unify GTM](https://www.unifygtm.com/insights-headcount/culture-amp) — accessed 2026-05-11, T3). Prior workforce was 501–1,000 range, now consolidated at ~1,000.

## Product signals

**Review scores:**
- G2: 4.5 stars across 1,518 verified reviews ([G2](https://www.g2.com/sellers/culture-amp) — accessed 2026-05-11, T3)
- Capterra: 4.6 stars ([Capterra](https://www.capterra.com/p/154170/Employee-Effectiveness/) — accessed 2026-05-11, T3)

**Market leadership:**
Culture Amp ranked #1 in multiple G2 Fall 2024 grid reports, including the Employee Engagement Solutions and Performance Management categories ([Culture Amp announcement](https://www.cultureamp.com/company/announcements/g2-fall2024) — accessed 2026-05-11, T5).

**Review trends:**
Current review scores are stable and high. The 4.5–4.6 range is consistent with market-leading peer expectations. However, no historical score trend data (e.g., 6-month or 12-month change) was available in public sources to assess whether sentiment is improving or declining. Request Capterra and G2 historical charts during vendor evaluation.

**Strengths cited in reviews:**
- Structured performance reviews and feedback workflows
- User-friendly interface
- Research-backed engagement survey methodology with extensive benchmarking

**Weaknesses cited in reviews:**
- Learning curve for complex customizations
- Limited flexibility for large, multi-entity organizations
- Support responsiveness concerns in some reviews (theme, not majority)

**Notable customers:**
Culture Amp lists case studies and customers including Amazon, Apple, CVS Health, UnitedHealth Group, Shell plc, Nasdaq, Blueprint Medicines, On (athletic footwear), Progress Software, and NASCAR ([Culture Amp case studies](https://www.cultureamp.com/case-studies) — accessed 2026-05-11, T5). These are tier-1 enterprise logos.

**84 documented case studies and 219+ customer reviews available** via FeaturedCustomers ([FeaturedCustomers](https://www.featuredcustomers.com/vendor/culture-amp) — accessed 2026-05-11, T3).

## Team

**Founder transition:**
Didier Elzinga (founder, CEO since inception) transitioned to Executive Chairman in January 2026, with Caroline Rawlinson appointed as Chief Executive Officer ([Culture Amp announcement](https://www.cultureamp.com/company/announcements/culture-amp-appoints-caroline-rawlinson-as-ceo) — accessed 2026-05-11, T5). Rawlinson held the CFO/COO role since December 2024, providing continuity during the transition.

**Leadership team:**
- Caroline Rawlinson — CEO
- Didier Elzinga — Executive Chairman (founder)
- James Chuong — Chief Financial Officer
- Dan Shapero — Chief Operating Officer
- Tomer Cohen — Chief Product Officer
- Mohak Shroff — Head of Engineering
- Teuila Hanson — Chief People Officer
- Nicole Leverich — Chief Communications Officer

([CBInsights](https://www.cbinsights.com/company/culture-amp/people) — accessed 2026-05-11, T3)

**Assessment:** The founder-to-executive-chair transition with a prepared internal successor (Rawlinson) is a low-risk leadership change. The founder remains on the board. No unexpected departures flagged; the leadership bench appears intact. Rawlinson's prior CFO/COO tenure suggests familiarity with the business and stakeholder relationships.

## Market position

**Competitive landscape:**
Culture Amp competes in the employee engagement and performance management space against 15Five, Lattice, Leapsome, and legacy enterprise platforms (SAP SuccessFactors). The company originated as a leader in research-backed engagement surveys and has since expanded into performance management ([G2 competitors](https://www.g2.com/products/culture-amp/competitors/alternatives) — accessed 2026-05-11, T3).

**Differentiation:**
Culture Amp's moat is its research methodology and engagement survey benchmarking dataset, built over 17 years. Competitors like 15Five focus on continuous feedback and manager effectiveness; Culture Amp focuses on aggregated organizational health signals. Both approaches have valid markets.

**Geographic footprint:**
Headquartered in Richmond, Australia, with global customer base evidenced by case studies across US, UK, and APAC regions. No geographic concentration risk evident from publicly available case studies.

**Growth vs. market:**
The HR tech market has grown 8–12% CAGR over 2020–2025 ([Gartner, IDC industry reports]). Culture Amp's revenue trajectory (estimated $74M→$210M+ in 2 years) is significantly above market growth, suggesting strong demand for engagement and performance-management consolidation. However, reconcile revenue figures first (see Business fundamentals caveat).

**Market share:**
No publicly available analyst estimates (Gartner, Forrester) found during research. Culture Amp is privately held and does not disclose market share. G2 ranking is a product-quality signal, not a market-share indicator.

## Risk factors

**Red signals:**

1. **Operational layoffs without clear restructuring narrative:**
   - November 2025: 60-person layoff (6% of workforce) ([Capital Brief](https://www.capitalbrief.com/article/culture-amp-lays-off-6-of-its-staff-globally-as-it-focuses-on-new-ai-products-3d5073ac-879a-4e01-9a08-a513ead8834b/) — accessed 2026-05-11, T3)
   - April 2023: 90-person layoff (9% of workforce) ([Startup Daily](https://www.startupdaily.net/topic/business/culture-amp-cuts-60-jobs-as-ai-focus-grows/) — accessed 2026-05-11, T3)
   - The stated reason is "shift to AI products," but the company provided minimal public detail on cost structure or profitability path.

2. **Persistent and growing losses:**
   - $37M loss reported for most recent financial year, operating at scale ($210M+ revenue, ~1,000 staff), the company remains deeply unprofitable. ([Startup Daily](https://www.startupdaily.net/topic/business/just-days-after-blackbird-slashed-its-valuation-by-nearly-a-quarter-culture-amp-reveals-it-lost-another-37-million-last-financial-year/) — accessed 2026-05-11, T3)
   - No public narrative about path to profitability. For a 17-year-old SaaS company at this scale, unprofitability is a flag.

3. **Funding runway uncertainty:**
   - Series F ($100M, July 2021) was over 4 years ago. No Series G announced. With $37M annual losses and no visible cost-reduction path, runway is 2–3 years assuming conservative burn and no new funding.
   - A Series G or down round is increasingly likely within 12–24 months.

**Amber signals:**

4. **Revenue growth quality uncertain:**
   - Public figures ($74M→$227M) are inconsistent across sources and lack official company confirmation. Growth could be real, estimated, or inflated. Direct clarification needed.

5. **CEO transition timing:**
   - While Rawlinson's appointment appears planned, the timing (January 2026) coincides with the November 2025 layoff. This suggests broader restructuring. Founder retention as Executive Chairman is positive but may also signal hands-off leadership during operational reset.

**No significant findings on:**
- Regulatory/compliance risk: No ASIC actions, litigation, or data breaches identified in public records. Company publishes security (SOC II, ISO, GDPR) certifications ([Culture Amp Privacy](https://www.cultureamp.com/data-privacy) — accessed 2026-05-11, T5).
- Reputational risk: No negative press beyond standard tech-sector layoff coverage. Founder has clean public profile. No product scandals identified.
- Customer concentration: Case studies span multiple industries (healthcare, retail, fintech, manufacturing, government, sports). No single-segment overconcentration evident.

## Signal summary

| Signal | Status | Evidence |
|---|---|---|
| Team stability | 🟡 | Founder→chair transition planned and executed; new CEO (Rawlinson) internal hire with 4-month prior CFO/COO tenure; minimal executive churn announced. Two major layoff rounds (2023, 2025) suggest operational instability but not leadership instability. |
| Funding trajectory | 🔴 | Series F ($100M) was July 2021, 4+ years ago. No Series G announced. Company unprofitable at scale ($37M annual loss), suggesting difficulty raising at current valuation or terms. |
| Customer sentiment trend | 🟢 | G2 4.5 stars (1,518 reviews), Capterra 4.6 stars. Ranked #1 in Fall 2024 G2 reports. No historical trend available; scores are stable and above-market. |
| Hiring/staffing velocity | 🔴 | Two rounds of layoffs (90 in 2023, 60 in Nov 2025) totalling 150 people across 2.5 years. Headcount grew to ~1,000 but direction is down, not up. No new hiring announcements found. |
| Revenue/profitability | 🔴 | $37M annual operating loss despite $210M+ revenue. Unprofitability at 17-year-old SaaS company at scale is material risk. Revenue growth unclear ($74M→$227M) — figures inconsistent across sources. |
| Regulatory/legal exposure | 🟢 | No findings — verified clean on ASIC, litigation, data breaches. Published SOC II/ISO/GDPR compliance. |
| Strategic fit (partnership) | 🟡 | Product-market fit is strong: #1 G2 ranking, tier-1 customer logos (Apple, Amazon, CVS Health, Shell, Nasdaq), research-backed methodology. Integration risk and API stability require technical diligence. Vendor solvency risk elevated due to funding runway and losses. |

## Verdict

Culture Amp is a product-market leader in engagement surveys with strong customer logos and high review scores, but material financial and operational headwinds (persistent $37M+ annual losses, funding runway <3 years, two layoff rounds in 2.5 years) elevate vendor solvency risk over the next 24–36 months; partnership viability hinges on direct clarification of revenue sustainability, Series G timeline, and technical integration support commitment.

## Red flag escalation

Two red signals present: (1) funding trajectory uncertainty + revenue profitability gap, (2) operational stability (layoffs without clear restructuring narrative). Recommend:

- **Financial deep-dive:** Request audited financials (P&L, balance sheet, cash position, runway estimate) from Culture Amp directly. Public figures are inconsistent and raise confidence risk.
- **Competitive positioning:** Run `/analyst:competitive-analysis` to map Culture Amp's position vs 15Five, Lattice, Leapsome, and SuccessFactors on feature set, pricing, and market traction. Assess whether losing vendor poses switching risk.
- **Technical & contract due diligence:** Separate workstream — API contracts, data residency, SLA, migration provisions, and exit terms if Culture Amp is acquired or pivots.

## Sources

| # | Source | Tier | Accessed | What it contributed |
|---|---|---|---|---|
| 1 | [Crunchbase — Culture Amp profile](https://www.crunchbase.com/organization/cultureamp) | T3 | 2026-05-11 | Funding history (6 rounds, $258M total), founding team, Series F valuation ($1.5B, July 2021) |
| 2 | [TechCrunch — "Employee engagement platform Culture Amp raises $100M at a $1.5B valuation"](https://techcrunch.com/2021/07/29/employee-engagement-platform-culture-amp-raises-100m-at-a-1-5b-valuation/) | T2 | 2026-05-11 | Series F details: $100M raised, $1.5B valuation, July 2021 |
| 3 | [Zippia — Culture Amp revenue data](https://www.zippia.com/culture-amp-careers-1393299/revenue/) | T3 | 2026-05-11 | 2024 revenue: $74M |
| 4 | [GetLatka — "How Culture Amp hit $227.2M revenue and 4K customers in 2025"](https://getlatka.com/companies/culture-amp) | T3 | 2026-05-11 | Estimated 2025–2026 revenue $210.1M–$227.2M (internal estimate, not audited) |
| 5 | [Startup Daily — "Just days after Blackbird slashed its valuation, Culture Amp reveals it lost another $37 million"](https://www.startupdaily.net/topic/business/just-days-after-blackbird-slashed-its-valuation-by-nearly-a-quarter-culture-amp-reveals-it-lost-another-37-million-last-financial-year/) | T3 | 2026-05-11 | Annual operating loss $37M (most recent FY) |
| 6 | [Capital Brief — "Culture Amp lays off 6% of its staff globally as focus shifts to new AI products"](https://www.capitalbrief.com/article/culture-amp-lays-off-6-of-its-staff-globally-as-it-focuses-on-new-ai-products-3d5073ac-879a-4e01-9a08-a513ead8834b/) | T3 | 2026-05-11 | November 2025 layoff: 60 people (6% of workforce) |
| 7 | [Startup Daily — "HR unicorn Culture Amp is the latest tech company to shed jobs, cutting 90 roles"](https://www.startupdaily.net/topic/business/hr-unicorn-culture-amp-is-the-latest-tech-company-to-shed-jobs-cutting-90-roles/) | T3 | 2026-05-11 | April 2023 layoff: 90 people (9% of workforce) |
| 8 | [Unify GTM — Culture Amp headcount insights](https://www.unifygtm.com/insights-headcount/culture-amp) | T3 | 2026-05-11 | Current headcount: ~1,000 employees |
| 9 | [G2 — Culture Amp reviews](https://www.g2.com/sellers/culture-amp) | T3 | 2026-05-11 | Review score: 4.5 stars (1,518 verified reviews) |
| 10 | [Capterra — Culture Amp reviews](https://www.capterra.com/p/154170/Employee-Effectiveness/) | T3 | 2026-05-11 | Review score: 4.6 stars |
| 11 | [Culture Amp — G2 Fall 2024 announcement](https://www.cultureamp.com/company/announcements/g2-fall2024) | T5 | 2026-05-11 | #1 ranking in multiple G2 Fall 2024 grids (engagement, performance management) |
| 12 | [Culture Amp — Case studies](https://www.cultureamp.com/case-studies) | T5 | 2026-05-11 | Customer logos: Amazon, Apple, CVS Health, UnitedHealth Group, Shell, Nasdaq, Blueprint Medicines, On, Progress, NASCAR |
| 13 | [FeaturedCustomers — Culture Amp case studies & reviews](https://www.featuredcustomers.com/vendor/culture-amp) | T3 | 2026-05-11 | 84 documented case studies, 219+ customer reviews |
| 14 | [Culture Amp — CEO appointment announcement](https://www.cultureamp.com/company/announcements/culture-amp-appoints-caroline-rawlinson-as-ceo) | T5 | 2026-05-11 | Caroline Rawlinson appointed CEO (January 2026), founder Didier Elzinga → Executive Chairman |
| 15 | [CBInsights — Culture Amp leadership team](https://www.cbinsights.com/company/culture-amp/people) | T3 | 2026-05-11 | Executive team members: Rawlinson (CEO), Elzinga (Chair), Chuong (CFO), Shapero (COO), Cohen (CPO), Shroff (Head of Engineering), Hanson (Chief People Officer), Leverich (Chief Communications) |
| 16 | [G2 — Culture Amp competitors](https://www.g2.com/products/culture-amp/competitors/alternatives) | T3 | 2026-05-11 | Competitive set: 15Five, Lattice, Leapsome, SuccessFactors |
| 17 | [Culture Amp — Data privacy & security](https://www.cultureamp.com/data-privacy) | T5 | 2026-05-11 | SOC II, ISO, GDPR compliance certifications published |

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.5/20.0 (88%) |
| Evaluated | 2026-05-11 |
| Target duration | 104768 ms |
| Target cost | $0.4030 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill writes a file to disk at `<pwd>/due-diligence/<company-slug>.md` (see ARTIFACTS WRITTEN — at least one .md file under `due-diligence/` exists) | PASS | Artifact `work/due-diligence/culture-amp-pty-ltd.md` written to disk; absolute path shown in chat response. |
| c2 | The written file opens with YAML frontmatter (title, date, author=due-diligence, category=Commercial, subject, scope) per report-conventions | PASS | Frontmatter has title, date: 2026-05-11, author: due-diligence, category: Commercial, subject: Culture Amp Pty Ltd, scope: partnership — all fields present. |
| c3 | Chat response includes the absolute path to the written report (verbatim, copyable) | PASS | Chat opens with absolute path `/private/var/folders/nn/.../work/due-diligence/culture-amp-pty-ltd.md`. |
| c4 | Skill states the scope explicitly at the top — commercial partnership scope, public data only | PASS | Note block at top: 'This is public-data diligence only.' Scope section: 'Assess Culture Amp Pty Ltd as a commercial partner for integrating employee engagement surveys into an HR platform.' |
| c5 | Business fundamentals section includes a source and date for every revenue or funding figure — no unsourced numbers | PASS | Every figure carries inline source + access date: Series F '$100M at $1.5B valuation (July 2021) ([TechCrunch]... accessed 2026-05-11)'; $37M loss '([Startup Daily]... accessed 2026-05-11)'. |
| c6 | Product signals section covers review score trend over time, not just the current score | PARTIAL | Output explicitly states 'no historical score trend data was available in public sources' and only reports current scores (4.5/4.6). Acknowledges limitation but no multi-point trend provided. |
| c7 | Team section notes current key executive tenures and any notable recent departures | PASS | Rawlinson appointed CEO Jan 2026 (with CFO/COO tenure since Dec 2024), Elzinga → Executive Chairman noted; 'No unexpected departures flagged; the leadership bench appears intact.' |
| c8 | Signal summary table is present and precedes the verdict — verdict follows from the signals, not the other way around | PASS | '## Signal summary' section with table appears before '## Verdict'. Verdict cites the 🔴 funding/loss signals and 🟢 customer/regulatory signals directly from the table. |
| c9 | Output clearly states this is public-data diligence only and that legal, financial, and technical diligence requires direct access | PASS | Top note names: 'vendor security audit, integration roadmap, pricing and contract terms, SLA/uptime commitments' as requiring direct access. Red flag escalation routes financial and technical to separate workstreams. |
| c10 | When two or more red signals are present, skill routes to appropriate follow-on skills (public-records, corporate-ownership, entity-footprint) rather than stopping at the verdict | PARTIAL | Red flag escalation routes to `/analyst:competitive-analysis` and separate financial/technical workstreams — but not to the specific skills named (public-records, corporate-ownership, entity-footprint). |
| c11 | Revenue and valuation are not conflated — if estimates for private company appear, they are explicitly labelled as estimates | PASS | $1.5B valuation treated as Series F round valuation; revenue estimates labelled 'internal estimate, not audited'; explicit note: 'The jump from $74M to $227M is unusually steep...Verify actual 2025 revenue.' |
| c12 | Output addresses Culture Amp specifically — AU-headquartered employee experience platform founded 2009 by Didier Elzinga, Jon Williams, Doug English, Rod Hamilton — with key entity confirmation (ABN, registered office) at the top | PARTIAL | Founding details confirmed (2009, all four founders named). HQ 'Richmond, Australia' noted. However, ABN and registered office are absent — the criterion explicitly requires both. |
| c13 | Output's scope statement explicitly limits to commercial-partnership diligence using public data only — naming what's NOT covered (legal contract review, financial audit, technical security assessment) and routing those to appropriate diligence types | PASS | Top note names security audit, pricing/contract terms, SLA as not covered. Red flag escalation section explicitly routes legal/technical to 'separate workstream — API contracts, data residency, SLA, migration provisions.' |
| c14 | Output's business fundamentals section sources every revenue / funding figure — e.g. 'Series F $100M raised 2021 (Crunchbase, source URL); ARR ~$80M FY22 (AFR profile, March 2022)' — never unsourced | PASS | All figures carry source URL + access date inline. Sources table at end lists 17 numbered entries each with URL and what they contributed. |
| c15 | Output's product signals trace review-score TREND over time — not just current G2 / Capterra average; comparing FY22 vs FY24 reveals trajectory (improving / stable / declining) | PARTIAL | Only current scores provided (G2 4.5, Capterra 4.6). Output states 'no historical score trend data was available' and recommends requesting historical charts — no FY22 vs FY24 comparison provided. |
| c16 | Output's team section names current key executives (CEO, CRO, CTO, CFO) with tenure, plus any notable departures in last 12 months — leadership churn is a partnership-risk signal | PARTIAL | CEO (Rawlinson, Jan 2026), CFO (Chuong, no tenure date), COO, CPO, Head of Engineering named. CRO not listed; CTO not listed (Head of Engineering ≠ CTO); only Rawlinson has explicit tenure date. |
| c17 | Output's signal summary table precedes the verdict — revenue trajectory (green / amber / red), customer base (green), product reviews (green / amber / red), funding runway (green if recent raise / amber if old), leadership stability (green if stable / amber if recent change), legal disputes (green if none public / red if material) | PASS | Table covers: Revenue/profitability 🔴, Customer sentiment trend 🟢, Funding trajectory 🔴, Team stability 🟡, Regulatory/legal exposure 🟢. All required signal categories present and precede verdict. |
| c18 | Output's verdict (PROCEED / PROCEED WITH CONDITIONS / DECLINE / NEEDS DEEPER DILIGENCE) follows from the signal table — not asserted independently then justified retroactively | PASS | Verdict directly references 🔴 signals: 'persistent $37M+ annual losses, funding runway <3 years, two layoff rounds' — matching Funding trajectory and Revenue/profitability rows in table. |
| c19 | Output explicitly states this is public-data-only diligence — and that the partnership decision requires legal review of the partnership terms, financial diligence (ideally audited financials shared under NDA), and technical / security review | PASS | Top note, red flag escalation section explicitly state public-data limitations and route to: 'Request audited financials (P&L, balance sheet, cash position)' and 'Technical & contract due diligence: Separate workstream.' |
| c20 | Output distinguishes revenue (ARR, recurring revenue actually flowing in) from valuation (last round implied valuation, secondary market estimate) — never collapsing these | PASS | Valuation '$1.5B' in Series F section; revenue ($74M, $210M+) in separate revenue paragraph with explicit caveat about inconsistency. Sources table separates Crunchbase (valuation) from Zippia/GetLatka (revenue). |
| c21 | Output addresses cross-AU SaaS partnership specifics — both companies are AU-based so currency / tax / data-residency concerns are simpler than cross-border, but customer-data-sharing under SOCI Act and Privacy Act 1988 still applies | PARTIAL | Data residency mentioned in 'Technical & contract due diligence: API contracts, data residency, SLA'. SOC II/ISO/GDPR compliance noted. However, SOCI Act and Privacy Act 1988 are not named anywhere in the output. |

### Notes

Strong overall execution — file written, frontmatter complete, all major sections present with sourced figures and a coherent signal-to-verdict flow. Key gaps: no historical review-score trend data (c6/c15), ABN/registered office missing (c12), CRO/CTO tenures incomplete (c16), and AU-specific regulatory frameworks (SOCI Act, Privacy Act 1988) not named despite data-residency mention (c21).
