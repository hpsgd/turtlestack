# Report conventions

Every research, investigation, or analysis skill that produces a markdown file follows the same contract: a YAML frontmatter block declaring the metadata below, and a deterministic output path under an engagement directory. This makes outputs discoverable, groupable, and renderable by downstream tools without each tool reverse-engineering each producer.

One file per skill invocation. Aggregation is the consumer's problem.

## Frontmatter — required

A file missing any of these is not a conforming report. Downstream consumers (e.g. dossier builders) skip non-conforming files.

| Field | Type | Notes |
|---|---|---|
| `title` | string | Renders as the section heading when the file is consumed elsewhere |
| `date` | ISO date (`YYYY-MM-DD`) | Used to order entries chronologically |
| `author` | string | Who or what produced the report — assessor name or skill name |
| `category` | string | Free text but consistent within an engagement. Suggested values: `People`, `Technical`, `Corporate`, `Commercial`, `OSINT` |

## Frontmatter — optional but recommended

| Field | Type | Notes |
|---|---|---|
| `subtitle` | string | Engagement context (typically the company or target name) |
| `subject` | string | What the report is specifically about — used for sub-grouping within a category (e.g. person name, domain, entity) |
| `status` | enum | `Draft` or `Final` |
| `confidence` | int 0-4 | Overall confidence rating per the source quality rubric |
| `tags` | list of strings | Free-form, for future filtering |

Other keys are permitted. Skill-specific frontmatter is fine — the rule defines the shared minimum, not a closed schema.

## File-naming pattern

```
<engagement_dir>/<skill-name>/<subject-slug>.md
```

The rule defines the *pattern*. Where `engagement_dir` lives is the user's choice (typical: `~/Assessments/<target-slug>/`). Each skill writes into a subdirectory named after itself.

Examples:

- `~/Assessments/visualcare/people-lookup/graves-michael.md`
- `~/Assessments/visualcare/domain-intel/visualcare-com-au.md`
- `~/Assessments/visualcare/corporate-ownership/visual-data-solutions-pty-ltd.md`

## Subject slug convention

Each skill applies the convention; there is no shared function. The rule states the convention so skills produce consistent slugs:

| Subject type | Slug pattern | Example |
|---|---|---|
| Person | `<lastname>-<firstname>`, kebab-case | `Michael Graves` → `graves-michael` |
| Domain | full domain with dots replaced by hyphens | `visualcare.com.au` → `visualcare-com-au` |
| Entity / company | full name, kebab-case, no legal suffix punctuation | `Visual Data Solutions Pty Ltd` → `visual-data-solutions-pty-ltd` |
| IP address | dots replaced by hyphens | `203.0.113.42` → `203-0-113-42` |
| Other | descriptive kebab-case | implementer's call, document in skill |

Slugs lowercase. ASCII only. Strip diacritics, punctuation, and apostrophes.

## Body heading convention

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

## What this rule does NOT cover

Downstream plugins extend the contract for their own purposes. Out of scope here:

- Evidence directory layout (e.g. `evidence/data/`, `evidence/web-snapshots/`)
- Multi-pass investigation workflows
- Source ID prefix conventions (`P-Sxx`, `S##`)
- Authorisation gates — those live in skill behaviour, not in the report file

Each skill defines its own body structure inside the file. The rule only fixes the metadata header and where the file lands.
