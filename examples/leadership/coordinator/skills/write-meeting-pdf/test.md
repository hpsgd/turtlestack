# Test: write-meeting-pdf

Scenario: A user has had a session-long discussion preparing for a board meeting and runs all three meeting skills in sequence — the agenda skill captures the agenda, the qanda skill produces the supporting Q-and-A document, and the PDF skill renders both into a printable document for note-taking on a Remarkable Paper Pro. The PDF must exist alongside the agenda and qanda, contain the expected number of pages (cover + content), be a valid PDF file, and the skill must report the absolute path.

## Prompt

End-state task: produce three files in `docs/meetings/2026-05-15-q2-board-meeting/` — `agenda.md`, `qanda.md`, and `meeting.pdf`. **All three files must exist when you finish — do not stop after the agenda or after the qanda.**

Run three skills in sequence. The first writes the agenda, the second expands it into the Q-and-A, the third renders both into the PDF. Carry the absolute path of the agenda from skill 1 to skill 2, and the path of the qanda from skill 2 to skill 3.

Discussion context for the agenda:

I've just had a long discussion with you about the upcoming quarterly board meeting for Acme Robotics. Here's a recap:

- **Meeting metadata:** Quarterly board meeting on 2026-05-15. 90 minutes scheduled. Attendees: CEO (Sam Patel), CFO (Rita Cho), Chair (Jordan Liu), two non-exec directors (Casey Morgan, Devi Iyer). Meeting type: board.
- Q1 financial results came in 8% ahead of plan on revenue but EBITDA margin compressed by 2.5 points due to one-off rebrand costs and accelerated R&D hiring. The CFO will walk through the bridge.
- Cash runway extended from 14 to 19 months because of the SAFE round closing in March. Need board acknowledgement of the new runway and the decision to defer the Series B by two quarters.
- Hiring: 12 of 15 planned engineering hires landed, 0 of 3 GTM hires landed because the head of GTM hasn't started yet. Need a board view on whether to delay the GTM hires until the head of GTM is onboarded or backfill via contractors.
- Product roadmap shift: customer feedback from the design partner programme has surfaced that the workflow automation feature ranks higher than the analytics dashboard we had prioritised. The CPO wants approval to swap them in the H2 roadmap.
- A strategic decision to discuss: whether to expand into the EU market in H2 (faster, but stretches the team) or wait until H1 next year (slower, but lets us hire a country lead first). Risk appetite question — board input needed.
- Standard governance: minutes from last meeting, conflicts of interest, AOB.
- The GTM hiring decision needs a board steer, not just a recommendation — flag it as a decision item.

Now run, in order:

1. `/coordinator:write-meeting-agenda "Q2 Board Meeting" --dir docs/meetings`
2. `/coordinator:write-meeting-qanda <absolute path to agenda.md from step 1>`
3. `/coordinator:write-meeting-pdf <absolute path to qanda.md from step 2>`

You are only finished when `meeting.pdf` exists alongside `agenda.md` and `qanda.md`. Confirm the absolute path of the PDF in your final message.

## Criteria

- [ ] PASS: Skill writes `meeting.pdf` to the same folder as the qanda (`docs/meetings/2026-05-15-q2-board-meeting/meeting.pdf` or equivalent absolute path). Confirms the absolute path in chat output.
- [ ] PASS: The PDF file exists with non-zero size — typically 50KB or larger because brand fonts and PNGs are embedded.
- [ ] PASS: The PDF has the expected page count: 1 cover page + ceiling(items_per_section / 2) for each of the four agenda sections. For the Acme Robotics scenario the qanda has 4 sections (Financial / People / Product and Strategy / Governance) with ~4 / 3 / 2 / 3 items respectively, giving 2 + 2 + 1 + 2 = 7 content pages plus 1 cover = 8 pages total.
- [ ] PASS: Skill does NOT modify `agenda.md` or `qanda.md` — only writes the new PDF.
- [ ] PASS: Skill output identifies the renderer's wrapper script (`render-meeting-pdf.sh`) or the Python entry, not just naked Python — and on first run, the wrapper builds a Docker image (`turtlestack/coordinator-meeting-pdf:<hash>`) from the bundled Dockerfile and reuses it thereafter; the host only needs Docker.
- [ ] PARTIAL: Output mentions the next step is sideloading the PDF to the Remarkable Paper Pro for use during the meeting.

## Output expectations

- [ ] PASS: `meeting.pdf` exists at the path reported in chat. The chat output gives an absolute path that resolves to a real file.
- [ ] PASS: `meeting.pdf` is a valid PDF (begins with the bytes `%PDF-` — i.e. recognised as a PDF by `file` command).
- [ ] PASS: `meeting.pdf` is between 50KB and 5MB. Smaller suggests a render failure; much larger suggests something other than a meeting PDF was written.
- [ ] PASS: `agenda.md` and `qanda.md` are also present in the same folder — the chained workflow produced all three artifacts.
- [ ] PARTIAL: The skill catches and surfaces any wrapper-script error (e.g. Docker missing — exit 69, image build failed) rather than reporting success and producing an empty file.
