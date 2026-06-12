# Design Experiment

Scenario: The only evidence for a proposed onboarding checklist is a survey of stated intent. The skill must place that evidence on the hierarchy and recommend a cheaper test before a full A/B, then still produce a rigorous design: one primary metric, the correct randomisation unit for a team-based product, a real sample-size calculation from the four supplied inputs, and a no-peeking stopping rule fixed before launch.

## Prompt

> /product-analyst:design-experiment We want to add a guided onboarding checklist to Cadence to lift week-1 activation. The only evidence so far is a survey where 68% of churned users said they "would have stayed if setup were easier." Current week-1 activation is 30%, the product-manager says the smallest lift worth shipping is 3 percentage points, and we get about 400 new teams per week. Write the experiment design to {workspace}/work/docs/analytics/experiment-design.md.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Done. I've written the experiment design to `docs/analytics/experiment-design.md`.

**Key takeaway**: Your survey evidence is **stated intent** (weak — what people say they'd do, not what they actually do), so I flagged two options: (1) run a cheaper fake-door test first to validate before engineering commits, or (2) if you're already building it, proceed with this full A/B. Either way, the design is solid.

**The math**: You need ~3,700 teams per variant to detect a 3pp lift with 80% power. At 400 new teams/week split 50-50, that's **18 weeks**. It's long, but it's the cost of detecting a modest effect at statistical rigor. I included a note on alternatives if timeline pressure is real (relax the MDE or use a holdout instead of A/B).

**Before launch**, lock in three things with your data engineer: (1) team-level randomization (not user-level — treatment leaks within teams), (2) the three activation milestones that define "activated", and (3) the guardrail dashboards (churn, errors, support tickets). No peeking before week 18.

### Artifacts written

#### `work/docs/analytics/experiment-design.md`

```
## Experiment Design: Guided Onboarding Checklist for Cadence

### Hypothesis
Because 68% of churned users said they would have stayed if setup were easier, we believe a guided onboarding checklist will increase week-1 activation by 3 percentage points for new teams.

### Prior evidence
**Stated intent** — Survey of churned users reporting hypothetical retention if setup improved. This is weak evidence per the hierarchy (stated intent is below observed behavior). Recommendation: This evidence alone doesn't justify committing full engineering resources yet. Consider running a cheaper validation first (fake-door test of the checklist concept with non-technical decision-makers, or a Figma walkthrough with 5–10 new teams) to confirm intent translates to action before building. If leadership has already committed to building, proceed with the full A/B as designed below, but flag that a 3pp lift is not guaranteed.

### Design
- **Type**: A/B test (concurrent control/treatment split)
- **Randomisation unit**: Team/Account (B2B; randomize by account to avoid treatment leakage within teams)
- **Primary metric (OEC)**: Week-1 activation rate — % of teams completing ≥3 of the key onboarding milestones (create first project, add team members, configure integrations, run first test) within 7 days of signup
- **Guardrails**:
  - Week-1 churn rate (% of teams with zero logins by day 7) — must not increase
  - Support ticket volume per new team — must not spike (early signal of confusion)
  - Onboarding error rate (% of teams encountering setup errors) — must not increase
- **Secondary**:
  - Checklist completion rate (% of treatment teams completing all steps)
  - Average time to first activation milestone
  - Day-1 activation rate (early engagement signal)
  - % of teams reaching each individual milestone

### Power
- **Baseline**: 30% | **MDE**: 3 percentage points | **α**: 0.05 | **Power**: 0.80
- **Sample per variant**: ~3,700 teams
- **Expected runtime**: 18 weeks (at 400 new teams/week split 50-50 into control/treatment = 200 teams/variant/week)

### Stopping & decision rules
- **Minimum runtime**: 2 weeks (must span at least one full Mon-Sun cycle in each variant to account for day-of-week effects)
- **Analysis approach**: Fixed horizon — launch, run for 18 weeks, analyze once. No peeking before week 18 to avoid inflating false-positive rate
- **Ship if**: Primary metric shows ≥3pp lift with 95% confidence (p < 0.05) AND all guardrails remain stable (no regressions)
- **Kill if**: After 18 weeks, no significant lift detected (p > 0.05) OR observed effect < 3pp OR guardrail breach (churn up, errors up, support tickets up)
- **Inconclusive if**: Significant effect detected but below MDE (e.g., 1.5pp lift, p < 0.05) — means the change works but isn't worth the cost; decide whether to iterate or shelve

### Hand-off
- **Data engineer** implements: team-level randomization on signup, assignment logging (control vs. treatment), activation-milestone tracking and pipeline, guardrail monitoring (churn, errors, support)
- **Product** defines the 3 activation milestones and configures which checklist items map to each
- **Analytics** sets up metric dashboards and pre-registers the decision rule before launch to lock in the ship/kill threshold

### Notes
- **Timeline risk**: 18 weeks is long; this assumes stable product and user base over 4.5 months. Flag if major features, pricing, or go-to-market changes are planned during the test window.
- **If runtime is unacceptable**: Consider either (1) relaxing the MDE to 4–5pp if smaller effects are less interesting to the business, or (2) increasing sample collection speed (e.g., accelerate new-team onboarding or run in parallel markets).
- **Staged rollout alternative**: If you want to ship faster and tolerate more risk, use a holdout design — roll out the checklist broadly, but keep a 10-20% holdout control cohort for measurement. This sacrifices some new teams' onboarding experience but gets you a result in weeks, not months. Trade the guaranteed 18-week timeline and high statistical rigor for faster business decision.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 11.0/11.0 (100%) |
| Evaluated | 2026-06-12 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 60954 ms |
| Target cost | $0.0868 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Writes a hypothesis that fills all five slots — reason, change, metric, expected direction and size, and segment | PASS | "Because 68% of churned users said they would have stayed if setup were easier, we believe a guided onboarding checklist will increase week-1 activation by 3 percentage points for new teams." |
| c2 | Places the prior evidence (a survey) on the evidence hierarchy and identifies it as stated intent (weak) — recommends a cheaper test (fake door / smoke test) before committing engineering to a full A/B | PASS | "Stated intent — ...weak evidence per the hierarchy...Consider running a cheaper validation first (fake-door test...or a Figma walkthrough with 5–10 new teams)" |
| c3 | Chooses an experiment type (A/B) and states the randomisation unit as team/account — and notes that randomising by user or session would leak treatment within a team | PASS | "Type: A/B test" and "Randomisation unit: Team/Account (B2B; randomize by account to avoid treatment leakage within teams)"; chat adds "not user-level — treatment leaks within teams" |
| c4 | Names exactly ONE primary metric (week-1 activation) plus guardrail metrics — not multiple primaries | PASS | "Primary metric (OEC): Week-1 activation rate" is singular; guardrails (churn rate, support tickets, error rate) and secondaries are separate sections. |
| c5 | Calculates the required sample size per variant from the four inputs (baseline 30%, MDE 3 percentage points, α 0.05, power 0.80) and converts it to an expected runtime using ~400 teams/week | PASS | "Baseline: 30% \| MDE: 3 percentage points \| α: 0.05 \| Power: 0.80 \| Sample per variant: ~3,700 teams \| Expected runtime: 18 weeks (at 400 new teams/week split 50-50)" |
| c6 | Sets a stopping rule that forbids early peeking (fixed horizon or an explicit sequential method) and a minimum runtime of at least one full business cycle | PASS | "Fixed horizon — launch, run for 18 weeks, analyze once. No peeking before week 18" and "Minimum runtime: 2 weeks (must span at least one full Mon-Sun cycle)" |
| c7 | States a ship / kill / inconclusive decision rule fixed before launch | PASS | Explicit "Ship if", "Kill if", and "Inconclusive if" sections present; hand-off section says "pre-registers the decision rule before launch to lock in the ship/kill threshold." |
| c8 | Notes that statistical significance is not the same as worth shipping — confirms the effect must clear the MDE that matters, not merely p < 0.05 | PARTIAL | "Inconclusive if: Significant effect detected but below MDE (e.g., 1.5pp lift, p < 0.05) — means the change works but isn't worth the cost" |
| c9 | The sample-size section shows the four inputs and a concrete per-variant n plus a runtime in days or weeks | PASS | Power section lists all four inputs inline, gives "~3,700 teams" per variant and "18 weeks" runtime explicitly. |
| c10 | The randomisation unit is team/account with the leakage reason stated | PASS | "Randomisation unit: Team/Account (B2B; randomize by account to avoid treatment leakage within teams)" |
| c11 | Hands off assignment and logging to the data-engineer | PASS | "Data engineer implements: team-level randomization on signup, assignment logging (control vs. treatment), activation-milestone tracking and pipeline, guardrail monitoring" |
| c12 | The hypothesis is a single sentence with all five slots visibly filled | PARTIAL | The hypothesis is one sentence covering all five slots: reason (68% survey), change (checklist), metric (week-1 activation), direction+size (increase 3pp), segment (new teams). |

### Notes

The output is exemplary — every required element is present and correctly structured in the written artifact. The chat summary reinforces key design decisions, and the document itself is complete with hypothesis, evidence critique, power calculation, fixed-horizon stopping rule, and tiered decision thresholds.
