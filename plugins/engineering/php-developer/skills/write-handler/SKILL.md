---
name: write-handler
description: Write a symfony/messenger command, query, or event handler with constructor injection and bus dispatch.
argument-hint: "[handler description, e.g. 'CompleteCrawl command handler']"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
paths:
  - "**/*.php"
---

Write a symfony/messenger handler for $ARGUMENTS.

## Process (sequential — do not skip steps)

### Step 1: Reconnaissance (RUN BEFORE WRITING ANY CODE)

This step is pre-emptive — it discovers what already exists. Do NOT skip ahead to writing the handler and then run grep "to verify". The reconnaissance commands must run first, their output reported in your response, and the design choices below must reflect what you actually found.

1. **Read existing handlers** — match the project's patterns:
   ```bash
   grep -rn "AsMessageHandler\|MessageHandlerInterface" --include="*.php" src/ | head -20
   ```

2. **Identify the bus** — which of the three buses does this message belong to?
   - `command.bus` — one handler, returns void, mutates aggregate state
   - `query.bus` — one handler, returns a result, no side effects
   - `event.bus` — zero or more handlers, returns void, reacts to a fact that happened

3. **Identify the aggregate or read model** — which aggregate does this handler operate on, or which read model does it query?

4. **Identify cascades** — does this handler dispatch follow-on messages? Each cascade is its own independent unit of work

5. **Check for existing messages** — reuse existing command/event types where appropriate. Don't create `CompleteCrawl` and `MarkCrawlCompleted` for the same thing

### Step 2: Message Class

The message is `final readonly class` — constructor-promoted, immutable, no logic. Messages live in `src/Application/<Context>/` alongside their handlers.

```php
<?php

declare(strict_types=1);

namespace App\Application\Crawl;

use App\Domain\Crawl\CrawlId;

final readonly class CompleteCrawl
{
    public function __construct(public CrawlId $crawlId) {}
}
```

**Message rules:**
- `final readonly class` — immutable, constructor-promoted
- Named in the imperative for commands (`CompleteCrawl`, not `CrawlCompletion`)
- Named with a noun for queries (`CrawlSummary`, not `GetCrawlSummary`)
- Typed properties only — `CrawlId` not `string $crawlId`
- No defaults that hide intent — every property either has a meaningful default or is required

### Step 3: Command Handler

A command handler mutates state and returns nothing. Cascades are dispatched, not returned.

```php
<?php

declare(strict_types=1);

namespace App\Application\Crawl;

use App\Domain\Crawl\CrawlAggregate;
use EventSauce\EventSourcing\AggregateRootRepository;
use Symfony\Component\Messenger\Attribute\AsMessageHandler;

#[AsMessageHandler(bus: 'command.bus')]
final readonly class CompleteCrawlHandler
{
    public function __construct(
        private AggregateRootRepository $repository,
    ) {}

    public function __invoke(CompleteCrawl $command): void
    {
        /** @var CrawlAggregate $crawl */
        $crawl = $this->repository->retrieve($command->crawlId);
        $crawl->complete();
        $this->repository->persist($crawl);
    }
}
```

**Command handler rules:**
- `final readonly class` with `__invoke()`
- `#[AsMessageHandler(bus: 'command.bus')]` attribute binds the handler to the command bus
- Constructor injection only — never service location, never `$container->get()`
- The handler is thin: load aggregate → call domain method → persist. Domain logic stays in the aggregate
- Cascading events flow via subscribers on the event bus, not by dispatching cascades from inside the handler — keep this handler focused on one aggregate

### Step 4: Query Handler

A query handler returns a result and has no side effects. Read from a projection or repository, never from event streams.

```php
<?php

declare(strict_types=1);

namespace App\Application\Crawl\Query;

use App\Domain\Crawl\CrawlId;
use App\Infrastructure\ReadModel\CrawlSummaryRepository;
use Symfony\Component\Messenger\Attribute\AsMessageHandler;

final readonly class GetCrawlSummary
{
    public function __construct(public CrawlId $crawlId) {}
}

final readonly class CrawlSummaryResult
{
    public function __construct(
        public CrawlId $crawlId,
        public int $totalPages,
        public int $extractedPages,
        public ?\DateTimeImmutable $completedAt,
    ) {}
}

#[AsMessageHandler(bus: 'query.bus')]
final readonly class GetCrawlSummaryHandler
{
    public function __construct(
        private CrawlSummaryRepository $summaries,
    ) {}

    public function __invoke(GetCrawlSummary $query): CrawlSummaryResult
    {
        $summary = $this->summaries->find($query->crawlId)
            ?? throw new \App\Application\Crawl\Exception\CrawlSummaryNotFound($query->crawlId);

        return new CrawlSummaryResult(
            crawlId: $summary->crawlId,
            totalPages: $summary->totalPages,
            extractedPages: $summary->extractedPages,
            completedAt: $summary->completedAt,
        );
    }
}
```

