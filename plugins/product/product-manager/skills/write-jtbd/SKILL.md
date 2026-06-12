---
name: write-jtbd
description: "Define a Jobs-to-be-Done analysis for a product or feature area. Produces structured job statements, outcome expectations, and hiring/firing criteria. Use when entering a new problem space, validating product-market fit, or reframing features as customer jobs."
argument-hint: "[product area, customer segment, or problem space]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Define a Jobs-to-be-Done analysis for $ARGUMENTS.

This skill carries the Ulwick Outcome-Driven Innovation treatment (outcome scoring) and the
Christensen narrative-job treatment (job statements, emotional/social jobs). The Moesta switch
interview — the retrospective push/pull/anxiety/habit timeline of a real purchase — is a separate
method, covered by the `/product-manager:switch-interview` skill. Use this skill to frame and score
jobs; use `switch-interview` to reconstruct why a specific customer actually switched.

Follow every step below. The output must be a complete JTBD analysis that product, design, and
engineering can use to evaluate feature priorities — not a theoretical exercise.

---

## Step 1: Identify the Job Performer

Before writing job statements, define who is hiring the product:

1. **Who is the primary job performer?** — not a persona, but a person in a specific circumstance. "A hiring manager reviewing 50+ applications for a senior role" not "HR professional"
2. **What is the triggering context?** — what situation causes the job to arise? Jobs exist in moments, not in general. "When I receive a customer complaint" not "managing customer relationships"
3. **What are they hiring today?** — what solution (product, workaround, spreadsheet, manual process) do they currently use to get this job done?
4. **Who else is involved?** — are there secondary job performers (approvers, reviewers, recipients) whose jobs interact with the primary performer's?

Document each job performer with:

| Field | Description |
|-------|-------------|
| **Performer** | Specific role + circumstance |
| **Triggering context** | The moment the job arises |
| **Current solution** | What they hire today |
| **Frequency** | How often does this job arise? |
| **Emotional state** | How do they feel when the job arises? (stressed, curious, bored, anxious) |

---

## Step 2: Write the Core Functional Job Statement

The functional job is the anchor. Write it using the canonical format:

```
When I [situation/context],
I want to [motivation/action],
so I can [expected outcome/goal].
```

### Rules for Job Statements

- **Jobs are solution-agnostic** — "I want to transfer money" not "I want to use the mobile banking app"
- **Jobs are stable over time** — "I want to arrive at my destination on time" has been the same job for centuries. The solutions (horse, car, rideshare) change
- **One job per statement** — if you wrote "and" in the motivation clause, you have two jobs. Split them
- **The outcome is the user's goal, not the product's goal** — "so I can feel confident the payment went through" not "so that the transaction is recorded in the database"

Write exactly one core functional job. This is the primary job the product is hired to do.

---

## Step 3: Map Related Jobs

Every core functional job has related jobs that influence the hiring decision. Map all three types:

### Functional Related Jobs

Jobs that must be done before, during, or after the core job:

| Sequence | Job Statement | Relationship to Core Job |
|----------|---------------|--------------------------|
| Before | When I [context], I want to [action], so I can [outcome] | Precondition for the core job |
| During | When I [context], I want to [action], so I can [outcome] | Happens alongside the core job |
| After | When I [context], I want to [action], so I can [outcome] | Follow-up to the core job |

### Emotional Jobs

How the performer wants to feel (or avoid feeling) while getting the job done:

- **Want to feel:** confident, in control, informed, relieved, proud
- **Want to avoid feeling:** anxious, embarrassed, confused, overwhelmed, incompetent

Write each as: "I want to feel [emotion] when [doing the core job]" or "I want to avoid feeling [emotion] when [doing the core job]."

### Social Jobs

How the performer wants to be perceived by others:

- "I want to be seen as [perception] by [audience]"
- "I want to avoid being seen as [perception] by [audience]"

**Do not skip emotional and social jobs.** They are often the real reason someone switches products. The functional job is table stakes — emotional and social jobs differentiate.

---

## Step 4: Define Desired Outcomes

For each job (core + related), define the outcomes the performer uses to measure success. Outcomes follow the format:

```
[Direction] + [metric] + [object of control] + [context]
```

Examples:
- "Minimise the time it takes to find the right candidate for a role"
- "Minimise the likelihood of missing a critical compliance deadline"
- "Increase the confidence that the report data is accurate before presenting to leadership"

### Outcome Table

| # | Job | Outcome Statement | Importance (1-10) | Current Satisfaction (1-10) | Opportunity |
|---|-----|-------------------|--------------------|-----------------------------|-------------|
| 1 | Core | Minimise the time it takes to... | 9 | 3 | **Underserved** |
| 2 | Core | Minimise the likelihood of... | 8 | 7 | Adequately served |
| 3 | Related | Increase the confidence that... | 7 | 2 | **Underserved** |

**Opportunity Score** = Importance + max(Importance - Satisfaction, 0). Scores above 12 are underserved. Scores below 6 are overserved.

**Rules:**
- Outcomes must be measurable — "minimise the time", "reduce the likelihood", "increase the confidence". Never "make it easier" or "improve the experience"
- Write at least 8 outcomes for the core job
- Rate importance and satisfaction from the performer's perspective, not your assumption

