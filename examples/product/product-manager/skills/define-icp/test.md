# Test: define-icp is account-level, built from best AND churned accounts, behaviour over firmographics

Scenario: A PM defines an Ideal Customer Profile. The skill must build it from real data — best-fit AND
churned/lost accounts (not wins only), extract firmographic criteria cross-checked against the worst-fit set,
add the stronger behavioural criteria (trigger, activation, usage), write explicit disqualifiers, and produce
a qualification checklist — keeping the ICP account-level and distinct from individual personas. Account data
is staged as a fixture.

## Prompt

Use the product-manager `define-icp` skill to define an Ideal Customer Profile for the reconciliation product.
The account data is staged at `{workspace}/work/docs/product/accounts.md` (best-fit and churned/lost
accounts) — read it first and derive the ICP from it. Write the ICP to a file under `docs/product/` in the
current working directory, in the skill's standard format.

Proceed without asking — produce the ICP.

## Criteria

- [ ] PASS: Builds the ICP from real data — uses BOTH the best-fit accounts AND the churned/lost accounts, not wins only (avoids survivorship bias)
- [ ] PASS: Extracts firmographic criteria (industry, size, geography, tech stack, buying structure) and cross-checks them against the worst-fit set
- [ ] PASS: Adds behavioural criteria — trigger, activation behaviour, usage pattern — drawn from the contrast between best-fit and churned accounts
- [ ] PASS: Treats behaviour as the STRONGER predictor — notes that right-size/right-vertical accounts still churned, so firmographics alone over-target
- [ ] PASS: Writes explicit disqualifiers (a "not the ICP" section) — the firmographic/behavioural signals that predicted churn or loss
- [ ] PASS: Produces an actionable qualification checklist a team can apply to a new account
- [ ] PASS: Keeps the ICP account-level and states the boundary — individual-level profiles are the ux-researcher's persona work; ICP and persona compose
- [ ] PARTIAL: Dates the ICP and sets a review (PMF erodes; the ICP is re-derived as data changes)

## Output expectations

- [ ] PASS: Output file exists under `docs/product/` with an evidence-base table covering BOTH best-fit and worst-fit accounts
- [ ] PASS: Firmographic criteria are contrasted against the predicted-failure (worst-fit) values, not stated in isolation
- [ ] PASS: Behavioural criteria (trigger / activation / usage) appear and are framed as the stronger predictor than firmographics
- [ ] PASS: An explicit "not the ICP" disqualifiers section is present, drawn from the churned/lost accounts
- [ ] PASS: A qualification checklist is produced for scoring new accounts
- [ ] PASS: The output states the account-level vs person-level boundary and points individual-level work to ux-researcher persona-definition — it does NOT collapse ICP into a persona
- [ ] PARTIAL: The ICP is dated with a review set
