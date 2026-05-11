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

I'll break down the framing and source quality so you can use these strategically in your brief.

## Framing Analysis

The three articles are asking fundamentally different questions:

| | **AFR** | **Guardian** | **MCA** |
|---|---|---|---|
| **Central question** | How can Australia capture this economic opportunity given approval delays? | Who bears the costs of the energy transition? | How can government remove barriers to investment? |
| **Frame** | Economic/geopolitical opportunity | Environmental & justice concern | Growth/national interest |
| **Core rhetoric** | Urgency, first-mover advantage, time-bound window | "Energy transition as moral permission slip" masks costs | Regional jobs, strategic partnerships, competitive window |
| **What's centered** | Speed of approvals, comparative timelines, processing capacity | Indigenous FPIC, lifecycle emissions, ecosystem damage | Investment capital, job creation, supply security |
| **What's downplayed** | Indigenous rights, environmental costs, processing risks | Economic opportunity, job benefits, strategic position | Environmental costs (absent), Indigenous concerns (minimal), legitimate tradeoffs |

## Source Quality Assessment

**AFR (Tier 2 — Independent journalist)**

- ✅ Professional journalist with editorial standards
- ✅ Cites specific sources: Benchmark Mineral Intelligence, Macquarie Bank, bilateral agreements
- ⚠️ **Citation gap:** No direct links to the studies or data cited. For your brief, you'd need to trace these independently (the 4.7-year vs 2.1-year approval figure is specific enough to be verifiable)
- **Confidence:** Facts about economics/timelines can support moderate-to-high confidence claims if you verify the underlying sources yourself

**Guardian (Tier 2 — Independent journalist)**

- ✅ Professional journalist with editorial standards
- ✅ Attributes claims to named expert: Professor Megan Davis is a real person (ANU, recognized Indigenous law scholar) — adds credibility
- ✅ Cites specific study: "Nature Sustainability 2023" — verifiable
- ⚠️ **Citation gap:** Doesn't link to the study or quote it directly. You need to verify the study exists and says what she claims it says
- ⚠️ **Quote accuracy:** Megan Davis quote about "fastest erosion of FPIC" should be traced to original source (speech, publication, interview)
- **Confidence:** Environmental and rights concerns can support moderate confidence if you verify the Nature study

