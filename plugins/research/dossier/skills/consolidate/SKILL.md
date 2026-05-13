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

Then ask a third `AskUserQuestion` about **Table of Contents depth**. Use the `preview` field on each option to show what the TOC will look like — render a small example built from the actual report titles in this run (and a couple of real h2s for the H1+H2 option) so the user can see the difference:

- **H1 only (Recommended)** — one bullet per report. Compact and scannable. This is the default.
- **H1 + H2** — nested: each report plus the section headings inside it. Use this when reports are long enough that section-level navigation is useful
- **No table of contents** — skip the Contents page entirely. The dossier flows from cover straight to the executive summary

The executive summary and the Appendices section never appear in the TOC regardless of depth — the executive summary follows the TOC directly, and appendices are reached by reading to the end.

In non-interactive runs (no user available to answer questions — driven from another agent, a script, or a test harness), skip all three AskUserQuestion steps and proceed with all eligible files, default category order, and H1-only TOC. Surface body-h1 warnings in the completion summary when any exist; silence is acceptable when there are none.

## Step 4: Build DOSSIER.md

Write `$ENG/DOSSIER.md`. The structure is:

1. **Dossier frontmatter** — produces the cover page when rendered
1. **Table of Contents** as `## Contents` — lands on page 2 (the cover forces a page break). Links to category reports only — omit the executive summary, the Appendices divider, and individual appendix titles. Skip this section entirely if the user chose "No table of contents" in Step 3
1. **Executive summary** as `h1` — `# Executive summary` forces its own page break. Not linked from the TOC
1. **One `h1` per embedded category report** — each report becomes its own page-break boundary and is the primary TOC target
1. **Appendices section** (only if there are appendix files) — `# Appendices` divider, then `# <Appendix title>` per file. Each h1 forces a page break. Not linked from the TOC

Categories drive **ordering only** in the main body. There are no visible category dividers. The default order is `People` → `Corporate` → `Commercial` → `Technical` → `OSINT` → any other categories alphabetically. The user can override this in Step 3; use whatever order they chose.

Appendices come after all category reports, separated from the main body by a single `# Appendices` divider page (its own page break). Inside, appendices order by filename alphabetically.

### Anchor scheme

Every heading the TOC links to needs an inline `<a name="…">` anchor. **Do not rely on `{#id}` attr_list syntax** — the python-markdown attr_list extension emits `id="…"` on the heading, which xhtml2pdf does not consistently treat as a navigable PDF anchor. The named-anchor element is the historically-reliable pattern. Embed it inside the heading text so the markdown stays clean:

```markdown
# <a name="report-1"></a>Michael Graves
```

The id scheme is sequential so collisions are impossible:

| Element | Anchor |
|---|---|
| Nth category report's title h1 | `report-N` (1-indexed in final emitted order across the whole dossier) |
| Mth h2 inside category report N | `report-N-sM` |

Only emit anchors that the TOC will actually link to. With H1-only depth, anchor every report h1 and leave h2s alone. With H1+H2 depth, anchor report h1s and every h2 in their bodies. With No TOC, emit no anchors at all.

Don't anchor the executive summary, the Appendices divider, individual appendix titles, or h2s inside appendices — none of them appear in the TOC. h3+ headings are never anchored.

When embedding a report, rewrite each `^## (.+)$` line to `## <a name="report-N-sM"></a>$1` (only when H1+H2 depth is selected), counting H2s as they appear. The h1 you inject for the report's title always gets `<a name="report-N"></a>` when a TOC exists.

### Table of Contents

Emit `## Contents` immediately after the dossier frontmatter. The body is a markdown bullet list — one entry per category report. When the user picked H1+H2 depth, each entry has a nested sub-list of the report's h2s. Skip the section entirely when the user picked "No table of contents".

Example shape (H1 only):

```markdown
## Contents

- [Michael Graves](#report-1)
- [Susan Lau](#report-2)
- [VisualCare Pty Ltd](#report-3)
- [visualcare.com.au](#report-4)
```

Example shape (H1 + H2):

```markdown
## Contents

- [Michael Graves](#report-1)
  - [Roles and directorships](#report-1-s1)
  - [Public profile](#report-1-s2)
- [Susan Lau](#report-2)
  - [Roles and directorships](#report-2-s1)
- [VisualCare Pty Ltd](#report-3)
  - [Corporate structure](#report-3-s1)
  - [Beneficial ownership](#report-3-s2)
```

