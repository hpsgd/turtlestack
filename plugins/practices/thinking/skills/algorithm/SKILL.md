---
name: algorithm
description: Structured seven-phase execution methodology for complex tasks. Transition from current state to ideal state using verifiable criteria. Use for any non-trivial work that benefits from systematic execution.
argument-hint: "[task to execute through the algorithm]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Execute $ARGUMENTS using the seven-phase algorithm. The goal: transition from CURRENT STATE to IDEAL STATE using verifiable criteria.

## Before Starting

Determine the effort level based on the task:

| Effort | Budget | ISC range | When |
|--------|--------|-----------|------|
| Standard | <2min | 8-16 | Normal request (default) |
| Extended | <8min | 16-32 | Quality must be extraordinary |
| Advanced | <16min | 24-48 | Substantial multi-file work |
| Deep | <32min | 40-80 | Complex multi-system design |
| Comprehensive | <120min | 64-150 | Large-scale, no time pressure |

## Phase 1: OBSERVE

Understand the current state and define the ideal state.

1. **Reverse engineer the request**: Extract explicit wants, implied wants, explicit not-wanted, implied not-wanted, gotchas
2. **Determine effort level** from the table above
3. **Generate ISC** — Ideal State Criteria as atomic checkboxes. Apply the Splitting Test to every criterion (see `/isc` skill for the full methodology)
4. **ISC Count Gate** — cannot exit OBSERVE with fewer criteria than the effort tier floor
5. **Identify approach** — what tools, skills, and techniques are needed?

Present the criteria checklist and approach before proceeding.

## Phase 2: THINK

Pressure-test the approach before committing.

1. **Riskiest assumptions** (2-12): What are you assuming that could be wrong? List and assess each
2. **Premortem** (2-12): Imagine the work is done and it failed. What went wrong? List the most likely failure modes
3. **Prerequisites check**: Is anything needed before starting? Missing context, permissions, dependencies?
4. **ISC refinement**: Re-test criteria against the Splitting Test. Add criteria for failure modes surfaced by the premortem

## Phase 3: PLAN

Lay out the execution sequence.

1. **Validate prerequisites** — confirm everything needed is available
2. **Sequence the work** — what order minimises risk and rework?
3. **Identify decision points** — where might you need to choose between approaches?
4. For Advanced+ effort: document the technical approach and key architectural decisions

## Phase 4: BUILD

Set up the scaffolding and infrastructure needed for execution.

1. Create any necessary structure (files, directories, configurations)
2. Set up test infrastructure if needed
3. Make non-obvious decisions and document them

## Phase 5: EXECUTE

Do the work. Mark criteria complete as they pass.

1. Work through the plan systematically
2. **Mark each ISC complete immediately** as it passes — don't batch at the end
3. Track progress: `3/8 criteria met`
4. If you hit a decision point, make the decision and document why

## Phase 6: VERIFY

Confirm every criterion is actually met.

1. Go through each ISC criterion individually
2. **Verify with evidence** — tool output, test results, file contents, grep results
3. "I believe it's correct" is not verification. Use a tool
4. Mark any criterion that doesn't pass with what's missing

## Phase 7: LEARN

Reflect on the execution.

1. What went well?
2. What could have been done differently?
3. Were the effort level and ISC count appropriate?
4. Any patterns worth remembering for similar tasks?

If the user has the learning skill available, capture insights there.

## Critical Rules

- **Criteria before execution** — never start building before OBSERVE is complete
- **Atomic criteria only** — every criterion must pass the Splitting Test
- **Evidence-based verification** — no criterion marked complete without tool-based proof
- **Mark progress immediately** — update criteria as they pass, not at the end
- **Document decisions** — non-obvious choices documented as they're made
- **Stay within scope** — the criteria define the work. Don't expand beyond them

## Output Format

```markdown
## Execution: [task name]

### Phase 1: OBSERVE
**Effort level:** [Standard/Extended/Advanced/Deep/Comprehensive]
**ISC Count:** [N] criteria

#### Ideal State Criteria
- [ ] ISC-1: [criterion]
- [ ] ISC-2: [criterion]
- [ ] ISC-N: [criterion]

### Phase 2: THINK
**Riskiest assumptions:**
1. [assumption] — impact if wrong: [impact]

**Premortem failures:**
1. [failure mode] — mitigation: [action]

### Phase 3: PLAN
[Sequenced work items]

### Phase 5: EXECUTE
Progress: [X]/[N] criteria met
- [x] ISC-1: [evidence]
- [ ] ISC-2: [in progress]

### Phase 6: VERIFY
| Criterion | Status | Evidence |
|---|---|---|
| ISC-1 | ✅ | [tool output or file reference] |
| ISC-2 | ✅ | [evidence] |

### Phase 7: LEARN
- [What went well]
- [What to do differently]
```

## Related Skills

- `/isc` — the criteria decomposition methodology used in Phase 1. Use for the Splitting Test.
- `/thinking:retrospective` — turn insights from Phase 7 into learned rules when they should hold everywhere.
- `/scientific-method` — for investigation tasks where the goal is understanding rather than building.
