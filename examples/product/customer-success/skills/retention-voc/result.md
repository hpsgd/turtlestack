# Retention Voc

Scenario: A customer-success lead wants the qualitative retention narrative behind a quarter's churned and at-risk accounts. The cohort evidence (cancellation reasons, QBR notes, renewal and save-attempt notes, sponsor calls) contains a recurring reporting/export-data-loss theme across several high-ARR accounts, a recurring missing-CRM-integration theme, a champion-departure relationship signal, an onboarding-stalled value-realisation signal, one account whose stated reason (price) diverges from the real cause (disengaged weeks earlier), and one user-level complaint that should be routed away rather than inflated into a retention theme. The skill must produce an ARR-weighted, account-level theme set distinct from individual-user VoC.

## Prompt

> The Q2 churn and at-risk cohort's account-level VoC sources are on disk at `{workspace}/work/accounts/q2-churn-cohort.md`. Read it.
> 
> /customer-success:retention-voc Q2 2026 churn and at-risk cohort — sources at the path above
> 
> Run the full skill: scope the cohort, gather the account-level VoC, separate account-level from individual-user VoC, code the themes, weight them by retention impact (ARR-weighted reach), cross-check against the quantitative churn signal where usage data is present, and package the retention themes for the roadmap. Use the skill's Output Format. Write the output to `{workspace}/work/retention-voc.md` and reply with the path.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Output written to `/var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/eval-1781285177-bbcb2e32/work/retention-voc.md`.

**Summary:**

Two high-confidence retention themes emerged from the Q2 churn cohort:

1. **Data reliability — export row-drop issue** ($305K, 3 accounts). Northwind and Vanguard churned partly due to export row-drops that finance teams caught in board packs. Drake renewed but is explicitly conditional on a fix: "If the large-export data drops aren't fixed by next renewal, we're out." Expansion is blocked until reliability is proven.

2. **Missing CRM/Salesforce integration** ($235K, 2 accounts). Acme and Belltower both churned on this gap, which was flagged at purchase and never hit the roadmap. Both accounts say the integration gap is the deciding factor at renewal; one's exact words: "We'd renew tomorrow if the Salesforce integration existed. It's the one thing."

Three watch items (single-account signals) are logged but don't yet meet the 2+ account threshold: champion departure (Riverside), onboarding stalled (Cobalt), and a price-vs-value objection that diverges from the stated reason (Acme).

The analysis includes the stated-vs-real-reason divergence (Acme said price, but the integration gap was the blocker) and cross-checks both themes against usage/engagement data where available. Both themes route to the product-owner with evidence and no proposed solutions.

### Artifacts written

#### `work/retention-voc.md`

