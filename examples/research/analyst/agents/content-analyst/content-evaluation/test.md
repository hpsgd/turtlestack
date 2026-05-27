---
# Match the model the agent declares (sonnet) in
# plugins/research/analyst/agents/content-analyst.md. The runner otherwise
# falls back to the harness default (Haiku), which is not what the
# agent is designed to run on.
target-model: claude-sonnet-4-6
---

# Test: content-analyst — content evaluation

Scenario: A user wants the content analyst to evaluate a competitor's blog post about remote work for framing, claims, and source structure.

## Prompt

We compete with Atlassian in the project management space. Can you analyse this post from their blog and tell me what it's actually claiming, how it frames things, and what sources it uses? https://www.atlassian.com/blog/teamwork/new-research-covid-19-remote-work-impact

A few specifics for the response:

- Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
- Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
- For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
- When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
- Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Criteria

- [ ] PASS: Agent routes to `/analyst:content-analysis` skill for a single article URL
- [ ] PASS: Agent distinguishes analysis from summarisation — produces entity extraction, key claims, sentiment, framing, and narrative sections rather than a plain summary
- [ ] PASS: Framing observations are stated as interpretive judgements, not facts ("the piece frames X as..." not "X is...")
- [ ] PASS: Sentiment is assessed at the author's tone level, not the subject's actual situation
- [ ] PASS: Source structure section identifies how claims are attributed (named sources, anonymous, unattributed)
- [ ] PARTIAL: Agent notes what the article omits or backgrounds, with a caveat if topic knowledge is insufficient to fully assess omissions
- [ ] PASS: Agent does not produce a literature review or academic-style output — output is analytical, not encyclopedic
- [ ] PASS: Agent does not assess whether the article's conclusions are correct, only how it argues

## Output expectations

- [ ] PASS: Output is structured per the content-analysis format — sections for Entities, Key Claims, Sentiment, Framing, Narrative, Source Structure — not a plain summary
- [ ] PASS: Output's Entities section extracts people (by role: source / subject / authority), organisations, key statistics and dates referenced in the article — with the article URL fetched and read
- [ ] PASS: Output's Key Claims section distinguishes the primary claim from supporting claims and implicit claims, with attribution per claim — "primary claim: remote work reduced productivity; attribution: anonymous internal Atlassian survey"
- [ ] PASS: Output's framing observations are clearly stated as INTERPRETIVE — e.g. "the piece frames remote work as a productivity question rather than a wellbeing or culture question" — not asserted as fact
- [ ] PASS: Output's sentiment assessment evaluates the AUTHOR's tone and target — "tone is mildly positive on hybrid models, mildly negative on fully remote" — not the actual reality of remote work
- [ ] PASS: Output's source structure analyses how claims are attributed — count of named primary sources (e.g. 2 named Atlassian executives), named secondary sources, anonymous citations, unattributed assertions
- [ ] PASS: Output identifies the dominant narrative structure — e.g. "transformation narrative" or "research-reveals narrative" — and what audience response it activates
- [ ] PASS: Output flags omissions where the article backgrounds or skips relevant context — e.g. "no mention of selection bias in the Atlassian-internal survey" — with a caveat if topic knowledge is insufficient to fully assess
- [ ] PASS: Output is analytical NOT encyclopedic — does NOT include a literature review on remote work; stays focused on this article's argument structure
- [ ] PARTIAL: Output flags the competitive context — Atlassian is a competitor in PM space, so framing of remote work productivity may align with their commercial interest in collaboration tooling — relevant for the requester's competitive intel use case
