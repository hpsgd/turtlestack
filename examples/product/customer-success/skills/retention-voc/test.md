# Test: Retention VoC from a churn cohort

Scenario: A customer-success lead wants the qualitative retention narrative behind a quarter's churned and at-risk accounts. The cohort evidence (cancellation reasons, QBR notes, renewal and save-attempt notes, sponsor calls) contains a recurring reporting/export-data-loss theme across several high-ARR accounts, a recurring missing-CRM-integration theme, a champion-departure relationship signal, an onboarding-stalled value-realisation signal, one account whose stated reason (price) diverges from the real cause (disengaged weeks earlier), and one user-level complaint that should be routed away rather than inflated into a retention theme. The skill must produce an ARR-weighted, account-level theme set distinct from individual-user VoC.

## Prompt

The Q2 churn and at-risk cohort's account-level VoC sources are on disk at `{workspace}/work/accounts/q2-churn-cohort.md`. Read it.

/customer-success:retention-voc Q2 2026 churn and at-risk cohort — sources at the path above

Run the full skill: scope the cohort, gather the account-level VoC, separate account-level from individual-user VoC, code the themes, weight them by retention impact (ARR-weighted reach), cross-check against the quantitative churn signal where usage data is present, and package the retention themes for the roadmap. Use the skill's Output Format. Write the output to `{workspace}/work/retention-voc.md` and reply with the path.

## Criteria

- [ ] PASS: Opens with a scope statement — cohort definition, account stages, ARR represented, sources used and any unavailable — before coding themes
- [ ] PASS: Operates at the account level (the buying account, the renewal decision, the sponsor's voice) — not the individual-user level — and tags this output as the customer-success lens among several
- [ ] PASS: Names the export/reporting data-loss reason as a theme spanning multiple accounts (e.g. Northwind, Drake, Vanguard), weighted by the ARR those accounts represent
- [ ] PASS: Names the missing-CRM/Salesforce-integration reason as a theme spanning multiple accounts (Acme, Belltower) — a product gap routed to the roadmap, not a usage complaint
- [ ] PASS: Routes the Pinecrest bulk-edit gripe away as individual-user VoC (and identifies budget, not UX, as the real account decision) — does NOT inflate one end user's frustration into a retention theme
- [ ] PASS: Surfaces the Northwind stated-vs-real divergence — the form cites reporting/value but usage declined ~6 weeks before the renewal conversation — rather than taking the stated reason as the root cause
- [ ] PASS: Weights themes by ARR and account reach, ranking the high-ARR multi-account themes above single-account signals — not by which account was loudest or most recent
- [ ] PASS: Treats single-account signals (e.g. Riverside champion departure, Cobalt onboarding stall) as watch items / single-account drivers, not as named themes requiring 2+ accounts
- [ ] PASS: Classifies each theme's driver (product gap / value realisation / relationship / commercial / quality) and routes it to the right owner
- [ ] PARTIAL: Does NOT propose solutions in the roadmap hand-off — names the problem, the accounts, the ARR, and the evidence, leaving prioritisation and solutioning to the product-owner

## Output expectations

- [ ] PASS: Output is written to the given path and follows the skill's Output Format — Scope, ranked Retention Themes table (with driver, accounts, ARR, routes-to, cross-check), Theme Detail with verbatim quotes, Watch List, User-Level Items Routed Elsewhere, and Roadmap Hand-off
- [ ] PASS: Output carries verbatim account quotes with attribution (account, stage, date) behind each theme — not assertions like "accounts wanted better reporting" with no quote
- [ ] PASS: Output's theme table shows ARR at stake per theme and a quantitative cross-check column (matches / diverges from the usage signal) — at minimum flagging the Northwind stated-vs-real gap
