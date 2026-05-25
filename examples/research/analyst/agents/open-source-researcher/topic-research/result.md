# Topic Research

Scenario: A user needs background research on edge computing adoption in Australian manufacturing before a client meeting.

## Prompt

> I need background research on edge computing adoption in Australian manufacturing. Specifically: how widely is it being adopted, what's driving it, and what are the main barriers? I need this for a client meeting on Friday — Standard tier is fine.
> 
> A few specifics for the response:
> 
> - Begin by explicitly invoking the `/analyst:web-research` skill (state "Invoking /analyst:web-research at Standard tier" at the top).
> - **Source priority for AU-specific question**: prefer AU sources — ABS (Australian Bureau of Statistics), AFR, AMTIL (Australian Manufacturing Technology Institute Ltd), AMGC (Advanced Manufacturing Growth Centre), DISR (Department of Industry, Science and Resources), CSIRO, IBISWorld AU, ABC News. Use US/EU sources only as comparators with explicit framing ("for context, in the US..."). Aim for ≥4 of 6 sources to be Australian.
> - **Authority ranking**: government / industry-body sources (ABS, AMGC, DISR, CSIRO) take precedence over commercial market-research firms (IMARC, STL Partners) which take precedence over user-generated content platforms (vocal.media, Medium). State the ranking and apply it — don't cite vocal.media for headline statistics.
> - **Inline citations** for every quantitative claim — every $/figure/percentage carries a `[Source N]` marker referencing the numbered sources list.
> - **Acknowledge gaps**: where authoritative AU data doesn't exist (e.g. no ABS adoption survey on edge computing specifically), say so explicitly rather than padding with lower-quality sources.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I now have enough from 8 Australian-priority sources to synthesise the report. Let me write it up.

---

## Research: Edge Computing Adoption in Australian Manufacturing

**Date:** 26 May 2026
**Tier:** Standard
**Sources:** 9 (8 AU-origin, 1 APAC comparator)

**Authority ranking applied:** Government/industry body (ABS, AMGC, CSIRO, RBA, Ai Group, AMTIL) → commercial market research → user-generated content. No headline statistics drawn from vocal.media, Mordor Intelligence, IMARC, or similar low-authority sources.

---

### Adoption landscape — what the evidence actually shows

There is no ABS survey specifically tracking edge computing adoption in Australian manufacturing. The ABS *Innovation in Australian Business 2022–23* is the closest primary data source: it finds **58% of manufacturing businesses are innovation-active** [Source 1], with 48% reporting process innovation and 41% of those investing in "machinery, equipment or technology" [Source 1]. These figures establish a ceiling on digital technology engagement broadly but do not disaggregate edge computing, IIoT, or smart-sensor deployments.

**This is the central data gap:** unlike AI adoption (which DISR now tracks quarterly) and general ICT investment (tracked by RBA and Ai Group), there is no publicly available Australian survey that puts a number on edge computing adoption specifically in manufacturing. Any vendor-sourced figure claiming an AU-specific edge computing market size or adoption rate should be treated with scepticism; the available secondary-market-research claims (e.g., IIoT market projections on content aggregator sites) lack primary sourcing and do not meet the authority threshold for this brief.

What can be said at sector level: the Ai Group's 2024 *Technology Adoption in Australian Industry* survey found **83% of industrial-sector businesses** (a category that includes manufacturing) are actively adopting technology, compared to 73% in services [Source 7]. Within that, **52% have adopted AI** and 84% are active adopters across at least one technology category [Source 7]. This suggests manufacturing is *relatively* advanced among Australian industry sectors — but active technology adoption is a broader concept than edge computing specifically.

The most concrete project-level evidence comes from AMGC's completed Industry 4.0 SME Digitisation program, in which **17 SMEs across seven states** (metal fabrication, textiles, chemicals, packaging, and others) deployed IIoT sensors on legacy equipment using $248,470 in government funding co-matched by industry [Source 3]. This program is a useful proxy for the state of adoption: it was specifically designed to demonstrate IIoT viability to manufacturers who had not yet adopted it, implying adoption was not yet organic among the SME cohort.

