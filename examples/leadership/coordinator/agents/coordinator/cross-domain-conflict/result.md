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

I'm going to step into coordinator mode here because this needs cross-domain sequencing, not just a debate. Let me map the constraint conflict and present concrete paths forward.

---

## The Core Tension (Why This Needs Coordination)

**Both constraints are real and non-negotiable in isolation:**
- CPO: Onboarding ships by May 31 (Q2 OKR, board commitment, activation metrics)
- CTO: Auth vulnerability (CVSS 7.8) cannot ship in production code

**Why coordination matters:** This isn't a disagreement about facts. Both are correct. The question is *sequencing and risk appetite*, which requires CPO + CTO alignment on trade-offs, and escalation only if they fundamentally disagree on acceptable risk.

---

## Three Sequencing Paths (With Trade-offs)

### **Option A: Scoped Onboarding + Compensating Control** ✓ Hits OKR deadline

**Sequence:**
- **Week 1 (CTO + Security, Owner: CTO)** — Identify the specific auth surface the onboarding flow touches. Implement a compensating control (rate limiting, input validation, additional auth gate, or request signing requirement) that neutralises the CVSS 7.8 risk *for that flow only*. De-risk the vulnerability surface without a full rebuild. Ship compensating control by Friday May 17.
- **Week 2 (CPO + CTO, Owner: CPO)** — Build scoped onboarding flow that either avoids the vulnerable surface or runs behind the compensating control. Ship by May 31 (OKR delivered).
- **Week 3+ (CTO, Owner: CTO)** — Full auth system rebuild post-OKR. Compensating control removed once new auth is live.

**Trade-off:**
- ✅ OKR ships on time
- ✅ Vulnerability is mitigated for onboarding flow
- ⚠️ Vulnerability remains in codebase for other surfaces
- ⚠️ Compensating control is temporary — must be removed before permanent use
- ⚠️ If compensating control design is flawed or scope creeps, you're exposed

**Owner accountability:** CPO owns onboarding delivery. CTO owns whether the compensating control actually neutralises the risk (technical sign-off required). Coordinator validates the handoff.

---

### **Option B: Full Auth Fix First, Then Onboarding** ✓ Hits Security First

**Sequence:**
- **Week 1 (CTO + Security, Owner: CTO)** — Full auth system rebuild. Complete and tested by Friday May 24.
- **Week 2–3 (CPO, Owner: CPO)** — Build onboarding against secure auth. Ship by Friday May 31 (or June 3–7 if integration takes 3 days).
- **OKR status:** Slips by 3–7 days depending on onboarding build time.

**Trade-off:**
- ✅ Full security posture — no compensating controls, no residual vulnerability
- ✅ Clean handoff — onboarding dev doesn't start until foundation is solid
- ❌ OKR ships late (June 3–7, not May 31)
- ❌ Board communication required: "Activation OKR slips by one week due to critical security fix"
- ✅ Low integration risk (onboarding builds against known-good auth)

**Owner accountability:** CTO owns auth fix completion (no slip past May 24). CPO owns onboarding timeline against clean auth. Coordinator tracks both.

---

### **Option C: Parallel Development + Gated Merge** ⚠️ High Risk / Time-Critical

**Sequence:**
- **Week 1 (both, concurrent)** — CTO rebuilds auth in isolated branch. CPO builds onboarding in parallel against current (vulnerable) auth *in a separate feature branch*.
- **Friday May 24 (CTO, Owner: CTO)** — Auth rebuild complete and tested. Merge to main.
- **Week 2 (CPO, Owner: CPO)** — Integrate onboarding against new auth, run full integration tests, ship by May 31.

