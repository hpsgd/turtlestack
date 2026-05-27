#!/usr/bin/env python3
"""Render a meeting Q-and-A document to a printable PDF for note-taking.

Targets the Remarkable Paper Pro (RMPP): native page size 1620x2160 px @ 229 PPI,
which is 509x679 pt. Reserves ~38 pt on the left for the device toolbar.

Inputs: a qanda.md file produced by /coordinator:write-meeting-qanda. Reads its
sibling agenda.md for cover-page metadata (attendees, duration, type).

Outputs: a single PDF in the same folder by default, or at --out.

Usage:
  render-meeting-pdf.py --qanda <path>
  render-meeting-pdf.py --qanda <path> --out <path.pdf>
  render-meeting-pdf.py --qanda <path> --refresh-assets

Branding assets are vendored in the publishing plugin under
plugins/practices/publishing/assets/. With network available the script can
refresh them from hps.gd via --refresh-assets; otherwise the vendored copies
are used (sandbox-safe).
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

try:
    from reportlab.lib import colors
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen.canvas import Canvas
except ImportError as e:
    sys.stderr.write(
        f"Missing dependency: {e}. This script normally runs inside the "
        "bundled Docker image (render-meeting-pdf.sh wrapper); to run it "
        "directly outside the container: pip install reportlab\n"
    )
    sys.exit(2)


# Brand fonts (matches hps.gd: Mona Sans for display, Inter for body).
# Both fonts vendored under publishing/assets/fonts/. Registration happens once at
# import time; if a TTF is missing or unreadable we fall back to Helvetica so
# the script still produces a usable PDF.
FONT_DISPLAY = "Helvetica-Bold"
FONT_BODY = "Helvetica"
FONT_BODY_BOLD = "Helvetica-Bold"


def _register_brand_fonts(asset_dir: Path) -> None:
    """Register Mona Sans + Inter from vendored TTFs. Updates the FONT_*
    globals on success; leaves them on Helvetica defaults if registration
    fails for any reason (missing file, unsupported format, etc.).

    Weight choices: display drops to Regular for headings (less aggressive than
    Bold), body to Light for an airy form-feel, labels to Medium for emphasis
    without bulk."""
    global FONT_DISPLAY, FONT_BODY, FONT_BODY_BOLD
    fonts = {
        "MonaSans-Regular": asset_dir / "fonts" / "MonaSans-Regular.ttf",
        "Inter-Light": asset_dir / "fonts" / "Inter-Light.ttf",
        "Inter-Medium": asset_dir / "fonts" / "Inter-Medium.ttf",
    }
    try:
        for name, path in fonts.items():
            if not path.exists():
                return
            pdfmetrics.registerFont(TTFont(name, str(path)))
        FONT_DISPLAY = "MonaSans-Regular"
        FONT_BODY = "Inter-Light"
        FONT_BODY_BOLD = "Inter-Medium"
    except Exception:
        # Any registration failure: keep Helvetica defaults.
        pass

# --- Constants -------------------------------------------------------------

# Page geometry. RMPP native is 1620x2160 px @ 229 PPI -> 509x679 pt.
PAGE_W = 509.0
PAGE_H = 679.0

# Toolbar reservation on the left edge (left-handed users would mirror).
TOOLBAR_PT = 38.0

# Header/footer bands. The bands reserve vertical space for the section title
# (top) and brand icon + page indicator (bottom). No rule lines are drawn —
# the actions block's ruled rows on each item already give the page its
# horizontal visual structure.
HEADER_H = 28.0
FOOTER_H = 22.0

# Items per page. Two items per page gives each item ~half the usable height
# for write-on capture (~318 pt) — enough for ~14 ruled note lines plus a
# 5-row actions block per item.
ITEMS_PER_PAGE = 2
ACTIONS_ROWS = 5

# Branding assets live in the publishing plugin (single source of truth for
# brand fonts and logos shared across PDF renderers). PNGs are the render
# source; SVGs are vendored alongside as the source-of-truth shape.
#
# This is a hard cross-plugin dependency: coordinator@turtlestack will not
# render correctly without publishing@turtlestack installed. The path resolves
# relative to the script's location in the marketplace tree:
#   plugins/leadership/coordinator/scripts/  →  parents[3] = plugins/
#   then /practices/publishing/assets        →  the consolidated asset dir.
ASSET_DIR = Path(__file__).resolve().parents[3] / "practices" / "publishing" / "assets"


def _verify_assets_available() -> None:
    """Fail loud if the publishing plugin's assets dir is missing.

    Without this check, missing assets degrade silently: fonts fall back to
    Helvetica and logos are skipped, producing a structurally valid but
    visually wrong PDF that nobody notices until a customer sees it.
    """
    if ASSET_DIR.is_dir():
        return
    sys.stderr.write(
        f"Brand assets not found at {ASSET_DIR}.\n"
        "This usually means the publishing plugin is not installed alongside\n"
        "coordinator. Install it with: /plugin install publishing@turtlestack\n"
    )
    sys.exit(2)
LOGO_URL = "https://hps.gd/img/logos/hps.gd%20-%20logo.svg"
ICON_URL = "https://hps.gd/img/logos/hps.gd%20-%20icon.svg"

# Colour palette. Per RMPP Gallery 3 research: deep saturated tones used as
# thin rules and headings render well; pastel fills go muddy. All accents are
# muted/dark and used as left-margin rules and headings only — never fills.
HEADING_COLOR = colors.HexColor("#1A2B3C")  # slate
RULE_COLOR = colors.HexColor("#9CA3AF")  # neutral grey for thin separators
TEXT_COLOR = colors.HexColor("#111827")  # near-black for body
MUTED_COLOR = colors.HexColor("#4B5563")  # secondary text

SECTION_COLORS = [
    colors.HexColor("#8B1A1A"),  # deep red
    colors.HexColor("#0A2A66"),  # navy
    colors.HexColor("#1F5230"),  # forest green
    colors.HexColor("#5A1F4F"),  # plum
    colors.HexColor("#8A5A12"),  # dark amber
    colors.HexColor("#2C4150"),  # slate
]

# --- Data model ------------------------------------------------------------


@dataclass
class MeetingItem:
    title: str
    talking_points: list[str] = field(default_factory=list)
    questions: list[str] = field(default_factory=list)


@dataclass
class MeetingSection:
    name: str  # full heading without (N min) suffix
    duration_min: int | None
    items: list[MeetingItem] = field(default_factory=list)


@dataclass
class Meeting:
    title: str
    date: str
    duration_minutes: int
    type: str
    attendees: list[str]
    summary: str
    sections: list[MeetingSection]


# --- Parsing ---------------------------------------------------------------

_SECTION_RE = re.compile(r"^##\s+(.+?)(?:\s*\((\d+)\s*min\))?\s*$")


def _parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    body = text[end + 5 :]
    fm: dict[str, object] = {}
    current_list_key: str | None = None
    for line in raw.splitlines():
        if not line.strip():
            current_list_key = None
            continue
        if line.startswith("  - ") and current_list_key:
            value = line[4:].strip().strip('"').strip("'")
            fm.setdefault(current_list_key, []).append(value)  # type: ignore[union-attr]
            continue
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            if not val:
                fm[key] = []
                current_list_key = key
            else:
                fm[key] = val.strip('"').strip("'")
                current_list_key = None
    return fm, body


def parse_agenda(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text()
    return _parse_frontmatter(text)


def parse_qanda(path: Path) -> tuple[dict[str, object], list[MeetingSection]]:
    text = path.read_text()
    fm, body = _parse_frontmatter(text)

    sections: list[MeetingSection] = []
    current: MeetingSection | None = None
    item: MeetingItem | None = None
    list_buffer: list[str] | None = None

    for raw_line in body.splitlines():
        line = raw_line.rstrip()
        section_match = _SECTION_RE.match(line)
        if section_match:
            if current is not None:
                if item is not None:
                    current.items.append(item)
                    item = None
                sections.append(current)
            name = section_match.group(1).strip()
            mins = section_match.group(2)
            current = MeetingSection(
                name=name,
                duration_min=int(mins) if mins else None,
            )
            list_buffer = None
            continue
        if line.startswith("### "):
            if item is not None and current is not None:
                current.items.append(item)
            item = MeetingItem(title=line[4:].strip())
            list_buffer = None
            continue
        if line.startswith("**Talking points:**"):
            list_buffer = item.talking_points if item else None
            continue
        if line.startswith("**Questions:**"):
            list_buffer = item.questions if item else None
            continue
        if line.startswith("**Notes:**") or line.startswith("---") or line.startswith("# "):
            list_buffer = None
            continue
        if line.startswith("- ") and list_buffer is not None:
            list_buffer.append(line[2:].strip())

    if item is not None and current is not None:
        current.items.append(item)
    if current is not None:
        sections.append(current)

    return fm, sections


def build_meeting(qanda_path: Path) -> Meeting:
    qanda_fm, sections = parse_qanda(qanda_path)
    agenda_ref = str(qanda_fm.get("agenda", "./agenda.md"))
    agenda_path = (qanda_path.parent / agenda_ref).resolve()
    agenda_fm, _ = parse_agenda(agenda_path)

    return Meeting(
        title=str(qanda_fm.get("title", agenda_fm.get("title", "Meeting"))),
        date=str(qanda_fm.get("date", agenda_fm.get("date", ""))),
        duration_minutes=int(str(agenda_fm.get("duration_minutes", 60))),
        type=str(agenda_fm.get("type", "Discussion")),
        attendees=list(agenda_fm.get("attendees", []) or []),  # type: ignore[arg-type]
        summary=_extract_summary(agenda_path),
        sections=sections,
    )


def _extract_summary(agenda_path: Path) -> str:
    if not agenda_path.exists():
        return ""
    text = agenda_path.read_text()
    _, body = _parse_frontmatter(text)
    in_summary = False
    out: list[str] = []
    for line in body.splitlines():
        if line.startswith("## Summary"):
            in_summary = True
            continue
        if in_summary and line.startswith("## "):
            break
        if in_summary and line.strip():
            out.append(line.strip())
    return " ".join(out)


# --- Asset handling --------------------------------------------------------


def _fetch(url: str, dest: Path) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = resp.read()
        dest.write_bytes(data)
        return True
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def resolve_assets(refresh: bool) -> tuple[Path, Path]:
    """Return (logo_png, icon_png).

    PNGs are vendored at publishing/assets/{logo,icon}.png and used by the renderer.
    With --refresh-assets, the SVGs are re-fetched from hps.gd for archival; the
    PNGs are not auto-regenerated (drop new PNGs into the assets directory by
    hand when the brand changes — rare).
    """
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    if refresh:
        _fetch(LOGO_URL, ASSET_DIR / "logo.svg")
        _fetch(ICON_URL, ASSET_DIR / "icon.svg")
    return ASSET_DIR / "logo.png", ASSET_DIR / "icon.png"


def _draw_image(c: Canvas, img_path: Path, x: float, y: float, w: float, h: float) -> None:
    if not img_path.exists():
        return
    img = ImageReader(str(img_path))
    iw, ih = img.getSize()
    sx = w / iw
    sy = h / ih
    s = min(sx, sy)
    draw_w = iw * s
    draw_h = ih * s
    # Centre within the requested box
    cx = x + (w - draw_w) / 2
    cy = y + (h - draw_h) / 2
    c.drawImage(img, cx, cy, draw_w, draw_h, mask="auto")


# --- Rendering -------------------------------------------------------------


def _content_box() -> tuple[float, float, float, float]:
    """Return (x, y, w, h) of the usable content area excluding toolbar/header/footer."""
    x = TOOLBAR_PT
    y = FOOTER_H
    w = PAGE_W - TOOLBAR_PT
    h = PAGE_H - HEADER_H - FOOTER_H
    return x, y, w, h


def _draw_header(c: Canvas, section_title: str) -> None:
    """Top band on every non-cover page: section title right-aligned, no rule."""
    band_y = PAGE_H - HEADER_H
    c.setFillColor(HEADING_COLOR)
    c.setFont(FONT_DISPLAY, 10)
    c.drawRightString(PAGE_W - 8, band_y + 9, section_title)


def _draw_footer(c: Canvas, page_num: int, total_pages: int, icon_path: Path) -> None:
    """Bottom band on every non-cover page: brand icon left, page indicator right, no rule."""
    band_y = 0
    _draw_image(c, icon_path, TOOLBAR_PT + 4, band_y + 3, 14, 14)
    c.setFillColor(MUTED_COLOR)
    c.setFont(FONT_BODY, 7)
    c.drawRightString(PAGE_W - 8, band_y + 6, f"{page_num} / {total_pages}")


def _wrap_lines(text: str, max_chars: int) -> list[str]:
    """Crude word wrap. Good enough for the bullets we're rendering."""
    words = text.split()
    lines: list[str] = []
    current = ""
    for w in words:
        if not current:
            current = w
        elif len(current) + 1 + len(w) <= max_chars:
            current += " " + w
        else:
            lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def render_cover(c: Canvas, m: Meeting, logo_path: Path, icon_path: Path) -> None:
    """First page: branding (icon + logo side by side), title, fillable form table
    (date/time/attendees/apologies — all blank to be written in on the day), and a
    Topics list showing the allocation per section from the agenda."""
    x, y, w, h = _content_box()
    centre_x = TOOLBAR_PT + w / 2

    # Branding: icon + small gap + logo, side by side, centred. Compact size to
    # leave room for a generous gap between the wordmark and the meeting title.
    icon_w, icon_h = 32, 32
    logo_w, logo_h = 64, 32
    gap = 8
    total_w = icon_w + gap + logo_w
    brand_x = TOOLBAR_PT + (w - total_w) / 2
    brand_y = PAGE_H - 60
    _draw_image(c, icon_path, brand_x, brand_y, icon_w, icon_h)
    _draw_image(c, logo_path, brand_x + icon_w + gap, brand_y, logo_w, logo_h)

    # Meeting title — generous padding below the branding.
    title_y = brand_y - 50
    c.setFillColor(HEADING_COLOR)
    c.setFont(FONT_DISPLAY, 18)
    c.drawCentredString(centre_x, title_y, m.title)

    # Fillable table: Date | _ , Time | _ , Attendees x 6 rows, Apologies x 4 rows.
    # All blank — the meeting facilitator writes these in on the day.
    label_x = TOOLBAR_PT + 24
    value_x = TOOLBAR_PT + 110
    value_end_x = PAGE_W - 30
    row_h = 18
    table_y = title_y - 36

    rows = [
        ("Date", 1),
        ("Time", 1),
        ("Attendees", 6),
        ("Apologies", 4),
    ]

    label_size = 9
    body_size = 8
    note_size = 7
    current_y = table_y
    c.setStrokeColor(RULE_COLOR)
    c.setLineWidth(0.4)
    for idx, (label, count) in enumerate(rows):
        for i in range(count):
            if i == 0:
                c.setFillColor(HEADING_COLOR)
                c.setFont(FONT_DISPLAY, label_size)
                c.drawString(label_x, current_y - 12, label)
            # Writable rule
            c.line(value_x, current_y - 14, value_end_x, current_y - 14)
            current_y -= row_h
        # Blank gap between sections (one row's worth of whitespace)
        if idx < len(rows) - 1:
            current_y -= row_h

    # Blank gap between Apologies and Topics
    current_y -= row_h
    # Topics list (renamed from "Topic allocations"). Sourced from the agenda's
    # per-topic minutes — printed because they're already known.
    topics_y = current_y - 6
    c.setFillColor(HEADING_COLOR)
    c.setFont(FONT_DISPLAY, label_size)
    c.drawString(label_x, topics_y, "Topics")
    row_y = topics_y - 16
    total_alloc = 0
    for i, section in enumerate(m.sections):
        accent = SECTION_COLORS[i % len(SECTION_COLORS)]
        c.setFillColor(accent)
        c.rect(label_x, row_y - 3, 5, 8, stroke=0, fill=1)
        c.setFillColor(TEXT_COLOR)
        c.setFont(FONT_BODY, body_size)
        c.drawString(label_x + 12, row_y, section.name)
        if section.duration_min is not None:
            c.drawRightString(value_end_x, row_y, f"{section.duration_min} min")
            total_alloc += section.duration_min
        row_y -= 12
    if total_alloc:
        c.setStrokeColor(RULE_COLOR)
        c.setLineWidth(0.4)
        c.line(label_x + 12, row_y + 4, value_end_x, row_y + 4)
        c.setFillColor(MUTED_COLOR)
        c.setFont(FONT_BODY, note_size)
        c.drawString(label_x + 12, row_y - 8, "Total allocated")
        c.drawRightString(value_end_x, row_y - 8, f"{total_alloc} min")
        row_y -= 18
        if total_alloc < m.duration_minutes:
            buffer = m.duration_minutes - total_alloc
            c.drawString(label_x + 12, row_y, "Buffer")
            c.drawRightString(value_end_x, row_y, f"{buffer} min")


