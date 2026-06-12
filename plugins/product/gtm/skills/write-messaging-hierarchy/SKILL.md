---
name: write-messaging-hierarchy
description: "Build a messaging hierarchy — the primary message, supporting messages, proof points, and per-persona variants — that flows from an existing positioning. Use when you have positioning and need the message architecture that turns it into consistent copy across web, sales, and campaigns. Complements positioning (market position) by defining the message system that derives from it."
argument-hint: "[product or campaign to build the messaging hierarchy for]"
user-invocable: true
allowed-tools: Read, Write, Bash, Glob, Grep
---

# Write a messaging hierarchy

Build the messaging hierarchy for $ARGUMENTS: a structured architecture of the primary message, the supporting messages beneath it, the proof points under each, and the per-persona variants. The hierarchy is the bridge between positioning and copy — it ensures every landing page, email, and sales deck says the same thing in the same order, varied only for audience.

**Boundary with positioning:** this skill does not redo positioning. Positioning (from `/gtm:positioning`) decides the market position — competitive alternatives, unique attributes, value, target customer, category. The messaging hierarchy is the message architecture that *flows from* that position. Positioning answers "where do we sit and why us"; the hierarchy answers "in what order do we say it, and how does it change per persona." Run `/gtm:positioning` first; this skill consumes its output. If no positioning exists, stop and produce it before continuing.

## Step 1 — Load the positioning

Pull the current positioning. Extract and restate, so the hierarchy is traceable to it:

- The positioning statement and tagline.
- The target customer(s) and any distinct personas within them.
- The unique attributes and the value each delivers.
- The market category.

If positioning is missing or stale, stop. A messaging hierarchy built on no positioning is just copy with a diagram around it. State the gap and route to `/gtm:positioning`.

## Step 2 — Write the primary message

The primary message is the single most important thing the market must believe. One sentence. It sits at the top of the hierarchy; everything below supports it.

Rules:

- It states the core value in the buyer's terms, derived from the positioning's value proposition — not a feature, not the category alone.
- It must pass the competitor test: if a competitor could truthfully say the same sentence, it is too generic. Rewrite until it is ours alone.
- It is not the tagline. The tagline is the compressed slogan; the primary message is the full claim a buyer would nod at.

Write three candidates, then commit to one with a one-line reason. State why the other two lose.

## Step 3 — Define supporting messages

Supporting messages are the 3-4 pillars that make the primary message believable. Each maps to a unique attribute or value theme from the positioning. Resist the rule-of-three reflex — use the number the positioning actually supports (often three, sometimes two or four).

| Supporting message | Maps to (positioning attribute/value) | Why a buyer cares |
|---|---|---|
| [pillar message] | [attribute] | [the outcome] |

Rules:

- Each pillar must trace to a positioning element. A pillar with no positioning root is invented messaging — cut it.
- Pillars are claims, not features. "Set up in minutes" not "guided onboarding wizard."
- If two pillars overlap, merge them. Overlapping pillars dilute the hierarchy.

## Step 4 — Attach proof points

Every claim needs evidence, or it is marketing noise. Under each supporting message, attach proof points that substantiate it.

| Supporting message | Proof point | Type | Source | Segment it applies to |
|---|---|---|---|---|
| [pillar] | [evidence] | metric / customer quote / case study / benchmark / certification | [where it's from] | SMB / mid-market / enterprise / all |

Rules:

- At least one proof point per supporting message. A pillar with no proof is a hope.
- Quantified proof beats adjectives. "Cuts onboarding from 2 hours to 5 minutes" beats "faster onboarding."
- Tag the segment each proof fits. An enterprise logo carries no weight in an SMB deal and vice versa.
- Mark any proof point you cannot source "unverified — needs confirmation." Do not ship unsourced claims in copy.

## Step 5 — Build persona variants

The hierarchy stays constant; the emphasis and language shift per persona. For each persona from the positioning, specify how the message bends.

```
### Persona: [role / segment]

- What they care about most: [their priority]
- Lead supporting message: [which pillar leads for this persona]
- Language adjustments: [their vocabulary vs ours]
- Proof points that land: [the subset that matters to this persona]
- Objection this pre-empts: [from market-voc, if available]
```

Rules:

- The primary message does not change per persona — only the order, emphasis, and proof do. If the primary message has to change, the personas belong to different positionings (and possibly different products).
- Lead with the pillar each persona cares about most. An economic buyer leads on a different pillar than an end user.
- Use the persona's own words. Pull buyer language from `/gtm:market-voc` where it exists.

## Step 6 — Assemble and pressure-test

Compile the hierarchy and test it: can a copywriter produce a consistent landing page, email, and sales line from this without inventing new claims? If they would have to invent, the hierarchy is incomplete.

## Rules

- Flows from positioning, never replaces it. Every level of the hierarchy traces to a positioning element. If it doesn't trace, it doesn't belong.
- One primary message. The moment there are two "most important things," the hierarchy has failed and the positioning is probably unfocused.
- Every claim carries proof. A supporting message without a proof point is cut or marked unverified.
- Persona variants change emphasis, not the core claim. A different primary message per persona means different products.
- Don't let the bold-label-colon list pattern leak into the copy this seeds. The hierarchy is the internal architecture; the copy derived from it follows the writing-style rules.
- **All output is DRAFT until human-reviewed.** Label every output "DRAFT — requires human review" at the top and bottom.

## Output Format

```markdown
# Messaging hierarchy — [product] (DRAFT — requires human review)

**Derived from positioning:** [statement / tagline restated]
**Date:** [date]

## Primary message
> [the one sentence]
- Why this over the alternatives: [reason; rejected candidates]

## Supporting messages
| Supporting message | Maps to | Why a buyer cares |
|---|---|---|

## Proof points
| Supporting message | Proof | Type | Source | Segment |
|---|---|---|---|---|

## Persona variants
### [Persona A]
- Cares about: [...]
- Leads with: [pillar]
- Language: [...]
- Proof that lands: [...]
- Pre-empts objection: [...]

[repeat per persona]

## Consistency check
[Can a copywriter produce web + email + sales line from this without inventing claims? Yes/No + gaps.]

DRAFT — requires human review
```

## Related Skills

- `/gtm:positioning` — the required input. Positioning sets the market position; this hierarchy is the message architecture that flows from it.
- `/gtm:write-narrative` — the strategic narrative is the long-form story; the hierarchy is the modular claim system. They share the same positioning root.
- `/gtm:market-voc` — buyer language and objections sharpen the persona variants.
- `/gtm:write-battle-card` — supporting messages and proof points feed competitive objection handling.
