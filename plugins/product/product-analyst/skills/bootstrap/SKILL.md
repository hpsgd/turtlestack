---
name: bootstrap
description: "Bootstrap the product analytics documentation structure for a project. Creates docs/analytics/, generates initial metric-tree and instrumentation templates, and writes domain CLAUDE.md. Idempotent — merges missing sections into existing files without overwriting."
argument-hint: "[project name]"
user-invocable: false
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Bootstrap Product Analytics Documentation

Bootstrap the product analytics documentation structure for **$ARGUMENTS**. This sets up the home for North Star definitions, metric trees, instrumentation specs, cohort analyses, and experiment designs produced by the other product-analyst skills.

## Step 1: Check and create domain directory

```bash
mkdir -p docs/analytics
```

## Step 2: Create or merge files

For each file below, apply the safe merge pattern:

- If the file does not exist → create from template
- If the file exists → read both, find sections in the template missing from the file, append the missing sections with `<!-- Merged from product-analyst bootstrap v0.1.0 -->`

Never overwrite existing content. Bootstrap is idempotent — running it twice changes nothing the second time.

### File 1: `docs/analytics/CLAUDE.md`

Create with this content:

```markdown
# Product Analytics Domain

This directory contains product analytics: the North Star Metric, the metric hierarchy,
instrumentation specs, cohort analyses, and experiment designs.

## What this domain covers

- **North Star Metric** — the single number capturing delivered customer value
- **Metric hierarchy** — input metrics that drive the North Star (HEART or AARRR)
- **Instrumentation specs** — events, properties, identity model, attribution (handed to data-engineer)
- **Cohort and retention analysis** — retention curves and segment cuts
- **Experiment design** — A/B and holdout tests with sample-size calculations

## Ownership boundary

The product-analyst defines *what* to measure and *why*. The data-engineer builds *how* data
flows (pipelines, warehouse, dashboards). Instrumentation specs are written here and handed off
for implementation. OKRs live with the product-manager; metrics here serve those OKRs.

## Metric definition standard

Every metric carries a definition block before implementation:

- **Question it answers** — the decision the number informs
- **Definition** — precise and unambiguous
- **Calculation** — exact formula or query logic
- **Granularity** — per user / session / account / cohort
- **Filters** — bots, test accounts, internal users (explicit)
- **Time window** — rolling 7d / calendar month / since signup
- **Goodhart risk** — how it could be gamed and who it would hurt
- **Owner** — who approves a definition change

## Conventions

- The North Star measures customer value, never company revenue directly
- Run the Goodhart check on every metric before promoting it
- Vanity metrics (cumulative totals) are never a North Star or an input
- Correlation is the default; causation requires an experiment
- Evidence hierarchy: observed behaviour > stated intent > opinion
- One file per artifact under `docs/analytics/`

## Available skills

| Skill | Purpose |
|-------|---------|
| `/product-analyst:define-north-star` | Define the North Star Metric and its input metrics |
| `/product-analyst:design-metric-hierarchy` | Build a HEART or AARRR metric tree tied to OKRs |
| `/product-analyst:write-instrumentation-spec` | Specify events for the data-engineer to implement |
| `/product-analyst:cohort-analysis` | Analyse retention curves and segment cuts |
| `/product-analyst:design-experiment` | Design an A/B or holdout experiment |
```

### File 2: `docs/analytics/metric-tree.md`

Create from the North Star canvas and metric-tree templates in the plugin's `templates/`
directory (`north-star-canvas.md`, `metric-tree.md`). Copy the template body, leaving the
placeholder rows for the team to fill via `/product-analyst:define-north-star`.

### File 3: `docs/analytics/instrumentation-spec.md`

Create from the plugin's `templates/instrumentation-spec.md`. This is the hand-off artifact to
the data-engineer; leave the event table empty for `/product-analyst:write-instrumentation-spec`
to populate.

## Step 3: Return manifest

After creating or merging all files, output a summary:

```markdown
## Product Analytics Bootstrap Complete

### Files created
- `docs/analytics/CLAUDE.md` — domain conventions and skill reference
- `docs/analytics/metric-tree.md` — North Star and metric-hierarchy template
- `docs/analytics/instrumentation-spec.md` — data-engineer hand-off template

### Files merged
- (list any existing files where sections were appended)

### Next steps
- Define the North Star with `/product-analyst:define-north-star`
- Build the metric hierarchy with `/product-analyst:design-metric-hierarchy`
- Write the instrumentation spec and hand it to the data-engineer
```

## Rules

- Always create `docs/analytics/`, never `docs/product-analytics/` or a variant — one canonical path
- Never overwrite an existing file. Merge missing sections only, tagged with the merge comment
- Do not invent metric values during bootstrap — templates ship with empty placeholder rows
- Don't duplicate OKR content here — OKRs live with the product-manager; link, don't copy

## Output Format

Return the manifest from Step 3 verbatim: files created, files merged, next steps. Nothing else.