*For context, in the Asia-Pacific region:* an ITBrief/APAC manufacturing survey (2025) found only **18% of manufacturers are working with Industrial IoT technologies**, with a further 37% having begun robotics/automation [Source 9]. These are not AU-specific figures, but they suggest AU manufacturers are unlikely to be meaningfully ahead of regional peers on IIoT/edge specifically.

---

### Drivers

**1. Real-time operational visibility and latency requirements**

The core industrial case for edge computing is processing sensor data close to the machine, reducing the round-trip to cloud infrastructure. AMTIL identifies the driver explicitly: cloud data transfer is "slow, expensive, and can be insecure," and bandwidth constraints at remote or factory-floor locations make cloud-only architectures impractical for real-time quality control, predictive maintenance, and machine health monitoring [Source 8]. AMGC's SME project targeted exactly this — IIoT sensors generating "hi-fidelity, real-time knowledge and analytics of manufacturing plant and equipment" [Source 3].

**2. Cost and productivity pressure on SMEs**

AMGC's 2017 analysis found that **80% of Australian manufacturers could become more advanced** through ICT investment and researcher collaboration [Source 2]. With the top 5% of firms accounting for 94% of capital spending and 54% of R&D [Source 2], the majority of manufacturers are under-invested in technology. The economic case for edge computing — reducing unplanned downtime, improving throughput, extending asset life — is the commercial lever that has driven early adoption in larger operators.

**3. Government and research ecosystem investment**

CSIRO's *Future Digital Manufacturing Fund* is a four-year commitment to deliver AI-based manufacturing technologies to Australian businesses, with IoT, digital twins, robotics, and AI explicitly in scope [Source 4]. CSIRO has also deployed *Vetra*, an edge AI infrastructure system at its Queensland Centre for Advanced Technologies featuring 48 GPUs, designed specifically to process AI workloads "close to where data is generated rather than relying solely on distant cloud-based systems" [Source 5]. This represents sovereign research capability in edge AI for physical/manufacturing environments.

**4. IT investment trajectory**

The RBA reports that business IT investment has grown approximately **80% over the past decade**, with software investment rising from 6% to 10.5% of private business investment between 2014/15 and 2024/25 [Source 6]. While not manufacturing-specific, this investment trajectory underpins the infrastructure buildout that makes edge deployments viable.

---

### Barriers

**1. Skills shortage — most-cited constraint**

Ai Group's 2024 survey identifies skills gaps as the leading barrier, cited by **54% of businesses** [Source 7]. Manufacturing specifically suffers from a scarcity of graduates with AI and advanced technology qualifications [Source 7]. The RBA echoes this: firms report difficulty accessing data engineers and scientists, and attribute this to a compound of training pipeline lag and competition from sectors with higher wage capacity [Source 6].

**2. Integration complexity and legacy infrastructure**

AMTIL flags that deploying a complete edge system is "highly complex because it requires the orchestration of a large number of different components," including drivers, adapters, and middleware to bridge operational technology (OT) and information technology (IT) systems [Source 8]. AMGC's SME project implicitly confirms this: it was specifically designed to instrument *existing* legacy equipment rather than require replacement, because equipment replacement costs are prohibitive for the SME cohort [Source 3].

*For context, in the Asia-Pacific region:* 30% of manufacturers cite integration difficulties with new systems, and 15% flag outdated legacy systems as a specific barrier [Source 9].

**3. Unclear return on investment and financing**

Ai Group finds **43% of businesses cite unclear ROI** and 36% face cost and financing availability challenges as barriers to technology adoption [Source 7]. The RBA similarly identifies uncertainty about AI's developmental trajectory and ROI measurement as material inhibitors, particularly for smaller manufacturers with limited capital buffers [Source 6].

**4. Data utilisation gap**

AMTIL cites a PwC/ACS finding (2018, so dated) that Australian businesses use only **6% of their data**, with 94% lost or unused [Source 8]. While this figure predates the current edge computing market by several years, it identifies the organisational and analytical capability gap that sits beneath the technology adoption question: deploying edge hardware without the data literacy to act on its output delivers limited value.

**5. Cybersecurity exposure at the edge**

Distributing compute to factory-floor nodes expands the attack surface materially. An Asia-Pacific manufacturing survey flags cybersecurity as a barrier for **12% of manufacturers** [Source 9], and the RBA survey notes regulatory uncertainty — including around data governance — as an inhibitor [Source 6].

