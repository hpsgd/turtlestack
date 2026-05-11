---
name: due-diligence
description: "Assess a company from public sources for a specific decision: partnership, investment consideration, or acquisition. Writes a conforming report (per report-conventions) to <engagement_dir>/due-diligence/<company-slug>.md with a structured signal summary. Public data only."
argument-hint: "<company name> for <partnership | investment | acquisition> [engagement_dir]"
user-invocable: true
allowed-tools: WebSearch, WebFetch, Read, Write, Bash
---

Produce a public-data due diligence report on the named company and write a conforming report.

This skill covers public-data diligence only. Legal, financial, and technical diligence requires direct access to private information — flag this clearly in the output.

## Step 0: Resolve arguments

Parse `$ARGUMENTS` as `<company name> for <scope> [engagement_dir]`. Scope is one of: `partnership`, `investment`, `acquisition`. The trailing path-shaped token, if present, is the engagement directory; otherwise default to `pwd`. Resolve to an absolute path.

## Step 1: Compute the output path

Subject slug: company name, kebab-case, lowercase, ASCII (per report-conventions). Strip apostrophes and other punctuation; keep legal suffixes lower-cased (`pty-ltd`, `inc`).

Output path: `$ENG/due-diligence/<slug>.md`

If a file already exists at that path, ask before overwriting (overwrite / write a `-2` sibling / abort).

## Step 2: Stage the report from the template

```bash
mkdir -p "$ENG/due-diligence"
cp "${CLAUDE_PLUGIN_ROOT}/templates/due-diligence.md" "$ENG/due-diligence/<slug>.md"
```

Replace placeholders in frontmatter:

| Placeholder | Replace with |
|---|---|
| `{SUBJECT}` | The company name as provided |
| `{SUBTITLE}` | Engagement directory basename, title-cased; drop the line if no useful inference |
| `{DATE}` | Today's ISO date |
| `{SCOPE}` | `partnership` / `investment` / `acquisition` |

Set the Scope section in the body to a one-sentence framing of what decision this report supports. The scope determines how deep to go on each section:

- **Commercial partnership** — focus on product-market fit, team stability, and reputational risk
- **Investment consideration** — focus on growth trajectory, unit economics signals, and competitive moat
- **Acquisition consideration** — full picture: fundamentals + product + team + market position + risk

Misclassified scope produces an incomplete report.

## Step 3: Research and write into the staged file

Work through the sections in the staged file. Write findings into the appropriate section as you go. Cite sources inline using the source-citations rule (deep links, access dates) and tag tier per source-quality.

### Business fundamentals

For public companies: pull latest annual report/filing for revenue, growth rate, gross margin, key operational metrics.

For private companies: Crunchbase for funding history; press for disclosed revenue milestones; LinkedIn for headcount growth as a proxy.

Each figure needs a source and date. Label revenue estimates for private companies explicitly.

### Product signals

Customer sentiment from public reviews:

- [G2](https://www.g2.com) — review count, score, score trend, category rank
- [Capterra](https://www.capterra.com) — secondary review source
- App Store / Google Play — mobile products

Look for: score trend over 6+ months (not just current score), review velocity (growing or stalling), themes in negative reviews (support, reliability, missing features).

Also note: notable customer wins mentioned in press, reference customers on their website, case studies.

### Team

From company website, LinkedIn, and press:

- Founding team backgrounds (relevant domain experience, prior exits)
- Current key executives — tenures, any recent departures
- Notable hires in last 12 months (signal of growth direction)
- Notable departures in last 12 months (potential instability flag)

Executive churn without a clear succession announcement is a red signal.

### Market position

- Analyst market share estimates (cite report and year)
- Growth rate vs market growth rate (is the company growing faster or slower than the market?)
- Any identifiable competitive moat (network effects, switching costs, data advantage, regulatory barriers)
- Customer concentration signals (are case studies all from one segment?)

### Risk factors

- Regulatory exposure: active proceedings, compliance actions — search ASIC Connect (AU), Companies House (UK), SEC EDGAR (US)
- Litigation: court filings, press coverage of legal disputes
- Reputational: negative press, data breach history, executive controversy
- Financial red flags: down rounds, flat rounds, long gaps between funding with no milestone announced
- Operational red flags: hiring freeze with no explanation, mass layoffs, major customer losses

### Signal summary

Classify every major finding against the signal taxonomy before writing the verdict.

**Green signals:**

- Consecutive funding rounds with increasing round size
- Core founding team still in place after 3+ years
- Review score stable or improving, review count growing
- Customer logos include recognisable names in target segment
- Hiring volume growing, seniority of hires increasing
- Press coverage is product-led (shipping) not just funding-led (raising)

**Red signals:**

- Sudden C-suite departure without succession announcement
- Down round or flat round after strong growth
- Review score declining over 6+ months
- Regulatory proceedings or litigation in public records
- Layoff announcements without a clear restructuring narrative
- Hiring freeze with no public explanation
- Long gap between funding rounds, no revenue milestone announced
- Heavy reliance on a single customer segment

Fill the Signal summary table in the file with status (🟢/🟡/🔴) and a one-line evidence cell for each row.

### Red flag escalation

When the signal summary contains two or more red signals, don't stop at the verdict. Route deeper:

| Red signal type | Follow-on |
|---|---|
| Regulatory or litigation findings | `/investigator:public-records` for the full court and regulatory record |
| Complex or opaque ownership | `/investigator:corporate-ownership` to map the full structure |
| Reputational concern or data breach history | `/investigator:entity-footprint` for digital footprint and press timeline |
| Customer concentration or market position concern | `/analyst:competitive-analysis` to understand alternatives |

One red signal warrants noting. Two or more warrants investigation. Record dispatched or recommended follow-ons in the Red flag escalation section of the report.

## Step 4: Finalise the report

- Write the verdict as one sentence with the 1-2 factors that most influence it.
- Replace placeholder source rows with actual sources, tagged with tier per source-quality.
- Set `status: Final` once complete; optionally set `confidence: 0-4`.

## Rules

- State the scope explicitly in the report frontmatter and the Scope section. Diligence for a partnership is narrower than for an acquisition.
- Every revenue figure needs a source and date.
- Revenue ≠ valuation. Distinguish them — the confusion causes real decisions to go wrong.
- The signal summary must precede the verdict. Don't write conclusions without showing the signals.
- Flag clearly that this is public-data diligence only. Private diligence (financials, legal, technical) requires direct access.
- One file per invocation. Don't write findings inline into chat.

## Output

A single line: the absolute path to the written report.
