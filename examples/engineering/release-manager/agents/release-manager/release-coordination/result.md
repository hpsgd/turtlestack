# Release Coordination

Scenario: User needs to coordinate a release that includes database migrations, a new feature behind a feature flag, a dependency security patch, and a rollback plan — with support team briefing before go-live.

## Prompt

> We need to release v2.4.0 this Thursday. It includes:
> 1. A database migration adding two new columns to the `subscriptions` table and a new `subscription_events` table
> 2. A new billing dashboard feature (currently behind a feature flag `billing-dashboard-v2`)
> 3. A security patch for CVE-2024-38372 in one of our dependencies
> 4. Some internal refactoring of the subscription service
> 
> The migration has been tested on staging. The security patch bumps a minor version. Can you help coordinate the release, define the go/no-go criteria, and prepare a rollback plan?

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

One important flag before the plan: **Thursday is tomorrow** (today is 2026-05-27), which means everything below that says "today" is time-sensitive right now.

---

## Release: v2.4.0

### Scope

| Change | Category | Risk | Notes |
|---|---|---|---|
| DB migration: 2 new columns on `subscriptions`, new `subscription_events` table | Migration | **High** | Schema change on a payment-critical table; code ↔ migration ordering matters |
| Billing dashboard v2 (`billing-dashboard-v2` flag) | Feature | Low | Flag off by default; blast radius contained at toggle |
| CVE-2024-38372 security patch (minor version bump) | Security | Medium | Bundled with feature release — see risk note below |
| Subscription service refactor | Infra/Refactor | **Medium–High** | Same surface area as the migration; correlated failure risk |

---

### Readiness Gates

| Gate | Status | Evidence needed |
|---|---|---|
| Tests pass (unit + integration) | **UNKNOWN** | Run full suite against current HEAD; need exit 0 |
| Staging acceptance suite | **UNKNOWN** | Confirm full acceptance suite — not just smoke tests |
| Security review: CVE-2024-38372 | **UNKNOWN** | What dependency? What's the CVSS score? Was a direct audit done or just the bump? |
| Migration tested on staging | **PARTIAL** | Tested ✓ — but has the **rollback** (DROP COLUMN, DROP TABLE) been exercised on staging? That's the part that matters when you're under pressure at 2am |
| Column type confirmed nullable / has defaults | **UNKNOWN** | Critical for safe rollback — non-nullable columns without defaults mean rollback is destructive if new code has written to them |
| Performance baseline captured | **UNKNOWN** | Capture error rate + p95 latency from production **today**, before any deploy |
| Rollback plan tested | **UNKNOWN** | See below |
| Support team briefed | **UNKNOWN** | Must happen today — they need the FAQ before the Thursday window opens |
| Release notes drafted | **UNKNOWN** | |
| Rollback owner assigned | **UNKNOWN** | One named person with access and authority |

---

### Deployment Strategy

**Two-phase deploy (migration-first), with feature flag for the dashboard.**

Phase 1 — Migration (can go tonight/early tomorrow):
- Deploy migration only, no code changes yet
- New columns must be **nullable or have server-side defaults** so existing code that doesn't know about them continues to work
- Verify `subscription_events` table created, columns present, no errors in prod

Phase 2 — Code + dependencies (Thursday release window):
- Deploy the subscription service refactor, CVE patch, and updated code that uses the new columns
- `billing-dashboard-v2` flag stays **OFF** for all users post-deploy; enable incrementally after verifying Phase 2 is stable

**Why two phases:** If you ship migration + code as one bundle and need to roll back code, the old code won't know about the new columns — but if the new code has already written data to them, the rollback may corrupt subscription records. Splitting phases gives you a safe intermediate state.

---

### Rollback Plan

**Code rollback (Phase 2 only):**
- Redeploy the previous release tag
- New columns remain in the schema but old code ignores them — safe, assuming columns are nullable/defaulted
- `subscription_events` table remains but is inert
- Timeline: ~10–15 min redeploy

**Feature flag rollback:**
- Toggle `billing-dashboard-v2` OFF
- Timeline: instant
- No code deploy needed

**Migration rollback (last resort only):**
- `ALTER TABLE subscriptions DROP COLUMN <col1>, DROP COLUMN <col2>`
- `DROP TABLE subscription_events`
- Only execute if Phase 2 code rollback is insufficient AND data integrity is at risk
- **Requires DBA sign-off** — destructive, irreversible if new code wrote rows to `subscription_events`

**Rollback criteria (establish baselines today):**

