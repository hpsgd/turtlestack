---
description: Writing rules and AI tell avoidance — applied to all text output including documentation, commit messages, PR descriptions, articles, and user-facing copy
---

# Writing Rules — AI Tell Avoidance

When drafting or editing any document, follow these rules. The goal: text that reads like a person wrote it, not like a model generated it.

## The Core Principle

Strip every sentence to its leanest form. For each word, ask: can I drop it without changing the meaning? If yes, drop it. Then do the same for phrases. Then for whole sentences within paragraphs.

> Before: "I attribute that to giving people a safe place to learn and grow, being transparent about direction even when the answers are uncomfortable, and being the kind of leader people know they can rely on when things get hard."

> After: "I attribute that to giving people a safe place to learn and grow, being transparent about direction, and being a leader people can rely on."

The longer version isn't wrong. It's just carrying weight that doesn't earn its place.

---

## Banned Vocabulary

These words appear at 2-50x the rate in AI text compared to human writing. Never use them.

**Tier 1 — immediate flags (near-certain AI signals):**

delve, delves, delving, tapestry, landscape (metaphorical), nuanced, nuance, multifaceted, robust (outside technical contexts), crucial, pivotal, foster, fostering, harness, harnessing, leverage (as verb), streamline, underscore, underscores, meticulous, meticulously, intricate, intricacies, comprehensive, myriad, paradigm, commendable, vibrant, showcasing, showcase, endeavour, seamless, seamlessly, holistic, cultivate, empower, elevate, navigate (metaphorical), cutting-edge, state-of-the-art, utilise, bolstered, enduring, transformative, game-changing, foundational, revolutionary, spearheaded, orchestrated, dynamic (as filler adjective), innovative, results-driven, actionable, keen, deriving, beacon, realm, testament, cornerstone, underpinnings, overarching, embark, synergy, resonate, resonates, groundbreaking, illuminating, illuminate, facilitate, garner, garnered, noteworthy, paramount, align, aligns, aligning, advancements, surpass, surpasses, surpassing, emphasising, emphasizes, highlighting, highlights, comprehending, boasts, enhance, enhances, enhancing, explore, explores, exploring, scalable, impactful, maximise, maximize, optimise, optimize, interplay, unleash, unlock, reshape, redefine, reimagine, capabilities (as filler noun), valuable (as filler adjective), profound, profoundly

**Tier 1 — corporate-jargon flags (separate sub-group, same severity):**

mission-critical, next-generation, turnkey, best-in-class, world-class, versatile, exemplary, agile (as filler adjective, not the methodology), catalyse, catalyze, amplify, pioneer, pioneering, undertake, champion (as verb), drive (as filler verb in business contexts), delivers, deliver (as filler), engage, engagement (as filler), execute, execution (corporate sense), revitalise, reimagine

**Tier 2 — contextual flags (suspicious in clusters of 2+):**

furthermore, moreover, additionally, consequently, notably, importantly, arguably, essentially, fundamentally, ultimately, primarily, particularly, significantly, remarkably, incredibly, exceedingly, enthusiastically, flawlessly, consistently, strategically, effectively, boast, unprecedented, sustainable (as filler), inclusive (as filler), diverse (as filler), stands (as in "stands as"), marks (as in "marks a moment"), features (as filler verb), maintains (as filler verb), reflects (when used as "reflects broader X"), genuine, genuinely (as authentication boosters — see Sentence Structure), subsequently, hence, henceforth, heretofore, hitherto, undoubtedly, undeniably, indeed (as paragraph opener or confirmation filler), specifically (as filler), generally (as filler), alternatively (as transition), invariably, inherently, quintessential, quintessentially, veritable, deceptive, deceptively (especially "deceptively simple"), conducive to, commensurate with, akin to, tantamount to, purview, embodies, represents (as copula-replacement), constitutes (as copula-replacement)

**Frequency note — 2025-2026 vintage (current highest-signal tells):**

Corpus studies (Juzek 2024, Kobak 2024, Liang 2025) show these words are *still rising* in AI output even after the public learned about "delve" and "tapestry": **significant, additionally, crucial, effectively, comprehensive, enhance, capabilities, valuable, align, advancements**. Earlier vintage words (delve, tapestry, intricate) have been edited out by aware AI users — these haven't yet. They are the most reliably discriminating words in 2026. All are already in Tier 1 above; flagging here so you know which words to scrub first in a quick-pass review.

**Quantified vocabulary (rate vs 2020 baseline, PubMed corpus, Juzek 2024):**

| Word | 2024 rate increase |
|---|---|
| delves | 6697% |
| showcasing | 1396% |
| delve | 1375% |
| boasts | 918% |
| underscores | 904% |
| comprehending | 899% |
| intricacies | 773% |
| surpassing | 667% |
| intricate | 611% |
| underscoring | 537% |
| garnered | 437% |
| showcases | 422% |
| emphasising | 397% |
| underscore | 391% |
| realm | 381% |
| surpasses | 368% |
| groundbreaking | 330% |
| advancements | 278% |
| aligns | 267% |

Use the table to recognise which words are doing the heaviest signalling. If a single paragraph contains two or more, the AI signal is near-certain regardless of what else is in it.

**Spatial-abstraction nouns (banned when used metaphorically):**

layers, levels, dimensions, planes, axes, vectors, surface, depths. AI loves to abstract concrete observations into rule-shaped geometry: "this applies at multiple layers", "operates across dimensions", "the deeper level". Same problem as "landscape" — turning specifics into a tidy abstraction. If you mean "in two places," say two places. If you mean "in code and in process," say that.

**Banned phrases:**

- "it's important to note that" / "it's worth noting/mentioning"
- "in today's [adjective] world/landscape/era"
- "in the ever-evolving [noun]"
- "in an era of/where"
- "at its core"
- "let's dive/delve into"
- "plays a crucial/vital/significant role"
- "a testament to"
- "the [noun] landscape"
- "navigate the complexities of"
- "a nuanced understanding of"
- "serves as a" (when you mean "is")
- "the intersection of X and Y"
- "fosters a sense of"
- "underscores the importance of"
- "as we move forward"
- "in conclusion" / "in summary" / "overall," (as a paragraph opener)
- "Whether you're..."
- "from a broader perspective"
- "it could be argued that"
- "represents a broader trend"
- "signals a fundamental shift"
- "solid foundation"
- "track record"
- "strong collaborator"
- "no discussion would be complete without"
- "this is particularly relevant"
- "offers valuable insights/perspectives"
- "gain insights into"
- "from [X] to [Y]" (false spectrum, e.g., "from intimate gatherings to global movements")
- "here's the thing"
- "let's break down"
- "stands as a testament"
- "paving the way for"
- "sheds light on"
- "reflects broader [noun]"
- "indelible mark"
- "enduring legacy"
- "I hope this helps"
- "what's your take?" (as a closer)
- "both are true" / "both can be true" (reconciliation move — see Sentence Structure)
- "the real X is Y" / "the actual X is Y" / "the underlying X is Y"
- "what looks like X is actually Y"
- "what this means is" / "what we're really talking about is"
- "X explains both" / "X explains the rest" / "that explains why"
- "the same principle applies" / "the same X applies at" / "at multiple layers/levels"
- "addresses two related symptoms" / "two interconnected issues" / "two related problems"
- "make sense?" / "does that track?" / "right?" (as closers)
- "look," / "honestly," / "I'll be honest" / "to be honest" (as openers)
- "three things matter here:" / "two patterns emerge:" / "here's what's actually happening:" (pronouncement openers)
- "picture this:" / "imagine for a moment"
- "the gap is" / "the gap isn't" (when followed by an abstract reveal)
- "the question isn't X. It's Y." (diagnostic two-sentence — see Sentence Structure)
- "X are real" / "X is real" / "both paths are real" (existence-as-validation closer)
- "a genuine X" / "is a genuine X, not a Y" (authentication move, often paired with negation)
- "direction of travel" / "line of sight" / "north star" (metaphorical) / "operating rhythm" / "shift left" / "raise the bar" / "table stakes" (corporate-consulting tropes — see Editing Pass)
- "how it lands" / "how that lands" / "lands well" / "the message landed" (coaching-speak for "what people thought" — just say what people thought)

