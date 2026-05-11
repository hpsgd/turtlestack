---
name: company-lookup
description: "Research a company from public sources: overview, products, team, financials, recent news, and strategic direction. Writes a conforming report (per report-conventions) to <engagement_dir>/company-lookup/<company-slug>.md. Covers AU/NZ sources (ASIC, ABN, NZ Companies Office)."
argument-hint: "<company name> [engagement_dir]"
user-invocable: true
allowed-tools: WebSearch, WebFetch, Read, Write, Bash
---

Produce a structured company snapshot for the named company and write a conforming report.

## Step 0: Resolve arguments

Parse `$ARGUMENTS` as `<company name> [engagement_dir]`. The trailing token, if it looks like a path (starts with `/` or `~`, or names a directory that exists), is the engagement directory. Otherwise default to `pwd`. Resolve to an absolute path.

## Step 1: Compute the output path

Subject slug: full company name, kebab-case, lowercase, ASCII (per report-conventions). Strip apostrophes and other punctuation; keep legal suffixes lower-cased (`pty-ltd`, `inc`, `gmbh`).

Examples:

- `Acme Corp Pty Ltd` → `acme-corp-pty-ltd`
- `Canva` → `canva`

Output path: `$ENG/company-lookup/<slug>.md`

If a file already exists at that path, ask before overwriting (overwrite / write a `-2` sibling / abort).

## Step 2: Stage the report from the template

```bash
mkdir -p "$ENG/company-lookup"
cp "${CLAUDE_PLUGIN_ROOT}/templates/company-lookup.md" "$ENG/company-lookup/<slug>.md"
```

Replace placeholders in frontmatter:

| Placeholder | Replace with |
|---|---|
| `{SUBJECT}` | The company name as provided |
| `{SUBTITLE}` | Engagement directory basename, title-cased; drop the line if no useful inference |
| `{DATE}` | Today's ISO date |

## Step 3: Identify source types

Before searching, determine which source types apply:

- **Public company (ASX/NZX/NYSE/NASDAQ):** annual reports, exchange filings
- **AU company:** [ASIC Connect](https://connect.asic.gov.au) for company extract, director history, financials; [ABN Lookup](https://abn.business.gov.au) for ABN/ACN cross-reference
- **NZ company:** [NZ Companies Office](https://companies.govt.nz) for director history, shareholding, annual returns
- **US public company:** SEC EDGAR for 10-K/10-Q filings
- **UK company:** Companies House for filings and structure
- **Private company:** Crunchbase, LinkedIn, press

If the company's jurisdiction or listing status is unclear, run a quick name search on ASIC Connect and Crunchbase first to establish it.

## Step 4: Research and write into the staged file

Work through the sections in the staged file. Write findings into the appropriate section as you go. Cite sources inline using the source-citations rule (deep links, access dates) and tag tier per source-quality.

### Overview and products

Search for: company name + "about", company website, LinkedIn company page.

Capture in the Overview and Products sections:

- What the company does and its business model
- Core products/services with pricing if public
- Target customer and market segment
- Founding year, HQ, and approximate size

### Team

Search company website "team" or "leadership" page, LinkedIn.

Capture founding team backgrounds and current key executives (name, role, tenure where visible). Note notable hires or departures in the last 12 months.

### Financials

For public companies: pull latest annual report or filing for revenue, growth rate, and key metrics.

For private companies: check Crunchbase for funding rounds (amount, date, investors, valuation if disclosed). Note when data was last confirmed.

Never present a revenue figure without its source and date. Label estimates as estimates.

### Recent news

Search: `[company name] site:news.google.com` or Google News for last 6 months.

Prioritise: funding rounds, product launches, leadership changes, regulatory actions, acquisitions, layoffs.

Flag known reputational issues — controversies, regulatory actions, public criticism, ethics concerns — that may surface in stakeholder conversations.

### Strategic direction

Signals for where the company is heading:

- Current job postings (company careers page + LinkedIn Jobs + Seek for AU/NZ) — engineering hires in a new area, senior leadership hires in a new function
- Recent press releases and executive statements
- Product launches and roadmap announcements
- Investor day or analyst day materials (public companies)

For meeting-prep contexts, also note likely conversation topics: strategic shifts the user may want to ask about, executive statements that have generated discussion, and known sensitivities the other party may raise.

## Step 5: Finalise the report

- Replace placeholder source rows with actual sources, tagged with tier per source-quality.
- Cross-reference at least two independent sources for any fact listed in the output.
- Set `status: Final` once complete; optionally set `confidence: 0-4`.

## Rules

- Never present a revenue estimate for a private company without stating the source and explicitly labelling it as an estimate.
- Cross-reference at least two independent sources for any fact listed in the output.
- If the company has no meaningful public web presence, flag before proceeding — may be too early-stage for useful intelligence.
- Revenue ≠ valuation. Distinguish these clearly when both appear.
- Recency matters on competitive data. Flag any source older than 12 months — for public companies that report quarterly, anything beyond the last few quarters is stale. Use a tighter threshold (6 months) for fast-moving sectors like AI, fintech, or anything where the previous quarter's narrative may already be obsolete.
- One file per invocation. Don't write findings inline into chat.

## Output

A single line: the absolute path to the written report.
