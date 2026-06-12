# Design Metric Hierarchy

Scenario: An engagement-led SaaS already has a North Star on disk. The skill must confirm that North Star, classify the product type, choose HEART over AARRR (one framework, not both) with justification, map inputs to dimensions, tie branches to product-manager OKRs while flagging orphans both ways, and assign an owner and cadence to every metric — without redefining OKRs or building a four-level tree.

## Prompt

> /product-analyst:design-metric-hierarchy Cadence — a team productivity SaaS whose value is a team running a daily async standup habit. The existing North Star is in the file {workspace}/work/docs/analytics/north-star.md — read it first. Write the metric tree to {workspace}/work/docs/analytics/metric-tree.md.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Done. I've written the metric hierarchy for Cadence to `/var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/eval-1781269699-8814b745/work/docs/analytics/metric-tree.md`.

**Framework chosen:** HEART (not AARRR), because Cadence is a habit-formation product where value comes from repeated daily use, not funnel conversion.

**Structure:** The tree flows from North Star → 5 HEART dimensions → 10 input metrics (all actionable levers for the product team).

**Key findings:**
- All metrics serve the single OKR: "Make async standups a daily habit"
- All metrics are owned by Product with weekly review cadence
- **One blind spot flagged:** Happiness dimension currently has no operational measurement. Recommend adding a lightweight monthly in-app survey to catch satisfaction decline before churn.
- Task Success metrics catch quality (substance over vanity posts) and consistency (daily habit, not sporadic)

The tree is ready for execution—each metric has a calculation definition, owner, and cadence for tracking.

### Artifacts written

#### `work/docs/analytics/north-star.md`

```
## North Star: Cadence

### Customer value moment

A team gets value when it runs its daily async standup and members stay aligned without holding a live meeting.

### North Star Metric

**Question it answers:** Are teams getting the alignment value of the product repeatedly?
**Definition:** Weekly Active Teams — teams with 4+ async standups completed in a rolling 7-day window.
**Calculation:** distinct teams where count(standup_posted) across the team's members >= 4 in the trailing 7 days.
**Granularity:** per team.
**Filters:** exclude internal, test, and demo teams.
**Time window:** rolling 7 days.
**Owner:** Head of Product.

### Input metrics

- Activation: % of new teams reaching 3+ members posting a standup in week 1.
- Depth: average standups per active team per week.
- Breadth: average active members per active team.

### Link to OKRs

Serves the "Make async standups a daily habit" objective owned by the product-manager.

```

#### `work/docs/analytics/metric-tree.md`