**Opener templates (banned):**

- "Have you ever wondered..." / "Ever noticed how..." (curiosity hook)
- "Let's be honest," / "I'll be honest with you," / "To be real with you," / "Truth be told," / "Real talk," (candor opener — performative honesty)
- "Here's the deal." / "Here's the kicker." / "Here's where it gets interesting." / "Here's what most people miss." / "Here's the truth:" (reveal setup variants)
- "Most people believe X. They're wrong." / "Conventional wisdom says X. The data says Y." (contrarian opener)
- "Studies show that..." / "Recent research suggests..." / "Recent data indicates..." / "According to industry data..." (uncited statistic opener — see Vague attribution)
- "If you've ever struggled with X, you know..." (empathy opener)
- "I used to think X. I was wrong." / "For years, I believed X." (confession opener)
- "The window for X is closing." / "Time is running out on X." (urgency frame)
- "The more you try to X, the less Y you get." / "X is harder than it looks. And it's about to get harder." (paradox opener)
- "Stop doing X. Start doing Y." (direct imperative opener)
- "Imagine a world where..." / "Now imagine..." / "Fast forward five years..." (imagine-a-world futurism)
- "In a world where X..." (world-state opener)
- "Let that sink in." / "Take a moment to consider X." (stop-and-think filler)
- "This study aims to..." (academic-AI opener)
- "I am writing to express my interest in..." (cover-letter AI opener — see Genre tells)
- "I hope this email finds you well" / "I hope you are doing well" / "Thank you for reaching out" (email AI openers — see Genre tells)

**Reveal / diagnostic templates (banned):**

- "The X? A Y." (self-posed question-answer fragment pair: "The result? A complete transformation.")
- "But what does X really mean?" (rhetorical-question reveal)
- "The reality is X." / "The truth is X." / "Here's the truth:" (reality-is reveal)
- "The truth is simple:" / "It's actually quite simple:" / "The answer is straightforward:" (simple-truth assertion)
- "Look closer and you'll see..." / "Beneath the surface, ..." (deeper-look reveal)
- "Deceptively simple." / "Surprisingly nuanced." / "Counterintuitively, X." (reframe-as-paradox)
- "X has been hiding in plain sight." (hidden-in-plain-sight reveal)

**Synthesis / reconciliation moves (banned):**

- "At the same time, X is also true." (at-the-same-time pivot)
- "Less is more." / "Sometimes the simplest answer is the best." (less-is-more cliché)
- "Clarity is speed." / "Specificity is the antidote to vagueness." (clarity-aphorism cadence)
- "Two things can be true at once." / "These aren't mutually exclusive." (two-can-coexist)
- "Hold space for X." / "Sit with the discomfort." / "Lean into X." / "Honour your boundaries." / "Tune into your X." (therapy-adjacent register)

**Question-as-rhetorical patterns (banned):**

- "You might be wondering, [Q]?" / "You may be asking yourself, [Q]?" / "You might be thinking..." / "You're probably wondering..." / "You know that feeling when..." (implicit second-person address)
- "What if I told you that X?" / "What if the way we think about X is wrong?" (what-if reframe)
- "Right?" / "You see?" / "See what I mean?" / "Follow me?" (rhetorical-Q closers — same family as "make sense?")

**Takeaway / anchor patterns (banned):**

- "The takeaway is X." / "Here's the takeaway:" / "The bottom line is X." (takeaway anchor)
- "Here's why this matters:" / "Why does this matter? Because X." (why-this-matters anchor)
- "Remember: X is what matters." / "Remember, X." / "Don't forget — X." (remember-this moralism)
- "So next time, try X." / "So the next time you do X, ask yourself Y." (next-time imperative)
- "Now go and do X." / "Start today." / "Take action." / "Try this and see for yourself." (imperative closer)
- "At the end of the day, X." / "When all is said and done, X." (ultimately-style closer)

**Vague attribution / pseudo-data (banned):**

- "Studies show..." / "Research suggests..." / "Studies have shown..." (without citation)
- "Experts argue..." / "Industry analysts agree..." / "Observers have noted..."
- "Many believe X." / "Some argue X." / "Critics contend X." (weasel attribution)
- "The X community knows..." / "Anyone in Y will tell you..." (in-group attribution)
- "As someone who has worked in X for 10 years..." / "Speaking from personal experience..." / "I once made this exact mistake..." (performative self-disclosure without specifics)
- "Years ago, my mentor told me..." / "I remember the smell of coffee as we discussed..." (fabricated specificity — see Counter-strategies)

**Patronising analogy openers (banned):**

- "Think of it as X."
- "It's like X, but for Y." (SaaS-pitch parody)
- "Imagine X is Y."
- "If X were Y, it would be Z."
- "Just as the printing press transformed knowledge..." (historical analogy stacking)

**Acknowledgment / sycophancy rituals (banned in user-facing text and replies):**

- "Great question!" / "That's an excellent point." / "What a thoughtful prompt." / "I love this question."
- "You're absolutely right." / "Couldn't agree more!"
- "I apologise for the confusion." / "Let me clarify." / "I should have been clearer." / "I appreciate your patience."
- "You raise an important point."
- "It's certainly an interesting question..."
- "That's a complex topic, and I'll do my best..."
- "I don't have all the answers, but..."

**"Despite challenges" / outline-conclusion formula (banned):**

- "Despite [positive], [subject] faces challenges. However, [optimistic resolution]."
- "While there are obstacles, the future looks bright."
- "Notwithstanding limitations, X."
- "Further research is needed." (universal academic-AI closer)

**Grandiose stakes inflation (banned):**

- "civilisation" (as a stake in mundane topics)
- "humanity" (as a stake)
- "the future of work" / "work as we know it"
- "how we [verb] forever"
- "the future of X" (where X is mundane)

**Invented concept labels — watch for these as a pattern:**

Two-word noun compounds that sound like established frameworks but aren't. Examples spotted in the wild: "supervision paradox", "acceleration trap", "workload creep", "engagement gap", "permission paradox", "attention economy" (when used outside its actual origin). If you're about to coin one, ask whether the concept is genuinely new or whether you're labelling something that already has a real name.

