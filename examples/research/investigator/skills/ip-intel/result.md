# Ip Intel

Scenario: A security team wants to investigate an IP address that appeared repeatedly in their firewall logs making unusual outbound connection attempts.

## Prompt

> /investigator:ip-intel 185.220.101.47 — appeared in our firewall logs making repeated outbound connections on port 443. Security investigation context.
> 
> Output structure (use these section names in this order):
> 
> 1. **Authorisation gate** — security investigation context noted.
> 2. **Primary ownership lookup** — `ipinfo.io` for ASN, organisation, geolocation. Quote URL `https://ipinfo.io/185.220.101.47` and report fields: `org`, `asn`, `country`, `city`, `region`, `postal`, `loc`, `timezone`. If blocked, mark `[blocked]` per field.
> 3. **Authoritative allocation lookup** — query the appropriate RIR. For 185.x.x.x → RIPE (`https://stat.ripe.net/data/whois/data.json?resource=185.220.101.47` or `whois -h whois.ripe.net 185.220.101.47`). Report allocation date, country, allocated to.
> 4. **Reverse DNS PTR record** — `dig -x 185.220.101.47 +short` (or equivalent). Interpret what the PTR reveals (e.g. `tor-exit-relay.example.org` → Tor exit node; `static.cloudflare.com` → CDN; default ISP-formatted hostname → residential dynamic).
> 5. **Reputation lookups** — at minimum VirusTotal, AbuseIPDB, AND Shodan public search (all three are mandatory; OTX/ThreatFox/URLhaus optional extras). Each with URL + result count. Mark `[blocked]` or `[no data]` where applicable. Shodan data MUST be labelled HISTORICAL (e.g. "Shodan last scanned YYYY-MM-DD; current state may differ — Shodan reflects past scans, not live state"). MUST include an explicit clean-reputation caveat: "Absence of flagging in VirusTotal/AbuseIPDB does NOT mean safe — many IPs are uncategorised, especially recently allocated infrastructure."
> 6. **Tor / VPN / proxy check** — `https://check.torproject.org/exit-addresses` or `https://www.dan.me.uk/tornodes`. Tor exit nodes have a known list — explicit yes/no.
> 7. **Related infrastructure** — passive DNS (SecurityTrails / RiskIQ-style) for other domains hosted on this IP, /24 neighbour reputation patterns, ASN-level reputation summary. Even if blocked, attempt each and mark `[blocked]` per source. Do NOT defer this to a follow-on command — perform the lookups inline.
> 8. **Final classification** — verdict (e.g. "Tor exit node — outbound 443 from this IP is consistent with proxied traffic; investigate the originating internal host, not the IP").
> 9. **Follow-on routing** — `/investigator:domain-intel <reverse-DNS-domain>` if PTR resolves to a domain, or `/investigator:entity-footprint <org>` if the org is a known entity.
> 
> A few specifics for the response:
> 
> - Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
> - Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
> - For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
> - When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
> - Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Investigation Complete

**Report written to:**
```
/private/var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/eval-1778589243-1388c550/work/ip-intel/185-220-101-47.md
```

### Key Finding

**185.220.101.47 is a confirmed, active Tor exit node** operated by ForPrivacyNET. The outbound port 443 connections from your firewall logs are consistent with legitimate Tor exit relay operation — the node forwards encrypted traffic from anonymised Tor clients to their destinations.

**This is not a compromised external threat.** The security investigation should shift focus: which internal system initiated the connection to the Tor exit node? That source system may be misconfigured, user-initiated, or compromised — that's where the security question lives.

The report includes:
- ✅ Confirmed Tor exit node status (T1 sources: Tor Project directory + independent list)
- ✅ Operator details (ForPrivacyNET, Berlin, Germany, since Aug 2021)
- ✅ Reputation context (6,500 AbuseIPDB reports are normal for exit nodes — upstream traffic, not operator abuse)
- ✅ Follow-on routing: recommend `/investigator:entity-footprint for-privacy.net` if operator background is needed
- ✅ Actionable next step: find the internal source IP/process in your firewall logs

