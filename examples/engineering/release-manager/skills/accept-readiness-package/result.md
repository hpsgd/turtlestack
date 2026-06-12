# Accept Readiness Package

Scenario: A delivery-manager hands the release-manager two release-readiness packages. One (Billing v2.4) is complete with evidence on every coordination item; the other (Search v3.0) has a missing ops runbook and a bare "Confirmed" on Support briefed with no evidence. The skill must gate the first to a GO input and return the second to sender as a NO-GO with the specific gaps named.

## Prompt

> Two release-readiness packages have been handed over by the delivery-manager. They are on disk at:
> 
> - `{workspace}/work/release-readiness/billing-v2.4-package.md` — Billing v2.4
> - `{workspace}/work/release-readiness/search-v3.0-package.md` — Search v3.0
> 
> Read both packages.
> 
> /release-manager:accept-readiness-package Billing v2.4 and Search v3.0 — packages at the paths above
> 
> Process BOTH packages. For each one, run the full skill: validate the package is complete, map each coordination item to a release-plan readiness gate, run the readiness assessment over the combined engineering + coordination picture, and produce a go/no-go input with explicit blockers. Use the Output Format from the skill for each. Treat a bare "Confirmed" with no evidence (a link, a date, a reference) as an open/unconfirmed item, exactly as the skill's rules require.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I have the skill instructions. Now I'll process both packages through the acceptance workflow.

## BILLING v2.4

### Package Validation

Examining each coordination item against the expected evidence:

| Coordination item | Evidence present | Status |
|---|---|---|
| Support briefed | Briefing doc `wiki/support/billing-v2.4-faq`, date 2026-06-09 | OK |
| GTM aligned | Launch plan `wiki/gtm/billing-v2.4-launch`, go-live 2026-06-12 09:00 UTC, deploy 2026-06-11 22:00 UTC (no clash) | OK |
| Ops runbook drafted | Runbook `wiki/ops/runbooks/usage-invoicing`, ops reviewed 2026-06-10, Grafana alerts added | OK |
| Governance approvals | SEC-2291 (no high), CAB-0884 (change board), LEG-1142 (legal) | OK |
| Customer comms planned | Comms plan `wiki/gtm/billing-v2.4-comms`, banner + email, scheduled 2026-06-12 08:00 UTC | OK |
| Gating dependencies cleared | RAID-204 (Resolved), RAID-211 (On track, staging deployed) | OK |

**Validation result: Complete** — All coordination items present with evidence. Package accepted.

### Engineering Assessment (RM direct)

| Gate | Status | Evidence |
|---|---|---|
| Definition of Done | PASS | All 6 stories in JIRA epic BILL-900 closed |
| Verification tests (staging) | PASS | `make test-billing-e2e` exit 0, 142 passed (2026-06-10) |
| No open critical/high bugs | PASS | tracker: label=billing-v2.4 priority>=high empty |
| Migrations tested | PASS | Migration 0042 (metering schema) up/down tested, rollback verified |
| Performance baseline | PASS | Invoice-gen p95 240ms vs baseline 260ms (within budget) |

### Combined Readiness Assessment

| Gate | Category | Source | Status | Evidence |
|---|---|---|---|---|
| Definition of Done | Engineering | RM direct | PASS | JIRA epic BILL-900 complete |
| Verification tests (staging) | Engineering | RM direct | PASS | `make test-billing-e2e` exit 0, 142 passed (2026-06-10) |
| No open critical/high bugs | Engineering | RM direct | PASS | Tracker clean (priority>=high empty) |
| Migrations tested | Engineering | RM direct | PASS | Migration 0042 up/down clean, rollback script verified |
| Performance baseline | Engineering | RM direct | PASS | p95 240ms vs 260ms baseline (within budget) |
| Support briefed | Operational | DM package | PASS | `wiki/support/billing-v2.4-faq`, briefing 2026-06-09 |
| Ops runbook / monitoring | Operational | DM package | PASS | `wiki/ops/runbooks/usage-invoicing`, ops reviewed 2026-06-10, Grafana alerts |
| Governance sign-offs | Operational | DM package | PASS | SEC-2291, CAB-0884, LEG-1142 |
| Gating dependencies clear | Operational | DM package | PASS | RAID-204 (Resolved), RAID-211 (On track, staging deployed) |
| Customer comms prepared | Communication | DM package | PASS | `wiki/gtm/billing-v2.4-comms`, banner + email 2026-06-12 08:00 UTC |
| GTM notified | Communication | DM package | PASS | `wiki/gtm/billing-v2.4-launch`, go-live agreed 2026-06-12 09:00 UTC |

