# Consolidate

Scenario: An engagement directory under `{workspace}/work/visualcare/` contains three conforming research reports across two categories (one People, two Technical). The fixtures are pre-staged by the harness from `fixtures/visualcare/`. The consolidate skill should detect them, group them by category, produce a `DOSSIER.md` with each report embedded under its category, and render a brand-styled PDF. The skill's design is "terse chat + rich artifact": the chat output is intentionally a short completion summary (report count, output paths), with every per-file detail captured inside the written `DOSSIER.md`. Criteria below evaluate the artifact as the primary source of truth, treating the chat as a confirmation surface, not a verbose progress log.

**Output files:** [DOSSIER.pdf](./DOSSIER.pdf) (34KB)

## Prompt

> The engagement directory at `{workspace}/work/visualcare/` already contains three research reports staged by the test harness:
> 
> - `people-lookup/graves-michael.md` (category: People)
> - `domain-intel/visualcare-com-au.md` (category: Technical)
> - `ip-intel/52-12-34-56.md` (category: Technical)
> 
> Run `/dossier:consolidate {workspace}/work/visualcare` to produce the dossier. Do not pause for confirmation — proceed with all defaults.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Dossier written.

```
Markdown: /var/folders/.../work/visualcare/DOSSIER.md
PDF:      /var/folders/.../work/visualcare/DOSSIER.pdf
```

Included 3 reports across 2 categories (People: 1, Technical: 2). No appendices. No ineligible files. Each report begins on a fresh page in the PDF.

### Artifacts written

#### `work/visualcare/DOSSIER.md`

```
---
title: VisualCare Dossier
subtitle: Visualcare Pty Ltd
date: 2026-05-13
author: Martin Lau
category: Dossier
status: Draft
---

## Executive summary

<!-- TODO: write a 3-5 paragraph summary covering the engagement target, scope of the investigation, and the headline findings across all categories. The dossier agent fills this in drive mode; in standalone consolidate runs, leave the placeholder for the user. -->

# People lookup — Michael Graves

## Summary

Michael Graves is listed as a current director of Visualcare Pty Ltd in ASIC Connect.

## Sources

1. ASIC Connect (https://connectonline.asic.gov.au) — accessed 2026-05-12 (T1)

# IP intel — 52.12.34.56

## Ownership

AWS EC2, us-east-1, no shared-hosting indicators.

# Domain intel — visualcare.com.au

## Registration

Registered 2009-03-04 via Crazy Domains. Current registrant Visualcare Pty Ltd.

## DNS records

A record points to AWS us-east-1 IP. MX records use Google Workspace.

```

#### `work/visualcare/people-lookup/graves-michael.md`

```
---
title: People lookup — Michael Graves
date: 2026-05-12
author: people-lookup
category: People
subject: Michael Graves
status: Final
---

## Summary

Michael Graves is listed as a current director of Visualcare Pty Ltd in ASIC Connect.

## Sources

1. ASIC Connect (https://connectonline.asic.gov.au) — accessed 2026-05-12 (T1)

```

#### `work/visualcare/domain-intel/visualcare-com-au.md`

```
---
title: Domain intel — visualcare.com.au
date: 2026-05-12
author: domain-intel
category: Technical
subject: visualcare.com.au
status: Final
---

## Registration

Registered 2009-03-04 via Crazy Domains. Current registrant Visualcare Pty Ltd.

## DNS records

A record points to AWS us-east-1 IP. MX records use Google Workspace.

```

#### `work/visualcare/ip-intel/52-12-34-56.md`

```
---
title: IP intel — 52.12.34.56
date: 2026-05-12
author: ip-intel
category: Technical
subject: 52.12.34.56
status: Final
---

## Ownership

AWS EC2, us-east-1, no shared-hosting indicators.

```

#### `work/visualcare/DOSSIER.pdf`

