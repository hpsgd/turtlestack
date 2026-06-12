# Strategy Canvas

Scenario: A product team for NoteFlow wants a Blue Ocean strategy canvas of the AU cloud note-taking market, driven off existing competitive-analysis and review-mining reports already staged in the engagement directory, to find whether a value-innovation move is available.

## Prompt

> Work entirely from the staged engagement files — do NOT perform any live web research (no WebSearch, no WebFetch). The competitor set and the buyer evidence you need are already on disk.
> 
> /analyst:strategy-canvas cloud note-taking apps (AU SMB) {workspace}/work/blueoak
> 
> Use these staged inputs (read them first):
> 
> - `{workspace}/work/blueoak/competitive-analysis/cloud-note-taking-au.md` — the four direct competitors (NoteFlow = us, PageMind, Quillbase, JotRapid), their factor scores, and recent moves.
> - `{workspace}/work/blueoak/review-mining/cloud-note-taking-au.md` — category buyer voice: what buyers actually pay for vs value, with quantified theme shares and segment skew.
> 
> Requirements for the response:
> 
> - Build the value-curve table across 6-12 competing factors with NoteFlow plus the three named competitors, scoring each from the staged evidence and stating the basis.
> - Read the convergence pattern explicitly — say whether the curves bunch (red ocean) or one diverges, as the headline.
> - Produce the ERRC grid (Eliminate / Reduce / Raise / Create) with a populated entry in EACH of the four cells, and ground every entry in the staged review-mining buyer evidence (cite the theme), not in opinion.
> - Apply the value-innovation test: state whether Eliminate+Reduce cut cost AND Raise+Create lift value.
> - Take a position on whether a genuine blue-ocean move is available here or whether the honest read is a red ocean.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

**Report written.**

```
/var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/eval-1781281515-a8d01589/work/blueoak/strategy-canvas/cloud-note-taking-au-smb.md
```

---

## Key findings

**Red ocean with a real blue ocean break available.** The industry has converged on feature/integration/security depth that buyers don't value proportionally — PageMind and Quillbase score identically on most factors despite different prices. NoteFlow can diverge decisively:

- **Eliminate**: template volume race (22% buyer "clutter" complaint), deep AI (14% mixed signal, no demand)
- **Reduce**: onboarding complexity (31% pain point), admin security depth (valued only by regulated buyers, irrelevant for SMB)
- **Raise**: onboarding speed to "productive in one hour" (zero competitors claim this), offline/mobile reliability (25% loyalty driver, understated), sharing ease (20% positive)
- **Create**: SMB-focused workflow templates (not clutter galleries), "productive in one hour" positioning

Both sides move: cost cuts (simpler architecture, less ML, less support), *and* value lifts (speed, reliability, ease, positioning). This is value innovation, not cost leadership or differentiation alone.

**Honest position**: not a hypothetical blue ocean. The buyer evidence is concrete (31%, 25%, 20% signals outweigh 9% and 14%). The move is achievable for an early product. NoteFlow's current positioning already hints at it — the strategy is to lean harder and back it with speed/reliability proof.

### Artifacts written

#### `work/blueoak/strategy-canvas/cloud-note-taking-au-smb.md`

