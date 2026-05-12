# Review Go

Scenario: A developer submits a Go file for review that contains four conventional violations: an unhandled error from `os.Open`, a `if err != nil { continue }` pattern that hides errors in flow control, errors returned without wrapping context, and a goroutine spawned without synchronisation. The skill should run its five passes, ground each finding in a grep snippet or line reference, and not invent findings the code doesn't support.

## Prompt

> First, write this file to disk at `{workspace}/work/processor.go`:
> 
> ```go
> package main
> 
> import (
> 	"encoding/json"
> 	"fmt"
> 	"os"
> )
> 
> type Record struct {
> 	ID    string `json:"id"`
> 	Value int    `json:"value"`
> }
> 
> func ProcessFile(path string) error {
> 	f, _ := os.Open(path)
> 	defer f.Close()
> 
> 	dec := json.NewDecoder(f)
> 	for dec.More() {
> 		var r Record
> 		if err := dec.Decode(&r); err != nil {
> 			continue
> 		}
> 		go handleRecord(r)
> 	}
> 	return nil
> }
> 
> func handleRecord(r Record) {
> 	result, err := compute(r)
> 	if err != nil {
> 		return err
> 	}
> 	fmt.Println(result)
> }
> 
> func compute(r Record) (int, error) {
> 	if r.Value < 0 {
> 		return 0, fmt.Errorf("invalid value")
> 	}
> 	return r.Value * 2, nil
> }
> ```
> 
> Then invoke `/coding-standards:review-go {workspace}/work/processor.go` and produce the review.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Go Review

### Summary
- Files reviewed: 1
- Error handling: 3 critical findings
- Interface design: 0 findings
- Goroutine safety: 2 critical findings
- Table-driven tests: 1 critical finding
- Code structure: 2 important findings

### Pass 1 — Error Handling

#### CRITICAL: Unhandled error from os.Open

**File:** `processor.go:16`

**Evidence:**
```go
f, _ := os.Open(path)
```

**Standard:** Rule — "Ignore errors only with intent. Never use bare `_` to ignore an error."

**Fix:** Handle the error explicitly:
```go
f, err := os.Open(path)
if err != nil {
	return fmt.Errorf("opening file: %w", err)
}
defer f.Close()
```

This is critical because the subsequent `defer f.Close()` and `json.NewDecoder(f)` operate on a potentially nil file handle.

---

#### CRITICAL: Compilation error in handleRecord function signature

**File:** `processor.go:24-26`

**Evidence:**
```go
func handleRecord(r Record) {
	result, err := compute(r)
	if err != nil {
		return err
	}
```

**Standard:** Go syntax — function signature declares no return type, but line 26 attempts to return an error value.

**Fix:** Either declare the return type or remove the return statement:
```go
func handleRecord(r Record) error {
	result, err := compute(r)
	if err != nil {
		return err
	}
	fmt.Println(result)
	return nil
}
```

This code does not compile as written.

---

#### IMPORTANT: Decode error silently skipped

**File:** `processor.go:19-20`

**Evidence:**
```go
if err := dec.Decode(&r); err != nil {
	continue
}
```

**Standard:** Rule — "Errors must be wrapped when crossing function boundaries. Every return err must become return fmt.Errorf with context."

**Fix:** At minimum, log or return the error:
```go
if err := dec.Decode(&r); err != nil {
	return fmt.Errorf("decoding record: %w", err)
}
```

Silently skipping decode errors means malformed records are dropped without caller awareness. If the intent is to skip bad records, add a comment and consider logging.

---

### Pass 2 — Interface Design

No findings. No interfaces defined in the code.

---

### Pass 3 — Goroutine Safety

#### CRITICAL: Goroutines spawned without synchronization

**File:** `processor.go:21`

**Evidence:**
```go
go handleRecord(r)
```

**Standard:** Rule — "Protect mutable shared state with mutexes. Channel directions must be explicit. Unbuffered channels require careful synchronization."

**Issue:** Goroutines are spawned in a loop with no synchronization mechanism. The `ProcessFile` function will return immediately (line 27) while the spawned goroutines may still be running. This creates a race condition where:
- The caller cannot wait for all records to be processed
- If an error occurs in a goroutine, it is lost
- Output from `fmt.Println(result)` in each goroutine is unsynchronized

**Fix:** Use `sync.WaitGroup` to coordinate:
```go
import "sync"

func ProcessFile(path string) error {
	// ... file opening ...
	
	var wg sync.WaitGroup
	for dec.More() {
		var r Record
		if err := dec.Decode(&r); err != nil {
			return fmt.Errorf("decoding: %w", err)
		}
		wg.Add(1)
		go func(r Record) {
			defer wg.Done()
			handleRecord(r)
		}(r)
	}
	wg.Wait()
	return nil
}
```

