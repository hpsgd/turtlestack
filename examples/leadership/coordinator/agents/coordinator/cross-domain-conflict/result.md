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

## Recommendation

Both are right, and this is exactly the shape of conflict that needs coordination — not resolution by fiat. Below is the sequencing plan I'd propose, plus the two deadline options and the questions I'd escalate if CPO+CTO can't converge.

Today is **Fri 2026-07-24**. EOM is **Fri 2026-07-31**. One working week.

---

### Sequencing plan (Option 1 — hit the OKR)

**Premise:** scope the onboarding flow to avoid the vulnerable auth surface; ship the compensating control this week; full auth rebuild after OKR lands.

| Window | Owner | Deliverable | Handoff |
|---|---|---|---|
| **Mon 07-27 → Wed 07-29** | **CTO** | Compensating control for CVSS 7.8 vuln (WAF rule / rate limit / feature-flag gate on vulnerable code path). Deployed to prod. Security sign-off in writing. | Security + CTO confirm control blocks known exploit path. Coordinator receives written attestation. |
| **Mon 07-27 → Thu 07-30 (parallel)** | **CPO** | Scoped onboarding flow that does NOT touch the vulnerable auth surface. Scope cut confirmed with CTO's tech lead by Mon EOD. | CPO confirms scope hits activation KR (or a stated %). |
| **Thu 07-30** | **CPO + CTO** | Joint go/no-go: compensating control verified + scoped flow QA green. | Coordinator holds the decision meeting; 30 min max. |
| **Fri 07-31** | **CPO** | Ship scoped onboarding. OKR hit (or short by stated %). | Post-ship activation metric baseline captured. |
| **Mon 08-03 → Fri 08-28 (4 weeks)** | **CTO** | Full auth rebuild. Removes need for compensating control. | CTO owns; CPO consulted on any onboarding-touching surface. |
| **Wk of 09-01** | **CPO** | Onboarding v2 — the parts we cut in the scope-down — ships on rebuilt auth. | — |

### Sequencing plan (Option 2 — slip OKR, full fix first)

| Window | Owner | Deliverable |
|---|---|---|
| **Mon 07-27 → Fri 08-14 (3 wks)** | **CTO** | Full auth rebuild. |
| **Mon 08-17 → Fri 08-28 (2 wks)** | **CPO** | Full onboarding flow on rebuilt auth. |
| **OKR outcome** | | Slips **~4 weeks** from EOM to end of August. |

---

### Trade-off per option

- **Option 1** — OKR hit on the board commitment, vulnerability is *mitigated but not eliminated* for ~4 weeks. Risk: compensating controls have historically been under-maintained. Risk: scoped onboarding may hit only a fraction of the activation target — CPO to state that fraction on Mon.
- **Option 2** — Vulnerability eliminated. OKR slips ~4 weeks; board notification required. Risk: sets precedent that security work always displaces feature commitments (which may be the right precedent — see escalation rationale below).

---

### Accountability

- **CPO retains ownership of the onboarding OKR** — including the scope-down decision if Option 1 is chosen, and the board comms if Option 2 is chosen.
- **CTO retains ownership of the auth security fix** — both the compensating control (Option 1) and the full rebuild (either option). Security sign-off is the CTO's to obtain.
- **Coordinator coordinates**: convenes the Mon 07-27 kick-off, holds the Thu 07-30 go/no-go, tracks handoffs, escalates to CEO if the two workstreams diverge. Coordinator does **not** take over either workstream and does **not** cast the tie-breaking vote on Option 1 vs Option 2.

---

### Why this needed cross-domain escalation

In the abstract, security trumps feature delivery — shipping a known CVSS 7.8 vulnerability is not a decision either function should make unilaterally. But the OKR is a **board commitment**, and treating board commitments as freely slippable is itself a governance problem. The deeper concern is precedent: **if we ship with the known vuln (even mitigated) to hit the OKR, we've established that security flags are negotiable against delivery pressure** — which will re-emerge every quarter. If we slip the OKR, we've established that security is a hard gate — which is probably the right posture, but has to be an *explicit* decision by the CEO/board, not a coordinator's call. That's the trade-off that needs to settle above the CPO/CTO line.

---

### Questions for the CEO/board if this can't settle at CPO+CTO

1. **Are we willing to communicate an OKR slip (~4 weeks) to the board this quarter to ship with the vulnerability fully eliminated, rather than mitigated?**
2. **Does the board accept a scoped-down onboarding (targeting, say, 60–70% of the original activation KR) as "OKR hit" — and is that the posture we want to signal for future quarters where security work collides with feature commitments?**

