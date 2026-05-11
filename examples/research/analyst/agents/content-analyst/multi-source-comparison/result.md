# Multi Source Comparison

Scenario: A user provides three articles on the same topic from different source types (financial press, progressive press, industry body) and asks the content analyst to compare framing and source quality before citing them in a policy brief.

## Prompt

> I have three articles about Australia's critical minerals strategy — one from the AFR, one from The Guardian, and one from the Minerals Council of Australia's website. Can you analyse how each one frames the issue differently? I want to understand the framing and source quality before I cite any of them in a policy brief.
> 
> Here are the three articles:
> 
> ---
> 
> **ARTICLE 1 — Australian Financial Review**
> 
> **Australia's Critical Minerals Opportunity: Why We Can't Afford to Blink**
> *Australian Financial Review, March 12, 2024. By Angela Marsh, Resources Correspondent.*
> 
> Australia sits atop one of the richest deposits of critical minerals on earth — lithium, cobalt, nickel, rare earths — at precisely the moment global demand for these materials is accelerating. The energy transition is not a future event; it is happening now, and the nations that control the supply of battery minerals will define the next industrial epoch.
> 
> The federal government's Critical Minerals Strategy, released late last year, correctly identifies Australia as a potential "renewable energy superpower." What it underestimates is the pace required. China currently processes roughly 60% of the world's lithium, 65% of its cobalt, and more than 80% of its rare earths. Australia ships raw ore and imports the value-added products back. This is a structural weakness that compounding investment can correct — but only if the regulatory and infrastructure settings attract capital rather than repel it.
> 
> The economics are compelling. Benchmark Mineral Intelligence estimates that meeting 2030 electric vehicle demand alone will require $514 billion in new mine and processing capacity globally. Macquarie Bank forecasts that Australian lithium exports could grow fivefold by 2030 if processing capacity is onshored. That is not a prediction — it is a conditional: if the approvals pipeline moves.
> 
> The strategic logic extends beyond economics. Japan, South Korea, the United States, and the European Union are all scrambling to reduce exposure to Chinese supply chains. Several bilateral agreements signed in the past 18 months — including the US–Australia Critical Minerals Partnership and supply agreements with Japan under the Quad framework — reflect this. The question is whether domestic policy settings are fast enough to match the opportunity window.
> 
> Current approval timelines for new mining projects average 4.7 years. Canada's fast-track critical minerals process averages 2.1 years. For an industry where first-mover advantage determines who captures downstream processing investment, this gap is not a minor inconvenience. The government's response — a Critical Minerals List and a $2 billion facility — signals intent. It does not yet signal urgency.
> 
> ---
> 
> **ARTICLE 2 — The Guardian Australia**
> 
> **The dark side of Australia's critical minerals rush**
> *The Guardian Australia, April 3, 2024. By Sienna Okafor, Environment Correspondent.*
> 
> The language of the energy transition has become a kind of moral permission slip. Because critical minerals are essential for batteries, solar panels, and electric vehicles, the logic runs, extracting them at scale is not just commercially sound but environmentally necessary. The contradiction embedded in this argument — that we must damage ecosystems to save them — is rarely examined.
> 
> The Pilbara, the Kimberley, the Flinders Ranges, and the Northern Territory — the regions identified in government strategy documents as priority areas for critical mineral extraction — are not blank administrative canvases. They are the country of Aboriginal and Torres Strait Islander peoples, many of whom have fought for decades to achieve the native title determinations now being tested by the pace of exploration licence approvals.
> 
> Professor Megan Davis, who has spent her career at the interface of Indigenous law and resources policy, has described the current moment as "the fastest erosion of free, prior and informed consent I've seen since the mining boom of the 2000s." Community consultations that should take 12–18 months are being compressed into weeks.
> 
> The science, too, is more complicated than the government narrative allows. Processing lithium and nickel generates sulphuric acid and toxic tailings. The water footprint of lithium brine extraction in arid environments is substantial. A study published in Nature Sustainability in 2023 found that when full lifecycle emissions are included, the carbon intensity of some processing pathways rivals that of the fossil fuel technologies they are meant to replace.
> 
> Conservation groups including the Wilderness Society and the Australian Conservation Foundation have raised concerns that Strategic Assessment provisions — allowing the federal government to fast-track approvals in exchange for high-level environmental commitments — provide cover for individual project impacts that would otherwise require closer scrutiny. The Environment Protection and Biodiversity Conservation Act has not been reformed since 1999; the government's own review, completed in 2020, recommended significant changes that have not been legislated.
> 
> None of this means Australia should not develop its critical minerals sector. It means the framing of the sector as a clean-energy story, rather than a mining story with clean-energy applications, obscures costs borne by communities and ecosystems — not by the shareholders who benefit.
> 
> ---
> 
> **ARTICLE 3 — Minerals Council of Australia**
> 
> **Critical Minerals: Delivering for Australia's Future**
> *Minerals Council of Australia, January 2024 Policy Position.*
> 
> Australia's critical minerals sector is at an inflection point. The global transition to clean energy technologies has created structural demand for minerals that Australia has in abundance — lithium, cobalt, vanadium, graphite, and a suite of rare earth elements essential for the permanent magnets in wind turbines and electric vehicle motors.
> 
> The Minerals Council of Australia represents the companies investing to develop this opportunity. Our members have committed more than $38 billion in announced critical minerals projects over the next decade. These investments will create 85,000 direct jobs in regional Australia — communities that have borne the brunt of agricultural downturns and manufacturing decline and are positioned to benefit most from a well-managed resource transition.
> 
> The strategic case is clear. Australia's Five Eyes partners — the United States, United Kingdom, Canada, and New Zealand — have each identified critical mineral supply security as a national security priority. Australia's geological endowment and institutional stability make it the partner of choice for friendly-nation supply chains.
> 
> To realise this potential, government must address the regulatory bottlenecks deterring investment. Project approval timelines are too long. Royalty frameworks designed for bulk commodity exports need updating for value-added processing. Infrastructure — particularly rail, water, and power to remote deposits — requires co-investment the private sector cannot provide unilaterally.
> 
> The MCA calls for a coordinated Critical Minerals Investment Compact: a single-window approval pathway, matched infrastructure co-investment, and a sovereign processing fund to support domestic value-add. Australia's major trading partners are moving fast; the window for positioning as the world's preferred critical minerals supplier will not remain open indefinitely.
> 
> ---

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll break down each article's framing, then assess source quality using your tier framework.

