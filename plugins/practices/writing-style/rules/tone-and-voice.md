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

**Highest-signal vocab to scrub first** (corpus-validated; Juzek 2024, Liang 2025):

- 2025-2026 vintage still rising (scrub first): `significant`, `additionally`, `crucial`, `effectively`, `comprehensive`, `enhance`, `capabilities`, `valuable`, `align`, `advancements`.
- Heaviest rate increases vs 2020 baseline: `delves` (+6697%), `showcasing` (+1396%), `delve` (+1375%), `boasts`, `underscores`, `intricacies`, `surpassing`, `intricate`, `garnered`, `realm`, `groundbreaking`, `aligns`.

Two or more in one paragraph = near-certain AI signal. Full table and vintage history in `research/ai-tells-2026.md` §1, §9.

**Spatial-abstraction nouns (banned when used metaphorically):**

layers, levels, dimensions, planes, axes, vectors, surface, depths. AI abstracts concrete observations into rule-shaped geometry ("operates across dimensions", "the deeper level"). Name the actual things — see Sentence Structure for fuller treatment.

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

- Curiosity hook: "Have you ever wondered..." / "Ever noticed how..."
- Candor opener: "Let's be honest," / "I'll be honest with you," / "Truth be told," / "Real talk,"
- Reveal setup: "Here's the deal." / "Here's the kicker." / "Here's what most people miss." / "Here's the truth:"
- Contrarian: "Most people believe X. They're wrong." / "Conventional wisdom says X. The data says Y."
- Uncited statistic: "Studies show that..." / "Recent research suggests..." / "According to industry data..."
- Empathy: "If you've ever struggled with X, you know..."
- Confession: "I used to think X. I was wrong." / "For years, I believed X."
- Urgency: "The window for X is closing." / "Time is running out on X."
- Paradox: "The more you try to X, the less Y you get."
- Direct imperative: "Stop doing X. Start doing Y."
- Imagine-a-world: "Imagine a world where..." / "Now imagine..." / "Fast forward five years..." / "In a world where X..."
- Stop-and-think filler: "Let that sink in." / "Take a moment to consider X."
- Academic: "This study aims to..."
- Cover letter: "I am writing to express my interest in..."
- Email: "I hope this email finds you well" / "I hope you are doing well" / "Thank you for reaching out"

**Reveal / diagnostic templates (banned):**

- Self-Q&A fragment: "The X? A Y."
- Rhetorical reveal: "But what does X really mean?"
- Reality-is: "The reality is X." / "The truth is X." / "Here's the truth:"
- Simple-truth: "The truth is simple:" / "It's actually quite simple:" / "The answer is straightforward:"
- Deeper-look: "Look closer and you'll see..." / "Beneath the surface, ..."
- Reframe-as-paradox: "Deceptively simple." / "Surprisingly nuanced." / "Counterintuitively, X."
- Hidden-in-plain-sight: "X has been hiding in plain sight."

**Synthesis / reconciliation moves (banned):**

- At-the-same-time pivot: "At the same time, X is also true."
- Less-is-more cliché: "Less is more." / "Sometimes the simplest answer is the best."
- Clarity-aphorism: "Clarity is speed." / "Specificity is the antidote to vagueness."
- Two-can-coexist: "Two things can be true at once." / "These aren't mutually exclusive."
- Therapy register: "Hold space for X." / "Sit with the discomfort." / "Lean into X." / "Honour your boundaries." / "Tune into your X."

**Question-as-rhetorical patterns (banned):**

- Implicit second-person: "You might be wondering, [Q]?" / "You might be thinking..." / "You're probably wondering..." / "You know that feeling when..."
- What-if reframe: "What if I told you that X?" / "What if the way we think about X is wrong?"
- Rhetorical-Q closers: "Right?" / "You see?" / "See what I mean?" / "Follow me?"

**Takeaway / anchor patterns (banned):**

- Takeaway anchor: "The takeaway is X." / "Here's the takeaway:" / "The bottom line is X."
- Why-this-matters: "Here's why this matters:" / "Why does this matter? Because X."
- Remember-this moralism: "Remember: X is what matters." / "Remember, X." / "Don't forget — X."
- Next-time imperative: "So next time, try X." / "So the next time you do X, ask yourself Y."
- Imperative closer: "Now go and do X." / "Start today." / "Take action." / "Try this and see for yourself."
- Ultimately-style closer: "At the end of the day, X." / "When all is said and done, X."