Binary artifact (34KB) — see [`DOSSIER.pdf`](./DOSSIER.pdf)

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 11.0/11.0 (100%) |
| Evaluated | 2026-05-13 |
| Target duration | 44144 ms |
| Target cost | $0.2828 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill resolves the engagement directory to the absolute path under `{workspace}` — evidence may be the absolute path appearing in chat output paths, an explicit confirmation line, or both | PASS | Chat shows: 'Markdown: /var/folders/.../work/visualcare/DOSSIER.md' and 'PDF: /var/folders/.../work/visualcare/DOSSIER.pdf' — absolute paths confirm resolution. |
| c2 | Skill detects all three fixture files — evidence may be a per-file enumeration in chat OR all three reports appearing in the written `DOSSIER.md`. A count summary in chat ("3 reports across 2 categories") is acceptable when the per-file detail is present in the artifact. | PASS | Chat states '3 reports across 2 categories (People: 1, Technical: 2)'; DOSSIER.md contains all three: Graves, 52.12.34.56, and visualcare.com.au. |
| c3 | Skill orders reports by category — People reports first, then Technical (per the skill's category-ordering rule) — sorted within category by subject then date | PASS | DOSSIER.md: People (Graves) first; Technical: '# IP intel — 52.12.34.56' before '# Domain intel — visualcare.com.au'; '5' < 'v' alphabetically is correct subject sort. |
| c4 | Skill writes `DOSSIER.md` to the engagement directory with the three source reports embedded inline, each as its own h1 page break | PASS | DOSSIER.md written to work/visualcare/; contains '# People lookup — Michael Graves', '# IP intel — 52.12.34.56', '# Domain intel — visualcare.com.au' as h1 headers. |
| c5 | Skill renders a PDF of the dossier (skill output names the rendered PDF path, and a `.pdf` file lands in the engagement directory) — OR — if rendering is unavailable in the test environment, the skill stops cleanly and reports that rendering would be the next step rather than silently skipping | PASS | Chat reports 'PDF: /var/folders/.../work/visualcare/DOSSIER.pdf'; artifact section confirms work/visualcare/DOSSIER.pdf as 34KB binary. |
| c6 | Each embedded report's body content is preserved verbatim — no body rewriting. Frontmatter stripping is intentional per the skill's template; titles become h1 page breaks. | PASS | All three report bodies match source fixtures verbatim: Graves '## Summary / Michael Graves...', IP '## Ownership / AWS EC2...', domain '## Registration / Registered 2009-03-04...' — no rewrites. |
| c7 | Skill flags any body `h1` violations from the source reports — explicitly stating "no body-h1 warnings" when the fixture is clean. Silence is acceptable when no warnings exist, but an explicit statement is preferred. | PARTIAL | Chat is silent on h1 violations. Criterion states silence is acceptable when no warnings exist; ceiling is PARTIAL. No explicit statement present, but silence is not a FAIL. |
| c8 | A re-run of consolidate against the same directory does not ingest the previous `DOSSIER.md` (`category: Dossier` is excluded) — evidence may be the `category: Dossier` line in the generated artifact's frontmatter, which is the exclusion mechanism. A demonstrated re-run is not required. | PASS | DOSSIER.md frontmatter contains 'category: Dossier' — the exclusion mechanism is in place, ensuring a re-run would skip this file. |
| c9 | Output's `DOSSIER.md` orders reports People first then Technical, with each report's title rendered as h1 (per the page-break-per-report rule) | PASS | DOSSIER.md: '# People lookup — Michael Graves' (h1) first, then '# IP intel — 52.12.34.56' and '# Domain intel — visualcare.com.au' (both h1, Technical). |
| c10 | Output's category ordering is stable — sorted reports within each category by subject then date — re-running on the same inputs produces the same ordering | PASS | Within Technical, sort is by subject ('52.12.34.56' < 'visualcare.com.au' alphabetically); both dates identical (2026-05-12), so subject sort is deterministic and stable. |
| c11 | Output reports the file path of the generated `DOSSIER.md` (and the PDF if rendering succeeded) so the user can open the result without searching | PASS | Chat explicitly shows 'Markdown: /var/folders/.../work/visualcare/DOSSIER.md' and 'PDF: /var/folders/.../work/visualcare/DOSSIER.pdf' — both paths reported. |
| c12 | Chat output identifies the three input files individually — either by listing them before consolidating or by naming them in a per-file summary line. A bare count ("3 reports") satisfies a PARTIAL ceiling here, since the per-file detail is recoverable from `DOSSIER.md` itself. | PARTIAL | Chat states 'Included 3 reports across 2 categories (People: 1, Technical: 2)' — bare count with category breakdown, no individual file names listed. Satisfies PARTIAL ceiling per criterion. |

### Notes

The skill executed cleanly against all structural and content criteria: correct category ordering, verbatim body preservation, exclusion mechanism via 'category: Dossier', PDF rendered, and both output paths reported. Only c7 and c12 scored below PASS, both by design (PARTIAL ceilings), yielding a perfect 11.0/11.0.
