# Test: market-voc surfaces resonance / objections / switching and holds the GTM lens boundary

Scenario: GTM is asked to pull the market voice-of-customer for a product. The skill must capture the
three market-facing slices — positioning resonance (in the buyer's words), ranked sales objections
(separating stated objection from root cause), and switching reasons (push/pull/anxiety/habit) — and it
must hold the distributed-VoC boundary: name itself as the GTM lens, point at the other lenses (Support,
Customer Success, UX Research), and refuse to centralise or reconcile conflicting VoC into a single number,
surfacing conflict instead. A generic "customers like the product, some find it pricey" summary must not
score well.

## Prompt

Use the gtm `market-voc` skill to gather the market voice-of-customer for "Tideline", an
appointment-and-records product for solo and small allied-health clinics. Scope it to the last two quarters,
SMB segment, drawn from sales call notes, win/loss interviews, and G2 reviews.

Working context you can use as the raw VoC material:

- Our positioning claims "run your clinic without a back office". Buyers in calls say things like "I just
  want to stop chasing no-shows" and "one login instead of the three tools I juggle now". A few buyers asked
  "so is this a booking tool or a notes tool?" — they couldn't tell what category we're in.
- The objection sales hears most is "it's too expensive for a solo practice" (high frequency). Sales also
  hears "I'd have to move all my notes across" (medium) and "does it do Medicare claiming?" (medium).
- Won deals switched after a no-show wiped a day's revenue; the pull was bookings plus reminders in one place;
  the anxiety was migrating existing client records; habit was their old spreadsheet.
- Lost deals went to a rival that already did Medicare claiming; the trigger was an end-of-year compliance push.
- Support has separately reported that onboarding is the top pain in tickets. That conflicts with what you
  hear in deals, where price is the loudest objection.

Write the VoC artifact to `docs/gtm/market-voc-tideline.md` (a relative path under the current working
directory). Respond in the skill's standard format. Proceed without asking.

## Criteria

- [ ] PASS: Names itself explicitly as the GTM / market-facing VoC lens and names the other lenses (Support / Customer Success / UX Research) that hold the rest — does not claim to be "the" voice of the customer
- [ ] PASS: Does NOT centralise or reconcile VoC into a single number; treats the Support-vs-GTM disagreement (onboarding pain vs price objection) as signal to surface, not noise to resolve
- [ ] PASS: Surfaces the Support/GTM conflict explicitly (e.g. a "conflicts with other lenses" section) and leaves it unresolved by design, routing the weighing to the consuming role (product-owner / CPO)
- [ ] PASS: Captures positioning resonance in the buyer's own words, recording the gap between our claim ("run your clinic without a back office") and buyer language ("one login instead of three tools", "stop chasing no-shows")
- [ ] PASS: Flags the category-confusion signal ("is this a booking tool or a notes tool?") as confusion — worse than falling flat — not just neutral feedback
- [ ] PASS: Catalogues sales objections ranked by frequency, separating the stated objection from the root cause (e.g. "too expensive" distinguished from "doesn't see the value yet")
- [ ] PASS: Classifies objections as real concern vs misconception vs competitor FUD, and notes that objections recurring across the segment are a positioning problem rather than an enablement one
- [ ] PASS: Reconstructs switching using the four-forces framing (push off old / pull to new / anxiety / habit) for both won and lost deals, naming the trigger event (no-show wiping a day; year-end compliance push)
- [ ] PASS: Weights lost / churned voices over won voices for finding gaps — and surfaces the Medicare-claiming gap that lost deals to the rival
- [ ] PASS: Synthesises findings into themes with evidence strength and routes each to an owning skill/role (positioning / messaging / battle-card / product-owner)
- [ ] PASS: Labels the output DRAFT — requires human review
- [ ] PASS: Has valid YAML frontmatter (name, description, argument-hint)

## Output expectations

- [ ] PASS: Output writes the VoC file to `docs/gtm/market-voc-tideline.md` under the working directory
- [ ] PASS: Output's positioning-resonance section uses verbatim buyer quotes and records the claim-vs-buyer-language gap, with the category-confusion quote flagged as confusing rather than merely weak
- [ ] PASS: Output's objections section is ranked by frequency and separates stated objection from root cause, classifying each (concern / misconception / FUD)
- [ ] PASS: Output's switching section uses push / pull / anxiety / habit for won AND lost deals and names the trigger event for each direction
- [ ] PASS: Output contains an explicit conflict between the GTM lens and the Support lens (onboarding vs price) that is left unresolved, with the weighing handed to the consuming role — NOT averaged or reconciled into one verdict
