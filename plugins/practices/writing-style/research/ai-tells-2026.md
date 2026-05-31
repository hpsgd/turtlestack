# AI Writing Tells — Comprehensive Research 2026

> **What this is:** the source research that informed the AI tell coverage in `../rules/tone-and-voice.md`. Not a rule itself — not installed via the SessionStart hook. Reference material for anyone maintaining the rule file: source URLs, corpus citations, disconfirming evidence, contested attributions, and patterns that didn't make the cut for the rule file (mostly model-specific markers in Section 8 which are noisy and migrate quickly).
>
> If you're updating the rule file, start here to check provenance. If a claim in the rule file feels shaky, search this document for the source.

## Method and scope

Research conducted 2026-05-31. Scope: identify AI writing tells from open-source literature (academic papers, detector tool blogs, writer critique posts, Reddit threads, Wikipedia "Signs of AI writing") that are NOT already covered in the existing rule file at `plugins/practices/writing-style/rules/tone-and-voice.md`.

Already covered (excluded from this research scope): Tier 1/2 banned vocabulary listed in the brief, the "not just X but Y" construction, em-dash overuse, -ing participial phrases, rule-of-three, uniform sentence/paragraph length, formal transitions, scene-setting openers, and the major tonal patterns (hedging, both-sides balance, flat register).

Search method: WebSearch + WebFetch across Wikipedia, detector vendor blogs (Originality.ai, GPTZero, Pangram, Copyleaks), academic preprints (arXiv, ACL Anthology), writer critique posts (Substack, Medium), Reddit threads (r/ChatGPT, r/ClaudeAI, r/writing), and LinkedIn critique posts.

Confidence ratings:
- **HIGH** — multiple independent sources (3+), at least one with corpus-based or empirical evidence
- **MEDIUM** — 2-3 sources, mostly qualitative
- **LOW** — single source or anecdotal
- **[UNVERIFIED]** — claim could not be corroborated

---

## Section 1: Vocabulary additions (not yet flagged in rule file)

### Tier 1 candidates (high-confidence single-word tells with corpus evidence)

These appear at 5x-60x+ human baseline rates in published corpus studies (Kobak et al. 2024 on PubMed; Liang et al. 2024 on arXiv; Juzek 2024 LLM lexical overrepresentation paper).

| Word | Evidence | Confidence |
|---|---|---|
| **align / aligns / aligning** | 267% spike 2020→2024 in PubMed abstracts (Juzek 2024) | HIGH |
| **advancements** | 278% spike in PubMed (Juzek 2024) | HIGH |
| **surpass / surpassing / surpasses** | 367-667% spikes (Juzek 2024); flagged by Walter Writes 2026 | HIGH |
| **emphasizing / emphasises** | 397% spike (Juzek 2024); flagged in Wikipedia Signs of AI 2024-2025 list | HIGH |
| **highlighting / highlights** | Wikipedia 2024-2025 AI vocabulary list; flagged across multiple detector blogs | HIGH |
| **fostering** | Wikipedia 2024-2025 list; flagged in HumanizeThisAI patterns | HIGH |
| **comprehending** | 899% spike (Juzek 2024) | HIGH |
| **boasts** | 918% spike (Juzek 2024); listed in Wikipedia "promotional language" tells | HIGH |
| **garner / garnered** | 437% spike (Juzek 2024); listed in PageOn.AI 2025 | HIGH |
| **enhance / enhances / enhancing** | Wikipedia 2024-2025 list; Plus AI, Matrix Group, Embryo all flag | HIGH |
| **explore / explores / exploring** | PageOn.AI 2025; flagged as overused "delve" substitute post-2024 | HIGH |
| **scalable** | SynkrLAB inventory; corporate-jargon AI tell | HIGH |
| **mission-critical** | SynkrLAB inventory | MEDIUM |
| **next-generation** | SynkrLAB inventory; pairs with "cutting-edge" | MEDIUM |
| **turnkey** | SynkrLAB; corporate-jargon AI tell | MEDIUM |
| **best-in-class / world-class** | SynkrLAB; flagged in Plus AI 2025 | MEDIUM |
| **impactful** | SynkrLAB; flagged in Embryo and Walter Writes | HIGH |
| **versatile** | SynkrLAB; appears as filler adjective | MEDIUM |
| **exemplary** | SynkrLAB | MEDIUM |
| **agile** (as filler adjective, not the methodology) | SynkrLAB | MEDIUM |
| **catalyze / catalyse** | SynkrLAB action-verb list | MEDIUM |
| **amplify** | SynkrLAB action-verb list; common Claude tell per Reddit threads | MEDIUM |
| **pioneer / pioneering** | SynkrLAB action-verb list | MEDIUM |
| **maximize / maximise** | "Maximize efficiency / potential" — 15-phrases Medium article; SynkrLAB | HIGH |
| **optimise / optimize** | SynkrLAB; flagged in HumanizeThisAI | HIGH |
| **drive / delivers / deliver** (as filler verbs in business contexts) | SynkrLAB; Plus AI | MEDIUM |
| **engage / engagement** (as filler) | SynkrLAB | MEDIUM |
| **execute / execution** (corporate sense) | SynkrLAB | LOW |
| **undertake** | SynkrLAB | MEDIUM |
| **champion** (as verb) | SynkrLAB | MEDIUM |
| **interplay** | Wikipedia 2023-2024 list; explicitly flagged as "AI vocabulary" | HIGH |
| **valuable** (as filler adjective) | Wikipedia 2023-2024 list | MEDIUM |
| **profound / profoundly** | "Implications are profound" — God of Prompt 500-list | MEDIUM |
| **iceberg** (metaphor) | SynkrLAB metaphor list | LOW |
| **mosaic / tapestry / constellation / prism / canvas / spectrum / labyrinth / symphony** (when used as metaphor for ideas/data) | SynkrLAB metaphor inventory | MEDIUM |
| **wizardry / wizard** | SynkrLAB sci-fi metaphor list | LOW |
| **revitalize / revitalise** | LinkedIn critiques 2025 | LOW |
| **reimagine** | "reimagine X for the modern Y" — listed in Walter Writes | MEDIUM |
| **reshape** | LinkedIn critique posts 2025; very common Claude tell | MEDIUM |
| **redefine** | LinkedIn critique posts 2025; appears with reshape/reimagine | MEDIUM |
| **unleash** | SynkrLAB; "unleash the power" — God of Prompt | HIGH |
| **unlock** (as verb) | 15-phrases article; God of Prompt; "unlock the potential" | HIGH |

### Tier 2 candidates (contextual flags)

| Word | Context | Source |
|---|---|---|
| **subsequently** | Connective overuse | God of Prompt |
| **hence** | Connective overuse | SynkrLAB |
| **thus** | Connective overuse — already in Tier 2 list, confirmed | Multiple |
| **henceforth / heretofore / hitherto** | Pseudo-formal connectives | LinkedIn critiques |
| **undoubtedly / undeniably** | Hedged certainty | SynkrLAB |
| **indeed** | Confirmation filler — "Indeed" as paragraph opener | God of Prompt |
| **specifically** (as filler) | God of Prompt | MEDIUM |
| **generally** (as filler) | God of Prompt | MEDIUM |
| **alternatively** | Transition overuse | God of Prompt |
| **invariably** | Pseudo-precision hedge | Walter Writes |
| **inherently** | Pseudo-precision hedge | Walter Writes |
| **quintessentially / quintessential** | Pretentious AI vocabulary | LinkedIn critiques |
| **veritable** | Pretentious AI vocabulary | LinkedIn critiques |
| **myriad of** (the construction, not just "myriad") | Multiple sources | HIGH |
| **plethora / plethora of** | Multiple sources; very common Claude tell | HIGH |
| **akin to** | Walter Writes; common in academic-flavoured AI text | MEDIUM |
| **tantamount to** | LinkedIn critiques | LOW |
| **purview** | Pseudo-formal noun | LOW |
| **nuance / nuanced** | Already in Tier 1, confirmed | n/a |
| **deceptive / deceptively** | "deceptively simple" reveal-paradox opener | MEDIUM |
| **arguably the most** | Hedged superlative | MEDIUM |
| **perhaps the most** | Hedged superlative | MEDIUM |
| **conducive to** | Walter Writes; pseudo-academic filler | LOW |
| **commensurate with** | Walter Writes; pseudo-formal | LOW |

