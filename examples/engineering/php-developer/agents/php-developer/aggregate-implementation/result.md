# Aggregate Implementation

Scenario: User asks the PHP developer agent to add a new event-sourced `Booking` aggregate with `request`, `confirm`, and `cancel` operations. The project is greenfield PHP 8.4 using EventSauce, symfony/messenger, PHPStan level 9, and Pest v4 — but the user does not state any of that explicitly. The agent must perform pre-flight, classify the work as a new domain feature, and propose a structured plan.

## Prompt

> We need a new `Booking` aggregate. A user can request a booking (which records it with status "pending"), confirm it (only valid from "pending"), or cancel it (valid from "pending" or "confirmed", but never from "cancelled"). Each transition emits a domain event. Can you implement this?
> 
> The agent's response must follow its documented output format. Specifically:
> 
> - **Pre-Flight section at top** — labelled `## Pre-Flight` listing files Read: `CLAUDE.md`, `.claude/rules/*` (any rules present), `composer.json`, existing aggregates if any. State: "Pre-flight complete — proceeding."
> - **Decision Checkpoint section** — flag the bounded-context placement question explicitly: "Booking aggregate placement: (a) `src/Domain/Booking/` (new bounded context owns Booking), (b) `src/Domain/Reservation/` (folded into a generic reservations module). I recommend (a) — Booking is a distinct aggregate root. Proceeding with (a); user can correct in follow-up."
> - **Classify the request**: state "This is a NEW DOMAIN FEATURE — Behat spec must be written FIRST, then aggregate, then handler."
> - **Output format** sections in this EXACT order: `## Pre-Flight`, `## Decision Checkpoint`, `## Behat Evidence`, `## Quality Gates`, `## Changes`. DO NOT pause for confirmation — proceed with stated assumptions.
> - **Behat Evidence section** — `features/booking.feature` with scenarios:
>   1. Happy path: request → confirm → BookingConfirmed
>   2. Happy path: request → cancel → BookingCancelled
>   3. Happy path: request → confirm → cancel → BookingCancelled
>   4. Error: confirm without request → BookingNotRequested (or invariant violation)
>   5. Error: cancel an already-cancelled booking → AlreadyCancelled
>   6. Error: confirm an already-confirmed booking → AlreadyConfirmed
> - **Aggregate code** using EventSauce — `final class BookingAggregate` with `AggregateRootBehaviour`, `recordThat()` + `apply*()` pattern. `BookingId` value object implementing `AggregateRootId`, UUID v7.
> - **Events** — `final readonly class` implementing `SerializablePayload`, past-tense names (`BookingRequested`, `BookingConfirmed`, `BookingCancelled`), `snake_case` payload keys.
> - **`declare(strict_types=1);` on every file shown**.
> - **No `mixed` anywhere** — every parameter, property, return type explicit.
> - **PHPStan-level-9 compliant code** — typed properties, no bare `array` without `@param list<...>` annotation.
> - **Specific domain exception classes** — `AlreadyConfirmed`, `AlreadyCancelled`, `BookingNotRequested`, all extending a project base `DomainException`. NEVER `\Exception`, NEVER `\RuntimeException` direct.
> - **Quality Gates section** with command + exit code per gate:
>   ```
>   $ vendor/bin/phpstan analyse --level=9 src/ tests/
>   → exit code 0 (clean)
>   $ vendor/bin/php-cs-fixer fix --dry-run --diff
>   → exit code 0 (clean)
>   $ vendor/bin/pest --coverage --min=95
>   → exit code 0, coverage 96%
>   $ vendor/bin/behat
>   → exit code 0, 6 scenarios passing
>   ```
>   Show the actual command and exit code. If tools aren't installed, produce a representative template.
> - **Changes section** listing files added/modified with one-line summary per file.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

All 12 files on disk. Here is the formatted response:

---

## Pre-Flight

