---
name: competitor-teardown
description: "Deep-dive analysis of a SINGLE competitor (15-30 pages) triggered by a strategic event — a raise, a launch, entry into your segment, or a pricing change. Covers product architecture from public sources, pricing, ICP, GTM motion, funding, and key people. Writes a conforming report (per report-conventions) to <engagement_dir>/competitor-teardown/<slug>.md. Use for one competitor in depth, not a landscape."
argument-hint: "<competitor name> [triggering event] [engagement_dir]"
user-invocable: true
allowed-tools: WebSearch, WebFetch, Read, Write, Bash
---

Produce a deep teardown of a single competitor and write a conforming report. A teardown is not a quarterly document and
not a competitive landscape — it is a one-time deep investigation triggered by a strategic event that made this
competitor material. It is broader and deeper than `/analyst:competitive-analysis` (which maps a whole set at the
landscape level): this one goes all the way down on one company. Output feeds `/analyst:write-market-landscape-report`
and `/analyst:win-loss-analysis`.

## Step 0: Resolve arguments

Parse `$ARGUMENTS` as `<competitor> [triggering event] [engagement_dir]`. A trailing path-shaped token is the engagement
directory; otherwise default to `pwd`. Resolve to `$ENG`.

## Step 1: Name the trigger

State up front *why this teardown is happening now*. A teardown without a trigger drifts into an unfocused company
profile. Valid triggers:

- The competitor raised a large round
- They launched in your primary segment or category
- They changed pricing or packaging materially
- They started showing up in more of your deals (cross-reference `/analyst:win-loss-analysis`)
- An acquisition changed their capability or reach

The trigger sets the lens. A funding-triggered teardown weights GTM expansion and hiring; a launch-triggered teardown
weights product architecture and positioning. Write the trigger into the report's opening.

## Step 2: Compute the output path

Subject slug: kebab-case, lowercase, ASCII (per report-conventions), competitor name without legal suffix punctuation.

Examples: `Canva` → `canva`; `Visual Data Solutions Pty Ltd` → `visual-data-solutions`.

Output path: `$ENG/competitor-teardown/<slug>.md`. If the file exists, ask before overwriting.

Stage the file on disk NOW, before any analysis: create the directory and write the report's
frontmatter and the section headings from the Output Format below to that path with the Write tool.
Then fill in each section in place as you work through the steps. The report file is the
deliverable — it must exist on disk before you produce the analysis. Do not compose the report in
your chat reply and skip writing the file.

## Step 3: Product architecture from public sources

Reconstruct how the product is built using only legitimate public sources — never pretexting, never unauthorised access.
Sources that reveal architecture:

- API documentation and developer docs (data model, integration surface, extensibility)
- Job postings describing the tech stack (languages, cloud, ML/data tooling) — a leading indicator of direction
- Conference talks, engineering blogs, public GitHub
- Status pages and changelogs (release cadence, reliability posture)

State what each inference rests on. "They use a specific cloud" sourced from a job ad is signal, not confirmation.

## Step 4: Pricing and packaging

Capture the full pricing model: tiers, price points (exact if public), the packaging logic (per-seat, consumption,
flat), what's gated behind which tier, and how it has changed over time. Where they hide pricing ("contact sales"),
record that as a signal about their motion — it usually means enterprise, negotiated, high-ACV.

## Step 5: ICP and target segments

Who do they actually sell to? Triangulate from: customer logos on the site, case studies (which segments, which use
cases), review-site populations (cross-reference `/analyst:review-mining`), and the seniority/function of their sales
hires. Distinguish who they *say* they target from who their evidence shows they *win*.

## Step 6: Go-to-market motion

How do they acquire customers? Product-led (free tier, self-serve), sales-led (demos, AEs, long cycles), channel/partner,
or community-led. Read it from: presence of a free tier, sales-team hiring volume, partner pages, event sponsorship,
content/SEO footprint. The motion predicts where they're strong and where they're beatable.

## Step 7: Funding and financial position

Funding rounds (amount, date, lead, valuation if disclosed), runway inference, public revenue signals (earnings if
public, press estimates if private — labelled as estimates with source). For AU/NZ entities, check ASIC / NZ Companies
Office filings. Never state a revenue figure without saying where it came from.

## Step 8: Key people

Leadership and recent senior hires — especially hires that signal direction (first Head of Enterprise Sales = moving
upmarket; first Head of Platform = opening an ecosystem). Use public professional context only (LinkedIn, published work,
talks). Do not profile individuals personally.

## Step 9: So what — the strategic read

Synthesise. Given the trigger, what does this competitor's full picture mean for us? Where are they genuinely stronger,
where are they exposed, and what should we do differently? Take a position. A teardown that ends in a neutral profile has
failed — the deliverable exists to inform a decision.

## Step 10: Finalise

You MUST write the full report to the output path with the Write tool — this is the deliverable, not the chat reply. Do
not answer the analysis inline and skip the file. Tag every source with a tier. Set `status: Final` when complete.

## Rules

- Lead with the trigger. No trigger, no teardown — it becomes an aimless company profile.
- Public sources only. No pretexting, no inducing NDA breaches, no unauthorised access. Cite the SCIP-style ethics line if scope is questioned.
- Separate claim from confirmation. Job-ad and changelog inferences are signal; label them.
- Distinguish stated targeting from won targeting. Marketing pages describe ambition; logos and case studies describe reality.
- Never state a revenue or valuation figure without its source and an "estimate" label where it isn't from a filing.
- End with a strategic read, not a summary. Take a position on what to do.
- One file per invocation. Don't write findings inline into chat.

## Output Format

Write a single conforming report to the output path with this structure:

```markdown
---
title: Competitor teardown — {COMPETITOR}
subtitle: {ENGAGEMENT}
date: {DATE}
author: competitor-teardown
category: Commercial
subject: {COMPETITOR}
status: Draft
confidence: {0-4}
---

## Trigger

[Why this teardown, why now. One paragraph. Sets the lens.]

## Strategic read (so what)

[The synthesis up front for executive readers: where they're stronger, where exposed, what we should do. Take a position.]

## Product architecture

[Reconstructed from public sources, each inference attributed.]

## Pricing and packaging

| Tier | Price | What's included | Gated behind |
|---|---|---|---|

[Plus narrative on packaging logic and changes over time.]

## ICP and target segments

[Who they say they target vs who the evidence shows they win.]

## Go-to-market motion

[PLG / sales-led / channel / community, read from the evidence.]

## Funding and financial position

[Rounds, valuation, revenue signals — all labelled estimate where not from a filing.]

## Key people

[Leadership and direction-signalling hires. Public professional context only.]

## Sources

| # | Source | Tier | Accessed | What it contributed |
|---|---|---|---|---|
| 1 | [Title](URL) | T1 / T2 / T3 / T4 / T5 | YYYY-MM-DD | — |
```

## Output

After writing the file, respond with a single line: the absolute path to the written report. The path must point to the
file you actually wrote with the Write tool — do not report a path without having written it.
