# Test: review-go flags unhandled errors, bare error checks, and missing context

Scenario: A developer submits a Go file for review that contains four conventional violations: an unhandled error from `os.Open`, a `if err != nil { continue }` pattern that hides errors in flow control, errors returned without wrapping context, and a goroutine spawned without synchronisation. The skill should run its five passes, ground each finding in a grep snippet or line reference, and not invent findings the code doesn't support.

## Prompt

First, write this file to disk at `{workspace}/work/processor.go`:

```go
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

Then invoke `/coding-standards:review-go {workspace}/work/processor.go` and produce the review.

## Criteria

- [ ] PASS: Pass 1 (Error Handling) flags `f, _ := os.Open(path)` as an unhandled error — `os.Open` returns an error that is discarded with `_`
- [ ] PASS: Pass 1 flags `if err := dec.Decode(&r); err != nil { continue }` as flow control that hides the error — the decode failure is silently dropped
- [ ] PASS: Pass 1 flags `return err` from `compute()` errors without `fmt.Errorf` wrapping — the error reaches the caller with no context about which record failed
- [ ] PASS: Skill flags that `handleRecord` is `func (r Record)` (no error return) but contains `return err` — this is a real compile error in the fixture, the skill should call it out
- [ ] PASS: Skill flags the bare `go handleRecord(r)` — goroutine spawned without sync.WaitGroup, channel, or other synchronisation; the surrounding function may return before the goroutine finishes
- [ ] PARTIAL: Skill notes that `defer f.Close()` should also check the close error in long-running code, or at minimum acknowledge that ignoring close errors is acceptable for read-only file handles
- [ ] PASS: Each finding cites a line number or quotes the offending line — no findings without evidence
- [ ] PASS: Skill does NOT invent findings the code doesn't support (e.g. no false claims about missing tests, missing interface boundaries, missing context.Context unless explicitly grounded)

## Output expectations

- [ ] PASS: Output is structured by the skill's five passes (Error Handling, Interface Design, Goroutine Safety, Table-Driven Tests, etc.) — the structure is visible even when a pass has no findings
- [ ] PASS: Output uses grep-pattern style evidence (file:line snippets) for findings rather than narrative-only descriptions
- [ ] PASS: Output's Goroutine Safety section names the specific risk for `go handleRecord(r)` (unsynchronised lifetime, potential lost work, no panic recovery)
- [ ] PARTIAL: Output suggests concrete fixes for each high-severity finding — `errors.Join` or `fmt.Errorf("decode record %s: %w", id, err)` rather than generic "wrap the error"
