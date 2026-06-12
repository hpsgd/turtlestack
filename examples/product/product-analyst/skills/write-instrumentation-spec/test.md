# Test: write-instrumentation-spec works backwards and nails identity + PII

Scenario: The analyst must turn an activation metric into an event spec for the data-engineer. Because Cadence lets
users browse a demo anonymously before creating an account, the spec must define the anonymous-to-known identity
stitching rule. It must also classify PII and route it to GRC, derive events backwards from the metric (no
speculative tracking), and keep property names canonical and typed.

## Prompt

/product-analyst:write-instrumentation-spec the activation metric for Cadence: "the percentage of newly-signed-up teams where at least 3 members each post a standup update within the first 7 days." Cadence has both a web app and a mobile app, and new users can browse a demo anonymously before they create an account. Write the spec to {workspace}/work/docs/analytics/instrumentation-spec.md.

## Criteria

- [ ] PASS: Works backwards from the activation metric to the events required to compute it — every event is justified by the metric it serves, with no speculative "might as well track it" events
- [ ] PASS: Defines events in snake_case, verb_noun, past tense (e.g. account_created, standup_posted) with a single trigger each — one trigger, one event
- [ ] PASS: Produces a property dictionary where every property is typed (string / int / bool / timestamp / enum) and uses one canonical name per concept (e.g. user_id everywhere, never userId in one place and uid in another)
- [ ] PASS: Defines the identity model AND states the anonymous-to-known stitching rule explicitly — how pre-account anonymous demo activity reconciles to the user once they sign up — given the browse-before-signup flow
- [ ] PASS: States an attribution model (first / last / multi-touch) AND an attribution window, with the reason for the choice
- [ ] PASS: Classifies every property for PII and routes any PII to GRC Lead review as a checkpoint — does not wave PII through silently
- [ ] PASS: Closes with an explicit hand-off naming the data-engineer as the implementer of capture and pipeline — the spec defines what to measure, not how to build it
- [ ] PARTIAL: Flags high-cardinality properties (raw URLs, free-text search) and buckets or patterns them rather than storing them raw

## Output expectations

- [ ] PASS: Output includes an events table with trigger, metric served, and dedup logic per event
- [ ] PASS: Output includes a property dictionary table with a PII column populated for every property
- [ ] PASS: The identity-model section contains an explicit stitching rule, not just "track the user"
- [ ] PARTIAL: A volume/day estimate is noted per event for the data-engineer's storage/cost awareness