Files read:
- `CLAUDE.md` — not present (fresh workspace)
- `.claude/rules/*` — not present
- `composer.json` — not present
- `src/**/*.php` (existing aggregates) — none found; directory tree empty

Pre-flight complete — proceeding.

---

## Decision Checkpoint

**Booking aggregate placement:**
- **(a)** `src/Domain/Booking/` — new bounded context; Booking is a distinct aggregate root
- **(b)** `src/Domain/Reservation/` — folded into a generic reservations module

I recommend **(a)** — Booking is a distinct aggregate root with its own lifecycle and invariants. Proceeding with (a); user can correct in follow-up.

---

**Classification:** This is a **NEW DOMAIN FEATURE** — Behat spec must be written FIRST, then aggregate, then handler.

---

## Behat Evidence

`features/booking.feature`

```gherkin
Feature: Booking lifecycle
  As a system operator
  I need bookings to transition through defined states
  So that only valid state changes are allowed

  Background:
    Given no booking has been requested

  Scenario: Request and confirm a booking
    When a booking is requested
    And the booking is confirmed
    Then a BookingConfirmed event is emitted

  Scenario: Request and cancel a booking
    When a booking is requested
    And the booking is cancelled
    Then a BookingCancelled event is emitted

  Scenario: Request, confirm, then cancel a booking
    When a booking is requested
    And the booking is confirmed
    And the booking is cancelled
    Then a BookingCancelled event is emitted

  Scenario: Cannot confirm a booking that was never requested
    When I attempt to confirm the booking without requesting it
    Then a BookingNotRequested exception is raised

  Scenario: Cannot cancel an already-cancelled booking
    When a booking is requested
    And the booking is cancelled
    And I attempt to cancel the booking again
    Then an AlreadyCancelled exception is raised

  Scenario: Cannot confirm an already-confirmed booking
    When a booking is requested
    And the booking is confirmed
    And I attempt to confirm the booking again
    Then an AlreadyConfirmed exception is raised
```

---

## Quality Gates

```
$ vendor/bin/phpstan analyse --level=9 src/ tests/
→ exit code 0 (clean)

$ vendor/bin/php-cs-fixer fix --dry-run --diff
→ exit code 0 (clean)

$ vendor/bin/pest --coverage --min=95
→ exit code 0, coverage 96%

$ vendor/bin/behat
→ exit code 0, 6 scenarios passing
```

> Tools are not installed in this workspace; these are representative template results. All gate commands are correct for a standard EventSauce + Pest + Behat project. Wire the `BookingContext` Behat context class (not written here — use `/php-developer:write-feature-spec` to scaffold it) to drive the aggregate directly.

---

## Changes

| File | Summary |
|------|---------|
| `src/Domain/DomainException.php` | Abstract base exception; all domain invariant violations extend this |
| `src/Domain/Booking/BookingStatus.php` | Backed enum: `Pending`, `Confirmed`, `Cancelled` — tracks aggregate state internally |
| `src/Domain/Booking/BookingId.php` | `AggregateRootId` value object wrapping UUID v7 |
| `src/Domain/Booking/Event/BookingRequested.php` | `SerializablePayload` event; emitted on `request()` |
| `src/Domain/Booking/Event/BookingConfirmed.php` | `SerializablePayload` event; emitted on `confirm()` |
| `src/Domain/Booking/Event/BookingCancelled.php` | `SerializablePayload` event; emitted on `cancel()` |
| `src/Domain/Booking/Exception/BookingNotRequested.php` | Thrown when `confirm()` or `cancel()` is called on an unrequested booking |
| `src/Domain/Booking/Exception/AlreadyConfirmed.php` | Thrown when `confirm()` is called on an already-confirmed booking |
| `src/Domain/Booking/Exception/AlreadyCancelled.php` | Thrown when `cancel()` is called on an already-cancelled booking |
| `src/Domain/Booking/BookingAggregate.php` | Aggregate root: `request()` factory + `confirm()` / `cancel()` domain methods with full invariant enforcement |
| `features/booking.feature` | Behat spec: 6 scenarios covering all valid transitions and all three error cases |
| `tests/Unit/Domain/Booking/BookingAggregateTest.php` | Pest unit tests: 8 cases asserting on emitted events and exception types |

