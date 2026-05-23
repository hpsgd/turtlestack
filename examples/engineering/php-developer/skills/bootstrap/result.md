# Bootstrap

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a `docs/architecture/CLAUDE.md` that already contains architecture conventions and a user-authored "Custom team notes" section with a sentinel line. The php-developer bootstrap skill should detect the existing file, append the "PHP Conventions" section (with a merge marker), and leave the user-authored content untouched. The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

> The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A `docs/architecture/CLAUDE.md` already exists — it contains architecture conventions from a prior architect bootstrap and a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.
> 
> Read the php-developer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/engineering/php-developer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Do not pause for confirmation — proceed with all defaults.
> 
> After the bootstrap completes, output the manifest summary the skill defines (files updated, files merged, next steps).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## PHP Developer Bootstrap Complete

### Files merged
- `docs/architecture/CLAUDE.md` — appended PHP Conventions section

### Next steps
- Confirm `composer.json` pins PHP 8.4+ and `config.platform.php`
- Add `phpstan/phpstan`, `phpstan/phpstan-strict-rules`, `friendsofphp/php-cs-fixer`, `pestphp/pest` (or PHPUnit), `behat/behat`, `infection/infection`, `roave/security-advisories` to `require-dev`
- Configure `phpstan.neon` at level 9
- Configure `.php-cs-fixer.dist.php` with `@PER-CS:risky`
- Use `/php-developer:write-feature-spec` for Behat specs
- Use `/php-developer:write-aggregate` for event-sourced aggregates
- Use `/php-developer:write-handler` for command/query handlers

### Artifacts written

#### `work/docs/architecture/CLAUDE.md`

```
# Architecture Domain

This directory contains architecture documentation for the project: decision records, system design artefacts, and API design guidelines.

## What This Domain Covers

- **Architecture Decision Records (ADRs)** — capturing significant technical decisions
- **System design** — C4 model diagrams, arc42 documentation, component relationships
- **API design** — REST/GraphQL/gRPC contract guidelines

## ADR Conventions

We use **MADR** (Markdown Any Decision Records) v3.0 format. Store ADRs in `docs/architecture/adr/`.

## Custom team notes

USER-EDIT-SENTINEL-DO-NOT-STRIP

This section was written by the team and must survive any bootstrap re-run.
It exists to test the safe-merge contract: the bootstrap skill must not
overwrite or remove user-authored content.

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

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 10.5/10.5 (100%) |
| Evaluated | 2026-05-23 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 38547 ms |
| Target cost | $0.1042 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | After bootstrap, `docs/architecture/CLAUDE.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim | PASS | Artifact contains 'USER-EDIT-SENTINEL-DO-NOT-STRIP' within the 'Custom team notes' section, followed by the full user-authored paragraph. |
| c2 | After bootstrap, `docs/architecture/CLAUDE.md` contains the merge marker `<!-- Added by php-developer bootstrap v3.0.1 -->` — the PHP Conventions section was appended with the correct marker | PASS | Artifact contains '<!-- Added by php-developer bootstrap v3.0.1 -->' immediately before the '## PHP Conventions' heading. |
| c3 | After bootstrap, `docs/architecture/CLAUDE.md` contains a `## PHP Conventions` heading — the conventions block was appended | PASS | Artifact contains '## PHP Conventions' heading with all subsections beneath it. |
| c4 | After bootstrap, `docs/architecture/CLAUDE.md` contains the `### Static analysis` subsection naming PHPStan | PASS | '### Static analysis' subsection present with '**PHPStan at level 9**' and 'phpstan/phpstan-strict-rules enabled'. |
| c5 | After bootstrap, `docs/architecture/CLAUDE.md` contains the `### Code style` subsection naming PHP-CS-Fixer and PER-CS | PASS | '### Code style' subsection present with '**PHP-CS-Fixer 3.x** with `@PER-CS:risky` ruleset' and 'PER Coding Style 3.0 supersedes PSR-12'. |
| c6 | After bootstrap, `docs/architecture/CLAUDE.md` contains the `### Testing` subsection naming Pest, Behat, and Infection | PASS | '### Testing' subsection present with '**Pest v4**', '**Behat** for BDD acceptance tests', and '**Infection** for mutation testing'. |
| c7 | After bootstrap, `docs/architecture/CLAUDE.md` contains the `### Event sourcing` subsection naming EventSauce | PASS | '### Event sourcing' subsection present with '**EventSauce** for framework-agnostic event sourcing'. |
| c8 | Chat output includes a manifest summary listing `docs/architecture/CLAUDE.md` as updated or merged | PASS | Chat output '### Files merged' section lists '`docs/architecture/CLAUDE.md` — appended PHP Conventions section'. |
| c9 | Output names `docs/architecture/CLAUDE.md` as the file that was updated — a bare 'bootstrap complete' without the per-file manifest is not enough | PASS | Chat output explicitly names '`docs/architecture/CLAUDE.md`' under '### Files merged' with a per-file description. |
| c10 | Output does not claim it overwrote or replaced `docs/architecture/CLAUDE.md` — the language reflects append or merge, not replacement | PASS | Chat output uses '### Files merged' heading and 'appended PHP Conventions section' — no overwrite/replacement language anywhere. |
| c11 | Output points the reader at next steps (configuring PHPStan, PHP-CS-Fixer, or using `/php-developer:write-feature-spec`) consistent with the skill's documented manifest | PARTIAL | '### Next steps' lists PHPStan level 9, PHP-CS-Fixer, and '/php-developer:write-feature-spec' among others — fully consistent with skill manifest. |

### Notes

The skill executed flawlessly: user-authored sentinel preserved, merge marker present, all required PHP Conventions subsections appended, and the chat manifest correctly uses merge/append language. All criteria met at ceiling.