### Spike data (Kobak et al. 2024 / Juzek 2024 — PubMed corpus, 2020 vs 2024)

Top 21 most-overrepresented words with frequency multipliers (already partly known, but the numbers are useful as evidence):

| Word | 2020 occurrences-per-million | 2024 opm | Increase |
|---|---|---|---|
| delves | 0.21 | 14.38 | **6697%** |
| delved | 0.12 | 2.90 | 2240% |
| delving | 0.12 | 2.38 | 1817% |
| showcasing | 0.59 | 8.79 | 1396% |
| delve | 0.58 | 8.50 | 1375% |
| boasts | 0.11 | 1.15 | 918% |
| underscores | 4.50 | 45.19 | 904% |
| comprehending | 0.56 | 5.58 | 899% |
| intricacies | 0.60 | 5.22 | 773% |
| surpassing | 1.37 | 10.50 | 667% |
| intricate | 6.22 | 44.22 | 611% |
| underscoring | 2.70 | 17.17 | 537% |
| garnered | 2.44 | 13.13 | 437% |
| showcases | 0.82 | 4.31 | 422% |
| emphasizing | 8.30 | 41.27 | 397% |
| underscore | 7.42 | 36.40 | 391% |
| realm | 2.25 | 10.85 | 381% |
| surpasses | 0.85 | 3.96 | 368% |
| groundbreaking | 0.87 | 3.75 | 330% |
| advancements | 12.49 | 47.17 | 278% |
| aligns | 1.55 | 5.68 | 267% |

Source: Juzek 2024, arXiv:2412.11385.


## Section 2: Phrase templates not yet covered

Categorised by function. Templates use `X / Y / Z` as variable placeholders. All flagged as HIGH-confidence unless noted, based on Bloomberry 7,400-pattern catalogue + tropes.fyi + cross-confirmation across detector blogs.

### Openers (not yet covered)

| Pattern | Example | Source |
|---|---|---|
| **Curiosity hook** | "Have you ever wondered..." / "Ever noticed how..." | Bloomberry; tropes.fyi |
| **Candor opener** | "Let's be honest," / "I'll be honest with you," | Bloomberry (ChatGPT marker) |
| **Reveal setup** | "Here's the thing." / "Here's the deal." / "Here's the kicker." / "Here's where it gets interesting." / "Here's what most people miss." | Bloomberry; tropes.fyi (ChatGPT marker) |
| **Contrarian opener** | "Most people believe X. They're wrong." / "Conventional wisdom says X. The data says Y." | Bloomberry |
| **Statistic opener** | "Studies show that X percent of..." / "Recent research suggests that..." | Bloomberry; flagged by detector blogs as low-credibility |
| **Empathy opener** | "If you've ever struggled with X, you know..." | Bloomberry |
| **Confession opener** | "I used to think X. I was wrong." / "For years, I believed X." | Bloomberry |
| **Urgency frame** | "The window for X is closing." / "Time is running out on X." | Bloomberry |
| **Paradox opener** | "The more you try to X, the less Y you get." / "X is harder than it looks. And it's about to get harder." | Bloomberry |
| **Direct imperative** | "Stop doing X. Start doing Y." | Bloomberry |
| **Definitional reveal** | "X is not just Y — it's Z." (also covered as banned not-just-X) | Bloomberry; tropes.fyi |
| **Imagine-a-world** | "Imagine a world where..." / "Picture this: ..." | tropes.fyi |
| **World-state opener** | "In a world where X..." | Bloomberry |
| **Stop and think** | "Let that sink in." / "Take a moment to consider X." | Reddit r/writing critiques 2025 |

### Reveal / diagnostic patterns (not yet covered)

| Pattern | Example | Source |
|---|---|---|
| **Self-posed rhetorical Q** | "The X? A Y." / "The question isn't X. It's Y." / "But what does X really mean?" | tropes.fyi; Bloomberry |
| **The reality-is reveal** | "The reality is X." / "The truth is X." / "Here's the truth:" | Bloomberry (Claude/ChatGPT marker) |
| **The simple-truth assertion** | "The truth is simple:" / "It's actually quite simple:" / "The answer is straightforward:" | tropes.fyi |
| **The deeper-look reveal** | "Look closer and you'll see..." / "Beneath the surface, ..." | LinkedIn critiques |
| **Reframe-as-paradox** | "Deceptively simple." / "Surprisingly nuanced." / "Counterintuitively, X." | Brief specifies; corroborated by Reddit critiques |
| **Hidden-in-plain-sight** | "X has been hiding in plain sight." | LinkedIn critiques 2025 |

### Synthesis / reconciliation moves (not yet covered)

| Pattern | Example | Source |
|---|---|---|
| **"At the same time" pivot** | "X is true. At the same time, Y is also true." | Bloomberry transition catalogue |
| **The "less is more" cliché** | "Less is more." / "Sometimes the simplest answer is the best." | Bloomberry (Claude marker) |
| **The clarity-is-speed aphorism** | "Clarity is speed." / "Specificity is the antidote to vagueness." | Bloomberry aphorism cadence |
| **The two-can-coexist** | "Two things can be true at once." / "These aren't mutually exclusive." | Reddit r/ClaudeAI threads |
| **The therapy-adjacent move** | "Hold space for X." / "Sit with the discomfort." / "Lean into X." | Bloomberry "specialised" category |

### Question-as-rhetorical patterns

| Pattern | Example | Source |
|---|---|---|
| **You-might-be-wondering** | "You might be wondering, [Q]?" / "You may be asking yourself, [Q]?" | tropes.fyi; LinkedIn critiques |
| **What-if reframe** | "What if I told you that X?" / "What if the way we think about X is wrong?" | Bloomberry hook patterns |
| **Make-sense closer** | "Make sense?" / "Does that track?" / "Follow me?" (Already partly in brief; included for completeness) | Brief |
| **Right closer** | "Right?" / "You see?" / "See what I mean?" | Reddit r/writing critiques |

### Takeaway / anchor patterns

| Pattern | Example | Source |
|---|---|---|
| **The takeaway is** | "The takeaway is X." / "Here's the takeaway:" / "The bottom line is X." | tropes.fyi; common in LinkedIn AI tells |
| **Why this matters** | "Here's why this matters:" / "Why does this matter? Because X." | tropes.fyi; LinkedIn critiques |
| **Remember-this moralism** | "Remember: X is what matters." / "Remember, X." / "Don't forget — X." | Reddit r/writing |
| **Next-time imperative** | "So next time, try X." / "So the next time you do X, ask yourself Y." | LinkedIn critiques |
| **At-its-core** | "At its core, X." / "Fundamentally, X." (already partly covered) | Multiple |

### Vague attribution / pseudo-data

| Pattern | Example | Source |
|---|---|---|
| **Studies show** | "Studies show..." / "Research suggests..." / "Recent data indicates..." (without citation) | Wikipedia Signs of AI |
| **Experts argue** | "Experts argue..." / "Industry analysts agree..." / "Observers have noted..." | Wikipedia |
| **Many believe** | "Many believe X." / "Some argue X." / "Critics contend X." | Wikipedia weasel-words list |
| **The Y community** | "The X community knows..." / "Anyone in Y will tell you..." | LinkedIn critiques |

### False-range "from X to Y" patterns (already partly covered)

The brief flags "from X to Y" generally. Specific common forms worth naming:

- "from boardrooms to break rooms"
- "from Silicon Valley to small-town America"
- "from cradle to grave"
- "from theory to practice"
- "from chaos to clarity"

Sources: tropes.fyi; LinkedIn critiques.

### "Imagine / Picture" futurism

- "Imagine a world where..."
- "Picture this:"
- "Now imagine..."
- "Fast forward five years..."

Source: tropes.fyi; Bloomberry; flagged in willfrancis.com Claude-prompt guide.

### Patronising analogy openers ("Think of it as")

- "Think of it as X."
- "It's like X, but for Y." (the SaaS-pitch parody pattern)
- "Imagine X is Y."
- "If X were Y, it would be Z."

