---
name: web-snapshot
description: "Save a web page as a rendered PDF using shot-scraper (Playwright/Chromium). Use to archive primary-source evidence for research — bot-protected and JS-rendered pages included. Different job from /web-tools:content-retrieval: this produces a PDF file for the evidence folder, content-retrieval returns text for analysis."
argument-hint: "[URL to snapshot]"
user-invocable: true
allowed-tools: Bash
---

Snapshot the page at $ARGUMENTS to a PDF using the bundled `web-snapshot.py` script.

## When to use this skill

Use `/web-tools:web-snapshot` when you need a **PDF archive** of a page — typically the highest-tier source citations in research output. Use `/web-tools:content-retrieval` when you need the **text content** for analysis.

Both tools share an underlying capability (Playwright/Chromium can render JS-heavy and bot-protected pages), but the output shape is different and the consumers are different.

## Prerequisites

Docker is the only host requirement. The wrapper at `${CLAUDE_PLUGIN_ROOT}/skills/web-snapshot/scripts/web-snapshot.sh` uses a Playwright-based image (Microsoft's official base + [shot-scraper](https://shot-scraper.datasette.io)).

On first run the wrapper pulls a pre-built image from `ghcr.io/hpsgd/turtlestack-web-snapshot:<plugin-version>` (~3.9GB; a few minutes on a slow link). If the registry is unreachable it falls back to building locally from the Dockerfile, which also pulls the Playwright base. The image shares its Playwright base layer with the `content-retrieval` image — if either is cached locally the other is much faster. Subsequent invocations add ~2s of container startup. Confirm Docker is available before running:

```bash
command -v docker || echo "MISSING — install Docker Desktop or the docker engine"
```

If Docker isn't installed, stop and tell the user. The wrapper fails fast with exit 69 in that case.

## Single URL

```bash
"${CLAUDE_PLUGIN_ROOT}/skills/web-snapshot/scripts/web-snapshot.sh" \
  --url "https://example.com/page" \
  --name "example-page" \
  --out ./evidence/web-snapshots
```

Output filename: `{YYYY-MM}--{name}.pdf` (e.g. `2026-05--example-page.pdf`). The date prefix groups snapshots by month for sources registers and makes the filename self-describing.

If `--name` is omitted, the script derives a slug from the URL host and path. Always prefer an explicit `--name` matching the source ID or human-readable label in the sources register.

## Batch mode

For multiple URLs in one pass, write a JSON file:

```json
{
  "urls": [
    { "url": "https://example.com/page", "name": "example-page" },
    { "url": "https://other.com/article", "name": "other-article" }
  ]
}
```

Then:

```bash
"${CLAUDE_PLUGIN_ROOT}/skills/web-snapshot/scripts/web-snapshot.sh" \
  --urls sources.json \
  --out ./evidence/web-snapshots
```

Existing files are skipped — re-running is incremental.

## Useful options

| Flag | Purpose |
|---|---|
| `--wait <ms>` | Milliseconds to wait after load before capture (default 2000). Increase for slow-rendering pages |
| `--timeout <ms>` | Navigation timeout (default 30000) |
| `--format <a4\|letter>` | Page format (default a4) |
| `--landscape` | Landscape orientation |
| `--no-date` | Omit the YYYY-MM filename prefix |

## On the captured PDF

The script injects a small header bar at the top of every snapshot showing the source URL and capture date. This is what makes the PDF self-evidencing — a reader can see where it came from and when, without consulting the sources register.

## Reporting

After the run, the script prints `OK: N  Skipped: N  Failed: N`. Surface that line back to the user. If any URLs failed, list them with their error so the user can decide whether to retry or escalate to manual capture.

## When this won't work

The script is bot-resistant but not bot-immune. If shot-scraper fails on a Cloudflare/Datadome-protected page, fall through to `/web-tools:content-retrieval`'s Tier 4 (human escalation) — ask the user to capture the page manually via their browser's Print → Save as PDF.