Link text is the verbatim heading text. Don't truncate.

Template (with H1-only TOC):

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

- [<Report 1 title>](#report-1)
- [<Report 2 title>](#report-2)
...

# Executive summary

<!-- TODO: write a 3-5 paragraph summary covering the engagement target, scope of the investigation, and the headline findings across all categories. The dossier agent fills this in drive mode; in standalone consolidate runs, leave the placeholder for the user. -->

# <a name="report-1"></a><Report 1 title — verbatim from frontmatter>

<full embedded body of report 1, frontmatter stripped>

# <a name="report-2"></a><Report 2 title>

...

# Appendices

# <Appendix 1 title — verbatim from frontmatter>

<full embedded body of appendix 1, frontmatter stripped>

# <Appendix 2 title>

...
```

For H1+H2 TOC, the only differences are: the TOC includes nested h2 entries, and each embedded report's body h2s get rewritten to `## <a name="report-N-sM"></a><heading text>`. The executive summary and appendices are unchanged.

For "No table of contents", omit the `## Contents` block entirely and emit no anchors. Everything else is the same.

Rules for embedding:

- **Strip the leading `---...---` frontmatter block** from each embedded report. Frontmatter values (`author`, `date`, `source`, `confidence`, `status`, etc.) are metadata, not body content — do not render them as visible text in the dossier
- **Do NOT demote headings.** The body is already `h2+` per the report-conventions rule. If a body has an `h1` (contract violation, flagged in Step 3), embed it as-is — the result will be visually wrong but doesn't require special handling here
- **Inject one `h1` per report** with the verbatim `title` from the report's frontmatter, prefixed with `<a name="report-N"></a>` when a TOC exists
- **Rewrite body h2s** to include `<a name="report-N-sM"></a>` only when the user picked H1+H2 TOC depth. With H1-only or No TOC, leave body h2s untouched. h3+ headings are always left alone
- **Category report order:** by category (default `People` → `Corporate` → `Commercial` → `Technical` → `OSINT` → alphabetical for any other, unless the user supplied a custom order in Step 3), then by `subject` if present, then by `date`, then by filename
- **No category headings.** Don't write `# People` or any category-level visible separator. Ordering carries the grouping
- **Executive summary as h1.** Emit `# Executive summary` before the first category report. No anchor — the TOC doesn't link to it
- **Appendix section:** emit a single `# Appendices` divider after the last category report only when there are appendix files. Then embed each appendix the same way as a category report — one `h1` per file with the verbatim `title`. No anchors on the divider or the appendix h1s — the TOC doesn't link to them. h2s inside appendix bodies are also left unanchored
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
- **Every `h1` forces a page break.** Use `h1` only for: the executive summary, each category report, the Appendices divider, and each appendix. Don't introduce h1s anywhere else. Don't keep body h1s from source reports — the rule forbids those — but if you find one anyway, embed as-is and the result will be visually wrong (Step 3 flags this).
- **No provenance in the body.** Frontmatter fields (`author`, `date`, `source`, `confidence`, `status`) are metadata. The reader sees the report title and content, not who wrote it or when. The provenance is in the source file for audit if anyone needs it.
- **`h2` for the table of contents.** The TOC must be `h2` so it flows on page 2 (after the cover's forced break) without inserting an additional blank page. The executive summary, reports, and appendix sections are h1 and force their own page breaks.
- **TOC links use `<a name="…">` anchors, not `{#id}` attr_list.** xhtml2pdf treats named-anchor elements as reliable PDF link targets; the `id` attribute does not consistently resolve. Anchors are only emitted for elements the TOC actually links to (report h1s always, body h2s only at H1+H2 depth).
- **Don't auto-fix ineligible files.** If a file is missing `category` or `date`, that's a producer-side issue. Surface it; let the user fix the source.
- **Confirm before writing.** The user gets a candidate list and chooses scope before any output is produced.

## Output format

Two paths and a one-line summary. See Step 7.

## Related

- `/dossier:dossier` agent — drive mode. Asks what to investigate, dispatches investigator/analyst skills, then calls this skill on completion.
- `/dossier:executive-summary` — fills the executive summary placeholder. Offered as a sub-step here (Step 5) and also callable standalone.
- `/publishing:write-document-pdf` — the renderer this skill calls. Invoked with `--css <dossier-css>` so the page-break rule is applied.
- `report-conventions.md` rule — the frontmatter contract every conforming report follows, including the body-heading clause.
