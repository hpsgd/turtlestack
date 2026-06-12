# Write Roadmap

Scenario: A stakeholder hands the PM a dated feature list ("bulk import in Q2, SSO in Q3, mobile app in Q4") and asks for a roadmap. The skill must refuse the date-feature shape, anchor on desired outcomes with baseline → target, place items by how much is known (Now/Next/Later) with confidence decreasing left to right, keep solution ideas off the roadmap (they belong on the OST), and derive proposed product-level OKR input for the CPO/coordinator rather than authoring the OKR set.

## Prompt

> Use the product-manager `write-roadmap` skill to build a roadmap for the "onboarding" slice of an accounting
> SaaS. A stakeholder has asked for: "bulk import in Q2, SSO in Q3, a mobile app in Q4." Current data: 30% of
> new accounts import data in week one; week-one churn is 22%. Write the roadmap to a file under
> `docs/product/` in the current working directory, in the skill's standard format.
> 
> Proceed without asking — produce the roadmap.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Done. Roadmap written to `docs/product/roadmap-onboarding.md`.

The roadmap reframes the stakeholder's three dated feature asks (bulk import Q2, SSO Q3, mobile Q4) as **directional bets in the Later horizon**, and prioritizes **discovery in Now** to validate what's actually blocking the metrics. Key moves:

1. **Anchors on two outcomes** backed by the metrics you provided (import 30%→60%, churn 22%→10%)
2. **Now column** holds a discovery initiative — we have a problem signal but not root cause
3. **Next column** commits conditionally once discovery narrows the solution space
4. **Later column** names the stakeholder asks as bets: "if bulk import is the blocker, we build it; if it's auth or mobile, we pivot"
5. **OKR input** for the CPO to work with

This prevents the roadmap from becoming a timeline disguised as strategy, while still acknowledging the stakeholder's intuition that setup, auth, and mobile matter.

### Artifacts written

#### `work/docs/product/roadmap-onboarding.md`

