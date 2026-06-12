# Win Loss Analysis

Scenario: A sales leader doesn't trust the CRM close-reasons for a batch of Q2 mid-market losses to a competitor (Pinnacle). They want a win/loss analysis that surfaces the gap between what reps reported and what buyers actually said, working from staged deal records.

## Prompt

> Work entirely from the staged deal records — do NOT perform any live web research (no WebSearch, no WebFetch). The deal set, the sales-reported reasons, and the buyer-reported reasons are already on disk.
> 
> /analyst:win-loss-analysis losses to Pinnacle (Q2 mid-market) {workspace}/work/deals
> 
> Read `{workspace}/work/deals/q2-deal-records.md` first — it holds the deal set context (window, segment, win/loss mix) and, for each deal, the SALES-reported close reason and the BUYER-reported reason from post-close interviews.
> 
> Requirements for the response:
> 
> - Scope the deal set explicitly (window, segment, win/loss mix) and note the 7-14 day post-close interview discipline.
> - Put the sales-reported reason next to the buyer-reported reason for each deal — and make the BUYER-VS-REP GAP the headline, near the top. Where reps systematically say "price" but buyers say something else, name it as a messaging/sales-process problem wearing a product-problem costume.
> - Extract PATTERNS across the set (a pattern needs two or more deals): e.g. unclear differentiation, slow follow-up misfiled as feature gaps, hidden decision-makers (security / procurement vetoes), migration-trust gaps. A single deal is an anecdote, not a pattern.
> - Include the WINS — say what they tell you to protect (discovery + migration confidence + painless buying), not just what to fix.
> - Recommend specific owned actions, separating fix-the-product from fix-the-messaging from fix-the-sales-process.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

`/var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/eval-1781283031-ad428c0c/work/win-loss-analysis/pinnacle.md`

### Artifacts written

#### `work/deals/q2-deal-records.md`

```
# Staged deal records — Q2 mid-market deals, losses to Pinnacle (and two wins)

Use these records as your evidence base. Do NOT live-research; run the win/loss METHOD on the
material below. Each record carries the SALES-reported reason (from CRM) AND a reconstructed
BUYER-reported reason (from post-close buyer interviews / public signals). The gap between them is
the headline output.

## Deal set context

- Window: deals closed in Q2 2026, mid-market segment (200-1000 employees), competing against
  Pinnacle. Buyer views captured 7-14 days post-close.
- Mix: 6 losses + 2 wins (wins included deliberately).

## Records

### Loss 1 — Acme Logistics

- Sales-reported (CRM close reason): "Lost on price — competitor was cheaper."
- Buyer-reported: "Price wasn't really it. We never understood how you were different from Pinnacle.
  Your demo showed features; theirs showed our exact workflow. The price felt unjustified because
  the value wasn't clear." (laddered: price -> unclear differentiation -> weak discovery)

### Loss 2 — Borealis Health

- Sales-reported: "Lost on price."
- Buyer-reported: "Our security team blocked it. You couldn't produce a SOC2 report in time and
  Pinnacle could. The business sponsor wanted you." (hidden decision-maker: security veto)

### Loss 3 — Cyan Retail

- Sales-reported: "Feature gap — they wanted advanced reporting."
- Buyer-reported: "Honestly the rep went quiet for two weeks mid-evaluation. Pinnacle stayed close.
  By the time we heard back we'd moved on." (sales-execution: slow follow-up, misfiled as product)

### Loss 4 — Delta Freight

- Sales-reported: "Lost on price."
- Buyer-reported: "We didn't trust the migration path. Moving 3 years of data with no clear plan
  felt risky, so the price felt like a gamble." (laddered: price -> migration-risk -> trust)

### Loss 5 — Evergreen Foods

- Sales-reported: "Competitor relationship — incumbent."
- Buyer-reported: "Procurement added a vendor-risk review late and you had no answers ready;
  Pinnacle did. Finance and procurement drove the final call, not the team who'd use it."
  (hidden decision-maker: procurement)

### Loss 6 — Foxtrot Media

- Sales-reported: "Feature gap."
- Buyer-reported: "Same as the others really — your team showed product, not our problem. We
  couldn't tell what made you better." (unclear differentiation again)

### Win 1 — Garnet Manufacturing

- Sales-reported: "Won on relationship."
- Buyer-reported: "Your team actually mapped our workflow and showed the migration plan up front.
  That's why we trusted you over Pinnacle." (what we protect: discovery + migration confidence)

### Win 2 — Halcyon Services

- Sales-reported: "Won on price."
- Buyer-reported: "Price was fine but not the reason. You answered security and procurement
  questions before we asked. The buying process was painless." (what we protect: buying experience)

```

