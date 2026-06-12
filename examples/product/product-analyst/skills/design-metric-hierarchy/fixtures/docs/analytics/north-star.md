## North Star: Cadence

### Customer value moment

A team gets value when it runs its daily async standup and members stay aligned without holding a live meeting.

### North Star Metric

**Question it answers:** Are teams getting the alignment value of the product repeatedly?
**Definition:** Weekly Active Teams — teams with 4+ async standups completed in a rolling 7-day window.
**Calculation:** distinct teams where count(standup_posted) across the team's members >= 4 in the trailing 7 days.
**Granularity:** per team.
**Filters:** exclude internal, test, and demo teams.
**Time window:** rolling 7 days.
**Owner:** Head of Product.

### Input metrics

- Activation: % of new teams reaching 3+ members posting a standup in week 1.
- Depth: average standups per active team per week.
- Breadth: average active members per active team.

### Link to OKRs

Serves the "Make async standups a daily habit" objective owned by the product-manager.