Source: tropes.fyi.

### Apology / acknowledgment rituals (model-conversational)

- "Great question!"
- "That's an excellent point."
- "You're absolutely right."
- "I apologise for the confusion."
- "Let me clarify."
- "You raise an important point."

Source: Anthropic/OpenAI sycophancy discussions; Reddit r/ClaudeAI; Nautil.us Claude sycophancy piece.

### "Despite its challenges" formula

Pattern: "Despite [positive] X, [subject] faces challenges. However, [optimistic resolution]."

Example: "Despite its rapid growth, the company faces headwinds. However, its strategic positioning suggests..."

Source: Wikipedia Signs of AI (the "outline-like conclusions" pattern); tropes.fyi.

### Invented concept labels

Pattern: fabricated compound noun phrases sounding analytical. Examples from tropes.fyi:

- "supervision paradox"
- "acceleration trap"
- "workload creep"
- "engagement gap"
- "attention economy"
- "permission paradox"

Pattern marker: a noun + noun compound that sounds like a known framework but isn't.


## Section 3: Sentence structures not yet covered

### Anaphora abuse

Repeating the same sentence opening across consecutive sentences. AI does this compulsively where humans use it sparingly for rhetorical effect.

Examples (tropes.fyi):
- "It's about X. It's about Y. It's about Z."
- "We need X. We need Y. We need Z."
- "Stop doing X. Stop doing Y. Stop doing Z."

### "Not X. Not Y. Just Z." dramatic countdown

Distinct from "not just X but Y" — this is a three-step negation pattern.

Examples:
- "Not a tool. Not a platform. A revolution."
- "Not faster. Not cheaper. Smarter."

Source: tropes.fyi; LinkedIn AI tells.

### "The X? A Y." self-posed question-answer

A two-fragment sentence pair where the first is a noun-phrase question and the second is a noun-phrase answer.

Examples:
- "The result? A complete transformation."
- "The catch? There isn't one."
- "Their secret? Consistency."

Source: tropes.fyi.

### Listicle-in-a-trench-coat

Numbered or labelled points dressed as continuous prose: "The first thing to know is X. The second thing is Y. The third thing is Z." or "First, X. Second, Y. Third, Z."

Source: tropes.fyi; LinkedIn critiques.

### Short fragment paragraphs for emphasis

Single-sentence (often 3-5 word) paragraphs scattered through prose. Used as a "stylistic" move but in AI output they cluster densely and read as performative.

Example pattern (from a paragraph of normal length):
> "It's a paradigm shift.
>
> It really is."

Source: tropes.fyi ("Short Punchy Fragments"); also surfaces in willfrancis.com Claude critique.

### Bold-term colon-explanation lists

Pattern: every bullet starts with a bolded word/phrase, then colon, then explanation.

Example:
- **Clarity:** The foundation of effective communication.
- **Brevity:** Saying more with fewer words.
- **Specificity:** The antidote to vagueness.

Source: tropes.fyi ("Bold-First Bullets"); Wikipedia Signs of AI ("Inline-Header Vertical Lists").

### The "Serves As" copula dodge (already partly noted)

Replacing plain "is/are" with "serves as," "stands as," "marks," "represents," "features," "offers," "constitutes," "embodies."

Specific replacements to flag:
- "X serves as Y" → "X is Y"
- "X stands as Y" → "X is Y"
- "X represents Y" → "X is Y" or "X means Y"
- "X marks a Y" → "X is a Y"
- "X embodies Y" → "X is Y"
- "X reflects Y" → "X shows Y" (if causal) or just "X is Y"

Source: Wikipedia Signs of AI ("Avoidance of Basic Copulas"); Juzek 2024 (>10% drop in "is/are" usage flagged).

### Magic adverb stacking

Stacking adverbs that convey faux-precision: "quietly," "deeply," "fundamentally," "remarkably," "arguably," "genuinely," "carefully," "deliberately," "consistently."

Pattern: more than 2 magic adverbs in a single paragraph.

Example: "It quietly transforms how we deeply think about what fundamentally matters."

Source: tropes.fyi; Reddit r/writing.

### Grandiose stakes inflation

Inflating mundane topics to civilisational significance.

Example: "This isn't about a new feature. It's about how we relate to technology itself."

Pattern markers:
- "civilisation"
- "humanity"
- "the future of work / work as we know it"
- "how we [verb] forever"

Source: tropes.fyi.

### False vulnerability

Simulated self-awareness that reads risk-free and performative.

Pattern: confession of a "flaw" that's actually a humblebrag, or an admission that does no work.

Example: "I'll admit it — I'm a perfectionist."

Source: tropes.fyi.

### Historical analogy stacking

Rapid-fire listing of historical events/companies for false authority.

Example: "Just as the printing press transformed knowledge, the steam engine transformed industry, and the internet transformed communication, AI will transform X."

Source: tropes.fyi.

### Pseudo-data framings

Pattern: invoking studies, surveys, or data without citation.

Examples:
- "Recent studies suggest..."
- "A survey found that..."
- "Research from leading institutions shows..."
- "According to industry data..."

Source: Wikipedia Signs of AI; tropes.fyi; detector blogs.


## Section 4: Paragraph/document structural patterns

### The "What is X? / Why does X matter? / How does X work?" SEO template

Document structure: H1 noun phrase → "What is X?" H2 → "Why does X matter?" H2 → "How does X work?" H2 → "Best practices for X" H2 → "Conclusion" H2.

The shape itself is an AI tell when consistent across pieces. Source: Sight AI listicle SEO 2026; tropes.fyi composition.

### The intro-context-problem-solution-conclusion document template

Five-section structure with near-equal section lengths. AI compulsively distributes content evenly. Source: Wikipedia Signs of AI; Hastewire patterns blog.

### Listicle conventions

Pattern markers:
- Exact "Top 10" framing
- Each item: bold name + 150-200 word description + "Best for: X" tag
- Conclusion that recaps each item in order
- "Honourable mentions" subsection

Source: Sight AI listicle template; LinkedIn AI tells.

### Bold-first bullets (every bullet starts with a bolded phrase + colon)

Already covered in Section 3 but worth restating as a structural document-level tell. Source: tropes.fyi; willfrancis.com.

### Fractal summaries

"What I'm going to tell you / what I'm telling you / what I just told you" applied at every hierarchical level — document-level intro/body/conclusion AND section-level intro/body/conclusion AND paragraph-level topic/evidence/restatement. Source: tropes.fyi.

### The "one point diluted across 2000 words" pattern

Restating the same single argument 10 different ways. Source: tropes.fyi.

### Content duplication

Repeating entire sentences or paragraphs verbatim within the same piece — a specific failure mode in long-form AI output. Source: tropes.fyi.

### Pre-placed maintenance / meta-commentary

"In this article, we will explore...", "This guide covers...", "By the end of this post, you will understand..." — opening self-summarisation as a separate paragraph before the content begins. Source: Wikipedia Signs of AI; LinkedIn critiques.

### Skipping heading levels

H1 → H3 (no H2), H2 → H4 (no H3). Source: Wikipedia Signs of AI ("Skipping Heading Levels").

### Title-case heading abuse

Pattern: every main word in headings capitalised — "The Power Of Strategic Thinking" — where sentence case is more natural. Source: Wikipedia Signs of AI ("Title Case in Headings").

### Thematic-break/horizontal-rule overuse

Pattern: `---` horizontal rules separating every section. Particularly common with H2-to-H2 transitions where headings alone would be enough. Source: Wikipedia Signs of AI ("Thematic Breaks Before Headings").

### Standardised "key takeaways" / "TL;DR" boxes

Pattern: callout box at top or bottom with bulleted "key takeaways" that restate the body content. Source: detector blogs; tropes.fyi.

### Section announcement → list → summary pattern

Pattern: paragraph announces a list ("Here are five reasons..."), the list appears, then a paragraph after restating ("These five reasons demonstrate..."). The closing summary is redundant. Source: tropes.fyi; Shankar 2024 blog.

### Mirror-conclusion that restates the introduction

Already covered, but worth confirming: AI conclusions structurally mirror their introductions verbatim. The literature is consistent. Source: Hastewire; tropes.fyi.

### Listicle-disguised-as-prose