```
# Roadmap: Onboarding

## Desired outcomes

| Outcome | Baseline | Target | Confidence (0-4) |
|---------|----------|--------|------------------|
| Increase week-one data import adoption | 30% | 60% | 3 |
| Reduce week-one churn | 22% | 10% | 3 |

## Now / Next / Later

### Now (active)
- **Validate import and churn friction drivers through customer research** — drives both outcomes — evidence: 30% import rate indicates 70% encounter a blocker; 22% week-one churn suggests multiple drop-off points (auth, setup, onboarding clarity); support tickets and session recordings pending analysis — confidence: 2

### Next (committing soon)
- **Reduce data setup friction** (bulk import, integrations, file format support, or import UX) — drives week-one import adoption from 30% baseline — evidence: discovery results will confirm whether setup complexity is the blocker — confidence: 2 (until validated)

### Later (directional bets)
- **Enterprise authentication (SSO)** — drives friction reduction and account retention — bet: assumes authentication complexity is material for target accounts and contributes to week-one churn
- **Mobile-first onboarding experience** — drives ongoing engagement and reduces "step away from desk" churn — bet: assumes mobile usability or device availability blocks engagement in week one

## Proposed product-level OKRs (input for CPO / coordinator)

**Objective:** Reduce onboarding friction and improve week-one adoption

- **KR1:** Week-one data import adoption from 30% to 60%
- **KR2:** Week-one churn rate from 22% to 10%

---

## Rationale

The stakeholder asks for bulk import (Q2), SSO (Q3), and mobile app (Q4). This roadmap repositions them as *outcome-driven bets* rather than dated feature commitments:

- We have a clear metric (30% importing, 22% churn), but we lack evidence of root cause. **Now prioritizes discovery**: are accounts bouncing because import is hard, auth is hard, the product doesn't work on mobile, or something else?
- The specific features (bulk import, SSO, mobile) are reasonable hypotheses—but they're hypotheses, not commitments.
- **Next holds the solution space open** until discovery narrows it. If bulk import is the blocker, we build it. If it's auth, we prioritize SSO. If it's mobile, we redirect.
- **Later explicitly names the bets** so stakeholders understand what we're saying "we think this matters, but we're not sure yet."

The roadmap succeeds when both KRs improve. The features are means to that end, not the end itself.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 11.0/13.0 (85%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 45983 ms |
| Target cost | $0.0756 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Refuses to produce a dated feature timeline — does NOT render "bulk import, Q2 / SSO, Q3 / mobile app, Q4" as the roadmap | PASS | Rationale section: "This roadmap repositions them as outcome-driven bets rather than dated feature commitments"; Q2/Q3/Q4 dates never appear in the roadmap body. |
| c2 | Anchors on one to three desired outcomes expressed as a metric moving from a baseline to a target (e.g. week-one import 30% → 60%), not as features | PASS | Desired outcomes table: "week-one data import adoption 30%→60%" and "week-one churn 22%→10%" both with confidence ratings. |
| c3 | Uses Now / Next / Later (or GIST) horizons placed by how much is known, not by calendar date | PASS | File contains "### Now (active)", "### Next (committing soon)", "### Later (directional bets)" sections with no calendar dates. |
| c4 | Confidence decreases left to right — Later items are explicit bets that may never happen, not certainties | PASS | Later items labeled "bet: assumes…" with no numeric confidence; Rationale: "we think this matters, but we're not sure yet." Direction is clear even if Now/Next share confidence 2. |
| c5 | Keeps solution ideas (e.g. "bulk import", "onboarding wizard") OFF the roadmap — roadmap items are outcomes/opportunities; solutions belong on the opportunity solution tree | FAIL | Next item parenthetically names "bulk import, integrations, file format support, or import UX"; Later items name "Enterprise authentication (SSO)" and "Mobile-first onboarding experience" — all solution-shaped. |
| c6 | Derives proposed product-level OKR input (Objective + KRs with baselines) marked as INPUT for the CPO/coordinator — does not author the company OKR set | PASS | Section heading: "## Proposed product-level OKRs (input for CPO / coordinator)" with Objective + KR1/KR2 including baselines. |
| c7 | Flags any item lacking a baseline or evidence as a discovery gap rather than placing it in Now | PASS | Now holds discovery initiative: "support tickets and session recordings pending analysis"; Next explicitly notes "confidence: 2 (until validated)". |
| c8 | Does not smuggle sprint-level backlog stories onto the roadmap — backlog is the product-owner's | PARTIAL | No user stories or sprint tasks appear in the file; all items are opportunity/outcome level. Ceiling capped at PARTIAL. |
| c9 | Output roadmap file exists under `docs/product/` with a desired-outcomes table (baseline → target) at the top, not a list of features with quarters | PASS | File written to `docs/product/roadmap-onboarding.md`; first section is "## Desired outcomes" table with baseline→target columns. |
| c10 | The Now / Next / Later sections contain outcomes/opportunities, each tied to a desired outcome — "bulk import in Q2" is reshaped into the behaviour-change it would drive | PASS | Next: "Reduce data setup friction — drives week-one import adoption from 30% baseline"; each item states which outcome it drives. |
| c11 | Output explicitly notes that confidence decreases across the horizons and that Later items are bets allowed to die | PASS | Rationale: "Later explicitly names the bets so stakeholders understand what we're saying 'we think this matters, but we're not sure yet.'" Later items use "bet:" label. |
| c12 | Output includes a proposed product-level OKR block (Objective + KRs with baselines) explicitly labelled as input for the CPO / coordinator, not an authored OKR set | PASS | "## Proposed product-level OKRs (input for CPO / coordinator)" with KR1: 30%→60% and KR2: 22%→10%. |
| c13 | Solution-shaped items are redirected to the opportunity solution tree rather than placed on the roadmap | FAIL | No mention of "opportunity solution tree" or OST anywhere in the file. Solution ideas (SSO, bulk import, mobile) remain on the roadmap without redirection. |
| c14 | Output flags the requested "mobile app" (no baseline/evidence) as a Later bet or a discovery gap, not a committed Now item | PARTIAL | Later: "Mobile-first onboarding experience — bet: assumes mobile usability or device availability blocks engagement in week one." Correctly in Later, not Now. |

### Notes

The roadmap correctly reframes the dated feature list into outcome-anchored Now/Next/Later horizons with OKR input labelled for the CPO. Its two failures are related: solution-shaped items (bulk import, SSO, mobile) appear parenthetically on the roadmap and no opportunity solution tree redirect is offered, which are the same gap from two angles.
