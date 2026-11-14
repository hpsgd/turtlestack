---
name: conventions
description: "Research output conventions: the report frontmatter contract and file naming (report-conventions), source tiers and the 0-4 confidence rubric (source-quality), and citation specificity (source-citations). Load before producing or consolidating any research, investigation or analysis report. Skills that say 'per report-conventions', 'per source-quality' or 'source-citations rule' mean this."
user-invocable: true
---

# Research conventions

Three conventions every research, investigation and analysis report follows. Skills refer to them by the names in brackets.

## Report conventions (report-conventions)

Every research, investigation, or analysis skill that produces a markdown file follows the same contract: a YAML frontmatter block declaring the metadata below, and a deterministic output path under an engagement directory. This makes outputs discoverable, groupable, and renderable by downstream tools without each tool reverse-engineering each producer.

One file per skill invocation. Aggregation is the consumer's problem.

### Frontmatter — required

A file missing any of these is not a conforming report. Downstream consumers (e.g. dossier builders) skip non-conforming files.

| Field | Type | Notes |
|---|---|---|
| `title` | string | Renders as the section heading when the file is consumed elsewhere |
| `date` | ISO date (`YYYY-MM-DD`) | Used to order entries chronologically |
| `author` | string | Who or what produced the report — assessor name or skill name |
| `category` | string | Free text but consistent within an engagement. Suggested values: `People`, `Technical`, `Corporate`, `Commercial`, `OSINT`. Optional when `appendix: true` (see below). |

### Frontmatter — optional but recommended

| Field | Type | Notes |
|---|---|---|
| `subtitle` | string | Engagement context (typically the company or target name) |
| `subject` | string | What the report is specifically about — used for sub-grouping within a category (e.g. person name, domain, entity) |
| `status` | enum | `Draft` or `Final` |
| `confidence` | int 0-4 | Overall confidence rating per the source quality rubric |
| `tags` | list of strings | Free-form, for future filtering |
| `appendix` | bool | If true, file renders as an appendix at the end of the dossier, after all category sections. Use for sources registers, questions logs, or other reference material that supports the main content. When set, `category` may be omitted. |

Other keys are permitted. Skill-specific frontmatter is fine — the rule defines the shared minimum, not a closed schema.

### Appendix files

A file with `appendix: true` is reference material that supports the main report content — sources registers, open-questions logs, glossaries, methodology notes. Downstream consumers (dossier builders) render appendices after all category sections, in their own dedicated Appendices section.

Appendix files still need `title`, `date`, and `author`. `category` is optional for appendices since they don't belong to a People/Corporate/Commercial/Technical/OSINT slice.

### File-naming pattern

```
<engagement_dir>/<skill-name>/<subject-slug>.md
```

The rule defines the *pattern*. Where `engagement_dir` lives is the user's choice (typical: `~/Assessments/<target-slug>/`). Each skill writes into a subdirectory named after itself.

Examples:

- `~/Assessments/visualcare/people-lookup/graves-michael.md`
- `~/Assessments/visualcare/domain-intel/visualcare-com-au.md`
- `~/Assessments/visualcare/corporate-ownership/visual-data-solutions-pty-ltd.md`

### Subject slug convention

Each skill applies the convention; there is no shared function. The rule states the convention so skills produce consistent slugs:

| Subject type | Slug pattern | Example |
|---|---|---|
| Person | `<lastname>-<firstname>`, kebab-case | `Michael Graves` → `graves-michael` |
| Domain | full domain with dots replaced by hyphens | `visualcare.com.au` → `visualcare-com-au` |
| Entity / company | full name, kebab-case, no legal suffix punctuation | `Visual Data Solutions Pty Ltd` → `visual-data-solutions-pty-ltd` |
| IP address | dots replaced by hyphens | `203.0.113.42` → `203-0-113-42` |
| Other | descriptive kebab-case | implementer's call, document in skill |

Slugs lowercase. ASCII only. Strip diacritics, punctuation, and apostrophes.

### Body heading convention

The report's title is the `title` frontmatter field. It is rendered as the cover page when the file is solo-rendered, and as a single `h1` page-break heading when the file is embedded in a dossier or other compilation.

The body therefore uses **`h2` and below** for all sub-sections. Do not put `h1` in the body. A body `h1` either competes with the rendered title or breaks the dossier's page-boundary contract (one report = one `h1` = one page break).

Bad:

```markdown
---
title: Domain intel — example.com
---

# Registration

...

# DNS records
```

Good:

```markdown
---
title: Domain intel — example.com
---

## Registration

...

## DNS records
```

Sub-sections within those use `h3`, then `h4`, etc. Don't skip levels.

### What this rule does NOT cover

Downstream plugins extend the contract for their own purposes. Out of scope here:

- Evidence directory layout (e.g. `evidence/data/`, `evidence/web-snapshots/`)
- Multi-pass investigation workflows
- Source ID prefix conventions (`P-Sxx`, `S##`)
- Authorisation gates — those live in skill behaviour, not in the report file

Each skill defines its own body structure inside the file. The rule only fixes the metadata header and where the file lands.

## Source quality (source-quality)

### Source tiers

Every source cited in research output must be classified by tier. The tier determines how much weight the evidence carries.

