# Review Php

Scenario: A developer submits PHP code for review with several violations: missing `declare(strict_types=1)`, a mutable class used as a domain value object, `mixed` in a method signature, an empty catch block, and a domain exception extending `\RuntimeException` directly.

## Prompt

> First, write this file to disk at `src/Domain/User/UserAccount.php`:
> 
> ```php
> <?php
> 
> namespace App\Domain\User;
> 
> class UserAccount
> {
>     public string $email;
>     public string $status;
>     private mixed $metadata;
> 
>     public function __construct(string $email, string $status, mixed $metadata)
>     {
>         $this->email = $email;
>         $this->status = $status;
>         $this->metadata = $metadata;
>     }
> 
>     public function suspend()
>     {
>         try {
>             $this->status = 'suspended';
>         } catch (\Exception $e) {
>         }
>     }
> }
> ```
> 
> And this file at `src/Domain/User/EmailAlreadyTaken.php`:
> 
> ```php
> <?php
> 
> namespace App\Domain\User;
> 
> class EmailAlreadyTaken extends \RuntimeException
> {
>     public function __construct(string $email)
>     {
>         parent::__construct("Email {$email} is already taken");
>     }
> }
> ```
> 
> Then run:
> 
> /coding-standards:review-php src/Domain/User/UserAccount.php src/Domain/User/EmailAlreadyTaken.php

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## PHP Review

### Summary
- Files reviewed: 2
- Type safety: 3 findings
- Immutability: 3 findings
- Linting: 0 findings
- Naming/structure: 0 findings
- Error handling: 3 findings
- Testing: 1 finding
- Domain/architecture: 1 finding

### Findings

#### CRITICAL

**1. Missing `declare(strict_types=1)`**

**Files:** 
- `src/Domain/User/UserAccount.php:1`
- `src/Domain/User/EmailAlreadyTaken.php:1`

**Evidence:** Both files open with `<?php` without the strict_types declaration.

**Standard:** Every PHP file must declare strict types (Pass 1, Type Safety)

**Fix:** Add as the second line after `<?php`:
```php
<?php

declare(strict_types=1);

namespace App\Domain\User;
```

---

**2. Domain Model Not `final readonly`**

**File:** `src/Domain/User/UserAccount.php:5`

**Evidence:**
```php
class UserAccount
{
    public string $email;
    public string $status;
```

**Standard:** Domain models in `src/Domain/` must be `final readonly class` to enforce immutability (Pass 2, Immutability)

**Fix:**
```php
final readonly class UserAccount
{
    public string $email;
    public string $status;
```

---

**3. Public Mutable Properties on Domain Model**

**File:** `src/Domain/User/UserAccount.php:7–8`

**Evidence:**
```php
public string $email;
public string $status;
```

**Standard:** Domain models must not expose public properties. State must be encapsulated and only modified through domain methods (Pass 2, Immutability)

**Fix:** Make properties private; expose through getter methods or a factory:
```php
final readonly class UserAccount
{
    public function __construct(
        private string $email,
        private string $status,
        private mixed $metadata,
    ) {}

    public function email(): string { return $this->email; }
    public function status(): string { return $this->status; }
```

---

**4. Empty Catch Block — Swallowed Exception**

**File:** `src/Domain/User/UserAccount.php:19–21`

**Evidence:**
```php
public function suspend()
{
    try {
        $this->status = 'suspended';
    } catch (\Exception $e) {
    }
}
```

**Standard:** Empty catch blocks hide errors and violate observability. At minimum, log with context. Catching bare `\Exception` is only acceptable at top-level entry points (Pass 5, Error Handling)

**Fix:** Either remove the try-catch if the assignment cannot fail, or log the error:
```php
public function suspend(): void
{
    $this->status = 'suspended';
}
```
(If an exception is genuinely expected, document it with `@throws` and handle it with a specific exception type and log statement.)

---

**5. Exception Extends `\RuntimeException` Directly**

**File:** `src/Domain/User/EmailAlreadyTaken.php:5`

**Evidence:**
```php
class EmailAlreadyTaken extends \RuntimeException
```

**Standard:** Domain exceptions should extend a project-specific base class (e.g., `App\Domain\DomainException`), not framework exceptions (Pass 5, Error Handling)

**Fix:** Create a base exception and extend it:
```php
class EmailAlreadyTaken extends \DomainException
{
    // or if using a custom base:
    // class EmailAlreadyTaken extends \App\Domain\DomainException
```

---

#### IMPORTANT

