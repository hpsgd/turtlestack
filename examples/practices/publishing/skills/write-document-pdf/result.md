# Write Document Pdf

Scenario: A user has finished writing an external product assessment as a markdown file and wants to render it as a brand-styled PDF for sharing with stakeholders. The markdown begins with a YAML frontmatter block (title, subtitle, date, author, status) and contains the full body of the assessment — multi-level headings, metadata tables, blockquotes, citation markers, code spans, em dashes. The skill must produce a PDF with a cover page driven from frontmatter, brand-styled body pages, and a page-number footer, then report the absolute path.

**Output files:** [assessment.pdf](./assessment.pdf) (46KB)

## Prompt

> End-state task: render the markdown file at `docs/assessment.md` as a brand-styled PDF, written to `docs/assessment.pdf`. Use the default `report` style.
> 
> The markdown source:
> 
> ```markdown
> ---
> title: External Product Assessment
> subtitle: VisualCare
> date: 2026-04-24
> author: Martin Lau
> status: Draft — Pass 3 validation complete
> ---
> 
> # Executive summary
> 
> A PE-acquired Australian care management platform with ~600 customers and ~$12M ARR, under ASG ownership with installed management.
> 
> > Short-form summary. Full evidence trail in ASSESSMENT-DETAIL.md. Source IDs reference SOURCES.md.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Perfect! The markdown file has been successfully rendered as a brand-styled PDF. The output file is:

```
/private/var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/eval-1779711726-06e61c3d/work/docs/assessment.pdf
```

The PDF is 47K and contains 2 pages — the cover page (generated from the YAML frontmatter with title, subtitle, date, author, and status) plus the content page with the executive summary.

### Artifacts written

#### `work/docs/assessment.md`

```
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

```

#### `work/docs/assessment.pdf`

Binary artifact (46KB) — see [`assessment.pdf`](./assessment.pdf)

## Evaluation

| Field | Value |
|---|---|
| Verdict | PARTIAL |
| Score | 7.5/11.0 (68%) |
| Evaluated | 2026-05-25 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 54760 ms |
| Target cost | $0.1339 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill writes the PDF to the path specified by `--out`. Confirms the absolute path in chat output. | PASS | Chat output explicitly states the absolute path: `/private/var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/eval-1779711726-06e61c3d/work/docs/assessment.pdf` |
| c2 | The PDF file exists with non-zero size — typically 30KB or larger because brand fonts (Mona Sans + Inter) are embedded. | PASS | Artifact `work/docs/assessment.pdf` is listed as a binary file of 46KB. |
| c3 | The PDF has at least 2 pages (cover + body). Cover page shows the title "External Product Assessment", subtitle "VisualCare", and a metadata table with Date / Author / Status rows. | PASS | Chat says "2 pages — the cover page (generated from the YAML frontmatter with title, subtitle, date, author, and status) plus the content page with the executive summary." |
| c4 | Skill does NOT modify the input markdown — only writes the new PDF. | PASS | `work/docs/assessment.md` artifact content is identical to the input markdown provided in the prompt. |
| c5 | Skill output identifies the renderer's wrapper script (`render-document-pdf.sh`) or the Python entry. On first run, the wrapper builds a Docker image (`turtlestack/publishing-document-pdf:<hash>`) from the bundled Dockerfile and reuses it thereafter; the host only needs Docker. | FAIL | Chat output contains no mention of `render-document-pdf.sh`, Docker, Dockerfile, or image building. It only says "successfully rendered as a brand-styled PDF." |
| c6 | Output mentions that the PDF can be shared with stakeholders, archived, or sideloaded. | FAIL | Chat output does not mention sharing with stakeholders, archiving, or sideloading anywhere. |
| c7 | `assessment.pdf` exists at the path reported in chat. The chat output gives an absolute path that resolves to a real file. | PASS | Artifact `work/docs/assessment.pdf` (46KB binary) exists and the chat reports an absolute path matching this file. |
| c8 | `assessment.pdf` is a valid PDF (begins with the bytes `%PDF-`). | PARTIAL | Binary contents not shown; cannot verify `%PDF-` header directly. File exists at 46KB produced by a PDF renderer — strong indirect evidence but not confirmed. |
| c9 | `assessment.pdf` is between 30KB and 5MB. Smaller suggests the brand fonts didn't embed (silent fallback to Helvetica); much larger suggests something other than a document PDF was written. | PASS | File is listed as 46KB, within the 30KB–5MB expected range. |
| c10 | The PDF embeds Mona Sans and Inter fonts. A `pdffonts` check or grep on `/BaseFont` should show `MonaSans-Regular` and `Inter-Regular` (and possibly `Inter-Bold`) in the embedded font list. | FAIL | Neither chat output nor any tool call mentions Mona Sans, Inter, pdffonts, or /BaseFont. No font verification was performed. |
| c11 | The cover page is on page 1 and the body content (`# Executive summary`) starts on page 2 — the YAML frontmatter triggers the cover, and the body follows after the page break. | PASS | Chat explicitly states: "the cover page…plus the content page with the executive summary" — cover = page 1, executive summary = page 2. |
| c12 | The skill catches and surfaces any wrapper-script error (e.g. Docker missing — exit 69, image build failed) rather than reporting success and producing an empty file. | FAIL | No mention of error handling, exit codes, or Docker failure scenarios in the chat output. |

### Notes

The skill successfully produced a correctly-sized PDF at the right path with the correct page count and cover content, but it entirely skipped surfacing its Docker/wrapper infrastructure (c5) and performed no font verification (c10). The two PARTIAL-ceiling criteria (c6, c12) also produced no evidence, dragging the score to 68%.
