---
name: write-market-landscape-report
description: "Produce a periodic (quarterly/annual) executive-audience market landscape report that stitches existing market-sizing and competitive-analysis outputs into one narrative: market definition and size, competitive set, recent moves, and a trend scan. Writes a conforming report (per report-conventions) to <engagement_dir>/market-landscape/<slug>.md. Use for board/leadership audiences, not for sales enablement."
argument-hint: "<market or category> [period, e.g. Q3-2026] [engagement_dir]"
user-invocable: true
allowed-tools: WebSearch, WebFetch, Read, Write, Bash, Glob
---

Produce a market landscape report for an executive audience and write a conforming report. This is a stitching skill: it
combines existing analyst outputs rather than re-researching from scratch. Its genuine workflow inputs are
`/analyst:market-sizing` (the TAM/SAM/SOM figures) and `/analyst:competitive-analysis` (the competitive set and recent
moves). Where those reports already exist in the engagement directory, read and cite them; where they don't, run them
first or commission them. It also draws on `/analyst:competitor-teardown` outputs for any competitor that warrants depth.

## Step 0: Resolve arguments

Parse `$ARGUMENTS` as `<market or category> [period] [engagement_dir]`. A trailing path-shaped token is the engagement
directory; otherwise default to `pwd`. Resolve to `$ENG`. If no period is given, default to the current quarter.

## Step 1: Locate the input reports

This report stitches existing work. Find the inputs in the engagement directory:

```bash
ls "$ENG"/market-sizing/*.md 2>/dev/null
ls "$ENG"/competitive-analysis/*.md 2>/dev/null
ls "$ENG"/competitor-teardown/*.md 2>/dev/null
```

For each input found, read it and note the path — you will cite it as a workflow source. If a required input is
**missing**:

- No market-sizing report → run `/analyst:market-sizing` for this market first, or state explicitly that the size figure
  is unsourced and flag it.
- No competitive-analysis report → run `/analyst:competitive-analysis` first.

Don't silently invent figures this report is supposed to inherit. The landscape report's credibility comes from its
sourced inputs.

## Step 2: Compute the output path

Subject slug: kebab-case, lowercase, ASCII (per report-conventions). Combine market and period.

Examples: `Australian payroll software, Q3 2026` → `australian-payroll-software-q3-2026`.

Output path: `$ENG/market-landscape/<slug>.md`. If the file exists, ask before overwriting.

Stage the file on disk NOW, before any analysis: create the directory and write the report's
frontmatter and the section headings from the Output Format below to that path with the Write tool.
Then fill in each section in place as you work through the steps. The report file is the
deliverable — it must exist on disk before you produce the analysis. Do not compose the report in
your chat reply and skip writing the file.

## Step 3: Market definition and size

Pull the definition and the TAM/SAM/SOM figures from the market-sizing input. Restate the definition (buyer, purchase
unit, geography) so the report stands alone, and cite the source report. Include the growth rate (CAGR) with its source
and period. If you ran the sizing fresh, the methodology lives in that report — summarise, don't duplicate.

## Step 4: Competitive set

Pull the competitor set from the competitive-analysis input. For an executive audience, condense to one-paragraph (or
one-line) profiles, organised direct / indirect / substitute. Include a visual competitive frame where useful — a 2x2
positioning map or category map. Axes must come from buyer decision criteria, not analyst intuition; state the axes
chosen and why.

## Step 5: Notable moves in the period

Synthesise the recent strategic moves from the competitive-analysis and teardown inputs, filtered to the reporting
period: funding, launches, M&A, pricing changes, key hires. Date every move. This section is what makes the report
*periodic* — it's the delta since the last landscape report.

## Step 6: Trend scan

Add the forward-looking layer the input reports don't carry. Cover the structural shifts that bear on this market over
the next 12-24 months: regulatory, technological, market-structure, buyer-behaviour. Keep it disciplined — name the two
or three trends with material effect, not an exhaustive horizon scan. If a full macro scan is warranted, commission
`/analyst:pestle` and cite it rather than padding this section.

## Step 7: Implications for leadership

Close with the "so what" for the executive audience: where the market is heading, where the whitespace is, what decisions
this landscape forces. Specific claims with evidence — never "the market is growing rapidly". Take a position.

## Step 8: Finalise

You MUST write the full report to the output path with the Write tool — this is the deliverable, not the chat reply. Do
not answer the analysis inline and skip the file. The Sources table must list the stitched analyst reports as workflow sources alongside external
sources, each tier-tagged. Set `status: Final`.

## Rules

- Stitch, don't re-research. The inputs are `/analyst:market-sizing` and `/analyst:competitive-analysis` outputs. Read and cite them; only research fresh for the trend scan or to fill a missing input.
- Never inherit an unsourced figure. If the market-sizing input is missing, run it or flag the gap — don't invent a TAM.
- Write for executives. Condense competitor detail; push depth into the teardown reports and link them.
- Cite the stitched reports as sources, with their file paths. Provenance is the point of a stitching skill.
- Specific claims with evidence. "The market is growing rapidly" is decoration, not analysis. Give the number and its source.
- Keep the trend scan to the few trends that matter. An exhaustive list signals you didn't prioritise.
- One file per invocation. Don't write findings inline into chat.

## Output Format

Write a single conforming report to the output path with this structure:

```markdown
---
title: Market landscape — {MARKET} ({PERIOD})
subtitle: {ENGAGEMENT}
date: {DATE}
author: write-market-landscape-report
category: Commercial
subject: {MARKET}
status: Draft
confidence: {0-4}
---

## Implications for leadership

[The "so what" up front for executive readers: where the market is heading, where the whitespace is, what decisions this
forces. Take a position.]

## Market definition and size

[Definition restated (buyer, purchase unit, geography). TAM/SAM/SOM with source. CAGR with source and period. Cite the
market-sizing report.]

## Competitive set

[Condensed profiles, organised direct / indirect / substitute. Positioning map with stated axes. Cite the
competitive-analysis report.]

## Notable moves this period

[Dated list of funding, launches, M&A, pricing, hires within the reporting period. The delta since last landscape.]

## Trend scan

[The two or three structural shifts with material effect over 12-24 months. Regulatory, technological, market-structure,
buyer-behaviour.]

## Sources

| # | Source | Tier | Accessed | What it contributed |
|---|---|---|---|---|
| 1 | [market-sizing/<slug>.md](relative path) | — (internal) | YYYY-MM-DD | Market size and growth |
| 2 | [competitive-analysis/<slug>.md](relative path) | — (internal) | YYYY-MM-DD | Competitive set and moves |
| 3 | [Title](URL) | T1 / T2 / T3 / T4 / T5 | YYYY-MM-DD | — |
```

## Output

After writing the file, respond with a single line: the absolute path to the written report. The path must point to the
file you actually wrote with the Write tool — do not report a path without having written it.
