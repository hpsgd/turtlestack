---
name: people-lookup
description: "Structured overview of a named individual's public presence: professional history, news coverage, academic work, people search aggregators, and company affiliations. Writes a conforming report (per report-conventions) to <engagement_dir>/people-lookup/<lastname>-<firstname>.md. Requires a complete authorisation gate before starting."
argument-hint: "<person name, with context: employer, location, or field> [engagement_dir]"
user-invocable: true
allowed-tools: WebSearch, WebFetch, Read, Write, Bash
---

Produce a structured overview of the named individual's public presence and write it to a deterministic file path.

> [!IMPORTANT]
> This skill requires the investigator agent's full authorisation gate before it can be invoked. Do not run this skill without a logged gate record (authorisation, purpose, scope, subject awareness). The gate is not optional. The gate itself stays in the session record — it is not embedded in the report file.

## Step 0: Resolve arguments

Parse `$ARGUMENTS` as `<person name with context> [engagement_dir]`. The trailing token, if it looks like a path (starts with `/` or `~`, or names a directory that exists), is the engagement directory. Otherwise default to `pwd`. Resolve to an absolute path.

The person name may include disambiguating context — keep the full string as the subject for searching. For the slug, use only the personal name component.

## Step 1: Compute the output path

Subject slug: `<lastname>-<firstname>`, kebab-case, lowercase, ASCII (strip diacritics, punctuation, apostrophes).

Examples:

- `Michael Graves` → `graves-michael`
- `María José O'Brien` → `obrien-maria-jose`

Output path: `$ENG/people-lookup/<slug>.md`

If a file already exists at that path, ask the user before overwriting (overwrite / write a `-2` sibling / abort).

## Step 2: Stage the report from the template

```bash
mkdir -p "$ENG/people-lookup"
cp "${CLAUDE_PLUGIN_ROOT}/templates/people-lookup.md" "$ENG/people-lookup/<slug>.md"
```

Then use the Edit tool to replace placeholders in the staged file:

| Placeholder | Replace with |
|---|---|
| `{SUBJECT}` | The personal name (e.g. "Michael Graves") |
| `{SUBTITLE}` | Engagement directory basename, title-cased; drop the `subtitle:` line if no useful inference |
| `{DATE}` | Today's ISO date (`YYYY-MM-DD`) |

## Step 3: Investigation

Run the investigation steps below and write findings into the staged file as you go. Every section heading in the template stays in the report — even if there is nothing to put under it. An empty section gets "None found." or "Out of scope per gate." A reader bundle-scanning multiple people-lookup reports needs to see the same structural shape every time. The headings are **mandatory**; the order is **fixed**.

Cite sources inline using the source-citations rule (deep links, access dates) and tag tier per source-quality.

### Identity verification — populate first

Confirm the subject's identity before running other searches. If you can't confirm identity, stop and ask the user for more disambiguation before proceeding — running searches against the wrong person is worse than no answer.

Record under `## Identity verification`: the confirmed identifiers (name, role, employer, location), the disambiguation method if the name is shared, and your confidence rating (0-4) per source-quality.

### Professional history

Search LinkedIn public profile, company website bios, and professional registrations.

For professionals in regulated fields, check licensing boards and record findings under `## Network and affiliations` (registrations) — but the role history itself lives under `## Professional history`.