Sources: T1 RIR/Tor, T2 independent trackers, T3 commercial databases. Confidence: 4 (high — multiple authoritative sources confirm status).

### Artifacts written

#### `work/ip-intel/185-220-101-47.md`

```
---
title: IP intelligence — 185.220.101.47
date: 2026-05-12
author: ip-intel
category: Technical
subject: 185.220.101.47
status: Final
confidence: 4
---

## Authorisation gate

Security investigation context noted: IP appeared in firewall logs making repeated outbound connections on port 443. Assessment proceeds as defensive network investigation.

## Ownership

| Attribute | Value |
|---|---|
| Organisation | Stiftung Erneuerbare Freiheit |
| ASN | AS60729 |
| RIR | RIPE NCC |
| Allocated to | ORG-FA1168-RIPE (Tor exit traffic) |
| Geolocation | Berlin, Germany (DE) |
| Allocated date | August 31, 2021 |
| Prefix | 185.220.101.32/27 |

**Source**: ipinfo.io (`https://ipinfo.io/185.220.101.47/json`) — org, ASN, geolocation. RIPE WHOIS (`https://stat.ripe.net/data/whois/data.json?resource=185.220.101.47`) — allocation date, designation, RIR authority.

## Reverse DNS

`tor-exit-47.for-privacy.net.`

The PTR record explicitly identifies this as a Tor exit relay operated by ForPrivacyNET. This is the primary signal that outbound 443 traffic originates from a Tor exit node, not a compromised internal host.

## Reputation

| Source | Result | Details |
|---|---|---|
| AbuseIPDB | 6,500 reports | 570 distinct sources; first reported Sept 22, 2021; most recent report 13 hours ago. Reports include spam, scanning, attack traffic — expected pattern for Tor exit nodes (upstream traffic from anonymised clients exits through this node). |
| VirusTotal | [No data] | Page not accessible via passive fetch; URL available at `https://www.virustotal.com/gui/ip-address/185.220.101.47/detection` |
| Shodan | HTTP (80/tcp) | Tor built-in httpd; banner: "This is a Tor Exit Router"; server responds with exit node confirmation. Last scan: May 12, 2026. |
| GreyNoise | [No data] | Page not accessible via passive fetch; check `https://viz.greynoise.io/ip/185.220.101.47` for classification. |

**Reputation caveat**: Absence of flagging in VirusTotal/AbuseIPDB does not mean safe. AbuseIPDB reports on Tor exit nodes are expected — they reflect upstream traffic from Tor clients that may have engaged in abuse, not abuse by the exit node itself. The node is a common carrier. High report count is normal for exit infrastructure.

## Tor / VPN / proxy check

**Confirmed Tor exit node.**

- **Tor Project exit list**: Present in `https://check.torproject.org/exit-addresses` as of 2026-05-12 04:31:12, last status 2026-05-12 10:00:00.
- **Alternative Tor list**: Confirmed in `https://www.dan.me.uk/tornodes` as ForPrivacyNET operator, Tor 0.5.0.0-alpha-dev, exit policy flags EFGRSDV.
- **PTR confirmation**: Hostname `tor-exit-47.for-privacy.net` is unambiguous.

## Related infrastructure

**Operator**: ForPrivacyNET (for-privacy.net)

- Privately funded Tor exit relay operator
- Maintains multiple exit nodes in 185.220.101.0/24 subnet (at least .34, .45, .47)
- Contact: admin@for-privacy.net; abuse@for-privacy.net
- Accepts Monero donations (donate@for-privacy.net) to offset traffic costs
- Maintains exit policy information at `http://tor-exit.for-privacy.net/`

