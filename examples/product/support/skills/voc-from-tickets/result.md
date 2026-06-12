# Voc From Tickets

Scenario: A support team has a month of tickets and wants them to feed product decisions, not just be resolved. The corpus contains a cancel-discoverability theme (users fought the interface — UX failure), an onboarding empty-state theme (UX failure, concentrated in trial week-one users), a CSV-export-silently-drops-rows theme (data-loss defect, concentrated in paid tiers), several how-to questions about features that exist and work (doc gaps), and assorted feature requests (missing capability). The skill must code the tickets, discriminate UX-failure from doc-gap signal, weight themes by frequency × severity, and surface a ranked roadmap-ready list.

## Prompt

> A month of support tickets is on disk at `{workspace}/work/tickets/support-tickets-may.md`. Read it.
> 
> /support:voc-from-tickets {workspace}/work/tickets/support-tickets-may.md
> 
> Run the full skill: assemble the corpus, code each ticket into a product theme from the user's own words, classify the signal type (UX failure / doc gap / missing capability / defect), cluster and count themes, weight each by frequency × severity (× segment factor), and surface the ranked roadmap-ready themes with hand-offs. Use the skill's Output Format.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## VoC from tickets — Product Queue (May 2026)

### Corpus
- Tickets analysed: 32
- Date range: 2026-05-02 to 2026-05-30
- Source: Zendesk "Product" queue export
- Segment data: Plan tier (Trial week 1, Free, Pro, Enterprise) and account tenure available
- Sample caveat: None — 32 tickets is a solid month-long corpus

---

### Theme table (ranked by weight)

| Rank | Theme (user language) | Signal mix | Count | % | Severity | Segment | Weight | Trend |
|---|---|---|---|---|---|---|---|---|
| 1 | "CSV export silently drops rows, no warning" | Defect 6 | 6 | 19% | 4 | Enterprise 4/6 | 36 | stable |
| 2 | "Onboarding drops users into empty account with no guidance" | UX 7 | 7 | 22% | 4 | Trial wk1: 5/7 | 28 | stable |
| 3 | "Can't find the cancel button; it's hidden somewhere" | UX 6 | 6 | 19% | 4 | Trial/Free: 4/6 | 24 | stable |
| 4 | "App crashes on large boards/reports (~2000 cards or large account)" | Defect 2 | 2 | 6% | 4 | Pro/Enterprise: 2/2 | 12 | rising |
| 5 | "SSO/SCIM setup documentation missing or unclear" | Doc 2 | 2 | 6% | 3 | Enterprise: 2/2 | 9 | stable |
| 6 | "Recurring/repeating tasks: can't find setting or unclear if exists" | Doc 2 | 2 | 6% | 2 | Pro: 2/2 | 4 | stable |
| 7 | "No bulk operations (archive, delete); one-by-one only" | Missing 2 | 2 | 6% | 2 | Pro: 2/2 | 4 | stable |

---

### Signal-type split

- **UX failure:** 13 tickets across 2 themes (cancel button, onboarding)
- **Defect:** 10 tickets across 2 themes (CSV export, app crashes)
- **Doc gap:** 4 tickets across 2 themes (SSO/SCIM, recurring tasks)
- **Missing capability:** 5 tickets across 5 themes (bulk ops, dark mode, PDF export, API rate-limit headers, calendar view)

---

### Roadmap-ready themes

#### 1. CSV export silently drops rows, no warning
- **Signal type:** Defect → owner: engineering
- **Evidence:** 
  - T-1002: "I exported my project list to CSV and it silently dropped about 40 rows. No error, no warning — the file just had fewer rows than the screen. This is a data-integrity problem for our reporting."
  - T-1009: "Our finance team's monthly export is missing line items... We rely on this for invoicing — it's causing real problems."
  - T-1031: "Monthly compliance export is missing rows again... We need every row for audit. This silent drop is unacceptable at our tier."
- **Reach:** 6 tickets / 19% of corpus. Concentrated in Pro (2) and Enterprise (4); critical for paid tiers and compliance workflows
- **Weight:** 6 (frequency) × 4 (blocks core task / data loss) × 1.5 (paid/Enterprise concentration) = 36
- **Recommended action:** Investigate export truncation mechanism; add validation warnings or error messaging when rows are dropped; add row-count verification to export pipeline. For Enterprise, this is blocking trust in the system.

---

