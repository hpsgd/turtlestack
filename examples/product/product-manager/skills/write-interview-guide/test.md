# Test: write-interview-guide applies The Mom Test — past behaviour, never future intent

Scenario: A PM needs a generative interview guide before running discovery. The skill must apply The Mom Test
rigorously: open with the three rules, write behavioural questions anchored to specific past events (never
"would you use X?"), arm the interviewer with fluff-redirect prompts (compliments are a warning, not a win),
and structure the arc with a soft close — without pitching the solution.

## Prompt

Use the product-manager `write-interview-guide` skill to write a generative discovery interview guide to
understand how mid-market ops managers currently deal with duplicate customer records and what it costs them.
Write the guide to a file under `docs/product/` in the current working directory, in the skill's standard
format.

Proceed without asking — produce the interview guide.

## Criteria

- [ ] PASS: States a learning goal about understanding a current behaviour ("how they reconcile duplicates and what it costs"), not validating a solution ("would they use our dedup feature")
- [ ] PASS: Opens the guide with the three Mom Test rules (talk about their life not your idea; ask about specific past events not hypotheticals; talk less, listen more)
- [ ] PASS: Every behavioural question anchors to a real, recent, specific past event — "tell me about the last time you dealt with a duplicate record" — NOT "would you..." or "how often do you..." in the abstract
- [ ] PASS: Contains NO hypothetical-future or opinion questions — no "would you use", "do you think", "how would you want to solve this"
- [ ] PASS: Includes fluff-redirect prompts for generic claims, future promises, and compliments — and treats a compliment as a warning sign, not validation
- [ ] PASS: Does NOT pitch or describe a solution anywhere in the guide (no concept reactions in a generative interview)
- [ ] PASS: Structures the arc: warm-up opening → behavioural core → soft close ("what didn't I ask that I should have?")
- [ ] PARTIAL: Notes a confirmation-bias guard — e.g. two interviewers, or that a zero-discard interview is a red flag

## Output expectations

- [ ] PASS: Output guide file exists under `docs/product/` opening with the three Mom Test rules and a behaviour-focused learning goal
- [ ] PASS: The behavioural-core questions are all anchored to specific past events; a reader could not find a "would you" / "do you think" hypothetical among them
- [ ] PASS: Output includes explicit redirects for compliments / generic claims / future promises, framing compliments as zero-signal
- [ ] PASS: No solution is pitched anywhere in the guide
- [ ] PASS: The guide has distinct opening, behavioural-core, and soft-close sections — the soft close keeps listening for the doorknob insight
- [ ] PARTIAL: Output flags a confirmation-bias guard (note-taker / two interviewers / zero-discard red flag)
