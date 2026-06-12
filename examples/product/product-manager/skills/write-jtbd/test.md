# Test: write-jtbd produces solution-agnostic jobs with outcome scoring

Scenario: A PM enters a new problem space and needs a JTBD analysis. The skill must define the job performer
in a specific circumstance, write a solution-agnostic core functional job in the canonical format, map
emotional and social jobs (not just functional), score desired outcomes on importance × satisfaction with an
opportunity calculation, and translate underserved outcomes into product implications.

## Prompt

Use the product-manager `write-jtbd` skill to define a Jobs-to-be-Done analysis for "freelance bookkeepers
preparing quarterly BAS (business activity statement) submissions for their small-business clients". Write
the analysis to a file under `docs/product/` in the current working directory, in the skill's standard
format.

Proceed without asking — produce the JTBD analysis.

## Criteria

- [ ] PASS: Defines the job performer as a specific person in a specific circumstance (e.g. a bookkeeper at quarter-end with N clients), not a generic persona like "accountant"
- [ ] PASS: Writes the core functional job in the canonical "When I [situation], I want to [motivation], so I can [outcome]" format
- [ ] PASS: The core job is solution-agnostic — does not mention a UI element, feature, or the product (e.g. "narrow results", not "use the filter dropdown")
- [ ] PASS: Maps emotional jobs (how they want to feel / avoid feeling) AND social jobs (how they want to be perceived) — does not skip these for functional jobs only
- [ ] PASS: Defines desired outcomes as measurable statements ("minimise the time to...", "reduce the likelihood of...") — never "make it easier" or "improve the experience"
- [ ] PASS: Scores outcomes on importance and satisfaction and computes an opportunity score, identifying underserved (high importance, low satisfaction) outcomes
- [ ] PASS: Translates underserved outcomes into product implications (what to build) AND names overserved areas to deprioritise — not just a list of jobs
- [ ] PARTIAL: Captures hiring/firing criteria or switching forces (push/pull/anxiety/habit) for the job

## Output expectations

- [ ] PASS: Output file exists under `docs/product/` with a job-performer table, a core functional job, related (functional/emotional/social) jobs, an outcome table, and product implications
- [ ] PASS: The core functional job statement contains no product feature, UI element, or technology reference — it is solution-agnostic
- [ ] PASS: Emotional AND social jobs are both present, not collapsed into functional jobs only
- [ ] PASS: The outcome table scores importance and satisfaction and flags at least one underserved outcome via an opportunity calculation, not a bare assertion of "high priority"
- [ ] PASS: Every outcome statement is measurable (direction + metric), not "make it easier" / "improve the experience"
- [ ] PARTIAL: The analysis distinguishes the job (stable need) from tasks (steps within a solution) — does not list tasks as jobs