| Signal | Baseline (capture today) | Threshold | Action | Owner |
|---|---|---|---|---|
| API error rate | _capture pre-deploy_ | >2× baseline for 5 min | Automatic redeploy of previous tag | [assign: on-call engineer] |
| p95 latency on subscription endpoints | _capture pre-deploy_ | >3× baseline for 5 min | Investigate; rollback if not resolving in 10 min | [assign: on-call engineer] |
| Billing/payment failure rate | _capture pre-deploy_ | Any spike | Immediate rollback + incident | [assign: release manager] |
| `subscription_events` write errors | 0 (new table) | Any errors in first 30 min | Rollback Phase 2 code | [assign: on-call engineer] |
| Health check endpoints | 200 | Non-200 | Immediate rollback | Automated |

---

### Communication Plan

| Audience | What | When | Status |
|---|---|---|---|
| Engineering (on-call) | Deploy time, phases, rollback steps, who to call | Today | Pending |
| Support | Billing dashboard FAQ, known flag state (off by default), CVE patch context | **Today — before Thursday** | Pending |
| Leadership | Go/no-go, risk summary | Before Thursday window | Pending |
| Customers | No user-facing changes ship enabled (flag is off) — no external comms needed at deploy time. Send release notes after flag enable is validated | Post-flag-enable | N/A at deploy |

---

### Risk Flags

**1. Correlated failure risk — migration + refactor**
The subscription service refactor touches the same table the migration extends. If something breaks in the subscription path post-deploy, you won't immediately know which change is responsible. Ensure there's explicit test coverage of the subscription service against the new schema *on the current staging state* before go/no-go.

**2. Bundled CVE patch**
Security patches ideally ship as standalone hotfixes to minimise blast radius. Bundling here means the patch inherits the feature release's risk surface, and the feature release inherits the security urgency (creates pressure to ship even if gates aren't clean). If CVE-2024-38372 is actively exploitable, consider whether a standalone patch today is safer. If it's low-CVSS or not actively exploited, bundling Thursday is defensible — just document the decision.

---

### Open Questions (need answers before go/no-go)

Before I can call this a firm GO, please confirm:

1. Are the two new `subscriptions` columns **nullable or do they have server-side defaults**? (Determines whether rollback is safe without data loss)
2. Has the migration **rollback** (DROP operations) been tested on staging, or only the forward migration?
3. Which dependency carries CVE-2024-38372, and what's the CVSS score? Has it been verified with a direct audit or just the version bump?
4. Who is the **rollback decision owner** on Thursday with authority to call it?
5. What are the current production baselines for subscription endpoint error rate and p95?

---

### Decision: **CONDITIONAL GO** (pending answers to open questions)

Engineering gate failures are never acceptable. The feature flag, staging test, and CVE patch are credible — but the migration rollback has not been confirmed tested, and the column nullability is unknown. **Confirm both today.** If rollback on staging passes and columns are nullable, this is a clean GO.

