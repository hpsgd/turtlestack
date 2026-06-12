# Cohort Analysis

Scenario: A retention table is provided where the blended curve flattens (looks like product-market fit) but one channel decays to near zero while another flattens high. The retention event in the data is the weak "opened the app," and no bot/internal exclusions have been applied. The skill must read the curve SHAPE as the verdict, benchmark it for a weekly SaaS, cut by channel to expose the divergence, flag the value-action problem, flag a correlation as not-causation, and require the missing exclusions.

## Prompt

> /product-analyst:cohort-analysis Cadence retention. A cohort retention table for the last six monthly signup cohorts, plus a breakout by acquisition channel, is in the file {workspace}/work/docs/analytics/retention-data.md — read it. Diagnose whether Cadence has product-market fit and where retention is strong versus bleeding. Write the analysis to {workspace}/work/docs/analytics/cohort-analysis.md.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Done. I've written a comprehensive cohort analysis to `docs/analytics/cohort-analysis.md`.

**Key findings:**

1. **Moderate fit, masked by channel:** Overall retention plateaus at 25–27%, which looks weak. But referral users plateau at 45% — strong fit. Paid social collapses to 2%. The product works; acquisition is targeting the wrong audience.

2. **Stable cohort pattern:** Jan, Feb, Mar all flatten to ~25–27%, proving this is structural, not a blip.

3. **Immediate action:** Pause paid social; double down on referral. The 22× divergence between channels is unsustainable.

4. **Diagnostic lead:** Calendar integration correlates with 2× better retention. Run an A/B test to see if it's causal — if it is, that's a retention lever to pull.

5. **Data quality flag:** Internal/test teams are included, which artificially inflates the numbers. Re-run on clean data before finalizing strategy.

The analysis ranks channels by fit and lays out next steps for acquisition (which channel to fund), product (what retention event to optimize for), and diagnostics (what cohort to profile).

### Artifacts written

#### `work/docs/analytics/retention-data.md`

```
# Cadence retention data

A team is counted as "retained" in a week if **any member opened the app** that week. Six monthly signup
cohorts are summarised below, plus a breakout by acquisition channel. Figures are the percentage of the original
signup cohort still retained in the given week.

## Overall (all channels combined)

| Cohort | W0 | W1 | W2 | W4 | W8 | W12 |
|---|---|---|---|---|---|---|
| Jan | 100% | 58% | 42% | 33% | 27% | 26% |
| Feb | 100% | 60% | 44% | 34% | 28% | 27% |
| Mar | 100% | 57% | 41% | 32% | 26% | 25% |

## By acquisition channel (single blended cohort, retention over weeks)

| Channel | W0 | W1 | W4 | W8 | W12 |
|---|---|---|---|---|---|
| Referral | 100% | 72% | 55% | 48% | 45% |
| Organic search | 100% | 60% | 38% | 30% | 28% |
| Paid social | 100% | 41% | 14% | 5% | 2% |

Notes:

- Figures include ALL signups. No exclusions have been applied for internal, test, or demo teams.
- The data team also observed that teams which connected a calendar integration in week 1 retain about 2x better
  at W12 than teams that did not.

```

#### `work/docs/analytics/cohort-analysis.md`

