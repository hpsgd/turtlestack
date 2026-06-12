# Test: competitor-teardown skill (event-triggered deep dive)

Scenario: A competitor (Lumadesk) just raised a $90M Series C and announced an aggressive move into our SMB segment. The team wants a deep teardown triggered by that event, working from a staged dossier rather than live research.

## Prompt

Work entirely from the staged dossier — do NOT perform any live web research (no WebSearch, no WebFetch). The competitor profile, pricing, ICP evidence, GTM signals, funding history, people, and the triggering event are all on disk.

/analyst:competitor-teardown Lumadesk — triggered by their $90M Series C and stated push into SMB {workspace}/work/lumadesk

Read `{workspace}/work/lumadesk/profile.md` first — it holds everything: product evidence from public docs and job ads, pricing tiers, ICP logos/case studies, GTM motion, funding rounds, key people, and the trigger (Series C + SMB-push announcement).

Requirements for the response:

- Name the TRIGGER up front and use it as the lens — a funding+segment-entry trigger weights GTM expansion, hiring, and the threat to our SMB segment.
- Reconstruct product architecture from the public-source evidence (API/data model, stack from job ads, release cadence) and ATTRIBUTE each inference to its source, labelling job-ad/changelog inferences as signal not confirmation.
- Capture the full pricing/packaging model and read the "contact sales" enterprise tier as a motion signal.
- Distinguish who they SAY they target ("all sizes") from who the evidence shows they WIN (mid-market/enterprise per logos and case studies).
- Read the GTM motion (sales-led / enterprise) from the evidence (no free tier, heavy sales hiring, partner page).
- Cover funding history and label the ARR figure as an estimate with its source, not a fact.
- Cover key people / direction-signalling hires (VP Platform, Head of Enterprise Sales, ML hires).
- END with a strategic "so what" read that takes a position on what the Series C + SMB push means for us — not a neutral profile.

## Criteria

- [ ] PASS: Skill writes a conforming report to disk under `lumadesk/competitor-teardown/` (see ARTIFACTS WRITTEN — at least one .md file there)
- [ ] PASS: The written file opens with YAML frontmatter including title, date, author=competitor-teardown, category (per report-conventions)
- [ ] PASS: The TRIGGER (Series C raise + stated SMB push) is named up front and used as the analytical lens, not a generic company profile
- [ ] PASS: Product architecture is reconstructed from public-source evidence (API/data model, stack from job ads, release cadence) with each inference attributed to its source
- [ ] PASS: Job-ad and changelog inferences are labelled as signal, not confirmation
- [ ] PASS: Pricing/packaging is captured with tiers and price points, and the "contact sales" enterprise tier is read as a motion signal
- [ ] PASS: The report distinguishes who they SAY they target ("all sizes") from who they actually WIN (mid-market/enterprise per logos and case studies)
- [ ] PASS: The GTM motion is read as sales-led / enterprise from the evidence (no free tier, heavy sales hiring, partner page) — not asserted blind
- [ ] PASS: Funding history is covered and the ARR figure is labelled an estimate with its source — not stated as a fact
- [ ] PASS: The report ends with a strategic "so what" read that takes a POSITION on what the raise + SMB push means for us — not a neutral summary
- [ ] PASS: The skill did NOT perform live web research — it built the teardown from the staged dossier
- [ ] PASS: Chat response includes the absolute path to the written report

## Output expectations

- [ ] PASS: The teardown is shaped by the trigger throughout — the SMB-segment threat and AI/GTM expansion are weighted because of the Series C, not treated as an even survey of all attributes
- [ ] PASS: The strategic read is genuinely a position (e.g. "they're coming downmarket into us with capital and an enterprise-built product that is over-engineered for SMB — our wedge is X"), not a restatement of the facts
