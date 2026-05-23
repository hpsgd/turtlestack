# Test: write-aggregate for a Subscription aggregate

Scenario: Developer invokes the write-aggregate skill to produce an event-sourced `Subscription` aggregate using EventSauce — a subscription can be started, paused, resumed, and cancelled. Cancelling a subscription twice must throw an `AlreadyCancelled` exception, and pausing an already-paused subscription must throw `AlreadyPaused`.

## Prompt

Write an event-sourced Subscription aggregate using EventSauce. The aggregate has four domain methods:

- `start(SubscriptionId $id, PlanId $planId, \DateTimeImmutable $startedAt): self`
- `pause(): void` — throws `AlreadyPaused` if currently paused
- `resume(): void` — throws `NotPaused` if not currently paused
- `cancel(): void` — throws `AlreadyCancelled` if already cancelled

Emit `SubscriptionStarted`, `SubscriptionPaused`, `SubscriptionResumed`, `SubscriptionCancelled` events.

Deliver ALL of the following:

1. **Reconnaissance** — show actual commands run (`grep -rn "AggregateRoot" --include="*.php" src/ 2>/dev/null` reporting "none found, greenfield" or whatever is present).
2. **`SubscriptionId` value object** implementing `EventSauce\EventSourcing\AggregateRootId`, backed by UUID v7 via `ramsey/uuid`, with `webmozart/assert` validation in the constructor.
3. **Four event classes** — each `final readonly class` implementing `SerializablePayload` with `toPayload()` and `fromPayload()` using `snake_case` payload keys.
4. **Four domain exceptions** — `AlreadyPaused`, `NotPaused`, `AlreadyCancelled`, and a base `App\Domain\DomainException` — each `final class` extending the base.
5. **`SubscriptionAggregate` class** — `final class` using `AggregateRootBehaviour`, with `recordThat()` for state changes, `apply*()` methods for each event, and invariant checks that throw before recording.
6. **Pest unit tests** — at minimum one `it()` per domain method covering happy path AND exception path. Assert on `releaseEvents()`, not internal state.
7. **Evidence of tests passing** — show the command (`vendor/bin/pest tests/Unit/Domain/Subscription`) and a representative output block. If tooling isn't installed, document the command that would be run and produce a template output.

Use `declare(strict_types=1);` on every file. PHPStan-level-9-clean code: no `mixed`, every parameter/return typed, `array` types annotated via PHPDoc `@param list<...>` where applicable. Aggregate ID raw strings forbidden — always pass typed `SubscriptionId`.

## Criteria

- [ ] PASS: Skill performs reconnaissance first — checks for existing aggregates before writing
- [ ] PASS: Aggregate ID is a typed `final readonly class` implementing `AggregateRootId`, not raw string
- [ ] PASS: UUID v7 used via `ramsey/uuid` (`Uuid::uuid7()`), not v4 — time-ordered IDs matter for event-store queries
- [ ] PASS: All four events are `final readonly class` implementing `SerializablePayload`
- [ ] PASS: Event names are past tense (`SubscriptionStarted`, `SubscriptionCancelled`) — not imperative or progressive
- [ ] PASS: Payload keys in `toPayload()` are `snake_case`
- [ ] PASS: Aggregate uses `recordThat()` + `apply*()` — never direct mutation outside `apply*()` methods
- [ ] PASS: Each invariant check (`cancel()` when already cancelled, etc.) throws BEFORE `recordThat()` — never record an event that violates the invariant
- [ ] PASS: Domain exceptions extend `App\Domain\DomainException`, not `\RuntimeException` or `\Exception` directly
- [ ] PASS: Unit tests assert on `releaseEvents()` — the emitted events — not on private aggregate state
- [ ] PASS: Each domain method has both happy-path and exception-path tests
- [ ] PASS: `declare(strict_types=1);` on every PHP file shown

## Output expectations

- [ ] PASS: Output's `SubscriptionId::generate()` uses `Uuid::uuid7()` — not `uuid4` or another v
- [ ] PASS: Output's `SubscriptionAggregate` is `final class` (not `abstract` or non-final) using the `AggregateRootBehaviour` trait
- [ ] PASS: Output's `apply*()` methods are `protected` and return `void`
- [ ] PASS: Output's `pause()` checks `$this->paused` (or equivalent) BEFORE calling `recordThat(new SubscriptionPaused(...))` and throws `AlreadyPaused` on violation
- [ ] PASS: Output's `cancel()` is idempotent-at-boundary — second call throws `AlreadyCancelled`, does NOT silently no-op
- [ ] PASS: Output's events implement `SerializablePayload` with both `toPayload()` AND `fromPayload()` defined — not just one
- [ ] PASS: Output's tests use Pest's `it('...')` form, each describing the behaviour ("it throws AlreadyCancelled when cancelling twice"), not implementation
- [ ] PASS: Output's tests use `expect(...)->toBeInstanceOf(...)` (Pest) or PHPUnit `assertInstanceOf` on emitted events
- [ ] PARTIAL: Output discusses snapshot strategy or notes that snapshots are appropriate when the event stream grows large
- [ ] PASS: Output's quality gates evidence shows at minimum `vendor/bin/pest` exit 0 OR a template documenting the command and expected exit code
