---
name: write-aggregate
description: Write an event-sourced aggregate using EventSauce — aggregate class, domain events, and state replay.
argument-hint: "[aggregate description, e.g. 'Crawl with start and complete']"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
paths:
  - "**/*.php"
---

Write an event-sourced aggregate for $ARGUMENTS.

## Process (sequential — do not skip steps)

### Step 1: Reconnaissance

Before writing the aggregate:

1. **Read existing aggregates** — match the project's patterns:
   ```bash
   grep -rn "AggregateRoot\|AggregateRootBehaviour" --include="*.php" src/ | head -20
   ```

2. **Confirm the event-sourcing library** — EventSauce is the recommended default. If `patchlevel/event-sourcing` is in use, follow its conventions instead (the structure is similar but the trait and method names differ)

3. **Identify the bounded context** — which directory under `src/Domain/` does this aggregate belong to? If unclear, STOP and consult the architect

4. **Identify the events** — what state changes does the aggregate emit? List them before writing the class. Each event corresponds to a fact that happened, in past tense

5. **Identify the invariants** — what must always be true? Examples: a completed crawl cannot be completed again; a page cannot be extracted before the crawl starts

### Step 2: Aggregate ID (Value Object)

The aggregate ID is a typed value object, not a raw string. Use UUID v7 — time-ordered, sorts chronologically, which matters for event-store queries.

```php
<?php

declare(strict_types=1);

namespace App\Domain\Crawl;

use EventSauce\EventSourcing\AggregateRootId;
use Ramsey\Uuid\Uuid;
use Webmozart\Assert\Assert;

final readonly class CrawlId implements AggregateRootId
{
    public function __construct(public string $value)
    {
        Assert::uuid($value);
    }

    public static function generate(): self
    {
        return new self(Uuid::uuid7()->toString());
    }

    public static function fromString(string $id): self
    {
        return new self($id);
    }

    public function toString(): string
    {
        return $this->value;
    }
}
```

### Step 3: Domain Events

Events are `final readonly class`. They represent facts that happened, named in past tense (`CrawlStarted`, not `StartCrawl`). Constructor-promoted, immutable.

```php
<?php

declare(strict_types=1);

namespace App\Domain\Crawl\Event;

use App\Domain\Crawl\CrawlId;
use App\Domain\Crawl\PageId;
use EventSauce\EventSourcing\Serialization\SerializablePayload;

final readonly class CrawlStarted implements SerializablePayload
{
    /**
     * @param list<PageId> $pageIds
     */
    public function __construct(
        public CrawlId $crawlId,
        public array $pageIds,
        public \DateTimeImmutable $startedAt,
    ) {}

    /**
     * @return array<string, mixed>
     */
    public function toPayload(): array
    {
        return [
            'crawl_id' => $this->crawlId->toString(),
            'page_ids' => array_map(static fn (PageId $p): string => $p->toString(), $this->pageIds),
            'started_at' => $this->startedAt->format(\DateTimeInterface::ATOM),
        ];
    }

    /**
     * @param array<string, mixed> $payload
     */
    public static function fromPayload(array $payload): static
    {
        assert(is_string($payload['crawl_id']));
        assert(is_array($payload['page_ids']));
        assert(is_string($payload['started_at']));

        return new self(
            crawlId: CrawlId::fromString($payload['crawl_id']),
            pageIds: array_map(
                static fn (mixed $p): PageId => PageId::fromString((string) $p),
                $payload['page_ids'],
            ),
            startedAt: new \DateTimeImmutable($payload['started_at']),
        );
    }
}
```

**Event rules:**
- Past tense: `CrawlStarted`, `CrawlCompleted`, `PageExtracted`
- One file per event in `src/Domain/<Context>/Event/`
- `final readonly class` with constructor promotion
- Implements `SerializablePayload` (EventSauce) — defines `toPayload()` / `fromPayload()`
- Payload keys are `snake_case` (matches JSON conventions)
- Never include domain logic in events — they are data, not behaviour

### Step 4: Domain Exceptions

Invariant violations throw domain exceptions, never raw `\RuntimeException`.