**6. Missing Return Type on `suspend()`**

**File:** `src/Domain/User/UserAccount.php:18`

**Evidence:**
```php
public function suspend()
{
```

**Standard:** Every method must have an explicit return type (Pass 1, Type Safety)

**Fix:**
```php
public function suspend(): void
{
```

---

**7. Explicit `mixed` Type Without Justification**

**File:** `src/Domain/User/UserAccount.php:9`

**Evidence:**
```php
private mixed $metadata;
```

**Standard:** `mixed` is acceptable only for third-party library wrapping (with `@phpstan-ignore-line`) or genuinely polymorphic callbacks. Otherwise, specify the concrete type, union, or interface (Pass 1, Type Safety)

**Fix:** Replace with a specific type:
```php
private array $metadata;  // or array<string, mixed> if shape is known
// or
private object $metadata;
```

---

**8. Direct State Mutation (Immutability Violation)**

**File:** `src/Domain/User/UserAccount.php:20`

**Evidence:**
```php
$this->status = 'suspended';
```

**Standard:** On a domain model (especially readonly), state changes should flow through event-sourcing: `recordThat(UserSuspended::for($this))` → `applyUserSuspended()`. Direct assignment defeats auditability (Pass 2, Immutability; Pass 7, Architecture)

**Fix:** Refactor to event-sourcing if this aggregate is event-sourced:
```php
public function suspend(): void
{
    $this->recordThat(new UserSuspended($this->email));
}

private function applyUserSuspended(UserSuspended $event): void
{
    $this->status = 'suspended';
}
```

---

#### SUGGESTION

**9. No Test File**

**File:** `src/Domain/User/UserAccount.php`

**Standard:** Every source file should have a corresponding test file covering constructor invariants and domain methods (Pass 6, Testing)

**Recommendation:** Create `tests/Unit/Domain/User/UserAccountTest.php` covering:
- Constructor validates immutability
- `suspend()` transitions status correctly
- Value objects for email and status (instead of raw strings)

---

### Clean Areas

- ✓ File names match class names
- ✓ Namespaces match PSR-4 paths
- ✓ No framework dependencies in domain code
- ✓ No service location or container access
- ✓ Code is concise and readable

---

### Verdict

**REQUEST_CHANGES**

The domain model has 5 critical issues (missing strict_types, not readonly, public mutable properties, swallowed exception, exception hierarchy) that prevent it from passing PHPStan level 9 and violating domain immutability guarantees. Address these before merging.

### Artifacts written

#### `work/src/Domain/User/EmailAlreadyTaken.php`

