# Test: due-diligence skill

Scenario: A SaaS company is evaluating a commercial partnership with Culture Amp, the AU-based employee experience platform.

## Prompt

/analyst:due-diligence Culture Amp Pty Ltd for commercial partnership — we're considering integrating their employee engagement surveys into our HR platform

Output structure (use these section names in this order):

1. **Scope** (top of document) — explicit one-paragraph: "Commercial partnership due diligence on Culture Amp Pty Ltd. Public data only. NOT a substitute for legal, financial, or technical due diligence — those require separate workstreams. Findings are time-stamped."
2. **Business fundamentals** — every revenue/funding figure carries source + date inline (e.g. "$200M ARR — Forbes, 2024-08-12"). No bare figures.
3. **Product signals** — review score TREND over time (e.g. G2 score 4.5→4.3 over 18 months), not just current score. List multiple data points.
4. **Customer / market signals** — named customers (with public proof), employee count trend, geographic footprint.
5. **Risk signals** — funding runway, leadership changes, competitive pressure, regulatory exposure.
6. **Signal Summary table** (BEFORE verdict) with columns: `Signal | Direction (positive/neutral/negative) | Confidence (HIGH/MED/LOW) | Source`.
7. **Verdict** (follows from the table, doesn't precede it).
8. **Sources** — numbered, each with URL + access date.

A few specifics for the response:

- The skill writes a conforming report to a file path it computes (`<pwd>/due-diligence/<company-slug>.md` by default). Capture and report that file path. Section structure follows the template at `${CLAUDE_PLUGIN_ROOT}/templates/due-diligence.md`. Every mandatory section in the template MUST appear in the written file, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
- Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
- For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
- When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
- Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Criteria

- [ ] PASS: Skill writes a file to disk at `<pwd>/due-diligence/<company-slug>.md` (see ARTIFACTS WRITTEN — at least one .md file under `due-diligence/` exists)
- [ ] PASS: The written file opens with YAML frontmatter (title, date, author=due-diligence, category=Commercial, subject, scope) per report-conventions
- [ ] PASS: Chat response ends with a single line giving the absolute path to the written report
- [ ] PASS: Skill states the scope explicitly at the top — commercial partnership scope, public data only
- [ ] PASS: Business fundamentals section includes a source and date for every revenue or funding figure — no unsourced numbers
- [ ] PASS: Product signals section covers review score trend over time, not just the current score
- [ ] PASS: Team section notes current key executive tenures and any notable recent departures
- [ ] PASS: Signal summary table is present and precedes the verdict — verdict follows from the signals, not the other way around
- [ ] PASS: Output clearly states this is public-data diligence only and that legal, financial, and technical diligence requires direct access
- [ ] PARTIAL: When two or more red signals are present, skill routes to appropriate follow-on skills (public-records, corporate-ownership, entity-footprint) rather than stopping at the verdict
- [ ] PASS: Revenue and valuation are not conflated — if estimates for private company appear, they are explicitly labelled as estimates

## Output expectations

- [ ] PASS: Output addresses Culture Amp specifically — AU-headquartered employee experience platform founded 2009 by Didier Elzinga, Jon Williams, Doug English, Rod Hamilton — with key entity confirmation (ABN, registered office) at the top
- [ ] PASS: Output's scope statement explicitly limits to commercial-partnership diligence using public data only — naming what's NOT covered (legal contract review, financial audit, technical security assessment) and routing those to appropriate diligence types
- [ ] PASS: Output's business fundamentals section sources every revenue / funding figure — e.g. "Series F $100M raised 2021 (Crunchbase, source URL); ARR ~$80M FY22 (AFR profile, March 2022)" — never unsourced
- [ ] PASS: Output's product signals trace review-score TREND over time — not just current G2 / Capterra average; comparing FY22 vs FY24 reveals trajectory (improving / stable / declining)
- [ ] PASS: Output's team section names current key executives (CEO, CRO, CTO, CFO) with tenure, plus any notable departures in last 12 months — leadership churn is a partnership-risk signal
- [ ] PASS: Output's signal summary table precedes the verdict — revenue trajectory (green / amber / red), customer base (green), product reviews (green / amber / red), funding runway (green if recent raise / amber if old), leadership stability (green if stable / amber if recent change), legal disputes (green if none public / red if material)
- [ ] PASS: Output's verdict (PROCEED / PROCEED WITH CONDITIONS / DECLINE / NEEDS DEEPER DILIGENCE) follows from the signal table — not asserted independently then justified retroactively
- [ ] PASS: Output explicitly states this is public-data-only diligence — and that the partnership decision requires legal review of the partnership terms, financial diligence (ideally audited financials shared under NDA), and technical / security review
- [ ] PASS: Output distinguishes revenue (ARR, recurring revenue actually flowing in) from valuation (last round implied valuation, secondary market estimate) — never collapsing these
- [ ] PARTIAL: Output addresses cross-AU SaaS partnership specifics — both companies are AU-based so currency / tax / data-residency concerns are simpler than cross-border, but customer-data-sharing under SOCI Act and Privacy Act 1988 still applies
