---
name: diagnose-strategy
description: "Critique an existing strategy document using Richard Rumelt's good-strategy/bad-strategy diagnostic. Checks for the kernel (diagnosis + guiding policy + coherent action) and flags the four hallmarks of bad strategy: fluff, failure to face the challenge, mistaking goals for strategy, and bad strategic objectives. Use to pressure-test a product or company strategy before it ships. Read-only critique skill, not an authoring skill."
argument-hint: "[path to the strategy document to diagnose]"
user-invocable: true
allowed-tools: Read, Glob, Grep
---

# Diagnose a strategy (Rumelt good-vs-bad)

Critique the strategy document at $ARGUMENTS using Richard Rumelt's framework from [Good Strategy / Bad Strategy](https://www.goodreads.com/book/show/11721966-good-strategy-bad-strategy) (2011). Most documents called "strategy" aren't — they're goals, aspirations, or buzzwords arranged to look like a plan. This skill checks for the kernel of good strategy and flags the hallmarks of bad strategy, with evidence cited from the document.

This is a **critique** skill, not an authoring skill. It reads an existing strategy and reports findings. It does not rewrite. Strategy authoring belongs to `/cpo:write-product-strategy`; this skill tells you whether what was authored is actually a strategy. Run it as the mandatory follow-up after writing a strategy, or over any inherited strategy document.

## Step 1: Read the document and identify what it claims to be

Read the full document. Establish:

1. **What it calls itself** — strategy, plan, roadmap, vision, OKRs. The label sets the expectation you're testing against.
2. **The intended scope and horizon** — product, company, portfolio; this quarter, this year, multi-year.
3. **The structure** — what sections exist. Note immediately whether there is anything resembling a diagnosis, a guiding policy, and coherent actions; their presence or absence is the core of the assessment.

Output of this step: a one-paragraph summary of what the document is and how it's organised. Quote the document's own framing.

## Step 2: Test for the kernel — diagnosis

Good strategy has a kernel of three interconnected elements. The first is the **diagnosis**: it simplifies a complex situation by naming the critical aspects and the biggest obstacle. Without a diagnosis, the rest of the strategy has nothing to address.

Check:

- Does the document **name the central challenge or obstacle** plainly? Or does it jump straight to goals and actions?
- Is the diagnosis **a simplification that brings clarity**, or a list of everything wrong (which is not a diagnosis)?
- Does it identify **the critical few** aspects, or treat all problems as equal?

Verdict: `Present and sharp` / `Present but vague` / `Missing`. Quote the diagnosis (or note its absence with the line where it should be).

## Step 3: Test for the kernel — guiding policy

The **guiding policy** is the overall approach for overcoming the obstacle named in the diagnosis. It constrains and directs without specifying every action — like the strategy of a military campaign versus the individual orders.

Check:

- Is there **an overall approach** that follows from the diagnosis? ("Solve for the enterprise buyer, not the end user" is a guiding policy; "improve everything" is not.)
- Does it **rule things out**? A guiding policy that permits every action isn't guiding anything.
- Does it **connect to the diagnosis**? A guiding policy addressing a different problem than the one diagnosed is incoherent.

Verdict: `Present and directive` / `Present but permits everything` / `Missing`. Quote it or note the gap.

## Step 4: Test for the kernel — coherent action

**Coherent actions** are the concrete, coordinated steps that carry out the guiding policy. The test is *coherence*: the actions reinforce one another rather than pulling in different directions or sitting as an unconnected list.

Check:

- Are there **specific, coordinated actions**, or just goals and targets?
- Do the actions **reinforce each other**, or compete for the same resources and attention?
- Do they **implement the guiding policy**, or are they a wish list assembled independently of it?
- Is there a **proximate objective** — a near-term target that is both achievable and real progress — rather than only distant aspirations?

Verdict: `Coherent` / `Present but uncoordinated` / `Missing`. Cite examples.

## Step 5: Flag the four hallmarks of bad strategy

Independently of the kernel, scan for Rumelt's four signatures of bad strategy. Each found instance is a flag with a quote.

