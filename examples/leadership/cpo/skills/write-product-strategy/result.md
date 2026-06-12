# Write Product Strategy

Scenario: The CPO is asked to write a product strategy for a single product with one broadly understood market. The skill must pick a format and justify the choice — defaulting to Cagan/SVPG for a single product rather than reaching for the Playing-to-Win cascade — and then take a real position: name the few specific problems it will solve, AND write the deliberate "not doing" list (the hardest, most valuable section), drive each bet from an insight rather than opinion, and avoid producing a roadmap or an aspiration dressed as a strategy. A generic "improve onboarding, grow revenue, delight users" plan must not score well.

## Prompt

> Use the cpo `write-product-strategy` skill to write a product strategy for "Tideline", an existing
> appointment-and-records product for solo and very small allied-health clinics. It is one product in one
> broadly understood market (Australian allied-health micro-practices). The vision already exists: help these
> clinics run without a back office. Today the product handles bookings well but clinicians still chase
> no-shows manually and do their compliance notes in a separate tool. Discovery shows no-shows are the number
> one cause of lost revenue for these practices, and that switching cost from their current spreadsheet is the
> biggest barrier to adoption.
> 
> Write the strategy artifact to `docs/strategy/product-strategy-tideline.md` (a relative path under the
> current working directory). Respond in the skill's standard format. Proceed without asking.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

**Strategy written to `docs/strategy/product-strategy-tideline.md`.**

The Cagan/SVPG format is the right fit here — one product, one market, the question is problem prioritisation, not market entry.

**Three reinforcing bets:**

1. **No-show automation** — the #1 revenue blocker; eliminates manual chasing
2. **Compliance integration** — breaks the context-switch that stops practices from running entirely in Tideline
3. **Switching friction reduction** — the adoption lock; without it, neither of the above matters

**Strong "not doing" list** — full EHR, billing, multi-staff rostering, and scattered integrations are all deferred. Narrow focus on the back-office elimination vision.

**Next:** Hand this to `/cpo:diagnose-strategy` for the full Rumelt diagnostic before it ships. The diagnosis will check for bad-strategy hallmarks (fluff, disconnected objectives, aspiration-masquerading-as-strategy) that the self-check may have missed.

### Artifacts written

#### `work/docs/strategy/product-strategy-tideline.md`

