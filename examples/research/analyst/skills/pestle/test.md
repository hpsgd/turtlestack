# Test: pestle skill (prioritise and argue, not a six-box checklist)

Scenario: A UK digital mental-health app is deciding whether to launch in Australia. They want a PESTLE scan that filters to the two or three forces that actually matter for THIS decision and says what they imply — not a six-box list where everything is "moderate impact". A staged brief provides the candidate factors.

## Prompt

Work entirely from the staged expansion brief — do NOT perform any live web research (no WebSearch, no WebFetch). The candidate factors across all six dimensions are already gathered for you on disk.

/analyst:pestle Launch of Meridian (digital mental-health app) in Australia {workspace}/work/meridian

Read `{workspace}/work/meridian/expansion-brief.md` first — it states the decision, the geography, and the candidate factors collected across Political, Economic, Social, Technological, Legal, and Environmental.

Requirements for the response:

- Frame the decision and geography at the top (UK app launching in Australia).
- Do the discipline: from the candidate factors, SELECT the two or three with material effect on this specific decision. Do NOT output all six dimensions at equal "moderate" weight.
- For each KEPT factor give direction (tailwind/headwind), magnitude, and time horizon — not a single flat impact label.
- Explicitly DISCARD the immaterial dimensions/factors (e.g. Environmental) and say why they're set aside.
- State the IMPLICATION of each material factor for the decision — not just that it exists (e.g. the TGA medical-device line forces a positioning choice; the privacy/health-data rules force a data-residency commitment).
- Conclude with a net read: does the macro-environment support, complicate, or block the launch, and the one thing to act on first.

## Criteria

- [ ] PASS: Skill writes a conforming report to disk under `meridian/pestle/` (see ARTIFACTS WRITTEN — at least one .md file there)
- [ ] PASS: The written file opens with YAML frontmatter including title, date, author=pestle, category (per report-conventions)
- [ ] PASS: The decision and geography are framed explicitly (UK mental-health app launching in Australia)
- [ ] FAIL-IF-CHECKLIST: The report does NOT present all six PESTLE dimensions at equal "moderate impact" weight — a flat six-box checklist with no prioritisation must NOT pass this criterion
- [ ] PASS: The report SELECTS the two or three material factors for this decision (Legal/TGA, Legal/privacy-data-residency, and the Economic B2C-squeeze-vs-B2B-growth split are the strong candidates) rather than treating all dimensions equally
- [ ] PASS: Each kept factor carries direction, magnitude, and time horizon — not a single impact label
- [ ] PASS: The report explicitly discards at least one immaterial dimension (e.g. Environmental) and states why it is set aside
- [ ] PASS: For each material factor the report states an IMPLICATION for the decision (what it forces the team to do), not just that the factor exists
- [ ] PASS: The report concludes with a net read (support / complicate / block) and names the one thing to act on first
- [ ] PASS: The skill did NOT perform live web research — it applied the discipline to the staged brief
- [ ] PASS: Chat response includes the absolute path to the written report

## Output expectations

- [ ] FAIL-IF-CHECKLIST: A mechanical six-box fill where every dimension gets a paragraph and a "moderate" rating with no prioritisation or discard would FAIL — the output prioritises and argues instead
- [ ] PASS: The Legal dimension is correctly identified as the highest-material area (TGA software-as-medical-device classification and health-data privacy), with a concrete implication for how Meridian must position or build
