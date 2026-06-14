---
name: bootstrap
bootstrap-phase: stack
description: "Bootstrap PHP conventions into the architecture documentation. Writes the php-developer fragment of the architecture domain doc. Idempotent — merges missing sections into existing files without overwriting."
argument-hint: "[project name]"
user-invocable: false
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Bootstrap PHP Conventions

Bootstrap PHP development conventions for **$ARGUMENTS**.

This skill writes only its own fragment — `docs/architecture/_sections/php-developer.md`. The architecture domain `CLAUDE.md` is assembled by the coordinator from every fragment in `_sections/`, so this skill never collides with the architect or the other stack developers.

## Process

### Step 1: Create the sections directory

```bash
mkdir -p docs/architecture/_sections
```

### Step 2: Write the PHP fragment

`docs/architecture/CLAUDE.md` is **assembled by the coordinator** from the fragments in `_sections/` — no plugin writes it directly, so this skill and the architect never collide on it. Write the PHP contribution as `docs/architecture/_sections/php-developer.md`. It starts at H2 (the coordinator generates the `# Architecture Domain` H1).

Apply the safe merge pattern:

- If the fragment does not exist → create it from the template below
- If the fragment exists → read both, find sections in the template missing from the file, append only the missing sections with the marker `<!-- Added by php-developer bootstrap v3.0.1 -->`

```markdown
<!-- Added by php-developer bootstrap v3.0.1 -->
## PHP Conventions

### Language baseline

- **PHP 8.4 minimum** for new projects; PHP 8.5 acceptable for greenfield work
- `declare(strict_types=1)` on every file (enforced by PHP-CS-Fixer)
- `composer.json` pins `"php": ">=8.4"` and `config.platform.php` to the deploy target

### Static analysis

- **PHPStan at level 9** — every parameter, property, and return annotated
- `phpstan/phpstan-strict-rules` enabled
- No `mixed` without an inline justification comment
- Baselines added only with explicit approval — never silently

### Code style

- **PHP-CS-Fixer 3.x** with `@PER-CS:risky` ruleset
- PER Coding Style 3.0 supersedes PSR-12 — use it
- CI gate: zero violations from `php-cs-fixer fix --dry-run`

### Testing

- **Pest v4** for new projects; **PHPUnit 12** acceptable for existing ones
- **Behat** for BDD acceptance tests (Given/When/Then in `features/`)
- **Infection** for mutation testing — target MSI 80%+ overall, 85%+ on covered code
- **Eris** for property-based testing of pure functions and invariants
- **spatie/phpunit-snapshot-assertions** for API response and serialised payload shapes
- Coverage: 95%+ overall, 98%+ on changed files

### Domain modelling

- `final readonly class` for value objects and domain events
- Invariants enforced in the constructor — invalid instances cannot exist
- UUID v7 (via `ramsey/uuid`) for aggregate IDs — time-ordered, sorts chronologically
- `moneyphp/money` for currency amounts — never roll your own
- `webmozart/assert` for domain invariants

### Event sourcing

- **EventSauce** for framework-agnostic event sourcing
- patchlevel/event-sourcing as alternative when more batteries-included
- State changes via `recordThat()` + `apply*()` — never direct mutation
- One aggregate, one stream. Stream ID = aggregate ID (UUID v7)

### Messaging

- **symfony/messenger** for command, query, and event buses
- Three separate buses (`command.bus`, `query.bus`, `event.bus`)
- One handler per command/query; multiple handlers per event
- Handlers are `final readonly class` with `__invoke()` and constructor injection

### Persistence

- **Doctrine ORM + DBAL** for read models and non-event-sourced aggregates
- **DBAL only** for the event store (no ORM)
- Repository interface in domain layer; implementation in infrastructure

### Parse, don't validate

- **cuyz/valinor** at every input boundary — maps raw arrays/JSON to typed objects
- `symfony/validator` only for form-style application-layer validation
- Inside the domain, every value already has the right type

### HTTP

- PSR-7 / PSR-15 / PSR-17 baseline
- **Slim 4** for micro-API projects
- **symfony/http-client** default outbound HTTP (PSR-18); Guzzle 7 acceptable
- Abstract HTTP client behind a domain interface

### Logging

- **Monolog 3** — inject `Psr\Log\LoggerInterface`, not Monolog classes
- Structured context arrays, not formatted strings
- `FingersCrossedHandler` in production for failure-context buffering

### CLI

- **symfony/console** — framework-agnostic standard
- Entry point: `bin/app`
- `--dry-run`, `--verbose`, `--format=json` where applicable

### Configuration

- **vlucas/phpdotenv** at the entry point only
- Typed `Config` readonly class built once at startup
- **symfony/yaml** for human-readable config files

### Dependency injection

- **PHP-DI 7** — autowiring + PSR-11
- Compiled container in production (`ContainerBuilder::enableCompilation()`)

### Security

- `composer audit --no-dev` in CI on every build
- `roave/security-advisories` in `require-dev`
- SonarCloud for SAST
- Psalm taint analysis if the application handles untrusted input

### Project structure

```
src/
├── Domain/          # Aggregates, value objects, domain events, domain exceptions
├── Application/     # Command/query/event classes + handlers, application services
└── Infrastructure/  # Doctrine entities/repos, HTTP, Symfony Console, EventSauce wiring
tests/
├── Unit/            # Pest/PHPUnit unit tests
├── Integration/     # DB-backed integration tests
└── Snapshot/        # Snapshot tests for serialised payloads
features/            # Behat .feature files
features/bootstrap/  # Behat step definitions
```

### Composer scripts

| Script | Purpose |
|---|---|
| `composer test` | Runs `vendor/bin/pest` (or `phpunit`) |
| `composer analyse` | Runs `vendor/bin/phpstan analyse --level=9` |
| `composer lint` | Runs `vendor/bin/php-cs-fixer fix --dry-run --diff` |
| `composer fix` | Runs `vendor/bin/php-cs-fixer fix` |
| `composer behat` | Runs `vendor/bin/behat` |
| `composer infection` | Runs `vendor/bin/infection --min-msi=80` |
| `composer audit` | Composer's built-in vulnerability check |

### Available PHP skills

| Skill | Purpose |
|---|---|
| `/php-developer:write-feature-spec` | Write a Behat feature specification |
| `/php-developer:write-aggregate` | Write an event-sourced aggregate (EventSauce) |
| `/php-developer:write-handler` | Write a symfony/messenger command/query/event handler |
```

