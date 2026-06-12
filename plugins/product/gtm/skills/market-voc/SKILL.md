---
name: market-voc
description: "Capture the go-to-market voice-of-customer lens — how the market reacts to positioning, what objections sales hears, and why customers switch to or away from us. Use when you need market-facing VoC (positioning resonance, objection patterns, switching triggers) as input to messaging, battle cards, or positioning. This is GTM's lens; other roles hold their own."
argument-hint: "[product, segment, or campaign to gather market VoC for]"
user-invocable: true
allowed-tools: Read, Write, Bash, Glob, Grep, WebSearch, WebFetch
---

# Market voice-of-customer (GTM lens)

Gather the go-to-market voice-of-customer view for $ARGUMENTS: how prospects and customers react to our positioning, what objections sales hears in deals, and what makes people switch toward us or away from us. This is the market-facing slice of VoC — the language buyers use, the doubts they raise, and the trigger that made them move.

VoC is deliberately distributed across the team. Each role holds its own lens, and the overlap is intentional. Support hears VoC through tickets. Customer Success hears it through renewals and churn. UX Research hears it through interviews. You hear it through the buying conversation — positioning resonance, sales objections, win/loss switching. Do not try to centralise VoC into one role or reconcile your findings with theirs into a single number. When findings conflict (e.g. Support says onboarding is the pain, you hear that price is the objection), surface the conflict — it is signal, not noise. The consuming role (product-owner, CPO) is expected to ask several lenses and weigh them.

This skill feeds `/gtm:positioning`, `/gtm:write-messaging-hierarchy`, and `/gtm:write-battle-card`. It does not replace the analyst plugin's strategic competitive intelligence or Support's `feedback-synthesis`.

## Step 1 — Scope the VoC pull

Define exactly whose voice you are capturing and through which channel. State:

- **Population** — prospects in active deals, recently won customers, recently lost deals, churned accounts, or all four.
- **Segment** — SMB, mid-market, or enterprise. Mixing segments hides the truth: an SMB price objection and an enterprise security objection are not the same finding.
- **Time window** — last quarter is signal; anything older than 12 months is stale and must be labelled as such.
- **Channel** — sales call notes, CRM deal records, win/loss interviews, public reviews ([G2](https://www.g2.com), [Capterra](https://www.capterra.com), [TrustRadius](https://www.trustradius.com)), social, support escalations passed up from Support's `feedback-synthesis`.

Output a one-line scope statement: "Market VoC for [product], [segment], [window], drawn from [channels]."

## Step 2 — Capture positioning resonance

For the current positioning (pull it from `/gtm:positioning` output if it exists), capture how the market actually reacts to it. For each core positioning claim, record:

| Positioning claim | How buyers react | Their words (verbatim) | Resonates / falls flat / confuses |
|---|---|---|---|
| [claim] | [paraphrase] | "[exact quote]" | [verdict] |

Rules:

- Use the buyer's words, not ours. If we say "unified platform" and buyers say "one login instead of five," record both — the gap is the finding.
- A claim that confuses is worse than a claim that falls flat. Flag confusion explicitly.
- At least 3 verbatim quotes per claim, or mark the claim "insufficient evidence."

## Step 3 — Catalogue sales objections

List the objections sales hears, ranked by frequency. For each:

| Objection (verbatim) | Frequency | Root cause | Real concern / misconception / competitor FUD | Current response | Works? |
|---|---|---|---|---|---|
| "[what they say]" | High / Med / Low | [why it comes up] | [classification] | [what sales says now] | Yes / No / Sometimes |

Rules:

- Separate the stated objection from the root cause. "Too expensive" is often "I don't see the value yet" — record both.
- Classify each: a real concern needs a product or pricing answer; a misconception needs a messaging fix; competitor FUD needs a battle-card response.
- Objections that recur across segments are positioning problems. Objections specific to one segment are enablement problems.

## Step 4 — Reconstruct switching reasons

For won and lost deals (and churn where available), reconstruct the switch. Borrow the four-forces framing — what pushed them off the old solution, what pulled them toward the new one, what anxiety held them back, and what habit anchored them:

| Direction | Push (off old) | Pull (toward new) | Anxiety (held back) | Habit (anchored to old) |
|---|---|---|---|---|
| Switched to us | [trigger] | [what won it] | [what nearly killed it] | [what they had to overcome] |
| Switched away / lost | [what pushed them to look] | [what the competitor offered] | [our reassurance that failed] | [inertia we couldn't break] |

Rules:

- The trigger matters most. People do not switch because a feature is nice — they switch when something breaks the status quo. Name the trigger event.
- Lost-deal switching is more valuable than won-deal switching. Winners are biased toward flattering us; losers tell you what is actually missing.
- Distinguish the reason sales recorded from the reason the buyer gives. The gap between the two is a known, repeatable finding — chase it.

## Step 5 — Synthesise and route

Pull the findings into themes. For each theme, state the evidence strength and route it to the owning skill or role:

| Theme | Evidence (count, tiers) | Confidence | Conflicts with | Route to |
|---|---|---|---|---|
| [theme] | [n quotes, n deals] | High / Med / Low | [other lens, if any] | positioning / messaging / battle-card / product-owner |

Surface conflicts with other VoC lenses explicitly in the "Conflicts with" column. Do not resolve them — name them so the consuming role can weigh both.

## Rules

- This is the GTM lens, not the whole of VoC. Never present your findings as "the" voice of the customer — present them as the market-facing view, and name the other lenses (Support, Customer Success, UX Research) that hold the rest.
- Don't reconcile conflicting VoC into one number. If your data and Support's data disagree, that conflict goes in the output. Reconciliation is the consuming role's job, and the disagreement is information.
- Verbatim over paraphrase. A finding without at least one real quote is an opinion. Quote the buyer.
- Separate stated reason from root cause everywhere — objections, switching, resonance. The stated thing is rarely the real thing.
- Lost and churned voices outweigh won and retained voices for finding gaps. Weight them accordingly.
- Date every source. VoC older than 12 months is labelled stale and excluded from confidence-2+ claims.
- **All output is DRAFT until human-reviewed.** Label every output "DRAFT — requires human review" at the top and bottom.

## Output Format

```markdown
# Market VoC — [product / segment] (DRAFT — requires human review)

**Scope:** [population, segment, window, channels]
**Date:** [date]
**Lens:** GTM (market-facing). Other VoC lenses: Support (tickets), Customer Success (churn/renewal), UX Research (interviews).

## Positioning resonance
| Claim | How buyers react | Verbatim | Verdict |
|---|---|---|---|

## Sales objections (ranked by frequency)
| Objection | Frequency | Root cause | Classification | Current response | Works? |
|---|---|---|---|---|---|

## Switching reasons
| Direction | Push | Pull | Anxiety | Habit |
|---|---|---|---|---|

## Themes and routing
| Theme | Evidence | Confidence | Conflicts with | Route to |
|---|---|---|---|---|

## Conflicts with other lenses
[Explicit list of where this lens disagrees with Support / CS / UX Research findings. Unresolved by design.]

## Recommended actions
1. [action] — [why, tied to a theme] — route to [owner]

DRAFT — requires human review
```

## Related Skills

- `/gtm:positioning` — positioning resonance findings feed directly into sharpening or revalidating positioning.
- `/gtm:write-messaging-hierarchy` — objection patterns and buyer language shape the message architecture.
- `/gtm:write-battle-card` — competitor FUD and lost-deal switching reasons feed objection handling on battle cards.
- `/gtm:competitive-analysis` — sales-enablement competitive view; pair switching reasons with head-to-head differentiation.