### Go/No-Go Input: **GO**

All engineering gates pass. All coordination items in the delivery-manager's package carry evidence and are confirmed. Ops runbook drafted and reviewed. Governance approvals on file (security, change board, legal). Support briefed with escalation paths. Customer comms scheduled to deploy before go-live. No open critical/high bugs. Migrations tested and rollback verified. Performance within budget.

**No blockers.**

---

## SEARCH v3.0

### Package Validation

Examining each coordination item against the expected evidence:

| Coordination item | Evidence present | Status |
|---|---|---|
| Support briefed | — (no doc attached) | **GAP** |
| GTM aligned | Launch plan `wiki/gtm/search-v3-launch`, go-live 2026-06-15, deploy 2026-06-14 23:00 UTC | OK |
| Ops runbook drafted | Not written; ops have not reviewed | **GAP** |
| Governance approvals | SEC-2305 (no high findings) | OK |
| Customer comms planned | Comms plan `wiki/gtm/search-v3-comms`, in-app changelog | OK |
| Gating dependencies cleared | RAID-230 (embedding index backfill — On track) | OK |

**Validation result: Returned-to-sender** — Package incomplete. Two critical gaps prevent acceptance.

### Named Gaps

| Item | What is missing | Evidence needed | Owner |
|---|---|---|---|
| Support briefed | No briefing documentation or date provided | FAQ doc covering semantic ranking behaviour, known ranking edge cases, escalation path. Briefing date. | Support |
| Ops runbook drafted | Runbook for new ranking service not yet written; ops team has not reviewed | Ops runbook (wiki link) for the new ranking service, including metering/latency monitoring, alert thresholds, runbook review date and sign-off from ops team | DevOps / ops on-call |

### Assessment

The package is **not complete** and cannot be gated. Per the acceptance rules:

- **Support briefed:** marked "Confirmed" with no evidence (no briefing doc, no date). Per the skill rules, a bare "Confirmed" without evidence is an unconfirmed item. This is a no-go until the briefing doc and date are present.
- **Ops runbook drafted:** explicitly marked "Open" — the runbook has not been written and ops has not reviewed. This is an open coordination item. No-go until the runbook is drafted, reviewed, and link provided.

**Do not proceed to engineering assessment.** The package must be closed and re-handed.

---

### Next Steps

**Billing v2.4:** GO input ready for `/release-manager:release-plan` Step 6 (go/no-go decision).

**Search v3.0:** Return to the delivery-manager. Close the two named gaps (support briefing doc + date, ops runbook drafted + reviewed), then re-hand the package for re-assessment.

### Artifacts written

#### `work/release-readiness/search-v3.0-package.md`

