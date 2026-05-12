---
name: review-go
description: "Review Go code against team conventions — error handling patterns, interface design, goroutine safety, and table-driven tests. Auto-invoked when reviewing .go files."
argument-hint: "[files, PR, or git range to review]"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
paths:
  - "**/*.go"
---

Review Go code against team standards covering error handling patterns, interface design, goroutine safety, and testing conventions. Every check has a concrete grep pattern. Every finding requires evidence.

## Mandatory Process

Execute all five passes. Do not skip.

### Pass 1: Error Handling

Go error handling is explicit. Every error must be handled or intentionally ignored.

1. **Unhandled errors** — grep for error-returning function calls without assignment:
   ```bash
   grep -rn '^\s*[a-zA-Z_].*(\s*$' --include='*.go' [changed files] | grep -v '= '
   ```
   Any function call that could return an error (look for known error-returning functions like `os.Open`, `json.Unmarshal`, `ioutil.ReadFile`) must be handled. Check each:
   - `err := function()` and verify the error is checked immediately after
   - If error is intentionally ignored, must have explicit `_ = function()` or a preceding comment `// error ignored on purpose`

2. **Bare error checks** — grep for error checks:
   ```bash
   grep -rn 'if err != nil' --include='*.go' [changed files]
   ```
   Verify each is followed by:
   - `return err` (wrapping if not at the top level)
   - `return fmt.Errorf(...)` (wrapping with context)
   - `return nil` (specific error was handled)
   - `panic(err)` (only if this is a fatal initialization error — rare)
   
   Finding: bare `if err != nil { continue }`, `if err != nil { break }`, or other flow control that hides the error.

3. **Error wrapping** — grep for error returns:
   ```bash
   grep -rn 'return err' --include='*.go' [changed files]
   ```
   At any point where an error crosses a function boundary, it must be wrapped with `fmt.Errorf("doing X: %w", err)` to add context. Returning a bare `err` from a called function is a finding unless this is in a one-liner that immediately wraps it.

4. **Sentinel errors** — grep for `errors.New`:
   ```bash
   grep -rn 'errors\.New' --include='*.go' [changed files]
   ```
   Sentinel errors (package-level `var ErrNotFound = errors.New(...)`) should be used for expected failure modes. Creating an error inline with `errors.New` inside a function is a finding unless it is truly transient.

5. **Panic for control flow** — grep for `panic(`:
   ```bash
   grep -rn 'panic(' --include='*.go' [changed files]
   ```
   Panic must not be used for expected error conditions (bad input, resource not found, network timeout). Panic is only for unrecoverable bugs (corrupt heap, programmer error). Any panic in business logic is a finding.

### Pass 2: Interface Design

Interfaces should be small, specific, and located close to the client, not the implementer.

1. **Exported interface definitions** — grep for `type.*interface`:
   ```bash
   grep -rn 'type.*interface {' --include='*.go' [changed files]
   ```
   Every interface should be asking: "Does this interface belong in this package, or should it be defined by the caller?" 
   - Interfaces for internal implementation details should be in the same package or file, not exported
   - Exported interfaces should represent behavior contracts (e.g., `io.Reader`, `io.Writer`)
   - Finding: a large interface (5+ methods) that mixes unrelated behaviors — split it

2. **Interface segregation** — if an interface has more than 4 methods, check if it could be split:
   ```bash
   grep -rn 'type [A-Z][a-zA-Z]* interface {' -A 10 --include='*.go' [changed files]
   ```
   Read the interface and check if clients actually use all methods. If some clients use only 2-3 methods, create smaller focused interfaces.

3. **Accepting interfaces, returning concrete types** — grep for function signatures:
   ```bash
   grep -rn 'func.*) [*]interface' --include='*.go' [changed files]
   ```
   Functions should never return `interface{}` or `*Interface`. Return concrete types. Accept interfaces as parameters to allow flexibility.

4. **Empty interface usage** — grep for `interface{}`:
   ```bash
   grep -rn 'interface{}' --include='*.go' [changed files]
   ```
   Every use of `interface{}` or `any` is a finding unless:
   - It is in a generic constraint where you genuinely need any type
   - It is in a variable-argument function like `fmt.Printf`
   - It is wrapping an external library with no type information
   All other uses should be replaced with specific types or generics.

### Pass 3: Goroutine Safety

Goroutines must not create race conditions. Every shared state must be protected.

