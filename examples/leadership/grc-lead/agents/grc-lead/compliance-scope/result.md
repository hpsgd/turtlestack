# Compliance Scope

Scenario: A user asks the GRC lead about compliance obligations for a new feature that will collect and process customer PII. Does the GRC lead identify the applicable frameworks, quantify the risks, and present a compliant path rather than just listing requirements?

## Prompt

> We're adding a "customer health score" feature to Meridian, our B2B CRM. It will pull together data from multiple sources: email open rates, support ticket history, login frequency, and payment history. The score will be calculated by an ML model and used by our customer success team to flag at-risk accounts. Our customers are businesses in Australia, the UK, and Germany. What do we need to know about compliance?
> 
> A few specifics for the response:
> 
> - **Risk Quantification table** — for each major risk, give explicit `Likelihood: LOW/MED/HIGH` and `Impact: LOW/MED/HIGH` ratings with a one-line rationale (e.g. "Likelihood: MEDIUM — opt-out rates from analytics suggest 5-10% will object; Impact: HIGH — automated decisioning without consent could trigger regulatory fines and account blocking"). Don't describe risks narratively.
> - **Lawful basis as a BLOCKING open question** per jurisdiction: present BOTH paths — (A) **Legitimate Interest** (Art 6(1)(f)) requiring a formal LIA, vs (B) **Consent** (Art 6(1)(a)) with explicit opt-in flow. State trade-offs of each and frame the choice as blocking — engineering cannot proceed without the call.
> - **Data minimisation analysis**: explicitly question whether ALL FOUR data sources (email open rates, support tickets, login frequency, payment history) are necessary. Propose the minimum subset that achieves the customer-success goal — e.g. "payment history may be excluded if churn signal is captured by support+login alone".
> - **Cross-border transfer**: Germany/UK data flowing to wherever the ML model trains/runs. If outside EU/UK, require Standard Contractual Clauses (SCCs) and a Transfer Impact Assessment (TIA). Name the safeguards.
> - **DPIA recommendation with skill handoff**: explicitly recommend `/grc-lead:write-dpia` as the next step (Article 35 mandates it for large-scale profiling combined with multiple data sources).
> - **GRC vs Engineering split**: explicitly delegate technical guardrails (input validation, audit logging, data deletion mechanisms, model explainability instrumentation) to the **security engineer / ML engineer**. Don't specify them yourself — just hand off.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

# Customer Health Score — Compliance Analysis

Jurisdictions in scope: **Australia** (Privacy Act 1988 + APPs), **UK** (UK GDPR + DPA 2018), **Germany** (EU GDPR + BDSG). The feature is **profiling** under GDPR Art 4(4) — combining behavioural, support, and financial signals to predict a business outcome (churn) — which engages the high-risk regime.

Note: data subjects are *individuals at customer businesses* (the user who opens the email, the user who logs in, the AP clerk who triggers payment). Even though customers are B2B, the inputs are personal data.

---

## 1. Risk Quantification

| # | Risk | Likelihood | Impact | Rationale |
|---|------|------------|--------|-----------|
| R1 | Profiling without a valid lawful basis (GDPR Art 6) | **HIGH** | **HIGH** | L: no basis selected yet — default state is non-compliant. I: EU/UK fines up to 4% global turnover; AU civil penalties up to AUD $50M under amended Privacy Act. |
| R2 | Automated decision-making engages GDPR Art 22 safeguards | **MED** | **HIGH** | L: depends on whether CS team treats score as advisory or actioned-without-review — drift toward "automated" is the default once volume grows. I: requires human-in-the-loop, explanation rights, contestation mechanism; retrofitting is expensive. |
| R3 | Failure to complete DPIA before processing begins (Art 35) | **HIGH** | **MED** | L: large-scale profiling + multi-source combination = DPIA mandatory; not yet started. I: supervisory authority can order processing to halt; evidence of non-compliance in any later investigation. |
| R4 | Cross-border transfer without SCCs/TIA (Ch V GDPR, UK IDTA) | **HIGH** | **HIGH** | L: ML training/inference location not yet decided — if any US/AU compute path exists, transfer occurs by default. I: BfDI (DE) and ICO (UK) have ordered transfer suspensions; Schrems II exposure. |
| R5 | Transparency failure — customers unaware of profiling (Art 13/14, APP 5) | **HIGH** | **MED** | L: existing privacy notices almost certainly don't describe profiling logic, sources, or consequences. I: complaints, regulator action, mandatory notice rewrite, possible re-consent across base. |
| R6 | Data subject rights gap — objection (Art 21), erasure (Art 17), access (Art 15) extended to model inputs/outputs | **MED** | **MED** | L: standard CRM DSAR processes don't typically cover model features or score history. I: 30-day response deadlines, regulator complaints from refused requests. |
| R7 | German BDSG §26 / works council issues if any customer's *employees* are scored | **MED** | **MED** | L: email opens and logins by named employees of a German customer can implicate that customer's co-determination obligations toward their staff. I: contractual indemnity claims from customers, reputational damage. |
| R8 | Discrimination / unfair outcomes against protected groups via proxy features | **MED** | **HIGH** | L: payment history and support volume correlate with company size, region, language — proxy risk is real. I: bias claim, regulatory scrutiny under emerging AI rules (EU AI Act high-risk classification possible). |
| R9 | AU Privacy Act amendments — statutory tort for serious invasions of privacy (commenced 2025) | **MED** | **MED** | L: profiling without notice is a documented tort risk vector. I: individual civil actions, class action exposure. |
| R10 | Security breach exposing combined profile (NDB scheme AU; Art 33/34 EU/UK) | **LOW** | **HIGH** | L: assumes baseline controls. I: combined dataset is more sensitive than parts — notification thresholds easily met. |

