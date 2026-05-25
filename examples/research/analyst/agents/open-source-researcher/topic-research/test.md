---
# Match the model the agent declares (`model: sonnet` in
# open-source-researcher.md). Multi-source research is variance-prone on
# Haiku; Sonnet is what the agent expects at runtime.
target-model: claude-sonnet-4-6
---

# Test: open-source-researcher — topic research

Scenario: A user needs background research on edge computing adoption in Australian manufacturing before a client meeting.

## Prompt

I need background research on edge computing adoption in Australian manufacturing. Specifically: how widely is it being adopted, what's driving it, and what are the main barriers? I need this for a client meeting on Friday — Standard tier is fine.

A few specifics for the response:

- Begin by explicitly invoking the `/analyst:web-research` skill (state "Invoking /analyst:web-research at Standard tier" at the top).
- **Source priority for AU-specific question**: prefer AU sources — ABS (Australian Bureau of Statistics), AFR, AMTIL (Australian Manufacturing Technology Institute Ltd), AMGC (Advanced Manufacturing Growth Centre), DISR (Department of Industry, Science and Resources), CSIRO, IBISWorld AU, ABC News. Use US/EU sources only as comparators with explicit framing ("for context, in the US..."). Aim for ≥4 of 6 sources to be Australian.
- **Authority ranking**: government / industry-body sources (ABS, AMGC, DISR, CSIRO) take precedence over commercial market-research firms (IMARC, STL Partners) which take precedence over user-generated content platforms (vocal.media, Medium). State the ranking and apply it — don't cite vocal.media for headline statistics.
- **Inline citations** for every quantitative claim — every $/figure/percentage carries a `[Source N]` marker referencing the numbered sources list.
- **Acknowledge gaps**: where authoritative AU data doesn't exist (e.g. no ABS adoption survey on edge computing specifically), say so explicitly rather than padding with lower-quality sources.

## Criteria

- [ ] PASS: Agent invokes `/analyst:web-research` with Standard tier
- [ ] PASS: Every finding cites a source that has been fetched and read — no uncited assertions
- [ ] PASS: Agent prioritises AU sources (ABS, ABC News, industry associations, AFR) over US or UK equivalents for an AU-specific question
- [ ] PASS: Sources are authority-ranked — government or industry body data takes precedence over blog posts or vendor content
- [ ] PASS: Where sources conflict or evidence is thin, agent flags this explicitly rather than presenting contested findings as settled
- [ ] PASS: Agent does not hand off to business-analyst or osint-analyst — this is a general topic research request, not a company or infrastructure investigation
- [ ] PARTIAL: Agent notes gaps where authoritative data doesn't exist publicly, rather than padding with lower-quality sources to appear thorough
- [ ] PASS: Output is organised by theme, not by "here's what each source said"

## Output expectations

- [ ] PASS: Output addresses the three explicit research questions — adoption rate / how widely, drivers, barriers — each as a section, NOT collapsed into a generic "edge computing in Australian manufacturing" summary
- [ ] PASS: Output's sources are predominantly Australian — AMTIL, AMGC, ABS, AFR, IBISWorld AU, Australian government bodies (DISR), CSIRO — over US / EU sources for an AU-specific question; non-AU sources used only as comparators
- [ ] PASS: Output flags conflicts or thin evidence where sources disagree
- [ ] PASS: Output uses Standard tier — moderate depth, fetched primary and secondary sources, but NOT exhaustive deep-research with all six passes; the prompt names Standard explicitly
- [ ] PASS: Output is organised by theme (adoption / drivers / barriers / examples) NOT by source ("AFR said X, ABC said Y") — the structure serves the research question
