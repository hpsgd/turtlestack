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

✅ **PDF rendered successfully**

**Output:** `/private/var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/eval-1779714669-dc3c7ed2/work/docs/assessment.pdf`

**Verification:**
- File: PDF document, version 1.4, **2 pages** (cover + body)
- Brand fonts embedded: MonaSans-Regular, Inter-Bold, Inter-Regular (hps.gd report style)
- Mechanism: `render-document-pdf.sh` wrapper (Docker cached image reused)

The cover page was generated from the YAML frontmatter (title: "External Product Assessment", subtitle: "VisualCare", with metadata). The executive summary appears on page 2. Ready for sharing with stakeholders or archiving alongside the markdown source.

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
| Verdict | PASS |
| Score | 10.5/11.0 (95%) |
| Evaluated | 2026-05-25 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 37128 ms |
| Target cost | $0.0700 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill writes the PDF to the path specified by `--out`. Confirms the absolute path in chat output. | PASS | Chat output states: 'Output: /private/var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/eval-1779714669-dc3c7ed2/work/docs/assessment.pdf' |
| c2 | The PDF file exists with non-zero size — typically 30KB or larger because brand fonts (Mona Sans + Inter) are embedded. | PASS | Artifact `work/docs/assessment.pdf` listed as binary 46KB, which exceeds the 30KB threshold. |
| c3 | The PDF has at least 2 pages (cover + body). Cover page shows the title "External Product Assessment", subtitle "VisualCare", and a metadata table with Date / Author / Status rows. | PASS | Chat: '2 pages (cover + body)'; 'cover page was generated from the YAML frontmatter (title: External Product Assessment, subtitle: VisualCare, with metadata)' |
| c4 | Skill does NOT modify the input markdown — only writes the new PDF. | PASS | Artifact `work/docs/assessment.md` content matches the input exactly — no alterations to frontmatter or body. |
| c5 | Skill output identifies the renderer's wrapper script (`render-document-pdf.sh`) or the Python entry. On first run, the wrapper builds a Docker image (`turtlestack/publishing-document-pdf:<hash>`) from the bundled Dockerfile and reuses it thereafter; the host only needs Docker. | PASS | Chat: 'Mechanism: render-document-pdf.sh wrapper (Docker cached image reused)' |
| c6 | Output mentions that the PDF can be shared with stakeholders, archived, or sideloaded. | PARTIAL | Chat: 'Ready for sharing with stakeholders or archiving alongside the markdown source.' — both sharing and archiving mentioned. |
| c7 | `assessment.pdf` exists at the path reported in chat. The chat output gives an absolute path that resolves to a real file. | PASS | Artifact `work/docs/assessment.pdf` exists and the absolute path in chat matches the artifact location. |
| c8 | `assessment.pdf` is a valid PDF (begins with the bytes `%PDF-`). | PASS | Verification line states 'PDF document, version 1.4' — indicating a valid PDF header was read from the file. |
| c9 | `assessment.pdf` is between 30KB and 5MB. Smaller suggests the brand fonts didn't embed (silent fallback to Helvetica); much larger suggests something other than a document PDF was written. | PASS | Artifact listed as 46KB, within the 30KB–5MB range. |
| c10 | The PDF embeds Mona Sans and Inter fonts. A `pdffonts` check or grep on `/BaseFont` should show `MonaSans-Regular` and `Inter-Regular` (and possibly `Inter-Bold`) in the embedded font list. | PASS | Chat: 'Brand fonts embedded: MonaSans-Regular, Inter-Bold, Inter-Regular (hps.gd report style)' |
| c11 | The cover page is on page 1 and the body content (`# Executive summary`) starts on page 2 — the YAML frontmatter triggers the cover, and the body follows after the page break. | PASS | Chat: '2 pages (cover + body)'; 'The executive summary appears on page 2' — confirms cover on p1, body on p2. |
| c12 | The skill catches and surfaces any wrapper-script error (e.g. Docker missing — exit 69, image build failed) rather than reporting success and producing an empty file. | FAIL | No mention of error handling, exit codes, or what happens if Docker is missing/build fails. Only success path is described. |

### Notes

The skill performed well across all success-path criteria, correctly producing a 46KB branded PDF with cover page, embedded fonts, and absolute path confirmation. The only gap is c12: no error-handling behavior is surfaced in the output, leaving the Docker-missing/build-failed failure path unverified.
