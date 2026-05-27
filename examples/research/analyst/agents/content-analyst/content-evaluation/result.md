# Content Evaluation

Scenario: A user wants the content analyst to evaluate a competitor's blog post about remote work for framing, claims, and source structure.

## Prompt

> We compete with Atlassian in the project management space. Can you analyse this post from their blog and tell me what it's actually claiming, how it frames things, and what sources it uses? https://www.atlassian.com/blog/teamwork/new-research-covid-19-remote-work-impact
> 
> A few specifics for the response:
> 
> - Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
> - Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
> - For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
> - When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
> - Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Here is the full analysis (also written to `content-analysis--atlassian-remote-work-research.md`):

---

## Content analysis: "How to debug distributed teamwork, as suggested by new research" (Atlassian Blog)

**Date of content:** 7 October 2020
**Date of analysis:** 2026-05-27
**Word count:** ~900 (body text, excluding navigation and CTAs)

---

### Entities

**People:**
- Leisa Reichelt — Head of Research & Insights (Atlassian); author of post; primary source and framing voice
- Tiffany Philippou — Podcaster; quoted as external voice on inequality; subject/illustrative authority (not a researcher)

**Organisations:**
- Atlassian — Publisher and funder of the underlying research; has direct commercial interest in distributed-work tooling
- Paper Giant — Australian UX/research agency; co-conducted the study; credited only in the PDF filename, not in the article body
- Confluence, Trello (Atlassian products) — recommended as solutions
- Miro, Mural, Slack, Microsoft Teams, Karmabot — non-Atlassian tools also recommended (creates appearance of impartiality)

**Key figures cited:**
| Statistic | Context | Attribution |
|---|---|---|
| 43% | Increased job security / career concern | "The research" (Atlassian/Paper Giant study) |
| 33% | Spend more time reporting progress than pre-COVID | Same study |
| 46% | Women reporting increased confidence in achieving goals | Same study |
| 40% | Men reporting the same | Same study |
| "four-month" | Duration of study, beginning April 2020 | Article text |

No sample size, country breakdown, industry split, or recruitment methodology is disclosed in the article.

---

### Key claims

**Primary claim:** Distributed work introduces predictable, manageable failure modes — and organisations that adopt the right practices and tools can navigate them effectively.

