---
name: web-research
description: "Research a topic, question, or domain using web sources. Three tiers: quick (5 min answer), standard (structured overview), deep (exhaustive with source cross-referencing). Use when you need to understand an unfamiliar topic before deeper analysis."
argument-hint: "[topic or question to research]"
user-invocable: true
allowed-tools: WebSearch, WebFetch
---

Research $ARGUMENTS using public web sources.

## Step 1: Choose tier

Pick the tier based on what's needed:

| Tier | When to use | Sources | Output |
|---|---|---|---|
| **Quick** | Fast answer, known domain | 2-3 sources | 1-2 paragraphs |
| **Standard** | Structured overview | 5-8 sources | Sections with source list |
| **Deep** | Exhaustive, unfamiliar domain | 10+ sources | Full report with cross-referenced findings |

If the tier isn't specified, default to Standard. Use Quick only when the question is narrow and factual. Use Deep when the domain is unfamiliar or the stakes are high enough to warrant comprehensive sourcing.

## Step 2: Source discovery (unfamiliar domains only)

Before searching in an unfamiliar domain, identify what the authoritative sources ARE. Don't assume — the right sources vary by field.

Search: `"[domain] official data"`, `"[domain] public registry"`, `"[domain] primary sources"`.

Authority hierarchy for most domains:

| Authority level | Examples |
|---|---|
| Government / regulatory | ABS, Stats NZ, RBA, APRA, FCA, SEC, FDA |
| Academic / peer-reviewed | Google Scholar, PubMed, arXiv, SSRN |
| Industry association | Standards bodies, trade associations |
| Journalism | Reuters, AP, ABC News, RNZ, BBC, FT |
| Analyst / research | Gartner, IDC, IBISWorld AU |
| Company / product | Official documentation, press releases |
| Community / opinion | Blogs, forums, social media |

Work from the top down. Don't cite a blog when a government dataset exists.

## Step 3: Search

For **Quick** tier:

- Run 2-3 targeted searches
- Fetch the most relevant result
- Extract the answer

For **Standard** tier:

- Run 4-6 searches across different angles (definitions, data, criticism, recent developments)
- Fetch the 4-6 most relevant sources
- Look for where sources agree and where they conflict

For **Deep** tier:

- Start with source discovery (Step 2) regardless of domain familiarity
- Run 8-12 searches covering the topic from multiple angles
- Fetch 10+ sources, prioritising primary and authoritative sources
- Identify where sources contradict each other — that gap is often the most important finding
- Cross-reference every key claim across at least two independent sources

## Step 4: Synthesise

For Quick: answer the question directly.

For Standard and Deep: organise findings by theme, not by source. The reader wants to understand the topic, not to read a list of what each website said.

Where sources conflict, explain the conflict rather than choosing a side arbitrarily. Conflicting findings are often the most useful output.

## Rules

- Never cite a source you haven't read. Fetch the page before including it.
- Absence is a finding. If the expected authoritative source has nothing on this topic, note it.
- Don't pad Quick answers into Standard length or Standard into Deep. Match depth to the tier.
- For AU/NZ topics, use AU/NZ sources first: ABS, Stats NZ, ABC News, RNZ, ASIC, APRA — before defaulting to US or UK sources.
- Label clearly when a finding is contested or uncertain rather than presenting all findings with equal confidence.

## Output format

### Quick

```markdown
**[Topic]**

[Direct answer — 1-3 paragraphs]

**Sources:** [inline citations]
```

### Standard

```markdown
## Research: [Topic]

**Date:** [today]
**Tier:** Standard
**Sources:** [count]

### [Theme 1]

[Findings]

### [Theme 2]

[Findings]

### Key uncertainties

[Where sources conflict or evidence is thin]

### Sources

1. [Title](URL) — [what it contributed]
```

### Deep

```markdown
## Research report: [Topic]

**Date:** [today]
**Tier:** Deep
**Sources:** [count]

### Summary

[3-5 sentence overview of what the research found]

### [Section 1]

[Findings with inline citations]

### [Section 2]

[Findings with inline citations]

### Cross-reference check

Key claims verified across multiple independent sources:

| Claim | Source 1 | Source 2 | Agreement |
|---|---|---|---|
| [claim] | [source] | [source] | Yes / Partial / No |

Claims confirmed by a single source only:

- [claim] — [source] — single source, treat as unverified

### Conflicting evidence

[Where sources disagree and what the conflict reveals]

### Gaps

[What couldn't be established from public sources]

### Sources

1. [Title](URL) — [authority level] — [what it contributed]
```
