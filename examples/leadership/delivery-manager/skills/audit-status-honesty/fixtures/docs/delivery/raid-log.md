# RAID Log — payments delivery

Last reviewed: 2026-06-13

## Risks

| ID | Risk (cause) | Impact | Probability | Mitigation | Owner | Review date | Status |
|---|---|---|---|---|---|---|---|
| R-001 | Supplier has not confirmed the integration environment date | Integration testing start slips ~2 weeks | High | Escalate to supplier account manager (no movement in 3 reviews) | Sam Okafor | 2026-06-13 | Amber |

## Assumptions

| ID | Assumption | Validation owner | Validate by | Status |
|---|---|---|---|---|
| A-001 | Legal will review the data-sharing agreement within two weeks | Priya Nandan | 2026-06-19 | Open |

## Issues

| ID | Issue (what happened) | Impact | Resolution plan | Escalate by | Owner | Status |
|---|---|---|---|---|---|---|
| I-002 | Reconciliation job failing overnight | Payments not reconciled; blocks acceptance | Root cause unknown | 2026-06-10 (now past) | Dani Roberts | Open |

## Dependencies

| ID | Dependency | Owning team | Contact | Status | Needed by |
|---|---|---|---|---|---|
| D-001 | Payments API v2 migration | Platform | Dani Roberts | Blocked | 2026-06-30 |