```php
<?php

declare(strict_types=1);

namespace App\Domain\Crawl\Exception;

use App\Domain\Crawl\CrawlId;
use App\Domain\DomainException;

final class CrawlAlreadyCompleted extends DomainException
{
    public function __construct(public readonly CrawlId $crawlId)
    {
        parent::__construct("Crawl {$crawlId->toString()} is already completed");
    }
}
```

### Step 5: The Aggregate

```php
<?php

declare(strict_types=1);

namespace App\Domain\Crawl;

use App\Domain\Crawl\Event\CrawlCompleted;
use App\Domain\Crawl\Event\CrawlStarted;
use App\Domain\Crawl\Exception\CrawlAlreadyCompleted;
use EventSauce\EventSourcing\AggregateRoot;
use EventSauce\EventSourcing\AggregateRootBehaviour;

final class CrawlAggregate implements AggregateRoot
{
    use AggregateRootBehaviour;

    /** @var list<PageId> */
    private array $pageIds = [];
    private bool $completed = false;

    /**
     * @param list<PageId> $pageIds
     */
    public static function start(CrawlId $id, array $pageIds): self
    {
        $crawl = new self($id);
        $crawl->recordThat(new CrawlStarted($id, $pageIds, new \DateTimeImmutable()));
        return $crawl;
    }

    public function complete(): void
    {
        if ($this->completed) {
            /** @var CrawlId $id */
            $id = $this->aggregateRootId();
            throw new CrawlAlreadyCompleted($id);
        }
        $this->recordThat(new CrawlCompleted(new \DateTimeImmutable()));
    }

    protected function applyCrawlStarted(CrawlStarted $event): void
    {
        $this->pageIds = $event->pageIds;
    }

    protected function applyCrawlCompleted(CrawlCompleted $event): void
    {
        $this->completed = true;
    }
}
```

**Aggregate rules:**
- `final class` with `AggregateRootBehaviour` trait
- Static factory methods for creation (`start`, `register`, `open`) — never `new` directly
- Domain methods (`complete`, `cancel`, `assignTo`) — express what the aggregate *does*, not setters
- State changes via `recordThat()` + `apply*()` — NEVER direct field mutation. If you do `$this->completed = true;` outside `applyCrawlCompleted()`, the change is lost on event replay
- Invariants enforced before `recordThat()` — throw a domain exception if violated
- `apply*()` methods are `protected`, take a single event argument, mutate state, return void
- The aggregate's reconstruction is automatic: EventSauce replays events, calling each `apply*()`

### Step 6: Tests (MANDATORY)

#### Unit test — assert on emitted events, not internal state

```php
<?php

declare(strict_types=1);

namespace App\Tests\Unit\Domain\Crawl;

use App\Domain\Crawl\CrawlAggregate;
use App\Domain\Crawl\CrawlId;
use App\Domain\Crawl\Event\CrawlCompleted;
use App\Domain\Crawl\Event\CrawlStarted;
use App\Domain\Crawl\Exception\CrawlAlreadyCompleted;
use App\Domain\Crawl\PageId;

it('records CrawlStarted when starting', function (): void {
    $id = CrawlId::generate();
    $pages = [PageId::generate(), PageId::generate()];

    $crawl = CrawlAggregate::start($id, $pages);

    expect($crawl->releaseEvents())
        ->toHaveCount(1)
        ->{0}->toBeInstanceOf(CrawlStarted::class);
});

it('records CrawlCompleted when completing', function (): void {
    $crawl = CrawlAggregate::start(CrawlId::generate(), [PageId::generate()]);
    $crawl->releaseEvents(); // discard creation events

    $crawl->complete();

    expect($crawl->releaseEvents())
        ->toHaveCount(1)
        ->{0}->toBeInstanceOf(CrawlCompleted::class);
});

it('throws when completing an already-completed crawl', function (): void {
    $crawl = CrawlAggregate::start(CrawlId::generate(), [PageId::generate()]);
    $crawl->complete();
    $crawl->releaseEvents();

    $crawl->complete();
})->throws(CrawlAlreadyCompleted::class);
```

#### Integration test — verify event-store round-trip

