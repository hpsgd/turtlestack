# Write Interview Guide

Scenario: A PM needs a generative interview guide before running discovery. The skill must apply The Mom Test rigorously: open with the three rules, write behavioural questions anchored to specific past events (never "would you use X?"), arm the interviewer with fluff-redirect prompts (compliments are a warning, not a win), and structure the arc with a soft close — without pitching the solution.

## Prompt

> Use the product-manager `write-interview-guide` skill to write a generative discovery interview guide to
> understand how mid-market ops managers currently deal with duplicate customer records and what it costs them.
> Write the guide to a file under `docs/product/` in the current working directory, in the skill's standard
> format.
> 
> Proceed without asking — produce the interview guide.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Interview guide created at `docs/product/interview-guide--duplicate-customer-records.md`.

The guide follows all five discovery steps:

1. **Learning goal** — Understanding how ops managers *currently* deal with duplicates and what it costs them (not validating a solution)

2. **Mom Test rules** — Reinforces talking about their life, anchoring to past events, and listening more than talking

3. **10 behavioural questions** — Each anchored to a recent, specific duplicate incident. Topics: detection, resolution process, time cost, frequency, volume, hidden incidents, current tools, past attempts to fix, merge logic, compliance/revenue impact

4. **Fluff redirects** — Immediate redirects for generic claims ("we usually catch them"), future promises ("we'd build something if we had time"), compliments, opinions, and vague timelines

5. **Conversation arc** — Opens with role/context (warm up), moves to the 10 core questions in sequence, ends with soft close and doorknob insights

The guide is ready to use by an interviewer. It's designed to avoid leading the witness, expose the real workarounds and costs, and identify whether the problem is one-person frustration or systemic team drag.

### Artifacts written

#### `work/docs/product/interview-guide--duplicate-customer-records.md`

