---
name: review-git
description: "Review git conventions — commit messages, PR titles, branch model, and content date integrity. Auto-invoked during PR and commit workflows."
argument-hint: "[PR number, commit range, or branch to review]"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

Review git practices against team conventions covering commit messages, PR standards, branch model, and content date integrity. Every check is concrete and verifiable.

## Mandatory Process

Execute all five passes. Every finding requires the specific commit hash or PR field that violates the convention.

### Pass 1: Conventional Commits Format

Every commit message must follow the Conventional Commits specification.

1. **Format check** — get all commit messages in scope:
   ```bash
   git log --oneline [range]
   ```
   Each commit must match: `<type>[optional scope]: <description>`

2. **Valid types** — the type must be one of:
   | Type | When to use |
   |------|-------------|
   | `feat` | New feature visible to users |
   | `fix` | Bug fix |
   | `docs` | Documentation only |
   | `style` | Formatting, whitespace, semicolons — no logic change |
   | `refactor` | Code change that neither fixes a bug nor adds a feature |
   | `test` | Adding or updating tests |
   | `chore` | Build process, tooling, dependencies |
   | `ci` | CI/CD configuration |
   | `perf` | Performance improvement |
   | `build` | Build system or external dependency changes |
   | `revert` | Reverts a previous commit |

   Anything else (`update`, `change`, `wip`, `misc`, `stuff`) is a finding.

3. **Imperative mood** — the description uses imperative: "Add feature" not "Added feature", "Adds feature", or "Adding feature":
   ```bash
   git log --format='%s' [range]
   ```
   Check each subject line. Common violations:
   - Past tense: "Fixed", "Updated", "Changed", "Removed"
   - Third person: "Fixes", "Updates", "Adds"
   - Gerund: "Fixing", "Updating", "Adding"

4. **Subject line length** — must be under 70 characters:
   ```bash
   git log --format='%s' [range] | awk 'length > 70'
   ```
   Any output is a finding.

5. **No period at end** — subject lines must not end with a period.

6. **Body separation** — if the commit has a body, a blank line must separate it from the subject. Check with:
   ```bash
   git log --format='%B' [range]
   ```

7. **Detail in the body** — for non-trivial commits, the body should explain WHY, not WHAT. The diff shows what changed. The body explains the reasoning, tradeoffs, or context that the diff cannot convey.

8. **Breaking changes** — breaking changes must use either `!` after the type/scope or a `BREAKING CHANGE:` footer:
   - `feat!: remove deprecated API`
   - Or in the footer: `BREAKING CHANGE: the /v1/users endpoint no longer accepts...`

### Pass 2: PR Title and Description

1. **PR title format** — must match conventional commit format. The PR title becomes the squash commit message, so it must be valid:
   ```bash
   gh pr view --json title
   ```
   Apply the same type, imperative mood, and length rules from Pass 1.

2. **One concern per PR** — a PR that touches unrelated systems is a finding. Signs of a multi-concern PR:
   - Title uses "and" to describe two separate things
   - Changes span multiple feature areas with no shared dependency
   - The diff could be split into independent PRs that each make sense alone

3. **Description completeness** — the PR description must include:
   - **What changed**: summary of the modification
   - **Why**: the motivation or problem being solved
   - **Test plan**: how to verify the changes work (manual steps, test commands, or "covered by CI")

   Missing any of these three sections is a finding.

4. **Linked issues** — if the project uses issue tracking, the PR should reference the relevant issue (`Closes #123`, `Fixes #456`). Not mandatory, but flag if there is no reference and the change is non-trivial.

### Pass 3: Branch Model

1. **Linear history** — branches land by rebase-then-fast-forward or by squash merge, never by merging `main` into the branch first. Check for merge commits:
   ```bash
   git log --merges [range]
   ```
   Merge commits on the main branch (except from the initial repo setup) are findings, including `Merge branch 'main' into feature/...` carried in by a fast-forward.