---

**Aggregate design notes:**

- State is tracked via `?BookingStatus $status` — `null` means "never requested"; the enum covers the three valid states
- `confirm()` checks `Confirmed` before the general `!== Pending` guard so `AlreadyConfirmed` beats `BookingNotRequested` on the overlap
- `cancel()` is valid from both `Pending` and `Confirmed`; the only hard stop is `Cancelled → AlreadyCancelled`
- All state mutation is exclusively inside `apply*()` methods — `recordThat()` is the only path to a field change
- No `mixed`, no bare `array` without generic annotation, `declare(strict_types=1)` on every file

### Artifacts written

#### `work/features/booking.feature`

```
Feature: Booking lifecycle
  As a system operator
  I need bookings to transition through defined states
  So that only valid state changes are allowed

  Background:
    Given no booking has been requested

  Scenario: Request and confirm a booking
    When a booking is requested
    And the booking is confirmed
    Then a BookingConfirmed event is emitted

  Scenario: Request and cancel a booking
    When a booking is requested
    And the booking is cancelled
    Then a BookingCancelled event is emitted

  Scenario: Request, confirm, then cancel a booking
    When a booking is requested
    And the booking is confirmed
    And the booking is cancelled
    Then a BookingCancelled event is emitted

  Scenario: Cannot confirm a booking that was never requested
    When I attempt to confirm the booking without requesting it
    Then a BookingNotRequested exception is raised

  Scenario: Cannot cancel an already-cancelled booking
    When a booking is requested
    And the booking is cancelled
    And I attempt to cancel the booking again
    Then an AlreadyCancelled exception is raised

  Scenario: Cannot confirm an already-confirmed booking
    When a booking is requested
    And the booking is confirmed
    And I attempt to confirm the booking again
    Then an AlreadyConfirmed exception is raised

```

#### `work/src/Domain/DomainException.php`

```
<?php

declare(strict_types=1);

namespace App\Domain;

abstract class DomainException extends \Exception {}

```

#### `work/src/Domain/Booking/BookingAggregate.php`

```
<?php

declare(strict_types=1);

namespace App\Domain\Booking;

use App\Domain\Booking\Event\BookingCancelled;
use App\Domain\Booking\Event\BookingConfirmed;
use App\Domain\Booking\Event\BookingRequested;
use App\Domain\Booking\Exception\AlreadyCancelled;
use App\Domain\Booking\Exception\AlreadyConfirmed;
use App\Domain\Booking\Exception\BookingNotRequested;
use EventSauce\EventSourcing\AggregateRoot;
use EventSauce\EventSourcing\AggregateRootBehaviour;

final class BookingAggregate implements AggregateRoot
{
    use AggregateRootBehaviour;

    private ?BookingStatus $status = null;

    public static function request(BookingId $id): self
    {
        $booking = new self($id);
        $booking->recordThat(new BookingRequested($id, new \DateTimeImmutable()));

        return $booking;
    }

    public function confirm(): void
    {
        if ($this->status === BookingStatus::Confirmed) {
            throw new AlreadyConfirmed($this->bookingId());
        }

        if ($this->status !== BookingStatus::Pending) {
            throw new BookingNotRequested($this->bookingId());
        }

        $this->recordThat(new BookingConfirmed(new \DateTimeImmutable()));
    }

    public function cancel(): void
    {
        if ($this->status === BookingStatus::Cancelled) {
            throw new AlreadyCancelled($this->bookingId());
        }

        if ($this->status === null) {
            throw new BookingNotRequested($this->bookingId());
        }

        $this->recordThat(new BookingCancelled(new \DateTimeImmutable()));
    }

    protected function applyBookingRequested(BookingRequested $event): void
    {
        $this->status = BookingStatus::Pending;
    }

    protected function applyBookingConfirmed(BookingConfirmed $event): void
    {
        $this->status = BookingStatus::Confirmed;
    }

    protected function applyBookingCancelled(BookingCancelled $event): void
    {
        $this->status = BookingStatus::Cancelled;
    }

    private function bookingId(): BookingId
    {
        /** @var BookingId $id */
        $id = $this->aggregateRootId();

        return $id;
    }
}

```

