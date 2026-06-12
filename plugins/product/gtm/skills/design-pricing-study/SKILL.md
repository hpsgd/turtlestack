---
name: design-pricing-study
description: "Design a willingness-to-pay or pricing research study — selects Van Westendorp, Gabor-Granger, conjoint, or MaxDiff based on the pricing question being asked, then produces the survey design (sample, questions, analysis plan). Use when you need evidence to inform a pricing or packaging decision. GTM owns pricing; the product-manager consults; a human approves the final price."
argument-hint: "[the pricing question, e.g. 'acceptable price band for the Pro tier']"
user-invocable: true
allowed-tools: Read, Write, Bash, Glob, Grep, WebSearch
---

# Design a pricing study

Design a pricing research study that answers the pricing question in $ARGUMENTS. The output is a survey design ready to field — not a price. You pick the right method for the question, then specify the sample, the instrument, and how the results will be analysed.

**Ownership boundary:** GTM owns pricing research and the pricing recommendation. The product-manager **consults** — they own packaging shape and feature-to-tier mapping, and their input shapes which attributes a study tests — but they do not own the price. The final pricing and packaging decision is a commercial call that **a human approves** (it is an explicit escalation checkpoint). This skill produces the evidence the human decides with; it never sets the price autonomously.

This skill pairs with `/gtm:competitor-price-benchmark` (market context for the price ranges you test) and `/gtm:positioning` (the value framing that anchors willingness to pay).

## Step 1 — Pin down the pricing question

You cannot pick a method until the question is precise. Force the question into one of four shapes:

| Question shape | Example | Method it points to |
|---|---|---|
| What price range is acceptable — where is too cheap / too expensive? | "What's the acceptable band for the Pro tier?" | Van Westendorp PSM |
| What price maximises revenue at a single price point? | "$49 or $59 for the standard plan?" | Gabor-Granger |
| How do buyers trade off price against features/packaging? | "Do they value SSO enough to pay $20 more?" | Conjoint analysis |
| Which features matter most when we can't show price? | "Rank these 10 features by importance for tiering" | MaxDiff |

Write the question as a single sentence with the decision it informs. If it doesn't fit one shape, it is two studies — split it.

## Step 2 — Select the method

Match the question to the method and record why. Link each method on first mention so the design is self-explanatory.

