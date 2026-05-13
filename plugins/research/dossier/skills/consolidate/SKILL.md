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

Once scope is confirmed, ask a second `AskUserQuestion` about **category ordering**:

- **Default order** — `People` → `Corporate` → `Commercial` → `Technical` → `OSINT` → any other categories alphabetically
- **Custom order** — follow-up free-text question listing only the categories present in this run; user types them in their preferred order. Categories present but not mentioned fall back to the default's relative order at the end.

Skip this question when only one category is present (there's nothing to order). The Appendices section is unaffected — it always comes last, ordered alphabetically by filename.

In non-interactive runs (no user available to answer questions — driven from another agent, a script, or a test harness), skip both AskUserQuestion steps and proceed with all eligible files in default order. Surface body-h1 warnings in the completion summary when any exist; silence is acceptable when there are none.

## Step 4: Build DOSSIER.md

Write `$ENG/DOSSIER.md`. The structure is:

1. **Dossier frontmatter** — produces the cover page when rendered
1. **Table of Contents** as `## Contents` — lands on page 2 (the cover forces a page break). Links to every `h1` and `h2` in the dossier (except itself)
1. **Executive summary** as `h2` — flows after the TOC
1. **One `h1` per embedded category report** — each report becomes its own page-break boundary
1. **Appendices section** (only if there are appendix files) — one `h1` divider, then one `h1` per embedded appendix

Categories drive **ordering only** in the main body. There are no visible category dividers. The default order is `People` → `Corporate` → `Commercial` → `Technical` → `OSINT` → any other categories alphabetically. The user can override this in Step 3; use whatever order they chose.

Appendices come after all category reports, separated from the main body by a single `# Appendices` divider page (its own page break). Inside, appendices order by filename alphabetically.

### Anchor scheme

Every heading that the TOC references needs a stable id. Use python-markdown's `attr_list` syntax (already enabled in the renderer): append `{#id}` to the heading line. The id scheme is sequential so collisions are impossible:

| Element | Anchor |
|---|---|
| Executive summary | `{#exec-summary}` |
| Nth category report's title h1 | `{#report-N}` (1-indexed across the whole dossier, in final emitted order) |
| Mth h2 inside category report N | `{#report-N-sM}` |
| Appendices divider | `{#appendices}` |
| Nth appendix's title h1 | `{#appendix-N}` |
| Mth h2 inside appendix N | `{#appendix-N-sM}` |

When embedding a report, rewrite every `^## (.+)$` line in its body to `## $1 {#report-N-sM}` (or `{#appendix-N-sM}` for appendices), counting H2s as they appear. The H1 you inject for the report's title gets `{#report-N}`. Don't touch h3+ headings.

### Table of Contents

Emit `## Contents` immediately after the dossier frontmatter, before the executive summary. The body is a nested unordered list of markdown links — one bullet per h1 and h2 in the dossier, in document order, excluding `## Contents` itself. h2s are nested one level under their parent h1; the executive summary is a top-level entry alongside the report h1s.

Example shape:

```markdown
## Contents

- [Executive summary](#exec-summary)
- [Michael Graves](#report-1)
  - [Roles and directorships](#report-1-s1)
  - [Public profile](#report-1-s2)
- [Susan Lau](#report-2)
  - [Roles and directorships](#report-2-s1)
- [Appendices](#appendices)
  - [Sources register](#appendix-1)
  - [Open questions](#appendix-2)
```

Link text is the verbatim heading text. Don't truncate.

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

## Contents

- [Executive summary](#exec-summary)
- [<Report 1 title>](#report-1)
  - [<H2 from report 1>](#report-1-s1)
  ...
- [Appendices](#appendices)
  - [<Appendix 1 title>](#appendix-1)
  ...

## Executive summary {#exec-summary}

<!-- TODO: write a 3-5 paragraph summary covering the engagement target, scope of the investigation, and the headline findings across all categories. The dossier agent fills this in drive mode; in standalone consolidate runs, leave the placeholder for the user. -->

# <Report 1 title — verbatim from frontmatter> {#report-1}

<full embedded body of report 1, frontmatter stripped, h2s rewritten with sequential anchors>

# <Report 2 title> {#report-2}

...

# Appendices {#appendices}

# <Appendix 1 title — verbatim from frontmatter> {#appendix-1}

<full embedded body of appendix 1, frontmatter stripped, h2s rewritten with sequential anchors>

# <Appendix 2 title> {#appendix-2}

...
```

Rules for embedding:

- **Strip the leading `---...---` frontmatter block** from each embedded report. Frontmatter values (`author`, `date`, `source`, `confidence`, `status`, etc.) are metadata, not body content — do not render them as visible text in the dossier
- **Do NOT demote headings.** The body is already `h2+` per the report-conventions rule. If a body has an `h1` (contract violation, flagged in Step 3), embed it as-is — the result will be visually wrong but doesn't require special handling here
- **Inject one `h1` per report** with the verbatim `title` from the report's frontmatter, plus its TOC anchor (see Anchor scheme above)
- **Rewrite body h2s** with sequential TOC anchors as they're embedded — h3+ left alone
- **Category report order:** by category (default `People` → `Corporate` → `Commercial` → `Technical` → `OSINT` → alphabetical for any other, unless the user supplied a custom order in Step 3), then by `subject` if present, then by `date`, then by filename
- **No category headings.** Don't write `# People` or any category-level visible separator. Ordering carries the grouping
- **Appendix section:** emit a single `# Appendices {#appendices}` divider after the last category report only when there are appendix files. Then embed each appendix the same way as a category report — one `h1` per file with the verbatim `title` and a `{#appendix-N}` anchor — ordered alphabetically by filename
- **No provenance footers.** Don't render `*Source: <path> — <author> — <date>*` under embedded reports. Provenance lives in the source file's frontmatter, which the reader does not need to see in the rendered dossier

## Step 5: Offer to generate the executive summary

The markdown now exists with a `<!-- TODO -->` placeholder in the executive summary section. Ask the user via `AskUserQuestion` whether to fill it now:

- **Generate now** — invoke `/dossier:executive-summary <engagement_dir>` as a sub-skill. That skill is interactive: it asks for inputs, audience, posture, and shows the user a draft before writing. When it returns, control comes back here and the rendering step proceeds with the populated summary
- **Skip** — leave the placeholder in place. The user can fill it manually or run `/dossier:executive-summary` later

In non-interactive runs, skip. The placeholder is honest — better than an unreviewed auto-generated summary.

## Step 6: Render to PDF

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

## Step 7: Output

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
- **`h2` for the table of contents and executive summary.** Both must be `h2` so they flow on page 2 (after the cover's forced break) without inserting additional blank pages. The first `h1` is reserved for the first embedded report.
- **Don't auto-fix ineligible files.** If a file is missing `category` or `date`, that's a producer-side issue. Surface it; let the user fix the source.
- **Confirm before writing.** The user gets a candidate list and chooses scope before any output is produced.

## Output format

Two paths and a one-line summary. See Step 7.

## Related

- `/dossier:dossier` agent — drive mode. Asks what to investigate, dispatches investigator/analyst skills, then calls this skill on completion.
- `/dossier:executive-summary` — fills the executive summary placeholder. Offered as a sub-step here (Step 5) and also callable standalone.
- `/publishing:write-document-pdf` — the renderer this skill calls. Invoked with `--css <dossier-css>` so the page-break rule is applied.
- `report-conventions.md` rule — the frontmatter contract every conforming report follows, including the body-heading clause.