**Vague attribution / pseudo-data (banned):**

- "Studies show..." / "Research suggests..." / "Studies have shown..." (uncited)
- "Experts argue..." / "Industry analysts agree..." / "Observers have noted..."
- "Many believe X." / "Some argue X." / "Critics contend X." (weasel attribution)
- "The X community knows..." / "Anyone in Y will tell you..." (in-group)
- "As someone who has worked in X for 10 years..." / "Speaking from personal experience..." (performative self-disclosure without specifics)
- "Years ago, my mentor told me..." / "I remember the smell of coffee as we discussed..." (fabricated specificity)

**Patronising analogy openers (banned):** "Think of it as X." / "It's like X, but for Y." / "Imagine X is Y." / "If X were Y, it would be Z." / "Just as the printing press transformed knowledge..." (historical analogy stacking).

**Acknowledgment / sycophancy rituals (banned in user-facing text and replies):** "Great question!" / "That's an excellent point." / "What a thoughtful prompt." / "I love this question." / "You're absolutely right." / "Couldn't agree more!" / "I apologise for the confusion." / "Let me clarify." / "I should have been clearer." / "I appreciate your patience." / "You raise an important point." / "It's certainly an interesting question..." / "That's a complex topic, and I'll do my best..." / "I don't have all the answers, but..."

**"Despite challenges" / outline-conclusion formula (banned):** "Despite [positive], [subject] faces challenges. However, [optimistic resolution]." / "While there are obstacles, the future looks bright." / "Notwithstanding limitations, X." / "Further research is needed." (universal academic-AI closer).

**Grandiose stakes inflation (banned):** "civilisation" / "humanity" as stakes in mundane topics, "the future of work" / "work as we know it", "how we [verb] forever", "the future of X" where X is mundane.

**Invented concept labels:** two-word noun compounds that sound like established frameworks but aren't ("supervision paradox", "acceleration trap", "engagement gap", "permission paradox"). Before coining, check whether the concept already has a real name.

**False-range "from X to Y" patterns:** "from boardrooms to break rooms", "from Silicon Valley to small-town America", "from cradle to grave", "from theory to practice", "from chaos to clarity".

**Empty intensifiers (delete on sight):**

fundamentally, dramatically, deeply, essentially, truly, significantly, remarkably, particularly, incredibly, exceedingly, enthusiastically, flawlessly, consistently, strategically, meticulously, seamlessly, lucidly, innovatively, compellingly, impressively

---

## Sentence Structure

### Vary sentence length — the single most measurable AI tell

AI clusters around 15-20 word sentences with uniform complexity; humans go spiky (6 words, then 35, then a fragment). Burstiness <0.30 is a strong AI flag.

After writing a paragraph, count words per sentence. If all within 5 words of each other, rewrite — break a long one, combine two short, add a fragment.

### Kill participial phrases

AI tacks "-ing" clauses onto sentences to inject shallow analysis at 2-5x the human rate.

Bad: "The team released the update, addressing several long-standing issues."
Fix: two sentences, or restructure. "The team released the update. It fixed several long-standing issues."

Also kill sentence-opening gerund transitions: "Building on this,", "Leveraging these insights,", "Moving forward,".

### Break parallel structure sometimes

AI compulsively balances clauses — three adjectives in a row, three equal-length bullets, perfectly mirrored "not only X but also Y." If you have three parallel items, make one longer, drop to two, or go to four.

### Avoid the "not just X, but Y" construction

One of the strongest single AI tells. Forms: "It's not just X, it's Y" / "It's not about X, it's about Y" / "Rather than A, focus on B" / "This isn't X — it's Y" / "Not only...but also". Just say what the thing is.

### Kill the two-sentence diagnostic

Same disease as "not X, it's Y" but split across two sentences. Setup states what it's *not*; reveal states what it *is*, often pairing two abstract nouns.

Bad: "The gap is not authorisation. It's communication and execution."
Fix: state the observation directly in one sentence. "The gap is in communication and execution."

### Reject the "both are true" synthesis

