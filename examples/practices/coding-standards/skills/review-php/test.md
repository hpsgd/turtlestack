# Test: review-php type safety, immutability, and error handling

Scenario: A developer submits PHP code for review with several violations: missing `declare(strict_types=1)`, a mutable class used as a domain value object, `mixed` in a method signature, an empty catch block, and a domain exception extending `\RuntimeException` directly.

## Prompt

First, write this file to disk at `src/Domain/User/UserAccount.php`:

```php
<?php

namespace App\Domain\User;

class UserAccount
{
    public string $email;
    public string $status;
    private mixed $metadata;

    public function __construct(string $email, string $status, mixed $metadata)
    {
        $this->email = $email;
        $this->status = $status;
        $this->metadata = $metadata;
    }

    public function suspend()
    {
        try {
            $this->status = 'suspended';
        } catch (\Exception $e) {
        }
    }
}
```

And this file at `src/Domain/User/EmailAlreadyTaken.php`:

```php
<?php

namespace App\Domain\User;

class EmailAlreadyTaken extends \RuntimeException
{
    public function __construct(string $email)
    {
        parent::__construct("Email {$email} is already taken");
    }
}
```

Then run:

/coding-standards:review-php src/Domain/User/UserAccount.php src/Domain/User/EmailAlreadyTaken.php

## Criteria

- [ ] PASS: Skill executes all seven mandatory passes — none skipped
- [ ] PASS: Missing `declare(strict_types=1);` is flagged as a critical Pass 1 finding for both files
- [ ] PASS: `mixed` type on the property and constructor parameter is flagged as a Pass 1 finding with the standard "no `mixed` without justification"
- [ ] PASS: Missing return type on `suspend()` is flagged as a Pass 1 finding
- [ ] PASS: `UserAccount` not being `final readonly class` is flagged as a Pass 2 immutability finding — public-set properties on a domain class is the specific issue
- [ ] PASS: Direct mutation `$this->status = 'suspended'` outside a constructor is flagged — value objects don't mutate; if `UserAccount` is an entity, this should be domain-method-driven, not direct field assignment
- [ ] PASS: Empty `catch (\Exception $e) {}` block is flagged as a critical Pass 5 error-handling finding
- [ ] PASS: `EmailAlreadyTaken extends \RuntimeException` is flagged as a Pass 5 finding — domain exceptions extend the project's `DomainException` base
- [ ] PASS: Each finding includes the evidence format — file, evidence, standard, and concrete fix
- [ ] PASS: Output uses the summary template with counts by category
- [ ] PARTIAL: Pass 6 (testing) notes that no test file was provided and recommends Pest/PHPUnit coverage for `suspend()` and the constructor invariants

## Output expectations

- [ ] PASS: Output's `declare(strict_types=1);` finding cites the missing declaration on line 1 of both files and shows the fix (add `declare(strict_types=1);` on the line after `<?php`)
- [ ] PASS: Output's `mixed` finding suggests a concrete type — at least a union, an intersection, or a Protocol-style interface — not just "remove `mixed`"
- [ ] PASS: Output's mutable-class finding cites `UserAccount` and shows the fix as `final readonly class UserAccount` with constructor-promoted readonly properties OR notes that if this is an entity (not a value object) the design should expose a `suspend()` domain method that records an event rather than mutating a field
- [ ] PASS: Output's empty-catch finding is severity HIGH/critical — explains that swallowing exceptions hides bugs — with the fix specifying either removing the try/catch (the body doesn't actually throw) or catching a specific exception type and logging
- [ ] PASS: Output's domain-exception finding cites `extends \RuntimeException` and shows the fix as `extends \App\Domain\DomainException` (or `extends \App\Domain\User\UserDomainException` for a per-context base) — never `\Exception` or `\RuntimeException` directly
- [ ] PASS: Output's findings each include severity, pass label (Pass 1, 2, 5), file path, line number where possible, evidence snippet, the standard violated, and a concrete fix code block — not just a list of issues
- [ ] PASS: Output runs all seven mandatory passes and reports per-pass finding counts in the summary, including passes with zero findings
- [ ] PASS: Output's overall verdict reflects the severity — mutable domain model + empty catch + wrong exception base are correctness/safety issues, so REQUEST_CHANGES (not APPROVE)
- [ ] PARTIAL: Output addresses Pass 6 (testing) by noting that no test file was provided and recommending tests for the suspend behaviour and constructor invariants