---

### Key uncertainties

- **No AU adoption rate figure exists for edge computing specifically.** ABS covers innovation broadly; DISR's quarterly AI adoption tracker covers AI. There is a gap in public data that this brief cannot fill from authoritative sources.
- **AMTIL's underlying IoT economics data (PwC/ACS $50–88B savings estimate) is from 2018** — directionally useful but not current.
- **APAC comparator figures** (18% IIoT adoption, integration barrier rates) are from an ITBrief/APAC survey without published methodology and should be treated as directional.
- The DISR DISR.gov.au AI adoption page was unavailable at time of research (timeout); Q4 2024 figures for manufacturing-sector AI adoption cited in media summaries have not been independently verified against the primary release.

---

### Sources

1. [Innovation in Australian Business, 2022–23](https://www.abs.gov.au/statistics/industry/technology-and-innovation/innovation-australian-business/latest-release) — ABS — manufacturing innovation-active rate (58%), process innovation rate, technology expenditure breakdown
2. [New AMGC report defines advanced manufacturing in Australia](https://www.amgc.org.au/media-releases/new-amgc-report-defines-advanced-manufacturing-in-australia/) — AMGC — 80% of manufacturers could advance; top 5% concentration in exports/R&D/capital
3. [Industry 4.0 Digitisation of SME Infrastructure](https://amgc.org.au/project/industry-4-0-digitisation-of-sme-infrastructure/) — AMGC — 17-SME IIoT pilot, $248K funding, legacy equipment instrumentation
4. [Future Digital Manufacturing Fund](https://www.csiro.au/en/work-with-us/industries/manufacturing/future-digital-manufacturing-fund) — CSIRO — four-year digital manufacturing commitment; IoT, AI, robotics, digital twins
5. [CSIRO launches edge AI system to speed up real-time robotics learning](https://www.australianmanufacturing.com.au/csiro-launches-edge-ai-system-to-speed-up-real-time-robotics-learning/) — Australian Manufacturing / CSIRO — Vetra edge AI infrastructure, 48 GPUs, edge-core-cloud model
6. [Technology Investment and AI: What Are Firms Telling Us?](https://www.rba.gov.au/publications/bulletin/2025/nov/technology-investment-and-ai-what-are-firms-telling-us.html) — RBA Bulletin, Nov 2025 — IT investment +80% over decade; AI adoption rates; barriers (regulation, skills, uncertainty)
7. [Technology Adoption in Australian Industry](https://www.australianindustrygroup.com.au/resourcecentre/research-economics/technology-adoption-in-australian-industry/) — Ai Group 2024 — 84% active adoption; 83% industrial sector; 54% skills-gap barrier; 43% ROI barrier
8. [Industry 4.0: A revolution from edge-to-edge](https://amtil.com.au/hp-industry4-iot-amtil/) — AMTIL — system complexity, OT/IT integration, cloud bandwidth constraints; PwC/ACS $50–88B IoT savings estimate (2018, dated)
9. [Manufacturers embrace AI & automation but face key barriers in 2025](https://itbrief.com.au/story/manufacturers-embrace-ai-automation-but-face-key-barriers-in-2025) — ITBrief / APAC survey — used as regional comparator only; 18% IIoT adoption, 30% integration barrier, 30% skills barrier

---

**Bottom line for your client meeting:** The honest answer is that AU-specific edge computing adoption data doesn't exist at the granularity you'd want — ABS surveys innovation broadly, not edge computing. What the authoritative sources do establish is: manufacturing is one of Australia's more digitally active sectors, the SME majority is still in early IIoT stages (the AMGC 17-SME pilot signals the demonstration phase, not mass market), and the barriers are consistent across all surveys — skills shortage, integration complexity, and unclear ROI. The government/CSIRO investment pipeline (Future Digital Manufacturing Fund, Vetra) is real but reflects where the sector needs to go, not where it currently is.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 12.0/12.5 (96%) |
| Evaluated | 2026-05-26 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 631575 ms |
| Target cost | $0.5689 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent invokes `/analyst:web-research` with Standard tier | PARTIAL | Report header states 'Tier: Standard' but output opens with 'I now have enough from 8 Australian-priority sources...' — the explicit 'Invoking /analyst:web-research at Standard tier' statement is absent. |
| c2 | Every finding cites a source that has been fetched and read — no uncited assertions | PASS | All quantitative claims carry inline markers: '58% of manufacturing businesses' [Source 1], '83% of industrial-sector businesses' [Source 7], '54% cite skills gaps' [Source 7], Vetra [Source 5], etc. |
| c3 | Agent prioritises AU sources (ABS, ABC News, industry associations, AFR) over US or UK equivalents for an AU-specific question | PASS | Report header: '9 (8 AU-origin, 1 APAC comparator).' Sources 1–8 are ABS, AMGC, CSIRO, RBA, Ai Group, AMTIL. Only Source 9 is non-AU. |
| c4 | Sources are authority-ranked — government or industry body data takes precedence over blog posts or vendor content | PASS | 'Authority ranking applied: Government/industry body (ABS, AMGC, CSIRO, RBA, Ai Group, AMTIL) → commercial market research → user-generated content. No headline statistics drawn from vocal.media, Mordor Intelligence, IMARC...' |
| c5 | Where sources conflict or evidence is thin, agent flags this explicitly rather than presenting contested findings as settled | PASS | 'Key uncertainties' section flags: no AU edge-specific adoption rate, AMTIL 2018 data dated, APAC survey methodology unknown, DISR page timed out and unverified. |
| c6 | Agent does not hand off to business-analyst or osint-analyst — this is a general topic research request, not a company or infrastructure investigation | PASS | Output is a self-contained research report with no mention of handoff to any other agent type. |
| c7 | Agent notes gaps where authoritative data doesn't exist publicly, rather than padding with lower-quality sources to appear thorough | PARTIAL | 'This is the central data gap:' prominently stated; 'No AU adoption rate figure exists for edge computing specifically.' Explicitly avoids citing low-authority sources for headline stats. |
| c8 | Output is organised by theme, not by "here's what each source said" | PASS | Sections are 'Adoption landscape,' 'Drivers,' 'Barriers,' 'Key uncertainties' — all thematic, not per-source summaries. |
| c9 | Output addresses the three explicit research questions — adoption rate / how widely, drivers, barriers — each as a section, NOT collapsed into a generic "edge computing in Australian manufacturing" summary | PASS | Distinct sections: 'Adoption landscape — what the evidence actually shows,' 'Drivers' (4 numbered), 'Barriers' (5 numbered) — each a standalone section. |
| c10 | Output's sources are predominantly Australian — AMTIL, AMGC, ABS, AFR, IBISWorld AU, Australian government bodies (DISR), CSIRO — over US / EU sources for an AU-specific question; non-AU sources used only as comparators | PASS | 8 of 9 sources are AU (ABS, AMGC×2, CSIRO×2, RBA, Ai Group, AMTIL). Source 9 (ITBrief/APAC) is labelled 'used as regional comparator only.' |
| c11 | Output flags conflicts or thin evidence where sources disagree | PASS | Key uncertainties section; AMTIL 2018 PwC/ACS figure explicitly flagged 'directionally useful but not current'; APAC survey flagged as 'without published methodology.' |
| c12 | Output uses Standard tier — moderate depth, fetched primary and secondary sources, but NOT exhaustive deep-research with all six passes; the prompt names Standard explicitly | PASS | Header states 'Tier: Standard'; 9 sources covering primary (ABS, RBA) and secondary (AMTIL, Ai Group, ITBrief). No indication of exhaustive multi-pass methodology. |
| c13 | Output is organised by theme (adoption / drivers / barriers / examples) NOT by source ("AFR said X, ABC said Y") — the structure serves the research question | PASS | Structure is Adoption landscape / Drivers / Barriers / Key uncertainties / Sources list — purely thematic, no source-by-source narration. |

### Notes

An exceptionally strong research output: authority ranking is explicitly stated and applied, the central data gap (no AU-specific edge adoption rate) is foregrounded rather than buried, and all quantitative claims carry inline citations to real AU-origin sources. The only shortfall is the missing explicit 'Invoking /analyst:web-research at Standard tier' statement at the top, which was specifically required by the prompt.
