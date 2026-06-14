---
name: bootstrap
bootstrap-phase: stack
description: "Bootstrap React/Next.js conventions into the architecture documentation. Writes the react-developer fragment of the architecture domain doc. Idempotent — merges missing sections into existing files without overwriting."
argument-hint: "[project name]"
user-invocable: false
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Bootstrap React/Next.js Conventions

Bootstrap React/Next.js development conventions for **$ARGUMENTS**.

This skill writes only its own fragment — `docs/architecture/_sections/react-developer.md`. The architecture domain `CLAUDE.md` is assembled by the coordinator from every fragment in `_sections/`, so this skill never collides with the architect or the other stack developers.

## Process

### Step 1: Create the sections directory

```bash
mkdir -p docs/architecture/_sections
```

### Step 2: Write the React fragment

`docs/architecture/CLAUDE.md` is **assembled by the coordinator** from the fragments in `_sections/` — no plugin writes it directly, so this skill and the architect never collide on it. Write the React/Next.js contribution as `docs/architecture/_sections/react-developer.md`. It starts at H2 (the coordinator generates the `# Architecture Domain` H1).

Apply the safe merge pattern:

- If the fragment does not exist → create it from the template below
- If the fragment exists → read both, find sections in the template missing from the file, append only the missing sections with the marker `<!-- Added by react-developer bootstrap v0.1.0 -->`

```markdown
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

### Step 3: Return manifest

After creating/merging all files, output a summary:

```
## React Developer Bootstrap Complete

### Files created
- `docs/architecture/_sections/react-developer.md` — react-developer's fragment of the architecture domain doc (assembled into `docs/architecture/CLAUDE.md` by the coordinator)

### Files merged
- (list the fragment here if it already existed and missing sections were appended, or "none")

### Next steps
- Configure Tailwind CSS and `cn()` utility
- Set up Vitest with React Testing Library
- Use `/react-developer:component-from-spec` for new components
- Use `/react-developer:performance-audit` for performance reviews
```

## Rules

- **Write only your own fragment.** `docs/architecture/CLAUDE.md` is assembled by the coordinator; this skill writes `docs/architecture/_sections/react-developer.md` and nothing else. The architect and the other stack developers write their own fragments — there is no shared file to clobber.
- **Safe-merge the fragment, idempotent by design.** If the fragment exists, preserve user-authored content and append only missing template sections with the marker — never overwrite. Running twice produces no duplicate sections.