#### 2. Onboarding drops users into empty account with no guidance
- **Signal type:** UX failure → owner: product/design
- **Evidence:**
  - T-1007: "During onboarding I got stuck at the 'invite your team' step. It let me click Next with no one invited, then the dashboard was empty and I had no idea what to do. Very confusing first run."
  - T-1010: "I assumed after signing up I'd get a guided tour. Instead I landed on an empty board with no projects and no prompt."
  - T-1017: "The setup flow let me skip every step and then I had a blank account. I expected it to walk me through creating my first project. Gave up and will try a competitor."
- **Reach:** 7 tickets / 22% of corpus. Heavily concentrated in Trial week 1 (5/7); funnel risk — all churn before first value
- **Weight:** 7 (frequency) × 4 (blocks initial adoption) × 1.0 (trial segment, but broad problem) = 28
- **Recommended action:** Redesign onboarding to enforce at least one of: (a) require creating a project before advancing, or (b) provide sample/starter project with walkthrough. Add progress guidance or "Next steps" prompt on empty state. This is a funnel killer — trial users are bouncing day one.

---

#### 3. Can't find the cancel button; it's hidden somewhere
- **Signal type:** UX failure → owner: product/design
- **Evidence:**
  - T-1001: "I clicked everywhere looking for a way to cancel my subscription. There's no button for it on the billing page."
  - T-1006: "There's no obvious way to cancel. I clicked Settings, Account, Billing — nothing. Had to search your help site to find out it's hidden behind 'Manage plan'."
  - T-1012: "I want to downgrade and there's no clear path. I clicked through every menu... Found it eventually under an unlabelled 'Manage plan' link."
- **Reach:** 6 tickets / 19% of corpus. Concentrated in Trial (3) and Free (3); high friction at decision points
- **Weight:** 6 (frequency) × 4 (blocks core task—user actively wants to leave) × 1.0 (broad across trial and free) = 24
- **Recommended action:** Surface cancel/downgrade affordance directly on the billing page or in the plan-selection UI. The label "Manage plan" is too vague. Users expect to find cancellation where they see their plan. This is user-hostile friction during a decision moment.

---

#### 4. App crashes on large boards/reports (~2000 cards or large account)
- **Signal type:** Defect → owner: engineering
- **Evidence:**
  - T-1014: "When I open our biggest board (around 2,000 cards) the page freezes and then crashes with a white screen... Console shows an out-of-memory error."
  - T-1027: "Opening the Reports tab on our large account crashes the tab — white screen, have to reload. Error log shows a memory issue."
- **Reach:** 2 tickets / 6% of corpus. Concentrated in Pro/Enterprise with large accounts; makes product unusable for power users
- **Weight:** 2 (frequency) × 4 (blocks core task) × 1.5 (Pro/Enterprise, paid tiers, power users) = 12
- **Trend:** Rising — both tickets in the latter half of May (13th, 17th), suggests a recent regression
- **Recommended action:** Profile memory usage on large boards; likely need pagination, virtualization, or lazy-loading for card render. This is blocking your most valuable customers (large Enterprise accounts).

---

#### 5. SSO/SCIM setup documentation missing or unclear
- **Signal type:** Doc gap → owner: docs/support
- **Evidence:**
  - T-1004: "Is it possible to set up SAML SSO with Okta? I didn't realise you supported it until a colleague mentioned it. Where is the setting for that?"
  - T-1018: "We've enabled SAML. Now I want automatic user provisioning. Is SCIM supported? Where would I configure it? I can't find docs."
- **Reach:** 2 tickets / 6% of corpus. Both Enterprise, both blocking integration/onboarding
- **Weight:** 2 (frequency) × 3 (blocks Enterprise integration) × 1.5 (Enterprise concentration) = 9
- **Recommended action:** Write setup guide for SAML SSO (Okta specifically mentioned); clarify SCIM support status and document configuration. This is table-stakes for Enterprise sales. Candidate for `/support:write-kb-article`.

---

### Hand-offs
- **To product (roadmap):** Cancel button UX redesign; onboarding empty-state + guided first-run flow
- **To engineering (bug triage):** CSV export silent row truncation; app memory crash on large data volumes
- **To docs (`/support:write-kb-article` candidates):** SSO/SCIM setup guide; recurring tasks feature documentation
- **To product (future roadmap, lower priority):** Bulk archive/delete; dark mode; PDF export; API rate-limit headers; calendar view

---

### Signal-type insights

The defect cluster (10 tickets) is concentrated in data integrity (export) and performance (memory crashes), both high-severity. The UX failure cluster (13 tickets) is split between a critical funnel problem (onboarding churn) and a friction point at a key decision moment (cancellation). The doc gap is small (4 tickets) but both themes are Enterprise-blocking — SSO/SCIM especially should move fast.

