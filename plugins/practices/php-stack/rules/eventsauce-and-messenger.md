---
description: EventSauce + symfony/messenger conventions for event-sourced PHP applications
paths:
  - "**/*.php"
---

# [EventSauce](https://eventsauce.io) and [symfony/messenger](https://symfony.com/doc/current/components/messenger.html)

## Buses (three, not one)

| Bus | Handlers per message | Returns | Purpose |
|---|---|---|---|
| `command.bus` | Exactly one | void | State change on an aggregate |
| `query.bus` | Exactly one | Result object | Read from a projection |
| `event.bus` | Zero or more | void | React to a fact that happened |

Configure them as separate transports in `messenger.yaml` (Symfony) or via the bus builder (standalone). Do not collapse them into a single bus — the cardinality contract is part of the design.

## Aggregates

- `final class <Name>Aggregate implements AggregateRoot` using the `AggregateRootBehaviour` trait
- State changes via `recordThat()` + `apply*()` methods — never mutate fields outside `apply*()`
- Static factory methods for creation (`start`, `register`, `open`) — never `new` directly from a handler
- Aggregate ID is a typed value object implementing `AggregateRootId`, backed by UUID v7 (time-ordered, sorts chronologically)
- Domain logic in the aggregate; the handler is thin (load → call method → persist)

## Events

- `final readonly class` implementing EventSauce's `SerializablePayload`
- Past tense names (`CrawlStarted`, not `StartCrawl`)
- `toPayload()` produces a JSON-friendly array with `snake_case` keys
- `fromPayload()` is strict — `assert()` types before constructing
- One event per file in `src/Domain/<Context>/Event/`

## Handlers

- `final readonly class` with `__invoke()`
- `#[AsMessageHandler(bus: '<bus-name>')]` attribute on the class (single handler) or method (subscriber with multiple events)
- Constructor injection only — never service location or `static::class` lookups
- One command, one handler; one query, one handler; events can have many subscribers

## One Message, One Unit of Work

Every handler is a self-contained unit of work with its own transaction. NEVER loop through N items doing heavy work inline — dispatch N independent messages instead. A single failure must not break the other N-1 items.

Canonical pattern: orchestration handler creates the parent aggregate, then dispatches one independent message per child item.

```php
public function __invoke(StartCrawl $command): void
{
    $crawl = CrawlAggregate::start($command->crawlId, $command->pageIds);
    $this->repository->persist($crawl);

    foreach ($command->pageIds as $pageId) {
        $this->commandBus->dispatch(new ExtractPage($command->crawlId, $pageId));
    }
}
```

## Projections

- Subscribers on `event.bus` build read models in Doctrine tables
- Idempotent — replaying an event must produce the same row. Use `INSERT ... ON CONFLICT` or check-then-write
- Inline projections (synchronous, same transaction as event append) for consistency-critical reads
- Async projections (separate worker) for everything else
- Projections are disposable — they can be rebuilt from the event stream at any time

## Event store

- Use EventSauce's DBAL message repository for the event store table
- Schema: `event_id`, `aggregate_root_id`, `aggregate_root_version`, `event_type`, `payload`, `recorded_at`
- Optimistic concurrency via `aggregate_root_version` — repository throws on version mismatch
- Snapshots (EventSauce's `SnapshotRepository`) for aggregates with many events; load snapshot + replay remaining events

## Upcasters

When an event's data shape changes:

1. Add a new event class — never edit the existing one
2. Register an upcaster that maps the old payload to the new event class
3. The upcaster runs on read — old events stored in the stream are transformed on rehydration
4. Never edit historical event payloads in the database

## Retries and failures

- Configure retry strategy per message class in `messenger.yaml` (or the bus config)
- Use exponential backoff for transient failures (rate-limited APIs, brief DB unavailability)
- Failed messages land in the failure transport — monitor it
- Don't catch `\Throwable` in a handler to keep workers alive; let messenger retry and dead-letter

## Outbox

The transactional outbox is critical when persisting events and dispatching cascades. EventSauce's `OutboxRepository` provides this — events are written to the outbox in the same transaction as the aggregate, then dispatched asynchronously by a worker. Do not dispatch cascades from inside the handler without an outbox; you risk dispatching a message for an aggregate change that never committed.

## What this rule does NOT cover

- PHP language conventions (types, readonly, error handling) — that's `coding-standards--php`
- Choice of EventSauce vs patchlevel/event-sourcing — EventSauce is the default; patchlevel is acceptable when you want a more batteries-included stack
- Symfony framework concerns (kernel, controllers, routing) — these are separate from the framework-agnostic Messenger and DBAL components