Note: Also capture `r` in the closure to avoid the loop-variable capture bug.

---

#### IMPORTANT: No error collection from goroutines

**File:** `processor.go:24-29`

**Evidence:**
```go
func handleRecord(r Record) {
	result, err := compute(r)
	if err != nil {
		return err
	}
	fmt.Println(result)
}
```

**Issue:** Even after fixing the function signature, errors computed inside goroutines are never returned to the caller. There's no channel or error collection mechanism.

**Fix:** Return errors through a channel or store them in a thread-safe structure:
```go
func ProcessFile(path string) error {
	// ...
	errChan := make(chan error, 1)
	var wg sync.WaitGroup
	
	for dec.More() {
		// ...
		wg.Add(1)
		go func(r Record) {
			defer wg.Done()
			if err := handleRecord(r); err != nil {
				select {
				case errChan <- err:
				default:
				}
			}
		}(r)
	}
	
	go func() {
		wg.Wait()
		close(errChan)
	}()
	
	for err := range errChan {
		return err
	}
	return nil
}
```

---

### Pass 4 — Table-Driven Tests

#### CRITICAL: No tests exist

**File:** `processor.go` (no `*_test.go` file)

**Standard:** Rule — "Table-driven tests are mandatory. Every test must follow the struct + range pattern."

**Issue:** The entire package is missing test coverage. At minimum, create `processor_test.go` with tests for:
- Successful record processing
- JSON decode errors
- Negative values in compute function
- Empty input file
- Goroutine completion (using channels or WaitGroup)

**Example structure:**
```go
func TestCompute(t *testing.T) {
	tests := []struct {
		name    string
		input   Record
		want    int
		wantErr bool
	}{
		{name: "positive value", input: Record{ID: "1", Value: 5}, want: 10, wantErr: false},
		{name: "negative value", input: Record{ID: "2", Value: -1}, want: 0, wantErr: true},
		{name: "zero value", input: Record{ID: "3", Value: 0}, want: 0, wantErr: false},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := compute(tt.input)
			if (err != nil) != tt.wantErr {
				t.Errorf("compute() error = %v, wantErr %v", err, tt.wantErr)
			}
			if got != tt.want {
				t.Errorf("compute() = %v, want %v", got, tt.want)
			}
		})
	}
}
```

---

### Pass 5 — Code Structure and Idiom

#### IMPORTANT: Missing doc comments on exported symbols

**File:** `processor.go`

**Evidence:**
- Line 6: `type Record struct` — exported, no comment
- Line 13: `func ProcessFile(path string) error` — exported, no comment
- Line 24: `func handleRecord(r Record)` — lowercase, doesn't need comment (but see below)
- Line 31: `func compute(r Record) (int, error)` — lowercase, doesn't need comment

**Standard:** Rule — "Comment usage — exported functions must have comments. Grep for `func [A-Z]`. Verify each exported function has a comment above it that starts with the function name."

**Fix:** Add doc comments:
```go
// Record represents a JSON record with an ID and integer value.
type Record struct {
	ID    string `json:"id"`
	Value int    `json:"value"`
}

// ProcessFile reads a JSON-encoded file line by line and processes each record.
func ProcessFile(path string) error {
	// ...
}
```

---

#### SUGGESTION: Defer Close without open verification

**File:** `processor.go:16-17`

**Evidence:**
```go
f, _ := os.Open(path)
defer f.Close()
```

**Issue:** The `defer` is attached to a potentially nil file pointer (because the os.Open error was ignored). While Go's Close on a nil pointer is safe, this is misleading code structure. Fix by handling the error first (see Pass 1 finding).

---

### Clean Areas

- Struct tagging is correct and well-formed (`json:"id"`, `json:"value"`).
- Package structure is appropriate (single file for a simple processor).
- Variable naming follows camelCase convention throughout.
- The intent to use JSON decoding for streaming is sound (good choice over unmarshaling the entire file).

---

## Summary of Fixes Required

1. **Handle os.Open error** (critical)
2. **Fix handleRecord function signature** — add `error` return type (critical, blocks compilation)
3. **Add WaitGroup or channel synchronization** for goroutines (critical)
4. **Handle or wrap Decode error** instead of silently skipping (important)
5. **Add table-driven tests** covering compute logic and ProcessFile (critical)
6. **Add doc comments** to Record and ProcessFile (important)

### Artifacts written

#### `work/processor.go`

