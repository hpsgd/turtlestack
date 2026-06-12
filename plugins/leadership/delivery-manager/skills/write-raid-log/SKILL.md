---
name: write-raid-log
description: "Write or add to a RAID log — risks, assumptions, issues, and dependencies for a delivery. Structures each item correctly (risk as cause not outcome, assumption with validation owner, issue with 48hr escalation, dependency with contact and date) and enforces a named owner per item. Use when starting a delivery, capturing a new risk/issue/dependency, or formalising delivery governance."
argument-hint: "[delivery or initiative name, or the item to capture]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Write a RAID log

Create or add to the RAID log for $ARGUMENTS. The RAID log (Risks, Assumptions, Issues, Dependencies) is the delivery-manager's primary governance artifact. This skill writes well-structured items; the weekly review and rot diagnostic live in the `review-raid-log` skill. The log lives at `docs/delivery/raid-log.md` (run `bootstrap` first if it is absent).

The four categories are not interchangeable. Conflating them is the most common failure. The discipline is to put each item in the right category, structure it so it is actionable, and give it a named owner.

## Step 1: Read the existing log

Read `docs/delivery/raid-log.md` if it exists. You are adding to a living document, not starting fresh each time. Note the highest existing ID in each category (R-, A-, I-, D-) so new items continue the sequence. If no log exists, copy `templates/raid-log.md` as the starting structure.

## Step 2: Classify the item

Decide which single category the item belongs to. Use this test:

| Question | Category |
|---|---|
| Has it happened yet? No, but it could | Risk |
| Is it believed true but unconfirmed? | Assumption |
| Has it already happened and is causing harm? | Issue |
| Is it work or a decision controlled by another team? | Dependency |

An item can move category over time: a risk that materialises becomes an issue; an assumption that relies on an external party is also a dependency. Capture it where it sits now, and note the link.

## Step 3: Structure the item for its category

### Risks

A risk is a cause, not an outcome. "The project will be delayed" is an outcome — useless. The risk is the cause that would produce it.

```markdown
| ID | Risk (cause) | Impact | Probability | Mitigation | Owner | Review date |
|---|---|---|---|---|---|---|
| R-007 | Supplier has not confirmed the integration environment date | Integration testing start slips ~2 weeks | High | Escalate to supplier account manager by Fri; line up a fallback sandbox | [name] | 2026-06-19 |
```

Structure every risk as cause → impact → probability → mitigation. Probability and impact each High/Medium/Low.

### Assumptions

```markdown
| ID | Assumption | Validation owner | Validate by | Status |
|---|---|---|---|---|
| A-004 | Legal will review the data-sharing agreement within two weeks | [name] | 2026-06-26 | Open |
```

Every assumption gets a validation owner and a date. Close it as Confirmed or Contradicted — an unvalidated assumption accumulates into a delivery surprise. If it depends on an external party, also raise it as a dependency.

### Issues

```markdown
| ID | Issue (what happened) | Impact | Resolution plan | Escalate by | Owner | Status |
|---|---|---|---|---|---|---|
| I-002 | Staging environment unavailable for 3 days | Blocks acceptance testing | DevOps rebuilding env; fallback to local stack | 2026-06-13 (48hr) | [name] | Open |
```

An issue with no resolution plan within 48 hours is escalated. The escalation date is mandatory for any blocking issue.

### Dependencies

```markdown
| ID | Dependency | Owning team | Contact | Status | Needed by |
|---|---|---|---|---|---|
| D-009 | Payment integration needs Payments API v2 migration | Payments | [name] | At risk | 2026-06-30 |
```

Status is one of On track / At risk / Blocked. Every dependency has a named contact at the other end — not a team name. Late dependencies are the single largest cause of delivery slippage, so the needed-by date is mandatory.

## Step 4: Assign a named owner

Every item — risk, assumption, issue, dependency — has a named accountable person. "Team" as owner means nobody. If you cannot name an owner, the item is not ready to log; find the owner first.

## Step 5: Write the item into the log

Append the item to the correct table in `docs/delivery/raid-log.md`. Keep the ID sequence continuous. Do not reorder or rewrite existing items.

## Rules

- Never log a risk as an outcome. "X will be late" is the impact; the risk is the cause that produces it.
- Never log an item without a named owner. "Team" is not an owner.
- Never put an item in two categories silently — if it spans (e.g. assumption + dependency), log it in its primary category and cross-reference the ID.
- Don't write down every conceivable assumption (assumption paralysis). Log the ones that, if wrong, would change a significant delivery decision.
- Every blocking issue has an escalation date within 48 hours. Every dependency has a needed-by date.
- Keep the log lean — this skill adds and structures items; `review-raid-log` closes and archives them.

## Output Format

Append to `docs/delivery/raid-log.md` using the four tables above, then report:

```markdown
## RAID items added: [delivery name]

| ID | Category | Summary | Owner | Key date |
|---|---|---|---|---|
| R-007 | Risk | Supplier integration env unconfirmed | [name] | Review 2026-06-19 |
| D-009 | Dependency | Payments API v2 migration | [name] | Needed by 2026-06-30 |

### Cross-references
- [Any items that span categories, e.g. "A-004 is also tracked as D-010"]

### Needs an owner (blocked from logging)
- [Any item that could not be logged because no owner could be named]
```