def _render_item_slot(
    c: Canvas,
    item: MeetingItem,
    x: float,
    y: float,
    w: float,
    h: float,
    accent: colors.Color,
) -> None:
    """One item: heading + talking points + questions, then NOTES filling the
    remaining vertical space with ruled lines, then a fixed-size ACTIONS block
    (header + 5 ruled rows × 3 columns) anchored to the bottom of the slot."""
    # Left margin rule in section accent
    c.setStrokeColor(accent)
    c.setLineWidth(2.5)
    c.line(x, y + 4, x, y + h - 4)

    text_x = x + 8
    right_x = x + w - 4

    # Item heading
    text_y = y + h - 12
    c.setFillColor(accent)
    c.setFont(FONT_DISPLAY, 11)
    c.drawString(text_x, text_y, item.title[:100])

    # Talking points
    text_y -= 16
    if item.talking_points:
        c.setFillColor(MUTED_COLOR)
        c.setFont(FONT_BODY_BOLD, 7.5)
        c.drawString(text_x, text_y, "Talking points")
        text_y -= 10
        c.setFillColor(TEXT_COLOR)
        c.setFont(FONT_BODY, 8)
        for tp in item.talking_points:
            for line in _wrap_lines("·  " + tp, 95):
                c.drawString(text_x, text_y, line)
                text_y -= 10

    # Questions
    if item.questions:
        text_y -= 4
        c.setFillColor(MUTED_COLOR)
        c.setFont(FONT_BODY_BOLD, 7.5)
        c.drawString(text_x, text_y, "Questions")
        text_y -= 10
        c.setFillColor(TEXT_COLOR)
        c.setFont(FONT_BODY, 8)
        for q in item.questions:
            for line in _wrap_lines("?  " + q, 95):
                c.drawString(text_x, text_y, line)
                text_y -= 10

    # Notes and Actions share the same line spacing so the page reads as one
    # continuous ruled grid. Actions block height is fixed at: label (10) +
    # ACTIONS_ROWS × line_step.
    line_step = 12
    actions_block_h = 10 + ACTIONS_ROWS * line_step
    actions_top = y + actions_block_h
    actions_bottom = y + 4

    # Notes band: from below printed content down to actions.
    notes_top = text_y - 4
    notes_bottom = actions_top + 6
    if notes_top - notes_bottom < 24:
        notes_top = notes_bottom + 24

    label_font_size = 6
    label_color = RULE_COLOR  # lighter grey than MUTED

    # NOTES label and ruled lines filling the band
    c.setFillColor(label_color)
    c.setFont(FONT_BODY_BOLD, label_font_size)
    c.drawString(text_x, notes_top - 7, "NOTES")
    c.setStrokeColor(RULE_COLOR)
    c.setLineWidth(0.3)
    line_y = notes_top - 14
    while line_y > notes_bottom:
        c.line(text_x, line_y, right_x, line_y)
        line_y -= line_step

    # ACTIONS label
    c.setFillColor(label_color)
    c.setFont(FONT_BODY_BOLD, label_font_size)
    c.drawString(text_x, actions_top - 8, "ACTIONS")

    # Action rows: full-width ruled lines with a checkbox at the start of each,
    # plus column dividers (no header labels — Who/What/When are assumed).
    rows_top = actions_top - 10
    rows_bottom = actions_bottom
    available = rows_top - rows_bottom
    row_step = available / ACTIONS_ROWS
    col_count = 3
    col_w = (right_x - text_x) / col_count

    c.setStrokeColor(RULE_COLOR)
    c.setLineWidth(0.3)

    # Column dividers
    c.line(text_x + col_w, rows_top, text_x + col_w, rows_bottom)
    c.line(text_x + 2 * col_w, rows_top, text_x + 2 * col_w, rows_bottom)

    # Per-row line + checkbox
    checkbox_size = 6
    for i in range(ACTIONS_ROWS):
        baseline_y = rows_top - (i + 1) * row_step
        c.line(text_x, baseline_y, right_x, baseline_y)
        # Checkbox sits just above the baseline, in the leftmost column
        cx = text_x + 2
        cy = baseline_y + 2
        c.rect(cx, cy, checkbox_size, checkbox_size, stroke=1, fill=0)