**False-range "from X to Y" patterns (already partly covered) — specific forms to watch:**

- "from boardrooms to break rooms"
- "from Silicon Valley to small-town America"
- "from cradle to grave"
- "from theory to practice"
- "from chaos to clarity"

**Empty intensifiers (delete on sight):**

fundamentally, dramatically, deeply, essentially, truly, significantly, remarkably, particularly, incredibly, exceedingly, enthusiastically, flawlessly, consistently, strategically, meticulously, seamlessly, lucidly, innovatively, compellingly, impressively

---

## Sentence Structure

### Vary sentence length — the single most measurable AI tell

AI text clusters around 15-20 word sentences with uniform complexity. Human text is spiky — a 6-word sentence followed by a 35-word one followed by a fragment. Detection tools measure the standard deviation of sentence length; low variance = AI signal. A burstiness coefficient below 0.30 is a strong AI flag.

Do this: after writing a paragraph, count the words in each sentence. If they're all within 5 words of each other, rewrite. Break a long one in two. Combine two short ones. Add a fragment. Deliberately make the rhythm uneven.

### Kill participial phrases

AI uses present participle constructions (-ing) at 2-5x the human rate. The pattern: tacking an "-ing" clause onto a sentence to inject shallow analysis.

Bad: "The team released the update, addressing several long-standing issues."
Bad: "She presented the findings, highlighting key areas for improvement."
Bad: "...reflecting broader societal trends"
Bad: "...underscoring its role as a dynamic hub"

Fix: just say what happened. Two sentences. Or restructure.

Good: "The team released the update. It fixed several long-standing issues."
Good: "She presented the findings and pointed to areas for improvement."

Also kill sentence-opening gerunds used as transitions: "Building on this,", "Leveraging these insights,", "Moving forward,". These are filler.

### Break parallel structure sometimes

AI compulsively balances clauses. Three adjectives in a row. Three bullet points of equal length. Perfectly mirrored "not only X but also Y" constructions. Humans don't write with that level of symmetry.

If you have three parallel items, make one longer than the others. Or drop it to two. Or four. Imperfect is human.

### Avoid the "not just X, but Y" construction

One of the strongest single AI tells. All forms:
- "It's not just X, it's Y"
- "It's not about X, it's about Y"
- "Rather than A, we should focus on B"
- "This isn't X — it's Y"
- "Not only...but also"

Just say what the thing is. You don't need to define it by negation first.

### Kill the two-sentence diagnostic

Same disease as "not X, it's Y" but split across two sentences, which makes it slip past the obvious check. Setup sentence states what the thing is *not*. Reveal sentence states what it *actually is*. Often the reveal pairs two abstract nouns.

Bad: "The gap is not authorisation. It's communication and execution."
Bad: "The question isn't whether to ship. It's when."
Bad: "This isn't a technology problem. It's a people problem."
Bad: "The bug isn't in the parser. It's in the assumption underneath it."

Fix: state the observation directly. If you genuinely need to rule something out, do it in one sentence with a comma, not two with the dramatic reveal.

Good: "The gap is in communication and execution."
Good: "We need to decide when to ship, not whether."

### Reject the "both are true" synthesis

AI's reflex when two claims compete is to validate both and offer its own higher-order frame that unifies them. This reads as wise. It is not. It is the model refusing to commit.

Bad: "Both are true. The communication gap explains both."
Bad: "Both views have merit. The deeper issue is X."
Bad: "Both can be right. What matters is the framing."

Fix: pick one. If both genuinely matter, say which one matters more and why. If one is wrong, say so. "Both are true" almost never adds information — it gestures at sophistication while ducking the call.

### Kill the em-dash triadic interrupter

The single most stylised AI sentence shape: a subject, em-dash, three parallel adjectives or short phrases, em-dash, predicate. It combines three tics in one move — em-dashes, the rule of three, and abstract framing.

Bad: "The same principle — explicit, accountable, no silent absorption — applies at two layers."
Bad: "Good leadership — clear, consistent, present — earns trust over time."
Bad: "The architecture — modular, typed, observable — handles this naturally."

Fix: drop the interrupter entirely and put the three items in a sentence of their own, or pick the one that actually matters. If you keep the triplet, lose the em-dashes and the abstract subject.

Good: "Be explicit, be accountable, and don't absorb things silently. That principle applies in two places: how we talk about work, and how we execute it."

### Stop authenticating your own claims

AI vouches for itself. When it senses a reader might dismiss something as hypothetical or rhetorical, it adds a credibility marker: *real*, *genuine*, *actual*, *true*. The marker doesn't add information — it just labels the claim as one the writer means seriously. A human would either state the thing plainly or back it with a specific example.

Bad: "Two paths are real."
Bad: "This is a genuine first option, not a fallback."
Bad: "These are real concerns, not edge cases."
Bad: "The risk is actual, not theoretical."

Fix: drop the marker. If the claim needs support, give a specific example or consequence instead.

Good: "Two paths." (and then describe them)
Good: "This is a first option. If A is unavailable, we ship B with no degradation."
Good: "We've hit this in production twice this quarter."

The "genuine X, not Y" form is especially worth flagging — it stacks authentication onto negation, hitting two AI tics at once.

### Don't reach for spatial abstraction

When you find yourself writing "layers", "levels", "dimensions", "axes", "planes" or "vectors" metaphorically, stop and name the actual things. AI uses these nouns to make ordinary observations sound rule-shaped.

Bad: "This needs to be addressed at multiple layers."
Bad: "There are two dimensions to this problem."
Bad: "The issue operates on several axes."

Fix: name the layers. "We need to fix the API contract and the UI copy." "There's a billing question and a permissions question."

### Avoid nominalization

AI turns verbs into nouns at 1.5-2x the human rate, creating prose that is information-dense but rhythmically dead. "The implementation of the system" instead of "implementing the system" or better, "we implemented the system." Use the verb form.

### Watch for inverted sentence structure

AI fronts objects or predicates for false emphasis. Read each sentence and check: is the subject-verb-object order natural, or has it been rearranged to sound more "writerly"? If a simpler ordering says the same thing, use it.

### Anaphora abuse

Repeating the same sentence opening across consecutive sentences. AI uses this compulsively where humans use it sparingly for genuine rhetorical effect.

Bad: "It's about clarity. It's about purpose. It's about momentum."
Bad: "We need to think differently. We need to act faster. We need to commit harder."
Bad: "Stop overthinking. Stop overplanning. Stop overpromising."

