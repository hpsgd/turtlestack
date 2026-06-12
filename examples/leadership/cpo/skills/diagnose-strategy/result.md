# Diagnose Strategy

Scenario: The CPO is handed an existing "strategy" document to pressure-test before it ships. The document (staged as a fixture) is a textbook Rumelt *bad* strategy: dense fluff, a list of goals presented as the plan, no diagnosis of any obstacle, a guiding policy that permits everything ("better across every dimension"), and a scattered grab-bag of unrelated initiatives. The diagnose-strategy skill must READ the fixture, test it against Rumelt's kernel (diagnosis + guiding policy + coherent action), flag the four hallmarks of bad strategy WITH quotes from the document, rate it overall as Bad strategy (not Incomplete, not Good), and recommend specific fixes pointing at the authoring skills. It must NOT rewrite the strategy — this is a read-only critique skill. The flawed strategy is pre-staged by the harness at `{workspace}/work/docs/strategy/product-strategy-helmsman.md`.

## Prompt

> A strategy document has been staged for you at `docs/strategy/product-strategy-helmsman.md` (relative to the
> current working directory). Use the cpo `diagnose-strategy` skill to critique it:
> `/cpo:diagnose-strategy docs/strategy/product-strategy-helmsman.md`
> 
> Read the document, run Rumelt's good-strategy/bad-strategy diagnostic over it, and return the critique in
> the skill's standard format. Do not rewrite the strategy. Proceed without asking.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

```markdown
# Strategy diagnosis — product-strategy-helmsman.md

**Document:** docs/strategy/product-strategy-helmsman.md · **Claims to be:** Strategy · **Scope:** Product (Helmsman fleet-management platform) · **Date diagnosed:** 2026-06-13

## Overall verdict: Bad strategy

This document is primarily a collection of goals, generic values, and disconnected initiatives. It lacks the fundamental kernel of strategy: no diagnosis of the central challenge, no guiding policy that constrains choices, and no coherent coordination between actions. The language is heavy on buzzwords and abstract aspiration, which masks the absence of a real plan. The "how we win" section (lines 38–39) reduces to a tautology: "we win by being better across every dimension" — which is not strategy, it's the definition of winning.

## The kernel

| Element | Verdict | Evidence |
|---|---|---|
| Diagnosis | Missing | Document opens at line 5 with goals ("become the leading fleet-management platform") and never names a central challenge or critical obstacle. No simplification of the current situation. No statement of what's actually blocking progress. |
| Guiding policy | Missing / Permits everything | Lines 20–24 list "Strategic pillars" (Customer obsession, Innovation, Operational excellence, Growth) — generic values, not policies. They don't constrain choices: "Innovation" permits building anything cutting-edge; "Operational excellence" permits any efficiency work. None rule out actions or trade-offs. None follow from a diagnosis (there is none). |
| Coherent action | Present but uncoordinated | Lines 28–34 list seven initiatives: mobile app, AI assistant, European expansion, onboarding improvement, partner marketplace, brand refresh, freemium tier. No evident coordination; each pulls in a different direction (Europe vs. onboarding vs. marketplace vs. pricing). No proximate objective to anchor progress. No explanation of how they implement the pillars or achieve the goals. This is a wish list, not a coordinated plan. |

## Bad-strategy hallmarks

| Hallmark | Found? | Evidence |
|---|---|---|
| Fluff | Yes | **Lines 7–9:** "delivering world-class value to our customers through a best-in-class, end-to-end experience. We will leverage synergies across our ecosystem to unlock transformative growth and cement our position as the category leader." Dense buzzwords ("world-class," "best-in-class," "end-to-end," "leverage synergies," "transformative growth," "category leader") with no concrete content. **Line 23:** "streamline our operations to maximise efficiency" — abstract with no actual policy or constraint. **Lines 38–39:** "We win by being better than the competition across every dimension and by relentlessly executing on our vision" — vacuous. |
| Failure to face the challenge | Yes | No diagnosis of what's blocking progress, what the critical few obstacles are, or what the real competitive position is today. Strategy cannot be evaluated against any named challenge. The directive to be "better across every dimension" suggests the author has not identified where to actually focus. |
| Mistaking goals for strategy | Yes | **Line 13:** "Grow annual recurring revenue to $50M within three years" — a goal, not how to get there. **Line 14:** "Become the #1 fleet-management product in the mid-market by market share" — a goal. **Line 15:** "Double our active user base year on year" — a goal. **Line 16:** "Achieve a world-class Net Promoter Score above 70" — a goal. **Line 17:** "Delight our customers at every touchpoint" — a goal. These belong under "Goals" (and correctly are) but the document then presents "Strategic pillars" and "Initiatives" without explaining *how* the initiatives achieve the goals or *why* these initiatives are the right moves. |
| Bad strategic objectives | Yes | The seven initiatives are scattered and incoherent. Mobile app, European expansion, AI assistant, onboarding, marketplace, brand, freemium — each a major commitment with different customer bases and resource trade-offs — are presented as equals with no prioritization or sequencing. No logic connects them to each other or to the goals. It's unclear which are essential vs. optional, and no proximate objective focuses near-term effort. |

## Recommended actions

1. **Add a diagnosis.** The document must open with a statement of the central challenge: What's blocking Helmsman from growing faster? Is it product adoption, market awareness, feature gaps, customer satisfaction, retention, sales capacity, or something else? Start with `/cpo:write-product-strategy` and front-load a "Current situation and challenge" section that clarifies the one or two critical obstacles you're addressing.

2. **Develop a guiding policy.** Once the challenge is named, state the overall approach for overcoming it — a policy that constrains choices and rules things out. Example (hypothetical): "We will win by becoming the easiest platform for mid-market fleets to integrate and operate, which means prioritizing ease-of-use and API simplicity over feature breadth." This policy would justify some initiatives (onboarding, integration marketplace) and question others (brand refresh, European expansion without a clear reason). Use `/cpo:write-product-strategy` to draft this after the diagnosis is clear.

3. **Coordinate the initiatives.** Once diagnosis and policy are in place, revisit the seven initiatives. Eliminate or defer those that don't follow from the policy. Sequence the remainder so they reinforce each other (e.g., if ease of integration is the policy, build the partner marketplace before expanding to Europe). Name a proximate objective — a near-term, achievable milestone that proves progress on the central challenge (e.g., "50% reduction in onboarding time within 6 months").

4. **Remove or replace fluff.** Scan the final strategy for buzzword density. Every instance of "world-class," "synergies," "transformative," "best-in-class," "cutting-edge," and vague abstractions should be replaced with concrete, specific language or removed entirely. The "how we win" section (line 38–39) must be rewritten to state the actual competitive advantage or logic, not a tautology.
```

