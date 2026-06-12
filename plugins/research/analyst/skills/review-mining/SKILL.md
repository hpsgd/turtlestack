---
name: review-mining
description: "Mine G2, Capterra, app stores, and Trustpilot reviews for OWN and COMPETITOR products: extract themes, quantify their weight, and segment-skew the findings. Writes a conforming report (per report-conventions) to <engagement_dir>/review-mining/<slug>.md. Use to surface unsolicited customer language, feature gaps, and a competitor's customer complaints as your opportunity inventory."
argument-hint: "<product or competitor to mine> [engagement_dir]"
user-invocable: true
allowed-tools: WebSearch, WebFetch, Read, Write, Bash
---

Mine public review sites for a product (yours or a competitor's) and write a conforming report. Reviews contain verbatim,
unsolicited customer language — which makes them more honest than survey responses, where the question shapes the answer.
This is the analyst's strategic review-VoC lens. It deliberately overlaps with the voice-of-customer work other roles
hold (support reads tickets, customer-success reads churn signal, UX reads interviews). That overlap is intentional —
each role mines customer voice through its own lens, and the different readings are meant to be consulted together, not
merged. This skill's lens is competitive and strategic: themes at category scale, and competitor reviews as an
opportunity inventory. It pairs with `/analyst:competitive-analysis` and `/analyst:competitor-teardown`.

## Step 0: Resolve arguments

Parse `$ARGUMENTS` as `<product or competitor> [engagement_dir]`. A trailing path-shaped token is the engagement
directory; otherwise default to `pwd`. Resolve to `$ENG`.

## Step 1: Compute the output path

Subject slug: kebab-case, lowercase, ASCII (per report-conventions), product/company name.

Example: `Notion` → `notion`.

Output path: `$ENG/review-mining/<slug>.md`. If the file exists, ask before overwriting.

Stage the file on disk NOW, before any analysis: create the directory and write the report's
frontmatter and the section headings from the Output Format below to that path with the Write tool.
Then fill in each section in place as you work through the steps. The report file is the
deliverable — it must exist on disk before you produce the analysis. Do not compose the report in
your chat reply and skip writing the file.

## Step 2: Identify the review sources

Locate the product's listings across the sites that matter for its category:

- [G2](https://www.g2.com) and [Capterra](https://www.capterra.com) — B2B software, richest verbatim and competitor-comparison content
- App stores ([Apple App Store](https://apps.apple.com), [Google Play](https://play.google.com)) — consumer and mobile products
- [Trustpilot](https://www.trustpilot.com) — consumer services and broad-market products
- Category-specific sites where relevant (e.g. industry-specific review platforms)

Link to the specific product listing, not the platform homepage (per source-citations). Record the review count and the
average rating per site as context.

## Step 3: Read across the rating distribution, not just the extremes

Review populations skew bimodal — people review when delighted enough to recommend or annoyed enough to warn. Read the
1-2 star reviews (the warnings) AND the 4-5 star reviews (what they value), and deliberately sample the 3-star reviews,
which carry the most balanced signal. A theme pulled only from 1-star reviews tells you what the angriest 5% think, not
what the market thinks.

## Step 4: Extract themes

Cluster the reviews into themes by topic — onboarding, specific features, support, reliability, pricing, integrations.
For each theme, capture:

- A representative verbatim quote (the customer's own words are the asset)
- Roughly what share of reviews touch it (quantify: "~17% of reviews mention onboarding friction")
- The sentiment direction (praised / complained-about / mixed)

Quantification matters. "Some users mention X" is weak. "X appears in roughly a fifth of reviews and skews negative" is a
finding.

## Step 5: Segment-skew the themes

Where reviews carry segment metadata (company size, role, industry, plan tier), check whether a theme concentrates in a
segment. "Onboarding friction skews toward enterprise reviewers" is far more actionable than the flat theme. Segment skew
is where review mining earns its keep over a star rating.

## Step 6: Competitor reviews as opportunity inventory

When mining a competitor, the complaints are your opportunity inventory. Run the same theme extraction on the
competitor's reviews and translate the top complaint themes into "what we could win on". When mining your own product,
the complaints are your fix-list. Be explicit about which lens this run is using.

## Step 7: Finalise

You MUST write the full report to the output path with the Write tool — this is the deliverable, not the chat reply. Do
not answer the analysis inline and skip the file. Flag the representativeness caveat explicitly — review populations are directional, not
statistically representative. Tag every source with a tier (review sites are typically T4 customer voice per
source-quality; flag incentivised-review programmes that inflate ratings). Set `status: Final`.

## Rules

- Link to the specific product listing, not the site homepage. Record review count and average rating per site.
- Read across the full rating distribution. A theme from 1-star reviews alone is the angriest 5%, not the market.
- Quantify every theme. "Some users say X" is not a finding; "X appears in ~20% of reviews, skewing negative" is.
- Segment-skew where metadata allows. The concentration is the insight, not the flat theme.
- State the lens: own-product mining produces a fix-list; competitor mining produces an opportunity inventory. Don't blur them.
- Always flag representativeness. Reviews are directional; the population self-selects. Check for incentivised-review programmes inflating ratings.
- Don't reconcile with other VoC lenses. This is the strategic/competitive lens; support tickets and churn signal are separate, deliberately overlapping readings.
- One file per invocation. Don't write findings inline into chat.

## Output Format

Write a single conforming report to the output path with this structure:

```markdown
---
title: Review mining — {PRODUCT}
subtitle: {ENGAGEMENT}
date: {DATE}
author: review-mining
category: Commercial
subject: {PRODUCT}
status: Draft
confidence: {0-4}
---

## Lens

[Own-product (fix-list) or competitor (opportunity inventory). One line.]

## Sources mined

| Site | Listing | Review count | Avg rating | Notes |
|---|---|---|---|---|

## Themes

| Theme | Share of reviews | Sentiment | Representative verbatim |
|---|---|---|---|

## Segment skew

[Where a theme concentrates in a segment — company size, role, industry, plan tier.]

## Opportunity inventory / fix-list

[Competitor lens: their top complaints translated into what we could win on. Own lens: the prioritised fix-list.]

## Representativeness caveat

[Who reviews and who doesn't; any incentivised-review signals; why these findings are directional not representative.]

## Sources

| # | Source | Tier | Accessed | What it contributed |
|---|---|---|---|---|
| 1 | [Listing](URL) | T4 | YYYY-MM-DD | — |
```

## Output

After writing the file, respond with a single line: the absolute path to the written report. The path must point to the
file you actually wrote with the Write tool — do not report a path without having written it.
