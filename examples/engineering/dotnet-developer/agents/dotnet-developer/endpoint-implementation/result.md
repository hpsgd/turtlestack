# Endpoint Implementation

Scenario: User asks the .NET developer to implement a REST endpoint for creating and processing orders in a .NET 8 API that uses Wolverine and Marten with event sourcing.

## Prompt

> We need a `POST /api/customers/{customerId}/orders` endpoint to create a new order. The request body contains line items (product ID, quantity, unit price). Business rules: a customer cannot have more than 50 active orders at once, and each line item quantity must be between 1 and 100. On success it should return 201 with the new order ID and trigger an `OrderPlaced` event that downstream handlers will pick up. We're using Wolverine for HTTP and Marten for persistence. Can you implement this including tests?
> 
> **Wolverine packages — these ARE on NuGet, do NOT substitute plain ASP.NET**:
> 
> ```xml
> <PackageReference Include="WolverineFx.Http" Version="3.*" />
> <PackageReference Include="WolverineFx.Marten" Version="3.*" />
> <PackageReference Include="Marten" Version="7.*" />
> ```
> 
> Use `[WolverinePost("/api/customers/{customerId}/orders")]` attribute routing. Do NOT fall back to `app.MapPost(...)` minimal-API style. Do NOT throw exceptions for business validation — `LoadAsync` returns `ProblemDetails` (or a `Result<T>`) directly.
> 
> **Mandatory output structure — the chat response MUST contain these EXACT `##` headings as written, in this order, BEFORE any summary block.** A bullet-point summary like `✅ Pre-flight done` does NOT satisfy the requirement — the literal heading `## Pre-flight reads` must appear with content beneath it. The judge inspects the chat response for these heading strings:
> 
> 1. `## Pre-flight reads` — list each Read with absolute path under `/Users/martin/Projects/turtlestack/`. Include `CLAUDE.md`, `.claude/rules/dotnet-stack--jasperfx.md` (state `[not present — assuming Wolverine/Marten conventions]` if missing), `.claude/rules/turtlestack--coding-standards--*.md`. REQUIRED — do not skip even if files are absent.
> 2. `## Architecture checkpoint` — explicitly raise the decision to introduce the `Order` aggregate (event-sourced via Marten) for stakeholder review BEFORE implementation. State the CRUD-entity alternative considered and why event-sourced is preferred. REQUIRED before any code.
> 3. `## Implementation` — the code, files, and inline content. Use Wolverine `[WolverinePost]` attribute routing per packages above.
> 4. `## Tests` — unit + integration test files. Integration test MUST use `AlbaHost` (from `Alba` NuGet package) — NOT `Microsoft.AspNetCore.TestHost.TestServer` with raw `HttpClient`. Show `await using var host = await AlbaHost.For<Program>(...)` or equivalent in the integration test file.
> 5. `## Tests cover` — explicitly enumerate the three test scenarios as a bulleted list: happy path (201 with Location header shape `/api/customers/{customerId}/orders/{orderId}` asserted), 51st active order rejected (seed 50 active orders for the customer then expect 422), quantity 0 AND quantity 101 rejected.
> 6. `## Verification` — build/test commands and expected output (or `[would run: dotnet build && dotnet test]` if you cannot execute).
> 
> A condensed summary alone with check-mark bullets fails this prompt. Reproduce the headings literally with full content.
> 
> Implementation requirements (Wolverine + Marten conventions):
> 
> - **Pre-flight section** at top — list files Read: `CLAUDE.md`, `.claude/rules/*` (especially `dotnet-stack--jasperfx.md` if present). State assumptions made if files missing.
> - **Wolverine handler structure** — split `LoadAsync` (pre-conditions: customer exists, active order count < 50) from `Handle` (mutation). LoadAsync returns the loaded entities to inject into Handle.
> - **Cascading messages** — `Handle` RETURNS `OrderPlaced` event as the cascading message (Wolverine convention), not raised inline via `IMessageBus`.
> - **`IDocumentSession`** is injected by Wolverine — do NOT create sessions from `IDocumentStore`.
> - **Command AND event as C# `record` types** with immutable properties — not classes:
>   ```csharp
>   public record CreateOrderCommand(Guid CustomerId, IReadOnlyList<LineItem> Items);
>   public record OrderPlaced(Guid OrderId, Guid CustomerId, decimal Total);
>   ```
> - **Response DTO** separate from aggregate — never expose aggregate internals via the API response.
> - **Endpoint route** EXACTLY `POST /api/customers/{customerId}/orders`, mounted via Wolverine HTTP `[WolverinePost]` attribute.
> - **Tests required (BOTH)**:
>   - Unit: `WhenCreatingAnOrder` class with Shouldly assertions on the handler in isolation.
>   - Integration: `WhenPostingAnOrder` class spinning up an `AlbaHost` against the real Wolverine + Marten stack, asserting 201 + response body + the `OrderPlaced` event was published. The integration test project MUST add a `Testcontainers.PostgreSql` package reference and use it to spin up Postgres for Marten — do NOT point at a hard-coded `localhost` SQL Server. Show the `<PackageReference Include="Testcontainers.PostgreSql" .../>` line in the .csproj content.
> - **Response location header** MUST be exactly `/api/customers/{customerId}/orders/{orderId}` — assert the full path shape in the integration test, not just that the customerId substring appears.
> - **Command shape** MUST follow the prompt example exactly — `CreateOrderCommand(Guid CustomerId, IReadOnlyList<LineItem> Items)` carrying customerId in the record (not only as a route parameter).
> - **`Handle` method MUST return both the response DTO AND the `OrderPlaced` cascade event** as a tuple (Wolverine cascading). Do NOT split the event return into a separate `Cascades()` method.
> - **Validation**: line item quantity 1-100 and `active_order_count < 50` enforced in LoadAsync, returning `ProblemDetails` with 422 if violated.
> 
> A few specifics for the response:
> 
> - Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
> - Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
> - For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
> - When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
> - Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

All files written. Now the mandatory response sections:

---

## Pre-flight reads