## Framing Analysis

**Article 1 — AFR: "Australia as Opportunity, Racing Against Time"**

- **Core narrative:** Australia has structural advantage (resources + stability) but regulatory bottlenecks will lose it to competitors
- **Key tension:** Economic opportunity vs. policy speed — portrayed as solvable if government moves
- **Actors:** China (threat), US/Japan/EU (allies scrambling to diversify supply), Australia (potential winner), government (enabler or blocker)
- **Tone:** Optimistic but urgent. The word "superpower" is aspirational; "blink" in the headline implies consequences for hesitation
- **Evidence type:** Forecasts (Benchmark Mineral Intelligence $514B, Macquarie's 5x growth) + comparative timelines (4.7 years vs Canada's 2.1 years)
- **What's absent:** Environmental costs, Indigenous consultation timelines, processing risks

**Article 2 — Guardian: "Mining Story, Not Clean-Energy Story"**

- **Core narrative:** Critical minerals narrative has become moral cover for extractive practices; climate language obscures genuine ecosystem and social costs
- **Key tension:** Energy transition necessity vs. the costs that transition pushes onto communities and ecosystems
- **Actors:** Government/industry (pushing fast-track), Indigenous communities (losing consent frameworks), researchers (flagging true costs), conservation groups (raising structural EPBC concerns)
- **Tone:** Critical but not dismissive — "None of this means Australia should not develop..." signals this is a reframing, not a rejection
- **Evidence type:** Expert observation (Megan Davis quote), peer-reviewed research (Nature Sustainability 2023), regulatory history (EPBC Act 1999, 2020 review), named conservation groups
- **What's absent:** Job creation figures, geopolitical security arguments, investment scale

**Article 3 — MCA: "Removing Barriers to Inevitable Growth"**

- **Core narrative:** Demand is structural and global; Australia just needs to remove regulatory friction to capture it
- **Key tension:** None explicitly — framed as alignment problem (market wants it, government just needs to enable)
- **Actors:** Australia (partner of choice), Five Eyes (validating demand), private sector (funding), government (bottleneck)
- **Tone:** Action-oriented, solutions-focused. The framing is "if we do X, we win"; no discussion of trade-offs
- **Evidence type:** Announced projects ($38B), job projections (85,000), geopolitical positioning (Five Eyes language)
- **What's absent:** Risk, environmental complexity, Indigenous consultation, processing challenges, regulatory justifications for timelines

