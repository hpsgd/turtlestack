---
# Match the model the agent declares (sonnet) in
# plugins/engineering/release-manager/agents/release-manager.md. The runner otherwise
# falls back to the harness default (Haiku), which is not what the
# agent is designed to run on.
target-model: claude-sonnet-4-6
---

# Test: Release coordination with migrations and feature flags

Scenario: User needs to coordinate a release that includes database migrations, a new feature behind a feature flag, a dependency security patch, and a rollback plan — with support team briefing before go-live.

## Prompt

We need to release v2.4.0 this Thursday. It includes:
1. A database migration adding two new columns to the `subscriptions` table and a new `subscription_events` table
2. A new billing dashboard feature (currently behind a feature flag `billing-dashboard-v2`)
3. A security patch for CVE-2024-38372 in one of our dependencies
4. Some internal refactoring of the subscription service

The migration has been tested on staging. The security patch bumps a minor version. Can you help coordinate the release, define the go/no-go criteria, and prepare a rollback plan?

## Criteria

- [ ] PASS: Agent checks all engineering gates (tests, staging verification, security review, migration rollback verified) before issuing a go/no-go
- [ ] PASS: Agent recommends feature flag strategy for the billing dashboard feature — not big-bang deployment
- [ ] PASS: Agent defines rollback criteria with specific thresholds (error rate >2x baseline, p95 latency >3x baseline) and assigns a rollback owner
- [ ] PASS: Agent confirms support team must be briefed BEFORE deployment, not after
- [ ] PASS: Agent categorises each change by risk: migration (medium-high), security patch (low-medium), feature flag (low), refactoring (low)
- [ ] PASS: Agent records current baseline metric values before deployment so rollback thresholds can be evaluated post-deploy
- [ ] PASS: Agent identifies the migration as requiring special attention — rollback of a migration that has already altered production data is different from code rollback
- [ ] PARTIAL: Agent produces a structured output with Scope table, Readiness gates, Strategy, Rollback Criteria, Communication plan, and Decision
- [ ] PASS: Agent refuses to override a failed engineering gate under time pressure

## Output expectations

- [ ] PASS: Output's scope table lists all four release items individually — migration (subscriptions columns + subscription_events table), billing dashboard feature, CVE-2024-38372 patch, subscription service refactor — with risk per item
- [ ] PASS: Output's risk classification matches the asks: migration medium-high (data shape change + new table), security patch low-medium (named CVE, minor bump), feature flag low (off by default), refactor low (unless tests are weak), with reasoning per
- [ ] PASS: Output's go/no-go gates require evidence per gate — staging test pass with screenshot/log, migration applied + reverted on staging, security scan re-run, baseline metrics captured — not just "team confirms"
- [ ] PASS: Output's rollback plan distinguishes code rollback (redeploy previous artefact) from data/migration rollback (the new columns/table either need a separate down-migration or a forward-fix-only policy if data was already written), naming which it is for THIS migration
- [ ] PASS: Output's rollback thresholds are concrete and pre-defined — error rate >2x baseline, p95 latency >3x baseline (or similar), with the baseline values recorded BEFORE deploy so the comparison is well-defined
- [ ] PASS: Output assigns a named rollback owner (single accountable person, not "the team") with on-call coverage for at least the post-deploy window
- [ ] PASS: Output's communication plan briefs the support team BEFORE deploy with the new feature flag state, the migration impact (none expected user-facing), and the support script for any billing dashboard questions
- [ ] PASS: Output's feature flag strategy keeps `billing-dashboard-v2` off in production at deploy time, with a stated rollout plan (% rollout or whitelist of customers) AFTER the deploy is verified stable
- [ ] PASS: Output explicitly states the agent will NOT override a failed engineering gate under Thursday-deadline pressure — if any gate fails, NO-GO and reschedule
- [ ] PARTIAL: Output's structured format covers Scope table, Readiness gates, Strategy, Rollback Criteria, Communication plan, and a final GO/NO-GO Decision with reasoning
