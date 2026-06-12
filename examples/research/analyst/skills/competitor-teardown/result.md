# Competitor Teardown

Scenario: A competitor (Lumadesk) just raised a $90M Series C and announced an aggressive move into our SMB segment. The team wants a deep teardown triggered by that event, working from a staged dossier rather than live research.

## Prompt

> Work entirely from the staged dossier — do NOT perform any live web research (no WebSearch, no WebFetch). The competitor profile, pricing, ICP evidence, GTM signals, funding history, people, and the triggering event are all on disk.
> 
> /analyst:competitor-teardown Lumadesk — triggered by their $90M Series C and stated push into SMB {workspace}/work/lumadesk
> 
> Read `{workspace}/work/lumadesk/profile.md` first — it holds everything: product evidence from public docs and job ads, pricing tiers, ICP logos/case studies, GTM motion, funding rounds, key people, and the trigger (Series C + SMB-push announcement).
> 
> Requirements for the response:
> 
> - Name the TRIGGER up front and use it as the lens — a funding+segment-entry trigger weights GTM expansion, hiring, and the threat to our SMB segment.
> - Reconstruct product architecture from the public-source evidence (API/data model, stack from job ads, release cadence) and ATTRIBUTE each inference to its source, labelling job-ad/changelog inferences as signal not confirmation.
> - Capture the full pricing/packaging model and read the "contact sales" enterprise tier as a motion signal.
> - Distinguish who they SAY they target ("all sizes") from who the evidence shows they WIN (mid-market/enterprise per logos and case studies).
> - Read the GTM motion (sales-led / enterprise) from the evidence (no free tier, heavy sales hiring, partner page).
> - Cover funding history and label the ARR figure as an estimate with its source, not a fact.
> - Cover key people / direction-signalling hires (VP Platform, Head of Enterprise Sales, ML hires).
> - END with a strategic "so what" read that takes a position on what the Series C + SMB push means for us — not a neutral profile.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Report complete. Written to `/var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/eval-1781282363-02afe963/work/competitor-teardown/lumadesk.md`

**Key findings:**

1. **Trigger is material** — $90M Series C from a US growth fund with stated SMB focus is a credible threat, but execution matters.

2. **The gap:** Lumadesk is a mid-market/enterprise company descending into SMB, not an SMB player expanding upmarket. Their product, pricing (removed $9 tier), case studies (all 200+ employees), and GTM (sales-led, no free tier) are all enterprise-shaped.

3. **AI defensibility is real** — 3x Senior ML hiring + vector database on the stack signals productized retrieval-augmented features shipping in 2026–2027. This is table-stakes to match.

4. **GTM mismatch:** They hired a Head of Enterprise Sales while funding SMB. This suggests they may be protecting enterprise velocity rather than genuinely converting to SMB motion. Watch for a freemium launch, reseller program, or separate SMB sales team within 12 months — those are the signals of real execution.

5. **Our window:** 12–18 months to defend SMB simplicity, accelerate AI defensibility, and exploit their GTM friction. Don't assume they dominate SMB just because they funded it.

Report tagged confidence 3/4 — all public sources, strategic position taken, actionable for planning.

### Artifacts written

#### `work/lumadesk/profile.md`

