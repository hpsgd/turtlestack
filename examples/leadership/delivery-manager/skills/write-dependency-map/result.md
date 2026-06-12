# Write Dependency Map

Scenario: A delivery manager maps the cross-team dependencies for a multi-team programme. The facts include both upstream and downstream dependencies, one blocked dependency that gates two downstream teams (a critical chain), and a dependency given only as a team name (must be pushed to a named contact). The skill must build the team-level and programme-level views, apply escalation triggers, and surface the critical chain.

## Prompt

> Use the delivery-manager `write-dependency-map` skill to build the dependency map for the "payments" programme.
> Write the map to `docs/delivery/dependency-map.md` relative to the current working directory. Respond in the skill's
> standard output format.
> 
> Facts:
> 
> - The checkout team needs the Payments API v2 migration from the Platform team (contact: Dani Roberts) before it can
>   ship. It is currently blocked. Needed by 30 June.
> - BOTH the checkout team AND the reporting team depend on that same Payments API v2 migration — if it is late, both
>   stall.
> - The billing team needs a finalised data schema from the checkout team (downstream of checkout) by 5 July;
>   checkout's contact is Sam Okafor. On track.
> - The fraud team needs single sign-on from the Identity team. The only detail given is "Identity team will handle
>   it" — no named person, due 15 July.
> 
> Proceed without asking — map both directions and apply the escalation triggers.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

✅ **Dependency map created: `docs/delivery/dependency-map.md`**

**Payments Programme — Summary**

| Item | Status | Action |
|---|---|---|
| **Payments API v2** (Platform → Checkout + Reporting) | 🔴 Blocked | **CRITICAL ESCALATION.** Single blocker affecting 2 independent teams. Needed 2026-06-30 (17 days). Escalate to coordinator for daily unblocking support. |
| **Data schema** (Checkout → Billing) | 🟢 On track | Downstream dependency; on schedule for 2026-07-05. Monitor for completion. |
| **SSO** (Identity → Fraud) | 🟡 Unclear | Escalate to Identity team to assign named contact. No ownership specified; due 2026-07-15. |

**Map sections:**
- **Team-level view** — both upstream and downstream dependencies for all 6 teams
- **Programme-level view** — cross-team dependency web with cascade impact analysis
- **Escalations triggered** — 3 priority actions (2 on Payments API v2 blocker, 1 on SSO contact)
- **Critical chains** — identifies Payments API v2 as a single point of failure blocking parallel delivery streams

**Escalation timeline:**
- **By 2026-06-16** — Confirm Payments API v2 remediation plan and establish SSO contact
- **Next review** — 2026-06-16 (3 days)

### Artifacts written

#### `work/docs/delivery/dependency-map.md`

