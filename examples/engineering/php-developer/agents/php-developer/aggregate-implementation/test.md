# Test: php-developer implements a new event-sourced aggregate

Scenario: User asks the PHP developer agent to add a new event-sourced `Booking` aggregate with `request`, `confirm`, and `cancel` operations. The project is greenfield PHP 8.4 using EventSauce, symfony/messenger, PHPStan level 9, and Pest v4 — but the user does not state any of that explicitly. The agent must perform pre-flight, classify the work as a new domain feature, and propose a structured plan.

## Prompt

We need a new `Booking` aggregate. A user can request a booking (which records it with status "pending"), confirm it (only valid from "pending"), or cancel it (valid from "pending" or "confirmed", but never from "cancelled"). Each transition emits a domain event. Can you implement this?

The agent's response must follow its documented output format. Specifically:

- **Pre-Flight section at top** — labelled `## Pre-Flight` listing files Read: `CLAUDE.md`, `.claude/rules/*` (any rules present), `composer.json`, existing aggregates if any. State: "Pre-flight complete — proceeding."
- **Decision Checkpoint section** — flag the bounded-context placement question explicitly: "Booking aggregate placement: (a) `src/Domain/Booking/` (new bounded context owns Booking), (b) `src/Domain/Reservation/` (folded into a generic reservations module). I recommend (a) — Booking is a distinct aggregate root. Proceeding with (a); user can correct in follow-up."
- **Classify the request**: state "This is a NEW DOMAIN FEATURE — Behat spec must be written FIRST, then aggregate, then handler."
- **Output format** sections in this EXACT order: `## Pre-Flight`, `## Decision Checkpoint`, `## Behat Evidence`, `## Quality Gates`, `## Changes`. DO NOT pause for confirmation — proceed with stated assumptions.
- **Behat Evidence section** — `features/booking.feature` with scenarios:
  1. Happy path: request → confirm → BookingConfirmed
  2. Happy path: request → cancel → BookingCancelled
  3. Happy path: request → confirm → cancel → BookingCancelled
  4. Error: confirm without request → BookingNotRequested (or invariant violation)
  5. Error: cancel an already-cancelled booking → AlreadyCancelled
  6. Error: confirm an already-confirmed booking → AlreadyConfirmed
- **Aggregate code** using EventSauce — `final class BookingAggregate` with `AggregateRootBehaviour`, `recordThat()` + `apply*()` pattern. `BookingId` value object implementing `AggregateRootId`, UUID v7.
- **Events** — `final readonly class` implementing `SerializablePayload`, past-tense names (`BookingRequested`, `BookingConfirmed`, `BookingCancelled`), `snake_case` payload keys.
- **`declare(strict_types=1);` on every file shown**.
- **No `mixed` anywhere** — every parameter, property, return type explicit.
- **PHPStan-level-9 compliant code** — typed properties, no bare `array` without `@param list<...>` annotation.
- **Specific domain exception classes** — `AlreadyConfirmed`, `AlreadyCancelled`, `BookingNotRequested`, all extending a project base `DomainException`. NEVER `\Exception`, NEVER `\RuntimeException` direct.
- **Quality Gates section** with command + exit code per gate:
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
  Show the actual command and exit code. If tools aren't installed, produce a representative template.
- **Changes section** listing files added/modified with one-line summary per file.

## Criteria

- [ ] PASS: Agent reads CLAUDE.md and `.claude/rules/` before writing any code
- [ ] PASS: Agent classifies this as a new domain feature and specifies Behat spec must be written first
- [ ] PASS: Agent produces or references a Behat feature file covering happy paths, all three error scenarios, and the request/confirm/cancel sequence
- [ ] PASS: Agent uses `final readonly class` for value objects (`BookingId`) and events
- [ ] PASS: Agent uses `AggregateRootBehaviour` trait and `recordThat()` + `apply*()` pattern — never direct mutation
- [ ] PASS: Agent uses UUID v7 (`Uuid::uuid7()`), not v4, for the aggregate ID
- [ ] PASS: Agent specifies `declare(strict_types=1);` on every file
- [ ] PASS: Agent rejects `mixed` and shows typed properties throughout
- [ ] PASS: Agent uses domain-specific exception classes extending a project `DomainException` base, not `\Exception` or `\RuntimeException` directly
- [ ] PASS: Agent lists all quality gates: PHPStan level 9, PHP-CS-Fixer dry-run, Pest with coverage ≥95%, Behat
- [ ] PARTIAL: Agent raises a decision checkpoint about bounded-context placement before implementing
- [ ] PASS: Output format includes Pre-Flight, Decision Checkpoint, Behat Evidence, Quality Gates, Changes sections in order

## Output expectations

- [ ] PASS: Output's events are past-tense names — `BookingRequested`, `BookingConfirmed`, `BookingCancelled` — never imperative
- [ ] PASS: Output's `BookingAggregate` invariants throw BEFORE `recordThat()`, not after. Confirming a cancelled booking does not record any event
- [ ] PASS: Output's `apply*()` methods are `protected` and return `void`
- [ ] PASS: Output's aggregate is `final class` (not `abstract`, not non-final)
- [ ] PASS: Output's `BookingId::generate()` calls `Uuid::uuid7()` and the constructor validates with `Assert::uuid(...)`
- [ ] PASS: Output's event classes implement `SerializablePayload` with both `toPayload()` and `fromPayload()` defined
- [ ] PASS: Output's `toPayload()` returns an array with `snake_case` keys
- [ ] PASS: Output's exception classes are `final class` extending the project's `DomainException` base — not `\Exception` or `\RuntimeException`
- [ ] PASS: Output's Behat feature uses business language only — no class names like `BookingAggregate`, no `recordThat()`, no PHP code in Given/When/Then
- [ ] PASS: Output's quality gates evidence shows PHPStan at level 9 (not 5, 6, 7, 8) — explicitly stated
- [ ] PARTIAL: Output mentions the command/query handler scaffolding needed to dispatch booking commands through symfony/messenger, even if not implemented in this response