1. **Fluff** — inflated language, abstraction, and buzzwords masking absence of content. ("Leverage synergies across our ecosystem to deliver world-class value.") Quote every instance. Dense fluff is the strongest single signal that the document is avoiding the actual challenge.
2. **Failure to face the challenge** — no clear definition of the obstacle, so the strategy can't be evaluated against it. If Step 2 found no diagnosis, this hallmark is present by definition.
3. **Mistaking goals for strategy** — statements of desire ("grow to $1B revenue", "become the category leader", "double our user base") presented as the plan. Goals describe the destination; strategy is how you get there. List each goal-as-strategy.
4. **Bad strategic objectives** — either a scattered "dog's dinner" of unrelated goals, or "blue-sky" objectives disconnected from current capabilities. Note whether the objectives are a coherent set or a grab-bag, and whether they're reachable from where the organisation actually is.

## Step 6: Score and produce the verdict

Synthesise into an overall verdict. The kernel is necessary: a document missing any of diagnosis, guiding policy, or coherent action is not a complete strategy, regardless of how polished it reads.

Overall rating:

| Rating | Meaning |
|---|---|
| **Good strategy** | Kernel complete and coherent; no significant bad-strategy hallmarks |
| **Incomplete** | Kernel has gaps (one element missing or vague); fixable with targeted work |
| **Bad strategy** | Multiple hallmarks present; kernel largely absent; mostly goals and fluff |

For each gap and flag, give a **specific, actionable recommendation** — what to add or fix, and which authoring skill produces it (`/cpo:write-product-strategy` for the strategy itself, `/cpo:write-product-vision` if the missing piece is actually the vision). Don't rewrite the strategy here; point to where the fix happens.

## Rules

- **Always cite the document.** Every verdict and flag quotes the relevant line, or names the line/section where the missing element should be. "No diagnosis" is not a finding; "No diagnosis — the document opens at line 12 with goals; no obstacle is named anywhere" is a finding.
- **Never rewrite the strategy.** This skill critiques. It is read-only. Fixes happen in the authoring skills. Recommend; don't author.
- **The kernel is necessary, not optional.** A beautifully written document with no guiding policy is still incomplete. Don't let polish substitute for the kernel.
- **Fluff is a signal, not a style note.** Dense buzzword language usually means the author is avoiding a challenge they can't face. Flag it as evidence of that avoidance, not just as wording.
- **Distinguish goals from strategy every time.** "Grow to $X", "be the leader", "delight customers" are goals. If the document's "strategy" section is a list of these, say so plainly.
- **Don't grade on a curve.** A document can be the best strategy in the organisation and still be bad strategy. Rate against Rumelt's bar, not against what's normal locally.

## Output Format

Return the critique directly (read-only skill — do not write a file unless asked).

```markdown
# Strategy diagnosis — [document name]

**Document:** [path] · **Claims to be:** [strategy/plan/etc.] · **Scope:** [product/company] · **Date diagnosed:** [YYYY-MM-DD]

## Overall verdict: [Good strategy | Incomplete | Bad strategy]

[Two or three sentences summarising the assessment.]

## The kernel

| Element | Verdict | Evidence |
|---|---|---|
| Diagnosis | [Present and sharp / Present but vague / Missing] | [quote or line reference] |
| Guiding policy | [Present and directive / Permits everything / Missing] | [quote or line reference] |
| Coherent action | [Coherent / Uncoordinated / Missing] | [quote or line reference] |

## Bad-strategy hallmarks

| Hallmark | Found? | Evidence |
|---|---|---|
| Fluff | [Yes/No] | [quoted instances or "none found"] |
| Failure to face the challenge | [Yes/No] | [evidence] |
| Mistaking goals for strategy | [Yes/No] | [each goal-as-strategy quoted] |
| Bad strategic objectives | [Yes/No] | [scattered or disconnected objectives] |

## Recommended actions

1. [Highest-priority gap → what to add → which skill produces it]
2. [Next]
3. [Next]
```

## Related skills

- `/cpo:write-product-strategy` — authors the strategy this skill critiques; the place to fix any kernel gaps found here.
- `/cpo:write-product-vision` — if the diagnosis reveals the missing element is actually the vision, write it here first.
