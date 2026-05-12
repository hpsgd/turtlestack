# Bootstrap

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/content/CLAUDE.md` containing a user-authored section. The developer-docs-writer bootstrap skill should preserve that user content while appending the template's missing sections (with a merge marker). Unlike the architect bootstrap, this skill creates only one file — the CLAUDE.md domain guide. The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

> The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/content/CLAUDE.md` is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.
> 
> Read the developer-docs-writer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/product/developer-docs-writer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.
> 
> After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Bootstrap complete. Here's the manifest summary:

## Content Bootstrap Complete

### Files created
- (none — `docs/content/` directory already existed)

### Files merged
- `docs/content/CLAUDE.md` — enhanced with Diataxis framework guidelines, API documentation standards, SDK guide format, docs-as-code practices, tooling recommendations, available developer-docs-writer skills, and developer documentation conventions. User-authored "Custom team notes" section with `USER-EDIT-SENTINEL-DO-NOT-STRIP` sentinel preserved intact. Missing sections appended after the sentinel with merge marker `<!-- Merged from developer-docs-writer bootstrap v0.1.0 -->`.

### Next steps
- Write API reference docs using `/developer-docs-writer:write-api-docs`
- Create SDK guides using `/developer-docs-writer:write-sdk-guide`
- Set up doc linting and link checking in CI (if not already configured)

### Artifacts written

#### `work/docs/content/CLAUDE.md`

```
# Content Domain

This directory contains documentation conventions: Diataxis framework, API docs standards, SDK guide format, and docs-as-code practices.

## What This Domain Covers

- **Developer documentation** — API references, SDK guides, integration guides, migration guides
- **User documentation** — user guides, onboarding content, KB articles
- **Internal documentation** — architecture docs, runbooks, changelogs, post-mortems

## Custom team notes

USER-EDIT-SENTINEL-DO-NOT-STRIP

This section was written by the team and must survive any bootstrap re-run.
It exists to test the safe-merge contract: the bootstrap skill must not
overwrite or remove user-authored content.

<!-- Merged from developer-docs-writer bootstrap v0.1.0 -->

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

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/7.5 (100%) |
| Evaluated | 2026-05-13 |
| Target duration | 33639 ms |
| Target cost | $0.1305 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | After bootstrap, `docs/content/CLAUDE.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim | PASS | Artifact contains the exact line `USER-EDIT-SENTINEL-DO-NOT-STRIP` with surrounding user-authored paragraph intact. |
| c2 | After bootstrap, `docs/content/CLAUDE.md` contains the safe-merge marker `<!-- Merged from developer-docs-writer bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged | PASS | Artifact contains `<!-- Merged from developer-docs-writer bootstrap v0.1.0 -->` placed immediately after the sentinel section. |
| c3 | After bootstrap, `docs/content/CLAUDE.md` contains the appended template sections — at minimum the "Diataxis Framework" and "API Documentation Standards" headings now appear alongside the preserved user content | PASS | Artifact contains `## Diataxis Framework` and `## API Documentation Standards` sections appended after the merge marker. |
| c4 | After bootstrap, `docs/content/CLAUDE.md` contains the "Available Developer Docs Skills" section listing at least one `/developer-docs-writer:` skill invocation path | PASS | Artifact has `## Available Developer Docs Skills` table listing `/developer-docs-writer:write-api-docs`, `/developer-docs-writer:write-sdk-guide`, etc. |
| c5 | Chat output includes a manifest summary that lists `docs/content/CLAUDE.md` under "Files merged" (not "Files created") since the file already existed | PASS | Chat output shows `### Files created: (none)` and `### Files merged: docs/content/CLAUDE.md — enhanced with...` |
| c6 | Output names the merged file individually — a bare "bootstrap complete" without the per-file manifest is not enough | PASS | Chat output explicitly names `docs/content/CLAUDE.md` with a detailed description of what was merged under the Files merged heading. |
| c7 | Output does not claim it overwrote or replaced `docs/content/CLAUDE.md` — the language reflects merge, not replacement | PASS | Chat uses "enhanced with", "preserved intact", and "Missing sections appended after the sentinel" — no overwrite/replace language. |
| c8 | Output points the reader at next steps consistent with the skill's documented manifest (writing API docs, SDK guides, or setting up CI doc linting) | PARTIAL | Chat lists next steps: `/developer-docs-writer:write-api-docs`, `/developer-docs-writer:write-sdk-guide`, and CI doc linting setup. |

### Notes

All criteria fully satisfied. The skill correctly executed the safe-merge pattern: user content and sentinel preserved verbatim, merge marker inserted, template sections appended, and the manifest accurately reflected 'merged' rather than 'created'.
