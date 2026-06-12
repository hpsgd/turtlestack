# Forecast With Reference Class

Scenario: A team has produced an optimistic bottoms-up estimate under stakeholder pressure. The delivery manager must build an outside-view reference class from comparable past deliveries, derive the median correction factor, apply it, and recommend committing to the reference-class forecast rather than the pressured number — presenting both figures and the gap between them.

## Prompt

> Use the delivery-manager `forecast-with-reference-class` skill to forecast the "payments rebuild". Write the
> forecast to `docs/delivery/forecast-payments-rebuild.md` relative to the current working directory. Respond in the
> skill's standard output format.
> 
> Facts:
> 
> - The team's bottoms-up estimate, given under pressure from the CPO to "hit 8 weeks", is 8 weeks.
> - Three comparable past rebuilds in this org, with their original estimates and actuals:
>   - Billing migration: estimated 8 weeks, actually took 13 weeks.
>   - Search rebuild: estimated 6 weeks, actually took 9 weeks.
>   - Notifications service: estimated 10 weeks, actually took 14 weeks.
> 
> Proceed without asking — build the reference class and produce the forecast.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

**Reference-Class Forecast: Payments Rebuild** written to `docs/delivery/forecast-payments-rebuild.md`.

**Key findings:**

| Field | Value |
|---|---|
| Team bottoms-up estimate | 8 weeks |
| Reference-class median ratio | 1.50 |
| **Reference-class forecast** | **12 weeks** |
| Optimism risk (team estimate) | HIGH |

The three comparable rebuilds show a consistent pattern: Billing migration (1.63×), Search rebuild (1.50×), Notifications service (1.40×). The median correction factor is 1.50. Applying this to the 8-week estimate, under pressure from the CPO, yields a 12-week forecast.

**Recommendation:** Commit to **12 weeks**. The team's bottoms-up estimate was made under stakeholder pressure—a condition that systematically inflates optimism. All three past deliveries overran; none came in at estimate or better. The 4-week gap between the estimate and the forecast represents the planning-fallacy correction. Executing against an 8-week commitment will likely surface a mid-execution schedule slip.

### Artifacts written

#### `work/docs/delivery/forecast-payments-rebuild.md`

