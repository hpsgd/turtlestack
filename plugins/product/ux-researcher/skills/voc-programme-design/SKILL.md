---
name: voc-programme-design
description: "Design an ongoing voice-of-customer (VoC) programme combining NPS, CSAT, CES and qualitative synthesis. Produces a programme blueprint covering metric selection, survey design (wording, sampling, cadence), closing-the-loop routing, and a method for tying quantitative signal to qualitative themes. Use to stand up or audit a continuous customer-feedback programme — not for a one-off survey or a persona artifact."
argument-hint: "[product or customer segment to design the VoC programme for]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Voice-of-Customer Programme Design

Design a continuous voice-of-customer programme for $ARGUMENTS. A VoC programme is the structured-research lens on customer signal: a repeating system that captures what customers think and do, turns it into evidence, and routes that evidence to an owner who acts on it. This is one lens among several — support reads tickets, customer-success reads account health, GTM reads win/loss. Each holds its own VoC view and the overlap is intentional. This skill owns the structured-survey-plus-qualitative-synthesis lens and is built to be cross-consulted, not to centralise feedback ownership.

This skill produces an ongoing signal programme, not a snapshot. It is distinct from `/ux-researcher:persona-definition` (which produces a persona artifact from evidence) and from `/ux-researcher:usability-test-plan` (which plans a single evaluative study). Use those for artifacts and studies; use this to design the machine that feeds them.

## Step 1: Define programme objectives and decision links (mandatory)

A VoC programme that measures everything and changes nothing is theatre. Before choosing a single metric, name the decisions the programme will feed.

```markdown
### Programme objectives

| Objective | Decision it informs | Owner who acts | Cadence of the decision |
|---|---|---|---|
| [e.g., Reduce onboarding drop-off] | [Which onboarding step to redesign next] | [Product owner] | [Per sprint] |
| [e.g., Detect at-risk accounts early] | [Which accounts get a success intervention] | [Customer success] | [Weekly] |
| [e.g., Track release perception] | [Whether to roll back or iterate a release] | [Product owner] | [Per release] |
```

**Rules for objectives:**

- Every objective names a decision and an owner. No owner, no objective — drop it.
- 3-5 objectives maximum for a first programme. More signal sources than the team can act on creates backlog, not insight.
- If an objective has no clear action owner, the programme will collect data nobody uses. Cut it or assign one.

**Output:** Objectives table with decision links and owners.

## Step 2: Select the right metric per question (mandatory)

Each relationship and transactional question maps to a different metric. Picking the wrong metric produces a number that moves for reasons you can't act on. Map each objective to a metric using the table below.

