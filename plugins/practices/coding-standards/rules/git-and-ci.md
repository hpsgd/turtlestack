---
description: Git workflow, branching, CI/CD, and commit conventions
---

# Git & CI/CD Conventions

## Commit message format

Commits must follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Common types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`, `perf`, `build`.

## Branch model

```
feature/my-thing ──rebase onto main, fast-forward (or squash)──> main
```

- Feature branches from `main`
- Linear history on main: rebase the branch onto `main` and fast-forward, or squash-merge. Rebase keeps the commit trail; squash collapses it to one message. Both are fine
- Never merge `main` into a feature branch. The merge commit rides along on the fast-forward and breaks linear history
- PR titles must be conventional commits
- No direct commits to main

## Pull requests
- Keep PRs focused — one feature or fix per PR
- Include a description of what changed and why
- Add a test plan describing how to verify the changes
- Request review from at least one team member

## Pre-commit checks
- Lint, format-check, and typecheck staged files before commit
- Fix issues before committing — don't bypass hooks

## Pre-push verification (monorepos)
- Run full CI across ALL projects, not just the one you changed
- In [Moon](https://moonrepo.dev) monorepos: `moon ci` checks web apps, packages, AND services
- Known gotchas: [Storybook](https://storybook.js.org) artifacts may need cleaning, CSharpier formatting, `package-lock.json` changes, .NET integration tests

## Updating a stale branch and force pushing
- Update a stale branch by rebasing onto `main`, not by merging `main` in
- Rebasing rewrites SHAs, so it's only free on a branch nobody else has pulled. Push it with `--force-with-lease`, never plain `--force`
- Discuss before rebasing or force-pushing a branch others have pulled, or when conflicts are messy
- Check `git remote -v` to verify the correct repo before any push

## Worktrees
- Put worktrees outside the repo directory (`../repo-topic`), not under `.claude/worktrees/`. A nested worktree shows up as untracked files in every other checkout
- Before `git worktree remove`, check and state: no uncommitted files, zero commits ahead of `main`, no stray test branches. It deletes the directory

## Content dates
- Preserve publication dates on articles and content — don't update to today's date
- Authors set intentional publish dates; changing them disrupts publishing schedules