2. **No force push to shared branches** — grep the reflog or check CI for force-push events. Force pushing to `main`, `develop`, or any shared branch is a critical finding. Force pushing to a personal feature branch is acceptable.

3. **Branch naming** — feature branches should follow a convention:
   - `feat/description` or `feature/description`
   - `fix/description` or `bugfix/description`
   - `chore/description`
   - `docs/description`

   Branch names using the developer's name (`martin/fix-thing`) are acceptable as an alternative.

   Check the current branch name:
   ```bash
   git branch --show-current
   ```

4. **Branch freshness** — if the branch is more than 5 days behind the base branch, note it as a suggestion. Stale branches accumulate merge conflicts.

5. **Rebase over merge to update** — when a feature branch is behind `main`, the convention is to rebase, not to merge `main` into the feature branch. Merge commits from `main` into a feature branch are findings:
   ```bash
   git log --oneline --merges [branch] ^main
   ```

### Pass 4: Content Date Preservation

This matters for content-heavy repositories (blogs, documentation sites, changelogs).

1. **Publication dates** — if the diff modifies content files (markdown, MDX, YAML frontmatter), check whether publication dates or `date` fields were changed:
   ```bash
   git diff [range] -- '*.md' '*.mdx' | grep '^[+-]date:'
   ```
   Changing a publication date to today's date when only editing content (not republishing) is a finding. Preserve the original publication date.

2. **Last-modified dates** — if the content system uses `lastModified` or `updated` fields, those SHOULD be updated when content changes. Not updating `lastModified` is a finding.

3. **Changelog entries** — new changelog entries should use today's date. Backdating changelog entries is a finding.

### Pass 5: Commit Hygiene

1. **WIP commits** — commits with "wip", "work in progress", "temp", "TODO" in the message are findings if they are going to be merged (not squashed away):
   ```bash
   git log --format='%s' [range] | grep -i 'wip\|work in progress\|temp\|fixup\|squash'
   ```
   In a squash-merge workflow, these are acceptable in the branch history but must not survive as the final squash commit message.

2. **Empty commits** — commits with no file changes:
   ```bash
   git log --format='%H' [range] | while read h; do [ $(git diff-tree --no-commit-id --name-only -r $h | wc -l) -eq 0 ] && echo "Empty: $h"; done
   ```

3. **Large files** — new binary files or files over 1MB:
   ```bash
   git diff --stat [range] | grep -E '\d{4,} insertions'
   ```
   Large files should use Git LFS or be excluded.

4. **Sensitive data** — grep the diff for patterns that suggest committed secrets:
   ```bash
   git diff [range] | grep -iE 'password|secret|api_key|token|private_key|AWS_|GITHUB_TOKEN'
   ```
   Any hit requires manual verification. If it is a real secret, the commit must be amended and the secret rotated.

## Evidence Format

```
### [SEVERITY] [Pass]: [Short description]

**Commit:** `abc1234` or **PR field:** title/description
**Evidence:** [the actual message or diff output]
**Convention:** [which rule is violated]
**Fix:** [concrete rewording or action]
```

## Output Template

```
## Git Review

### Summary
- Commits reviewed: N
- Commit format: X findings
- PR standards: X findings
- Branch model: X findings
- Content dates: X findings (or N/A)
- Commit hygiene: X findings

### Findings
[grouped by severity: critical, important, suggestion]

### Clean Areas
[what was done well]
```

## Zero-Finding Gate

If all conventions are followed: "No findings. Git review complete — all commits and PR metadata follow team conventions." Do not manufacture findings.

## Related Skills

- `/coding-standards:review-standards` — cross-cutting quality and writing style checks. Complements git convention review.
- Language-specific reviews (`/coding-standards:review-dotnet`, `/coding-standards:review-python`, `/coding-standards:review-typescript`) — run alongside for code quality checks.
