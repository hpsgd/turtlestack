# Test: content-retrieval skill — JS-rendered SPA via Playwright tier path

Scenario: A researcher needs to retrieve a JavaScript-rendered government report. WebFetch returned an empty div, signalling JS rendering. The skill should follow its Output Format template — including the Tier 3 Pre-Flight section (availability check, robots.txt acknowledgement, intended Playwright command) and the Tier 4 fallback options.

## Prompt

/web-tools:content-retrieval https://transparency.gov.au/annual-reports/australian-signals-directorate/reporting-year/2023-24 — WebFetch returned an empty div with no content, likely JS-rendered

Follow the skill's Output Format template strictly. Every mandatory section must appear, including:

- Tier 1, Tier 2, Tier 3 Pre-Flight (availability check + robots.txt + intended snippet), Tier 3 Execution, Tier 4 fallback options, Retrieved content, Metadata, Content Quality Notes.
- Tier 2 either runs `curl -A "Mozilla/5.0..." -L <url>` with output, or is "Skipped — <rationale>".
- Tier 3 Pre-Flight is mandatory even if Tier 3 succeeds (documents intent).
- Tier 4 options listed even if Tier 3 succeeds.
- Content Quality Notes describe structure preservation rules and expected lossy steps for tables and footnotes.

## Criteria

- [ ] PASS: Skill classifies the target before attempting retrieval — identifies JS-rendered SPA as the likely Tier 3 case based on the empty response signal
- [ ] PASS: Tier 2 (curl with browser headers) is either attempted with the command shown, or explicitly skipped with a stated rationale
- [ ] PASS: Tier 3 invokes the bundled wrapper `fetch-rendered.sh` (Docker-driven Playwright) rather than expecting a local Playwright install. Wrapper availability is confirmed via `command -v docker` or `docker image inspect`.
- [ ] PASS: Tier 3 Playwright invocation waits for content render (network-idle by default, optionally `--wait-for <selector>`) — not bare `page.content()`
- [ ] PASS: robots.txt + ToS acknowledgement appears in the Tier 3 Pre-Flight section, before the Tier 3 Execution
- [ ] PASS: Tier 4 (human escalation) options are listed in the report — at least three actionable options, no silent paid-service invocation
- [ ] PASS: Retrieved content is reported with structure-preservation notes — headings/paragraphs/tables retained, navigation/footer/chrome stripped
- [ ] PASS: If all tiers fail, skill reports the failure with specific errors and suggests manual retrieval or an alternative source — does not fabricate content

## Output expectations

- [ ] PASS: Output classifies the target as a likely JS-rendered SPA based on the prompt's signal (empty div from WebFetch) and routes directly to Tier 3 reasoning
- [ ] PASS: Output documents the Tier 1 attempt as already failed per the prompt, and either runs Tier 2 (curl with browser UA) or explicitly states why it's being skipped
- [ ] PASS: Output's Tier 3 invocation uses the bundled `fetch-rendered.sh` wrapper (or names it explicitly) and waits for content render via network-idle / `--wait-for` selector — not bare `page.content()` immediately after navigation
- [ ] PASS: Output checks Docker availability before attempting Tier 3 (the wrapper requires Docker) and reports the result
- [ ] PASS: Output includes the robots.txt + ToS acknowledgement in the Tier 3 Pre-Flight section
- [ ] PASS: Output's Tier 4 (human escalation) lists at least three actionable options — manual download, alternative format, alternative source — and does NOT silently invoke a paid service
- [ ] PASS: Output preserves document structure on extraction — headings, paragraphs, tables retained; navigation, footer, and chrome stripped — and reports any lossy steps in Content Quality Notes
- [ ] PASS: Output reports the tier ultimately used, the escalation path attempted, and content-quality notes (e.g. "table extracted may have merged cells", "footnotes attached at end") rather than just dumping content
- [ ] PASS: If all tiers fail, output does NOT fabricate content — explicitly reports the failure with the exact error per tier and recommends a specific human action
