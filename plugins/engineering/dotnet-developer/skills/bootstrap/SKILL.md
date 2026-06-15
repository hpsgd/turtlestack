---
name: bootstrap
bootstrap-phase: stack
description: "Bootstrap .NET conventions into the architecture documentation. Writes the dotnet-developer fragment of the architecture domain doc. Idempotent — merges missing sections into existing files without overwriting."
argument-hint: "[project name]"
user-invocable: false
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Bootstrap .NET Conventions

Bootstrap .NET development conventions for **$ARGUMENTS**.

This skill writes only its own fragment — `docs/architecture/_sections/dotnet-developer.md`. The architecture domain `CLAUDE.md` is assembled by the coordinator from every fragment in `_sections/`, so this skill never collides with the architect or the other stack developers.

## Process

### Step 1: Create the sections directory

```bash
mkdir -p docs/architecture/_sections
```

### Step 2: Write the .NET fragment

`docs/architecture/CLAUDE.md` is **assembled by the coordinator** from the fragments in `_sections/` — no plugin writes it directly, so this skill and the architect never collide on it. Write the .NET contribution as `docs/architecture/_sections/dotnet-developer.md`. It starts at H2 (the coordinator generates the `# Architecture Domain` H1).

Apply the safe merge pattern:

- If the fragment does not exist → create it from the template below
- If the fragment exists → read both, find sections in the template missing from the file, append only the missing sections with the marker `<!-- Added by dotnet-developer bootstrap v0.1.0 -->`

```markdown
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

### Step 3: Return manifest

After creating/merging all files, output a summary:

```
## .NET Developer Bootstrap Complete

### Files created
- `docs/architecture/_sections/dotnet-developer.md` — dotnet-developer's fragment of the architecture domain doc (assembled into `docs/architecture/CLAUDE.md` by the coordinator)

### Files merged
- (list the fragment here if it already existed and missing sections were appended, or "none")

### Next steps
- Configure Wolverine and Marten in `Program.cs`
- Set up Alba test project for integration testing
- Use `/dotnet-developer:write-endpoint` for new HTTP endpoints
- Use `/dotnet-developer:write-handler` for command/event handlers
```

## Rules

- **Write only your own fragment.** `docs/architecture/CLAUDE.md` is assembled by the coordinator; this skill writes `docs/architecture/_sections/dotnet-developer.md` and nothing else. The architect and the other stack developers write their own fragments — there is no shared file to clobber.
- **Safe-merge the fragment, idempotent by design.** If the fragment exists, preserve user-authored content and append only missing template sections with the marker — never overwrite. Running twice produces no duplicate sections.