My recommendation to the CEO would be **Option 1 with a hard, tracked commitment on the Aug 3–28 rebuild window** — but only if the CTO signs off in writing that the compensating control fully blocks the known exploit path. If the CTO won't sign that attestation, it's Option 2.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.5/15.0 (97%) |
| Evaluated | 2026-07-24 |
| Target model | claude-opus-4-7 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 35317 ms |
| Target cost | $0.3388 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Coordinator does not simply side with one party — acknowledges both concerns are legitimate | PASS | "Both are right, and this is exactly the shape of conflict that needs coordination — not resolution by fiat." |
| c2 | Coordinator assesses whether the work can be sequenced (auth fix first, then onboarding) or must be parallel | PASS | Option 1 proposes parallel work (Mon 07-27→Wed 07-29 CTO compensating control, Mon 07-27→Thu 07-30 CPO onboarding in parallel). Option 2 proposes sequential. Both assessed. |
| c3 | Security vulnerability is treated as a constraint, not a competing priority — CVSS 7.8 is High severity | PASS | "if the CTO won't sign that attestation, it's Option 2" — security sign-off is a hard gate, not a tradable priority. Compensating control or full fix required before ship. |
| c4 | A concrete resolution is proposed with specific sequencing, not 'you two should work it out' | PASS | Detailed table with specific dates (Mon 07-27, Wed 07-29, Thu 07-30, Fri 07-31, Mon 08-03→Fri 08-28) and named owners per step. |
| c5 | The resolution preserves accountability — CPO still owns the onboarding OKR, CTO still owns the security fix | PASS | "CPO retains ownership of the onboarding OKR... CTO retains ownership of the auth security fix... Coordinator coordinates: convenes... does not take over either workstream." |
| c6 | Coordinator identifies whether the OKR deadline can be adjusted given the security constraint, with specific options | PARTIAL | Option 2 states OKR "Slips ~4 weeks from EOM to end of August." Option 1 proposes hitting EOM. Both options address deadline adjustment with specific dates. |
| c7 | Escalation framing is clear — the coordinator explains WHY this needed escalation (cross-domain, security vs delivery trade-off) | PASS | "Why this needed cross-domain escalation" section explicitly frames security vs. board commitment vs. precedent-setting risk across two dimensions. |
| c8 | Output explicitly acknowledges both concerns are legitimate — does not start by ranking them, does not dismiss either as overblown | PASS | "Both are right" opens the response; both CPO and CTO concerns are treated as valid throughout without dismissal. |
| c9 | Output treats the CVSS 7.8 vulnerability as a non-negotiable constraint (HIGH severity, must be fixed before exposing more attack surface to it via the new onboarding flow), not as a tradable priority | PASS | Option 1 requires CTO written attestation that compensating control "fully blocks the known exploit path" before ship; if not, defaults to Option 2. Not negotiable. |
| c10 | Output assesses sequencing options — auth fix first then onboarding, parallel work with onboarding behind a feature flag until auth is patched, or partial onboarding flow scoped to avoid touching auth — with reasoning for the recommended path | PASS | Option 1: parallel work + scoped onboarding avoiding vulnerable surface. Option 2: sequential auth first then onboarding. Reasoning per option in trade-off section. |
| c11 | Output's recommendation is concrete — a specific sequencing or parallel plan with handoffs and dates — not 'have a meeting' or 'you two work it out' | PASS | Two full sequencing tables with exact dates, owners, deliverables, and handoff conditions. Final recommendation: "Option 1 with a hard, tracked commitment on the Aug 3–28 rebuild window." |
| c12 | Output preserves accountability — the CPO retains ownership of the onboarding OKR and the CTO retains ownership of the security fix; the coordinator coordinates, doesn't take over | PASS | Dedicated Accountability section states this verbatim: "Coordinator coordinates... does not take over either workstream and does not cast the tie-breaking vote." |
| c13 | Output identifies whether the OKR deadline can shift — proposing a specific revised date or a scoped-down onboarding flow that meets the activation target without touching auth — rather than just declaring 'the OKR slips' | PASS | Option 1: scoped onboarding ships Fri 07-31 avoiding vulnerable surface. Option 2: slips to end of August (specific date). Both concrete, not vague declarations. |
| c14 | Output frames the escalation rationale — why this needed cross-domain coordination (security trumps feature delivery, but the OKR is also a board commitment) — so the parties understand the call wasn't arbitrary | PASS | "shipping a known CVSS 7.8 vulnerability is not a decision either function should make unilaterally. But the OKR is a board commitment... the deeper concern is precedent." |
| c15 | Output identifies one or two questions for the executive level (CEO / board) if the trade-off is too large for the coordinator to settle — e.g. 'are we willing to communicate an OKR slip to the board to ship securely?' | PASS | Two explicit CEO/board questions provided, including "Are we willing to communicate an OKR slip (~4 weeks) to the board..." and scoped-down OKR acceptance question. |

### Notes

Exceptionally strong output that meets every criterion. The only minor gap is c6 (PARTIAL ceiling): the options cover deadline adjustment but don't deeply interrogate whether partial activation KR percentages could be formally renegotiated mid-quarter, though the executive questions partially address this.