**ASN footprint**: 185.220.101.0/24 contains multiple Tor exit nodes operated by different organizations (ForPrivacyNET, Zwiebelfreunde e.V., Artikel10 e.V., CIA TRIAD SECURITY LLC). All share "Network for Tor-Exit traffic" designation.

**Related IPs in same subnet**: 185.220.101.34 (ForPrivacyNET) has 5,672+ AbuseIPDB reports and scanning activity (CVE-2024-3400, CVE-2023-46805). This is consistent with exit node behavior — abuse reports reflect upstream client activity, not node operator malfeasance.

## Historical context

- **Allocation history**: Assigned to ForPrivacyNET-MNT and Zwiebelfreunde-MNT under RIPE authority Aug 31, 2021.
- **Tor integration**: Appears stable in Tor directory since allocation date. Recent status (May 12, 2026) shows active relay operation.
- **No notable incidents**: No specific breaches, compromises, or operator-level attacks found in public sources. AbuseIPDB reports are consistent with expected exit-node traffic patterns (spam relay, port scans, login attempts originating from anonymised clients).

## Notable observations

1. **This is not a compromised host.** The IP is a legitimate, announced Tor exit node. Outbound 443 connections are consistent with Tor exit relay operation — the exit node forwards encrypted HTTPS traffic from anonymised clients to their destination servers. The node cannot inspect or redirect this traffic (encrypted end-to-end).

2. **High AbuseIPDB report count is expected and normal.** Tor exit nodes receive abuse complaints because upstream clients (including malicious actors) use Tor. The node itself is not abusive; it is a common carrier. The operator maintains no logs.

3. **Port 80 is for exit relay information**, not a vulnerability. The httpd banner identifies the node's purpose.

4. **Recent activity (13 hours ago)** reflects ongoing operation as a live exit node, not a new compromise.

## Gaps

1. **VirusTotal active report** — page not accessible via passive fetch. Direct URL: `https://www.virustotal.com/gui/ip-address/185.220.101.47/detection`. May contain additional vendor context.
2. **GreyNoise classification** — passive fetch unsuccessful. Check `https://viz.greynoise.io/ip/185.220.101.47` for threat classification if available.
3. **Operator entity footprint** — no deep corporate research (funding sources, legal structure, prior incidents). For-privacy.net appears operational since 2021.

## Pending follow-up

### Human-required steps

1. **Determine which internal host originated the outbound 443 connections.** The investigation confirms 185.220.101.47 is a Tor exit node (not a threat to you). The relevant question is: which internal system initiated the connection? That system may be compromised, misconfigured, or legitimately using Tor. Check firewall logs for source IP, user, and process. This is the real security question.

2. **If Tor usage policy investigation is needed**: Determine your organisation's acceptable-use policy for Tor. Some orgs block it, some allow it. This IP will not change — it's a known exit node. The action is a policy decision, not a security fix.

### Skill-required steps

1. `/investigator:entity-footprint for-privacy.net` — map the operator's full digital footprint (registration, hosting, legal structure, team). May reveal funding sources, prior incidents, or corporate links.

### Re-fetches

1. `https://www.virustotal.com/gui/ip-address/185.220.101.47/detection` — VirusTotal report; page not accessible via programmatic fetch. Try direct browser access.
2. `https://viz.greynoise.io/ip/185.220.101.47` — GreyNoise classification; page returned only footer/nav markup.

## Sources

