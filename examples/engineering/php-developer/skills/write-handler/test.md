# Test: write-handler for CancelSubscription command

Scenario: Developer invokes the write-handler skill to produce a symfony/messenger command handler for `CancelSubscription`. The handler loads the `Subscription` aggregate via an EventSauce `AggregateRootRepository`, calls its `cancel()` domain method, and persists. An accompanying projection updates a `subscription_summary` read model when `SubscriptionCancelled` fires.

## Prompt

Write a symfony/messenger handler for cancelling a subscription. Deliver:

1. **Reconnaissance** — show actual commands run (e.g. `grep -rn "AsMessageHandler" --include="*.php" src/ 2>/dev/null`).
2. **`CancelSubscription` command class** — `final readonly class` in `src/Application/Subscription/`, with a `SubscriptionId` property (NOT a raw string).
3. **`CancelSubscriptionHandler`** — `final readonly class` with `__invoke(CancelSubscription $command): void`, attribute `#[AsMessageHandler(bus: 'command.bus')]`. Constructor injection of `AggregateRootRepository`. The handler loads, calls `cancel()`, persists. Nothing else.
4. **`SubscriptionSummaryProjection`** — `final readonly class` with `whenSubscriptionCancelled(SubscriptionCancelled $event): void` method having `#[AsMessageHandler(bus: 'event.bus')]`. Updates the `subscription_summary` read model — idempotent (handles replay).
5. **Pest unit test for the handler** — mocks the repository (`Mockery::mock(AggregateRootRepository::class)`), verifies `retrieve` and `persist` are called, asserts the aggregate emitted `SubscriptionCancelled`.
6. **Pest integration test** — dispatches `CancelSubscription` through a real `MessageBusInterface`, asserts the projection updated the read model.
7. **Evidence of tests passing** — show `vendor/bin/pest tests/` with exit code, or a template output.

Constraints (any violation is a failure):
- Command handler returns `void` — never a result
- No `foreach` inside the handler — one command, one unit of work
- No service location (`$container->get(...)`)
- `declare(strict_types=1);` on every file
- The handler does NOT contain domain logic — it loads, calls a domain method, persists. Domain decisions live in the aggregate

## Criteria

- [ ] PASS: Skill performs reconnaissance first — checks for existing handlers/patterns
- [ ] PASS: Command class is `final readonly class` with typed `SubscriptionId` property (not raw `string`)
- [ ] PASS: Handler class is `final readonly class` with `__invoke()` and `#[AsMessageHandler(bus: 'command.bus')]` attribute
- [ ] PASS: Constructor injection only — no service location, no static container lookups
- [ ] PASS: Handler body is thin: load aggregate → call domain method → persist. No conditionals, no domain logic
- [ ] PASS: Handler `__invoke()` returns `void`
- [ ] PASS: Projection is on `event.bus`, not `command.bus`
- [ ] PASS: Projection is idempotent (uses `INSERT ... ON CONFLICT`, check-then-write, or equivalent) — replaying `SubscriptionCancelled` must not corrupt the row
- [ ] PASS: Unit test mocks the repository and asserts on aggregate emitted events, not on internal state
- [ ] PASS: Integration test dispatches through the real bus and asserts on the projected read model
- [ ] PASS: No `foreach` inside the handler — one message, one unit of work
- [ ] PASS: `declare(strict_types=1);` on every PHP file

## Output expectations

- [ ] PASS: Output's `CancelSubscription` command has a `SubscriptionId` property — never `string $subscriptionId`
- [ ] PASS: Output's handler class has the `#[AsMessageHandler(bus: 'command.bus')]` attribute exactly — not a different bus name, not on `event.bus`
- [ ] PASS: Output's handler does NOT loop over a collection inline — if cascades are needed, dispatch N messages, not foreach
- [ ] PASS: Output's projection method name follows the `when<EventName>` pattern (e.g. `whenSubscriptionCancelled`) and takes the event as its single parameter
- [ ] PASS: Output's unit test verifies `Mockery::mock(AggregateRootRepository::class)` (or equivalent) and `shouldReceive('retrieve')` + `shouldReceive('persist')`
- [ ] PASS: Output's integration test asserts on the read model state AFTER dispatch, not on bus internals
- [ ] PASS: Output's handler does NOT catch `\Exception` or `\Throwable` — fatal errors propagate to messenger for retry/dead-letter
- [ ] PASS: Output's projection has at least one explicit idempotency mechanism — INSERT ON CONFLICT, an existence check, or a documented upsert pattern
- [ ] PASS: Output's evidence shows `vendor/bin/pest` exit code or a representative output template
- [ ] PARTIAL: Output discusses retry strategy for the command (messenger config), even briefly