**Trade-off:**
- ✅ Tries to hit OKR deadline
- ✅ Auth fix happens in parallel (doesn't block onboarding design)
- ❌ Integration risk is high — onboarding code written against old auth may break or require rework against new auth
- ❌ If integration takes more than 1 week (likely), OKR still slips
- ❌ Tight margin for error — any issues in week 2 sink both the OKR and security timeline

**Owner accountability:** CTO completes auth rebuild. CPO owns integration risk and onboarding delivery. Coordinator escalates if integration blocks ship.

---

## Accountability (Explicit)

- **CPO retains ownership of the onboarding OKR.** Accountable for delivery date and activation target. Will adapt scope and resource as needed.
- **CTO retains ownership of the auth security fix.** Accountable for vulnerability remediation and no production risk.
- **Coordinator orchestrates.** Sequences work, manages handoffs, removes blockers, escalates only if fundamental trade-off can't be resolved by working teams.

**Neither team can override the other.** CPO cannot demand shipping a known vulnerability. CTO cannot unilaterally slip an OKR. Coordinator breaks the tie by presenting options, not by deciding.

---

## Recommendation to CPO + CTO (Before Escalation)

**Try Option A first.** Compensating controls are a legitimate interim strategy — they're temporary, scoped, and time-bound. If the CTO can design and ship a control by May 17 that genuinely de-risks the onboarding surface, you hit the OKR and mitigate the vulnerability. The full rebuild happens after.

**Fallback to Option B if compensating control design is too risky or takes longer than 3 days.** A one-week OKR slip is better than shipping with residual vulnerability.

**Avoid Option C.** Integration risk under a tight deadline is exactly when preventable bugs slip through.

---

## Escalation Rationale (Why This Needs Board Visibility)

This isn't a working-team decision because the constraint conflict is *real* — security and feature delivery are both non-negotiable in the abstract. A compensating control is a risk mitigation play (Option A). An OKR slip is a board communication (Option B). Either way, *someone* is accepting a trade-off. That's a board-level appetite question, not an engineering call.

The escalation is: "CPO + CTO agree on technical path and risk profile. Coordinator confirms the path is credible. If they disagree on risk appetite (e.g., CTO won't accept compensating control, CPO won't slip OKR), escalate to CEO with two options and ask which risk the board accepts."

---

## Executive Escalation Questions (If CPO + CTO Can't Align)

**Question 1:** "Are we willing to communicate an OKR slip to the board (Option B: 1-week delay, full security), or do we ask CTO to design a compensating control that mitigates CVSS 7.8 for the onboarding surface only, with commitment to full auth rebuild post-OKR (Option A: on-time delivery, residual risk)?"

**Question 2:** "If we ship with a compensating control (Option A) and the control is later found to be inadequate or breaks in production, what's our incident response and communication plan to the board/customers?"

**Question 3 (if still unresolved):** "Which commitment is more important — the May 31 activation target, or a zero-known-vulnerability product? This isn't a trick question; the answer determines the path."

---

## Next Steps

1. **CTO + CPO discussion (same meeting, async OK):** Review the three options. CTO evaluates whether a compensating control is viable by May 17. CPO assesses whether a one-week OKR slip is acceptable given board expectations.
2. **Coordinator check-in (24 hours):** "Which path are we taking? What's the first blocker we need to unblock?"
3. **If alignment:** Coordinator publishes the sequencing plan, names owners, and tracks dates.
4. **If no alignment by EOD tomorrow:** Escalate to CEO with the board questions above.

The goal is to move *one way* clearly by EOW. Thrashing between options costs more time than either option itself.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.5/14.5 (100%) |
| Evaluated | 2026-05-12 |
| Target duration | 33775 ms |
| Target cost | $0.0983 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Coordinator does not simply side with one party — acknowledges both concerns are legitimate | PASS | "Both constraints are real and non-negotiable in isolation" and "Both are correct." |
| c2 | Coordinator assesses whether the work can be sequenced (auth fix first, then onboarding) or must be parallel | PASS | Three options presented: Option A (scoped sequential), Option B (auth-first sequential), Option C (parallel with gated merge). |
| c3 | Security vulnerability is treated as a constraint, not a competing priority — CVSS 7.8 is High severity | PASS | "Auth vulnerability (CVSS 7.8) cannot ship in production code" — treated as a hard constraint across all three options. |
| c4 | A concrete resolution is proposed with specific sequencing, not "you two should work it out" | PASS | Three detailed options each with named week-by-week steps, owners, and specific dates (May 17, May 24, May 31). |
| c5 | The resolution preserves accountability — CPO still owns the onboarding OKR, CTO still owns the security fix | PASS | Explicit section: "CPO retains ownership of the onboarding OKR. CTO retains ownership of the auth security fix. Coordinator orchestrates." |
| c6 | Coordinator identifies whether the OKR deadline can be adjusted given the security constraint, with specific options | PARTIAL | Option B explicitly states OKR slips to "June 3–7"; Option A keeps May 31. Both are specific and offered as choices. |
| c7 | Escalation framing is clear — the coordinator explains WHY this needed escalation (cross-domain, security vs delivery trade-off) | PASS | "Escalation Rationale" section: "security and feature delivery are both non-negotiable in the abstract... That's a board-level appetite question, not an engineering call." |
| c8 | Output explicitly acknowledges both concerns are legitimate — does not start by ranking them, does not dismiss either as overblown | PASS | Opening section lists both CPO and CTO constraints as "real and non-negotiable in isolation" with no ranking. |
| c9 | Output treats the CVSS 7.8 vulnerability as a non-negotiable constraint (HIGH severity, must be fixed before exposing more attack surface to it via the new onboarding flow), not as a tradable priority | PASS | Every option either mitigates via compensating control, fixes auth first, or gates onboarding merge behind completed auth rebuild. |
| c10 | Output assesses sequencing options — auth fix first then onboarding, parallel work with onboarding behind a feature flag until auth is patched, or partial onboarding flow scoped to avoid touching auth — with reasoning for the recommended path | PASS | Option A (scoped to avoid vulnerable surface), Option B (auth first), Option C (parallel gated merge) — all three assessed with trade-offs and a recommendation. |
| c11 | Output's recommendation is concrete — a specific sequencing or parallel plan with handoffs and dates — not "have a meeting" or "you two work it out" | PASS | Week-by-week breakdown with named owners (CTO, CPO) and explicit dates: May 17, May 24, May 31, June 3–7. |
| c12 | Output preserves accountability — the CPO retains ownership of the onboarding OKR and the CTO retains ownership of the security fix; the coordinator coordinates, doesn't take over | PASS | "Coordinator orchestrates. Sequences work, manages handoffs, removes blockers, escalates only if fundamental trade-off can't be resolved." |
| c13 | Output identifies whether the OKR deadline can shift — proposing a specific revised date or a scoped-down onboarding flow that meets the activation target without touching auth — rather than just declaring "the OKR slips" | PASS | Option A preserves May 31 via scoped onboarding; Option B gives specific slip to June 3–7. Neither just says "OKR slips." |
| c14 | Output frames the escalation rationale — why this needed cross-domain coordination (security trumps feature delivery, but the OKR is also a board commitment) — so the parties understand the call wasn't arbitrary | PASS | "security flag is negotiable precedent" concern raised; "OKR is a board commitment" explicitly named; escalation to CEO framed around risk appetite. |
| c15 | Output identifies one or two questions for the executive level (CEO / board) if the trade-off is too large for the coordinator to settle — e.g. "are we willing to communicate an OKR slip to the board to ship securely?" | PASS | Three explicit executive escalation questions provided, including verbatim match: "Are we willing to communicate an OKR slip to the board..." |

### Notes

The output is comprehensive and fully satisfies all criteria, including the named-owner sequencing, explicit accountability preservation, and specific executive escalation questions. The only ceiling constraint (c6: PARTIAL) is met at its maximum.
