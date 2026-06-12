---
name: switch-interview
description: "Run a Bob Moesta JTBD switch interview — reconstruct the timeline of a real purchase and code the four forces (push, pull, anxiety, habit). Produces a force-coded timeline of why a specific customer actually switched. Use to understand real buying decisions for B2B or high-consideration purchases."
argument-hint: "[a recent customer who switched to or from the product]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Run a switch interview for $ARGUMENTS.

A switch interview answers one specific question: why did this person buy this product at that moment? It
is post-purchase and retrospective — distinct from generative discovery interviews
(`/product-manager:write-interview-guide`), which are prospective and exploratory. This skill follows
[Bob Moesta's switch interview method](https://therewiredgroup.com/) (Demand-Side Sales 101): a purchase
only happens when four forces align, and you reconstruct the real timeline like a documentary maker rather
than asking evaluative questions.

Follow every step. The output is a force-coded timeline of an actual purchase, not a hypothetical.

## Step 1: Pick a real, recent switch

Choose someone who made an actual purchase or behavioural switch — to your product, away from it, or to a
competitor — recently enough to remember the detail. The switch must be real and specific; "people who
might buy" is not a switch interview subject. This step is complete when you have one named person and the
switch they made.

## Step 2: Reconstruct the timeline (the documentary frame)

Rather than asking evaluative questions, reconstruct what actually happened, with the level of detail
you'd use to make a film of that day. Walk the four moments of the timeline:

| Moment | What you're reconstructing | Sample prompt |
|--------|----------------------------|---------------|
| **First thought** | When they first noticed the problem | "Take me back to when you first realised the old way wasn't working. Where were you?" |
| **Passive looking** | Idle awareness, no active search yet | "After that, were you keeping half an eye out? What did you notice?" |
| **Active looking** | What triggered real research | "What happened that made you actually start looking? What did you do that day?" |
| **The event / decision** | What tipped them into buying | "Walk me through the day you decided. What happened right before?" |

Use specifics — days, places, who else was in the room, what was said. Vague summaries ("I just needed
something better") are a signal to dig: "What specifically happened?" This step is complete when you have a
dated, detailed timeline from first thought to decision.

## Step 3: Code the four forces

Map what you heard onto the [Forces of Progress](https://therewiredgroup.com/). Push and pull drive the
switch; anxiety and habit resist it. If push and pull outweigh anxiety and habit, people switch — if not,
they don't, regardless of product quality:

| Force | Direction | Definition | What you heard |
|-------|-----------|------------|----------------|
| **Push** | Drives switch | Dissatisfaction with the current situation | [quote] |
| **Pull** | Drives switch | Attraction of the new approach | [quote] |
| **Anxiety** | Resists switch | Uncertainty about whether the new thing will work or fit | [quote] |
| **Habit** | Resists switch | Inertia toward what they already do | [quote] |

Code with real quotes from the timeline, not your interpretation. This step is complete when each force has
at least one quote, or is explicitly marked absent.

## Step 4: Extract the demand-side insight

Synthesise what the forces reveal:

- **What job were they hiring the product to do?** Often non-obvious and different from your feature framing
- **What anxiety nearly stopped the switch?** This is where onboarding, guarantees, and trial design earn
  their keep
- **What habit had to be overcome?** And what made it possible
- **What was the real competition?** Often not who you think — sometimes "do nothing" or a spreadsheet

This step is complete when the analysis names the job, the decisive anxiety, the overcome habit, and the
real competition.

## Rules

- **Reconstruct, don't evaluate.** "How did you feel about feature X?" is the wrong question. "Walk me
  through the day you decided" is the right one. Evaluative questions get rationalisations; timeline
  reconstruction gets what happened.
- **Demand specifics.** Days, places, people, exact words. Vague summaries hide the real forces. When you
  hear a summary, dig for the moment.
- **Code with quotes, not interpretation.** A force coded from your inference is your assumption. A force
  coded from their words is evidence.
- **Switch interviews are retrospective.** This is not the tool for exploring a problem space before a
  product exists — use generative interviews for that.
- **The real competition is often "nothing".** Habit and the status quo are the most common things you're
  actually competing against. Code them seriously.

## Output Format

Write to `docs/product/switch-interview-[participant-slug].md`:

```markdown
# Switch interview: [participant] — [the switch]

| Field | Value |
|-------|-------|
| Switched | [from → to] |
| When | [date of purchase] |
| Interview date | [date] |

## Timeline
| Moment | What happened (specific) |
|--------|--------------------------|
| First thought | ... |
| Passive looking | ... |
| Active looking | ... |
| The event / decision | ... |

## Force coding
| Force | Quote |
|-------|-------|
| Push | "..." |
| Pull | "..." |
| Anxiety | "..." |
| Habit | "..." |

## Demand-side insight
- **Job hired for:** ...
- **Decisive anxiety:** ...
- **Habit overcome:** ...
- **Real competition:** ...
```

## Related Skills

- `/product-manager:write-jtbd` — the four forces also appear in the JTBD hiring criteria; this skill
  grounds them in a real purchase rather than assumption.
- `/product-manager:write-interview-guide` — the prospective, exploratory counterpart for problem discovery.
- `/product-manager:synthesise-interviews` — fold force patterns across several switch interviews into the OST.
