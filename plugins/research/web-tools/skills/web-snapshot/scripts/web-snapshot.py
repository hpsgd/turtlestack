#!/usr/bin/env python3
"""
Save web pages as rendered PDFs using shot-scraper (Playwright/Chromium).

Usage:
  python web-snapshot.py --url "https://example.com" --name "example-page" --out ./snapshots
  python web-snapshot.py --urls sources.json --out ./snapshots

Single URL mode:
  --url     URL to snapshot
  --name    Slug for the output filename (optional, derived from URL if omitted)
  --out     Output directory (default: ./web-snapshots)

Batch mode (sources.json):
  {
    "urls": [
      { "url": "https://example.com/page", "name": "example-page" },
      { "url": "https://other.com", "name": "other-site" }
    ]
  }

Output: {YYYY-MM}--{name}.pdf per URL in the --out directory.

Options:
  --wait       Milliseconds to wait after load (default: 2000)
  --timeout    Navigation timeout in ms (default: 30000)
  --no-date    Omit the YYYY-MM prefix from filenames
  --format     Page format: a4, letter, etc. (default: a4)
  --landscape  Use landscape orientation

Prerequisites:
  pip install shot-scraper
  shot-scraper install
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


def slug_from_url(url: str) -> str:
    try:
        parsed = urlparse(url)
        host = re.sub(r"^www\.", "", parsed.hostname or "")
        path = parsed.path.strip("/").replace("/", "-")
        slug = f"{host}--{path}" if path else host
    except Exception:
        slug = url
    slug = re.sub(r"[^a-z0-9-]", "-", slug, flags=re.IGNORECASE)
    slug = re.sub(r"-+", "-", slug)
    return slug[:80]


def date_prefix() -> str:
    now = datetime.now(timezone.utc)
    return f"{now.year}-{now.month:02d}--"


# JS injected into the page before PDF capture — adds a source URL and date bar
def header_js(url: str, date: str) -> str:
    return (
        "(() => {"
        "const d = document.createElement('div');"
        "d.style.cssText = 'position:relative;width:100%;padding:4px 8px;"
        "font-size:9px;color:#666;border-bottom:1px solid #ddd;"
        "font-family:system-ui,sans-serif;display:flex;"
        "justify-content:space-between;box-sizing:border-box;';"
        f"d.innerHTML = '<span>{url}</span><span>Snapshot: {date}</span>';"
        "document.body.insertBefore(d, document.body.firstChild);"
        "})()"
    )


def snapshot(entry: dict, out_dir: Path, args: argparse.Namespace) -> dict:
    prefix = "" if args.no_date else date_prefix()
    filename = f"{prefix}{entry['name']}.pdf"
    out_path = out_dir / filename

    if out_path.exists():
        print(f"  {entry['name']}: already exists, skipping")
        return {"name": entry["name"], "status": "skipped"}

    print(f"  {entry['name']}: {entry['url']}")

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    js = header_js(entry["url"], today)

    cmd = [
        "shot-scraper", "pdf",
        entry["url"],
        "-o", str(out_path),
        "--javascript", js,
        "--wait", str(args.wait),
        "--timeout", str(args.timeout),
        "--format", args.format,
        "--print-background",
        "--media-screen",
    ]
    if args.landscape:
        cmd.append("--landscape")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        err = (result.stderr or result.stdout or "unknown error").strip()[:200]
        print(f"  {entry['name']}: FAILED — {err}")
        return {"name": entry["name"], "status": "error", "error": err}

    print(f"  {entry['name']}: saved → {filename}")
    return {"name": entry["name"], "status": "ok", "path": str(out_path)}


def main():
    parser = argparse.ArgumentParser(description="Snapshot web pages to PDF")
    parser.add_argument("--url", help="Single URL to snapshot")
    parser.add_argument("--urls", help="JSON file with URL list")
    parser.add_argument("--name", help="Slug for output filename (single URL mode)")
    parser.add_argument("--out", default="./web-snapshots", help="Output directory")
    parser.add_argument("--wait", type=int, default=2000, help="Wait ms after load")
    parser.add_argument("--timeout", type=int, default=30000, help="Navigation timeout ms")
    parser.add_argument("--no-date", action="store_true", help="Omit YYYY-MM prefix")
    parser.add_argument("--format", default="a4", help="Page format (a4, letter, etc.)")
    parser.add_argument("--landscape", action="store_true", help="Landscape orientation")
    args = parser.parse_args()

    queue: list[dict] = []

    if args.urls:
        with open(args.urls) as f:
            config = json.load(f)
        entries = config.get("urls", config)
        if not isinstance(entries, list):
            print("JSON file must contain a 'urls' array or be an array", file=sys.stderr)
            sys.exit(1)
        for entry in entries:
            if not entry.get("url"):
                print(f"Entry missing 'url': {entry}", file=sys.stderr)
                continue
            queue.append({
                "url": entry["url"],
                "name": entry.get("name") or slug_from_url(entry["url"]),
            })
    elif args.url:
        queue.append({
            "url": args.url,
            "name": args.name or slug_from_url(args.url),
        })
    else:
        parser.print_help()
        sys.exit(1)

    if not queue:
        print("No URLs to snapshot.", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Snapshotting {len(queue)} URL(s) → {out_dir}\n")

    results = [snapshot(entry, out_dir, args) for entry in queue]

    ok = sum(1 for r in results if r["status"] == "ok")
    skipped = sum(1 for r in results if r["status"] == "skipped")
    failed = sum(1 for r in results if r["status"] == "error")

    print(f"\nDone. OK: {ok}  Skipped: {skipped}  Failed: {failed}")

    if failed > 0:
        print("\nFailures:")
        for r in results:
            if r["status"] == "error":
                print(f"  {r['name']}: {r['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