```php
<?php

declare(strict_types=1);

namespace App\Tests\Integration\Domain\Crawl;

use App\Domain\Crawl\CrawlAggregate;
use App\Domain\Crawl\CrawlId;
use App\Domain\Crawl\PageId;
use EventSauce\EventSourcing\AggregateRootRepository;

it('rehydrates the aggregate from the event stream', function (AggregateRootRepository $repo): void {
    $id = CrawlId::generate();
    $crawl = CrawlAggregate::start($id, [PageId::generate()]);
    $crawl->complete();
    $repo->persist($crawl);

    /** @var CrawlAggregate $rehydrated */
    $rehydrated = $repo->retrieve($id);

    // Attempting to complete an already-completed rehydrated crawl proves state replayed correctly
    expect(fn () => $rehydrated->complete())
        ->toThrow(\App\Domain\Crawl\Exception\CrawlAlreadyCompleted::class);
})->with('aggregate_repository');
```

**Test rules:**
- Unit tests assert on **emitted events** (the cascade), not on private state. Private state is the implementation detail; emitted events are the contract
- One assertion per behaviour — the "it does X" naming forces this
- Integration tests prove round-trip persistence — start → persist → rehydrate → continue
- Property-based tests (Eris) for invariants: "for any sequence of valid commands, the aggregate ends in a consistent state"

### Step 7: Snapshot Strategy

Aggregates that accumulate many events (subscriptions billed monthly for years, accounts with thousands of transactions, long-running workflows) become expensive to rehydrate as the stream grows. EventSauce's `SnapshotRepository` is the standard fix — periodically persist the aggregate's state, and on rehydration load the snapshot plus only events recorded since.

```php
// Wire snapshotting in the aggregate repository factory
$snapshotRepository = new ConstructingSnapshotRepository(
    aggregateRootClass: CrawlAggregate::class,
    snapshotStateSerializer: new ConstructingSnapshotStateSerializer(),
    snapshotMessageStorage: $dbalSnapshotStorage,
);

$aggregateRepository = new EventSourcedAggregateRootRepositoryWithSnapshotting(
    aggregateRootClass: CrawlAggregate::class,
    messageRepository: $messageRepository,
    snapshotRepository: $snapshotRepository,
    dispatcher: $dispatcher,
);
```

**Snapshot rules:**
- Snapshot every N events (N=50–100 is a common starting point; tune to event-replay cost)
- Snapshots are disposable — they can always be rebuilt from the event stream. Treat them as a cache, not a source of truth
- When an event's data shape changes (upcaster added), old snapshots become invalid. Delete the snapshot table and rebuild from events, or version snapshots alongside events
- Short-lived aggregates with bounded event counts (e.g., a workflow that emits <20 events then completes) do not need snapshots — skip the complexity

Decide upfront whether this aggregate needs snapshots. If unsure, document the expected event count per aggregate lifetime in the aggregate's docblock and revisit when the count exceeds 100.

## Anti-Patterns (NEVER do these)

- **Mutating fields outside `apply*()`** — the change is invisible on replay. Always go through `recordThat()`
- **Domain logic in events** — events are data. Logic lives in the aggregate
- **Public setters on aggregates** — aggregates expose domain methods (`complete`, `assignTo`), not property setters
- **`extends` from frameworks in the domain** — the aggregate uses the EventSauce trait but does not depend on framework code beyond the AggregateRoot interface. No Doctrine, no Symfony in the domain layer
- **Raw strings as IDs** — wrap in a typed value object (`CrawlId`, not `string $id`)
- **Past-imperfect or future-tense event names** — `CrawlCompleting` or `CrawlWillComplete` are wrong. Past tense only
- **Optional event fields** — every event field is required and typed. Optionality is a smell that the event is two events crammed into one
- **Skipping the invariant check** — `complete()` must throw before recording if the crawl is already complete. Recording an event that should not have happened poisons the stream

## Output

Deliver:
1. Aggregate ID value object (`<Name>Id implements AggregateRootId`)
2. Domain event classes (`final readonly class ... implements SerializablePayload`)
3. Domain exception classes for invariant violations
4. Aggregate class (`final class ... implements AggregateRoot` using `AggregateRootBehaviour`)
5. Unit tests for each domain method (Pest preferred)
6. Integration test proving event-store round-trip
7. Evidence that tests pass (`vendor/bin/pest`, exit code)

## Related Skills

- `/php-developer:write-feature-spec` — write the Behat scenario before this aggregate. The scenario specifies the behaviour; the aggregate satisfies it
- `/php-developer:write-handler` — once the aggregate exists, the handler dispatches commands to it via the message bus