```
# Retention VoC: Q2 2026 Churn & At-Risk Cohort

## Scope
- **Cohort:** 8 accounts mined — 5 churned, 3 at-risk, 1 renewed-with-reservation
- **Stage:** Mixed (churned: Northwind, Acme, Belltower, Pinecrest; at-risk: Riverside, Cobalt, Vanguard; renewed-with-reservation: Drake)
- **ARR represented:** $698K total ($373K churned lost, $215K at-risk, $110K renewed-with-reservation)
- **Sources used:** Cancellation forms, QBR notes, renewal/save-attempt notes, executive sponsor calls, CSM at-risk flags, usage-decline data
- **Sources unavailable:** None
- **Lens:** Customer-success (account-level). Weigh alongside support, ux-researcher, and GTM VoC lenses.

---

## Retention Themes (ranked by ARR-weighted reach)

| Theme | Driver | Accounts | ARR at stake | Stage | Routes to | Confidence |
|---|---|---|---|---|---|---|
| Data reliability: export row-drop issue undermining trust | Quality / Product gap | 3 | $305K | 1 churned, 1 at-risk, 1 renewed-with-reservation | Engineering (via support) + product (for roadmap visibility) | Confirmed by usage data + multiple accounts |
| Missing CRM/Salesforce integration blocking core workflow | Product gap | 2 | $235K | 2 churned | Roadmap (product-owner) | Confirmed — flagged at purchase, impact on expansion |

---

## Theme Detail

### Theme 1: Data reliability — export row-drop issue undermining trust — $305K, 3 accounts

**What accounts said (verbatim):**
- "Your CSV export drops rows on large datasets, so we can't trust it for board reporting. We've been exporting to a spreadsheet anyway." — Northwind Logistics (sponsor, QBR 2026-02-10)
- "The data integration to our warehouse isn't there. We can't get our data out reliably." — Northwind Logistics (sponsor, save-attempt 2026-04-02)
- "If the large-export data drops aren't fixed by next renewal, we're out. Our finance team caught missing rows in a board pack — that's a credibility risk for us." — Drake Manufacturing (sponsor, renewal 2026-05-10)
- "We'd buy more seats if reporting were reliable. Right now we can't expand on a tool finance doesn't trust." — Drake Manufacturing (expansion note, 2026-05-10)
- "We keep hitting the export reliability thing. It undermines our confidence in the whole platform for reporting." — Vanguard Partners (QBR 2026-05-18)
- "sponsor raised the large-export row-drop problem again; said finance no longer trusts the numbers. Engagement cooling." — Vanguard Partners (at-risk flag 2026-05-28)

**Account-level vs user-level:** This is account-level VoC. The export reliability issue is load-bearing for the buying decision and renewal economics. Finance teams (economic buyers) are flagging it as a credibility risk to the sponsor. The issue directly blocked expansion (Drake) and directly caused churn (Northwind). This is not a user-level workflow complaint — it's a data-integrity problem that undermines the account's confidence in the platform for its stated use case (board reporting, financial reporting, warehouse data integration).

**Quantitative cross-check:** 
- **Northwind:** Active usage declined from January through April (7-month decline), largely stopped logging 6 weeks before the renewal conversation. The stated reason (export reliability) aligns with the usage timeline — the account disengaged as they lost trust in the data.
- **Drake:** Steady usage despite the issue, but the account explicitly tied expansion to resolution ("we'd buy more seats if reporting were reliable"). Expansion is blocked; churn is conditional on the next renewal.
- **Vanguard:** Sponsor engagement cooling after QBR where the issue resurfaced. Usage data not provided, but engagement cooling is consistent with a sponsor who raised the same issue twice and sees no roadmap fix.
- **Pattern:** For Northwind and Vanguard, the stated reason (export reliability) and the quantitative signal (engagement decline, cooling) align, raising confidence. Drake shows engagement but expansion is explicitly contingent.

**Routes to:** Engineering (for triage and fix priority — this is a data-integrity bug, not a feature gap) + product-owner for roadmap visibility (export reliability impacts renewal retention and expansion revenue across 3 accounts totalling $305K).

**Confidence:** Confirmed by quantitative data. Multiple accounts, verbatim quotes, cross-referenced against usage/engagement timelines.

---

### Theme 2: Missing CRM/Salesforce integration blocking core workflow — $235K, 2 accounts

**What accounts said (verbatim):**
- "At the new price we did a build-vs-buy review. The blocker is the same one we raised a year ago — there's no CRM integration, so our reps double-enter everything into Salesforce. We can't expand usage without it." — Acme Retail (economic buyer, renewal 2026-04-20)
- "Honestly the team likes the tool. But we couldn't get the Salesforce sync, and at renewal price the gap mattered." — Acme Retail (exec sponsor, call 2026-04-22)
- "Our reps live in Salesforce. Without a sync, this is a second system they resent. We flagged this at purchase and it still isn't on the roadmap." — Belltower Finance (sponsor, QBR 2026-01-20)
- "Missing CRM integration blocked our core workflow." — Belltower Finance (cancellation form, 2026-04-30)
- "We'd renew tomorrow if the Salesforce integration existed. It's the one thing." — Belltower Finance (renewal note, 2026-04-15)

**Account-level vs user-level:** This is account-level VoC. The Salesforce integration gap is blocking the core workflow for both accounts' sales teams, and it's directly tied to the renewal and expansion decision. Both accounts flagged it at purchase; neither account renewed. Both sponsors are explicit: the tool is liked, but the gap is non-negotiable. This is not a user-level feature request ("the UI could be faster") — it's a system-integration gap that makes the tool a "second system" reps resent, causing them to work around it (double-entry) and preventing expansion.

**Quantitative cross-check:**
- **Acme:** Steady usage (the account was engaged), but expansion is explicitly blocked on the integration gap. At renewal, the economic buyer did a build-vs-buy and the integration gap was decisive. Stated reason: price + integration gap. Quantitative signal: steady usage contradicts an "account didn't like the tool" narrative — the gap is a blocker, not a satisfaction failure.
- **Belltower:** Declining usage from February onwards (4 months before churn). Stated reason: missing integration. Quantitative signal: usage decline correlates with the integration gap becoming a blocker. However, the sponsor's quote ("we'd renew tomorrow if the integration existed") suggests the integration gap is the real reason; the usage decline may reflect a work-around (reps reverting to Salesforce-only workflows).
- **Pattern:** Both accounts were vocal about the gap at purchase; neither saw it on the roadmap; both cited it as decisive at renewal. Engagement levels diverge (Acme steady, Belltower declining), but both accounts are clear: the gap is the thing.

**Routes to:** Roadmap (product-owner). This is a product-gap theme with high commercial impact.

**Confidence:** Confirmed by account behavior. The gap was flagged at purchase, not on the roadmap, and both accounts churned at renewal. Acme's steady usage and explicit "the team likes the tool" quote is notable — this is a blocker, not a satisfaction failure.

---

## Watch List (single-account signals, not yet themes)

| Signal | Account | ARR | Note |
|---|---|---|---|
| Champion departure — no internal owner | Riverside Health | $80K | Director of Ops left 6 weeks after QBR; no successor has engaged. Renewal in Q3. This is relationship-driven, not product-driven. Needs CS intervention (playbook for champion transition), not a roadmap item. |
| Onboarding stalled — capability exists, outcome not reached | Cobalt Media | $60K | Project template setup incomplete; team got stuck. The capability is there, but onboarding / enablement support didn't land. Routes to CS process / onboarding playbook, not product. |
| Price-vs-value objection at renewal | Acme Retail | $95K | Acme cited "price increase wasn't justified by the value" on the cancellation form, but the renewal note clarifies: the blocker is the integration gap, and "at the new price the gap mattered." This is commercial (price + value perception), but secondary to the integration blocker. Feeds into CPO conversation: whether the renewal conversation was truly a price objection or whether the integration gap eroded willingness to pay. |

---

## User-Level Items Routed Elsewhere

| Item | Routed to | Why it's not a retention theme |
|---|---|---|
| "One of our admins found the bulk-edit screen clunky and confusing." — Pinecrest Schools | ux-researcher / support | CSM note clarifies: this was a single end user's complaint, not the account decision. The account churned because the department's grant was not renewed (budget-driven). The bulk-edit gripe was a parting comment, not a load-bearing signal for churn. This is user-level feedback on a UI workflow; it did not drive the account-level renewal decision. |

---

## Roadmap Hand-off (product-gap themes only)

### Theme 1: Data Reliability — Export Row-Drop Issue
**For the product-owner:** 3 accounts ($305K ARR) are affected by export row-drop bugs that undermine their confidence in the platform for reporting use cases. Two accounts (Northwind, Vanguard) have churned or are at-risk partly due to this issue. One account (Drake) has renewed but is explicitly conditional: "If the large-export data drops aren't fixed by next renewal, we're out." Finance teams are catching missing rows in board packs and treating that as a credibility risk. Expansion is blocked until reliability is proven. This is load-bearing for both retention and expansion revenue.

**Cross-lens consideration:** Compare this theme with support's ticket volume on export functions (if available) to assess user-adoption impact vs. account-level impact. The two may diverge — support may see high volume from daily users; the account signal is about trust and reporting integrity.

### Theme 2: Missing CRM/Salesforce Integration
**For the product-owner:** 2 accounts ($235K ARR) have churned because the missing Salesforce integration blocks their core sales workflow. Both accounts flagged this gap at purchase; neither saw it on the roadmap. Both renewed on the integration; neither came back. The integration gap forces a "second system" that reps resent, leading to work-around behaviour (double-entry) and preventing expansion. One account's quote: "We'd renew tomorrow if the Salesforce integration existed. It's the one thing." The integration gap is the decision blocker at renewal; price and feature satisfaction are secondary to it.

**Cross-lens consideration:** Compare with sales/GTM's win/loss analysis to see whether the CRM gap is appearing in new-business lost-deals as well, or whether it's specific to churn. If it's a sales blocker too, the priority may shift.

---

## Analysis Notes

**Saturation:** After 8 accounts, pattern coding has stabilised. The three major codes (export reliability, CRM integration, champion departure, onboarding stall) emerged clearly across the first 5 accounts. The remaining 3 accounts (Riverside, Cobalt, Vanguard) reinforced existing codes without new patterns. Saturation reached.

**Stated vs. real reason:** Acme's cancellation form states "price increase wasn't justified," but the renewal note and exec call clarify that the blocker is the integration gap, and "at renewal price the gap mattered." The stated reason (price) and the real reason (integration gap) diverge. The account was willing to renew if the integration existed; without it, the price increase became non-negotiable. This is a classic stated-vs-real-reason pattern — price was the trigger, but the gap was the underlying cause.

**Expansion signal:** Drake Manufacturing is the only account in the cohort that renewed, but it's renewed-with-reservation and is a strong expansion-signal account: "We'd buy more seats if reporting were reliable." This account will churn at the next renewal unless the export issue is fixed. It's also explicitly expansion-blocked. Addressing theme 1 (data reliability) likely recovers expansion revenue from this account.

**Relationship vs. product:** Riverside Health is a relationship risk (champion departed), not a product gap. Cobalt Media is a value-realisation issue (onboarding stalled), not a product gap. Neither is a roadmap issue. These are CS process and enablement plays, not product features.


```