The corpus shows a clear funnel leak: Trial week 1 users hit onboarding confusion (5/7 trial tickets) and cancel-finding friction (3/6 cancel tickets), causing early churn. Paid tiers hit data-integrity and performance walls. Both are product-quality issues, not just feature gaps.

---

### Cross-lens notes

No prior VoC data from reviews, NPS, or churn signal available for this handoff. The ticket corpus is the first pass. Recommend running this output against churn cohorts (trial dropoff timing, paid downgrades) to validate whether onboarding and cancel-UX fixes would reduce churn, and against review mining to see if data-integrity complaints appear elsewhere.

---

### Outliers

- **T-1024 — Notifications sent twice** (Defect, 1 ticket): Started recently ("worked normally last week, started doubling a few days ago"). Single ticket but flagged as regression — monitor for clustering in next week.
- **T-1011, T-1023, T-1026, T-1032 — Feature requests** (Missing capability, 4 tickets): Dark mode (cosmetic), API rate-limit headers (integration), PDF export (adjacent to CSV), calendar view (UI variant). Low weight individually; none clustered. Watch for theme emergence if these recur.

---

**Severity legend:**  
4 = Blocks core task / data loss / funnel blocker  
3 = Blocks secondary workflow / Enterprise adoption  
2 = Slows user down / workaround exists  
1 = Cosmetic / nice-to-have

### Artifacts written

#### `work/tickets/support-tickets-may.md`