"The first thing to know is X. The second thing is Y. The third thing is Z." paragraph forms — a list pretending to be flowing text. Source: tropes.fyi ("Listicle in a Trench Coat").


## Section 5: Punctuation and typography tells

### Em dashes (U+2014)

Already covered in rule file. Confirmed and reinforced: the single most persistent typographic tell, present at ~10x human baseline rate (Shady Characters Aug 2025 analysis; Originality.ai). AI models use em dashes (Unicode U+2014) where humans would use commas, parentheses, or new sentences.

### En dashes (U+2013)

Used by AI for ranges ("pages 1–10", "2020–2025") more consistently than humans. Many humans use a hyphen for ranges; AI uses the proper en dash. Source: Originality.ai invisible-text article; Leap AI formatter docs.

### Curly / smart quotes (U+201C / U+201D / U+2018 / U+2019)

AI defaults to curly typesetters' quotes where humans default to straight ASCII quotes (U+0022, U+0027) in informal writing. Wikipedia Signs of AI explicitly flags as tell. Source: Wikipedia; Originality.ai.

### Horizontal ellipsis (U+2026)

AI uses the single-character horizontal ellipsis where humans type three periods. Source: Originality.ai; Leap AI text formatter.

### Zero-width spaces (U+200B)

Documented in detector blogs as a tell BUT — important caveat — Originality.ai analysis found "adding or removing hidden characters did NOT change the detectability of AI-generated content." Treat as suggestive, not diagnostic. Source: Originality.ai invisible-text article.

### Zero-width joiner / non-joiner (U+200D / U+200C)

Same status as U+200B — appears in AI output but not reliably so. Source: Originality.ai.

### Narrow no-break space (U+202F)

Surge in appearance in GPT-o3 and o4-mini outputs through late 2024–2025. Source: thepromptindex.com AI detection 2025; humanwritesai.com.

### Directional marks (U+200E, U+200F, U+202A–E, U+2066–2069)

Occasionally present in AI output; same caveat about reliability. Source: Originality.ai.

### Unicode arrows (→, ↑, ↓, ⟶)

AI uses Unicode arrows in prose where humans would type "->" or describe. Source: tropes.fyi; Wikipedia Signs of AI.

### Markdown asterisk-bold for emphasis on every key term

Pattern: every named concept, every key noun, every introduced term is wrapped in `**bold**` — "The **product manager** must define the **roadmap** in collaboration with the **stakeholders**." Source: Wikipedia Signs of AI; tropes.fyi.

### Markdown code-fence overuse

Pattern: short single-word terms wrapped in backticks (`` `term` ``) where italics or no formatting would be enough. Specifically common with file names, variable names, but extended to ordinary nouns. Source: detector observations.

### Title-case headings

Already covered in Section 4. Source: Wikipedia.

### Single-space after period

AI consistently uses single-space sentence spacing (the modern convention); humans split. Some older humans double-space. Single-space alone is not a tell, but if combined with other markers, worth noting. Source: shady characters and typography blogs.

### Sentence-final whitespace and trailing blank lines

AI output often has consistent trailing whitespace patterns. No strong empirical evidence, treat as LOW confidence.

### Bullet-style consistency (always `-` or always `*`)

Humans mix bullet styles. AI is rigorously consistent within and across documents. Source: tropes.fyi.

### Excessive bold + italic combined

Pattern: `***bold italic***` for "extra emphasis" — almost never natural in human prose. Source: tropes.fyi.

### Heading hierarchy without natural skips

AI nests H1 → H2 → H3 → H4 in perfect order even when the document doesn't warrant it. Conversely, when it skips, it skips by exactly one level. Source: Wikipedia ("Skipping Heading Levels").


## Section 6: Tonal and rhetorical patterns

### Apology rituals and over-acknowledgment

Pattern: opening a reply with apology for the previous turn's content.

Examples:
- "I apologise for the confusion."
- "You're absolutely right, my mistake."
- "I appreciate your patience."
- "Let me clarify."
- "I should have been clearer."

Especially common in Claude when the user pushes back. Anthropic's documented sycophancy patterns (Nautil.us; Anthropic constitution discussion) describe this as the "yes-but" pattern: agreement first, then qualification.

Source: Nautil.us "I asked Claude why it won't stop flattering me" (2026); Anthropic research blog on sycophancy.

### Over-agreement and praise

Pattern: opening with praise of the user's question or input before answering.

Examples:
- "Great question!"
- "That's an excellent point."
- "What a thoughtful prompt."
- "I love this question."

Documented across all major chat models, particularly pre-RLHF-tuned variants. Anthropic explicitly trained against this in Opus 4.6 and 4.7.

Source: Anthropic 2026 research blog "How people ask Claude for personal guidance"; Reddit r/ClaudeAI sycophancy threads.

### Politeness inflation

Pattern: using extra modal verbs and softeners where direct language would do.

Examples:
- "I would suggest considering..."
- "You might want to think about..."
- "It could be worth exploring..."
- "Perhaps you could..."

Source: Reddit r/ChatGPT critique threads; sycophancy literature.

### Pseudo-humility / hedged enthusiasm

Pattern: false modesty + hedged-enthusiasm hybrid.

Examples:
- "It's certainly an interesting question..."
- "That's a complex topic, and I'll do my best..."
- "I don't have all the answers, but..."

Source: Reddit r/ClaudeAI threads; willfrancis.com.

### Diplomatic non-commitment ("suggest" vs "argue")

Already covered in brief. Confirmed by Liang et al. 2024: AI uses "suggest" / "indicates" / "demonstrates" / "shows" as dominant attribution verbs; humans use "argue," "claim," "say." AI attribution verbs avoid committing the author to a position.

Source: Liang et al. 2024; Hastewire patterns blog.

### Listicle moralism

Pattern: closing a list with a moralising imperative.

Examples:
- "Remember: clarity matters more than cleverness."
- "Don't forget — the simplest answer is often the right one."
- "The lesson? Consistency wins."

Source: Reddit r/writing critique threads.

### Imperative closers

Pattern: closing with a direct command to the reader.

Examples:
- "So next time you face this, ask yourself..."
- "Now go and do X."
- "Start today."
- "Take action."
- "Try this and see for yourself."

Source: tropes.fyi; LinkedIn AI critique posts.

### The "Ultimately" closer

Pattern: penultimate-paragraph sentence beginning with "Ultimately" that restates the thesis.

Example: "Ultimately, the key to X is Y."

Variants:
- "At the end of the day, X."
- "When all is said and done, X."
- "The bottom line is X."

Source: Bloomberry transition catalogue; tropes.fyi signposted conclusion.

### The fake-personal "Honestly" / "Look" opener

Pattern: opening a sentence or paragraph with "Honestly," / "Look," / "Frankly," to signal directness — but the content that follows is just generic AI prose.

Examples:
- "Look, X is complicated."
- "Honestly? It's not that simple."
- "Frankly, most people get this wrong."

Especially common in Claude 4.x and ChatGPT post-2024 RLHF training that tried to inject "casualness." Counter-strategy that became a tell.

Source: Brief mentions; corroborated by Reddit r/ClaudeAI; willfrancis.com.

### Therapeutic / coaching register

Pattern: borrowing therapy vocabulary into business contexts.

Examples:
- "Hold space for X."
- "Sit with that for a moment."
- "Lean into the discomfort."
- "Honour your boundaries."
- "Tune into your X."

Source: Bloomberry specialised-register category; LinkedIn AI critique threads.

### "Show, don't tell" overcorrection

Counter-strategy that became a tell: AI now inserts specific-sounding details that read fake.

Example: "It was a Tuesday afternoon when I first realised X" (fabricated specificity).

Source: Reddit r/writing critique threads; counter-strategy discussion in detector blogs.

### Implicit second-person address

Pattern: speaking to "you" the reader as if reading their mind.

Examples:
- "You might be thinking..."
- "You're probably wondering..."
- "You know that feeling when..."

Source: tropes.fyi; LinkedIn AI critique posts.

### Performative honesty markers

Pattern: prefixing statements with honesty signifiers.

Examples:
- "To be honest,"
- "Let me be honest,"
- "I'll be real with you,"
- "Truth be told,"
- "Real talk,"