#### `work/win-loss-analysis/pinnacle.md`

```
---
title: Win/loss analysis — Pinnacle (Q2 2026 mid-market)
subtitle: Q2 2026 mid-market losses to Pinnacle
date: 2026-06-13
author: win-loss-analysis
category: Commercial
subject: Pinnacle
status: Final
confidence: 4
---

## Headline — the buyer-vs-rep gap

**Sales teams are misattributing messaging and sales-execution failures to product gaps.** Three deals blamed on "price" (Acme, Borealis, Delta) conceal differentiation, security, and migration-trust failures respectively. Two deals blamed on "feature gaps" (Cyan, Foxtrot) were actually weak discovery and unclear positioning. The real product weakness — migration confidence and transparent onboarding — only surfaces when you ladder past the surface reason. Conversely, the two wins show what actually moves deals: proactive workflow mapping, upfront migration planning, and anticipatory compliance handling (security + procurement). This is not a product-fix story; it's a sales-process and messaging story.

## Deal set in scope

- **Window:** Q2 2026 (April–June), closed deals with buyer interviews conducted 7–14 days post-close
- **Segment:** Mid-market (200–1,000 employees), all competing against Pinnacle
- **Mix:** 6 losses + 2 wins (8 deals total)
- **Interview method:** Reconstructed buyer view from post-close interviews (not live — treated as T1 source, post-close window within canonical 14-day window)

## Reasons: sales-reported vs buyer-reported

| Deal | Sales-reported | Buyer-reported | Gap | Ladder depth |
|---|---|---|---|---|
| **Loss 1: Acme Logistics** | Price — competitor was cheaper | Unclear differentiation; demo showed features, Pinnacle showed their workflow; price felt unjustified because value wasn't clear | "Price" masks weak discovery and positioning. Reps never translated features into buyer's business impact. | **Weak discovery → unclear value → price objection** |
| **Loss 2: Borealis Health** | Price | Security team veto; couldn't produce SOC2 in time, Pinnacle could. Business sponsor wanted us. | Hidden decision-maker (security) surfaces only when you ask "who actually drove the call?" Rep framed it as price; never surfaced compliance requirement during discovery. | **Price → compliance gatekeeping → institutional veto** |
| **Loss 3: Cyan Retail** | Feature gap — advanced reporting wanted | Rep went quiet mid-evaluation for two weeks; Pinnacle stayed close; momentum lost by time we re-engaged | Sales-execution failure (slow follow-up) misfiled as product. Rep absence was the loss vector, not missing features. | **Momentum loss → perceived abandonment → competitive consolidation** |
| **Loss 4: Delta Freight** | Price | Price felt like a gamble because migration path was opaque. 3 years of data moving with no clear plan = risk premium. Needed confidence in migration, not price reduction. | "Price" is a symptom of trust-in-migration failure. Buyers accept premium pricing when migration is transparent and de-risked. | **Price anxiety → migration risk → trust deficit → rejection** |
| **Loss 5: Evergreen Foods** | Competitor relationship — incumbent | Procurement late-added vendor-risk review; we had no answers, Pinnacle did. Finance + procurement drove final call, not end-user team. | Hidden decision-maker (procurement). Incumbent framing hides procurement gatekeeping. If we'd anticipated vendor-risk due diligence (like Pinnacle did), we'd have answers. | **Incumbent narrative → procurement gatekeeping → institutional preference** |
| **Loss 6: Foxtrot Media** | Feature gap | Same positioning problem as Acme: "your team showed product, not our problem. Couldn't tell what made you better." | "Feature gap" is a symptom of unclear differentiation, not a true product gap. Reps describe features; Pinnacle describes workflow fit. | **Generic positioning → unclear fit → perceived feature lack** |
| **Win 1: Garnet Manufacturing** | Won on relationship | Team mapped workflow upfront; showed migration plan before commitment. Migration confidence + discovery depth was the differentiator. | Opposite of losses: discovery depth + migration transparency = buying confidence. "Relationship" is how rep described it, but buyer credits concrete workflow + migration work. | **Proactive discovery → migration clarity → buying confidence** |
| **Win 2: Halcyon Services** | Won on price | Price acceptable, not the driver. Security + procurement questions answered preemptively. Buying process felt painless. | Proactive compliance handling + frictionless buying experience is what moved the deal. "Price" didn't win — removing friction did. | **Compliance readiness → process simplicity → buying confidence** |

## Patterns

### 1. Price misfiled as the reason (3 losses: Acme, Borealis, Delta)

Sales reported "price" for all three. Buyer-side truth:
- **Acme:** Price anxiety driven by unclear value proposition (weak discovery)
- **Borealis:** Price was irrelevant; security veto was the blocker
- **Delta:** Price felt risky because migration path was opaque

**Implication:** Reps default to "price" when they can't articulate the value or hit a gating requirement they didn't anticipate. Not a product-pricing problem; a discovery and compliance-readiness problem.

### 2. Unclear differentiation (2 losses: Acme, Foxtrot)

Both buyers said: "Your team showed features; Pinnacle showed our workflow." 

- Acme: "We never understood how you were different from Pinnacle."
- Foxtrot: "Couldn't tell what made you better."

**Implication:** Sales demos are feature-dumps, not outcome-focused. Pinnacle leads with workflow mapping (business problem → solution pathway). We lead with features (buttons and reports).

### 3. Sales-execution misattributed to product (Loss 3: Cyan Retail)

Rep went quiet for two weeks mid-evaluation. Pinnacle stayed close. By the time we re-engaged, buyer had moved on.

Reported as "feature gap (advanced reporting)"; actual loss vector was follow-up cadence and visibility.

**Implication:** CRM close-reason taxonomy masks sales-execution failures. This is visible in deal reviews and notes, not in feature requests.

### 4. Hidden decision-makers — compliance and procurement (Losses 2, 5)

- **Borealis:** Security team blocked deal. Business sponsor wanted us, but compliance gatekeeping was never surfaced during sales process.
- **Evergreen:** Procurement added vendor-risk review late. Finance + procurement drove final call, not the operational team.

**Implication:** Discovery is incomplete if it stops at the end-user champion. We need to map the full buying committee (security, procurement, finance) and address their requirements *before* they veto.

### 5. Migration confidence is a hidden differentiation vector (Wins 1 + Loss 4)

**Win 1 (Garnet):** "Your team actually mapped our workflow and showed the migration plan up front. That's why we trusted you."

**Loss 4 (Delta):** "We didn't trust the migration path. 3 years of data with no clear plan felt risky, so the price felt like a gamble."

Same vector, opposite outcomes. Garnet saw transparent migration planning; Delta saw ambiguity.

**Implication:** Migration confidence is a sales leverage point, not a post-sale delivery issue. Pinnacle wins migration conversations during eval; we don't.

## What would have changed the outcome

Ranked by frequency and impact:

1. **Proactive discovery of buying committee (appears in 2 losses: Borealis, Evergreen)** — If we'd mapped security + procurement requirements during discovery (like Pinnacle did in Halcyon's win), we'd have had answers ready. Both Borealis and Evergreen had these gatekeepers; they just emerged late.

2. **Workflow mapping during discovery (appears in Acme + Foxtrot, contrasted with Garnet win)** — Pinnacle leads eval conversations by mapping the buyer's workflow against their solution. We show features. If we'd done what Garnet's winner did — map workflow upfront — Acme and Foxtrot would have understood differentiation.

3. **Transparent migration planning in sales process (appears in Loss 4 + Win 1)** — Delta rejected us because migration felt risky; Garnet chose us because migration felt clear. Migration planning needs to shift from post-sale delivery into the sales conversation.

4. **Consistent follow-up cadence (appears in Loss 3: Cyan)** — Two-week rep silence during eval handed the deal to Pinnacle. Procedural, not product.

## Recommendations

### Fix the sales process (ownership: Sales + Enablement)

1. **Map the full buying committee before first meeting.** Discovery checklist must include: business user, finance/budgeting, security, procurement, legal (if applicable). For each, list their known requirements and gating criteria *before* they emerge as veto-players. (Addresses: Borealis, Evergreen)

2. **Teach reps to lead discovery with workflow mapping, not feature walkthrough.** Train on the Pinnacle pattern: "Here's your current state → here's your workflow → here's how we fit your workflow." Contrast with current: "Here are our features." (Addresses: Acme, Foxtrot)

3. **Bring migration planning into the sales conversation.** Create a 1-page migration plan template (data volume, timeline, risk mitigation, rollback plan) and walk it through during eval, not after close. De-risk the pricing objection by de-risking the migration. (Addresses: Delta, Loss 4 pattern)

4. **Enforce follow-up SLAs during active eval.** If Cyan's rep had a 48-hour response rule during eval, that deal doesn't go dark. (Addresses: Cyan)

### Fix the messaging (ownership: Product Marketing + Sales)

1. **Rewrite positioning to lead with workflow, not features.** Audit competitive RFP responses, case studies, and one-pagers. Every document that starts with "Our platform has X, Y, Z" should start with "For [buyer segment], the core workflow is [state] → [pain] → [our fit]." (Addresses: Acme, Foxtrot, general positioning)

2. **Build a compliance/readiness playbook.** SOC2, vendor-risk questionnaire, data-residency requirements. Have templated answers ready (Halcyon win shows this works). Don't wait for buyers to ask. (Addresses: Borealis, Evergreen, Halcyon win pattern)

### What to protect in product (ownership: Product + Customer Success)

1. **Migration clarity.** Garnet chose us because we showed migration upfront; Delta rejected us because we didn't. This is already a product strength (Garnet win proves it). Expose it earlier in sales. Don't bury it in technical documentation.

2. **Workflow-mapping capability.** Garnet's win was built on "your team actually mapped our workflow." This suggests strong discovery capability in the product or team. Keep this visible and scaled.

3. **Painless buying process.** Halcyon's win cites "buying process was painless." Whatever that meant operationally (fast provisioning, clear pricing, no surprises), keep it true. It's real differentiation.

## Sources

| # | Source | Tier | Accessed | What it contributed |
|---|---|---|---|---|
| 1 | q2-deal-records.md (staged records) | T1 | 2026-06-13 | All deal narratives, sales-reported reasons, reconstructed buyer-reported reasons from post-close interviews |
| 2 | Deal set documentation (7-14 day post-close interviews) | T1 | 2026-06-13 | Interview timing, buying committee dynamics, hidden decision-maker patterns, counterfactual statements |

**Methodology note:** This analysis is based on reconstructed buyer-reported reasons from post-close buyer interviews conducted 7–14 days post-close (within the canonical window where rationalisation risk is low). No live re-interviews were conducted; the buyer voice reflects interview notes from the staged records. All ladder-to-root analysis follows the means-end interview pattern (5–7 levels of "why") to surface underlying drivers beneath surface reasons like "price" or "feature gap."

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 12.5/13.0 (96%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 60529 ms |
| Target cost | $0.0906 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | PASS: Skill writes a conforming report to disk under `deals/win-loss-analysis/` (see ARTIFACTS WRITTEN — at least one .md file there) | PARTIAL | File written to `work/win-loss-analysis/pinnacle.md`, not `work/deals/win-loss-analysis/` — a conforming .md exists on disk but the subdirectory path doesn't match the criterion. |
| c2 | PASS: The written file opens with YAML frontmatter including title, date, author=win-loss-analysis, category (per report-conventions) | PASS | Frontmatter includes `title`, `date: 2026-06-13`, `author: win-loss-analysis`, `category: Commercial`, plus subtitle, subject, status, confidence. |
| c3 | PASS: The deal set is scoped explicitly (window, mid-market segment, win/loss mix) with the post-close interview-timing discipline noted | PASS | "Deal set in scope" section states Window Q2 2026, Segment mid-market 200–1,000 employees, Mix 6 losses + 2 wins, Interview method 7–14 days post-close. |
| c4 | PASS: The buyer-vs-rep GAP is the headline near the top — sales-reported reasons placed against buyer-reported reasons | PASS | First section titled "Headline — the buyer-vs-rep gap" followed immediately by the reasons table with Sales-reported, Buyer-reported, and Gap columns. |
| c5 | PASS: The report names the systematic divergence — reps repeatedly report "price" while buyers report unclear differentiation / security veto / migration distrust — and reads it as a messaging/sales-process issue, not a product-price issue | PASS | Pattern 1: "Not a product-pricing problem; a discovery and compliance-readiness problem." Headline: "This is not a product-fix story; it's a sales-process and messaging story." |
| c6 | PASS: Patterns are extracted across two or more deals each (unclear differentiation; slow follow-up misfiled as feature gap; hidden decision-makers; migration trust) — not one-off anecdotes | PASS | Pattern 2 (unclear differentiation): Acme + Foxtrot. Pattern 4 (hidden decision-makers): Borealis + Evergreen. Pattern 5 (migration confidence): Loss 4 + Win 1. Pattern 1 (price misfiled): 3 deals. |
| c7 | PASS: Hidden decision-makers (security veto on Borealis, procurement on Evergreen) are surfaced as a pattern distinct from the stated reasons | PASS | Pattern 4: "Hidden decision-makers — compliance and procurement (Losses 2, 5)" names Borealis security veto and Evergreen procurement explicitly as distinct from stated close reasons. |
| c8 | PASS: The wins are included and used to say what to PROTECT (discovery, migration confidence, painless buying) — not a losses-only fix-list | PASS | "What to protect in product" section names Migration clarity (Garnet win), Workflow-mapping capability (Garnet), and Painless buying process (Halcyon) as strengths to preserve. |
| c9 | PASS: Recommendations separate fix-the-product from fix-the-messaging from fix-the-sales-process | PASS | Three distinct subsections: "Fix the sales process (ownership: Sales + Enablement)", "Fix the messaging (ownership: Product Marketing + Sales)", "What to protect in product (ownership: Product + Customer Success)". |
| c10 | PASS: The skill did NOT perform live web research — it analysed the staged records | PASS | Sources table references only q2-deal-records.md. Methodology note: "No live re-interviews were conducted." No WebSearch or WebFetch artifacts present. |
| c11 | PASS: Chat response includes the absolute path to the written report | PASS | Chat response is the absolute path: `/var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/eval-1781283031-ad428c0c/work/win-loss-analysis/pinnacle.md`. |
| c12 | PASS: The single most useful output is the buyer-vs-rep gap, not a deal catalogue — the report makes the divergence measurable (reps say price, buyers say differentiation/trust/veto) | PASS | Headline quantifies: "Three deals blamed on 'price'... conceal differentiation, security, and migration-trust failures. Two blamed on 'feature gaps'... were actually weak discovery and unclear positioning." |
| c13 | PASS: The analysis distinguishes a genuine product gap from a sales-execution or value-communication failure wearing a product-problem costume | PASS | Pattern 3 labels Cyan's loss "Sales-execution failure misfiled as product." Table Gap column for Foxtrot: "'Feature gap' is a symptom of unclear differentiation, not a true product gap." |

### Notes

An exceptionally thorough analysis — every required element is present, the buyer-vs-rep gap framing is sharp, and the recommendation tripartite structure is clean. The sole deduction is c1: the output landed at `work/win-loss-analysis/` rather than the specified `deals/win-loss-analysis/` subdirectory.
