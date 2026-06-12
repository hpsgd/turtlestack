---
name: strategic-voc-synthesis
description: "Validate discovery hypotheses against Voice-of-Customer signal across tickets, reviews, churn reasons, surveys, and sales feedback. Produces a synthesis that confirms, contradicts, or qualifies a hypothesis with triangulated VoC evidence. Use to pressure-test a discovery finding before committing it to the roadmap."
argument-hint: "[the discovery hypothesis to validate against VoC]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Validate $ARGUMENTS against Voice-of-Customer signal.

This is the product manager's VoC lens. In a distributed-VoC model, several roles each hold their own
distinct view of the customer's voice — support hears tickets, customer-success hears churn and health, the
ux-researcher hears usability sessions, GTM hears win/loss. Those lenses overlap on purpose: different
roles surface different signals from the same customer base, and the conflict between them is informative,
not a problem to reconcile away. The PM's lens is specifically about whether a discovery hypothesis holds
up against the breadth of customer signal before it earns a place on the roadmap.

Follow every step. The output is a triangulated verdict on the hypothesis, with the conflicting lenses
surfaced rather than smoothed over.

## Step 1: State the hypothesis precisely

Write the discovery hypothesis as a falsifiable claim about a customer need or behaviour, usually carried
over from interview synthesis (`/product-manager:synthesise-interviews`): "Mid-market accounts churn
primarily because onboarding takes more than two weeks." Vague hypotheses can't be validated. This step is
complete when the hypothesis is a single falsifiable statement.

## Step 2: Pull each VoC source and tag its lens

Gather signal from every available source, and record which role's lens it comes from:

| Source | Lens / owner | What it tells you | Bias to watch |
|--------|--------------|-------------------|---------------|
| Support tickets | Support | Frequency and acuteness of friction | Skews to users who complain |
| Churn / health signal | Customer success | Why accounts leave or stall | Post-hoc rationalisation |
| Reviews (G2, Capterra, app stores) | (no single owner) | Comparative sentiment, competitor gaps | Self-selecting; reviewers go to complain or rave |
| Surveys (NPS/CSAT/CES) | Product / CS | Trend and segment cuts | Stated, not behavioural |
| Win/loss | GTM | Buyer-side decision drivers | Sales-reported reasons differ from buyer-reported |
| Discovery interviews | PM | Depth on the specific need | Small N |

For each source, record what it says about the hypothesis. This step is complete when each available source
has been pulled and tagged with its lens.

## Step 3: Triangulate and weight by evidence tier

Don't treat all sources equally. Weight regulatory/behavioural and independent signal above self-reported
and subject-supplied. A claim supported by one source is single-sourced — label it. A claim supported
across two or more independent lenses is triangulated. Behavioural signal (what accounts actually did)
outweighs stated signal (what they said in a survey). This step is complete when each piece of support is
tiered and single-source claims are labelled.

## Step 4: Surface the conflicting lenses

Where two lenses disagree — sales says price, the interviews say onboarding; tickets say one thing, churn
data another — surface the conflict explicitly. Do not average it away or pick the convenient one. The
disagreement usually means the hypothesis is partial, segment-specific, or that one lens is closer to the
real driver. Name which lens you trust more for this hypothesis and why. This step is complete when every
cross-lens conflict is stated, not hidden.

## Step 5: Verdict

Render one of three verdicts with the evidence behind it:

- **Confirmed** — triangulated across independent lenses, behavioural signal present. Ready for the roadmap
- **Qualified** — true for a segment or under conditions; state the boundary
- **Contradicted** — VoC doesn't support it; send back to discovery or drop

This step is complete when the verdict is stated with a confidence rating (0-4) and the evidence behind it.

## Rules

- **Triangulate or label single-source.** A hypothesis riding on one VoC source is not validated. Mark it
  `[single source]` and seek a second lens.
- **Behaviour over stated intent.** What accounts did outweighs what they said in a survey. Weight
  accordingly.
- **Surface conflict, don't reconcile it.** When lenses disagree, the disagreement is the finding. Don't
  pick the lens that confirms your plan.
- **Watch self-selecting samples.** Review sites and complaint channels skew. Note the skew rather than
  treating raw sentiment as representative.
- **Consult the other lens-holders.** This is the PM's view, not the only view. Where the hypothesis touches
  pricing, churn, or positioning, consult GTM, customer-success, or the ux-researcher for their lens.
- **Don't manufacture a verdict.** If the signal is genuinely thin, the verdict is "needs more discovery",
  not a forced confirm.

## Output Format

Write to `docs/product/voc-synthesis-[hypothesis-slug].md`:

```markdown
# VoC synthesis: [hypothesis]

**Hypothesis (falsifiable):** ...

## Signal by source
| Source | Lens | What it says | Tier | Single-source? |
|--------|------|--------------|------|----------------|
| ... | ... | ... | T1-T5 | yes/no |

## Cross-lens conflicts
- [Lens A] says X; [Lens B] says Y → [which is closer for this hypothesis, and why]

## Verdict
**[Confirmed / Qualified / Contradicted]** — confidence [0-4]
[evidence summary; if Qualified, state the segment boundary]

## Lenses to consult further
- [role] for [aspect]
```

## Related Skills

- `/product-manager:synthesise-interviews` — produces the hypotheses this skill validates.
- `/product-manager:define-icp` — VoC signal sharpens the ICP's behavioural criteria.
- `/product-manager:write-roadmap` — only confirmed or qualified hypotheses earn a roadmap place.
