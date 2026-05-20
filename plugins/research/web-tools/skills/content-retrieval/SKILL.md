---
name: content-retrieval
description: "Retrieve content from a URL using a four-tier escalation strategy: WebFetch → curl → Playwright (JS rendering) → human escalation (anti-bot bypass). Use when standard WebFetch fails or when the target URL is known to require JS rendering or bot mitigation bypass."
argument-hint: "[URL to retrieve]"
user-invocable: true
allowed-tools: WebFetch, Bash
---

Retrieve the content at $ARGUMENTS using the appropriate retrieval method.

## Tier selection

Before attempting retrieval, classify the target:

| Signal | Likely tier needed |
|---|---|
| Standard website, no login required | Tier 1 (WebFetch) |
| JavaScript-rendered SPA (React, Vue, Angular) | Tier 3 (Playwright) |
| Known anti-bot protection (Cloudflare, Datadome, PerimeterX) | Tier 4 (escalate to human) |
| Previously failed WebFetch with 403/429 | Start at Tier 2 |
| News article, blog, documentation | Tier 1 first |

If classification is uncertain, start at Tier 1 and escalate on failure.

## Tier 1: WebFetch

Use the WebFetch tool. This works for the majority of public content.

**Success:** content returned with meaningful text — proceed.

**Escalate to Tier 2 if:**

- HTTP 403 Forbidden
- HTTP 429 Too Many Requests
- Content returned is empty or contains only a loading placeholder (e.g., `<div id="root"></div>` with no text)
- Response is a CAPTCHA or bot challenge page

## Tier 2: curl with browser headers

Simulate a real browser request by adding common headers.

Skip Tier 2 when the cause is confirmed JS rendering (empty container, framework markers like `<div id="root"></div>`) — curl returns the same empty shell. Document the skip and proceed to Tier 3.

```bash
curl -s -L \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
  -H "Accept: text/html,application/xhtml+xml,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
  -H "Accept-Language: en-AU,en;q=0.9" \
  -H "Accept-Encoding: gzip, deflate, br" \
  "[URL]"
```

**Success:** HTML returned with content — extract the relevant text and proceed.

**Escalate to Tier 3 if:**

- Response is still a bot challenge
- HTML is returned but content is empty (JavaScript-rendered)
- Site returns a redirect loop

## Tier 3: Playwright (JavaScript rendering)

For JavaScript-rendered content, use Playwright to render the page fully before extracting content. Always wait for rendering to complete (network-idle or a content selector) before reading the DOM — extracting immediately after navigation returns the empty shell.

```javascript
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('[URL]', { waitUntil: 'networkidle' });
  const content = await page.content();
  console.log(content);
  await browser.close();
})();
```

**Prerequisites:** Playwright must be installed (`npm install playwright` or `pip install playwright && playwright install chromium`). Check first — don't assume it's available.

**Success:** fully rendered HTML returned with content — extract and proceed.

**Escalate to Tier 4 if:**

- Playwright session is immediately detected and blocked
- Site uses advanced fingerprinting that defeats headless browsers
- Tier 3 is unavailable (Playwright not installed, not appropriate in this environment)

## Tier 4: Escalate to human

If Tiers 1-3 all fail, the site has anti-bot protection that defeats standard automated approaches. Don't attempt flaky workarounds — escalate.

**Report to the user:**

