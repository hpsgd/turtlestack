---
name: analyst-briefing-prep
description: "Prepare for an industry-analyst briefing (Gartner, Forrester, IDC) — briefing deck structure, proof points mapped to evaluation criteria, demo flow, and Q&A prep for hard analyst questions. Use before a vendor briefing, Magic Quadrant / Forrester Wave inclusion cycle, or analyst inquiry. Produces the prep pack, not the live delivery."
argument-hint: "[the briefing — e.g. 'Gartner MQ briefing for the platform']"
user-invocable: true
allowed-tools: Read, Write, Bash, Glob, Grep, WebSearch
---

# Analyst briefing prep

Prepare the briefing pack for $ARGUMENTS — a vendor briefing with an industry analyst firm ([Gartner](https://www.gartner.com), [Forrester](https://www.forrester.com), [IDC](https://www.idc.com), or similar). Analysts shape how enterprise buyers build shortlists; a briefing is your chance to make them understand your position before they evaluate it. This skill produces the deck structure, the proof points mapped to the firm's evaluation criteria, the demo flow, and the Q&A prep. It does not deliver the briefing — a human does that.

An analyst briefing is not a sales pitch. Analysts are sceptical, well-informed, and have seen every competitor. They reward specificity and clarity of position, and they punish hand-waving. The prep draws on `/gtm:positioning`, `/gtm:write-narrative` (the framing story), and `/gtm:competitive-analysis` (how analysts will compare you).

## Step 1 — Profile the firm and the evaluation

Different firms evaluate differently. Establish the ground:

- **Firm and analyst:** who you're briefing, their coverage area, their recent published notes on the category (search for them).
- **Evaluation vehicle:** Gartner Magic Quadrant (ability to execute × completeness of vision), Forrester Wave (current offering × strategy × market presence), IDC MarketScape, or an inquiry with no scoring. The axes determine what to emphasise.
- **Cycle timing:** is this pre-inclusion, mid-evaluation, or relationship-building? Pre-evaluation briefings set the frame; mid-evaluation briefings answer specific scoring gaps.
- **Their current view:** what does the analyst already believe about you and the category? If they've published, read it and note where you agree and where you must correct.

Output a one-paragraph situation brief.

## Step 2 — Map proof points to evaluation criteria

Analysts score against published criteria. Map your evidence to their axes so every claim lands where it counts. For a quadrant/wave, build the mapping:

| Evaluation criterion | Axis (execution / vision / offering / strategy) | Your evidence | Strength | Gap to address |
|---|---|---|---|---|

Rules:

- Lead with the criteria the firm weights most heavily. For an MQ, "completeness of vision" and "ability to execute" each decompose into sub-criteria — map to the sub-criteria, not the headline.
- Every claim is a proof point, not an assertion. Analysts discount unsubstantiated claims instantly. Use customers, metrics, named capabilities, roadmap with dates.
- Name your gaps honestly in the internal prep. The analyst will find them; better you have a prepared answer than get caught. Gaps go in Q&A prep (Step 5), not in the deck.

## Step 3 — Structure the briefing deck

Analysts sit through dozens of briefings. A clear structure respects their time and makes your position memorable. Recommended flow:

1. **Company snapshot** — who you are, traction signals (customers, growth, funding), in 1-2 slides. No fluff.
2. **The market change and your point of view** — the strategic narrative compressed (from `/gtm:write-narrative`). Analysts reward a clear, defensible thesis on where the category is going.
3. **Positioning and differentiation** — where you sit, who you serve, what's unique (from `/gtm:positioning`). Be precise about the segment you win.
4. **Capabilities mapped to the evaluation** — your offering against the firm's criteria (from Step 2).
5. **Proof** — customers, outcomes, metrics. Reference customers the analyst can verify.
6. **Roadmap** — vision with dated milestones. Analysts score vision; a credible, specific roadmap is evidence.
7. **Demo** — see Step 4.

Rules:

- Keep it to the analyst's allotted time with room for questions — analysts value the Q&A more than the slides.
- One thesis. If the deck argues three different positions, the analyst remembers none.
- No marketing superlatives. "Market-leading" and "best-in-class" are downgraded on sight. Specifics only.

## Step 4 — Design the demo flow

A demo for an analyst is not a feature tour. It proves the differentiated capabilities and the point of view. Storyboard it:

| Demo beat | What it shows | Which criterion / claim it proves | Time |
|---|---|---|---|

Rules:

- Demo only the capabilities that prove your differentiation and the criteria that matter. A generic feature walkthrough wastes the slot.
- Tie each beat to a claim from Step 2. The demo is evidence, not entertainment.
- Rehearse the failure path. Live demos break; have a recorded fallback and know what each beat proves so you can narrate without the live system.

## Step 5 — Build the Q&A prep

This is the most valuable part. Anticipate the hard questions and prepare honest, specific answers. Analysts probe weaknesses, roadmap credibility, and competitive comparison.

```
### Q: [the hard question]
**Why they ask:** [what they're really testing — a gap, a doubt, a comparison]
**Answer:** [specific, honest response]
**Proof:** [evidence to back it]
**Do not:** [the defensive or evasive answer to avoid]
```

Cover at minimum:

- Your weakest evaluation criterion (from Step 2 gaps).
- Direct competitor comparison ("how are you different from [the leader]?") — pull from `/gtm:competitive-analysis`.
- Roadmap credibility ("you said this last year — where is it?").
- Pricing and market traction questions.
- Any negative the analyst has published or implied.

Rules:

- Honesty beats spin with analysts. They have the full market view; a deflection is transparent and costs credibility. "That's a known gap; here's our plan and timeline" outperforms denial.
- Never disparage competitors by name. Analysts cover them too; trashing a rival reads as insecurity. Differentiate on your strength, not their weakness.
- Every answer has a proof point or it's an opinion.

## Step 6 — Assemble the prep pack

Compile the deck outline, demo storyboard, and Q&A into one prep pack the human briefer can rehearse from.

## Rules

- A briefing is not a pitch. Analysts reward a clear, defensible point of view and specific evidence; they punish marketing language and hand-waving.
- Map everything to the firm's published criteria. Generic excellence doesn't score — fit to the evaluation axes does.
- Proof points everywhere. An unsubstantiated claim in front of an analyst is worse than silence.
- Name gaps in the prep, answer them in Q&A. The analyst will find every weakness; preparation beats getting caught.
- Never disparage named competitors. Differentiate on your strength.
- This produces the prep pack; a human delivers the briefing. Do not present the output as the briefing itself.
- **All output is DRAFT until human-reviewed.** Label every output "DRAFT — requires human review" at the top and bottom.

## Output Format

```markdown
# Analyst briefing prep — [firm / evaluation] (DRAFT — requires human review)

**Firm / analyst:** [who] | **Vehicle:** [MQ / Wave / MarketScape / inquiry] | **Timing:** [cycle stage]
**Date:** [date]

## Situation brief
[One paragraph: firm, axes, current view, what to set or correct]

## Proof points mapped to evaluation criteria
| Criterion | Axis | Evidence | Strength | Gap |
|---|---|---|---|---|

## Deck outline
1. Company snapshot — [key points]
2. Market change / POV — [the thesis]
3. Positioning / differentiation — [...]
4. Capabilities vs criteria — [...]
5. Proof — [reference customers, metrics]
6. Roadmap — [dated milestones]
7. Demo — [link to storyboard]

## Demo storyboard
| Beat | Shows | Proves | Time |
|---|---|---|---|

## Q&A prep
### Q: [hard question]
- Why they ask: [...]
- Answer: [...]
- Proof: [...]
- Do not: [...]

[repeat per anticipated question]

DRAFT — requires human review
```

## Related Skills

- `/gtm:positioning` — the position you present and defend to the analyst.
- `/gtm:write-narrative` — the market point-of-view that opens the briefing.
- `/gtm:competitive-analysis` — how the analyst will compare you; feeds the comparison Q&A.
- `/gtm:write-messaging-hierarchy` — the proof points and claims, structured for the deck.
