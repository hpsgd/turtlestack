# Write Raid Log

Scenario: A delivery manager is handed four raw delivery facts that must be classified into the correct RAID categories and structured for action. One is phrased as an outcome (must be rewritten as a cause), one has no nameable owner (must be blocked from logging), one is an external dependency, and one is a live issue. The skill must place each in the right category, apply the per-category shape, and enforce a named owner per item.

## Prompt

> Use the delivery-manager `write-raid-log` skill to capture the following four items for the "payments" delivery.
> Write the RAID log to `docs/delivery/raid-log.md` relative to the current working directory. Respond in the skill's
> standard output format.
> 
> 1. "The project will be delayed if the supplier doesn't confirm the integration environment date." The supplier is
>    chased by Sam Okafor, our integration lead.
> 2. We believe Legal will sign off the data-sharing agreement within two weeks. Nobody has confirmed this with Legal
>    yet; Priya Nandan would be the one to check.
> 3. The checkout team needs the Payments API v2 migration before it can finish — that work is owned by the separate
>    Platform team. Our contact there is Dani Roberts. We need it by 30 June and it is looking shaky.
> 4. The staging environment has been down for two days and is blocking acceptance testing right now. Owner is Sam
>    Okafor; DevOps is rebuilding it.
> 
> Proceed without asking — classify, structure, and log each item.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## RAID items added: payments

| ID | Category | Summary | Owner | Key date |
|---|---|---|---|---|
| R-001 | Risk | Supplier integration environment unconfirmed | Sam Okafor | Review 2026-06-19 |
| A-001 | Assumption | Legal data-sharing agreement sign-off | Priya Nandan | Validate by 2026-06-26 |
| I-001 | Issue | Staging environment down (2 days) — blocks acceptance testing | Sam Okafor | Escalate by 2026-06-15 |
| D-001 | Dependency | Payments API v2 migration from Platform team | Dani Roberts | Needed by 2026-06-30 |

### Cross-references
- None — each item occupies a single category

### Owner assignments
- **Sam Okafor** owns the integration lead risk (R-001) and the staging rebuild issue (I-001)
- **Priya Nandan** validates the Legal assumption (A-001)
- **Dani Roberts** is the contact for the Platform team dependency (D-001)

**Log location:** `docs/delivery/raid-log.md`

### Artifacts written

#### `work/docs/delivery/raid-log.md`