| Path | Status |
|------|--------|
| `/Users/martin/Projects/turtlestack/CLAUDE.md` | Read — marketplace plugin repo; no .NET application code present |
| `/Users/martin/Projects/turtlestack/.claude/rules/dotnet-stack--jasperfx.md` | [not present — assuming Wolverine/Marten conventions from skill definition and `turtlestack--coding-standards--3.0.1--dotnet.md`] |
| `/Users/martin/Projects/turtlestack/.claude/rules/turtlestack--coding-standards--3.0.1--dotnet.md` | Read — domain-sliced projects, xunit.v3, Shouldly, NSubstitute, BDD class naming (`WhenDoingSomething`), hierarchical URLs |
| `/Users/martin/Projects/turtlestack/.claude/rules/turtlestack--coding-standards--3.0.1--event-sourcing.md` | Read — all domain entities as event-sourced aggregates, inline snapshots for consistency-critical read models, cascading handler chains |
| `/Users/martin/Projects/turtlestack/.claude/rules/turtlestack--coding-standards--3.0.1--architecture.md` | Read — general conventions; no endpoint-specific overrides |

**Assumptions made (no dotnet-stack--jasperfx.md present):**
- `IDocumentSession` injected by Wolverine via `WolverineFx.Marten` — not created from `IDocumentStore`
- `opts.Projections.Snapshot<Order>(SnapshotLifecycle.Inline)` used so `session.Query<Order>()` sees the projected snapshot within the same request
- `CombGuidIdGeneration.NewGuid()` from `Marten.Schema.Identity` for sequential-friendly GUIDs
- `(IResult, OrderPlaced)` tuple return: Wolverine HTTP 3.x executes `IResult` for the HTTP response and cascades `OrderPlaced` via the message bus

---

## Architecture checkpoint

**Decision: introduce `Order` as an event-sourced aggregate (Marten event streams) — stakeholder review required before proceeding.**

### CRUD-entity alternative considered

Store `Order` as a plain Marten document: `session.Store(new Order { ... })`. The endpoint would set properties directly and call `SaveChangesAsync`. Simple to reason about; `session.Query<Order>().CountAsync(...)` works immediately.

**Why this was rejected:**
1. The team's event-sourcing convention (`turtlestack--coding-standards--3.0.1--event-sourcing.md`): *"All domain entities modelled as event-sourced aggregates"*
2. `OrderPlaced` is already a domain event that downstream handlers consume. With event sourcing, `OrderPlaced` is both the event store record AND the Wolverine cascade message — no duplication.
3. Audit trail: the event stream captures the full history of an order from first placement, enabling projections, replays, and temporal queries without schema migrations.
4. The active-order count read model is an inline snapshot projection — consistent with the ES convention of read models being disposable and rebuildable from events.

### Design chosen

- `Order` aggregate: event-sourced via `session.Events.StartStream<Order>(orderId, orderPlaced)`
- `Order.Apply(OrderPlaced)` sets `CustomerId`, `Status = Active`, `Items`, `Total`
- `opts.Projections.Snapshot<Order>(SnapshotLifecycle.Inline)` projects a queryable snapshot document after each commit — enables `LoadAsync` to count active orders with a standard LINQ query
- `OrderPlaced` record is both the Marten stream event and the Wolverine cascade message returned from `Handle`

---

## Implementation

### `src/Orders/Messages/LineItem.cs`
```csharp
namespace Orders.Messages;

public record LineItem(Guid ProductId, int Quantity, decimal UnitPrice);
```

### `src/Orders/Messages/CreateOrderCommand.cs`
```csharp
using Orders.Messages;

namespace Orders.Messages;

public record CreateOrderCommand(Guid CustomerId, IReadOnlyList<LineItem> Items);
```

### `src/Orders/Messages/OrderPlaced.cs`
```csharp
using Orders.Messages;

namespace Orders.Messages;

public record OrderPlaced(Guid OrderId, Guid CustomerId, IReadOnlyList<LineItem> Items, decimal Total);
```

### `src/Orders/Responses/OrderCreatedResponse.cs`
```csharp
namespace Orders.Responses;

public record OrderCreatedResponse(Guid OrderId);
```

### `src/Orders/Aggregates/OrderStatus.cs`
```csharp
namespace Orders.Aggregates;

public enum OrderStatus { Active, Cancelled, Completed }
```

### `src/Orders/Aggregates/Order.cs`
```csharp
using Orders.Messages;

namespace Orders.Aggregates;

public class Order
{
    public Guid Id { get; set; }          // Set by Marten from stream ID
    public Guid CustomerId { get; set; }
    public OrderStatus Status { get; set; }
    public List<LineItem> Items { get; set; } = [];
    public decimal Total { get; set; }

    public void Apply(OrderPlaced @event)
    {
        CustomerId = @event.CustomerId;
        Status = OrderStatus.Active;
        Items = @event.Items.ToList();
        Total = @event.Total;
    }
}
```

### `src/Orders/Endpoints/CreateOrderEndpoint.cs`
```csharp
using Marten;
using Marten.Schema.Identity;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Orders.Aggregates;
using Orders.Messages;
using Orders.Responses;
using Wolverine.Http;

namespace Orders.Endpoints;

public static class CreateOrderEndpoint
{
    // Pre-condition: validates business rules before mutation.
    // Returns ProblemDetails (422) to short-circuit; null to proceed to Handle.
    public static async Task<ProblemDetails?> LoadAsync(
        CreateOrderCommand command,
        IDocumentSession session,
        CancellationToken ct)
    {
        foreach (var item in command.Items)
        {
            if (item.Quantity < 1 || item.Quantity > 100)
            {
                return new ProblemDetails
                {
                    Status = 422,
                    Title = "Invalid line item quantity",
                    Detail = $"Quantity for product {item.ProductId} must be between 1 and 100. Got {item.Quantity}."
                };
            }
        }

        var activeCount = await session.Query<Order>()
            .CountAsync(o => o.CustomerId == command.CustomerId && o.Status == OrderStatus.Active, ct);

        if (activeCount >= 50)
        {
            return new ProblemDetails
            {
                Status = 422,
                Title = "Active order limit reached",
                Detail = $"Customer already has {activeCount} active orders. The maximum is 50."
            };
        }

        return null;
    }

    // Handler: pure business logic. Returns the HTTP response and the OrderPlaced cascade event as a tuple.
    // Wolverine executes the IResult for the HTTP response and publishes OrderPlaced via the message bus.
    [WolverinePost("/api/customers/{customerId}/orders")]
    public static (IResult, OrderPlaced) Handle(
        CreateOrderCommand command,
        IDocumentSession session)
    {
        var orderId = CombGuidIdGeneration.NewGuid();
        var total = command.Items.Sum(i => i.Quantity * i.UnitPrice);

        var orderPlaced = new OrderPlaced(orderId, command.CustomerId, command.Items, total);

        session.Events.StartStream<Order>(orderId, orderPlaced);

        return (
            Results.Created(
                $"/api/customers/{command.CustomerId}/orders/{orderId}",
                new OrderCreatedResponse(orderId)),
            orderPlaced);
    }
}
```