```
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

#### `work/src/Domain/User/UserAccount.php`

```
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

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 19.0/19.0 (100%) |
| Evaluated | 2026-05-23 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 38116 ms |
| Target cost | $0.0529 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill executes all seven mandatory passes — none skipped | PASS | Summary lists all 7 pass categories: Type safety, Immutability, Linting, Naming/structure, Error handling, Testing, Domain/architecture. |
| c2 | Missing `declare(strict_types=1);` is flagged as a critical Pass 1 finding for both files | PASS | Finding #1 is CRITICAL, lists both files at line 1, references 'Pass 1, Type Safety', and shows the fix. |
| c3 | `mixed` type on the property and constructor parameter is flagged as a Pass 1 finding with the standard "no `mixed` without justification" | PASS | Finding #7: 'Explicit `mixed` Type Without Justification' at UserAccount.php:9, references Pass 1, Type Safety, states mixed is only acceptable with justification. |
| c4 | Missing return type on `suspend()` is flagged as a Pass 1 finding | PASS | Finding #6: 'Missing Return Type on `suspend()`' at UserAccount.php:18, 'Every method must have an explicit return type (Pass 1, Type Safety)'. |
| c5 | `UserAccount` not being `final readonly class` is flagged as a Pass 2 immutability finding — public-set properties on a domain class is the specific issue | PASS | Finding #2: 'Domain Model Not `final readonly`' and Finding #3: 'Public Mutable Properties on Domain Model', both Pass 2 Immutability. |
| c6 | Direct mutation `$this->status = 'suspended'` outside a constructor is flagged — value objects don't mutate; if `UserAccount` is an entity, this should be domain-method-driven, not direct field assignment | PASS | Finding #8: 'Direct State Mutation (Immutability Violation)' at UserAccount.php:20, evidence `$this->status = 'suspended';`, recommends event-sourcing pattern. |
| c7 | Empty `catch (\Exception $e) {}` block is flagged as a critical Pass 5 error-handling finding | PASS | Finding #4: 'Empty Catch Block — Swallowed Exception', severity CRITICAL, 'Pass 5, Error Handling', at UserAccount.php:19–21. |
| c8 | `EmailAlreadyTaken extends \RuntimeException` is flagged as a Pass 5 finding — domain exceptions extend the project's `DomainException` base | PASS | Finding #5: 'Exception Extends `\RuntimeException` Directly' at EmailAlreadyTaken.php:5, 'Pass 5, Error Handling', fix shows App\Domain\DomainException. |
| c9 | Each finding includes the evidence format — file, evidence, standard, and concrete fix | PASS | All 8+ findings include File/Files field, Evidence code or description, Standard citation, and Fix code block. |
| c10 | Output uses the summary template with counts by category | PASS | Summary block lists 'Files reviewed: 2' then 7 categories with counts, e.g. 'Type safety: 3 findings', 'Linting: 0 findings'. |
| c11 | Pass 6 (testing) notes that no test file was provided and recommends Pest/PHPUnit coverage for `suspend()` and the constructor invariants | PARTIAL | Finding #9 notes no test file and recommends UserAccountTest.php covering constructor and suspend(), but does not name Pest or PHPUnit explicitly. |
| c12 | Output's `declare(strict_types=1);` finding cites the missing declaration on line 1 of both files and shows the fix (add `declare(strict_types=1);` on the line after `<?php`) | PASS | Finding #1 cites both files at line 1, fix shows `<?php` then blank line then `declare(strict_types=1);` then namespace. |
| c13 | Output's `mixed` finding suggests a concrete type — at least a union, an intersection, or a Protocol-style interface — not just "remove `mixed`" | PASS | Finding #7 fix: `private array $metadata; // or array<string, mixed>` and `private object $metadata;` as concrete alternatives. |
| c14 | Output's mutable-class finding cites `UserAccount` and shows the fix as `final readonly class UserAccount` with constructor-promoted readonly properties OR notes that if this is an entity (not a value object) the design should expose a `suspend()` domain method that records an event rather than mutating a field | PASS | Finding #2 shows `final readonly class UserAccount`; Finding #3 shows constructor-promoted private properties; Finding #8 shows the event-sourcing suspend() approach. |
| c15 | Output's empty-catch finding is severity HIGH/critical — explains that swallowing exceptions hides bugs — with the fix specifying either removing the try/catch (the body doesn't actually throw) or catching a specific exception type and logging | PASS | Finding #4 is CRITICAL, 'Empty catch blocks hide errors and violate observability', fix says 'remove the try-catch if the assignment cannot fail, or log the error'. |
| c16 | Output's domain-exception finding cites `extends \RuntimeException` and shows the fix as `extends \App\Domain\DomainException` (or `extends \App\Domain\User\UserDomainException` for a per-context base) — never `\Exception` or `\RuntimeException` directly | PASS | Finding #5 cites `extends \RuntimeException`, fix shows `// class EmailAlreadyTaken extends \App\Domain\DomainException`. |
| c17 | Output's findings each include severity, pass label (Pass 1, 2, 5), file path, line number where possible, evidence snippet, the standard violated, and a concrete fix code block — not just a list of issues | PASS | Each finding has CRITICAL/IMPORTANT/SUGGESTION severity, Pass N label, file+line, evidence code, Standard field, Fix code block. |
| c18 | Output runs all seven mandatory passes and reports per-pass finding counts in the summary, including passes with zero findings | PASS | Summary includes 'Linting: 0 findings' and 'Naming/structure: 0 findings' alongside non-zero categories. |
| c19 | Output's overall verdict reflects the severity — mutable domain model + empty catch + wrong exception base are correctness/safety issues, so REQUEST_CHANGES (not APPROVE) | PASS | Verdict section concludes 'REQUEST_CHANGES' with explicit rationale citing the 5 critical issues. |
| c20 | Output addresses Pass 6 (testing) by noting that no test file was provided and recommending tests for the suspend behaviour and constructor invariants | PARTIAL | Finding #9 notes no test file and recommends coverage of 'Constructor validates immutability' and '`suspend()` transitions status correctly'. |

### Notes

The skill produced a near-perfect review: all 7 passes executed, every targeted violation caught with severity, pass label, file/line, evidence, standard, and fix code. The only gap keeping two criteria at PARTIAL is the omission of Pest/PHPUnit by name in the testing recommendation, which is a minor detail given the ceiling was already capped at PARTIAL.
