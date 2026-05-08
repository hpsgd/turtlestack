---
description: "Check for a spec before starting implementation. Never write code without a spec that has passed the Definition of Ready."
alwaysApply: true
---

# Spec-First Implementation

Before writing any implementation code (models, API endpoints, infrastructure, tests), verify:

1. **A spec exists** for this work (check `docs/specs/` or `docs/quality/specs/`)
2. **Acceptance criteria** are written in Given/When/Then format
3. **A manual verification plan** exists (how QA verifies it works for real — not just automated tests)
4. **3 amigos review** has happened (Product Owner + Architect + QA Lead have signed off)

If no spec exists, **stop and report back** to your lead (CTO or CPO) that the work is not ready for implementation. Do not proceed without the spec — even if the task description seems clear.

## What "done" means

Code is not done when tests pass. Code is done when:
- Automated tests pass (unit, integration, acceptance)
- Manual verification succeeds (someone can actually use the feature)
- The spec's acceptance criteria are all met with evidence
- QA has signed off

## Exceptions

- **Trivial fixes** (<2 minutes): typos, single-line bug fixes, formatting. The git diff is the spec.
- **Spike/investigation work**: explicitly scoped as "investigation, not implementation." The output is a report, not code.

## Why this rule exists

A full pipeline was built with 237 passing automated tests, but nobody could actually run it and see results. The QA process was purely automated — no manual verification, no 3 amigos, no observability. "Tests pass" is not the same as "it works."
