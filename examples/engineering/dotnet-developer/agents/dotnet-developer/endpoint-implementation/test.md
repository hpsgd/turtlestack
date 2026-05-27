---
# Match the model the agent declares (sonnet) in
# plugins/engineering/dotnet-developer/agents/dotnet-developer.md. The runner otherwise
# falls back to the harness default (Haiku), which is not what the
# agent is designed to run on.
target-model: claude-sonnet-4-6
---

# Test: Order processing REST endpoint

Scenario: User asks the .NET developer to implement a REST endpoint for creating and processing orders in a .NET 8 API that uses Wolverine and Marten with event sourcing.

## Prompt

We need a `POST /api/customers/{customerId}/orders` endpoint to create a new order. The request body contains line items (product ID, quantity, unit price). Business rules: a customer cannot have more than 50 active orders at once, and each line item quantity must be between 1 and 100. On success it should return 201 with the new order ID and trigger an `OrderPlaced` event that downstream handlers will pick up. We're using Wolverine for HTTP and Marten for persistence. Can you implement this including tests?

**Wolverine packages — these ARE on NuGet, do NOT substitute plain ASP.NET**:

```xml
<PackageReference Include="WolverineFx.Http" Version="3.*" />
<PackageReference Include="WolverineFx.Marten" Version="3.*" />
<PackageReference Include="Marten" Version="7.*" />
```

Use `[WolverinePost("/api/customers/{customerId}/orders")]` attribute routing. Do NOT fall back to `app.MapPost(...)` minimal-API style. Do NOT throw exceptions for business validation — `LoadAsync` returns `ProblemDetails` (or a `Result<T>`) directly.

**Mandatory output structure — the chat response MUST contain these EXACT `##` headings as written, in this order, BEFORE any summary block.** A bullet-point summary like `✅ Pre-flight done` does NOT satisfy the requirement — the literal heading `## Pre-flight reads` must appear with content beneath it. The judge inspects the chat response for these heading strings:

1. `## Pre-flight reads` — list each Read with absolute path under `/Users/martin/Projects/turtlestack/`. Include `CLAUDE.md`, `.claude/rules/dotnet-stack--jasperfx.md` (state `[not present — assuming Wolverine/Marten conventions]` if missing), `.claude/rules/turtlestack--coding-standards--*.md`. REQUIRED — do not skip even if files are absent.
2. `## Architecture checkpoint` — explicitly raise the decision to introduce the `Order` aggregate (event-sourced via Marten) for stakeholder review BEFORE implementation. State the CRUD-entity alternative considered and why event-sourced is preferred. REQUIRED before any code.
3. `## Implementation` — the code, files, and inline content. Use Wolverine `[WolverinePost]` attribute routing per packages above.
4. `## Tests` — unit + integration test files. Integration test MUST use `AlbaHost` (from `Alba` NuGet package) — NOT `Microsoft.AspNetCore.TestHost.TestServer` with raw `HttpClient`. Show `await using var host = await AlbaHost.For<Program>(...)` or equivalent in the integration test file.
5. `## Tests cover` — explicitly enumerate the three test scenarios as a bulleted list: happy path (201 with Location header shape `/api/customers/{customerId}/orders/{orderId}` asserted), 51st active order rejected (seed 50 active orders for the customer then expect 422), quantity 0 AND quantity 101 rejected.
6. `## Verification` — build/test commands and expected output (or `[would run: dotnet build && dotnet test]` if you cannot execute).

A condensed summary alone with check-mark bullets fails this prompt. Reproduce the headings literally with full content.

Implementation requirements (Wolverine + Marten conventions):

- **Pre-flight section** at top — list files Read: `CLAUDE.md`, `.claude/rules/*` (especially `dotnet-stack--jasperfx.md` if present). State assumptions made if files missing.
- **Wolverine handler structure** — split `LoadAsync` (pre-conditions: customer exists, active order count < 50) from `Handle` (mutation). LoadAsync returns the loaded entities to inject into Handle.
- **Cascading messages** — `Handle` RETURNS `OrderPlaced` event as the cascading message (Wolverine convention), not raised inline via `IMessageBus`.
- **`IDocumentSession`** is injected by Wolverine — do NOT create sessions from `IDocumentStore`.
- **Command AND event as C# `record` types** with immutable properties — not classes:
  ```csharp
  public record CreateOrderCommand(Guid CustomerId, IReadOnlyList<LineItem> Items);
  public record OrderPlaced(Guid OrderId, Guid CustomerId, decimal Total);
  ```