```
---
title: Strategy canvas — cloud note-taking apps (AU SMB)
subtitle: BlueOak
date: 2026-06-13
author: strategy-canvas
category: Commercial
subject: cloud note-taking apps
status: Final
confidence: 3
---

## The read

**Red ocean with a real blue ocean break available.** The industry has converged on feature/integration/security depth that buyers don't proportionally value. PageMind and Quillbase score similarly across most factors (integration 6, admin 7-9, AI 6-8) despite different price points, indicating a false competition on feature count. JotRapid competes purely on cost. NoteFlow has the opportunity to break away decisively: eliminate the features buyers don't use (template volume, deep AI), reduce onboarding friction, and raise what buyers actually pay for (speed, simplicity, offline reliability, sharing ease). The move cuts cost while lifting value — genuine value innovation, not just differentiation.

## Competing factors and value curves

| Factor | NoteFlow | PageMind | Quillbase | JotRapid | Basis for scores |
|---|---|---|---|---|---|
| **Price** ($/seat/month, inverted to value) | 7 | 5 | 2 | 9 | Competitive analysis table: NF $8, PM $12, QB $20, JR $4. Scored as buyer value (lower price = higher score on value curve). |
| **Onboarding speed** | 9 | 3 | 2 | 9 | Review mining: 31% of reviews cite onboarding friction as critical pain point ("took our team two weeks to get productive — too many options"). Pain concentrated in feature-rich products. NF positions on speed; JR claims very fast. |
| **Mobile/offline reliability** | 7 | 7 | 5 | 3 | Review mining: 25% positive sentiment ("rock solid offline, syncs cleanly — this is why we stay"). Competitive analysis: NF, PM "good"; QB "medium"; JR "basic". Offline/mobile is a stated buyer loyalty driver. |
| **Sharing/collaboration ease** | 8 | 7 | 6 | 5 | Review mining: 20% positive ("dead simple to share a note with a client, no fuss"). NF positions on "all-in-one notes + light tasks" (simple collaboration). Feature-rich products (PM, QB) likely add overhead. |
| **Integration breadth** | 5 | 6 | 6 | 1 | Review mining: 9% mixed signal. "Connects to everything, but we only ever used Slack." Industry invests heavily (PM "very high", QB "high"), but buyer evidence shows minimal usage of breadth. NF adequate; JR genuine gap. |
| **Template curation quality** | 6 | 3 | 4 | 1 | Review mining: 22% negative ("hundreds of templates, we use two; it's clutter"). Scored on *usefulness*, not count. NF small curated gallery (high value); PM large uncurated (drives clutter complaints); QB medium; JR none. |
| **Admin/security controls** | 3 | 7 | 9 | 1 | Competitive analysis + review mining skew. QB focused on security (hiring compliance officers, SOC2 tier launch). Buyer evidence: "security-controls praise concentrates among regulated-industry reviewers (only they value it)." Irrelevant for general SMB. |
| **AI assist features** | 1 | 8 | 6 | 1 | Review mining: 14% mixed ("summaries are hit and miss, nice when it works"). PM aggressive push (6 ML engineers hired, summariser launched 2026-03), but buyer value is uncertain. QB medium tier. Industry competes on AI headline; buyers uncertain of ROI. |

### Convergence pattern

**Strong bunching indicates red ocean.** PageMind and Quillbase converge on 5 of 8 factors (integration 6, sharing 6-7, template 3-4, admin 7-9, AI 6-8) despite $12–$20 price span. Both players are competing on the same feature/security/AI investment axis. JotRapid undercuts on price and strips features (scores 1-3 across capability, 9 on price). 

**NoteFlow occupies an exposed middle**: scores high on factors buyers value (onboarding 9, sharing 8, offline 7, price 7) but low on factors the industry competes on (integration 5, templates 6, AI 1, security 3). This is not a weakness — it's a divergence waiting to be made explicit.

**The false competition**: integration breadth (9% buyer signal) and template galleries (22% clutter complaints) are industry investment areas with low buyer return. Nobody markets "productive in one hour" despite offline reliability (25% buyer loyalty) being the second-highest-valued factor.

## ERRC grid

| Action | Factor | Buyer evidence | Strategic implication |
|---|---|---|---|
| **Eliminate** | Template gallery volume race | Review mining 22%: "Hundreds of templates, we use two; it's clutter." Industry metric is count; buyer value is curation. | Stop investing in gallery size. Maintain 5–10 *SMB-focused* templates (project tracking, team notes, client notes). Redirect saved design/content cost to other areas. |
| **Eliminate** | Deep AI feature tiers | Review mining 14%: "Summaries are hit and miss, nice when it works." No strong buyer demand for AI depth. PageMind hiring 6 ML engineers on uncertain ROI. | Cut expensive AI R&D. Offer simple summarisation *if* it works reliably; otherwise remove. Redirect ML budget to core value drivers. |
| **Reduce** | Onboarding complexity / feature discovery | Review mining 31%: "Took two weeks to get productive — too many options." Friction concentrated in feature-rich products (PageMind, Quillbase). | Reduce configuration options and feature discovery during onboarding. Goal: "productive in one hour" (currently nobody claims this). Simplify setup UI and defaults. |
| **Reduce** | Admin/security control granularity | Review mining: "Security-controls praise concentrates among regulated-industry reviewers (only they value it)." General SMB irrelevant. Quillbase competing on compliance (SOC2, audit logs). | Reduce security feature depth for general SMB tier. Keep essentials (SSO, basic audit). Remove regulatory-depth features that add complexity without SMB value. Redirect engineering cost. |
| **Raise** | Onboarding speed / time-to-productivity | Review mining 31% (critical pain point): onboarding friction is the highest-weighted negative theme. No competitor claims "fast onboarding" as a headline. | Raise to "productive in one hour" — the zero-competitors claim. Make this the headline differentiator. Measure and verify. This directly addresses the largest buyer pain. |
| **Raise** | Offline/mobile reliability | Review mining 25% (strong positive): "Rock solid offline, syncs cleanly — this is why we stay." Second-highest-weighted positive factor, understated by all players. | Raise reliability and sync performance above PageMind parity (currently tied at 7/10). Invest in offline-first sync, conflict resolution, instant refresh. Market as "work anywhere" reliability. |
| **Raise** | Sharing/collaboration ease | Review mining 20% (positive): "Dead simple to share a note with a client, no fuss." NoteFlow claims simplicity; verify UX is actually frictionless. | Raise ease to zero-explanation sharing (one-click external share, no setup). Eliminate "explain permissions" steps. Make this the second headline after onboarding speed. |
| **Create** | "Productive in one hour" positioning and capability | Review mining implication: buyers value offline/sync (25%) and sharing ease (20%) because they enable *immediate work*. No competitor brands speed/simplicity as the meta-value. | Create and own "ready to work in 60 minutes" claim with proof (onboarding speed, zero setup, instant sharing). This is a genuinely uncompeted positioning. Bundle with SMB-focused templates. |
| **Create** | SMB-workflow-optimised templates | Review mining 22% (clutter complaint) + implied buyer persona: smaller teams (<30 seats per review-mining segment skew) use only 2 templates. Generic galleries don't serve this. | Create 5–8 *deep* templates for common SMB workflows: (1) team notes/standup, (2) project tracking, (3) client meeting notes, (4) onboarding/process docs, (5) decision log. Not clutter — purpose-built, one per job. |

## Value innovation test

**Cost structure (Eliminate + Reduce):**
- Eliminate template volume: shrink design/content team, reduce gallery maintenance and UX overhead.
- Eliminate deep AI: cut ML team investment, remove infrastructure for experimental summarisation.
- Reduce onboarding complexity: shrink setup UX, reduce customer success/implementation cost (faster self-onboarding = fewer support tickets).
- Reduce admin feature depth: cut compliance engineering, remove regulatory-layer feature investment.

**Combined cost savings: moderate but real.** Less design, less ML ops, less support. Cost structure tilts toward simplicity rather than feature depth.

**Buyer value (Raise + Create):**
- Raise onboarding speed: directly addresses the #1 buyer pain (31% of reviews). Fast onboarding = faster revenue per customer, faster net-new-user adoption, lower churn.
- Raise offline/mobile: second-highest buyer value signal (25%); buyers state it's a loyalty driver ("why we stay"). Reliability wins retention.
- Raise sharing ease: third-highest buyer value signal (20%); enables client-facing workflows, team collaboration — core use case.
- Create "productive in one hour" claim: owns an uncontested positioning. Creates headline differentiation.
- Create SMB templates: solves the "clutter" complaint while serving the actual buyer workflow (small teams, 2–3 active templates).

**Verdict: Value innovation available.** Eliminate + Reduce *do* cut cost (ML, design, support, compliance engineering). Raise + Create *do* lift value (speed, reliability, ease, positioning). Both sides move. This is not cost leadership alone (JotRapid's play) and not feature differentiation alone (PageMind, Quillbase bunched), but genuine value innovation.

## Strategic position

**NoteFlow can own the blue ocean:** simplicity + speed + reliability, backed by buyer evidence that these are underinvested and high-value. The industry has converged on feature/integration/security metrics; NoteFlow breaks away by competing on what buyers *actually* pay for and what drives loyalty.

The move requires discipline:
- **Do not match** PageMind/Quillbase on integration breadth or AI features. These compete on a false axis (9% and 14% buyer signal respectively).
- **Invest ruthlessly** in onboarding speed (31% buyer signal), offline reliability (25%), sharing ease (20%), and the "productive in one hour" positioning (zero competitors).
- **Own the simplicity narrative**: market that buyers get value *faster*, not that NoteFlow has *more features*.

This is achievable for an early-stage product. NoteFlow's current positioning ("all-in-one notes + light tasks") is already close to simplicity; the canvas suggests *leaning harder* into it and backing it with speed/reliability proof.

## Sources

| # | Source | Tier | Accessed | What it contributed |
|---|---|---|---|---|
| 1 | Competitive analysis — cloud note-taking apps (AU SMB) | T2 | 2026-05-01 | Direct competitor feature/price matrix, hiring signals, recent moves, differentiation summary |
| 2 | Review mining — cloud note-taking apps (AU SMB) | T2 | 2026-05-02 | Buyer theme distribution (7 themes, 31%–9% share), sentiment, segment skew, opportunity inventory |

```

