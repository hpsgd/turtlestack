# Cross Domain Conflict

Scenario: The coordinator receives a conflict where product delivery (CPO) and security remediation (CTO) are at odds. Both parties have legitimate, time-sensitive concerns and neither can be simply overruled.

## Prompt

> The CPO wants to ship a new onboarding flow by end of month to hit activation targets — it's the top priority for Q2 OKRs. The CTO says the authentication system needs to be rebuilt first because it has a known vulnerability (CVSS 7.8) that security flagged last week, and the new onboarding flow touches auth. Both are right. The CPO says we can't slip the OKR, the CTO says we can't ship with a known vulnerability. What do we do?
> 
> A few specifics for the response:
> 
> - **Sequencing plan with concrete dates and owners** — not "have a meeting". Propose a specific sequence with handoffs (e.g. `Week 1 (CTO): scope auth fix, ship compensating control by Friday → Week 2 (CPO + CTO): scoped onboarding flow that avoids vulnerable surface, ship by EOM → Week 3+: full auth rebuild post-OKR`). Include named owner per step.
> - **Accountability preserved (state explicitly)**: "CPO retains ownership of the onboarding OKR. CTO retains ownership of the auth security fix. Coordinator coordinates; does not take over either workstream."
> - **Deadline options (specific)**: present at minimum two: (1) hit OKR with scoped-down onboarding bypassing auth changes, (2) slip OKR by N days with full security fix first. State the trade-off per option.
> - **Escalation rationale (one paragraph)**: why this needed cross-domain coordination — security trumps feature delivery in the abstract, BUT the OKR is a board commitment, AND a known-vulnerability ship sets a precedent that security flags are negotiable. Frame this systematically.
> - **Executive escalation questions**: include 1-2 questions the coordinator would put to the CEO/board if the trade-off can't settle at CPO+CTO level — e.g. "Are we willing to communicate an OKR slip to the board to ship securely?" and "Does the board accept a scoped-down OKR (X% of the original target) as success?"

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

# Recommendation: Option A (scoped onboarding, ship on time) — with Option B ready if scoping fails

Both leaders are correct on their own turf. The coordinator's job here is to **decouple the two workstreams** so each owner can ship their thing without becoming a bottleneck for the other, then escalate the one decision that genuinely sits above them.

## Accountability (stated explicitly)

- **CPO** retains ownership of the onboarding OKR and the activation target.
- **CTO** retains ownership of the auth vulnerability remediation and the security posture.
- **Coordinator** sequences handoffs, brokers the scope conversation, and owns the escalation if Option A scoping isn't viable. Coordinator does **not** take over either workstream.

## Sequencing plan — Option A (recommended): hit OKR with scoped onboarding

Today = Fri 13 Jun 2026. EOM = Tue 30 Jun 2026 (12 working days).

| Window | Owner | Deliverable | Gate |
|---|---|---|---|
| **Mon 16 Jun – Wed 18 Jun** | CTO + Security lead | Scope auth fix; ship **compensating control** (WAF rule / rate-limit / feature flag on the vulnerable code path) by **EOD Wed 18 Jun**. Document residual risk. | Security signs off that residual CVSS is ≤ 4.0 with compensating control in place. |
| **Mon 16 Jun – Thu 18 Jun** (parallel) | CPO + CTO (joint, 1 session, 90 min) | Identify the **vulnerable auth surface**; redesign onboarding flow to route around it (e.g. reuse existing session creation, defer the touched endpoint to v2). Produce a 1-page "scoped onboarding" spec. | Both sign. If they can't sign → escalate (see below). |
| **Fri 19 Jun – Fri 27 Jun** | CPO (eng lead reporting to CPO) | Build & ship scoped onboarding flow. **Code freeze Fri 27 Jun.** | Activation instrumented; meets ≥ 80% of original OKR target. |
| **Mon 30 Jun** | CPO | Ship to 100%. OKR booked. | — |
| **Wed 1 Jul – Fri 1 Aug** | CTO | Full auth rebuild (removes need for compensating control). | Vulnerability closed at source; compensating control removed. |
| **Aug+** | CPO | Onboarding v2 — add back any features deferred in the scoped flow. | — |

