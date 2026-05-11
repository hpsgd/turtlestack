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

```markdown
## Content analysis: How to Debug Distributed Teamwork, as Suggested by New Research

**Date of content:** October 7, 2020
**Date of analysis:** 2026-05-11
**Word count:** Approximately 1,200

### Entities

**People:**
- Leisa Reichelt — Author, researcher focused on teamwork and team effectiveness (source/authority)
- Tiffany Philippou — Podcast host (quoted subject, cited as external voice)

**Organisations:**
- Atlassian — Commissioned the study, employer/publisher of content (interested party)

**Locations:**
- International (study scope stated but no specific countries named)
- Various industries (mentioned generically, no specifics)

**Key figures and statistics:**
- 43% of remote workers — increased concern about job security/career progression
- 46% of women — reported increased confidence in ability to achieve
- 40% of men — reported increased confidence in ability to achieve
- One-third of remote workers — spent more time reporting progress than before

**Products/technologies cited:**
- Confluence, Google Docs, Trello, Miro, Mural (listed as visibility/collaboration solutions)

### Key claims

**Primary claim:**
Remote work presents both challenges and unexpected benefits. Organizations that intentionally address five key issues through deliberate practices and tool adoption can build more equitable and effective distributed work cultures.

**Supporting claims:**
- Remote collaboration reduces spontaneous exchanges and organic knowledge-sharing (attributed to "the research")
- 43% of workers worry about visibility and career progression in remote settings (research finding)
- Women report higher confidence in remote-work video settings than men (46% vs 40%) due to visual equality, relaxed dress codes, and reduced dominance dynamics (research finding)
- Home environment inequalities (space, wifi, background visibility) create career disadvantages based on geography and income (research finding)
- Three factors explain remote work success: household complexity, role complexity, and network quality (research framework)

**Implicit claims:**
- Atlassian's internal study is a credible research authority on teamwork effectiveness
- The tools Atlassian sells or recommends (Confluence, Trello, etc.) help mitigate identified problems
- Remote work is permanent or long-term; organizations must adapt rather than await return to offices
- Intentional management and tool choices can engineer better remote work outcomes

### Sentiment

**Overall tone:** Positive with concern undertones — Mixed. 
The piece acknowledges challenges sympathetically but frames them as solvable through organizational action and tool adoption. Optimistic closing ("opportunities to learn," "optimism").

**Sentiment targets:**
- Positive toward: women benefiting from remote work visibility and inclusivity; organizations taking intentional action; distributed collaboration methods
- Sympathetic concern toward: workers in tight living quarters, those experiencing "out of sight, out of mind" anxiety
- Implicit criticism of: offices that amplify dominant personalities, companies not providing home office support, practices that surface inequality

**Notable language signals:**
- "Innovation drought" — loaded, suggests stagnation and risk
- "Unexpected benefits" — frames women's gains as surprising, not obvious or expected
- "Latent inequalities" — passive framing; inequalities existed but were hidden, now "surfaced" by remote work (not created by it)
- "Creative solutions," "opportunities to learn" — agency and optimism
- "Out-of-sight, out-of-mind" — quoted directly, colloquial language humanizes the anxiety

### Framing

**Perspective:**
Framed from an organizational change-management perspective — how companies can optimize remote work. Predominantly Atlassian's research lens. Individual worker voices appear only as illustration of organizational problems, not as stakeholders setting the agenda.

**Foregrounded:**
- Solutions and recommendations (each finding includes "recommended solutions")
- Tools and processes (visibility tools, asynchronous practices, OKRs, digital recognition)
- The benefits for women (entire section, positive framing)
- Organizational agency ("organizations can," "teams will creatively address")

**Backgrounded:**
- Costs of implementing recommendations (home office stipends, tool adoption, process changes unpriced)
- Tension between different workers' needs (women's comfort vs. those needing structure)
- Methodological details of the research (sample size, geographic distribution, industry breakdown, validation)
- External research or competing perspectives on remote work

**Omissions:**
- No discussion of hybrid work or phased return trade-offs (mentions "phased returns" only in context of office access prioritization)
- No environmental benefits of remote work (commuting reduction, etc.)
- No worker/union perspective on remote work rights or permanence
- No measurement of actual innovation output — only inference from collaboration patterns
- No discussion of implementation barriers or failure modes
- No competing research or studies cited
- No mention of peer review or academic validation of the study
- No discussion of selection bias (Atlassian customers more likely to have remote-work infrastructure than general population)

**Dominant framing device:**
Progress/solution framing: identifies problems → frames them as solvable → provides actionable recommendations. Secondary device: human interest (individual quotes and experiences).

### Narrative

**Story structure:** "Organizations Face New Reality; Those Who Act Thoughtfully Will Thrive"

The piece activates a pragmatic, problem-solving narrative. Remote work is framed as a novel challenge requiring intentional experimentation rather than a threat. The implied arc: chaos/uncertainty (March 2020) → research-backed insight → organizational action → equitable remote culture.

Audience response activated: managerial confidence ("we can solve this"), sense of responsibility ("we must act"), and buy-in to organizational/tool-based solutions. The women's benefits angle activates recognition of an unexpected positive outcome, positioning organizations as winners when they maintain remote-friendly practices.

The narrative does NOT position this as workers advocating for rights or permanent remote options — it positions organizations as the active agents making choices.

### Source structure

| Source type | Count | For what claims |
|---|---|---|
| Named primary | 1 | Tiffany Philippou (anecdote about home office inequality; external validation of a concern) |
| Named secondary | 0 | No external studies or published research cited |
| Anonymous/unattributed quotes | 4+ | Worker experiences ("out-of-sight, out-of-mind," "restrained in business office," etc.) — illustrate research findings |
| Unattributed assertions | 5 | The five key findings presented as research conclusions without methodological disclosure |
| Internal proprietary research | 1 | "Atlassian commissioned an international, multimodal study beginning in April 2020" — described but not linked, no peer review mentioned, no raw data available |

**Source credibility assessment:** The piece relies almost entirely on Atlassian's unpublished, unvalidated internal research. No external studies are cited. The single external voice (Tiffany Philippou) is a podcast host, not a researcher. Worker quotes are anonymous, lending authenticity but preventing verification. The "multimodal, international study" is mentioned but not characterized by sample size, methodology, or validation status. Readers are asked to trust Atlassian's research authority without independent verification.

### Summary assessment

This is a strategically framed thought leadership piece designed to position Atlassian as a remote-work expertise authority while subtly marketing Atlassian's tools as solutions to identified problems. The research findings are presented as neutral discoveries, but every finding connects to a Atlassian product category (visibility via Confluence, OKRs tracking, digital recognition via team tools). The piece frames remote work as solvable through better processes and tools rather than as a structural challenge that may benefit workers and hurt organizations — a narrative that serves Atlassian's business interests. The source structure (one internal study, zero external validation, anonymous worker quotes) means claims cannot be independently verified; the framing choices position organizations and tools as active agents while workers appear only as problems to be managed.

```