AI's reflex when two claims compete: validate both and offer a higher-order frame that unifies them. Reads as wise; is actually refusing to commit.

Bad: "Both are true. The communication gap explains both."
Fix: pick one. If both genuinely matter, say which matters more and why.

### Kill the em-dash triadic interrupter

Subject, em-dash, three parallel adjectives, em-dash, predicate. Combines three tics in one — em-dashes, rule of three, abstract framing.

Bad: "The same principle — explicit, accountable, no silent absorption — applies at two layers."
Fix: drop the interrupter. Put the three items in their own sentence, or pick the one that matters.

### Stop authenticating your own claims

AI vouches for itself with *real*, *genuine*, *actual*, *true* — credibility markers that add no information.

Bad: "Two paths are real." / "This is a genuine first option, not a fallback."
Fix: drop the marker. If the claim needs support, give a specific example or consequence.

The "genuine X, not Y" form stacks authentication onto negation — two tics at once.

### Don't reach for spatial abstraction

"Layers", "levels", "dimensions", "axes", "planes", "vectors" used metaphorically make ordinary observations sound rule-shaped.

Bad: "This needs to be addressed at multiple layers."
Fix: name the actual things. "We need to fix the API contract and the UI copy."

### Avoid nominalization

AI turns verbs into nouns at 1.5-2x the human rate, creating prose that is information-dense but rhythmically dead. "The implementation of the system" instead of "implementing the system" or better, "we implemented the system." Use the verb form.

### Watch for inverted sentence structure

AI fronts objects or predicates for false emphasis. Read each sentence and check: is the subject-verb-object order natural, or has it been rearranged to sound more "writerly"? If a simpler ordering says the same thing, use it.

### Anaphora abuse

Repeating the same sentence opening across consecutive sentences. AI does this compulsively; humans reserve it for genuine rhetorical effect.

Bad: "It's about clarity. It's about purpose. It's about momentum."
Fix: state the point once and move on. Reserve anaphora for once per document, not as default cadence.

### Kill the "Not X. Not Y. Just Z." countdown

Three-step dramatic negation. Marketing-AI staple.

Bad: "Not a tool. Not a platform. A revolution."
Fix: state what the thing is. Contrast once in one sentence if at all.

### Kill the "The X? A Y." self-Q&A fragment

Noun-phrase question, noun-phrase answer.

Bad: "The result? A complete transformation."
Fix: drop the rhetorical question. "The result is a complete transformation." Better: describe it.

### Don't disguise a list as prose

Numbered/labelled points dressed up as continuous sentences to avoid bullets while keeping listicle structure.

Bad: "The first thing to know is X. The second thing is Y. The third thing is Z."
Fix: if it's a list, use a list. If it's prose, let ideas connect through content. "First/second/third" is a tell either way.

### Stop replacing "is" with "serves as"

AI swaps plain copulas for structural verbs that sound more writerly: *serves as, stands as, marks, represents, features, offers, constitutes, embodies, reflects*. Corpus studies show "is/are" usage dropped 10%+ in AI-influenced text.

Bad: "Clarity serves as the foundation of effective writing."
Good: "Clarity is the foundation of effective writing."

Or restructure to a verb that says what happened: "The meeting marks a turning point" → "We turned a corner at the meeting."

### Stop the bold-term colon-explanation list

Every bullet starts `**Term:** explanation`. The single most-recognised AI list-formatting tell across detector blogs.

Bad:
- **Clarity:** The foundation of effective communication.
- **Brevity:** Saying more with fewer words.

Fix: if labels are needed, use plain text without bold. If labels add nothing, drop them and write full sentences.

### Don't stack magic adverbs

Faux-precision adverbs piled together: *quietly, deeply, fundamentally, remarkably, arguably, genuinely, carefully, deliberately, consistently*. Two in a paragraph is suspicious; three is diagnostic.

Bad: "It quietly transforms how we deeply think about what fundamentally matters."

Fix: cut all of them, then add one back only if its meaning genuinely changes the sentence.

### Don't inflate the stakes

AI scales mundane topics to civilisational significance. Watch for: *civilisation, humanity, the future of work, how we [verb] forever, this changes everything*.

Bad: "This isn't about a new feature. It's about how we relate to technology itself."
Fix: write at the actual scale of the thing.

### Don't fake vulnerability

