---
name: write-product-vision
description: "Write a one-page product vision using Roman Pichler's Product Vision Board (vision, target group, needs, product, business goals). Use when starting a product, entering a new market, or when a team has lost strategic coherence and needs alignment on direction before roadmap work. Produces a single-page vision artifact owned by the CPO."
argument-hint: "[product or product area to write a vision for]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Write a product vision (Pichler Vision Board)

Write a one-page product vision for $ARGUMENTS using the [Product Vision Board](https://www.romanpichler.com/blog/product-vision-board/) (Roman Pichler). The vision is the change in the world the product is trying to make; this artifact captures it on one page across five cells — vision, target group, needs, product, and business goals.

This is a CPO-owned artifact. Strategy authoring belongs to the CPO, not the product manager — the PM provides slice-level input (a segment's needs, a feature area's evidence) but the vision and its cells are set here. The vision sits above the roadmap. Once it exists, `/cpo:write-product-strategy` turns it into the plan to get there, and `/cpo:diagnose-strategy` checks that plan.

## Step 1: Establish context and scope

Before filling any cell, establish:

1. **Scope** — is this a vision for the whole product, a product line, or a distinct product area? A vision board describes one product. If the scope spans several products with different users, you need several boards.
2. **Time horizon** — the vision describes the product 2-5 years out. State the horizon explicitly so the cells are written at the right altitude.
3. **Trigger** — why now? New product, new market entry, or recovering lost coherence. The trigger shapes how much is fixed versus open.
4. **Existing evidence** — read any PRDs, OKRs, customer research, or prior vision artifacts in the project (`docs/`, backlog, research outputs). Reference them. A vision invented without evidence is a wish.

Output of this step: a short context paragraph naming scope, horizon, trigger, and the evidence consulted.

## Step 2: Draft the vision cell

The vision is the ultimate purpose — the positive change the product creates in the world. Not what the product is; what it makes possible.

Rules for the vision statement:

- **Broad and aspirational, but not vacuous.** It should outlast any single release and any single feature.
- **Describes a change in the world, not a product.** "Help small clinics run without a back office" is a vision. "Build the best clinic scheduling app" is a product description.
- **One or two sentences.** If it needs a paragraph, it isn't a vision yet.
- **Free of the word "best", "leading", "world-class".** Those are filler, not direction.

Pressure-test: would this vision still be true if a competitor shipped the same product? If yes, it's about the change, not the artifact — good. Would it survive replacing every current feature? It must.

## Step 3: Draft the target group cell

Who are the users and customers? Be specific. "Everyone" is not a target group.

- Name the **primary** user segment and, if distinct, the **paying customer** (they may differ — the user of a school product is a teacher; the buyer is an administrator).
- Describe them by situation and behaviour, not just demographics. "Solo physiotherapists who currently run bookings on paper or a shared spreadsheet" beats "healthcare SMBs".
- If you can't name a single primary group, the scope (Step 1) is too wide. Narrow it or split the board.

Pressure-test: could you find ten of these people to talk to this week? If the description is too abstract to recruit against, sharpen it.

## Step 4: Draft the needs cell

What problem does the product solve, or what benefit does it provide, for the target group? This is the cell that justifies the product's existence.

- State the need as a **customer problem**, not a feature. "Can't tell which clients are about to cancel" is a need. "Churn dashboard" is a feature.
- Limit to the **two or three core needs** the product exists to serve. A list of ten needs means the vision isn't focused.
- Each need must connect to the target group named in Step 3 — a need for a different group signals scope drift.

Pressure-test: for each need, what is the evidence it's real and important to this group? Tag each as `[evidenced]`, `[assumed]`, or `[to validate]`. An all-`[assumed]` needs cell is the most common failure of a vision board — flag it.

## Step 5: Draft the product cell

What is the product, and what makes it stand out? Three to five differentiating characteristics — not a feature list.

- Each item answers "why would the target group choose this over the alternative (including doing nothing)?"
- Differentiators are **characteristics**, not features. "Works offline in low-signal clinics" is a characteristic; "offline mode" is a feature implementing it.
- Three to five maximum. If you have more, you're listing the backlog, which is exactly the mistake Pichler warns against.

Pressure-test: cross-check each differentiator against a need in Step 4. A differentiator that serves no stated need is a feature looking for a justification — cut it or surface the missing need.

## Step 6: Draft the business goals cell

What does the company gain from the product? How does it benefit the business?

- State **business outcomes**, not vanity metrics. "Reach profitability on this line within 8 quarters" beats "acquire many users".
- Two to four goals. These are the reasons the business invests, expressed as outcomes (revenue, market position, strategic capability, retention).
- Keep them measurable in principle even if not yet quantified — they become the anchor for OKRs later (`/coordinator:define-okrs`).

Pressure-test: if every business goal were met but the needs cell weren't served, would that be success? If yes, the goals are disconnected from the users — realign.

## Step 7: Pressure-test the whole board for coherence

A vision board fails as a set even when each cell passes alone. Run these cross-cell checks:

- [ ] **Target group ↔ needs** — every need belongs to the named group, and the group has no major unserved need missing from the board.
- [ ] **Needs ↔ product** — every differentiator serves a stated need; every core need has a differentiator addressing it.
- [ ] **Product ↔ business goals** — the differentiators plausibly produce the business outcomes.
- [ ] **Altitude** — nothing in the board is a roadmap item or a sprint-level feature. The board operates above the roadmap.
- [ ] **Evidence honesty** — assumptions are labelled, not disguised as facts.

If a check fails, revise the relevant cell and re-run. Don't ship a board with a known broken link.

## Rules

- **Always fill all five cells.** A board missing the needs or business-goals cell is not a vision — it's a slogan. If a cell can't be filled, that's the finding: name what's unknown.
- **Never let the product cell become a feature list.** Three to five differentiating characteristics, full stop. The moment it reads like a backlog, you've made Pichler's most common mistake.
- **Never write "everyone" in the target group.** If the product genuinely serves multiple distinct groups, produce multiple boards, not one vague one.
- **Don't invent evidence.** Label needs and differentiators as `[evidenced]`, `[assumed]`, or `[to validate]`. An honest assumption beats a fabricated fact.
- **Don't reach for "best", "leading", "world-class", "seamless".** They signal absence of direction. State the actual change in the world.
- **The vision is the CPO's to author.** Take slice-level input from the PM and discovery, but the board is set here. Don't delegate the authoring; delegate the input.
- **Keep it to one page.** The artifact's value is that it fits on one page and can be read in a minute. Two pages means it's drifted into strategy or roadmap territory.

## Output Format

Write the result to `docs/product-vision-[product-slug].md`. A blank template lives at `plugins/leadership/cpo/templates/product-vision-board.md`.

```markdown
# Product vision — [product or area]

**Horizon:** [2-5 year target] · **Scope:** [whole product / line / area] · **Author:** CPO · **Date:** [YYYY-MM-DD]

**Context:** [scope, horizon, trigger, and evidence consulted — one short paragraph]

## Vision

[One or two sentences — the change in the world this product makes.]

## Target group

- **Primary user:** [specific, recruitable description]
- **Paying customer (if distinct):** [who buys]
- [Behavioural / situational detail]

## Needs

- [Core customer problem 1] — `[evidenced | assumed | to validate]`
- [Core customer problem 2] — `[evidenced | assumed | to validate]`
- [Core customer problem 3] — `[evidenced | assumed | to validate]`

## Product

- [Differentiating characteristic 1 — why they'd choose this]
- [Differentiating characteristic 2]
- [Differentiating characteristic 3]
- [Up to 5 total — not a feature list]

## Business goals

- [Business outcome 1 — why the company invests]
- [Business outcome 2]
- [Up to 4 total]

## Coherence check

- [ ] Target group ↔ needs aligned
- [ ] Needs ↔ product aligned
- [ ] Product ↔ business goals aligned
- [ ] Above-the-roadmap altitude held
- [ ] Assumptions labelled honestly

## Open questions

- [What's unknown and who can resolve it]
```

## Related skills

- `/cpo:write-product-strategy` — once the vision exists, write the strategy: the plan to get from today to the vision.
- `/cpo:diagnose-strategy` — run Rumelt's good-vs-bad diagnostic over the strategy that descends from this vision.
- `/coordinator:define-okrs` — the business goals cell anchors the OKRs that measure progress toward the vision.
