---
name: consolidate
description: "Scan an engagement directory for conforming research reports, group them by category, and produce a single DOSSIER.md plus brand-styled PDF that embeds every included report. Each embedded report's title becomes an h1 page break, so every report starts on a fresh page. Reports must declare frontmatter per the report-conventions rule (title, date, author required; category required unless appendix: true) and use h2+ for body sub-sections. Files marked `appendix: true` render as a trailing Appendices section."
argument-hint: "[engagement_dir]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion, Skill
---

# Consolidate

Build a single dossier from every conforming research report in an engagement directory. The output is one markdown file (`DOSSIER.md`) with all source reports embedded inline, then rendered to PDF with a dossier-specific stylesheet that page-breaks before each embedded report.

This skill is the back end of the dossier workflow. The companion `dossier` agent drives end-to-end campaigns; this skill just does the gather-and-render step. Run this skill directly when you've already produced reports manually or via individual skills and want to compile them.

The skill's contract is **terse chat + rich artifact**: the chat output is a short completion summary (report count, output paths, any warnings); every per-file detail lands inside the written `DOSSIER.md`. Treat `DOSSIER.md` as the primary source of truth — reviewers can re-derive the candidate listing from it.

## Step 1: Resolve engagement directory

The first argument is the engagement directory. If omitted, default to `pwd`. Resolve to an absolute path. The directory must exist and must contain at least one markdown file — if not, stop and report.

```bash
ARG="${1:-$(pwd)}"
case "$ARG" in
  /*) ENG="$ARG" ;;
  *) ENG="$(pwd)/$ARG" ;;
esac
```

## Step 2: Discover candidates

Scan `$ENG/**/*.md` for files. For each, parse the YAML frontmatter (between leading `---` markers). A file is **eligible** as one of two kinds:

- **Category report** — declares `title`, `date`, `author`, and `category`. Renders inside its category section.
- **Appendix** — declares `title`, `date`, `author`, and `appendix: true`. `category` is optional and ignored for appendix routing. Renders in the trailing Appendices section.

A file is **ineligible** if it has frontmatter but is missing the fields above for either kind, or has no frontmatter at all.

Also flag (but still treat as eligible) any file whose body contains an `h1` heading — this violates the body-heading clause of the report-conventions rule. The dossier will still embed it, but the rendered PDF will get an unintended extra page break at every body `h1`. Surface the violation when listing candidates.

Skip the dossier itself: any file with `category: Dossier` is excluded, so a re-run does not ingest the previous output.

Use `Glob` to enumerate, then `Read` each to extract frontmatter. For larger engagements (50+ files), prefer a small inline shell pass to extract frontmatter blocks before opening each file.

## Step 3: Present candidates and confirm scope

Group eligible category reports by `category`, sorted within category by `subject` then `date` then filename. Appendix files are listed separately under an "Appendices" group, sorted alphabetically by filename. When the run is interactive — the user can answer follow-up questions — show a summary like this in chat so they can confirm scope before anything is written:

```
Eligible reports in <engagement_dir>: 16

  People (6)
    - Graves, Michael — 2026-04-24 — people-lookup/graves-michael.md
    - Lau, Susan      — 2026-04-24 — people-lookup/lau-susan.md
    ...
  Corporate (4)
    ...
  Technical (3)
    ...
  OSINT (1)
    ...

  Appendices (2)
    - QUESTIONS.md — 2026-04-24 — questions log
    - SOURCES.md   — 2026-04-24 — sources register

Ineligible (3):
  - drafts/notes.md — no frontmatter
  - evidence/web-snapshots/index.md — missing 'category' (and not marked appendix)
  - README.md — missing 'date', 'author'

Body-heading warnings (1):
  - corporate-ownership/old-report.md — body uses h1 (will produce extra page breaks)
```

Then ask the user via `AskUserQuestion` how to proceed:

- **Include all eligible** — proceed with every conforming file (category reports and appendices)
- **Exclude a category** — drop everything in one category (follow-up question for which). "Appendices" is a valid choice here
- **Exclude individual files** — drop specific files (follow-up for paths)
- **Abort** — stop without writing anything

Ineligible files are never included automatically. If the user wants any of them in, they fix the frontmatter and re-run.

In non-interactive runs (no user available to answer questions — driven from another agent, a script, or a test harness), skip the AskUserQuestion step and proceed with all eligible files. Surface body-h1 warnings in the completion summary when any exist; silence is acceptable when there are none.

## Step 4: Build DOSSIER.md

Write `$ENG/DOSSIER.md`. The structure is:

1. **Dossier frontmatter** — produces the cover page when rendered
1. **Executive summary** as `h2` — does not force a page break, so it shares the page that follows the cover
1. **One `h1` per embedded category report** — each report becomes its own page-break boundary
1. **Appendices section** (only if there are appendix files) — one `h1` divider, then one `h1` per embedded appendix

Categories drive **ordering only** in the main body. There are no visible category dividers. All People reports come first, then Corporate, Commercial, Technical, OSINT, then any other categories alphabetically.

