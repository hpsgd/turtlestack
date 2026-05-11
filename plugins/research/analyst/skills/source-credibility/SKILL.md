---
name: source-credibility
description: "Assess the credibility and reliability of a publication, website, or individual source. Writes a conforming report (per report-conventions) to <engagement_dir>/source-credibility/<source-slug>.md. Covers ownership, funding, editorial standards, track record, and known biases. Use before relying on a source for research or decisions."
argument-hint: "<source name or URL> [engagement_dir]"
user-invocable: true
allowed-tools: WebSearch, WebFetch, Read, Write, Bash
---

Assess the credibility of the named source and write a conforming report.

## Step 0: Resolve arguments

Parse `$ARGUMENTS` as `<source name or URL> [engagement_dir]`. Trailing path-shaped token is the engagement directory; otherwise default to `pwd`. Resolve to an absolute path.

## Step 1: Compute the output path

Subject slug: kebab-case, lowercase, ASCII (per report-conventions).

- For a publication: use the publication name. `The Guardian` → `the-guardian`
- For a URL: use the domain, with dots replaced by hyphens. `example.com.au` → `example-com-au`
- For an individual: `<lastname>-<firstname>`. `Jane Smith` → `smith-jane`

Output path: `$ENG/source-credibility/<slug>.md`

If a file already exists at that path, ask before overwriting (overwrite / write a `-2` sibling / abort).

## Step 2: Stage the report from the template

```bash
mkdir -p "$ENG/source-credibility"
cp "${CLAUDE_PLUGIN_ROOT}/templates/source-credibility.md" "$ENG/source-credibility/<slug>.md"
```

Replace placeholders in frontmatter:

| Placeholder | Replace with |
|---|---|
| `{SUBJECT}` | The source name as provided |
| `{SUBTITLE}` | Engagement directory basename, title-cased; drop the line if no useful inference |
| `{DATE}` | Today's ISO date |
| `{SOURCE_TYPE}` | One of: `news`, `trade`, `think-tank`, `government`, `academic`, `company`, `individual`, `aggregator` |

## Step 3: Identify the source type

Different source types have different credibility frameworks:

| Type | What to assess |
|---|---|
| News publication | Ownership, editorial standards, corrections policy, press council membership |
| Trade/industry publication | Who funds it, advertiser relationships, editorial independence |
| Think tank / research organisation | Funding sources, declared mission, publication peer review |
| Government / regulatory body | Statutory mandate, transparency obligations |
| Academic institution | Peer review process, retraction history, funding disclosure |
| Company / PR | By definition advocacy — assess transparency, not neutrality |
| Individual / expert | Credentials, institutional affiliation, track record, conflicts of interest |
| Aggregator / social platform | No editorial standard — assess the underlying sources it links to |

Set both the frontmatter `source_type` and the Source type section in the body.

## Step 4: Research and write into the staged file

Work through the sections in the staged file. Cite sources inline using the source-citations rule (deep links, access dates) and tag tier per source-quality.

### Ownership and funding

Who owns the source and who funds it? This doesn't determine whether individual pieces are accurate, but it shapes systematic biases and blind spots.

Search the source's "About" page, press releases, and public records. For significant publications:

- Media ownership databases: [MEAA](https://www.meaa.org) (AU media), Muck Rack, Columbia Journalism Review
- Company registration: ASIC Connect (AU), Companies House (UK) for ownership chains
- Known AU media ownership: News Corp AU (The Australian, Herald Sun, Daily Telegraph), Nine Entertainment (SMH, The Age, AFR), Seven West Media (The West Australian)
- NZ media ownership: NZME (NZHerald), Stuff

For think tanks and research organisations: check annual reports, funding pages, and donation transparency disclosures.

### Editorial standards

Does the source have published editorial standards? Assess:

- **Corrections policy:** does it publish corrections? How prominently?
- **Press council or regulatory membership:** AU — [ACMA](https://www.acma.gov.au) for broadcast, [Press Council](https://www.presscouncil.org.au) for print/digital; NZ — [Broadcasting Standards Authority](https://www.bsa.govt.nz), [NZ Press Council](https://www.presscouncil.org.nz)
- **Bylines and accountability:** are authors named and contactable?
- **Source attribution standards:** does it name sources or rely heavily on anonymous attribution?

Publications outside a press council or regulatory body have no external accountability mechanism.

### Track record

Has the source been accurate and reliable historically?

- Search for notable corrections, retractions, or failures
- Check [Media Bias / Fact Check](https://mediabiasfactcheck.com) — useful as a starting point, though it has its own limitations; use alongside other sources
- Look for: fabricated stories, misrepresentation of studies, consistent pattern of one-sided coverage on specific topics
- For academic sources: retraction databases (Retraction Watch, PubMed retraction notices)

A single error doesn't define a source. A pattern does.

### Declared mission and known biases

What does the source say its purpose is? Is that consistent with its output?

Most sources have a perspective — the question is whether they're transparent about it. A declared advocacy organisation that publishes transparently is more credible than a neutral-seeming publication with undisclosed funding.

Common bias patterns to identify:

- **Selection bias:** consistently covers certain topics, ignores others
- **Framing bias:** systematically frames issues in particular directions
- **Source bias:** routinely quotes from a narrow range of perspectives
- **Commercial bias:** coverage aligns with advertiser or funder interests

Note the distinction between bias (a systematic pattern) and error (a specific inaccuracy). Both matter but they're different problems.

### For individual experts

If the subject is an individual expert, assess:

- **Credentials:** does the claimed expertise match the topic? (A cardiologist commenting on climate science is outside their domain)
- **Institutional affiliation:** current role, past roles
- **Funding and conflicts:** has the expert received funding from parties with a stake in their conclusions?
- **Track record:** have their claims in this domain held up over time?
- **Citation and peer engagement:** are they cited by other credentialed people in their field, or primarily by media?

## Step 5: Fill the credibility assessment

Complete the Credibility assessment table with a rating (High / Medium / Low / Unknown) and a one-line evidence cell for each dimension. Then write:

- **Overall credibility:** one rating with a justifying sentence
- **Appropriate use:** what this source is reliable for, and what it's not

## Step 6: Finalise the report

- Replace placeholder source rows with actual sources, tagged with tier per source-quality.
- Set `status: Final` once complete; optionally set `confidence: 0-4`.

## Rules

- Credibility is not binary. Assess on a spectrum and be specific about which dimensions are strong or weak.
- Bias ≠ inaccuracy. A biased source can report individual facts accurately. A neutral-seeming source can publish errors.
- Funding creates incentives, not conclusions. Note it as a flag, not proof of corruption.
- No source is perfectly credible. The question is whether the credibility is sufficient for the intended use.
- Absence of information about a source is itself a credibility signal — opacity is a flag.
- One file per invocation. Don't write findings inline into chat.

## Output

A single line: the absolute path to the written report.