**MCA (Tier 5 — Subject's own materials)**

- ❌ Self-published industry advocacy, not independent reporting
- ❌ Cites no external data: "$38 billion in announced projects" and "85,000 jobs" are claims about member intentions, not independently verified figures
- ❌ No acknowledgment of tradeoffs or legitimate concerns — this is pure advocacy
- **Confidence:** Capped at 1 (confidence) unless corroborated by T1-T3 sources. You can cite it to show what industry is claiming, but not as factual support
- **Use case:** "The Minerals Council of Australia has committed to $38 billion in investment" (what they say they'll do) — not "Australia will create 85,000 jobs" (unsupported claim)

## For Your Policy Brief

**What to do:**

1. **Use AFR and Guardian together** — they're both T2, credible on their respective domains. AFR on economics, Guardian on environmental/Indigenous concerns. They're not contradictory; they're incomplete views of the same issue.

2. **Verify before citing specific numbers:**
   - AFR's approval timeline figures (4.7 vs 2.1 years) — trace to source
   - Guardian's Nature Sustainability study — read it directly and quote accurately
   - MCA's $38B and 85k jobs — check whether these appear in press releases or annual reports with methodology

3. **Cross-check the Indigenous claim** — Okafor attributes "fastest erosion of FPIC since 2000s boom" to Megan Davis. Find where Davis said this (published paper? speech? interview?) and cite the original, not the journalist's paraphrase.

4. **For your brief's credibility:** If you cite only economics (AFR + MCA), policy readers will see you've ignored half the actual debate. If you cite both AFR and Guardian at T2, you show you've considered tradeoffs. That's more persuasive.

5. **Flag the MCA claim gap** — If you use MCA's employment numbers, add a caveat: "Minerals Council of Australia claims 85,000 direct jobs, though these figures are not independently audited." This is honest and maintains credibility.

**Single-source red flag:** 
The specific claim "Australia's FPIC erosion is the fastest since the 2000s boom" appears only in the Guardian article attributed to one expert. Before using this as a primary claim, seek a second T2-T3 source (e.g., Indigenous legal organizations, regulatory bodies, news coverage of specific failed consultations).

What's the intended audience for your brief, and how much space do you have for environmental/rights concerns vs. economic opportunity?

## Evaluation

| Field | Value |
|---|---|
| Verdict | PARTIAL |
| Score | 11.5/17.0 (68%) |
| Evaluated | 2026-05-11 |
| Target duration | 28093 ms |
| Target cost | $0.0526 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent routes each article to content-analysis skill separately, then produces a comparative view | FAIL | Output is a single unified chat response. No evidence of routing to a content-analysis skill per article — analysis is produced inline. |
| c2 | Framing differences between the three sources are stated as interpretive observations, not facts | PASS | Framing Analysis table uses labels like 'Economic/geopolitical opportunity', 'Environmental & justice concern' — presented as characterizations, not factual claims. |
| c3 | Source credibility differences are noted (industry body vs independent press) | PASS | MCA labeled 'Tier 5 — Subject's own materials' / 'Self-published industry advocacy'; AFR and Guardian labeled 'Tier 2 — Independent journalist'. |
| c4 | Each article's source structure is assessed independently (named/anonymous/unattributed sources) | PASS | AFR: 'Cites Benchmark Mineral Intelligence, Macquarie Bank'; Guardian: 'Attributes to Prof Megan Davis, Nature Sustainability 2023'; MCA: 'Cites no external data'. |
| c5 | The comparison identifies where the three articles agree and where they diverge on key claims | PARTIAL | Divergence is mapped clearly in the comparison table. Agreement is not explicitly stated; the brief note 'they're not contradictory; they're incomplete views' gestures at agreement without naming it. |
| c6 | Agent recommends which source(s) are most appropriate for the policy brief context, with reasoning | PARTIAL | 'Use AFR and Guardian together... AFR on economics, Guardian on environmental/Indigenous concerns'; MCA: 'cite to show what industry is claiming, but not as factual support'. |
| c7 | Agent does not produce a merged summary — each article is analysed independently before comparison | PASS | Each article has its own Source Quality Assessment block. No merged 'the truth is...' synthesis. Perspectives kept distinct throughout. |
| c8 | Agent flags any claims that appear in only one source as requiring independent verification | PASS | 'Single-source red flag: The specific claim... appears only in the Guardian article attributed to one expert. Before using this as a primary claim, seek a second T2-T3 source.' |
| c9 | Output runs content-analysis independently per article first — three separate analyses for AFR, The Guardian, MCA — before any comparative view | FAIL | Output leads with a comparative framing table, then per-article source quality assessments follow. Per-article analysis comes AFTER the comparative view, not before it. |
| c10 | Output's per-article analyses each cover the standard dimensions — entities, key claims, sentiment, framing, narrative, source structure — at parity, not deeper analysis on one article | FAIL | Per-article sections cover source quality and credibility only. No explicit entities, sentiment, or narrative dimensions. Standard content-analysis dimensions are absent. |
| c11 | Output's framing comparison states differences as interpretive observations — "AFR frames as economic opportunity / national competitiveness; The Guardian frames as environmental / Indigenous land rights tension; MCA frames as industrial development / employment story" — clearly tagged as interpretation | PASS | Framing Analysis table: 'Frame' row — 'Economic/geopolitical opportunity', 'Environmental & justice concern', 'Growth/national interest'. Presented as frame labels, not factual assertions. |
| c12 | Output addresses source credibility differences — MCA is an industry advocacy body (advocacy bias toward industry positions), AFR is financial press (economic-frame bias), The Guardian is progressive-leaning (political-frame bias) — without dismissing any | PARTIAL | MCA's advocacy bias is explicit: 'pure advocacy'. AFR's economic bias and Guardian's progressive lean are implied by domain ('on economics', 'on environmental/Indigenous') but not named as systematic biases. |
| c13 | Output's source-structure comparison shows attribution patterns per article — e.g. MCA cites named industry executives + own commissioned research, The Guardian cites independent academics + Indigenous-community sources, AFR cites government officials + corporate executives | PARTIAL | AFR: 'Benchmark Mineral Intelligence, Macquarie Bank, bilateral agreements'; Guardian: 'Prof Megan Davis, Nature Sustainability 2023'; MCA: 'no external data'. Patterns shown but not typed (e.g. 'corporate executives' vs 'academics'). |
| c14 | Output identifies where the three articles AGREE (likely on the basic economic/strategic premise) and where they DIVERGE (impact assessment, Indigenous rights, environmental cost) on key claims | FAIL | Divergence is mapped in the table. No explicit identification of agreement points (e.g. all three accept Australia's geological endowment as strategically significant). |
| c15 | Output flags claims appearing in only one source — e.g. "MCA claims X jobs; not corroborated in AFR or The Guardian; would need independent verification before citing in policy brief" | PASS | 'Flag the MCA claim gap — If you use MCA's employment numbers, add a caveat: Minerals Council claims 85,000 direct jobs, though these figures are not independently audited.' |
| c16 | Output's recommendation for the policy brief context names which sources are appropriate for which kinds of claims — MCA for industry positions (cited as industry view, not as fact), The Guardian / academic-cited material for civil society perspective, AFR for market-impact claims | PASS | 'AFR on economics, Guardian on environmental/Indigenous concerns... MCA: cite to show what industry is claiming, but not as factual support.' Each source matched to appropriate claim type. |
| c17 | Output does NOT produce a merged synthesis ("the truth is...") — comparison preserves the perspectives without collapsing them | PASS | All three perspectives are maintained separately throughout. No synthesis claim like 'the true picture is...'. 'They're not contradictory; they're incomplete views' explicitly refuses to merge them. |
| c18 | Output recommends additional source types the policy brief should consider beyond these three — academic peer-reviewed journals, Senate inquiry submissions, Indigenous-community direct sources — for a balanced citation set | PARTIAL | 'Seek a second T2-T3 source (e.g., Indigenous legal organizations, regulatory bodies, news coverage).' Partial — names some additional source types but not Senate inquiry submissions or peer-reviewed journals broadly. |

### Notes

The output demonstrates strong framing analysis, clear source tier differentiation, and useful policy-brief guidance, but fails on two structural criteria: it leads with the comparative table rather than per-article analyses first (c9), and the per-article sections cover source quality only — not the full standard content-analysis dimensions (c10). Agreement identification between articles is also missing (c14).