- AU health practitioners: [AHPRA](https://www.ahpra.gov.au) (doctors, nurses, pharmacists, physios, psychologists, allied health)
- AU financial advisers: [ASIC Financial Advisers Register](https://moneysmart.gov.au/financial-advice/financial-advisers-register)
- AU lawyers: state law societies
- NZ health practitioners: [Medical Council NZ](https://www.mcnz.org.nz), [Nursing Council NZ](https://www.nursingcouncil.org.nz)
- NZ lawyers: [NZ Law Society](https://www.lawsociety.org.nz)
- NZ financial services: [FMA Financial Services Register](https://www.fma.govt.nz/compliance/registers-and-warnings/financial-service-providers/)
- US professionals: relevant state licensing boards

### Public presence — news, press, academic work, social

Search Google News (`site:news.google.com "[name]"`) and relevant industry press for the subject's name combined with professional context. Add qualifiers (employer, location, field) for names with many homonyms. For older coverage, check newspaper archives where accessible.

For researchers, academics, or published professionals:

- [Google Scholar](https://scholar.google.com)
- [ResearchGate](https://www.researchgate.net)
- [ORCID](https://orcid.org)
- [Semantic Scholar](https://www.semanticscholar.org)

Note publication count, citation count (very rough proxy for influence in field), and institutional affiliations.

People search aggregators — use for confirmation, not as primary source:

**US-based subjects:**

- [TruePeopleSearch](https://www.truepeoplesearch.com)
- [That's Them](https://thatsthem.com)
- [Radaris](https://radaris.com)

**AU-based subjects:**

- [White Pages AU](https://www.whitepages.com.au)
- [Australia411](https://www.australia411.com.au)

AU/NZ have no equivalent of the comprehensive US people-search aggregators. These directories are narrower and less cross-referenced — use for directory-style confirmation only.

**NZ-based subjects:**

- [White Pages NZ](https://www.whitepages.co.nz)

### Network and affiliations — directorships and registrations

Check for current and historical directorships or company registrations:

- AU: [ASIC Connect](https://connect.asic.gov.au) — director search across all registered companies
- NZ: [NZ Companies Office](https://companies.govt.nz) — director appointments, historical roles
- UK: [Companies House](https://find-and-update.company-information.service.gov.uk) — director history
- US public companies: [SEC EDGAR](https://www.sec.gov/cgi-bin/browse-edgar) for officer listings
- Global: [OpenCorporates](https://opencorporates.com) for cross-jurisdiction search

### Cross-reference

Before including any fact in the output, confirm it across at least two independent sources. A single people search result is a lead, not a finding. Flag single-source findings explicitly in the relevant section using `[single source]`.

### Raise human-required steps explicitly

Some sources can't be retrieved automatically — paid ASIC director extracts, paywalled databases, certain Companies House documents, court records requiring a subscription. **Silently skipping them is the bug to avoid.** If a reasonable lookup exists but can't run from this session, raise it under `## Pending follow-up → Human-required steps`. Name the source, the access path (URL or registry name), the rough cost, and what the lookup would resolve. The assessor decides whether to do it; a "skip for now" answer is fine.

If another investigator skill would resolve a gap (`/investigator:social-media-footprint`, `/investigator:public-records`, `/investigator:identity-verification`), name it under `## Pending follow-up → Skill-required steps` with a one-line rationale.

If a source failed mid-investigation (timeout, rate limit, transient error), log it under `## Pending follow-up → Re-fetches` with the URL and what it was meant to confirm.

## Step 4: Finalise the report

After populating the body sections:

- Every template section heading must remain in the report, even if empty. Use "None found." or "Out of scope per gate." rather than removing the section.
- The three sub-sections under `## Pending follow-up` (Human-required steps, Skill-required steps, Re-fetches) also stay. Write "None." under any that are empty.
- Replace the placeholder rows in Sources with the actual sources used, with tier tags (T1-T5) per source-quality and access dates.
- Set `status: Final` once content is complete; leave `Draft` if any section is incomplete.
- Optionally set `confidence: 0-4` based on coverage and source mix.

## Follow-on skills

A complete background check typically needs both this skill and `/investigator:public-records` — this skill covers professional history and licensing; `public-records` covers court filings and company directorships. Run both unless the gate scope explicitly limits to one.

If a company affiliation is found and the investigation scope includes the organisation, hand off to `/investigator:entity-footprint` (digital presence) or `/investigator:corporate-ownership` (ownership structure).

When the dossier plugin is in use, suggest `/dossier:consolidate <engagement_dir>` once the campaign is complete.

## Rules

- This skill cannot run without a complete authorisation gate. Stop if the gate record is missing.
- Cross-reference key facts across two independent sources before asserting them.
- Don't pivot from professional background into personal life — addresses, family, daily routine are out of scope unless the gate record explicitly includes them.
- Name disambiguation: if multiple people share the name, use context anchors (location, employer, field) to isolate the correct subject. Document the disambiguation method in the output.
- Absence is a finding. No press, no academic work, minimal professional footprint is a result — not a failed investigation.
- One file per invocation. Don't write findings inline into chat.
- **Mandatory section structure.** Every report uses the same template headings in the same order. An empty section gets "None found." — never delete the heading. Reports get bundled into a dossier where structural parity matters more than terse omission.
- **Silently skipping a paid or human-required lookup is a bug.** If the lookup exists and is in scope, raise it in `## Pending follow-up → Human-required steps`. Let the assessor decide whether to spend the money or the time.

## Output

A single line: the absolute path to the written report.

```
/Users/<user>/Assessments/<target>/people-lookup/<slug>.md
```