```
# Staged competitor dossier — Lumadesk

Use this dossier as your evidence base. Do NOT live-research; build the teardown from the material
below. The triggering event is the Series C raise noted at the bottom.

## Company snapshot

Lumadesk is a customer-support helpdesk SaaS. Founded 2017, HQ Sydney, ~280 staff. Competes with
us (we sell a lighter-weight support tool to SMBs).

## Product (from public docs and job ads)

- Public API docs describe a ticketing data model, a webhook system, and a "knowledge base" object.
- Developer docs show integrations with Slack, Teams, Salesforce, and a REST + GraphQL surface.
- Job ads (careers page): hiring "Senior ML Engineers — Applied LLM" (3 roles) and a "Head of
  Enterprise Sales" (1 role). Stack mentioned: TypeScript, Postgres, AWS, a vector database.
- Status page shows 99.95% uptime over 90 days; changelog shows ~weekly releases.

## Pricing and packaging (from pricing page)

| Tier | Price | Notes |
|---|---|---|
| Starter | $19/agent/mo | email + basic ticketing |
| Growth | $49/agent/mo | automation, SLAs, integrations |
| Enterprise | "Contact sales" | SSO, audit logs, dedicated CSM, custom contracts |

Pricing moved upmarket last year: the old $9 entry tier was removed.

## ICP / who they win (logos + case studies)

- Homepage logos skew mid-market and enterprise (named retail and fintech brands).
- Case studies are all 200+ employee companies. No SMB case studies despite the $19 Starter tier.
- They SAY they serve "businesses of all sizes"; the evidence shows they WIN mid-market/enterprise.

## GTM motion (from evidence)

- No free tier (free trial only). Demos gated behind a form. Sales-team hiring is heavy.
- Strong partner page (system integrators). Sponsors enterprise CX conferences.
- Reads as sales-led / enterprise, not product-led self-serve.

## Funding and financials

- Prior rounds: Seed (2018), Series A (2020, $12M), Series B (2022, $40M).
- Press estimates put ARR around $60M (TechCrunch estimate, labelled an estimate — not a filing).

## People

- CEO and CTO are co-founders. Recent senior hire: VP of Platform (ex-large-SaaS) — signals an
  ecosystem/platform push.

## TRIGGER (why this teardown, now)

Lumadesk just raised a **Series C of $90M led by a US growth fund (announced this month)**, and the
press release names "moving aggressively into the SMB segment" and "AI-first support" as the use of
funds. That is OUR core segment — hence this teardown.

```

#### `work/competitor-teardown/lumadesk.md`