**Query handler rules:**
- Returns a typed result object (`final readonly class`), never `array` or `mixed`
- Throws a domain exception when the queried entity is missing — never returns `null` silently
- Reads from a projection / read-model repository, not by replaying events. Event replay belongs to the write side
- Pure — no state changes, no message dispatch, no side effects beyond the read

### Step 5: Event Subscriber (Projection)

Event subscribers react to facts. Multiple subscribers per event. Use them to build read models, send notifications, or trigger downstream commands.

```php
<?php

declare(strict_types=1);

namespace App\Application\Crawl\Projection;

use App\Domain\Crawl\Event\CrawlCompleted;
use App\Domain\Crawl\Event\CrawlStarted;
use App\Infrastructure\ReadModel\CrawlSummaryRepository;
use Symfony\Component\Messenger\Attribute\AsMessageHandler;

final readonly class CrawlSummaryProjection
{
    public function __construct(private CrawlSummaryRepository $summaries) {}

    #[AsMessageHandler(bus: 'event.bus')]
    public function whenCrawlStarted(CrawlStarted $event): void
    {
        $this->summaries->insert(
            crawlId: $event->crawlId,
            totalPages: count($event->pageIds),
            startedAt: $event->startedAt,
        );
    }

    #[AsMessageHandler(bus: 'event.bus')]
    public function whenCrawlCompleted(CrawlCompleted $event): void
    {
        $this->summaries->markCompleted($event->crawlId, $event->completedAt);
    }
}
```

**Subscriber rules:**
- One projection class per read model — group related event handlers
- Each method has its own `#[AsMessageHandler(bus: 'event.bus')]` attribute
- Method name describes the trigger: `whenCrawlStarted`, `whenPageExtracted`
- Idempotent — replaying an event should produce the same read model. Use `INSERT ... ON CONFLICT` or check-then-write
- Fast — no external HTTP calls in inline projections. If you need to call an external service, dispatch a command, don't block the projection

### Step 6: One Message, One Unit of Work (IRON LAW)

If you find yourself looping over N items inside a handler, you are doing it wrong. Fan out by dispatching N messages.

```php
// WRONG — processing N items inline
public function __invoke(ExtractAllPages $command): void
{
    foreach ($command->pageIds as $pageId) {
        $this->extractor->extract($pageId);  // BAD: page 47 failing loses pages 1-46
    }
}

// CORRECT — fan out one message per item
public function __invoke(ExtractAllPages $command): void
{
    foreach ($command->pageIds as $pageId) {
        $this->commandBus->dispatch(new ExtractPage($command->crawlId, $pageId));
    }
}
```

**Why:**
- Individual failures don't block the batch — page 47 failing doesn't affect pages 1-46
- symfony/messenger handles retries per message — each unit of work can be retried independently
- Workers can process fan-out messages concurrently
- Observability — each message has its own trace, timing, and error reporting

### Step 7: Error Handling

```php
// Fatal errors — let them propagate. Messenger retries per the configured policy
public function __invoke(CompleteCrawl $command): void
{
    $crawl = $this->repository->retrieve($command->crawlId);
    $crawl->complete();              // may throw CrawlAlreadyCompleted — bubble up
    $this->repository->persist($crawl); // may throw on optimistic-concurrency conflict — bubble up
}

// Non-fatal — catch the specific exception, log, do not retry
public function __invoke(NotifyExternalService $command): void
{
    try {
        $this->client->notify($command->payload);
    } catch (HttpClientException $e) {
        $this->logger->warning('External notification failed', [
            'command_id' => $command->id,
            'exception' => $e->getMessage(),
        ]);
        // Swallow — external system is best-effort, don't retry-loop
    }
}
```

**Error handling rules:**
- **Fatal errors** (DB unavailable, aggregate missing, concurrency conflict): let them propagate. Messenger retries per policy; failed retries land in the failure transport
- **Non-fatal errors** (best-effort external calls, expected validation failures): catch the specific exception, log with context, do not re-throw
- **Never bare `catch (\Exception $e)`** — top-level handlers in HTTP/CLI entry points are the only exception
- Configure retry strategy per message class in messenger config — not per handler
- Failed messages go to the failure transport. Monitor it. Don't let it grow silently

