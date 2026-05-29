---
name: write-document-pdf
description: "Render a markdown document as a brand-styled A4 PDF (hps.gd typography and palette). Optional cover page from YAML frontmatter (title, subtitle, metadata). Use --style <name> for a bundled stylesheet (default: report) or --css <path> for a project-specific CSS file. Runs inside a Docker image (xhtml2pdf + python-markdown) — Docker is the only host requirement."
argument-hint: "<path to markdown> [--out <path>] [--style <name>] [--css <path>]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Write Document PDF

Render a markdown file into a brand-styled A4 PDF. Suitable for assessments, reports, briefs, and any prose document that needs a clean, brand-consistent layout. The renderer handles tables, blockquotes, code blocks, footnotes, and Unicode well.

For meeting notes (cover with attendee blanks, two items per page with NOTES + ACTIONS blocks for handwritten capture), use `/coordinator:write-meeting-pdf` instead — that skill is purpose-built for the Remarkable Paper Pro form factor.

## Step 1: Resolve markdown path to absolute

The first non-flag argument is the markdown source. Required.

```bash
ARG="<path>"
case "$ARG" in
  /*) ABS="$ARG" ;;
  *) ABS="$(pwd)/$ARG" ;;
esac
```

If the path doesn't exist or isn't a `.md` file, stop and report.

## Step 2: Resolve output path

By default the PDF is written next to the markdown with the same stem (`foo.md` → `foo.pdf`). Override with `--out <path>`. If the override is relative, resolve against `pwd`.

## Step 3: Resolve stylesheet selection

Two flags, mutually exclusive in effect (`--css` wins if both passed):

- `--style <name>` — selects a bundled stylesheet at `${CLAUDE_PLUGIN_ROOT}/assets/styles/<name>.css`. Defaults to `report` if neither flag given.
- `--css <path>` — points at a project-specific CSS file. Resolve to absolute the same way as the markdown path. The file must exist.

The bundled `report` style is brand-styled (Mona Sans display, Inter body, hps.gd palette) and is the right default for internal reports and assessments. Use `--css` when a downstream project (a client deliverable, a tortoisestack assessment with project-specific theming) needs different styling.

## Step 4: Invoke the renderer

The renderer is at `${CLAUDE_PLUGIN_ROOT}/scripts/render-document-pdf.sh` — a wrapper that runs `render-document-pdf.py` inside a Docker image. The only host requirement is Docker. On first run the wrapper pulls a pre-built image from `ghcr.io/hpsgd/turtlestack-publishing-document-pdf:<plugin-version>` (~338MB) and caches it. If the registry is unreachable (offline, GHCR outage, fork without registry access) the wrapper falls back to building locally from `${CLAUDE_PLUGIN_ROOT}/scripts/Dockerfile` (~30-60s). A hash-tagged local image, if present, takes precedence over the registry tag — that path supports dev iteration on the Dockerfile without round-tripping through a release.

User-supplied paths under `$HOME` and `/tmp` resolve inside the container identically (both are bind-mounted at the same path). For markdown sources or CSS files outside both, set `TURTLESTACK_DOCKER_MOUNTS` to a colon-separated list of extra host paths to bind-mount.

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/render-document-pdf.sh" \
  <absolute markdown path> \
  --out <absolute output path> \
  [--style <name>] \
  [--css <absolute css path>]
```

The script prints the output path on success and exits non-zero on failure. Capture stderr so any rendering errors surface back to the user.

## Step 5: Verify the output

Don't claim success without running these checks:

```bash
# File exists and is non-empty
[ -s <path> ] || { echo "render failed: empty or missing output"; exit 1; }

# Valid PDF and page count
file <path>

# Embedded fonts — Mona Sans + Inter should both appear; absence means a silent fallback to Helvetica
pdffonts <path> 2>/dev/null || grep -ao '/BaseFont [^ ]*' <path> | sort -u
```

`file <path>` reports something like `PDF document, version 1.4, 2 pages` — copy that line into the chat so the page count and PDF magic are visible. `pdffonts` (or the `grep` fallback when `pdffonts` isn't installed) confirms the brand fonts embedded; if `MonaSans-Regular` and `Inter-Regular` are missing, the render fell back to Helvetica and the user needs to know.

## Step 6: Report what happened

After verification, surface the following in your chat reply:

- The absolute path to the PDF.
- The mechanism — name the wrapper script (`render-document-pdf.sh`) so the user knows what fired. If this was a first run, mention whether the image was pulled from GHCR or built locally as a fallback; otherwise note that the cached image was reused.
- The verification evidence — the `file` output (page count, PDF version) and the embedded font check.
- A one-line note on typical next steps for a document PDF: sharing with stakeholders, archiving alongside source markdown, or sideloading to a tablet for review. Don't open the PDF.

## Cover page from frontmatter

If the markdown begins with a YAML frontmatter block containing a `title` field, the renderer emits a cover page before the body. Recognised keys: `title` (required to trigger the cover), `subtitle`, plus any of `date`, `author`, `client`, `subject`, `version`, `status` for the metadata table. Other keys are ignored at render time.

Example markdown:

```markdown
---
title: External Product Assessment
subtitle: VisualCare
date: 2026-04-24
author: Martin Lau
status: Draft
---

# Executive summary

...
```

If there's no frontmatter or no `title`, no cover is rendered — the document starts on page 1 with the body.

## Rules

- **Read-only on the markdown source.** Never modify the input.
- **Don't open the PDF for the user.** Just report the path.
- **Don't re-render if nothing has changed.** If the output file exists and is newer than both the markdown and the chosen stylesheet, ask before overwriting.
- **Surface bootstrap delays.** First run on a fresh machine pulls the pre-built image from GHCR (seconds to tens of seconds depending on connection); local-build fallback takes ~30-60s. Subsequent runs add ~1-2s of container startup. If the wrapper hangs longer than that, something is wrong — investigate, don't silently retry. If Docker isn't installed, the wrapper fails fast with a clear message; tell the user to install Docker rather than try to work around it.
- **Wide tables (7+ columns) may overflow.** xhtml2pdf has a known weak spot with wide tables. If the source markdown contains wide tables and the output overflows, options are (a) reduce columns, (b) write a custom CSS file with `table-layout: fixed; word-wrap: break-word; font-size: 8pt` for the affected tables, or (c) restructure the data.

## Output format

A single line: the absolute path to the generated PDF.

```
/path/to/document.pdf
```

## Related skills

- `/coordinator:write-meeting-pdf` — purpose-built for printable meeting notes on a Remarkable Paper Pro (fillable form cover, two items per page with NOTES + ACTIONS blocks). Different output, different audience.