**Handoff #1:** CTO → CPO on Thu 18 Jun — "here's the auth surface you must not touch, here's what's safe to call."
**Handoff #2:** CPO → CTO on Mon 30 Jun — "scoped flow shipped, here's the production traffic the auth rebuild must preserve."

## Option B (fallback): slip OKR ~2 weeks, full security fix first

| Window | Owner | Deliverable |
|---|---|---|
| **Mon 16 Jun – Fri 3 Jul** | CTO | Full auth rebuild. Vulnerability closed at source. |
| **Mon 6 Jul – Fri 17 Jul** | CPO | Onboarding flow on rebuilt auth. **Ship Fri 17 Jul.** |
| **End Q2 (30 Jun)** | CPO | OKR booked at ~50% (slip communicated to board on 19 Jun). |

**Trade-off comparison:**

| | Option A | Option B |
|---|---|---|
| OKR | Hit (~80% of original scope, 100% of activation target if scoping is honest) | Miss EOM by ~17 days |
| Security | Residual risk for ~6 weeks behind compensating control | Clean — no residual risk |
| Precedent | "We route around known vulns when the OKR demands it" — must be ring-fenced explicitly to avoid becoming policy | "Security flags stop the line" — clean precedent |
| Execution risk | Scoping may not be feasible; discovered late = worst of both worlds | Low — sequential, no coordination overhead |
| Reversibility | Compensating control is real engineering — has to actually work | High |

Option A is preferred **only if** the joint scoping session on 16–18 Jun produces a credible "auth surface to avoid" boundary. If that session ends in hand-waving, switch to Option B immediately — don't burn the week.

## Why this needed cross-domain coordination

In the abstract, security trumps feature delivery — shipping a known CVSS 7.8 is not a thing a responsible org does. But two facts make this genuinely cross-domain rather than a straight CTO veto. **First**, the OKR is a board commitment, and unilaterally slipping it without explicit board acknowledgement damages CPO credibility and the company's external narrative on activation. **Second**, the way an org handles its first "security says no, product says yes" collision becomes the precedent — if security flags can be negotiated down implicitly, every future flag gets discounted; if product OKRs can be slipped without board conversation, every future OKR becomes soft. The coordinator's job is to make sure **both** norms are reinforced explicitly: security gets a real remediation path (compensating control + dated full fix) and product gets a real shipping path (scoped flow + dated v2), and the trade-off gets named out loud rather than absorbed.

## Executive escalation questions (for CEO / board, if 16–18 Jun scoping fails)

1. **OKR slip:** *"Are we willing to communicate a ~2-week OKR slip to the board on 19 Jun to ship the onboarding flow on a fully remediated auth stack? If yes, we proceed with Option B and the board hears it from us before quarter close."*
2. **Scoped success:** *"Does the board accept a scoped-down onboarding flow — ~80% of the original feature surface, 100% of the activation target — as Q2 OKR success, with the deferred 20% landing in July? If yes, we proceed with Option A and the scoped spec is signed by CPO + CTO + Security by EOD Thu 18 Jun."*

A "no" to both means the trade-off is genuinely above the C-suite and needs a board-level call this week, not at quarter end.

## Next concrete step (today)