Fix: state the point once and move on. If you genuinely want anaphora (Churchill's "we shall fight" — one of two or three per career), use it once per document, not as a default cadence.

### Kill the "Not X. Not Y. Just Z." countdown

Three-step dramatic negation. Variant of "not just X but Y" and very common in marketing AI.

Bad: "Not a tool. Not a platform. A revolution."
Bad: "Not faster. Not cheaper. Smarter."
Bad: "Not just code. Not just architecture. Engineering."

Fix: state what the thing is. If you want contrast, do it in one sentence, once.

### Kill the "The X? A Y." self-Q&A fragment

Two-fragment sentence pair where a noun-phrase question precedes a noun-phrase answer.

Bad: "The result? A complete transformation."
Bad: "The catch? There isn't one."
Bad: "Their secret? Consistency."

Fix: drop the rhetorical question. "The result is a complete transformation." Or better: describe the result.

### Don't disguise a list as prose

Numbered or labelled points dressed up as continuous sentences. AI uses this to avoid bullets while keeping the listicle structure.

Bad: "The first thing to know is X. The second thing is Y. The third thing is Z."
Bad: "First, X. Second, Y. Third, Z."
Bad: "There are three reasons for this. One: X. Two: Y. Three: Z."

Fix: if it's actually a list, use a list. If it's prose, let the ideas connect through content rather than enumeration. "First/second/third" is a tell either way.

### Stop replacing "is" with "serves as"

AI replaces plain copulas ("is", "are") with structural verbs that sound more writerly: *serves as, stands as, marks, represents, features, offers, constitutes, embodies, reflects*. Corpus studies show "is/are" usage dropped over 10% in AI-influenced text — the dodge is one of the most reliable structural tells.

Bad: "Clarity serves as the foundation of effective writing."
Bad: "The meeting marks a turning point."
Bad: "This decision represents our commitment to quality."
Bad: "Our team embodies the values of the organisation."

Fix: use "is" or restructure into a verb that actually says what happened.

Good: "Clarity is the foundation of effective writing."
Good: "We turned a corner at the meeting."
Good: "We chose quality." / "We're committed to quality, and this proves it."

### Stop the bold-term colon-explanation list

Every bullet starts with a bolded word or phrase, then colon, then explanation. The single most-recognised AI list-formatting tell across detector blogs.

Bad:
- **Clarity:** The foundation of effective communication.
- **Brevity:** Saying more with fewer words.
- **Specificity:** The antidote to vagueness.

Fix: if the list genuinely needs labels, use plain text without bold. If labels add nothing, drop them and write the items as full sentences. Always-bolded list items are the formatting equivalent of an em-dash interrupter — once you see the pattern, the document reads as machine output.

### Don't stack magic adverbs

Faux-precision adverbs piled together: *quietly, deeply, fundamentally, remarkably, arguably, genuinely, carefully, deliberately, consistently*. Two in a paragraph is suspicious; three is diagnostic.

Bad: "It quietly transforms how we deeply think about what fundamentally matters."

Fix: cut all of them, then add one back only if its meaning genuinely changes the sentence.

### Don't inflate the stakes

AI scales mundane topics to civilisational significance — the launch of a feature becomes "how we relate to technology itself". Watch for: *civilisation, humanity, the future of work, how we [verb] forever, this changes everything*.

Bad: "This isn't about a new feature. It's about how we relate to technology itself."
Bad: "This is bigger than any one team. It's a referendum on how we work."

Fix: write at the actual scale of the thing.

### Don't fake vulnerability

Performative self-awareness that risks nothing and reveals nothing. The "flaw" is always a humblebrag.

Bad: "I'll admit it — I'm a perfectionist."
Bad: "If I'm being honest, I sometimes care too much."
Bad: "My biggest weakness? Probably that I get too invested."

Fix: don't include the admission unless it's a real flaw with concrete consequences. "I once shipped the wrong API key to a prod env. I've been paranoid about secrets ever since."

### Don't stack historical analogies

Rapid-fire listing of historical events for false authority. The classic AI sentence: three civilisation-scale comparisons concluding "X will do the same."

Bad: "Just as the printing press transformed knowledge, the steam engine transformed industry, and the internet transformed communication, AI will transform business."

Fix: pick one analogy if you need one. Use it specifically — what does the analogy genuinely buy you? Most of the time, drop it and state the claim.

### Don't smuggle data in with vague attribution

Invoking studies or experts without citation. This is both bad sourcing and an AI tell.

Bad: "Recent studies suggest..."
Bad: "A survey found that..."
Bad: "Research from leading institutions shows..."
Bad: "Experts argue..."

Fix: name the study, the year, the finding. Or drop the false-evidence framing and state your actual view.

---

## Punctuation

### Em dashes — use 1-2 per page, maximum

AI uses em dashes at 10x+ the rate of human writing. This is the most persistent formatting tell across all models, resistant to prompting and fine-tuning. AI uses em dashes formulaically — as drama — where humans would use commas.

Replace with: periods (start a new sentence), commas, parentheses, colons, or restructure the sentence entirely. If an em dash is the best choice, use it, but only once or twice in a document.

### Semicolons — almost never

AI joins clauses with semicolons where a period works better. Use a semicolon only when you'd genuinely pause mid-thought in speech. In most professional documents, periods are better.

### Colons — watch the setup-payoff pattern

AI loves "Here's the thing:" followed by the reveal. One per document is fine. Three is a pattern.

### Ellipses — use them

Humans trail off. AI rarely does. An occasional ellipsis is a natural human tell that AI almost never produces.

### Exclamation marks — sparingly but not never

AI either overuses them (especially in enthusiastic modes) or avoids them entirely. Humans use them occasionally and inconsistently. One or two in a longer piece is natural.

### Smart quotes and curly apostrophes

AI defaults to typographer's curly quotes (`U+201C / U+201D` for double, `U+2018 / U+2019` for single) where humans default to straight ASCII quotes (`U+0022`, `U+0027`) in casual writing — emails, chat, code comments, commits, internal docs. If your editor is silently converting straight to curly, turn it off. Curly quotes in an otherwise casual document are an AI tell.

When curly is *correct* (publication-grade typesetting), use it deliberately. When in doubt, straight.

### En dashes for ranges

AI uses the proper en dash (`U+2013`) for ranges — "pages 1–10", "2020–2025" — more consistently than humans, who normally type a hyphen. Same logic as curly quotes: only use the en dash when you're typesetting; otherwise a hyphen is what you'd actually type.

### Horizontal ellipsis character

AI uses the single-character horizontal ellipsis (`U+2026`) where humans type three periods (`...`). Three periods are what you'd actually type — use those.

### Unicode arrows in prose

`→`, `⟶`, `↑`, `↓` appearing in prose is an AI tell. Humans either type `->` or describe in words. Reserve Unicode arrows for diagrams, equations, or formal notation.

### Don't bold every key term

The "every named concept is in bold" pattern is one of the strongest AI formatting tells. Bolding is signal — every-other-noun bolding means nothing is signal.

Bad: "The **product manager** must define the **roadmap** in collaboration with the **stakeholders** while balancing **technical debt** against **velocity**."

Fix: bold a term once on its first introduction if it genuinely needs emphasis. Then stop.

### Don't backtick ordinary nouns

AI extends the convention of code-formatting filenames and variables (`like-this`) to ordinary nouns. `The team` should not be in backticks. Reserve them for code, filenames, command flags, and literal identifiers.

### Don't combine bold and italic for "extra emphasis"

`***bold italic***` is almost never natural in human prose. If you need that much emphasis, restructure the sentence.

### Bullet style consistency is suspicious

AI is rigorously consistent: always `-`, or always `*`, with the same indentation everywhere. Humans mix styles, change conventions mid-document, occasionally indent inconsistently. Don't manufacture sloppiness, but don't read perfect consistency as evidence of human authorship either.

### Don't use zero-width characters

Some AI-evasion guides suggest inserting zero-width spaces (`U+200B`), zero-width joiners (`U+200D`), or narrow no-break spaces (`U+202F`) to fool detectors. Originality.ai's 2025 analysis showed this doesn't actually work — modern detectors strip them in pre-processing. They're now a counter-tell: if a document contains zero-width characters, that itself is evidence of AI generation by a user who tried to evade detection.

### Heading levels and thematic breaks

- AI skips heading levels predictably — `H1 → H3` (no `H2`), `H2 → H4`. The skip is always by exactly one. Humans skip irregularly.
- AI uses thematic breaks (`---`) before headings even where the heading alone would be enough. Reserve `---` for genuine document-level transitions.

---

## Document Structure

### Vary paragraph length

AI paragraphs cluster around the same length with the same internal structure: topic sentence, evidence, conclusion. Human writing has one-sentence paragraphs for emphasis, long dense paragraphs for context, and mid-length ones for everything else.

Aim for at least a 3:1 ratio between your longest and shortest paragraphs in any piece. If any three consecutive paragraphs are roughly the same length, break the pattern.

### Let sections be unequal

AI distributes content into 3-5 body sections of near-identical length, each following the same internal template. If one idea deserves 600 words and another deserves 80, honour that. Merge small points into a single paragraph instead of inflating them into full sections.

### Break the rule-of-three default

AI compulsively uses triadic structures — three examples, three adjectives, three bullets. A single tricolon is fine. Three back-to-back tricolons is a pattern. Use two examples, or four, or one extended example. When you catch yourself writing three parallel items, ask whether you genuinely have three points or whether three just felt like the "right" number.

### Don't cover everything

AI tries to be comprehensive. It addresses every angle, every counterpoint, every qualification. Humans choose what matters and skip the rest. Pick the 3-4 things that matter most and go deep on those.

### Cut transitions

AI overuses formal connectors: "Furthermore," "Moreover," "Additionally," "In addition," "Consequently," "However." Humans let ideas connect through content, not signposts. If the next paragraph follows logically, you don't need a transition word. Just start it.

If you must transition, prefer short ones: "And," "But," "So," "Still," "Also." The formal connectors read as academic at best, AI at worst.

### Don't announce your structure

Delete structural announcements like "First, we will examine... Next, we will consider... Finally, we will address..." Let readers discover the structure through the argument itself. Topic sentences are fine sometimes, but not in every paragraph. Never end a section with a sentence that restates what the section just said.

### Don't restate the opening at the end

AI conclusions mirror introductions — restating the thesis, recapping each point in order. Your conclusion must go somewhere your introduction did not. Introduce a new implication, a remaining tension, or a question that emerged. Never recap your body paragraphs in order.

Never open a conclusion with "Overall," "In conclusion," "In summary." Just stop when you're done.

### Skip the scene-setting opener

Never open with "In today's...", "In an era of...", "In the rapidly evolving...", "Throughout history...", "As we stand at the crossroads of...". Start with what you actually want to say.

### Prefer prose over lists

AI defaults to bullet points and numbered lists for almost any enumerable content. Default to prose. Use a list only when the items genuinely need to be scanned independently — steps in a process, specifications, reference tables. If you could read the list items as a paragraph and they'd flow naturally, write them as a paragraph.

### Abolish compulsive summarisation

Summaries are for genuinely complex or lengthy material where the reader needs re-orientation. In a piece under 2,000 words, you almost certainly don't need one. If your "summary" sentence communicates nothing the preceding paragraph didn't already make clear, delete it.

### Avoid the "What is X? / Why does X matter? / How does X work?" SEO template

Universal blog-AI template. The shape itself is the tell — H1 noun phrase, then "What is X?", "Why does X matter?", "How does X work?", "Best practices for X", "Conclusion". If your document's headings could be generated from a template, they should be rewritten to match the actual structure of your argument.

### Don't recap at every level

AI nests "what I'm going to tell you / what I'm telling you / what I just told you" at the document, section, and paragraph levels. Fractal summaries.

If you've already said it, don't say it again at the end of the section. And don't restate it again at the end of the document.

### No self-summary openers

Don't open with "In this article, we will explore...", "This document covers...", "By the end of this post, you will...". Start with the actual content. The reader can see how long the document is.

### Don't repeat one point ten ways

AI fills space by restating the same single argument in different framings. If your second paragraph is the first paragraph in different words, cut it. If your fifth example is the same example as the second, cut it.

### Watch for verbatim duplication

A specific failure mode in long-form AI output: the same sentence or paragraph appearing twice, sometimes hundreds of words apart. Always re-read the full document end-to-end before shipping.

### Title-case heading abuse

Headings in title case ("The Power Of Strategic Thinking") instead of sentence case ("The power of strategic thinking") read as machine-generated. Use sentence case for headings unless you have a specific reason not to.

### Don't standardise "Key Takeaways" boxes

Callout boxes at the top or bottom restating the body content are an SEO-AI signature. Either the box says something the body doesn't (in which case why is it in a box?), or it duplicates the body (in which case cut it).

### Don't announce a list then summarise it after

Bad: paragraph says "Here are five reasons..." → list of five reasons → paragraph after says "These five reasons demonstrate that..." The closing summary is always redundant when the list is right above.

---

## Tone and Voice

### Direct, conversational, Australian

Open sections with punchy, direct statements (not essay-style lead-ins). Avoid consulting jargon and capabilities-list register. "Heaps good" is the brand identity — use it sparingly and deliberately.

### Argue, don't explain

AI over-explains and under-argues. It defines terms, provides context, spells out implications, but rarely makes a claim and defends it. Human writing takes positions.

### Don't hedge obvious claims

AI hedges everything because it avoids falsifiable statements. "It could be argued that...", "generally speaking...", "to some extent..." Cut these. If you believe something, say it. If you don't believe it enough to state it plainly, ask whether it belongs in the document at all.

AI uses "suggest" as its dominant attribution verb; humans use "argue." This reflects a deeper pattern: AI hedges toward diplomatic non-commitment while human text takes actual positions.

### Don't balance artificially

AI presents all perspectives as equal. If the evidence points one way, say so. The "While X is true, Y is also important" template appearing paragraph after paragraph is a dead giveaway. Take a side.

### Show emotional range

AI maintains the same neutral-to-optimistic tone regardless of subject gravity. A piece about layoffs shouldn't read with the same emotional register as a piece about product launches. Humans hold opposing feelings simultaneously — loving something and being frustrated by it, believing in a cause while doubting its execution. AI resolves contradictions; humans live in them.

Include irritation, ambivalence, dark humour, resignation, and enthusiasm where they're genuine. Not everything is "exciting" or "fascinating."

### Write like you'd talk about it

The difference between AI writing about someone and a person writing about themselves is ownership. The human version has a point of view. It risks being wrong. It sounds like someone who actually did the work.

### Include things AI wouldn't say

Specific memories. Concrete details only you'd know. What actually went wrong. What you learned the hard way. Opinions you hold that not everyone agrees with. Sentence fragments for emphasis. The occasional short, blunt sentence.

AI says "a recent experience" where a human says "Tuesday's board meeting where we debated pricing for 90 minutes." AI says "many companies are adopting" where a human names three specific companies and what they did differently. Specificity is the deepest dividing line between human and AI text.

### Stop telling the reader what things represent

AI compulsively tells you what things mean rather than simply stating facts. "This stands as a testament to..." "This reflects broader trends in..." "This underscores the importance of..." Just state the fact. If it's significant, the reader will see that.

### Stop diagnosing

A close cousin: the fake-insight reveal. "The real problem is X." "What's actually happening is Y." "X explains the rest." This reads as the writer cutting through to truth. It is the model padding an observation with the *shape* of insight. If the observation is sharp, it doesn't need announcing as the real one. Just state it.

Bad: "What's really going on here is a misalignment between teams."
Bad: "The actual issue is that nobody owns the queue."
Bad: "That explains why the rollout stalled."

Good: "Nobody owns the queue."
Good: "The rollout stalled because the two teams disagreed on scope and nobody escalated."

### No apology rituals or over-acknowledgment

When replying or revising, don't open with apology. Don't recap the user's point back to them. Don't tell them they raised a good question.

Bad: "I apologise for the confusion."
Bad: "You're absolutely right, my mistake."
Bad: "Great question! Let me clarify."
Bad: "You raise an important point."

Fix: state the correction. "The bug is in line 42." "I had X wrong; it's actually Y." The acknowledgment is implicit in correcting yourself.

### No sycophancy

Don't open with praise of the user's question or input. The reader is here for the answer, not for validation of their question.

Bad: "Great question!"
Bad: "That's an excellent point."
Bad: "What a thoughtful prompt."
Bad: "I love this question."

Fix: answer. If you need a beat before the answer, restate the question in your own words. If you don't need a beat, skip it.

### Cut politeness inflation

AI stacks modal verbs and softeners where direct language would do the job: *would suggest considering, might want to think about, could be worth exploring, perhaps you could*. One layer of hedging is fine. Three is corporate-AI.

Bad: "You might want to consider perhaps exploring whether you could possibly..."

Fix: state the recommendation. "Try X." If you're uncertain, say so once: "I'd try X first."

### Drop pseudo-humility

Hedged enthusiasm and false modesty: "It's certainly an interesting question..." / "That's a complex topic, and I'll do my best..." / "I don't have all the answers, but..."

Fix: just answer. Acknowledge a gap when one is real, not when it's a defensive habit.

### No moralising closers

Don't end a list or section with a "remember:" line, a moral, or a lesson. The reader can extract the point themselves.

Bad: "Remember: clarity matters more than cleverness."
Bad: "Don't forget — the simplest answer is often the right one."
Bad: "The lesson? Consistency wins."

Fix: stop when the content stops.

### No imperative closers to the reader

Don't tell the reader what to do next. "So next time you face this, ask yourself..." / "Now go and do X." / "Start today." / "Take action." These are content-marketing tics.

If there's a genuine call to action (you actually need them to file a ticket, run a command, sign a PR), state it plainly. If you're just telling them to "go and apply this", cut it.

### Don't open conclusions with "Ultimately"

"Ultimately, X." / "At the end of the day, X." / "When all is said and done, X." / "The bottom line is X." These openers signal you're about to restate the thesis. If you're restating the thesis, don't. If you're saying something new, drop the opener.

### Avoid therapy and coaching register in business writing

"Hold space for X." / "Sit with the discomfort." / "Lean into X." / "Honour your boundaries." / "Tune into your X." When you find yourself using this register outside actual therapy or coaching contexts, stop. Translate to plain language: "give X room", "stay with the question", "go further into X".

### Stop the implicit second-person reading

"You might be thinking..." / "You're probably wondering..." / "You know that feeling when..." reads as the writer claiming to know the reader's internal state. Even when accurate, it's intrusive. Just state what you mean.

Bad: "You're probably wondering why this matters."
Bad: "You know that feeling when a deploy goes sideways."

Fix: write your own statement, not the reader's imagined reaction. "Here's why this matters: [reason]." "When a deploy goes sideways, X happens."

### No performative honesty markers

"To be honest," / "Honestly," / "Let me be honest," / "I'll be real with you," / "Truth be told," / "Real talk," — these prefix nothing surprising and signal performance rather than candour. Already flagged in openers; restated here as a register check.

If you're being honest, the content shows it. The marker is the giveaway.

### Show cognitive motion

AI argument progression is monotonically linear: Point A leads to Point B leads to Point C, each building cleanly on the last. No wrong turns, no moments of realisation, no reconsiderations.

Show your thinking in motion. Introduce an idea, then complicate it. Start down one path and explain why you turned back. Say "I initially thought X, but..." Human arguments meander productively; they don't march in formation.

### Earn your counterarguments

AI handles counterarguments with formulaic acknowledgment: "While some argue X, it is important to note Y." When you address a counterargument, spend enough time on it that a reader holding that view would feel represented. Then dismantle it with specificity. If your counterargument paragraph follows "While [opposing view], [dismissal]," rewrite it.

---

## Commit Messages and PR Descriptions

- Follow Conventional Commits: `<type>[optional scope]: <description>`
- Common types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`, `perf`, `build`
- Imperative mood: "Add feature" not "Added feature" or "Adds feature"
- Keep the first line under 70 characters
- Lead with what changed, then why

## Comments in Code

- Explain *why*, not *what* — the code shows what, comments explain intent
- Don't add comments that restate the code
- Use TODO/FIXME with context: `// TODO(team): migrate to v2 API after Q3 deprecation`
- Keep comments up to date — stale comments are worse than no comments

---

## Genre-specific tells

Patterns above apply across all writing. The patterns below are concentrated in specific genres — strong in their native context, but easier to miss because they read as "normal for the genre".

### Email replies

Strongest single-line tells:

- "I hope this email finds you well." / "I hope this finds you well." / "I hope you are doing well." (the dominant single email opener tell)
- "Thank you for reaching out." / "Thank you for your email regarding..."
- "Please don't hesitate to reach out."
- "Looking forward to hearing from you." (neutral but at-rate suspicious)
- "Best regards," / "Warm regards," (when context is casual)

Structural tell: rigid "Acknowledgment / Body / Next steps / Sign-off" four-part template. Even if every individual line is fine, the shape is the signal. Vary it. Skip parts. Open with the actual point sometimes.

Martin's preferred opener style is in `personal-voice.md` — warmth before business, but as a genuine reaction, not a corporate template.

### Cover letters and job applications

- "I am writing to express my interest in..." (the single most-recognised cover-letter AI opener)
- "I am excited to apply for..."
- "I believe my skills align with..." ("align" is high-signal Tier 1)
- "My passion for X drives me to..."
- "I would be thrilled to contribute to..."
- "Please find my resume attached."
- "I look forward to the opportunity to discuss..."

Structural: three paragraphs of equal length (intro / fit / closing) is itself a tell. Real cover letters have different shapes for different jobs.

### LinkedIn posts

- The "hook + three takeaways + question closer" template
- "Here are my three takeaways:"
- Emoji opener (🚀 💡 🎯) + bold claim
- Numbered emoji bullets (1️⃣ 2️⃣ 3️⃣)
- "Most people think X. They're wrong. Here's why." (contrarian-LinkedIn)
- "Quick story:" / "Real talk:" / "Hot take:" (performative casualness)
- Single-sentence-per-line throughout
- Closing engagement question: "What's your take?" / "Agree?" / "What would you add?"

The "I learned X. Here's why it matters." framing is recognised AI-LinkedIn template even when the lesson is genuine. If you have a real story, tell it with specifics that only you would know.

### Blog posts / SEO content

- "What is X? / Why does X matter? / How does X work?" template (already covered above)
- H1 = "The Ultimate Guide to X" / "Everything You Need to Know About X"
- "By the end of this post, you'll know..."
- "Let's dive in" / "Let's get started" within first 100 words
- TL;DR or Key Takeaways box at top (mechanical)
- FAQ section at bottom with too-clean Q-and-A pairs
- "Conclusion" H2 that restates the intro

### Marketing copy

- "Unlock your potential" / "Unlock the power of X"
- "Elevate your X" (brand, business, performance)
- "Revolutionise your X" / "Transform your X" / "Empower your X"
- "Drive results" / "Drive growth" / "Drive engagement"
- "End-to-end solution"
- "Best-in-class" / "World-class"
- "Game-changer" / "Game-changing"
- "Take your X to the next level"

### Documentation / technical writing

- "This document covers..." (self-summary opener)
- "By following this guide, you will be able to..."
- "The following sections will walk you through..."
- Step-by-step pattern with three sub-headings per step (Description / Steps / Notes)
- "Best practices" sub-section in every section
- "Common pitfalls" / "Troubleshooting" sub-sections with too-clean parallel structure
- Excessive `**Note:**` / `**Important:**` callouts
- Every code block sandwiched by explanatory paragraphs that just restate the code

### Code comments

- Comments that restate the code in English (`# Initialize the variable` above `let x = 0`)
- Verbose docstrings on simple functions
- Docstrings on every function regardless of size
- `# TODO: Add error handling` left as a placeholder rather than implemented

### Commit messages and PR descriptions

- "Added X" / "Updated Y" / "Fixed Z" — restates the diff without saying why
- Over-detailed PR description that just recaps the diff
- Rigid "Summary / Changes / Testing / Notes" four-section PR template applied uniformly
- Bullet points listing every file changed
- Auto-generated emoji prefixes (🐛 fix:, ✨ feat:) without team convention
- "This PR introduces..." opener

### Social media replies

- "Great point!" + paraphrase of the original
- "Couldn't agree more!" + restate
- Three emojis + statement
- Long reply on a short post (mismatched length)
- Every reply ends with a question

---

## Counter-strategies that became tells

These are evasion techniques that AI users adopted to avoid detection. Detector tools and human readers have learned to spot them, so they now signal "AI text that someone tried to clean up" rather than "human text".

### Performative typos

A typo every paragraph in otherwise polished prose. The texture is wrong — too uniform, too contained, never extending to substantive content. Real human typos are messy and cluster around fatigue, distraction, or shift-key timing.

Bad: a single-letter swap ("teh") once per paragraph, missing apostrophes ("dont", "Im"), capitalisation drops only at sentence starts.

If you make typos, leave them or fix them naturally. Don't seed them deliberately.

### Forced fragments

Short fragment sentences inserted "for rhythm" but appearing every 2-3 sentences and always punchy.

Bad: "Really." / "Period." / "Full stop." / "And that's it."

Genuine fragments arrive at the moment you'd actually use them, not on a metronome.

### Performative "actually" / "honestly" / "look"

RLHF training added these as casualness markers and they're now overrepresented. Already covered above — restated here as a counter-strategy that backfired.

### Fabricated specificity ("show don't tell" overcorrection)

AI now invents sensory details to seem grounded. They don't survive scrutiny.

Bad: "It was a crisp morning in October when..."
Bad: "I remember the smell of coffee as we discussed..."
Bad: "Years ago, my mentor told me..."

If the detail isn't real, don't include it. Specifics work because they're real, not because they're concrete.

### Deliberate sentence-length variance

AI now inserts a short sentence between longer ones to break uniformity. The short sentence reads as performative.

Bad: "Three words long sentences." appearing mechanically between paragraphs.

Vary length because the content varies, not because a checklist told you to.

### Performative self-disclosure

False personal claims to bypass detection.

Bad: "As someone who has worked in X for 10 years..."
Bad: "Speaking from personal experience..."
Bad: "I once made this exact mistake..."

When generic and unsupported by concrete detail, this is a counter-tell. Include the actual mistake, the actual year, the actual consequence — or drop the claim.

### "Sound dumb" simplification

Prompts like "write this as a college freshman" produce simplification artefacts — short sentences, basic vocabulary, but the underlying AI template remains. The simplification itself becomes a tell when the structure doesn't match the register.

### Manual em-dash scrubbing

Text with all em dashes removed but every other AI marker still present (curly quotes, structural rigidity, "serves as", bold-first bullets). The *conspicuous absence* of em dashes in otherwise polished AI-style prose has itself become detectable.

The fix isn't to scrub the em dashes — it's to fix the underlying structural patterns. If you only remove em dashes, you signal that you knew about em dashes but missed everything else.

### Zero-width character insertion

Adding `U+200B`, `U+200D`, `U+202F` between words to fool detectors. Originality.ai (2025) found this doesn't work — modern detectors strip them in pre-processing. Now a counter-tell. Don't do this.

### Humaniser tool artefacts

Text processed through humaniser tools (Walter Writes, Phrasly, GPTinf) has its own fingerprint: awkward synonym substitutions, sentence restructuring that breaks meaning, occasional grammar errors that don't match the surrounding register. If you use a humaniser, edit the output as if it were AI output — because it is, with extra steps.

---

## Era markers and vintage vocabulary

AI vocabulary shifts. Words that were near-certain tells in 2023 (`delve`, `tapestry`) are no longer the highest-signal markers in 2026 — aware users edit them out, and RLHF training has down-weighted them. The current-vintage tells are different.

Use this to prioritise what you scrub first.

### 2023 vintage (peaked, declining — still tell but lower signal)

`delve / delves / delving / delved`, `intricate`, `realm`, `showcasing`, `commendable`, `meticulous`. Sharp decline in arXiv abstracts after these became publicly recognised as tells in early 2024. Still appear in unedited AI output; gone from edited AI output.

### 2024 vintage (peaked Q1-Q2 2024, declining)

`pivotal`, `innovative`, `notable`, `versatile`, `underscore / underscores / underscoring`, `tapestry`. Decline started late 2024 after public mockery and detector tools started searching for them.

### 2025-2026 vintage (still rising — current highest-signal tells)

`significant / significantly`, `additionally`, `crucial`, `effectively`, `comprehensive`, `enhance`, `capabilities`, `valuable`, `align / aligns / aligning`, `advancements`.

These continued to rise in AI output even after AI-detection awareness became mainstream. They are the strongest current discriminators because users editing for AI tells learned to remove the 2023 vintage but didn't know about these. Per Liang et al. 2025.

### Format-level era shifts

- **2023:** structured headers and bold-term colon lists
- **2024:** em-dash overuse becomes the dominant signature
- **2025:** Unicode tells (curly quotes, en-dashes for ranges, narrow no-break space `U+202F` in GPT-o3/o4-mini)
- **2026:** structural patterns (bold-first bullets, listicle-disguised-as-prose, "What is X / Why does X matter / How does X work" template) are more reliable than individual vocabulary

### Practical implication

When scrubbing your own writing for AI tells: scrub the 2025-2026 vintage words first, then check structural patterns, then check format-level tells (em dashes, curly quotes, bold-first bullets), then check the 2023-2024 vintage as a final pass. Reversing the order does the same work but catches less.

---

## Sources for this rule

- Juzek, T. (2024). "Why Does ChatGPT Delve So Much? Exploring the Sources of Lexical Overrepresentation in Large Language Models." arXiv:2412.11385
- Kobak, D. et al. (2024). "Delving into ChatGPT usage in academic writing through excess vocabulary." arXiv:2406.07016
- Liang, W. et al. (2025). "Human-LLM Coevolution: Evidence from Academic Writing." arXiv:2502.09606
- Wikipedia: Signs of AI writing (en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- Bloomberry "AI Writing Patterns: The Complete Database" (7,400+ patterns)
- tropes.fyi
- Anthropic, OpenAI sycophancy research
- Originality.ai, Pangram, GPTZero detector blogs

A fuller research register with source URLs, corpus citations, disconfirming evidence, and contested attributions lives in the writing-style plugin source under `research/ai-tells-2026.md`. It is not installed as a rule (the SessionStart hook only installs files from `rules/`), so the relative path won't resolve from an active session. Maintainers updating these rules should consult the file directly via the plugin source — it's the provenance for the claims here.

---

## The Editing Pass

After drafting, run this checklist:

1. **Word count per sentence** — is there real variation? Any sentence under 8 words? Any over 30?
2. **Em dashes** — count them. More than 2 in the whole document? Replace most with periods or commas
3. **-ing constructions** — search for ", [verb]ing" patterns. Rewrite as direct statements
4. **Banned words** — search the document against the banned list above
5. **Paragraph lengths** — are they all roughly the same? Break the pattern
6. **Transitions** — do any paragraphs start with Furthermore/Moreover/Additionally/However? Cut the transition word or replace with something shorter
7. **The lean test** — read each sentence and drop every word you can without changing the meaning. Then do the same for phrases. Then for sentences within paragraphs
8. **The ownership test** — does this sound like someone writing about their own experience, or someone summarising? Add specifics only you'd know
9. **The conversation test** — would you actually say this out loud to a colleague? If not, rewrite it in the words you'd actually use
10. **The uniformity test** — is anything uneven? If every paragraph is the same length, every section the same depth, every example the same weight, every transition the same formality, introduce deliberate asymmetry
11. **The cognitive footprint test** — could a mind that doesn't care about any of these ideas have written this? If yes, show evidence of intellectual investment: a moment of surprise, a change in emphasis, an admission that something is harder than it looks
12. **The specificity test** — count specific details (names, dates, numbers, places, described scenarios). Fewer than 2 per 500 words in a business article is a strong AI signal
13. **The template inversion test** — identify the template your document follows, then break it at least once in a way that serves the content
14. **The rule-of-three check** — does the piece use triadic structures more than twice? Convert some to pairs or singles
15. **The "not just X, but Y" check** — search for negation-contrast patterns and rewrite as direct statements
16. **The two-sentence diagnostic check** — search for sentences ending in "is not [X]." or "isn't [X]." followed by "It's" or "It is". Rewrite as one direct statement
17. **The "both are true" check** — search for "both are true", "both can be", "both views", "both have merit". Pick one and commit
18. **The em-dash triadic check** — search for sentences with mid-sentence em-dash pairs wrapping three short items. If you find one, restructure
19. **The spatial-abstraction check** — search for "layers", "levels", "dimensions", "axes", "planes", "vectors" used metaphorically. Replace with the concrete things you mean
20. **The diagnostic-reveal check** — search for "the real X is", "what's actually", "what's really", "X explains both", "X explains the rest". Cut the announcement and keep the observation
21. **The pronouncement opener check** — search for sentences opening with "Look,", "Honestly,", "Here's what's actually", "Three things matter", "Two patterns emerge". These are AI throat-clearing — start with the point itself
22. **The authentication check** — search for "are real", "is real", "a genuine", "genuinely", "actual" (when used to vouch rather than contrast with conceptual). Drop the marker or replace with a specific example
23. **The corporate-consulting trope check** — search for "direction of travel", "line of sight", "shift left", "north star" (metaphorical), "operating rhythm", "raise the bar", "table stakes", "how it lands", "how that lands". If a real human in the team wouldn't say it out loud in a meeting, cut it
24. **The current-vintage word scrub** — search for "significant", "additionally", "crucial", "effectively", "comprehensive", "enhance", "capabilities", "valuable", "align", "advancements". These are the highest-signal 2025-2026 tells per Liang 2025. Scrub before checking older vintage
25. **The "serves as" copula check** — search for "serves as", "stands as", "marks a", "represents", "embodies", "constitutes". Replace with "is" or with a verb that says what actually happened
26. **The bold-first bullet check** — scan every bullet list. If every item starts with `**Term:**`, restructure
27. **The Unicode tell sweep** — search for curly quotes (`"`, `'`, `'`), en-dash (`–`), horizontal ellipsis (`…`), Unicode arrows (`→ ⟶`), and any zero-width characters (`U+200B`, `U+200D`, `U+202F`). Convert to ASCII equivalents (`"`, `'`, `-`, `...`, `->`) in casual writing. Leave zero-widths nowhere
28. **The "What is X / Why does X matter / How does X work" check** — if your H2 structure matches this template, rewrite the headings to match the actual structure of your argument
29. **The anaphora check** — scan for three consecutive sentences starting with the same word ("It's about X. It's about Y. It's about Z."). Pick one and drop the rest
30. **The countdown check** — search for "Not X. Not Y. Just Z." three-step negation; rewrite as a direct statement
31. **The self-Q&A check** — search for "The X? A Y." fragment pairs; restructure as a single statement
32. **The opener-template check** — search the first sentence/paragraph against the opener template list (curiosity hook, candor opener, reveal setup, contrarian opener, statistic opener, empathy opener, confession opener, urgency frame, paradox opener, imperative opener, world-state opener, imagine-a-world, picture-this, stop-and-think). If you find a match, restart the document with the actual point
33. **The pseudo-data check** — search for "studies show", "research suggests", "experts argue", "many believe". Add a real citation or cut the claim
34. **The sycophancy check** — search for "great question", "excellent point", "absolutely right", "thank you for". Cut from any non-conversational document
35. **The closer check** — search for "Ultimately,", "At the end of the day,", "The bottom line is", "Remember:", "So next time,". Cut all of them and stop the document where the content stops
36. **The historical-analogy check** — search for "just as the X transformed Y". Pick one analogy or drop them all
37. **The fabricated-specificity check** — every sensory detail and named example should be real. If you can't point to when, where, who — cut it