Timeline for today:
- [ ] Confirm column nullable/default status
- [ ] Exercise migration rollback on staging
- [ ] Assign rollback owner
- [ ] Capture production baselines
- [ ] Brief support team
- [ ] Brief on-call engineer with the two-phase deploy steps

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.5/18.0 (92%) |
| Evaluated | 2026-05-27 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 126260 ms |
| Target cost | $0.5292 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent checks all engineering gates (tests, staging verification, security review, migration rollback verified) before issuing a go/no-go | PASS | Readiness Gates table lists tests, staging acceptance, security review, migration rollback — all marked UNKNOWN/PARTIAL. Decision is CONDITIONAL GO pending answers to open questions. |
| c2 | Agent recommends feature flag strategy for the billing dashboard feature — not big-bang deployment | PASS | Phase 2: 'billing-dashboard-v2 flag stays OFF for all users post-deploy; enable incrementally after verifying Phase 2 is stable.' |
| c3 | Agent defines rollback criteria with specific thresholds (error rate >2x baseline, p95 latency >3x baseline) and assigns a rollback owner | PASS | Rollback criteria table: API error rate '>2× baseline for 5 min', p95 latency '>3× baseline for 5 min', plus '[assign: on-call engineer]' and '[assign: release manager]' columns. |
| c4 | Agent confirms support team must be briefed BEFORE deployment, not after | PASS | Communication plan: 'Support \| Billing dashboard FAQ, known flag state (off by default), CVE patch context \| Today — before Thursday \| Pending' |
| c5 | Agent categorises each change by risk: migration (medium-high), security patch (low-medium), feature flag (low), refactoring (low) | PARTIAL | Scope table has: migration=High (criterion: medium-high), security=Medium (criterion: low-medium), feature flag=Low ✓, refactor=Medium-High (criterion: low). Two of four match. |
| c6 | Agent records current baseline metric values before deployment so rollback thresholds can be evaluated post-deploy | PASS | Readiness Gate: 'Capture error rate + p95 latency from production today, before any deploy.' Rollback table: '_capture pre-deploy_' for all baselines. Timeline: '[ ] Capture production baselines'. |
| c7 | Agent identifies the migration as requiring special attention — rollback of a migration that has already altered production data is different from code rollback | PASS | Rollback Plan section separates 'Code rollback' from 'Migration rollback (last resort only)' noting it is 'destructive, irreversible if new code wrote rows to subscription_events.' |
| c8 | Agent produces a structured output with Scope table, Readiness gates, Strategy, Rollback Criteria, Communication plan, and Decision | PARTIAL | Output contains all six sections: Scope table, Readiness Gates table, Deployment Strategy, Rollback Plan (with criteria table), Communication Plan, and Decision: CONDITIONAL GO. |
| c9 | Agent refuses to override a failed engineering gate under time pressure | PASS | 'Engineering gate failures are never acceptable.' Decision remains CONDITIONAL GO despite 'Thursday is tomorrow' pressure noted at top. |
| c10 | Output's scope table lists all four release items individually — migration (subscriptions columns + subscription_events table), billing dashboard feature, CVE-2024-38372 patch, subscription service refactor — with risk per item | PASS | Scope table has all four rows: DB migration (2 columns + subscription_events), billing-dashboard-v2, CVE-2024-38372 patch, and subscription service refactor — each with a Risk column. |
| c11 | Output's risk classification matches the asks: migration medium-high (data shape change + new table), security patch low-medium (named CVE, minor bump), feature flag low (off by default), refactor low (unless tests are weak), with reasoning per | PARTIAL | Feature flag=Low ✓ with reasoning. Migration=High (not medium-high), security=Medium (not low-medium), refactor=Medium-High (not low). Reasoning is provided per item but two of four levels diverge notably. |
| c12 | Output's go/no-go gates require evidence per gate — staging test pass with screenshot/log, migration applied + reverted on staging, security scan re-run, baseline metrics captured — not just 'team confirms' | PASS | Evidence column: 'need exit 0', 'full acceptance suite — not just smoke tests', 'CVSS score? Was a direct audit done or just the bump?', 'has the rollback (DROP operations) been exercised on staging?' |
| c13 | Output's rollback plan distinguishes code rollback (redeploy previous artefact) from data/migration rollback (the new columns/table either need a separate down-migration or a forward-fix-only policy if data was already written), naming which it is for THIS migration | PASS | Three named sections: 'Code rollback (Phase 2 only)' = redeploy previous tag; 'Migration rollback (last resort only)' = ALTER/DROP with DBA sign-off; notes 'irreversible if new code wrote rows.' |
| c14 | Output's rollback thresholds are concrete and pre-defined — error rate >2x baseline, p95 latency >3x baseline (or similar), with the baseline values recorded BEFORE deploy so the comparison is well-defined | PASS | Rollback criteria table: '>2× baseline for 5 min' and '>3× baseline for 5 min', baseline column shows '_capture pre-deploy_' for all metrics requiring comparison. |
| c15 | Output assigns a named rollback owner (single accountable person, not 'the team') with on-call coverage for at least the post-deploy window | PASS | Rollback criteria table uses '[assign: on-call engineer]' and '[assign: release manager]' per signal, plus Open Question #4: 'Who is the rollback decision owner on Thursday with authority to call it?' |
| c16 | Output's communication plan briefs the support team BEFORE deploy with the new feature flag state, the migration impact (none expected user-facing), and the support script for any billing dashboard questions | PASS | Support row: 'Billing dashboard FAQ, known flag state (off by default), CVE patch context \| Today — before Thursday.' FAQ = support script; flag state = off by default; timing before deploy. |
| c17 | Output's feature flag strategy keeps `billing-dashboard-v2` off in production at deploy time, with a stated rollout plan (% rollout or whitelist of customers) AFTER the deploy is verified stable | PARTIAL | Flag stays OFF ✓ and 'enable incrementally after verifying Phase 2 is stable' — but no specific % rollout or customer whitelist plan is stated. |
| c18 | Output explicitly states the agent will NOT override a failed engineering gate under Thursday-deadline pressure — if any gate fails, NO-GO and reschedule | PASS | 'Engineering gate failures are never acceptable.' Decision section: 'Confirm both today. If rollback on staging passes and columns are nullable, this is a clean GO.' — no GO issued without gate closure. |
| c19 | Output's structured format covers Scope table, Readiness gates, Strategy, Rollback Criteria, Communication plan, and a final GO/NO-GO Decision with reasoning | PARTIAL | All six structural elements present and clearly labeled: Scope, Readiness Gates, Deployment Strategy, Rollback Plan (with criteria), Communication Plan, Decision: CONDITIONAL GO with reasoning. |

### Notes

The output is comprehensive and well-structured, covering nearly all criteria. The main gaps are: (1) risk levels for migration (High vs medium-high) and refactor (Medium-High vs low) diverge from the rubric's expectations, and (2) the feature flag rollout plan lacks specific % or whitelist detail after deploy verification.
