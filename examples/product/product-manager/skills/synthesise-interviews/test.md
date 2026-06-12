# Test: synthesise-interviews codes needs, seeks disconfirmation, calls saturation

Scenario: A PM has run several interviews and must synthesise them. The skill must pattern-code observations
at the need level (not feature requests), require multiple participants per theme (one quote is an anecdote),
actively look for disconfirming evidence and report the discard rate, map themes onto OST changes that cite
their interviews, and make an explicit saturation call. Raw interview notes are staged as a fixture.

## Prompt

Use the product-manager `synthesise-interviews` skill to synthesise the discovery interviews for the
"activation" slice. The raw interview notes are at `{workspace}/work/docs/product/interviews/` (five files) —
read them all. The desired outcome is to lift week-one activation. Write the synthesis to a file under
`docs/product/` in the current working directory, in the skill's standard format.

Proceed without asking — produce the synthesis.

## Criteria

- [ ] PASS: Reads the staged interview notes and assembles the window (participant, segment, type, date)
- [ ] PASS: Codes at the NEED/behaviour level, not feature requests — translates "I wish it had a bulk button" up to the underlying need
- [ ] PASS: Promotes a pattern to a theme only when multiple participants support it — a single vivid quote is an anecdote, not a theme
- [ ] PASS: Actively seeks disconfirming evidence and reports a discard rate — flags a zero-discard theme as a possible confirmation-bias artifact
- [ ] PASS: Correctly distinguishes the cross-participant themes (mobile bank-feed failure; no setup confirmation) from the single-participant anecdote (invite discoverability)
- [ ] PASS: Maps themes onto OST changes — add / strengthen / flag-contradicted — each change citing the interviews it came from
- [ ] PASS: Makes an explicit saturation call (continue vs saturated) based on the rate of new themes, not a feeling
- [ ] PARTIAL: Notes the mixed segment as a reason themes may not be saturating, recommending a narrower segment

## Output expectations

- [ ] PASS: Output file exists under `docs/product/` with a window table, a themes table (with participant support counts and discard rate), an OST-updates table, and a saturation call
- [ ] PASS: Themes are need-level, and each cites the participants/interviews supporting it
- [ ] PASS: The single-participant invite-discoverability signal is treated as an anecdote to watch, not promoted to a confirmed theme
- [ ] PASS: A discard rate / disconfirmation check appears for the themes — not an all-confirming synthesis
- [ ] PASS: The saturation call is stated as a decision with reasoning (rate of new themes), not omitted
- [ ] PARTIAL: OST changes cite source interviews rather than appearing as unsourced assertions
