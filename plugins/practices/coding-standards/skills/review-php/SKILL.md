---
name: review-php
description: "Review PHP code against team conventions — type safety, immutability, testing, linting, error handling, and code structure. Auto-invoked when reviewing .php files."
argument-hint: "[files, PR, or git range to review]"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
paths:
  - "**/*.php"
---

Review PHP code against team standards covering type safety, immutability and data modelling, testing, linting, configuration, error handling, and code structure. Every check has a concrete grep pattern. Every finding requires evidence.

## Mandatory Process

Execute all seven passes. Do not skip.

**File not on disk:** If Read returns "not found" for the target file(s), check whether code is provided inline in the prompt. If so, apply all seven passes to that code, treating it as the file under review. Do not skip passes because the file is absent from the workspace.

### Pass 1: Type Safety — PHPStan Level 9

The project runs PHPStan at level 9 with `phpstan-strict-rules`. Code must pass without exceptions.

1. **`mixed` usage** — grep for explicit `mixed` in type declarations and PHPDoc:
   ```bash
   grep -rn '\bmixed\b' --include='*.php' [changed files]
   ```
   Every hit is a finding unless it meets one of these conditions:
   - Wrapping a third-party library with no PHPStan stubs (must have `@phpstan-ignore-line` with a rule code and explanatory comment)
   - Genuinely unknown polymorphic callback parameters (rare)

   The fix: use a specific type, intersection type (`Countable&Traversable`), union type, or an interface.

2. **`@phpstan-ignore` audit** — grep for all PHPStan ignore comments:
   ```bash
   grep -rn '@phpstan-ignore' --include='*.php' [changed files]
   ```
   Each must specify the rule code: `@phpstan-ignore-line ruleId` not bare `@phpstan-ignore-line`. Each must have a justification comment on the same or preceding line.

3. **Missing return types** — every function/method must have a return type. Read each function definition in changed files:
   ```bash
   grep -rn 'function ' --include='*.php' [changed files]
   ```
   Methods without `: ReturnType` are findings. This includes constructors (always `: void` implicit — fine) and methods that throw unconditionally (should be `: never`).

4. **Missing parameter types** — every parameter must have a type. Untyped parameters in `function (` declarations are findings.

5. **Bare `array` in signatures** — grep for `array` without generic annotation:
   ```bash
   grep -rn ': array\b\|, array \|(array \b' --include='*.php' [changed files]
   ```
   Every signature with bare `array` should have a PHPDoc `@param array<K, V>` or `@param list<T>`. Bare `array` without a PHPDoc shape is a finding.

6. **`@var` and `@phpstan-var` audit** — grep for type hint annotations that bypass strict checks:
   ```bash
   grep -rn '@var \|@phpstan-var \|@phpstan-assert ' --include='*.php' [changed files]
   ```
   Each `@var` cast should have a justification — usually narrowing a known-broader type. Don't sprinkle them to silence PHPStan.

7. **`declare(strict_types=1)`** — every file must start with this declaration:
   ```bash
   for f in [changed files]; do head -3 "$f" | grep -q 'declare(strict_types=1)' || echo "MISSING: $f"; done
   ```
   Any file without it is a critical finding.

### Pass 2: Immutability — Readonly Classes

Domain models (value objects, events) use `final readonly class`. Not mutable classes. Not arrays. Not stdClass.

1. **Domain models without readonly** — find class declarations in domain directories:
   ```bash
   grep -rn '^class \|^final class \|^abstract class ' --include='*.php' src/Domain/ | grep -v readonly
   ```
   Every class in `src/Domain/<Context>/` or `src/Domain/<Context>/Event/` that is not an aggregate (no `AggregateRootBehaviour`) should be `final readonly class`. Mutable domain models are findings.

2. **`final` modifier** — application services and infrastructure should be `final` by default:
   ```bash
   grep -rn '^class ' --include='*.php' src/Application/ src/Infrastructure/ | grep -v 'abstract\|final\|trait\|interface'
   ```
   Non-final concrete classes are suggestions (not critical) — `final` prevents accidental inheritance. Exception: classes that are extended in the same package have a documented reason.

