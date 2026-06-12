# Test: analyst-briefing-prep structures a Gartner/Forrester briefing pack

Scenario: GTM is asked to prepare for an industry-analyst briefing tied to a specific evaluation vehicle
(a Gartner Magic Quadrant). The skill must profile the firm and the evaluation axes, map proof points to the
firm's published criteria (mapping to the right axes, not generic excellence), structure the briefing deck,
storyboard a demo that proves differentiation, and build Q&A prep for the hard analyst questions — naming
gaps honestly in prep and answering them in Q&A. It must produce a prep pack (not the live delivery), avoid
marketing superlatives, and never disparage named competitors. A generic "here are some slides" deck must not
score well.

## Prompt

Use the gtm `analyst-briefing-prep` skill to prepare for a Gartner Magic Quadrant briefing for "Tideline", an
appointment-and-records platform for allied-health clinics. This is a pre-inclusion briefing — Gartner has not
yet evaluated us and we want to set the frame before they do. Our known weak spot is enterprise/multi-site
scale (we are strong for solo and small clinics but light on large clinic groups), and the category leader,
"CareLedger", is strong there. We have customer proof for SMB outcomes (no-show recovery, fast onboarding) but
thin enterprise references.

Write the prep-pack artifact to `docs/gtm/analyst-briefing-gartner-mq.md` (a relative path under the current
working directory). Respond in the skill's standard format. Proceed without asking.

## Criteria

- [ ] PASS: Profiles the firm and the evaluation vehicle — recognises Gartner MQ and its two axes (ability to execute × completeness of vision) and uses the cycle stage (pre-inclusion = set the frame)
- [ ] PASS: Maps proof points to the MQ evaluation criteria/axes (execution vs vision), not to generic "we're great" claims — every claim attached to an axis
- [ ] PASS: Names the enterprise/multi-site scale weakness HONESTLY in the internal prep, and routes the prepared answer to Q&A rather than burying it in the deck
- [ ] PASS: Structures a briefing deck with a clear single thesis (company snapshot → market change/POV → positioning → capabilities-vs-criteria → proof → roadmap → demo), respecting the analyst's time
- [ ] PASS: Storyboards a demo that proves differentiated capabilities mapped to claims/criteria — not a generic feature tour — and plans a failure/fallback path
- [ ] PASS: Builds Q&A prep for the hard questions including the weakest criterion (enterprise scale), the direct CareLedger comparison, roadmap credibility, and pricing/traction
- [ ] PASS: For the competitor-comparison Q&A, differentiates on Tideline's strength (SMB fit) rather than disparaging CareLedger by name
- [ ] PASS: Avoids marketing superlatives ("market-leading", "best-in-class") — notes analysts downgrade them on sight and uses specifics/proof instead
- [ ] PASS: Treats every Q&A answer as needing a proof point, and the gap answer as "known gap + plan + timeline" rather than denial
- [ ] PASS: Produces a PREP PACK (deck outline + demo storyboard + Q&A) and states a human delivers the briefing — does not present the output as the live briefing
- [ ] PASS: Labels the output DRAFT — requires human review
- [ ] PASS: Has valid YAML frontmatter (name, description, argument-hint)

## Output expectations

- [ ] PASS: Output writes the prep pack to `docs/gtm/analyst-briefing-gartner-mq.md` under the working directory
- [ ] PASS: Output maps proof points to the MQ axes (execution / vision) in a criteria table, leading with the most heavily weighted criteria — not a generic strengths list
- [ ] PASS: Output's deck outline carries a single thesis and the recommended section flow, with no marketing superlatives
- [ ] PASS: Output's demo storyboard ties each beat to a claim/criterion it proves and includes a fallback for a live-demo failure
- [ ] PASS: Output's Q&A prep covers the enterprise-scale gap (as known-gap-plus-plan), the CareLedger comparison (differentiate-on-strength, no disparagement), and roadmap credibility — each answer backed by a proof point
