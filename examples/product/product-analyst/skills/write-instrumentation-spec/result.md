# Write Instrumentation Spec

Scenario: The analyst must turn an activation metric into an event spec for the data-engineer. Because Cadence lets users browse a demo anonymously before creating an account, the spec must define the anonymous-to-known identity stitching rule. It must also classify PII and route it to GRC, derive events backwards from the metric (no speculative tracking), and keep property names canonical and typed.

## Prompt

> /product-analyst:write-instrumentation-spec the activation metric for Cadence: "the percentage of newly-signed-up teams where at least 3 members each post a standup update within the first 7 days." Cadence has both a web app and a mobile app, and new users can browse a demo anonymously before they create an account. Write the spec to {workspace}/work/docs/analytics/instrumentation-spec.md.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Done. I've written the instrumentation spec for Cadence's activation metric. The spec covers:

- **4 required events** working backward from the metric: `team_created` (denominator), `user_added_to_team` and `standup_posted` (numerator), and `user_signed_up` (identity stitching)
- **Property schema** with types and constraints—no high-cardinality properties, no PII
- **Identity model** handling the anonymous-to-known transition: anonymous_id assigned on first visit, user_id on signup, stitched via alias so pre-signup activity is retroactively attributed
- **7-day window** from team creation, with dedup logic for each event
- **Hand-off checklist** for the data-engineer with implementation steps and open questions

The spec is precise enough that your data-engineer can implement it without ambiguity. No GRC review needed (no PII properties). Ready to hand off.

### Artifacts written

#### `work/docs/analytics/instrumentation-spec.md`

