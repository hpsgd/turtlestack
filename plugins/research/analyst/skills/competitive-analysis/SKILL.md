---
name: competitive-analysis
description: "Map the competitive landscape for a market or product space: identify competitors, compare on key dimensions, and surface strategic moves. Writes a conforming report (per report-conventions) to <engagement_dir>/competitive-analysis/<market-slug>.md. Includes job posting analysis as a leading indicator of product direction."
argument-hint: "<market, product, or company to analyse> [engagement_dir]"
user-invocable: true
allowed-tools: WebSearch, WebFetch, Read, Write, Bash
---

Produce a competitive analysis for the named market/product/company and write a conforming report.

## Step 0: Resolve arguments

Parse `$ARGUMENTS` as `<market or product> [engagement_dir]`. Trailing path-shaped token is the engagement directory; otherwise default to `pwd`. Resolve to an absolute path.

## Step 1: Compute the output path

Subject slug: kebab-case, lowercase, ASCII (per report-conventions). For a named product or company, use the product/company name. For a market space, use the most specific phrase that identifies it.

Examples:

- `Australian payroll software` → `australian-payroll-software`
- `Canva alternatives` → `canva-alternatives`
- `Notion` → `notion`

Output path: `$ENG/competitive-analysis/<slug>.md`

If a file already exists at that path, ask before overwriting (overwrite / write a `-2` sibling / abort).

## Step 2: Stage the report from the template

```bash
mkdir -p "$ENG/competitive-analysis"
cp "${CLAUDE_PLUGIN_ROOT}/templates/competitive-analysis.md" "$ENG/competitive-analysis/<slug>.md"
```

Replace placeholders in frontmatter:

| Placeholder | Replace with |
|---|---|
| `{SUBJECT}` | The market/product/company name as provided |
| `{SUBTITLE}` | Engagement directory basename, title-cased; drop the line if no useful inference |
| `{DATE}` | Today's ISO date |

## Step 3: Define the market

Write into the Market definition section of the staged file. Before identifying competitors, define what you're actually comparing:

- What problem is being solved?
- Who is the buyer? (individual, SMB, enterprise, government)
- What is the purchase unit? (subscription, licence, one-time, services)
- What geography? (global, US, AU/NZ, other)

If these aren't clear from the input, make your assumptions explicit in the output.

## Step 4: Identify competitors

Three categories:

- **Direct** — same solution, same customer, competing for the same purchase decision
- **Indirect** — different solution, same underlying problem
- **Substitutes** — alternative approaches the buyer might choose instead (including doing nothing or building in-house)

Sources: G2 category pages, Capterra category pages, "alternatives to [product]" searches, industry analyst quadrant reports, LinkedIn "companies also viewed."

For AU/NZ markets: IBISWorld AU reports, Seek job postings pattern, local industry press.

List each competitor with a one-line positioning statement in the appropriate subsection of the Competitors identified section.

## Step 5: Build the comparison matrix

For each identified competitor, research and fill into the Competitor comparison table:

| Attribute | What to look for |
|---|---|
| Positioning | Their own words — tagline, homepage hero, ICP |
| Pricing tier | Free/freemium/SMB/mid-market/enterprise — exact pricing if public |
| Strengths | G2/Capterra review themes, analyst commentary, customer win stories |
| Weaknesses | Negative review themes, gaps in feature set, company risk factors |

## Step 6: Job postings as roadmap signal

Search each competitor's careers page and LinkedIn Jobs. Engineering hires in a new area signal product direction before any announcement.

Patterns to look for:

- New language or platform skills appearing in bulk (ML, mobile, specific cloud)
- Senior leadership hires in a new function (first Head of Enterprise Sales = moving upmarket)
- Spikes in hiring volume (growth mode) or absence of hiring (freeze or pivot)

For AU/NZ companies: check Seek (`seek.com.au` / `seek.co.nz`) alongside LinkedIn for a fuller picture of hiring activity.

Cross-reference with their public announcements — divergence between what they say and what they're hiring for is the more useful signal.

Record in the Hiring signals table.

## Step 7: Recent strategic moves

For each competitor, note the last 12 months in the Recent strategic moves section:

- Acquisitions and partnerships
- Pricing changes or packaging shifts
- Major product launches or deprecations
- Fundraising rounds or M&A activity
- Leadership changes

## Step 8: Differentiation analysis

Synthesise into the Differentiation analysis section: who is winning on what dimension, and why? One paragraph per meaningful differentiation axis. Take a position — don't just describe, conclude.

## Step 9: Finalise the report

- Replace placeholder source rows with actual sources, tagged with tier per source-quality.
- Set `status: Final` once complete; optionally set `confidence: 0-4`.

## Rules

- Define the market before mapping competitors. A comparison without scope is noise.
- Label market share estimates as estimates with source and date.
- Flag sources older than 18 months on competitive analysis — a competitor can ship a lot in that time.
- Don't produce a matrix so wide it can't be read. Cap at 6 attributes if there are more than 4 competitors.
- Job posting data is a leading indicator, not a fact. Label it as signal, not confirmation.
- One file per invocation. Don't write findings inline into chat.

## Output

A single line: the absolute path to the written report.