```
# Release-readiness package — Search v3.0

Source: delivery-manager (`coordinate-release-readiness`)
Handed to: release-manager
Date: 2026-06-10
Release: Search v3.0 (semantic ranking)

This package collects the organisational readiness for the Search v3.0 release.

| Coordination item | Status | Evidence | Owner |
|---|---|---|---|
| Support briefed | Confirmed | — (no doc attached) | Support |
| GTM aligned | Confirmed | Launch plan `wiki/gtm/search-v3-launch`. Go-live 2026-06-15, deploy window 2026-06-14 23:00 UTC, no clash. | GTM — Daniel R. |
| Ops runbook drafted | Open | Runbook for the new ranking service not yet written; ops have not reviewed. | DevOps |
| Governance approvals | Confirmed | Security review sign-off `SEC-2305` (no high findings). | GRC Lead |
| Customer comms planned | Confirmed | Comms plan `wiki/gtm/search-v3-comms`: in-app changelog entry on go-live. | GTM — Daniel R. |
| Gating dependencies cleared | Confirmed | RAID `RAID-230` (embedding index backfill — On track). | Delivery-manager |

## Engineering evidence

- Definition of Done: met for all stories in the v3.0 epic.
- Verification tests in staging: `make test-search-e2e` exit 0 (run 2026-06-10, 98 passed).
- Open bugs: no open critical or high bugs.
- Migrations: N/A (no schema change this release).
- Performance: query p95 180ms in staging (baseline 175ms — within budget).

```

#### `work/release-readiness/billing-v2.4-package.md`

