# Define Icp

Scenario: A PM defines an Ideal Customer Profile. The skill must build it from real data — best-fit AND churned/lost accounts (not wins only), extract firmographic criteria cross-checked against the worst-fit set, add the stronger behavioural criteria (trigger, activation, usage), write explicit disqualifiers, and produce a qualification checklist — keeping the ICP account-level and distinct from individual personas. Account data is staged as a fixture.

## Prompt

> Use the product-manager `define-icp` skill to define an Ideal Customer Profile for the reconciliation product.
> The account data is staged at `{workspace}/work/docs/product/accounts.md` (best-fit and churned/lost
> accounts) — read it first and derive the ICP from it. Write the ICP to a file under `docs/product/` in the
> current working directory, in the skill's standard format.
> 
> Proceed without asking — produce the ICP.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Done. I've written the ICP to `docs/product/icp-reconciliation.md` following all five steps.

**Key findings:**

1. **Firmographics**: 140–260 FTE in logistics/wholesale/distribution/construction, AU/NZ, on Xero/MYOB + payments stack
2. **Behavioural separator** (strongest signal): Best-fit accounts connected a data source AND invited 2+ team members in week 1; worst-fit did not
3. **Critical disqualifier**: Globex Retail had perfect firmographics but churned because only the admin activated — no team adoption = no value realization
4. **Trigger matters**: Accounts adopted on concrete events (audit flag, new hire, scaling past spreadsheets, switching competitors), not exploration

The qualification checklist is actionable for sales: six signals scored as Yes/No/Uncertain, with a 6-7/4-5/<4 scoring guide. The ICP is dated for review in six months.

### Artifacts written

#### `work/docs/product/icp-reconciliation.md`

```
# Ideal Customer Profile: Reconciliation

**Derived:** 2026-06-13 · **Next review:** 2026-12-13

## Evidence base

| Set | Accounts | Placing metric |
|-----|----------|----------------|
| Best fit | Northwind Logistics, Harbour Freight Co, Meridian Trades, Coastal Distribution | 18–36 mo retention; NPS 8–10; expansion (new seats / use cases) |
| Worst fit | Acme Consulting, Pixel Studio, Globex Retail, Initech SMB | Churn at 60–120 days; loss / downgrade |

## Firmographic criteria

| Dimension | ICP value | Predicted-failure value (worst fit) |
|-----------|-----------|-------------------------------------|
| **Industry** | Logistics, wholesale, distribution, construction | Professional services (Acme), creative agencies (Pixel), retail solo (Initech), UK-based (Pixel) |
| **Company size** | 140–260 FTE | <50 FTE (Pixel: 25 FTE, Initech: 18 FTE) — too small for team-based workflows |
| **Geography** | Australia, New Zealand | UK, US — likely timezone/regulatory mismatch; no local tax/payments context |
| **Tech stack** | Xero or MYOB + payment processor (Stripe/Shopify) | QuickBooks-only (Acme) or spreadsheets only (Pixel, Initech) — no modern data integrations |

**Key insight:** Globex Retail (230 FTE, AU, Xero+Stripe) matches best-fit firmographics exactly — yet churned at 4 months. Firmographics alone do not predict retention. Behavioural activation is the decisive separator.

## Behavioural criteria

| Signal | Best-fit behaviour | Worst-fit behaviour |
|--------|--------------------|--------------------|
| **Trigger** | Concrete, urgent business event (new finance hire overhauling process; audit flagged errors; scaling past spreadsheet capacity; replacing a competitor) | Vague or aspirational ("exploring tools", "curiosity") — no forcing function |
| **Week 1 activation** | Connected a data source (bank feed) AND invited 2+ users to platform within first 7 days | Failed one or both: no data source connection (Acme), or no second user invited (Globex Retail: admin only; Pixel: solo user) |
| **Usage pattern** | Regular (daily or weekly) reconciliation by 3–6 active users; sustained over 18+ months | Sporadic access (Pixel), single admin user (Globex), or light ad-hoc usage (Initech: 3 logins total) |
| **Team adoption** | Finance ops or accounting team, not just one person | Confined to admin or solo practitioner — no team accountability loop |

## Not the ICP (disqualifiers)

- **Very small teams** (<50 FTE): team-based reconciliation workflow doesn't exist yet; too small to absorb onboarding friction
- **Spreadsheet-only or QuickBooks-only tech stack**: no modern data source integrations; likely manual workflow entrenched; integration-averse
- **No concrete adoption trigger**: "exploring" or "trying it out" as the reason to adopt predicts churn; they lack urgency to push past week-one friction
- **Single-user activation in week 1**: if only the admin engages, the team never sees value; no second user = no usage momentum
- **Outside AU/NZ**: geographic mismatch; reconciliation involves tax, payments, and regulatory context (superannuation, GST, etc.) specific to ANZ
- **Enterprise with centralised procurement**: slow buying cycle and implementation burden not suited to a lean product

## Qualification checklist

Rate each signal: **Yes** (meets criteria) / **No** (disqualifies) / **Uncertain** (gather more data).

- [ ] **Size check**: 140–260 FTE (or strong evidence account has dedicated finance team with 2+ people)
- [ ] **Tech stack**: Xero or MYOB in active use + payment processor (Stripe/Shopify/Square) with accessible data feeds
- [ ] **Geography**: Australia or New Zealand (home market context: tax, payments, regulations)
- [ ] **Trigger identified**: Can you name a concrete business event prompting the search (scaling, audit flag, new hire, switching from competitor)?
- [ ] **Early activation signal**: Will the champion commit to connecting a data source in week 1 and inviting 2+ finance team members?
- [ ] **Team scope**: Is the finance team 2+ people who'll use the product regularly, or is it a one-person admin function?
- [ ] **Vertical signal**: Are they in logistics, wholesale, distribution, construction, or a neighbouring operations-heavy vertical?

**Scoring guide:**
- **6–7 Yes**: Strong ICP fit; prioritise for sales and onboarding
- **4–5 Yes**: Viable fit; qualify further before committing resources
- **<4 Yes**: Poor fit; high churn risk; escalate disqualifiers to the sales team

## Boundary

This is the **account-level** ICP. It describes which organisations get value from the reconciliation product and stay.

For **individual user profiles** within these accounts (the finance manager's goals, the bookkeeper's workflow, the audit requirements), refer to `/ux-researcher:persona-definition`. The ICP and personas compose: the account must match the ICP; the people within it must match personas.

---

### Related context

- **Best-fit behaviour**: The four best-fit accounts all exhibited data-source connection + team activation in week 1. This is the strongest predictor of retention and expansion.
- **Worst-fit pattern**: Two accounts (Globex Retail, Acme) matched firmographics or had clear triggers but failed on behavioural activation — they never got a team using the product.
- **Configuration opportunity**: If future roadmap work reduces week-1 onboarding friction (e.g. pre-seeded bank feed templates, team invite flows), this ICP may expand downmarket (smaller teams, other geos). Flag for review when that work lands.

```

