# Bootstrap

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/architecture/CLAUDE.md` containing a user-authored section. The react-developer bootstrap skill should preserve that user content while appending the React/Next.js Conventions section (with a merge marker), without creating any new files. The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

> The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/architecture/CLAUDE.md` is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.
> 
> Read the react-developer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/engineering/react-developer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.
> 
> After the bootstrap completes, output the manifest summary the skill defines (files updated, files merged, next steps).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

**Step 3: Return manifest**

## React Developer Bootstrap Complete

### Files updated
- `docs/architecture/CLAUDE.md` — appended React/Next.js Conventions section

### Files merged
- `docs/architecture/CLAUDE.md` — React conventions appended while preserving existing custom team notes section and USER-EDIT-SENTINEL marker

### Next steps
- Configure Tailwind CSS and `cn()` utility
- Set up Vitest with React Testing Library
- Use `/react-developer:component-from-spec` for new components
- Use `/react-developer:performance-audit` for performance reviews

### Artifacts written

#### `work/docs/architecture/CLAUDE.md`

```
# Architecture Domain

This directory contains architecture documentation for the project.

## Custom team notes

USER-EDIT-SENTINEL-DO-NOT-STRIP

This section was written by the team and must survive any bootstrap re-run.
It exists to test the safe-merge contract: the bootstrap skill must not
overwrite or remove user-authored content.

<!-- Added by react-developer bootstrap v0.1.0 -->
## React/Next.js Conventions

### TypeScript

- **Strict mode enabled** — `"strict": true` in `tsconfig.json`
- No `any` — use `unknown` and narrow, or define proper types
- Prefer `interface` for object shapes, `type` for unions and intersections
- Export types alongside components: co-locate types in the same file

### Styling

- **Tailwind CSS** for all styling — no CSS modules or styled-components
- Use `cn()` utility (clsx + tailwind-merge) for conditional classes
- Design tokens via Tailwind config (`tailwind.config.ts`)
- Responsive: mobile-first (`sm:`, `md:`, `lg:` breakpoints)

### Component Patterns

- Server Components by default (Next.js App Router)
- `"use client"` only when the component needs interactivity or browser APIs
- Co-locate components with their tests: `Button.tsx` + `Button.test.tsx`
- Props interfaces named `{Component}Props`
- Prefer composition over prop drilling — use React Context sparingly

### Testing

- **Vitest** for unit and component tests
- **React Testing Library** for component testing — test behaviour, not implementation
- Test file naming: `{Component}.test.tsx`
- Use `screen.getByRole()` queries — avoid `getByTestId` unless necessary
- Coverage enforced via SonarCloud (project-specific threshold)

### Project Structure

```
src/
├── app/                 # Next.js App Router (pages, layouts, routes)
├── components/
│   ├── ui/              # Reusable primitives (Button, Input, Card)
│   └── features/        # Feature-specific composed components
├── lib/                 # Shared utilities, API clients, hooks
├── types/               # Shared TypeScript types
└── styles/              # Global styles, Tailwind config
```

### Deployment

- **Vercel** for hosting with preview deployments on every PR
- Environment variables managed in Vercel dashboard
- Production deploy on merge to main (or release tag)

### React/Next.js Tooling

| Tool | Purpose |
|------|---------|
| [Vercel](https://vercel.com) | Frontend hosting with preview deploys |
| [SonarCloud](https://sonarcloud.io) | TypeScript code quality and coverage gate |
| [GitHub Actions](https://docs.github.com/en/actions) | `vitest` in CI on every PR |

### Available React Skills

| Skill | Purpose |
|-------|---------|
| `/react-developer:component-from-spec` | Create a React component from a design spec |
| `/react-developer:performance-audit` | Audit frontend performance |

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/8.0 (94%) |
| Evaluated | 2026-05-13 |
| Target duration | 24894 ms |
| Target cost | $0.1185 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | After bootstrap, `docs/architecture/CLAUDE.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim | PASS | Artifact shows 'USER-EDIT-SENTINEL-DO-NOT-STRIP' on its own line under '## Custom team notes', preserved verbatim. |
| c2 | After bootstrap, `docs/architecture/CLAUDE.md` contains the merge marker `<!-- Added by react-developer bootstrap v0.1.0 -->` — the React conventions section was appended with the correct marker, not silently dropped | PASS | Artifact contains '<!-- Added by react-developer bootstrap v0.1.0 -->' immediately before '## React/Next.js Conventions'. |
| c3 | After bootstrap, `docs/architecture/CLAUDE.md` contains a `## React/Next.js Conventions` heading — the top-level section was appended | PASS | Artifact contains '## React/Next.js Conventions' as a heading after the merge marker. |
| c4 | After bootstrap, `docs/architecture/CLAUDE.md` contains at least two of the subsection headings from the template (`### TypeScript`, `### Styling`, `### Component Patterns`, `### Testing`, `### Project Structure`, `### Deployment`) — proving the template body was appended, not just the heading | PASS | Artifact contains all six subsections: '### TypeScript', '### Styling', '### Component Patterns', '### Testing', '### Project Structure', '### Deployment'. |
| c5 | Chat output includes a manifest summary that names `docs/architecture/CLAUDE.md` and uses append or update language (not "overwrote" or "replaced") | PASS | Chat output: 'docs/architecture/CLAUDE.md — appended React/Next.js Conventions section' and 'React conventions appended while preserving existing custom team notes'. |
| c6 | Output names `docs/architecture/CLAUDE.md` individually in the manifest — a bare "bootstrap complete" without listing the file is not enough | PASS | Manifest lists 'docs/architecture/CLAUDE.md' explicitly under both 'Files updated' and 'Files merged' sections. |
| c7 | Output does not claim it overwrote or replaced `docs/architecture/CLAUDE.md` — the language reflects append/merge, not replacement | PASS | Only 'appended' and 'merged' language used. No 'overwrote' or 'replaced' anywhere in chat output or artifact. |
| c8 | Output points the reader at next steps consistent with the skill's documented manifest (mentions Tailwind, Vitest, or `/react-developer:component-from-spec`) | PARTIAL | Next steps section mentions 'Configure Tailwind CSS', 'Set up Vitest with React Testing Library', and '/react-developer:component-from-spec' — all three skill markers present. |

### Notes

All criteria met cleanly. The safe-merge contract was honoured: user-authored content and sentinel preserved, merge marker applied, full template body appended, and manifest language accurately described append/merge semantics throughout.