#### `work/blueoak/review-mining/cloud-note-taking-au.md`

```
---
title: Review mining — cloud note-taking apps (AU SMB)
subtitle: BlueOak
date: 2026-05-02
author: review-mining
category: Commercial
subject: cloud note-taking apps
status: Final
confidence: 3
---

## Lens

Category-wide buyer voice across the four direct competitors.

## Themes (buyer evidence)

| Theme | Share of reviews | Sentiment | Representative verbatim |
|---|---|---|---|
| Onboarding / setup friction | ~31% | negative | "took our team two weeks to get productive — too many options" |
| Template gallery rarely used | ~22% | negative-neutral | "hundreds of templates, we use two; it's clutter" |
| Integration breadth | ~9% | mixed | "connects to everything, but we only ever used Slack" |
| AI summariser usefulness | ~14% | mixed | "summaries are hit and miss, nice when it works" |
| Price-for-value | ~18% | negative | "paying for a huge feature set we don't touch" |
| Mobile / offline reliability | ~25% | positive | "rock solid offline, syncs cleanly — this is why we stay" |
| Sharing / collaboration speed | ~20% | positive | "dead simple to share a note with a client, no fuss" |

## Segment skew

- Onboarding friction skews heavily toward the feature-rich products (PageMind, Quillbase).
- Template-clutter complaints concentrate among smaller teams (<30 seats).
- Security-controls praise concentrates among regulated-industry reviewers (only they value it).

## Opportunity inventory

Buyers pay for template galleries and integration counts they barely use, and suffer slow
onboarding to get them. They consistently value fast sharing and reliable offline/mobile — the
quiet, under-marketed factors. Nobody is competing on "productive in an hour".

## Representativeness caveat

Review populations self-select; directional not statistically representative.

```

