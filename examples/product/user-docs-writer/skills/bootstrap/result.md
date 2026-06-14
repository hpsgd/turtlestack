# Bootstrap

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/content/_sections/user-docs-writer.md` fragment containing a user-authored section. The user-docs-writer bootstrap skill should preserve that user content while appending the missing user-documentation sections (with a merge marker). The skill writes only its own fragment under `docs/content/_sections/` — `docs/content/CLAUDE.md` is assembled later by the coordinator, so the three content writers never collide on it. The test focuses on the safe-merge contract and the manifest output. The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

> The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/content/_sections/user-docs-writer.md` fragment is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.
> 
> Read the user-docs-writer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/product/user-docs-writer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.
> 
> After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## User Docs Bootstrap Complete

### Files created
- None (existing file merged)

### Files merged
- `docs/content/_sections/user-docs-writer.md` — user-docs-writer's fragment of the content domain doc. User-authored "Custom team notes" section preserved; template sections appended with merge marker.

### Next steps
- Write onboarding content using `/user-docs-writer:write-onboarding`
- Create initial KB articles using `/user-docs-writer:write-kb-article`
- Define content strategy using `/user-docs-writer:content-strategy`

### Artifacts written

#### `work/docs/content/_sections/user-docs-writer.md`

```
## Custom team notes

USER-EDIT-SENTINEL-DO-NOT-STRIP

This section was written by the team and must survive any bootstrap re-run.
It exists to test the safe-merge contract: the bootstrap skill must not
overwrite or remove user-authored content.

<!-- Merged from user-docs-writer bootstrap v0.1.0 -->

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
| Score | 8.5/8.5 (100%) |
| Evaluated | 2026-06-15 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 28508 ms |
| Target cost | $0.0671 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | After bootstrap, `docs/content/_sections/user-docs-writer.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim | PASS | Artifact line 3: `USER-EDIT-SENTINEL-DO-NOT-STRIP` present verbatim, with the surrounding 'Custom team notes' section intact above the merge marker. |
| c2 | After bootstrap, `docs/content/_sections/user-docs-writer.md` contains the safe-merge marker `<!-- Merged from user-docs-writer bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged | PASS | Artifact line 8: `<!-- Merged from user-docs-writer bootstrap v0.1.0 -->` appears between the preserved user content and the appended template sections. |
| c3 | After bootstrap, `docs/content/_sections/user-docs-writer.md` contains the appended user-docs sections — at minimum the `## User Documentation` heading and the `### User Guide Conventions` heading now appear alongside the preserved user content | PASS | Artifact contains `## User Documentation` (line 10) and `### User Guide Conventions` (line 19) both present after the merge marker. |
| c4 | After bootstrap, `docs/content/_sections/user-docs-writer.md` contains the `### KB Article Structure` section, which defines the KB article template | PASS | Artifact contains `### KB Article Structure` with a table defining Title, Summary, Steps/Explanation, Related articles, and Last verified sections. |
| c5 | After bootstrap, `docs/content/_sections/user-docs-writer.md` contains the `### Available User Docs Skills` section listing the four skill slash commands | PASS | Artifact contains `### Available User Docs Skills` table listing all four: `write-user-guide`, `write-onboarding`, `write-kb-article`, `content-strategy`. |
| c6 | The skill did not create or write `docs/content/CLAUDE.md` — that file is the coordinator's to assemble from the `_sections/` fragments | PASS | Chat output: 'Files created: None (existing file merged)'. Only artifact written is `work/docs/content/_sections/user-docs-writer.md`. No CLAUDE.md artifact present. |
| c7 | Output includes a manifest summary naming `docs/content/_sections/user-docs-writer.md` | PASS | Chat output 'Files merged' section explicitly names `docs/content/_sections/user-docs-writer.md` with a description of what was preserved and appended. |
| c8 | Output does not claim it overwrote or replaced the fragment — the language reflects merge or append, not replacement | PASS | Chat output: 'Files created: None (existing file merged)' and 'User-authored "Custom team notes" section preserved; template sections appended with merge marker.' — no overwrite language. |
| c9 | Output points the reader at next steps referencing at least two of the three skills (`write-onboarding`, `write-kb-article`, `content-strategy`) consistent with the skill's documented manifest | PARTIAL | Chat output 'Next steps' lists all three: `/user-docs-writer:write-onboarding`, `/user-docs-writer:write-kb-article`, `/user-docs-writer:content-strategy`. |

### Notes

The skill executed the safe-merge contract perfectly: sentinel line preserved, merge marker inserted, all template sections appended, CLAUDE.md untouched, and manifest language accurately reflects a merge not a replacement. All criteria met at ceiling.
