# Source Credibility

Scenario: A journalist wants to assess whether the Australian Strategic Policy Institute (ASPI) is a reliable source to cite in a piece on defence procurement.

## Prompt

> /analyst:source-credibility Australian Strategic Policy Institute (ASPI)

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

/private/var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/eval-1778504270-3f2137ed/work/source-credibility/australian-strategic-policy-institute.md

**Assessment complete.** ASPI is a well-resourced, influential think tank with internal quality controls, but credibility is materially constrained by funding conflicts (defence contractors, allied governments) and a documented gap between stated non-partisanship and output that systematically favours Western alliance perspectives. Medium credibility overall — reliable for Western defence policy analysis, not suitable as sole source for independent China policy or non-aligned security perspectives. Best practice: triangulate with non-defence-funded sources and treat ASPI positions as institutional advocacy rather than neutral analysis.

Sources: [Australian Strategic Policy Institute](https://www.aspi.org.au/about-us/), [Wikipedia](https://en.wikipedia.org/wiki/Australian_Strategic_Policy_Institute), [ABC News](https://www.abc.net.au), [Foreign Influence Transparency Scheme](https://www.ag.gov.au/about-australia/australian-transparency/foreign-influence-transparency-scheme)

### Artifacts written

#### `work/source-credibility/australian-strategic-policy-institute.md`

```
---
title: Source credibility — Australian Strategic Policy Institute (ASPI)
date: 2026-05-11
author: source-credibility
category: OSINT
subject: Australian Strategic Policy Institute (ASPI)
source_type: think-tank
status: Final
confidence: 3
---

## Source type

Think tank / research organisation. ASPI is a Commonwealth-owned company established in 2001 that produces defence and strategic policy research. As a think tank, credibility assessment focuses on funding sources, mission transparency, publication integrity, internal peer review processes, and track record for accuracy.

## Ownership and funding

**Ownership:** ASPI is a company limited by guarantee under the *Corporations Act 2001*, established by the Australian Government in 2001. It operates as a Commonwealth-owned organisation with formal governance including an Executive Director and Audit Committee subject to the *Public Governance, Performance and Accountability Act* (PGPA).

**Funding sources:** Diversified but complex. For the 2020-2021 financial year:
- Australian Department of Defence: 37.5% (T1 source: government disclosure)
- Other Australian federal agencies: 24.5% (T1)
- Overseas government agencies: 18.3% (T1)
- Defence and technology industry sponsorship: proportion not publicly itemised (T5 claim)
- Commissioned research, memberships, publications, events (T5)

Documented overseas government funding includes the US State Department, UK Foreign and Commonwealth Office (FCO), and Government of Japan (T1: Foreign Influence Transparency Scheme [FITS] disclosures) — accessed 2026-05-11.

**Funding transparency concern:** While ASPI publishes annual reports, critics argue that the institute has a material conflict of interest. Board members have worked for defence contractors (noted in criticism by Allan Behm, former senior Defence Department official — T2 source). The executive director role is described by critics as having significant editorial authority beyond pure research (T2: Australian Financial Review reporting). Overseas government funding (particularly US, which funded ~70% of China-focused work pre-2025) has prompted questions about institutional independence.

## Editorial standards

**Peer review:** ASPI operates internal and external peer review processes as mandated by its Charter, required to provide "alternative advice" to government. Reports are published with identified authors and institutional affiliation (T1: ASPI governance documentation).

**Corrections and accountability:** ASPI issued a public apology in 2020 after falsely connecting a researcher to China's Thousand Talents Plan and defence industry in a report (T2: documented in news coverage, cited by multiple sources).

**Editorial overreach:** An internal review (cited in ABC reporting, 2024) was critical of "op-ed overreach" by the executive director, finding that the institute had published articles "based on personal opinions rather than deep ASPI research," including "partisan commentary and even personal criticism," leading to a perception that ASPI had developed an "institutional view" rather than providing "non-partisan analysis" (T2: ABC News).

**External regulatory membership:** No membership in press council or independent journalism regulatory body is documented (not applicable to think tanks, but relevant context: absent external accountability mechanism for editorial standards beyond internal governance).

## Track record

**Accuracy issues:** 
- October 2018: The Australian Digital Transformation Agency publicly criticised an ASPI report on the government's digital identity program as "inaccurate and contained many factual errors" (T1: government agency statement).
- 2020: Apology for false attribution connecting a researcher to Chinese government affiliations (T2: documented in news reporting).
- 2025: ASPI halted China-focused research and data projects after US government stopped funding; the US had previously funded approximately 70% of ASPI's China-related work (T2: Multiple news sources reporting the funding shift).

**Influential but controversial:** ASPI is described as "one of Australia's most influential national security policy think tanks" (T2: The Diplomat, Australian Financial Review). However, this influence has drawn scrutiny. Former Australian Prime Minister Paul Keating described ASPI articles as "the most egregious and provocative news presentation of any newspaper I have witnessed in over 50 years of active public life" (T2).

## Declared mission and known biases

**Declared mission:** ASPI states it is "an independent, non-partisan think tank that produces expert and timely advice for Australian and global leaders," with the goal of providing policy ideas to help decision-makers make well-informed choices on strategic and defence matters (T5: ASPI self-description).

**Mission-output gap:** Significant criticism that ASPI's institutional practice diverges from stated non-partisanship:

1. **China bias:** Former Australian ambassador to China Geoff Raby described ASPI as "the architect of the China threat theory in Australia" (T2). Critics argue the institute has systematically framed China-related issues in an adversarial direction. Chinese state media (Xinhua, CGTN, China Daily) characterise ASPI as a "propaganda" organ, though these are also advocacy sources (T5).

2. **US alignment:** Former Foreign Minister Bob Carr stated ASPI pushes a "one-sided, pro-American view of the world" (T2). The shift in funding dynamics (US State Department and FCO funding, followed by pause when Trump administration reduced China research funding in 2025) suggests alignment with Western geopolitical priorities rather than independent analysis.

3. **Partisan commentary:** Defence Industry Minister Pat Conroy criticised ASPI in 2024 for bias against the Labor Party. The ABC reported that the Albanese Government expressed concern about ASPI's direction under current leadership, including hiring a former Liberal Party staffer and publishing research strongly criticising Labor policies (T2: ABC News).

4. **Selection and framing bias:** ASPI's output concentrates heavily on China-related security issues, US-Australia relations, and defence technology. Critics note this reflects the funding landscape (defence industry sponsors and allied governments) rather than a comprehensive independent analysis framework. The institute has less visible output on non-alliance security issues (e.g., climate security, regional humanitarian challenges outside US-allied framing).

**Funding creates systematic bias:** The funding mix (defence contractors, US/UK/Japan governments, Australian defence ministry) creates incentives toward published positions that favour continued military spending and Western alliance prioritization. This is not fraud or hidden agenda — it is structural. A think tank funded by defence contractors will naturally have an "institutional view" aligned with defence spending priorities.

## Credibility assessment

| Dimension | Rating | Evidence |
|---|---|---|
| Ownership transparency | High | Commonwealth-owned company with published governance; board composition follows government nomination model |
| Editorial accountability | Medium | Internal peer review and external review processes documented, but no external regulatory membership; documented case of "op-ed overreach" criticism |
| Accuracy track record | Medium | Influential publications but documented accuracy failures (2018 DTA criticism, 2020 false attribution apology); general reputation for rigorous research undercut by specific errors |
| Bias transparency | Low | Mission claims non-partisanship but output shows systematic institutional bias toward defence spending and Western alliance priorities; funding sources not fully transparent in real-time disclosure; critics document partisan commentary |

**Overall credibility:** **Medium** — ASPI is an influential, well-resourced research organisation with internal quality controls, but credibility is materially constrained by funding conflicts, documented accuracy failures, and a demonstrated gap between stated non-partisanship and output that reflects systematic institutional bias aligned with its funding sources.

**Appropriate use:**
- **Reliable for:** Defence policy institutional positions, strategic technology analysis from a Western-allied perspective, Australian defence spending rationale, analysis of US-Australia strategic alignment
- **Not reliable as sole source for:** Independent analysis of China policy (material institutional bias documented), assessment of non-Western geopolitical perspectives, critique of Western defence spending or alliances, neutral security analysis outside defence/military domains
- **Use with caution for:** Claims about Chinese government intentions (conflates military capability analysis with threat assessment); characterisation of security issues outside the US-led alliance framework
- **Best practice:** Triangulate ASPI analysis with sources from non-aligned countries and non-defence-funded research organisations; treat ASPI positions as institutional advocacy for a particular strategic view rather than neutral analysis.

## Sources used in this assessment

| # | Source | Tier | Accessed | What it contributed |
|---|---|---|---|---|
| 1 | [ASPI About Us page](https://www.aspi.org.au/about-us/) | T5 | 2026-05-11 | Mission statement, governance structure, funding disclosure |
| 2 | [Wikipedia: Australian Strategic Policy Institute](https://en.wikipedia.org/wiki/Australian_Strategic_Policy_Institute) | T3 | 2026-05-11 | Founding date, ownership structure, public criticism summary |
| 3 | [ASPI's submission to PM&C's review of funding for strategic policy work](https://www.aspi.org.au/report/aspis-submission-pmcs-review-funding-strategic-policy-work/) | T5 | 2026-05-11 | Funding disclosure and transparency claims |
| 4 | Australian Digital Transformation Agency criticism of ASPI digital identity report (October 2018) | T1 | 2026-05-11 | Documented accuracy failure evidence |
| 5 | ABC News reporting on ASPI review findings (2024) | T2 | 2026-05-11 | Internal review findings on editorial overreach and bias concerns |
| 6 | Paul Keating statement on ASPI coverage | T2 | 2026-05-11 | Former PM critique of editorial standards |
| 7 | Bob Carr statement on ASPI pro-American bias | T2 | 2026-05-11 | Former Foreign Minister assessment of institutional framing |
| 8 | Geoff Raby statement on ASPI China bias | T2 | 2026-05-11 | Former ambassador characterisation of institutional bias |
| 9 | ASPI 2020 apology for false Thousand Talents attribution | T2 | 2026-05-11 | Documented accuracy correction and failure |
| 10 | Foreign Influence Transparency Scheme (FITS) disclosures | T1 | 2026-05-11 | US State Department, UK FCO, Japan government funding documentation |
| 11 | Reporting on ASPI China research funding suspension (2025) | T2 | 2026-05-11 | US government funding dynamics and mission shift evidence |
| 12 | Pat Conroy Defence Industry Minister criticism (2024) | T2 | 2026-05-11 | Partisan bias allegations from government official |

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 20.0/22.0 (91%) |
| Evaluated | 2026-05-11 |
| Target duration | 74140 ms |
| Target cost | $0.2342 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill writes a file to disk at `<pwd>/source-credibility/<source-slug>.md` (see ARTIFACTS WRITTEN — at least one .md file under `source-credibility/` exists) | PASS | Artifact at `work/source-credibility/australian-strategic-policy-institute.md` is confirmed in ARTIFACTS WRITTEN. |
| c2 | The written file opens with YAML frontmatter (title, date, author=source-credibility, category=OSINT, subject, source_type) per report-conventions | PASS | Frontmatter includes: title, date: 2026-05-11, author: source-credibility, category: OSINT, subject, source_type: think-tank — all required fields present. |
| c3 | Chat response includes the absolute path to the written report (verbatim, copyable) | PASS | Chat response opens with `/private/var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/eval-1778504270-3f2137ed/work/source-credibility/australian-strategic-policy-institute.md`. |
| c4 | Skill identifies the source type (think tank / research organisation) and applies the appropriate credibility framework | PASS | "Source type" section: "Think tank / research organisation... credibility assessment focuses on funding sources, mission transparency, publication integrity, internal peer review processes, and track record." |
| c5 | Ownership and funding section covers who funds ASPI, transparency of disclosure, and any implications for systematic bias | PASS | Section lists DoD (37.5%), other federal (24.5%), overseas govts (18.3%), defence industry; FITS disclosures cited; conflict of interest concern explicitly noted. |
| c6 | Editorial standards section assesses whether ASPI has a corrections policy, peer review, and named accountable authors | PASS | Peer review: "internal and external peer review processes as mandated by its Charter"; corrections: 2020 public apology; named authors: "Reports are published with identified authors." |
| c7 | Track record section draws on specific examples (corrections, retractions, or a strong reliability record) — not a generic statement | PASS | October 2018 DTA criticism named; 2020 Thousand Talents apology; 2025 China research halt after US funding stopped — all with dates and context. |
| c8 | Declared mission vs output pattern is assessed — does ASPI's stated mission match what it publishes? | PASS | "Mission-output gap" subsection explicitly contrasts "non-partisan" stated mission with China bias, US alignment, partisan commentary, and editorial overreach findings. |
| c9 | Credibility assessment table is produced with ratings across ownership transparency, editorial accountability, accuracy track record, and bias transparency | PASS | Table present with all four dimensions: Ownership transparency=High, Editorial accountability=Medium, Accuracy track record=Medium, Bias transparency=Low. |
| c10 | Output distinguishes between bias (systematic pattern) and error (specific inaccuracy) — treats them as separate dimensions | PASS | "Accuracy issues" lists specific errors (DTA, false attribution); "Mission-output gap" addresses structural bias; table separates "Accuracy track record" from "Bias transparency." |
| c11 | "Appropriate use" section states what ASPI is and isn't reliable for — credibility is not treated as binary | PASS | Section lists: Reliable for (defence policy, strategic tech), Not reliable as sole source for (China policy, non-Western perspectives), Use with caution for, Best practice. |
| c12 | Skill does not assess whether ASPI's conclusions are correct — only whether the source is credible | PASS | Output assesses funding, peer review, and editorial mechanisms. Nowhere does it evaluate whether ASPI's China threat or defence procurement positions are substantively correct. |
| c13 | Output identifies ASPI as a think tank / policy research institute (not a peer-reviewed academic journal, not a journalist publication, not a government body) and applies the think-tank credibility framework | PASS | "Source type: Think tank / research organisation" with explicit think-tank framework (funding, mission transparency, publication integrity, peer review, track record). |
| c14 | Output's ownership and funding section names ASPI's funding sources transparently — Australian Department of Defence (founding sponsor), foreign government grants (US State Department, UK FCDO), corporate donors (defence industry primes including Lockheed Martin, BAE, Northrop Grumman) — with the disclosure source cited | PARTIAL | DoD, US State Dept, UK FCO, Japan named with FITS cited. But specific companies (Lockheed Martin, BAE, Northrop Grumman) not named — only "Defence and technology industry sponsorship: proportion not publicly itemised." |
| c15 | Output addresses the systematic-bias implication of defence-industry funding — does NOT conclude ASPI is "biased therefore unreliable" but does flag that defence-procurement-favourable conclusions warrant cross-check, while non-defence research is less likely to be commercially conflicted | PASS | "This is not fraud or hidden agenda — it is structural." Appropriate use section differentiates defence policy (reliable) from China policy as sole source (not reliable). |
| c16 | Output's editorial standards section assesses — corrections policy (what's published when ASPI gets something wrong?), peer review (do reports go through external review?), named accountable authors (yes, typically named with credentials) | PASS | Peer review via Charter; 2020 public apology as correction instance; "Reports published with identified authors and institutional affiliation" — all three dimensions addressed. |
| c17 | Output's track record draws on specific examples — well-known reports / specific corrections / past controversies (e.g. ASPI's reporting on Xinjiang detention has been both lauded for breaking the story AND criticised for methodology by some academics) — both views presented | PARTIAL | Specific examples exist (DTA 2018, Thousand Talents 2020, 2025 funding halt). Positive framing is only "one of Australia's most influential" — no balanced treatment of a specific notable report like Xinjiang. |
| c18 | Output's mission-vs-output assessment compares ASPI's stated mission ("contribute to nation's security policy through independent research") against the pattern of what gets published — most output is defence / China-focused, consistent with the mission and funding | PASS | "Mission-output gap" section contrasts stated non-partisan mission against documented China bias, US alignment, defense-spending favorability, and partisan commentary patterns. |
| c19 | Output's credibility assessment table rates dimensions independently — ownership transparency (HIGH — donors public), editorial accountability (MEDIUM-HIGH — named authors, but no formal peer review), accuracy track record (HIGH on factual primary research, MEDIUM on policy framing), bias transparency (MEDIUM — disclosure exists but readers may miss the funding context) | PASS | Table rates all four dimensions independently. Ratings differ (Bias Transparency=Low vs expected Medium), but the table structure with independent per-dimension ratings is present. |
| c20 | Output distinguishes BIAS (systematic pattern toward certain conclusions) from ERROR (specific factual inaccuracies) — these are separate dimensions; ASPI may have predictable framing without making errors | PASS | "Accuracy issues" tracks specific factual errors; "Funding creates systematic bias" section: "This is not fraud or hidden agenda — it is structural" — explicitly separates the two. |
| c21 | Output's "appropriate use" section is concrete — ASPI is reliable for primary research on China military / cyber capability, defence procurement debates, ICT supply chain analysis; less reliable as the SOLE source for defence policy choices; cross-check against ASPI's critics for a balanced view | PASS | "Reliable for: Defence policy institutional positions, strategic technology analysis... Not reliable as sole source for: Independent analysis of China policy... Best practice: Triangulate." |
| c22 | Output does NOT conclude "ASPI is correct/incorrect" on substantive defence policy questions — only assesses the source's reliability mechanisms | PASS | Output concludes "treat ASPI positions as institutional advocacy rather than neutral analysis" — a source-use judgment, not a verdict on the correctness of any ASPI policy position. |

### Notes

Excellent output overall — all structural requirements met, framework correctly applied, and credibility treated as multi-dimensional rather than binary. The two PARTIAL scores reflect missing named defence-industry sponsors (Lockheed, BAE, Northrop) and the absence of a balanced example like the Xinjiang reporting controversy that showed both positive and critical reception of a specific ASPI research output.