Performative self-awareness that risks nothing. The "flaw" is always a humblebrag.

Bad: "I'll admit it — I'm a perfectionist." / "My biggest weakness? Probably that I get too invested."
Fix: omit the admission unless it's a real flaw with concrete consequences. "I once shipped the wrong API key to a prod env. I've been paranoid about secrets ever since."

### Don't stack historical analogies

Three civilisation-scale comparisons concluding "X will do the same" is the classic AI sentence.

Bad: "Just as the printing press transformed knowledge, the steam engine transformed industry, and the internet transformed communication, AI will transform business."
Fix: pick one analogy if you need one. Most of the time, drop it and state the claim.

### Don't smuggle data in with vague attribution

Invoking studies or experts without citation. Bad sourcing and AI tell.

Bad: "Recent studies suggest..." / "Research from leading institutions shows..." / "Experts argue..."
Fix: name the study, year, finding. Or drop the false-evidence framing.

---

## Punctuation

### Em dashes — use 1-2 per page, maximum

AI uses em dashes at 10x+ the human rate. The most persistent formatting tell across all models, resistant to prompting and fine-tuning. Replace with periods, commas, parentheses, colons, or restructure.

### Semicolons — almost never

AI joins clauses with semicolons where a period works better. Use only when you'd genuinely pause mid-thought in speech.

### Colons — watch the setup-payoff pattern

AI loves "Here's the thing:" followed by the reveal. One per document is fine. Three is a pattern.

### Ellipses — use them

Humans trail off. AI rarely does. An occasional ellipsis is a natural human tell.

### Exclamation marks — sparingly but not never

AI either overuses or avoids them. One or two in a longer piece is natural.

### Smart quotes and curly apostrophes

AI defaults to curly quotes (`U+201C/201D`, `U+2018/2019`); humans type straight ASCII (`"`, `'`) in casual writing. Turn off auto-conversion. Curly quotes in an otherwise casual document are an AI tell. Use curly deliberately only for typesetting.

### En dashes for ranges

AI uses the proper en dash (`U+2013`) for ranges — "pages 1–10" — more consistently than humans, who type a hyphen. Only use en dashes when typesetting.

### Horizontal ellipsis character

AI uses `U+2026` where humans type `...`. Use three periods.

### Unicode arrows in prose

`→`, `⟶`, `↑`, `↓` in prose is an AI tell. Type `->` or describe in words. Reserve Unicode arrows for diagrams.

### Don't bold every key term

The "every named concept is in bold" pattern is one of the strongest AI formatting tells. Bold a term once on first introduction if it genuinely needs emphasis. Then stop.

Bad: "The **product manager** must define the **roadmap** in collaboration with the **stakeholders** while balancing **technical debt** against **velocity**."

### Don't backtick ordinary nouns

Reserve backticks for code, filenames, command flags, and literal identifiers. Not for ordinary nouns.

### Don't combine bold and italic for "extra emphasis"

`***bold italic***` is almost never natural. If you need that much emphasis, restructure.

### Bullet style consistency is suspicious

AI is rigorously consistent (always `-` or always `*`, same indentation everywhere). Humans mix styles occasionally. Don't manufacture sloppiness, but perfect consistency isn't evidence of human authorship either.

### Don't use zero-width characters

`U+200B`, `U+200D`, `U+202F` insertion to fool detectors doesn't work (Originality.ai 2025). Modern detectors strip them in pre-processing. Now a counter-tell.

### Heading levels and thematic breaks

- AI skips heading levels by exactly one (`H1 → H3`, `H2 → H4`). Humans skip irregularly.
- AI uses `---` before headings where the heading alone would be enough. Reserve `---` for genuine document-level transitions.

---

## Document Structure

### Vary paragraph length

AI paragraphs cluster around the same length with the same internal structure (topic / evidence / conclusion). Aim for 3:1 ratio between longest and shortest in any piece. Break the pattern if three consecutive paragraphs are similar length.

### Let sections be unequal

AI distributes content into 3-5 body sections of near-identical length and template. If one idea deserves 600 words and another 80, honour that. Merge small points into a paragraph instead of inflating into a section.

### Break the rule-of-three default

AI compulsively uses triadic structures. A single tricolon is fine; three back-to-back is a pattern. Use two, four, or one extended example. Ask whether you genuinely have three points or three just felt right.