### `src/Orders/Orders.csproj`
```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net9.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="WolverineFx.Http" Version="3.*" />
    <PackageReference Include="WolverineFx.Marten" Version="3.*" />
    <PackageReference Include="Marten" Version="7.*" />
    <PackageReference Include="Microsoft.AspNetCore.Http.Abstractions" Version="2.*" />
  </ItemGroup>
</Project>
```

### `src/Orders.Api/Program.cs`
```csharp
using Marten;
using Orders.Aggregates;
using Weasel.Core;
using Wolverine;
using Wolverine.Http;
using Wolverine.Marten;

var builder = WebApplication.CreateBuilder(args);

builder.Host.UseWolverine(opts =>
{
    opts.Policies.AutoApplyTransactions();
});

builder.Services.AddMarten(opts =>
{
    opts.Connection(builder.Configuration.GetConnectionString("Marten")
        ?? throw new InvalidOperationException("ConnectionStrings:Marten is required"));

    opts.AutoCreateSchemaObjects = AutoCreate.All;

    // Inline snapshot: after each event-stream commit, Marten applies Order.Apply(OrderPlaced)
    // synchronously and stores the projected Order document in the same transaction.
    opts.Projections.Snapshot<Order>(SnapshotLifecycle.Inline);
})
.IntegrateWithWolverine();

var app = builder.Build();
app.MapWolverineEndpoints();
app.Run();

public partial class Program { }
```

### `src/Orders.Api/Orders.Api.csproj`
```xml
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net9.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="WolverineFx.Http" Version="3.*" />
    <PackageReference Include="WolverineFx.Marten" Version="3.*" />
    <PackageReference Include="Marten" Version="7.*" />
  </ItemGroup>
  <ItemGroup>
    <ProjectReference Include="..\Orders\Orders.csproj" />
  </ItemGroup>
</Project>
```

---

## Tests

### `tests/Orders.Tests/WhenCreatingAnOrder.cs`
```csharp
using Marten;
using NSubstitute;
using Orders.Aggregates;
using Orders.Endpoints;
using Orders.Messages;
using Shouldly;

namespace Orders.Tests;

public class WhenCreatingAnOrder
{
    private readonly IDocumentSession _session;

    public WhenCreatingAnOrder()
    {
        _session = Substitute.For<IDocumentSession>();
        _session.Events.Returns(Substitute.For<IEventStore>());
    }

    [Fact]
    public void it_returns_an_order_created_response_and_order_placed_event()
    {
        var customerId = Guid.NewGuid();
        var items = new List<LineItem>
        {
            new(Guid.NewGuid(), 2, 9.99m),
            new(Guid.NewGuid(), 1, 4.50m)
        };
        var command = new CreateOrderCommand(customerId, items);

        var (response, @event) = CreateOrderEndpoint.Handle(command, _session);

        response.ShouldNotBeNull();
        response.OrderId.ShouldNotBe(Guid.Empty);
        @event.ShouldNotBeNull();
        @event.OrderId.ShouldBe(response.OrderId);
        @event.CustomerId.ShouldBe(customerId);
        @event.Total.ShouldBe(2 * 9.99m + 1 * 4.50m);
        @event.Items.Count.ShouldBe(2);
    }

    [Fact]
    public void it_starts_an_order_event_stream_on_the_session()
    {
        var customerId = Guid.NewGuid();
        var command = new CreateOrderCommand(customerId, [new LineItem(Guid.NewGuid(), 1, 10.00m)]);

        var (response, _) = CreateOrderEndpoint.Handle(command, _session);

        _session.Events.Received(1).StartStream<Order>(response.OrderId, Arg.Any<OrderPlaced>());
    }

    [Fact]
    public async Task load_async_returns_422_when_quantity_is_zero()
    {
        var session = Substitute.For<IDocumentSession>();
        var command = new CreateOrderCommand(Guid.NewGuid(), [new LineItem(Guid.NewGuid(), 0, 1.00m)]);

        var result = await CreateOrderEndpoint.LoadAsync(command, session, CancellationToken.None);

        result.ShouldNotBeNull();
        result!.Status.ShouldBe(422);
    }

    [Fact]
    public async Task load_async_returns_422_when_quantity_exceeds_100()
    {
        var session = Substitute.For<IDocumentSession>();
        var command = new CreateOrderCommand(Guid.NewGuid(), [new LineItem(Guid.NewGuid(), 101, 1.00m)]);

        var result = await CreateOrderEndpoint.LoadAsync(command, session, CancellationToken.None);

        result.ShouldNotBeNull();
        result!.Status.ShouldBe(422);
    }
}
```

### `tests/Orders.Tests.Integration/IntegrationContext.cs`
```csharp
using Alba;
using Marten;
using Microsoft.Extensions.DependencyInjection;
using Testcontainers.PostgreSql;
using Weasel.Core;
using Orders.Aggregates;

namespace Orders.Tests.Integration;

public class IntegrationContext : IAsyncLifetime
{
    private readonly PostgreSqlContainer _postgres = new PostgreSqlBuilder()
        .WithDatabase("orders_test")
        .WithUsername("postgres")
        .WithPassword("postgres")
        .Build();

    public IAlbaHost Host { get; private set; } = null!;

    public async Task InitializeAsync()
    {
        await _postgres.StartAsync();

        Host = await AlbaHost.For<Program>(builder =>
        {
            builder.ConfigureServices((ctx, services) =>
            {
                var descriptor = services.SingleOrDefault(d => d.ServiceType == typeof(IDocumentStore));
                if (descriptor is not null) services.Remove(descriptor);

                services.AddMarten(opts =>
                {
                    opts.Connection(_postgres.GetConnectionString());
                    opts.AutoCreateSchemaObjects = AutoCreate.All;
                    opts.Projections.Snapshot<Order>(SnapshotLifecycle.Inline);
                })
                .IntegrateWithWolverine();
            });
        });
    }

    public async Task DisposeAsync()
    {
        await Host.DisposeAsync();
        await _postgres.DisposeAsync();
    }
}
```

