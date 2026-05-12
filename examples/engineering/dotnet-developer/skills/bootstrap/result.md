# Bootstrap

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/architecture/CLAUDE.md` containing a user-authored section. The dotnet-developer bootstrap skill should preserve that user content while appending the .NET Conventions section (with a merge marker). Unlike the architect bootstrap, this skill does NOT create a new domain directory — it only appends to the existing architecture CLAUDE.md. The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

> The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/architecture/CLAUDE.md` is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`. There is no `.NET Conventions` section yet.
> 
> Read the dotnet-developer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/engineering/dotnet-developer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.
> 
> After the bootstrap completes, output the manifest summary the skill defines (files updated, files merged, next steps).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

**Step 3: Manifest Summary**

## .NET Developer Bootstrap Complete

### Files updated
- `docs/architecture/CLAUDE.md` — appended .NET Conventions section

### Files merged
- `docs/architecture/CLAUDE.md` — preserved existing "Custom team notes" section with USER-EDIT-SENTINEL-DO-NOT-STRIP; appended .NET Conventions at end without overwriting

### Next steps
- Configure Wolverine and Marten in `Program.cs`
- Set up Alba test project for integration testing
- Use `/dotnet-developer:write-endpoint` for new HTTP endpoints
- Use `/dotnet-developer:write-handler` for command/event handlers

### Artifacts written

#### `work/docs/architecture/CLAUDE.md`

```
# Architecture Domain

This directory contains architecture documentation for the project.

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
| Score | 11.5/11.5 (100%) |
| Evaluated | 2026-05-13 |
| Target duration | 26655 ms |
| Target cost | $0.1246 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | After bootstrap, `docs/architecture/CLAUDE.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim | PASS | File artifact line: `USER-EDIT-SENTINEL-DO-NOT-STRIP` appears in the Custom team notes section, unchanged. |
| c2 | After bootstrap, `docs/architecture/CLAUDE.md` contains the safe-merge marker `<!-- Added by dotnet-developer bootstrap v0.1.0 -->` — the .NET Conventions section was appended with the correct marker | PASS | File artifact contains `<!-- Added by dotnet-developer bootstrap v0.1.0 -->` immediately before the `## .NET Conventions` heading. |
| c3 | After bootstrap, `docs/architecture/CLAUDE.md` contains the `.NET Conventions` heading — the section was appended to the file | PASS | File artifact contains `## .NET Conventions` as a heading after the user-authored section. |
| c4 | After bootstrap, `docs/architecture/CLAUDE.md` contains sub-sections for Wolverine and Marten conventions — the technology-specific content was included | PASS | File artifact contains `### Wolverine and Marten` subsection with bullet points for both technologies. |
| c5 | After bootstrap, `docs/architecture/CLAUDE.md` contains a Testing sub-section mentioning Alba and xUnit — the testing conventions were included | PASS | File artifact contains `### Testing` with `**Alba** for integration testing` and `**xUnit** as the test framework`. |
| c6 | After bootstrap, `docs/architecture/CLAUDE.md` contains the Available .NET Skills table referencing `/dotnet-developer:write-endpoint` and `/dotnet-developer:write-handler` | PASS | File artifact contains `### Available .NET Skills` table with both `/dotnet-developer:write-endpoint` and `/dotnet-developer:write-handler`. |
| c7 | Chat output includes a manifest summary with a "Files updated" or equivalent section listing `docs/architecture/CLAUDE.md` | PASS | Chat output has `### Files updated` section listing `docs/architecture/CLAUDE.md — appended .NET Conventions section`. |
| c8 | The skill did NOT create any new domain directory (no new `docs/dotnet/` or similar) — it only modified the existing architecture CLAUDE.md | PASS | Only artifact written is `work/docs/architecture/CLAUDE.md`. No new directories or files created. |
| c9 | Output names the updated file explicitly — a bare "bootstrap complete" without listing `docs/architecture/CLAUDE.md` is not enough | PASS | Chat output explicitly lists `docs/architecture/CLAUDE.md` under both Files updated and Files merged sections. |
| c10 | Output does not claim it overwrote or replaced `docs/architecture/CLAUDE.md` — the language reflects append/merge, not replacement | PASS | Chat output uses `appended` and `preserved existing...section` language; Files merged section explicitly states preservation of user content. |
| c11 | Output points the reader at next steps consistent with the skill's documented manifest — at minimum mentions configuring Wolverine and Marten or using the available skills | PARTIAL | Chat output has `### Next steps` with `Configure Wolverine and Marten in Program.cs` and references to both available skills. |

### Notes

The skill executed flawlessly: user sentinel preserved, merge marker present, all required sections included, no extra directories created, and manifest output was complete and accurate. All criteria met at their ceiling.
