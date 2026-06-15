---
name: bootstrap
bootstrap-phase: content
description: "Bootstrap the content documentation structure for a project. Creates docs/content/, and writes the developer-docs-writer fragment of the content domain doc with the Diataxis framework and docs-as-code conventions. Idempotent — merges missing sections into existing files without overwriting."
argument-hint: "[project name]"
user-invocable: false
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Bootstrap Content Documentation

Bootstrap the content documentation structure for **$ARGUMENTS**.

## Process

### Step 1: Check and create domain directory

```bash
mkdir -p docs/content/_sections
```

### Step 2: Create or merge files

For each file below, apply the safe merge pattern:
- If file does not exist → create from template
- If file exists → read both, find sections in template missing from file, append missing sections with `<!-- Merged from developer-docs-writer bootstrap v0.1.0 -->`

#### Fragment: `docs/content/_sections/developer-docs-writer.md`

`docs/content/CLAUDE.md` is **assembled by the coordinator** from the fragments in `_sections/` — no plugin
writes it directly, so developer-docs-writer, internal-docs-writer, and user-docs-writer never collide on it.
Write the developer-docs-writer contribution as this fragment. It starts at H2 (the coordinator generates the
`# Content Domain` H1):

```markdown
## What This Domain Covers

- **Developer documentation** — API references, SDK guides, integration guides, migration guides
- **User documentation** — user guides, onboarding content, KB articles
- **Internal documentation** — architecture docs, runbooks, changelogs, post-mortems

## Diataxis Framework

All documentation follows the [Diataxis](https://diataxis.fr/) framework — four modes of documentation, each with a distinct purpose:

| Mode | Purpose | Reader Need | Example |
|------|---------|-------------|---------|
| **Tutorial** | Learning-oriented | "Teach me" | Getting started guide |
| **How-to** | Task-oriented | "Help me do X" | Integrate webhooks |
| **Reference** | Information-oriented | "Give me the facts" | API endpoint list |
| **Explanation** | Understanding-oriented | "Help me understand" | Architecture overview |

### Rules
- Never mix modes in a single document — a tutorial should not become a reference
- Tutorials follow a guided path with a concrete outcome
- How-to guides are goal-oriented and assume basic knowledge
- Reference docs are complete, accurate, and consistently structured
- Explanations provide context and rationale, not step-by-step instructions

## API Documentation Standards

### Required sections for every endpoint
1. **Summary** — one-line description
2. **HTTP method and path** — `GET /v1/users/{id}`
3. **Parameters** — path, query, header, body (with types and constraints)
4. **Request example** — complete, copy-pasteable request
5. **Response examples** — success and error responses with status codes
6. **Error codes** — specific error codes this endpoint may return
7. **Rate limits** — if applicable

### API doc conventions
- Use OpenAPI 3.1 as the source of truth for REST APIs
- Generate reference docs from the OpenAPI spec where possible
- Keep prose descriptions alongside generated docs for context
- Version-specific docs when breaking changes occur

## SDK Guide Format

SDK guides follow a standard structure:
1. **Installation** — package manager commands for all supported platforms
2. **Authentication** — how to configure credentials
3. **Quick start** — minimal working example (< 20 lines)
4. **Core concepts** — key abstractions and patterns
5. **Common tasks** — how-to guides for frequent operations
6. **Error handling** — how the SDK surfaces errors
7. **Migration** — upgrading from previous versions

## Docs-as-Code Practices

- Documentation lives in the repository alongside code (`docs/` directory)
- Documentation changes go through the same PR review process as code
- Use Markdown for all documentation — no binary formats in the repo
- Docs are tested in CI: link checking, spell checking, Markdown linting
- Screenshots and diagrams use Mermaid (embedded) or committed SVG/PNG with alt text

## Tooling

| Tool | Purpose |
|------|---------|
| GitHub (in-repo) | Developer docs in `docs/` — versioned with code |
| GitHub Wiki | Operational content — runbooks, KB articles |
| Mermaid | Diagrams embedded in Markdown |

## Available Developer Docs Skills

| Skill | Purpose |
|-------|---------|
| `/developer-docs-writer:write-api-docs` | Write API reference documentation |
| `/developer-docs-writer:write-sdk-guide` | Write an SDK getting started guide |
| `/developer-docs-writer:write-integration-guide` | Write a third-party integration guide |
| `/developer-docs-writer:write-migration-guide` | Write a version migration guide |

## Developer Docs Conventions

- Every public API endpoint must have reference documentation before release
- API docs are generated from OpenAPI spec where possible, supplemented with prose
- SDK guides include a working quick-start example that can be copy-pasted
- Documentation PRs require review from at least one subject-matter expert
- Broken doc links in CI are treated as build failures
```

### Step 3: Return manifest

After creating/merging all files, output a summary:

```
## Content Bootstrap Complete

### Files created
- `docs/content/_sections/developer-docs-writer.md` — developer-docs-writer's fragment of the content domain doc (assembled into `docs/content/CLAUDE.md` by the coordinator)

### Files merged
- (list any existing files where sections were appended)

### Next steps
- Write API reference docs using `/developer-docs-writer:write-api-docs`
- Create SDK guides using `/developer-docs-writer:write-sdk-guide`
- Set up doc linting and link checking in CI
```