### `tests/Orders.Tests.Integration/WhenPostingAnOrder.cs`
```csharp
using Alba;
using Marten;
using Microsoft.Extensions.DependencyInjection;
using Orders.Aggregates;
using Orders.Messages;
using Orders.Responses;
using Shouldly;

namespace Orders.Tests.Integration;

public class WhenPostingAnOrder : IClassFixture<IntegrationContext>
{
    private readonly IntegrationContext _ctx;
    public WhenPostingAnOrder(IntegrationContext ctx) => _ctx = ctx;

    [Fact]
    public async Task happy_path_returns_201_with_location_header_and_order_id()
    {
        var customerId = Guid.NewGuid();
        var command = new CreateOrderCommand(customerId, [new LineItem(Guid.NewGuid(), 2, 9.99m)]);

        var result = await _ctx.Host.Scenario(s =>
        {
            s.Post.Json(command).ToUrl($"/api/customers/{customerId}/orders");
            s.StatusCodeShouldBe(201);
        });

        var response = result.ReadAsJson<OrderCreatedResponse>();
        response.ShouldNotBeNull();
        response!.OrderId.ShouldNotBe(Guid.Empty);

        var location = result.Context.Response.Headers.Location.ToString();
        location.ShouldBe($"/api/customers/{customerId}/orders/{response.OrderId}");
    }

    [Fact]
    public async Task happy_path_publishes_order_placed_event_to_marten_stream()
    {
        var customerId = Guid.NewGuid();
        var command = new CreateOrderCommand(customerId, [new LineItem(Guid.NewGuid(), 3, 5.00m)]);

        var result = await _ctx.Host.Scenario(s =>
        {
            s.Post.Json(command).ToUrl($"/api/customers/{customerId}/orders");
            s.StatusCodeShouldBe(201);
        });

        var response = result.ReadAsJson<OrderCreatedResponse>()!;

        await using var session = _ctx.Host.Services
            .GetRequiredService<IDocumentStore>()
            .QuerySession();

        var events = await session.Events.FetchStreamAsync(response.OrderId);
        var placed = events.Select(e => e.Data).OfType<OrderPlaced>().SingleOrDefault();

        placed.ShouldNotBeNull();
        placed!.CustomerId.ShouldBe(customerId);
        placed.Total.ShouldBe(15.00m);
    }

    [Fact]
    public async Task returns_422_when_customer_already_has_50_active_orders()
    {
        var customerId = Guid.NewGuid();

        // Seed 50 active orders directly via the event store — avoids 50 HTTP round-trips.
        await using (var session = _ctx.Host.Services
            .GetRequiredService<IDocumentStore>()
            .OpenSession())
        {
            for (var i = 0; i < 50; i++)
            {
                var orderId = Guid.NewGuid();
                session.Events.StartStream<Order>(orderId,
                    new OrderPlaced(orderId, customerId, [new LineItem(Guid.NewGuid(), 1, 1.00m)], 1.00m));
            }
            await session.SaveChangesAsync();
        }

        var command = new CreateOrderCommand(customerId, [new LineItem(Guid.NewGuid(), 1, 1.00m)]);

        await _ctx.Host.Scenario(s =>
        {
            s.Post.Json(command).ToUrl($"/api/customers/{customerId}/orders");
            s.StatusCodeShouldBe(422);
        });
    }

    [Theory]
    [InlineData(0)]
    [InlineData(101)]
    public async Task returns_422_for_out_of_range_quantity(int quantity)
    {
        var customerId = Guid.NewGuid();
        var command = new CreateOrderCommand(customerId, [new LineItem(Guid.NewGuid(), quantity, 1.00m)]);

        await _ctx.Host.Scenario(s =>
        {
            s.Post.Json(command).ToUrl($"/api/customers/{customerId}/orders");
            s.StatusCodeShouldBe(422);
        });
    }
}
```

### `tests/Orders.Tests.Integration/Orders.Tests.Integration.csproj`
```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net9.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <IsPackable>false</IsPackable>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="xunit" Version="2.*" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.*">
      <PrivateAssets>all</PrivateAssets>
      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
    </PackageReference>
    <PackageReference Include="Shouldly" Version="4.*" />
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.*" />
    <PackageReference Include="Alba" Version="8.*" />
    <PackageReference Include="Testcontainers.PostgreSql" Version="3.*" />
    <PackageReference Include="Marten" Version="7.*" />
    <PackageReference Include="WolverineFx.Http" Version="3.*" />
    <PackageReference Include="WolverineFx.Marten" Version="3.*" />
  </ItemGroup>
  <ItemGroup>
    <ProjectReference Include="..\..\src\Orders.Api\Orders.Api.csproj" />
  </ItemGroup>
</Project>
```

---

## Tests cover

- **Happy path (201 + Location header shape):** `happy_path_returns_201_with_location_header_and_order_id` — POSTs a valid command, asserts HTTP 201, reads `OrderCreatedResponse`, asserts `Location` header is exactly `/api/customers/{customerId}/orders/{orderId}` (full path shape, not just substring). A second test (`happy_path_publishes_order_placed_event_to_marten_stream`) verifies the `OrderPlaced` event appears in the Marten event stream for the returned `OrderId`.
- **51st active order rejected (422):** `returns_422_when_customer_already_has_50_active_orders` — seeds exactly 50 `OrderPlaced` events directly into the Marten event store (not 50 HTTP calls) for a fresh `customerId`, then POSTs a 51st order and asserts 422.
- **Quantity 0 AND quantity 101 rejected (422):** `returns_422_for_out_of_range_quantity` — parameterised `[Theory]` with `[InlineData(0)]` and `[InlineData(101)]`, both asserting 422. Additional unit-test coverage in `WhenCreatingAnOrder.load_async_returns_422_when_quantity_is_zero` and `load_async_returns_422_when_quantity_exceeds_100` for the same rules in isolation.

---

## Verification

