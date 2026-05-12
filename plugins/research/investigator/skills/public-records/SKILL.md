---
name: public-records
description: "Search public records for a named individual: court records, business registrations, property (where public), professional licences, and electoral roll. Writes a conforming report (per report-conventions) to <engagement_dir>/public-records/<lastname>-<firstname>.md. Full AU/NZ/UK/US source coverage. Requires authorisation gate."
argument-hint: "<person name> [engagement_dir]"
user-invocable: true
allowed-tools: WebSearch, WebFetch, Read, Write, Bash
---

Search public records for the named individual and write a conforming report.

> [!IMPORTANT]
> This skill requires the investigator agent's full authorisation gate before invocation. Document the jurisdiction for every record found — public records laws vary significantly. The gate stays in the session record — it is not embedded in the report file.

## Step 0: Resolve arguments

Parse `$ARGUMENTS` as `<person name> [engagement_dir]`. Trailing path-shaped token is the engagement directory; otherwise default to `pwd`. Resolve to an absolute path.

If the gate record specifies a jurisdiction focus, lift it for use in Step 3 — it's not a CLI argument here.

## Step 1: Compute the output path

Subject slug: `<lastname>-<firstname>`, kebab-case, lowercase, ASCII (per report-conventions).

Output path: `$ENG/public-records/<slug>.md`

If a file already exists at that path, ask before overwriting.

## Step 2: Stage the report from the template

```bash
mkdir -p "$ENG/public-records"
cp "${CLAUDE_PLUGIN_ROOT}/templates/public-records.md" "$ENG/public-records/<slug>.md"
```

Replace placeholders in frontmatter:

| Placeholder | Replace with |
|---|---|
| `{SUBJECT}` | The personal name |
| `{SUBTITLE}` | Engagement directory basename, title-cased; drop the line if no useful inference |
| `{DATE}` | Today's ISO date |

## Step 3: Investigation

Write findings into the staged file as you go. Document jurisdiction for every record.

### Court records

Search court records for filings involving the subject as plaintiff, defendant, or party.

**Australia:**