def _render_section(
    c: Canvas,
    section: MeetingSection,
    accent: colors.Color,
    icon_path: Path,
    page_counter: list[int],
    total_pages: int,
) -> None:
    x, y, w, h = _content_box()
    # Whitespace: ~24 pt below the header (above the first item) and a matching
    # gap between items. Items share the remaining vertical space equally.
    top_gap = 24.0
    inter_gap = 24.0
    usable_h = h - top_gap - inter_gap * (ITEMS_PER_PAGE - 1)
    item_h = usable_h / ITEMS_PER_PAGE
    section_label = section.name
    if section.duration_min is not None:
        section_label = f"{section.name} ({section.duration_min} min)"

    items = section.items
    # Pages for this section
    for page_idx in range(0, max(1, len(items)), ITEMS_PER_PAGE):
        page_items = items[page_idx : page_idx + ITEMS_PER_PAGE]
        _draw_header(c, section_label)
        # First item starts top_gap below the header band
        slot_top = y + h - top_gap
        for it in page_items:
            slot_y = slot_top - item_h
            _render_item_slot(c, it, x + 6, slot_y, w - 8, item_h, accent)
            slot_top = slot_y - inter_gap
        page_counter[0] += 1
        _draw_footer(c, page_counter[0], total_pages, icon_path)
        c.showPage()