### Don't cover everything

Pick the 3-4 things that matter most and go deep. AI's reflex is to address every angle, counterpoint, and qualification; humans skip what doesn't earn its place.

### Cut transitions

Drop "Furthermore," "Moreover," "Additionally," "In addition," "Consequently," "However." If the next paragraph follows logically, you don't need a transition word. Prefer "And," "But," "So," "Still," "Also" if you must.

### Don't announce your structure

Delete "First, we will examine... Next, we will consider... Finally..." Let readers discover structure through argument. Never end a section by restating what the section just said.

### Don't restate the opening at the end

AI conclusions mirror introductions. Your conclusion must go somewhere your introduction did not — a new implication, remaining tension, or question that emerged. Never open with "Overall," "In conclusion," "In summary." Stop when you're done.

### Skip the scene-setting opener

Never open with "In today's...", "In an era of...", "In the rapidly evolving...", "Throughout history...", "As we stand at the crossroads of..." Start with what you actually want to say.

### Prefer prose over lists

AI defaults to bullets for anything enumerable. Default to prose. Use a list only when items need to be scanned independently (steps, specs, reference tables). If you could read them as a paragraph that flows naturally, write the paragraph.

### Abolish compulsive summarisation

Summaries are for genuinely complex/long material. Under 2,000 words you almost certainly don't need one. If the summary sentence communicates nothing the preceding paragraph didn't, delete it.

### Avoid the "What is X / Why does X matter / How does X work" SEO template

Universal blog-AI template. The shape is the tell. If your headings could be generated from a template, rewrite them to match the actual structure of your argument.

### Don't recap at every level

AI nests "what I'm going to tell you / what I'm telling you / what I just told you" at document, section, and paragraph levels. Fractal summaries. Don't restate at the end of a section, and don't restate again at the end of the document.

### No self-summary openers

Don't open with "In this article, we will explore...", "This document covers...", "By the end of this post, you will..." The reader can see how long it is.

### Don't repeat one point ten ways

If your second paragraph is the first in different words, cut it. If your fifth example is the same as the second, cut it.

### Watch for verbatim duplication

A failure mode in long-form AI output: the same sentence or paragraph appearing twice, sometimes hundreds of words apart. Re-read end-to-end before shipping.

### Title-case heading abuse

Headings in title case ("The Power Of Strategic Thinking") read as machine-generated. Use sentence case ("The power of strategic thinking") unless you have a specific reason not to.

### Don't standardise "Key Takeaways" boxes

Callout boxes at top/bottom restating body content are an SEO-AI signature. If it says something the body doesn't, why is it in a box? If it duplicates the body, cut it.

### Don't announce a list then summarise it after

"Here are five reasons..." → list → "These five reasons demonstrate that..." The closing summary is always redundant when the list is right above.

---

## Tone and Voice

### Direct, conversational, Australian

Open sections with punchy, direct statements (not essay-style lead-ins). Avoid consulting jargon and capabilities-list register. "Heaps good" is the brand identity — use it sparingly and deliberately.

### Argue, don't explain

AI over-explains and under-argues. It defines terms, provides context, spells out implications, but rarely makes a claim and defends it. Human writing takes positions.

### Don't hedge obvious claims

Cut "It could be argued that...", "generally speaking...", "to some extent..." If you believe it, say it. If you don't believe it enough to state plainly, ask whether it belongs in the document.

AI's dominant attribution verb is "suggest"; humans use "argue" — a deeper pattern of diplomatic non-commitment.

### Don't balance artificially

If evidence points one way, say so. "While X is true, Y is also important" paragraph after paragraph is a dead giveaway. Take a side.

### Show emotional range

AI keeps the same neutral-to-optimistic register regardless of subject gravity. Layoffs shouldn't read like product launches. Include irritation, ambivalence, dark humour, resignation. Not everything is "exciting" or "fascinating."

### Write like you'd talk about it

The difference between AI writing about someone and a person writing about themselves is ownership — point of view, willingness to be wrong, sounding like someone who did the work.

### Include things AI wouldn't say

Specific memories. Details only you'd know. What actually went wrong. Opinions not everyone agrees with. AI says "a recent experience"; a human says "Tuesday's board meeting where we debated pricing for 90 minutes." Specificity is the deepest divide.

