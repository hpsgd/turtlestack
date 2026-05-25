# Test: write-document-pdf

Scenario: A user has finished writing an external product assessment as a markdown file and wants to render it as a brand-styled PDF for sharing with stakeholders. The markdown begins with a YAML frontmatter block (title, subtitle, date, author, status) and contains the full body of the assessment — multi-level headings, metadata tables, blockquotes, citation markers, code spans, em dashes. The skill must produce a PDF with a cover page driven from frontmatter, brand-styled body pages, and a page-number footer, then report the absolute path.

## Prompt

End-state task: render the markdown file at `docs/assessment.md` as a brand-styled PDF, written to `docs/assessment.pdf`. Use the default `report` style.

The markdown source:

```markdown
---
title: External Product Assessment
subtitle: VisualCare
date: 2026-04-24
author: Martin Lau
status: Draft — Pass 3 validation complete
---

# Executive summary

A PE-acquired Australian care management platform with ~600 customers and ~$12M ARR, under ASG ownership with installed management.

> Short-form summary. Full evidence trail in ASSESSMENT-DETAIL.md. Source IDs reference SOURCES.md.

## Market position

| Field | Value |
|---|---|
| Customers | ~600 providers |
| Participants | ~158,000 |
| ARR | ~$12M |

The team is 37 people across 8 functions, with ~6-8 in engineering. Feature releases dropped to zero in Q1 2026 — engineering capacity consumed by incident response.

Mobile is a weak point. vWorker iOS rates 2.5/5 across 101 ratings [T4]. Code references like `ASSESSMENT-DETAIL.md` should render in monospace.
```

Write that markdown to `docs/assessment.md`, then run:

```
/publishing:write-document-pdf docs/assessment.md --out docs/assessment.pdf
```

Confirm the absolute path of the PDF in your final message.

## Criteria

- [ ] PASS: Skill writes the PDF to the path specified by `--out`. Confirms the absolute path in chat output.
- [ ] PASS: The PDF file exists with non-zero size — typically 30KB or larger because brand fonts (Mona Sans + Inter) are embedded.
- [ ] PASS: The PDF has at least 2 pages (cover + body). Cover page shows the title "External Product Assessment", subtitle "VisualCare", and a metadata table with Date / Author / Status rows.
- [ ] PASS: Skill does NOT modify the input markdown — only writes the new PDF.
- [ ] PASS: Skill output identifies the renderer's wrapper script (`render-document-pdf.sh`) or the Python entry. On first run, the wrapper builds a Docker image (`turtlestack/publishing-document-pdf:<hash>`) from the bundled Dockerfile and reuses it thereafter; the host only needs Docker.
- [ ] PARTIAL: Output mentions that the PDF can be shared with stakeholders, archived, or sideloaded.

## Output expectations

- [ ] PASS: `assessment.pdf` exists at the path reported in chat. The chat output gives an absolute path that resolves to a real file.
- [ ] PASS: `assessment.pdf` is a valid PDF (begins with the bytes `%PDF-`).
- [ ] PASS: `assessment.pdf` is between 30KB and 5MB. Smaller suggests the brand fonts didn't embed (silent fallback to Helvetica); much larger suggests something other than a document PDF was written.
- [ ] PASS: The PDF embeds Mona Sans and Inter fonts. A `pdffonts` check or grep on `/BaseFont` should show `MonaSans-Regular` and `Inter-Regular` (and possibly `Inter-Bold`) in the embedded font list.
- [ ] PASS: The cover page is on page 1 and the body content (`# Executive summary`) starts on page 2 — the YAML frontmatter triggers the cover, and the body follows after the page break.
- [ ] PARTIAL: The skill catches and surfaces any wrapper-script error (e.g. Docker missing — exit 69, image build failed) rather than reporting success and producing an empty file.