```bash
# Build
dotnet build Orders.sln

# Unit tests (no infrastructure required)
dotnet test tests/Orders.Tests/Orders.Tests.csproj

# Integration tests (requires Docker for Testcontainers.PostgreSql)
dotnet test tests/Orders.Tests.Integration/Orders.Tests.Integration.csproj

# All together
dotnet build Orders.sln && dotnet test Orders.sln
```

Expected output:

```
Build succeeded.

Passed!  - Failed: 0, Passed: 4, Skipped: 0, Total: 4   [Orders.Tests]
Passed!  - Failed: 0, Passed: 5, Skipped: 0, Total: 5   [Orders.Tests.Integration]
```

[would run: `dotnet build Orders.sln && dotnet test Orders.sln` — cannot execute here as no .NET SDK is available in this eval environment]

### Artifacts written

#### `work/Orders.sln`

```

Microsoft Visual Studio Solution File, Format Version 12.00
# Visual Studio Version 17
VisualStudioVersion = 17.0.31903.59

Project("{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}") = "Orders", "src\Orders\Orders.csproj", "{11111111-1111-1111-1111-111111111111}"
EndProject
Project("{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}") = "Orders.Api", "src\Orders.Api\Orders.Api.csproj", "{22222222-2222-2222-2222-222222222222}"
EndProject
Project("{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}") = "Orders.Tests", "tests\Orders.Tests\Orders.Tests.csproj", "{33333333-3333-3333-3333-333333333333}"
EndProject
Project("{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}") = "Orders.Tests.Integration", "tests\Orders.Tests.Integration\Orders.Tests.Integration.csproj", "{44444444-4444-4444-4444-444444444444}"
EndProject

Global
  GlobalSection(SolutionConfigurationPlatforms) = preSolution
    Debug|Any CPU = Debug|Any CPU
    Release|Any CPU = Release|Any CPU
  EndGlobalSection
  GlobalSection(ProjectConfigurationPlatforms) = postSolution
    {11111111-1111-1111-1111-111111111111}.Debug|Any CPU.ActiveCfg = Debug|Any CPU
    {11111111-1111-1111-1111-111111111111}.Debug|Any CPU.Build.0 = Debug|Any CPU
    {22222222-2222-2222-2222-222222222222}.Debug|Any CPU.ActiveCfg = Debug|Any CPU
    {22222222-2222-2222-2222-222222222222}.Debug|Any CPU.Build.0 = Debug|Any CPU
    {33333333-3333-3333-3333-333333333333}.Debug|Any CPU.ActiveCfg = Debug|Any CPU
    {33333333-3333-3333-3333-333333333333}.Debug|Any CPU.Build.0 = Debug|Any CPU
    {44444444-4444-4444-4444-444444444444}.Debug|Any CPU.ActiveCfg = Debug|Any CPU
    {44444444-4444-4444-4444-444444444444}.Debug|Any CPU.Build.0 = Debug|Any CPU
  EndGlobalSection
EndGlobal

```

#### `work/src/Orders.Api/appsettings.json`

```
{
  "ConnectionStrings": {
    "Marten": "Host=localhost;Database=orders;Username=postgres;Password=postgres"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*"
}

```

#### `work/src/Orders.Api/Orders.Api.csproj`

```
<Project Sdk="Microsoft.NET.Sdk.Web">

  <PropertyGroup>
    <TargetFramework>net9.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="WolverineFx.Http" Version="3.*" />
    <PackageReference Include="WolverineFx.Marten" Version="3.*" />
    <PackageReference Include="Marten" Version="7.*" />
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="..\Orders\Orders.csproj" />
  </ItemGroup>

</Project>

```

#### `work/src/Orders.Api/Program.cs`

```
using Marten;
using Orders.Aggregates;
using Weasel.Core;
using Wolverine;
using Wolverine.Http;
using Wolverine.Marten;

var builder = WebApplication.CreateBuilder(args);

builder.Host.UseWolverine(opts =>
{
    opts.Policies.AutoApplyTransactions();
});

builder.Services.AddMarten(opts =>
{
    opts.Connection(builder.Configuration.GetConnectionString("Marten")
        ?? throw new InvalidOperationException("ConnectionStrings:Marten is required"));

    opts.AutoCreateSchemaObjects = AutoCreate.All;

    // Inline snapshot: after each event-stream commit, Marten applies Order.Apply(OrderPlaced)
    // synchronously and stores the projected Order document in the same transaction.
    // This ensures LoadAsync's active-order count query sees immediately consistent data.
    opts.Projections.Snapshot<Order>(SnapshotLifecycle.Inline);
})
.IntegrateWithWolverine();

var app = builder.Build();

app.MapWolverineEndpoints();

app.Run();

// Exposed so AlbaHost.For<Program>(...) can reference it from the integration test project.
public partial class Program { }

```

#### `work/src/Orders/Orders.csproj`

```
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net9.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="WolverineFx.Http" Version="3.*" />
    <PackageReference Include="WolverineFx.Marten" Version="3.*" />
    <PackageReference Include="Marten" Version="7.*" />
    <PackageReference Include="Microsoft.AspNetCore.Http.Abstractions" Version="2.*" />
  </ItemGroup>

</Project>

```

#### `work/src/Orders/Messages/OrderPlaced.cs`

```
using Orders.Messages;

namespace Orders.Messages;

public record OrderPlaced(Guid OrderId, Guid CustomerId, IReadOnlyList<LineItem> Items, decimal Total);

```

#### `work/src/Orders/Messages/LineItem.cs`

```
namespace Orders.Messages;

public record LineItem(Guid ProductId, int Quantity, decimal UnitPrice);

```

#### `work/src/Orders/Messages/CreateOrderCommand.cs`

```
using Orders.Messages;

namespace Orders.Messages;

public record CreateOrderCommand(Guid CustomerId, IReadOnlyList<LineItem> Items);

```

#### `work/src/Orders/Endpoints/CreateOrderEndpoint.cs`

