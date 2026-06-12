---
name: design-pretotype
description: "Design a pretotype experiment from Alberto Savoia's catalogue (Mechanical Turk, fake door, smoke test, concierge MVP, Wizard of Oz) plus a Market Engagement Hypothesis in XYZ format. Produces a runnable experiment that generates behavioural data before anything is built. Use to test demand or value for a bet cheaply."
argument-hint: "[the bet or assumption to test]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Design a pretotype experiment for $ARGUMENTS.

Roughly 80% of innovations fail even when competently executed — the failure is usually building the wrong
thing, not building it badly. A pretotype tests whether you're building the right thing, before you build
it. This skill follows [Alberto Savoia's pretotyping](https://www.pretotyping.org/) (The Right It): state a
testable Market Engagement Hypothesis, pick the cheapest pretotype that generates real behavioural data,
and collect only skin-in-the-game evidence. A pretotype is distinct from a prototype — a prototype tests
whether you can build it right; a pretotype tests whether you should build it at all.

Follow every step. The output is an experiment a team can run this week.

## Step 1: State the Market Engagement Hypothesis (MEH)

Before designing anything, state your key assumption about how the market will engage, in testable XYZ
form: **X% of Y will do Z.** The format forces specificity on three dimensions — the audience (Y), the
behaviour (Z), and the threshold (X):

- Vague (fails): "People will like the bulk-import feature"
- MEH (passes): "20% of new accounts shown the import prompt will complete an import within their first
  session"

Set the X threshold before you run, not after — a threshold chosen after seeing results proves nothing.
This step is complete when you have one XYZ hypothesis with a pre-committed threshold.

## Step 2: Pick the pretotype

Choose the cheapest pretotype that produces real behavioural data for your hypothesis:

| Pretotype | What it does | Best for |
|-----------|--------------|----------|
| **Mechanical Turk** | Replace the planned technology with humans performing the function | Testing AI/automation concepts before the tech exists |
| **Fake door / 404 test** | A real-looking entry point (button, menu item, ad) that leads nowhere; count clicks | Testing demand for a feature before building it |
| **Smoke test / landing page** | Real landing page with a call-to-action (sign up, pre-order); count conversions | Testing market demand before building anything |
| **Concierge MVP** | Manually deliver the service the product would automate | Validating a service concept and finding process problems |
| **Wizard of Oz** | A human performs the "automated" function invisibly behind the scenes | Testing intelligent/adaptive system concepts |
| **Pinocchio / pop-up** | A non-functional physical mockup, or a temporary real version run for a limited time | Testing form factor or actual (not intended) usage |

State why this pretotype fits the hypothesis. This step is complete when one pretotype is chosen with a
rationale.

## Step 3: Define the skin-in-the-game metric

Only "skin-in-the-game" data counts. Likes, thumbs-up, and verbal enthusiasm score zero — they cost
nothing. Time committed, money spent, or actions taken score meaningfully. Define exactly what behaviour
you'll count and how:

- Bad (no skin in game): "How many people said they'd use it"
- Good (skin in game): "How many clicked the fake-door button and then entered their email"

This step is complete when the metric is a real action, with an instrumentation plan.

## Step 4: Specify the run

State the audience (matching Y), the sample size needed to read the threshold, the duration, and the stop
condition. Keep it small and fast — the point of a pretotype is to kill or confirm a bet cheaply, often in
days. This step is complete when audience, sample, duration, and stop condition are written.

## Step 5: Pre-commit the decision

Before running, write down what each result means: above threshold → proceed; below → kill or pivot. This
prevents post-hoc rationalisation. This step is complete when the proceed/kill rule is recorded against the
threshold from Step 1.

## Rules

- **State the threshold before running.** A threshold set after seeing the data proves nothing. Pre-commit.
- **Only behaviour counts.** Likes and verbal enthusiasm are zero-signal. Measure time, money, or actions.
- **Cheapest pretotype that answers the question.** Don't build a Wizard of Oz when a fake door answers the
  hypothesis. The whole point is low cost.
- **Pretotype ≠ prototype.** A prototype tests build quality; a pretotype tests whether to build. Don't
  conflate them.
- **Flag any spend.** If the pretotype needs ad spend or a paid landing-page tool, name the cost up front.
- **Be honest about a fake door.** A fake-door test shows users something that isn't there yet — handle the
  dead end gracefully (a "coming soon, want to be notified?" rather than a broken page) and don't run it at
  a scale that erodes trust.

## Output Format

Write to `docs/product/pretotype-[bet-slug].md`:

```markdown
# Pretotype: [bet]

## Market Engagement Hypothesis
**[X]% of [Y] will [Z]** within [timeframe].
Threshold committed before running: [X]%.

## Pretotype
| Field | Value |
|-------|-------|
| Type | [Mechanical Turk / fake door / smoke test / concierge / Wizard of Oz / pop-up] |
| Why this fits | ... |
| Skin-in-the-game metric | [real action measured] |
| Audience (Y) | ... |
| Sample size | ... |
| Duration | ... |
| Stop condition | ... |
| Cost / paid tools | [none / named cost] |

## Decision rule (pre-committed)
- Above [X]% → proceed: [next step]
- Below [X]% → kill or pivot: [reasoning]
```

## Related Skills

- `/product-manager:assumption-map` — identifies which assumption is riskiest and worth a pretotype.
- `/product-manager:write-opportunity-solution-tree` — pretotypes are the experiments that hang off solutions.
- `/product-manager:synthesise-interviews` — qualitative discovery that surfaces what to pretotype.
