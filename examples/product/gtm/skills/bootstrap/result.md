# Bootstrap

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/gtm/CLAUDE.md` containing a user-authored section. The GTM bootstrap skill should preserve that user content while appending the template's missing sections (with a merge marker), and should create the file the fixture is missing — `docs/gtm/positioning-canvas.md`. The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

> The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/gtm/CLAUDE.md` is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.
> 
> Read the GTM bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/product/gtm/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.
> 
> After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## GTM Bootstrap Complete

### Files created
- `docs/gtm/positioning-canvas.md` — positioning canvas template

### Files merged
- `docs/gtm/CLAUDE.md` — appended missing sections (What This Domain Covers, Positioning methodology, Launch Tiers, Competitive Intelligence, Tooling, Available Skills, Conventions) while preserving user-authored "Custom team notes" section and sentinel line

### Next steps
- Complete positioning canvas using `/gtm:positioning`
- Create launch plans for upcoming releases using `/gtm:launch-plan`
- Set up competitor tracking in `docs/gtm/competitors/`

### Artifacts written

#### `work/docs/gtm/positioning-canvas.md`

```
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

#### `work/docs/gtm/CLAUDE.md`

```
# GTM Domain

This directory contains go-to-market documentation for the project.

## Custom team notes

USER-EDIT-SENTINEL-DO-NOT-STRIP

This section was written by the team and must survive any bootstrap re-run.
It exists to test the safe-merge contract: the bootstrap skill must not
overwrite or remove user-authored content.

<!-- Merged from gtm bootstrap v0.1.0 -->

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

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 8.5/8.5 (100%) |
| Evaluated | 2026-05-13 |
| Target duration | 36136 ms |
| Target cost | $0.1487 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | After bootstrap, `docs/gtm/CLAUDE.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim | PASS | Artifact `work/docs/gtm/CLAUDE.md` contains the exact line `USER-EDIT-SENTINEL-DO-NOT-STRIP` within the preserved 'Custom team notes' section. |
| c2 | After bootstrap, `docs/gtm/CLAUDE.md` contains the safe-merge marker `<!-- Merged from gtm bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged | PASS | Artifact `work/docs/gtm/CLAUDE.md` contains `<!-- Merged from gtm bootstrap v0.1.0 -->` immediately after the user-authored section. |
| c3 | After bootstrap, `docs/gtm/CLAUDE.md` contains the appended template sections — at minimum the "Positioning (April Dunford Methodology)" and "Launch Tiers" headings now appear alongside the preserved user content | PASS | Artifact contains `## Positioning (April Dunford Methodology)` and `## Launch Tiers` headings alongside the preserved user section. |
| c4 | After bootstrap, `docs/gtm/positioning-canvas.md` exists and was created from the skill's template | PASS | Artifact `work/docs/gtm/positioning-canvas.md` is present and contains a fully structured positioning canvas template based on April Dunford's methodology. |
| c5 | The created `positioning-canvas.md` contains the five positioning components (Competitive Alternatives, Unique Attributes, Value, Target Customer Segments, Market Category) as section headings | PASS | All five headings present: `## 1. Competitive Alternatives`, `## 2. Unique Attributes`, `## 3. Value for Customers`, `## 4. Target Customer Segments`, `## 5. Market Category`. |
| c6 | Chat output includes a manifest summary that distinguishes files created (`positioning-canvas.md`) from files merged (`CLAUDE.md`) | PASS | Chat output has explicit `### Files created` and `### Files merged` sections, listing `positioning-canvas.md` under created and `CLAUDE.md` under merged. |
| c7 | Output names each created and merged file individually — a bare "bootstrap complete" without the per-file manifest is not enough | PASS | Each file is individually named with a description: `docs/gtm/positioning-canvas.md — positioning canvas template` and `docs/gtm/CLAUDE.md — appended missing sections…`. |
| c8 | Output does not claim it overwrote or replaced `docs/gtm/CLAUDE.md` — the language reflects merge, not replacement | PASS | Chat says 'appended missing sections… while preserving user-authored "Custom team notes" section and sentinel line' — merge language throughout, no replacement claim. |
| c9 | Output points the reader at next steps (completing the positioning canvas, creating launch plans) consistent with the skill's documented manifest | PARTIAL | Next steps list: 'Complete positioning canvas using `/gtm:positioning`', 'Create launch plans using `/gtm:launch-plan`', 'Set up competitor tracking in `docs/gtm/competitors/`'. |

### Notes

The skill executed flawlessly across all dimensions: the safe-merge pattern preserved the sentinel and user content, the merge marker was correctly inserted, all template sections were appended, `positioning-canvas.md` was created with all five April Dunford components, and the manifest clearly separated created from merged files. c9 is capped at PARTIAL per test design.
