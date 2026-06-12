---
name: retention-voc
description: Mine account-level voice-of-customer themes from churn, at-risk, QBR, renewal, expansion, and cancellation evidence. Use to extract the qualitative retention narrative behind churn and feed retention themes to the roadmap. The customer-success VoC lens — account-level, distinct from individual-user VoC.
argument-hint: "[account, segment, churn cohort, or time window to mine]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

Mine the account-level voice-of-customer for $ARGUMENTS.

This is the customer-success voice-of-customer lens. Voice-of-customer is deliberately distributed across the
marketplace: support holds the ticket lens, ux-researcher holds the individual-user lens, GTM holds the
win/loss lens, and you hold the account-retention lens. The overlap is intentional. Don't try to reconcile your
themes into one canonical VoC — hand your lens to the product-owner alongside the others and let the conflict
surface. Your lens answers one question the others can't: *why do paying accounts leave, contract, or expand, in
their own words?*

This skill extracts the **qualitative** retention narrative. It is the upstream partner of
`/customer-success:churn-analysis`, which does the **quantitative** root-cause scoring and probability work for a
single account. Run this skill across a cohort to find themes; run churn-analysis on the individual accounts a
theme implicates. Pull the account cohort from `/customer-success:health-assessment` when you need a portfolio to
mine.

## Step 1: Scope the cohort and the source set

Define exactly which accounts you are mining and which evidence counts. A VoC pull with no defined cohort produces
anecdotes, not themes.

| Decision | Resolve before gathering |
|---|---|
| **Cohort** | Named account, a segment (tier/industry/size), a churn cohort (all accounts lost this quarter), or a time window |
| **Account stage** | Churned, at-risk, renewed, expanded, or a mix — state which. The stage colours every theme |
| **ARR band** | Note the ARR represented by the cohort. Themes are weighted by revenue at risk later |
| **Source set** | Which evidence types are in scope (Step 2). Note any source you wanted but couldn't access |

Output of this step: a one-line scope statement — "Mining 14 churned accounts (Q2, $310k ARR lost) across QBR
notes, cancellation reasons, and CSM save-attempt notes." If the cohort is a single account, say so; single-account
VoC is valid but cannot claim a theme.

## Step 2: Gather account-level VoC sources

Pull from the evidence the customer-success function uniquely holds. These are account-level artifacts — they carry
the account's context, the commercial relationship, and the trajectory over time.

| Source | What it reveals | Where it lives |
|---|---|---|
| **Cancellation / churn reasons** | The stated reason for leaving, in the customer's words | Churn log, cancellation form, save-attempt notes |
| **QBR notes** | Goals, blockers, sentiment, and unmet expectations raised in business reviews | QBR decks, meeting notes |
| **Renewal conversations** | What the account weighed when deciding to stay or go, price/value objections | Renewal notes, commercial threads |
| **Expansion conversations** | What made an account want *more* — the value that landed, the gap that blocked it | Expansion/upsell notes |
| **At-risk account notes** | Why the CSM flagged the account, what the intervention surfaced | Health-assessment outputs, save plans |
| **Executive sponsor feedback** | Strategic-level satisfaction, the buyer's (not the user's) view of value | Sponsor calls, exec business reviews |

Capture each datum with attribution: account, stage, date, and the verbatim quote or close paraphrase. A theme with
no quotes behind it is an assertion. Note explicitly where a source was unavailable — a churn analysis missing the
cancellation reasons is a known blind spot, not a silent gap.

## Step 3: Separate account-level VoC from individual-user VoC

This is the boundary that defines your lens. The same product complaint means different things at the two levels,
and conflating them produces roadmap noise.

| | Account-level VoC (yours) | Individual-user VoC (ux-researcher / support) |
|---|---|---|
| **Unit** | The buying account — the contract, the sponsor, the renewal decision | The individual user — the person clicking the button |
| **Voice** | Champion, economic buyer, executive sponsor | End user, daily operator |
| **Signal** | "We didn't see ROI to justify renewal" | "This workflow has too many steps" |
| **Decision it drives** | Renew, expand, contract, churn | Adopt, abandon, work around a feature |
| **Weighting** | By ARR and account count | By user count and frequency |

