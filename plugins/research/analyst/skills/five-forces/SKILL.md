---
name: five-forces
description: "Run Porter's Five Forces (supplier power, buyer power, new entrants, substitutes, rivalry) to judge whether an industry or segment is structurally attractive to enter or stay in — and where the real pressure sits. Writes a conforming report (per report-conventions) to <engagement_dir>/five-forces/<slug>.md. This forces a JUDGMENT on attractiveness, not a filled-in five-box grid. Use for category-entry and segment decisions."
argument-hint: "<industry or segment, with the decision at stake> [engagement_dir]"
user-invocable: true
allowed-tools: WebSearch, WebFetch, Read, Write, Bash
---

Run [Porter's Five Forces](https://hbr.org/2008/01/the-five-competitive-forces-that-shape-strategy) (Michael Porter, HBR
1979, updated 2008) on the named industry or segment and write a conforming report. The framework models the structural
profitability of an industry — *why* airlines struggle and pharmaceuticals print money — rather than what any one company
should do. The point of this skill is the judgment, not the grid: a five-box template with every force rated "moderate"
is not analysis. You must conclude whether this industry is structurally attractive for the decision at hand, and name
where the pressure actually concentrates. It pairs with `/analyst:competitive-analysis` and `/analyst:market-sizing`.

## Step 0: Resolve arguments

Parse `$ARGUMENTS` as `<industry or segment> [engagement_dir]`. A trailing path-shaped token is the engagement directory;
otherwise default to `pwd`. Resolve to `$ENG`.

## Step 1: Name the decision

Five Forces is a tool for a decision — usually "should we enter / stay in / double down on this market?" State the
decision at the top. The same industry can be attractive for an incumbent and brutal for a new entrant; without the
decision framed, the forces have no reference point and you'll drift into a neutral description.

## Step 2: Compute the output path

Subject slug: kebab-case, lowercase, ASCII (per report-conventions).

Output path: `$ENG/five-forces/<slug>.md`. If the file exists, ask before overwriting.

Stage the file on disk NOW, before any analysis: create the directory and write the report's
frontmatter and the section headings from the Output Format below to that path with the Write tool.
Then fill in each section in place as you work through the steps. The report file is the
deliverable — it must exist on disk before you produce the analysis. Do not compose the report in
your chat reply and skip writing the file.

## Step 3: Assess each force from evidence

For each of the five forces, gather evidence and rate the *intensity* (low / moderate / high) AND say which direction it
points for profitability. A rating with no evidence is a guess.

- **Supplier power** — how much leverage do input providers have? Concentrated suppliers, switching costs, scarce inputs
  (talent, data, a platform you depend on) raise supplier power and squeeze margin.
- **Buyer power** — can buyers force prices down? Concentrated buyers, low switching costs, easy comparison, and
  price-transparency raise buyer power.
- **Threat of new entrants** — how defensible is the position? Low capital requirements, no network effects, weak brand
  moats, and easy access to distribution make entry easy and cap profitability.
- **Threat of substitutes** — what else solves the buyer's problem, including doing nothing or building in-house? Cheap,
  good-enough substitutes cap the price ceiling.
- **Competitive rivalry** — how intense is the head-to-head? Many similar players, slow growth, high fixed costs, and
  low differentiation drive margin-destroying rivalry.

For each, state the two or three pieces of evidence the rating rests on.

## Step 4: Find where the pressure actually concentrates

Don't stop at five independent ratings — that's the box-ticking failure. The forces interact and they are not equal.
Identify the **one or two forces that dominate** the structural picture for this decision. In most software markets, for
instance, the binding constraints are substitutes (build-in-house, adjacent tools) and rivalry, while supplier power is
minor. Name the dominant force(s) and explain why they outweigh the others. This is the core judgment.

## Step 5: Judge attractiveness and take a position

Conclude. Is this industry structurally attractive for the decision framed in Step 1 — yes, no, or conditional on a
specific move? "It depends" is only acceptable if you state precisely what it depends on. A reader should finish this
report knowing whether you'd enter and why, not holding a balanced grid with no verdict.

## Step 6: Note the framework's limits

Five Forces is static — a snapshot. Where the market has platform dynamics (buyers and suppliers are the same
population), fast evolution, or network effects the model handles poorly, say so and lean on `/analyst:wardley-map` for
the dynamic view. Honesty about the tool's edges strengthens the judgment.

## Step 7: Finalise

You MUST write the full report to the output path with the Write tool — this is the deliverable, not the chat reply. Do
not answer the analysis inline and skip the file. Tag every source with a tier. Set `status: Final`.

## Rules

- Frame the decision first. The same industry scores differently for an entrant and an incumbent — the forces need a reference point.
- Rate every force from evidence and state the evidence. An unsourced rating is a guess wearing a label.
- Never leave five equal ratings. Name the one or two dominant forces and why they outweigh the rest. That's the analysis; the grid is just the input.
- Take a position on attractiveness. "Moderate across the board" is a refusal to conclude. If it genuinely depends, state exactly what on.
- Name the framework's limits where platform dynamics or fast evolution break the static model. Defer the dynamic view to a Wardley map.
- One file per invocation. Don't write findings inline into chat.

## Output Format

Write a single conforming report to the output path with this structure:

```markdown
---
title: Five Forces — {INDUSTRY}
subtitle: {ENGAGEMENT}
date: {DATE}
author: five-forces
category: Commercial
subject: {INDUSTRY}
status: Draft
confidence: {0-4}
---

## The decision and the verdict

[The decision at stake (Step 1) and the answer: is this industry structurally attractive for it? Yes / no / conditional
on X. Take a position — this goes first, not last.]

## Where the pressure concentrates

[The one or two dominant forces and why they outweigh the others. The core judgment.]

## The five forces

| Force | Intensity | Direction for profitability | Key evidence |
|---|---|---|---|
| Supplier power | low/mod/high | | |
| Buyer power | low/mod/high | | |
| Threat of new entrants | low/mod/high | | |
| Threat of substitutes | low/mod/high | | |
| Competitive rivalry | low/mod/high | | |

[Narrative per force — two or three sentences each, not a restatement of the table.]

## Limits of this read

[Where the static model breaks for this market — platform dynamics, fast evolution, network effects. What to use instead.]

## Sources

| # | Source | Tier | Accessed | What it contributed |
|---|---|---|---|---|
| 1 | [Title](URL) | T1 / T2 / T3 / T4 / T5 | YYYY-MM-DD | — |
```

## Output

After writing the file, respond with a single line: the absolute path to the written report. The path must point to the
file you actually wrote with the Write tool — do not report a path without having written it.
