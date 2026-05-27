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

# Cross-domain conflict: onboarding OKR vs auth vulnerability

**Reading the situation.** Both leads are correct in their own frame. This is not resolvable by either of them alone, because each is optimising for the constraint they own. The coordinator's job here is to surface the trade-off cleanly, propose sequenced options, and escalate the policy question (not the technical one) if it doesn't settle.

**Date assumption (flagging):** "End of month" reads as end of Q2 (2026-06-30), since the framing ties it to Q2 OKRs and a 5-week runway from today (2026-05-27). If CPO means end of May (2026-05-31, 4 days), Option A below is the only physically possible path and Option B collapses — confirm before locking the plan.

---

## Accountability (stated explicitly)

- **CPO retains ownership** of the onboarding OKR and the activation target.
- **CTO retains ownership** of the auth vulnerability remediation (CVSS 7.8) and the rebuild.
- **Coordinator coordinates the handoff points and the escalation**; does not take over either workstream, does not set the OKR target, does not approve the security fix.

---

## Two deadline options to put to CPO + CTO

### Option A — Hit OKR, scoped onboarding that avoids vulnerable surface

| Week | Dates | Owner | Deliverable |
|---|---|---|---|
| W1 | Mon 2026-06-01 → Fri 2026-06-05 | **CTO** | Scope the vulnerable surface precisely (which endpoints/flows). Ship a **compensating control** by Fri (rate-limit + WAF rule + monitoring alert on the specific exploit path). Sign-off from security. |
| W1 (parallel) | Mon 2026-06-01 → Fri 2026-06-05 | **CPO + CTO jointly** | Re-scope onboarding flow to avoid the vulnerable auth surface (e.g. defer the auth-touching step, use existing hardened session path, or feature-flag the risky bit off). CTO signs off that the scoped flow doesn't traverse the CVE. |
| W2–W4 | Mon 2026-06-08 → Fri 2026-06-26 | **CPO** | Build + ship scoped onboarding. CTO available for architecture review, not driving. |
| W4 | Fri 2026-06-26 | **CPO** | Onboarding ships. OKR hit (with scope caveat documented). |
| W5+ | Mon 2026-06-29 → mid-Jul | **CTO** | Full auth rebuild, removes compensating control once verified. |

**Trade-off:** OKR met, but the activation target is hit on a *scoped* flow — measure carefully whether the descope materially hurts the activation lift you were aiming for. Compensating control is real risk reduction, not zero risk; if it fails, the vulnerability is still live. Document the compensating control + monitoring as the audit trail.

### Option B — Slip OKR by ~2 weeks, full security fix first

| Week | Dates | Owner | Deliverable |
|---|---|---|---|
| W1–W3 | Mon 2026-06-01 → Fri 2026-06-19 | **CTO** | Full auth rebuild. Security sign-off. |
| W4–W5 | Mon 2026-06-22 → Fri 2026-07-10 | **CPO** | Onboarding flow on rebuilt auth. |
| Slip | OKR hits ~2026-07-10, **~10 working days past EoQ2** | **CPO** | Communicate slip to board. |

**Trade-off:** Vulnerability gone before any new feature ships near it. OKR slips into Q3 — board-visible commitment misses. CPO needs cover from CEO/board to absorb the slip without it counting as a failed OKR.

---

## Escalation rationale (why this came to coordination, not resolved by CPO/CTO alone)

Security trumps feature delivery as an abstract principle, but the OKR is a **board-visible commitment** and a known-vulnerability ship establishes a **precedent that security flags are negotiable under deadline pressure** — which is the more expensive long-term outcome. Conversely, slipping the OKR without authorisation undermines CPO's mandate and the board's read of the company's delivery confidence. Neither lead can settle this alone because each would be ceding their own accountability boundary to do so. The trade-off is a **policy call about acceptable risk vs schedule integrity** — that belongs above CPO + CTO.

---

## Questions for the CEO / board if CPO + CTO can't settle

