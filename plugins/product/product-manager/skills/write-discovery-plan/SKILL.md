---
name: write-discovery-plan
description: "Set up a Teresa Torres continuous-discovery cadence — weekly customer interviews with the product trio, automated recruiting, and calendar discipline. Produces a discovery plan that runs continuously rather than as a one-off research sprint. Use when standing up discovery for a product slice or fixing a stalled interview cadence."
argument-hint: "[product slice and its desired outcome]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Set up a continuous-discovery cadence for $ARGUMENTS.

Most products fail because teams build the wrong thing, and the cure is talking to customers continuously
rather than in big-bang research sprints that go stale before you ship. This skill produces a discovery
plan based on [Teresa Torres's continuous discovery](https://www.producttalk.org/opportunity-solution-trees/):
weekly touch points, run by the team building the product, in pursuit of a desired outcome. The plan must
be runnable — a protected calendar slot, a self-sustaining recruiting mechanism, and the trio committed.

Follow every step. The output is a plan the team can start running next week.

## Step 1: Confirm the desired outcome

Discovery serves a specific outcome — the metric you're trying to move. Agree it with the product leader
before anything else. "Increase weekly active users" or "reduce week-one churn", not "learn about
customers". If the slice has a roadmap (`/product-manager:write-roadmap`), the desired outcome is the
roadmap root. This step is complete when one desired outcome is written and agreed.

## Step 2: Form the discovery trio

Name the [product trio](https://www.producttalk.org/opportunity-solution-trees/): the PM, a designer, and
an engineer. All three attend every interview. The rationale is non-negotiable: each role hears different
things — the engineer hears constraints and workarounds, the designer hears interaction friction, the PM
hears business context. If only the PM attends, the PM becomes a filter on what reaches the team, and
filters distort. This step is complete when three named people have committed.

## Step 3: Protect a recurring calendar slot

Set one recurring weekly slot for interviews — Torres's example is "Tuesday at 11am" — and protect it.
The target is at least one customer conversation per week. Bi-weekly is the floor for teams that genuinely
can't hit weekly; anything less frequent collapses back into periodic research, which is a weaker practice.
This step is complete when a recurring slot exists on the trio's calendars.

## Step 4: Automate recruiting

The most common reason a weekly cadence collapses is recruiting friction — hunting for participants each
week becomes a bottleneck that kills the cadence within a few weeks. Automate it from the start:

| Situation | Recruiting mechanism |
|-----------|----------------------|
| Active product with logged-in users | In-product prompt to a % of users: "Do you have 20 minutes to talk about your experience in exchange for [incentive]?" Agreers enter a scheduling pool; a calendar integration books the next slot |
| Pre-launch / small B2B / enterprise | Recurring pool via customer success, LinkedIn, industry communities, or a specialist panel — build a pool, don't recruit per-interview |

The goal: wake up Monday with an interview already on the calendar, having done nothing to arrange it that
week. If you reference a paid panel or recruiting service, flag the cost explicitly — prefer the in-product
or customer-success route first. This step is complete when the recruiting mechanism is specified and the
first participants are in the pool.

## Step 5: Define the interview type and target segment

State whether the cadence runs generative discovery interviews
(`/product-manager:write-interview-guide`), switch interviews
(`/product-manager:switch-interview`), or alternates. Name the target segment narrowly enough that themes
will saturate — 20-30 interviews across a reasonably homogeneous segment typically reaches 90-95%
saturation. This step is complete when interview type and segment are stated.

## Step 6: Set the synthesis and OST update rhythm

Discovery without synthesis is just conversation. Set the rhythm:

- After every interview: log the participant, type, and key signal to `docs/product/discovery-log.md`
- Every 3-4 interviews: revisit the opportunity space and update the OST
  (`/product-manager:synthesise-interviews`, `/product-manager:write-opportunity-solution-tree`)
- Monthly minimum: full OST review

This step is complete when the synthesis cadence is written into the plan.

## Rules

- **The trio attends every interview.** Researchers reporting back to a PM is not continuous discovery — it reintroduces the filter the trio exists to remove.
- **Protect the slot.** A discovery cadence that gets bumped for "more urgent" work isn't a cadence. The recurring slot is sacred.
- **Automate recruiting before the first interview, not after the cadence stalls.** Manual recruiting is the single biggest cause of collapse.
- **Weekly beats a sprint.** A one-time discovery sprint produces understanding that is months old by ship date. Continuous discovery keeps pace with a changing world.
- **Flag paid recruiting services.** In-product and customer-success recruiting are free; panels cost money. Name the cost and prefer the free route first.
- **Discovery serves an outcome, not curiosity.** If interviews aren't connected to a desired outcome and changing decisions, you're running discovery theatre.

## Output Format

Write the plan to `docs/product/discovery-plan-[slice].md`:

```markdown
# Discovery plan: [slice]

| Field | Value |
|-------|-------|
| Desired outcome | [metric, baseline → target] |
| Trio | [PM / designer / engineer] |
| Recurring slot | [day / time] |
| Cadence target | [weekly / bi-weekly] |
| Recruiting mechanism | [in-product / CS / panel] — [cost note] |
| Interview type | [generative / switch / alternating] |
| Target segment | [narrow segment] |
| Synthesis rhythm | [per-interview log; OST update every 3-4; monthly review] |

## First two weeks
- [ ] Calendar slot created and protected
- [ ] Recruiting mechanism live, first participants in pool
- [ ] First interview scheduled
- [ ] Discovery log initialised
```

## Related Skills

- `/product-manager:write-interview-guide` — the guide for each generative interview.
- `/product-manager:switch-interview` — the guide when the cadence runs switch interviews.
- `/product-manager:synthesise-interviews` — turn the interview window into OST updates.
- `/product-manager:write-opportunity-solution-tree` — the artifact discovery keeps current.
