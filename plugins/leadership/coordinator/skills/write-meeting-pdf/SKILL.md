---
name: write-meeting-pdf
description: "Render a meeting Q-and-A document as a printable PDF for note-taking on a Remarkable Paper Pro. Cover page is a fillable form (date, time, attendees, apologies, topic allocations); subsequent pages give each agenda item half a page with a NOTES area and a 5-row ACTIONS block. Brand-aware (hps.gd colours, Mona Sans + Inter typography) and optimised for Gallery 3 colour e-ink. Defaults to the most recent qanda.md under `docs/meetings/`."
argument-hint: "[path to qanda.md] [--dir <path>] [--out <path>] [--refresh-assets]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Write Meeting PDF

Render an existing meeting Q-and-A document into a printable PDF designed for handwritten note-taking on a Remarkable Paper Pro tablet. The PDF is built from `qanda.md` (sections + items + talking points + questions) and its sibling `agenda.md` (cover-page metadata).

The output is a single PDF stored alongside the input by default. The cover page is a fillable form — date, time, attendees, and apologies are blank to be written in on the meeting day. Each section's pages mirror the qanda's structure with two items per page; each item has talking points and questions printed at the top, then a generous ruled NOTES area, then a 5-row ACTIONS block with checkboxes.

## Step 1: Resolve qanda path to absolute

Parse `$ARGUMENTS`:

- If a path ending in `.md` is provided, use it as the qanda path.
- Otherwise:
  - If `--dir <path>` provided, resolve under that root; else `docs/meetings/`.
  - Find the most recently modified `qanda.md` under that root and use it.

Use `Bash` to compute the absolute path:

```bash
ARG="<input path or directory>"
case "$ARG" in
  /*) ABS="$ARG" ;;
  *) ABS="$(pwd)/$ARG" ;;
esac
[ -d "$ABS" ] && ABS=$(find "$ABS" -name 'qanda.md' -type f -print0 | xargs -0 ls -t 2>/dev/null | head -1)
echo "$ABS"
```

If no qanda is found, stop and report. The qanda must have a sibling `agenda.md` — the renderer reads both.

## Step 2: Resolve output path

By default the PDF is written as `<meeting-folder>/meeting.pdf`. The user can override with `--out <path>`. If override is relative, resolve against `pwd`.

## Step 3: Invoke the renderer

The renderer is a standalone script. Use the wrapper at `${CLAUDE_PLUGIN_ROOT}/scripts/render-meeting-pdf.sh` — it runs `render-meeting-pdf.py` inside a Docker image built from `${CLAUDE_PLUGIN_ROOT}/scripts/Dockerfile` on first run (~30-60s) and reuses it thereafter. The only host requirement is Docker. The image bundles `reportlab` plus the brand fonts and logos from the publishing plugin's `assets/` directory:

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/render-meeting-pdf.sh" \
  --qanda <absolute path to qanda.md> \
  --out <absolute path to output.pdf>
```

Don't pass `--refresh-assets` from this skill. The flag re-downloads brand SVGs into `practices/publishing/assets/`, which only makes sense against a writable repo checkout — inside the Docker container the assets are baked into the image and any refresh writes are lost on exit. `--refresh-assets` is a maintainer-only path: run `python plugins/leadership/coordinator/scripts/render-meeting-pdf.py --refresh-assets ...` directly against the marketplace repo to update vendored assets, then commit the result.

The script prints the output path on success and exits non-zero on failure. Capture stderr so any rendering errors surface back to the user.

## Step 4: Confirm path

Output the absolute path to the generated PDF. Do not claim success without verifying the file exists and has non-zero size — `[ -s <path> ]`.

## Rules

- **Read-only on inputs.** Never modify `qanda.md` or `agenda.md` from this skill.
- **Don't open the PDF for the user.** Just report the path. Whether they sideload to a tablet, open in a viewer, or upload to a cloud service is their call.
- **Don't re-render if nothing has changed.** If `meeting.pdf` exists and is newer than both `qanda.md` and `agenda.md`, ask the user before overwriting.
- **Don't substitute fonts or colours.** The renderer chooses brand-consistent typography and a colour palette tuned for e-ink. If the user wants a variant, they can fork the script — don't adjust ad-hoc per invocation.
- **Surface bootstrap delays.** First run on a fresh machine builds the Docker image (~30-60s). Subsequent runs add ~1-2s of container startup. If the wrapper hangs longer than that, something is wrong — investigate, don't silently retry. If Docker is missing, the wrapper fails fast with exit 69 — tell the user to install Docker.

## Output Format

A single line: the absolute path to the generated PDF.

```
/Users/.../docs/meetings/2026-05-15-q2-board-meeting/meeting.pdf
```

## Layout reference

For the user's understanding of what the PDF contains:

| Page | Contents |
|---|---|
| 1 (cover) | Centred icon + wordmark, meeting title, fillable form table (Date / Time / Attendees / Apologies — all blank), Topics list with per-section colour swatches and time allocations summed against the meeting duration |
| 2..N (sections) | Header with section title (right-aligned). Two items per page. Per item: title in section accent colour, talking points + questions printed, ruled NOTES area, ACTIONS block with 5 ruled rows × 3 columns and a checkbox at the start of each row. Footer with brand icon and page indicator. |

The page is sized to the [Remarkable Paper Pro](https://remarkable.com/paper-pro) native (1620 × 2160 px @ 229 PPI; ~509 × 679 pt). The leftmost ~38 pt is left blank to accommodate the device's stylus toolbar (right-hander default; if you use the device left-handed, the toolbar mirrors and the margin remains usable).

## Related Skills

- `/coordinator:write-meeting-agenda` — produces the agenda this skill consumes (via the qanda).
- `/coordinator:write-meeting-qanda` — produces the Q-and-A document this skill renders. Run that first.
