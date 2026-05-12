---
name: domain-intel
description: "Investigate a domain's registration, DNS, certificates, hosting, and history using passive public sources. Writes a conforming report (per report-conventions.md) to <engagement_dir>/domain-intel/<domain-slug>.md. Use when mapping a domain's infrastructure or researching who owns/operates it."
argument-hint: "<domain name> [engagement_dir]"
user-invocable: true
allowed-tools: WebSearch, WebFetch, Read, Write, Bash
---

Produce a domain intelligence report for the given domain using passive public sources only. The report is written to a deterministic file path so the dossier plugin and other consumers can find it.

## Step 0: Resolve arguments

Parse `$ARGUMENTS` as `<domain> [engagement_dir]`:

- The first whitespace-separated token is the domain (required)
- If a second token is supplied, it is the engagement directory; otherwise default to `pwd`
- Resolve the engagement directory to an absolute path

```bash
DOMAIN="<first token, lowercase>"
ENG_RAW="<second token, or empty>"
case "${ENG_RAW:-$(pwd)}" in
  /*) ENG="${ENG_RAW:-$(pwd)}" ;;
  *) ENG="$(pwd)/${ENG_RAW}" ;;
esac
```

The domain must look like a domain (one or more dot-separated labels, no scheme, no path). If the user passed `https://example.com/foo`, strip to `example.com` and note the normalisation in the output.

## Step 1: Compute the output path

The slug for a domain replaces dots with hyphens (per report-conventions). The output path is:

```
$ENG/domain-intel/<domain-slug>.md
```

Examples:

- `acmecorp.com.au` → `domain-intel/acmecorp-com-au.md`
- `example.com` → `domain-intel/example-com.md`

If a file already exists at that path, ask the user before overwriting (offer overwrite / write a sibling with a `-2` suffix / abort).

## Step 2: Stage the report from the template

Copy the template at `${CLAUDE_PLUGIN_ROOT}/templates/domain-intel.md` to the output path, then substitute placeholders in the frontmatter:

| Placeholder | Replace with |
|---|---|
| `{SUBJECT}` | The normalised domain |
| `{SUBTITLE}` | The engagement directory's basename, title-cased; or leave the placeholder line for the user to fill if no useful inference is possible |
| `{DATE}` | Today's ISO date (`YYYY-MM-DD`) |

If `{SUBTITLE}` can't be inferred (e.g. the engagement directory is `pwd` and `pwd` is a generic location), drop the `subtitle:` line entirely rather than leaving an unfilled placeholder.

```bash
mkdir -p "$ENG/domain-intel"
cp "${CLAUDE_PLUGIN_ROOT}/templates/domain-intel.md" "$ENG/domain-intel/<slug>.md"
# then use the Edit tool to replace placeholders — don't sed-edit the file out-of-band
```

## Step 3: Investigation

Run the investigation steps below and write findings into the staged file as you go. Each finding goes under its existing heading in the template — don't create new top-level headings unless something genuinely doesn't fit. Cite sources inline using the source-citations rule (deep links, access dates).

### Registration

Look up WHOIS to establish registrant, registrar, creation/expiry dates, and nameservers.

Choose the right registry for the TLD:

- **.com/.net/.org and generic TLDs:** [who.is](https://who.is) or registrar lookup
- **.au domains:** [auDA WHOIS](https://whois.audns.net.au) — the authoritative .au registry
- **.nz domains:** [NZRS WHOIS](https://whois.nic.nz) — InternetNZ
- **.uk domains:** Nominet WHOIS
- **Country TLDs generally:** [IANA WHOIS](https://www.iana.org/whois) redirects to the authoritative registry

Privacy protection is a finding, not a failure — log it and continue with DNS and certificate transparency.

### DNS records

Fetch DNS records via [MXToolbox](https://mxtoolbox.com) or [dnsdumpster.com](https://dnsdumpster.com).

Collect: A, AAAA, MX, TXT, NS, CNAME records.

TXT records frequently reveal: email providers (Google Workspace, Microsoft 365), SPF/DKIM configuration, third-party service ownership verification (Stripe, HubSpot, Salesforce), and site verification codes.

### Certificate transparency

Search [crt.sh](https://crt.sh) for all certificates issued to the domain and its subdomains.

Certificate transparency reveals:

- All subdomains (including internal-looking names that suggest architecture)
- Naming patterns (environments: dev/staging/prod; regions; services)
- Certificate issuer (Let's Encrypt = self-managed; DigiCert/Sectigo = often enterprise)
- Certificate history (when the domain started using HTTPS; any gaps)

### ASN and hosting

Use [ipinfo.io](https://ipinfo.io) or [BGP.he.net](https://bgp.he.net) to identify:

- Hosting provider and ASN
- IP range the domain resolves to
- Geographic location of hosting

Cross-reference with MX records to identify email hosting (separate from web hosting is common).

### Reverse WHOIS and related domains

Search [ViewDNS.info](https://viewdns.info) for other domains registered to the same entity (registrant name or email where not privacy-protected). This can reveal related brands, acquired properties, or shell domains.

### Historical data

- [Wayback Machine](https://web.archive.org) — what has the site looked like historically? When was it first indexed? Any major content changes?
- SecurityTrails public tier — DNS history and IP history where available

Historical gaps (domain registered but no Wayback content for a period) can be significant.

### Raise human-required steps explicitly

Some sources need a paid subscription or commercial access — DomainTools paid WHOIS history, SecurityTrails/Farsight commercial passive DNS, trademark or registration disputes that need legal counsel. **Silently skipping them is the bug to avoid.** If a reasonable lookup exists but can't run from this session, raise it under `## Pending follow-up → Human-required steps`. Name the source, the access path, the rough cost, and what it would resolve. The assessor decides whether to spend.

If another investigator skill would resolve a gap (`/investigator:ip-intel` on the hosting ASN, `/investigator:entity-footprint` for the wider org picture, follow-on `/investigator:domain-intel` on a related domain), name it under `## Pending follow-up → Skill-required steps` with a one-line rationale.

If a source failed mid-investigation (timeout, rate limit, transient error), log it under `## Pending follow-up → Re-fetches` with the URL and what it was meant to confirm.

## Step 4: Finalise the report

After populating the body sections:

- Every template section heading must remain in the report, even if empty. Use "None found." or "Privacy-protected, unable to determine." rather than removing sections.
- The three sub-sections under `## Pending follow-up` (Human-required steps, Skill-required steps, Re-fetches) also stay. Write "None." under any that are empty.
- Strip the placeholder rows in the Sources section and replace with the actual sources used, with tier tags (T1-T5) per source-quality and access dates.
- Set `status: Final` in the frontmatter once content is complete (Draft is fine if any section is incomplete).
- Optionally set `confidence: 0-4` based on overall source quality and coverage.

## Follow-on skills

Domain intel often surfaces leads worth deeper investigation:

- **Multiple related domains found** → run this skill again per domain, or use `/investigator:entity-footprint` for the full organisational picture
- **IP addresses from A/AAAA records worth investigating** → `/investigator:ip-intel`
- **Organisation behind the domain** → `/investigator:corporate-ownership` for the legal entity structure

When the dossier plugin is in use, suggest `/dossier:consolidate <engagement_dir>` once the campaign is complete.

## Rules

- Passive methods only. Never attempt active scanning, port enumeration, or authenticated access.
- Log every source used, including those that returned no results.
- Privacy-protected WHOIS is a finding, not a failure — note it and continue with other sources.
- Don't pivot from infrastructure investigation into profiling individuals whose names appear in records. Note the name exists if relevant; don't expand.
- Absence is data. A domain with no Wayback history, a brand-new registration, or no TXT records is telling you something.
- One file per invocation. Don't append to or overwrite an existing report without confirming. Don't write findings inline into chat — they belong in the file.

## Output

A single line: the absolute path to the written report.

```
/Users/<user>/Assessments/<target>/domain-intel/<slug>.md
```
