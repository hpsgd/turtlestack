---
name: define-icp
description: "Define an Ideal Customer Profile from firmographic and behavioural criteria, built from current best customers and lost/churned accounts. Produces an account-level ICP distinct from an individual-level persona. Use to focus discovery, qualification, and targeting on the accounts most likely to get value."
argument-hint: "[product or segment, plus access to customer/account data]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Define an Ideal Customer Profile for $ARGUMENTS.

An ICP describes the *account* most likely to get value from and stay with the product — a firmographic and
behavioural profile, not an individual. It is distinct from a persona: the ux-researcher's
`/ux-researcher:persona-definition` describes a *person* (their goals, context, behaviours as a user); the
ICP describes the *organisation* you should target and qualify for. Both lenses are needed and they
compose — an account matches the ICP; people within it match personas.

Build the ICP from evidence, not aspiration: your current best customers and your lost/churned accounts
tell you who fits and who doesn't. Follow every step. The output is an ICP a team can qualify and target
against.

## Step 1: Identify best and worst-fit accounts

Pull two account sets from real data:

- **Best fit** — accounts with strong retention, expansion, high NPS/health, and low support burden. These
  define who gets value
- **Worst fit** — lost deals and churned accounts. These define who doesn't, and why

You need both. An ICP built only from wins is survivorship bias; the churned and lost accounts are where
the disqualifying signals live. This step is complete when both account sets are listed with the metric
that placed them.

## Step 2: Extract firmographic criteria

From the best-fit set, extract the structural attributes of the organisation:

| Dimension | Examples |
|-----------|----------|
| Industry / vertical | [the verticals where best-fit accounts cluster] |
| Company size | [employee count / revenue band] |
| Geography | [regions] |
| Tech stack / maturity | [systems they run that the product fits alongside] |
| Buying structure | [who holds budget; procurement complexity] |

Cross-check against the worst-fit set: which firmographic attributes predicted failure? This step is
complete when firmographic criteria are stated and contrasted against worst-fit accounts.

## Step 3: Extract behavioural criteria

Firmographics alone over-target — plenty of right-sized companies in the right vertical still churn. Add
the behavioural signals that separated best-fit from worst-fit accounts:

- **Trigger** — what was happening in the account when they adopted (a switch, a growth event, a regulation)
- **Activation behaviour** — what best-fit accounts did early that churned accounts didn't (e.g. connected
  a data source in week one, added more than three users)
- **Usage pattern** — the behaviour that correlates with retention and expansion

Behavioural criteria are usually the stronger predictor. This step is complete when behavioural criteria
are stated, drawn from the contrast between the two sets.

## Step 4: Write disqualifiers

State explicitly who is NOT the ICP — the firmographic and behavioural signals that predicted churn or
loss. Disqualifiers are as valuable as qualifiers: they stop the team chasing accounts that will churn.
This step is complete when there is an explicit "not the ICP" section.

## Step 5: Make it actionable for qualification

Turn the criteria into a qualification checklist a team can apply to a new account — a short set of
yes/no or scored signals that score account-product fit. This step is complete when the qualification
checklist exists.

## Rules

- **Build from data, not aspiration.** An ICP describing who you wish bought the product is marketing
  fiction. Derive it from who actually gets value and who actually churned.
- **Include the churned and lost accounts.** Wins-only ICPs miss the disqualifying signals that prevent
  future churn. The worst-fit set is half the analysis.
- **Behaviour beats firmographics.** Right-size, right-vertical accounts still churn. The behavioural
  signal (activation, trigger, usage) is the stronger predictor — don't stop at firmographics.
- **ICP is account-level; persona is person-level.** Don't collapse them. Refer individual-level work to
  `/ux-researcher:persona-definition`. State the boundary in the output.
- **Write explicit disqualifiers.** Who is *not* the ICP is as important as who is.
- **Re-derive as the data changes.** Product-market fit erodes; the ICP that held last year may not hold
  now. Date the ICP and set a review.

## Output Format

Write to `docs/product/icp-[segment].md`:

```markdown
# Ideal Customer Profile: [segment]

**Derived:** [date] · **Next review:** [date]

## Evidence base
| Set | Accounts | Placing metric |
|-----|----------|----------------|
| Best fit | ... | retention / expansion / NPS |
| Worst fit | ... | churn / lost deal |

## Firmographic criteria
| Dimension | ICP value | Predicted-failure value (worst fit) |
|-----------|-----------|-------------------------------------|
| ... | ... | ... |

## Behavioural criteria
| Signal | Best-fit behaviour | Worst-fit behaviour |
|--------|--------------------|--------------------|
| Trigger | ... | ... |
| Activation | ... | ... |
| Usage pattern | ... | ... |

## Not the ICP (disqualifiers)
- [firmographic or behavioural signal that predicted churn/loss]

## Qualification checklist
- [ ] [scored signal 1]
- [ ] [scored signal 2]

## Boundary
This is the account-level ICP. For individual-level user profiles, see
`/ux-researcher:persona-definition` — the lenses compose.
```

## Related Skills

- `/product-manager:strategic-voc-synthesis` — VoC signal sharpens the behavioural criteria.
- `/ux-researcher:persona-definition` — the individual-level counterpart; ICP and persona compose.
- `/product-manager:write-roadmap` — the ICP focuses which accounts the roadmap's outcomes serve.