3. **Public setters on domain models** — grep for setter methods on readonly classes (shouldn't compile, but PHPDoc magic methods can sneak through):
   ```bash
   grep -rn 'public function set' --include='*.php' src/Domain/
   ```
   Every hit on a domain model is a critical finding. Aggregates expose domain methods (`complete()`, `cancel()`), not property setters.

4. **Direct mutation in aggregates** — grep for property assignments outside `apply*()` methods:
   ```bash
   grep -rn '\$this->[a-z][a-zA-Z]* = ' --include='*.php' src/Domain/ | grep -v 'apply[A-Z]'
   ```
   Assignments outside an `apply*()` method or constructor are likely findings — event-sourced state changes must go through `recordThat()` + `apply*()`.

### Pass 3: Linting — PHP-CS-Fixer Clean

The project uses PHP-CS-Fixer with `@PER-CS:risky`. Code must be clean.

1. **Mixed quote style** — verify single quotes for strings without interpolation (PER-CS default):
   PHP-CS-Fixer handles this. If running the review on uncommitted code, suggest running `composer fix` before review.

2. **`use` statement organisation** — verify imports are alphabetised and grouped. PHP-CS-Fixer handles this; manual review only when the formatter hasn't run.

3. **Trailing whitespace, missing final newlines, inconsistent indentation** — all handled by PHP-CS-Fixer. Findings here mean the developer hasn't run `composer fix`.

4. **String interpolation vs concatenation** — prefer interpolation:
   ```bash
   grep -rn "' \. \$\|\" \. \$" --include='*.php' [changed files]
   ```
   `"Hello " . $name` is a finding when `"Hello {$name}"` works. Concatenation is acceptable for multi-line strings or when the variables aren't simple.

### Pass 4: Naming and Structure

1. **One class per file** — find files with multiple class declarations:
   ```bash
   for f in [changed files]; do count=$(grep -c '^class \|^final class \|^abstract class \|^interface \|^trait \|^enum ' "$f"); [ "$count" -gt 1 ] && echo "MULTIPLE in $f"; done
   ```
   Findings.

2. **File name = class name** — verify each `.php` file's name matches its primary class:
   ```bash
   for f in [changed files]; do basename=$(basename "$f" .php); grep -q "^\(final \|abstract \)\?\(class\|interface\|trait\|enum\) $basename\b" "$f" || echo "MISMATCH: $f"; done
   ```
   Findings.

3. **Namespace matches directory** — verify the `namespace` declaration matches the PSR-4 path. Mismatches cause autoload failures.

4. **Module organization** — files with 500+ lines are flagged for review. Domain models with more than 20 public methods suggest the responsibility is too broad.

### Pass 5: Error Handling

1. **Bare catch blocks** — grep for `catch (\Exception` and `catch (\Throwable`:
   ```bash
   grep -rn 'catch (\\\\\?Exception\|catch (\\\\\?Throwable' --include='*.php' [changed files]
   ```
   These are acceptable only at top-level CLI/HTTP entry points (a `main()` equivalent, a global error handler, a Messenger middleware). Inside business logic they are findings.

2. **Empty catch blocks** — grep for catch followed by `}` on the next non-trivial line:
   ```bash
   grep -rn -A2 'catch (' --include='*.php' [changed files] | grep -B1 '^\s*}\s*$'
   ```
   Swallowed exceptions are critical findings. At minimum, log with context.

3. **Re-raise without context** — grep for `throw new` inside `catch` blocks without `previous:`:
   ```bash
   grep -rn -B5 'throw new ' --include='*.php' [changed files] | grep -B5 'throw new' | grep 'catch'
   ```
   Re-raises that drop the original exception (`throw new MyError($message)` without `previous: $e`) lose the traceback. Findings.

4. **Domain exception base class** — verify new exception classes extend a project-specific base (e.g., `App\Domain\DomainException`), not `\Exception` or `\RuntimeException` directly:
   ```bash
   grep -rn 'extends \\\\Exception\|extends \\\\RuntimeException\|extends \\\\LogicException' --include='*.php' src/Domain/
   ```
   Findings.

5. **`@throws` annotations** — public methods that throw should declare it in PHPDoc:
   ```bash
   grep -rn 'public function ' --include='*.php' src/Domain/ src/Application/
   ```
   Check that methods which throw have an `@throws ExceptionClass` annotation.

### Pass 6: Testing — Behat Hierarchy

Tests follow a BDD-first hierarchy: Behat for acceptance, Pest/PHPUnit for unit and integration.

1. **Test naming** — Pest tests use `it('describes behaviour')`; PHPUnit tests use `test_method_describes_behaviour`:
   ```bash
   grep -rn "it('test\|public function test\b" --include='*.php' [changed test files]
   ```
   Test names like `test_register` or `it('works')` are findings — describe the scenario.

2. **No control flow in tests** — tests must not contain `if`, `for`, `while`, or `try/catch`:
   ```bash
   grep -rn -A20 'it(\|public function test' --include='*.php' [changed test files] | grep -E '^\s+(if|for|while|try)\b'
   ```
   A test that branches is testing multiple things. Findings.

3. **Mock-heavy tests** — count mock usage in test files:
   ```bash
   grep -rn 'Mockery::mock\|->createMock\|->createStub' --include='*.php' [changed test files]
   ```
   Tests with more than 3 mocks per test are suggestions — consider an integration test through the real bus instead. Mock-heavy tests test the mocks, not the code.

4. **Behat coverage** — every user-facing feature should have a Behat scenario. If the change introduces a new command/query/endpoint, verify there is a corresponding `.feature` file:
   ```bash
   find features/ -name '*.feature'
   ```
   Missing acceptance coverage for user-facing behaviour is a finding.

5. **Missing test file** — for every changed source file, look for a corresponding test:
   ```bash
   for f in [changed files]; do
     base=$(basename "$f" .php)
     find tests/ -name "${base}Test.php" -o -name "${base}.spec.php" 2>/dev/null
   done
   ```
   If a source file has no companion test file, surface it as an explicit finding — "No test file found for `src/Domain/User/UserAccount.php`. Recommend `tests/Unit/Domain/User/UserAccountTest.php` covering the constructor invariants and the `suspend()` domain method." Do not let Pass 6 report "0 findings" when there are no tests — that is itself a finding.

6. **Coverage targets**:
   - Line coverage: 95%+ on changed files
   - Infection MSI: 80%+ if mutation testing is configured
   If reports are available, check them. Otherwise verify by reading that every code path has a test.

### Pass 7: Domain & Architecture

1. **Framework dependencies in domain** — grep for framework classes in `src/Domain/`:
   ```bash
   grep -rn 'use Symfony\|use Doctrine\\\\ORM\|use Laravel\|use Illuminate' --include='*.php' src/Domain/
   ```
   Domain code should not depend on Symfony, Doctrine ORM, Laravel, or any framework. The aggregate uses EventSauce's `AggregateRoot` interface (acceptable — it's a domain abstraction), but not framework controllers, ORM entities, or HTTP classes. Findings.