---

## Key takeaways for your competitive positioning

**What Atlassian is actually claiming:** "We studied remote work, found five categories of problems, and here's how to solve them" — positioning the company as both researcher and solution provider.

**The framing strategy:** 
- Frames remote work as *manageable challenges* (not structural advantages/disadvantages or worker rights)
- Centers organizational agency (what companies should do) over worker voice (what workers want)
- Buries the fact that women benefit from remote work by wrapping it as a finding to "maintain," not a reason to embrace remote-first
- Positions Atlassian's tools as solutions without ever saying "buy our products"

**Source quality:** This is the weak point for Atlassian. The entire piece rests on their internal, unpublished study. No external validation. No peer review. No competing research cited. Tiffany Philippou's quote is the only external voice, and she's not a researcher. The five "findings" are asserted without showing methodological rigor.

If you're competing here, independent research citing peer-reviewed studies or broader data would outflank this — especially on the innovation drought claim, which is intuitive but not proven.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.0/17.0 (88%) |
| Evaluated | 2026-05-11 |
| Target duration | 61812 ms |
| Target cost | $0.0901 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent routes to `/analyst:content-analysis` skill for a single article URL | FAIL | Captured output is the direct analysis with no mention of skill invocation or routing to `/analyst:content-analysis`. Output jumps straight to the markdown analysis block. |
| c2 | Agent distinguishes analysis from summarisation — produces entity extraction, key claims, sentiment, framing, and narrative sections rather than a plain summary | PASS | Discrete sections present: Entities, Key Claims, Sentiment, Framing, Narrative, Source Structure — not a plain summary. |
| c3 | Framing observations are stated as interpretive judgements, not facts ("the piece frames X as..." not "X is...") | PASS | "Framed from an organizational change-management perspective", "The piece activates a pragmatic, problem-solving narrative", "Frames remote work as manageable challenges". |
| c4 | Sentiment is assessed at the author's tone level, not the subject's actual situation | PASS | "Overall tone: Positive with concern undertones — Mixed. The piece acknowledges challenges sympathetically but frames them as solvable through organizational action and tool adoption." |
| c5 | Source structure section identifies how claims are attributed (named sources, anonymous, unattributed) | PASS | Table with Named primary (1), Named secondary (0), Anonymous/unattributed quotes (4+), Unattributed assertions (5), Internal proprietary research (1). |
| c6 | Agent notes what the article omits or backgrounds, with a caveat if topic knowledge is insufficient to fully assess omissions | PARTIAL | Detailed Omissions sub-section lists 8 specific omissions. No caveat about knowledge limitations is included, though ceiling is PARTIAL regardless. |
| c7 | Agent does not produce a literature review or academic-style output — output is analytical, not encyclopedic | PASS | No literature review present. Output stays scoped to the single Atlassian article's argument structure. |
| c8 | Agent does not assess whether the article's conclusions are correct, only how it argues | PASS | Analytical body consistently examines argument structure. One minor slip: "intuitive but not proven" on innovation drought, but main output stays on how the piece argues. |
| c9 | Output is structured per the content-analysis format — sections for Entities, Key Claims, Sentiment, Framing, Narrative, Source Structure — not a plain summary | PASS | All six required sections (Entities, Key Claims, Sentiment, Framing, Narrative, Source Structure) are explicitly present with named headings. |
| c10 | Output's Entities section extracts people (by role: source / subject / authority), organisations, key statistics and dates referenced in the article — with the article URL fetched and read | PASS | Reichelt listed as "source/authority", Philippou as "quoted subject"; Atlassian listed; key figures (43%, 46%, 40%, one-third) and date (October 7, 2020) extracted. |
| c11 | Output's Key Claims section distinguishes the primary claim from supporting claims and implicit claims, with attribution per claim | PASS | Explicit sub-sections: Primary claim, Supporting claims (each attributed to "the research"/"research finding"), Implicit claims — all clearly labelled. |
| c12 | Output's framing observations are clearly stated as INTERPRETIVE — e.g. "the piece frames remote work as a productivity question rather than a wellbeing or culture question" — not asserted as fact | PASS | "Dominant framing device: Progress/solution framing"; "The piece activates a pragmatic, problem-solving narrative" — consistently interpretive language. |
| c13 | Output's sentiment assessment evaluates the AUTHOR's tone and target — "tone is mildly positive on hybrid models, mildly negative on fully remote" — not the actual reality of remote work | PASS | "Sentiment targets: Positive toward: women benefiting... Sympathetic concern toward: workers in tight living quarters" — author tone/targets, not remote work reality. |
| c14 | Output's source structure analyses how claims are attributed — count of named primary sources (e.g. 2 named Atlassian executives), named secondary sources, anonymous citations, unattributed assertions | PASS | Source structure table counts each category with specific numbers and describes what claims each type supports. |
| c15 | Output identifies the dominant narrative structure — e.g. "transformation narrative" or "research-reveals narrative" — and what audience response it activates | PASS | "Story structure: 'Organizations Face New Reality; Those Who Act Thoughtfully Will Thrive'"; "Audience response activated: managerial confidence, sense of responsibility, buy-in to organizational/tool-based solutions." |
| c16 | Output flags omissions where the article backgrounds or skips relevant context — e.g. "no mention of selection bias in the Atlassian-internal survey" — with a caveat if topic knowledge is insufficient to fully assess | PASS | Explicitly: "No discussion of selection bias (Atlassian customers more likely to have remote-work infrastructure than general population)" — the example criterion named is present. |
| c17 | Output is analytical NOT encyclopedic — does NOT include a literature review on remote work; stays focused on this article's argument structure | PASS | No remote work literature review. Entire analysis addresses the single Atlassian post's structure, claims, and framing choices. |
| c18 | Output flags the competitive context — Atlassian is a competitor in PM space, so framing of remote work productivity may align with their commercial interest in collaboration tooling — relevant for the requester's competitive intel use case | PARTIAL | "Strategically framed thought leadership piece designed to position Atlassian as a remote-work expertise authority while subtly marketing Atlassian's tools"; explicit "Key takeaways for your competitive positioning" section. |

### Notes

The output is a high-quality, structurally complete content analysis that satisfies nearly every criterion on interpretation, framing language, source structure, and narrative identification. The only clean miss is c1 — no evidence of skill routing appears in the captured chat response.
