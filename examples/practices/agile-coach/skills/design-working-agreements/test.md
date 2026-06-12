# Test: design-working-agreements coaches the team from vague values to testable behaviours

Scenario: A coach facilitates a team to author its own working agreements. The skill must surface friction first, coach vague aspirations into specific testable behavioural agreements, distinguish agreements from the Definition of Done, set a review cadence, and never author the agreements itself.

## Prompt

Use the agile-coach `design-working-agreements` skill to facilitate the "billing" team authoring its working agreements. Context: standups regularly start late, blockers get sat on until the next day, and people talk over each other in meetings. In a quick round the team offered these as starting points: "we'll respect each other", "we'll communicate better", "we'll be on time", and "auth changes should have a security review before merge". Coach these into proper agreements and write the result to `docs/coaching/working-agreements.md` in the current working directory. Respond in the skill's standard format.

Proceed without asking — facilitate and produce the artifact.

## Criteria

- [ ] PASS: Surfaces the friction points first (late standups, sat-on blockers, talking over each other) before drafting agreements
- [ ] PASS: Coaches each vague value into a specific, testable, behavioural agreement — e.g. "we'll be on time" becomes "standup starts at 9:30; we start without latecomers"
- [ ] PASS: Applies a specific/testable test to each candidate and rejects or rewrites anything that names a value rather than an observable behaviour
- [ ] PASS: Recognises "auth changes should have a security review before merge" is a quality gate (Definition of Done), not a working agreement, and routes it to coach-definition-of-done
- [ ] PASS: The coach facilitates the team to author the agreements and explicitly does NOT author them itself — an agreement the coach wrote is the coach's, not the team's
- [ ] PASS: Sets a review cadence / trigger so the agreements are revisited rather than becoming invisible wallpaper
- [ ] PARTIAL: Keeps the set small — favours a short list the team lives by over a long list it forgets

## Output expectations

- [ ] PASS: Output writes a working-agreements artifact with the friction points surfaced, the team-authored agreements, a review cadence, and a routed-to-DoD section
- [ ] PASS: Every agreement in the output is specific, testable, and behavioural — you could observe whether it happened — not an aspiration like "we'll respect each other"
- [ ] PASS: The output explicitly moves the security-review item out of the agreements and into the Definition-of-Done routing section
- [ ] PASS: Output frames the agreements as team-authored (records who was present / that the team produced them) rather than presenting agreements the coach wrote
- [ ] PASS: Output sets a concrete review trigger (a standing retro item or a trigger like a new joiner or recurring friction)
- [ ] PARTIAL: Output shows the vague-to-specific coaching for at least three of the four starting points, demonstrating the transformation rather than just listing finished agreements
