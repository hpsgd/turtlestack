---
name: entity-footprint
description: "Map an organisation's complete public digital presence: domains, web presence, social profiles, apps, code repositories, job postings, and regulatory filings. Writes a conforming report (per report-conventions) to <engagement_dir>/entity-footprint/<entity-slug>.md."
argument-hint: "<organisation name> [engagement_dir]"
user-invocable: true
allowed-tools: WebSearch, WebFetch, Read, Write, Bash
---

Map the public digital footprint of the named organisation and write a conforming report.

## Step 0: Resolve arguments

Parse `$ARGUMENTS` as `<organisation name> [engagement_dir]`. Trailing path-shaped token is the engagement directory; otherwise default to `pwd`. Resolve to an absolute path.

## Step 1: Compute the output path

Subject slug: full organisation name, kebab-case, lowercase, ASCII (per report-conventions). Strip apostrophes and other punctuation; keep legal suffixes lower-cased.

Examples:

- `Acme Corp Pty Ltd` → `acme-corp-pty-ltd`
- `Stripe, Inc.` → `stripe-inc`

Output path: `$ENG/entity-footprint/<slug>.md`

If a file already exists at that path, ask before overwriting.

## Step 2: Stage the report from the template

```bash
mkdir -p "$ENG/entity-footprint"
cp "${CLAUDE_PLUGIN_ROOT}/templates/entity-footprint.md" "$ENG/entity-footprint/<slug>.md"
```

Replace placeholders in frontmatter:

| Placeholder | Replace with |
|---|---|
| `{SUBJECT}` | The organisation name |
| `{SUBTITLE}` | Engagement directory basename, title-cased; drop the line if no useful inference |
| `{DATE}` | Today's ISO date |

## Step 3: Investigation

### Owned domains

Establish the primary domain, then discover related ones.

- **Reverse WHOIS:** search [ViewDNS.info](https://viewdns.info) for domains registered to the same entity (by registrant name or email where not privacy-protected)
- **Certificate transparency:** search [crt.sh](https://crt.sh) for the primary domain — wildcard and SANs often reveal subdomain patterns and product domains
- **Search variation:** `"[org name]" site:domain` patterns, regional variants (`.com.au`, `.co.nz`), product-specific domains, acquired brand domains

### Web presence

- Primary site and its key sections (products, pricing, about, careers)
- Regional variants or localised sites
- Documentation or developer portals (often `docs.`, `developers.`, `api.`)
- Blog or content properties
- Status page (`status.`)

Use Wayback Machine to understand when properties were established and how they've evolved.

### Social profiles

Search each platform:

| Platform | What to look for |
|---|---|
| LinkedIn | Company page, employee count, key executives |
| Twitter/X | Official account, follower count, posting cadence |
| GitHub | Organisation account, public repos, contributor patterns |
| YouTube | Product demos, conference talks, webinar archives |
| Facebook | Company page (often useful for older or B2C companies) |

The absence of a platform presence is itself a signal — a tech company with no GitHub presence is unusual.

### App store presence

Search iOS App Store and Google Play for the organisation's name.

Published apps reveal:

- Product scope beyond the website description
- User ratings and review sentiment (public)
- Update frequency (activity signal)
- Tech stack signals from app categories and permissions

### Code repositories

[GitHub](https://github.com) organisation search:

- Public repositories — what they've open-sourced
- Tech stack patterns across repos
- Contributor patterns (team size, activity, geography)
- Stars and forks as adoption signal for developer-facing products

Also check [GitLab](https://gitlab.com) for organisations with non-GitHub presence.

### Job postings as leading indicator

Current job postings reveal operational reality more reliably than press releases.

- Company careers page
- LinkedIn Jobs
- [Seek](https://www.seek.com.au) / [Seek NZ](https://www.seek.co.nz) for AU/NZ companies

Look for: technology stack requirements, new functional areas being built out, seniority distribution of open roles, hiring volume relative to declared company size.

### Press and regulatory filings

- News search for the last 12 months
- Regulatory filings: [ASIC Connect](https://connect.asic.gov.au) (AU), [NZ Companies Office](https://companies.govt.nz) (NZ), Companies House (UK), SEC EDGAR (US public companies)
- AU broadcast/telco entities: [ACMA](https://www.acma.gov.au) register
- Any relevant industry-specific regulatory bodies

## Step 4: Finalise the report

- Confirm every section has either content or an explicit "none found" note. A minimal footprint is itself a finding.
- Replace placeholder source rows with actual sources, tagged with tier per source-quality.
- Set `status: Final` once complete; optionally set `confidence: 0-4`.

## Follow-on skills

This skill maps the surface of an organisation's digital presence. For deeper investigation of specific assets found here:

- **Domains discovered** → `/investigator:domain-intel` for registration, DNS, cert transparency, and hosting detail
- **IP addresses surfaced** → `/investigator:ip-intel` for ownership, ASN, and reputation
- **Ownership structure questions** → `/investigator:corporate-ownership`

When the dossier plugin is in use, suggest `/dossier:consolidate <engagement_dir>` once the campaign is complete.

## Rules

- Stay on organisational targets. If investigation reveals individual employee details, note the data exists but don't expand.
- Passive only — no authenticated access, no scraping behind login walls.
- Every claim about the organisation's footprint needs a source.
- A minimal footprint is a finding. A company that's hard to find online is telling you something.
- One file per invocation.

## Output

A single line: the absolute path to the written report.
