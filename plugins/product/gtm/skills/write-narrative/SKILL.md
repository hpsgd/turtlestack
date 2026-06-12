---
name: write-narrative
description: "Write a strategic narrative using the Andy Raskin structure — name the big change in the world, name the stakes of the old world (the enemy), paint the promised land, and prove you can get the buyer there. Use for keynote, pitch, vision deck, or category-defining story. Argues a real narrative grounded in positioning, not a template fill."
argument-hint: "[product or company to write the strategic narrative for]"
user-invocable: true
allowed-tools: Read, Write, Bash, Glob, Grep
---

# Write a strategic narrative

Write a strategic narrative for $ARGUMENTS using the [Andy Raskin strategic narrative](https://www.andyraskin.com/) structure. A strategic narrative is not a product pitch and not a messaging list — it is the story that reframes the buyer's world so that choosing you becomes the obvious move. It opens a keynote, anchors a pitch deck, and gives the whole company one story.

The five Raskin moves, in order: **name the big change** in the world, **name the stakes** of that change (winners and losers — the "enemy" is the old way), **show the promised land** (the future the buyer wants), **show the magic** (your capabilities as the means to reach it), and **prove it** with evidence. The order is the argument. You cannot pitch the product before the buyer feels the change.

This narrative must argue a real position, not fill a template. It draws on `/gtm:positioning` for the underlying truth and pairs with `/gtm:write-messaging-hierarchy` (the modular claims; the narrative is the long-form story those claims live inside).

## Step 1 — Ground in positioning

Load the positioning (`/gtm:positioning`) and the messaging hierarchy if it exists. Extract the raw material the narrative will dramatise:

- The unique attributes and value (these become "the magic" and "the promised land").
- The competitive alternatives and status quo (these become "the old world" and its stakes).
- The target customer (the protagonist of the narrative — it's their story, not yours).

If there is no positioning, stop and build it first. A narrative without positioning is fiction.

## Step 2 — Name the big change

Open with an undeniable shift in the world — economic, technological, regulatory, behavioural. Not about your product. A change the buyer already half-feels and will nod at.

Rules:

- The change must be true and external. "AI is changing software" is a cliché; name the *specific* shift that creates the buyer's new problem.
- It must be undeniable. If a buyer could shrug and say "not really," it is too weak. The change should make standing still feel risky.
- It is not about you. The product does not appear yet. The change creates the stakes that the product later resolves.

Write the change as a claim you would defend in a debate, then the one-sentence version for the keynote.

## Step 3 — Name the stakes (the enemy)

Show what the change means: there will be winners and losers. The "enemy" is never a competitor by name — it is the old way of operating that the change has made dangerous. Make the buyer feel the cost of staying in the old world.

Rules:

- The enemy is the old world / status quo, not a rival company. Naming a competitor makes it a sales fight; naming the old way makes it a movement.
- Make the stakes concrete and asymmetric: the winners pull ahead, the losers fall behind, and the gap widens. Show why the middle ground disappears.
- Tie the stakes to the buyer's actual world — their job, their numbers, their risk — using language from `/gtm:market-voc` where available.

## Step 4 — Show the promised land

Paint the future the buyer wants — the world after they adopt the new way. The promised land is desirable and currently hard to reach. It is a state of the buyer's world, described as outcomes, not a feature list.

Rules:

- The promised land is about the buyer, not the product. Describe what becomes true for them, not what your product does.
- It must be hard enough to reach that the buyer needs help — otherwise there's no role for you. If they could get there alone, there's no story.
- Make it specific and visual. "Everything just works" is not a promised land; a concrete picture of the buyer's better day is.

## Step 5 — Show the magic and prove it

Now, and only now, introduce your product — as the capabilities that make the previously-hard promised land reachable. Then prove each capability with evidence.

| Promised-land outcome | The magic (your capability) | Why it was hard before | Proof |
|---|---|---|---|
| [outcome] | [capability] | [old-world obstacle] | [customer evidence, metric, demo moment] |

Rules:

- Every capability maps to a promised-land outcome. A capability that doesn't move the buyer toward the promised land doesn't belong in the narrative — it goes in the spec sheet.
- Proof is mandatory and specific. Customer stories where someone reached the promised land are the strongest proof. "Trust us" is not proof.
- Keep it tight. The narrative names the few capabilities that matter, not the full feature list.

## Step 6 — Write it as one continuous story

Assemble the five moves into prose that reads as one argument, in order. It should be speakable — a person delivers this from a stage. Then pressure-test it.

## Step 7 — Pressure-test the argument

A template-filled narrative passes the structure but fails the room. Test:

- **Change test:** would an informed buyer nod, or shrug? Shrug = the change is too weak.
- **Enemy test:** does the old world feel genuinely dangerous now? If not, the stakes are too soft.
- **Promised-land test:** does the buyer want it badly enough to act? If it's mild, it's not a promised land.
- **Earned-product test:** by the time the product appears, does its arrival feel inevitable? If it feels like a pivot to a pitch, the setup didn't do its work.
- **Ownership test:** could a competitor tell the same story? If yes, the narrative isn't grounded in your real differentiation — return to positioning.

If any test fails, the narrative is not done. Fix the failing move, not the wording.

## Rules

- Argue, don't fill. The five moves are the structure of an argument, not boxes to populate. A narrative that names a change nobody feels and a promised land nobody wants is a template, and the room will know.
- The enemy is the old way, never a named competitor. Movements have enemies that are conditions; sales fights have enemies that are companies.
- The product arrives late, by design. Introduce capabilities only after the change, stakes, and promised land have earned their place.
- It's the buyer's story. The protagonist is the customer reaching the promised land — not the company.
- Ground every move in positioning. If the narrative could be a competitor's, it isn't yours — the differentiation isn't in it.
- Write it to be spoken. If it can't be delivered from a stage in a few minutes, it's an essay, not a narrative.
- **All output is DRAFT until human-reviewed.** Label every output "DRAFT — requires human review" at the top and bottom. Apply the writing-style rules — a narrative riddled with AI tells dies on delivery.

## Output Format

```markdown
# Strategic narrative — [product / company] (DRAFT — requires human review)

**Grounded in positioning:** [one-line restatement]
**Date:** [date]

## 1. The change
[Defensible claim + one-sentence keynote version]

## 2. The stakes (the enemy = the old world)
[Winners vs losers, concrete and asymmetric, tied to the buyer's world]

## 3. The promised land
[The buyer's desirable, hard-to-reach future, as outcomes]

## 4. The magic + proof
| Outcome | Capability | Hard before because | Proof |
|---|---|---|---|

## The narrative (continuous, speakable)
[The full story in prose, five moves in order, ready to deliver]

## Pressure-test results
| Test | Pass/Fail | Fix if fail |
|---|---|---|
| Change | | |
| Enemy | | |
| Promised land | | |
| Earned product | | |
| Ownership | | |

DRAFT — requires human review
```

## Related Skills

- `/gtm:positioning` — the required foundation. The narrative dramatises the positioning; it cannot invent differentiation positioning doesn't have.
- `/gtm:write-messaging-hierarchy` — the modular claim system; the narrative is the long-form story those claims live inside. Same positioning root.
- `/gtm:market-voc` — buyer language and felt stakes sharpen the change and the enemy.
- `/gtm:launch-plan` — the narrative anchors launch keynotes and campaign storytelling.