When you find a usage-level complaint in your sources, decide whether it is *load-bearing for the account decision*.
"A user found the export clunky" is individual-user VoC — route it to support/ux-researcher, don't inflate it into a
retention theme. "The account churned because the export gap blocked their core reporting use case and the sponsor
lost confidence" is account-level VoC — it's yours. The test: did this change the contract decision, or just the
click? Tag every datum `account-level` or `user-level`. Carry only the account-level data into Step 4.

## Step 4: Code the themes

Group the account-level data into themes through pattern coding. A theme is a recurring reason that appears across
multiple accounts — not a single account's complaint.

1. Read all account-level data and assign a short code to each datum ("value-not-realised", "champion-departed",
   "missing-integration", "price-vs-value", "onboarding-stalled").
1. Collapse codes into themes. A theme needs evidence from **2+ accounts** to be named a theme; a single-account
   signal is logged as a watch item, not a theme.
1. For each theme, classify the underlying driver so it routes to the right owner:

| Driver | Means | Routes to |
|---|---|---|
| **Product gap** | A missing or weak capability blocked the account's use case | Roadmap (product-owner) |
| **Value realisation** | The capability exists but the account never reached outcome | Onboarding / CS process |
| **Relationship** | Champion left, no sponsor, eroded trust | CS playbook |
| **Commercial** | Price-vs-value, packaging, contract friction | CPO / commercial (human) |
| **Quality** | Bugs, reliability, performance degraded confidence | Engineering via support |

Note theme saturation: if new accounts stop adding new codes, you have enough evidence. Say so.

## Step 5: Weight themes by retention impact

Themes are not equal. A theme that touches three accounts worth $20k total matters less than one touching two
accounts worth $200k. Weight by both reach and revenue so the roadmap sees the real stakes.

| Weighting axis | How to score |
|---|---|
| **Account reach** | Number of accounts in the cohort the theme appears in |
| **ARR at stake** | Sum of ARR for accounts the theme implicates (churned = lost; at-risk = at risk) |
| **Stage severity** | Churned > at-risk > renewed-with-reservation > expansion-blocker |
| **Addressability** | Can the named owner act on it? A theme you can't action is context, not a recommendation |

Rank themes by ARR-weighted reach. The top themes are the retention narrative; the long tail is the watch list.

## Step 6: Cross-check against the quantitative churn analysis

This is the genuine dependency between the two skills, and it runs both ways. Your themes are qualitative
hypotheses about *why*. `/customer-success:churn-analysis` produces the quantitative root-cause diagnosis and
churn-probability scoring for individual accounts. Reconcile them:

- For each top theme, run or pull `/customer-success:churn-analysis` on the accounts it implicates. Does the
  quantitative root cause match your qualitative theme? Agreement raises confidence; divergence is a finding.
- Where the numbers and the narrative disagree, say so explicitly. "Cancellation reasons cite price (qualitative),
  but usage-decline timelines show the accounts had already disengaged 8 weeks before the price conversation
  (quantitative). Price was the stated reason; disengagement was the cause." The stated reason and the real reason
  diverge often — surfacing the gap is the value.
- Never present a theme as validated on qualitative evidence alone if quantitative data exists to test it. If no
  quantitative data exists, label the theme `unconfirmed — qualitative only`.

## Step 7: Package retention themes for the roadmap

The output's job is to feed the product-owner's prioritisation with evidence they don't otherwise have. Frame each
theme as: the theme, the accounts and ARR behind it, the verbatim voice, the quantitative cross-check, and the
owner it routes to. Product-gap themes go to the roadmap; do not propose solutions — name the problem and the
evidence, and let the product-owner prioritise. Tag the output as the *customer-success lens* so the product-owner
knows to weigh it alongside the support, ux-researcher, and GTM lenses rather than treating it as the whole VoC.

## Rules

- Always weight themes by ARR and account reach, not by how loud or recent a single account was. The squeaky
  account is not the biggest theme.