Coordinator to send a single calendar hold: **Mon 16 Jun, 10:00–11:30, CPO + CTO + Security lead, 1 agenda item — "can onboarding route around the vulnerable auth surface, yes or no."** That meeting determines Option A vs Option B. Everything else flows from it.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.5/15.0 (97%) |
| Evaluated | 2026-06-13 |
| Target model | claude-opus-4-7 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 41582 ms |
| Target cost | $0.3226 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Coordinator does not simply side with one party — acknowledges both concerns are legitimate | PASS | "Both leaders are correct on their own turf." and "Both are correct on their own turf. The coordinator's job here is to decouple the two workstreams" |
| c2 | Coordinator assesses whether the work can be sequenced (auth fix first, then onboarding) or must be parallel | PASS | Option A proposes parallel work with compensating control; Option B proposes sequential (auth rebuild first, then onboarding). Both are explicitly assessed with trade-offs. |
| c3 | Security vulnerability is treated as a constraint, not a competing priority — CVSS 7.8 is High severity | PASS | "shipping a known CVSS 7.8 is not a thing a responsible org does" and compensating control required to reduce residual CVSS ≤ 4.0 before onboarding ships. |
| c4 | A concrete resolution is proposed with specific sequencing, not 'you two should work it out' | PASS | Detailed table with specific date windows (Mon 16 Jun – Wed 18 Jun, etc.), named owners (CTO, CPO, Security lead), and explicit gates per step. |
| c5 | The resolution preserves accountability — CPO still owns the onboarding OKR, CTO still owns the security fix | PASS | Explicit accountability section: "CPO retains ownership of the onboarding OKR... CTO retains ownership of the auth vulnerability remediation... Coordinator does not take over either workstream." |
| c6 | Coordinator identifies whether the OKR deadline can be adjusted given the security constraint, with specific options | PARTIAL | Option B states OKR slips ~17 days (ship Fri 17 Jul, booked at ~50% by EOM). Two specific deadline options presented with dates. |
| c7 | Escalation framing is clear — the coordinator explains WHY this needed escalation (cross-domain, security vs delivery trade-off) | PASS | "Why this needed cross-domain coordination" section explicitly frames OKR as board commitment and explains precedent risk for both security and OKR norms. |
| c8 | Output explicitly acknowledges both concerns are legitimate — does not start by ranking them, does not dismiss either as overblown | PASS | Opening: "Both leaders are correct on their own turf." Neither concern is dismissed; the structure explicitly decouples rather than ranks. |
| c9 | Output treats the CVSS 7.8 vulnerability as a non-negotiable constraint (HIGH severity, must be fixed before exposing more attack surface to it via the new onboarding flow), not as a tradable priority | PASS | Gate in Option A: "Security signs off that residual CVSS is ≤ 4.0 with compensating control in place" — shipping without this is not presented as an option. |
| c10 | Output assesses sequencing options — auth fix first then onboarding, parallel work with onboarding behind a feature flag until auth is patched, or partial onboarding flow scoped to avoid touching auth — with reasoning for the recommended path | PASS | Option A = scoped onboarding avoiding vulnerable surface (parallel with compensating control). Option B = auth rebuild first then onboarding. Reasoning given in trade-off table. |
| c11 | Output's recommendation is concrete — a specific sequencing or parallel plan with handoffs and dates — not 'have a meeting' or 'you two work it out' | PASS | Named handoffs with dates: "Handoff #1: CTO → CPO on Thu 18 Jun", "Handoff #2: CPO → CTO on Mon 30 Jun". Table has specific date ranges per step. |
| c12 | Output preserves accountability — the CPO retains ownership of the onboarding OKR and the CTO retains ownership of the security fix; the coordinator coordinates, doesn't take over | PASS | Accountability section verbatim: "Coordinator coordinates; does not take over either workstream." Each table row has a named owner (CPO or CTO). |
| c13 | Output identifies whether the OKR deadline can shift — proposing a specific revised date or a scoped-down onboarding flow that meets the activation target without touching auth — rather than just declaring 'the OKR slips' | PASS | Option A: scoped onboarding ships Mon 30 Jun (OKR hit). Option B: ship Fri 17 Jul with ~50% booked at EOM. Both paths have specific dates, not just "slips". |
| c14 | Output frames the escalation rationale — why this needed cross-domain coordination (security trumps feature delivery, but the OKR is also a board commitment) — so the parties understand the call wasn't arbitrary | PASS | "the OKR is a board commitment... the way an org handles its first 'security says no, product says yes' collision becomes the precedent" — systematic framing provided. |
| c15 | Output identifies one or two questions for the executive level (CEO / board) if the trade-off is too large for the coordinator to settle — e.g. 'are we willing to communicate an OKR slip to the board to ship securely?' | PASS | Two explicit escalation questions: "Are we willing to communicate a ~2-week OKR slip..." and "Does the board accept a scoped-down onboarding flow...as Q2 OKR success" |

### Notes

The output is exceptionally strong — it meets or exceeds every criterion with specific dates, named owners, explicit trade-off tables, and a named accountability section. The only criterion capped at PARTIAL (c6) was already ceiling-limited by the test author, and the output actually delivers two specific deadline options with dates, which is full coverage within that cap.