---

## 2. Lawful Basis — BLOCKING Open Question

Engineering cannot proceed until product/legal picks a path **per jurisdiction**. Both options are viable in principle; the trade-offs differ.

### Path A — Legitimate Interest (GDPR Art 6(1)(f) / UK GDPR / "reasonable expectations" analogy for AU APP 6)

- **Requires:** formal Legitimate Interests Assessment (LIA) — purpose test, necessity test, balancing test — documented and signed off before processing.
- **Pros:** no opt-in friction; covers existing customer base without re-papering; allows the CS team to operate at full coverage.
- **Cons:** balancing test is harder when profiling is involved (recital 47 GDPR explicitly flags profiling as a case where DS interests may override); Art 21 right to object is **absolute** for direct-marketing-adjacent uses and strong for others — must build objection handling; supervisory authorities (esp. BfDI in DE) scrutinise LI for profiling more heavily.
- **Germany-specific:** BfDI has historically taken a narrow view of LI for behavioural profiling; expect challenge.

### Path B — Explicit Consent (GDPR Art 6(1)(a) / APP 3 collection notice + consent)

- **Requires:** opt-in flow, granular (separate from T&Cs), revocable, demonstrably freely given. Consent records retained.
- **Pros:** cleanest legal basis; aligns with transparency obligations; defensible in DE.
- **Cons:** opt-out rates will reduce coverage (commonly 20–40% for non-essential profiling); re-consent campaign needed for existing base; revocation must propagate to model — score must be deletable on withdrawal; questions about whether consent is "freely given" when the data subject is an employee of the customer (power imbalance argument).

### Why this is blocking

The choice determines: (a) what the UX must contain, (b) what the privacy notice says, (c) whether you need consent-state storage and revocation plumbing, (d) which DPIA mitigations apply, (e) whether the DE rollout differs from UK/AU. None of those can be built speculatively.

**Recommendation to put to product/legal:** mixed path — **Consent in DE**, **LI + LIA in UK**, **notification + opt-out under APP 6 in AU** — but the call is not mine to make.

---

## 3. Data Minimisation Analysis

GDPR Art 5(1)(c) and APP 3.1 require data to be limited to what is *necessary*. "We have it, so we'll use it" is not lawful. Each source must be justified independently.

| Source | Necessary? | Justification needed | Comment |
|---|---|---|---|
| Login frequency | **Likely yes** | Direct engagement signal; strong churn predictor in most B2B SaaS. | Strongest single signal — most models can carry the load with this + support. |
| Support ticket history | **Likely yes** | Tickets (volume, sentiment, resolution time) are well-established at-risk indicators. | PII-light if reduced to counts/categories rather than ticket bodies. |
| Email open rates | **Question** | Often redundant with login frequency; opens are noisy (pixel blocking, MS Defender pre-fetch inflate them). | Propose: include only if model evaluation shows incremental AUC vs login+support baseline. Otherwise drop. |
| Payment history | **Question** | Financial data has heightened sensitivity perception and is often a *lagging* indicator of churn, not leading. | Propose: exclude from v1. If support+login captures churn signal sufficiently, the marginal lift isn't worth the regulator/customer-trust cost. Reintroduce later with explicit justification if v1 underperforms. |

**Proposed minimum viable feature set:** login frequency + support ticket metadata. Add email opens only if measurably useful; defer payment history to v2 pending evidence. Document the rationale — minimisation decisions are auditable.

---

## 4. Cross-Border Transfers

UK and Germany data leaving the UK/EEA requires Chapter V safeguards. AU data leaving Australia requires APP 8 compliance.