Appendices come after all category reports, separated from the main body by a single `# Appendices` divider page (its own page break). Inside, appendices order by filename alphabetically.

Template:

```markdown
---
title: <inferred from engagement dir name, e.g. "VisualCare Dossier">
subtitle: <engagement target, if discernible from reports' subtitle>
date: <today, ISO>
author: <user name from git config, fallback to "Dossier">
category: Dossier
status: Draft
---

## Executive summary

<!-- TODO: write a 3-5 paragraph summary covering the engagement target, scope of the investigation, and the headline findings across all categories. The dossier agent fills this in drive mode; in standalone consolidate runs, leave the placeholder for the user. -->

# <Report 1 title — verbatim from frontmatter>

<full embedded body of report 1, frontmatter stripped, body left unchanged>

# <Report 2 title>

...

# Appendices

# <Appendix 1 title — verbatim from frontmatter>

<full embedded body of appendix 1, frontmatter stripped, body left unchanged>

# <Appendix 2 title>

...
```

Rules for embedding:

- **Strip the leading `---...---` frontmatter block** from each embedded report. Frontmatter values (`author`, `date`, `source`, `confidence`, `status`, etc.) are metadata, not body content — do not render them as visible text in the dossier
- **Do NOT demote headings.** The body is already `h2+` per the report-conventions rule. If a body has an `h1` (contract violation, flagged in Step 3), embed it as-is — the result will be visually wrong but doesn't require special handling here
- **Inject one `h1` per report** with the verbatim `title` from the report's frontmatter
- **Category report order:** by category (`People`, `Corporate`, `Commercial`, `Technical`, `OSINT`, then alphabetical for any other), then by `subject` if present, then by `date`, then by filename
- **No category headings.** Don't write `# People` or any category-level visible separator. Ordering carries the grouping
- **Appendix section:** emit a single `# Appendices` divider after the last category report only when there are appendix files. Then embed each appendix the same way as a category report — one `h1` per file with the verbatim `title` — ordered alphabetically by filename
- **No provenance footers.** Don't render `*Source: <path> — <author> — <date>*` under embedded reports. Provenance lives in the source file's frontmatter, which the reader does not need to see in the rendered dossier

## Step 5: Render to PDF

Invoke the publishing plugin's render skill with the dossier stylesheet:

```
/publishing:write-document-pdf <engagement_dir>/DOSSIER.md \
  --out <engagement_dir>/DOSSIER.pdf \
  --css ${CLAUDE_PLUGIN_ROOT}/assets/styles/dossier.css
```

The dossier stylesheet adds `h1 { page-break-before: always; }` on top of the standard report styling, which is what produces the per-report page breaks.

If `/publishing:write-document-pdf` is not installed, report the path to `DOSSIER.md` and tell the user the renderer plugin is needed for the PDF step. Do not silently skip — the user expects a PDF and needs to know if they didn't get one.

Verify the PDF was produced and is non-empty before reporting success:

```bash
[ -s "$ENG/DOSSIER.pdf" ] && echo "OK"
```

## Step 6: Output

Report two paths and a content summary:

```
Dossier written.

  Markdown: <engagement_dir>/DOSSIER.md
  PDF:      <engagement_dir>/DOSSIER.pdf

Included 14 reports across 4 categories (People: 6, Corporate: 4, Technical: 3, OSINT: 1) plus 2 appendices.
Each report begins on a fresh page in the PDF.
3 files were ineligible — fix their frontmatter and re-run to include them.
```

## Rules

- **Never modify source reports.** Read-only on everything except `DOSSIER.md` and `DOSSIER.pdf`.
- **The dossier file declares `category: Dossier`.** Re-runs must skip it.
- **Embed full content, not synopses.** The dossier is a single document with everything we know.
- **One `h1` per report, ever.** Don't add category h1s, don't keep body h1s from source reports (the rule forbids those, and the renderer treats every h1 as a page break). The single `# Appendices` divider is the one exception — it's a section divider, not a report.
- **No provenance in the body.** Frontmatter fields (`author`, `date`, `source`, `confidence`, `status`) are metadata. The reader sees the report title and content, not who wrote it or when. The provenance is in the source file for audit if anyone needs it.
- **`h2` for the executive summary.** The cover already starts the document; an `h1` here would force a redundant page break.
- **Don't auto-fix ineligible files.** If a file is missing `category` or `date`, that's a producer-side issue. Surface it; let the user fix the source.
- **Confirm before writing.** The user gets a candidate list and chooses scope before any output is produced.

## Output format

Two paths and a one-line summary. See Step 6.

## Related

- `/dossier:dossier` agent — drive mode. Asks what to investigate, dispatches investigator/analyst skills, then calls this skill on completion.
- `/publishing:write-document-pdf` — the renderer this skill calls. Invoked with `--css <dossier-css>` so the page-break rule is applied.
- `report-conventions.md` rule — the frontmatter contract every conforming report follows, including the body-heading clause.
