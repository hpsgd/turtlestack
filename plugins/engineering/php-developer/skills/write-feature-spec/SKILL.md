---
name: write-feature-spec
description: Write a Behat feature specification in Gherkin with step definitions.
argument-hint: "[feature or behaviour to specify]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
paths:
  - "**/*.php"
  - "**/*.feature"
---

Write a Behat feature spec for $ARGUMENTS.

## Process (sequential — do not skip steps)

### Step 1: Reconnaissance

Before writing any Gherkin:

1. **Read existing features** — match conventions:
   ```bash
   find . -name "*.feature" -not -path "*/vendor/*" | head -20
   find . -path "*/features/bootstrap/*" -name "*.php" | head -20
   ```

2. **Check existing step definitions** — reuse where possible:
   ```bash
   grep -rn "@Given\|@When\|@Then" --include="*.php" features/ | head -30
   ```

3. **Identify the domain language** — what terms do product/business use? Use those, not technical terms

4. **Confirm Behat is set up** — `composer.json` should have `behat/behat` in `require-dev`, and `behat.yml` (or `behat.yml.dist`) should configure the suite path

### Step 2: Feature File Structure

Every feature file follows this structure:

```gherkin
# features/<feature-name>.feature

Feature: <Feature name in business language>
  As a <role>
  I want <capability>
  So that <business value>

  Background:
    Given <common precondition shared by all scenarios>

  Scenario: <Happy path — most common success case>
    Given <specific precondition in business language>
    When <user action in business language>
    Then <expected outcome in business language>

  Scenario: <Edge case — boundary or unusual input>
    Given <precondition>
    When <action with edge-case input>
    Then <expected outcome>

  Scenario: <Error case — invalid input or failed precondition>
    Given <precondition>
    When <action that should fail>
    Then a <SpecificError> is reported with <relevant context>

  Scenario Outline: <Parameterised scenarios>
    Given a crawl with <pages> pages
    When the operator completes the crawl
    Then <events> events are emitted

    Examples:
      | pages | events |
      | 1     | 2      |
      | 3     | 4      |
      | 10    | 11     |
```

**Feature rules:**
- One feature file per behaviour or capability — not per class
- Business language only — no `HttpRequest`, `Repository`, `getId()`. Use `crawl`, `operator`, `page`
- One scenario per behaviour — Happy path, edge cases, errors as separate scenarios
- Given/When/Then exactly once each (use `And` for additional conditions)
- `Background:` for preconditions shared by every scenario in the file
- `Scenario Outline:` only when the variation is genuinely tabular

### Step 3: Step Definitions

Step definitions go in `features/bootstrap/` (typical) as `final class` implementing `Context`:

```php
<?php

declare(strict_types=1);

namespace App\Tests\Behat;

use App\Application\Crawl\CompleteCrawl;
use App\Domain\Crawl\CrawlAggregate;
use App\Domain\Crawl\CrawlId;
use Behat\Behat\Context\Context;
use PHPUnit\Framework\Assert;
use Symfony\Component\Messenger\MessageBusInterface;

final class CrawlContext implements Context
{
    private ?CrawlId $crawlId = null;
    /** @var list<object> */
    private array $dispatchedMessages = [];

    public function __construct(
        private readonly MessageBusInterface $commandBus,
        private readonly InMemoryMessageRepository $messageRepository,
    ) {}

    /**
     * @Given a started crawl with :pages pages
     */
    public function aStartedCrawlWith(int $pages): void
    {
        $this->crawlId = CrawlId::generate();
        // Infrastructure setup hidden here — seed the event stream
    }

    /**
     * @When the operator completes the crawl
     */
    public function theOperatorCompletesTheCrawl(): void
    {
        Assert::assertNotNull($this->crawlId, 'crawl not started');
        $this->commandBus->dispatch(new CompleteCrawl($this->crawlId));
    }

    /**
     * @Then a :event event is recorded
     */
    public function aEventIsRecorded(string $event): void
    {
        $events = $this->messageRepository->retrieveAll($this->crawlId);
        $names = array_map(static fn (object $e): string => (new \ReflectionClass($e))->getShortName(), $events);
        Assert::assertContains($event, $names);
    }
}
```

**Step definition rules:**
- One context class per bounded context or feature area — avoid a single god `FeatureContext`
- Constructor injection of dependencies via `behat.yml` service config — never service location
- Step methods are `void` and assert directly with `PHPUnit\Framework\Assert`
- Hide infrastructure — fixtures, seeding, transport wiring — inside steps. The feature stays at business language
- Reuse steps by extracting helpers, not by copy-paste

### Step 4: Wire the Context

`behat.yml` (or `behat.yml.dist`):

```yaml
default:
    suites:
        default:
            paths:
                - "%paths.base%/features"
            contexts:
                - App\Tests\Behat\CrawlContext:
                    commandBus: '@command.bus'
                    messageRepository: '@App\Infrastructure\EventStore\InMemoryMessageRepository'
    extensions:
        FriendsOfBehat\SymfonyExtension:
            kernel:
                class: App\Tests\Behat\TestKernel
```

For non-Symfony projects, configure via the Behat container directly or use `FriendsOfBehat\ServiceContainerExtension`.

### Step 5: Verify the Feature Fails (RED)

Run the scenario before implementing the behaviour. It must fail because the behaviour does not exist yet. This is the spec contract — if it passes on first run, either the behaviour is already implemented (verify it matches) or the step definitions are not asserting anything.

```bash
vendor/bin/behat features/<name>.feature
```

Expected output: scenarios fail with concrete errors pointing at missing classes, methods, or assertions.

### Step 6: Output

Deliver:
1. The feature file(s) at `features/<name>.feature`
2. The step definition class(es) at `features/bootstrap/` (or configured location)
3. `behat.yml` updates if a new context was wired
4. Evidence that the feature is RED — Behat output showing failures with explanations
5. A short summary of which scenarios cover happy path, edge cases, and errors

## Anti-Patterns (NEVER do these)

- **Technical language in features** — `HttpRequest`, `Repository`, `Doctrine` — these belong in step defs, not Gherkin
- **One scenario covering multiple behaviours** — split each behaviour into its own scenario
- **Asserting on implementation details** — assert on observable outcomes (events emitted, messages dispatched, response status), not on internal field values
- **God context classes** — one `FeatureContext` with 50 steps. Split by bounded context
- **Skipping the RED step** — running the scenario before implementation is non-negotiable. Without it, the spec doesn't prove anything
- **Mocking the unit under test** — Behat is acceptance-level. If you find yourself mocking the aggregate or handler, you're in the wrong test layer

## Related Skills

- `/php-developer:write-aggregate` — once a scenario fails on missing aggregate behaviour, this skill writes the event-sourced aggregate
- `/php-developer:write-handler` — once a scenario fails on missing handler, this skill writes the command/query handler