```
# Interview guide: Duplicate customer records in mid-market ops

**Learning goal:** Understand how mid-market operations managers currently identify, resolve, and live with duplicate customer records — including the manual effort, error costs, compliance exposure, and workarounds they've developed.

## The three rules (read before every interview)

1. **Talk about their life, not your idea.** Don't describe a deduplication tool or solution. The moment you do, every answer becomes polite validation instead of honest signal
2. **Ask about specific past events, not hypotheticals.** "Would you want a dedup tool?" gets a yes. "Tell me about the last time you found a duplicate and what you did" gets the truth
3. **Talk less, listen more.** After they answer, wait. The silence is where they fill in the real frustration, the workaround they're embarrassed about, the actual cost

---

## Opening (warm up)

Start broad to establish context. Let them talk about their role and world before you narrow to duplicates.

- **"Tell me about your role. What does a typical week look like for you?"**
  - Goal: understand their world, not your solution. Learn what "customer data management" means in their context (CRM work? Manual spreadsheets? Legacy system?). Notice what takes their time.

- **"How big is your team, and who touches customer data?"**
  - Goal: understand whether this is a one-person bottleneck or a distributed problem. Learn about dependencies (e.g., sales enters data, ops cleans it, accounting uses it).

- **"Walk me through how a new customer gets into your system. From the first touchpoint to 'now they're in the database,' what happens?"**
  - Goal: map the entry points where duplicates could form (multiple sources, imports, manual entry, integrations).

---

## Behavioural core

Each question is anchored to a recent, specific event. No hypotheticals. No "usually." A real thing they did.

| # | Question | What it tells us |
|---|----------|------------------|
| 1 | **"Tell me about the last time you discovered a duplicate customer record. When was that, and how did you notice it?"** | Frequency, detection method (manual? system alert? customer complaint?), how visible the problem is. Also: does a duplicate have to cause a symptom before they notice it? |
| 2 | **"Walk me through what you did when you found that duplicate. Step by step — what actually happened?"** | The manual process, tools used, people involved, decision logic (merge? delete? which one is 'correct'?). This is where you find the workarounds and the embarrassment. |
| 3 | **"How long did it take you to resolve that one duplicate? From 'I noticed it' to 'it's fixed,' what was the time investment?"** | The true operational cost. Do they know? (If they don't, that's a signal the problem is diffuse.) |
| 4 | **"Before that one, when was the time before that you had to deal with a duplicate?"** | Frequency. Push for actual dates/timeframes, not "every week" or "pretty often." |
| 5 | **"How many duplicates do you think you're dealing with right now — records that exist in your system today that shouldn't?"** | Scope of the problem. Also notice: can they even estimate? Do they have visibility? |
| 6 | **"Have you ever discovered a duplicate *after* something bad happened — a missed sale, a billing error, a customer call because they got contacted twice?"** | The hidden cost. Focus on the incident, not the hypothetical. Let them walk through what the customer experienced, what the business lost. |
| 7 | **"What systems or tools are you currently using to find or prevent duplicates?"** | Current state — homegrown scripts? CRM built-ins? Manual spot-checks? Nothing? |
| 8 | **"Have you ever tried to fix the duplicate problem — bought a tool, built something, changed a process? What did you try?"** | What have they already invested? What did and didn't work? Why didn't it stick? |
| 9 | **"When you merge two customer records, how do you decide which one is 'correct'? What data do you trust, and what data do you throw away?"** | The logic and fear. Are they worried about losing data? Do they keep both? Do they have a standard or is it per-record judgment? |
| 10 | **"Is there anything about duplicate records that affects how your company communicates with or bills customers — or anything compliance-related you worry about?"** | Downstream impact — regulatory exposure, customer experience, revenue risk. Let them talk about the worry, not the policy. |

---

## Fluff redirects

Keep the interviewer honest. Redirect these patterns immediately:

| Type | What it sounds like | Redirect |
|------|-------------------|----------|
| **Generic claim** | "We usually catch them pretty quickly" / "I don't think it's a big problem for us" | "Tell me about the last time that happened. When did you actually catch a duplicate?" / "When was the most recent one you had to deal with?" |
| **Future promise** | "We've been meaning to implement a system" / "If we had time, we'd set up a check" | "Have you ever actually built something like that before? When?" / "What happened the last time you tried to prioritize this?" |
| **Compliment to your probe** | "That's a great idea" / "Yeah, something like that would definitely help" | "What about it would fit how you work today?" / "Have you ever seen that approach work in practice? Where?" |
| **Opinion instead of experience** | "I think most of our duplicates come from X" / "The problem is usually Y" | "Tell me about a specific duplicate you found. What was actually causing that one?" |
| **Vague timeline** | "This happens pretty often" / "We deal with this all the time" | "When did you last deal with one? And the one before that? How many in the last month?" |

---

## Soft close

Don't end abruptly. The best insights often arrive in the last 60 seconds.

- **"What didn't I ask about that I should have?"**
  - Let them volunteer. Often they'll surface the thing that matters most to them but didn't fit your questions.

- **"Is there anyone else on your team I should talk to about this — someone who handles the day-to-day dedup work?"**
  - Map the team. Get a name. The ops manager may oversee it, but the person doing the manual work has the real story.

- **Keep the recorder running after they think the interview is over.** Walk them to the door. Ask a casual follow-up. The doorknob insight (the thing they mention as they're about to leave) is often the most honest.

---

## Notes for the interviewer

- **Two people minimum:** One leads, one takes notes. The note-taker catches what the lead missed — also prevents confirmation bias.
- **Record if they consent.** Audio lets you catch the tone and the pauses. Transcribe the behavioural sections later.
- **If every answer supports your solution, you ran a confirmatory interview, not a generative one.** Discomfort is a sign you're asking the right questions.
- **Data quality = silence.** If you feel awkward after a long pause, that's working. Don't fill it.
- **One duplicate story per interview is better than five vague claims.** Go deep into one incident, not wide across five.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 13.0/13.0 (100%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 39222 ms |
| Target cost | $0.0665 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | PASS: States a learning goal about understanding a current behaviour ("how they reconcile duplicates and what it costs"), not validating a solution ("would they use our dedup feature") | PASS | Learning goal: 'Understand how mid-market operations managers currently identify, resolve, and live with duplicate customer records — including the manual effort, error costs...' |
| c2 | PASS: Opens the guide with the three Mom Test rules (talk about their life not your idea; ask about specific past events not hypotheticals; talk less, listen more) | PASS | Section 'The three rules (read before every interview)' lists all three verbatim: life not idea, past events not hypotheticals, talk less listen more. |
| c3 | PASS: Every behavioural question anchors to a real, recent, specific past event — "tell me about the last time you dealt with a duplicate record" — NOT "would you..." or "how often do you..." in the abstract | PASS | Q1: 'Tell me about the last time you discovered a duplicate'; Q2: 'Walk me through what you did when you found that duplicate'; Q4: 'Before that one, when was the time before that...' |
| c4 | PASS: Contains NO hypothetical-future or opinion questions — no "would you use", "do you think", "how would you want to solve this" | PASS | All 10 core questions use past-event or current-state anchors. No 'would you', 'do you think', or 'how would you want' phrasing found in the behavioural core. |
| c5 | PASS: Includes fluff-redirect prompts for generic claims, future promises, and compliments — and treats a compliment as a warning sign, not validation | PASS | Fluff redirects table lists 'Generic claim', 'Future promise', 'Compliment to your probe' with redirects — compliment redirect asks 'What about it would fit how you work today?' |
| c6 | PASS: Does NOT pitch or describe a solution anywhere in the guide (no concept reactions in a generative interview) | PASS | Rule 1 explicitly says 'Don't describe a deduplication tool or solution.' No product or feature concept is mentioned anywhere in the guide. |
| c7 | PASS: Structures the arc: warm-up opening → behavioural core → soft close ("what didn't I ask that I should have?") | PASS | Distinct sections: 'Opening (warm up)', 'Behavioural core', 'Soft close' — soft close includes exact phrasing 'What didn't I ask about that I should have?' |
| c8 | PARTIAL: Notes a confirmation-bias guard — e.g. two interviewers, or that a zero-discard interview is a red flag | PARTIAL | Notes: 'Two people minimum... prevents confirmation bias' and 'If every answer supports your solution, you ran a confirmatory interview, not a generative one.' |
| c9 | PASS: Output guide file exists under `docs/product/` opening with the three Mom Test rules and a behaviour-focused learning goal | PASS | File at `work/docs/product/interview-guide--duplicate-customer-records.md` opens with learning goal then 'The three rules' section containing all three Mom Test rules. |
| c10 | PASS: The behavioural-core questions are all anchored to specific past events; a reader could not find a "would you" / "do you think" hypothetical among them | PASS | All 10 questions in the behavioural core table use past-event anchors or current-state probes. No 'would you' or 'do you think' phrasing present. |
| c11 | PASS: Output includes explicit redirects for compliments / generic claims / future promises, framing compliments as zero-signal | PASS | Fluff redirects table explicitly covers 'Compliment to your probe' with redirect questioning practical fit — treating the compliment as requiring investigation, not acceptance. |
| c12 | PASS: No solution is pitched anywhere in the guide | PASS | No deduplication product, tool, or feature concept is described or pitched. Rule 1 and the guide body are consistently solution-agnostic. |
| c13 | PASS: The guide has distinct opening, behavioural-core, and soft-close sections — the soft close keeps listening for the doorknob insight | PASS | Soft close includes 'Keep the recorder running after they think the interview is over. Walk them to the door... The doorknob insight... is often the most honest.' |
| c14 | PARTIAL: Output flags a confirmation-bias guard (note-taker / two interviewers / zero-discard red flag) | PARTIAL | Notes section: 'Two people minimum: One leads, one takes notes... prevents confirmation bias' and zero-discard red flag warning about confirmatory vs generative interviews. |

### Notes

The guide is exceptionally well-formed: all three Mom Test rules appear verbatim before the questions, every behavioural question anchors to a past event, the fluff-redirect table covers all required patterns including compliments-as-warning, no solution is pitched, and the arc is complete with a doorknob-insight soft close. Both PARTIAL-capped criteria (c8, c14) are fully satisfied within their ceiling.