---

## Step 5: Identify Hiring and Firing Criteria

### Hiring Criteria (Why someone switches TO this product)

What causes the performer to seek a new solution? Map the "switching triggers" — these are the four
forces of progress. To reconstruct them from a real customer's actual purchase, use the
`/product-manager:switch-interview` skill; here, capture what you know:

| Trigger | Description | Example |
|---------|-------------|---------|
| **Push (current solution)** | What frustration with the current solution causes them to look? | "My spreadsheet broke when we hit 10,000 rows" |
| **Pull (new solution)** | What attractive quality of the new solution draws them in? | "I saw a demo where the report generated in 2 seconds" |
| **Anxiety (switching cost)** | What fear prevents them from switching? | "Will I lose my historical data?" |
| **Habit (inertia)** | What keeps them with the current solution despite frustration? | "My team already knows how to use the spreadsheet" |

### Firing Criteria (Why someone switches AWAY from this product)

What would cause the performer to stop using the product?

- List the top 5 "firing moments" — the specific incidents that trigger churn
- For each, note whether it is a sudden event (the product broke) or gradual erosion (it slowly stopped meeting needs)

---

## Step 6: Connect to Product Implications

Synthesise the analysis into actionable product decisions:

### Opportunity Landscape

Classify every outcome from Step 4:

| Category | Definition | Product Implication |
|----------|------------|---------------------|
| **Underserved** | High importance, low satisfaction (opportunity > 12) | Build here — this is where value is created |
| **Adequately served** | Importance matches satisfaction | Maintain parity — do not regress |
| **Overserved** | Low importance, high satisfaction (opportunity < 6) | Simplify or remove — you are over-investing |

### Recommendations

For each underserved outcome:
1. **What to build** — feature or capability that addresses the outcome
2. **How to measure success** — metric that proves the outcome is better served
3. **What NOT to build** — explicitly state which overserved areas to deprioritise

---

## Rules

- **Jobs are stable, solutions change** — if your job statement mentions a technology, UI element, or product feature, rewrite it. "I want to use the filter dropdown" is not a job. "I want to narrow results to only relevant items" is a job.
- **Never define a job using your product's features** — "I want to use the dashboard" describes a solution, not a job. Ask: what does the dashboard help them accomplish?
- **Outcomes must be measurable** — "minimise the time it takes to..." not "make it easier to...". If you cannot put a metric on it, it is not an outcome.
- **Emotional and social jobs matter as much as functional jobs** — skipping them produces a functionally correct but emotionally empty product that loses to competitors who get the feelings right.
- **Do not confuse jobs with tasks** — "Upload a CSV file" is a task within a solution. "Get my data into the system accurately" is the job. Always go one level up.
- **Score from evidence, not assumption** — importance and satisfaction ratings should come from interviews or surveys. If you are guessing, label them as hypotheses and validate before acting.
- Reference [Jobs-to-be-Done](https://jobs-to-be-done.com/) (Christensen) and [Outcome-Driven Innovation](https://strategyn.com/) (Ulwick) for methodology foundations.

---

## Output Format

```markdown
# Jobs-to-be-Done Analysis: [Product Area / Feature]

## Job Performer

| Field | Description |
|-------|-------------|
| **Performer** | [Specific role + circumstance] |
| **Triggering context** | [The moment the job arises] |
| **Current solution** | [What they hire today] |
| **Frequency** | [How often] |
| **Emotional state** | [How they feel] |

## Core Functional Job

> When I [situation], I want to [motivation], so I can [outcome].

## Related Jobs

### Functional
| Sequence | Job Statement | Relationship |
|----------|---------------|--------------|
| Before | ... | ... |
| During | ... | ... |
| After | ... | ... |

### Emotional
- I want to feel [emotion] when [context]
- I want to avoid feeling [emotion] when [context]

### Social
- I want to be seen as [perception] by [audience]

## Desired Outcomes

| # | Job | Outcome Statement | Importance | Satisfaction | Opportunity |
|---|-----|-------------------|------------|--------------|-------------|
| 1 | ... | ... | ... | ... | ... |

## Hiring / Firing Criteria

### Hiring (switching triggers)
| Push | Pull | Anxiety | Habit |
|------|------|---------|-------|
| ... | ... | ... | ... |

### Firing (churn triggers)
1. [Firing moment] — [sudden / gradual]

## Product Implications

### Underserved Opportunities
| Outcome | What to Build | Success Metric |
|---------|---------------|----------------|
| ... | ... | ... |

### Overserved (deprioritise)
- [Outcome] — current investment exceeds importance
```

Write the output to a file: `docs/product/jtbd-[area].md`.

---

## Related Skills

- `/product-manager:switch-interview` — reconstruct the four forces from a real customer's actual purchase, rather than assuming them.
- `/product-manager:write-prd` — JTBD informs the PRD problem statement. The core job becomes the "problem" section; underserved outcomes become requirements.
- `/product-manager:write-opportunity-solution-tree` — underserved outcomes become opportunity nodes on the tree.
- `/ux-researcher:persona-definition` — personas and jobs are complementary lenses. Personas describe who; jobs describe why.

Use the JTBD canvas template (`templates/jtbd-canvas.md`) for output structure.
