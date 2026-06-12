# Test: diagnose-strategy catches a textbook bad strategy with cited evidence

Scenario: The CPO is handed an existing "strategy" document to pressure-test before it ships. The document
(staged as a fixture) is a textbook Rumelt *bad* strategy: dense fluff, a list of goals presented as the
plan, no diagnosis of any obstacle, a guiding policy that permits everything ("better across every
dimension"), and a scattered grab-bag of unrelated initiatives. The diagnose-strategy skill must READ the
fixture, test it against Rumelt's kernel (diagnosis + guiding policy + coherent action), flag the four
hallmarks of bad strategy WITH quotes from the document, rate it overall as Bad strategy (not Incomplete,
not Good), and recommend specific fixes pointing at the authoring skills. It must NOT rewrite the strategy —
this is a read-only critique skill.

The flawed strategy is pre-staged by the harness at `{workspace}/work/docs/strategy/product-strategy-helmsman.md`.

## Prompt

A strategy document has been staged for you at `docs/strategy/product-strategy-helmsman.md` (relative to the
current working directory). Use the cpo `diagnose-strategy` skill to critique it:
`/cpo:diagnose-strategy docs/strategy/product-strategy-helmsman.md`

Read the document, run Rumelt's good-strategy/bad-strategy diagnostic over it, and return the critique in
the skill's standard format. Do not rewrite the strategy. Proceed without asking.

## Criteria

- [ ] PASS: Reads the staged document and summarises what it claims to be (a "strategy") and how it is organised, quoting the document's own framing
- [ ] PASS: Tests for the kernel's DIAGNOSIS and finds it MISSING — no central obstacle/challenge is named anywhere; the document jumps straight to goals and pillars
- [ ] PASS: Tests for the GUIDING POLICY and finds it absent or permits-everything — quotes the "better than the competition across every dimension" / "best in the industry" framing as a non-guiding policy
- [ ] PASS: Tests for COHERENT ACTION and finds the initiatives uncoordinated — names the initiative list (mobile app, AI assistant, Europe, onboarding, marketplace, rebrand, freemium) as a scattered grab-bag that does not reinforce a single approach
- [ ] PASS: Flags FLUFF as present and quotes specific instances — e.g. "world-class value", "leverage synergies across our ecosystem", "transformative growth", "cutting-edge" — as inflated language masking absent content
- [ ] PASS: Flags FAILURE TO FACE THE CHALLENGE (no obstacle defined) AND MISTAKING GOALS FOR STRATEGY — quoting goals presented as the plan (e.g. "grow ARR to $50M", "become the #1 fleet-management product", "double our active user base")
- [ ] PASS: Flags BAD STRATEGIC OBJECTIVES — the "strategic pillars" (customer obsession, innovation, operational excellence, growth) are recognised as a dog's-dinner / blue-sky list, not a coherent reachable set
- [ ] PASS: Rates the document OVERALL as **Bad strategy** (not "Good strategy", not merely "Incomplete"), applying Rumelt's bar plainly without grading on a curve because the document reads as polished
- [ ] PASS: Every kernel verdict and hallmark flag cites the document (quotes the offending line or names the section); does NOT rewrite or author a replacement, instead giving actionable recommendations that point fixes to `/cpo:write-product-strategy` (and `/cpo:write-product-vision` if the missing piece is the vision)

## Output expectations

- [ ] PASS: Output presents the kernel as a table (Diagnosis / Guiding policy / Coherent action) with a verdict and cited evidence per row, and a bad-strategy-hallmarks table with Found?/Evidence per hallmark — all four hallmarks marked Found with quotes
- [ ] PASS: Output's overall verdict is **Bad strategy** and the recommended actions name what to add (a diagnosis, a guiding policy) and which skill produces the fix, without rewriting the document