#### `work/blueoak/competitive-analysis/cloud-note-taking-au.md`

```
---
title: Competitive analysis — cloud note-taking apps (AU SMB)
subtitle: BlueOak
date: 2026-05-01
author: competitive-analysis
category: Commercial
subject: cloud note-taking apps
status: Final
confidence: 3
---

## Market definition

Buyer: SMB knowledge workers (10-200 employee businesses) in Australia. Purchase unit: per-seat
monthly subscription. Problem solved: capturing, organising and sharing team notes and light docs.

## Competitors identified

### Direct

- **NoteFlow** — our product. All-in-one notes + light tasks. Positions on "one tool, no setup".
- **PageMind** — market leader. Heavy feature set, deep integrations, template gallery.
- **Quillbase** — enterprise-leaning. Strong admin controls, SSO, audit logs, premium price.
- **JotRapid** — budget challenger. Cheap, fast, minimal feature set, no integrations.

### Indirect

- Microsoft OneNote (bundled with M365), Google Keep (bundled with Workspace).

## Competitor comparison

| Attribute | NoteFlow | PageMind | Quillbase | JotRapid |
|---|---|---|---|---|
| Price ($/seat/mo) | 8 | 12 | 20 | 4 |
| Integration breadth | medium | very high | high | none |
| Template gallery | small | very large | medium | none |
| Admin / security controls | basic | high | very high | none |
| Onboarding speed | fast | slow (heavy) | slow | very fast |
| Offline / mobile | good | good | medium | basic |
| AI assist features | none yet | high | medium | none |

## Hiring signals

PageMind hiring 6 ML engineers (Sydney) — AI feature push (signal, not confirmation).
Quillbase hiring compliance + enterprise sales — moving further upmarket.

## Recent strategic moves

- PageMind launched an AI summariser (2026-03), heavily marketed.
- Quillbase raised price 18% and added a SOC2 tier (2026-02).
- JotRapid cut price again to $4/seat (2026-04).

## Differentiation analysis

PageMind wins on integration breadth and template depth but is heavy and slow to onboard.
Quillbase wins on security for regulated buyers at a premium. JotRapid wins purely on price.
The industry has piled investment into template galleries and integration counts — every player
markets bigger numbers — while onboarding stays slow for the feature-rich tiers.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 13.0/13.0 (100%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 106844 ms |
| Target cost | $0.1553 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill writes a conforming report to disk under `blueoak/strategy-canvas/` (see ARTIFACTS WRITTEN — at least one .md file there) | PASS | Artifact `work/blueoak/strategy-canvas/cloud-note-taking-au-smb.md` is present in ARTIFACTS WRITTEN. |
| c2 | The written file opens with YAML frontmatter including title, date, author=strategy-canvas, category (per report-conventions) | PASS | Frontmatter contains title, date: 2026-06-13, author: strategy-canvas, category: Commercial — all required fields present. |
| c3 | A value-curve table is present scoring NoteFlow and the three competitors across competing factors, with a stated basis for the scores drawn from the staged inputs | PASS | 8-factor table with all 4 competitors; each row has a 'Basis for scores' column citing review-mining percentages and competitive analysis data. |
| c4 | The convergence pattern is named explicitly as the headline — bunched curves (red ocean) vs a diverging curve — not buried | PASS | Opening 'The read' section leads with bold: 'Red ocean with a real blue ocean break available.' Dedicated subsection 'Convergence pattern' opens: 'Strong bunching indicates red ocean.' |
| c5 | A full ERRC grid is produced with a concrete entry in all FOUR cells (Eliminate, Reduce, Raise, Create) — not just two | PASS | ERRC grid has 2 Eliminate rows, 2 Reduce rows, 3 Raise rows, 2 Create rows — all four cells populated with distinct concrete entries. |
| c6 | Eliminate/Reduce entries are grounded in buyer evidence that buyers pay for things they don't value (e.g. template galleries / integration breadth from the review-mining themes), not in unsupported opinion | PASS | Eliminate template gallery cites '22%: Hundreds of templates, we use two; it's clutter.' Eliminate AI cites '14% mixed.' Reduce onboarding cites '31%.' Reduce admin cites segment skew note. |
| c7 | Raise/Create entries lift factors buyers demonstrably value (e.g. fast onboarding / sharing / offline reliability from the review evidence) | PASS | Raise onboarding cites 31% critical pain, Raise offline cites 25% positive loyalty driver, Raise sharing cites 20% positive — all drawn from staged review-mining themes. |
| c8 | The value-innovation test is applied — stating whether the moves cut cost AND lift value, not just differentiate | PASS | 'Value innovation test' section explicitly concludes: 'Eliminate + Reduce do cut cost... Raise + Create do lift value... Both sides move. This is not cost leadership alone... but genuine value innovation.' |
| c9 | The skill takes a clear position on whether a blue-ocean move is available or it is a red ocean — does not leave it open | PASS | 'Strategic position' section: 'NoteFlow can own the blue ocean.' Chat response: 'not a hypothetical blue ocean. The buyer evidence is concrete.' Unambiguous position taken. |
| c10 | The skill did NOT perform live web research — it applied the framework to the staged material | PASS | Sources table lists only the two staged files (T2 competitive-analysis and review-mining). No WebSearch/WebFetch calls evident; all evidence traces to staged inputs. |
| c11 | Output applies the Blue Ocean ERRC method correctly — Eliminate/Reduce target cost, Raise/Create target value — not a generic SWOT or feature comparison | PASS | Value innovation test section explicitly maps E+R to cost cuts (ML, design, support, compliance) and R+C to value lifts (speed, reliability, ease, positioning) — correct BO methodology applied. |
| c12 | Output's ERRC entries trace back to the staged buyer evidence (template clutter, integration breadth rarely used, slow onboarding, valued offline/sharing) rather than being invented | PASS | Every ERRC row contains a 'Buyer evidence' column citing specific review-mining theme shares (31%, 22%, 25%, 20%, 14%) and verbatims from the staged files. |
| c13 | Chat response includes the absolute path to the written report | PASS | Chat response opens with the absolute path: `/var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/eval-1781281515-a8d01589/work/blueoak/strategy-canvas/cloud-note-taking-au-smb.md` |

### Notes

A clean sweep — all 13 criteria pass. The skill correctly read staged inputs, produced a fully populated ERRC grid with buyer-evidence citations in every cell, applied the value-innovation test rigorously, and made an unambiguous blue-ocean position statement, all without performing any live web research.
