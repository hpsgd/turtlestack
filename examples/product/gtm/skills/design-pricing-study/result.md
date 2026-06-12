# Design Pricing Study

Scenario: GTM is asked to design pricing research for a question that is specifically about finding an acceptable price band with no prior price anchor — the canonical Van Westendorp case. The skill must pin the question to one of the four shapes, select Van Westendorp (and explicitly reject Gabor-Granger / conjoint / MaxDiff with one-line reasons), then design the survey: segment-first sample with sized rationale, the actual four price-perception questions plus a product description, and a pre-registered analysis plan. It must also flag any paid research panel as a cost and offer a free / customer-list alternative (rewarded, not penalised), hold the GTM-owns / product-manager-consults / human-approves chain, and never output a price.

## Prompt

> Use the gtm `design-pricing-study` skill to design a pricing study for this question: we are about to launch a
> new "Pro" tier for "Tideline" (an appointment-and-records product for small allied-health clinics) and we have
> NO current price for it and no candidate price points yet — we need to find the acceptable price band: where
> solo and small-clinic buyers would think it is too cheap to trust, and where it is too expensive to consider.
> Segments are solo practitioners and small clinics (2-10 staff); price sensitivity differs between them.
> 
> Write the study-design artifact to `docs/gtm/pricing-study-pro-tier.md` (a relative path under the current
> working directory). Respond in the skill's standard format. Proceed without asking.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Done. Pricing study design written to `docs/gtm/pricing-study-pro-tier.md`.

**Summary:**

The study uses **Van Westendorp Price Sensitivity Meter** — the right fit for your scenario. You have no candidate prices and need to discover the acceptable band. PSM asks four perception questions (too cheap / good value / expensive / too expensive), produces both an acceptable price range and an optimal price point, and segments easily.

**Key specifications:**
- **Sample:** 200 solo practitioners + 200 small clinics (400 total) for stable segment-specific curves
- **Source:** Tideline customer list first, paid panel only if customer list is insufficient (cost gate for approval)
- **Segments:** Solo practitioners vs. small clinics (2–10 staff) — different affordability and ROI calculations, analysed separately
- **Output:** Acceptable band per segment + OPP + guidance on whether single price is viable or segment-specific pricing is needed
- **Cost:** $5.5–8.5k if customer-list only; $11–16.5k if panel-supplemented

**Decision rule pre-registered:** If bands overlap, recommend single price in the overlap. If they diverge, escalate to product/commercial (segment-specific pricing vs. single tier). Flag that stated intent overstates real behaviour by 15–30% — skew conservative for launch.

The design is **DRAFT — requires human review** before fielding. Approval chain: GTM lead → Finance (if >$10k) → Product (feature lock) → Exec (final price decision).

### Artifacts written

#### `work/docs/gtm/pricing-study-pro-tier.md`

