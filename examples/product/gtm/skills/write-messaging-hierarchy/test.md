# Test: write-messaging-hierarchy produces primary + supporting + proof + persona variants from positioning

Scenario: GTM is given an existing positioning (staged on disk) and asked to build the messaging hierarchy.
The skill must consume that positioning (not redo it), produce ONE primary message that passes the competitor
test, 3-4 supporting messages each traceable to a positioning attribute, at least one proof point per
supporting message tagged by segment, and per-persona variants that change emphasis/order/proof but keep the
primary message constant. A hierarchy with invented pillars that don't trace to the positioning, or a
different primary message per persona, must not score well.

## Prompt

A positioning document already exists at `docs/gtm/positioning.md` (relative to your current working
directory) — read it first. Then use the gtm `write-messaging-hierarchy` skill to build the messaging
hierarchy for "Tideline" from that positioning.

Write the messaging-hierarchy artifact to `docs/gtm/messaging-hierarchy-tideline.md` (a relative path under
the current working directory). Respond in the skill's standard format. Proceed without asking.

## Criteria

- [ ] PASS: Loads the existing positioning from `docs/gtm/positioning.md` and restates its statement / tagline / personas / unique attributes — does NOT redo positioning or invent a new market position
- [ ] PASS: Produces exactly ONE primary message (a single sentence stating core value in buyer terms), not two co-equal "most important things"
- [ ] PASS: The primary message passes the competitor test — it is specific to Tideline (back-office-runs-itself / no-show recovery), not a sentence a generic practice tool could also truthfully say
- [ ] PASS: Writes the primary message as candidates then commits to one with a reason — distinguishes the primary message from the tagline
- [ ] PASS: Defines 3-4 supporting messages, each mapped to a specific positioning attribute/value (one-login, no-show recovery, compliance-at-point-of-care, clinician-run) — not the rule-of-three reflex with invented pillars
- [ ] PASS: Each supporting message is a claim, not a feature ("set up in minutes" not "import wizard"), and traces to a positioning element
- [ ] PASS: Attaches at least one proof point per supporting message, preferring quantified proof (e.g. ~3 no-shows recovered/week, <30-min onboarding, ~5 hours/week reclaimed) drawn from the positioning's proof list
- [ ] PASS: Tags each proof point by the segment it applies to (solo practitioner vs small-clinic practice manager) and marks any unsourced proof "unverified"
- [ ] PASS: Builds per-persona variants for the two personas, leading each with the pillar that persona cares about most and shifting language/proof — solo leads on time-back/no-shows, practice manager leads on consistency/compliance
- [ ] PASS: Keeps the primary message constant across personas — only emphasis, order, and proof change per persona
- [ ] PASS: Pressure-tests with the consistency check (could a copywriter produce web + email + sales line without inventing claims)
- [ ] PASS: Labels the output DRAFT — requires human review and has valid YAML frontmatter

## Output expectations

- [ ] PASS: Output writes the hierarchy to `docs/gtm/messaging-hierarchy-tideline.md` under the working directory and restates the source positioning at the top
- [ ] PASS: Output has a single primary message that is Tideline-specific (would fail a competitor saying it), with rejected candidates noted
- [ ] PASS: Output's supporting messages each map to a named positioning attribute — no invented pillar without a positioning root
- [ ] PASS: Output attaches segment-tagged proof points (quantified where possible) under each supporting message, with unsourced ones marked unverified
- [ ] PASS: Output's persona variants keep the SAME primary message and only change which pillar leads, the language, and the proof — solo vs practice-manager emphasis is visibly different
