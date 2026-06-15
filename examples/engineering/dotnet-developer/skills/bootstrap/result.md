# Bootstrap

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/architecture/_sections/dotnet-developer.md` fragment containing a user-authored section. The dotnet-developer bootstrap skill should preserve that user content while appending the .NET Conventions section (with a merge marker). It writes only its own fragment — `docs/architecture/CLAUDE.md` is assembled by the coordinator from the fragments in `_sections/`, so this skill never touches it. The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

> The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/architecture/_sections/dotnet-developer.md` fragment is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`. There is no `.NET Conventions` section yet.
> 
> Read the dotnet-developer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/engineering/dotnet-developer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.
> 
> After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## .NET Developer Bootstrap Complete

### Files created
- (none — fragment already existed)

### Files merged
- `docs/architecture/_sections/dotnet-developer.md` — appended `.NET Conventions` section with 6 subsections (Wolverine & Marten, Event Sourcing & CQRS, Testing, Project Structure, Coding Style, Tooling, Skills). User-authored "Custom team notes" section preserved intact.

### Next steps
- Configure Wolverine and Marten in `Program.cs`
- Set up Alba test project for integration testing
- Use `/dotnet-developer:write-endpoint` for new HTTP endpoints
- Use `/dotnet-developer:write-handler` for command/event handlers

### Artifacts written

#### `work/docs/architecture/_sections/dotnet-developer.md`

```
<!-- dotnet-developer fragment of the architecture domain doc. Assembled into docs/architecture/CLAUDE.md by the coordinator. -->

## Custom team notes

USER-EDIT-SENTINEL-DO-NOT-STRIP

This section was written by the team and must survive any bootstrap re-run.
It exists to test the safe-merge contract: the bootstrap skill must not
overwrite or remove user-authored content.

<!-- Added by dotnet-developer bootstrap v0.1.0 -->
## .NET Conventions

### Wolverine and Marten

- **Wolverine** for message handling (commands, events, HTTP endpoints)
- **Marten** for document DB and event store (PostgreSQL-backed)
- Use Wolverine's `[WolverineHandler]` conventions — no manual DI wiring
- Prefer Marten's `IDocumentSession` over raw SQL for document operations

### Event Sourcing and CQRS

- Commands mutate state via event streams — never update documents directly for event-sourced aggregates
- Projections build read models from event streams
- Use Marten's inline projections for simple cases, async projections for complex
- Event naming: past tense, domain language (e.g., `OrderPlaced`, `PaymentReceived`)
- Stream identity: `{AggregateType}-{id}` convention

### Testing

- **Alba** for integration testing of HTTP endpoints (in-process test server)
- **xUnit** as the test framework
- **NSubstitute** for mocking dependencies
- **Shouldly** for fluent assertions
- Test naming: `Should_{expected_behaviour}_When_{condition}`
- Use `IAlbaHost` for end-to-end handler testing with real Marten sessions

### Project Structure

```
src/
├── {Project}.Api/           # HTTP endpoints, middleware
├── {Project}.Domain/        # Aggregates, events, domain logic
├── {Project}.Application/   # Handlers (commands, queries, events)
├── {Project}.Infrastructure/ # Marten config, external services
tests/
├── {Project}.Tests.Unit/
├── {Project}.Tests.Integration/
└── {Project}.Tests.Alba/     # Alba HTTP integration tests
```

### Coding Style

