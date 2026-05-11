# Test: company-lookup skill

Scenario: a business analyst needs to research an unfamiliar company before a client meeting.

## Prompt

"Can you look up Palantir Technologies for me? I need to understand what they do, their business model, and any recent developments before a meeting tomorrow."

A few specifics for the response:

- The skill writes a conforming report to a file path it computes (`<pwd>/company-lookup/<company-slug>.md` by default). Capture and report that file path. Section structure follows the template at `${CLAUDE_PLUGIN_ROOT}/templates/company-lookup.md`. Every mandatory section in the template MUST appear in the written file, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
- Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
- For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
- When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
- Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Criteria

- [ ] PASS: Skill writes a file to disk at `<pwd>/company-lookup/<company-slug>.md` (see ARTIFACTS WRITTEN — at least one .md file under `company-lookup/` exists)
- [ ] PASS: The written file opens with YAML frontmatter (title, date, author=company-lookup, category=Corporate, subject) per report-conventions
- [ ] PASS: Chat response includes the absolute path to the written report (verbatim, copyable)
- [ ] PASS: Skill defines a clear trigger or usage context (when to invoke this skill)
- [ ] PASS: Skill specifies what sources to check (e.g. company website, LinkedIn, Crunchbase, news)
- [ ] PASS: Skill defines an output structure with named sections (not freeform)
- [ ] PASS: Output structure includes business model or "what they do" section
- [ ] PASS: Output structure includes financials or funding section
- [ ] PASS: Output structure includes recent news or developments section
- [ ] PARTIAL: Skill includes guidance on assessing source credibility or recency
- [ ] SKIP: Skill references collaboration with other agents (only relevant if plugin includes multiple agents)

## Output expectations

- [ ] PASS: Skill instructs the model to surface controversies / reputational risks (surveillance, military contracts, regulatory actions) — relevant to a meeting if the user might be asked about them
- [ ] PASS: Output's structure has named sections — Overview, What They Do, Business Model, Financials, Recent Developments, Key People, Sources — not freeform prose
- [ ] PASS: Skill flags any source >12 months old as potentially stale, with tighter thresholds for fast-moving sectors
- [ ] PASS: Skill instructs the model to surface meeting-prep angles — likely conversation topics, strategic shifts, executive statements, known sensitivities — not just facts
