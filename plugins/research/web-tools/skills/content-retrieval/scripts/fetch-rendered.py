#!/usr/bin/env python3
"""Fetch a URL with Playwright/Chromium and print the rendered HTML to stdout.

Used by the content-retrieval skill at Tier 3 (JavaScript-rendered pages) so
the skill doesn't depend on the user having Playwright installed locally.

Usage:
  fetch-rendered.py <url> [--wait-for <selector>] [--timeout <ms>] [--wait-after <ms>]

Defaults: timeout 30000ms, wait-until networkidle, no extra wait after load.
"""

from __future__ import annotations

import argparse
import sys

from playwright.sync_api import sync_playwright


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("url", help="URL to fetch")
    p.add_argument(
        "--wait-for",
        help="CSS selector to wait for before reading the DOM",
    )
    p.add_argument(
        "--timeout",
        type=int,
        default=30000,
        help="Navigation timeout in ms (default 30000)",
    )
    p.add_argument(
        "--wait-after",
        type=int,
        default=0,
        help="Additional ms to wait after load before reading DOM (default 0)",
    )
    args = p.parse_args()

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        try:
            context = browser.new_context()
            page = context.new_page()
            page.goto(args.url, wait_until="networkidle", timeout=args.timeout)
            if args.wait_for:
                page.wait_for_selector(args.wait_for, timeout=args.timeout)
            if args.wait_after:
                page.wait_for_timeout(args.wait_after)
            sys.stdout.write(page.content())
        finally:
            browser.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