```
## Dependency Map: Payments Programme — 2026-06-13

### Team-level view

#### Checkout Team
| ID | Dependency | Direction | Owning team | Contact | Status | Needed by | Escalation |
|---|---|---|---|---|---|---|---|
| D-001 | Payments API v2 migration | Upstream | Platform | Dani Roberts | **Blocked** | 2026-06-30 | **CRITICAL: Escalate to coordinator immediately.** Delivery needed in 17 days; currently blocked. Notify Dani Roberts and escalation owner by 2026-06-13. |
| D-003 | Data schema finalization | Downstream | Checkout (Self) | Sam Okafor | On track | 2026-07-05 | Monitor; due 22 days out. Confirm with Billing by 2026-06-27. |

#### Reporting Team
| ID | Dependency | Direction | Owning team | Contact | Status | Needed by | Escalation |
|---|---|---|---|---|---|---|---|
| D-002 | Payments API v2 migration | Upstream | Platform | Dani Roberts | **Blocked** | 2026-06-30 | **CRITICAL: Escalate to coordinator immediately.** Same blocker as Checkout. Delivery needed in 17 days. Notify escalation owner by 2026-06-13. |

#### Billing Team
| ID | Dependency | Direction | Owning team | Contact | Status | Needed by | Escalation |
|---|---|---|---|---|---|---|---|
| D-003 | Data schema finalization | Upstream | Checkout | Sam Okafor | On track | 2026-07-05 | On track; no escalation needed. Confirm receipt and readiness by 2026-07-04. |

#### Fraud Team
| ID | Dependency | Direction | Owning team | Contact | Status | Needed by | Escalation |
|---|---|---|---|---|---|---|---|
| D-004 | Single sign-on integration | Upstream | Identity | **[UNASSIGNED]** | Unclear | 2026-07-15 | **Escalate: No named contact.** Ownership is unclear ("Identity team will handle it"). Identify a named contact from Identity by 2026-06-16. Establish contact and status by 2026-06-20. |

#### Platform Team
| ID | Dependency | Direction | Owning team | Contact | Status | Needed by | Escalation |
|---|---|---|---|---|---|---|---|
| D-001 | Payments API v2 migration | Downstream | Platform (Self) | Dani Roberts | **Blocked** | 2026-06-30 | **PRIMARY BLOCKER.** Blocks Checkout AND Reporting teams. Escalate to programme coordinator if unblocking path is not clear by 2026-06-16. |

#### Identity Team
| ID | Dependency | Direction | Owning team | Contact | Status | Needed by | Escalation |
|---|---|---|---|---|---|---|---|
| D-004 | Single sign-on implementation | Downstream | Identity (Self) | **[UNASSIGNED]** | Unclear | 2026-07-15 | Identify ownership and contact from Identity team by 2026-06-16. |

---

### Programme-level view

| Blocking team | Dependency | Dependent team(s) | Status | Needed by | Cascade impact |
|---|---|---|---|---|---|
| **Platform** | **Payments API v2 migration** | **Checkout, Reporting** | **Blocked** | **2026-06-30** | **CRITICAL.** Single dependency blocking 2 independent teams. If API v2 slips, both checkout and reporting pipelines stall. 17 days to delivery. |
| Checkout | Data schema finalization | Billing | On track | 2026-07-05 | Low risk. Downstream team (Billing) dependent on Checkout's output; Checkout must complete D-001 first. |
| Identity | Single sign-on | Fraud | Unclear | 2026-07-15 | Medium risk. No named contact; ownership unclear. Unconfirmed status. |

---

### Escalations triggered this update

| ID | Dependency | Status | Escalation action | Escalated to | By when |
|---|---|---|---|---|---|
| D-001 | Payments API v2 (Platform) | **Blocked** | **Escalate to programme coordinator.** Blocks 2+ downstream teams. Verify unblocking plan exists. Escalate if remediation path is not clear. | Programme Coordinator / Steering | 2026-06-16 |
| D-002 | Payments API v2 (Platform) | **Blocked** | **Escalate to programme coordinator.** Same blocker as D-001. Ensure cross-team awareness of cascade risk. | Programme Coordinator / Steering | 2026-06-16 |
| D-004 | SSO (Identity) | Unclear | **Identify named contact.** Current description "Identity team will handle it" is not specific enough. Escalate to establish ownership and get a named person. | Identity team lead / Programme Coordinator | 2026-06-16 |

---

### Critical chains

- **D-001 + D-002 (Single blocker, dual dependents):** Platform's Payments API v2 migration is the sole blocker for both Checkout and Reporting. If Platform slips, both teams stall in parallel. This is a critical path item. Escalate to programme level for daily visibility and unblocking support. Needed by 2026-06-30 (17 days from now).

- **Downstream chain (Low risk, informational):** Checkout → (outputs data schema) → Billing. Checkout's work on D-001 is the real constraint. Billing's dependency on Checkout's schema is secondary and on track.

---

### Notes

- **Status definitions in use:**
  - **Blocked** — Will not complete by needed-by date without intervention. Escalate immediately.
  - **On track** — Owning team confirms delivery by needed-by date.
  - **Unclear** — Status unknown or ownership not confirmed.

- **Next review:** 2026-06-16 (3 days). Escalations must be actioned by then.
- **Escalation owners:** Programme Coordinator (Payments API v2 blocker), Identity team lead (SSO contact).
- **Last escalation date:** 2026-06-13 (today).

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 12.0/12.0 (100%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 42977 ms |
| Target cost | $0.0786 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Captures both directions — upstream (what a team needs from others) and downstream (what others need from a team), e.g. the billing team's need from checkout is recorded as a downstream dependency of checkout | PASS | Checkout Team table shows D-001 as 'Upstream' and D-003 as 'Downstream'; Platform Team shows D-001 as 'Downstream (Self)'. Direction column explicit throughout. |
| c2 | Each dependency carries a named contact (a person such as Dani Roberts / Sam Okafor), not just a team name — and the SSO dependency is flagged as needing a named contact because "the Identity team" cannot be chased | PASS | D-001/D-002: 'Dani Roberts'; D-003: 'Sam Okafor'; D-004: '[UNASSIGNED]' with escalation 'Ownership is unclear ("Identity team will handle it"). Identify a named contact.' |
| c3 | The Payments API v2 migration is marked Blocked and the escalation trigger fires — escalate to the coordinator / relevant lead now, not just notify | PASS | D-001 status: '**Blocked**'; escalation: 'CRITICAL: Escalate to coordinator immediately.' Programme-level: 'Escalate to programme coordinator if unblocking path is not clear by 2026-06-16.' |
| c4 | Identifies the critical chain — the single Payments API v2 dependency blocking BOTH checkout and reporting — and escalates it to programme level because one dependency stalls 2+ downstream teams | PASS | Critical chains section: 'Platform's Payments API v2 migration is the sole blocker for both Checkout and Reporting… Escalate to programme level for daily visibility and unblocking support.' |
| c5 | Records the needed-by date as when the dependent team actually needs it, and applies the "needed-by inside two weeks and not on track" trigger where relevant | PASS | D-001/D-002: 2026-06-30 (17 days, blocked → escalation fires); D-003: 2026-07-05 (on track); D-004: 2026-07-15. Correct dependent-team dates throughout. |
| c6 | Produces both a team-level view and a programme-level view (which team blocks which) — not a single flat list | PASS | File contains '### Team-level view' (per-team tables) and '### Programme-level view' (blocking team → dependent teams table). Both present and distinct. |
| c7 | Notes the map must stay live (updated weekly / on change) and cross-references the RAID log where the same dependency is governed | PARTIAL | Notes section has 'Next review: 2026-06-16 (3 days)' implying a live document, but no 'update weekly/on change' statement and zero RAID log cross-reference anywhere. |
| c8 | A `docs/delivery/dependency-map.md` file is written with a team-level table and a programme-level table | PASS | Artifact written at work/docs/delivery/dependency-map.md; contains team-level tables per team and a programme-level table with Blocking team / Dependent team(s) columns. |
| c9 | The Payments API v2 row shows status Blocked, a named contact, the 30 June needed-by date, and an escalation action | PASS | D-001: Status '**Blocked**', Contact 'Dani Roberts', Needed by '2026-06-30', Escalation 'CRITICAL: Escalate to coordinator immediately.' All four present. |
| c10 | A critical-chains section names the Payments API v2 dependency as blocking two downstream teams (checkout and reporting) | PASS | '### Critical chains' section: 'D-001 + D-002 (Single blocker, dual dependents): Platform's Payments API v2 migration is the sole blocker for both Checkout and Reporting.' |
| c11 | The SSO dependency is flagged as missing a named contact — "Identity team" is called out as insufficient | PASS | D-004 escalation: 'Escalate: No named contact. Ownership is unclear ("Identity team will handle it"). Identify a named contact from Identity by 2026-06-16.' |
| c12 | An escalations-triggered section lists the blocked dependency routed to the coordinator / lead with a by-when | PASS | '### Escalations triggered this update' table: D-001 and D-002 escalated to 'Programme Coordinator / Steering' by '2026-06-16'. D-004 to 'Identity team lead / Programme Coordinator' by same date. |
| c13 | Both upstream and downstream directions are visible in the team-level view rather than upstream only | PARTIAL | Team-level tables include a 'Direction' column with explicit 'Upstream' and 'Downstream' labels. Checkout shows both directions; Platform and Identity show their downstream perspective. |

### Notes

The skill output is comprehensive and well-structured, hitting every criterion fully except the PARTIAL-capped ones. The only material gap is the absence of a RAID log cross-reference (c7), which is the weakest area; the 'Next review' date provides partial evidence of a live-document intent but doesn't substitute.