### Step 3: Return manifest

After creating/merging all files, output a summary:

```
## PHP Developer Bootstrap Complete

### Files created
- `docs/architecture/_sections/php-developer.md` — php-developer's fragment of the architecture domain doc (assembled into `docs/architecture/CLAUDE.md` by the coordinator)

### Files merged
- (list the fragment here if it already existed and missing sections were appended, or "none")

### Next steps
- Confirm `composer.json` pins PHP 8.4+ and `config.platform.php`
- Add `phpstan/phpstan`, `phpstan/phpstan-strict-rules`, `friendsofphp/php-cs-fixer`, `pestphp/pest` (or PHPUnit), `behat/behat`, `infection/infection`, `roave/security-advisories` to `require-dev`
- Configure `phpstan.neon` at level 9
- Configure `.php-cs-fixer.dist.php` with `@PER-CS:risky`
- Use `/php-developer:write-feature-spec` for Behat specs
- Use `/php-developer:write-aggregate` for event-sourced aggregates
- Use `/php-developer:write-handler` for command/query handlers
```

## Rules

- **Write only your own fragment.** `docs/architecture/CLAUDE.md` is assembled by the coordinator; this skill writes `docs/architecture/_sections/php-developer.md` and nothing else. The architect and the other stack developers write their own fragments — there is no shared file to clobber.
- **Safe-merge the fragment, idempotent by design.** If the fragment exists, preserve user-authored content and append only missing template sections with the marker — never overwrite. Running twice produces no duplicate sections.