```
# Cohort Analysis: Cadence Retention

## Verdict

**Moderate product-market fit, with strong channel divergence.** All three signup cohorts flatten at ~25–27% retention — a stable plateau that proves core fit exists. However, the plateau is driven almost entirely by referral users (45% retention), while paid social is nearly dead (2% retention). Organic search sits between at 28%.

The flattening curve shape is healthy; the variation by channel suggests **acquisition strategy, not product quality, is the constraint.**

## Setup

- **Cohort dimension:** Signup month (Jan, Feb, Mar 2026)
- **Retention event:** "Any team member opened the app" in a given week (activity, not value action)
- **Retention definition:** Week-level point-in-time (team active in week W, not unbounded rolling)
- **Exclusions:** None applied — internal, test, and demo teams are included. This inflates retention slightly but should be re-run on clean data
- **Product type:** Team collaboration / calendar tool

## Retention table

### Overall retention (all channels combined)

| Cohort | W0 | W1 | W2 | W4 | W8 | W12 | Plateau |
|---|---|---|---|---|---|---|---|
| Jan | 100% | 58% | 42% | 33% | 27% | 26% | 26% |
| Feb | 100% | 60% | 44% | 34% | 28% | 27% | 27% |
| Mar | 100% | 57% | 41% | 32% | 26% | 25% | 25% |

**Curve shape:** Steep initial drop (W0→W1: –40–42%), then smooth deceleration flattening to ~25–27% by W8. Plateau is stable; no further decay from W8 to W12.

### Retention by acquisition channel

| Channel | W0 | W1 | W4 | W8 | W12 | Plateau |
|---|---|---|---|---|---|---|
| Referral | 100% | 72% | 55% | 48% | 45% | 45% |
| Organic search | 100% | 60% | 38% | 30% | 28% | 28% |
| Paid social | 100% | 41% | 14% | 5% | 2% | ~2% |

**Curve shapes:**
- **Referral:** Decays to 72% by W1, then slow decay to 45% plateau. Stable, high-fit curve.
- **Organic:** Decays steeply to 60% by W1, then gradual decay to 28% plateau. Moderate fit.
- **Paid social:** Catastrophic decay: 100% → 41% → 14% → 5% → 2%. No fit — users try the product, find no value, and leave.

## Curve read against benchmark

For a **weekly-use team collaboration tool**, healthy plateau is 30–50% of signups returning regularly.

| Segment | Plateau | vs Benchmark | Verdict |
|---|---|---|---|
| Overall | 25–27% | Below healthy range | Fit exists, but marginal |
| Referral | 45% | Within healthy range | Strong fit for this audience |
| Organic | 28% | Below healthy range | Weak but stable; possible long-tail effect |
| Paid social | 2% | Far below | No fit; unqualified traffic |

**Interpretation:** The overall plateau of 25–27% masks a winner (referral) and a catastrophic miss (paid social). Referral users are engaged because they came via peer endorsement—likely higher intent. Paid social users are cold traffic with mismatched expectations; the product is working fine for the right audience, but acquisition is targeting the wrong one.

## Segment cut: Retention divergence

**Strongest:** Referral channel at 45% W12 retention.  
**Weakest:** Paid social channel at 2% W12 retention.  
**Divergence factor:** 22.5×

This is a 22× difference in retention. The product is not the problem; the acquisition channel is. Referral users stick; paid social users do not.

## Signal: Calendar integration adoption

**Correlation observed:** Teams connecting a calendar integration in W1 retain ~2× better at W12.

- **Not causal yet** — teams that integrated are likely more engaged/serious from the start. This is selection bias, not proof that integration *causes* retention.
- **Strong lead to test:** Run an A/B experiment (nudge, gating, onboarding flow tweak) to see if driving earlier integration actually lifts retention. If calendar integration is the value action, making it more discoverable/frictionless could shift the overall plateau up.

## Next steps

### Immediate (acquisition)
1. **Pause or reduce paid social spend.** ROI is clearly broken — 2% retention is unsalvageable at any price.
2. **Double down on referral channels.** 45% retention justifies higher CAC and more referral incentive investment.
3. **Investigate organic search intent.** Organic sits at 28%, just above overall average. Is there a sub-segment (e.g., "team scheduling" vs "personal calendar") that performs better? Can content or SEO target higher-intent keywords?

### Diagnostic (product)
1. **Profile the retained 25%.** Who are the 25–27% that stick? Team size, domain, use frequency? This cohort is your product-market fit proof; understanding their profile could guide positioning.
2. **Audit the 75% that leaves (W1).** Why do 42–45% of new signups abandon by W1? Onboarding friction? Unclear value proposition? Unmet expectation?
3. **Test calendar integration causation.** Run A/B: (a) current onboarding, (b) nudge/enable calendar integration earlier. If it lifts W12 retention from 25% to 35%+, you've found a retention lever.

### Data quality
- **Exclude internal, test, demo teams** before re-running. These skew retention artificially high. A cleaner run may reveal the true plateau is lower — or higher if they're dragging the average down.
- **Define retention event more precisely.** "Opened the app" is activity, not necessarily value. If possible, re-segment by the value action (e.g., "scheduled a meeting," "shared a calendar," "accepted an invite"). The calendar integration finding suggests the value action is not mere login.

## Conclusion

Cadence has **proven product-market fit for a specific audience (referral, engaged teams)** but is **acquiring the wrong users at scale (paid social).** The product works; the acquisition strategy is broken. Fix acquisition first; then use the retained 25% to guide deeper product improvements.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 10.5/11.0 (96%) |
| Evaluated | 2026-06-12 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 46149 ms |
| Target cost | $0.0731 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Flags that the retention event should be the value action (a standup posted), and that the provided "opened the app" definition overstates retention — returning without getting value is not retention | PASS | Setup: 'Retention event: activity, not value action'. Data quality: 'Opened the app is activity, not necessarily value. Re-segment by value action (scheduled a meeting, shared a calendar, accepted an invite).' |
| c2 | States which retention definition (N-day / unbounded / bracket) fits Cadence's natural usage frequency, with a one-line reason | PARTIAL | Setup describes current definition as 'Week-level point-in-time (team active in week W, not unbounded rolling)' but never explicitly recommends which definition fits Cadence's natural cadence and why. |
| c3 | Reads the curve SHAPE as the verdict (flattens above zero = fit vs decays to zero = no fit) rather than reporting a single average retention number | PASS | Verdict: 'a stable plateau that proves core fit exists.' Per channel: 'Stable, high-fit curve' vs 'Catastrophic decay: 100%→41%→14%→5%→2%. No fit.' |
| c4 | Benchmarks the plateau against what is healthy for the product type (weekly SaaS) rather than an absolute target pulled from nowhere | PASS | 'For a weekly-use team collaboration tool, healthy plateau is 30–50% of signups returning regularly.' Referral rated 'Within healthy range'; overall rated 'Below healthy range'. |
| c5 | Cuts the cohorts by channel and names the strongest and weakest segments — surfacing the divergence the blended aggregate hides (referral flattens high; paid social decays to ~2%) | PASS | 'Strongest: Referral channel at 45% W12 retention. Weakest: Paid social channel at 2% W12 retention. Divergence factor: 22.5×' |
| c6 | Flags the "calendar integration in week 1 → 2x retention" finding as correlation, NOT causation, and routes it to an experiment to test | PASS | 'Not causal yet — teams that integrated are likely more engaged/serious from the start. This is selection bias.' And: 'Run an A/B experiment… to see if driving earlier integration actually lifts retention.' |
| c7 | Calls out that bots, test, and internal accounts have not been excluded and states they must be, since internal users retain near 100% and poison cohorts | PASS | Setup: 'None applied — internal, test, and demo teams are included. This inflates retention.' Data quality: 'Exclude internal, test, demo teams before re-running. These skew retention artificially high.' |
| c8 | Leads the write-up with the curve-shape verdict (the answer) before presenting the table | PARTIAL | Document opens with '## Verdict' section ('flatten at ~25–27% — a stable plateau that proves core fit exists') before any tables appear. Ceiling is PARTIAL. |
| c9 | Output opens with a verdict line stating product-market fit / no fit / improving, tied to the curve shape — not to a single number | PASS | First line: 'Moderate product-market fit, with strong channel divergence. All three signup cohorts flatten at ~25–27% retention — a stable plateau that proves core fit exists.' |
| c10 | Output includes a retention table or curve plus at least one segment cut | PASS | Full overall retention table (3 cohorts × 7 columns) plus channel breakout table (3 channels × 6 columns) both present in the artifact. |
| c11 | Output names the strongest and weakest channel segments with their retention figures | PASS | Explicit section: 'Strongest: Referral channel at 45% W12 retention. Weakest: Paid social channel at 2% W12 retention.' |
| c12 | Output includes a "next" section listing the correlations to test via experiment | PARTIAL | Next steps / Diagnostic section: 'Test calendar integration causation. Run A/B: (a) current onboarding, (b) nudge/enable calendar integration earlier.' Ceiling is PARTIAL. |

### Notes

The output is near-complete: curve-shape verdict, benchmark, channel divergence, correlation-vs-causation flag, and exclusion call-out are all present and well-executed. The only meaningful gap is c2 — the output describes the current bracket/week-level definition but never explicitly recommends which definition fits Cadence's natural usage cadence or gives a stated reason.
