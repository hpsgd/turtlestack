# Test: competitive-analysis skill

Scenario: A product team wants a competitive analysis of Australian HR software vendors to inform their positioning before a funding pitch.

## Prompt

/analyst:competitive-analysis Australian HR software for SMBs — specifically payroll and leave management. We're targeting businesses with 10-200 employees in AU.

A few specifics for the response:

- **Three-way classification**: Direct (HR + payroll specialists for AU SMB — Employment Hero, KeyPay, foundU, Microkeeper, etc.), Indirect (broader accounting suites with payroll modules — Xero, MYOB, QuickBooks), Substitute (manual processes — spreadsheets + accountant, outsourced bookkeeping). Three distinct categories — do NOT collapse Substitute into Indirect.
- **Source staleness flag**: any source older than 18 months (relative to the analysis date) MUST carry a `[STALE — N months old, may be outdated]` annotation inline at every citation. Competitive landscape moves fast in AU SaaS.
- **AU-specific source coverage**: include all five source types — IBISWorld AU, Seek job postings (hiring signal), G2/Capterra AU reviews, AFR coverage, SmartCompany. List each in the source list.
- **Comparison matrix columns**: Competitor | AU compliance coverage (STP Phase 2, SuperStream, Award interpretation) | Pricing tier ($/employee/month) | Feature breadth (payroll-only / payroll+leave / full HRIS) | Strengths | Weaknesses | SMB segment fit (10-50 / 50-200). Include each column explicitly.
- **White-space synthesis (mandatory final section)**: name the specific segment + feature + pricing combination that's currently underserved, framed as the funding-pitch positioning angle ("the gap is X for Y customers at Z price point because incumbents are moving in the opposite direction").

## Criteria

- [ ] PASS: Skill writes a file to disk at `<pwd>/competitive-analysis/<market-slug>.md` (see ARTIFACTS WRITTEN — at least one .md file under `competitive-analysis/` exists)
- [ ] PASS: The written file opens with YAML frontmatter (title, date, author=competitive-analysis, category=Commercial, subject) per report-conventions
- [ ] PASS: Chat response includes the absolute path to the written report (verbatim, copyable)
- [ ] PASS: Skill defines the market before listing competitors — states buyer type (SMB), purchase unit, geography (AU), and any timing assumptions
- [ ] PASS: Competitors are classified into direct, indirect, and substitute categories
- [ ] PASS: Skill uses AU-specific sources (IBISWorld AU, Seek job postings, G2 AU category) alongside global sources — not US-only competitive intelligence
- [ ] PASS: Comparison matrix is present with positioning, pricing tier, strengths, and weaknesses per competitor
- [ ] PASS: Market share figures are labelled as estimates with source and date — not presented as facts
- [ ] PASS: Job posting analysis is included as a leading indicator of product direction, and labelled as signal not confirmation
- [ ] PASS: Sources older than 18 months are flagged
- [ ] PARTIAL: Differentiation analysis takes a position on who is winning on each dimension — not just a neutral description of differences
- [ ] PASS: Output includes a sources section with URLs and what each source contributed

## Output expectations

- [ ] PASS: Output's market definition specifies — buyer (SMB HR / payroll administrator), purchase unit (per-employee per-month subscription typically), geography (Australia), specifically payroll + leave management for 10-200 employee businesses, AU regulatory context (Single Touch Payroll, Fair Work Act, super)
- [ ] PASS: Output names AU-relevant competitors — Xero Payroll, MYOB Payroll, Employment Hero, KeyPay (Employment Innovations), Deputy, Cloud Payroll — with at least 4-6 direct competitors named, plus indirect (Xero, MYOB as accounting suite that includes payroll) and substitute (manual / spreadsheet / accountant-handled)
- [ ] PASS: Output's classification distinguishes direct (HR + payroll specialists for AU SMB), indirect (broader accounting suites with payroll modules), and substitute (manual processes, outsourced bookkeeping) — not flattening into one list
- [ ] PASS: Output's sources include AU-specific — IBISWorld AU industry reports, Seek job postings (signal of which competitors are hiring engineers), G2 / Capterra AU category reviews, AFR / SmartCompany coverage — alongside global vendor sites
- [ ] PASS: Output's comparison matrix has columns for each competitor — AU compliance coverage, pricing tier (per-employee /month), feature breadth (payroll only vs HRIS suite), strengths, weaknesses — and is filterable by SMB segment
- [ ] PASS: Output presents market share figures with source AND date — e.g. "Xero Payroll: ~30% of AU SMB segment per Xero FY24 report" — never as bare unsourced facts
- [ ] PASS: Output uses job posting analysis as a leading indicator — competitor hiring signals product direction (e.g. "Employment Hero hiring 5 ML engineers in Sydney suggests AI-feature push") — labelled as signal, not confirmation
- [ ] PASS: Output flags any source older than 18 months as potentially stale — competitive landscape changes fast in AU SaaS
- [ ] PASS: Output's differentiation section takes a POSITION on who is winning on each dimension — e.g. "On price, Xero Payroll wins for accountant-managed; on feature breadth Employment Hero wins as full HRIS; on compliance depth KeyPay wins" — not a neutral catalogue
- [ ] PARTIAL: Output identifies the funding-pitch-relevant white space — the segment / feature / pricing combination that's currently underserved and would justify the requester's positioning
