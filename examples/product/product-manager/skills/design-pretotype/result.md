# Design Pretotype

Scenario: A PM wants to test demand for a bet cheaply before any build. The skill must state a Market Engagement Hypothesis in XYZ form (X% of Y will do Z) with a threshold committed before running, pick the cheapest pretotype that yields behavioural data, define a skin-in-the-game metric (likes/verbal enthusiasm score zero), specify the run, and pre-commit the proceed/kill decision.

## Prompt

> Use the product-manager `design-pretotype` skill to design a pretotype experiment to test whether there's
> real demand for a "bulk-retry-and-reconcile" view before we build it. The product has logged-in users.
> Write the experiment to a file under `docs/product/` in the current working directory, in the skill's
> standard format.
> 
> Proceed without asking — produce the pretotype design.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Done. Pretotype design written to `docs/product/pretotype-bulk-retry-reconcile.md`.

**Summary:**

The experiment tests whether users actually want bulk-retry functionality using a **Concierge MVP** (manually handled, zero-code). You'll invite ~25–30 users who've had failures, give them a list of failed operations, and ask them to request retries. If ≥15% of them request retries, the feature is worth building. If fewer do, either the friction isn't real or bulk-retry isn't the solution.

The concierge approach is cheapest and gives you real behavioral data (actual retry requests) plus workflow insights (which operations matter, how users batch them) — information a fake-door test can't provide. You can run this by end of next week.

### Artifacts written

#### `work/docs/product/pretotype-bulk-retry-reconcile.md`

```
# Pretotype: Bulk Retry & Reconcile

## Market Engagement Hypothesis
**15% of users who experience failed operations will submit at least 2 retry requests when offered a manual bulk-reconcile service within 1 week.**

Threshold committed before running: **15%**.

## Pretotype

| Field | Value |
|-------|-------|
| Type | Concierge MVP |
| Why this fits | Directly tests whether users have the friction point (failed operations they want to retry). Manual delivery reveals the actual workflow and what users prioritize. Generates real behavioral data (explicit retry requests) without engineering investment. If users won't request retries even when we hand them a list, the feature won't help. |
| Skin-in-the-game metric | Users who submit ≥2 retry requests OR complete ≥1 reconciliation action |
| Audience (Y) | Logged-in users who experienced ≥2 failed operations in the past 30 days |
| Sample size | 25–30 users |
| Duration | 7 days |
| Stop condition | Reach 30 users invited OR end of week, whichever comes first |
| Delivery method | Manual email from support: "We noticed some operations didn't complete for you. Here's what we found. Reply with which ones you'd like us to retry—just list the operation IDs." Include a simple reply template or optional web form. |
| Cost | None (internal labor only) |

## Decision rule (pre-committed)

- **Above 15%** (≥4 of 25–30 users submit retries): Proceed to build. The demand is validated—users have real friction and will use bulk-retry when it's available.
- **Below 15%** (<4 users): Kill the feature or pivot. Either:
  - Users don't experience failed operations as a problem in practice
  - They're solving it a different way (manual email, support tickets)
  - Batch-retry isn't the right solution (maybe they just want better failure notifications)
  - Investigate why via follow-up on non-respondents

## Next steps if threshold is met
1. Validate the workflow: Review which operations users requested retried and in what batches. Identify reconciliation patterns.
2. Prototype the UI based on concierge learnings.
3. Instrument for volume: Estimate monthly retry volume and reconciliation frequency to scope engineering.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 12.0/13.0 (92%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 44462 ms |
| Target cost | $0.0825 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | States a Market Engagement Hypothesis in XYZ form — "X% of Y will do Z" — specific on audience, behaviour, and threshold | PASS | "15% of users who experience failed operations will submit at least 2 retry requests when offered a manual bulk-reconcile service within 1 week." |
| c2 | Commits the X threshold BEFORE running, and says so explicitly (a threshold chosen after seeing results proves nothing) | PASS | "Threshold committed before running: **15%**." — explicit pre-commitment statement in the document. |
| c3 | Picks a specific pretotype (e.g. fake door / smoke test / concierge / Wizard of Oz) and justifies why it fits this hypothesis — the cheapest one that yields behavioural data | PASS | Type: "Concierge MVP"; Why: "Generates real behavioral data (explicit retry requests) without engineering investment. If users won't request retries even when we hand them a list, the feature won't help." |
| c4 | Defines a skin-in-the-game metric — a real action (clicks, email entry, money, time) — and explicitly rejects likes / verbal enthusiasm / "would you use it" as zero-signal | PARTIAL | Metric is a real action: "Users who submit ≥2 retry requests OR complete ≥1 reconciliation action". No explicit rejection of likes/verbal enthusiasm/stated intent anywhere in the document. |
| c5 | Specifies the run: audience (matching Y), sample size, duration, and stop condition — small and fast | PASS | Audience: "Logged-in users who experienced ≥2 failed operations in past 30 days"; Sample: 25–30; Duration: 7 days; Stop: "Reach 30 users invited OR end of week, whichever comes first." |
| c6 | Pre-commits the decision rule — above threshold → proceed; below → kill or pivot — written before running | PASS | "Above 15% (≥4 of 25–30 users): Proceed to build" and "Below 15% (<4 users): Kill the feature or pivot." |
| c7 | If a fake door is used, handles the dead end gracefully (a "coming soon / notify me" rather than a broken page) and avoids running at trust-eroding scale | PASS | A Concierge MVP was chosen, not a fake door — the conditional is not triggered. Graceful-dead-end handling is moot and no trust-eroding scale issue arises. |
| c8 | Distinguishes pretotype (should we build it) from prototype (can we build it right); flags any ad/tool spend | PARTIAL | Cost is flagged: "None (internal labor only)". No pretotype-vs-prototype distinction is drawn anywhere in the document or chat response. |
| c9 | Output file exists under `docs/product/` with an MEH in "X% of Y will Z" form and the threshold marked as pre-committed | PASS | File written to `work/docs/product/pretotype-bulk-retry-reconcile.md`; MEH in XYZ form present; "Threshold committed before running: 15%" explicit. |
| c10 | A specific pretotype type is chosen with a fit rationale, not a generic "run an experiment" | PASS | "Type: Concierge MVP" with a multi-sentence fit rationale in the Why field explaining direct behaviour testing and zero engineering cost. |
| c11 | The measured metric is a behaviour (an action taken), and stated intent / likes are explicitly excluded as evidence | PARTIAL | Metric is behavioural ("submit ≥2 retry requests"). Document never explicitly excludes stated intent, survey responses, or likes as invalid evidence. |
| c12 | The run spec includes audience, sample size, duration, and stop condition | PASS | All four present in the table: Audience, Sample size (25–30), Duration (7 days), Stop condition (30 invited OR end of week). |
| c13 | A pre-committed proceed/kill decision rule is recorded against the threshold | PASS | "Decision rule (pre-committed)" section with numeric proceed (≥4/25–30) and kill (<4) branches, both anchored to the 15% threshold. |
| c14 | Any paid tool / ad spend is flagged, and pretotype-vs-prototype is distinguished | PARTIAL | Cost flagged as "None (internal labor only)". Pretotype-vs-prototype distinction is absent from both the document and the chat summary. |

### Notes

Strong output: MEH in correct XYZ form, explicit pre-commitment, Concierge MVP well-justified with full run spec and proceed/kill rule. The two consistent gaps are (1) no explicit rejection of vanity/stated-intent metrics and (2) no pretotype-vs-prototype framing — both minor omissions against an otherwise complete design.