- Nullable reference types enabled (`<Nullable>enable</Nullable>`)
- File-scoped namespaces
- Primary constructors for DI (C# 12+)
- Records for DTOs, events, and value objects
- `sealed` by default — unseal only when inheritance is needed

### .NET Tooling

| Tool | Purpose |
|------|---------|
| [SonarCloud](https://sonarcloud.io) | .NET code quality and coverage gate |
| [GitHub Actions](https://docs.github.com/en/actions) | `dotnet test` in CI on every PR |

### Available .NET Skills

| Skill | Purpose |
|-------|---------|
| `/dotnet-developer:write-endpoint` | Write a Wolverine HTTP endpoint |
| `/dotnet-developer:write-handler` | Write a Wolverine command/event handler |

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 10.5/10.5 (100%) |
| Evaluated | 2026-06-15 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 32309 ms |
| Target cost | $0.0652 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | After bootstrap, `docs/architecture/_sections/dotnet-developer.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim | PASS | Artifact line: 'USER-EDIT-SENTINEL-DO-NOT-STRIP' appears in the file under the '## Custom team notes' section, intact. |
| c2 | After bootstrap, `docs/architecture/_sections/dotnet-developer.md` contains the safe-merge marker `<!-- Added by dotnet-developer bootstrap v0.1.0 -->` — the .NET Conventions section was appended with the correct marker | PASS | Artifact contains '<!-- Added by dotnet-developer bootstrap v0.1.0 -->' immediately before the '## .NET Conventions' heading. |
| c3 | After bootstrap, `docs/architecture/_sections/dotnet-developer.md` contains the `.NET Conventions` heading — the section was appended to the fragment | PASS | Artifact contains '## .NET Conventions' as a top-level section heading after the user-authored content. |
| c4 | After bootstrap, `docs/architecture/_sections/dotnet-developer.md` contains sub-sections for Wolverine and Marten conventions — the technology-specific content was included | PASS | '### Wolverine and Marten' subsection present with bullet points covering IDocumentSession, WolverineHandler conventions, and Marten usage. |
| c5 | After bootstrap, `docs/architecture/_sections/dotnet-developer.md` contains a Testing sub-section mentioning Alba and xUnit — the testing conventions were included | PASS | '### Testing' subsection explicitly lists 'Alba for integration testing' and 'xUnit as the test framework' with usage details. |
| c6 | After bootstrap, `docs/architecture/_sections/dotnet-developer.md` contains the Available .NET Skills table referencing `/dotnet-developer:write-endpoint` and `/dotnet-developer:write-handler` | PASS | '### Available .NET Skills' table in artifact lists both `/dotnet-developer:write-endpoint` and `/dotnet-developer:write-handler` with descriptions. |
| c7 | Chat output includes a manifest summary with a "Files created" or equivalent section listing `docs/architecture/_sections/dotnet-developer.md` | PASS | Chat output has '### Files merged' section explicitly listing `docs/architecture/_sections/dotnet-developer.md` — equivalent to 'Files created' given existing fragment. |
| c8 | The skill did NOT write `docs/architecture/CLAUDE.md` and did NOT create any new domain directory — that file is coordinator-assembled, and the skill writes only its own fragment under `_sections/` | PASS | Only artifact written is `work/docs/architecture/_sections/dotnet-developer.md`. No `CLAUDE.md` or domain directory appears in the artifacts. |
| c9 | Output names the written fragment explicitly — a bare "bootstrap complete" without listing `docs/architecture/_sections/dotnet-developer.md` is not enough | PASS | Chat output under '### Files merged' explicitly names `docs/architecture/_sections/dotnet-developer.md`. |
| c10 | Output does not claim it overwrote or replaced `docs/architecture/_sections/dotnet-developer.md` — the language reflects append/merge, not replacement | PASS | Chat uses 'Files merged' and 'appended .NET Conventions section' — no language of overwrite or replacement. |
| c11 | Output points the reader at next steps consistent with the skill's documented manifest — at minimum mentions configuring Wolverine and Marten or using the available skills | PARTIAL | '### Next steps' lists 'Configure Wolverine and Marten in Program.cs', 'Set up Alba test project', and usage of both available skills. |

### Notes

The skill executed flawlessly: sentinel preserved, merge marker correct, all subsections present, no coordinator file touched, and manifest language reflects append semantics throughout. All criteria met at ceiling.
