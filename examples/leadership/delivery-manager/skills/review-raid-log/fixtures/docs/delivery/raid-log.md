# RAID Log — payments delivery

Last reviewed: 2026-05-29

## Risks

| ID | Risk (cause) | Impact | Probability | Mitigation | Owner | Review date | Status |
|---|---|---|---|---|---|---|---|
| R-001 | Supplier has not confirmed the integration environment date | Integration testing start slips ~2 weeks | High | Escalate to supplier account manager | Sam Okafor | 2026-05-29 | Amber |
| R-002 | The payments programme will be delayed | We will miss the go-live | Medium | Watch it | Sam Okafor | 2026-05-29 | Amber |
| R-003 | Performance testing may find latency regressions late | Rework close to release | Low | Run an early load test | Dani Roberts | 2026-05-29 | Green |

> R-001 has been Amber at High/High with the same mitigation text and no movement since 2026-05-15 (across the last
> three weekly reviews).

## Assumptions

| ID | Assumption | Validation owner | Validate by | Status |
|---|---|---|---|---|
| A-001 | Legal will review the data-sharing agreement within two weeks | Priya Nandan | 2026-06-05 | Open |
| A-002 | Users have access to the new portal | — | — | Open |
| A-003 | The brand colours will not change before launch | — | — | Open |
| A-004 | Stakeholders read the weekly status report | — | — | Open |
| A-005 | The CI pipeline stays green | — | — | Open |
| A-006 | Nobody takes leave during the release window | — | — | Open |

## Issues

| ID | Issue (what happened) | Impact | Resolution plan | Escalate by | Owner | Status |
|---|---|---|---|---|---|---|
| I-001 | Staging environment unavailable for 3 days | Blocks acceptance testing | DevOps rebuilding env | 2026-05-30 | Sam Okafor | Resolved |
| I-002 | Reconciliation job intermittently failing | Some payments not reconciled overnight | Investigating root cause | 2026-05-29 | Dani Roberts | Open |

## Dependencies

| ID | Dependency | Owning team | Contact | Status | Needed by |
|---|---|---|---|---|---|
| D-001 | Payments API v2 migration | Platform | Dani Roberts | At risk | 2026-06-30 |
| D-002 | Single sign-on integration | Identity | Priya Nandan | On track | 2026-07-15 |