```
using Marten;
using Marten.Schema.Identity;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Orders.Aggregates;
using Orders.Messages;
using Orders.Responses;
using Wolverine.Http;

namespace Orders.Endpoints;

public static class CreateOrderEndpoint
{
    // Pre-condition: validates business rules before mutation.
    // Returns ProblemDetails (422) to short-circuit; null to proceed to Handle.
    public static async Task<ProblemDetails?> LoadAsync(
        CreateOrderCommand command,
        IDocumentSession session,
        CancellationToken ct)
    {
        foreach (var item in command.Items)
        {
            if (item.Quantity < 1 || item.Quantity > 100)
            {
                return new ProblemDetails
                {
                    Status = 422,
                    Title = "Invalid line item quantity",
                    Detail = $"Quantity for product {item.ProductId} must be between 1 and 100. Got {item.Quantity}."
                };
            }
        }

        var activeCount = await session.Query<Order>()
            .CountAsync(o => o.CustomerId == command.CustomerId && o.Status == OrderStatus.Active, ct);

        if (activeCount >= 50)
        {
            return new ProblemDetails
            {
                Status = 422,
                Title = "Active order limit reached",
                Detail = $"Customer already has {activeCount} active orders. The maximum is 50."
            };
        }

        return null;
    }

    // Handler: pure business logic. Returns the HTTP response and the OrderPlaced cascade event as a tuple.
    // Wolverine executes the IResult for the HTTP response and publishes OrderPlaced via the message bus.
    [WolverinePost("/api/customers/{customerId}/orders")]
    public static (IResult, OrderPlaced) Handle(
        CreateOrderCommand command,
        IDocumentSession session)
    {
        var orderId = CombGuidIdGeneration.NewGuid();
        var total = command.Items.Sum(i => i.Quantity * i.UnitPrice);

        var orderPlaced = new OrderPlaced(orderId, command.CustomerId, command.Items, total);

        session.Events.StartStream<Order>(orderId, orderPlaced);

        return (
            Results.Created(
                $"/api/customers/{command.CustomerId}/orders/{orderId}",
                new OrderCreatedResponse(orderId)),
            orderPlaced);
    }
}

```

#### `work/src/Orders/Aggregates/Order.cs`

```
using Orders.Messages;

namespace Orders.Aggregates;

public class Order
{
    // Marten sets Id from the event stream ID
    public Guid Id { get; set; }
    public Guid CustomerId { get; set; }
    public OrderStatus Status { get; set; }
    public List<LineItem> Items { get; set; } = [];
    public decimal Total { get; set; }

    public void Apply(OrderPlaced @event)
    {
        CustomerId = @event.CustomerId;
        Status = OrderStatus.Active;
        Items = @event.Items.ToList();
        Total = @event.Total;
    }
}

```

#### `work/src/Orders/Aggregates/OrderStatus.cs`

```
namespace Orders.Aggregates;

public enum OrderStatus
{
    Active,
    Cancelled,
    Completed
}

```

#### `work/src/Orders/Responses/OrderCreatedResponse.cs`

```
namespace Orders.Responses;

public record OrderCreatedResponse(Guid OrderId);

```

#### `work/tests/Orders.Tests.Integration/Orders.Tests.Integration.csproj`

```
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net9.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <IsPackable>false</IsPackable>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="xunit" Version="2.*" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.*">
      <PrivateAssets>all</PrivateAssets>
      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
    </PackageReference>
    <PackageReference Include="Shouldly" Version="4.*" />
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.*" />
    <PackageReference Include="Alba" Version="8.*" />
    <PackageReference Include="Testcontainers.PostgreSql" Version="3.*" />
    <PackageReference Include="Marten" Version="7.*" />
    <PackageReference Include="WolverineFx.Http" Version="3.*" />
    <PackageReference Include="WolverineFx.Marten" Version="3.*" />
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="..\..\src\Orders.Api\Orders.Api.csproj" />
  </ItemGroup>

</Project>

```

#### `work/tests/Orders.Tests.Integration/IntegrationContext.cs`

```
using Alba;
using Marten;
using Microsoft.Extensions.DependencyInjection;
using Testcontainers.PostgreSql;
using Weasel.Core;
using Orders.Aggregates;

namespace Orders.Tests.Integration;

public class IntegrationContext : IAsyncLifetime
{
    private readonly PostgreSqlContainer _postgres = new PostgreSqlBuilder()
        .WithDatabase("orders_test")
        .WithUsername("postgres")
        .WithPassword("postgres")
        .Build();

    public IAlbaHost Host { get; private set; } = null!;

    public async Task InitializeAsync()
    {
        await _postgres.StartAsync();

        Host = await AlbaHost.For<Program>(builder =>
        {
            builder.ConfigureServices((ctx, services) =>
            {
                // Replace the Marten registration with one pointing at the test container.
                // Remove the existing Marten registration added in Program.cs.
                var descriptor = services.SingleOrDefault(d => d.ServiceType == typeof(IDocumentStore));
                if (descriptor is not null)
                    services.Remove(descriptor);

                services.AddMarten(opts =>
                {
                    opts.Connection(_postgres.GetConnectionString());
                    opts.AutoCreateSchemaObjects = AutoCreate.All;
                    opts.Projections.Snapshot<Order>(SnapshotLifecycle.Inline);
                })
                .IntegrateWithWolverine();
            });
        });
    }

    public async Task DisposeAsync()
    {
        await Host.DisposeAsync();
        await _postgres.DisposeAsync();
    }
}

```

#### `work/tests/Orders.Tests.Integration/WhenPostingAnOrder.cs`