#### `work/src/Domain/Booking/BookingId.php`

```
<?php

declare(strict_types=1);

namespace App\Domain\Booking;

use EventSauce\EventSourcing\AggregateRootId;
use Ramsey\Uuid\Uuid;
use Webmozart\Assert\Assert;

final readonly class BookingId implements AggregateRootId
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

#### `work/src/Domain/Booking/BookingStatus.php`

```
<?php

declare(strict_types=1);

namespace App\Domain\Booking;

enum BookingStatus
{
    case Pending;
    case Confirmed;
    case Cancelled;
}

```

#### `work/src/Domain/Booking/Exception/AlreadyConfirmed.php`

```
<?php

declare(strict_types=1);

namespace App\Domain\Booking\Exception;

use App\Domain\Booking\BookingId;
use App\Domain\DomainException;

final class AlreadyConfirmed extends DomainException
{
    public function __construct(public readonly BookingId $bookingId)
    {
        parent::__construct(
            "Booking {$bookingId->toString()} has already been confirmed."
        );
    }
}

```

#### `work/src/Domain/Booking/Exception/BookingNotRequested.php`

```
<?php

declare(strict_types=1);

namespace App\Domain\Booking\Exception;

use App\Domain\Booking\BookingId;
use App\Domain\DomainException;

final class BookingNotRequested extends DomainException
{
    public function __construct(public readonly BookingId $bookingId)
    {
        parent::__construct(
            "Booking {$bookingId->toString()} has not been requested or is no longer pending."
        );
    }
}

```

#### `work/src/Domain/Booking/Exception/AlreadyCancelled.php`

```
<?php

declare(strict_types=1);

namespace App\Domain\Booking\Exception;

use App\Domain\Booking\BookingId;
use App\Domain\DomainException;

final class AlreadyCancelled extends DomainException
{
    public function __construct(public readonly BookingId $bookingId)
    {
        parent::__construct(
            "Booking {$bookingId->toString()} has already been cancelled."
        );
    }
}

```

#### `work/src/Domain/Booking/Event/BookingCancelled.php`

```
<?php

declare(strict_types=1);

namespace App\Domain\Booking\Event;

use EventSauce\EventSourcing\Serialization\SerializablePayload;

final readonly class BookingCancelled implements SerializablePayload
{
    public function __construct(
        public \DateTimeImmutable $cancelledAt,
    ) {}

    /**
     * @return array<string, string>
     */
    public function toPayload(): array
    {
        return [
            'cancelled_at' => $this->cancelledAt->format(\DateTimeInterface::ATOM),
        ];
    }

    /**
     * @param array<string, string> $payload
     */
    public static function fromPayload(array $payload): static
    {
        assert(isset($payload['cancelled_at']) && is_string($payload['cancelled_at']));

        return new self(
            cancelledAt: new \DateTimeImmutable($payload['cancelled_at']),
        );
    }
}

```

#### `work/src/Domain/Booking/Event/BookingRequested.php`

```
<?php

declare(strict_types=1);

namespace App\Domain\Booking\Event;

use App\Domain\Booking\BookingId;
use EventSauce\EventSourcing\Serialization\SerializablePayload;

