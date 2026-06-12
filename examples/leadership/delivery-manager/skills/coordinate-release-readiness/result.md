# Coordinate Release Readiness

Scenario: A delivery manager coordinates the upstream readiness for a release. Some pieces are confirmed, one is an open gap (no ops runbook), and a gating dependency is still at risk. The skill must work the readiness checklist with evidence, refuse to present an incomplete package as complete, hand off to the release-manager, and not execute the release or own the go/no-go.

## Prompt

> Use the delivery-manager `coordinate-release-readiness` skill to coordinate readiness for the "payments v2.0"
> release. Write the release-readiness package to `docs/delivery/release-readiness.md` relative to the current working
> directory. Respond in the skill's standard output format.
> 
> State of play:
> 
> - Support has been briefed (FAQ + known issues handed over, dated 11 June).
> - GTM is aligned — launch announcement drafted, no clash with the deployment window.
> - Customer comms are planned (email + in-app, to go out after the release is verified stable).
> - Governance: security sign-off is on file.
> - The ops runbook for the new reconciliation behaviour does NOT exist yet — nobody has written it.
> - A gating dependency, the Payments API v2 migration (D-001), is still At risk.
> 
> Proceed without asking — work the checklist, assemble the package, and decide whether it can be handed off.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Release-Readiness Hand-off Decision

**Package Status: INCOMPLETE — Cannot hand off**

The release-readiness package for Payments v2.0 has two material gaps that block hand-off to the release-manager:

### Gaps Requiring Closure

1. **Ops runbook (CRITICAL)** — The runbook for the new reconciliation behaviour is not written. Ops cannot manage incident response or configuration without it. This is a prerequisite for release, not optional work.
   - Owner: DevOps / ops
   - Deadline: Must be written and signed off before release window opens

2. **Gating dependency at risk (BLOCKER)** — Payments API v2 migration (D-001) is listed as "At risk". An at-risk dependency means v2.0 inherits that risk. D-001 must either be cleared to "On track with confirmed date" or the release-manager must explicitly acknowledge the inherited risk.
   - Owner: Delivery-manager (escalate / resolve in RAID log)
   - Deadline: ASAP — blocks the entire release-readiness assessment

### What's in place ✓

- Support: briefed (11 June)
- GTM: aligned, no deployment clash
- Customer comms: planned (post-verification)
- Governance: security sign-off on file

### Next Actions

| Action | Owner | Urgency |
|---|---|---|
| Write + sign-off ops runbook | DevOps + ops lead | Before release window |
| Resolve D-001 status in RAID log | Delivery-manager | Immediate |
| Re-present package | Delivery-manager | Once gaps closed |

**Handed to release-manager:** Pending closure of gaps  
**Recommendation:** Do not proceed to release-plan readiness assessment until both items are resolved.

---

The package has been written to `docs/delivery/release-readiness.md` and is ready for team coordination. Both gaps are actionable and closure dates should be tracked in the weekly status report.

### Artifacts written

#### `work/docs/delivery/release-readiness.md`