Source: Reddit r/writing critique threads; LinkedIn AI critique.


## Section 7: Genre-specific tells

### Email replies

Strong tells in email-specific contexts:

| Pattern | Status |
|---|---|
| "I hope this email finds you well" | Single most-recognised email opener AI tell |
| "I hope this finds you well" | Variant |
| "I hope you are doing well" | Variant |
| "Thank you for reaching out" | Opening of received-email reply |
| "Thank you for your email regarding..." | Formal pattern |
| "Please don't hesitate to reach out" | Closing |
| "Looking forward to hearing from you" | Closing — neutral but at-rate |
| "Best regards," (always) | Formal sign-off when context is casual |
| "Warm regards," | Sign-off |
| "Dear [Name]," + "Thank you" opener | Documented OpenAI community pattern |
| Structured into "Acknowledgment / Body / Next steps / Sign-off" | Template tell |

Source: Hacker News thread on ChatGPT email tells (35869582); LinkedIn "I hope this email finds you well" engineai post; OpenAI dev community thread 544032.

### Cover letters / job applications

| Pattern | Status |
|---|---|
| "I am writing to express my interest in..." | The single most-recognised cover-letter AI opener |
| "I am excited to apply for..." | Variant |
| "I believe my skills align with..." | "align" is a Tier-1 LLM word |
| "My passion for X drives me to..." | Inauthentic enthusiasm marker |
| "I would be thrilled to contribute to..." | Hedged enthusiasm |
| "Please find my resume attached" | Antique formal marker |
| "I look forward to the opportunity to discuss..." | Closing template |
| Three-paragraph structure (intro / fit / closing) of equal length | Structural tell |

Source: TealHQ cover letter guide 2025; MultipleChat AI cover letter 2026; Mondo cover letter article.

### LinkedIn posts

| Pattern | Status |
|---|---|
| Hook + three takeaways + question closer | The recognised AI LinkedIn template |
| "Here are my three takeaways:" | Specific phrase tell |
| Short paragraphs (1-2 lines each), heavily fragmented | Structural tell — LinkedIn algorithm favours this so humans copy, but the pattern is AI-cluster strong |
| "I learned X. Here's why it matters." | Common framing |
| Closing question to drive engagement: "What's your take?" / "Agree?" / "What would you add?" | The engagement bait closer |
| Emoji opener (🚀, 💡, 🎯) + bold claim | LinkedIn-specific AI tell |
| "Most people think X. They're wrong. Here's why." | Contrarian-LinkedIn pattern |
| Numbered emoji bullets ("1️⃣ X, 2️⃣ Y, 3️⃣ Z") | LinkedIn-specific |
| "Quick story:" / "Real talk:" / "Hot take:" openers | Performative casualness |
| Single-sentence-per-line throughout | LinkedIn-AI tell |

Source: aiunpacker.com 30 LinkedIn prompt templates; Letterdrop thought leadership prompts; LinkedIn "AI tells" critique posts.

### Blog posts / SEO content

| Pattern | Status |
|---|---|
| "What is X?" / "Why does X matter?" / "How does X work?" three-section template | Universal SEO listicle tell |
| "Top 10 X" structure | When combined with 150-200 word equal sections, an AI tell |
| H1 = "The Ultimate Guide to X" / "Everything You Need to Know About X" | Title formula |
| "By the end of this post, you'll know..." opener | Self-summary tell |
| "Let's dive in" / "Let's get started" close to top | Section transition tell |
| TL;DR or Key Takeaways box at top | When mechanical, a tell |
| "FAQ" section at bottom with predictable Q-and-A pairs | SEO-AI tell |
| "Conclusion" H2 with restated intro | Structural tell |

Source: Sight AI listicle SEO 2026; Memorable.design listicle SEO 2026; Sight AI templates 2026.

### Marketing copy

| Pattern | Status |
|---|---|
| "Unlock your potential" / "Unlock the power of X" | Top marketing-AI phrase |
| "Elevate your X" (brand, business, performance) | Top marketing-AI phrase |
| "Revolutionise your X" | Top marketing-AI phrase |
| "Transform your X" | Variant |
| "Empower your X" (team, users, customers) | Variant |
| "Drive results" / "Drive growth" / "Drive engagement" | Action-verb buzzword |
| "End-to-end solution" | Buzzword |
| "Best-in-class" / "World-class" | Self-praise tell |
| "Game-changer" / "Game-changing" | Hype marker |
| "Take your X to the next level" | Engagement cliché |

Source: SynkrLAB 310+ list; God of Prompt 500 list; LinkedIn "ChatGPT corporate jargon" post.

### Documentation / technical writing

| Pattern | Status |
|---|---|
| "This document covers..." opening self-summary | Tell |
| "By following this guide, you will be able to..." | Tell |
| "The following sections will walk you through..." | Tell |
| Step-by-step with three subheadings per step (Description / Steps / Notes) | Template tell |
| "Best practices" subsection in every section | Template tell |
| "Common pitfalls" or "Troubleshooting" subsections with too-clean parallel structure | Tell |
| Excessive use of `**Note:**` / `**Important:**` callouts | Tell |
| Every code block preceded by explanatory paragraph and followed by explanatory paragraph | Padding tell |

Source: detector blogs; Shankar AI writing blog; tropes.fyi composition.

### Academic-flavoured writing

Already heavily covered by Kobak/Juzek/Liang corpus studies. Additional tells:

| Pattern | Status |
|---|---|
| "This study aims to..." opener | Standard academic-AI tell |
| "The findings suggest..." / "The results indicate..." | Hedged attribution |
| "Further research is needed" closer | Universal AI-academic closer |
| "Notwithstanding limitations, ..." | Hedged-confidence pattern |
| Equal-length intro / methods / results / discussion sections | Structural tell |
| Citation density without specificity | Tell |

Source: Kobak et al. 2024; Juzek 2024; Liang et al. 2024.

### Code comments

| Pattern | Status |
|---|---|
| Comments that restate the code in English | Universal AI code comment tell |
| Verbose docstrings on simple functions | Tell |
| Every function has a docstring even when 1-line | Tell |
| `# Initialize the variable` (the obvious-comment pattern) | Tell |
| `# TODO: Add error handling` (left as placeholder rather than implemented) | Tell |

Source: exceeds.ai blog on AI code analysis; QWE AI Academy 2026 commit message guide.

### Commit messages / PR descriptions

| Pattern | Status |
|---|---|
| "Added X" / "Updated Y" / "Fixed Z" — what, not why | Universal AI commit tell |
| Over-detailed PR description that recaps the diff | Tell |
| "Summary / Changes / Testing / Notes" four-section PR template applied uniformly | Tell |
| Bullet points listing every file changed | Tell |
| Auto-generated emoji prefixes (🐛 fix:, ✨ feat:) without team convention | Tell |
| "This PR introduces..." opening | Tell |

Source: QWE AI Academy commit 2026; graphite blog on AI code review.

### Social media replies

| Pattern | Status |
|---|---|
| "Great point!" + paraphrase of the original post | Tell |
| "Couldn't agree more!" + restate | Tell |
| Three emojis + statement | Tell |
| Long reply on a short post (mismatched length) | Tell |
| Every reply ends with a question | Engagement-pattern tell |

Source: LinkedIn AI critique posts; Reddit r/ChatGPT discussion.


## Section 8: Model-specific tells (where the literature distinguishes)

Important caveat: model-specific attribution is contested. Models are training-data-trained on each other's outputs, so tells migrate. The list below reflects 2025–2026 literature; some tells in the "ChatGPT marker" column will be Claude markers in 12 months and vice versa.

### ChatGPT (GPT-4o through GPT-5)

Specific markers per Bloomberry, type.ai, Scientific American, and detector blogs:

| Tell | Source |
|---|---|
| "let's unpack" | Bloomberry |
| "move the needle" | Bloomberry |
| "double down on" | Bloomberry |
| "circle back" | Bloomberry; some say Gemini too |
| "here's the thing" reveal opener | Bloomberry |
| "Let's be honest" candor opener | Bloomberry |
| "blood glucose levels" + clinical-formal register | Scientific American |
| Heavy bullet points and bold-header lists | type.ai; Bloomberry |
| Collapse-into-bullet-points when asked for paragraphs (GPT-5) | every.to vibe check |
| Em dashes at very high rate | shadycharacters.co.uk |
| Performative casualness ("Look,", "Honestly,") post-RLHF | willfrancis.com |
| Tendency to start with restating the user's question | OpenAI dev community thread |

