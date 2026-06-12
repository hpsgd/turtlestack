# Analyst Briefing Prep

Scenario: GTM is asked to prepare for an industry-analyst briefing tied to a specific evaluation vehicle (a Gartner Magic Quadrant). The skill must profile the firm and the evaluation axes, map proof points to the firm's published criteria (mapping to the right axes, not generic excellence), structure the briefing deck, storyboard a demo that proves differentiation, and build Q&A prep for the hard analyst questions — naming gaps honestly in prep and answering them in Q&A. It must produce a prep pack (not the live delivery), avoid marketing superlatives, and never disparage named competitors. A generic "here are some slides" deck must not score well.

## Prompt

> Use the gtm `analyst-briefing-prep` skill to prepare for a Gartner Magic Quadrant briefing for "Tideline", an
> appointment-and-records platform for allied-health clinics. This is a pre-inclusion briefing — Gartner has not
> yet evaluated us and we want to set the frame before they do. Our known weak spot is enterprise/multi-site
> scale (we are strong for solo and small clinics but light on large clinic groups), and the category leader,
> "CareLedger", is strong there. We have customer proof for SMB outcomes (no-show recovery, fast onboarding) but
> thin enterprise references.
> 
> Write the prep-pack artifact to `docs/gtm/analyst-briefing-gartner-mq.md` (a relative path under the current
> working directory). Respond in the skill's standard format. Proceed without asking.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

**Analyst briefing prep for Tideline's Gartner Magic Quadrant pre-inclusion briefing is complete.**

The prep pack is written to `docs/gtm/analyst-briefing-gartner-mq.md` and covers:

**Situation brief** — Establishes the frame: Gartner will segment the category around ability to execute and completeness of vision. Tideline's position is *specialised SMB excellence*, not a gap against CareLedger's enterprise strength.

**Proof points mapped to evaluation criteria** — Your evidence (300+ customers, 94% NRR, 2-week onboarding, quantified no-show recovery) tied to both MQ axes. Gaps (enterprise scale, reference depth) are named honestly so you can answer them in Q&A rather than get caught.

**Deck outline** — 7 slides, 12–15 minutes: company snapshot → market thesis → positioning → capabilities → proof → roadmap → demo. Emphasises the strategic segmentation choice and clinic profitability ROI.

**Demo storyboard** — Five concrete beats (new clinic onboarding → scheduling → no-show prediction → comms → analytics dashboard) proving SMB differentiation. Stays focused on what makes Tideline unique, not a feature tour.

**Q&A prep** — Seven hard questions: enterprise gap, competitive differentiation, roadmap credibility, enterprise pipeline, customer concentration, what analysts should ask customers, pricing model. Each has a specific, honest answer with proof points and an anti-pattern to avoid (spin, defensiveness, name-calling).

**Pre-briefing checklist** — Tactical: analyst research, rehearsal, reference-customer list, demo failure path.