def _count_total_pages(m: Meeting) -> int:
    total = 1  # cover
    for s in m.sections:
        items = max(1, len(s.items))
        total += -(-items // ITEMS_PER_PAGE)  # ceil division
    return total


def render_pdf(meeting: Meeting, out_path: Path, logo: Path, icon: Path) -> None:
    c = Canvas(str(out_path), pagesize=(PAGE_W, PAGE_H))
    c.setTitle(meeting.title)
    c.setAuthor("hps.gd")

    render_cover(c, meeting, logo, icon)
    page_counter = [1]
    total_pages = _count_total_pages(meeting)
    # No footer on the cover page — keep it clean.
    c.showPage()

    for i, section in enumerate(meeting.sections):
        accent = SECTION_COLORS[i % len(SECTION_COLORS)]
        _render_section(c, section, accent, icon, page_counter, total_pages)

    c.save()


# --- CLI -------------------------------------------------------------------


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--qanda", required=True, type=Path, help="Path to qanda.md")
    p.add_argument("--out", type=Path, help="Output PDF path (default: <meeting-folder>/meeting.pdf)")
    p.add_argument("--refresh-assets", action="store_true",
                   help="Fetch fresh brand assets from hps.gd before rendering")
    args = p.parse_args()

    _verify_assets_available()

    qanda = args.qanda.resolve()
    if not qanda.exists():
        print(f"qanda not found: {qanda}", file=sys.stderr)
        return 1

    out = (args.out or qanda.parent / "meeting.pdf").resolve()
    _register_brand_fonts(ASSET_DIR)
    logo, icon = resolve_assets(refresh=args.refresh_assets)
    meeting = build_meeting(qanda)
    render_pdf(meeting, out, logo, icon)
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