- [AustLII](https://www.austlii.edu.au) — published court decisions and tribunal decisions (free, comprehensive coverage of published judgments)
- eCourts (NSW), VCAT (VIC) — state portals for specific jurisdictions
- Not all court records are published online in AU — many first-instance decisions are not publicly accessible

**New Zealand:**

- [NZLII](https://www.nzlii.org) — published court decisions
- [NZ Courts](https://www.courtsofnz.govt.nz) — Supreme Court, Court of Appeal, High Court judgments
- District Court decisions are less consistently published

**United States:**

- [CourtListener](https://www.courtlistener.com) — federal and state courts, free
- [PACER](https://pacer.uscourts.gov) — federal courts public search
- State court online portals (coverage varies by state)

**United Kingdom:**

- [The Gazette](https://www.thegazette.co.uk) — insolvency, bankruptcy, company winding-up notices
- BAILII for published judgments

### Business registrations

Has the subject been registered as a director or officer of any company?

**Australia:**

- [ASIC Connect](https://connect.asic.gov.au) — director search; current and historical appointments, insolvency notices
- [ABN Lookup](https://abn.business.gov.au) — ABN/ACN cross-reference, business name registration

**New Zealand:**

- [NZ Companies Office](https://companies.govt.nz) — director appointments, shareholding, historical roles, annual returns

**UK:**

- [Companies House](https://find-and-update.company-information.service.gov.uk) — director history, all registered companies

**US:**

- State secretary of state portals — coverage varies
- [OpenCorporates](https://opencorporates.com) — global cross-jurisdiction search

### Property records

Check within the scope defined by the gate record only. Property records reveal addresses — handle carefully.

**Australia:**

- Property records are managed by state-level land registries (NSW LRS, Titles Victoria, LINZ for NZ)
- These are largely restricted to paid searches or in-person access. Note as requiring manual follow-up if within scope.

**New Zealand:**

- [LINZ](https://www.linz.govt.nz) — land title searches (paid)

**United Kingdom:**

- [HM Land Registry](https://www.gov.uk/search-property-information-land-registry) — public property search (reveals addresses)

**United States:**

- County assessor public search — coverage and access vary significantly by county

### Professional licences

If the gate record covers professional background:

**Australia:**

- [AHPRA](https://www.ahpra.gov.au) — all registered health practitioners
- [ASIC Financial Advisers Register](https://moneysmart.gov.au/financial-advice/financial-advisers-register)
- State law societies for lawyers

**New Zealand:**

- [Medical Council of NZ](https://www.mcnz.org.nz)
- [Nursing Council of NZ](https://www.nursingcouncil.org.nz)
- [NZ Law Society](https://www.lawsociety.org.nz) — practising certificate search
- [FMA Financial Services Register](https://www.fma.govt.nz/compliance/registers-and-warnings/financial-service-providers/)

**United States:**

- State licensing boards for medicine, law, finance, real estate, engineering — check state-level

### Electoral roll

**United Kingdom:**

- UK electoral register — public search via local council

**United States:**

- Voter registration is publicly available in many states — availability and access vary

**Australia:**

- AU electoral rolls are NOT publicly searchable online. AEC rolls can only be inspected in person at AEC offices. Note this as checked but inaccessible via public search.

**New Zealand:**

- NZ Electoral Commission has limited public search capability. Note what's accessible.

### Raise human-required steps explicitly

Public-records work hits paid or restricted sources constantly — PACER subscription for US federal court records, AU property titles via state land registries, AEC electoral rolls only inspectable in person, certain court files held only on paper. **Silently skipping these is the bug to avoid.** When a lookup is in scope and would meaningfully advance the picture, raise it under `## Pending follow-up → Human-required steps`. Name the source, the access path (URL, registry name, office location), the rough cost or process, and what it would resolve. The assessor decides whether to invest the time or money.

If another investigator skill would resolve a gap (`/investigator:people-lookup` for professional context, `/investigator:corporate-ownership` to map a company structure surfaced here), name it under `## Pending follow-up → Skill-required steps`.

Failed fetches (timeouts, rate limits) go under `## Pending follow-up → Re-fetches`.

## Step 4: Finalise the report

- Every template section heading must remain in the report. Use explicit "None found." or "Not publicly searchable" rather than removing sections.
- The three sub-sections under `## Pending follow-up` (Human-required steps, Skill-required steps, Re-fetches) also stay. Write "None." under any that are empty.
- **The Source log table must include every named primary source for the subject's jurisdiction — searched, blocked, and not-checked alike.** Use `Searched: Yes / No / Blocked` to distinguish them. Sources that were skipped or deferred to a human still get a row. Do not move not-checked sources into the Gaps narrative as a substitute for a table entry.
- **Mandatory rows when the subject is AU:** AustLII, ASIC Connect, ASIC banned/disqualified persons register, ABN Lookup, AFSA bankruptcy register, NSW Caselaw (if NSW-connected). Each gets a row even if the result is `[no data]`, `[blocked]`, or `[deferred to human follow-up]`. Same pattern applies for NZ (NZLII, Companies Office), UK (BAILII, Companies House, The Gazette), and US (CourtListener, PACER, state SoS portals) — name the jurisdiction's primary sources and include them all.
- Note paid/restricted sources as requiring manual follow-up (and raise them under Pending follow-up → Human-required steps).
- Replace placeholder source rows with actual sources, tagged with tier per source-quality.
- Set `status: Final` once complete; optionally set `confidence: 0-4`.

## Follow-on skills

This skill covers formal records (court, licences, registrations). For professional history, social presence, and people-search aggregators, run `/investigator:people-lookup` alongside this skill — together they constitute a complete background check.

If company records surface a complex ownership structure worth mapping, hand off to `/investigator:corporate-ownership`.

If the assessor is relying on media reports of cases that don't appear in AustLII / NZLII / BAILII, suggest `/analyst:source-credibility` to assess the reporting outlet before treating media as a substitute for primary records.

When the dossier plugin is in use, suggest `/dossier:consolidate <engagement_dir>` once the campaign is complete.

## Rules

- Document jurisdiction for every record found. "Court records" without jurisdiction is meaningless.
- Note when a resource requires account creation or paid access — mark as checked but inaccessible, and suggest manual follow-up.
- AU property records are largely paid/restricted — don't attempt paid searches. Note as requiring manual follow-up.
- AU electoral rolls cannot be searched online — note clearly, don't skip without explanation.
- Distinguish between "no records found" (searched, nothing returned) and "not checked" (didn't search this source).
- One file per invocation.
- **Silently skipping a paid or human-required lookup is a bug.** If the lookup exists and is in scope, raise it in `## Pending follow-up → Human-required steps`. PACER subscriptions, AU property titles, AEC roll inspections, paywalled court archives — the assessor decides whether to spend.

## Output

A single line: the absolute path to the written report.
