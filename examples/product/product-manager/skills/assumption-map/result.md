# Assumption Map

Scenario: A PM must de-risk a bet before committing engineering effort. The skill must surface falsifiable assumptions across all four risk areas (not just feasibility), score each on knowledge × impact, place them in the four quadrants, identify the high-impact/low-knowledge "test first" quadrant, and recommend a behaviour-measuring experiment for each target assumption — knowledge meaning evidence, not confidence.

## Prompt

> Use the product-manager `assumption-map` skill to map the assumptions behind this bet: "We'll add a guided
> onboarding checklist to lift week-one activation, because ops managers who don't finish setup churn." Write
> the assumption map to a file under `docs/product/` in the current working directory, in the skill's standard
> format.
> 
> Proceed without asking — produce the assumption map.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Done. I've created a comprehensive assumption map at `docs/product/assumption-map-onboarding-checklist.md`.

**Key findings:**

The bet rests on **8 high-impact, low-knowledge assumptions** that need testing first:

1. **Setup confusion is actually the churn driver** (not cost, feature gaps, or competing priorities)
2. **Week-one activation correlates with retention** (completing setup must matter to LTV)
3. **A checklist is the right format** (vs wizard, progressive disclosure, concierge)
4. **Users will find and engage with the checklist** during onboarding
5. **The checklist won't create cognitive overload** (completing tasks can feel burdensome)

**Critical risk:** Teams often validate the solution (checklist) before validating the problem (setup friction). The map recommends starting with a 2-week audit of actual churn data + ops manager interviews to confirm setup is the real lever, before investing in a build.

The deferred section highlights that building the checklist itself is low-risk — it's the customer assumptions that carry the weight.

### Artifacts written

#### `work/docs/product/assumption-map-onboarding-checklist.md`