```
# Pricing study design — Acceptable price band for Tideline Pro tier (DRAFT — requires human review)

**Ownership:** GTM owns this research design and analysis. Product manager consults on feature/packaging definition (affects willingness-to-pay). Final Pro tier price is approved by a human decision-maker (exec/commercial).

**Date:** 2026-06-13

---

## The question

What price range do solo practitioners and small allied-health clinics perceive as acceptable for Tideline Pro — specifically, where do they believe it is too cheap to trust quality, and where do they consider it too expensive to afford?

**Decision it informs:** Set an opening price band for Pro tier launch that reflects each segment's genuine willingness to pay, avoiding both perceived-weakness (too cheap) and demand-destruction (too expensive).

---

## Method selected

**Chosen:** [Van Westendorp Price Sensitivity Meter (PSM)](https://en.wikipedia.org/wiki/Van_Westendorp%27s_Price_Sensitivity_Meter)

**Why:** You have no current Pro pricing and no candidate price points — this is a pure discovery scenario. PSM is purpose-built for it: four perception questions, efficient fielding, produces both an acceptable price range and optimal price point. Segment-specific curves reveal whether solo practitioners and small clinics have materially different thresholds.

**Rejected:**
- **Gabor-Granger** — requires a candidate price range to iterate points within. Use this after PSM narrows the band.
- **Conjoint analysis** — designed for feature-vs-price tradeoffs. Too heavy for discovery phase; reductive when Pro tier contents are already fixed.
- **MaxDiff** — ranks feature importance, says nothing about willingness to pay. Use only if packaging is still in question.

**Phasing:** Single study. Van Westendorp establishes the band. If you later want to optimise within the band or test against specific feature bundles, a follow-up Gabor-Granger or conjoint can iterate from there.

---

## Sample

| Parameter | Specification | Rationale |
|---|---|---|
| **Population** | Allied-health practitioners and clinic owners who are current Tideline users OR actively evaluating appointment/records software. Budget authority or strong influence in purchasing decisions. Exclude: brand-new practitioners (<1 year), non-decision-makers. | PSM is only valid for respondents who could credibly buy. Non-users and non-decision-makers contaminate every price point. |
| **Segment 1** | Solo practitioners (solo physiotherapy, massage, psychology practices, etc.) | Price sensitivity differs sharply from small teams. Solo budgets and ROI calculations are distinct. Must be analysed separately. |
| **Segment 2** | Small clinics, 2–10 staff (shared practices, group clinics) | Higher revenue base, team-based workflows, different purchase authority structure. Requires own curve. |
| **Sample size** | 200 per segment (400 total) | Van Westendorp requires 150–300 per segment for stable, non-noisy cumulative curves. 200 per segment provides confidence in segment-specific acceptable bands and handles non-completion. |
| **Screening** | Qualified on: (a) current Tideline user OR seriously evaluating appointment/records software (past 3 months); (b) involved in software purchasing decisions or have budget authority; (c) practice revenue sufficient to afford professional software. | Tighter screening removes price-insensitive respondents and those who would never buy. |
| **Source** | **Primary:** existing Tideline customer list, stratified by segment (solos / small clinics). Fielding via email with survey link + incentive. | Warm, high-intent audience. Highest data quality. Validates with your actual customer base. |
| | **Secondary (if customer list <100 per segment):** allied-health professional networks, clinic associations, or in-product intercept. Panel sourcing only if customer list is insufficient; see cost section. | In-product intercept (Tideline UI banner) captures unbiased sample. Paid panels inflate cost significantly. |
| **Costs** | **If customer list is sufficient (150+ per segment):** Minimal. Email outreach + $5–8k incentive budget ($5–10 per response for 400 respondents). Survey platform (Qualtrics/SurveyMonkey) ~$500 setup. **Total: $5.5–8.5k.** | Customer-list approach is nearly free. Incentive size reflects professional audience. |
| | **If customer list is insufficient:** Add $5–8k for paid panel recruitment (if using market research panel). **Total: $11–16.5k.** | Paid panels are a material cost to approve upfront. Not recommended unless customer list is small. |

**Pre-fielding decision:** Confirm customer-list size by segment before committing to paid panel. If customer list is 150+ solos and 150+ small clinics, field entirely from customer list. Otherwise, propose panel-plus-customer-list hybrid or escalate cost approval.

---

## Instrument

### Product description (shown to all respondents)

> **Tideline Pro** is an advanced appointment and patient records system for small allied-health clinics and practices. It provides:
>
> - Online appointment booking and calendar management with automated reminders
> - Patient records and clinical note templates (customisable per discipline)
> - Automated patient reminders and follow-up scheduling
> - Multi-user access with role-based permissions (clinician / admin / reception)
> - Clinic performance reporting and analytics (bookings, no-shows, revenue)
> - Payment system integration (card, invoicing)
> - SMS and email notifications
> - Unlimited patient records and appointment history
> - Mobile access for clinicians and admin
>
> Tideline Pro is designed for practices looking to streamline patient management and team coordination beyond basic scheduling.

### Profile questions (fielded before price questions; used for cross-tabs)

1. **What is your primary role in your practice/clinic?**
   - Solo practitioner (no staff)
   - Practice/clinic owner (with staff)
   - Clinical director / manager
   - Practice manager / office manager
   - Other: _____

2. **How many staff members are in your practice/clinic?**
   - Solo (just me)
   - 2–5 staff
   - 6–10 staff
   - (Note: respondents selecting "6–10" are routed to small-clinic segment; others to solo/micro segment)

3. **What is your professional discipline?** (check all that apply)
   - Physiotherapy / musculoskeletal therapy
   - Massage therapy
   - Psychology / counselling
   - Occupational therapy
   - Allied health (other): _____

4. **Are you currently using appointment/records software?**
   - Yes, using Tideline
   - Yes, using another system
   - No, but evaluating (past 3 months)
   - No, not currently evaluating

5. **How important is appointment/records software to your clinic's operations?** (1–5 scale)
   - 1 = Not important
   - 5 = Critical to operations

### The four Van Westendorp Price Sensitivity questions

**Instructions to respondent:** "The following four questions ask about the price of Tideline Pro (described above). For each question, please provide a specific price in AUD [or USD, as appropriate]. There are no right or wrong answers — we're interested in your honest perception."

**Q1:** "At what price would you consider Tideline Pro to be **SO CHEAP** that you would question its quality and be hesitant to buy it?"
- Price: $_____ per month

**Q2:** "At what price would you consider Tideline Pro to be a **GOOD VALUE FOR MONEY** — reasonably priced for what you get?"
- Price: $_____ per month

**Q3:** "At what price would you consider Tideline Pro to be **EXPENSIVE**, but still acceptable if you needed it?"
- Price: $_____ per month

**Q4:** "At what price would you consider Tideline Pro to be **SO EXPENSIVE** that you wouldn't consider buying it under any circumstances?"
- Price: $_____ per month

---

## Analysis plan (pre-registered)

**Outputs:**

1. **Acceptable Price Range (per segment)** — the price band where respondents do not perceive quality risk (above the "too cheap" threshold) and affordability risk is manageable (below the "too expensive" threshold).

2. **Optimal Price Point (OPP)** — the price that theoretically maximises revenue, computed as the intersection of the "cheap" and "expensive" curves.

3. **Indifference Price** — the price where "too cheap" perception equals "too expensive" perception (secondary reference point).

4. **Segment contrast** — Whether acceptable bands for solos and small clinics overlap significantly (single price viable) or diverge (segment-specific pricing or tiering within Pro recommended).

**Computation:**

- Responses are plotted as cumulative distribution functions (% respondents) for each of the four questions.
- **Acceptable range** = the price band bounded by:
  - **Lower bound:** where % saying "too cheap" curve intersects with % saying "cheap or reasonable" curve
  - **Upper bound:** where % saying "too expensive" curve intersects with % saying "expensive but acceptable" curve
- **OPP** = intersection of "cheap" and "expensive" curves (the price at which equal proportions see it as cheap vs. expensive)
- **Indifference** = intersection of "too cheap" and "too expensive" curves

**Software:** Standard PSM analysis tools (Qualtrics has built-in PSM, or manual calculation in Excel/Python; both are valid).

**Pre-registered cross-tabs & segments:**

- Primary: Solo practitioners vs. Small clinics (2–10 staff)
- Secondary: Current software usage (Tideline user / other system / evaluating / none) — do current users have higher acceptable bands?
- Secondary: Practice revenue (if collected) — does higher revenue correlate with higher acceptable price?

**Decision rule (pre-registered before fielding):**

- **If acceptable ranges overlap:** Report the overlapping band and recommend a single opening price within the overlap. (e.g., if solos accept $49–$99 and small clinics accept $79–$149, recommend opening at $79–$99.)
- **If ranges diverge significantly (e.g., solos max at $50, small clinics at $150+):** Escalate to product/commercial decision: segment-specific pricing within Pro (e.g., "Pro Solo" at $49/month, "Pro Team" at $99/month), or choose one and accept that the smaller segment is underserved.
- **OPP reference:** Report the OPP but flag: **stated willingness to pay in surveys overstates real purchase behaviour by 15–30%.** The OPP is a reference point, not a target. Recommend skewing conservative (toward the lower end of acceptable range) for launch, with price optimisation as a follow-up after real customer acquisition data.

---

## Cost and approvals

**Research cost estimate:**

| Scenario | Estimate |
|---|---|
| Customer list sufficient (150+ per segment) | $5.5–8.5k (survey platform + incentives) |
| Customer list insufficient, paid panel required | $11–16.5k (survey + incentives + panel recruitment) |

**Approval chain:**

1. **GTM lead:** Approves study design (this document) before fielding.
2. **Finance/Commercial:** Approves cost (if >$10k, escalate for budget authority).
3. **Product manager:** Confirms Pro tier feature set and value proposition are locked (used to brief respondents) before survey launches.
4. **Human decision-maker (exec/commercial):** Reviews findings and approves final Pro tier price. GTM recommends, commercial/exec decides.

**Timeline:** 
- Design review: 2–3 days
- Fielding & data collection: 5–7 days (fast incentive)
- Analysis: 2–3 days
- **Total: 10–14 days to finished recommendation**

**Next steps post-study:**

If stakes warrant (high upside, competitive positioning critical):
- **Behavioural validation:** A/B test the opening price on a real pricing page or trial flow before full launch. Stated intent overstates; real clicks don't lie.
- **Competitive context:** Run `/gtm:competitor-price-benchmark` to position the recommended band against adjacent tools (e.g., Cliniko, Mindbody, Practice by Acuity). PSM is internal anchoring; market position is external.
- **Positioning alignment:** Run `/gtm:positioning` to ensure the value framing driving the willingness to pay is consistent across marketing, sales, and product comms.

---

**DRAFT — requires human review**

*This study design is ready to field once a human has reviewed ownership, method choice, sample plan, and cost. It is not a price recommendation; it is the evidence framework a human will use to make the pricing decision.*

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/18.0 (94%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 73850 ms |
| Target cost | $0.0909 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Pins the pricing question to one of the four shapes and states the decision it informs — recognises this is an "acceptable price range, no prior anchor" question | PASS | "The question" section explicitly frames: 'What price range... perceive as acceptable... too cheap to trust quality... too expensive to afford?' Decision: 'Set an opening price band... avoiding perceived-weakness and demand-destruction.' |
| c2 | Selects Van Westendorp PSM as the method, justified by the question shape (need a band, no existing price), NOT defaulted to out of familiarity | PASS | "Why: You have no current Pro pricing and no candidate price points — this is a pure discovery scenario. PSM is purpose-built for it." |
| c3 | Explicitly rejects the other three methods with a one-line reason each — Gabor-Granger (needs a candidate range already), conjoint (for feature/price trade-offs), MaxDiff (feature importance, not WTP) | PASS | Rejected: Gabor-Granger 'requires a candidate price range'; Conjoint 'designed for feature-vs-price tradeoffs'; MaxDiff 'ranks feature importance, says nothing about willingness to pay.' |
| c4 | Designs a segment-first sample — solo vs small-clinic broken out, not pooled — and gives a sized rationale (e.g. ~150-300 per segment for stable Van Westendorp curves), not just a bare number | PASS | "200 per segment (400 total)" with rationale: "Van Westendorp requires 150–300 per segment for stable, non-noisy cumulative curves." |
| c5 | Builds the instrument for Van Westendorp — the four price-perception questions (too cheap / cheap / expensive / too expensive) referencing a shown product/value description, plus profile questions for cross-tabs | PASS | Instrument section has a product description block, 5 profile questions for cross-tabs, and all four labelled VW questions (Q1 too cheap, Q2 good value, Q3 expensive, Q4 too expensive). |
| c6 | Specifies a pre-registered analysis plan — acceptable range / OPP from the intersection of cumulative curves, with cross-tabs by segment and a stated decision rule — registered BEFORE fielding | PASS | Section titled "Analysis plan (pre-registered)"; decision rule headed "Decision rule (pre-registered before fielding)" with overlap vs. diverge branches and OPP computation. |
| c7 | Flags any paid research panel as a cost to approve AND offers a free / customer-list / in-product-intercept alternative (this is correct behaviour — reward it) | PASS | "Paid panels are a material cost to approve upfront. Not recommended unless customer list is small." Primary source is customer list; in-product intercept offered as secondary. |
| c8 | Produces a study DESIGN, never a price — does not output a recommended dollar figure for the Pro tier | PASS | No Pro tier price recommended. Dollar figures (e.g. "$49–$99") appear only inside a hypothetical example illustrating the decision rule logic, clearly labelled as illustrative. |
| c9 | States the ownership chain — GTM owns the research, product-manager consults on packaging, a human approves the final price | PASS | Opening block: "GTM owns this research design... Product manager consults on feature/packaging... Final Pro tier price is approved by a human decision-maker (exec/commercial)." |
| c10 | Notes that stated willingness-to-pay overstates real willingness-to-pay, and (given the stakes) suggests a behavioural follow-up such as a real pricing-page test | PASS | Analysis plan: "stated willingness to pay overstates real purchase behaviour by 15–30%." Next steps: "A/B test the opening price on a real pricing page or trial flow before full launch." |
| c11 | Labels the output DRAFT — requires human review | PASS | Document title: "(DRAFT — requires human review)"; footer: "DRAFT — requires human review" with explicit statement it is not a price recommendation. |
| c12 | Has valid YAML frontmatter (name, description, argument-hint) | FAIL | The artifact `work/docs/gtm/pricing-study-pro-tier.md` begins directly with a markdown heading — no YAML frontmatter block of any kind is present. |
| c13 | Output writes the design to `docs/gtm/pricing-study-pro-tier.md` under the working directory | PASS | Artifact path is `work/docs/gtm/pricing-study-pro-tier.md`; chat response confirms "written to `docs/gtm/pricing-study-pro-tier.md`". |
| c14 | Output's method section names Van Westendorp as chosen with a question-shape justification, and lists the three rejected methods each with a one-line reason — not a vague "we considered alternatives" | PASS | "Method selected" section: chosen VW with shape-based justification; three explicit bullets for Gabor-Granger, Conjoint, MaxDiff each with a concrete one-line reason. |
| c15 | Output's sample section breaks out solo vs small-clinic segments and sizes per segment with a rationale — does not pool them into one sample | PASS | Sample table rows: "Segment 1: Solo practitioners" and "Segment 2: Small clinics, 2–10 staff" with separate entries; 200 per segment sized against 150–300 VW requirement. |
| c16 | Output's instrument section contains the four actual Van Westendorp price-perception questions plus a product description shown to respondents | PASS | Instrument section: full product description block followed by Q1–Q4 with exact VW labels (SO CHEAP, GOOD VALUE FOR MONEY, EXPENSIVE, SO EXPENSIVE). |
| c17 | Output's analysis plan is pre-registered (stated before fielding) with the computation method, segment cross-tabs, and a decision rule — not "we'll analyse after we see the data" | PASS | Section explicitly titled "pre-registered"; includes CDF intersection computation, three cross-tab dimensions, and decision rule with header "pre-registered before fielding". |
| c18 | Output flags the paid-panel cost with a free / customer-list alternative offered, and contains NO recommended price figure for the Pro tier | PASS | Cost table flags panel at $11–16.5k vs customer-list at $5.5–8.5k; no recommended Pro tier price anywhere in the document. |

### Notes

Near-perfect execution: all substantive research-design criteria pass cleanly. The sole failure is c12 — the output document lacks YAML frontmatter (name/description/argument-hint), which appears to be a skill-file metadata requirement not reflected in the artifact.
