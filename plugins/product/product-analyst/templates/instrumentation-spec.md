# Instrumentation Spec — [metric or feature]

> Produced by `/product-analyst:write-instrumentation-spec`. Hand-off artifact to the data-engineer.
> Precise enough that two engineers would build the same thing.

## Metrics this instruments

> Work backwards from metrics to events. Every event below must serve at least one metric here.

| Metric | Events required |
|---|---|
| | |

## Events

> `snake_case`, verb_noun, consistent past tense. One trigger per event.

| Event name | Trigger | Metric served | Volume/day | Dedup logic |
|---|---|---|---|---|
| `verb_noun` | exact user action or system condition | | estimate | what makes it unique |

## Property dictionary

> One canonical name per concept across every event. Typed. PII flagged.

| Property | Type | Allowed values | On events | PII? (safe / sensitive / PII) |
|---|---|---|---|---|
| `user_id` | string | — | all | safe |
| `timestamp` | timestamp | — | all | safe |
| `session_id` | string | — | all | safe |

## Identity model

| Element | Definition |
|---|---|
| Anonymous ID | scope (device / cookie) before login |
| User ID | scope after signup/login, stable across devices |
| Stitching rule | how anonymous activity reconciles to a user once identified |
| Account / org ID | for B2B, the workspace the user belongs to |
| Multi-device rule | how the same user across devices is handled |

## Attribution

| Element | Value |
|---|---|
| Touchpoints captured | sources / campaigns / referrers recorded |
| Attribution model | first-touch / last-touch / multi-touch |
| Why this model | |
| Attribution window | e.g. 30-day click |

## Hand-off to data-engineer

| Item | Detail |
|---|---|
| data-engineer implements | event capture, pipeline, storage, dashboards |
| Needs GRC Lead review | PII properties flagged above |
| Open questions for engineering | volume/cost concerns, sampling |
