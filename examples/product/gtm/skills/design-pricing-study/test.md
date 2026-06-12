# Test: design-pricing-study picks the right method for the question and designs the survey

Scenario: GTM is asked to design pricing research for a question that is specifically about finding an
acceptable price band with no prior price anchor — the canonical Van Westendorp case. The skill must pin the
question to one of the four shapes, select Van Westendorp (and explicitly reject Gabor-Granger / conjoint /
MaxDiff with one-line reasons), then design the survey: segment-first sample with sized rationale, the actual
four price-perception questions plus a product description, and a pre-registered analysis plan. It must also
flag any paid research panel as a cost and offer a free / customer-list alternative (rewarded, not penalised),
hold the GTM-owns / product-manager-consults / human-approves chain, and never output a price.

## Prompt

Use the gtm `design-pricing-study` skill to design a pricing study for this question: we are about to launch a
new "Pro" tier for "Tideline" (an appointment-and-records product for small allied-health clinics) and we have
NO current price for it and no candidate price points yet — we need to find the acceptable price band: where
solo and small-clinic buyers would think it is too cheap to trust, and where it is too expensive to consider.
Segments are solo practitioners and small clinics (2-10 staff); price sensitivity differs between them.

Write the study-design artifact to `docs/gtm/pricing-study-pro-tier.md` (a relative path under the current
working directory). Respond in the skill's standard format. Proceed without asking.

## Criteria

- [ ] PASS: Pins the pricing question to one of the four shapes and states the decision it informs — recognises this is an "acceptable price range, no prior anchor" question
- [ ] PASS: Selects Van Westendorp PSM as the method, justified by the question shape (need a band, no existing price), NOT defaulted to out of familiarity
- [ ] PASS: Explicitly rejects the other three methods with a one-line reason each — Gabor-Granger (needs a candidate range already), conjoint (for feature/price trade-offs), MaxDiff (feature importance, not WTP)
- [ ] PASS: Designs a segment-first sample — solo vs small-clinic broken out, not pooled — and gives a sized rationale (e.g. ~150-300 per segment for stable Van Westendorp curves), not just a bare number
- [ ] PASS: Builds the instrument for Van Westendorp — the four price-perception questions (too cheap / cheap / expensive / too expensive) referencing a shown product/value description, plus profile questions for cross-tabs
- [ ] PASS: Specifies a pre-registered analysis plan — acceptable range / OPP from the intersection of cumulative curves, with cross-tabs by segment and a stated decision rule — registered BEFORE fielding
- [ ] PASS: Flags any paid research panel as a cost to approve AND offers a free / customer-list / in-product-intercept alternative (this is correct behaviour — reward it)
- [ ] PASS: Produces a study DESIGN, never a price — does not output a recommended dollar figure for the Pro tier
- [ ] PASS: States the ownership chain — GTM owns the research, product-manager consults on packaging, a human approves the final price
- [ ] PASS: Notes that stated willingness-to-pay overstates real willingness-to-pay, and (given the stakes) suggests a behavioural follow-up such as a real pricing-page test
- [ ] PASS: Labels the output DRAFT — requires human review
- [ ] PASS: Has valid YAML frontmatter (name, description, argument-hint)

## Output expectations

- [ ] PASS: Output writes the design to `docs/gtm/pricing-study-pro-tier.md` under the working directory
- [ ] PASS: Output's method section names Van Westendorp as chosen with a question-shape justification, and lists the three rejected methods each with a one-line reason — not a vague "we considered alternatives"
- [ ] PASS: Output's sample section breaks out solo vs small-clinic segments and sizes per segment with a rationale — does not pool them into one sample
- [ ] PASS: Output's instrument section contains the four actual Van Westendorp price-perception questions plus a product description shown to respondents
- [ ] PASS: Output's analysis plan is pre-registered (stated before fielding) with the computation method, segment cross-tabs, and a decision rule — not "we'll analyse after we see the data"
- [ ] PASS: Output flags the paid-panel cost with a free / customer-list alternative offered, and contains NO recommended price figure for the Pro tier