| Tier | Type | Examples | Trust level |
|---|---|---|---|
| T1 — Regulatory/Legal | Government bodies, regulators, court records | ACCC decisions, Auditor-General reports, procurement registers, company filings, AustLII | Highest — treat as factual |
| T2 — Independent Analysis | Analysts, journalists, industry publications | Gartner, IDC, iTnews, CRN, AFR, industry journals | High — professional editorial standards |
| T3 — Market Signal | Job boards, review sites, tech community, financial databases | SEEK/LinkedIn jobs, G2/Capterra reviews, StackOverflow, GitHub, Crunchbase | Moderate — useful signal, verify context |
| T4 — Customer/User Voice | End-user reviews, community forums, meeting minutes | App store reviews, local news, community groups, FOI responses | Moderate — genuine but potentially unrepresentative |
| T5 — Subject's Own Materials | Company website, press releases, marketing collateral, case studies | Corporate blog, branded case studies, investor presentations | Lowest — treat as claims to validate, not facts |

### Confidence rubric (0-4)

Confidence measures confidence in the assessment, not whether a finding is positive or negative. A high confidence score on a concern means you're very confident the concern is real.

This is the rubric the `confidence` field in the report-conventions frontmatter refers to.

| Rating | Label | Definition | Evidence standard |
|---|---|---|---|
| 0 | No confidence | Insufficient data to form a view | No reliable sources; contradictory signals |
| 1 | Low | Directional sense only. Gut feel territory | 1-2 indirect signals. Label as "gut feel" |
| 2 | Moderate | Reasonable view with gaps | 3+ corroborating sources from 2+ tiers. At least 1 T1-T3 source |
| 3 | High | Would confidently present to a board | Multiple validated T1-T3 sources. Disconfirming search attempted |
| 4 | Very high | Near-certain, cross-validated | Extensive T1-T2 anchored validation. Withstands board-level scrutiny |

T5-only sourcing caps confidence at 1 regardless of how compelling the claim sounds.

### Validation rules

1. **No claim at confidence 2+ without a T1-T3 source.** Subject-only sourcing (T5) caps confidence at 1.
1. **Triangulate.** Any claim in the final output should be supported by at least 2 sources from different tiers. One-source claims must be labelled `[single source]`.
1. **Challenge every superlative.** "Market-leading", "only company that...", "end-to-end" — these are marketing language. Find independent evidence or downgrade to hedged language ("claims to be...").
1. **Seek disconfirming evidence.** For every positive claim, actively search for contradicting data. Note failed searches ("searched for X, found no contradicting evidence").
1. **Tag source tier.** Every citation gets a tier tag so source quality is visible at a glance.
1. **Recency matters.** Prefer sources from the last 12 months. Flag anything older than 24 months as potentially stale.

### Source tier classification pitfalls

| Looks like | Actually is | Example |
|---|---|---|
| T2 (independent) | T5 (self-published) | Industry directories where companies submit their own profiles |
| T1 (government) | T3 (commercial aggregator) | .com sites aggregating government data — trace back to actual government source for T1 |
| Strong negative signal | Self-selecting sample | ProductReview.com.au, Trustpilot — people go there specifically to complain |
| Strong positive signal | Potentially incentivised | Very high app ratings — check for discount/reward programs for reviews |

### Claim validation checklist

Before finalising any research dimension:

- Are any findings supported only by T5 (subject's own) sources?
- Has at least one disconfirming search been attempted?
- Are superlatives backed by independent evidence?
- Does the source tier mix justify the confidence level?
- Are single-source claims labelled as such?

## Source citations (source-citations)

Every source cited in research output must be verifiable by the reader without repeating the research. A source URL must point to the specific content being cited, not the tool or registry homepage.

### What a good source looks like

A source citation has three parts: what you found, where exactly you found it, and when you accessed it.

**Good:** `ASIC Connect director search for "Salim Mehajer" (https://connectonline.asic.gov.au/RegistrySearch/faces/landing/SearchRegisters.jspx) — accessed 2026-04-16, 4 current directorships found`

**Bad:** `ASIC Connect (https://connect.asic.gov.au) — director search`

The first lets someone verify your finding. The second just names a website.

### URL specificity rules

- **Company pages:** link to the specific company profile, not the platform homepage. `linkedin.com/company/safetyculture` not `linkedin.com`
- **App stores:** link to the specific app listing. `apps.apple.com/app/safetyculture/id1234567` not `apps.apple.com`
- **Registries (ASIC, ABN, Companies Office):** link to the search results page or entity page, not the registry homepage. If the registry doesn't support deep linking, state the exact search terms used
- **News articles:** link to the specific article. `afr.com/technology/canva-hits-40b-valuation-20230925` not `news.google.com`
- **Archive tools:** link to the specific archived page. `web.archive.org/web/2023/https://example.com` not `web.archive.org`
- **Court records:** link to the specific case or judgment on AustLII/NZLII, not the portal homepage
- **Certificate transparency:** include the query parameter. `crt.sh/?q=example.com` not `crt.sh`

### When deep linking isn't possible

Some registries don't support direct URLs to search results (e.g., ASIC Connect director search generates session-based URLs). When this happens:

1. State the registry name and the exact search path: "ASIC Connect → Organisation & Business Names → Director Search → 'Mehajer'"
2. Include the access date
3. Summarise what the search returned

This is acceptable because it gives the reader enough to reproduce the lookup. A bare homepage URL does not.

### Access dates

Every source gets an access date. Public web content changes. A finding verified on 2026-04-16 may not be at the same URL next month. The access date tells the reader when the information was confirmed.

### Source vs reference

A **source** is something you checked and found specific information in. A **reference** is a resource you're pointing the reader to for further context. Don't mix them. If you didn't actually check it, don't list it as a source.
