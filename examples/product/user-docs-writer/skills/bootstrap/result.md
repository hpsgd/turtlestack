# Bootstrap

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/content/CLAUDE.md` containing a user-authored section. The user-docs-writer bootstrap skill should preserve that user content while appending the missing user-documentation sections (with a merge marker). Unlike the architect bootstrap, this skill manages only one file — `docs/content/CLAUDE.md` — so the test focuses on the safe-merge contract and the manifest output. The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

> The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/content/CLAUDE.md` is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.
> 
> Read the user-docs-writer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/product/user-docs-writer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.
> 
> After the bootstrap completes, output the manifest summary the skill defines (files merged, next steps).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## User Docs Bootstrap Complete

### Files merged
- `docs/content/CLAUDE.md` — appended user documentation conventions (safe merge: preserved existing "Custom team notes" section with USER-EDIT-SENTINEL-DO-NOT-STRIP)

### Next steps
- Write onboarding content using `/user-docs-writer:write-onboarding`
- Create initial KB articles using `/user-docs-writer:write-kb-article`
- Define content strategy using `/user-docs-writer:content-strategy`

### Artifacts written

#### `work/docs/content/CLAUDE.md`

```
# Content Domain

This directory contains documentation conventions for the project.

## Custom team notes

USER-EDIT-SENTINEL-DO-NOT-STRIP

This section was written by the team and must survive any bootstrap re-run.
It exists to test the safe-merge contract: the bootstrap skill must not
overwrite or remove user-authored content.

<!-- User documentation section — added by user-docs-writer bootstrap v0.1.0 -->

## User Documentation

This section covers user guide conventions, onboarding content format, KB article structure, and content strategy.

### What User Docs Covers

- **User guides** — task-oriented documentation for end users
- **Onboarding content** — first-run experiences and getting started flows
- **KB articles** — self-service support content
- **Content strategy** — information architecture and content lifecycle

### User Guide Conventions

User guides follow the Diataxis "how-to" mode — task-oriented, goal-focused:

| Principle | Description |
|-----------|-------------|
| Start with the goal | Title = what the user wants to achieve, not the feature name |
| Assume basic knowledge | Don't re-explain concepts covered in tutorials |
| Numbered steps | Every procedure uses numbered steps with one action per step |
| Show outcomes | Include expected results after key steps (screenshots or output) |
| Link, don't repeat | Cross-reference related guides rather than duplicating content |

### Onboarding Content Format

Onboarding content follows a progressive disclosure pattern:

1. **Welcome** — what the product does (one sentence), what the user will achieve
2. **Quick win** — shortest path to first value (< 5 minutes)
3. **Core workflow** — the primary task loop the user will repeat
4. **Next steps** — links to deeper guides and features

### Rules
- Onboarding targets time-to-first-value, not feature coverage
- Every onboarding flow has a measurable success metric (e.g., activation event)
- Content is tested with real users — iterate based on drop-off data

### KB Article Structure

Every KB article follows this template:

| Section | Purpose |
|---------|---------|
| **Title** | Question format preferred — "How do I..." or "Why does..." |
| **Summary** | One-paragraph answer (for quick scanning) |
| **Steps / Explanation** | Detailed procedure or explanation |
| **Related articles** | Links to related KB content |
| **Last verified** | Date the article was confirmed accurate |

### KB conventions
- Articles are written for scanning — use headings, bullets, and bold key terms
- Every article has a "Last verified" date — stale articles (> 6 months) are flagged for review
- Search keywords are included in the article metadata
- Publish to GitHub Wiki for discoverability

### User Docs Tooling

| Tool | Purpose |
|------|---------|
| GitHub Wiki | KB articles, onboarding guides |
| GitHub (in-repo) | Versioned user guides in `docs/` |

### Available User Docs Skills

| Skill | Purpose |
|-------|---------|
| `/user-docs-writer:write-user-guide` | Write a task-oriented user guide |
| `/user-docs-writer:write-onboarding` | Write onboarding content |
| `/user-docs-writer:write-kb-article` | Write a KB article |
| `/user-docs-writer:content-strategy` | Define content strategy and information architecture |

### User Docs Conventions

- User guides are titled by goal, not by feature ("Export your data" not "Export feature")
- Onboarding content is reviewed quarterly against activation metrics
- KB articles are verified for accuracy at least every 6 months
- All user-facing content is written at a reading level appropriate to the audience
- Screenshots include alt text and are updated when the UI changes

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 6.5/7.5 (87%) |
| Evaluated | 2026-05-13 |
| Target duration | 25318 ms |
| Target cost | $0.1266 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | After bootstrap, `docs/content/CLAUDE.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim | PASS | Artifact contains the line `USER-EDIT-SENTINEL-DO-NOT-STRIP` under the 'Custom team notes' section, intact and verbatim. |
| c2 | After bootstrap, `docs/content/CLAUDE.md` contains the safe-merge marker `<!-- Merged from user-docs-writer bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged | FAIL | Artifact has `<!-- User documentation section — added by user-docs-writer bootstrap v0.1.0 -->` — different text. The exact required marker `<!-- Merged from user-docs-writer bootstrap v0.1.0 -->` is absent. |
| c3 | After bootstrap, `docs/content/CLAUDE.md` contains the appended user-docs sections — at minimum the `## User Documentation` heading and the `### User Guide Conventions` heading now appear alongside the preserved user content | PASS | Artifact contains both `## User Documentation` and `### User Guide Conventions` headings, appearing after the preserved 'Custom team notes' section. |
| c4 | After bootstrap, `docs/content/CLAUDE.md` contains the `### KB Article Structure` section, which defines the KB article template | PASS | `### KB Article Structure` section is present with a full table defining Title, Summary, Steps/Explanation, Related articles, and Last verified fields. |
| c5 | After bootstrap, `docs/content/CLAUDE.md` contains the `### Available User Docs Skills` section listing the four skill slash commands | PASS | `### Available User Docs Skills` section lists all four: `write-user-guide`, `write-onboarding`, `write-kb-article`, `content-strategy` with slash-command format. |
| c6 | Output includes a manifest summary with a "Files merged" section naming `docs/content/CLAUDE.md` | PASS | Chat response has `### Files merged` with `- \`docs/content/CLAUDE.md\`` listed explicitly. |
| c7 | Output does not claim it overwrote or replaced `docs/content/CLAUDE.md` — the language reflects merge or append, not replacement | PASS | Chat uses 'appended user documentation conventions (safe merge: preserved existing...)' — no replacement or overwrite language. |
| c8 | Output points the reader at next steps referencing at least two of the three skills (`write-onboarding`, `write-kb-article`, `content-strategy`) consistent with the skill's documented manifest | PARTIAL | Chat next steps list all three: `/user-docs-writer:write-onboarding`, `/user-docs-writer:write-kb-article`, `/user-docs-writer:content-strategy` — satisfies the criterion at the PARTIAL ceiling. |

### Notes

The bootstrap correctly preserved the sentinel content and appended all required sections. The only failure is c2: the safe-merge HTML comment uses 'added by' rather than the exact 'Merged from' wording required by the criterion.