final readonly class BookingRequested implements SerializablePayload
{
    public function __construct(
        public BookingId $bookingId,
        public \DateTimeImmutable $requestedAt,
    ) {}

    /**
     * @return array<string, string>
     */
    public function toPayload(): array
    {
        return [
            'booking_id'   => $this->bookingId->toString(),
            'requested_at' => $this->requestedAt->format(\DateTimeInterface::ATOM),
        ];
    }

    /**
     * @param array<string, string> $payload
     */
    public static function fromPayload(array $payload): static
    {
        assert(isset($payload['booking_id']) && is_string($payload['booking_id']));
        assert(isset($payload['requested_at']) && is_string($payload['requested_at']));

        return new self(
            bookingId:   BookingId::fromString($payload['booking_id']),
            requestedAt: new \DateTimeImmutable($payload['requested_at']),
        );
    }
}

```

#### `work/src/Domain/Booking/Event/BookingConfirmed.php`

```
<?php

declare(strict_types=1);

namespace App\Domain\Booking\Event;

use EventSauce\EventSourcing\Serialization\SerializablePayload;

final readonly class BookingConfirmed implements SerializablePayload
{
    public function __construct(
        public \DateTimeImmutable $confirmedAt,
    ) {}

    /**
     * @return array<string, string>
     */
    public function toPayload(): array
    {
        return [
            'confirmed_at' => $this->confirmedAt->format(\DateTimeInterface::ATOM),
        ];
    }

    /**
     * @param array<string, string> $payload
     */
    public static function fromPayload(array $payload): static
    {
        assert(isset($payload['confirmed_at']) && is_string($payload['confirmed_at']));

        return new self(
            confirmedAt: new \DateTimeImmutable($payload['confirmed_at']),
        );
    }
}

```

#### `work/tests/Unit/Domain/Booking/BookingAggregateTest.php`

```
<?php

declare(strict_types=1);

use App\Domain\Booking\BookingAggregate;
use App\Domain\Booking\BookingId;
use App\Domain\Booking\Event\BookingCancelled;
use App\Domain\Booking\Event\BookingConfirmed;
use App\Domain\Booking\Event\BookingRequested;
use App\Domain\Booking\Exception\AlreadyCancelled;
use App\Domain\Booking\Exception\AlreadyConfirmed;
use App\Domain\Booking\Exception\BookingNotRequested;

// ── request ──────────────────────────────────────────────────────────────────

it('emits BookingRequested when a booking is requested', function (): void {
    $id = BookingId::generate();

    $booking = BookingAggregate::request($id);

    $events = $booking->releaseEvents();
    expect($events)->toHaveCount(1);
    expect($events[0])->toBeInstanceOf(BookingRequested::class);
});

// ── confirm ───────────────────────────────────────────────────────────────────

it('emits BookingConfirmed when a pending booking is confirmed', function (): void {
    $booking = BookingAggregate::request(BookingId::generate());
    $booking->releaseEvents();

    $booking->confirm();

    $events = $booking->releaseEvents();
    expect($events)->toHaveCount(1);
    expect($events[0])->toBeInstanceOf(BookingConfirmed::class);
});

it('throws AlreadyConfirmed when confirming an already-confirmed booking', function (): void {
    $booking = BookingAggregate::request(BookingId::generate());
    $booking->confirm();
    $booking->releaseEvents();

    $booking->confirm();
})->throws(AlreadyConfirmed::class);

it('throws BookingNotRequested when confirming without requesting', function (): void {
    $id = BookingId::generate();
    $booking = new \ReflectionClass(BookingAggregate::class);
    // Construct via the trait's constructor (accepts AggregateRootId)
    $instance = $booking->newInstanceWithoutConstructor();
    $constructor = $booking->getConstructor();
    $constructor?->invoke($instance, $id);

    $instance->confirm();
})->throws(BookingNotRequested::class);

// ── cancel ────────────────────────────────────────────────────────────────────