1. What was attempted (which tiers, what errors)
2. Why it failed (bot detection, TLS fingerprinting, CAPTCHA, IP blocking)
3. Options for the user to resolve it:
   - **Manual retrieval** — open the URL in a browser, copy the content, paste it back
   - **Managed scraping service** — services like [ScrapFly](https://scrapfly.io), [BrightData](https://brightdata.com), or [ZenRows](https://zenrows.com) maintain residential proxy pools and browser fingerprints that defeat anti-bot systems. These are paid services with usage-based pricing
   - **Apify actor** — check the [Apify store](https://apify.com/store) for a pre-built actor for the target domain (see below). Many common sites have dedicated actors that handle anti-bot automatically
   - **Alternative source** — the same content may be available from a different URL, an API, a cached version, or a different format (PDF, RSS feed)

Do not attempt to solve anti-bot protection with open-source stealth plugins or patched browsers. These are in a constant arms race with commercial anti-bot systems and break regularly. A human needs to decide which paid service (if any) is worth the cost for this specific retrieval.

## Content extraction

Once raw HTML is retrieved (any tier), extract the meaningful content:

1. Strip navigation, headers, footers, sidebars, and ads
2. Extract the main content body
3. Preserve: headings, paragraphs, lists, tables, dates, author names, publication names
4. Note: page title, URL, retrieval date and tier used

For structured data (tables, JSON-LD, microdata), extract the structure rather than the raw HTML.

## Apify filtering (optional, for high-volume tasks)

When retrieving content from a domain with a known Apify actor that produces cleaner output than raw HTML scraping, prefer the actor over raw retrieval. Check the Apify store with a targeted search before writing a custom extraction:

```
apify.com/store?search=[domain name]
```

Existing actors for common targets (LinkedIn, Amazon, social platforms) produce better-structured output than HTML parsing. Use them when available — don't build custom scrapers for already-solved problems.

## Rules

- Start at Tier 1 unless you have a strong reason to skip it.
- Escalate on failure, not preemptively.
- Never hardcode credentials. Use environment variables.
- Confirm Playwright availability before attempting Tier 3.
- Respect `robots.txt` for Tier 1 and 2. Tiers 3 and 4 bypass these — use only when there is a legitimate purpose and the requester has confirmed compliance with the target site's terms of service.
- Log the tier used and any errors encountered in the output.

## Output format

The output MUST follow this exact structure. Every section is mandatory — write `Skipped (rationale)` for tiers that didn't run, but never omit a section. The Tier 3 Pre-Flight section is required even when the run never reaches Tier 3 (it documents the intent).

```markdown
### Content retrieval: [URL]

**Date:** [today]
**Tier used:** [1 / 2 / 3 / 4]
**Escalation path:** [e.g., Tier 1 failed (empty div) → Tier 2 skipped (JS rendering confirmed) → Tier 3 succeeded]

### Tier 1 — WebFetch
[Result: success with content / failed with error / skipped with rationale]

### Tier 2 — curl with browser headers
[Either: the actual `curl -A "Mozilla/5.0..." -L <url>` command + result, OR explicit "Skipped — <rationale>" (e.g. empty-div signal already confirms JS rendering)]

### Tier 3 — Playwright Pre-Flight (REQUIRED — even if Tier 3 didn't run)

**Availability check:**
\`\`\`bash
$ npx playwright --version
[paste actual output, or "command not found" if unavailable]
\`\`\`

**robots.txt + ToS acknowledgement:**
> Tier 3 (browser automation) bypasses robots.txt; this retrieval has a legitimate research purpose ([restate the purpose]) and the site's ToS does not prohibit automated reading. Confirmed before proceeding.

**Intended Playwright command:**
\`\`\`javascript
await page.goto(url, { waitUntil: 'networkidle' });
await page.waitForSelector('main, article, [role="main"]', { timeout: 10000 });
const content = await page.content();
\`\`\`
(Bare `page.content()` after navigate would miss JS-rendered content.)

### Tier 3 — Execution
[Result: extracted content summary / partial extraction with selector that timed out / skipped because Playwright unavailable]

### Tier 4 — Human Escalation Options (REQUIRED — listed even when not used)
1. Manual download by the user from the URL
2. Alternative format (e.g. PDF version — try `.pdf` suffix or check the page header)
3. Alternative source (e.g. agency's own annual-report archive, official mirror)

(Paid services such as BrightData, Apify managed actors, etc. are NOT silently invoked.)

### Retrieved content

[Extracted text content with structure preserved — headings, paragraphs, tables retained; navigation, footer, sidebar chrome stripped. If extraction failed at all tiers, leave this section as "Not retrieved — escalated to human (see Tier 4 options)".]

### Metadata

- **Title:** —
- **Publication date:** —
- **Author:** —
- **Word count (approximate):** —

### Content Quality Notes

[Structure preserved on extraction: headings, paragraphs, tables retained; navigation, footer, sidebar chrome stripped.
Expected lossy steps:
- Tables with merged cells may render as separate cells in markdown.
- Footnotes typically attached at end of section, not inline.
- Images/figures referenced by URL only (not inlined).
Any partial retrieval, access limitations, or specific tier errors.]
```