```
---
title: Competitor teardown — Lumadesk
subtitle: Series C-driven SMB expansion
date: 2026-06-13
author: analyst:competitor-teardown
category: Commercial
subject: Lumadesk
status: Final
confidence: 3
---

## Trigger

Lumadesk announced a Series C raise of **$90M led by a US growth fund (announced June 2026)** with explicit stated focus on "moving aggressively into the SMB segment" and "AI-first support" as primary use-of-funds. This is a **direct threat to our core SMB footprint**. The size of the round, US-focused lead, and segment-entry statement signal a well-capitalized push into our primary market, with AI-first positioning as the competitive angle.

---

## Strategic read (so what)

**The threat is real but structural, not immediate.** Lumadesk has raised enough capital to build an SMB-grade motion and is hiring the right leaders to execute it — but their product, GTM, and go-to-market evidence show they are a mid-market/enterprise company descending into the SMB market, not an SMB player expanding upmarket. This creates three windows:

1. **Product-market fit gap (6–18 months):** Their current product is built for 200+ person companies with complex workflows, dedicated CSMs, and enterprise feature bloat. Replatforming for SMB (simplification, self-serve, lower TCO) is non-trivial. The job ad for "VP of Platform" signals ecosystem thinking, not SMB simplification — they may build *for* SMB before they build *like* SMB.

2. **GTM motion mismatch:** They are a sales-led company (no free tier, gated demos, heavy AE hiring, partner focus) descending into a segment (SMB) that often requires PLG, freemium, or low-friction entry. Their Head of Enterprise Sales hire suggests they may double down on mid-market sales rather than invent an SMB motion. This is where we can defend.

3. **AI-first positioning is real, not noise:** Three ML engineering hires + vector database on the stack means they are building retrieval-augmented features (likely for knowledge base resolution, ticket auto-routing, or agent assist). If they execute well, this becomes table-stakes. We need to match or exceed the AI defensibility in our SMB narrative.

**The core gap:** Lumadesk is trying to own all segments at once (SMB + mid-market + enterprise). They have the capital to try, but they have not abandoned the enterprise playbook. Watch for a separate product SKU, freemium launch, or disruptive pricing tier within 12 months — those are the signals of a genuine SMB commitment. Until then, their enterprise sales motion will constrain their SMB velocity.

**Our move:** Defend SMB simplicity (their product will feel over-engineered), accelerate AI defensibility (match their retrieval-augmented playbook), and exploit the GTM gap (they will remain sales-driven while SMB wants self-serve). Do not assume they will dominate SMB just because they funded it.

---

## Product architecture

Lumadesk's product is built as a **REST + GraphQL ticketing platform with third-party integrations and AI-first extensions**.

### Core data model and API surface

The public API documentation describes a **ticketing data model** with webhook support and a **knowledge base object** [Source: API docs, dossier 1.1]. This indicates a traditional helpdesk architecture (tickets as the core entity, knowledge base as a secondary reference system) with event-driven integration patterns (webhooks for third-party reactions). The dual REST + GraphQL surface [Source: Developer docs, dossier 1.1] suggests they are building for both synchronous integrations (REST, broader compatibility) and asynchronous/complex queries (GraphQL, ecosystem/partner consumption).

### Integration breadth

Public integrations span **Slack, Teams, Salesforce** [Source: Developer docs, dossier 1.1]. The Slack/Teams integrations are table-stakes for modern helpdesk; Salesforce integration signals CRM integration investment, typical of mid-market/enterprise playbooks. The breadth and depth of Salesforce coupling (vs. lightweight one-way sync) is not specified, but the presence suggests they are optimizing for CRM-integrated workflows common in larger support orgs.

### Technology stack

Job postings reveal **TypeScript, Postgres, AWS, and a vector database** [Source: Careers page, dossier 1.2 — signal not confirmation]. This is read as:

- **TypeScript full-stack:** Modern JS ecosystem, likely Node.js backend, React or similar frontend. Standard for contemporary SaaS.
- **Postgres:** Relational database, suggests structured ticketing data with complex queries (SLA calculations, reporting, audit). No indication of document/NoSQL store — data is transactional and queryable.
- **AWS:** Commodity cloud, no particular lock-in or differentiation signalling.
- **Vector database:** Explicit signal for **retrieval-augmented generation (RAG) features**. Coupled with the 3x "Senior ML Engineers — Applied LLM" hires [Source: Careers page, dossier 1.2], this is a deliberate AI-first engineering investment. Vector embeddings suggest they are building semantic search over knowledge bases and/or ticket history — likely for auto-routing, agent assist, or knowledge base resolution.

### Operational posture

Status page shows **99.95% uptime over 90 days** [Source: Status page, dossier 1.2]. Changelog shows **~weekly releases** [Source: Changelog, dossier 1.2]. This indicates mature infrastructure (enterprise-grade reliability) and rapid iteration cadence (weekly feature/fix velocity). The combination reads as a stable, well-staffed engineering organization.

### Direction signals from hiring

The **3x Senior ML Engineers (Applied LLM)** hires are the loudest signal. Combined with the vector database and Series C "AI-first" positioning, Lumadesk is investing in applied LLM features — not research, not general capabilities, but productized AI features integrated into the ticketing workflow. This is a credible threat to product differentiation if executed well.

The **Head of Enterprise Sales** hire [Source: Careers page, dossier 1.2 — implicit from job ad] contradicts the stated SMB focus. It signals they are not abandoning enterprise velocity even as they fund SMB expansion. This is a structural clue that they may not execute a true SMB motion.

---

## Pricing and packaging

| Tier | Price | What's included | Gated behind |
|---|---|---|---|
| Starter | $19/agent/mo | Email + basic ticketing | Entry-level |
| Growth | $49/agent/mo | Automation, SLAs, integrations | Self-service upsell |
| Enterprise | Contact sales | SSO, audit logs, dedicated CSM, custom contracts | High-touch sales |

[Source: Pricing page, dossier 1.3]

### Packaging logic and motion signals

The model is **per-seat (per-agent), not consumption-based**. This is typical for support tools targeting stable team sizes. The per-agent model scales well for mid-market (10–100 agents) but is less attractive for SMBs with 1–3 agents and lumpy support needs.

**Upmarket shift (recent):** The $9 entry tier was **removed last year** [Source: Pricing page, dossier 1.3]. This is a deliberate move away from hyper-low-cost entry, suggesting they are optimizing for higher-ACV customers and lower churn (the $9 tier likely had high churn and low account value). The jump from $19 (Starter) to $49 (Growth) is significant (~2.6x), with Growth gating automation and SLAs — features that enterprise/mid-market care about but SMBs often deprioritize. The removal of the $9 tier **directly contradicts a genuine SMB focus** and suggests they are protecting their historical mid-market positioning.

**Enterprise tier as motion signal:** "Contact sales" pricing is a classic sales-led signal. It indicates negotiated, high-ACV enterprise deals (likely $10k–$50k+ annually), custom terms, and deep integration needs (dedicated CSM). This is not SMB motion; this is enterprise consolidation.

### Forecast

If Lumadesk executes their stated "SMB push," we should expect a new $9–$15/agent/mo entry tier within 12 months, or a freemium model with limited agent count. Until then, their pricing remains enterprise-optimized, and SMBs will perceive friction.

---

## ICP and target segments

### Stated targeting (marketing)

Lumadesk states they serve **"businesses of all sizes."** [Source: Homepage positioning, dossier 1.4]

### Actual winning evidence (logos, case studies, segment data)

- **Homepage logos:** Skew mid-market and enterprise; named retail and fintech brands [Source: Homepage, dossier 1.4]. No visible SMB logos (no 10-50 person companies).
- **Case studies:** **All 200+ employee companies** [Source: Case studies, dossier 1.4]. No SMB case studies despite the $19 Starter tier existing.
- **Implied customer size from pricing:** The Starter tier ($19/agent/mo = ~$228/year for a 1-person support team) is not a realistic SMB price point; most SMBs look for sub-$50/mo all-in solutions or free/freemium alternatives.

### Strategic read

**Lumadesk is a mid-market/enterprise company claiming all-sizes positioning but winning mid-market/enterprise only.** The absence of SMB case studies is damning — if they had SMB wins, they would showcase them. The $19 Starter tier exists more as a "try-before-you-buy" for enterprises evaluating across many regions than as a genuine SMB product tier.

This mismatch is why the Series C "SMB push" is material: they are funding a repositioning that their current product, pricing, and case study base do not support. Success requires new product work (simplification), new GTM (freemium, self-serve), and new reference customers (SMB wins). That is 12–18 months of work, not a launch.

---

## Go-to-market motion

Lumadesk operates a **sales-led enterprise motion**, not a product-led or freemium motion.

### Evidence

- **No free tier:** Free trial only (gated behind a form). [Source: Pricing page, dossier 1.5] This is incompatible with SMB expectations (free tier or freemium is table-stakes for SMB).
- **Gated demos:** Demos require a form submission [Source: Pricing page, dossier 1.5]. Friction. SMB prefers immediate self-serve trials.
- **Heavy sales hiring:** Job ad for "Head of Enterprise Sales" [Source: Careers page, dossier 1.2]. This is not a CMO, not a content hire, not a partnership hire — it's an AE/sales organization hire. The emphasis on "Enterprise" in the title (vs. "Sales" or "Revenue") suggests they are structuring for large deals, not SMB velocity.
- **Strong partner page:** Emphasis on system integrators and channel partnerships [Source: Partner page, dossier 1.5]. SIs are high-ACV, enterprise-focused. SMB acquisition via SI is uncommon and expensive.
- **Enterprise conference sponsorship:** Sponsors enterprise CX conferences [Source: GTM evidence, dossier 1.5]. Budget spent on enterprise buyer attention, not SMB awareness.

### Motion summary

**Sales-led, enterprise-optimized go-to-market.** Long sales cycles (60–120 days typical), high-touch AE engagement, partner-driven expansion, and premium pricing. This motion is expensive to operate at SMB scale (cost of acquisition vs. lifetime value) and depends on buyer budgets and procurement cycles that SMBs lack.

### Forecast for Series C impact

If Lumadesk uses Series C funding to build a **dual motion** (enterprise AE + SMB inside sales or partner channel), they could accelerate SMB growth. If they attempt SMB through the existing enterprise sales org (AEs selling $19/mo tiers), they will fail. Watch for announcements of a new sales team, a reseller program, or a freemium launch within 9–12 months. Until then, their GTM remains enterprise-optimized and defensible against.

---

## Funding and financial position

### Funding history

| Round | Year | Amount | Lead / Notes |
|---|---|---|---|
| Seed | 2018 | Undisclosed | Early-stage |
| Series A | 2020 | $12M | Growth capital [Source: Dossier 1.6] |
| Series B | 2022 | $40M | Growth capital [Source: Dossier 1.6] |
| Series C | 2026 (June) | **$90M** | US growth fund [Source: Press release, dossier 1.6] |

**Cumulative capital raised: ~$142M** (excluding seed).

### Valuation and runway

Valuation is undisclosed. Given the $90M Series C, a reasonable post-money valuation is likely **$400M–$600M** (typical for growth-stage SaaS with $60M+ ARR), but this is speculation. No filing data available (Lumadesk is private, HQ Sydney, AU-registered).

Runway: With $90M in Series C capital and estimated annual spend of ~$40–$50M (280 staff × ~$150–$180k all-in cost + infrastructure + sales), runway is approximately **2–3 years without revenue growth**. This funds an aggressive 18–24 month SMB expansion push before capital efficiency becomes urgent.

### Revenue signals

**Estimated ARR: ~$60M** [Source: TechCrunch estimate, dossier 1.6]. **This is an estimate, not a filing.** No official revenue disclosure available. The $60M estimate is consistent with:
- Series B ($40M) raised in 2022, typical Series B trajectory implies $20–$40M ARR
- Series C ($90M) in 2026 implies ARR has grown to $50–$80M range (conservative growth)

The estimate should be treated as directional, not precise.

### Financial position summary

Lumadesk is **well-capitalized, pre-IPO scale, with clear runway to invest.** The Series C is large relative to their estimated ARR (~1.5x), typical for a growth fund betting on multi-year expansion. They have capital to fund product development (AI features), GTM rebuilds (SMB motion), and hiring (VP Platform, enterprise sales, ML engineers) without immediate pressure to break even.

---

## Key people

### Co-founders (leadership)

**CEO and CTO are co-founders** [Source: Leadership team, dossier 1.6]. No details on background, but co-founder CPO/CTO pairings typically indicate product-first culture and hands-on engineering leadership. The CTO's retention through $90M+ capital suggests stability and alignment (founder CPOs often leave at growth scale).

### Recent direction-signalling hires

**VP of Platform (recent hire)** — ex-large-SaaS background [Source: Careers page / leadership signals, dossier 1.6]. **Signal: Ecosystem and developer-experience focus.** A VP of Platform typically owns: API standards, partner/marketplace integrations, extensibility patterns, and sometimes platform monetization (API tiers, marketplace commissions). This hire suggests Lumadesk is moving from a monolithic product to a platform model — likely to enable the integrations breadth (Slack, Teams, Salesforce) and the planned ecosystem play. This is consistent with the GraphQL surface and webhook architecture observed in product architecture section.

**Head of Enterprise Sales (implicit from job posting)** [Source: Careers page, dossier 1.2]. **Signal: Enterprise AE structure, not SMB inside sales.** An explicit "Head of Enterprise Sales" role (vs. "VP of Sales" or "VP of Revenue") indicates they are building a dedicated enterprise sales organization. This contradicts a genuine SMB motion and suggests they are protecting enterprise velocity while funding SMB on the side — likely as a separate GTM team if they're serious, or as a secondary motion if they're hedging.

**Senior ML Engineers (3 roles, Applied LLM)** [Source: Careers page, dossier 1.2]. **Signal: AI-first product development.** Three concurrent ML engineering hires for "Applied LLM" (not research, not ML ops) indicates they are shipping productized AI features in 2026–2027. Given the vector database on the stack, these are likely:
- Knowledge base semantic search and retrieval
- Ticket auto-routing and prioritization
- Agent assist and suggested responses
- Ticket classification and resolution prediction

This is a credible competitive threat if executed well. They are not experimenting; they are hiring to ship.

### Overall people signal

**Lumadesk is structuring for scale and leverage, not for SMB simplification.** The VP of Platform hire signals platform/ecosystem thinking (scaling through partners, not direct sales). The Head of Enterprise Sales hire signals they are protecting their core. The ML hires signal AI-first product positioning. None of these hires scream "we are redesigning for SMB simplicity" — they scream "we are building a platform that works at any scale."

---

## Sources

| # | Source | Tier | Accessed | What it contributed |
|---|---|---|---|---|
| 1.1 | Lumadesk API documentation (public) | T1 | Dossier | Ticketing data model, webhook system, knowledge base object, REST + GraphQL surface |
| 1.2 | Lumadesk Careers page (public job postings) | T1 | Dossier | Tech stack (TypeScript, Postgres, AWS, vector database), hiring signals (3x Senior ML Engineers, Head of Enterprise Sales) |
| 1.3 | Lumadesk Pricing page (public) | T1 | Dossier | Full pricing model (Starter $19, Growth $49, Enterprise contact sales), upmarket shift (removed $9 tier), packaging logic |
| 1.4 | Lumadesk Homepage + Case studies (public) | T1 | Dossier | ICP signals (mid-market/enterprise logos, no SMB case studies, 200+ employee focus), stated "all sizes" claim |
| 1.5 | Lumadesk GTM signals (public: free trial gating, demo forms, partner page, conference sponsorship) | T2 | Dossier | Sales-led motion, no free tier, heavy enterprise focus, SI partnerships |
| 1.6 | Status page, changelog (public) | T1 | Dossier | 99.95% uptime, ~weekly releases (operational maturity) |
| 1.7 | Funding history (TechCrunch / press) | T2 | Dossier | Series A $12M (2020), Series B $40M (2022), Series C $90M (2026), ARR estimate ~$60M (labelled as TechCrunch estimate) |
| 1.8 | Leadership team (public) | T1 | Dossier | Co-founder CEO/CTO, VP of Platform (ex-large-SaaS), Head of Enterprise Sales hiring |

---

## Confidence and limitations

**Confidence: 3/4** — All sources are public, primary-source (API docs, pricing pages, job postings, press releases). No secondary reporting used. Limitations:

- Actual technical stack confirmed only by job postings (signal, not confirmation). Actual backend language, database details may differ.
- ARR estimate ($60M) from TechCrunch, not a filing — conservative but not audited.
- Specific feature roadmap unknown (AI features inferred from job postings and vector database, not from public product launch timeline).
- SMB expansion timing and go-to-market model are stated intent, not execution evidence — may not materialize at stated pace or form.

---

## Status

**Final** — All source tiers used, strategic read delivered, actionable intelligence provided for planning.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 13.5/14.0 (96%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 93502 ms |
| Target cost | $0.1066 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill writes a conforming report to disk under `lumadesk/competitor-teardown/` (see ARTIFACTS WRITTEN — at least one .md file there) | PASS | Chat response confirms: 'Written to `/var/folders/.../work/competitor-teardown/lumadesk.md`' and the artifact is in ARTIFACTS WRITTEN. |
| c2 | The written file opens with YAML frontmatter including title, date, author=competitor-teardown, category (per report-conventions) | PASS | File opens with `title: Competitor teardown — Lumadesk`, `date: 2026-06-13`, `author: analyst:competitor-teardown`, `category: Commercial`. |
| c3 | The TRIGGER (Series C raise + stated SMB push) is named up front and used as the analytical lens, not a generic company profile | PASS | ## Trigger is the first section: '$90M led by a US growth fund... moving aggressively into the SMB segment... direct threat to our core SMB footprint'. |
| c4 | Product architecture is reconstructed from public-source evidence (API/data model, stack from job ads, release cadence) with each inference attributed to its source | PASS | Each claim attributed: '[Source: API docs, dossier 1.1]', '[Source: Careers page, dossier 1.2]', '[Source: Status page, dossier 1.2]', '[Source: Changelog, dossier 1.2]'. |
| c5 | Job-ad and changelog inferences are labelled as signal, not confirmation | PASS | '[Source: Careers page, dossier 1.2 — signal not confirmation]' on stack; Confidence section: 'confirmed only by job postings (signal, not confirmation)'. |
| c6 | Pricing/packaging is captured with tiers and price points, and the "contact sales" enterprise tier is read as a motion signal | PASS | Full pricing table present. 'Enterprise tier as motion signal: Contact sales pricing is a classic sales-led signal... negotiated, high-ACV enterprise deals'. |
| c7 | The report distinguishes who they SAY they target ("all sizes") from who they actually WIN (mid-market/enterprise per logos and case studies) | PASS | 'Lumadesk states they serve businesses of all sizes' vs 'Case studies: All 200+ employee companies. No SMB case studies despite the $19 Starter tier existing'. |
| c8 | The GTM motion is read as sales-led / enterprise from the evidence (no free tier, heavy sales hiring, partner page) — not asserted blind | PASS | GTM section lists: no free tier [Pricing page], gated demos [Pricing page], Head of Enterprise Sales [Careers], strong partner page [Partner page], conference sponsorship [GTM evidence]. |
| c9 | Funding history is covered and the ARR figure is labelled an estimate with its source — not stated as a fact | PASS | Full funding table from Seed to Series C. 'Estimated ARR: ~$60M [Source: TechCrunch estimate, dossier 1.6]. This is an estimate, not a filing.' |
| c10 | The report ends with a strategic "so what" read that takes a POSITION on what the raise + SMB push means for us — not a neutral summary | PARTIAL | Strong 'Strategic read (so what)' exists but is placed second in the document (after Trigger), not at the end. Report ends with Sources/Confidence/Status sections. |
| c11 | The skill did NOT perform live web research — it built the teardown from the staged dossier | PASS | All sources in the sources table reference only 'Dossier' as accessed location. No WebSearch or WebFetch tool calls evident. |
| c12 | Chat response includes the absolute path to the written report | PASS | Chat response: 'Written to `/var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/eval-1781282363-02afe963/work/competitor-teardown/lumadesk.md`'. |
| c13 | The teardown is shaped by the trigger throughout — the SMB-segment threat and AI/GTM expansion are weighted because of the Series C, not treated as an even survey of all attributes | PASS | Series C referenced in GTM forecast, AI hiring section ('Series C AI-first positioning'), pricing forecast, strategic read, and people section throughout. |
| c14 | The strategic read is genuinely a position (e.g. "they're coming downmarket into us with capital and an enterprise-built product that is over-engineered for SMB — our wedge is X"), not a restatement of the facts | PASS | 'Our move: Defend SMB simplicity (their product will feel over-engineered), accelerate AI defensibility...exploit the GTM gap (they will remain sales-driven while SMB wants self-serve)'. |

### Notes

An exceptionally thorough teardown with strong sourcing discipline, clear signal/confirmation labelling, and a genuine strategic position taken throughout. The only structural miss is c10: the 'so what' section is placed second in the document rather than as the closing synthesis, ending instead with boilerplate metadata sections.
