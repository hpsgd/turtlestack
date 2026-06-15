# Bootstrap

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/gtm/_sections/gtm.md` fragment containing a user-authored section. The GTM bootstrap skill should preserve that user content while appending the template's missing sections (with a merge marker), and should create the file the fixture is missing — `docs/gtm/positioning-canvas.md`. The GTM skill never writes `docs/gtm/CLAUDE.md` directly — the coordinator assembles it from the fragments in `_sections/`. The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

> The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/gtm/_sections/gtm.md` fragment is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.
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
- `docs/gtm/_sections/gtm.md` — appended 8 missing sections (What This Domain Covers, Positioning, Launch Tiers, Competitive Intelligence, Tooling, Available Skills, Conventions) while preserving user-authored "Custom team notes" section with `USER-EDIT-SENTINEL-DO-NOT-STRIP`

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

#### `work/docs/gtm/_sections/gtm.md`

```
<!-- gtm fragment of the gtm domain doc. Assembled into docs/gtm/CLAUDE.md by the coordinator. -->

## Custom team notes

USER-EDIT-SENTINEL-DO-NOT-STRIP

This section was written by the team and must survive any bootstrap re-run.
It exists to test the safe-merge contract: the bootstrap skill must not
overwrite or remove user-authored content.

<!-- Merged from gtm bootstrap v0.1.0 -->

<!-- domain-title: GTM -->
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
| Score | 10.5/10.5 (100%) |
| Evaluated | 2026-06-15 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 37643 ms |
| Target cost | $0.0827 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | After bootstrap, `docs/gtm/_sections/gtm.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim | PASS | Artifact shows '## Custom team notes\n\nUSER-EDIT-SENTINEL-DO-NOT-STRIP\n\nThis section was written by the team...' intact at the top of the merged file. |
| c2 | After bootstrap, `docs/gtm/_sections/gtm.md` contains the safe-merge marker `<!-- Merged from gtm bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged | PASS | Artifact contains the exact line '<!-- Merged from gtm bootstrap v0.1.0 -->' immediately before the appended template sections. |
| c3 | After bootstrap, `docs/gtm/_sections/gtm.md` contains the appended template sections — at minimum the "Positioning (April Dunford Methodology)" and "Launch Tiers" headings now appear alongside the preserved user content | PASS | Artifact shows '## Positioning (April Dunford Methodology)' and '## Launch Tiers' both present after the user-authored section and merge marker. |
| c4 | The gtm fragment is authored at H2 and below — it does not introduce a `# Gtm Domain` H1 (the coordinator generates that when it assembles `docs/gtm/CLAUDE.md`) | PASS | All headings in `_sections/gtm.md` are `##` or lower (e.g. '## Custom team notes', '## What This Domain Covers'). No `#` H1 present. |
| c5 | The skill does NOT write `docs/gtm/CLAUDE.md` directly — that file is the coordinator's to assemble from `_sections/` | PASS | Only two artifacts were written: `work/docs/gtm/positioning-canvas.md` and `work/docs/gtm/_sections/gtm.md`. No `docs/gtm/CLAUDE.md` artifact exists. |
| c6 | After bootstrap, `docs/gtm/positioning-canvas.md` exists and was created from the skill's template | PASS | Artifact `work/docs/gtm/positioning-canvas.md` is fully present with the April Dunford canvas template content. |
| c7 | The created `positioning-canvas.md` contains the five positioning components (Competitive Alternatives, Unique Attributes, Value, Target Customer Segments, Market Category) as section headings | PASS | Artifact shows '## 1. Competitive Alternatives', '## 2. Unique Attributes', '## 3. Value for Customers', '## 4. Target Customer Segments', '## 5. Market Category' — all five present. |
| c8 | Chat output includes a manifest summary that distinguishes files created (`positioning-canvas.md`) from files merged (`_sections/gtm.md`) | PASS | Chat output has separate '### Files created' and '### Files merged' sections, each listing the respective file. |
| c9 | Output names each created and merged file individually — a bare "bootstrap complete" without the per-file manifest is not enough | PASS | Output explicitly names '`docs/gtm/positioning-canvas.md`' under created and '`docs/gtm/_sections/gtm.md`' under merged with descriptions. |
| c10 | Output does not claim it overwrote or replaced `docs/gtm/_sections/gtm.md` — the language reflects merge, not replacement | PASS | Chat output says 'appended 8 missing sections... while preserving user-authored "Custom team notes" section' — clear merge language, no replacement claim. |
| c11 | Output points the reader at next steps (completing the positioning canvas, creating launch plans) consistent with the skill's documented manifest | PARTIAL | '### Next steps' lists 'Complete positioning canvas using `/gtm:positioning`' and 'Create launch plans for upcoming releases using `/gtm:launch-plan`' — both expected items present. |

### Notes

The skill executed flawlessly: sentinel preserved, merge marker applied, all template sections appended, no H1 introduced, CLAUDE.md not written, positioning canvas created with all five Dunford components, and manifest clearly distinguished created vs merged files. A perfect score within the rubric's ceiling constraints.