#### `work/docs/product/accounts.md`

```
# Account data — reconciliation product

Two account sets pulled for ICP derivation: best-fit (strong retention/expansion/health) and worst-fit
(churned or lost). Behavioural fields drawn from product telemetry.

## Best-fit accounts

| Account | Industry | Size (FTE) | Geo | Tech stack | Trigger to adopt | Week-1 activation | Usage pattern | Retention / NPS |
|---------|----------|-----------|-----|-----------|------------------|-------------------|---------------|-----------------|
| Northwind Logistics | Logistics | 220 | AU | Xero + Stripe | New finance hire overhauling process | Connected bank feed + invited 3 users in 2 days | Daily reconciliation, 5 active users | 3 yrs, NPS 9, expanded |
| Harbour Freight Co | Wholesale | 180 | AU | Xero + Shopify | Audit flagged manual errors | Connected feed day 1, 4 users week 1 | Weekly close, 4 users | 2 yrs, NPS 10, expanded |
| Meridian Trades | Construction | 140 | NZ | MYOB + Stripe | Scaling past spreadsheet capacity | Feed + 2 users in week 1 | Daily, 3 users | 2 yrs, NPS 8 |
| Coastal Distribution | Distribution | 260 | AU | Xero + Stripe | Replacing a churned competitor | Feed + 5 users in 3 days | Daily, 6 users | 18 mo, NPS 9, expanded |

Best-fit cluster: AU/NZ wholesale/logistics/distribution/construction, 140-260 FTE, on Xero/MYOB + a payments
stack, adopting on a concrete trigger (new hire, audit, scaling, competitor switch). Behaviourally: connected
a data source AND invited 2+ users within week one, then used it at least weekly.

## Worst-fit accounts (churned or lost)

| Account | Industry | Size (FTE) | Geo | Tech stack | Trigger to adopt | Week-1 activation | Usage pattern | Outcome |
|---------|----------|-----------|-----|-----------|------------------|-------------------|---------------|---------|
| Acme Consulting | Professional services | 200 | AU | QuickBooks only | "Exploring tools" (no concrete trigger) | Never connected a data source | Admin logged in twice, then dark | Churned at 60 days |
| Pixel Studio | Creative agency | 25 | UK | Spreadsheets | Curiosity | Connected feed but never invited anyone | Solo, sporadic | Churned at 90 days |
| Globex Retail | Retail | 230 | AU | Xero + Stripe | New hire | Only admin activated; no second user | Single user, weekly | Churned at 4 mo ("couldn't get team on") |
| Initech SMB | Software | 18 | US | Spreadsheets | Found us via ad | No bank feed; manual CSV once | Logged in 3 times | Lost / downgraded |

Worst-fit signals: no concrete adoption trigger ("exploring"/"curiosity"); right-sized right-vertical
accounts (Globex: 230 FTE AU retail on Xero+Stripe — looks like a best-fit firmographically) that still
churned because only the admin activated and no second user was invited. Very small agencies/solo (Pixel,
Initech) and QuickBooks-only / spreadsheet-only stacks under-fit. The decisive separator is behavioural:
best-fit accounts connected a data source AND invited a second user in week one; worst-fit did not — even
when the firmographics matched.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.0/14.0 (100%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 45630 ms |
| Target cost | $0.0772 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Builds the ICP from real data — uses BOTH the best-fit accounts AND the churned/lost accounts, not wins only (avoids survivorship bias) | PASS | Evidence base table explicitly lists both sets: 'Best fit: Northwind Logistics, Harbour Freight Co, Meridian Trades, Coastal Distribution' and 'Worst fit: Acme Consulting, Pixel Studio, Globex Retail, Initech SMB'. |
| c2 | Extracts firmographic criteria (industry, size, geography, tech stack, buying structure) and cross-checks them against the worst-fit set | PASS | Firmographic criteria table has columns 'ICP value' and 'Predicted-failure value (worst fit)' covering Industry, Company size, Geography, and Tech stack. |
| c3 | Adds behavioural criteria — trigger, activation behaviour, usage pattern — drawn from the contrast between best-fit and churned accounts | PASS | Behavioural criteria table has rows for Trigger, Week 1 activation, Usage pattern, and Team adoption, each with 'Best-fit behaviour' vs 'Worst-fit behaviour' columns. |
| c4 | Treats behaviour as the STRONGER predictor — notes that right-size/right-vertical accounts still churned, so firmographics alone over-target | PASS | 'Key insight: Globex Retail (230 FTE, AU, Xero+Stripe) matches best-fit firmographics exactly — yet churned at 4 months. Firmographics alone do not predict retention. Behavioural activation is the decisive separator.' |
| c5 | Writes explicit disqualifiers (a "not the ICP" section) — the firmographic/behavioural signals that predicted churn or loss | PASS | 'Not the ICP (disqualifiers)' section has six bullet points: <50 FTE, spreadsheet-only/QuickBooks-only, no concrete trigger, single-user activation, outside AU/NZ, enterprise with centralised procurement. |
| c6 | Produces an actionable qualification checklist a team can apply to a new account | PASS | 'Qualification checklist' section has seven checkboxes (size, tech stack, geography, trigger, early activation, team scope, vertical) plus a scoring guide: 6–7 Yes / 4–5 Yes / <4 Yes. |
| c7 | Keeps the ICP account-level and states the boundary — individual-level profiles are the ux-researcher's persona work; ICP and persona compose | PASS | 'Boundary' section: 'This is the account-level ICP… For individual user profiles… refer to /ux-researcher:persona-definition. The ICP and personas compose: the account must match the ICP; the people within it must match personas.' |
| c8 | Dates the ICP and sets a review (PMF erodes; the ICP is re-derived as data changes) | PARTIAL | Document header: 'Derived: 2026-06-13 · Next review: 2026-12-13' — both derived date and review date present. |
| c9 | Output file exists under `docs/product/` with an evidence-base table covering BOTH best-fit and worst-fit accounts | PASS | File at `work/docs/product/icp-reconciliation.md` contains 'Evidence base' table with both Best fit and Worst fit rows listing all eight accounts. |
| c10 | Firmographic criteria are contrasted against the predicted-failure (worst-fit) values, not stated in isolation | PASS | Each firmographic row has a 'Predicted-failure value (worst fit)' column, e.g. size: '<50 FTE (Pixel: 25 FTE, Initech: 18 FTE) — too small for team-based workflows'. |
| c11 | Behavioural criteria (trigger / activation / usage) appear and are framed as the stronger predictor than firmographics | PASS | Behavioural criteria section present. Key insight explicitly frames behaviour as 'the decisive separator' over firmographics using the Globex Retail counter-example. |
| c12 | An explicit "not the ICP" disqualifiers section is present, drawn from the churned/lost accounts | PASS | 'Not the ICP (disqualifiers)' section directly references churned accounts: 'Acme', 'Globex', 'Pixel', 'Initech' patterns mapped to each disqualifier bullet. |
| c13 | A qualification checklist is produced for scoring new accounts | PASS | 'Qualification checklist' with seven checkboxes and a '6–7 Yes: Strong ICP fit / 4–5 Yes: Viable fit / <4 Yes: Poor fit' scoring guide. |
| c14 | The output states the account-level vs person-level boundary and points individual-level work to ux-researcher persona-definition — it does NOT collapse ICP into a persona | PASS | 'Boundary' section distinguishes account vs individual level, explicitly references '/ux-researcher:persona-definition', and states 'The ICP and personas compose'. |
| c15 | The ICP is dated with a review set | PARTIAL | Header line: 'Derived: 2026-06-13 · Next review: 2026-12-13' — six-month review window set. |

### Notes

The output is a near-perfect execution: all criteria met, firmographic table explicitly cross-references worst-fit values, the Globex Retail counter-example is used precisely to elevate behavioural criteria above firmographics, and the account/persona boundary is cleanly stated with a pointer to the ux-researcher skill. The two PARTIAL-ceiling criteria (dating/review) are fully satisfied within their caps.