```
# RAID Log — Payments Delivery

**Last reviewed:** 2026-06-13  
**Next review:** 2026-06-20

---

## Risks

| ID | Risk (cause) | Impact | Probability | Mitigation | Owner | Review date |
|---|---|---|---|---|---|---|
| R-001 | Supplier has not confirmed the integration environment date | Integration testing start slips ~2 weeks | High | Escalate to supplier account manager; line up fallback sandbox | Sam Okafor | 2026-06-19 |

---

## Assumptions

| ID | Assumption | Validation owner | Validate by | Status |
|---|---|---|---|---|
| A-001 | Legal will review and sign off the data-sharing agreement within two weeks | Priya Nandan | 2026-06-26 | Open |

---

## Issues

| ID | Issue (what happened) | Impact | Resolution plan | Escalate by | Owner | Status |
|---|---|---|---|---|---|---|
| I-001 | Staging environment unavailable (down for 2 days) | Blocks acceptance testing | DevOps rebuilding environment; fallback to local stack if needed | 2026-06-15 | Sam Okafor | Open |

---

## Dependencies

| ID | Dependency | Owning team | Contact | Status | Needed by |
|---|---|---|---|---|---|
| D-001 | Payments API v2 migration (required before checkout team can finish) | Platform | Dani Roberts | At risk | 2026-06-30 |

---

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 11.5/13.0 (88%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 39480 ms |
| Target cost | $0.0898 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Item 1 is logged as a Risk, and the outcome phrasing ("the project will be delayed") is rewritten as the cause ("supplier has not confirmed the integration environment date") — not logged verbatim as an outcome | PASS | R-001 Risk (cause) column reads: "Supplier has not confirmed the integration environment date" — outcome phrasing entirely absent. |
| c2 | The Item 1 risk is structured as cause → impact → probability → mitigation, with probability and impact each rated (High/Medium/Low) and a review date — not a bare sentence | PASS | R-001 row: Impact="Integration testing start slips ~2 weeks", Probability="High", Mitigation="Escalate to supplier…", Review date=2026-06-19. |
| c3 | Item 2 is logged as an Assumption with a validation owner (Priya Nandan) and a validate-by date, and is flagged as also a dependency on Legal (cross-reference) since it relies on an external party | PARTIAL | A-001 has Priya Nandan as validation owner and 2026-06-26 validate-by date, but chat response states "None — each item occupies a single category" for cross-references; no Legal dependency cross-reference present. |
| c4 | Item 3 is logged as a Dependency with the owning team (Platform), a named contact (Dani Roberts, not "the Platform team"), a status (At risk), and the needed-by date (30 June) | PASS | D-001: Owning team=Platform, Contact=Dani Roberts, Status=At risk, Needed by=2026-06-30. |
| c5 | Item 4 is logged as an Issue (already happening) with an impact, a resolution plan, and an escalation date within 48 hours — not as a risk | PASS | I-001 in Issues table: Impact="Blocks acceptance testing", Resolution plan="DevOps rebuilding…", Escalate by=2026-06-15 (48 hrs from 2026-06-13). |
| c6 | Every logged item carries a named owner (a person), and the skill states that "the team" is not an acceptable owner | PARTIAL | All four items have named persons (Sam Okafor×2, Priya Nandan, Dani Roberts). No explicit statement in output that "the team" is not an acceptable owner. |
| c7 | IDs follow the per-category sequence (R-, A-, I-, D-) so the log can grow without collisions | PASS | IDs assigned: R-001, A-001, I-001, D-001 — each prefixed by category letter. |
| c8 | The output distinguishes the four categories as genuinely different (risk = not happened yet / issue = already harming / dependency = controlled by another team / assumption = believed unconfirmed) rather than dumping all four into one list | PARTIAL | File has four separate tables (Risks, Assumptions, Issues, Dependencies) with distinct column schemas per category; no explicit definitional prose distinguishing the categories. |
| c9 | A `docs/delivery/raid-log.md` file is written with four separate tables (Risks, Assumptions, Issues, Dependencies), each item in its correct table | PASS | File work/docs/delivery/raid-log.md written with ## Risks, ## Assumptions, ## Issues, ## Dependencies sections, one item each in the correct table. |
| c10 | The risk row shows distinct cause, impact, probability, and mitigation columns — the cause is the unconfirmed environment date, NOT "the project will be delayed" | PASS | R-001 cause column: "Supplier has not confirmed the integration environment date"; separate Impact, Probability, Mitigation columns all populated. |
| c11 | The dependency row names Dani Roberts as the contact and 30 June as the needed-by date, with status At risk | PASS | D-001: Contact=Dani Roberts, Needed by=2026-06-30, Status=At risk. |
| c12 | The issue row carries an escalation date within 48 hours, marking it as a blocking issue | PASS | I-001 Escalate by=2026-06-15; today is 2026-06-13, so 48-hour window satisfied. |
| c13 | The assumption row has a validation owner and a validate-by date, with a cross-reference noting it is also a Legal dependency | PARTIAL | A-001 has Priya Nandan and 2026-06-26 validate-by date. No cross-reference to Legal dependency; chat explicitly says "None — each item occupies a single category." |
| c14 | The output summary lists each item with its category, owner, and key date, and flags any item that could not be logged for want of an owner | PARTIAL | Chat response summary table shows ID, Category, Summary, Owner, Key date for all four items. No items were unloggable in this scenario so the flagging path was not exercised. |

### Notes

The skill performs strongly on structural correctness — correct category placement, cause rewriting, per-category column schemas, and named person owners throughout. The main gap is the cross-reference requirement for item 2/A-001: the output explicitly declares no cross-references exist, missing the Legal-dependency flag called for in c3 and c13.
