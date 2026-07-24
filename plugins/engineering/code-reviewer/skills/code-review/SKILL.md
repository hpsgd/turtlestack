---
name: code-review
description: Review staged or recent changes — native Claude Code review for mechanics, layered with team conventions and the team verdict contract
argument-hint: "[branch or commit range, e.g. 'main..HEAD']"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Skill, Agent
---

Review changes by layering team conventions on top of Claude Code's native review. The native `/code-review` owns generic review mechanics — multi-agent finding, adversarial verification, bug hunting. This skill owns what the native review can't know: team conventions, the verdict contract, and the calibration bar for what counts as a finding.

## Step 1: Determine scope

Run `git diff $ARGUMENTS` (default: `git diff --staged`, falling back to `git diff main..HEAD` if nothing is staged). Record:

1. Files changed and lines touched
2. Languages involved (by file extension)
3. Whether the diff touches auth, payments, data access, PII handling, or a security control (rate limiting, session management, crypto, input validation at a boundary) — flag these for Step 3

## Step 2: Run the native review (mechanics)

Invoke the bundled Claude Code review via the Skill tool:

```
Skill(skill="code-review")
```

This runs the native multi-agent review — correctness, security, and quality findings, adversarially verified. Collect its findings as the mechanics layer.

**Fallback:** if the bundled skill is unavailable (disabled via `disableBundledSkills`, or an older Claude Code), dispatch the `code-reviewer:code-reviewer` agent instead — it carries the full standalone four-pass methodology. If neither is available, perform the mechanics pass inline yourself.

Whichever path produces Layer 1, the mechanics pass covers at minimum: logic errors, null/absent-value handling, concurrency (races, TOCTOU on any read-modify-write), edge cases (empty, zero, max, unicode), error propagation, and resource lifecycle (leaks, cleanup, unbounded growth).

However Layer 1 was produced — bundled skill, agent, or inline — **the review is incomplete until Steps 3 and 4 run.** Layer 1 is generic mechanics; it cannot see team conventions. Never emit a verdict from Layer 1 alone.

## Step 3: Layer the team conventions

The native review doesn't know the team's standards. Apply them on top.

For each layer below, invoke the named skill via the Skill tool when its plugin is enabled. When it isn't (the Skill call errors or the skill isn't listed), don't skip the layer: apply the corresponding installed rules from `.claude/rules/` (e.g. the typescript, testing, and security-baseline rules) inline, and record `inline — via installed rules` for that row in the Layers table. The layer's job is applying the conventions; the skill is just the preferred vehicle.

1. **Language conventions** — for each language in the diff, invoke the matching review skill:

   | Files | Skill |
   |---|---|
   | `.ts` / `.tsx` | `coding-standards:review-typescript` |
   | `.cs` | `coding-standards:review-dotnet` |
   | `.py` | `coding-standards:review-python` |
   | `.php` | `coding-standards:review-php` |
   | `.go` | `coding-standards:review-go` |

2. **Cross-cutting standards** — always invoke `coding-standards:review-standards` (quality and writing-style concerns that apply to every file type).
3. **Git conventions** — when the review covers commits or a PR, invoke `coding-standards:review-git` (commit format, branch model, content dates).
4. **Project rules** — check `.claude/rules/` and CLAUDE.md for project-specific constraints the diff may violate. Installed rules define what "correct" means for this project; a diff can pass native review and still break them.
5. **Security-sensitive areas** — if Step 1 flagged anything (auth, payments, data access, PII, or a security control), also run `security-compliance:security-audit` on the diff and label its findings with that source.

## Step 4: Merge into the team verdict

Combine native findings and conventions findings into one report. Deduplicate: where both layers flag the same line, keep the finding with the stronger evidence and note the corroboration.

Every finding — blocker, important, and suggestion alike — uses the finding template from the output format (category, `file:line`, evidence, source layer, fix). Do not reformat any tier into an ad-hoc table; a finding without its source layer or location is incomplete.

### Scoring — HARD vs SOFT signals

- **HARD signal**: an issue that will cause wrong behaviour in production, a security vulnerability, or possible data loss. These are blockers.
- **SOFT signal**: a concern that might cause issues under specific conditions, or a conventions violation with no runtime impact. Important but not blocking.

Conventions violations default to SOFT unless the convention exists to prevent a production failure (e.g. strict-validation gaps at a boundary are HARD).

## Output Format

**Deliver the entire report as one final message.** Brief status lines between layer invocations are fine, but the final message must contain the complete report below — context, layers table, every finding in full, and verdict. A report split across earlier messages is lost to the reader: never reference findings by number without restating them in the final message.

```
## Code Review: [brief description of what was reviewed]

### Context
[2-3 sentences: what changed, why, what the intent is]

### Layers applied

| Layer | What ran | Findings |
|---|---|---|
| Mechanics | [bundled /code-review \| code-reviewer agent \| inline pass] | [N] |
| Conventions | [review-* skills invoked \| inline — via installed rules, naming them] | [N or "none — checked"] |
| Security | [security-audit \| inline — via security-baseline rules \| not triggered — say why] | [N or —] |

This table is mandatory. A row may report zero findings, but a missing row means the layer was skipped and the review is incomplete.

### Findings

#### Blockers (HARD signals — must fix before merge)

[Each finding:]
**[Category]** `file:line` — [description]
**Evidence:** [code or grep output]
**Source:** [native review | <conventions skill> | both]
**Fix:** [concrete suggestion]

#### Important (SOFT signals — should fix, not blocking)

[same format]

#### Suggestions (quality improvements)

[same format]

### Verdict

**[APPROVE | REQUEST_CHANGES | NEEDS_DISCUSSION]**

- APPROVE: Zero blockers, suggestions are optional
- REQUEST_CHANGES: One or more blockers present
- NEEDS_DISCUSSION: Architectural concerns that need team input

Zero-finding gate: [triggered — positive assertion with file:line | N/A — findings present]
Files reviewed: N | Blockers: X | Important: Y | Suggestions: Z
```

## Zero-Finding Gate

If both layers come back clean, say so and name one positive assertion with a `file:line` reference — something specific that was done well. "No findings from the native review or the conventions layer. Notably, `src/auth/middleware.ts:42` correctly validates the JWT audience claim before extracting permissions. APPROVE." Do not manufacture issues to appear thorough — false positives erode trust.

## Calibration Rules

- A finding without evidence is not a finding. Show the code.
- A finding without a fix suggestion is incomplete. Propose the change.
- "Consider whether..." is not a finding. Either it is a problem or it is not.
- Performance concerns without measurement or obvious complexity analysis are noise.
- Style preferences that are not codified in team standards are not findings. Style preferences that ARE codified (installed rules, review skills) are findings — cite the rule.

## Related Skills

- `/code-reviewer:pr-create` — for creating PRs after review is complete or when the user needs to submit their changes.
- `coding-standards:review-*` — the per-language conventions layers this skill orchestrates; invoke one directly for a single-language spot check.
- `security-compliance:security-audit` — deeper security audit for sensitive areas or whole directories.