**Required regardless of destination decision:**
- **Map the data flow.** Where does training data sit? Where does inference run? Where are model artifacts stored? Where do logs go? Each hop is a potential transfer.
- **If any leg is outside UK/EEA** (e.g. US-hosted model API, AU-hosted compute, Anthropic/OpenAI inference):
  - **EU → 3rd country:** EU SCCs (2021 modules — likely Module 2 controller→processor) + **Transfer Impact Assessment** evaluating destination country surveillance laws.
  - **UK → 3rd country:** UK IDTA *or* EU SCCs + UK Addendum + TIA.
  - **AU → 3rd country:** APP 8.1 — either contractual binding equivalent to APPs, or rely on customer consent under APP 8.2(b), or one of the other exceptions.
- **Supplementary measures** if TIA flags risk: encryption in transit + at rest with keys held in EU, pseudonymisation of inputs before transfer, contractual audit rights, transparency reports.
- **US-specific:** if using a US sub-processor certified under the **EU–US Data Privacy Framework** (and the UK Extension), that provides an adequacy route — but check the sub-processor's certification is current and covers the relevant processing.

**Hard ask for engineering/architecture:** pin down the inference and training topology *before* compliance can sign off. "We'll figure it out" is not assessable.

---

## 5. DPIA — Required, Recommended Next Step

Article 35(3)(a) GDPR mandates a DPIA for *"systematic and extensive evaluation … based on automated processing, including profiling, on which decisions are based that produce legal effects or similarly significant effects."* The ICO and EDPB lists also flag *"combining datasets from multiple sources"* and *"innovative use of new technology (ML)"* as DPIA triggers — this feature hits at least three.

**Next step:** run `/grc-lead:write-dpia` to produce the formal Article 35 assessment. It needs the lawful basis decision (§2) and data flow map (§4) as inputs — start gathering those in parallel.

The DPIA will also surface whether **prior consultation with the supervisory authority** (Art 36) is required — likely not, but the assessment determines that.

---

## 6. Scope Boundary — GRC vs Engineering

The following are **engineering deliverables**, not GRC ones. Handing off:

- **Security engineer** — input validation on collected fields, audit logging of model inputs/outputs and score-driven actions, data deletion mechanisms (per-record + cascade to model artifacts where feasible), encryption posture, access controls on the score store.
- **ML engineer** — model explainability instrumentation (per-prediction feature attribution sufficient to answer a DSAR), bias evaluation across customer segments (size, region, language), drift monitoring, training data lineage, model versioning so a contested score can be reproduced.
- **Product/UX** — privacy notice updates, opt-in/opt-out flows if consent path chosen, objection-handling UX, the CS team's workflow for human review of low scores.

GRC owns: lawful basis sign-off, DPIA, LIA (if Path A), records of processing (Art 30), transfer paperwork (SCCs/TIA/IDTA), regulator-facing documentation, and the policy that says when a score may or may not be acted on automatically.

---

## Immediate Asks (Blocking)

