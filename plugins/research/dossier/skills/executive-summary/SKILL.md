---
name: executive-summary
description: "Generate the executive summary section for a dossier. Interactive: the user picks which input reports feed in, names the audience and posture, signs off on an outline, then reviews the draft before it's written into DOSSIER.md. Call standalone to regenerate without re-running the whole dossier, or from `/dossier:consolidate` after the markdown has been assembled."
argument-hint: "[engagement_dir]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

# Executive summary

Draft and inject the executive summary section of a dossier. The skill is interactive end-to-end: nothing is written to `DOSSIER.md` until the user signs off on the final draft.

This skill is a sibling of `/dossier:consolidate`. Consolidate builds the document skeleton with a `<!-- TODO -->` placeholder where the summary belongs; this skill fills that placeholder. Run it standalone any time you want to regenerate without re-running consolidate.

## Step 1: Resolve engagement directory

The first argument is the engagement directory. If omitted, default to `pwd`. Resolve to an absolute path.

```bash
ARG="${1:-$(pwd)}"
case "$ARG" in
  /*) ENG="$ARG" ;;
  *) ENG="$(pwd)/$ARG" ;;
esac
```

`$ENG/DOSSIER.md` must exist. If it doesn't, stop and tell the user to run `/dossier:consolidate` first — this skill fills a placeholder, it doesn't create the dossier.

## Step 2: List candidate input reports

Re-scan `$ENG/**/*.md` and identify conforming reports the same way consolidate does: YAML frontmatter with `title`, `date`, `author`, and either `category` or `appendix: true`. Skip `DOSSIER.md` itself. Group by `category` (treating `appendix: true` files as the `Appendices` group). Within a group, sort by `subject` then `date` then filename.

The skill operates on the same eligibility contract as consolidate. If a file isn't conforming, it can't feed the summary — the user fixes the frontmatter and re-runs.

## Step 3: Pick which inputs feed the summary

Show the candidate list grouped by category and ask via `AskUserQuestion` which inputs to use:

- **All eligible** — every conforming report (the usual choice)
- **Exclude a category** — drop everything in one category (follow-up question)
- **Exclude individual files** — drop specific files (follow-up for paths)
- **Pick a subset** — opposite of exclude. Useful when only one or two reports matter for the summary (follow-up for paths)

In non-interactive runs, default to all eligible.

## Step 4: Audience and posture

Ask `AskUserQuestion` with these options:

**Audience** — who reads this first:

- Board / investors
- Client executive (CEO / CFO of the engaging party)
- Internal ops (delivery team, ground-floor staff)
- External / public (if the summary will be shared widely or published)

**Posture** — what the summary leads with:

- Neutral — present what was found, no recommendation
- Recommendation-led — open with the recommended action
- Risk-led — open with the highest-priority risk or concern
- Opportunity-led — open with the highest-value opportunity

**Length** — soft target:

- Short (~150 words, a single paragraph)
- Medium (~300 words, 2-3 paragraphs)
- Long (~500 words, 3-5 paragraphs)

## Step 5: Read the inputs and propose an outline

Read the selected reports (strip frontmatter). Identify the cross-cutting threads — not a list of every report, but the 3-5 things a reader at the chosen audience needs to know. Use the report `confidence` field where present to weight findings: low-confidence items belong in caveats, not headlines.

Propose the outline as a short bullet list in chat. Each bullet is a one-line section heading, not the prose itself:

```
Proposed outline (Medium, Recommendation-led, Client executive):

  1. Recommendation up-front — proceed with the partnership, with conditions on the IP licensing question
  2. Who VisualCare are — Sydney-based aged-care software, 80 staff, founder-led
  3. Headline findings — strong technical posture, three commercial relationships at risk
  4. Outstanding risks — IP licensing on the legacy product, key-person dependency on the founder
  5. What we still don't know — financial detail beyond public filings, full customer list

Accept this outline / revise / change audience or posture?
```

Use `AskUserQuestion` to gather the response. If revise, get the changes and propose again. If audience or posture change, jump back to Step 4 with the new selection.

## Step 6: Draft

Write the prose summary following the agreed outline, target audience, and posture. Honour the length target — short is one paragraph, medium is two or three, long is three to five.

Constraints:

- No `h1` or `h2` inside the summary body. The `## Executive summary` heading is already there; sub-sections (if any) use `h3+`
- Reference reports by what they cover, not their filenames ("the corporate-ownership report" reads worse than "the ownership analysis")
- Don't recap every report. Synthesise. A reader who only reads the summary should know the headline answer
- Honour confidence: hedge low-confidence findings explicitly ("appears to", "single-source") rather than presenting them as facts
- Follow the writing-style rules. The banned-vocabulary list and AI-tell rules apply — this is a piece of business writing, not a generated artifact

## Step 7: Review and approve

Show the draft to the user in chat — verbatim, not summarised. Then ask via `AskUserQuestion`:

- **Accept** — write to `DOSSIER.md`
- **Revise** — user specifies what to change; re-draft and re-show
- **Restart** — go back to outline (Step 5) or audience/posture (Step 4)
- **Abort** — exit without modifying `DOSSIER.md`

Iterate until accept or abort. Don't shortcut this loop — the user explicitly asked for a confirm step before the summary lands.

## Step 8: Inject into DOSSIER.md

Find the executive summary section in `DOSSIER.md`. The block is everything between the `## Executive summary` heading (which may carry a `{#exec-summary}` anchor) and the next h1 or h2.

Replace that block's body with the approved draft. Keep the heading line and the blank line that follows. Don't rewrite anything outside the section.

If the existing body contains anything other than the `<!-- TODO -->` placeholder — i.e. someone has already written or edited a summary — pause and ask before overwriting:

- **Replace** — overwrite the existing content
- **Append** — keep the existing content above the new draft
- **Abort** — leave the file untouched

## Step 9: Output

Report what changed:

```
Executive summary written.

  Markdown: <engagement_dir>/DOSSIER.md
  Audience: Client executive
  Posture:  Recommendation-led
  Length:   Medium (312 words)

The PDF is not re-rendered automatically. Run /publishing:write-document-pdf
(or re-run /dossier:consolidate) to refresh DOSSIER.pdf.
```

Don't auto-render the PDF — the user may want to make other edits first, and re-rendering belongs to the publishing step. State the next command explicitly so the user knows what's needed.

## Rules

- **Never modify source reports.** Read-only on everything except `DOSSIER.md`.
- **Stop at sign-off, every time.** The draft is shown to the user before it touches `DOSSIER.md`. No exceptions, even in agent-driven flows
- **Don't rewrite outside the executive summary section.** Boundary is the `## Executive summary` heading and the next `h1`/`h2`
- **Don't re-render the PDF.** Surface the command, let the user run it
- **Synthesise, don't enumerate.** A list of "Report X says Y, Report Z says W" isn't an executive summary

## Output format

Three to four lines as in Step 9.

## Related

- `/dossier:consolidate` — builds the `DOSSIER.md` skeleton this skill fills. If the placeholder is missing because someone manually edited the file, fix the markdown first or run consolidate again
- `/publishing:write-document-pdf` — re-render the PDF after the summary is written
- `report-conventions.md` rule — the frontmatter contract input reports must conform to
