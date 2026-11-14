---
name: scientific-method
description: "Apply the scientific method to any problem — define goal, hypothesise, experiment, measure, iterate. The meta-skill governing all structured investigation. Use when debugging, validating assumptions, or turning uncertainty into knowledge."
argument-hint: "[problem to investigate or goal to achieve]"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

Apply the scientific method to $ARGUMENTS. This is the universal cycle for turning uncertainty into knowledge.

```
GOAL → OBSERVE → HYPOTHESISE → EXPERIMENT → MEASURE → ANALYSE → ITERATE
```

## Step 1: Define the goal (mandatory)

What does success look like? Without clear success criteria, you cannot judge results.

```markdown
### Goal definition

**Goal:** [specific, measurable outcome]
**Current state:** [where things are now — with numbers if possible]
**Target state:** [where they need to be — with numbers]
**How to measure:** [the specific metric or observation that proves success]
```

**Rules for goals:**
- Bad: "Make it faster" — unmeasurable
- Good: "Reduce p95 latency from 800ms to under 200ms on the /api/search endpoint"
- Every goal must have a number or a binary pass/fail condition

**Output:** Goal definition with current state, target state, and measurement method.

## Step 2: Observe (mandatory)

Gather data about the current state BEFORE forming hypotheses. Observation without hypothesis prevents confirmation bias.

```markdown
### Observations

| # | Observation | Source | Surprising? |
|---|---|---|---|
| 1 | [what you actually see — not what you expect] | [where you found it] | Yes/No |
| 2 | [observation] | [source] | [surprise?] |

**What has been tried before:** [previous attempts and their outcomes]
**What measurements exist:** [available data, logs, metrics]
**What's missing:** [data you wish you had but don't]
```

**Rules for observation:**
- Record what you SEE, not what you EXPECT. The gap between these is where discoveries live
- Surprising observations are the most valuable — flag them explicitly
- "I don't know" is a valid and important observation

**Output:** Observation table with sources and surprise flags.

## Step 3: Hypothesise (mandatory)

Generate MULTIPLE hypotheses, not just one. A single hypothesis is confirmation bias waiting to happen.

```markdown
### Hypotheses

| # | Hypothesis | If true, expect to see | If false, expect to see | Likelihood |
|---|---|---|---|---|
| H1 | [specific claim about what's happening and why] | [predicted observation] | [predicted observation] | High/Medium/Low |
| H2 | [alternative explanation] | [prediction] | [prediction] | [likelihood] |
| H3 | [another possibility] | [prediction] | [prediction] | [likelihood] |
```

**Rules for hypotheses:**
- Minimum 3 hypotheses. If you can only think of one, you don't understand the problem yet
- Every hypothesis must be falsifiable — if no observation could disprove it, it's not a hypothesis
- The "if false" column is the most important — it tells you what would change your mind
- Rank by likelihood but test the most likely first, not the most interesting

**Output:** Hypothesis table with predictions and falsification criteria.

## Step 4: Design experiment (mandatory)

For the highest-likelihood hypothesis, design the smallest test that would confirm or refute it:

```markdown
### Experiment design

**Testing hypothesis:** H[N]
**Variable (what changes):** [the one thing you're changing]
**Control (what stays the same):** [everything else]
**Measurement:** [how you'll know the result]
**Expected result if hypothesis is correct:** [specific outcome]
**Expected result if hypothesis is wrong:** [specific outcome]
**Time budget:** [maximum time before concluding]
```

**Rules for experiments:**
- Change ONE variable at a time. Changing multiple things makes results uninterpretable
- Define the expected result BEFORE running the experiment. Post-hoc rationalisation is not science
- Set a time budget. An experiment that runs indefinitely is not an experiment

**Output:** Experiment design with single variable, control, and predictions.

## Step 5: Measure (mandatory)

Run the experiment and record results:

```markdown
### Results

**What happened:** [factual description of outcome]
**Expected outcome matched:** Yes / No / Partially
**Quantitative result:** [numbers if applicable]
**Unexpected observations:** [anything you didn't predict]
```

**Rules for measurement:**
- Record what ACTUALLY happened, not what you hoped for
- Unexpected observations are often more valuable than the expected result — do not discard them
- If the result is ambiguous, the experiment needs to be more precise, not re-interpreted

**Output:** Results with comparison to predictions.

## Step 6: Analyse (mandatory)

Compare results to the goal:

```markdown
### Analysis

**Hypothesis H[N] status:** Confirmed / Refuted / Inconclusive
**Distance from goal:** [how far current state is from target state]
**What we learned:** [new knowledge gained — the actual value of this cycle]
**What we still don't know:** [remaining uncertainty]
```

**Output:** Hypothesis verdict and remaining uncertainty.

## Step 7: Iterate (mandatory)

Based on analysis, decide next action:

- **Goal met** → Document what worked, why, and what would break it. Done.
- **Goal not met, hypothesis confirmed** → The fix didn't work despite correct diagnosis. Revise the approach, return to Step 3 with new hypotheses.
- **Goal not met, hypothesis refuted** → Move to next hypothesis. Return to Step 4.
- **Stuck** → Challenge assumptions with `/first-principles`. The problem framing may be wrong.

**Output:** Decision on next action with reasoning.

## Quick Diagnosis Mode

For debugging (the 15-minute rule):

1. What exactly is the symptom? (Step 2 — observe)
2. What are 3 possible causes? (Step 3 — hypothesise)
3. Which is most likely? Test that ONE thing (Steps 4–5)
4. Did it fix it? (Step 6 — analyse)
5. If not, next hypothesis. Don't change multiple things at once (Step 7 — iterate)

## Rules

- **Multiple hypotheses are mandatory.** A single hypothesis is not the scientific method — it's guessing with extra steps. Minimum 3.
- **Change one variable at a time.** Changing two things simultaneously makes the result uninterpretable. If you're tempted to change multiple things, run multiple experiments.
- **Record before interpreting.** Write down what you observe before forming an explanation. Observation and interpretation are separate steps.
- **Falsification over confirmation.** Seek evidence that DISPROVES your hypothesis, not evidence that confirms it. Confirmation bias is the #1 enemy of investigation.
- **Time-box everything.** An experiment without a time budget becomes an infinite loop. If you haven't learned something in the allotted time, the experiment design is wrong.
- **"I don't know" is progress.** Eliminating a hypothesis is as valuable as confirming one. Three refuted hypotheses is not failure — it's three things you've ruled out.

## Output Format

```markdown
## Investigation: [problem]

### Goal
[Goal definition from Step 1]

### Observations
[Observation table from Step 2]

### Hypotheses
[Hypothesis table from Step 3]

### Experiment
[Design from Step 4]

### Results
[Measurements from Step 5]

### Analysis
[Verdict from Step 6]

### Next Action
[Decision from Step 7]
```

## Related Skills

- `/first-principles` — when the scientific method reveals that the problem framing itself is wrong. Decompose and rebuild.
- `/algorithm` — for systematic execution once you know WHAT to do. Scientific method figures out what's true; algorithm executes the plan.
- `/thinking:retrospective` — turn a lesson from the experiment into a learned rule when it should hold everywhere.