- **Response DTO** separate from aggregate — never expose aggregate internals via the API response.
- **Endpoint route** EXACTLY `POST /api/customers/{customerId}/orders`, mounted via Wolverine HTTP `[WolverinePost]` attribute.
- **Tests required (BOTH)**:
  - Unit: `WhenCreatingAnOrder` class with Shouldly assertions on the handler in isolation.
  - Integration: `WhenPostingAnOrder` class spinning up an `AlbaHost` against the real Wolverine + Marten stack, asserting 201 + response body + the `OrderPlaced` event was published. The integration test project MUST add a `Testcontainers.PostgreSql` package reference and use it to spin up Postgres for Marten — do NOT point at a hard-coded `localhost` SQL Server. Show the `<PackageReference Include="Testcontainers.PostgreSql" .../>` line in the .csproj content.
- **Response location header** MUST be exactly `/api/customers/{customerId}/orders/{orderId}` — assert the full path shape in the integration test, not just that the customerId substring appears.
- **Command shape** MUST follow the prompt example exactly — `CreateOrderCommand(Guid CustomerId, IReadOnlyList<LineItem> Items)` carrying customerId in the record (not only as a route parameter).
- **`Handle` method MUST return both the response DTO AND the `OrderPlaced` cascade event** as a tuple (Wolverine cascading). Do NOT split the event return into a separate `Cascades()` method.
- **Validation**: line item quantity 1-100 and `active_order_count < 50` enforced in LoadAsync, returning `ProblemDetails` with 422 if violated.

A few specifics for the response:

- Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
- Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
- For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
- When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
- Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Criteria

- [ ] PASS: Agent reads CLAUDE.md and checks `.claude/rules/` including `dotnet-stack--jasperfx.md` before writing code
- [ ] PASS: Agent uses hierarchical URL `/api/customers/{customerId}/orders` — does not propose a flat `/api/orders`
- [ ] PASS: Agent separates LoadAsync (pre-condition: customer exists, active order count < 50) from Handle (pure business logic returning OrderPlaced event)
- [ ] PASS: Agent uses `IDocumentSession` injected by Wolverine — does not create sessions from `IDocumentStore` directly
- [ ] PASS: Agent returns `OrderPlaced` event as a cascading message from Handle, not inline side-effect processing
- [ ] PASS: Agent produces both a unit test (WhenCreatingAnOrder class, Shouldly assertions) and an integration test (Alba + Testcontainers)
- [ ] PASS: Agent raises a decision checkpoint before creating the Order aggregate (architecture decision)
- [ ] PASS: Command and event are C# records (not classes), with immutable properties
- [ ] PARTIAL: Agent includes a response DTO separate from the aggregate — does not expose aggregate internals directly

## Output expectations

- [ ] PASS: Output's endpoint route is exactly `POST /api/customers/{customerId}/orders`, mounted via Wolverine HTTP attributes/conventions, with the customerId bound from the route
- [ ] PASS: Output's command record (e.g. `CreateOrder`) is a C# `record` with `init`-only or positional-immutable properties — not a class with mutable setters — and contains the line items collection and customerId
- [ ] PASS: Output enforces both business rules in code: line item quantity range [1,100] (validated via FluentValidation or in LoadAsync) and the customer's active-order count below 50 checked against persisted state
- [ ] PASS: Output's `LoadAsync` (or equivalent pre-condition step) loads the customer / counts active orders and returns a Problem Details / 4xx response when pre-conditions fail — not throwing exceptions for business validation
- [ ] PASS: Output's `Handle` returns the new domain event(s) (`OrderPlaced` and any cascading messages) plus the HTTP response — it does NOT execute side effects inline
- [ ] PASS: Output uses an `IDocumentSession` parameter injected by Wolverine and never instantiates a session from `IDocumentStore` directly, and never calls `SaveChangesAsync` manually
- [ ] PASS: Output's response is 201 Created with a Location header pointing to `/api/customers/{customerId}/orders/{orderId}` and a response DTO that does NOT directly serialise the aggregate
- [ ] PASS: Output includes both a unit test class named in the `When...` style (e.g. `WhenCreatingAnOrder`) using Shouldly assertions, and an integration test using Alba + Testcontainers for Postgres
- [ ] PASS: Output's tests cover the happy path plus both rule violations (51st active order rejected, quantity 0 / 101 rejected) with explicit Given/When/Then or arrange/act/assert structure
- [ ] PARTIAL: Output flags the architecture decision (introducing the Order aggregate) for stakeholder review before implementing rather than just creating it