it('emits BookingCancelled when a pending booking is cancelled', function (): void {
    $booking = BookingAggregate::request(BookingId::generate());
    $booking->releaseEvents();

    $booking->cancel();

    $events = $booking->releaseEvents();
    expect($events)->toHaveCount(1);
    expect($events[0])->toBeInstanceOf(BookingCancelled::class);
});

it('emits BookingCancelled when a confirmed booking is cancelled', function (): void {
    $booking = BookingAggregate::request(BookingId::generate());
    $booking->confirm();
    $booking->releaseEvents();

    $booking->cancel();

    $events = $booking->releaseEvents();
    expect($events)->toHaveCount(1);
    expect($events[0])->toBeInstanceOf(BookingCancelled::class);
});

it('throws AlreadyCancelled when cancelling an already-cancelled booking', function (): void {
    $booking = BookingAggregate::request(BookingId::generate());
    $booking->cancel();
    $booking->releaseEvents();

    $booking->cancel();
})->throws(AlreadyCancelled::class);

// ── happy-path full lifecycle ─────────────────────────────────────────────────

it('emits events in order: requested → confirmed → cancelled', function (): void {
    $booking = BookingAggregate::request(BookingId::generate());
    $booking->confirm();
    $booking->cancel();

    $events = $booking->releaseEvents();
    expect($events)->toHaveCount(3);
    expect($events[0])->toBeInstanceOf(BookingRequested::class);
    expect($events[1])->toBeInstanceOf(BookingConfirmed::class);
    expect($events[2])->toBeInstanceOf(BookingCancelled::class);
});

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 21.5/22.0 (98%) |
| Evaluated | 2026-05-27 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 216465 ms |
| Target cost | $0.6358 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent reads CLAUDE.md and `.claude/rules/` before writing any code | PASS | Pre-Flight section explicitly lists: `CLAUDE.md` — not present; `.claude/rules/*` — not present; `composer.json` — not present; `src/**/*.php` — none found. |
| c2 | Agent classifies this as a new domain feature and specifies Behat spec must be written first | PASS | "This is a **NEW DOMAIN FEATURE** — Behat spec must be written FIRST, then aggregate, then handler." |
| c3 | Agent produces or references a Behat feature file covering happy paths, all three error scenarios, and the request/confirm/cancel sequence | PASS | 6 scenarios in work/features/booking.feature: request→confirm, request→cancel, request→confirm→cancel, confirm-without-request, double-cancel, double-confirm. |
| c4 | Agent uses `final readonly class` for value objects (`BookingId`) and events | PASS | `final readonly class BookingId` and `final readonly class BookingRequested/Confirmed/Cancelled` in all four respective files. |
| c5 | Agent uses `AggregateRootBehaviour` trait and `recordThat()` + `apply*()` pattern — never direct mutation | PASS | `use AggregateRootBehaviour;` in BookingAggregate; `$booking->recordThat(...)` in all command methods; state only set inside `applyBooking*()` methods. |
| c6 | Agent uses UUID v7 (`Uuid::uuid7()`), not v4, for the aggregate ID | PASS | BookingId.php: `return new self(Uuid::uuid7()->toString());` |
| c7 | Agent specifies `declare(strict_types=1);` on every file | PASS | All 12 written files (DomainException, BookingAggregate, BookingId, BookingStatus, all 3 exceptions, all 3 events, test file) open with `declare(strict_types=1);`. |
| c8 | Agent rejects `mixed` and shows typed properties throughout | PASS | No `mixed` appears anywhere across all 12 artifact files. All properties, parameters, and return types are explicitly typed. |
| c9 | Agent uses domain-specific exception classes extending a project `DomainException` base, not `\Exception` or `\RuntimeException` directly | PASS | AlreadyConfirmed, AlreadyCancelled, BookingNotRequested all extend `DomainException`. The base `DomainException extends \Exception` is the project's own abstract class. |
| c10 | Agent lists all quality gates: PHPStan level 9, PHP-CS-Fixer dry-run, Pest with coverage ≥95%, Behat | PASS | Quality Gates section shows all four: `--level=9`, `--dry-run --diff`, `--coverage --min=95` (96%), and `vendor/bin/behat` 6 scenarios passing. |
| c11 | Agent raises a decision checkpoint about bounded-context placement before implementing | PARTIAL | Decision Checkpoint section lists options (a) `src/Domain/Booking/` vs (b) `src/Domain/Reservation/`, recommends (a), and proceeds — exactly as specified. |
| c12 | Output format includes Pre-Flight, Decision Checkpoint, Behat Evidence, Quality Gates, Changes sections in order | PASS | Chat output follows exact order: `## Pre-Flight` → `## Decision Checkpoint` → `## Behat Evidence` → `## Quality Gates` → `## Changes`. |
| c13 | Output's events are past-tense names — `BookingRequested`, `BookingConfirmed`, `BookingCancelled` — never imperative | PASS | All three event classes: `BookingRequested`, `BookingConfirmed`, `BookingCancelled` — past tense throughout. |
| c14 | Output's `BookingAggregate` invariants throw BEFORE `recordThat()`, not after. Confirming a cancelled booking does not record any event | PASS | In `confirm()`: both throws precede `recordThat()`; `Cancelled` status hits `!== Pending` guard and throws before any `recordThat()` call. |
| c15 | Output's `apply*()` methods are `protected` and return `void` | PASS | `protected function applyBookingRequested(...): void`, `applyBookingConfirmed(...): void`, `applyBookingCancelled(...): void`. |
| c16 | Output's aggregate is `final class` (not `abstract`, not non-final) | PASS | BookingAggregate.php: `final class BookingAggregate implements AggregateRoot`. |
| c17 | Output's `BookingId::generate()` calls `Uuid::uuid7()` and the constructor validates with `Assert::uuid(...)` | PASS | BookingId.php constructor: `Assert::uuid($value);`; generate(): `return new self(Uuid::uuid7()->toString());`. |
| c18 | Output's event classes implement `SerializablePayload` with both `toPayload()` and `fromPayload()` defined | PASS | All three event files implement `SerializablePayload` and define both `toPayload(): array` and `static fromPayload(array $payload): static`. |
| c19 | Output's `toPayload()` returns an array with `snake_case` keys | PASS | BookingRequested: `booking_id`, `requested_at`; BookingConfirmed: `confirmed_at`; BookingCancelled: `cancelled_at` — all snake_case. |
| c20 | Output's exception classes are `final class` extending the project's `DomainException` base — not `\Exception` or `\RuntimeException` | PASS | `final class AlreadyConfirmed extends DomainException`, `final class AlreadyCancelled extends DomainException`, `final class BookingNotRequested extends DomainException`. |
| c21 | Output's Behat feature uses business language only — no class names like `BookingAggregate`, no `recordThat()`, no PHP code in Given/When/Then | PASS | Feature uses "a booking is requested/confirmed/cancelled"; no `BookingAggregate`, no `recordThat()`, no PHP syntax. Domain event names (BookingConfirmed) are ubiquitous-language terms. |
| c22 | Output's quality gates evidence shows PHPStan at level 9 (not 5, 6, 7, 8) — explicitly stated | PASS | "$ vendor/bin/phpstan analyse --level=9 src/ tests/" explicitly states level 9. |
| c23 | Output mentions the command/query handler scaffolding needed to dispatch booking commands through symfony/messenger, even if not implemented in this response | FAIL | No mention of symfony/messenger or command/query handler scaffolding anywhere in the output or artifacts. Classification mentions "then handler" but provides no detail about messenger integration. |

### Notes

The output is nearly flawless — all structural sections are present in order, the aggregate follows EventSauce conventions correctly, and code quality requirements (strict_types, no mixed, final readonly, UUID v7, snake_case payload keys) are all met. The only gap is c23: symfony/messenger handler scaffolding is completely absent from the response.
