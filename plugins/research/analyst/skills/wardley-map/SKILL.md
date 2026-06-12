---
name: wardley-map
description: "Build a Wardley Map (Simon Wardley): plot the components of a value chain on visibility (user need at top) x evolution (genesis -> commodity) axes to expose where commoditisation is approaching, where competitors over/under-invest, and where build/buy/partner decisions sit. Writes a conforming report (per report-conventions) to <engagement_dir>/wardley-map/<slug>.md. Use for situational awareness and roadmap planning under uncertainty."
argument-hint: "<user need or capability to map> [engagement_dir]"
user-invocable: true
allowed-tools: WebSearch, WebFetch, Read, Write, Bash
---

Build a [Wardley Map](https://learnwardleymapping.com/) (Simon Wardley, ~2005) for the named user need and write a
conforming report. Wardley framed strategy as situational awareness: generals have maps of terrain, business strategists
usually don't. A Wardley Map plots a value chain on two axes so you can see where components are heading toward
commodity, where a competitor is over-investing in something that's become table stakes, and where your differentiation
is quietly eroding. It pairs with `/analyst:competitor-teardown` (whose value chain are you comparing against) and
`/analyst:strategy-canvas` (the value-factor view of the same competitive question).

## Step 0: Resolve arguments

Parse `$ARGUMENTS` as `<user need or capability> [engagement_dir]`. A trailing path-shaped token is the engagement
directory; otherwise default to `pwd`. Resolve to `$ENG`.

## Step 1: Compute the output path

Subject slug: kebab-case, lowercase, ASCII (per report-conventions).

Output path: `$ENG/wardley-map/<slug>.md`. If the file exists, ask before overwriting.

Stage the file on disk NOW, before any analysis: create the directory and write the report's
frontmatter and the section headings from the Output Format below to that path with the Write tool.
Then fill in each section in place as you work through the steps. The report file is the
deliverable — it must exist on disk before you produce the analysis. Do not compose the report in
your chat reply and skip writing the file.

## Step 2: Anchor on the user need

Start at the top of the map with the user and the need being served. Everything below exists to satisfy that need. Get
the need right — a map anchored on the wrong need (a feature you like, rather than the outcome the user wants) maps the
wrong terrain. State the user and the need in one sentence.

## Step 3: Build the value chain

Working down from the need, list the components required to deliver it — the capabilities, then the things those depend
on, down to underlying infrastructure. Each component sits on the **visibility** axis: high (close to the user, the need)
at the top, low (infrastructure the user never sees) at the bottom. Draw the dependency links — what needs what.

## Step 4: Place each component on the evolution axis

Position every component left-to-right by maturity:

- **Genesis** — novel, uncertain, custom one-off work, no agreed practice
- **Custom-built** — understood enough to build deliberately, still bespoke
- **Product / rental** — packaged, bought off-the-shelf, competing products exist
- **Commodity / utility** — standardised, undifferentiated, priced like a utility (electricity is the canonical example)

Evolution placement is the hard part and the whole value. Judge from market evidence: are there off-the-shelf products
for this? open-source equivalents? cloud services? The more substitutes and the more standardised, the further right.

## Step 5: Read the strategic signals

A placed map reveals three things — extract each:

- **Approaching commoditisation.** A component currently at product stage will drift toward commodity (cloud service,
  open-source equivalent, utility pricing). If your differentiation sits on a component heading right, your moat is
  eroding — map the trajectory and the timeline.
- **Competitor over/under-investment.** Where a competitor custom-builds something that's become a commodity elsewhere,
  they're spending engineering on table stakes — that's either inertia or a moat you don't understand yet. Determine which.
- **Build / buy / partner.** Genesis and custom-built components closest to the user need are where to invest and own;
  commodity components are where to buy or rent rather than build. Call the decision for each component that matters.

## Step 6: Movement and plays

Components evolve rightward over time. Note which components are moving, how fast, and what that implies for the roadmap —
especially the classic trap of building custom something a cloud provider is likely to commoditise within 18-24 months.
Where relevant, name a play (e.g. attacking a constraint in a competitor's chain rather than competing head-on).

## Step 7: Finalise

You MUST write the full report to the output path with the Write tool — this is the deliverable, not the chat reply. Do
not answer the analysis inline and skip the file. Take a position: given the map, where should investment go and what
should stop? A map that ends without a strategic call is just a diagram. Set `status: Final`.

## Rules

- Anchor on the user need, not a feature. A map on the wrong need maps the wrong terrain.
- Place evolution from market evidence (substitutes, open-source, cloud services), not from how novel it feels internally.
- Always extract the three signals: approaching commoditisation, competitor over/under-investment, build/buy/partner.
- Flag differentiation sitting on a commoditising component. That's the erosion warning the map exists to surface.
- End with an investment call. A map without a strategic position is a diagram, not analysis.
- One file per invocation. Don't write findings inline into chat.

## Output Format

Write a single conforming report to the output path with this structure:

```markdown
---
title: Wardley map — {USER NEED}
subtitle: {ENGAGEMENT}
date: {DATE}
author: wardley-map
category: Commercial
subject: {USER NEED}
status: Draft
confidence: {0-4}
---

## The strategic call

[Given the map: where should investment go, what should stop, where is the moat eroding. Take a position up front.]

## User and need

[One sentence: who the user is and the need the chain serves.]

## Value chain (components, visibility, evolution)

| Component | Depends on | Visibility | Evolution stage | Basis for evolution placement |
|---|---|---|---|---|

## Strategic signals

### Approaching commoditisation
[Components drifting toward commodity; any of our differentiation sitting on them; timeline.]

### Competitor over/under-investment
[Where a competitor custom-builds a commodity, or vice versa. Inertia or moat?]

### Build / buy / partner
[The call for each component that matters.]

## Movement and plays

[Which components are moving, how fast, the 18-24 month commoditisation trap, any play worth naming.]

## Sources

| # | Source | Tier | Accessed | What it contributed |
|---|---|---|---|---|
| 1 | [Title](URL) | T1 / T2 / T3 / T4 / T5 | YYYY-MM-DD | — |
```

## Output

After writing the file, respond with a single line: the absolute path to the written report. The path must point to the
file you actually wrote with the Write tool — do not report a path without having written it.