1. **Are we willing to communicate a ~2-week OKR slip to the board to ship securely, or do we accept compensating-control mitigation as sufficient to ship on time?** (Picks Option A vs B.)
2. **If we ship scoped (Option A), does the board accept the scoped flow as OKR success, or does it need to hit the original activation target unchanged to count?** (Decides whether Option A actually closes the OKR or whether it's a hidden slip.)

A third, only if the first two surface disagreement: **what is the company's standing policy on shipping with known CVSS ≥ 7 vulnerabilities behind compensating controls?** — so the next instance of this conflict doesn't need to escalate.

---

## What I'd recommend next (not deciding for them)

Get CPO and CTO in a 30-minute room **tomorrow (Thu 2026-05-28)** with this document. If they converge on Option A or B, the coordinator owns making sure the handoffs in the table happen on the dates listed. If they don't converge — specifically if CPO won't accept slip *and* CTO won't accept ship-with-compensating-control — escalate questions 1 and 2 to CEO by **Fri 2026-05-29** so a decision lands before W1 starts on Mon 2026-06-01.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.5/15.0 (97%) |
| Evaluated | 2026-05-27 |
| Target model | claude-opus-4-7 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 44997 ms |
| Target cost | $0.3533 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Coordinator does not simply side with one party — acknowledges both concerns are legitimate | PASS | "Both leads are correct in their own frame. This is not resolvable by either of them alone, because each is optimising for the constraint they own." |
| c2 | Coordinator assesses whether the work can be sequenced (auth fix first, then onboarding) or must be parallel | PASS | Option A proposes parallel work (W1 CTO scopes+compensating control, W1 CPO+CTO re-scope onboarding, W2-W4 ship). Option B proposes full sequence (auth rebuild W1-W3, then onboarding W4-W5). |
| c3 | Security vulnerability is treated as a constraint, not a competing priority — CVSS 7.8 is High severity | PASS | Escalation rationale states "a known-vulnerability ship establishes a precedent that security flags are negotiable under deadline pressure — which is the more expensive long-term outcome." |
| c4 | A concrete resolution is proposed with specific sequencing, not 'you two should work it out' | PASS | Two detailed tables with specific week-by-week dates (e.g. "Mon 2026-06-01 → Fri 2026-06-05"), named owners, and deliverables per step. |
| c5 | The resolution preserves accountability — CPO still owns the onboarding OKR, CTO still owns the security fix | PASS | Explicit "Accountability" section: "CPO retains ownership of the onboarding OKR... CTO retains ownership of the auth vulnerability remediation... Coordinator coordinates the handoff points and the escalation; does not take over either workstream." |
| c6 | Coordinator identifies whether the OKR deadline can be adjusted given the security constraint, with specific options | PARTIAL | Option B states "OKR hits ~2026-07-10, ~10 working days past EoQ2" with slip framing. Option A preserves EOM. Specific dates provided for both paths. |
| c7 | Escalation framing is clear — the coordinator explains WHY this needed escalation (cross-domain, security vs delivery trade-off) | PASS | "Neither lead can settle this alone because each would be ceding their own accountability boundary to do so. The trade-off is a policy call about acceptable risk vs schedule integrity — that belongs above CPO + CTO." |
| c8 | Output explicitly acknowledges both concerns are legitimate — does not start by ranking them, does not dismiss either as overblown | PASS | "Both leads are correct in their own frame." Opening section presents both constraints without ranking before presenting options. |
| c9 | Output treats the CVSS 7.8 vulnerability as a non-negotiable constraint (HIGH severity, must be fixed before exposing more attack surface to it via the new onboarding flow), not as a tradable priority | PASS | Option A requires CTO to "Ship a compensating control by Fri (rate-limit + WAF rule + monitoring alert on the specific exploit path). Sign-off from security" and CTO must sign off "that the scoped flow doesn't traverse the CVE." |
| c10 | Output assesses sequencing options — auth fix first then onboarding, parallel work with onboarding behind a feature flag until auth is patched, or partial onboarding flow scoped to avoid touching auth — with reasoning for the recommended path | PASS | Option A covers scoped onboarding avoiding vulnerable surface with feature-flag mention; Option B covers auth-first full sequence. Trade-offs stated per option. |
| c11 | Output's recommendation is concrete — a specific sequencing or parallel plan with handoffs and dates — not 'have a meeting' or 'you two work it out' | PASS | Two detailed tables with specific date ranges ("Mon 2026-06-01 → Fri 2026-06-05"), named owners (CTO, CPO, CPO+CTO jointly), and defined deliverables per step. |
| c12 | Output preserves accountability — the CPO retains ownership of the onboarding OKR and the CTO retains ownership of the security fix; the coordinator coordinates, doesn't take over | PASS | Dedicated "Accountability (stated explicitly)" section with three bullet points naming each party's retained ownership and the coordinator's bounded role. |
| c13 | Output identifies whether the OKR deadline can shift — proposing a specific revised date or a scoped-down onboarding flow that meets the activation target without touching auth — rather than just declaring 'the OKR slips' | PASS | Option A preserves EOM with scoped flow; Option B gives specific slip date "~2026-07-10, ~10 working days past EoQ2". Executive question 2 asks whether scoped flow counts as OKR success. |
| c14 | Output frames the escalation rationale — why this needed cross-domain coordination (security trumps feature delivery, but the OKR is also a board commitment) — so the parties understand the call wasn't arbitrary | PASS | "Security trumps feature delivery as an abstract principle, but the OKR is a board-visible commitment... slipping the OKR without authorisation undermines CPO's mandate and the board's read of the company's delivery confidence." |
| c15 | Output identifies one or two questions for the executive level (CEO / board) if the trade-off is too large for the coordinator to settle — e.g. 'are we willing to communicate an OKR slip to the board to ship securely?' | PASS | Two questions provided: "Are we willing to communicate a ~2-week OKR slip to the board to ship securely..." and "If we ship scoped (Option A), does the board accept the scoped flow as OKR success..." |

### Notes

The output is exceptionally well-structured and directly addresses every specified requirement, including the explicit accountability statement, two concrete deadline options with dated tables, escalation rationale paragraph, and two executive escalation questions. The one partial criterion (c6) is capped by the test author at PARTIAL; the output fully satisfies it with specific dates, so it earns the maximum allowed.
