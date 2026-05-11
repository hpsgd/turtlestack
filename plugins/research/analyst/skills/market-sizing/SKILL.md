---
name: market-sizing
description: "Estimate the size of a market using top-down and bottom-up methods with explicit methodology. Writes a conforming report (per report-conventions) to <engagement_dir>/market-sizing/<market-slug>.md. Use when you need a defensible TAM/SAM/SOM figure for a business plan, pitch, or investment decision."
argument-hint: "<market to size, with geography and buyer type if known> [engagement_dir]"
user-invocable: true
allowed-tools: WebSearch, WebFetch, Read, Write, Bash
---

Produce a market sizing estimate for the named market and write a conforming report with explicit methodology.

## Step 0: Resolve arguments

Parse `$ARGUMENTS` as `<market description> [engagement_dir]`. Trailing path-shaped token is the engagement directory; otherwise default to `pwd`. Resolve to an absolute path.

## Step 1: Compute the output path

Subject slug: kebab-case, lowercase, ASCII (per report-conventions). Use the most specific phrase that identifies the market.

Examples:

- `Australian payroll software for SMBs` → `australian-payroll-software-smb`
- `Global cloud security` → `global-cloud-security`

Output path: `$ENG/market-sizing/<slug>.md`

If a file already exists at that path, ask before overwriting (overwrite / write a `-2` sibling / abort).

## Step 2: Stage the report from the template

```bash
mkdir -p "$ENG/market-sizing"
cp "${CLAUDE_PLUGIN_ROOT}/templates/market-sizing.md" "$ENG/market-sizing/<slug>.md"
```

Replace placeholders in frontmatter:

| Placeholder | Replace with |
|---|---|
| `{SUBJECT}` | The market description as provided |
| `{SUBTITLE}` | Engagement directory basename, title-cased; drop the line if no useful inference |
| `{DATE}` | Today's ISO date |

## Step 3: Define the market

Write into the Market definition section of the staged file. A market size without a definition is a number without meaning. Establish:

- **Buyer:** who is paying? (individual, SMB, enterprise, government department)
- **Purchase unit:** what are they buying? (subscription, one-time, services engagement)
- **Geography:** global, country-level, or regional?
- **Time horizon:** current year, or a projected year?

State these assumptions explicitly. Different assumptions produce wildly different numbers — the definition IS the methodology.

## Step 4: Top-down estimate

Find analyst estimates from credible sources:

- [Gartner](https://www.gartner.com) — technology markets
- [IDC](https://www.idc.com) — technology markets
- [Grand View Research](https://www.grandviewresearch.com) — broad industry coverage
- [IBISWorld](https://www.ibisworld.com) — AU industry reports specifically (`ibisworld.com/au`)
- [ABS](https://www.abs.gov.au) — AU macro/industry data
- [Stats NZ](https://www.stats.govt.nz) — NZ industry data

For each estimate: note the specific report title, year published, and the exact figure cited. Never round-trip a sourced figure without the original citation.

Record findings in the Top-down estimate section and add the row to the Size estimates table.

If no analyst report exists for this specific market, note it and proceed to bottom-up.

## Step 5: Bottom-up estimate

Build independently from first principles. Write into the Bottom-up estimate section:

1. **Estimate addressable customer count** — how many potential buyers exist? (Use industry association data, government statistics, LinkedIn company size filters as proxies)
2. **Estimate average annual spend** — what does a typical buyer spend? (Use public pricing, customer testimonials, analyst benchmarks)
3. **Apply realistic penetration** — what share could be captured at maturity? (Comparable market penetration rates from analogous markets)

Show the calculation explicitly: `N customers × $X avg spend × Y% penetration = $Z`

Add the row to the Size estimates table.

## Step 6: Reconcile

Do the top-down and bottom-up figures agree within 2x?

- **Yes:** record both, note the alignment as confidence signal
- **No:** explain the variance. Common reasons: different market definitions, different geographies, different buyer segmentation. Don't average them — resolve the discrepancy

Write the reconciliation into the Reconciliation section.

## Step 7: Growth rate

Find CAGR from:

- Analyst report projections (preferred)
- Public company revenue growth rates in the space (proxy — available from earnings reports)
- VC/PE investment velocity as a leading signal

Note the source and the period it covers. Write into the Growth rate section.

## Step 8: Finalise the report

- Set the Confidence rating (High / Medium / Low) with reasoning.
- Replace placeholder source rows with actual sources, tagged with tier per source-quality.
- Set `status: Final` once complete; optionally set `confidence: 0-4`.

## Rules

- A market size without methodology is a guess wearing a number's clothes. Always show the working.
- Label all estimates as estimates. Never present a number as fact unless it comes from a primary regulatory or government source.
- Top-down and bottom-up must both be attempted. If one genuinely can't be done, explain why.
- Don't average unreconciled top-down and bottom-up figures. Diagnose the gap instead.
- Distinguish TAM (total addressable), SAM (serviceable addressable), and SOM (serviceable obtainable) if the question calls for it. If not asked, default to TAM and state what's included.
- One file per invocation. Don't write findings inline into chat.

## Output

A single line: the absolute path to the written report.
