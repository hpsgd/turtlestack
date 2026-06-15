---
name: bootstrap
bootstrap-phase: market
description: "Bootstrap the go-to-market documentation structure for a project. Creates docs/gtm/, generates initial templates, and writes domain CLAUDE.md. Idempotent — merges missing sections into existing files without overwriting."
argument-hint: "[project name]"
user-invocable: false
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Bootstrap GTM Documentation

Bootstrap the go-to-market documentation structure for **$ARGUMENTS**.

## Process

### Step 1: Check and create domain directory

```bash
mkdir -p docs/gtm
```

### Step 2: Create or merge files

For each file below, apply the safe merge pattern:
- If file does not exist -> create from template
- If file exists -> read both, find sections in template missing from file, append missing sections with `<!-- Merged from gtm bootstrap v0.1.0 -->`

#### File 1: `docs/gtm/CLAUDE.md`

Create with this content (~80 lines):

```markdown
# GTM Domain

This directory contains go-to-market documentation: positioning, launch plans, competitive intelligence, and battle cards.

## What This Domain Covers

- **Positioning** — April Dunford methodology for product positioning
- **Launch planning** — tiered launch process and checklists
- **Competitive intelligence** — structured competitor analysis
- **Battle cards** — sales enablement for competitive situations

## Positioning (April Dunford Methodology)

Follow [April Dunford's positioning framework](https://www.aprildunford.com/obviously-awesome) from *Obviously Awesome*:

### Five positioning components

| Component | Question | Example |
|-----------|----------|---------|
| **Competitive alternatives** | What would customers use if we didn't exist? | Spreadsheets, manual process, competitor X |
| **Unique attributes** | What do we have that alternatives don't? | Real-time collaboration, AI-assisted |
| **Value** | What value do those attributes enable? | 50% faster reporting |
| **Target customers** | Who cares most about that value? | Mid-market SaaS finance teams |
| **Market category** | What market context makes our value obvious? | Collaborative FP&A platform |

### Positioning process

1. **Align** — get cross-functional team in a room (product, sales, marketing, CS)
2. **Audit** — list competitive alternatives honestly
3. **Isolate** — identify genuinely unique attributes
4. **Map** — connect attributes to customer value
5. **Target** — define best-fit customer segments
6. **Frame** — choose the market category that makes value obvious

## Launch Tiers

| Tier | Scope | Activities | Timeline |
|------|-------|-----------|----------|
| **Tier 1** — Major | New product, major pivot, new market | Full campaign: PR, content, events, sales enablement | 6–8 weeks prep |
| **Tier 2** — Significant | Major feature, new integration, pricing change | Blog, email, social, sales enablement | 3–4 weeks prep |
| **Tier 3** — Minor | Feature update, improvement, bug fix | Changelog, in-app notification, help docs | 1 week prep |

## Competitive Intelligence

### Competitor tracking

Maintain a competitor file per major competitor in `docs/gtm/competitors/`:
- **Overview** — what they do, target market, funding/size
- **Strengths** — where they beat us
- **Weaknesses** — where we beat them
- **Recent moves** — product launches, pricing changes, partnerships
- **Win/loss patterns** — when we win against them, when we lose

### Battle card format

Battle cards are 1-page sales enablement docs for competitive situations:
- **Quick positioning** — our one-liner vs. theirs
- **Key differentiators** — top 3 reasons to choose us
- **Landmines** — questions to ask that expose competitor weaknesses
- **Objection handling** — responses to common competitor-favourable objections
- **Proof points** — case studies, metrics, testimonials

## Tooling

| Tool | Purpose |
|------|---------|
| [GitHub Discussions](https://docs.github.com/en/discussions) | Positioning review and cross-functional alignment |
| [MS 365](https://www.microsoft.com/en-au/microsoft-365) | Marketing materials and stakeholder presentations |
| [Perplexity](https://perplexity.ai) | Competitive research and market analysis |

## Available Skills

| Skill | Purpose |
|-------|---------|
| `/gtm:positioning` | Develop product positioning |
| `/gtm:launch-plan` | Create a launch plan |
| `/gtm:competitive-analysis` | Conduct competitive analysis |
| `/gtm:write-battle-card` | Write a sales battle card |

## Conventions

- Positioning is reviewed quarterly and after major product changes
- Every launch has a tier assignment and corresponding checklist
- Competitive intelligence is updated monthly
- Battle cards are refreshed when competitors make significant changes
- All GTM materials reference the current positioning — no off-message content
```

#### File 2: `docs/gtm/positioning-canvas.md`

Create with this content:

```markdown
# Positioning Canvas — [Product/Feature Name]

> Based on April Dunford's *Obviously Awesome* methodology.

## Date

<!-- YYYY-MM-DD -->

## Participants

<!-- Cross-functional team: product, sales, marketing, CS -->

## 1. Competitive Alternatives

> What would customers do if our product didn't exist?

| Alternative | Type | Market Share |
|-------------|------|-------------|
| | Direct competitor / Indirect / Manual process | |

## 2. Unique Attributes

> What do we have that the alternatives lack?

| Attribute | Category | Evidence |
|-----------|----------|----------|
| | Feature / Technology / Service / Integration | |

## 3. Value for Customers

> What value do those unique attributes enable?

| Attribute | Value Enabled | Quantified Impact |
|-----------|--------------|-------------------|
| | | |

## 4. Target Customer Segments

> Who cares most about this value?

| Segment | Characteristics | Why They Care Most |
|---------|----------------|-------------------|
| | | |

## 5. Market Category

> What market context makes our value obvious?

**Chosen category:** [Category name]

**Why this category:**
<!-- Explain why this framing makes the value immediately clear -->

## Positioning Statement

> For [target customers] who [need/job-to-be-done], [product name] is a [market category] that [key value proposition]. Unlike [competitive alternatives], we [key differentiator].

## Validation Plan

| Test | Method | Success Criteria | Status |
|------|--------|-----------------|--------|
| Customer interviews | 5–10 target customers | > 80% resonate with positioning | |
| Sales pitch test | A/B test new vs old pitch | Improved win rate | |
| Website messaging | Update landing page | Improved conversion | |

> Review positioning quarterly. Re-run this canvas when market conditions change significantly.
```

### Step 3: Return manifest

After creating/merging all files, output a summary:

```
## GTM Bootstrap Complete

### Files created
- `docs/gtm/CLAUDE.md` — domain conventions and skill reference
- `docs/gtm/positioning-canvas.md` — positioning canvas template

### Files merged
- (list any existing files where sections were appended)

### Next steps
- Complete positioning canvas using `/gtm:positioning`
- Create launch plans for upcoming releases using `/gtm:launch-plan`
- Set up competitor tracking in `docs/gtm/competitors/`
```
