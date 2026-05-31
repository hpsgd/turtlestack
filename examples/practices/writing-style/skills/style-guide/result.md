# Style Guide

Scenario: A developer asks for a style review of a newly written API documentation section before publishing. The text contains banned words, passive voice, overly long sentences, and missing Oxford commas.

## Prompt

> /style-guide Review this API documentation section: "The endpoint leverages a comprehensive authentication paradigm that facilitates robust access control. It's important to note that the request payload is validated by the middleware layer prior to being processed. Tokens are utilized to ensure that only authorized, authenticated and verified users can access the endpoint. Moving forward, we will be adding support for OAuth 2.0, SAML and API key authentication mechanisms."

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Style Review: API authentication documentation

### Findings

| # | Rule violated | Original text | Rewrite |
|---|---|---|---|
| 1 | Banned word: "leverages" | "The endpoint leverages a comprehensive authentication paradigm" | "The endpoint enforces authentication" or "The endpoint uses authentication" |
| 2 | Banned word: "comprehensive" | "a comprehensive authentication paradigm" | "an authentication model" or just "authentication" |
| 3 | Banned word: "paradigm" | "authentication paradigm that facilitates" | "authentication model that provides" |
| 4 | Banned word: "facilitates" | "that facilitates robust access control" | "that provides strong access control" |
| 5 | Banned word: "robust" | "facilitates robust access control" | "provides strong access control" |
| 6 | Banned phrase: "It's important to note" | "It's important to note that the request payload is validated" | "The middleware validates the request payload before processing." |
| 7 | Banned word: "utilized" | "Tokens are utilized to ensure" | "Tokens ensure" |
| 8 | Banned word: "prior to" | "prior to being processed" | "before processing" |
| 9 | Passive voice + weak structure | "the request payload is validated by the middleware layer" | "The middleware validates the request payload" |
| 10 | Redundant terms | "only authorized, authenticated and verified users" | "only authorized users" (authorized already encompasses authenticated and verified) |
| 11 | Missing Oxford comma | "authorized, authenticated and verified" | "authorized, authenticated, and verified" |
| 12 | Banned phrase: "Moving forward" | "Moving forward, we will be adding support" | "Next, we'll add support" or "We plan to add support" |
| 13 | Missing Oxford comma | "OAuth 2.0, SAML and API key" | "OAuth 2.0, SAML, and API key" |
| 14 | Weak future tense | "we will be adding support" | "we'll add support" or "we plan to add" |