**Retry configuration** in `messenger.yaml` (or the bus config) — every message-bearing transport needs an explicit `retry_strategy` and a `failure_transport`:

```yaml
framework:
    messenger:
        failure_transport: failed
        transports:
            async:
                dsn: '%env(MESSENGER_TRANSPORT_DSN)%'
                retry_strategy:
                    max_retries: 3
                    delay: 1000          # 1s
                    multiplier: 2        # 1s, 2s, 4s
                    max_delay: 10000     # cap at 10s
            failed:
                dsn: 'doctrine://default?queue_name=failed'
```

Tune per message class for messages with different idempotency or cost profiles. Idempotent commands can retry aggressively; commands with side-effects (notifications, payments) should retry less. Document the choice in the messenger config — future-you will not remember why `max_retries: 3` instead of `5`.

### Step 8: Tests (MANDATORY)

#### Unit test — handler with mocked dependencies

```php
<?php

declare(strict_types=1);

it('completes the crawl and persists', function (): void {
    $id = CrawlId::generate();
    $crawl = CrawlAggregate::start($id, [PageId::generate()]);
    $repository = Mockery::mock(AggregateRootRepository::class);
    $repository->shouldReceive('retrieve')->with($id)->andReturn($crawl);
    $repository->shouldReceive('persist')->with($crawl)->once();

    $handler = new CompleteCrawlHandler($repository);
    $handler(new CompleteCrawl($id));

    // Behaviour: the aggregate emits CrawlCompleted (verified via the event releaser pattern)
    expect($crawl->releaseEvents())->toHaveCount(1);
});
```

#### Integration test — through the message bus

```php
<?php

declare(strict_types=1);

it('dispatches CompleteCrawl through the bus and projects the summary', function (
    MessageBusInterface $commandBus,
    CrawlSummaryRepository $summaries,
): void {
    $id = CrawlId::generate();
    // Seed: dispatch StartCrawl first (or seed event stream directly)
    $commandBus->dispatch(new StartCrawl($id, [PageId::generate()]));

    $commandBus->dispatch(new CompleteCrawl($id));

    $summary = $summaries->find($id);
    expect($summary)->not->toBeNull()
        ->and($summary->completedAt)->not->toBeNull();
})->with('messenger_test_container');
```

**Test rules:**
- Unit test: mock the repository, prove the handler calls the right aggregate methods
- Integration test: dispatch through the real `MessageBusInterface` from the test container — never `new CancelSubscriptionHandler($repo)`. Instantiating the handler directly bypasses the bus, the messenger middleware stack (transaction, retry, outbox), and the routing config — none of which get tested. If your "integration test" instantiates the handler, it is a unit test mislabelled
- Don't test the framework — symfony/messenger has its own tests. Test your handler's behaviour
- For event subscribers, integration test with the real event dispatched through `event.bus`; assert on the projection

## Anti-Patterns (NEVER do these)

- **Multiple command handlers per command** — symfony/messenger enforces this; don't fight it with conditional dispatch
- **Returning from a command handler** — commands are fire-and-forget; if you need a result, it's a query
- **Domain logic in the handler** — the handler is thin. `if ($crawl->status === 'pending') { ... }` belongs in the aggregate
- **Service location** — `$this->container->get('something')` defeats DI. Constructor injection only
- **Inline loops processing N items** — fan out via N messages
- **Catching `\Throwable` to keep workers alive** — let messenger handle retry and dead-lettering. Don't muffle errors
- **Manual transaction management** — let the messenger middleware or your repository handle transactions. Don't `beginTransaction()` in the handler
- **Side effects in queries** — queries are pure reads. No logging, no metrics increments, no event dispatch

## Output

Deliver:
1. Message class (`final readonly class` for command/query/event)
2. Handler class (`final readonly class` with `__invoke()`)
3. For queries: result type (`final readonly class`)
4. For commands: domain exception classes if new ones are needed
5. messenger configuration update if the message routes to a non-default transport
6. Unit test with mocked dependencies
7. Integration test through the bus
8. Evidence that tests pass (`vendor/bin/pest`, exit code)

## Related Skills

- `/php-developer:write-aggregate` — command handlers operate on aggregates. Write the aggregate first
- `/php-developer:write-feature-spec` — the Behat scenario specifies the user-facing behaviour the handler delivers