---

## Source Quality Assessment

| Article | Tier | Credibility | Caveats for Citation |
|---|---|---|---|
| **AFR** | T2 (independent analysis) | High — professional editorial standards, bylined correspondent | Forecasts are conditional ("if processing capacity is onshored"). Always cite the original forecast source (Benchmark, Macquarie) rather than AFR's interpretation. The 4.7 vs 2.1 year comparison is factual but needs baseline (what does "average" include?). |
| **Guardian** | T2 (independent analysis) | High — professional editorial standards, cites peer-reviewed source + named experts | Megan Davis quote is a paraphrase/observation, not a direct quote — verify the exact claim if citing. The Nature Sustainability study is citable directly. EPBC Act history is factual. |
| **MCA** | T5 (subject's own materials) | Low — advocacy piece representing industry members | Announced projects and job figures are claims, not independently verified. You cannot cite "$38B invested" or "85,000 jobs" from this source — you must source these from corporate filings, government data, or T1/T2 reporting. The Five Eyes framing is real policy positioning, but "strategic demand" is an interpreted claim. |

---

## What Each Source Actually Lets You Say

**For your policy brief, here's what you can reliably cite from each:**

**AFR** ✓ Cite:
- Comparative approval timelines (4.7 vs 2.1 years) — but source the methodology
- The existence of the US–Australia Critical Minerals Partnership
- Macquarie Bank's forecast (label as forecast, not fact)

**Guardian** ✓ Cite:
- The Nature Sustainability 2023 study on processing emissions (get the DOI and read it yourself)
- EPBC Act history (no reform since 1999)
- The existence of conservation group concerns (name the groups)
- The observation that consultation timelines are being compressed

**MCA** ✗ Do not cite directly for:
- Investment figures or job projections
- Use only for: understanding industry positioning, or as evidence that "the minerals industry argues X"

---

## Confidence Rubric (your own framework applies)

- **AFR on opportunity economics:** Confidence 2-3 (forecasts are T2-sourced but conditional)
- **Guardian on environmental/social costs:** Confidence 3 (peer-reviewed study + regulatory facts)
- **MCA on investment commitment:** Confidence 1 (T5 only; verify the numbers elsewhere)

**For your policy brief:** Use AFR and Guardian as your primary sources. Use MCA only to demonstrate industry advocacy, not as evidence of facts. If you need investment or jobs figures, find T1 sourcing (government reports, ASX filings, DFAT statements).

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.0/17.0 (82%) |
| Evaluated | 2026-05-11 |
| Target duration | 32547 ms |
| Target cost | $0.0522 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent routes each article to content-analysis skill separately, then produces a comparative view | FAIL | Output is a single inline chat response with no evidence of routing to a content-analysis skill. No tool calls or skill invocations appear; analysis is performed directly. |
| c2 | Framing differences between the three sources are stated as interpretive observations, not facts | PASS | Uses interpretive labels throughout: 'Core narrative:', 'Key tension:', 'Tone:' — e.g. 'The core narrative: Australia has structural advantage but regulatory bottlenecks will lose it.' |
| c3 | Source credibility differences are noted (industry body vs independent press) | PASS | Source Quality Assessment table assigns T2 to AFR and Guardian ('independent analysis') and T5 to MCA ('subject's own materials'), with credibility rated High vs Low. |
| c4 | Each article's source structure is assessed independently (named/anonymous/unattributed sources) | PASS | Per-article 'Evidence type' sections name specific sources: AFR cites Benchmark Mineral Intelligence and Macquarie; Guardian cites Megan Davis, Nature Sustainability 2023, named groups; MCA uses own figures. |
| c5 | The comparison identifies where the three articles agree and where they diverge on key claims | PARTIAL | Divergence is clearly shown (environmental costs absent in AFR/MCA; jobs/investment absent in Guardian). However, explicit agreement ('all three agree on X') is never stated. |
| c6 | Agent recommends which source(s) are most appropriate for the policy brief context, with reasoning | PARTIAL | 'What Each Source Actually Lets You Say' gives specific cite/don't-cite guidance with reasoning: AFR for timelines/forecasts, Guardian for EPBC/academic, MCA only for industry positioning. |
| c7 | Agent does not produce a merged summary — each article is analysed independently before comparison | PASS | Three separate per-article sections under 'Framing Analysis' precede the Source Quality Assessment table. No merged summary at the outset. |
| c8 | Agent flags any claims that appear in only one source as requiring independent verification | PASS | 'You cannot cite $38B invested or 85,000 jobs from this source — you must source these from corporate filings, government data, or T1/T2 reporting.' MCA figures flagged as unverified single-source. |
| c9 | Output runs content-analysis independently per article first — three separate analyses for AFR, The Guardian, MCA — before any comparative view | PASS | Output has 'Article 1 — AFR', 'Article 2 — Guardian', 'Article 3 — MCA' sub-sections in Framing Analysis before the comparative Source Quality Assessment table appears. |
| c10 | Output's per-article analyses each cover the standard dimensions — entities, key claims, sentiment, framing, narrative, source structure — at parity, not deeper analysis on one article | PASS | All three articles receive identical structural treatment: Core narrative, Key tension, Actors, Tone, Evidence type, What's absent — equal depth across all. |
| c11 | Output's framing comparison states differences as interpretive observations — 'AFR frames as economic opportunity / national competitiveness; The Guardian frames as environmental / Indigenous land rights tension; MCA frames as industrial development / employment story' — clearly tagged as interpretation | PASS | AFR: 'Australia as Opportunity, Racing Against Time'; Guardian: 'Mining Story, Not Clean-Energy Story'; MCA: 'Removing Barriers to Inevitable Growth' — all tagged interpretively with explanatory labels. |
| c12 | Output addresses source credibility differences — MCA is an industry advocacy body (advocacy bias toward industry positions), AFR is financial press (economic-frame bias), The Guardian is progressive-leaning (political-frame bias) — without dismissing any | PARTIAL | MCA advocacy bias explicitly stated. AFR economic bias implicit (forecasts-only evidence noted). Guardian's progressive lean not explicitly labelled, though civil-society framing is described. No source dismissed. |
| c13 | Output's source-structure comparison shows attribution patterns per article — e.g. MCA cites named industry executives + own commissioned research, The Guardian cites independent academics + Indigenous-community sources, AFR cites government officials + corporate executives | PARTIAL | Attribution patterns noted per article in 'Evidence type' sections. But no side-by-side comparison table and 'Indigenous-community sources' vs 'named industry executives' distinction is not made. |
| c14 | Output identifies where the three articles AGREE (likely on the basic economic/strategic premise) and where they DIVERGE (impact assessment, Indigenous rights, environmental cost) on key claims | PARTIAL | Divergence clearly shown via 'What's absent' sections. No explicit statement of shared agreement (e.g. all three accept the strategic premise). Agreement only inferrable, not stated. |
| c15 | Output flags claims appearing in only one source — e.g. 'MCA claims X jobs; not corroborated in AFR or The Guardian; would need independent verification before citing in policy brief' | PASS | 'MCA on investment commitment: Confidence 1 (T5 only; verify the numbers elsewhere)' and explicit 'you cannot cite $38B or 85,000 jobs from this source' flags single-source claims. |
| c16 | Output's recommendation for the policy brief context names which sources are appropriate for which kinds of claims — MCA for industry positions (cited as industry view, not as fact), The Guardian / academic-cited material for civil society perspective, AFR for market-impact claims | PASS | 'What Each Source Actually Lets You Say' maps each source to specific claim types with ✓/✗ markers and explicit guidance on how to attribute MCA ('only to demonstrate industry advocacy, not as evidence of facts'). |
| c17 | Output does NOT produce a merged synthesis ('the truth is...') — comparison preserves the perspectives without collapsing them | PASS | Each perspective is preserved independently. Conclusion is a usage guide ('Use AFR and Guardian as primary sources'), not a synthesised truth claim. |
| c18 | Output recommends additional source types the policy brief should consider beyond these three — academic peer-reviewed journals, Senate inquiry submissions, Indigenous-community direct sources — for a balanced citation set | PARTIAL | Recommends T1 sourcing: 'government reports, ASX filings, DFAT statements' and reading the Nature Sustainability DOI directly. Senate inquiry submissions and Indigenous-community direct sources not mentioned. |

### Notes

The output is a strong per-article analysis with well-structured framing breakdowns and clear source-tier guidance, meeting most criteria at or above expectations. The main gap is c1 (no skill routing evidence) and partial gaps on explicit agreement identification (c14) and frame-bias labelling for AFR/Guardian (c12).