### Artifacts written

#### `work/docs/strategy/product-strategy-helmsman.md`

```
# Product strategy — Helmsman

**Author:** Product leadership · **Date:** 2026-02-01

## Our strategy

Helmsman will become the leading fleet-management platform in the mid-market, delivering world-class value
to our customers through a best-in-class, end-to-end experience. We will leverage synergies across our
ecosystem to unlock transformative growth and cement our position as the category leader.

## Goals

1. Grow annual recurring revenue to $50M within three years.
2. Become the #1 fleet-management product in the mid-market by market share.
3. Double our active user base year on year.
4. Achieve a world-class Net Promoter Score above 70.
5. Delight our customers at every touchpoint.

## Strategic pillars

- **Customer obsession.** We will put the customer at the heart of everything we do.
- **Innovation.** We will harness cutting-edge technology to stay ahead of the curve.
- **Operational excellence.** We will streamline our operations to maximise efficiency.
- **Growth.** We will aggressively pursue new markets and expand our footprint globally.

## Initiatives

- Launch a mobile app.
- Add an AI assistant.
- Expand into the European market.
- Improve the onboarding flow.
- Build a partner integrations marketplace.
- Refresh the brand and website.
- Explore a freemium pricing tier.

## How we win

We win by being better than the competition across every dimension and by relentlessly executing on our
vision to be the best in the industry.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 10.5/11.0 (96%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 36255 ms |
| Target cost | $0.0653 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Reads the staged document and summarises what it claims to be (a "strategy") and how it is organised, quoting the document's own framing | PASS | Header: 'Claims to be: Strategy · Scope: Product (Helmsman fleet-management platform)'; quotes 'how we win' section (lines 38–39) verbatim and describes the doc's sections (Goals, pillars, initiatives). |
| c2 | Tests for the kernel's DIAGNOSIS and finds it MISSING — no central obstacle/challenge is named anywhere; the document jumps straight to goals and pillars | PASS | Kernel table row: 'Diagnosis \| Missing \| Document opens at line 5 with goals… and never names a central challenge or critical obstacle. No simplification of the current situation.' |
| c3 | Tests for the GUIDING POLICY and finds it absent or permits-everything — quotes the "better than the competition across every dimension" / "best in the industry" framing as a non-guiding policy | PASS | Kernel: 'Guiding policy \| Missing / Permits everything'; quotes lines 38–39 'We win by being better than the competition across every dimension' and notes pillars 'don't constrain choices'. |
| c4 | Tests for COHERENT ACTION and finds the initiatives uncoordinated — names the initiative list (mobile app, AI assistant, Europe, onboarding, marketplace, rebrand, freemium) as a scattered grab-bag that does not reinforce a single approach | PASS | Kernel: 'Coherent action \| Present but uncoordinated'; names all seven: 'mobile app, AI assistant, European expansion, onboarding improvement, partner marketplace, brand refresh, freemium tier. No evident coordination.' |
| c5 | Flags FLUFF as present and quotes specific instances — e.g. "world-class value", "leverage synergies across our ecosystem", "transformative growth", "cutting-edge" — as inflated language masking absent content | PASS | Fluff row quotes lines 7–9 verbatim: 'world-class value… best-in-class… end-to-end… leverage synergies… transformative growth… category leader' with explicit call-out of buzzword density. |
| c6 | Flags FAILURE TO FACE THE CHALLENGE (no obstacle defined) AND MISTAKING GOALS FOR STRATEGY — quoting goals presented as the plan (e.g. "grow ARR to $50M", "become the #1 fleet-management product", "double our active user base") | PASS | Hallmarks table: 'Failure to face the challenge \| Yes' and 'Mistaking goals for strategy \| Yes' with line-level quotes: Line 13 'Grow ARR to $50M', Line 14 'Become the #1 fleet-management product', Line 15 'Double our active user base'. |
| c7 | Flags BAD STRATEGIC OBJECTIVES — the "strategic pillars" (customer obsession, innovation, operational excellence, growth) are recognised as a dog's-dinner / blue-sky list, not a coherent reachable set | PARTIAL | Pillars named as 'generic values, not policies' under Guiding policy kernel row (lines 20–24). The 'Bad strategic objectives' hallmark row instead focuses on the seven initiatives. Pillars not explicitly called bad strategic objectives. |
| c8 | Rates the document OVERALL as **Bad strategy** (not "Good strategy", not merely "Incomplete"), applying Rumelt's bar plainly without grading on a curve because the document reads as polished | PASS | Opening verdict header: 'Overall verdict: Bad strategy' with plain language: 'primarily a collection of goals, generic values, and disconnected initiatives.' No hedging or partial credit. |
| c9 | Every kernel verdict and hallmark flag cites the document (quotes the offending line or names the section); does NOT rewrite or author a replacement, instead giving actionable recommendations that point fixes to `/cpo:write-product-strategy` (and `/cpo:write-product-vision` if the missing piece is the vision) | PASS | All rows cite specific lines (Lines 5, 7–9, 13–17, 20–24, 28–34, 38–39). Recommendations 1 and 2 explicitly reference '/cpo:write-product-strategy'. No replacement strategy authored. |
| c10 | Output presents the kernel as a table (Diagnosis / Guiding policy / Coherent action) with a verdict and cited evidence per row, and a bad-strategy-hallmarks table with Found?/Evidence per hallmark — all four hallmarks marked Found with quotes | PASS | Kernel table has three rows with Verdict+Evidence columns. Hallmarks table has four rows (Fluff, Failure to face challenge, Mistaking goals, Bad strategic objectives) all marked 'Yes' with quoted evidence. |
| c11 | Output's overall verdict is **Bad strategy** and the recommended actions name what to add (a diagnosis, a guiding policy) and which skill produces the fix, without rewriting the document | PASS | Recommendations section: 'Add a diagnosis… /cpo:write-product-strategy', 'Develop a guiding policy… /cpo:write-product-strategy'. No strategy rewrite present. |

### Notes

Exceptionally strong output — all four Rumelt hallmarks flagged with direct quotes, kernel table fully populated, overall verdict unambiguous. The only shortfall is c7: the four strategic pillars are correctly identified as generic non-policies under the Guiding policy kernel row, but the Bad strategic objectives hallmark row targets the seven initiatives instead, so the criterion's specific ask (pillars as bad objectives) is only partially satisfied.