### Stop telling the reader what things represent

AI compulsively explains what things mean: "This stands as a testament to..." / "This reflects broader trends in..." / "This underscores the importance of..." State the fact. If significant, the reader sees that.

### Stop diagnosing

The fake-insight reveal: "The real problem is X." "What's actually happening is Y." "X explains the rest." Reads as cutting through to truth; is the *shape* of insight without the substance. If the observation is sharp, it doesn't need announcing.

Bad: "What's really going on here is a misalignment between teams."
Good: "Nobody owns the queue."

### No apology rituals or over-acknowledgment

When replying or revising, don't open with apology, recap the user's point, or tell them they raised a good question.

Bad: "I apologise for the confusion." / "You're absolutely right, my mistake." / "You raise an important point."
Fix: state the correction. The acknowledgment is implicit in correcting yourself.

### No sycophancy

Don't open with praise of the user's question. The reader is here for the answer.

Bad: "Great question!" / "That's an excellent point." / "What a thoughtful prompt."
Fix: answer. If you need a beat, restate the question in your own words.

### Cut politeness inflation

AI stacks modal softeners: *would suggest considering, might want to think about, could be worth exploring, perhaps you could*. One layer of hedging is fine; three is corporate-AI.

Bad: "You might want to consider perhaps exploring whether you could possibly..."
Fix: state it. "Try X." Uncertain? Say so once: "I'd try X first."

### Drop pseudo-humility

Hedged enthusiasm and false modesty: "It's certainly an interesting question..." / "That's a complex topic, and I'll do my best..." / "I don't have all the answers, but..."

Fix: answer. Acknowledge a gap only when real, not as defensive habit.

### No moralising closers

Don't end with "remember:", a moral, or a lesson. "Remember: clarity matters more than cleverness." / "The lesson? Consistency wins." Stop when the content stops.

### No imperative closers to the reader

"So next time..." / "Now go and do X." / "Start today." / "Take action." are content-marketing tics. Cut unless there's a genuine call to action (file a ticket, run a command).

### Don't open conclusions with "Ultimately"

"Ultimately, X." / "At the end of the day, X." / "The bottom line is X." signal thesis-restatement. If restating, don't. If saying something new, drop the opener.

### Avoid therapy and coaching register in business writing

"Hold space for X." / "Sit with the discomfort." / "Lean into X." / "Honour your boundaries." Outside therapy/coaching, translate to plain language.

### Stop the implicit second-person reading

"You might be thinking..." / "You're probably wondering..." / "You know that feeling when..." claims the reader's internal state. State your own meaning instead.

### No performative honesty markers

"To be honest," / "Honestly," / "Truth be told," / "Real talk," prefix nothing surprising. If you're being honest, the content shows it.

### Show cognitive motion

AI progression is linear (A → B → C, no wrong turns). Introduce an idea, complicate it. "I initially thought X, but..." Human arguments meander productively.

### Earn your counterarguments

AI uses "While some argue X, it is important to note Y." Spend enough time that a holder feels represented, then dismantle with specificity. "While [opposing view], [dismissal]" is a rewrite.

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

## Reference areas in the research file

When working in a specific genre or doing a deliberate scrub, consult `research/ai-tells-2026.md`:

- §7 — Genre-specific tells (email, cover letters, LinkedIn, blog/SEO, marketing, docs, code comments, commits, social).
- §9 — Era markers and vintage vocabulary (2023 → 2024 → 2025-2026 scrub order).
- §10 — Counter-strategies that became tells (performative typos, fabricated specificity, em-dash scrubbing, zero-widths, humaniser tools).

General rules above apply across all genres.

---

## Sources for this rule

Primary sources: Juzek 2024 (arXiv:2412.11385), Kobak et al. 2024 (arXiv:2406.07016), Liang et al. 2025 (arXiv:2502.09606), Wikipedia "Signs of AI writing", Bloomberry "AI Writing Patterns" database, tropes.fyi, Anthropic/OpenAI sycophancy research, Originality.ai/Pangram/GPTZero detector blogs.