### Claude (3.5 through 4.7)

| Tell | Source |
|---|---|
| "tapestry" | Bloomberry |
| "delve" (still common despite arXiv decline) | Bloomberry |
| "nuanced" / "nuance" | Bloomberry |
| "fundamentally" | Bloomberry |
| "moreover" | Bloomberry |
| "indeed" | Bloomberry |
| "less is more" aphorism | Bloomberry |
| "the reality is" reveal | Bloomberry |
| Long-form prose preservation (4.5+) | every.to vibe check |
| "Yes-but" sycophancy pattern | Nautil.us; Anthropic 2026 research |
| Apology rituals on pushback (pre-4.6) | Anthropic 2026 research |
| Diplomatic non-commitment | Anthropic constitution discussion |
| "Honestly," / "Look," conversational injection | Brief; willfrancis.com |
| "I want to make sure I understand" prompt-back | Reddit r/ClaudeAI |
| "Happy to" sign-off and confirmation | Reddit r/ClaudeAI |
| "Two things can be true at once" synthesis | Reddit r/ClaudeAI |
| Increased mechanical formatting in 4.7 — bullets + headers for long-form | boringbot Opus 4.7 review |
| Reads "corporate" / slide-deck-flavoured in 4.7 | boringbot Opus 4.7 review |
| Literal instruction-following without inferring intent (4.7) | claudefa.st 4.7 best practices |

### Gemini