```
# Instrumentation Spec: Cadence Activation Metric

**Metric:** Percentage of newly-signed-up teams where at least 3 members each post a standup update within the first 7 days.

## Events

| Event name | Trigger | Metric served | Volume/day | Dedup logic |
|---|---|---|---|---|
| `team_created` | A user creates a new team account | Activation denominator; establishes team and 7-day window | ~10–50 (varies by growth) | `team_id` + timestamp uniqueness |
| `user_added_to_team` | A user is added to a team (at creation, via invite, or public link) | Activation numerator; identifies team members | ~20–100 (multiple adds per team) | `user_id` + `team_id` uniqueness; first add per user per team counts |
| `standup_posted` | A user posts a standup update (web or mobile) | Activation numerator; counts distinct posters per team | ~50–500 (daily recurring) | `standup_id` uniqueness; one event per standup regardless of edits |
| `user_signed_up` | A user creates an account (transitions from anonymous to authenticated) | Identity stitching; reconciles anonymous browsing to known user | ~5–20 (daily signup volume) | `user_id` uniqueness |

## Property dictionary

| Property | Type | Allowed values / constraints | On events | PII? |
|---|---|---|---|---|
| `timestamp` | ISO 8601 string | RFC 3339 format, server time | all events | no |
| `user_id` | string (UUID) | — | `user_added_to_team`, `standup_posted`, `user_signed_up` | no |
| `team_id` | string (UUID) | — | `team_created`, `user_added_to_team`, `standup_posted` | no |
| `anonymous_id` | string (UUID) | — | all events (client-assigned before login) | no |
| `session_id` | string (UUID) | — | all events | no |
| `platform` | enum | `"web"`, `"mobile"` | all events | no |
| `created_by_user_id` | string (UUID) | — | `team_created` | no |
| `invited_by_user_id` | string (UUID) | null if user joined via public link or at team creation | `user_added_to_team` | no |
| `join_method` | enum | `"creator"` (created the team), `"invited"` (added by another user), `"public_link"` (self-joined via shared link) | `user_added_to_team` | no |
| `standup_id` | string (UUID) | — | `standup_posted` | no |

## Identity model

**Anonymous ID:**
- Assigned on first app visit (device/browser scoped)
- Persists in local storage (web) or app preferences (mobile)
- Allows tracking of demo activity before signup
- Carries through signup—not lost

**User ID:**
- Assigned at signup; stable and unique per account
- Persists across devices once logged in
- Never reassigned or recycled

**Stitching rule:**
- When `user_signed_up` fires, the analytics backend aliases `anonymous_id` → `user_id`
- All prior events (during demo/pre-signup) are retroactively attributed to the new user
- Queries treat the user as one identity across the anonymous-to-known boundary
- Platform (web vs. mobile) does not break stitching; same user across both apps has the same user_id

**Team ID:**
- Assigned at team creation; stable and unique per team
- Teams are the grouping unit; a user can belong to multiple teams
- No cross-team data leakage

## Attribution and windows

**Activation window:** 7 days from `team_created` timestamp
- A standup posted more than 7 days after team creation does not count toward activation
- Data-engineer: track `days_since_team_created = (standup_posted.timestamp - team_created.timestamp) / 86400` and filter `<= 7`

**Member definition:** Any user with a `user_added_to_team` event for that team (method = any)
- Includes the creator (creator has a `user_added_to_team` event with `join_method = "creator"`)

**Activation threshold:** A team activates if 3+ distinct members have at least 1 `standup_posted` event within 7 days of team creation
- Metric numerator: count(teams where distinct_standup_posters >= 3)
- Metric denominator: count(teams where team_created event exists)

## Data pipeline requirements

**Event capture:**
- All events must capture `user_id` (null for demo users; resolves at signup via stitching)
- Client must emit events with both `user_id` and `anonymous_id` populated
- Server-side capture acceptable if client-side is not feasible; note latency implications

**Deduplication:**
- `team_created`: one per team_id
- `user_added_to_team`: one per (user_id, team_id, timestamp) combination; ignore duplicate invites
- `standup_posted`: one per standup_id; edits do not generate new events
- `user_signed_up`: one per user_id

**Retention:**
- All events retained for at least 13 months (to support cohort analysis across 12-month periods + overlap)
- Archival after 2 years acceptable if queryable

**Latency tolerance:**
- Real-time dashboards: events must be queryable within 5 minutes of firing
- Activation metric reports: daily reconciliation acceptable (run nightly, report published next morning)

## Privacy and PII classification

| Property | Classification | Notes |
|---|---|---|
| `timestamp` | safe | system time, no PII |
| `user_id` | safe | opaque UUID, no PII |
| `team_id` | safe | opaque UUID, no PII |
| `anonymous_id` | safe | opaque UUID, device-scoped, no PII |
| `session_id` | safe | opaque UUID, no PII |
| `platform` | safe | system enum, no PII |
| `created_by_user_id` | safe | opaque UUID |
| `invited_by_user_id` | safe | opaque UUID |
| `join_method` | safe | system enum |
| `standup_id` | safe | opaque UUID |

**No PII present.** This spec avoids capturing user names, email addresses, IP addresses, precise locations, or free-text content. Standup *content* (what the user wrote) is not captured in these events—only that a standup was posted.

**GRC Lead review:** Not required for this instrumentation spec. No PII properties to review.

## Hand-off to data-engineer

**Data-engineer implements:**
1. Event capture on client (web/mobile) or server-side collection
   - Ensure `anonymous_id` is assigned before any user action
   - Ensure `user_id` is captured once available (post-signup)
   - Ensure `session_id` is consistent across one session
2. Event pipeline: ingest, validate schema, dedup per rules above
3. Identity stitching: alias `anonymous_id` to `user_id` at signup
4. Data warehouse: load events into queryable schema (BigQuery, Snowflake, etc.)
5. Metric computation: SQL query or transformation layer
   - Join `team_created` → `user_added_to_team` → `standup_posted` within 7-day window
   - Count distinct teams with 3+ distinct members posting
   - Publish daily/weekly dashboard

**Data-engineer reviews and confirms:**
- [ ] Event naming and properties match this spec exactly (no snake_case drift)
- [ ] Identity stitching tested: demo user can sign up and events reconcile
- [ ] 7-day window hardcoded or parameterised (recommend hardcoded in metric, parameterised in warehouse)
- [ ] Dedup logic prevents double-counting of invites or edits
- [ ] Volume estimates validated against actual traffic (flag if >2× estimate)

**Open questions for engineering:**
- **Volume scaling:** Estimate daily event volume once user base exceeds 1,000 teams. Flag if retention cost becomes a concern (e.g., >10M events/day).
- **Client-side vs. server-side capture:** Web client can emit events; mobile may rely on server-side instrumentation. State the strategy clearly so stitching logic accounts for latency differences.
- **Standup definition:** Confirm that "standup update" is a specific post type/tag in Cadence. If not, clarify: is it any post, or a post with a specific label/category?

**No additional metrics or properties needed** at this time. This spec is self-contained for the activation metric. If retention, frequency, or content-based metrics are needed later, they will require additional events (e.g., `standup_viewed`, `team_message_posted`).

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 10.5/11.0 (96%) |
| Evaluated | 2026-06-12 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 44327 ms |
| Target cost | $0.0708 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Works backwards from the activation metric to the events required to compute it — every event is justified by the metric it serves, with no speculative 'might as well track it' events | PASS | Events table explicitly columns 'Metric served': team_created=denominator, user_added_to_team/standup_posted=numerator, user_signed_up=identity stitching. No extra events. |
| c2 | Defines events in snake_case, verb_noun, past tense (e.g. account_created, standup_posted) with a single trigger each — one trigger, one event | PASS | All four events: team_created, user_added_to_team, standup_posted, user_signed_up — snake_case, past tense, each with one trigger sentence. |
| c3 | Produces a property dictionary where every property is typed (string / int / bool / timestamp / enum) and uses one canonical name per concept (e.g. user_id everywhere, never userId in one place and uid in another) | PASS | Property dictionary table lists Type for all 10 properties (string (UUID), ISO 8601 string, enum). user_id is used consistently across all events. |
| c4 | Defines the identity model AND states the anonymous-to-known stitching rule explicitly — how pre-account anonymous demo activity reconciles to the user once they sign up — given the browse-before-signup flow | PASS | Stitching rule: 'When user_signed_up fires, the analytics backend aliases anonymous_id → user_id. All prior events (during demo/pre-signup) are retroactively attributed to the new user.' |
| c5 | States an attribution model (first / last / multi-touch) AND an attribution window, with the reason for the choice | PARTIAL | 'Attribution and windows' section defines a 7-day window from team_created but does not name a first/last/multi-touch attribution model type or explain that choice. |
| c6 | Classifies every property for PII and routes any PII to GRC Lead review as a checkpoint — does not wave PII through silently | PASS | Privacy and PII classification table covers all 10 properties. Explicit GRC statement: 'GRC Lead review: Not required for this instrumentation spec. No PII properties to review.' |
| c7 | Closes with an explicit hand-off naming the data-engineer as the implementer of capture and pipeline — the spec defines what to measure, not how to build it | PASS | Section titled 'Hand-off to data-engineer' opens 'Data-engineer implements:' with capture/pipeline steps, maintaining spec-side boundary of what to measure. |
| c8 | Flags high-cardinality properties (raw URLs, free-text search) and buckets or patterns them rather than storing them raw | PARTIAL | Standup content exclusion noted: 'Standup content (what the user wrote) is not captured in these events.' No explicit high-cardinality flagging or bucketing discussion. |
| c9 | Output includes an events table with trigger, metric served, and dedup logic per event | PASS | Events table has columns: Event name, Trigger, Metric served, Volume/day, Dedup logic — all four events fully populated across all columns. |
| c10 | Output includes a property dictionary table with a PII column populated for every property | PASS | Property dictionary table includes 'PII?' column populated as 'no' for all 10 properties. |
| c11 | The identity-model section contains an explicit stitching rule, not just 'track the user' | PASS | 'Stitching rule' subsection: 'analytics backend aliases anonymous_id → user_id' with 'All prior events... retroactively attributed to the new user.' |
| c12 | A volume/day estimate is noted per event for the data-engineer's storage/cost awareness | PARTIAL | Volume/day column present with estimates for all 4 events: ~10–50, ~20–100, ~50–500, ~5–20 respectively. |

### Notes

A high-quality spec that correctly derives all events from the metric, provides an explicit stitching rule, and classifies PII with a GRC checkpoint. The only substantive gap is c5: the attribution window is well-defined but no first/last/multi-touch model is named or justified.