1. **Lawful basis decision per jurisdiction** (§2) — product + legal.
2. **Data flow / hosting topology** (§4) — engineering architect.
3. **Data source minimisation call** (§3) — product + ML lead; confirm v1 source set.
4. Once 1–3 land, kick off `/grc-lead:write-dpia`.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/17.0 (100%) |
| Evaluated | 2026-05-27 |
| Target model | claude-opus-4-7 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 84409 ms |
| Target cost | $0.3875 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Identifies the applicable regulatory frameworks correctly — Australian Privacy Principles (APPs), GDPR (Germany and UK), and UK GDPR post-Brexit | PASS | Opening line: 'Australia (Privacy Act 1988 + APPs), UK (UK GDPR + DPA 2018), Germany (EU GDPR + BDSG)' — all three named explicitly. |
| c2 | Flags that automated/ML-based profiling triggers specific GDPR requirements (Article 22 — automated decision-making and profiling) | PASS | R2 in risk table: 'Automated decision-making engages GDPR Art 22 safeguards… requires human-in-the-loop, explanation rights, contestation mechanism.' |
| c3 | Quantifies risks using likelihood and impact language — not just listing concerns generically | PASS | 10-row risk table with explicit Likelihood/Impact ratings (e.g. R1: Likelihood HIGH, Impact HIGH) plus a one-line rationale per row. |
| c4 | Identifies the lawful basis question for each jurisdiction (consent vs legitimate interest) as a blocking open question | PASS | Section 2 titled 'Lawful Basis — BLOCKING Open Question' presents Path A (LI + LIA) and Path B (Consent) with per-jurisdiction notes and 'Why this is blocking' subsection. |
| c5 | Recommends a DPIA given the profiling + ML combination and scale of processing | PASS | Section 5: 'Article 35(3)(a) GDPR mandates a DPIA… this feature hits at least three [triggers].' Explicitly required. |
| c6 | Does not simply block the feature — presents a compliant path forward | PASS | 'Immediate Asks (Blocking)' section lays out a 4-step compliant path; output presents minimisation, lawful basis options, DPIA steps, transfer safeguards. |
| c7 | Separates GRC concerns (policies, frameworks, classification) from technical implementation (delegates guardrails to security engineer) | PASS | Section 6 explicitly delegates to 'Security engineer' and 'ML engineer' and lists GRC-owned items separately ('GRC owns: lawful basis sign-off, DPIA, LIA…'). |
| c8 | Addresses data minimisation — whether all four data sources are necessary for the score | PARTIAL | Section 3 table evaluates all four sources; proposes minimum viable set (login + support metadata); email opens and payment history flagged as 'Question' with drop rationale. |
| c9 | Recommends prior supervisory authority consultation under GDPR Art. 36 — only if residual risk would remain high after mitigations | SKIP | SKIP per test instructions. |
| c10 | Output names all three frameworks explicitly — Australian Privacy Principles (APPs / Privacy Act 1988), GDPR (Germany), and UK GDPR + Data Protection Act 2018 (UK) — and notes UK GDPR diverges slightly post-Brexit | PASS | Header names all three with full citations; Section 4 uses UK IDTA separately from EU SCCs, acknowledging post-Brexit divergence implicitly through separate instruments. |
| c11 | Output flags GDPR Article 22 (automated decision-making and profiling) as triggered by the ML-driven health score — including the right to human review and the requirement to inform the data subject | PASS | R2 names Art 22, lists 'human-in-the-loop, explanation rights, contestation mechanism'; R5 covers transparency/informing data subjects; Section 6 assigns human-review UX to Product. |
| c12 | Output recommends a DPIA (Data Protection Impact Assessment) under Article 35 given large-scale profiling combined with multiple data sources, and names the next step (`/grc-lead:write-dpia`) | PASS | Section 5: 'Next step: run `/grc-lead:write-dpia` to produce the formal Article 35 assessment.' Exact skill name present. |
| c13 | Output identifies the lawful basis question per jurisdiction as a blocking open issue — likely legitimate interest with a Legitimate Interests Assessment (LIA), or consent if customer-facing transparency is the chosen path — with the trade-offs of each | PASS | Section 2 presents Path A (LI + LIA with pros/cons) and Path B (Consent with pros/cons); Germany-specific BfDI note; mixed-path recommendation framed as 'not mine to make.' |
| c14 | Output quantifies risks with likelihood and impact (e.g. 'Likelihood: Medium — opt-out rates from current product analytics suggest 5-10% will object; Impact: High — automated decisioning without consent could trigger regulatory action'), not generic 'this is a privacy concern' | PASS | R1: 'L: no basis selected yet — default state is non-compliant. I: EU/UK fines up to 4% global turnover; AU civil penalties up to AUD $50M.' All 10 rows follow same structure. |
| c15 | Output does not block the feature — presents a compliant path forward (data minimisation, transparent notice, opt-out mechanism, human review on at-risk-account decisions, retention limits) | PASS | Sections 2–6 and Immediate Asks collectively form a compliant path; minimisation, lawful basis choice, notice, human review, and DPIA are all addressed. |
| c16 | Output addresses data minimisation — questions whether all four sources (email open rates, support tickets, login frequency, payment history) are necessary, and proposes the minimum subset that achieves the customer-success goal | PASS | Section 3 table covers all four; 'Proposed minimum viable feature set: login frequency + support ticket metadata.' Email opens and payment history receive drop rationale. |
| c17 | Output separates GRC concerns (policies, lawful basis, DPIA, customer notice) from technical implementation (delegates the technical guardrails — input validation, audit logging, deletion mechanisms — to the security engineer or developer, not specifying them itself) | PASS | Section 6: 'Security engineer — input validation… audit logging… data deletion mechanisms'; 'GRC owns: lawful basis sign-off, DPIA, LIA…' Clean split. |
| c18 | Output addresses transparency — the customer-success team using the score must know what data went in, customers must be informed in privacy notice and product UI, and there must be a route to challenge a decision | PASS | R5 covers privacy notice update obligation; R2 names contestation mechanism; Section 6 delegates 'objection-handling UX' and privacy notice updates to Product/UX. |
| c19 | Output addresses cross-border data transfer — German/UK customer data flowing to wherever the ML model runs, with adequacy decisions or Standard Contractual Clauses if outside the EU/UK | PARTIAL | Section 4 covers EU SCCs (Module 2), UK IDTA, TIA, supplementary measures, AU APP 8, and EU–US DPF adequacy. Detailed and specific. |

### Notes

The output is a near-perfect response, meeting every scored criterion fully and both PARTIAL-capped criteria at their ceiling. The only gap worth noting is that UK GDPR post-Brexit divergence is acknowledged implicitly (separate IDTA instrument) rather than with an explicit sentence — but the evidence is unambiguous.
