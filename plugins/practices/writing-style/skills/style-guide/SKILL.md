---
name: style-guide
description: "Apply writing style and tone guidelines when creating or reviewing documentation, commit messages, PR descriptions, error messages, or user-facing text. Produces specific rewrites for every violation found."
argument-hint: "[text to review, or 'review' to check recent output]"
user-invocable: true
allowed-tools: Read, Grep, Glob
---

Apply these writing standards to all text output. When reviewing existing text, check against every rule and provide specific rewrites — not abstract feedback.

## Step 1: Apply core principles (mandatory)

Every piece of text must pass these five tests:

1. **Say it directly.** Lead with the point. No preamble, no throat-clearing.
2. **Say it once.** If you have made the point, move on.
3. **Say it concretely.** Examples beat abstractions. Specific beats general.
4. **Say it actively.** The subject does the action. Not "the file was deleted" but "the script deletes the file."
5. **Say it plainly.** If a simpler word works, use it.

## Step 2: Scan for banned words and phrases (mandatory)

Read `references/ai-tells-catalogue.md` (next to this file) first. It is the full catalogue behind the always-on `tone-and-voice` rule: every banned word, phrase, opener, closer and structural tell, plus the 37-point editing pass. Check the text against all of it; the tables below are the quick substitutions.

### Word substitutions

Replace the left column with the right:

| Do not write | Write instead |
|---|---|
| utilize | use |
| implement | build |
| facilitate | help, enable |
| leverage | use |
| comprehensive | complete, thorough, full |
| robust | strong, reliable, solid |
| streamline | simplify |
| empower | let, enable |
| foster | encourage, support |
| paradigm | model, approach |
| synergy | (cut the word entirely) |
| ecosystem | system, platform |
| cutting-edge | modern, current |
| game-changing | (describe the actual change) |
| best practices | (say what the practice is) |
| deep dive | look at, examine, review |
| in order to | to |
| it should be noted | (cut — just state the thing) |
| going forward / moving forward | from now on, next |
| a myriad of / a plethora of | many |
| optimal | best |
| prior to | before |
| subsequent to | after |
| in the event that | if |
| due to the fact that | because |
| at this point in time | now |

### Banned words — hard stops

Flag every occurrence. These are AI tells and corporate filler:

`delve`, `tapestry`, `landscape`, `nuanced`, `realm`, `multifaceted`, `holistic`,
`pivotal`, `cornerstone`, `underpinning`, `intricate`, `noteworthy`, `commendable`,
`meticulous`, `elevate`, `testament`, `embark`, `encompass`, `spearhead`

No exceptions. If you find one, rewrite the sentence.

### Banned phrases — hard stops

- "It's important to note" / "It's worth mentioning" — just state the fact
- "In today's world" / "In the modern era" — cut
- "At its core" / "At the heart of" — state what it is directly
- "This allows us to" / "This enables us to" — state what it does
- "When it comes to" — cut and restructure
- "As mentioned earlier/above" — repeat the info briefly if needed
- "Without further ado" / "Let's take a look at" — just present it
- "It goes without saying" / "Needless to say" — then don't say it
- "Additionally" / "Furthermore" / "Moreover" — just state the next point

**Output:** List of violations found with exact locations and rewrites.

## Step 3: Check sentence structure (mandatory)

| Rule | Check | Wrong | Right |
|---|---|---|---|
| **Active voice** | Subject performs the action | "The configuration is loaded by the service" | "The service loads the configuration" |
| **No -ing openers** | Don't start with participial phrases | "Leveraging the new API, the client..." | "The client fetches data faster with the new API" |
| **Sentence length** | Flag sentences over 30 words | [split into two] | [two shorter sentences] |
| **One idea per sentence** | Split "and" connecting independent clauses | "It validates input and sends the response" | "It validates input. Then it sends the response." |
| **Front-load key terms** | Put the subject early | "For the purpose of improving reliability, we added retry logic" | "Retry logic improves reliability" |
| **Parallel structure** | List items use the same grammatical form | "handles auth, is logging requests, and data validation" | "handles auth, logs requests, and validates data" |

**Output:** Structure violations with specific rewrites.

## Step 4: Check punctuation and formatting (mandatory)

| Rule | Limit | Action |
|---|---|---|
| **Em dashes** | Max 2 per document | Replace extras with periods, commas, or parentheses |
| **Semicolons** | Use sparingly | Most should be two separate sentences |
| **Exclamation marks** | Max 1 per document (0 is better) | They reduce credibility, not increase excitement |
| **Oxford comma** | Always | "Red, white, and blue" not "Red, white and blue" |
| **Paragraphs** | 1–4 sentences | A full-screen paragraph is not a paragraph |
| **Code references** | Backticks for code | `function_name`, not function_name |
| **Links** | Descriptive text | "See the [deployment guide](url)" not "[here](url)" |
| **Headings** | No skipped levels | `##` then `###`, never `##` then `####` |

**Output:** Formatting violations with corrections.

## Step 5: Apply context-specific rules (mandatory)

### Commit messages
- Imperative mood: "Add feature" not "Added feature"
- First line under 70 characters
- Body explains WHY, not WHAT (the diff shows WHAT)

### PR descriptions
- Lead with the problem being solved
- Bullet points, not prose paragraphs
- Test plan is concrete and actionable

### Error messages
- State what went wrong, what the user can do, and where to find help
- No jargon the user would not understand
- No stack traces in user-facing errors

### API documentation
- Start with what the endpoint does (one sentence)
- Parameters: name, type, required/optional, constraints
- Include example request and response

### README files
- First paragraph: what it is and why you would use it
- Quick start: fewest steps to working code
- One line of badges maximum

**Output:** Context-specific violations with rewrites.

## Rules

- **Rewrite, don't describe.** "Make it more concise" is not feedback. Rewrite the specific sentence.
- **Every finding needs the exact text, the violated rule, and a specific rewrite.** No exceptions.
- **Zero findings is valid.** If the text follows all rules, say so. Do not manufacture findings.
- **Apply proportionally.** A quick Slack message doesn't need the full checklist. A published doc does.
- **Preserve the author's voice.** Fix violations without rewriting the entire personality out of the text. The goal is clarity, not homogeneity.

## Output Format

```markdown
## Style Review: [what was reviewed]

### Findings

| # | Rule violated | Original text | Rewrite |
|---|---|---|---|
| 1 | [rule] | "[exact text]" | "[specific rewrite]" |
| 2 | [rule] | "[text]" | "[rewrite]" |

### Summary
- Total findings: [count]
- Banned words: [count]
- Structure issues: [count]
- Formatting issues: [count]
- Context-specific: [count]

### Overall assessment
[One sentence: is the text ready to publish, or does it need a revision pass?]
```

## Related Skills

- `/coding-standards:review-standards` — for code-level quality standards (naming, structure, comments). Style-guide covers prose; review-standards covers code.