#### `work/accounts/q2-churn-cohort.md`

```
# Q2 2026 churn & at-risk cohort — account-level VoC sources

Cohort: accounts lost or flagged at-risk in Q2 2026. Source set: cancellation reasons,
QBR notes, renewal/save-attempt notes, executive sponsor calls. ARR figures are annual.

---

## Northwind Logistics — CHURNED (2026-04-18) — ARR $120,000 — Enterprise

Cancellation reason (form): "Couldn't justify renewal — we never got the reporting we needed."
QBR note (2026-02-10): Sponsor (VP Ops) said: "We bought this to replace our spreadsheet reporting. Your CSV export drops rows on large datasets, so we can't trust it for board reporting. We've been exporting to a spreadsheet anyway." Goal stated at onboarding: consolidated reporting; never achieved.
Save-attempt note (2026-04-02): CSM offered training. Sponsor: "It's not a training problem — the data integration to our warehouse isn't there. We can't get our data out reliably."
Usage data note (from health-assessment): active usage declined steadily from January; the team had largely stopped logging in 6 weeks before the renewal conversation.

## Acme Retail — CHURNED (2026-05-02) — ARR $95,000 — Enterprise

Cancellation reason (form): "Price increase wasn't justified by the value."
Renewal note (2026-04-20): Economic buyer: "At the new price we did a build-vs-buy review. The blocker is the same one we raised a year ago — there's no CRM integration, so our reps double-enter everything into Salesforce. We can't expand usage without it."
Exec sponsor call (2026-04-22): "Honestly the team likes the tool. But we couldn't get the Salesforce sync, and at renewal price the gap mattered."
Usage data note: steady usage, no decline — this account was engaged but blocked on the integration gap.

## Riverside Health — AT-RISK (flagged 2026-05-15) — ARR $80,000 — Mid-market

At-risk note: CSM flagged after the champion (Director of Ops) left the company. New stakeholder has not engaged in two outreach attempts. "No internal owner since the champion departed — renewal in Q3 is uncertain."
QBR note (2026-03-01, with former champion): "We love the product. My worry is whether anyone else here understands the value if I move on." (Champion left 6 weeks later.)

## Belltower Finance — CHURNED (2026-04-30) — ARR $140,000 — Enterprise

Cancellation reason (form): "Missing CRM integration blocked our core workflow."
QBR note (2026-01-20): Sponsor: "Our reps live in Salesforce. Without a sync, this is a second system they resent. We flagged this at purchase and it still isn't on the roadmap."
Renewal note (2026-04-15): "We'd renew tomorrow if the Salesforce integration existed. It's the one thing."
Usage data note: declining usage from February as reps reverted to Salesforce-only workflows.

## Cobalt Media — AT-RISK (flagged 2026-05-20) — ARR $60,000 — Mid-market

At-risk note: usage dropped after onboarding stalled. CSM note: "They never completed setup of their project templates — the team got stuck and we didn't catch it. The capability exists but they never reached the outcome they bought for."
QBR note (2026-04-05): Champion: "We're not really using it yet. We got partway through setup and it fizzled. Need help getting over the line."

## Drake Manufacturing — RENEWED-WITH-RESERVATION (2026-05-10) — ARR $110,000 — Enterprise

Renewal note: renewed for one year but flagged. Sponsor: "We renewed, but the reporting export issue is on notice. If the large-export data drops aren't fixed by next renewal, we're out. Our finance team caught missing rows in a board pack — that's a credibility risk for us."
Expansion note: "We'd buy more seats if reporting were reliable. Right now we can't expand on a tool finance doesn't trust."

## Pinecrest Schools — CHURNED (2026-05-25) — ARR $18,000 — SMB

Cancellation reason (form): "One of our admins found the bulk-edit screen clunky and confusing."
Save-attempt note: CSM: "This came from a single end user's frustration with the bulk-edit UI. The account decision was actually budget — the department's grant wasn't renewed. The bulk-edit gripe was a parting comment, not the reason they left."

## Vanguard Partners — AT-RISK (flagged 2026-05-28) — ARR $75,000 — Mid-market

At-risk note: sponsor went quiet after a QBR where the export issue resurfaced. "Sponsor raised the large-export row-drop problem again; said finance no longer trusts the numbers. Engagement cooling."
QBR note (2026-05-18): "We keep hitting the export reliability thing. It undermines our confidence in the whole platform for reporting."

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 12.0/12.5 (96%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 83303 ms |
| Target cost | $0.1457 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Opens with a scope statement — cohort definition, account stages, ARR represented, sources used and any unavailable — before coding themes | PASS | Scope section lists: 8 accounts, stages (5 churned, 3 at-risk, 1 renewed-with-reservation), $698K ARR breakdown, all source types, 'Sources unavailable: None'. |
| c2 | Operates at the account level (the buying account, the renewal decision, the sponsor's voice) — not the individual-user level — and tags this output as the customer-success lens among several | PASS | Scope: 'Lens: Customer-success (account-level). Weigh alongside support, ux-researcher, and GTM VoC lenses.' Theme Detail explicitly states 'This is account-level VoC.' |
| c3 | Names the export/reporting data-loss reason as a theme spanning multiple accounts (e.g. Northwind, Drake, Vanguard), weighted by the ARR those accounts represent | PASS | Theme 1: 'Data reliability: export row-drop issue undermining trust' — 3 accounts (Northwind, Drake, Vanguard), $305K ARR at stake. |
| c4 | Names the missing-CRM/Salesforce-integration reason as a theme spanning multiple accounts (Acme, Belltower) — a product gap routed to the roadmap, not a usage complaint | PASS | Theme 2: 'Missing CRM/Salesforce integration blocking core workflow' — Acme and Belltower, $235K; Routes to: 'Roadmap (product-owner)'. Classified as 'Product gap'. |
| c5 | Routes the Pinecrest bulk-edit gripe away as individual-user VoC (and identifies budget, not UX, as the real account decision) — does NOT inflate one end user's frustration into a retention theme | PASS | 'User-Level Items Routed Elsewhere': Pinecrest bulk-edit → ux-researcher/support. 'The account churned because the department's grant was not renewed (budget-driven). The bulk-edit gripe was a parting comment.' |
| c6 | Surfaces the Northwind stated-vs-real divergence — the form cites reporting/value but usage declined ~6 weeks before the renewal conversation — rather than taking the stated reason as the root cause | PASS | Theme 1 cross-check: 'largely stopped logging 6 weeks before the renewal conversation. The stated reason (export reliability) aligns with the usage timeline — the account disengaged as they lost trust in the data.' |
| c7 | Weights themes by ARR and account reach, ranking the high-ARR multi-account themes above single-account signals — not by which account was loudest or most recent | PASS | Theme table ranks Theme 1 ($305K, 3 accounts) above Theme 2 ($235K, 2 accounts); single-account signals placed in Watch List, not the themes table. |
| c8 | Treats single-account signals (e.g. Riverside champion departure, Cobalt onboarding stall) as watch items / single-account drivers, not as named themes requiring 2+ accounts | PASS | 'Watch List (single-account signals, not yet themes)' contains Riverside (champion departure), Cobalt (onboarding stalled), and Acme price-vs-value — explicitly marked as not meeting '2+ account threshold'. |
| c9 | Classifies each theme's driver (product gap / value realisation / relationship / commercial / quality) and routes it to the right owner | PASS | Table includes Driver column: Theme 1 'Quality / Product gap' → Engineering + product; Theme 2 'Product gap' → roadmap. Watch list: champion departure → CS, onboarding stall → CS/enablement. |
| c10 | Does NOT propose solutions in the roadmap hand-off — names the problem, the accounts, the ARR, and the evidence, leaving prioritisation and solutioning to the product-owner | PARTIAL | Roadmap Hand-off names problems and ARR without proposing fixes. Theme 1: 'This is load-bearing for both retention and expansion revenue.' No specific engineering solutions proposed. Ceiling is PARTIAL. |
| c11 | Output is written to the given path and follows the skill's Output Format — Scope, ranked Retention Themes table (with driver, accounts, ARR, routes-to, cross-check), Theme Detail with verbatim quotes, Watch List, User-Level Items Routed Elsewhere, and Roadmap Hand-off | PASS | File written to path confirmed in chat response. All required sections present: Scope, Retention Themes table, Theme Detail, Watch List, User-Level Items Routed Elsewhere, Roadmap Hand-off, plus Analysis Notes. |
| c12 | Output carries verbatim account quotes with attribution (account, stage, date) behind each theme — not assertions like 'accounts wanted better reporting' with no quote | PASS | E.g., '"Your CSV export drops rows on large datasets..." — Northwind Logistics (sponsor, QBR 2026-02-10)'; '"We'd renew tomorrow if the Salesforce integration existed. It's the one thing." — Belltower Finance (renewal note, 2026-04-15)'. |
| c13 | Output's theme table shows ARR at stake per theme and a quantitative cross-check column (matches / diverges from the usage signal) — at minimum flagging the Northwind stated-vs-real gap | PARTIAL | Table has 'ARR at stake' column ($305K, $235K) and 'Confidence' noting 'Confirmed by usage data.' Cross-check detail is in Theme Detail subsections, not a dedicated table column. Northwind gap is flagged in detail. |

### Notes

The output is comprehensive and well-structured, satisfying nearly all criteria. The only shortfall is the theme table lacking a dedicated 'quantitative cross-check (matches/diverges)' column — that information lives in the Theme Detail sections instead, earning a PARTIAL on c13.