1. **Global mutable state** — grep for package-level variables that are modified:
   ```bash
   grep -rn '^var [a-z_]' --include='*.go' [changed files]
   ```
   Read each package-level variable. If it is mutable (a map, slice, or struct that changes after initialization), it must be protected by a mutex. Finding: a package-level map or slice that is written from multiple goroutines without synchronization.

2. **Mutex protection** — grep for map and slice access:
   ```bash
   grep -rn '\[.*\] =' --include='*.go' [changed files]
   ```
   Verify each write to a shared map or slice is preceded by a mutex lock. Search for `lock.Lock()` or `m.Lock()` in the vicinity.

3. **Channel usage** — grep for channel operations:
   ```bash
   grep -rn 'make(chan' --include='*.go' [changed files]
   ```
   Verify:
   - Buffered channels are used only when the buffer size is explicitly justified (comment required)
   - Channels are closed by the sender, not the receiver
   - Select statements have a timeout or context deadline to prevent deadlock
   - Finding: unbuffered channels in loops without careful synchronization

4. **Race detector** — the codebase should be tested with `go test -race`. Check if this is configured in CI:
   ```bash
   grep -rn '\-race' --include='*.yaml' --include='*.yml' [changed files]
   ```
   If race detector is not enabled, flag as a finding.

### Pass 4: Table-Driven Tests

Go tests must follow the table-driven pattern. This is idiomatic Go.

1. **Test structure** — grep for test functions:
   ```bash
   grep -rn 'func Test' --include='*_test.go' [changed files]
   ```
   Every test must follow this pattern:
   ```go
   func TestFunctionName(t *testing.T) {
       tests := []struct {
           name    string
           input   InputType
           want    OutputType
           wantErr bool
       }{
           {name: "...", input: ..., want: ..., wantErr: false},
       }
       for _, tt := range tests {
           t.Run(tt.name, func(t *testing.T) {
               got, err := Function(tt.input)
               if (err != nil) != tt.wantErr {
                   t.Errorf("expected error %v, got %v", tt.wantErr, err)
               }
               if got != tt.want {
                   t.Errorf("got %v, want %v", got, tt.want)
               }
           })
       }
   }
   ```
   Finding: test functions that branch with if statements instead of using table-driven structure.

2. **Test naming** — each table entry must have a descriptive `name` field:
   ```bash
   grep -rn '{name: ""' --include='*_test.go' [changed files]
   ```
   Every test case name must describe the scenario, not just be empty or "case 1". Example: `"empty input returns error"`, `"special characters in email"`.

3. **Subtests** — verify the test uses `t.Run(tt.name, ...)`:
   ```bash
   grep -rn 't\.Run' --include='*_test.go' [changed files]
   ```
   All table-driven tests must use subtests for isolation and parallel execution.

4. **Test coverage** — the codebase should have high test coverage (80%+). Check if coverage is reported in CI.

### Pass 5: Code Structure and Idiom

Go has specific idioms. Follow them.

1. **Named return values** — grep for named returns:
   ```bash
   grep -rn 'func.*(\s*\w\+\s\+\w\+)\s*(' --include='*.go' [changed files]
   ```
   Named return values are acceptable only when they document the return value (rare). For most functions, use anonymous returns. Finding: named returns that are not immediately used in a bare `return` statement.

2. **Blank identifier usage** — grep for `_`:
   ```bash
   grep -rn '_ =' --include='*.go' [changed files]
   ```
   Verify the blank identifier is used correctly:
   - `_ = someFunc()` — intentionally ignoring an error or return value
   - `for _, item := range slice` — ignoring the index in a range
   All uses must have justification. Unused `_` variables are a finding.

3. **Defer usage** — grep for `defer`:
   ```bash
   grep -rn 'defer ' --include='*.go' [changed files]
   ```
   Defer should be used for cleanup (closing files, releasing locks). Verify:
   - Deferred functions are called as close as possible to the resource acquisition
   - Deferred functions don't capture loop variables (common bug)

4. **Naming conventions** — Go uses camelCase for identifiers. Check:
   ```bash
   grep -rn '[a-z_]*_[a-z_]*' --include='*.go' [changed files] | grep -v 'test_\|_test\.go\|_version\|_v[0-9]'
   ```
   Variables and functions must use camelCase, not snake_case. Constants and package names are exceptions (ALL_CAPS and lowercase respectively).

5. **Comment usage** — exported functions must have comments. Grep for `func [A-Z]`:
   ```bash
   grep -rn 'func [A-Z]' --include='*.go' [changed files]
   ```
   Verify each exported function (starts with uppercase) has a comment above it that starts with the function name.

## Rules