Full research register with source URLs, corpus citations, disconfirming evidence, and contested attributions: `research/ai-tells-2026.md` in the writing-style plugin. Read from plugin source (when working in the turtlestack repo) or from the per-version cache at `~/.claude/plugins/cache/turtlestack/writing-style/<version>/research/ai-tells-2026.md` (when working from an installed copy). The SessionStart hook only installs `rules/` into `.claude/rules/`, so the research file isn't pulled into an active session.

---

## The Editing Pass

After drafting, run this checklist:

1. **Sentence length variation** — any sentence under 8 words? Any over 30? If all within 5 words of each other, rewrite.
2. **Em dashes** — more than 2 in the document? Replace most with periods or commas.
3. **-ing constructions** — search `, [verb]ing`. Rewrite as direct statements.
4. **Banned words** — search the document against the banned list above.
5. **Paragraph lengths** — break the pattern if all similar.
6. **Transitions** — paragraphs starting with Furthermore/Moreover/Additionally/However? Cut.
7. **The lean test** — drop every word/phrase/sentence you can without changing meaning.
8. **The ownership test** — does this sound like someone who did the work? Add specifics only you'd know.
9. **The conversation test** — would you say this aloud to a colleague? If not, rewrite.
10. **The uniformity test** — if every paragraph/section/example is the same weight, introduce asymmetry.
11. **The cognitive footprint test** — show evidence of intellectual investment (surprise, emphasis shift, admission of difficulty).
12. **The specificity test** — fewer than 2 specific details per 500 words is a strong AI signal.
13. **The template inversion test** — break the template you're following at least once.
14. **Rule-of-three check** — triadic structures more than twice? Convert some to pairs or singles.
15. **"Not just X, but Y"** — rewrite negation-contrast as direct statements.
16. **Two-sentence diagnostic** — "is not [X]." followed by "It's [Y]." → one direct sentence.
17. **"Both are true" check** — pick one and commit.
18. **Em-dash triadic interrupter** — mid-sentence em-dash pair wrapping three items → restructure.
19. **Spatial abstraction** — "layers", "levels", "dimensions", "axes" used metaphorically → name the concrete things.
20. **Diagnostic-reveal** — "the real X is", "what's actually", "what's really", "X explains both" → cut announcement, keep observation.
21. **Pronouncement opener** — "Look,", "Honestly,", "Here's what's actually", "Three things matter" → start with the point.
22. **Authentication** — "are real", "is real", "a genuine", "genuinely", "actual" (when vouching) → drop marker or give specific example.
23. **Corporate-consulting tropes** — "direction of travel", "line of sight", "north star", "shift left", "table stakes", "how it lands" → cut if your team wouldn't say it aloud.
24. **Current-vintage word scrub** — "significant", "additionally", "crucial", "effectively", "comprehensive", "enhance", "capabilities", "valuable", "align", "advancements" (highest-signal 2025-2026 tells, Liang 2025). Scrub before older vintage.
25. **"Serves as" copula check** — "serves as", "stands as", "marks a", "represents", "embodies", "constitutes" → "is" or a verb that says what happened.
26. **Bold-first bullets** — every item starts with `**Term:**`? Restructure.
27. **Unicode tell sweep** — curly quotes (`"`, `'`), en-dash (`–`), horizontal ellipsis (`…`), Unicode arrows (`→`), zero-widths (`U+200B/200D/202F`) → ASCII equivalents in casual writing. Zero-widths: nowhere.
28. **"What is X / Why does X matter / How does X work"** — if your H2s match this template, rewrite to match your actual argument.
29. **Anaphora** — three consecutive sentences starting the same way → pick one.
30. **Countdown** — "Not X. Not Y. Just Z." → direct statement.
31. **Self-Q&A** — "The X? A Y." → single statement.
32. **Opener-template check** — match the first paragraph against the opener-templates list above. If matched, restart with the actual point.
33. **Pseudo-data** — "studies show", "research suggests", "experts argue" → add a real citation or cut.
34. **Sycophancy** — "great question", "excellent point", "absolutely right" → cut from non-conversational text.
35. **Closer** — "Ultimately,", "At the end of the day,", "The bottom line is", "Remember:", "So next time," → cut. Stop where content stops.
36. **Historical analogy** — "just as the X transformed Y" → pick one or drop all.
37. **Fabricated specificity** — every sensory detail and named example must be real. Can't point to when/where/who? Cut.
