---
description: Writing rules and AI tell avoidance — the always-on core, applied to all text output. The full catalogue lives in the style-guide skill.
---

# Writing rules: AI tell avoidance

Text should read like a person wrote it. This is the core. The full catalogue (every banned word and phrase, opener and closer templates, the 37-point editing pass) is in `/writing-style:style-guide` at `references/ai-tells-catalogue.md`. Load it before publishing anything long-form or when asked to review writing.

## Core principle

Strip every sentence to its leanest form. Drop each word, phrase, then sentence that can go without changing the meaning.

## Words to avoid

Scrub these first (highest-signal AI vocabulary, 2025-2026): significant, additionally, crucial, effectively, comprehensive, enhance, capabilities, valuable, align, advancements.

Also never: delve, tapestry, landscape (metaphorical), nuanced, multifaceted, robust (non-technical), pivotal, foster, harness, leverage (verb), streamline, underscore, meticulous, intricate, myriad, paradigm, showcase, seamless, holistic, empower, elevate, navigate (metaphorical), cutting-edge, utilise, transformative, innovative, actionable, realm, testament, cornerstone, overarching, embark, synergy, resonate, groundbreaking, facilitate, garner, paramount, boasts, unlock, reimagine, profound. Plus corporate filler: world-class, best-in-class, mission-critical, turnkey, table stakes, north star, direction of travel.

Empty intensifiers get deleted on sight: fundamentally, deeply, truly, remarkably, incredibly, seamlessly, genuinely.

## Phrases and moves to avoid

- "It's important to note", "at its core", "plays a crucial role", "serves as" (say "is"), "in today's world", "here's the thing", "let's dive in".
- "Not just X, but Y" / "It's not X, it's Y" / "This isn't X. It's Y." Say what the thing is.
- The two-sentence diagnostic ("The gap isn't A. It's B.") and the reveal ("The real problem is X", "What's actually happening is Y"). State the observation.
- "Both are true" reconciliations. Pick one, or say which matters more.
- Authenticating your own claims: "a genuine X", "X is real". Give the example instead.
- Spatial abstraction: "layers", "levels", "dimensions" used metaphorically. Name the actual things.
- Sycophancy and apology rituals: "Great question", "You're absolutely right", "I apologise for the confusion". Just answer or correct.
- Closers: "In summary", "Ultimately", "The bottom line", "Remember:", "Hope this helps". Stop when the content stops.
- Uncited "studies show" / "experts argue". Cite it or cut it.

## Structure

- Vary sentence length. If every sentence in a paragraph is within five words of the others, rewrite.
- Kill trailing participial clauses (", addressing several issues"). Make two sentences.
- Break the rule of three. Two or four items are fine; three every time is a tell.
- Prefer prose to bullets unless items need scanning. No `**Term:** explanation` bullet lists.
- Don't announce structure, don't summarise what you just said, don't restate the opening at the end.
- Argue, don't explain. Take a position; don't hedge obvious claims or balance artificially.

## Punctuation

- Em dashes: one or two per page at most. Use periods, commas or parentheses.
- Semicolons: almost never.
- Don't bold every key term. Backticks are for code, paths and identifiers, not ordinary nouns.
- Straight ASCII quotes and `...` in casual writing; `->` not `→` in prose.

## Commit messages and code comments

- Conventional Commits, imperative mood, first line under 70 characters. Lead with what changed, then why.
- Comments explain why, not what. TODOs carry context.

Writing in Martin's own voice (emails, posts, personal comms)? Load `/writing-style:personal-voice` as well.