- **[Van Westendorp Price Sensitivity Meter](https://en.wikipedia.org/wiki/Van_Westendorp%27s_Price_Sensitivity_Meter)** — four questions (too cheap / cheap / expensive / too expensive). Produces an acceptable price range and the optimal price point (OPP). Use early, when you have no price and need a band. Weakness: measures stated perception, not purchase behaviour; no demand curve.
- **[Gabor-Granger](https://en.wikipedia.org/wiki/Gabor%E2%80%93Granger_method)** — ask purchase intent at a series of randomised price points. Produces a demand curve and revenue-maximising price. Use when you already have a candidate range and want to optimise within it. Weakness: tests prices in isolation, ignores competition and packaging.
- **[Conjoint analysis](https://en.wikipedia.org/wiki/Conjoint_analysis)** (choice-based) — respondents choose among product profiles that vary by feature and price. Produces part-worth utilities and price elasticity per feature; supports a market-simulator. Use for packaging and tiering decisions where price trades against features. Weakness: heavier to design, needs larger samples, longer survey.
- **[MaxDiff](https://en.wikipedia.org/wiki/MaxDiff)** (best-worst scaling) — respondents pick most/least important from sets of attributes. Produces a clean importance ranking. Use to decide which features belong in which tier before you attach prices. Weakness: ranks importance, says nothing about willingness to pay directly.

Record the choice:

```
Method: [chosen]
Because: [the question shape from Step 1 maps to this method]
Rejected: [other methods and the one-line reason each doesn't fit]
```

If two methods are genuinely needed (e.g. MaxDiff to set tier contents, then Van Westendorp to price each tier), state the sequence and treat them as a two-phase design.

## Step 3 — Define the sample

Specify who answers and how many. A pricing study fielded to the wrong audience produces a confidently wrong number.

| Parameter | Specify |
|---|---|
| Population | The ICP — actual or target buyers, not anyone. Screen out non-buyers. |
| Segments | Break out by segment (SMB / mid-market / enterprise). Price sensitivity differs sharply; never pool blindly. |
| Sample size | Van Westendorp / Gabor-Granger: ~150-300 per segment for stable curves. Conjoint: 300+ (more attributes need more respondents). MaxDiff: 200+. State the rationale, not just the number. |
| Screening | Qualify on relevant usage, budget authority, and category familiarity. |
| Source | Customer list, panel, or in-product intercept. Flag any paid panel as a cost to approve. |

Rules:

- Never field a single pooled sample across segments with different willingness to pay. Segment first, size per segment.
- Screen hard. A respondent who would never buy contaminates every price point.
- If a paid panel is in the path, flag the cost explicitly and offer the customer-list alternative — do not bury a subscription cost in the design.

## Step 4 — Build the instrument

Write the actual questions for the chosen method.

- **Van Westendorp:** the four price-perception questions, each referencing the same described product. Provide the product description shown to respondents.
- **Gabor-Granger:** the purchase-intent question plus the randomised price ladder (list the price points and the order-randomisation rule).
- **Conjoint:** the attribute-and-level table (including price as an attribute), the number of choice tasks, and one example choice set.
- **MaxDiff:** the attribute list, set size (typically 4-5 per screen), and number of screens.

Always include: a product/value description (so respondents price the same thing), and a small set of profile questions (segment, role, current spend) for cross-tabs.

## Step 5 — Specify the analysis plan

State how raw responses become a decision input before fielding — deciding analysis after seeing data invites cherry-picking.

| Method | Output | How computed |
|---|---|---|
| Van Westendorp | Acceptable range, OPP, indifference price | Intersection of the four cumulative curves |
| Gabor-Granger | Demand curve, revenue-max price | Intent × price across the ladder |
| Conjoint | Part-worth utilities, WTP per feature, share simulation | Hierarchical Bayes or logit estimation |
| MaxDiff | Importance scores, ranked attributes | Count or HB-estimated utilities |

Pre-register the cross-tabs (by segment, by current spend) and the decision rule ("we will recommend the OPP unless a segment band excludes it").

## Step 6 — Package for the decision-maker

Assemble the design into a fieldable brief and state the consult/approve chain explicitly.

## Rules

- Produce a study design, never a price. The price is the human's decision; this skill produces the evidence.
- State the ownership chain in every output: GTM owns the research, product-manager consults on packaging, a human approves the price.
- Method follows the question. Never default to Van Westendorp because it's familiar — match the four shapes in Step 1.
- Segment before sizing. Pooling segments with different price sensitivity is the most common pricing-study error.
- Pre-register the analysis plan. Deciding what counts as success after seeing the data is how studies lie.
- Flag any paid panel or research-tool subscription as a cost to approve, with a free or customer-list alternative offered.
- Stated willingness to pay overstates real willingness to pay. Note the bias and, where the stakes are high, recommend a behavioural follow-up (a real pricing page test) over the survey alone.
- **All output is DRAFT until human-reviewed.** Label every output "DRAFT — requires human review" at the top and bottom.

## Output Format

```markdown
# Pricing study design — [question] (DRAFT — requires human review)

**Ownership:** GTM owns this research. Product-manager consults on packaging. Final price approved by a human.
**Date:** [date]

## The question
[Single sentence + the decision it informs]

## Method selected
- Chosen: [method] — [why, mapped to question shape]
- Rejected: [methods + one-line reasons]
- Phasing: [single study / two-phase sequence]

## Sample
| Parameter | Value | Rationale |
|---|---|---|
[population, segments, size per segment, screening, source, cost flags]

## Instrument
[The actual questions for the method, plus product description and profile questions]

## Analysis plan (pre-registered)
[Outputs, computation, pre-registered cross-tabs, decision rule]

## Cost and approvals
[Panel/tool costs to approve; consult/approve chain]

DRAFT — requires human review
```

## Related Skills

- `/gtm:competitor-price-benchmark` — market price context that sets the realistic range to test.
- `/gtm:positioning` — the value framing that anchors willingness-to-pay perception.
- `/gtm:market-voc` — buyer price objections that signal where to focus the study.