```
# Product strategy — Tideline

**Format:** Cagan/SVPG · **Author:** CPO · **Date:** 2026-06-13 · **Next review:** 2026-09-13

**Vision link:** Help these clinics run without a back office

**Format justification:** Single product in one well-defined market; the strategic question is which problems to solve next to move toward the vision, not where to compete or how to enter new markets.

---

## The problems we will solve

1. **No-show revenue loss and manual recovery chasing** — No-shows are the #1 cause of lost revenue for these practices, yet the product leaves clinicians to chase them manually. Automating no-show management (reminders, tracking, cancellation/rebooking flows) directly unblocks the top revenue problem and moves the product toward the vision of eliminating manual work.

2. **Compliance note fragmentation and context-switching** — Clinicians complete compliance-required notes in separate tools, breaking workflow continuity and creating data silos. Integrating note capture into the appointment context eliminates context-switching and moves clinicians closer to "running without a back office."

3. **Switching friction from legacy spreadsheet workflows** — The #1 adoption barrier is the cost of migrating from spreadsheets. Removing friction (data migration tooling, import workflows, simplified onboarding) is essential to growth; discovery shows this is what stops prospects from converting.

## What we are deliberately not doing

- **Full patient medical records / EHR system** — while relevant long-term, building a full EHR is beyond the scope of a back-office elimination tool and raises compliance burden. Narrow focus: appointment, no-show management, and compliance notes only.
- **Billing, invoicing, and accounts** — financial workflows are a separate domain with their own regulatory requirements; many clinics have existing accounting systems. Stay focused on operational efficiency, not accounting.
- **Staff scheduling and rostering** — while solo practices don't need this, very-small practices (2–3 clinicians) might. Defer; multi-staff workflows introduce significant design complexity that distracts from the core problems.
- **Deep integrations with external systems** — avoid chasing every calendar, SMS gateway, or compliance software integration request. Defer to "must-have integrations" only, identified after switching-friction work.

## Focus rationale

These three problems are mutually reinforcing and directly unblock the vision:

- **No-show automation** directly addresses the #1 revenue blocker and the most painful manual task in the practice.
- **Compliance integration** eliminates the context-switch that prevents clinics from running their whole practice in Tideline — a prerequisite for "without a back office."
- **Switching friction removal** is the adoption lock; without it, the product remains a nice-to-have, not a must-have. This is the limiting factor on growth.

The sequence matters: switching friction must be addressed first or second, because without it, even a superior product won't acquire new clinics fast enough to validate the other bets. No-show automation is the highest-value problem to solve once switching is less painful. Compliance integration follows, consolidating the product into a single tool.

## Refresh cadence

Strategy review: quarterly (next 2026-09-13). Trigger for earlier refresh:
- Discovery finding that changes the top revenue blocker (e.g., no-shows drop below #2)
- Evidence that a chosen bet is failing (e.g., compliance integration adoption after launch is <30%)
- Market or regulatory change affecting micro-clinic practices

---

## Bad-strategy self-check

- [x] No fluff — specific problems, not "leverage", "world-class", or "best-in-class"
- [x] Core challenge faced plainly — adoption barrier and revenue blocker are named and clear
- [x] No aspiration posing as strategy — vision is stated separately; strategy is the plan to reach it
- [x] Objectives coherent, not scattered — three problems are interdependent and reinforcing

## Execution handoff

- **OKRs:** To be defined via `/coordinator:define-okrs`; each problem above should map to an OKR.
- **Downstream owners:** Product Manager → translates problems into PRD and roadmap; Engineering → delivery; Customer Success → switching-friction metrics and support.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 13.0/13.0 (100%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 43403 ms |
| Target cost | $0.0765 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Picks a format explicitly and justifies it in one sentence — defaults to Cagan/SVPG for this single product / single market, and does NOT reach for the Playing-to-Win cascade where 'where to play' is not open | PASS | File header: '**Format:** Cagan/SVPG' + justification: 'the strategic question is which problems to solve next … not where to compete or how to enter new markets' |
| c2 | Reads/links the existing vision and frames the strategy as the plan to close the gap between today and the vision, not a blank-slate plan | PASS | '**Vision link:** Help these clinics run without a back office' — each problem section ties back with 'moves toward the vision of eliminating manual work' |
| c3 | Names a few specific problems to solve (typically two to four) — each a customer or business problem (e.g. no-shows, compliance-notes friction), NOT a feature or initiative | PASS | Three named problems: 'No-show revenue loss and manual recovery chasing', 'Compliance note fragmentation and context-switching', 'Switching friction from legacy spreadsheet workflows' — all business/customer problems, not features |
| c4 | Each chosen problem is driven from the supplied insight/evidence (no-shows = #1 revenue loss; switching cost = top adoption barrier), not from opinion or gut feel | PASS | No-shows: 'No-shows are the #1 cause of lost revenue'; switching: 'The #1 adoption barrier is the cost of migrating from spreadsheets' — both trace directly to supplied discovery |
| c5 | Writes an explicit 'what we are deliberately NOT doing' section listing tempting problems being said no to this period, with reasons — present and substantive, not an afterthought | PASS | '## What we are deliberately not doing' lists four items (EHR, billing, staff rostering, deep integrations), each with a specific reason for deferral |
| c6 | Provides a focus rationale explaining why these problems, in this order, this period — tied to discovery/market/technology, not just listed | PASS | '## Focus rationale' explains mutual reinforcement, sequencing ('switching friction must be addressed first or second'), and ties each bet to the discovery evidence |
| c7 | States a refresh cadence (no less than quarterly) and what would trigger an earlier refresh | PASS | 'Strategy review: quarterly (next 2026-09-13). Trigger for earlier refresh:' followed by three named triggers including discovery and adoption metrics |
| c8 | Takes a real position — the strategy is opinionated and specific to Tideline's situation, not a generic 'improve onboarding / grow revenue / delight customers' plan applicable to any product | PASS | All three bets name Tideline-specific conditions: manual no-show chasing, compliance notes in a separate tool, spreadsheet switching cost — none are generic platitudes |
| c9 | Does NOT produce a roadmap or dated feature/sprint list in place of strategy, and does not let an aspiration ('become the market leader', 'reach $X') pose as the strategy | PASS | No sprint list or dated features present. Self-check explicitly flags 'No aspiration posing as strategy — vision is stated separately; strategy is the plan to reach it' |
| c10 | Runs the bad-strategy self-check (fluff / facing the challenge / goals-as-strategy / disconnected objectives) and points to `/cpo:diagnose-strategy` as the mandatory follow-up | PASS | File has '## Bad-strategy self-check' with four checkboxes; chat response: 'Hand this to `/cpo:diagnose-strategy` for the full Rumelt diagnostic before it ships' |
| c11 | Connects to execution — names downstream owners (PM → PRD/roadmap, engineering → delivery) and ties bets to OKRs | PASS | '## Execution handoff': 'OKRs: To be defined via /coordinator:define-okrs … Downstream owners: Product Manager → PRD and roadmap; Engineering → delivery; Customer Success → switching-friction metrics' |
| c12 | Output writes the strategy file to `docs/strategy/product-strategy-tideline.md` under the working directory, with the chosen format declared and the 'deliberately not doing' section present as a named heading | PASS | File written to `work/docs/strategy/product-strategy-tideline.md`; format declared in header; '## What we are deliberately not doing' present as a named heading |
| c13 | The written strategy is concrete to Tideline (no-shows, compliance notes, switching cost) and reads as a set of focused bets with rationale — demonstrating the take-a-position bar rather than a generic template fill | PASS | All three bets are named with Tideline-specific context, sequencing argument given ('switching friction must be addressed first or second'), and rationale tied to discovery |

### Notes

The artifact hits every criterion cleanly: format justified, vision linked, three discovery-backed bets, a substantive 'not doing' list with reasons, an ordered focus rationale, quarterly cadence with triggers, bad-strategy self-check in the file and `/cpo:diagnose-strategy` in the chat, and execution handoff. No generic filler — every sentence is specific to Tideline's situation.
