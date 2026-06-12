# Test: review-mining skill (competitor opportunity inventory)

Scenario: A product team wants to mine a competitor's (TaskBridge) public reviews to build an opportunity inventory — what their customers complain about that we could win on. A staged review corpus stands in for the live review sites so the run is deterministic.

## Prompt

Work entirely from the staged review corpus — do NOT perform any live web research and do NOT fetch any review sites (no WebSearch, no WebFetch). The reviews, listings, ratings, and segment metadata are already on disk.

/analyst:review-mining TaskBridge {workspace}/work/taskbridge

Read `{workspace}/work/taskbridge/reviews.md` first — it holds the G2 / Capterra / App Store listings with review counts and average ratings, sampled reviews across the full 1-5 star distribution, and a note on segment skew.

Requirements for the response:

- State the lens explicitly: this is a COMPETITOR, so the output is an opportunity inventory (not a fix-list).
- Record the per-site listings with review count and average rating from the corpus.
- Read across the FULL rating distribution — pull what 4-5 star reviewers value AND what 1-2 star reviewers warn about, and use the 3-star reviews for balanced signal. Don't build themes from 1-star reviews alone.
- Extract themes by topic, each with a representative verbatim quote, a QUANTIFIED weight (rough share of reviews), and a sentiment direction.
- Apply segment skew — show where a theme concentrates (the staged note shows mobile-crash and onboarding-complexity complaints concentrate in SMB / App Store).
- Translate the top competitor complaint themes into an opportunity inventory ("what we could win on").
- Flag the representativeness caveat — reviews self-select and are directional, not statistically representative.

## Criteria

- [ ] PASS: Skill writes a conforming report to disk under `taskbridge/review-mining/` (see ARTIFACTS WRITTEN — at least one .md file there)
- [ ] PASS: The written file opens with YAML frontmatter including title, date, author=review-mining, category (per report-conventions)
- [ ] PASS: The lens is stated explicitly as COMPETITOR / opportunity inventory — not own-product fix-list
- [ ] PASS: Per-site listings are recorded with review count and average rating from the corpus (G2 412/4.1, Capterra 188/4.0, App Store 95/3.6)
- [ ] PASS: Themes are read across the full rating distribution — both what high-star reviewers value and what low-star reviewers warn about — not from 1-star reviews alone
- [ ] PASS: Each theme carries a representative verbatim quote AND a quantified weight (rough share of reviews), not "some users say X"
- [ ] PASS: Segment skew is applied — at least one theme (mobile crashes / onboarding complexity) is shown concentrating in SMB / App Store reviewers per the staged metadata
- [ ] PASS: The top complaint themes are translated into an opportunity inventory ("what we could win on") — the competitor lens
- [ ] PASS: A representativeness caveat is included — reviews self-select, directional not statistically representative
- [ ] PASS: The skill did NOT perform live web research or fetch review sites — it mined the staged corpus
- [ ] PASS: Chat response includes the absolute path to the written report

## Output expectations

- [ ] PASS: Themes are quantified (e.g. "mobile reliability appears in ~X of reviews, skews strongly negative") rather than vaguely asserted
- [ ] PASS: The opportunity inventory ties specific competitor weaknesses (mobile reliability, onboarding complexity, support latency, tier-pricing cliff) to concrete angles we could win on