- **Ignore errors only with intent.** Never use bare `_` to ignore an error. Use `_ = function()` with an explicit comment explaining why the error is safe to discard. Finding: `result, _ := function()` without justification.
- **Never panic in business logic.** Panic must only occur in unrecoverable initialization errors (`main`, `init`) or to catch programmer bugs (corrupt state, violated invariants). Any panic in a handler, API endpoint, or utility is a finding.
- **Errors must be wrapped when crossing function boundaries.** Every `return err` must become `return fmt.Errorf("context: %w", err)` unless the error is being handled by the same function that caught it. Bare error returns lose context.
- **Accept interfaces, return concrete types.** Never return `interface{}`, `any`, or pointer to interface. Return concrete types. Accept interface{} only in generic containers (fmt.Printf-style), and only when a generic TypeVar won't work.
- **Protect mutable shared state with mutexes.** Any map, slice, or mutable struct accessed from multiple goroutines must be guarded by `sync.Mutex` or `sync.RWMutex`. Finding: a package-level map written without lock protection.
- **Use sync.RWMutex only for read-heavy workloads.** If a map is written frequently (more than 5% of accesses), use `sync.Mutex`. RWMutex has contention overhead; Mutex is simpler and faster for balanced read/write.
- **Channel directions must be explicit in function signatures.** Use `chan<-` (send-only) and `<-chan` (receive-only) in parameters and return types, never bare `chan`. Finding: `func Process(ch chan string)` should be `func Process(ch <-chan string)`.
- **context.Context must be the first parameter.** Any function that accepts a context (concurrent work, network I/O) must have `ctx context.Context` as the first parameter. Finding: `func DoWork(timeout int, ctx context.Context)`.
- **Table-driven tests are mandatory.** Every test must follow the struct + range pattern. Branching with `if` statements inside tests is a finding.
- **Unbuffered channels require careful synchronization.** Buffered channels must justify their size with a comment. Unbuffered channels in loops are a finding unless the loop carefully syncs with the receiver.
- **Sentinel errors belong at package scope.** Create expected errors as `var ErrNotFound = errors.New(...)` at package level. Creating errors inline is acceptable only for transient errors (should be rare). Finding: `return errors.New("not found")` instead of checking a package sentinel.
- **Use named returns only for documentation.** Named returns are acceptable when they document the semantics of return values (e.g., `func Divide(a, b int) (quotient, remainder int)`), but never just to reduce the return statement. Finding: named returns followed by explicit values in the return statement.

## Evidence Format

```
### [SEVERITY] [Pass]: [Short description]

**File:** `path/to/file.go:42`
**Evidence:** [grep output or code]
**Standard:** [which rule is violated]
**Fix:** [concrete code change]
```

## Output Template

```
## Go Review

### Summary
- Files reviewed: N
- Error handling: X findings
- Interface design: X findings
- Goroutine safety: X findings
- Table-driven tests: X findings
- Code structure: X findings

### Pass 1 — Error Handling
[findings, or "No findings." Each finding follows the Evidence Format above.]

### Pass 2 — Interface Design
[findings, or "No findings."]

### Pass 3 — Goroutine Safety
[findings, or "No findings."]

### Pass 4 — Table-Driven Tests
[findings, or "No findings."]

### Pass 5 — Code Structure and Idiom
[findings, or "No findings."]

### Clean Areas
[what was done well]
```

Severity (critical / important / suggestion) is part of each finding header, not the section structure. The five passes are the primary skeleton; severity belongs inside the per-pass section.

## Evidence Gate (non-negotiable)

Every finding must be grounded in the actual fixture code. Before recording a finding:

1. Quote the line that violates the rule. The quote must match the source byte-for-byte.
2. State the line number.
3. Name the specific rule from "Rules" above that is violated.

If you cannot quote a matching line, the finding is fabricated — drop it. Do not paraphrase "this function should be lowercase" when the function already is lowercase. Do not apply exported-symbol rules to unexported identifiers. Do not invent missing tests, missing context.Context parameters, or missing interface boundaries unless you can quote the place they should have appeared and explain why their absence is observable in the diff under review.

When in doubt: re-grep the fixture for the pattern the finding depends on. If the grep returns nothing, the finding has no evidence — drop it.

## Zero-Finding Gate

If everything passes: "No findings. Go review complete — all changed files comply with team standards." Do not invent issues to appear thorough.

## Related Skills

- `/coding-standards:review-standards` — cross-cutting quality and writing style checks that apply to all languages. Run alongside this review.
- `/coding-standards:review-git` — commit message and PR conventions. Run when reviewing a PR.