2. **Service location** — grep for container access:
   ```bash
   grep -rn '\$container->get\|ContainerInterface\|getContainer()' --include='*.php' [changed files]
   ```
   Service location defeats DI. Constructor injection only. Acceptable in bootstrap/wiring code, not in handlers or services.

3. **Inline loops in handlers** — grep for `foreach` inside handler `__invoke()` methods:
   ```bash
   grep -rn -A20 'public function __invoke' --include='*.php' src/Application/ | grep -E '^\s+foreach'
   ```
   A handler that loops over N items doing heavy work inline violates one-message-one-unit-of-work. Should dispatch N messages instead. Findings.

4. **Raw strings as IDs** — grep for `string $id` or `string $crawlId`:
   ```bash
   grep -rn 'string \$[a-z][a-zA-Z]*Id\b' --include='*.php' src/Domain/ src/Application/
   ```
   IDs should be typed value objects (`CrawlId`, not `string`). Findings.

5. **Mutating event-sourced aggregate state** — already covered in Pass 2, but re-verify in domain methods:
   ```bash
   grep -rn -A10 'public function ' --include='*.php' src/Domain/ | grep -E '\$this->[a-z][a-zA-Z]* ='
   ```
   Mutations outside `apply*()` are findings.

## Evidence Format

```
### [SEVERITY] [Pass]: [Short description]

**File:** `path/to/file.php:42`
**Evidence:** [grep output or code]
**Standard:** [which rule is violated]
**Fix:** [concrete code change]
```

## Output Template

```
## PHP Review

### Summary
- Files reviewed: N
- Type safety: X findings
- Immutability: X findings
- Linting: X findings
- Naming/structure: X findings
- Error handling: X findings
- Testing: X findings
- Domain/architecture: X findings

### Findings
[grouped by severity: critical, important, suggestion]

### Clean Areas
[what was done well]

### Verdict
REQUEST_CHANGES / APPROVE
```

## Zero-Finding Gate

If everything passes: "No findings. PHP review complete — all changed files comply with team standards." Do not invent issues to appear thorough.

## Related Skills

- `/coding-standards:review-standards` — cross-cutting quality and writing style checks that apply to all languages. Run alongside this review.
- `/coding-standards:review-git` — commit message and PR conventions. Run when reviewing a PR.