**Supporting claims:**
- Spontaneous collaboration declines in remote settings, threatening innovation. *(Study; no sample size given)*
- 43% of remote workers have increased job security concerns despite feeling individually productive. *(Study; no denominator disclosed)*
- 33% of remote workers spend more time reporting progress than pre-COVID. *(Study; no denominator)*
- Women benefit disproportionately from video-call equality and relaxed appearance standards. *(Study: 46% vs 40%)*
- Three structural factors — household complexity, role complexity, network quality — explain variation in remote work experience. *(Author's interpretive framework from the study)*
- Asynchronous tools and OKRs are the correct organisational response. *(Author assertion; unattributed)*

**Implicit claims:**
1. **Atlassian is a credible, neutral authority on distributed work.** Company-funded research is presented without conflict-of-interest disclosure.
2. **Atlassian's products are the natural solution.** Confluence and Trello appear in "recommended solutions" immediately after each negative finding — the research structure creates a purchase justification.
3. **Findings are generalisable.** The piece uses universal language ("distributed work could lead to…") without qualifying for the study's unknown sample composition.
4. **The problem is primarily a tooling and process problem.** Structural issues (housing inequality, care burden, internet access gaps) are surfaced but resolved via employer stipends and async tools — systemic causation is deprioritised in favour of product-addressable solutions.

---

### Sentiment

**Overall tone:** Optimistic — challenges are real but framed as solvable puzzles with available solutions.

**Sentiment targets:**
- Remote / distributed work: cautiously positive — problems are tractable
- Atlassian tools and frameworks: unambiguously positive (presented as solutions)
- Employers: mildly pressured — framed as having a responsibility to act
- Women: empathetic and celebratory of gains; inequality surfaced as a silver lining
- Workers in difficult circumstances: sympathetic, but resolved via employer action rather than structural critique

**Notable language signals:**
- *"fascinating moment"* — neutralises a crisis; researcher excitement over worker disruption
- *"unexpected benefits"* — finding 3 headline; frames inequality as having an upside
- *"creative problem-solving"* / *"innovative solutions"* — progress framing; forecloses pessimism
- *"lasting reality"* — normalises distributed work as permanent; aligns with Atlassian's market position
- *"debug distributed teamwork"* — headline metaphor; frames human collaboration as a software engineering problem amenable to technical fixes (directly flatters a tool-buying, technical audience)

---

### Framing

**Perspective:** Structured entirely from the employer / team-leader viewpoint. Workers appear as data points and illustrative quotes, not as agents whose interests might conflict with employer decisions.

**Foregrounded:**
- Five numbered findings with clean headlines — signals rigour and completeness
- Specific percentage statistics — lend authority and memorability
- Actionable recommendations after every finding — positions Atlassian as solutions provider
- Atlassian's own Team Playbook ("Work Life Impact" play) as a recommended tool

**Backgrounded:**
- Paper Giant's co-researcher role — absent from article body; only discoverable in the PDF filename
- Research methodology — sample size, recruitment, geography, industry: none disclosed
- Atlassian's commercial conflict of interest — no disclosure statement
- The statistical gap between 46% and 40% in the gender finding is small and unqualified for significance

**Omissions:**
- No competing or independent academic research cited
- No external researchers or critics
- Causality question: does remote work cause innovation decline, or does emergency disruption?
- Temporal limitation: a four-month acute-shock study is generalised to "distributed work" as a permanent mode — a significant analytical leap
- Worker recourse: the piece recommends employer action with no discussion of accountability if employers don't follow through

**Dominant framing device:** Progress framing with embedded responsibility framing. "Yes, things are hard — here is what forward-thinking organisations will do." Activates reader identity as a capable, progressive leader who implements solutions.

---

### Narrative

The piece tells a **revelation + progress** story: COVID-19 exposed hidden truths about team dynamics, and Atlassian's research now provides the map forward. Team leads and managers are cast as capable actors; workers are cast as beneficiaries of good management decisions.

A secondary **human cost** narrative runs through findings 2 and 4 (job insecurity, housing inequality), rendered personal through individual quotes to activate empathy and urgency — but each is immediately contained by a "recommended solutions" section, keeping the emotional register within an actionable framework.

Together the narratives make the piece *feel* like honest research journalism while functioning as a product-category whitepaper. The reader arrives at "distributed work requires investment in the right tools and practices" as a research conclusion rather than a marketing claim.

---

### Source structure

| Source type | Count | For what claims |
|---|---|---|
| Named primary | 2 | Leisa Reichelt (all findings, all framing); Tiffany Philippou (inequality illustration only) |
| Named secondary | 1 | Atlassian + Paper Giant study — self-produced; not peer-reviewed; no methodology disclosed |
| Anonymous | Several | Research participants quoted without name, role, industry, or country |
| Unattributed | Multiple | All percentage statistics (no denominators); OKR recommendation; dress-code recommendation |

No external academic studies, no independent researchers, no government or NGO data sources are cited.

---

### Summary assessment

This is research-branded content marketing. The findings are structured to create a purchase journey — each "problem" is followed by a "solution" that includes an Atlassian product — while the research provenance (self-funded, Paper Giant co-author uncredited in the article body, no disclosed methodology or sample size) is insufficient to support the authoritative, universal tone. For competitive intelligence: the most significant move here is not the data but the positioning — **Atlassian frames itself as the epistemic authority on distributed teamwork**, not merely a toolmaker. That's a category-ownership play: if Atlassian defines the language and evidence base for how distributed work is understood, competitors are permanently responding to a frame Atlassian controls.

### Artifacts written

#### `work/content-analysis--atlassian-remote-work-research.md`

```
## Content analysis: "How to debug distributed teamwork, as suggested by new research" (Atlassian Blog)

**Date of content:** 7 October 2020
**Date of analysis:** 2026-05-27
**Word count:** ~900 (body text, excluding navigation and CTAs)

---

### Entities

**People:**
- Leisa Reichelt — Head of Research & Insights (Atlassian); author of post; primary source and framing voice
- Tiffany Philippou — Podcaster; quoted as external voice on inequality; subject/illustrative authority (not a researcher)

**Organisations:**
- Atlassian — Publisher and funder of the underlying research; has direct commercial interest in distributed-work tooling
- Paper Giant — Australian UX/research agency; co-conducted the study; credited only in the PDF filename, not in the article body
- Confluence, Trello (Atlassian products) — recommended as solutions
- Miro, Mural, Slack, Microsoft Teams, Karmabot — non-Atlassian tools also recommended (creates appearance of impartiality)

**Key figures cited:**
| Statistic | Context | Attribution |
|---|---|---|
| 43% | Increased job security / career concern | "The research" (Atlassian/Paper Giant study) |
| 33% | Spend more time reporting progress than pre-COVID | Same study |
| 46% | Women reporting increased confidence in achieving goals | Same study |
| 40% | Men reporting the same | Same study |
| "four-month" | Duration of study, beginning April 2020 | Article text |

No sample size, country breakdown, industry split, or recruitment methodology is disclosed in the article.

---

### Key claims

**Primary claim:** Distributed work introduces predictable, manageable failure modes for teams — and organisations that adopt the right practices and tools can navigate them effectively.

**Supporting claims:**
- Spontaneous collaboration declines in remote settings, threatening innovation. *(Attributed to the Atlassian/Paper Giant study — no sample size given)*
- 43% of remote workers have increased job security concerns despite feeling individually productive. *(Study; no denominator disclosed)*
- 33% of remote workers spend more time reporting progress than pre-COVID. *(Study; no denominator)*
- Women benefit disproportionately from video-call equality and relaxed appearance standards. *(Study: 46% vs 40%)*
- Three structural factors — household complexity, role complexity, network quality — explain variation in remote work experience. *(Author's interpretive framework derived from study)*
- Asynchronous tools and outcome-based measurement (OKRs) are the correct response to these challenges. *(Author assertion, unattributed)*

**Implicit claims:**
1. **Atlassian is a credible, neutral authority on distributed work.** The post presents company-funded research as independent research without disclosing the commercial conflict of interest.
2. **Atlassian's products are the correct solution.** Confluence and Trello appear in the "recommended solutions" for findings 1 and 2 — the research findings are structured to create purchase justification.
3. **These findings are generalisable.** The article uses universal language ("distributed work could lead to…", "people missed…") without qualifying for the study's unknown sample composition.
4. **The problem is primarily a tooling and process problem.** Structural issues (housing inequality, care burden distribution, internet access gaps) are surfaced but then resolved with employer stipends and asynchronous tools — systemic causation is deprioritised in favour of product-addressable solutions.

---

### Sentiment

**Overall tone:** Optimistic — the piece frames serious challenges as solvable puzzles with available solutions.

**Sentiment targets:**
- Remote / distributed work: cautiously positive — problems are real but tractable
- Atlassian tools and frameworks: unambiguously positive (presented as solutions)
- Employers: mildly pressured — framed as having a responsibility to act
- Women: empathetic and celebratory of gains; inequality findings treated as a silver lining
- Workers in difficult home circumstances: sympathetic, but their situation is resolved via employer action rather than structural critique

**Notable language signals:**
- *"fascinating moment"* — neutralises a crisis; researcher excitement over worker disruption
- *"unexpected benefits"* — finding 3 headline; frames inequality as having an upside
- *"creative problem-solving"* / *"innovative solutions"* — progress framing; forecloses pessimism
- *"lasting reality"* — normalises distributed work as permanent; aligns with Atlassian's market position
- *"debug distributed teamwork"* — headline metaphor; frames human collaboration as a software problem amenable to engineering fixes (directly flatters a technical, tool-buying audience)

---

### Framing

**Perspective:** The piece is structured entirely from the perspective of the employer/team-leader making decisions about distributed work. Workers appear as data points and illustrative quotes, not as agents with perspectives that might conflict with employer interests.

**Foregrounded:**
- Five numbered findings with clean headlines — signals rigour and completeness
- Specific percentage statistics — lend authority and memorability
- Actionable recommendations after every finding — positions Atlassian as a solutions provider
- Atlassian's own Team Playbook ("Work Life Impact" play) as a recommended tool

**Backgrounded:**
- Paper Giant's role as co-researcher — buried in PDF URL, absent from article text
- Research methodology — sample size, participant recruitment, geographic scope, industry distribution: none disclosed
- Atlassian's commercial interest in the conclusions — no conflict-of-interest statement
- The minority finding that 46% vs 40% difference in women's confidence is statistically small and based on an undisclosed sample

**Omissions:**
- No competing research or external academic literature cited
- No dissenting or critical voices from researchers outside Atlassian
- The causality question: does remote work *cause* innovation decline, or were the studied organisations already in disruption?
- The temporal limitation: a four-month study during a global emergency captures an acute shock, not a stable remote-work equilibrium — generalising to "distributed work" broadly is an unsupported leap
- Power dynamics: the piece recommends employers offer coworking stipends but does not address whether workers have any recourse if employers don't

**Dominant framing device:** Progress framing with embedded responsibility framing. The piece says: "yes, things are hard — here is what forward-thinking organisations will do." It activates reader identity as a capable, progressive leader who will adopt the recommendations.

---

### Narrative

The piece tells a **revelation + progress** story: a unique historical moment (COVID-19) has exposed hidden truths about how teams work, and those who study the data carefully (Atlassian) can now offer the map forward. The audience — team leads and managers — are cast as the capable actors who can implement the solutions. Workers are cast as the beneficiaries of good management decisions.

A secondary **human cost** narrative runs through findings 2 and 4 (job insecurity, housing inequality), rendered personal through individual quotes. This activates empathy and urgency — but is quickly resolved by each finding's "recommended solutions" section, containing the distress within an action framework.

Together the narratives produce a piece that *feels* like honest research journalism but functions as a product-category whitepaper: the reader arrives at "distributed work requires investment in the right tools and practices" as a research conclusion rather than a marketing claim.

---

### Source structure

| Source type | Count | For what claims |
|---|---|---|
| Named primary | 2 | Leisa Reichelt (all findings, all framing); Tiffany Philippou (inequality illustration) |
| Named secondary | 1 | Atlassian + Paper Giant study — self-produced; not peer-reviewed; no methodology disclosed |
| Anonymous | Several | Research participants quoted without name, role, industry, or country |
| Unattributed | Multiple | All percentage statistics presented without sample-size denominator; OKR recommendation; dress-code recommendation |

No external academic studies, no independent researchers, no government or NGO data sources are cited.

---

### Summary assessment

This is a piece of research-branded content marketing. The findings are structured to create a purchase journey — each "problem" is followed by a "solution" that includes an Atlassian product — while the research provenance (self-funded, Paper Giant co-author uncredited in body text, no disclosed methodology) is insufficient to support the authoritative, universal tone. The statistics cited are individually plausible but collectively unverifiable: no sample size, no methodology, no peer review. For competitive intelligence purposes, the most significant observation is the implicit claim: **Atlassian frames itself as the epistemic authority on distributed teamwork**, not just a toolmaker — a positioning move that positions the product suite as the natural infrastructure for the future of work.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/17.0 (100%) |
| Evaluated | 2026-05-27 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 161419 ms |
| Target cost | $0.2529 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent routes to `/analyst:content-analysis` skill for a single article URL | PASS | Output follows the exact section structure of the content-analysis skill (Entities, Key Claims, Sentiment, Framing, Narrative, Source Structure) and file is named with the skill's naming convention. |
| c2 | Agent distinguishes analysis from summarisation — produces entity extraction, key claims, sentiment, framing, and narrative sections rather than a plain summary | PASS | Output has all six distinct analytical sections: Entities, Key Claims, Sentiment, Framing, Narrative, Source Structure — clearly not a plain summary. |
| c3 | Framing observations are stated as interpretive judgements, not facts ("the piece frames X as..." not "X is...") | PASS | "Dominant framing device: Progress framing with embedded responsibility framing. The piece says..." and "The piece is structured entirely from the perspective of the employer/team-leader" are analytical characterisations. |
| c4 | Sentiment is assessed at the author's tone level, not the subject's actual situation | PASS | "Overall tone: Optimistic" and sentiment targets like "Remote/distributed work: cautiously positive — problems are real but tractable" assess the author's framing, not the actual state of remote work. |
| c5 | Source structure section identifies how claims are attributed (named sources, anonymous, unattributed) | PASS | Source structure table explicitly categorises: Named primary (2), Named secondary (1), Anonymous (Several), Unattributed (Multiple) with specific attribution per claim type. |
| c6 | Agent notes what the article omits or backgrounds, with a caveat if topic knowledge is insufficient to fully assess omissions | PARTIAL | Framing section has detailed Backgrounded and Omissions subsections, but no explicit caveat about topic-knowledge limitations. Ceiling is PARTIAL; omissions are well-covered so awarding full partial. |
| c7 | Agent does not produce a literature review or academic-style output — output is analytical, not encyclopedic | PASS | No literature review or external academic citations introduced; all analysis stays tightly focused on the single Atlassian article's argument structure. |
| c8 | Agent does not assess whether the article's conclusions are correct, only how it argues | PASS | Output consistently evaluates argumentative structure: "research provenance...is insufficient to support the authoritative, universal tone" — not a verdict on whether remote work actually reduces innovation. |
| c9 | Output is structured per the content-analysis format — sections for Entities, Key Claims, Sentiment, Framing, Narrative, Source Structure — not a plain summary | PASS | All six required sections present in both chat response and artifact: Entities, Key Claims, Sentiment, Framing, Narrative, Source Structure. |
| c10 | Output's Entities section extracts people (by role: source / subject / authority), organisations, key statistics and dates referenced in the article — with the article URL fetched and read | PASS | Entities section lists people with roles (author, podcaster/external voice), organisations, and a statistics table with percentages, their context, and attribution. Content clearly derived from fetched article. |
| c11 | Output's Key Claims section distinguishes the primary claim from supporting claims and implicit claims, with attribution per claim — "primary claim: remote work reduced productivity; attribution: anonymous internal Atlassian survey" | PASS | Key Claims has three tiers: Primary claim, Supporting claims (each with attribution like "(Study; no denominator disclosed)"), and four numbered Implicit claims with specific framing attribution. |
| c12 | Output's framing observations are clearly stated as INTERPRETIVE — e.g. "the piece frames remote work as a productivity question rather than a wellbeing or culture question" — not asserted as fact | PASS | "Dominant framing device: Progress framing with embedded responsibility framing" and "The piece says: 'yes, things are hard — here is what forward-thinking organisations will do'" are clearly interpretive characterisations. |
| c13 | Output's sentiment assessment evaluates the AUTHOR's tone and target — "tone is mildly positive on hybrid models, mildly negative on fully remote" — not the actual reality of remote work | PASS | Sentiment section evaluates author language signals ("fascinating moment", "debug distributed teamwork") and author tone targets, not actual remote work outcomes. |
| c14 | Output's source structure analyses how claims are attributed — count of named primary sources (e.g. 2 named Atlassian executives), named secondary sources, anonymous citations, unattributed assertions | PASS | Source structure table counts Named primary: 2, Named secondary: 1, Anonymous: Several, Unattributed: Multiple, with "for what claims" column specifying what each type covers. |
| c15 | Output identifies the dominant narrative structure — e.g. "transformation narrative" or "research-reveals narrative" — and what audience response it activates | PASS | Narrative section names "revelation + progress story" and secondary "human cost narrative", then states it "activates reader identity as a capable, progressive leader who will adopt the recommendations." |
| c16 | Output flags omissions where the article backgrounds or skips relevant context — e.g. "no mention of selection bias in the Atlassian-internal survey" — with a caveat if topic knowledge is insufficient to fully assess | PASS | Omissions subsection lists five specific gaps: no competing research, causality question, temporal limitation of four-month shock study, power dynamics. Agent shows confidence; conditional caveat not required. |
| c17 | Output is analytical NOT encyclopedic — does NOT include a literature review on remote work; stays focused on this article's argument structure | PASS | No external academic literature introduced. Every section stays focused on the Atlassian article's specific claims, language choices, and structural moves. |
| c18 | Output flags the competitive context — Atlassian is a competitor in PM space, so framing of remote work productivity may align with their commercial interest in collaboration tooling — relevant for the requester's competitive intel use case | PARTIAL | Summary assessment calls it "research-branded content marketing" and flags "Atlassian frames itself as the epistemic authority on distributed teamwork" as a category-ownership play. Ceiling is PARTIAL. |

### Notes

An exceptionally strong output that hits every criterion cleanly. The only structural gap is the absence of an explicit topic-knowledge caveat in the omissions section (c6), but the omissions analysis itself is thorough and confident, and the conditional caveat was arguably not required given the agent's evident contextual competence.