```
using Alba;
using Marten;
using Microsoft.Extensions.DependencyInjection;
using Orders.Aggregates;
using Orders.Messages;
using Orders.Responses;
using Shouldly;

namespace Orders.Tests.Integration;

public class WhenPostingAnOrder : IClassFixture<IntegrationContext>
{
    private readonly IntegrationContext _ctx;

    public WhenPostingAnOrder(IntegrationContext ctx) => _ctx = ctx;

    [Fact]
    public async Task happy_path_returns_201_with_location_header_and_order_id()
    {
        var customerId = Guid.NewGuid();
        var command = new CreateOrderCommand(customerId, [
            new LineItem(Guid.NewGuid(), 2, 9.99m)
        ]);

        var result = await _ctx.Host.Scenario(s =>
        {
            s.Post.Json(command).ToUrl($"/api/customers/{customerId}/orders");
            s.StatusCodeShouldBe(201);
        });

        var response = result.ReadAsJson<OrderCreatedResponse>();
        response.ShouldNotBeNull();
        response!.OrderId.ShouldNotBe(Guid.Empty);

        var location = result.Context.Response.Headers.Location.ToString();
        location.ShouldBe($"/api/customers/{customerId}/orders/{response.OrderId}");
    }

    [Fact]
    public async Task happy_path_publishes_order_placed_event_to_marten_stream()
    {
        var customerId = Guid.NewGuid();
        var command = new CreateOrderCommand(customerId, [
            new LineItem(Guid.NewGuid(), 3, 5.00m)
        ]);

        var result = await _ctx.Host.Scenario(s =>
        {
            s.Post.Json(command).ToUrl($"/api/customers/{customerId}/orders");
            s.StatusCodeShouldBe(201);
        });

        var response = result.ReadAsJson<OrderCreatedResponse>()!;

        await using var session = _ctx.Host.Services
            .GetRequiredService<IDocumentStore>()
            .QuerySession();

        var events = await session.Events.FetchStreamAsync(response.OrderId);
        events.ShouldNotBeEmpty();

        var placed = events
            .Select(e => e.Data)
            .OfType<OrderPlaced>()
            .SingleOrDefault();

        placed.ShouldNotBeNull();
        placed!.CustomerId.ShouldBe(customerId);
        placed.OrderId.ShouldBe(response.OrderId);
        placed.Total.ShouldBe(15.00m);
    }

    [Fact]
    public async Task returns_422_when_customer_already_has_50_active_orders()
    {
        var customerId = Guid.NewGuid();

        // Seed 50 active orders directly via the event store — faster than 50 HTTP POSTs.
        await using (var session = _ctx.Host.Services
            .GetRequiredService<IDocumentStore>()
            .OpenSession())
        {
            for (var i = 0; i < 50; i++)
            {
                var orderId = Guid.NewGuid();
                var placed = new OrderPlaced(
                    orderId,
                    customerId,
                    [new LineItem(Guid.NewGuid(), 1, 1.00m)],
                    1.00m);

                session.Events.StartStream<Order>(orderId, placed);
            }

            await session.SaveChangesAsync();
        }

        // 51st order must be rejected.
        var command = new CreateOrderCommand(customerId, [new LineItem(Guid.NewGuid(), 1, 1.00m)]);

        await _ctx.Host.Scenario(s =>
        {
            s.Post.Json(command).ToUrl($"/api/customers/{customerId}/orders");
            s.StatusCodeShouldBe(422);
        });
    }

    [Theory]
    [InlineData(0)]
    [InlineData(101)]
    public async Task returns_422_for_out_of_range_quantity(int quantity)
    {
        var customerId = Guid.NewGuid();
        var command = new CreateOrderCommand(customerId, [
            new LineItem(Guid.NewGuid(), quantity, 1.00m)
        ]);

        await _ctx.Host.Scenario(s =>
        {
            s.Post.Json(command).ToUrl($"/api/customers/{customerId}/orders");
            s.StatusCodeShouldBe(422);
        });
    }
}

```

#### `work/tests/Orders.Tests/WhenCreatingAnOrder.cs`

```
using Marten;
using NSubstitute;
using Orders.Aggregates;
using Orders.Endpoints;
using Orders.Messages;
using Shouldly;

namespace Orders.Tests;

public class WhenCreatingAnOrder
{
    private readonly IDocumentSession _session;

    public WhenCreatingAnOrder()
    {
        _session = Substitute.For<IDocumentSession>();
        _session.Events.Returns(Substitute.For<IEventStore>());
    }

    [Fact]
    public void it_returns_an_order_created_response_and_order_placed_event()
    {
        var customerId = Guid.NewGuid();
        var items = new List<LineItem>
        {
            new(Guid.NewGuid(), 2, 9.99m),
            new(Guid.NewGuid(), 1, 4.50m)
        };
        var command = new CreateOrderCommand(customerId, items);

        var (response, @event) = CreateOrderEndpoint.Handle(command, _session);

        response.ShouldNotBeNull();
        response.OrderId.ShouldNotBe(Guid.Empty);

        @event.ShouldNotBeNull();
        @event.OrderId.ShouldBe(response.OrderId);
        @event.CustomerId.ShouldBe(customerId);
        @event.Total.ShouldBe(2 * 9.99m + 1 * 4.50m);
        @event.Items.Count.ShouldBe(2);
    }

    [Fact]
    public void it_starts_an_order_event_stream_on_the_session()
    {
        var customerId = Guid.NewGuid();
        var command = new CreateOrderCommand(customerId, [new LineItem(Guid.NewGuid(), 1, 10.00m)]);

        var (response, _) = CreateOrderEndpoint.Handle(command, _session);

        _session.Events.Received(1).StartStream<Order>(response.OrderId, Arg.Any<OrderPlaced>());
    }

    [Fact]
    public async Task load_async_returns_422_when_quantity_is_zero()
    {
        var session = Substitute.For<IDocumentSession>();
        var command = new CreateOrderCommand(Guid.NewGuid(), [new LineItem(Guid.NewGuid(), 0, 1.00m)]);

        var result = await CreateOrderEndpoint.LoadAsync(command, session, CancellationToken.None);

        result.ShouldNotBeNull();
        result!.Status.ShouldBe(422);
    }

    [Fact]
    public async Task load_async_returns_422_when_quantity_exceeds_100()
    {
        var session = Substitute.For<IDocumentSession>();
        var command = new CreateOrderCommand(Guid.NewGuid(), [new LineItem(Guid.NewGuid(), 101, 1.00m)]);

        var result = await CreateOrderEndpoint.LoadAsync(command, session, CancellationToken.None);

        result.ShouldNotBeNull();
        result!.Status.ShouldBe(422);
    }
}

```

#### `work/tests/Orders.Tests/Orders.Tests.csproj`

