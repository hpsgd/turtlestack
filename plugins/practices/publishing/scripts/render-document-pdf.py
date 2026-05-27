#!/usr/bin/env python3
"""Render a markdown document to a brand-styled A4 PDF.

Reads markdown, parses with python-markdown (tables, fenced_code, footnotes,
attr_list, meta, sane_lists), wraps in HTML with the resolved stylesheet, and
hands off to xhtml2pdf to produce the PDF.

Cover page: optional, driven by YAML frontmatter. If the markdown begins with
a YAML preamble (`---` delimited) containing `title` (and optionally `subtitle`,
plus any other key/value metadata), the renderer injects a `.cover` div before
the document body. The default stylesheet has `@page :first` rules that style
the first page as a cover.

Stylesheet resolution: --css <path> takes precedence; otherwise --style <name>
resolves to assets/styles/<name>.css under this plugin (default: report).

Usage:
  render-document-pdf.py <markdown> --out <pdf>
  render-document-pdf.py <markdown> --out <pdf> --style report
  render-document-pdf.py <markdown> --out <pdf> --css /path/to/custom.css
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    import markdown
    from xhtml2pdf import pisa
except ImportError as e:
    sys.stderr.write(
        f"Missing dependency: {e}. This script normally runs inside the "
        "bundled Docker image (render-document-pdf.sh wrapper); to run it "
        "directly outside the container: pip install --constraint "
        "constraints.txt xhtml2pdf markdown\n"
    )
    sys.exit(2)


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = PLUGIN_ROOT / "assets"
STYLES_DIR = ASSETS_DIR / "styles"
FONTS_DIR = ASSETS_DIR / "fonts"

MARKDOWN_EXTENSIONS = [
    "tables",
    "fenced_code",
    "footnotes",
    "attr_list",
    "meta",
    "sane_lists",
]

# Frontmatter keys that, when present, get rendered as a key/value table on the
# cover page. Anything else in the frontmatter is ignored at render time.
COVER_METADATA_KEYS = ("date", "author", "client", "subject", "version", "status")


@dataclass(frozen=True)
class Frontmatter:
    title: str | None
    subtitle: str | None
    metadata: dict[str, str]


def _strip_frontmatter(md_text: str) -> tuple[Frontmatter | None, str]:
    """Split off a leading YAML frontmatter block, if present.

    We avoid pulling PyYAML — frontmatter here is a flat key:value map and we
    only need a few specific keys. A handful of regex parses cover the cases
    we care about.
    """
    if not md_text.startswith("---\n"):
        return None, md_text

    end = md_text.find("\n---\n", 4)
    if end < 0:
        return None, md_text

    block = md_text[4:end]
    body = md_text[end + 5 :]

    parsed: dict[str, str] = {}
    for line in block.splitlines():
        m = re.match(r"^([A-Za-z][\w-]*)\s*:\s*(.*?)\s*$", line)
        if m:
            key = m.group(1).strip().lower()
            value = m.group(2).strip().strip('"').strip("'")
            parsed[key] = value

    if not parsed.get("title"):
        return None, body

    metadata = {k: parsed[k] for k in COVER_METADATA_KEYS if parsed.get(k)}
    return (
        Frontmatter(
            title=parsed.get("title"),
            subtitle=parsed.get("subtitle"),
            metadata=metadata,
        ),
        body,
    )


def _cover_html(fm: Frontmatter) -> str:
    rows = "".join(
        f'<tr><th>{k.title()}</th><td>{v}</td></tr>'
        for k, v in fm.metadata.items()
    )
    table = f'<table class="cover-meta"><tbody>{rows}</tbody></table>' if rows else ""
    subtitle = (
        f'<div class="cover-subtitle">{fm.subtitle}</div>'
        if fm.subtitle
        else ""
    )
    return (
        '<div class="cover">'
        f'<h1 class="cover-title">{fm.title}</h1>'
        f"{subtitle}"
        f"{table}"
        "</div>"
    )


def _resolve_css(style: str, css_path: Path | None) -> str:
    """--css <path> wins; otherwise --style <name> resolves to bundled CSS."""
    if css_path is not None:
        if not css_path.exists():
            sys.stderr.write(f"--css path not found: {css_path}\n")
            sys.exit(2)
        return css_path.read_text(encoding="utf-8")

    bundled = STYLES_DIR / f"{style}.css"
    if not bundled.exists():
        available = ", ".join(sorted(p.stem for p in STYLES_DIR.glob("*.css"))) or "(none)"
        sys.stderr.write(
            f"--style {style!r} not found at {bundled}. "
            f"Available styles: {available}\n"
        )
        sys.exit(2)
    return bundled.read_text(encoding="utf-8")


def _font_face_block() -> str:
    """Inject @font-face declarations pointing at the vendored TTFs.

    xhtml2pdf wants a bare absolute path inside `url(...)` — not a `file://`
    URL. With that path, the parser registers the TTF and emits it as an
    embedded font in the PDF. Only normal/bold weights are declared because
    xhtml2pdf's CSS parser rejects numeric font-weight values.
    """
    fonts = [
        ("Mona Sans", "MonaSans-Regular.ttf", "normal"),
        ("Mona Sans", "MonaSans-Bold.ttf", "bold"),
        ("Inter", "Inter-Regular.ttf", "normal"),
        ("Inter", "Inter-Bold.ttf", "bold"),
    ]
    blocks: list[str] = []
    for family, filename, weight in fonts:
        path = FONTS_DIR / filename
        if not path.exists():
            continue
        blocks.append(
            "@font-face { "
            f'font-family: "{family}"; '
            f'src: url("{path}"); '
            f"font-weight: {weight}; "
            "font-style: normal; "
            "}"
        )
    return "\n".join(blocks)


def render(
    md_path: Path,
    pdf_path: Path,
    style: str,
    css_path: Path | None,
) -> None:
    md_text = md_path.read_text(encoding="utf-8")
    fm, body_text = _strip_frontmatter(md_text)

    md = markdown.Markdown(extensions=MARKDOWN_EXTENSIONS)
    html_body = md.convert(body_text)

    fonts = _font_face_block()
    css = _resolve_css(style, css_path)
    cover = _cover_html(fm) if fm else ""

    # The page-number frame is conventional for xhtml2pdf — a div with id=footer
    # bound via @frame footer { -pdf-frame-content: footer; ... } in the CSS.
    footer = (
        '<div id="footer">Page <pdf:pagenumber> of <pdf:pagecount></div>'
    )

    html = f"""<!doctype html>
<html><head><meta charset="utf-8"><style>{fonts}\n{css}</style></head>
<body>
{footer}
{cover}
{html_body}
</body></html>"""

    with pdf_path.open("wb") as out:
        result = pisa.CreatePDF(html, dest=out, encoding="utf-8")

    if result.err:
        sys.stderr.write(f"xhtml2pdf reported {result.err} error(s)\n")
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render a markdown document to a brand-styled A4 PDF.",
    )
    parser.add_argument("markdown", type=Path, help="Path to the markdown source.")
    parser.add_argument(
        "--out", type=Path, required=True, help="Path to write the PDF.",
    )
    parser.add_argument(
        "--style",
        default="report",
        help="Bundled stylesheet name (assets/styles/<name>.css). Default: report.",
    )
    parser.add_argument(
        "--css",
        type=Path,
        default=None,
        help="Path to a custom CSS file. Takes precedence over --style.",
    )
    args = parser.parse_args()

    if not args.markdown.exists():
        sys.stderr.write(f"Markdown not found: {args.markdown}\n")
        sys.exit(2)

    render(args.markdown, args.out, args.style, args.css)
    print(args.out)


if __name__ == "__main__":
    main()
