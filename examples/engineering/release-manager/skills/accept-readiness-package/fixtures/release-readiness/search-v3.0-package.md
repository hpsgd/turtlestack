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