### Summary
- Total findings: 14
- Banned words: 5 (leverages, comprehensive, paradigm, facilitates, robust)
- Banned phrases: 3 (It's important to note, prior to, Moving forward)
- Structure issues: 3 (passive voice, redundancy, weak future tense)
- Formatting issues: 2 (missing Oxford commas)
- Word choice: 1 (utilized)

### Suggested rewrite

**Original:** "The endpoint leverages a comprehensive authentication paradigm that facilitates robust access control. It's important to note that the request payload is validated by the middleware layer prior to being processed. Tokens are utilized to ensure that only authorized, authenticated and verified users can access the endpoint. Moving forward, we will be adding support for OAuth 2.0, SAML and API key authentication mechanisms."

**Revised:** "This endpoint enforces authentication to control access. The middleware validates all requests before processing. Tokens ensure only authorized users can access the endpoint. Next, we'll add support for OAuth 2.0, SAML, and API key authentication."

### Overall assessment
The original document requires revision. It contains 5 banned words/phrases, relies on passive constructions, and uses vague terms ("paradigm," "mechanisms"). The rewrite above cuts word count by 50%, removes all violations, and leads with concrete actions instead of abstract concepts.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/16.5 (97%) |
| Evaluated | 2026-05-31 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 18663 ms |
| Target cost | $0.0827 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 2 identifies all banned words present — leverage, comprehensive, paradigm, facilitates, robust, utilized — each flagged with the exact occurrence | PASS | Rows 1-5 and 7 flag leverages, comprehensive, paradigm, facilitates, robust, utilized with exact quoted occurrences from the source text. |
| c2 | Each banned word finding includes the exact original text and a specific rewrite, not just identification | PASS | Every banned-word row contains 'Original text' quote and a concrete 'Rewrite' suggestion, e.g. row 7: 'Tokens are utilized to ensure' → 'Tokens ensure'. |
| c3 | "It's important to note that" is flagged as a banned phrase and removed in the rewrite | PASS | Row 6 labels 'Banned phrase: "It's important to note"' and rewrites to 'The middleware validates the request payload before processing.' |
| c4 | Passive voice constructions ("is validated by", "are utilized") are identified in Step 3 and rewritten to active voice | PASS | Row 9 flags 'Passive voice + weak structure: the request payload is validated by the middleware layer' → 'The middleware validates the request payload'; row 7 handles 'are utilized'. |
| c5 | "Moving forward" is flagged as a banned phrase with a suggested rewrite ("From [date]," or "Next,") | PASS | Row 12 labels 'Banned phrase: "Moving forward"' and offers 'Next, we'll add support' — matching the skill's listed alternative. |
| c6 | Missing Oxford commas ("authorized, authenticated and verified", "OAuth 2.0, SAML and API key") are flagged in Step 4 | PASS | Row 11 flags 'authorized, authenticated and verified' → adds comma; row 13 flags 'OAuth 2.0, SAML and API key' → adds comma. |
| c7 | Output uses the defined findings table format with rule violated, original text, and specific rewrite for each finding | PASS | Table has exactly columns '#, Rule violated, Original text, Rewrite' for all 14 rows. |
| c8 | Overall assessment states whether the text is ready to publish or needs a revision pass — not left implicit | PARTIAL | Overall assessment explicitly states 'The original document requires revision' with rationale — not left implicit. |
| c9 | Output begins with a "## Style Review:" heading naming what was reviewed (the API documentation snippet), not generic prose | PASS | Output opens with '## Style Review: API authentication documentation'. |
| c10 | Output's findings table uses exactly four columns in order: number, rule violated, original text, rewrite — matching the format defined in the skill | PASS | Table header is '\| # \| Rule violated \| Original text \| Rewrite \|' — exactly four columns in the specified order. |
| c11 | Each rewrite preserves the technical meaning of the original (authentication, validation, token use, future protocol support) without inventing new requirements | PASS | Suggested rewrite retains authentication enforcement, middleware validation, token-based access control, and OAuth 2.0/SAML/API key future support. |
| c12 | Rewrites for banned-word substitutions follow the skill's substitution table (leverage→use, comprehensive→complete/thorough/full, facilitate→help/enable, robust→strong/reliable/solid, utilized→used) | PARTIAL | leverage→'uses' ✓; robust→'strong' ✓; but comprehensive→'an authentication model' (not complete/thorough/full), facilitate→'provides' (not help/enable), utilized→'ensure' (not 'used'). |
| c13 | At least one rewrite turns a passive construction into a clear active-voice sentence with an explicit subject (e.g., "the middleware validates the request payload") | PASS | Row 9 rewrite: 'The middleware validates the request payload' — explicit subject 'The middleware' with active verb 'validates'. |
| c14 | Output produces a Summary block with numeric counts for total findings, banned words, structure issues, formatting issues, and context-specific issues — counts are consistent with the findings table | PASS | Summary: Total 14, Banned words 5, Banned phrases 3, Structure 3, Formatting 2, Word choice 1 — sums to 14, consistent with 14-row table. |
| c15 | Findings include specific line/quote anchors (the exact original text in quotes) so a reader can locate each issue in the source without re-reading the whole snippet | PASS | Every row in the 'Original text' column contains a verbatim quoted phrase from the source, e.g. '"prior to being processed"', '"Moving forward, we will be adding support"'. |
| c16 | Output does not introduce any new banned words from the skill's hard-stop list in its own rewrites or commentary | PASS | Suggested rewrite and commentary use 'enforces', 'validates', 'ensures', 'plan to add' — none match the banned word list. |
| c17 | Output groups or orders findings by step (Step 2 banned words, Step 3 structure, Step 4 formatting) rather than mixing them randomly | PARTIAL | Rows 1-5 cluster banned words, but rows 6-8 mix banned phrases with a structure issue (#9), and rows 11/13 (Oxford commas) are split by #12 (banned phrase). No explicit step headings. |
| c18 | Output flags the API-documentation context (this is API docs) and notes whether the rewritten version meets the README/API doc context-specific rules from Step 5 | PARTIAL | Title names 'API authentication documentation' context, but no explicit Step 5 API-doc context-specific rule check is performed or referenced in the assessment. |

### Notes

The output is thorough and well-structured, correctly catching all 6 banned words, both banned phrases, both Oxford comma omissions, and passive constructions, with a clean suggested rewrite. The only notable gap is that a few banned-word substitutions deviate from the skill's prescribed table (facilitate→provides instead of help/enable; comprehensive removed rather than replaced with complete/thorough/full), and there is no explicit Step 5 API-doc context evaluation.
