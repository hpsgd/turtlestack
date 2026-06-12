# RAID Log — payments delivery

Last reviewed: 2026-06-13

## Risks

| ID | Risk (cause) | Impact | Probability | Mitigation | Owner | Review date | Status |
|---|---|---|---|---|---|---|---|
| R-001 | Supplier has not confirmed the integration environment date | Integration testing start slips ~2 weeks | High | Escalate to supplier account manager by Fri | Sam Okafor | 2026-06-13 | Amber |

## Assumptions

| ID | Assumption | Validation owner | Validate by | Status |
|---|---|---|---|---|
| A-001 | Legal will review the data-sharing agreement within two weeks | Priya Nandan | 2026-06-19 | Open |

## Issues

| ID | Issue (what happened) | Impact | Resolution plan | Escalate by | Owner | Status |
|---|---|---|---|---|---|---|
| I-002 | Reconciliation job intermittently failing overnight | Some payments not reconciled | DevOps investigating root cause | 2026-06-14 | Dani Roberts | Open |

## Dependencies

| ID | Dependency | Owning team | Contact | Status | Needed by |
|---|---|---|---|---|---|
| D-001 | Payments API v2 migration | Platform | Dani Roberts | Blocked | 2026-06-30 |