```
package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type Record struct {
	ID    string `json:"id"`
	Value int    `json:"value"`
}

func ProcessFile(path string) error {
	f, _ := os.Open(path)
	defer f.Close()

	dec := json.NewDecoder(f)
	for dec.More() {
		var r Record
		if err := dec.Decode(&r); err != nil {
			continue
		}
		go handleRecord(r)
	}
	return nil
}

func handleRecord(r Record) {
	result, err := compute(r)
	if err != nil {
		return err
	}
	fmt.Println(result)
}

func compute(r Record) (int, error) {
	if r.Value < 0 {
		return 0, fmt.Errorf("invalid value")
	}
	return r.Value * 2, nil
}

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 10.0/11.0 (91%) |
| Evaluated | 2026-05-12 |
| Target duration | 37184 ms |
| Target cost | $0.0808 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Pass 1 (Error Handling) flags `f, _ := os.Open(path)` as an unhandled error — `os.Open` returns an error that is discarded with `_` | PASS | "CRITICAL: Unhandled error from os.Open" at processor.go:16, quotes `f, _ := os.Open(path)` exactly. |
| c2 | Pass 1 flags `if err := dec.Decode(&r); err != nil { continue }` as flow control that hides the error — the decode failure is silently dropped | PASS | "IMPORTANT: Decode error silently skipped" at processor.go:19-20, quotes the if/continue block and notes malformed records are dropped silently. |
| c3 | Pass 1 flags `return err` from `compute()` errors without `fmt.Errorf` wrapping — the error reaches the caller with no context about which record failed | FAIL | The wrapping rule is cited only for the decode path. The `return err` in handleRecord for compute errors is treated as a compile error only; no wrapping-with-context finding for compute errors. |
| c4 | Skill flags that `handleRecord` is `func (r Record)` (no error return) but contains `return err` — this is a real compile error in the fixture, the skill should call it out | PASS | "CRITICAL: Compilation error in handleRecord function signature" at processor.go:24-26: "function signature declares no return type, but line 26 attempts to return an error value." |
| c5 | Skill flags the bare `go handleRecord(r)` — goroutine spawned without sync.WaitGroup, channel, or other synchronisation; the surrounding function may return before the goroutine finishes | PASS | "CRITICAL: Goroutines spawned without synchronization" at processor.go:21, evidence quotes `go handleRecord(r)`, names WaitGroup and channel alternatives. |
| c6 | Skill notes that `defer f.Close()` should also check the close error in long-running code, or at minimum acknowledge that ignoring close errors is acceptable for read-only file handles | PARTIAL | Pass 5 "SUGGESTION: Defer Close without open verification" mentions the defer on a potentially nil pointer but frames it as misleading code structure, not as a close-error-checking concern. |
| c7 | Each finding cites a line number or quotes the offending line — no findings without evidence | PASS | Every finding has a **File:** line (e.g., processor.go:16, processor.go:19-20, processor.go:21, processor.go:24-26) and a quoted code block. |
| c8 | Skill does NOT invent findings the code doesn't support (e.g. no false claims about missing tests, missing interface boundaries, missing context.Context unless explicitly grounded) | PASS | Pass 2 states "No findings. No interfaces defined in the code." Tests are genuinely absent. No context.Context or false interface findings present. |
| c9 | Output is structured by the skill's five passes (Error Handling, Interface Design, Goroutine Safety, Table-Driven Tests, etc.) — the structure is visible even when a pass has no findings | PASS | All five passes are explicit headers: Pass 1 — Error Handling, Pass 2 — Interface Design, Pass 3 — Goroutine Safety, Pass 4 — Table-Driven Tests, Pass 5 — Code Structure and Idiom. |
| c10 | Output uses grep-pattern style evidence (file:line snippets) for findings rather than narrative-only descriptions | PASS | Every finding has a **File:** `processor.go:<line>` header and a fenced code block quoting the offending snippet, not just narrative prose. |
| c11 | Output's Goroutine Safety section names the specific risk for `go handleRecord(r)` (unsynchronised lifetime, potential lost work, no panic recovery) | PASS | Names: function returns while goroutines still running, errors lost from goroutines, unsynchronized fmt.Println output. Covers unsynchronised lifetime and lost work explicitly. |
| c12 | Output suggests concrete fixes for each high-severity finding — `errors.Join` or `fmt.Errorf("decode record %s: %w", id, err)` rather than generic "wrap the error" | PARTIAL | Fixes shown: `fmt.Errorf("opening file: %w", err)` and `fmt.Errorf("decoding record: %w", err)` — concrete but missing record ID in context; no `errors.Join` usage. |

### Notes

The review is thorough and well-structured across all five passes, correctly identifying the four seeded violations and the bonus compile error. The one gap is c3: the criterion asked specifically for flagging unwrapped errors from compute() propagating without record context, which the skill absorbed into the compile-error finding rather than treating as a separate wrapping-convention violation.
