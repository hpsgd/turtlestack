# Bootstrap

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/content/_sections/developer-docs-writer.md` fragment containing a user-authored section. The developer-docs-writer bootstrap skill should preserve that user content while appending the template's missing sections (with a merge marker). The skill writes only its own fragment under `docs/content/_sections/` — `docs/content/CLAUDE.md` is assembled later by the coordinator, so the three content writers never collide on it. The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

> The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/content/_sections/developer-docs-writer.md` fragment is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.
> 
> Read the developer-docs-writer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/product/developer-docs-writer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.
> 
> After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Content Bootstrap Complete

### Files created
- (none — file already existed)

### Files merged
- `docs/content/_sections/developer-docs-writer.md` — merged 8 missing sections from bootstrap template:
  - What This Domain Covers
  - Diataxis Framework
  - API Documentation Standards
  - SDK Guide Format
  - Docs-as-Code Practices
  - Tooling
  - Available Developer Docs Skills
  - Developer Docs Conventions
  - User-authored "Custom team notes" section preserved ✓

### Next steps
- Write API reference docs using `/developer-docs-writer:write-api-docs`
- Create SDK guides using `/developer-docs-writer:write-sdk-guide`
- Set up doc linting and link checking in CI

### Artifacts written

#### `work/docs/content/_sections/developer-docs-writer.md`

```
## Custom team notes

USER-EDIT-SENTINEL-DO-NOT-STRIP

This section was written by the team and must survive any bootstrap re-run.
It exists to test the safe-merge contract: the bootstrap skill must not
overwrite or remove user-authored content.

<!-- Merged from developer-docs-writer bootstrap v0.1.0 -->

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

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 9.5/9.5 (100%) |
| Evaluated | 2026-06-15 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 28102 ms |
| Target cost | $0.0802 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | PASS: After bootstrap, `docs/content/_sections/developer-docs-writer.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim | PASS | The artifact file contains 'USER-EDIT-SENTINEL-DO-NOT-STRIP' on its own line, with the full 'Custom team notes' section intact above the merge marker. |
| c2 | PASS: After bootstrap, `docs/content/_sections/developer-docs-writer.md` contains the safe-merge marker `<!-- Merged from developer-docs-writer bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged | PASS | Artifact contains exactly '<!-- Merged from developer-docs-writer bootstrap v0.1.0 -->' between the user content and the appended template sections. |
| c3 | PASS: After bootstrap, `docs/content/_sections/developer-docs-writer.md` contains the appended template sections — at minimum the "Diataxis Framework" and "API Documentation Standards" headings now appear alongside the preserved user content | PASS | Artifact contains '## Diataxis Framework' and '## API Documentation Standards' headings with full content, appearing after the user section. |
| c4 | PASS: After bootstrap, `docs/content/_sections/developer-docs-writer.md` contains the "Available Developer Docs Skills" section listing at least one `/developer-docs-writer:` skill invocation path | PASS | Artifact contains '## Available Developer Docs Skills' section with '/developer-docs-writer:write-api-docs', '/developer-docs-writer:write-sdk-guide', and two more skill paths. |
| c5 | PASS: The skill did not create or write `docs/content/CLAUDE.md` — that file is the coordinator's to assemble from the `_sections/` fragments | PASS | No artifact for 'docs/content/CLAUDE.md' appears in the written files. Only 'work/docs/content/_sections/developer-docs-writer.md' was written. |
| c6 | PASS: Chat output includes a manifest summary that lists `docs/content/_sections/developer-docs-writer.md` under "Files merged" (not "Files created") since the fragment already existed | PASS | Chat output shows '### Files merged' section listing 'docs/content/_sections/developer-docs-writer.md' and '### Files created' shows '(none — file already existed)'. |
| c7 | PASS: Output names the merged fragment individually — a bare "bootstrap complete" without the per-file manifest is not enough | PASS | Chat output lists 'docs/content/_sections/developer-docs-writer.md' explicitly under Files merged with 8 named sections enumerated. |
| c8 | PASS: Output does not claim it overwrote or replaced the fragment — the language reflects merge, not replacement | PASS | Output uses 'merged 8 missing sections from bootstrap template' and 'User-authored "Custom team notes" section preserved ✓' — no overwrite/replace language. |
| c9 | PARTIAL: Output points the reader at next steps consistent with the skill's documented manifest (writing API docs, SDK guides, or setting up CI doc linting) | PARTIAL | Chat output '### Next steps' lists writing API reference docs, SDK guides, and setting up doc linting/link checking in CI — all consistent with the skill manifest. |

### Notes

The skill executed flawlessly: user content preserved with sentinel intact, merge marker present, all template sections appended, no CLAUDE.md created, and the manifest summary correctly categorized the file as merged not created. All criteria met at their maximum possible score.
