---
name: bootstrap
bootstrap-phase: content
description: "Bootstrap the user documentation conventions for a project. Creates docs/content/, and writes the user-docs-writer fragment of the content domain doc — user guide, onboarding, and KB article conventions. Idempotent — merges missing sections into existing files without overwriting."
argument-hint: "[project name]"
user-invocable: false
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Bootstrap User Documentation

Bootstrap the user documentation conventions for **$ARGUMENTS**.

## Process

### Step 1: Check and create domain directory

```bash
mkdir -p docs/content/_sections
```

### Step 2: Create or merge files

For each file below, apply the safe merge pattern:
- If file does not exist → create from template
- If file exists → read both, find sections in template missing from file, append missing sections with `<!-- Merged from user-docs-writer bootstrap v0.1.0 -->`

#### Fragment: `docs/content/_sections/user-docs-writer.md`

`docs/content/CLAUDE.md` is **assembled by the coordinator** from the fragments in `_sections/` — no plugin
writes it directly, so developer-docs-writer, internal-docs-writer, and user-docs-writer never collide on it.
Write the user-documentation contribution as this fragment. It starts at H2 (the coordinator generates the
`# Content Domain` H1):

```markdown
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

### Step 3: Return manifest

After creating/merging all files, output a summary:

```
## User Docs Bootstrap Complete

### Files created
- `docs/content/_sections/user-docs-writer.md` — user-docs-writer's fragment of the content domain doc (assembled into `docs/content/CLAUDE.md` by the coordinator)

### Files merged
- (list the fragment here instead if it already existed and sections were appended, or "none")

### Next steps
- Write onboarding content using `/user-docs-writer:write-onboarding`
- Create initial KB articles using `/user-docs-writer:write-kb-article`
- Define content strategy using `/user-docs-writer:content-strategy`
```

## Rules

- **Write only your own fragment.** `docs/content/CLAUDE.md` is assembled by the coordinator; this skill writes `docs/content/_sections/user-docs-writer.md` and nothing else. The developer-docs-writer and internal-docs-writer write their own fragments — there is no shared file to clobber.
- **Safe-merge the fragment, idempotent by design.** If the fragment exists, preserve user-authored content and append only missing template sections with the merge marker — never overwrite. Running twice produces no duplicate sections.

## Output Format

The manifest in Step 3 is the output. Report files created, files merged, and next steps. Nothing else.