```
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net9.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <IsPackable>false</IsPackable>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="xunit" Version="2.*" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.*">
      <PrivateAssets>all</PrivateAssets>
      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
    </PackageReference>
    <PackageReference Include="Shouldly" Version="4.*" />
    <PackageReference Include="NSubstitute" Version="5.*" />
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.*" />
    <PackageReference Include="Marten" Version="7.*" />
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="..\..\src\Orders\Orders.csproj" />
  </ItemGroup>

</Project>

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 18.0/18.0 (100%) |
| Evaluated | 2026-05-27 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 668540 ms |
| Target cost | $1.7675 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent reads CLAUDE.md and checks `.claude/rules/` including `dotnet-stack--jasperfx.md` before writing code | PASS | Pre-flight reads table lists CLAUDE.md (Read), dotnet-stack--jasperfx.md ([not present — assuming...]), and three turtlestack coding-standards rules — all before Implementation section. |
| c2 | Agent uses hierarchical URL `/api/customers/{customerId}/orders` — does not propose a flat `/api/orders` | PASS | `[WolverinePost("/api/customers/{customerId}/orders")]` in CreateOrderEndpoint.cs Handle method. |
| c3 | Agent separates LoadAsync (pre-condition: customer exists, active order count < 50) from Handle (pure business logic returning OrderPlaced event) | PASS | LoadAsync validates quantity range and counts active orders; Handle only creates the stream and returns the tuple. Two distinct static methods in CreateOrderEndpoint. |
| c4 | Agent uses `IDocumentSession` injected by Wolverine — does not create sessions from `IDocumentStore` directly | PASS | Both LoadAsync and Handle accept `IDocumentSession session` as an injected parameter; IDocumentStore is never used in the endpoint code. |
| c5 | Agent returns `OrderPlaced` event as a cascading message from Handle, not inline side-effect processing | PASS | Handle returns `(IResult, OrderPlaced)` tuple; no IMessageBus.PublishAsync call. OrderPlaced is the second element of the returned tuple. |
| c6 | Agent produces both a unit test (WhenCreatingAnOrder class, Shouldly assertions) and an integration test (Alba + Testcontainers) | PASS | WhenCreatingAnOrder.cs uses Shouldly + NSubstitute; WhenPostingAnOrder.cs uses AlbaHost + Testcontainers.PostgreSql (PackageReference present in .csproj). |
| c7 | Agent raises a decision checkpoint before creating the Order aggregate (architecture decision) | PASS | ## Architecture checkpoint section states "stakeholder review required before proceeding", presents CRUD-entity alternative, and explains why ES was chosen. |
| c8 | Command and event are C# records (not classes), with immutable properties | PASS | `public record CreateOrderCommand(Guid CustomerId, IReadOnlyList<LineItem> Items)` and `public record OrderPlaced(Guid OrderId, Guid CustomerId, IReadOnlyList<LineItem> Items, decimal Total)` — both positional records. |
| c9 | Agent includes a response DTO separate from the aggregate — does not expose aggregate internals directly | PARTIAL | `public record OrderCreatedResponse(Guid OrderId)` in Responses/ folder; Handle returns it via Results.Created, never exposing Order aggregate fields. |
| c10 | Output's endpoint route is exactly `POST /api/customers/{customerId}/orders`, mounted via Wolverine HTTP attributes/conventions, with the customerId bound from the route | PASS | `[WolverinePost("/api/customers/{customerId}/orders")]` attribute on Handle method; customerId used via `command.CustomerId` which comes from the request body bound by Wolverine. |
| c11 | Output's command record (e.g. `CreateOrder`) is a C# `record` with `init`-only or positional-immutable properties — not a class with mutable setters — and contains the line items collection and customerId | PASS | `public record CreateOrderCommand(Guid CustomerId, IReadOnlyList<LineItem> Items)` — positional record, IReadOnlyList items, contains both CustomerId and Items. |
| c12 | Output enforces both business rules in code: line item quantity range [1,100] (validated via FluentValidation or in LoadAsync) and the customer's active-order count below 50 checked against persisted state | PASS | LoadAsync checks `item.Quantity < 1 \|\| item.Quantity > 100` and `activeCount >= 50` via `session.Query<Order>().CountAsync(...)`. |
| c13 | Output's `LoadAsync` (or equivalent pre-condition step) loads the customer / counts active orders and returns a Problem Details / 4xx response when pre-conditions fail — not throwing exceptions for business validation | PASS | LoadAsync returns `new ProblemDetails { Status = 422, ... }` for both quantity and active-order violations; no exceptions thrown. |
| c14 | Output's `Handle` returns the new domain event(s) (`OrderPlaced` and any cascading messages) plus the HTTP response — it does NOT execute side effects inline | PASS | Handle returns `(Results.Created(...), orderPlaced)` tuple; no IMessageBus calls. session.Events.StartStream registers with UoW; Wolverine AutoApplyTransactions commits. |
| c15 | Output uses an `IDocumentSession` parameter injected by Wolverine and never instantiates a session from `IDocumentStore` directly, and never calls `SaveChangesAsync` manually | PASS | Endpoint injects IDocumentSession; no SaveChangesAsync in handler; Program.cs uses `opts.Policies.AutoApplyTransactions()` for auto-commit. |
| c16 | Output's response is 201 Created with a Location header pointing to `/api/customers/{customerId}/orders/{orderId}` and a response DTO that does NOT directly serialise the aggregate | PASS | `Results.Created($"/api/customers/{command.CustomerId}/orders/{orderId}", new OrderCreatedResponse(orderId))` — 201 with correct location path and separate DTO. |
| c17 | Output includes both a unit test class named in the `When...` style (e.g. `WhenCreatingAnOrder`) using Shouldly assertions, and an integration test using Alba + Testcontainers for Postgres | PASS | `WhenCreatingAnOrder` class with Shouldly; `WhenPostingAnOrder` uses `AlbaHost.For<Program>` and `Testcontainers.PostgreSql` package reference. |
| c18 | Output's tests cover the happy path plus both rule violations (51st active order rejected, quantity 0 / 101 rejected) with explicit Given/When/Then or arrange/act/assert structure | PASS | happy_path_returns_201..., returns_422_when_customer_already_has_50_active_orders (seeds 50 then posts 51st), returns_422_for_out_of_range_quantity [Theory][InlineData(0)][InlineData(101)]. |
| c19 | Output flags the architecture decision (introducing the Order aggregate) for stakeholder review before implementing rather than just creating it | PARTIAL | ## Architecture checkpoint says "stakeholder review required before proceeding", presents CRUD alternative and justifies ES choice — appears before ## Implementation. |

### Notes

The output is comprehensive and meets every criterion. All mandatory headings appear in order with full content, Wolverine/Marten conventions are correctly applied (LoadAsync/Handle split, cascading tuple return, injected IDocumentSession, AutoApplyTransactions), and tests cover all three required scenarios using AlbaHost and Testcontainers.PostgreSql.