| Tell | Source |
|---|---|
| Heavy structural rigidity (claim-evidence-conclusion per paragraph) | tactiq.io; HumanizeThisAI |
| Default to numbered lists and bullets even when not asked | type.ai; contentpen.ai |
| "Sugar" / "high blood sugar" register (vs ChatGPT's "glucose") | Scientific American |
| Reads like well-organised Wikipedia entry | type.ai; tactiq.io |
| "leverage" overused | Bloomberry |
| Conversational and explanatory trigrams over formal-academic | Scientific American |
| Functional dryness over personality | tactiq.io |
| Stronger intro-body-summary at every section level | type.ai |

### Open-source models (Llama, Mistral, DeepSeek)

| Tell | Source |
|---|---|
| Motivational cadence (short claim → evidence → imperative) | Bloomberry (open-source marker) |
| Lower lexical refinement than commercial closed models | detector blogs |
| Stronger fingerprint of GPT-4 outputs in training data (distillation artefacts) | academic literature on synthetic data |
| Less RLHF-induced sycophancy in base models | Hugging Face evaluation discussions |

### DeepSeek-specific

Limited literature. Some observation:
- Tends toward longer, less-bulleted prose than GPT-5
- Distillation-related stylistic similarity to early-generation Claude

Source: getpassionfruit.com 2026 comparison.


## Section 9: Era markers and vocabulary shifts

Established empirically by Liang et al. 2025 ("Human-LLM Coevolution: Evidence from Academic Writing", arXiv:2502.09606). The arXiv-abstracts corpus shows distinct vocabulary trajectories:

### 2023 vintage (peak then sharp decline by mid-2024)

These words peaked in late 2023 and fell after being publicly identified as AI tells in early 2024:

- **delve / delves / delving / delved** — peak Nov 2023, sharp decline post-March 2024
- **intricate** — same trajectory
- **realm** — peaked, then declined
- **showcasing** — peaked Jan-March 2024, declined
- **commendable** — declined post-recognition
- **meticulous** — declined post-recognition

### 2024 vintage (peaked Q1-Q2 2024, declining)

- **pivotal** — declining
- **innovative** — declining (per Liang)
- **notable** — declining
- **versatile** — declining
- **underscore / underscores / underscoring** — late 2024 decline
- **tapestry** — Late 2024 decline (after public mockery)

### 2025-2026 vintage (still rising)

These have continued to rise even after recognition — making them the **current** highest-confidence tells:

- **significant / significantly** — continuing to grow (Liang 2025)
- **additionally** — ongoing increase
- **crucial** — sustained rise
- **effectively** — continuing growth
- **comprehensive** — maintained elevation
- **enhance** — persistent increase
- **capabilities** — ongoing rise
- **valuable** — sustained growth
- **align / aligns / aligning** — rising (per Juzek 2024 data)
- **advancements** — rising

### Independent declining signals

- **"is" / "are"** as copulas — declining trend even without explicit recognition (replaced by "serves as / stands as / marks / represents") (Liang 2025)

### Implication for current rule design

The strongest currently-discriminating words are the 2025-2026 vintage that haven't yet been broadly recognised. The early-vintage words (delve, tapestry) still appear in unedited AI output but are no longer the highest-signal tells because:

1. AI users actively edit them out
2. RLHF training has down-weighted them
3. Detector tools that searched for them have become unreliable

The 2025-2026 vintage (significant, comprehensive, enhance, align, capabilities) are more reliable because they haven't been part of the public consciousness as tells.

### Format-level era markers

- **2023:** structured headers + bold-term colon lists
- **2024:** em-dash overuse becomes the dominant signature (per shadycharacters.co.uk Aug 2025)
- **2025:** Unicode tells (curly quotes, en-dash for ranges, narrow no-break space U+202F in GPT-o3/o4-mini outputs)
- **2026:** structural patterns (the "Bold term: explanation" list, the listicle-disguised-as-prose) more reliable than vocabulary


## Section 10: Counter-strategies that became tells

### Performative typos

Pattern: introducing deliberate typos to seem human. The texture is wrong — they're too uniform, too contained, never extend to substantive content.

Examples:
- Single-letter swaps in common words ("teh" once per paragraph)
- Missing apostrophes ("dont", "Im")
- Capitalisation drops at sentence start

Evidence: Thomas Smith (March 2025) experiments found typos don't fool current detectors and create their own pattern. Minding The Campus reports college students adding typos to evade detection. Facebook post by Omar (literatureByOmar) on performative typos.

Source: medium.com/the-generator do-typos-fool-ai-detectors; Minding The Campus 2025-06-12.

### Forced fragments

Pattern: short fragment sentences inserted for "human" rhythm but appearing too consistently (every 2-3 sentences) and too punchy.

Examples:
- "Really."
- "Period."
- "Full stop."
- "And that's it."

When clustered, becomes a tell. Source: tropes.fyi; Reddit r/writing.

### Performative "actually" / "honestly" markers

The brief already flags these. Counter-strategy origin: RLHF training that tried to make models sound less formal injected these as "casualness markers" — now overrepresented in models 2024+ and detectable.

Source: willfrancis.com Claude prompts; brief.

### "Show, don't tell" fabrication

Pattern: AI inserts specific-sounding sensory details to seem grounded — but they don't survive scrutiny.

Examples:
- "It was a crisp morning in October when..." (fabricated specificity)
- "I remember the smell of coffee as we discussed..." (fake memory)
- "Years ago, my mentor told me..." (no mentor)

Source: Reddit r/writing critique threads; counter-strategy discussion in detector blogs.

### Deliberate sentence-length variance

Pattern: AI now adds one short sentence between longer ones to break uniformity. The short sentences read as performative.

Example: "Three words long sentences." appearing between paragraphs.

Source: detector blogs; arXiv:2603.23146 on AI-detection failure modes.

### "Sound dumb" prompts

Pattern: prompts like "write this as a college freshman" introduce simplification artefacts — short sentences, basic vocabulary, but the structure remains AI-template.

Source: Minding The Campus 2025; tropes.fyi.

### Manual em-dash removal

Pattern: text scrubbed of em dashes but retaining all other tells (curly quotes, structural rigidity, etc.). The conspicuous absence of em dashes in otherwise polished AI-style prose is itself becoming a counter-tell.

Source: GPTCleanup AI; shady characters analysis.

### Zero-width-character insertion

Pattern: adding U+200B between words to fool detectors. Originality.ai (2025) found this DOESN'T affect detectability for capable detectors. It's now a counter-tell rather than a counter-strategy.

Source: Originality.ai invisible-text article; gptcleanuptools.com.

### "Humaniser" tool artifacts

Pattern: text processed through humaniser tools (Walter Writes, Phrasly, GPTinf) has its own fingerprint — synonym substitutions that don't quite fit, awkward sentence-restructuring, occasional grammar errors.

Source: phrasly.ai GPTinf review; humanizethisai.com.

### Performative self-disclosure

Pattern: false personal claims to bypass detection.

Examples:
- "As someone who has worked in X for 10 years..."
- "Speaking from personal experience..."
- "I once made this exact mistake..."

When generic and unsupported by concrete detail, a counter-tell. Source: tropes.fyi; LinkedIn AI critique posts.


## Sources register

### Academic / empirical (highest weight)

| Source | Coverage | URL | Accessed |
|---|---|---|---|
| Juzek, T. (2024). "Why Does ChatGPT Delve So Much? Exploring the Sources of Lexical Overrepresentation in Large Language Models." arXiv:2412.11385 | 21 focal words with frequency multipliers; RLHF hypothesis | https://arxiv.org/html/2412.11385v1 | 2026-05-31 |
| Kobak, D. et al. (2024). "Delving into ChatGPT usage in academic writing through excess vocabulary." arXiv:2406.07016 | 900 excess words 2013-2024; GitHub data | https://arxiv.org/pdf/2406.07016 | 2026-05-31 |
| Liang, W. et al. (2025). "Human-LLM Coevolution: Evidence from Academic Writing." arXiv:2502.09606 | Rising vs falling AI words 2023-2025 | https://arxiv.org/html/2502.09606v1 | 2026-05-31 |
| FSU News (2025-02-17). "Why Does ChatGPT 'Delve' So Much?" | Press write-up of FSU research | https://news.fsu.edu/news/science-technology/2025/02/17/ | 2026-05-31 |
| FSU News (2025-08-26). "On-screen and now IRL: ChatGPT buzzwords in everyday speech" | Spoken-language influence study | https://news.fsu.edu/news/education-society/2025/08/26/ | 2026-05-31 |
| arXiv:2603.23146. "Why AI-Generated Text Detection Fails" | Detection failure modes | https://arxiv.org/pdf/2603.23146 | 2026-05-31 |
| Scientific American. "ChatGPT and Gemini AIs Have Their Own Distinctive Writing Styles" | Trigram comparison; Delta method | https://www.scientificamerican.com/article/chatgpt-and-gemini-ai-have-uniquely-different-writing-styles/ | 2026-05-31 |

### Reference / encyclopedic

| Source | Coverage | URL | Accessed |
|---|---|---|---|
| Wikipedia: Signs of AI writing | Comprehensive tells catalogue | https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing | 2026-05-31 |

### Detector vendors

| Source | Coverage | URL | Accessed |
|---|---|---|---|
| GPTZero AI Vocabulary | Top 50 AI words and phrases (May 2026 update) — page exists but list not extractable via webfetch | https://gptzero.me/ai-vocabulary | 2026-05-31 |
| Originality.ai. "Invisible Text Detector & Remover" | Unicode tells; zero-width char analysis | https://originality.ai/blog/invisible-text-detector-remover | 2026-05-31 |
| Pangram Labs. "Which AI Detector Is Most Accurate?" | 30-tool comparison 2026 | https://www.pangram.com/blog/best-ai-detector-tools | 2026-05-31 |
| Leap AI Text Formatter | Em-dash and smart-quote removal | https://www.tryleap.ai/tools/ai-text-formatter | 2026-05-31 |
| Walter Writes AI. "Most Common ChatGPT Words to Avoid 2026" | Current vintage word list | https://walterwrites.ai/most-common-chatgpt-words-to-avoid/ | 2026-05-31 |
| GPTCleanup AI. "Em Dash Remover" | Em-dash artefact discussion | https://gptcleanuptools.com/em-dash-remover | 2026-05-31 |

### Aggregated catalogues

| Source | Coverage | URL | Accessed |
|---|---|---|---|
| Bloomberry. "AI Writing Patterns: The Complete Database" | 7,400+ patterns; 4,628 vocabulary; 129 cadences; 17 hooks; 625 transitions | https://www.bloomberry.ai/research/ai-writing-patterns | 2026-05-31 |
| tropes.fyi / gist by ossa-ma | 33 tropes catalogued by category | https://tropes.fyi/directory ; https://gist.github.com/ossa-ma/f3baa9d25154c33095e22272c631f5a1 | 2026-05-31 |
| SynkrLAB. "ChatGPT's Most Overused Words and Phrases (310+ List)" | Categorised inventory | https://synkrlab.com/chatgpts-most-overused-words-and-phrases/ | 2026-05-31 |
| God of Prompt. "500 ChatGPT Overused Words" | Numerical 500 list | https://www.godofprompt.ai/blog/500-chatgpt-overused-words-heres-how-to-avoid-them | 2026-05-31 |
| PageOn.AI. "The Most Overused ChatGPT Words in 2025" | 2025 ranking | https://www.pageon.ai/blog/the-most-overused-chatgpt-words | 2026-05-31 |
| Plus AI. "The most overused ChatGPT words" | Word list with commentary | https://plusai.com/blog/the-most-overused-chatgpt-words | 2026-05-31 |
| Embryo. "A list of words that AI over-uses" | Compact list | https://embryo.com/blog/list-words-ai-overuses/ | 2026-05-31 |
| Matrix Group. "Customize ChatGPT to Avoid Overused AI Words" | Word list with avoidance prompts | https://www.matrixgroup.net/blog/how-to-customize-chatgpt-to-avoid-overused-ai-words/ | 2026-05-31 |

### Model-specific analysis

| Source | Coverage | URL | Accessed |
|---|---|---|---|
| willfrancis.com. "How to Stop Claude Writing Like an AI" | Claude tells + prompt | https://willfrancis.com/how-to-stop-claude-writing-like-an-ai/ | 2026-05-31 |
| Every.to. "We Tested Claude Sonnet 4.5 for Writing and Editing" | Claude Sonnet 4.5 vs others | https://every.to/vibe-check/vibe-check-we-tested-claude-sonnet-4-5-for-writing-and-editing | 2026-05-31 |
| boringbot.substack. "Claude Opus 4.7, Here's what works and what doesn't" | Claude 4.7 critique | https://boringbot.substack.com/p/claude-opus-47-heres-what-works-and | 2026-05-31 |
| claudefa.st. "Claude Opus 4.7 Best Practices" | 4.7 behaviour | https://claudefa.st/blog/guide/development/opus-4-7-best-practices | 2026-05-31 |
| Anthropic. "How people ask Claude for personal guidance" | Sycophancy improvements 4.6 vs 4.7 | https://www.anthropic.com/research/claude-personal-guidance | 2026-05-31 |
| Nautil.us. "I Asked Claude Why It Won't Stop Flattering Me" | Sycophancy patterns | https://nautil.us/i-asked-claude-why-it-wont-stop-flattering-me-1279510 | 2026-05-31 |
| Type.ai blog. "Claude vs ChatGPT vs Gemini" | Model-style comparison | https://blog.type.ai/post/claude-vs-gpt | 2026-05-31 |
| Tactiq.io. "Claude vs ChatGPT vs Gemini: Which AI Writes Best 2026" | Style comparison | https://tactiq.io/learn/claude-vs-gemini-vs-chatgpt-for-writing | 2026-05-31 |
| HumanizeThisAI. "ChatGPT vs Claude vs Gemini Writing Quality" | Comparison | https://humanizethisai.com/blog/chatgpt-vs-claude-vs-gemini-writing | 2026-05-31 |

### Typography / punctuation specific

| Source | Coverage | URL | Accessed |
|---|---|---|---|
| Shady Characters. "The dash for AI" (Aug 2025) | Em-dash empirical analysis | https://shadycharacters.co.uk/2025/08/the-dash-for-ai/ (403 from WebFetch but referenced in search results) | 2026-05-31 |
| The Prompt Index. "AI Detection in 2025: Watermarks, New Models" | U+202F GPT-o3/o4-mini surge | https://www.thepromptindex.com/ai-detection-in-2025-watermarks-new-models-staying-undetected.html | 2026-05-31 |

### Genre-specific

| Source | Coverage | URL | Accessed |
|---|---|---|---|
| Medium / Everyday AI. "These 15 Phrases Prove You Used ChatGPT" | Email + business phrase tells | https://medium.com/everyday-ai/these-15-phrases-prove-you-used-chatgpt-and-everyone-can-tell-53accf90a742 | 2026-05-31 |
| OpenAI dev community. "GPT generation follows a hidden email pattern" | Email-template tell | https://community.openai.com/t/gpt-generation-follows-a-hidden-email-pattern/544032 | 2026-05-31 |
| Hacker News thread 35869582 | "I hope this message finds you well" tell | https://news.ycombinator.com/item?id=35869582 | 2026-05-31 |
| TealHQ. "AI Cover Letter Example 2025" | Cover letter template tells | https://www.tealhq.com/cover-letter-example/artificial-intelligence | 2026-05-31 |
| MultipleChat. "How to Write a Cover Letter With AI 2026" | Cover letter critique | https://multiple.chat/ai-cover-letter | 2026-05-31 |
| aiunpacker.com. "30 ChatGPT LinkedIn Prompts" | LinkedIn template tells | https://aiunpacker.com/blog/chatgpt-prompts-for-linkedin-30-templates-for-viral-posts/ | 2026-05-31 |
| Letterdrop. "LinkedIn Thought Leadership ChatGPT" | LinkedIn templates | https://letterdrop.com/blog/linkedin-thought-leadership-chatgpt | 2026-05-31 |
| Sight AI. "SEO Article Templates AI 2026" | SEO listicle template | https://www.trysight.ai/blog/seo-article-templates-ai | 2026-05-31 |
| Memorable.design. "Listicle SEO 2026" | Listicle conventions | https://memorable.design/listicle-seo-2026/ | 2026-05-31 |
| Exceeds.ai. "Assess Pull Request Code Quality with AI" | AI code review patterns | https://blog.exceeds.ai/assess-pr-code-ai-tools/ | 2026-05-31 |
| Graphite. "Experimenting with AI code review" | PR description patterns | https://graphite.com/blog/ai-code-review-experiments | 2026-05-31 |
| QWE AI Academy. "AI Tools for Git Commits and PR Reviews 2026" | Commit message tells | https://www.qwe.edu.pl/tutorial/ai-tools-git-commit-messages-pr-reviews/ | 2026-05-31 |

### Counter-strategy literature

| Source | Coverage | URL | Accessed |
|---|---|---|---|
| Medium / Thomas Smith. "Do Typos Fool AI Detectors?" (March 2025) | Counter-strategy empirical test | https://medium.com/the-generator/do-typos-fool-ai-detectors-df5821bb1a66 | 2026-05-31 |
| Minding The Campus. "College Students Are 'Dumbing Down' Their Essays" (June 2025) | Detection-evasion practice | https://mindingthecampus.org/2025/06/12/college-students-are-dumbing-down-their-essays-to-avoid-ai-detection/ | 2026-05-31 |
| WHYY. "Penn researchers weigh in on accuracy of AI detectors" | Detector limitations | https://whyy.org/articles/penn-professor-tests-ai-vs-human-detection/ | 2026-05-31 |

### Critique / commentary

| Source | Coverage | URL | Accessed |
|---|---|---|---|
| Shankar, S. "Writing in the Age of LLMs" (sh-reya.com) | Practitioner-author critique | https://www.sh-reya.com/blog/ai-writing/ | 2026-05-31 |
| Hastewire. "Uncover Linguistic Patterns of AI Writing" | Pattern catalogue | https://hastewire.com/blog/uncover-linguistic-patterns-of-ai-writing-key-tells | 2026-05-31 |
| Revolution in AI. "Why Claude Agrees With You Even When You're Wrong" (April 2026) | Sycophancy patterns | https://www.revolutioninai.com/2026/04/why-claude-agrees-sycophancy-problem-explained.html | 2026-05-31 |
| Substack: Robots Ate My Homework. "The internet made a ban list for AI writing" | Defence of AI-flagged techniques | https://robotsatemyhomework.substack.com/p/ai-writing-patterns | 2026-05-31 |

## Notes and caveats

### Strong empirical anchors

The Juzek 2024 / Kobak 2024 / Liang 2025 trio provides the most reliable evidence for vocabulary tells. The Bloomberry catalogue (7,400+ patterns) is the largest aggregated source for sentence-level and phrase-level patterns but lacks the per-pattern empirical confidence weighting that the academic sources provide.

### Disconfirming evidence found

- **Em dashes used by skilled human writers:** thefederal.com (2025) and shadycharacters.co.uk argue em dashes are legitimate punctuation appropriated by AI through training data. Heavy users (Cormac McCarthy, Emily Dickinson) wrote with em dashes well before LLMs. Conclusion: em dashes are a TELL only at high rates (3+ per page); occasional use is not diagnostic.
- **Shankar 2024 (sh-reya.com) defends:** intentional repetition, signposting phrases, parallel structure, predictable section headings, declarative openings, and em dashes — when purposefully deployed. The pattern matters more than the marker.
- **Zero-width characters (U+200B):** Originality.ai found these don't actually affect detection. Often cited as a "hidden watermark" but the empirical evidence doesn't support reliability as a tell.

### Open questions / unresolved

- **The Claude 4.7 "corporate" shift** — multiple sources note that Claude 4.7 prose has become more mechanical and bullet-heavy than 4.6, contradicting Anthropic's marketing. Whether this is a long-form regression or a deliberate choice is unclear. Worth monitoring.
- **GPT-5 "bullet collapse"** behaviour — every.to vibe check notes GPT-5 collapses into bullets at length. Useful as a model-attribution tell.
- **Counter-strategies that became tells** — the entire Section 10 set is the fastest-evolving category. Today's counter-strategy is tomorrow's tell. The performative-typos pattern is in this transition right now per Minding The Campus 2025.

### Items I could NOT verify

- **[UNVERIFIED]** GPTZero's "Top 50 AI Words and Phrases" list — the page exists but the actual word list was not extractable via WebFetch. To verify the GPTZero-specific ranking, the live page would need direct browser inspection.
- **[UNVERIFIED]** Specific phrase frequencies for "I want to make sure" and "Happy to" as Claude tics — Reddit threads reference them but no corpus study. Treat as MEDIUM confidence.
- **[UNVERIFIED]** "circle back" as Gemini-specific (vs ChatGPT) — Bloomberry lists it as both. Conflicting attribution.

### Coverage gaps

- **Audio / spoken AI patterns** — not researched. The FSU 2025 study on "ChatGPT buzzwords in spoken language" suggests there are oral analogues but they're outside the scope of writing.
- **Image-caption AI tells** — not researched. Different domain.
- **Multilingual AI tells** — the Juzek, Kobak, Liang studies are English-only. Tells in other languages may differ substantially.
- **AI-flagged content by social platform algorithms** — LinkedIn, X, and Facebook all have internal AI-detection signals not publicly documented.
- **Academic-flavoured prose in specific disciplines** — the corpus studies cover biomedical (PubMed) and CS (arXiv). Humanities, law, business writing may have different tells.

### Synthesis priority for the rule file

Highest-value additions to the existing rule file based on this research:

1. **Section 9's "still rising" vocabulary** (significant, additionally, crucial, effectively, comprehensive, enhance, capabilities, valuable, align, advancements) — these are the current-vintage tells with empirical backing that aren't yet broadly recognised.
2. **The "Serves As" copula dodge** as a named anti-pattern (corpus-evidenced via the "is/are" decline).
3. **Bold-first bullet pattern** (single most-recognised AI list-formatting pattern across sources).
4. **The full set of opener templates** (Section 2): curiosity hook, candor opener, reveal setup, contrarian opener, statistic opener, empathy opener, confession opener — these are catalogued by Bloomberry with model-specific attribution.
5. **Email / cover-letter / LinkedIn / SEO** genre-specific templates from Section 7 — most useful for the writing-style rule because the user writes in these genres.
6. **Section 10 counter-strategies** — these will save the user from over-correcting in ways that themselves trigger AI signals.

