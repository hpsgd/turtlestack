---
name: write-instrumentation-spec
description: "Specify the analytics events, properties, identity model, and attribution needed to measure a product's metrics, as a hand-off to the data-engineer for implementation. Use when defining what events to track, designing an event schema, or preparing a tracking plan for engineering to build."
argument-hint: "[metric or feature to instrument]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Write the Instrumentation Spec

Write the instrumentation spec for **$ARGUMENTS** — the precise definition of events, properties, identity model, and attribution that the metrics require. This is the hand-off artifact to the **data-engineer**, who implements the tracking and builds the pipelines. The spec must be precise enough that two engineers would build the same thing. It consumes the metric tree from `/product-analyst:design-metric-hierarchy` and produces the event plan that powers `/product-analyst:cohort-analysis` and `/product-analyst:design-experiment`.

## Step 1: Work backwards from the metrics

Never start from "what could we track?" — that produces over-tracking and a maintenance burden. Start from the metric tree: for each metric, list the events required to compute it. If a metric needs an event that doesn't exist, that's a new event. If an event serves no metric, it doesn't belong in the spec.

Verifiable output: a metric → required-events table, with every event justified by at least one metric.

## Step 2: Define each event

Every event gets a full definition. Use `snake_case`, `verb_noun` naming (`report_viewed`, `checkout_completed`).

| Field | Requirement |
|---|---|
| Event name | `snake_case`, verb_noun, consistent tense (past: `_viewed`, `_completed`) |
| Trigger | The exact user action or system condition that fires it — one trigger, one event |
| Properties | Key-value pairs, each with a type and allowed values |
| Metric served | Which metric(s) this event feeds |
| Volume estimate | Expected events/day — affects storage and cost (flag to data-engineer) |
| Dedup logic | What makes this event unique; how to avoid double-counting |

Verifiable output: a definition block per event with all six fields populated.

## Step 3: Specify the property schema

Properties are where instrumentation rots. Enforce consistency:

- Property names identical across events: always `user_id`, never `userId` in one place and `uid` in another
- Every property typed: string, int, bool, timestamp, enum (with allowed values)
- Avoid high-cardinality free-text properties (full URLs, raw search strings) — use route patterns and bucketed categories
- Every event carries `timestamp`, a user identifier, and a session identifier

Verifiable output: a property dictionary — name, type, allowed values, present-on-which-events.

## Step 4: Define the identity model

State how a user is identified across the anonymous-to-known boundary, which is where analytics most often breaks.

- **Anonymous ID** — assigned before login (device/cookie scoped)
- **User ID** — assigned at signup/login, stable across devices
- **Stitching rule** — how anonymous activity is reconciled to a user once they identify (alias the anonymous ID to the user ID; pre-identity events join retroactively)
- **Account/org ID** — for B2B, the workspace a user belongs to

State the rule for users across multiple devices and for shared accounts.

Verifiable output: the identity model with the stitching rule written explicitly.

## Step 5: Define attribution

State how an outcome is credited to its cause, and over what window:

- **Touchpoints captured** — what sources/campaigns/referrers are recorded
- **Attribution model** — first-touch, last-touch, or multi-touch (state which and why)
- **Attribution window** — how long after a touchpoint a conversion still counts (e.g. 30-day click)

Verifiable output: the attribution model and window, stated with the reason for the choice.

## Step 6: Write the privacy and PII note

Flag any property that is or could become PII (email, name, IP, precise location, free-text that may contain personal data). Mark each as PII / sensitive / safe. PII in events requires GRC Lead review — note it as a checkpoint, do not wave it through.

Verifiable output: a PII classification on every property.

## Step 7: Assemble the spec and hand off

Fill the instrumentation-spec template (`templates/instrumentation-spec.md`): event table, property dictionary, identity model, attribution, PII note. Write it to `docs/analytics/instrumentation-spec.md`. Close with an explicit hand-off block naming what the data-engineer implements and what needs GRC review.

## Rules

- Work backwards from metrics to events — never track speculatively. Every event must name a metric it serves, or it's cut
- Hand off to the data-engineer; do not implement the tracking yourself. You define the schema; they build the capture and the pipeline. State this boundary in the spec
- Property names are a contract — one canonical name per concept across every event. Inconsistent naming (`user_id` vs `userId`) is the single most common cause of broken analytics
- Always specify the identity stitching rule. "Track the user" is not a spec until you've said how anonymous and known identities reconcile
- Flag every PII property and route it to GRC Lead review — never ship PII instrumentation silently
- Avoid high-cardinality properties; they explode storage cost and rarely answer a question. Bucket and pattern instead
- Don't reuse one event for two distinct triggers — one trigger, one event, or analysis can't tell them apart

## Output Format

```markdown
## Instrumentation Spec: [metric or feature]

### Events
| Event name | Trigger | Metric served | Volume/day | Dedup |
|---|---|---|---|---|
| `verb_noun` | [exact trigger] | [metric] | [estimate] | [rule] |

### Property dictionary
| Property | Type | Allowed values | On events | PII? |
|---|---|---|---|---|
| `user_id` | string | — | all | no |

### Identity model
- Anonymous ID: [scope]
- User ID: [scope]
- Stitching rule: [how anonymous reconciles to known]
- Account ID: [if B2B]

### Attribution
- Model: [first / last / multi-touch] because [reason]
- Window: [duration]

### Hand-off to data-engineer
- Implements: [event capture, pipeline, storage]
- Needs GRC Lead review: [PII properties flagged above]
- Open questions for engineering: [volume/cost concerns]
```
