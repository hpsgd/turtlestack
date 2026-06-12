# Test: write-discovery-plan sets up a continuous, trio-run, self-sustaining cadence

Scenario: A PM is standing up discovery for a slice. The skill must produce a Torres continuous-discovery
plan: tied to a desired outcome, run by the full product trio in every interview, on a protected weekly slot,
with automated recruiting set up before the first interview, and a synthesis/OST rhythm — not a one-off
research sprint.

## Prompt

Use the product-manager `write-discovery-plan` skill to set up a continuous-discovery cadence for the
"activation" slice of a B2B SaaS whose desired outcome is to lift week-one activation from 30% to 55%. The
product has logged-in users. Write the plan to a file under `docs/product/` in the current working
directory, in the skill's standard format.

Proceed without asking — produce the discovery plan.

## Criteria

- [ ] PASS: Ties discovery to a specific desired outcome (week-one activation 30% → 55%), not "learn about customers"
- [ ] PASS: Forms the product trio (PM + designer + engineer) and states all three attend EVERY interview — not a researcher reporting back to the PM
- [ ] PASS: Protects a recurring weekly slot and targets at least one customer conversation per week (continuous, not a sprint)
- [ ] PASS: Automates recruiting BEFORE the first interview (e.g. in-product prompt to a % of logged-in users feeding a scheduling pool) — names manual recruiting as the main cause of cadence collapse
- [ ] PASS: States the interview type (generative / switch) and a narrow target segment that will reach theme saturation (~20-30 interviews)
- [ ] PASS: Sets a synthesis / OST update rhythm (per-interview log, OST update every 3-4 interviews, monthly review) — discovery without synthesis is just conversation
- [ ] PASS: If any paid panel or recruiting service is mentioned, flags the cost and prefers the free in-product / customer-success route first
- [ ] PARTIAL: Frames the plan as runnable next week — a concrete first-two-weeks checklist

## Output expectations

- [ ] PASS: Output plan file exists under `docs/product/` and names the desired outcome as the thing discovery serves
- [ ] PASS: The plan names the trio and states explicitly that all three attend every interview (the no-filter rationale)
- [ ] PASS: The plan specifies an automated, self-sustaining recruiting mechanism set up before the cadence starts, not per-interview manual recruiting
- [ ] PASS: The plan sets weekly (or bi-weekly floor) cadence and a synthesis rhythm with OST updates, not a single discovery sprint
- [ ] PASS: A target segment narrow enough to saturate is named, with an interview type
- [ ] PARTIAL: Any paid recruiting path is cost-flagged with the free route preferred first
