---
name: win-loss-analysis
description: "Analyse why deals were won or lost from the BUYER's perspective using third-party-style retrospective interviews. Surfaces the gap between sales-reported and buyer-reported loss reasons. Writes a conforming report (per report-conventions) to <engagement_dir>/win-loss-analysis/<slug>.md. Use after a batch of deals close, or when sales-reported loss reasons feel unreliable."
argument-hint: "<product or competitor the deals were against> [engagement_dir]"
user-invocable: true
allowed-tools: WebSearch, WebFetch, Read, Write, Bash
---

Run a win/loss analysis for the named product or competitor and write a conforming report. Win/loss examines why deals
closed the way they did from the buyer's point of view — not the sales rep's. The whole value of the method is that
buyers tell a neutral interviewer things they never tell the rep who just lost the deal. This skill produces the
interview protocol, the analysis, and the buyer-vs-rep gap that is the single most useful output. It pairs with
`/analyst:competitive-analysis` (who you lose to) and feeds `/analyst:write-market-landscape-report`.

## Step 0: Resolve arguments

Parse `$ARGUMENTS` as `<product or competitor> [engagement_dir]`. A trailing path-shaped token is the engagement
directory; otherwise default to `pwd`. Resolve to an absolute path stored as `$ENG`.

## Step 1: Compute the output path

Subject slug: kebab-case, lowercase, ASCII (per report-conventions). Use the competitor name if the analysis is
"why we lose to X", or the product name if it spans a deal batch.

Examples:

- `losses to Notion` → `notion`
- `Q3 mid-market deals` → `q3-mid-market-deals`

Output path: `$ENG/win-loss-analysis/<slug>.md`. If a file already exists, ask before overwriting (overwrite / write a
`-2` sibling / abort).

Stage the file on disk NOW, before any analysis: create the directory and write the report's
frontmatter and the section headings from the Output Format below to that path with the Write tool.
Then fill in each section in place as you work through the steps. The report file is the
deliverable — it must exist on disk before you produce the analysis. Do not compose the report in
your chat reply and skip writing the file.

## Step 2: Scope the deal set

Define which deals are in scope before interviewing anyone. State explicitly:

- **Window:** which closed deals, over what period. Interview buyers 7-14 days post-close — not later. After ~30 days
  buyers rationalise the outcome to fit the decision they made (post-purchase cognitive consistency), and the evaluation
  they actually ran gets overwritten by the story they now tell themselves.
- **Segment:** all deals, or filtered by size / region / competitor. Mixing enterprise and SMB losses averages away the
  signal — keep segments separable.
- **Win/loss mix:** include wins, not just losses. Wins tell you what your real differentiation is; a losses-only study
  produces a fix-list with no sense of what to protect.

## Step 3: Reconstruct the sales-reported reasons first

Before going to buyers, record what the *sales team* believes happened for each deal — from CRM close-reason fields,
sales debrief notes, or the public deal narrative. This is the baseline you will compare against. Reps report the full
story of why they lost roughly 40% of the time; the rest is incomplete or self-serving. Capturing the rep view first
makes the gap measurable instead of anecdotal.

## Step 4: Build the interview protocol

A good win/loss interview walks the decision **chronologically**, not thematically. Use a neutral-party framing — the
candour drops the moment the buyer thinks they're talking to someone with a stake in the outcome. Cover, in order:

1. **Trigger** — what happened that started the evaluation? (a pain, a mandate, a contract renewal)
2. **Timeline** — walk the process date by date, not "what mattered most". Let the sequence surface the real drivers.
3. **Alternatives** — who else was in the process, and *when* each was eliminated. Not just who won.
4. **Stakeholders** — whose opinion actually drove the decision? Finance, security, the end user, procurement?
5. **The counterfactual** — what would have changed the outcome? This is where product and sales gaps fall out.
6. **Laddering** — follow each answer down five to seven levels of "why". The first answer ("price") is almost never the
   real reason ("we didn't trust the migration path, so the price felt unjustified"). Laddering is what separates win/loss
   from a satisfaction survey. See the [laddering technique](https://en.wikipedia.org/wiki/Laddering) (means-end interviewing).

If live interviews aren't possible, reconstruct the buyer view from public signals: the buyer's own post-decision posts,
review-site entries (cross-reference `/analyst:review-mining`), case studies the winner published, and any procurement
records. Label reconstructed findings as inference, not interview data.

## Step 5: Extract patterns

Across the deal set, identify recurring patterns rather than one-off anecdotes. Look for:

- Product gaps that appear repeatedly in losses to one specific competitor
- Sales-execution issues (weak discovery, wrong champion, slow follow-up) misattributed to product
- Value-justification gaps — not "too expensive" but "the value didn't clear the price"
- Hidden decision-makers (security, legal, procurement) who vetoed deals the business sponsor wanted

A pattern needs at least two independent deals. A single deal is a story, not a finding.

## Step 6: Surface the buyer-vs-rep gap

This is the headline output. For each loss reason, put the sales-reported reason next to the buyer-reported reason. When
they diverge **systematically** — reps say "price", buyers say "we never understood the differentiation" — that's a
messaging or sales-process problem wearing a product-problem costume. Name it as such. Don't bury this in the body; it
goes near the top.

## Step 7: Finalise

You MUST write the full report to the output path with the Write tool — this is the deliverable, not the chat reply. Do
not answer the analysis inline and skip the file. Tag every source with a tier per source-quality. Set `status: Final`. Take a
position in the recommendations — this skill exists to change what the team does next, not to catalogue deals.

## Rules

- Interview within 14 days of close. State the actual window used; if any interview is later, flag the rationalisation risk.
- Always capture the sales-reported reason before the buyer-reported one. The gap is the product. Without the baseline, you can't measure it.
- Never let the rep who owned the deal frame the buyer's reasons. Don't repeat the CRM close-reason as fact — treat it as a claim to test.
- Don't ladder once and stop. The first answer is the surface. Push to five-plus levels of "why".
- Include wins. A losses-only study tells you what to fix and nothing about what to protect.
- A finding needs two or more deals. Label single-deal observations as anecdote, not pattern.
- One file per invocation. Don't write findings inline into chat.

## Output Format

Write a single conforming report to the output path with this structure:

```markdown
---
title: Win/loss analysis — {SUBJECT}
subtitle: {ENGAGEMENT}
date: {DATE}
author: win-loss-analysis
category: Commercial
subject: {SUBJECT}
status: Draft
confidence: {0-4}
---

## Headline — the buyer-vs-rep gap

[The single most important finding: where sales-reported and buyer-reported reasons diverge systematically, and what that
means. One or two paragraphs. Take a position.]

## Deal set in scope

[Window (with the 7-14 day post-close note), segment filters, win/loss mix, number of deals, number of interviews or
reconstructed buyer views.]

## Reasons: sales-reported vs buyer-reported

| Deal / segment | Sales-reported reason | Buyer-reported reason | Gap |
|---|---|---|---|

## Patterns

### Product gaps
[Recurring gaps, with the deals they appeared in.]

### Sales-execution issues
[Execution problems misattributed to product.]

### Value-justification gaps
[Where price perception was really a value-communication failure.]

### Decision-maker dynamics
[Hidden vetoes — security, legal, procurement.]

## What would have changed the outcome

[The counterfactuals, ranked by how often they recurred.]

## Recommendations

[Specific, owned actions. Separate "fix the product" from "fix the messaging" from "fix the sales process" — the gap
analysis above tells you which bucket each belongs in.]

## Sources

| # | Source | Tier | Accessed | What it contributed |
|---|---|---|---|---|
| 1 | [Title](URL) | T1 / T2 / T3 / T4 / T5 | YYYY-MM-DD | — |
```

## Output

After writing the file, respond with a single line: the absolute path to the written report. The path must point to the
file you actually wrote with the Write tool — do not report a path without having written it.