```
## Reference-Class Forecast: Payments Rebuild

### Forecasting
| Field | Value |
|---|---|
| What is forecast | Payments rebuild delivery duration |
| Team bottoms-up estimate | 8 weeks |

### Reference class

| Past delivery | Estimate | Actual | Ratio |
|---|---|---|---|
| Billing migration | 8 weeks | 13 weeks | 1.63 |
| Search rebuild | 6 weeks | 9 weeks | 1.50 |
| Notifications service | 10 weeks | 14 weeks | 1.40 |

**Reference class analysis:**
- Median ratio: 1.50
- Reference-class forecast: **12 weeks**

### Recommendation

- **Commit to:** 12 weeks
- **Reasoning:** The three comparable rebuilds in this organisation show a consistent pattern: actual delivery takes 1.4–1.6× the original estimate. The median ratio of 1.50 is robust across the class. Applying this to the team's 8-week estimate yields a 12-week forecast. The team's bottoms-up estimate was given under stakeholder pressure to "hit 8 weeks" — a condition that systematically inflates optimism (planning fallacy). Historical actuals are more predictive than fresh estimates made under that pressure. The gap between 8 and 12 weeks represents the planning-fallacy correction.

- **Optimism risk if the team estimate is used instead:** **HIGH**
  - Committing to 8 weeks contradicts the reference class by 33% (4 weeks)
  - All three past deliveries overran. None came in at estimate or better.
  - The team's estimate was elicited under explicit CPO pressure to meet a timeline, not derived from independent technical assessment.
  - Executing against an 8-week commitment is likely to surface a 2–4 week schedule slip mid-execution, triggering reactive re-planning and scope cuts.

### Context

The bottoms-up estimate of 8 weeks reflects what the team believes is achievable, but is subject to the planning fallacy — the systematic tendency to underestimate effort, costs, and durations for tasks ahead, especially under stakeholder pressure. Reference-class forecasting corrects for this by grounding the forecast in what *actually happened* on comparable past work, not in a fresh estimate of this work.

**The finding:** This organisation's rebuild deliveries run 40–63% longer than estimated. The median correction factor is 1.50. Until there is evidence of a shift in estimation discipline, the 12-week forecast is the appropriate commitment, and the 8-week estimate should be explicitly flagged as the planning-fallacy risk when presented to steering or stakeholders.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 11.5/12.0 (96%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 21914 ms |
| Target cost | $0.0585 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Builds an outside-view reference class from the three comparable past deliveries — pulling each one's original estimate and actual outcome, not reasoning only from the current team's inside-view estimate | PASS | Reference-class table in file lists Billing migration (8w/13w), Search rebuild (6w/9w), Notifications service (10w/14w) — all three past deliveries with estimates and actuals. |
| c2 | Computes the actual/estimate ratio for each past delivery (≈1.63, 1.50, 1.40) and derives a correction factor — preferring the MEDIAN (≈1.50) for the small class rather than padding the estimate by an arbitrary buffer | PASS | Table shows Billing 1.63, Search 1.50, Notifications 1.40. File states 'Median ratio: 1.50' explicitly. |
| c3 | Applies the correction factor to the 8-week bottoms-up estimate to produce a reference-class forecast of roughly 12 weeks — derived from history, not from inflating the team number by a gut feel | PASS | File: 'Reference-class forecast: 12 weeks'; chat: '8 × 1.50 = 12 weeks' derivation stated explicitly. |
| c4 | Presents BOTH numbers — the 8-week bottoms-up estimate and the ~12-week reference-class forecast — and names the gap between them as the planning-fallacy correction | PASS | Chat response: 'The 4-week gap between the estimate and the forecast represents the planning-fallacy correction.' Both figures appear in file and chat. |
| c5 | Recommends committing to the reference-class forecast (~12 weeks), not the pressured 8-week number, with the reasoning visible — naming that committing to the optimistic figure embeds the planning fallacy | PASS | File: 'Commit to: 12 weeks'; recommendation section explicitly states '8-week estimate was given under stakeholder pressure' and 'planning-fallacy risk'. |
| c6 | Names the method as reference-class forecasting / the planning-fallacy correction (Kahneman/Lovallo via Flyvbjerg) rather than presenting it as a generic "add contingency" | PASS | File title 'Reference-Class Forecast'; context section uses 'reference-class forecasting' and 'planning fallacy' as named concepts, not generic contingency. |
| c7 | Notes that a reference class needs comparable deliveries (three to five is usable; one is an anecdote) and does not fabricate data to fill it | PARTIAL | No fabricated data; all three deliveries match the prompt. However, no explicit note about class-size adequacy ('three to five is usable; one is an anecdote') appears anywhere in file or chat. |
| c8 | A `docs/delivery/forecast-payments-rebuild.md` file is written with a reference-class table (past delivery / estimate / actual / ratio), a derived correction factor, and a recommendation | PASS | File written at `work/docs/delivery/forecast-payments-rebuild.md` containing the reference-class table, 'Median ratio: 1.50', and a Recommendation section. |
| c9 | The reference-class table shows all three past deliveries with their estimate, actual, and computed ratio | PASS | Table rows: Billing migration 8w/13w/1.63, Search rebuild 6w/9w/1.50, Notifications service 10w/14w/1.40 — all three with all four columns. |
| c10 | The median ratio (≈1.50) is stated and used, with a note that median is preferred over mean for the small class | PARTIAL | File states 'Median ratio: 1.50' and chat says 'robust across the class', but no explicit note explaining why median is preferred over mean for a small reference class. |
| c11 | Both the 8-week bottoms-up estimate and the ~12-week reference-class forecast appear, and the recommendation is to commit to ~12 weeks | PASS | File: 'Team bottoms-up estimate: 8 weeks', 'Reference-class forecast: 12 weeks', 'Commit to: 12 weeks'. |
| c12 | The recommendation explains the gap as the planning-fallacy correction and flags the optimism risk of using the 8-week estimate instead | PASS | File: 'Optimism risk if the team estimate is used instead: HIGH'; 'The gap between 8 and 12 weeks represents the planning-fallacy correction.' |
| c13 | The forecast is grounded in the outside-view history rather than an arbitrary buffer added to the team's number | PARTIAL | Context section: 'grounding the forecast in what actually happened on comparable past work, not in a fresh estimate of this work.' Derivation traced explicitly to historical ratios. |

### Notes

The output is strong across all core criteria — reference class built correctly, ratios computed accurately, median applied, both numbers presented, and the recommendation firmly names the planning fallacy. The only notable gap is c10: the median is used but no explicit rationale for preferring it over the mean for a small class is given.
