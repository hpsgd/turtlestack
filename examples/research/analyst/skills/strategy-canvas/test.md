# Test: strategy-canvas skill (Blue Ocean ERRC)

Scenario: A product team for NoteFlow wants a Blue Ocean strategy canvas of the AU cloud note-taking market, driven off existing competitive-analysis and review-mining reports already staged in the engagement directory, to find whether a value-innovation move is available.

## Prompt

Work entirely from the staged engagement files — do NOT perform any live web research (no WebSearch, no WebFetch). The competitor set and the buyer evidence you need are already on disk.

/analyst:strategy-canvas cloud note-taking apps (AU SMB) {workspace}/work/blueoak

Use these staged inputs (read them first):

- `{workspace}/work/blueoak/competitive-analysis/cloud-note-taking-au.md` — the four direct competitors (NoteFlow = us, PageMind, Quillbase, JotRapid), their factor scores, and recent moves.
- `{workspace}/work/blueoak/review-mining/cloud-note-taking-au.md` — category buyer voice: what buyers actually pay for vs value, with quantified theme shares and segment skew.

Requirements for the response:

- Build the value-curve table across 6-12 competing factors with NoteFlow plus the three named competitors, scoring each from the staged evidence and stating the basis.
- Read the convergence pattern explicitly — say whether the curves bunch (red ocean) or one diverges, as the headline.
- Produce the ERRC grid (Eliminate / Reduce / Raise / Create) with a populated entry in EACH of the four cells, and ground every entry in the staged review-mining buyer evidence (cite the theme), not in opinion.
- Apply the value-innovation test: state whether Eliminate+Reduce cut cost AND Raise+Create lift value.
- Take a position on whether a genuine blue-ocean move is available here or whether the honest read is a red ocean.

## Criteria

- [ ] PASS: Skill writes a conforming report to disk under `blueoak/strategy-canvas/` (see ARTIFACTS WRITTEN — at least one .md file there)
- [ ] PASS: The written file opens with YAML frontmatter including title, date, author=strategy-canvas, category (per report-conventions)
- [ ] PASS: A value-curve table is present scoring NoteFlow and the three competitors across competing factors, with a stated basis for the scores drawn from the staged inputs
- [ ] PASS: The convergence pattern is named explicitly as the headline — bunched curves (red ocean) vs a diverging curve — not buried
- [ ] PASS: A full ERRC grid is produced with a concrete entry in all FOUR cells (Eliminate, Reduce, Raise, Create) — not just two
- [ ] PASS: Eliminate/Reduce entries are grounded in buyer evidence that buyers pay for things they don't value (e.g. template galleries / integration breadth from the review-mining themes), not in unsupported opinion
- [ ] PASS: Raise/Create entries lift factors buyers demonstrably value (e.g. fast onboarding / sharing / offline reliability from the review evidence)
- [ ] PASS: The value-innovation test is applied — stating whether the moves cut cost AND lift value, not just differentiate
- [ ] PASS: The skill takes a clear position on whether a blue-ocean move is available or it is a red ocean — does not leave it open
- [ ] PASS: The skill did NOT perform live web research — it applied the framework to the staged material

## Output expectations

- [ ] PASS: Output applies the Blue Ocean ERRC method correctly — Eliminate/Reduce target cost, Raise/Create target value — not a generic SWOT or feature comparison
- [ ] PASS: Output's ERRC entries trace back to the staged buyer evidence (template clutter, integration breadth rarely used, slow onboarding, valued offline/sharing) rather than being invented
- [ ] PASS: Chat response includes the absolute path to the written report