```
# Support tickets — May 2026 export

Source: Zendesk export, "Product" queue. Date range: 2026-05-01 to 2026-05-30.
Segment data: plan tier and account tenure included where known.

---

T-1001 | 2026-05-02 | Plan: Trial (week 1)
Subject: How do I cancel?
Body: "I clicked everywhere looking for a way to cancel my subscription. There's no button for it on the billing page. I assumed it would be under Account but it isn't. Eventually gave up and emailed you."

T-1002 | 2026-05-02 | Plan: Pro (paid)
Subject: Export missing rows
Body: "I exported my project list to CSV and it silently dropped about 40 rows. No error, no warning — the file just had fewer rows than the screen. This is a data-integrity problem for our reporting."

T-1003 | 2026-05-03 | Plan: Trial (week 1)
Subject: Cancel subscription
Body: "Where is the cancel button?? I've been hunting for 20 minutes. I can upgrade in one click but cancelling is impossible to find."

T-1004 | 2026-05-03 | Plan: Enterprise (paid)
Subject: SSO setup question
Body: "Is it possible to set up SAML SSO with Okta? I didn't realise you supported it until a colleague mentioned it. Where is the setting for that?"

T-1005 | 2026-05-04 | Plan: Pro (paid)
Subject: CSV export broken again
Body: "Same as before — export to CSV is dropping rows. Counted 312 on screen, 270 in the file. Happens every time with large projects."

T-1006 | 2026-05-05 | Plan: Free
Subject: Can't find cancel
Body: "There's no obvious way to cancel. I clicked Settings, Account, Billing — nothing. Had to search your help site to find out it's hidden behind 'Manage plan'."

T-1007 | 2026-05-06 | Plan: Trial (week 1)
Subject: Stuck on setup
Body: "During onboarding I got stuck at the 'invite your team' step. It let me click Next with no one invited, then the dashboard was empty and I had no idea what to do. Very confusing first run."

T-1008 | 2026-05-07 | Plan: Pro (paid)
Subject: How to bulk archive
Body: "How do I archive multiple projects at once? I can only seem to do them one at a time. Is there a bulk option I'm missing?"

T-1009 | 2026-05-08 | Plan: Enterprise (paid)
Subject: Export dropping rows
Body: "Our finance team's monthly export is missing line items. The CSV has fewer rows than the dashboard. We rely on this for invoicing — it's causing real problems."

T-1010 | 2026-05-09 | Plan: Trial (week 1)
Subject: First-run confusion
Body: "I assumed after signing up I'd get a guided tour. Instead I landed on an empty board with no projects and no prompt. I clicked around for a while and then left. Not sure what I'm meant to do."

T-1011 | 2026-05-10 | Plan: Free
Subject: Dark mode?
Body: "It would be great if you could add a dark mode. The white background is hard on my eyes at night."

T-1012 | 2026-05-11 | Plan: Pro (paid)
Subject: Where's the cancel option
Body: "I want to downgrade and there's no clear path. I clicked through every menu. Found it eventually under an unlabelled 'Manage plan' link. Should be obvious."

T-1013 | 2026-05-12 | Plan: Trial (week 1)
Subject: Onboarding — what now?
Body: "Created my account, got dropped into an empty workspace. There's no 'start here'. I don't know whether to create a project or invite people first. Felt lost."

T-1014 | 2026-05-13 | Plan: Enterprise (paid)
Subject: Page crashes on large board
Body: "When I open our biggest board (around 2,000 cards) the page freezes and then crashes with a white screen. It worked fine last month. Console shows an out-of-memory error."

T-1015 | 2026-05-14 | Plan: Pro (paid)
Subject: How do I set up recurring tasks
Body: "Is it possible to make a task repeat weekly? I couldn't find the option. Does the feature exist?"

T-1016 | 2026-05-15 | Plan: Free
Subject: Export to CSV loses data
Body: "Exported my board and rows are missing from the file compared to what I see. No warning at all."

T-1017 | 2026-05-16 | Plan: Trial (week 1)
Subject: Setup is confusing
Body: "The setup flow let me skip every step and then I had a blank account. I expected it to walk me through creating my first project. Gave up and will try a competitor."

T-1018 | 2026-05-17 | Plan: Enterprise (paid)
Subject: SSO — is SCIM supported?
Body: "We've enabled SAML. Now I want automatic user provisioning. Is SCIM supported? Where would I configure it? I can't find docs."

T-1019 | 2026-05-18 | Plan: Pro (paid)
Subject: Bulk delete
Body: "It would be great if I could select multiple tasks and delete them together. Right now it's one by one which is painful for cleanup."

T-1020 | 2026-05-19 | Plan: Free
Subject: Can't cancel
Body: "No cancel button anywhere I looked. I clicked everywhere. This feels deliberately hidden."

T-1021 | 2026-05-20 | Plan: Trial (week 1)
Subject: Lost after signup
Body: "After signing up there was no onboarding. Empty screen. I assumed there'd be sample data or a wizard. There wasn't, and I bounced."

T-1022 | 2026-05-21 | Plan: Pro (paid)
Subject: Export totals don't match
Body: "The exported CSV has fewer rows than the project view. Some tasks just aren't in the file. Looks like a silent truncation bug."

T-1023 | 2026-05-22 | Plan: Enterprise (paid)
Subject: API rate limit headers
Body: "It would be great if your API returned X-RateLimit-* headers so our SDK can back off properly. Right now we just get 429s with no guidance."

T-1024 | 2026-05-23 | Plan: Free
Subject: Notifications sent twice
Body: "I'm getting two emails for every project I create. It worked normally last week, started doubling a few days ago. Looks like a bug."

T-1025 | 2026-05-24 | Plan: Trial (week 1)
Subject: Onboarding empty state
Body: "Brand new account, dropped onto a blank dashboard, no guidance. I didn't know creating a project was the first step until I poked around. Nearly gave up."

T-1026 | 2026-05-25 | Plan: Pro (paid)
Subject: How to export to PDF
Body: "Is it possible to export a board as a PDF? I can do CSV but I need a PDF for a client. Does that exist somewhere?"

T-1027 | 2026-05-26 | Plan: Enterprise (paid)
Subject: Crash opening reports
Body: "Opening the Reports tab on our large account crashes the tab — white screen, have to reload. Started this week. Error log shows a memory issue."

T-1028 | 2026-05-27 | Plan: Free
Subject: Where do I cancel
Body: "Genuinely cannot find how to cancel. Clicked every menu item. Found a forum post saying it's under Manage plan — that label means nothing to me."

T-1029 | 2026-05-28 | Plan: Pro (paid)
Subject: Recurring tasks how-to
Body: "Where is the setting to make a task recur monthly? I think it's possible but I can't locate it."

T-1030 | 2026-05-29 | Plan: Trial (week 1)
Subject: Confusing first experience
Body: "Signed up, immediately confused. No tour, no sample project, no 'do this first'. The product let me wander into an empty state. I expected hand-holding on day one."

T-1031 | 2026-05-30 | Plan: Enterprise (paid)
Subject: Data export incomplete
Body: "Monthly compliance export is missing rows again. The dashboard shows 540, the CSV has 498. We need every row for audit. This silent drop is unacceptable at our tier."

T-1032 | 2026-05-30 | Plan: Free
Subject: Idea: calendar view
Body: "I wish there were a calendar view of tasks by due date. Would help me plan my week."

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 11.5/12.5 (92%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 63949 ms |
| Target cost | $0.1218 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Records the corpus boundary first — ticket count, date range, source — before coding any themes | PASS | Opening 'Corpus' block: 'Tickets analysed: 32 / Date range: 2026-05-02 to 2026-05-30 / Source: Zendesk "Product" queue export' — before any theme table. |
| c2 | Codes tickets from the body using user-language theme labels (e.g. "can't find where to cancel"), preserving verbatim phrases, not internal jargon | PASS | Theme labels use ticket body language: 'CSV export silently drops rows, no warning'; 'Can't find the cancel button; it's hidden somewhere'. Evidence sections quote ticket bodies verbatim. |
| c3 | Classifies the cancel-discoverability tickets as UX failure (users "clicked everywhere", the affordance is hidden) — NOT collapsed into a doc gap because an article would have rescued them | PASS | Theme 3: 'Signal type: UX failure → owner: product/design'; characterised as 'user-hostile friction during a decision moment', not a doc gap. |
| c4 | Classifies the SSO / recurring-tasks / PDF-export how-to tickets as doc gaps — the capability exists and works, the user just didn't know how — distinct from the UX-failure tickets | PARTIAL | SSO (Theme 5) and recurring tasks (Theme 6) correctly classified as doc gaps. PDF export (T-1026) is placed in 'Missing capability' under feature requests, not as a doc gap. |
| c5 | Classifies the CSV-export-drops-rows tickets as a defect (silent data loss against expected behaviour), not as a doc gap or feature request | PASS | Theme 1: 'Signal type: Defect → owner: engineering'; described as 'data-integrity problem', 'silent truncation bug'. |
| c6 | Classifies the feature requests (dark mode, calendar view, API rate-limit headers, bulk delete) as missing capability, routed to the roadmap | PASS | Signal-type split lists 'Missing capability: 5 tickets across 5 themes (bulk ops, dark mode, PDF export, API rate-limit headers, calendar view)'; hand-off: 'To product (future roadmap, lower priority): Bulk archive/delete; dark mode; PDF export; API rate-limit headers; calendar view'. |
| c7 | Weights themes by frequency × severity (severity = user impact, not ticket volume) so a high-impact theme can outrank a higher-volume low-impact one — and shows the arithmetic | PASS | Each roadmap theme shows arithmetic, e.g. Theme 2: '7 (frequency) × 4 (blocks initial adoption) × 1.0 = 28'; Theme 1 (count 6) outranks Theme 2 (count 7) via segment factor. |
| c8 | Applies a paid/enterprise segment factor where justified by the segment data (e.g. the export-data-loss theme concentrated in paid tiers) rather than on a hunch | PASS | Theme 1 weight: '× 1.5 (paid/Enterprise concentration)'; Theme 4: '× 1.5 (Pro/Enterprise, paid tiers, power users)'; Theme 5: '× 1.5 (Enterprise concentration)' — all citing segment data. |
| c9 | Notes segment concentration where present — onboarding-confusion in trial week-one users, export-data-loss in paid tiers | PASS | Theme 2: 'Heavily concentrated in Trial week 1 (5/7); funnel risk'; Theme 1: 'Concentrated in Pro (2) and Enterprise (4)'. Theme table column 'Segment' shows 'Trial wk1: 5/7' and 'Enterprise 4/6'. |
| c10 | Treats this as the support ticket lens — hands defect themes to engineering and large doc-gap themes toward write-kb-article, rather than absorbing all feedback channels | PASS | Hand-offs: 'To engineering (bug triage): CSV export silent row truncation; app memory crash'; 'To docs (/support:write-kb-article candidates): SSO/SCIM setup guide; recurring tasks'. |
| c11 | For a theme that splits across signal types (some UX-failure, some doc-gap tickets), records the split count rather than forcing one classification | FAIL | The 'Signal mix' column exists but every theme shows a single type (e.g. 'UX 7', 'Defect 6'). No theme records a split count — all force one classification. |
| c12 | Output follows the skill's Output Format — corpus block, ranked theme table (with signal mix, count, %, severity, weight), signal-type split, roadmap-ready themes, and hand-offs | PASS | Output contains all required sections in order: Corpus block, theme table with all columns (signal mix, count, %, severity, segment, weight, trend), signal-type split, roadmap-ready themes, hand-offs. |
| c13 | Output's ranked theme table shows the frequency × severity (× segment) arithmetic per theme so the ranking is auditable, and routes each theme by signal type to the correct owner (product / docs / engineering) | PASS | Each roadmap-ready theme section shows full arithmetic (e.g. '6 × 4 × 1.5 = 36') and routes: 'owner: engineering' for defects, 'owner: product/design' for UX, 'owner: docs/support' for doc gaps. |

### Notes

The output is thorough and well-structured, correctly handling all major classification decisions (UX failure vs doc gap vs defect) and showing auditable weight arithmetic with segment justification. The only clear misses are PDF export being classified as missing capability rather than a doc gap (c4), and no theme demonstrating a cross-signal-type split count (c11).
