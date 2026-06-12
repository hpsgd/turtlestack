# Test: coach-definition-of-done facilitates a specific, testable, team-owned DoD

Scenario: A team keeps presenting half-done work as complete because its Definition of Done is vague. The coach must facilitate the team to author its own DoD, establish what it applies to, run a specificity test that converts vague criteria to objectively testable ones, tie the DoD to the release-manager's gates, and never hand down the DoD from management.

## Prompt

Use the agile-coach `coach-definition-of-done` skill to facilitate the "billing" team authoring its Definition of Done. Context: the team's current "DoD" is just "code reviewed, tested, documented" and arguments break out at the sprint review about whether something is actually done. The team works on user-facing features, API changes, and infrastructure changes. Auth and payment-data changes are involved, and the release manager's go/no-go gate already requires a security review for auth changes. Facilitate the team to a real DoD and write it to `docs/coaching/definition-of-done.md` in the current working directory. Respond in the skill's standard format.

Proceed without asking — facilitate and produce the artifact.

## Criteria

- [ ] PASS: Establishes the work types the DoD applies to (user-facing features, API changes, infrastructure) rather than one undifferentiated DoD
- [ ] PASS: Runs a specificity test that converts vague criteria into objectively testable ones — e.g. "tested" becomes "unit tests written, line coverage >= 80%" or "acceptance tests pass; manual smoke test recorded"
- [ ] PASS: Rewrites or drops any criterion you could argue about at the sprint review — "reviewed" becomes "approved by one engineer not the author"
- [ ] PASS: Ties the DoD to the release-manager's go/no-go gates, keeping it coherent with the existing security-review-for-auth gate
- [ ] PASS: The coach facilitates the team to author the DoD and explicitly does NOT hand down a management-authored DoD
- [ ] PASS: Treats "deployed to production" as a conscious continuous-delivery commitment if included, not an accidental criterion
- [ ] PARTIAL: Sets a review trigger — revisit the DoD in the retro when an item proves vague or is repeatedly skipped — and keeps quality criteria out of the working agreements

## Output expectations

- [ ] PASS: Output writes a Definition-of-Done artifact with scope (work types), team-authored testable criteria, a specificity check, release-gate coherence, and a review trigger
- [ ] PASS: Every criterion in the output is objectively checkable — no criterion you could dispute at the review — demonstrating the vague-to-specific transformation
- [ ] PASS: Output's release-gate-coherence section explicitly includes the security-review-for-auth gate and keeps the DoD aligned with it
- [ ] PASS: Output frames the DoD as team-authored (records who was present / that the team produced it), not handed down
- [ ] PASS: Output organises criteria by the work types in scope (feature / API / infrastructure) rather than one flat list
- [ ] PARTIAL: Output sets a concrete review trigger and notes that gate-affecting DoD changes route through the release manager
