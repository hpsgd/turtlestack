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