- Always carry verbatim quotes into the output. A theme with no quote behind it is your opinion, not the customer's
  voice. Anti-pattern: writing "accounts wanted better reporting" with no account, date, or quote — that's an
  assertion dressed as VoC.
- Never inflate an individual-user complaint into a retention theme. Anti-pattern: a user disliking a button colour
  becomes "UX is driving churn." Instead, tag it `user-level`, route it to ux-researcher/support, and keep your lens
  on account decisions.
- Never reconcile your lens with the other VoC lenses into one canonical view. Different lenses producing different
  recommendations is the design intent — hand the product-owner your account-retention view and let conflict
  surface. Anti-pattern: merging your churn themes with support's ticket themes and presenting a single "VoC truth."
- Never present the stated cancellation reason as the root cause without the quantitative cross-check (Step 6). The
  reason a customer gives and the reason they left diverge routinely. Anti-pattern: "they said price, so the theme is
  price" — when the usage data shows they disengaged months earlier.
- Never propose solutions in the roadmap hand-off. Name the problem, the evidence, and the ARR at stake. Solutioning
  is the product-owner's job. Anti-pattern: "we should build a Salesforce integration" instead of "4 churned
  accounts ($140k) cited the missing CRM integration as blocking their core workflow."
- A theme needs 2+ accounts. A single account is a watch item, not a theme. Don't name a theme off one voice.
- State your blind spots. A source you couldn't access (no cancellation form, sponsor wouldn't take the call) is a
  named gap in the output, not a silent omission.

## Output Format

```markdown
# Retention VoC: [cohort / account / segment]

## Scope
- **Cohort:** [accounts mined — count and definition]
- **Stage:** [churned / at-risk / renewed / expanded / mixed]
- **ARR represented:** [$]
- **Sources used:** [list]
- **Sources unavailable:** [named blind spots, or "none"]
- **Lens:** Customer-success (account-level). Weigh alongside support, ux-researcher, and GTM VoC lenses.

## Retention Themes (ranked by ARR-weighted reach)

| Theme | Driver | Accounts | ARR at stake | Stage | Routes to | Cross-check |
|---|---|---|---|---|---|---|
| [theme] | [product gap / value / relationship / commercial / quality] | [n] | [$] | [stage] | [owner] | [matches / diverges from churn-analysis] |

## Theme Detail

### [Theme name] — [ARR at stake], [n] accounts
- **What accounts said (verbatim):**
  - "[quote]" — [account], [stage], [date]
  - "[quote]" — [account], [stage], [date]
- **Account-level vs user-level:** [why this is a retention theme, not a usage complaint]
- **Quantitative cross-check:** [churn-analysis root cause for these accounts — agreement or the stated-vs-real gap]
- **Routes to:** [owner] — [problem statement only, no proposed solution]
- **Confidence:** [confirmed by quantitative data / unconfirmed — qualitative only]

## Watch List (single-account signals, not yet themes)
| Signal | Account | ARR | Note |
|---|---|---|---|
| [signal] | [account] | [$] | [why it's a watch item, not a theme] |

## User-Level Items Routed Elsewhere
| Item | Routed to | Why it's not a retention theme |
|---|---|---|
| [usage complaint] | [ux-researcher / support] | [didn't drive the account decision] |

## Roadmap Hand-off (product-gap themes only)
- **For the product-owner:** [theme, accounts, ARR, evidence — no solution proposed]
- **Tagged as:** Customer-success VoC lens. Compare with other lenses before prioritising.
```

## Related skills

- `/customer-success:churn-analysis` — the quantitative partner. This skill extracts the qualitative *why* across a
  cohort; churn-analysis does the root-cause diagnosis and probability scoring for the individual accounts a theme
  implicates. Run churn-analysis in Step 6 to cross-check every top theme.
- `/customer-success:health-assessment` — run a portfolio health assessment first to define the at-risk cohort, then
  mine that cohort's VoC here. Health-assessment finds *which* accounts; retention-voc finds *why* in their words.
