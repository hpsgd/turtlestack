---
name: write-interview-guide
description: "Write a generative discovery interview guide following The Mom Test — questions about specific past behaviour, not hypothetical future intent. Produces a runnable guide with opening, behavioural questions, fluff-redirect prompts, and a close. Use before running customer discovery interviews."
argument-hint: "[problem space or desired outcome to explore]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Write a generative discovery interview guide for $ARGUMENTS.

Generative interviews explore and discover — they run before you have a solution, to map a problem space
the team didn't have before. They are not usability tests and not surveys. The hard part is avoiding
feedback that confirms your idea when the real signal is that people are being polite. This guide follows
[The Mom Test (Rob Fitzpatrick)](http://momtestbook.com/): talk about their life not your idea, ask about
specific past events not hypothetical futures, and listen more than you talk.

Follow every step. The output is a guide an interviewer can run without leading the witness.

## Step 1: State the learning goal

One sentence: what does the team need to understand that it doesn't now? This is about the customer's
world, not your solution. "Understand how ops managers currently reconcile duplicate records and what it
costs them" — not "find out if they'd use our dedup feature". This step is complete when the learning goal
names a behaviour to understand, not a solution to validate.

## Step 2: Write the three Mom Test rules at the top of the guide

Every guide opens with the rules, as a reminder to the interviewer:

1. **Talk about their life, not your idea.** Don't pitch. The moment you describe your solution, you've
   biased every answer that follows
2. **Ask about specific past events, not hypothetical future behaviour.** "Would you use X?" gets a polite
   yes. "Tell me about the last time you did X" gets the truth
3. **Talk less, listen more.** After they answer, wait. The continuation after the silence is usually
   where the real information lives

## Step 3: Write behavioural questions

Every question anchors on a real, recent, specific event. Convert each thing you want to learn into a
past-behaviour question:

| Want to learn | Bad (hypothetical/opinion) | Good (specific past behaviour) |
|---------------|----------------------------|-------------------------------|
| Whether the problem is real | "Is duplicate data a problem for you?" | "Tell me about the last time you dealt with a duplicate record. Walk me through what happened." |
| Frequency and cost | "How often does this happen?" | "When did it last happen? And before that? How long did it take you?" |
| Current workaround | "How would you want to solve this?" | "What did you actually do about it last time? Show me, if you can." |
| Willingness to pay | "Would you pay for a fix?" | "Have you spent money trying to solve this? What did you buy?" |

Write 6-10 behavioural questions. Each must reference a specific past event. This step is complete when no
question asks about a hypothetical future or an opinion.

## Step 4: Write fluff-redirect prompts

Fluff is generic claims ("I usually…"), future promises ("I would…"), and hypothetical maybes ("I could
see myself…"). It feels like validation but carries no signal. Compliments ("that's a great idea") are the
strongest warning sign — they cost nothing. Arm the interviewer with redirects:

- On a generic claim → "Tell me about the last time that happened specifically."
- On a future promise → "Have you ever actually done that? When?"
- On a compliment → don't accept it as data — redirect: "What about it would fit how you work today?"

This step is complete when the guide has a redirect for each fluff type.

## Step 5: Structure the conversation arc

Order the guide for rapport, not interrogation:

1. **Open** — broad, easy context questions to warm up ("Tell me about your role and a typical week")
2. **Behavioural core** — the Step 3 questions, easiest to hardest
3. **Soft close** — "What didn't I ask about that I should have?" Keep listening after they think it's over;
   the "doorknob" insight often arrives last

This step is complete when the guide has open, core, and close sections.

## Rules

- **Never pitch your idea in a generative interview.** The instant you describe the solution, you've
  contaminated the data. Save solution reactions for concept testing, not discovery.
- **Anchor every question to a real past event.** Future-tense and opinion questions produce fluff.
- **Treat compliments as a warning, not a win.** Redirect them immediately.
- **Two people minimum.** One leads, one takes notes — the note-taker notices what the lead misses, which
  also counters confirmation bias. In the trio model, all three attend.
- **A zero-discard interview is a red flag.** If every answer supports your plan, you ran a confirmatory
  interview, not a generative one.
- **Silence is a tool.** After an answer, wait. Don't fill the gap with the next question.

## Output Format

Write the guide to `docs/product/interview-guide-[topic].md` using `templates/interview-guide.md`:

```markdown
# Interview guide: [topic]

**Learning goal:** [one sentence — a behaviour to understand]

## The three rules (read before every interview)
1. Talk about their life, not your idea
2. Ask about specific past events, not hypotheticals
3. Talk less, listen more

## Opening (warm up)
- [broad context question]

## Behavioural core
| # | Question (anchored to a past event) | What it tells us |
|---|-------------------------------------|------------------|
| 1 | Tell me about the last time you... | ... |

## Fluff redirects
- Generic claim → "Tell me about the last time that happened."
- Future promise → "Have you ever actually done that? When?"
- Compliment → "What about it fits how you work today?"

## Soft close
- "What didn't I ask about that I should have?"
- [keep recording — note doorknob insights]
```

## Related Skills

- `/product-manager:write-discovery-plan` — the cadence this guide runs inside.
- `/product-manager:switch-interview` — the retrospective purchase-moment variant (Moesta four forces).
- `/product-manager:synthesise-interviews` — turn the answers into OST updates.