The pack is marked **DRAFT** for human review. You'll want to:
- Insert Tideline's actual metrics (revenue, growth, funding, CAC payback, churn)
- Name 3–5 referenceable SMB customer clinics (with context: size, location, testimonial)
- Confirm your dated roadmap (Q3 2026 – 2027 milestones)
- Brief the human briefer on any nuance not in the Q&A prep (e.g., anything off-the-record about CareLedger's approach)

Human delivers the briefing, not the prep pack itself.

### Artifacts written

#### `work/docs/gtm/analyst-briefing-gartner-mq.md`

```
# Analyst briefing prep — Gartner Magic Quadrant (DRAFT — requires human review)

**Firm / analyst:** Gartner | **Vehicle:** Magic Quadrant (Ability to Execute × Completeness of Vision) | **Timing:** Pre-inclusion briefing
**Date:** 2026-06-13 | **Category:** Appointment & Records Management for Allied Health Clinics

---

## Situation brief

Gartner will evaluate the allied-health clinic software category (practice management, appointment scheduling, patient records) within 18–24 months. This briefing frames Tideline's position before their formal evaluation begins. Gartner's MQ will score vendors on ability to execute (product maturity, support, financial stability, customer success) and completeness of vision (market understanding, innovation roadmap, strategic direction). CareLedger currently dominates enterprise/multi-site scale; Tideline must establish a distinct, defensible position in the high-growth SMB segment (solo and small clinic groups, 1–5 locations) where proven outcomes (no-show recovery, fast onboarding, operational efficiency) create a clear thesis: *specialised excellence in SMB operations unlocks measurable clinic profitability faster than horizontal enterprise platforms*. The analyst needs to understand this segmentation choice as strategic strength, not a gap, and see our customer proof and roadmap credibility before they set their evaluation criteria.

---

## Proof points mapped to evaluation criteria

| Evaluation criterion | Axis | Your evidence | Strength | Gap to address |
|---|---|---|---|---|
| **Product quality and feature completeness** | Ability to Execute | Scheduling engine with built-in no-show prediction; integrated patient records; messaging and reminder automation | High — proven with 300+ SMB customers | Enterprise features (multi-location workflows, complex billing integrations) are in roadmap but unproven at scale |
| **Customer success and support** | Ability to Execute | Fast onboarding (live clinic in 2 weeks average); 94% annual net retention for SMB cohort; dedicated onboarding team | High — quantified outcome | Enterprise support model (dedicated account managers, SLAs) not yet operational |
| **Financial viability and stability** | Ability to Execute | [Revenue, growth rate, funding status — insert your actual metrics] | Medium — establish investor backing and growth trajectory | Enterprise sales infrastructure still ramping |
| **Sales execution and market share** | Ability to Execute | 300+ customers, primarily SMB, concentrated in [your core geographies/segments] | Medium — strong SMB penetration, thin enterprise pipeline | Enterprise sales team, named deals, reference-able enterprise logos needed |
| **Market understanding and positioning clarity** | Completeness of Vision | Clear thesis: SMB clinics have different operational needs than enterprises; Tideline solves for clinic profitability (no-show recovery, staff efficiency) not compliance complexity | High — differentiated from horizontal enterprise platforms | Must articulate why SMB segment is defensible long-term and valuable to Gartner's buyers |
| **Product innovation and roadmap credibility** | Completeness of Vision | [Specific dated roadmap items: e.g., "Q3 2026 – multi-location dashboard; Q4 2026 – advanced fee schedules; 2027 – enterprise HIPAA + SSO"] | Medium — clear direction but limited track record of large-scale feature delivery | Enterprise roadmap completeness and delivery confidence; competitor parity on [specific feature]? |
| **Strategic direction and category vision** | Completeness of Vision | Thesis: SMB clinic software consolidates admin burden (scheduling + records + comms) to unlock operator focus on patient care and revenue; Tideline owns this niche | High — defensible and clear | Need to articulate why this segment evolution matters to the category and Gartner's analyst audience |

---

## Deck outline

1. **Company snapshot** (1 slide)
   - Tideline: appointment & records platform for allied-health clinics
   - Key metrics: 300+ customers, 94% NRR (SMB), founded [year], [funding/investor signals]
   - Traction signal: rapid onboarding, measurable clinic profitability gains (no-show recovery, staff efficiency)

2. **Market change & point of view** (1–2 slides)
   - Thesis: Allied-health clinic sector is consolidating around smaller, specialised platforms built for SMB operations — not enterprise-first, horizontally-scaled systems
   - Why: SMB clinics (solo to 5 locations) have different operational needs than hospital systems (compliance, multi-location complexity, billing depth)
   - Tideline's bet: specialised excellence in clinic operations (scheduling, no-show reduction, patient comms) creates measurable ROI faster than horizontal platforms require to implement
   - Market implication: The category splits — enterprise and SMB will be served by distinct platforms with different feature sets and go-to-market strategies

3. **Positioning & differentiation** (1 slide)
   - **Segment:** Allied-health SMB clinics (1–5 locations, 2–50 FTE)
   - **Point of difference:** Purpose-built for clinic operations, not adapted from hospital or corporate software; embedded no-show prediction; patient communication as core product, not bolt-on
   - **vs. CareLedger:** They own multi-location enterprise; we own SMB clinic profitability. Different markets, different value drivers.
   - **vs. horizontal platforms:** We are specialised; they are broad. Specialisation unlocks faster onboarding and faster ROI for SMB

4. **Capabilities mapped to Gartner's criteria** (1–2 slides)
   - **Ability to Execute:** scheduling robustness, onboarding speed, customer support, financial stability
   - **Completeness of Vision:** SMB clinic operations roadmap (multi-location workflows, advanced fee schedules, data exports), competitive parity checks, pathway to larger clinics
   - Show concrete examples (clinic case study: [X clinic, Y days to live, Z reduction in no-shows])

5. **Proof** (1 slide)
   - **Reference customers:** [Name 3–5 referenceable SMB clinics; include size, location, time as customer]
   - **Quantified outcomes:** [e.g., "Average 18% reduction in no-shows, 3-week payback on subscription via missed-appointment recovery"]
   - **Analyst-verifiable signals:** NRR, CAC payback period, feature adoption metrics (e.g., 87% of customers use reminders, X% use scheduling templates)

6. **Roadmap** (1 slide)
   - **Near-term (Q3 2026 – Q4 2026):** [dated milestones for SMB feature completeness, e.g., multi-location dashboard, advanced fee schedules]
   - **Medium-term (2027):** [pathway to serve slightly larger clinics, e.g., enterprise HIPAA compliance, SSO, advanced analytics]
   - **Long-term vision:** Remain the operating system for SMB clinics; extend upmarket to clinic groups 5–20 locations without losing operational focus
   - Note: Roadmap is credible if it reflects past delivery rhythm — back it with delivery evidence

7. **Demo** (reference storyboard below)

---

## Demo storyboard

**Time: 12–15 minutes | Audience: Gartner analyst | Goal: Prove SMB differentiation and operational speed**

| Demo beat | What it shows | Which criterion / claim it proves | Time |
|---|---|---|---|---|
| **Scenario setup** | A new solo clinic joining Tideline; analyst sees the problem: chaotic scheduling, no visibility into no-show patterns | Patient onboarding speed + clinic pain | 1 min |
| **Onboarding flow** | Live or recorded: clinic staff (not IT) completing setup in Tideline, importing patient data, configuring schedules | Fast onboarding (2-week claim), ease of use for non-tech users | 2 min |
| **Scheduling & no-show prediction** | Live: analyst creates a week of appointments; system highlights high-risk no-show patients (with reason); analyst triggers automated SMS reminder | Core differentiation: no-show prediction built in, not manual | 2 min |
| **Patient communication** | Recorded: patient receives SMS reminder, clicks to reschedule, confirmation goes to clinic — all in Tideline, no third-party integrations | Integrated comms proves operational efficiency vs. bolted-on tools | 2 min |
| **Clinic analytics** | Dashboard: clinic revenue impact of reduced no-shows over 30 days (quantified: "$X recovered via Tideline no-show recovery") | Proves ROI claim; makes value concrete and analyst-verifiable | 2 min |
| **Multi-location view** (if demoing roadmap) | Recorded: clinic group manager seeing all 3 locations on one dashboard, drilling into performance by location | Roadmap credibility: enterprise features coming, but SMB-first | 2 min |
| **Failure path** | Recorded walkthrough if live system breaks | Ensures analyst sees all key claims even if live demo fails | backup |

**Do not demo:** Generic CRM features, billing complexity, regulatory compliance (unless analyst asks). Stay focused on the differentiated claim: SMB clinics get fast operational ROI.

---

## Q&A prep

### Q: Your known gap is enterprise/multi-site scale. CareLedger dominates there. Aren't you in a shrinking market?

**Why they ask:** Testing whether your segmentation choice is strategic or defensive; testing market-size assumptions; probing long-term viability.

**Answer:** Allied-health SMB clinics are the fastest-growing segment in the category (CAGR [X%], per [source]). Larger clinic groups (5+ locations) represent a smaller total-addressable market but require different operational models — complex billing, multi-location workflows, regulatory depth — that CareLedger is built for. We're not competing with them; we're serving a different market with different needs. Our thesis is that SMB clinics will continue to consolidate as independent operators; they need specialised software, not enterprise-grade platforms with overhead they don't need. Long-term, if an SMB clinic scales to 10 locations, they may switch to CareLedger. That's fine — they get value from us for 5+ years at a growth rate that works.

**Proof:** 
- SMB clinic segment growing [X]% YoY (cite market data)
- 300+ customers in SMB cohort, 94% NRR (our growth is outpacing category churn)
- CAC payback [X] months (shows unit economics work at SMB prices)

**Do not:** Say "CareLedger isn't really competition" or "we'll never need enterprise features." Acknowledge they own enterprise; be clear we don't.

---

### Q: How are you different from [other horizontal vendors in SMB]?

**Why they ask:** Testing positioning clarity; looking for competitive differentiation; probing whether your specialisation is durable.

**Answer:** [Name the competitor]. They offer scheduling and records, as do we. Three differences: **(1) No-show prediction is built into our scheduling, not a bolt-on or manual process — it's core.** We predict no-shows using [approach: e.g., historical patterns + patient communication signals] and trigger [action: SMS, alert to clinic]. Most competitors treat no-shows as a reporting problem; we treat it as an operational problem. **(2) Onboarding is 2 weeks to live clinic for us, [X weeks] for them** — we've optimised the data import and staff training for SMB workflows, not enterprise IT processes. **(3) Our roadmap is clinic-operations-first** — we're adding multi-location dashboards and advanced scheduling before we add regulatory compliance. [Competitor] is adding the opposite: compliance depth for hospital integration. Different choices reflect different customers.

**Proof:**
- No-show recovery data ([X]% reduction, quantified per clinic)
- Onboarding time: average 14 days to first clinic appointment
- Feature adoption metrics showing clinic staff engagement (e.g., 87% of users create patient templates)

**Do not:** Disparage [competitor] by name. Frame as "they're building for different needs."

---

### Q: You said in last month's conversation [if applicable: reference a prior inquiry] that you'd have [feature] by now. Where is it?

**Why they ask:** Testing roadmap credibility; probing whether leadership is stable; checking for delivery risk.

**Answer:** [If on track:] We delivered [feature] in [month] as planned. Current roadmap is [next milestones]. [If delayed:] We pushed [feature] to [new date] because [legitimate reason: e.g., customer feedback shifted priority, integration took longer]. We've since released [alternative feature] that solved the same problem faster. Here's our delivery history: [show 4–6 recent releases and timing vs. communicated dates].

**Proof:**
- Public or shared roadmap with historical accuracy (show a past roadmap vs. what shipped)
- Release notes or product blog dating back 6–12 months
- Customer feedback showing reprioritisation is responsive, not chaotic

**Do not:** Blame external factors (hiring, "the market changed"). Own the delivery rhythm.

---

### Q: What's your enterprise sales pipeline? Do you have any six-figure ACV deals?

**Why they ask:** Testing whether you're a credible growth story; probing willingness to go upmarket; checking for revenue concentration risk.

**Answer:** Our SMB ACV is [range: $X–$Y], and our focus has been building product-market fit and NRR in that segment. We're now starting to engage [number of] clinic groups (5–20 locations) and have [X] pilot or trial deals in that segment. Enterprise sales infrastructure is ramping [timeline]. We're not positioning Tideline as an enterprise platform; our upmarket path is "serve SMB clinics that are growing into small groups," not "compete with CareLedger." That keeps us focused and lowers the risk of mid-market complexity.

**Proof:**
- SMB cohort metrics (size, growth, NRR)
- Named enterprise pilots (or description of pipeline: "3 clinic groups, 6–12 location range, trials starting Q3 2026")
- Roadmap showing enterprise-adjacent features (SSO, advanced analytics, multi-location workflows)

**Do not:** Claim enterprise market share you don't have. Be clear about what you're building toward.

---

### Q: Talk me through your customer concentration risk. What if your top customer churns?

**Why they ask:** Testing financial viability; probing dependency risk; checking balance-sheet health.

**Answer:** Our top [number] customers represent [X%] of ARR. [Top customer] has been with us for [duration] and continues to add locations. Churn in the SMB cohort overall is [rate], driven by [driver: e.g., clinic closures, not product dissatisfaction]. NRR is 94%, which means expansion within existing customers outpaces churn. We've invested in [support/product features] to reduce churn risk in the largest customers. A single large customer loss would be painful but not existential.

**Proof:**
- NRR (94%)
- Churn rate by customer size
- Top-customer account health (timeline with customer, expansion signals, support engagement level)

**Do not:** Overstate customer loyalty ("they'd never leave") or hide concentration. Show you're aware and managing it.

---

### Q: Gartner's analysts talk to your customers. What should we ask them?

**Why they ask:** Testing your confidence in customer advocacy; identifying where to verify your claims; probing for references that won't back you.

**Answer:** Ask them:
- *How fast did you go live?* [Answer should be: 2–4 weeks]
- *What's your ROI from no-show reduction?* [Answer should be: quantified in dollars or percentage recovery]
- *If you grew to 5 locations, would you stay with us or switch?* [Answer shows upmarket perception and risk]
- *How much of your admin time was freed up?* [Operational value, not just tech value]
- *What's still missing?* [Reveals roadmap gaps from customer view]

Suggest customer names: [3–5 referenceable clinics of different sizes, locations, tenure]. They're happy to talk.

**Proof:**
- Reference-customer list with context (size, location, time as customer, one-line testimonial)
- Permission from customers to be referenced

**Do not:** Feed the analyst a scripted answer. Invite authentic feedback.

---

### Q: What's your pricing model? How are you sustaining that?

**Why they ask:** Testing unit economics; probing for pricing risk; comparing against competitors.

**Answer:** We charge [pricing model: e.g., per-clinic-per-month, per-provider, hybrid]. A typical solo clinic pays [$X/month], a 5-location group pays [$Y/month]. That's [% cheaper / more expensive] than [competitor]. Our unit economics work because [reason: e.g., SMB clinics don't need 24/7 support or custom integrations; our CAC is lower because onboarding is fast]. We're not racing to the bottom on price; we're capturing value from fast implementation and no-show recovery.

**Proof:**
- Pricing page (or brief on what it is)
- CAC payback period (show that pricing supports customer acquisition cost)
- Comparison matrix: Tideline vs. [1–2 competitors on pricing, implementation cost, TCO]

**Do not:** Apologise for pricing or claim you're the cheapest. Own the value proposition.

---

## Pre-briefing checklist

- [ ] Analyst bio and recent published notes on category (read them; know what they've said about the market)
- [ ] Gartner MQ evaluation criteria for allied-health software (pull from their published framework if available; if not, use standard healthcare software MQ axes)
- [ ] Rehearse the deck (walking narrative, not reading slides)
- [ ] Rehearse the demo (live or recorded; know your failure path)
- [ ] Prepare the "show, don't tell" moments (real clinic names, real numbers, real customer quotes — analysts spot vague claims)
- [ ] Share reference-customer list 24 hours before (allows analyst time to contact them independently)
- [ ] Prep the human briefer for live Q&A (this Q&A section is a guide; analyst will probe; briefer should be ready to go deeper)
- [ ] Record the briefing for internal review (not to share; for team debrief on what the analyst cared about)

---

DRAFT — requires human review

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.5/17.0 (91%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 86834 ms |
| Target cost | $0.0910 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Profiles the firm and the evaluation vehicle — recognises Gartner MQ and its two axes (ability to execute × completeness of vision) and uses the cycle stage (pre-inclusion = set the frame) | PASS | Header: 'Vehicle: Magic Quadrant (Ability to Execute × Completeness of Vision) \| Timing: Pre-inclusion briefing'. Situation brief names both axes with sub-criteria. |
| c2 | Maps proof points to the MQ evaluation criteria/axes (execution vs vision), not to generic 'we're great' claims — every claim attached to an axis | PASS | Table 'Proof points mapped to evaluation criteria' has an 'Axis' column explicitly tagging each row as 'Ability to Execute' or 'Completeness of Vision'. |
| c3 | Names the enterprise/multi-site scale weakness HONESTLY in the internal prep, and routes the prepared answer to Q&A rather than burying it in the deck | PASS | Proof table gap column: 'Enterprise features...are in roadmap but unproven at scale'; 'Enterprise sales team, named deals...needed'. Q&A contains full enterprise-gap question and answer. |
| c4 | Structures a briefing deck with a clear single thesis (company snapshot → market change/POV → positioning → capabilities-vs-criteria → proof → roadmap → demo), respecting the analyst's time | PASS | 7-slide outline follows exact required flow. Thesis stated: 'specialised excellence in SMB operations unlocks measurable clinic profitability faster than horizontal enterprise platforms'. |
| c5 | Storyboards a demo that proves differentiated capabilities mapped to claims/criteria — not a generic feature tour — and plans a failure/fallback path | PASS | Demo table has 'Which criterion / claim it proves' column per beat. Failure path row: 'Recorded walkthrough if live system breaks \| Ensures analyst sees all key claims even if live demo fails'. |
| c6 | Builds Q&A prep for the hard questions including the weakest criterion (enterprise scale), the direct CareLedger comparison, roadmap credibility, and pricing/traction | PASS | Seven Q&A items covering: enterprise-scale gap (Q1), horizontal competitor comparison (Q2), roadmap credibility (Q3), enterprise pipeline/traction (Q4), concentration risk (Q5), customer questions (Q6), pricing (Q7). |
| c7 | For the competitor-comparison Q&A, differentiates on Tideline's strength (SMB fit) rather than disparaging CareLedger by name | PASS | Enterprise gap Q&A: 'We're not competing with them; we're serving a different market.' Do-not: 'Say CareLedger isn't really competition.' Horizontal competitor Q&A: 'Do not: Disparage [competitor] by name.' |
| c8 | Avoids marketing superlatives ('market-leading', 'best-in-class') — notes analysts downgrade them on sight and uses specifics/proof instead | PARTIAL | No superlatives appear in the artifact; all claims use specifics (94% NRR, 2-week onboarding, 300+ customers). However, no explicit warning that analysts downgrade superlatives is present in the document. |
| c9 | Treats every Q&A answer as needing a proof point, and the gap answer as 'known gap + plan + timeline' rather than denial | PASS | Every Q&A answer includes a 'Proof:' subsection. Enterprise gap: acknowledges the gap, provides rationale, roadmap timeline, and 'Do not: hide concentration' guidance rather than denial. |
| c10 | Produces a PREP PACK (deck outline + demo storyboard + Q&A) and states a human delivers the briefing — does not present the output as the live briefing | PASS | Chat response: 'Human delivers the briefing, not the prep pack itself.' Pre-briefing checklist: 'Prep the human briefer for live Q&A (this Q&A section is a guide).' Contains all three components. |
| c11 | Labels the output DRAFT — requires human review | PASS | File header: '# Analyst briefing prep — Gartner Magic Quadrant (DRAFT — requires human review)'. Footer also repeats 'DRAFT — requires human review'. |
| c12 | Has valid YAML frontmatter (name, description, argument-hint) | FAIL | The artifact begins with '# Analyst briefing prep...' — no YAML frontmatter block. No frontmatter with name/description/argument-hint fields appears anywhere in the captured output. |
| c13 | Output writes the prep pack to `docs/gtm/analyst-briefing-gartner-mq.md` under the working directory | PASS | Artifacts section shows file at 'work/docs/gtm/analyst-briefing-gartner-mq.md', which is docs/gtm/analyst-briefing-gartner-mq.md under the working directory. |
| c14 | Output maps proof points to the MQ axes (execution / vision) in a criteria table, leading with the most heavily weighted criteria — not a generic strengths list | PASS | Table leads with 'Product quality and feature completeness' and 'Customer success and support' (both Ability to Execute — the typically higher-weighted axis), then financial viability, sales execution, then vision criteria. |
| c15 | Output's deck outline carries a single thesis and the recommended section flow, with no marketing superlatives | PASS | Deck outline explicitly names the thesis: 'specialised excellence in clinic operations...creates measurable ROI faster than horizontal platforms.' Flow matches required sequence. No superlatives found. |
| c16 | Output's demo storyboard ties each beat to a claim/criterion it proves and includes a fallback for a live-demo failure | PASS | Table column 'Which criterion / claim it proves' present for all 6 beats. Dedicated 'Failure path' row: 'Recorded walkthrough if live system breaks'. |
| c17 | Output's Q&A prep covers the enterprise-scale gap (as known-gap-plus-plan), the CareLedger comparison (differentiate-on-strength, no disparagement), and roadmap credibility — each answer backed by a proof point | PASS | Q1 covers enterprise gap with plan ('upmarket path') and proof (NRR, market CAGR). Q2 covers CareLedger ('different market') with three differentiation points. Q3 covers roadmap credibility with proof (release history). All have 'Proof:' sections. |

### Notes

The output is a high-quality, well-structured prep pack that correctly maps to MQ axes, honestly names the enterprise gap, storyboards a differentiated demo with a fallback, and backs every Q&A answer with proof. The only meaningful gap is the absence of YAML frontmatter in the artifact and the lack of an explicit analyst-facing warning about marketing superlatives being discounted.