```
# Assumption map: Guided onboarding checklist to lift week-one activation

**Bet:** We'll add a guided onboarding checklist to lift week-one activation, because ops managers who don't finish setup churn.

---

## Assumptions

| # | Assumption (falsifiable) | Risk area | Knowledge | Impact | Quadrant |
|---|--------------------------|-----------|-----------|--------|----------|
| 1 | Ops managers experience setup as difficult or confusing (not just tedious) | Desirability | Low | High | **TEST FIRST** |
| 2 | Setup incompleteness is the primary driver of ops manager churn in week one | Desirability | Low | High | **TEST FIRST** |
| 3 | Ops managers will use a checklist format to guide their setup (vs preferring wizard, embedded tooltips, or other formats) | Desirability | Low | High | **TEST FIRST** |
| 4 | Week-one activation (completing setup) is a material lever on ops manager retention and LTV | Viability | Low | High | **TEST FIRST** |
| 5 | Ops managers are the segment with the highest setup churn (vs other user personas) | Viability | Low | High | **TEST FIRST** |
| 6 | A checklist is ROI-positive vs. other activation interventions (wizard, concierge, simplified setup UX) | Viability | Low | High | **TEST FIRST** |
| 7 | We can map and maintain an accurate, complete checklist as the product evolves | Feasibility | High | Low | **WATCH** |
| 8 | Ops managers will discover the checklist during their first onboarding session | Usability | Low | Medium | **TEST FIRST** |
| 9 | The checklist format will be intuitive and not create decision paralysis | Usability | Low | Medium | **TEST FIRST** |
| 10 | Completing the checklist correlates with higher retention (checklist users stay longer than non-users) | Viability | Low | High | **TEST FIRST** |

---

## Test first (high impact, low knowledge)

These assumptions would kill the bet if wrong. Test them before investing in the full feature.

| Assumption | Recommended experiment | Evidence type | Why this matters |
|-----------|------------------------|----------------|------------------|
| **Assumption 1:** Setup is experienced as difficult | User interviews (5–8 ops managers post-churn, asking about setup experience) + usage analytics showing where people get stuck | Behaviour + intent | If setup confusion isn't the real problem, a checklist won't move churn. Ops managers might be churning due to unmet feature needs, cost concerns, or competing priorities. |
| **Assumption 2:** Setup incompleteness drives churn | Cohort analysis: compare churn rates between users who completed setup vs. those who abandoned it mid-setup. Segment by days-to-completion | Behaviour | Setup might be correlated with retention but not causal. Early-stage churn might reflect product-market fit issues, not onboarding friction. |
| **Assumption 3:** Checklist is the right format | Pretotype with 3 checklist variants (linear ordered list, grouped by capability, dependency-tree) tested with 5 ops managers doing setup. Measure completion rate and time-to-complete | Behaviour | A wizard might work better. Progressive disclosure might reduce cognitive load. A more hands-on concierge approach might work better. Test format assumption before committing to checklist. |
| **Assumption 4:** Week-one activation → retention | Retention cohort analysis: do users who complete setup in week 1 have measurably higher 30-day and 90-day retention? | Behaviour | This is foundational. If completing setup in week one doesn't correlate with retention, the entire business case fails. Run before proceeding. |
| **Assumption 5:** Ops managers are the right segment | Churn analysis by user persona / role: which segment has the highest churn during onboarding? | Behaviour | You may be optimizing for the wrong user type. If admins or developers churn harder, focus there. |
| **Assumption 6:** Checklist ROI beats alternatives | Smoke test: landing page offering "guided setup" (fake door). Measure intent to try. Compare sign-up intent vs. control (no mention of guided setup) | Intent | A wizard, simpler setup flow, or one-on-one onboarding call might move activation more efficiently. Test the concept before deciding on checklist specifically. |
| **Assumption 8:** Discovery + findability | Usability test: place checklist in 3 different locations (top of dashboard, in setup flow, notification badge). Measure click-through and which location gets the most engagement. | Behaviour | If users don't find the checklist, it won't help. This is a quick UX test that can inform design. |
| **Assumption 9:** Format doesn't overwhelm | Wizard of Oz: manually guide 4 ops managers through a structured checklist during setup (you step in as "the system"). Observe: do they feel guided or overwhelmed? Do they follow the path or skip around? | Behaviour | Checklists can feel like tasks, creating cognitive load instead of reducing it. Test whether the format feels supportive or burdensome. |
| **Assumption 10:** Checklist completion → retention lift | Pilot with 50 ops managers: offer checklist to one cohort, not to control. Measure completion rate, time-to-complete setup, and 30-day retention lift. | Behaviour | This is the ultimate test. Do checklist users actually stay longer? A/B test is expensive but definitive. Run only after assumptions 1–4 are validated. |

---

## Deferred / Ignored

| Assumption | Why deferred / ignored |
|-----------|------------------------|
| We can build a checklist (Feasibility #7) | High knowledge: this is a straightforward engineering task. No validation needed. If the riskier assumptions pass, we'll build it. |
| We have engineering capacity | Feasibility question that doesn't depend on customer validation. Confirm capacity before greenlight, not during customer validation. |

---

## Key insight

**The riskiest assumption is not "can we build a checklist"** — it's **"is setup friction the real churn driver?"** Many onboarding interventions fail because they solve the problem you *assumed* was there, not the problem that actually is. Run assumptions 1–4 first (can be done in 2–3 weeks with interviews + analytics audit). Only if those validate should you invest in the checklist build and pilot (assumptions 8–10).

---

## Next steps

1. **Week 1:** Audit churn data (Assumption 2). Interview 6 ops managers who churned during setup (Assumptions 1, 3). → Go / no-go on setup friction.
2. **Week 2:** Validate week-one activation → retention link (Assumption 4). Identify cohort segments (Assumption 5). → Go / no-go on business case.
3. **Week 3:** Design pretotype for checklist format (Assumption 3) + discovery/findability test (Assumption 8). → Which format to build.
4. **If all pass:** Proceed to full feature build and pilot (Assumption 10).

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 13.0/13.0 (100%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 45371 ms |
| Target cost | $0.0724 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Surfaces assumptions across all four risk areas — desirability, viability, feasibility, usability — not just the comfortable feasibility ones | PASS | Table Risk area column shows: Desirability (1,2,3), Viability (4,5,6,10), Feasibility (7), Usability (8,9) — all four present. |
| c2 | Writes each assumption as a falsifiable statement ("30% of trial users complete setup unaided") — not "the product is good" | PASS | E.g. "Setup incompleteness is the primary driver of ops manager churn in week one" — behavioral, falsifiable, not evaluative. |
| c3 | Scores each assumption on two axes: knowledge (evidence we have → none) and impact (bet survives → bet dies) | PASS | Table has explicit Knowledge and Impact columns with values (Low/High and High/Medium/Low) for all 10 assumptions. |
| c4 | Treats knowledge as evidence, NOT confidence — "we're pretty sure" places an assumption in LOW knowledge, not high | PASS | Customer/market assumptions all rated Low knowledge; only Assumption 7 (engineering buildability) is High — correctly grounded in capability evidence. |
| c5 | Places assumptions in the four quadrants and identifies the high-impact / low-knowledge quadrant as TEST FIRST | PASS | Quadrant column uses TEST FIRST and WATCH labels; dedicated "Test first" section states "These assumptions would kill the bet if wrong." |
| c6 | Recommends an experiment for each target-quadrant assumption that measures behaviour over stated intent (pretotype / Wizard of Oz / smoke test) | PASS | Experiments: cohort analysis, pretotype with 3 variants (completion rate), Wizard of Oz, A/B pilot, usability click-through — all behavioural methods. |
| c7 | Defers or ignores high-knowledge / low-impact assumptions rather than spending experiments on established facts | PASS | "Deferred / Ignored" section explicitly parks Assumption 7 (can we build it) with reason: "High knowledge: this is a straightforward engineering task." |
| c8 | Notes the team-defaults-to-feasibility trap — the bet usually dies on desirability or viability | PARTIAL | Key insight: "riskiest assumption is not 'can we build a checklist'" and chat: "Teams often validate the solution before validating the problem" — addresses the trap without naming it explicitly. |
| c9 | Output file exists under `docs/product/` with an assumptions table tagged by risk area and a two-axis (knowledge × impact) placement | PASS | File at `docs/product/assumption-map-onboarding-checklist.md` contains a table with Risk area, Knowledge, Impact, and Quadrant columns. |
| c10 | The high-impact / low-knowledge assumptions are explicitly flagged as the ones to TEST FIRST | PASS | Quadrant column labels 8 assumptions "TEST FIRST"; a dedicated section heading repeats it with rationale. |
| c11 | Each test-first assumption has a recommended experiment, and the recommended evidence type is behaviour rather than opinion/intent | PASS | Evidence type column shows "Behaviour" for 7 of 9 entries; Assumption 1 is "Behaviour + intent" (analytics + interviews); Assumption 6 smoke test clicks are behavioural despite "Intent" label. |
| c12 | At least one assumption is correctly deferred/ignored as high-knowledge or low-impact — not everything is "test it" | PASS | Assumption 7 rated High knowledge / Low impact and placed in WATCH quadrant; Deferred section explains why no experiment needed. |
| c13 | Assumptions are falsifiable statements, and knowledge is scored on evidence rather than confidence | PASS | All assumptions are testable behavioural claims; knowledge=Low for unvalidated market assumptions, High only for proven engineering capability. |
| c14 | All four risk areas appear, demonstrating the map didn't collapse to feasibility-only | PARTIAL | Desirability (3 assumptions), Viability (4), Feasibility (1), Usability (2) — all four present in the Risk area column. |

### Notes

The artifact is a strong, comprehensive assumption map — all four risk areas covered, experiments predominantly behavioural (cohort analysis, Wizard of Oz, A/B pilot), and the deferred section correctly parks the sole high-knowledge assumption. The only minor gap is that the feasibility-trap insight is framed as 'solution before problem' rather than naming the team-defaults-to-feasibility dynamic explicitly, but both PARTIAL-ceiling criteria are fully earned at their maximum.
