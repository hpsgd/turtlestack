---
description: PHP language conventions and engineering standards
paths:
  - "**/*.php"
---

# PHP Conventions

## Language settings

- **PHP 8.4 minimum** for new code; PHP 8.5 acceptable for greenfield
- `declare(strict_types=1)` on every file — enforced by [PHP-CS-Fixer](https://cs.symfony.com)'s `declare_strict_types` rule
- Code style: [PER Coding Style 3.0](https://www.php-fig.org/per/coding-style/) via PHP-CS-Fixer's `@PER-CS:risky` ruleset (PSR-12 is frozen legacy)
- `# noqa` equivalent: `@phpstan-ignore-line` with a rule code AND a justification comment. Bare ignores are findings

## Naming

- `PascalCase` for classes, interfaces, traits, enums
- `camelCase` for methods, properties, parameters, local variables
- `UPPER_SNAKE_CASE` for constants and enum cases
- `snake_case` for array keys (matches JSON conventions for serialised payloads)
- Namespaces map PSR-4 directly to directory structure under `src/`
- One class per file. File name = class name + `.php`

## Type safety

- [PHPStan](https://phpstan.org) level 9 minimum, with `phpstan/phpstan-strict-rules`
- Every parameter, property, and return type annotated — no inferred types
- No `mixed` without justification. Prefer specific types, intersection types (`Countable&Traversable`), union types (`int|string`), or interfaces
- PHPDoc generics (`@param array<int, Page>`, `@return list<Crawl>`) where the syntax can't express them — PHPStan understands them natively
- Bare `array` is a finding — always `array<K, V>` or `list<T>` in PHPDoc
- `final` by default on application services, infrastructure, and value objects

## Immutability

- `final readonly class` for value objects and domain events
- Invariants enforced in the constructor — invalid instances cannot exist
- Constructor promotion for all properties — no separate `$this->x = $x` assignments
- Use `clone $obj with [prop: value]` (PHP 8.5+) or `with*()` methods for immutable updates
- Mutable classes only for stateful application services and infrastructure adapters — and document why

## Testing hierarchy

[Pest](https://pestphp.com) v4 (preferred for new projects) or [PHPUnit](https://phpunit.de) 12, [Behat](https://behat.org) for BDD, [Infection](https://infection.github.io) for mutation testing. The hierarchy is deliberate:

1. **Behat** — Gherkin `.feature` files in `features/`, step definitions in `features/bootstrap/`. Primary acceptance testing. Features use business language; hide infrastructure in step defs
2. **Property-based** ([Eris](https://github.com/giorgiosironi/eris)) — for pure functions, data transformations, domain invariant verification
3. **Unit tests** (Pest/PHPUnit) — for isolated logic, edge cases, error paths. Co-located in `tests/Unit/`
4. **Integration tests** — DB-backed in `tests/Integration/`. Through real bus, real repository, real DB
5. **Snapshot tests** ([spatie/phpunit-snapshot-assertions](https://github.com/spatie/phpunit-snapshot-assertions)) — for API response shapes, serialised event payloads

Targets: 95%+ line coverage, 80%+ Infection MSI (mutation kill rate).

## Error handling

- No empty `catch` blocks — every exception either handled or re-raised with context
- Catch specific exception classes — bare `catch (\Throwable)` and `catch (\Exception)` reserved for top-level CLI/HTTP entry points
- Re-raise with context: `throw new ConfigError("Failed to load {$path}", previous: $e);`
- Domain exceptions extend a project-specific base (e.g., `App\Domain\DomainException`) — never `\RuntimeException` directly
- Use `never` return type on methods that always throw

## Configuration

- Env vars loaded by [vlucas/phpdotenv](https://github.com/vlucas/phpdotenv) at the entry point only — never `getenv()` deep in domain code
- Typed `Config` readonly class built once at startup, injected via the DI container
- [symfony/yaml](https://symfony.com/doc/current/components/yaml.html) for human-readable config files
- Fail fast at startup if config is invalid — crash with a clear error before serving any request

## Composer

- `composer.json` pins `"php": ">=8.4"` in `require` and `config.platform.php` to the exact deploy target
- `composer.lock` committed for applications; not for libraries
- Production install: `composer install --no-dev --optimize-autoloader --classmap-authoritative`
- PSR-4 only (no PSR-0). `App\\` → `src/`, `App\\Tests\\` → `tests/` in `autoload-dev`
- Define `composer test`, `composer analyse`, `composer lint`, `composer fix`, `composer behat`, `composer audit` shortcuts in `scripts`

## Security

- `composer audit --no-dev` in CI on every build
- [`roave/security-advisories`](https://github.com/Roave/SecurityAdvisories) in `require-dev` — Composer refuses to install packages with known CVEs
- SonarCloud for SAST (per the org tooling register)
- [Psalm](https://psalm.dev) taint analysis as an add-on when the application handles untrusted input (Psalm's data-flow analysis is unique to it; PHPStan can't do it)