| Metric | Question it answers | When to use | Scale |
|---|---|---|---|
| [NPS](https://www.netpromoter.com/know/) (Net Promoter Score) | "How likely is the overall relationship to generate advocacy?" | Relationship-level, periodic, benchmarkable across companies | 0-10 "likely to recommend"; promoters (9-10) minus detractors (0-6) |
| [CSAT](https://www.theacsi.org/) (Customer Satisfaction) | "Were you satisfied with this specific thing?" | Transactional — after a support interaction, a feature use, a delivery | 1-5 (or 1-7) satisfaction; % top-2-box |
| [CES](https://hbr.org/2010/07/stop-trying-to-delight-your-customers) (Customer Effort Score) | "How hard was it to get this done?" | After an effortful task — onboarding, resolving an issue, completing a purchase | 1-7 agreement with "the company made it easy"; effort predicts churn better than delight |

```markdown
### Metric selection

| Objective (from Step 1) | Metric | Trigger point | Rationale |
|---|---|---|---|
| [objective] | NPS / CSAT / CES | [Relationship periodic / after event X] | [Why this metric answers this question] |
```

**Rules for metric selection:**

- Never use one metric for everything. NPS for relationship trajectory, CSAT for satisfaction with a specific touchpoint, CES for friction on a task. Using NPS to measure a support interaction tells you about the relationship, not the interaction.
- A relationship metric (NPS) is periodic and benchmarkable. A transactional metric (CSAT, CES) fires after a specific event and is most useful in trend, not absolute value.
- Effort (CES) is the strongest predictor of disloyalty for service interactions. Prefer it over CSAT when the objective is about reducing friction.

**Output:** Metric selection table mapping every objective to a metric, trigger, and rationale.

## Step 3: Design the surveys (mandatory)

The number is only as good as the question that produced it. Design wording, scale, sampling, and cadence for each metric.

```markdown
### Survey design — [metric, e.g., post-onboarding CES]

**Primary question (verbatim):** [Exact wording — e.g., "[Product] made it easy for me to set up my account." Strongly disagree (1) → Strongly agree (7)]
**Follow-up (open text, mandatory):** ["What was the main reason for your score?"]
**Trigger:** [Event or schedule that fires the survey]
**Sampling:** [Who is asked — census or sample; exclusions; rate limit per respondent]
**Cadence / fatigue control:** [Max one survey per respondent per N days; suppression window after a recent survey]
**Channel:** [In-product, email, SMS — match to where the moment happens]
**Target response rate:** [With a floor below which the sample is not trustworthy]
```

**Survey wording rules:**

- One construct per question. "How satisfied and how likely to recommend" is two questions wearing one collar. Split them.
- Always pair the rating with an open-text "why." The score tells you the temperature; the verbatim tells you the cause. A score with no verbatim is a dead end (Step 4 needs the text).
- No leading wording. "How much did you love the new dashboard?" presumes the answer. Ask "How satisfied were you with the new dashboard?" and let the scale carry it.
- Keep the scale consistent within a metric across time. Switching a CSAT from 1-5 to 1-10 mid-programme breaks every trend line you have.

**Sampling and cadence rules:**

- Set a fatigue cap: no respondent gets more than one survey per defined window (commonly 30-90 days). Over-surveying collapses response rate and skews toward the angry and the delighted.
- Sample by segment, not by convenience. If 80% of responses come from one plan tier, the programme speaks for that tier only. State the segment mix you need and quota for it.
- Define a response-rate floor per segment below which results are flagged "insufficient sample," not reported as fact. Tie this to the confidence rubric the team already uses.
- Trigger transactional surveys close to the event (within hours), while memory is intact. A CSAT sent two weeks after a support call measures recall, not satisfaction.

**Output:** One survey design block per metric, with verbatim wording, sampling, and cadence.

## Step 4: Tie quantitative signal to qualitative themes (mandatory)

A score that moves without an explanation cannot be acted on. The programme's core method is connecting the metric movement to the verbatim themes behind it.

```markdown
### Quant-to-qual synthesis method

**Verbatim coding:** [How open-text responses are coded into themes — e.g., affinity grouping each cycle; a stable code frame that grows over time]
**Code frame:** [Starting themes — e.g., "setup confusion", "missing feature", "pricing", "performance" — with rules for adding a code]
**Driver analysis:** [How themes are correlated with score — e.g., detractor verbatims grouped by theme; theme frequency among low scorers vs high scorers]
**Segment cut:** [Themes broken out by segment so a pattern in one tier isn't washed out by the average]
**Saturation check:** [When a theme is considered established — e.g., appears in N% of detractor verbatims across two cycles]
```

**Synthesis rules:**

- Never report a score without its top themes. "NPS dropped 8 points" is an alarm; "NPS dropped 8 points, driven by setup-confusion verbatims up 3x among new mid-market accounts" is a brief someone can act on.
- Code the verbatims of low scorers and high scorers separately. The themes that distinguish a detractor from a promoter are the drivers worth acting on. Themes common to both are noise.
- Keep a stable code frame across cycles so themes are comparable over time. Re-inventing categories each cycle makes trend impossible.
- Cut every theme by segment before concluding. An average hides the case where one segment is furious and another is delighted — exactly the signal worth finding.

**Output:** Synthesis method with code frame, driver-analysis approach, and saturation rule.

## Step 5: Design closing the loop (mandatory)

The programme is only worth running if feedback changes something the customer can see. Design both loops.

```markdown
### Inner loop (individual response → individual action)

| Trigger | Routing rule | Owner | SLA |
|---|---|---|---|
| [Detractor score + verbatim] | [Route to account owner] | [Customer success] | [Contact within 48h] |
| [CSAT ≤ 2 on support] | [Reopen ticket, escalate] | [Support lead] | [Same day] |

### Outer loop (aggregate themes → product/process change)

| Trigger | Routing rule | Owner | Forum |
|---|---|---|---|
| [Theme crosses saturation threshold] | [Becomes a discovery input / backlog candidate] | [Product owner] | [Backlog grooming] |
| [Systemic effort driver] | [Process or design change] | [UX researcher → product owner] | [Quarterly review] |
```

**Closing-the-loop rules:**

- Both loops are mandatory. The inner loop recovers the individual customer (a detractor who is contacted often becomes neutral or better). The outer loop fixes the cause so the next cohort never hits it. A programme with only the inner loop treats symptoms forever.
- Every routing rule names an owner and a service level. "Someone will look at detractors" is not a rule; "account owner contacts detractors within 48 hours" is.
- The outer loop feeds discovery and the backlog, not a slide. A saturated theme becomes a candidate problem for `/product-owner:write-jtbd` or a discovery input, with the evidence attached.
- Tell customers what changed. "You said X, we did Y" closes the loop visibly and is the single biggest driver of future response rate.

**Output:** Inner-loop and outer-loop routing tables with owners and SLAs.

## Step 6: Define governance and anti-gaming (mandatory)

A metric tied to incentives gets gamed. Define ownership, cadence, and the guards that keep the number honest.

```markdown
### Governance

| Item | Detail |
|---|---|
| **Programme owner** | [Who owns the programme end to end] |
| **Reporting cadence** | [How often results are reviewed and by whom] |
| **Benchmark** | [Internal trend baseline; external benchmark if used] |
| **Anti-gaming guards** | [No solicitation of high scores; no surveying only happy cohorts; raw verbatims visible, not just the score] |
| **Review trigger** | [What forces a re-design — e.g., response rate below floor for two cycles] |
```

**Governance rules:**

- Never tie a frontline incentive directly to the score without guards. "Please give us a 10" coaching destroys the signal's validity (Goodhart's Law — when a measure becomes a target, it stops being a good measure).
- Report trend, not absolute value, as the headline. A single NPS number out of context invites comparison games; the trajectory and its drivers are what inform decisions.
- Keep raw verbatims visible to the people who act. Summary scores let bad news get smoothed away; the unedited customer sentence does not.

**Output:** Governance table with owner, cadence, benchmark, and anti-gaming guards.

## Rules

- **No metric without a decision and an owner.** A VoC programme exists to change decisions. Any signal source that doesn't feed a named decision and a named owner is collected for its own sake — cut it.
- **Right metric for the right question.** NPS for relationship trajectory, CSAT for satisfaction with a specific touchpoint, CES for task friction. Don't use one metric as a universal thermometer.
- **Always pair score with verbatim.** A number tells you something moved; the open-text tells you why. Never ship a survey that captures the rating without the reason.
- **Both loops or neither.** Inner loop recovers the individual; outer loop fixes the cause. A programme with only one is half a programme.
- **Trend over absolute.** Survey methods, samples, and seasons shift the absolute number. The trajectory and its drivers are the signal. Don't over-read a single cycle's headline figure.
- **Don't centralise the lens.** This is the structured-research VoC view. Support, customer-success, and GTM hold their own. When designing routing, cross-consult those owners rather than absorbing their feedback streams into this one — surface conflicting reads, don't reconcile them away.
- **Don't build a persona here.** If the work is "describe a customer segment," that's `/ux-researcher:persona-definition`. This skill builds the ongoing signal machine, not the artifact.

## Output Format

```markdown
# VoC Programme: [product / segment]

**Date:** [date]  |  **Researcher:** [name]  |  **Status:** [Draft / Approved / Live]

## 1. Objectives
[Objectives table from Step 1 — objective, decision, owner, cadence]

## 2. Metric Selection
[Metric table from Step 2 — objective → metric, trigger, rationale]

## 3. Survey Design
[One survey block per metric from Step 3 — verbatim wording, sampling, cadence, channel]

## 4. Quant-to-Qual Synthesis
[Synthesis method from Step 4 — code frame, driver analysis, saturation rule]

## 5. Closing the Loop
[Inner-loop and outer-loop routing tables from Step 5 — trigger, routing, owner, SLA]

## 6. Governance
[Governance table from Step 6 — owner, cadence, benchmark, anti-gaming guards]

## Cross-Consultation
[Which other lenses to consult — support feedback-synthesis, customer-success health, GTM win/loss — and where their reads may conflict with this programme's]
```

## Related Skills

- `/ux-researcher:persona-definition` — turns accumulated VoC evidence into a customer archetype. The programme feeds the persona; it is not the persona.
- `/ux-researcher:usability-test-plan` — a single evaluative study. When a VoC theme saturates ("setup is confusing"), a usability test diagnoses the specific cause.
- `/ux-researcher:journey-map` — VoC metrics attach to journey stages. Map the journey, then place each transactional survey at the moment it measures.