```
# Release-readiness package — Billing v2.4

Source: delivery-manager (`coordinate-release-readiness`)
Handed to: release-manager
Date: 2026-06-10
Release: Billing v2.4 (usage-based invoicing)

This package collects the organisational readiness for the Billing v2.4 release. Each
coordination item carries a status, evidence, and owner.

| Coordination item | Status | Evidence | Owner |
|---|---|---|---|
| Support briefed | Confirmed | Briefing doc `wiki/support/billing-v2.4-faq` covering FAQ, known issues (proration rounding), escalation path to billing-eng on-call. Briefing held 2026-06-09. | Support — Priya N. |
| GTM aligned | Confirmed | Launch plan `wiki/gtm/billing-v2.4-launch`. Agreed go-live 2026-06-12 09:00 UTC, no clash with the deploy window (deploy 2026-06-11 22:00 UTC). | GTM — Daniel R. |
| Ops runbook drafted | Confirmed | Runbook `wiki/ops/runbooks/usage-invoicing` for the new metering pipeline. Ops reviewed 2026-06-10, alerts on metering lag added to Grafana board `billing-prod`. | DevOps — on-call team |
| Governance approvals | Confirmed | Security review sign-off `SEC-2291` (no high findings). Change board approval `CAB-0884`. Legal reviewed billing terms change `LEG-1142`. | GRC Lead |
| Customer comms planned | Confirmed | Comms plan `wiki/gtm/billing-v2.4-comms`: in-app banner + email to all paid accounts, sent 2026-06-12 08:00 UTC (one hour before go-live). | GTM — Daniel R. |
| Gating dependencies cleared | Confirmed | RAID items `RAID-204` (metering schema migration — Resolved), `RAID-211` (Stripe webhook version bump — On track, deployed to staging). | Delivery-manager |

## Engineering evidence (for the release-manager's direct assessment)

- Definition of Done: met for all 6 stories in the v2.4 epic (`JIRA epic BILL-900`).
- Verification tests in staging: `make test-billing-e2e` exit 0 (run 2026-06-10, 142 passed).
- Open bugs: no open critical or high bugs against v2.4 (`tracker: label=billing-v2.4 priority>=high` empty).
- Migrations: metering schema migration tested in staging, rollback script verified (`migrate billing 0042` up+down clean).
- Performance: invoice-generation p95 240ms in staging load test (baseline 260ms — within budget).

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 11.0/11.5 (96%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 37779 ms |
| Target cost | $0.1064 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Billing v2.4 is validated as a complete package — all six coordination items present with evidence (link/date/reference), so it proceeds to assessment | PASS | Validation table shows all 6 items (Support briefed, GTM, Ops runbook, Governance, Comms, RAID) marked OK with wiki links/dates/ticket refs. Result: 'Validation result: Complete'. |
| c2 | Search v3.0 is returned-to-sender / NO-GO — the missing ops runbook is named as a gap, not downgraded to a warning | PASS | 'Ops runbook drafted \| Not written; ops have not reviewed \| **GAP**' in validation table; 'Validation result: Returned-to-sender — Package incomplete. Two critical gaps prevent acceptance.' |
| c3 | Search v3.0's "Support briefed: Confirmed" with no evidence is treated as an open/unconfirmed item — a bare status is not acceptance | PASS | 'Support briefed: marked "Confirmed" with no evidence (no briefing doc, no date). Per the skill rules, a bare "Confirmed" without evidence is an unconfirmed item. This is a no-go.' |
| c4 | Billing v2.4 produces a GO input; Search v3.0 produces a NO-GO input — the two verdicts are distinct and justified | PASS | Billing: 'Go/No-Go Input: GO — No blockers.' Search: 'The package is not complete and cannot be gated.' Distinct, justified, separate sections. |
| c5 | The engineering gates (Definition of Done, verification tests, open bugs, migrations, performance) are assessed directly by the release-manager — not assumed satisfied by the package | PASS | Separate 'Engineering Assessment (RM direct)' section for Billing assesses all 5 gates individually with evidence (JIRA BILL-900, make test-billing-e2e, tracker empty, Migration 0042, p95 240ms). |
| c6 | The skill does not re-coordinate the missing items itself (does not quietly draft the runbook or brief support) — it returns the gap to the delivery-manager | PASS | 'Return to the delivery-manager. Close the two named gaps (support briefing doc + date, ops runbook drafted + reviewed), then re-hand the package for re-assessment.' |
| c7 | Output uses the skill's structured Output Format — package-validation table, gate-mapping/combined-assessment table, and go/no-go input with a blockers table | PARTIAL | Package-validation table and combined-assessment table present for Billing. Named Gaps table for Search exists but uses 'Item \| What is missing \| Evidence needed \| Owner' rather than the exact schema. |
| c8 | Output contains two separate assessments (Billing v2.4 and Search v3.0), each with its own package-validation result and go/no-go verdict — not a single merged verdict | PASS | Output has '## BILLING v2.4' and '## SEARCH v3.0' sections, each with its own validation table and distinct verdict. Not merged. |
| c9 | Search v3.0's validation table marks the Ops runbook as a Gap (MISSING) and the result is "Returned-to-sender" → NO-GO | PASS | 'Ops runbook drafted \| Not written; ops have not reviewed \| **GAP**' and 'Validation result: Returned-to-sender — Package incomplete.' |
| c10 | The combined assessment table fills the engineering gates from each package's engineering evidence (test exit codes, migration logs, performance numbers) and the operational/communication gates from the coordination items | PASS | Billing combined table shows engineering gates with package evidence (make test-billing-e2e exit 0, Migration 0042 up/down, p95 240ms) and operational gates from coordination items (wiki links, SEC/CAB/LEG tickets). |
| c11 | Search v3.0's NO-GO lists blockers in a table with Blocker \| Gate \| Owner \| Action to clear — naming the runbook (DevOps) and the unconfirmed support briefing | PARTIAL | Named Gaps table lists both items with owners (DevOps for runbook, Support for briefing) but uses 'Item \| What is missing \| Evidence needed \| Owner' — not 'Blocker \| Gate \| Owner \| Action to clear'. |
| c12 | Output does not propose a conditional go for Search v3.0's missing package items (a missing package item is never a conditional go per the skill) | PASS | 'Do not proceed to engineering assessment. The package must be closed and re-handed.' No conditional language anywhere in Search v3.0 section. |

### Notes

Near-perfect execution: both packages processed correctly with Billing as GO and Search as returned-to-sender, bare 'Confirmed' treated as unconfirmed, engineering gates assessed directly from evidence, and no re-coordination attempted. The only gap is that the blockers table for Search v3.0 uses different column headings ('Item | What is missing | Evidence needed | Owner') rather than the exact 'Blocker | Gate | Owner | Action to clear' schema specified by the skill.
