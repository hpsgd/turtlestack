---
name: strategy-canvas
description: "Build a Blue Ocean strategy canvas (Kim & Mauborgne): plot your value curve against competitors across the factors the industry competes on, then drive an ERRC grid (Eliminate / Reduce / Raise / Create) off it. Writes a conforming report (per report-conventions) to <engagement_dir>/strategy-canvas/<slug>.md. Use to find where the industry has converged and where value innovation is possible."
argument-hint: "<market or category to map> [engagement_dir]"
user-invocable: true
allowed-tools: WebSearch, WebFetch, Read, Write, Bash
---

Build a [Blue Ocean Strategy](https://www.blueoceanstrategy.com/) strategy canvas (Kim & Mauborgne, 2005) for the named
market and write a conforming report. The canvas plots how every player performs across the factors the industry actually
competes on; when the value curves bunch together, the industry has converged and everyone is competing on
incrementalism. The follow-on ERRC grid structures how to break away. This skill pairs with `/analyst:competitive-analysis`
(for the competitor set) and `/analyst:review-mining` (for what buyers actually value — the input that keeps the ERRC
grid honest).

## Step 0: Resolve arguments

Parse `$ARGUMENTS` as `<market or category> [engagement_dir]`. A trailing path-shaped token is the engagement directory;
otherwise default to `pwd`. Resolve to `$ENG`.

## Step 1: Compute the output path

Subject slug: kebab-case, lowercase, ASCII (per report-conventions).

Output path: `$ENG/strategy-canvas/<slug>.md`. If the file exists, ask before overwriting.

Stage the file on disk NOW, before any analysis: create the directory and write the report's
frontmatter and the section headings from the Output Format below to that path with the Write tool.
Then fill in each section in place as you work through the steps. The report file is the
deliverable — it must exist on disk before you produce the analysis. Do not compose the report in
your chat reply and skip writing the file.

## Step 2: Identify the competing factors

List the factors the industry competes on — the things every player invests in and markets on. These go on the
horizontal axis. Examples in software: price, ease of onboarding, integration breadth, support responsiveness, specific
headline features. Derive these from what players actually advertise and what buyers actually weigh — not from your own
feature list. Aim for 6-12 factors; fewer hides the pattern, more turns the canvas into noise.

## Step 3: Identify the players

Pick yourself (or the subject product) plus three or four key competitors. If you don't have a competitor set,
cross-reference an existing `/analyst:competitive-analysis` report or run one first.

## Step 4: Score each value curve

For each player, score performance on each factor on a consistent scale (e.g. 1-5 or low/medium/high). Score from
evidence — pricing pages, feature matrices, review themes, analyst commentary — not impression. State the basis for each
score so the curve is defensible. Connecting one player's scores across all factors is its value curve.

## Step 5: Read the convergence

Compare the curves. The signal:

- **Bunched curves** → the industry has converged. Everyone competes on the same factors at similar levels — a red ocean
  of incrementalism. This is the most common and most important finding.
- **A diverging curve** → someone has already broken away. Study what they raised or created.

Name the pattern explicitly. The canvas exists to make convergence visible before sales data confirms the disruption.

## Step 6: Drive the ERRC grid

The Eliminate-Reduce-Raise-Create grid turns the canvas read into strategic choices:

- **Eliminate** — which factors the industry competes on can be dropped entirely? (Things every incumbent includes but no
  buyer actually values.)
- **Reduce** — which factors can go below industry standard? (Overinvested areas that add cost without proportionate buyer value.)
- **Raise** — which factors should go above industry standard? (Genuine points of differentiation.)
- **Create** — what should be introduced that the industry has never offered?

Eliminate and Reduce cut the cost structure; Raise and Create lift buyer value. Doing both at once is the value
innovation test — not differentiation alone, not cost leadership alone, but both.

## Step 7: Ground the grid in buyer evidence

The ERRC grid fails when it's a brainstorm. The inputs to Eliminate and Reduce must come from what buyers pay for but
don't value — pull that from review mining, win/loss, or interviews, not from the team's opinion about what's wasteful.
State the evidence behind each ERRC entry. Any entry with no buyer evidence is a wish; flag it as such or cut it.

## Step 8: Finalise

You MUST write the full report to the output path with the Write tool — this is the deliverable, not the chat reply. Do
not answer the analysis inline and skip the file. Take a position on whether a blue-ocean move is genuinely available here or whether the honest
read is "this is a red ocean and the play is to compete better". Not every market has a blue ocean — saying so is a valid
and useful conclusion. Set `status: Final`.

## Rules

- Derive factors from what the industry markets and what buyers weigh — not from your own feature list.
- Score from evidence and state the basis. An unsourced value curve is decoration.
- Name the convergence pattern explicitly. Bunched curves = red ocean; that's the headline, not a footnote.
- Ground every ERRC entry in buyer evidence. No evidence → it's a wish, not a strategy. Flag or cut it.
- Don't force a blue ocean. "This is a red ocean, compete on execution" is a legitimate conclusion — take the position.
- One file per invocation. Don't write findings inline into chat.

## Output Format

Write a single conforming report to the output path with this structure:

```markdown
---
title: Strategy canvas — {MARKET}
subtitle: {ENGAGEMENT}
date: {DATE}
author: strategy-canvas
category: Commercial
subject: {MARKET}
status: Draft
confidence: {0-4}
---

## The read

[The headline: has the industry converged? Is a value-innovation move available, or is the honest answer a red ocean?
Take a position.]

## Competing factors and value curves

| Factor | {Us} | {Competitor A} | {Competitor B} | {Competitor C} | Basis for scores |
|---|---|---|---|---|---|

[Narrative reading the curves: where they bunch, where any diverge.]

## ERRC grid

| Action | Factor | Buyer evidence |
|---|---|---|
| Eliminate | | |
| Reduce | | |
| Raise | | |
| Create | | |

## Value innovation test

[Do the Eliminate/Reduce actions cut cost AND the Raise/Create actions lift value? If only one side moves, it isn't value
innovation — say so.]

## Sources

| # | Source | Tier | Accessed | What it contributed |
|---|---|---|---|---|
| 1 | [Title](URL) | T1 / T2 / T3 / T4 / T5 | YYYY-MM-DD | — |
```

## Output

After writing the file, respond with a single line: the absolute path to the written report. The path must point to the
file you actually wrote with the Write tool — do not report a path without having written it.