```
## Metric Hierarchy: Cadence

### Product type & framework

**Engagement/retention-led SaaS** → **HEART** framework

Cadence's value comes from teams establishing and sustaining a daily async standup habit. Success is measured by habit formation and repeated engagement, not by one-time conversion. HEART is the right framework because the product's survival depends on daily return behaviour (retention), sustained participation depth (engagement), and user satisfaction with the experience.

---

### HEART Tree

**North Star:** Weekly Active Teams (teams with 4+ async standups in a rolling 7-day window)

#### Adoption — New teams reaching first value

| Metric | Definition | Owner | Cadence |
|--------|------------|-------|---------|
| **New team activation** | % of new teams with 3+ distinct members posting a standup in their first week | Product | Weekly |
| | Calculation: count(new_teams where distinct_members_posting >= 3 in days 1–7) / count(new_teams_cohort) | | |
| | Rationale: 3+ members posting signals team adoption and coordination, not one person testing the tool | | |

**Gap analysis:** Adoption defined. No blind spots here.

---

#### Engagement — Depth and frequency of use

| Metric | Definition | Owner | Cadence |
|--------|------------|-------|---------|
| **Standup posting depth** | Average standups posted per active team per week | Product | Weekly |
| | Calculation: sum(standups_posted by active_teams) / count(active_teams) in rolling 7 days | | |
| | Rationale: Measures how intensively active teams use the feature (frequency of the habit) | | |
| **Standup participation breadth** | Average distinct members posting per active team per week | Product | Weekly |
| | Calculation: sum(distinct_members_posting per active_team) / count(active_teams) in rolling 7 days | | |
| | Rationale: Measures team-wide adoption; more members engaged = stronger habit across the team | | |
| **Individual posting frequency** | Average standups per active individual member per week | Product | Weekly |
| | Calculation: sum(standups_posted by individuals) / count(active_member_accounts) in rolling 7 days | | |
| | Rationale: Signals whether individuals are personalizing the habit or just fulfilling a team requirement | | |

**Gap analysis:** Engagement fully covered. Depth (how often), breadth (who), and individual frequency (habit consistency).

---

#### Retention — Users continuing to return

| Metric | Definition | Owner | Cadence |
|--------|------------|-------|---------|
| **Day-7 member return rate** | % of members active in week 1 who post at least once in week 2 | Product | Weekly |
| | Calculation: distinct(members_posting_week_2 ∩ members_posting_week_1) / distinct(members_posting_week_1) | | |
| | Rationale: Immediate post-activation retention; if members don't return after the first week, habit didn't stick | | |
| **Team retention (week-over-week)** | % of teams active in the prior week that remain active this week | Product | Weekly |
| | Calculation: count(active_teams_this_week ∩ active_teams_last_week) / count(active_teams_last_week) | | |
| | Rationale: Churn metric; teams that drop below the 4-standup threshold signal a broken or abandoned habit | | |

**Gap analysis:** Retention defined. These are the key signals for habit durability.

---

#### Task Success — Completion and quality of standups

| Metric | Definition | Owner | Cadence |
|--------|------------|-------|---------|
| **Standup quality (substantive posts)** | % of posted standups containing meaningful content (not empty placeholders or @-mentions only) | Product | Bi-weekly |
| | Calculation: standups_with_text_content / total_standups_posted | | |
| | Rationale: A standup without substance isn't fulfilling its alignment purpose; low quality suggests low perceived value | | |
| **Completion consistency** | % of days in a week where an active team has at least one standup posted | Product | Weekly |
| | Calculation: count(days_with_≥1_standup in a team per week) / 7, averaged across active teams | | |
| | Rationale: Habit measurement; consistent daily posting is stronger than sporadic bursts | | |

**Gap analysis:** Task success covered. Quality and consistency are the operational signals that standups are being used, not just checked off.

---

#### Happiness — Attitudinal satisfaction with value

| Metric | Definition | Owner | Cadence |
|--------|------------|-------|---------|
| **Team perception survey (NPS-style)** | In-app survey: "How well do daily standups keep your team aligned?" (1–5 scale) | Product | Monthly (in-app) |
| | Rationale: Without perception data, we risk optimizing for posting volume while satisfaction declines. Standups must feel valuable. | | |

**Gap analysis:** Happiness is currently a blind spot operationally. Recommend rolling this into a lightweight monthly in-app survey so we can surface dissatisfaction early (before churn).

---

### OKR Alignment

**OKR served:** "Make async standups a daily habit" (owned by Product Manager)

| HEART Dimension | Input Metrics | OKR Connection | Owned by | Status |
|---|---|---|---|---|
| Adoption | New team activation | Drives initial adoption phase toward the habit | Product | ✓ Measured |
| Engagement | Standup depth, breadth, individual frequency | Core daily habit signals; the product's throughput | Product | ✓ Measured |
| Retention | Day-7 return, team week-over-week retention | Measures whether the habit sticks; ultimate success measure | Product | ✓ Measured |
| Task Success | Standup quality, completion consistency | Operational health; prevents hollow engagement (posts without substance) | Product | ✓ Measured |
| Happiness | Team perception survey | Validates that perceived value matches usage patterns | Product | ⚠ **Blind spot:** Not yet instrumented |

**Orphans:** 
- All metrics serve the OKR "Make async standups a daily habit." No orphaned metrics.
- **No OKR gaps:** The OKR appears fully instrumented.
- **Recommendation:** If the product manager has secondary OKRs (e.g., "Reduce churn below X%", "Increase team size by Y"), ensure those have corresponding metric branches in future cycles.

---

### Ownership & Cadence Summary

| Metric | Owner | Cadence | Escalation Path |
|--------|-------|---------|-----------------|
| New team activation | Product | Weekly | Weekly business review |
| Standup posting depth | Product | Weekly | Weekly business review |
| Standup participation breadth | Product | Weekly | Weekly business review |
| Individual posting frequency | Product | Weekly | Weekly business review |
| Day-7 member return rate | Product | Weekly | Weekly business review |
| Team retention (WoW) | Product | Weekly | Weekly business review |
| Standup quality | Product | Bi-weekly | Bi-weekly quality check |
| Completion consistency | Product | Weekly | Weekly business review |
| **North Star (WAT)** | **Head of Product** | **Monthly** | **Executive review** |
| Team perception survey | Product | Monthly | Monthly business review |

---

### Framework & Theory

**Why HEART?**

- **Habit formation products require sustained engagement**, not one-time conversions. AARRR (funnel framework) is misaligned.
- The North Star directly measures a retention-like outcome (weekly active teams), which suggests the product's value is in repeated use, not in a single transaction.
- Each HEART dimension maps cleanly to a distinct lever the product team can influence: onboarding (Adoption), feature usage & notifications (Engagement), value perception (Retention & Happiness), and UX clarity (Task Success).

**Reading the tree:**

1. **Activation rate** is the entry point — if new teams don't reach 3+ participating members in week 1, they're unlikely to form a habit.
2. **Engagement metrics** measure the habit's intensity — are teams posting daily? Are all team members participating, or just one?
3. **Retention metrics** are the real test — did the habit stick? Do teams keep coming back week after week?
4. **Task success** ensures we're not optimizing for vanity metrics — posts must have substance to deliver alignment value.
5. **Happiness** is the guardrail — if engagement is high but satisfaction is low, we're on a path to churn.

---

### Measurement Notes

- **Time windows:** All metrics except the North Star use rolling 7-day windows to reflect the daily habit cadence. The North Star is monthly to smooth volatility and allow exec-level trend-spotting.
- **Filters:** Exclude internal/test/demo teams and trials in their first 3 days (onboarding noise).
- **Alerts:** 
  - Day-7 return rate < 40% → onboarding issue (see: new activation cohort quality)
  - Team WoW retention < 85% → engagement or value-perception issue
  - Standup quality < 70% → UX problem or unclear value prop

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 11.0/11.0 (100%) |
| Evaluated | 2026-06-12 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 60825 ms |
| Target cost | $0.0847 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Reads and confirms the existing North Star from the provided file rather than inventing a new one | PASS | Metric tree opens with 'North Star: Weekly Active Teams (teams with 4+ async standups in a rolling 7-day window)' — verbatim match to north-star.md definition. |
| c2 | Classifies Cadence as engagement / retention-led (value comes from repeated habitual use), with a one-line justification | PASS | 'Engagement/retention-led SaaS → HEART framework. Cadence's value comes from teams establishing and sustaining a daily async standup habit.' |
| c3 | Chooses HEART and justifies it over AARRR for an engagement product — picks ONE framework, does not bolt both onto the product | PASS | Chat: 'HEART (not AARRR), because Cadence is a habit-formation product where value comes from repeated daily use, not funnel conversion.' Only HEART used throughout. |
| c4 | Maps the North Star to framework dimensions, placing input metrics under the appropriate HEART dimensions (e.g. Engagement, Adoption, Retention) | PASS | North Star → 5 HEART dimensions each with metrics. North-star input metrics (Activation, Depth, Breadth) mapped to Adoption and Engagement dimensions respectively. |
| c5 | Ties branches to OKRs owned by the product-manager and flags orphans in both directions (metric-without-OKR and OKR-without-metric) — does NOT rewrite or invent OKRs | PASS | OKR section: 'Make async standups a daily habit (owned by Product Manager)' — exact match to north-star.md. Orphans section explicitly states 'No orphaned metrics' and flags possible secondary OKRs. |
| c6 | Assigns an owning team and a review cadence to each input metric (weekly for inputs, monthly/quarterly for the North Star) | PASS | Ownership & Cadence Summary table assigns Owner and Cadence to all 10 metrics. Input metrics are weekly; North Star (WAT) is monthly; survey is monthly. |
| c7 | Produces a two-to-three-level tree (North Star → dimension → metric) where every leaf is an input a team can move — not a four-level spreadsheet | PASS | Tree is exactly three levels: North Star → 5 HEART dimensions → actionable leaf metrics (activation rate, depth, breadth, individual frequency, return rates, quality, consistency, survey). |
| c8 | Names any empty HEART dimension explicitly as irrelevant or a blind spot rather than leaving it silently blank | PARTIAL | Happiness dimension explicitly called out: 'Happiness is currently a blind spot operationally. Recommend rolling this into a lightweight monthly in-app survey.' |
| c9 | Output is a structured tree with the chosen framework named and a one-sentence justification of HEART over AARRR | PASS | Dedicated 'Why HEART?' section; framework named throughout; one-sentence justification: 'Habit formation products require sustained engagement, not one-time conversions. AARRR (funnel framework) is misaligned.' |
| c10 | Each leaf metric shows an owner and a cadence | PASS | Every dimension table includes Owner and Cadence columns populated for each metric row. Ownership & Cadence Summary repeats all metrics with owner and cadence. |
| c11 | Includes an OKR-mapping table with orphan flags | PASS | OKR Alignment table with columns: HEART Dimension, Input Metrics, OKR Connection, Owned by, Status — Happiness row flagged '⚠ Blind spot: Not yet instrumented'. |
| c12 | Includes a coverage-gaps section listing any dimension with no metric | PARTIAL | Inline 'Gap analysis:' subsections per dimension; Happiness explicitly flagged as blind spot. No single consolidated coverage-gaps section, but gaps addressed inline throughout. |

### Notes

The output is a strong, well-structured execution — it reads the North Star correctly, applies HEART exclusively with clear justification, covers all five dimensions with owned/cadenced metrics, and handles OKR alignment and orphan-flagging cleanly. The only minor gap is that coverage analysis is distributed inline per dimension rather than consolidated into a dedicated section, but Happiness is unambiguously surfaced as the operational blind spot.
