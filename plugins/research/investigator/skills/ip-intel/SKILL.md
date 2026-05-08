---
name: ip-intel
description: "Investigate an IP address: ownership, hosting provider, ASN, reputation, and associated infrastructure. Writes a conforming report (per report-conventions) to <engagement_dir>/ip-intel/<ip-slug>.md. Passive sources only — no active scanning."
argument-hint: "<IP address or CIDR range> [engagement_dir]"
user-invocable: true
allowed-tools: WebSearch, WebFetch, Read, Write, Bash
---

Produce an IP intelligence report using passive public sources only, and write it to a deterministic file path.

## Step 0: Resolve arguments

Parse `$ARGUMENTS` as `<IP or CIDR> [engagement_dir]`. Trailing path-shaped token is the engagement directory; otherwise default to `pwd`. Resolve to an absolute path.

The IP must be a valid IPv4 or IPv6 literal, optionally with a CIDR suffix.

## Step 1: Compute the output path

Subject slug:

| Form | Slug |
|---|---|
| IPv4 (`203.0.113.42`) | dots → hyphens (`203-0-113-42`) |
| IPv4 with CIDR (`203.0.113.0/24`) | dots → hyphens, slash → underscore (`203-0-113-0_24`) |
| IPv6 (`2001:db8::1`) | colons → hyphens; for compactness, keep zero-compressed form (`2001-db8--1`) |

Output path: `$ENG/ip-intel/<slug>.md`

If a file already exists at that path, ask before overwriting.

## Step 2: Stage the report from the template

```bash
mkdir -p "$ENG/ip-intel"
cp "${CLAUDE_PLUGIN_ROOT}/templates/ip-intel.md" "$ENG/ip-intel/<slug>.md"
```

Replace placeholders in frontmatter:

| Placeholder | Replace with |
|---|---|
| `{SUBJECT}` | The IP address or CIDR string (verbatim) |
| `{SUBTITLE}` | Engagement directory basename, title-cased; drop the line if no useful inference |
| `{DATE}` | Today's ISO date |

## Step 3: Investigation

### Ownership and geolocation

Use [ipinfo.io](https://ipinfo.io) for the primary lookup: ASN, organisation name, geolocation.

Then cross-reference with the authoritative regional internet registry for the IP's allocation:

| Region | Registry | URL |
|---|---|---|
| North America | ARIN | [arin.net](https://arin.net) |
| Europe, Middle East, Central Asia | RIPE NCC | [ripe.net](https://ripe.net) |
| Asia Pacific (including AU/NZ) | APNIC | [apnic.net](https://apnic.net) |
| Latin America | LACNIC | [lacnic.net](https://lacnic.net) |
| Africa | AFRINIC | [afrinic.net](https://afrinic.net) |

The RIR record gives the authoritative allocation — who IANA assigned the block to, and any sub-allocations.

### Reverse DNS

Look up the PTR record via [MXToolbox](https://mxtoolbox.com) reverse lookup.

Reverse DNS naming conventions often reveal:

- The operator's naming scheme (`mail.company.com`, `api-prod-1.cloud.company.com`)
- Hosting provider patterns (`compute.amazonaws.com`, `servers.ovh.net`)
- Geographic or functional naming (`syd01.hosting.example.com` suggests Sydney data centre)

### Reputation

Check multiple reputation sources — a clean result on one doesn't mean clean everywhere:

- [VirusTotal](https://www.virustotal.com) — malware associations, URL/file detections tied to this IP
- [AbuseIPDB](https://www.abuseipdb.com) — crowdsourced abuse reports (spam, scanning, brute force)
- [Shodan](https://www.shodan.io) public search — services exposed, banners, historical ports (search only, no active scanning)

Shodan data may be stale. It's a historical record of what was observed, not necessarily current state.

### Related infrastructure

- Other IPs in the same ASN range that share patterns with this IP
- Reverse IP lookup on [ViewDNS.info](https://viewdns.info) — other domains hosted on this IP
- Shared hosting detection — if multiple unrelated domains resolve here, it's likely a shared hosting environment

### Historical context

Has this IP been notable before? Search:

- `[IP address] incident` / `[IP address] breach` / `[IP address] attack`
- Threat intelligence feeds with public exposure (GreyNoise, pulsedive)
- Any major ownership changes (ASN transfers, RIPE records)

## Step 4: Finalise the report

- Confirm every section has either content or an explicit "none found" note.
- Replace placeholder source rows with actual sources, tagged with tier per source-quality.
- Set `status: Final` once complete; optionally set `confidence: 0-4`.

## Rules

- Passive methods only. Do not port scan, banner grab, or interact with any service on this IP.
- Shodan is a passive source — use its search interface, not any active scanning capability.
- If the IP belongs to a major cloud provider (AWS, Azure, GCP, Cloudflare), note that attribution to the provider doesn't identify the actual customer.
- A clean reputation score doesn't mean the IP is benign. It means it hasn't been reported. State this distinction clearly.
- One file per invocation.

## Output

A single line: the absolute path to the written report.
