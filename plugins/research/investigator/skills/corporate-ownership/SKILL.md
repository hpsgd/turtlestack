---
name: corporate-ownership
description: "Map a company's ownership chain, related entities, and director networks. Writes a conforming report (per report-conventions) to <engagement_dir>/corporate-ownership/<entity-slug>.md. Use for beneficial ownership investigation, M&A research, or understanding complex corporate structures. Full AU/NZ/UK/US registry coverage."
argument-hint: "<company name or registration number> [engagement_dir]"
user-invocable: true
allowed-tools: WebSearch, WebFetch, Read, Write, Bash
---

Map the corporate ownership structure for the named entity and write a conforming report.

## Step 0: Resolve arguments

Parse `$ARGUMENTS` as `<company name or registration number> [engagement_dir]`. Trailing path-shaped token is the engagement directory; otherwise default to `pwd`. Resolve to an absolute path.

## Step 1: Compute the output path

Subject slug: full company name, kebab-case, lowercase, ASCII (per report-conventions). Strip apostrophes and other punctuation; keep legal suffixes lower-cased (`pty-ltd`, `inc`, `gmbh`).

Examples:

- `Acme Corp Pty Ltd` → `acme-corp-pty-ltd`
- `O'Brien Holdings Inc` → `obrien-holdings-inc`

If the input is a registration number rather than a name, look up the legal name first and use that for the slug.

Output path: `$ENG/corporate-ownership/<slug>.md`

If a file already exists at that path, ask before overwriting.

## Step 2: Stage the report from the template

```bash
mkdir -p "$ENG/corporate-ownership"
cp "${CLAUDE_PLUGIN_ROOT}/templates/corporate-ownership.md" "$ENG/corporate-ownership/<slug>.md"
```

Replace placeholders in frontmatter:

| Placeholder | Replace with |
|---|---|
| `{SUBJECT}` | The legal company name |
| `{SUBTITLE}` | Engagement directory basename, title-cased; drop the line if no useful inference |
| `{DATE}` | Today's ISO date |

## Step 3: Investigation

### Primary registration

Look up the company's official registration record. This establishes the legal entity, jurisdiction, and current status.

**Australia:**

- [ASIC Connect](https://connect.asic.gov.au) — company extract: directors (current + historical), shareholders for proprietary companies, registered office, registration date, status
- [ABN Lookup](https://abn.business.gov.au) — ABN/ACN cross-reference, business name registration, GST registration status

**New Zealand:**

- [NZ Companies Office](https://companies.govt.nz) — director history, shareholding structure, registered office, annual returns, filing history

**United Kingdom:**

- [Companies House](https://find-and-update.company-information.service.gov.uk) — full filing history, director history, PSC register (persons with significant control = beneficial owners), accounts

**United States:**

- State secretary of state portals for private companies (coverage varies)
- [SEC EDGAR](https://www.sec.gov/cgi-bin/browse-edgar) for public companies — 10-K lists subsidiaries

**Global cross-reference:**

- [OpenCorporates](https://opencorporates.com) — cross-jurisdiction search, links entities across registries

### Beneficial ownership

Identify who ultimately controls or owns the company beyond the registered directors.

Sources:

- UK PSC register (Companies House) — requires disclosure of beneficial owners holding 25%+ control
- [ICIJ Offshore Leaks Database](https://offshoreleaks.icij.org) — offshore structures from leaked datasets (Panama Papers, Pandora Papers, etc.). Public data only.
- [ABN Lookup](https://abn.business.gov.au) for AU — parent entity relationships sometimes disclosed
- SEC 13D/13G filings for US public companies — major shareholder disclosures

Beneficial ownership disclosure requirements vary by jurisdiction. Absence of disclosed owners doesn't mean there aren't any — note this distinction.

### Director networks

Map all director appointments across the entity:

- Identify current and historical directors from the primary registration
- For each director, search their other company appointments:
  - AU: ASIC Connect director search
  - NZ: NZ Companies Office director search
  - UK: Companies House director search
  - Global: OpenCorporates officer search

Director networks often reveal undisclosed relationships between apparently separate entities.

### Subsidiary mapping

For the target company, identify subsidiaries and related entities:

- SEC 10-K Exhibit 21 (US public companies) — lists all subsidiaries
- Companies House group structures (UK)
- ASX/NZX annual report subsidiaries note (AU/NZ public companies)
- ASIC Connect — corporate group searches

### Related entities

Look for entities that share:

- The same registered address
- The same directors (cross-reference Director networks above)
- The same registered agent
- Similar naming patterns

OpenCorporates "related companies" and ViewDNS.info reverse WHOIS (for digital footprint overlap) can help here.

### Raise human-required steps explicitly

Beneficial-ownership tracing frequently reaches a registry that needs a paid extract, an in-person filing review, or a paywalled jurisdiction (offshore registries, certain US state portals). **Silently skipping these is the bug to avoid.** If the lookup is in scope and would meaningfully advance the ownership chain, raise it under `## Pending follow-up → Human-required steps`. Name the source, the access path, the rough cost, and what it would resolve. The assessor decides whether to spend the money.

If another investigator skill would resolve a gap (`/investigator:domain-intel` to triangulate via registered address, `/investigator:entity-footprint` for the digital side, a follow-on `/investigator:corporate-ownership` run on a parent entity), name it under `## Pending follow-up → Skill-required steps`.

Failed fetches (timeouts, rate limits) go under `## Pending follow-up → Re-fetches`.

## Step 4: Finalise the report

- Every template section heading must remain in the report. Use "None found." for empty sections rather than removing them.
- The three sub-sections under `## Pending follow-up` (Human-required steps, Skill-required steps, Re-fetches) also stay. Write "None." under any that are empty.
- Document the jurisdiction for every entity in the ownership chain.
- Distinguish between registered ownership (what the registry shows) and beneficial ownership (who actually controls the entity).
- Note when an ownership chain terminates in a jurisdiction with limited disclosure requirements (offshore structures, certain US states) — this is a significant finding, not a gap.
- Replace placeholder source rows with actual sources, tagged with tier per source-quality.
- Set `status: Final` once complete; optionally set `confidence: 0-4`.

## Rules

- Document the jurisdiction for every entity in the ownership chain.
- Distinguish between registered ownership (what the registry shows) and beneficial ownership (who actually controls the entity). These often differ.
- Note when an ownership chain terminates in a jurisdiction with limited disclosure requirements (offshore structures, certain US states) — this is a significant finding, not a gap.
- ICIJ data covers specific leaked datasets — it's a signal, not a comprehensive offshore registry. Absence from ICIJ doesn't mean no offshore structure.
- One file per invocation.
- **Silently skipping a paid or human-required lookup is a bug.** If the lookup exists and is in scope, raise it in `## Pending follow-up → Human-required steps`.

## Output

A single line: the absolute path to the written report.