```
# Release-Readiness Package: Payments v2.0

## Readiness Checklist

| Readiness item | Status | Evidence | Owner |
|---|---|---|---|
| Support briefed | ✓ Confirmed | FAQ + known issues handed over, dated 11 June | Support |
| GTM aligned | ✓ Confirmed | Launch announcement drafted; no clash with deployment window | GTM |
| Ops runbook drafted | ✗ **OPEN** | Ops runbook for new reconciliation behaviour NOT WRITTEN | DevOps / ops |
| Governance approvals | ✓ Confirmed | Security sign-off on file | GRC Lead |
| Customer comms planned | ✓ Confirmed | Email + in-app comms scheduled post-verification | GTM / product |
| Gating dependencies | ⚠ **AT RISK** | Payments API v2 migration (D-001) At risk | Delivery-manager |

## Open Items

### 1. Ops Runbook — New Reconciliation Behaviour
- **Owner:** DevOps / ops
- **Action:** Write and review ops runbook covering the new reconciliation behaviour in payments v2.0
- **Blocker:** Yes — ops cannot respond to incidents or configuration issues without this
- **Deadline:** Must be complete and signed off by ops before release window opens
- **Evidence required:** Runbook document + ops team sign-off (ops lead)

### 2. Gating Dependency: Payments API v2 Migration (D-001)
- **Owner:** Delivery-manager (escalate to release-manager)
- **Status:** At risk
- **Impact:** If D-001 is blocked or incomplete, it gates v2.0 entirely
- **Action:** Clarify current status — is D-001:
  - On track to complete in time? → Confirm date, move to "Cleared"
  - Slipping but will complete before release? → Document slip, accept risk
  - Blocked? → Escalate as blocker to release-manager and status report
- **Evidence required:** RAID log update with D-001 status and resolution date

## Readiness Assessment

**Package Status: INCOMPLETE**

The release-readiness package has **two material gaps** that prevent hand-off:

1. **Ops runbook is missing.** This is not a "nice to have" — ops cannot manage the new reconciliation behaviour without documented procedures. If ops responds to an incident during or after v2.0 release and the runbook doesn't exist, the incident response is delayed and the release is at risk. **This must be written and signed off before the release window opens.**

2. **Gating dependency D-001 is at risk.** The Payments API v2 migration is a prerequisite for payments v2.0. An at-risk dependency means the release inherits that risk. Either D-001 must be cleared to "On track" with a confirmed completion date, or the release-manager must acknowledge and accept the risk explicitly.

## Hand-off Status

**Cannot hand off to release-manager at this time.**

The delivery-manager's coordination role is to confirm the organisational and cross-team pieces are in place. Two pieces are not in place:
- The ops runbook gap is the delivery-manager's to close (coordinate with ops to write it).
- The at-risk dependency must be resolved in the RAID log before the package can be presented as ready.

## Next Actions

| Action | Owner | Date due | Status |
|---|---|---|---|
| Write ops runbook for new reconciliation behaviour | DevOps | Before release window | Open |
| Review and sign-off ops runbook | Ops lead | Before release window | Open |
| Update RAID log with D-001 status (cleared or risk accepted) | Delivery-manager | ASAP | Open |
| Re-present package to release-manager | Delivery-manager | Once gaps closed | Blocked on above |

---

**Assessment Date:** 13 June 2026  
**Release:** Payments v2.0  
**Prepared by:** Delivery-manager


```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 11.0/11.0 (100%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 32718 ms |
| Target cost | $0.0644 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Works the readiness checklist with evidence per item (support briefed with the 11 June date, GTM with the drafted announcement, security sign-off on file) — confirming each rather than assuming | PASS | File table: Support row cites 'FAQ + known issues handed over, dated 11 June'; GTM row cites 'Launch announcement drafted; no clash'; Governance row cites 'Security sign-off on file'. |
| c2 | Identifies the missing ops runbook as an open gap and names an owner (DevOps / ops) and an action/date to close it — not glossed over | PASS | File has dedicated Open Items section: 'Owner: DevOps / ops', action 'Write and review ops runbook', deadline 'Must be complete and signed off by ops before release window opens'. |
| c3 | Flags the at-risk gating dependency (D-001) as a blocker to a complete package — a release cannot be ready while a gating dependency is at risk, so it is raised in the RAID / status, not buried | PASS | Chat response labels D-001 'BLOCKER'; file dedicates a full Open Items section to D-001 with 'If D-001 is blocked or incomplete, it gates v2.0 entirely' and action to update RAID log. |
| c4 | Does NOT present the package as complete given the open runbook gap and the at-risk dependency — the package status is Incomplete with the open items listed (decision checkpoint honoured) | PASS | Chat: '**Package Status: INCOMPLETE — Cannot hand off**'; file header: '**Package Status: INCOMPLETE**' with both gaps listed under Open Items. |
| c5 | Confirms customer comms are planned now but go out only AFTER the release is verified stable, while support is briefed before deployment | PASS | File: Support 'dated 11 June' (before deployment); Customer comms evidence 'Email + in-app comms scheduled post-verification'. Chat: 'Customer comms: planned (post-verification)'. |
| c6 | Hands the package to the release-manager and explicitly stops at the gate — the release-manager owns go/no-go, deployment, and rollback; this skill does not execute the release | PASS | File: 'Cannot hand off to release-manager at this time'; Next Actions: 'Re-present package to release-manager \| Once gaps closed'. Chat: 'Handed to release-manager: Pending closure of gaps'. |
| c7 | Does not absorb the release-manager's engineering gates (tests, performance, migrations, rollback) into the readiness checklist — keeps the boundary | PARTIAL | Checklist covers only coordination items (support, GTM, governance, ops runbook, customer comms, gating deps). No tests, performance, migrations, or rollback rows appear. |
| c8 | A `docs/delivery/release-readiness.md` file is written with a readiness checklist table (item / status / evidence / owner) | PASS | File written to work/docs/delivery/release-readiness.md with table columns 'Readiness item \| Status \| Evidence \| Owner' and six populated rows. |
| c9 | The package status is Incomplete (not Complete) with the ops runbook gap and the at-risk dependency listed as open items | PASS | File Readiness Assessment: '**Package Status: INCOMPLETE**' with two numbered gaps: ops runbook missing and D-001 at risk, each with detail. |
| c10 | A hand-off note routes the package to the release-manager and states the release-manager owns the go/no-go — the delivery manager does not make that call | PASS | File 'Hand-off Status' scopes DM as coordinator, says 'release-manager must acknowledge and accept the risk explicitly'. Next Actions routes 'Re-present package to release-manager'. |
| c11 | The confirmed items (support, GTM, security sign-off, customer comms plan) carry evidence rather than bare assertions | PASS | Each confirmed row has specific evidence: '11 June' date, 'announcement drafted', 'sign-off on file', 'email + in-app comms scheduled post-verification'. |
| c12 | Output states the delivery manager coordinates readiness but does not execute the release, holding the boundary explicitly | PARTIAL | File: 'The delivery-manager's coordination role is to confirm the organisational and cross-team pieces are in place.' DM role scoped to coordination; release execution not claimed. |

### Notes

The output is a strong, complete execution: every checklist item carries its evidence, both gaps are named with owners and actions, the package is correctly marked INCOMPLETE, and the hand-off is properly gated. The boundary between DM coordination and release-manager go/no-go is maintained throughout.
