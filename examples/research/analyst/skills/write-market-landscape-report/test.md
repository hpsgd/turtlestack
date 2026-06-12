# Test: write-market-landscape-report skill (stitch existing reports)

Scenario: A leadership team wants a quarterly market landscape report for AU field-service management software. Prior market-sizing and competitive-analysis reports already exist in the engagement directory; the landscape report should STITCH them into one executive narrative rather than re-research.

## Prompt

Work entirely from the staged input reports — do NOT perform any live web research (no WebSearch, no WebFetch). The market-sizing and competitive-analysis reports this stitching skill consumes are already on disk; for the trend scan, reason from those inputs rather than searching.

/analyst:write-market-landscape-report AU field-service management software Q2-2026 {workspace}/work/aurora

Locate and read the staged inputs first:

- `{workspace}/work/aurora/market-sizing/au-field-service-software.md` — TAM/SAM/SOM and CAGR with sources.
- `{workspace}/work/aurora/competitive-analysis/au-field-service-software.md` — the competitor set (ServiceFox, FieldNimbus, TradieFlow), comparison matrix, and recent strategic moves.

Requirements for the response:

- This is a STITCHING skill: pull the market definition, TAM/SAM/SOM, and CAGR from the market-sizing input (cite that report and its figures — do NOT invent a new TAM), and the competitive set + recent moves from the competitive-analysis input (cite that report).
- Lead with implications for leadership (the "so what") — where the market is heading, where the whitespace is, what decision it forces. Take a position with specific evidence, not "the market is growing rapidly".
- Condense competitor detail for an executive audience (one-line/one-paragraph profiles, organised direct / indirect / substitute).
- Include a "notable moves this period" section, dated, drawn from the competitive-analysis input's recent moves (ServiceFox acquisition + price rise, FieldNimbus AI-dispatch, TradieFlow Series A).
- Add a disciplined trend scan — the two or three structural shifts with material effect over 12-24 months — not an exhaustive horizon scan.
- The Sources table must cite the stitched analyst reports as workflow sources WITH their file paths, alongside any external sources.

## Criteria

- [ ] PASS: Skill writes a conforming report to disk under `aurora/market-landscape/` (see ARTIFACTS WRITTEN — at least one .md file there)
- [ ] PASS: The written file opens with YAML frontmatter including title, date, author=write-market-landscape-report, category (per report-conventions)
- [ ] PASS: The report STITCHES the inputs — it pulls TAM/SAM/SOM and CAGR from the market-sizing report and the competitor set from the competitive-analysis report, rather than re-researching from scratch
- [ ] PASS: The TAM/SAM/SOM figures match the staged market-sizing input (TAM ~A$1.4B, SAM ~A$480M, ~11% CAGR) and are NOT invented — the report inherits the sourced figures
- [ ] PASS: The report leads with implications for leadership (the "so what") taking a position with specific evidence — not "the market is growing rapidly" filler
- [ ] PASS: Competitor detail is condensed for an executive audience, organised direct / indirect / substitute
- [ ] PASS: A dated "notable moves this period" section reflects the recent moves from the competitive-analysis input (ServiceFox acquisition/price rise, FieldNimbus AI-dispatch, TradieFlow Series A)
- [ ] PASS: A disciplined trend scan names only the two or three structural shifts with material effect over 12-24 months — not an exhaustive list
- [ ] PASS: The Sources table cites the stitched analyst reports as workflow sources with their file paths (market-sizing and competitive-analysis), marked as internal
- [ ] PASS: The skill did NOT perform live web research — it stitched the staged inputs
- [ ] PASS: Chat response includes the absolute path to the written report

## Output expectations

- [ ] PASS: Provenance is visible — the report shows it inherited size from the market-sizing report and the competitive set from the competitive-analysis report, citing their paths, rather than presenting figures as freshly researched
- [ ] PASS: The report is written for an executive/leadership audience (condensed, decision-oriented), not as sales enablement or an exhaustive analyst dump
