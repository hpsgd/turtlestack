# Test: write-feature-spec for invoice generation

Scenario: Developer invokes the write-feature-spec skill to produce a Behat feature spec for invoice generation. When a subscription's billing period ends, the system generates an invoice. Failed payment retries up to three times before moving the subscription to a grace period; a successful payment closes the invoice.

## Prompt

Write a Behat feature spec for invoice generation. When a subscription's billing period ends, the system generates an invoice. The invoice attempts payment up to three times (initial + two retries, 24 hours apart). On success the invoice is marked paid. After three failures the subscription enters a 7-day grace period; if payment succeeds within the grace period the subscription is restored, otherwise it is suspended.

Deliver ALL of:

1. **Reconnaissance** — show actual commands run: `find . -name "*.feature" -not -path "*/vendor/*" 2>/dev/null` and `find features/bootstrap -name "*.php" 2>/dev/null`. Report results.
2. **Feature file** at `features/invoice_generation.feature` with:
   - Background covering "a subscription with an active billing period"
   - Happy-path scenario: end-of-period → invoice generated → payment succeeds → invoice marked paid
   - Scenario covering the retry sequence (first attempt fails, second succeeds — paid)
   - Scenario covering three-failure grace period entry
   - Scenario covering grace-period recovery (payment within 7 days restores)
   - Scenario covering grace-period suspension (no payment in 7 days → suspended)
   - Use `Scenario Outline` + `Examples` where parameterisation makes sense (e.g. different attempt counts), NOT 5 nearly-identical scenarios copy-pasted
   - Business language only — no `HttpRequest`, no `Repository`, no `Doctrine`, no HTTP status codes in steps
3. **Step definition class** at `features/bootstrap/InvoiceContext.php` — `final class InvoiceContext implements Context`, constructor injection of services (e.g. `MessageBusInterface`, an in-memory invoice repository), `declare(strict_types=1);` at the top
4. **Step methods** use `PHPUnit\Framework\Assert` for assertions
5. **behat.yml** config snippet showing the context wired with its dependencies
6. **Evidence the feature is RED** — show `vendor/bin/behat features/invoice_generation.feature` failing with clear "missing class" or "undefined step" errors before implementation. If Behat isn't installed, document the command and produce a template RED output.

## Criteria

- [ ] PASS: Skill performs reconnaissance first — checks for existing `.feature` files and bootstrap contexts
- [ ] PASS: Feature file uses business language exclusively — no `POST /invoices`, no `200 OK`, no Doctrine class names, no table names in Given/When/Then
- [ ] PASS: Each Given/When/Then is a single statement — no conjunctive steps combining two actions in one When
- [ ] PASS: Feature covers the four key paths: invoice generation, retry-then-pay, three-failure-grace, grace-period-resolution (recover OR suspend)
- [ ] PASS: At least one `Scenario Outline` with `Examples` is used for parameterised cases — not copy-paste
- [ ] PASS: Step definition class is `final class ... implements Context` with constructor injection — no service location
- [ ] PASS: `declare(strict_types=1);` at the top of the step definition file
- [ ] PASS: `behat.yml` snippet shows the context's dependencies being wired explicitly
- [ ] PASS: Evidence shows the feature is RED before implementation — Behat reports failures with specific causes

## Output expectations

- [ ] PASS: Output's feature file is at `features/invoice_generation.feature` (or close — `tests/Behat/Features/` is acceptable if conventional in the project)
- [ ] PASS: Output's scenarios collectively cover invoice generation, retry success, three-failure grace entry, grace recovery, and grace suspension — five behaviours, named scenarios that describe each
- [ ] PASS: Output's Given/When/Then steps do NOT contain HTTP verbs, status codes, Doctrine class names, SQL, or other technical artefacts
- [ ] PASS: Output's step definitions use `PHPUnit\Framework\Assert` (or another assertion library) — not echo, not raw `if (... !==) throw`
- [ ] PASS: Output's step methods inject dependencies via the constructor — no `$container->get(...)`, no static helpers
- [ ] PASS: Output's `Scenario Outline` includes an `Examples:` table — not a placeholder TODO
- [ ] PASS: Output's `behat.yml` wires the `InvoiceContext` with at least one named service argument — not bare `- App\Tests\Behat\InvoiceContext` with no args
- [ ] PASS: Output's RED evidence shows specific failure causes (missing class, undefined step) — not just "0 passing"
- [ ] PARTIAL: Output documents how time-based scenarios (24h retry, 7-day grace) are tested — clock abstraction, time-travel helper, or note about a separate integration-test layer
