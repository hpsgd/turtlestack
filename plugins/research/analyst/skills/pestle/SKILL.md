---
name: pestle
description: "Run a PESTLE macro-environmental scan (political, economic, social, technological, legal, environmental) for a market or expansion decision — then argue which forces actually matter and what they imply. Writes a conforming report (per report-conventions) to <engagement_dir>/pestle/<slug>.md. This prioritises and takes a position; it is NOT a six-box checklist where everything is 'moderate impact'. Use for category strategy, regulated-industry launches, and international expansion."
argument-hint: "<market or expansion decision, with geography> [engagement_dir]"
user-invocable: true
allowed-tools: WebSearch, WebFetch, Read, Write, Bash
---

Run a [PESTLE](https://en.wikipedia.org/wiki/PEST_analysis) macro-environmental scan (Political, Economic, Social,
Technological, Legal, Environmental) for the named market or decision and write a conforming report. PESTLE exists to
prevent tunnel vision — teams fixated on competitive dynamics miss the regulatory shift or demographic change that
invalidates their assumptions. But its standard failure mode is a 40-factor list where everything is rated "moderate to
high impact", which is not analysis. The discipline, and the whole point of this skill, is to identify the two or three
factors with material effect on *this specific decision*, weight them, and say what they imply. It pairs with
`/analyst:five-forces` (industry structure) and `/analyst:write-market-landscape-report` (which consumes the trend read).

## Step 0: Resolve arguments

Parse `$ARGUMENTS` as `<market or decision> [engagement_dir]`. A trailing path-shaped token is the engagement directory;
otherwise default to `pwd`. Resolve to `$ENG`.

## Step 1: Frame the decision and geography

PESTLE is only meaningful against a specific decision in a specific place. "Launching a healthcare product in Australia"
scans different forces than "expanding a consumer app into Southeast Asia". State the decision and the geography. A scan
with no decision produces an encyclopaedia entry, not analysis.

## Step 2: Compute the output path

Subject slug: kebab-case, lowercase, ASCII (per report-conventions).

Output path: `$ENG/pestle/<slug>.md`. If the file exists, ask before overwriting.

Stage the file on disk NOW, before any analysis: create the directory and write the report's
frontmatter and the section headings from the Output Format below to that path with the Write tool.
Then fill in each section in place as you work through the steps. The report file is the
deliverable — it must exist on disk before you produce the analysis. Do not compose the report in
your chat reply and skip writing the file.

## Step 3: Scan each dimension for candidate factors

Gather candidate factors across the six dimensions from credible sources (government data, regulators, industry analysts):

- **Political** — government stability, policy direction, trade posture, public-sector procurement rules
- **Economic** — growth, inflation, interest rates, currency, employment, sector-specific cycles
- **Social** — demographics, attitudes, behaviour shifts, workforce expectations
- **Technological** — platform shifts, infrastructure maturity, adjacent-tech disruption, automation
- **Legal** — regulation specific to the product (privacy, licensing, consumer law, sector compliance), pending changes
- **Environmental** — sustainability requirements, climate exposure, ESG reporting obligations

Cast wide here, but this is collection — not the output. Don't ship the raw list.

## Step 4: Filter to what's material — the discipline

This is where the skill earns its keep. From the candidate factors, select the **two or three** with material effect on
the decision framed in Step 1. For each kept factor, judge:

- **Direction** — tailwind or headwind for the decision
- **Magnitude** — how much it actually moves the outcome (not a flat "moderate")
- **Time horizon** — already biting, or a 12-24 month risk

Explicitly discard the factors that don't matter, and say why. "Environmental factors are low-material for this SaaS
launch — noted and set aside" is a stronger move than rating them "moderate" to fill the box. A PESTLE that keeps all six
dimensions at equal weight has not been analysed.

## Step 5: Draw the implications and take a position

For each material factor, state what it *implies for the decision* — not just that it exists. "New privacy regulation
takes effect next year" is an observation; "the privacy regime makes a local data-residency commitment a condition of
entry, which adds cost X and rules out the lightweight launch" is analysis. Conclude with the net read: does the
macro-environment support, complicate, or block the decision, and what's the one thing to act on first?

## Step 6: Finalise

You MUST write the full report to the output path with the Write tool — this is the deliverable, not the chat reply. Do
not answer the analysis inline and skip the file. Tag every source with a tier (regulatory/government sources are T1 per source-quality — prefer
them for Legal and Political factors). Set `status: Final`.

## Rules

- Frame the decision and geography first. A scan with no decision is an encyclopaedia entry.
- Scan wide, ship narrow. Collect across six dimensions; output only the two or three material factors.
- Never rate everything "moderate". Equal weight across all six dimensions means the analysis didn't happen. Discard the immaterial factors explicitly and say why.
- Give each kept factor direction, magnitude, and time horizon — not a single impact label.
- State implications, not observations. "X is happening" is collection; "X means we must do Y, at cost Z" is analysis.
- Prefer T1 government/regulator sources for Legal and Political factors.
- One file per invocation. Don't write findings inline into chat.

## Output Format

Write a single conforming report to the output path with this structure:

```markdown
---
title: PESTLE scan — {MARKET}
subtitle: {ENGAGEMENT}
date: {DATE}
author: pestle
category: Commercial
subject: {MARKET}
status: Draft
confidence: {0-4}
---

## Decision, geography, and net read

[The decision and place (Step 1) and the conclusion: does the macro-environment support, complicate, or block it? The
one thing to act on first. Take a position up front.]

## What matters (the material factors)

| Factor | Dimension | Direction | Magnitude | Horizon | Implication for the decision |
|---|---|---|---|---|---|

[Narrative on each material factor — what it is, the evidence, and what it forces.]

## Scanned and set aside

[The dimensions/factors judged immaterial for this decision, each with a one-line reason. This is evidence the scan was
done, not skipped — and it's why the kept factors earned their place.]

## Sources

| # | Source | Tier | Accessed | What it contributed |
|---|---|---|---|---|
| 1 | [Title](URL) | T1 / T2 / T3 / T4 / T5 | YYYY-MM-DD | — |
```

## Output

After writing the file, respond with a single line: the absolute path to the written report. The path must point to the
file you actually wrote with the Write tool — do not report a path without having written it.