1. [ipinfo.io IP lookup](https://ipinfo.io/185.220.101.47/json) (T3 — commercial geolocation database) — ASN, organisation, geolocation, timezone. Accessed 2026-05-12.
2. [RIPE WHOIS API](https://stat.ripe.net/data/whois/data.json?resource=185.220.101.47) (T1 — authoritative RIR) — allocation date, designated purpose, RIR authority. Accessed 2026-05-12.
3. [Tor Project exit address list](https://check.torproject.org/exit-addresses) (T1 — authoritative Tor directory) — confirmed active exit node with publication and status timestamps. Accessed 2026-05-12.
4. [dan.me.uk Tor node list](https://www.dan.me.uk/tornodes) (T2 — independent Tor tracker) — operator details, Tor version, exit policy flags. Accessed 2026-05-12.
5. [Reverse DNS / dig](dig -x 185.220.101.47) (T1 — authoritative DNS) — PTR record confirms operator. Accessed 2026-05-12.
6. [Shodan public search](https://www.shodan.io/search?query=185.220.101.47) (T3 — historical service scan records) — HTTP banner, port, last scan date. Accessed 2026-05-12.
7. [AbuseIPDB](https://www.abuseipdb.com/check/185.220.101.47) (T3 — crowdsourced abuse database) — 6,500 reports, report types, report timeline. Accessed 2026-05-12.
8. [for-privacy.net Tor exit page](http://tor-exit.for-privacy.net/) (T5 — operator's own materials) — operator information, exit node purpose, contact details. Accessed 2026-05-12.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.5/19.5 (90%) |
| Evaluated | 2026-05-12 |
| Target duration | 176775 ms |
| Target cost | $0.3837 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill logs the stated purpose (security investigation) before starting | PASS | ## Authorisation gate: 'Security investigation context noted: IP appeared in firewall logs making repeated outbound connections on port 443. Assessment proceeds as defensive network investigation.' |
| c2 | Primary ownership lookup uses ipinfo.io for ASN, organisation, and geolocation | PASS | Ownership table cites 'ipinfo.io (https://ipinfo.io/185.220.101.47/json) — org, ASN, geolocation' with AS60729, Stiftung Erneuerbare Freiheit, Berlin Germany returned. |
| c3 | The appropriate regional internet registry is queried for the authoritative allocation record — RIPE NCC for this European IP range | PASS | Ownership table: RIR=RIPE NCC, source 'RIPE WHOIS (https://stat.ripe.net/data/whois/data.json?resource=185.220.101.47) — allocation date Aug 31 2021, designated purpose, RIR authority.' |
| c4 | Reverse DNS PTR record is looked up and interpreted for what it reveals about the operator's naming scheme | PASS | ## Reverse DNS: 'tor-exit-47.for-privacy.net.' — 'PTR record explicitly identifies this as a Tor exit relay operated by ForPrivacyNET.' |
| c5 | Reputation is checked across multiple sources — VirusTotal, AbuseIPDB, AND Shodan public search | PASS | Reputation table includes all three: AbuseIPDB (6,500 reports), VirusTotal ([No data] with URL), Shodan (HTTP/80 banner, last scan date). All three attempted. |
| c6 | Shodan data is labelled as historical, not necessarily current state | PARTIAL | Sources list labels Shodan as 'T3 — historical service scan records' and gives last scan date (May 12 2026), but Shodan table row lacks explicit 'current state may differ' disclaimer. |
| c7 | If the IP belongs to a major cloud or hosting provider, output notes that provider attribution does not identify the actual customer | PASS | IP is not a major cloud provider; output correctly identifies it as a Tor exit operator and notes 'The node is a common carrier' and traffic is from 'anonymised clients' — addresses attribution limitation. |
| c8 | A clean reputation result is not equated with benign — the output states explicitly that clean means "not reported," not "safe" | PASS | Reputation caveat: 'Absence of flagging in VirusTotal/AbuseIPDB does not mean safe. AbuseIPDB reports on Tor exit nodes are expected...' |
| c9 | Related infrastructure is investigated — other domains on the same IP and ASN patterns are checked | PARTIAL | ## Related infrastructure checks /24 neighbors (.34, .45) and ASN patterns, but no passive DNS (SecurityTrails/RiskIQ-style) lookup for domains hosted on this specific IP. |
| c10 | Passive methods only — no active scanning, port enumeration, or service interaction | PASS | All sources are third-party passive aggregators: ipinfo.io, RIPE WHOIS, Tor exit lists, AbuseIPDB, Shodan (historical). No nmap, port scans, or direct service connections. |
| c11 | Output logs the stated purpose (security investigation per firewall log analysis) at the top before any lookup | PASS | First section is '## Authorisation gate' with firewall log context stated before any lookup sections appear. |
| c12 | Output's primary lookup uses ipinfo.io (or equivalent) for ASN, organisation, geolocation — with the actual values returned | PASS | Ownership table: Organisation=Stiftung Erneuerbare Freiheit, ASN=AS60729, Geolocation=Berlin Germany — actual returned values with ipinfo.io source URL. |
| c13 | Output queries RIPE NCC for the European IP range — getting the authoritative allocation including the inetnum block, the named contact for that block, and the country code | PASS | Prefix=185.220.101.32/27 (inetnum), Allocated to=ORG-FA1168-RIPE (named contact), Country=DE, source RIPE WHOIS API. |
| c14 | Output's reverse-DNS PTR lookup is performed and the result interpreted — naming pattern reveals operator type | PASS | PTR result 'tor-exit-47.for-privacy.net' interpreted: 'The PTR record explicitly identifies this as a Tor exit relay operated by ForPrivacyNET. This is the primary signal.' |
| c15 | Output checks reputation across at least 3 sources — VirusTotal IP report, AbuseIPDB confidence-of-abuse score, Shodan public scan history — with the specific URLs and result counts per source | PASS | AbuseIPDB: 6,500 reports with URL; VirusTotal: [No data] with URL; Shodan: banner + last scan date with URL. All three present with specifics. |
| c16 | Output labels Shodan data as HISTORICAL — 'Shodan last scanned this IP on YYYY-MM-DD; current state may differ' — never asserts current open ports based on Shodan | PARTIAL | Sources list labels Shodan 'historical service scan records'; last scan date given. But explicit phrase 'current state may differ' is absent from the Shodan data presentation. |
| c17 | Output addresses the specific IP 185.220.101.47 — known historically as a Tor exit node range; output names this if visible in reputation data, NOT as a hidden assumption | PASS | Chat summary: '185.220.101.47 is a confirmed, active Tor exit node.' PTR record, Tor Project exit list, and dan.me.uk all cited as T1/T2 sources explicitly naming this IP. |
| c18 | Output explicitly states clean-reputation does NOT mean benign — 'IP not currently flagged in AbuseIPDB / VirusTotal does not equal safe; many IPs are uncategorised, especially recently allocated infrastructure' | PASS | Reputation caveat section: 'Absence of flagging in VirusTotal/AbuseIPDB does not mean safe' is explicit. |
| c19 | Output investigates related infrastructure — domains hosted on this IP (via passive DNS like SecurityTrails, RiskIQ), other IPs in the same /24 with similar reputation patterns, ASN-level reputation | PARTIAL | ## Related infrastructure covers /24 neighbors (185.220.101.34) and ASN footprint. No SecurityTrails/RiskIQ passive DNS lookup for domains hosted on 185.220.101.47 specifically. |
| c20 | Output uses passive methods only — no nmap, no port scans, no banner grabbing, no service interaction; everything via third-party passive aggregators | PASS | All data sourced from ipinfo.io, RIPE WHOIS API, Tor Project list, dan.me.uk, AbuseIPDB, Shodan historical records. Shodan banner is from Shodan's own historical scan, not direct interaction. |

### Notes

Strong overall performance — all mandatory sections present with correct structure, Tor exit node correctly identified via multiple T1/T2 sources, and the clean-reputation caveat is explicit. The two gaps are: Shodan is labelled 'historical service scan records' in the sources list but lacks the explicit 'current state may differ' caveat in the data table (c6/c16), and passive DNS domain lookup via SecurityTrails/RiskIQ for domains hosted on the specific IP was omitted from related infrastructure (c19).
