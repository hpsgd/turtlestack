---
name: bootstrap
bootstrap-phase: product
description: "Bootstrap the design system documentation structure for a project. Creates docs/design/, generates initial templates, and writes the ui-designer fragment of the design domain doc. Idempotent — merges missing sections into existing files without overwriting."
argument-hint: "[project name]"
user-invocable: false
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Bootstrap Design Documentation

Bootstrap the design system documentation structure for **$ARGUMENTS**.

## Process

### Step 1: Check and create domain directory

```bash
mkdir -p docs/design/_sections
```

### Step 2: Create or merge files

For each file below, apply the safe merge pattern:
- If file does not exist → create from template
- If file exists → read both, find sections in template missing from file, append missing sections with `<!-- Merged from ui-designer bootstrap v0.1.0 -->`

#### Fragment: `docs/design/_sections/ui-designer.md`

`docs/design/CLAUDE.md` is **assembled by the coordinator** from the fragments in `_sections/` — no plugin
writes it directly, so the ui-designer and ux-researcher never collide on it. Write the ui-designer's
contribution as this fragment. It starts at H2 (the coordinator generates the `# Design Domain` H1):

```markdown
## What This Domain Covers

- **Design tokens** — primitives, semantic tokens, and theme architecture
- **Component specifications** — anatomy, states, variants, and accessibility
- **Accessibility audits** — WCAG 2.2 conformance assessments
- **Design reviews** — structured feedback on UI implementations

## Design Token Architecture

Design tokens follow a two-tier model:

| Layer | Purpose | Example |
|-------|---------|---------|
| **Primitives** | Raw values — colours, sizes, durations | `color-blue-500`, `space-4` |
| **Semantic** | Usage-mapped tokens referencing primitives | `color-text-primary`, `color-bg-surface` |

### Rules
- **Never reference primitives directly in components** — always go through semantic tokens
- All semantic colour tokens must define both light and dark values
- New primitives require design-system review before merge
- Naming convention: `{category}-{property}-{variant}` (e.g., `color-bg-surface`, `space-4`)

## Component Spec Process

Every new or significantly changed component follows this process:

1. **Spec** — write component specification (anatomy, states, variants, accessibility)
2. **Review** — design review with at least one designer
3. **Implement** — build against the spec
4. **Verify** — accessibility audit and visual regression check

### Component spec structure
- **Anatomy** — labelled diagram of sub-elements
- **States** — default, hover, focus, active, disabled, error, loading
- **Variants** — size, colour, layout variations
- **Responsive behaviour** — how the component adapts across breakpoints
- **Accessibility** — keyboard interaction, ARIA roles, screen reader behaviour

## WCAG 2.2 Accessibility Requirements

Target **WCAG 2.2 Level AA** conformance as the minimum standard.

### Key requirements
| Criterion | Requirement |
|-----------|-------------|
| Colour contrast | 4.5:1 for body text, 3:1 for large text (>= 18px bold / 24px) |
| Focus indicators | Visible focus ring on all interactive elements (minimum 2px, 3:1 contrast) |
| Target size | Minimum 24x24px for touch targets (Level AA) |
| Motion | Respect `prefers-reduced-motion` — disable non-essential animation |
| Keyboard | All functionality accessible via keyboard alone |
| Screen reader | Meaningful alt text, ARIA labels, logical heading hierarchy |

### Testing
- Automated: axe-core in CI (catches ~30% of issues)
- Manual: keyboard-only navigation, screen reader testing (VoiceOver / NVDA)
- Visual: colour contrast checker for all text/background pairings

## Tooling

| Tool | Purpose |
|------|---------|
| GitHub Pull Requests | Design review on UI changes |
| Figma | Design source of truth (if applicable) |
| axe-core | Automated accessibility testing in CI |

## Available Skills

| Skill | Purpose |
|-------|---------|
| `/ui-designer:component-spec` | Write a component specification |
| `/ui-designer:accessibility-audit` | Conduct a WCAG 2.2 accessibility audit |
| `/ui-designer:design-review` | Perform a structured design review |
| `/ui-designer:design-tokens` | Define or update design tokens |

## Conventions

- Design tokens are the single source of truth for visual values — no magic numbers in code
- Every UI component must have a written spec before implementation
- Accessibility is not optional — all components must pass WCAG 2.2 AA
- Design reviews are required for all PRs that change user-facing UI
- Dark mode support is mandatory — all semantic tokens define both light and dark values
- Use `docs/design/` for design system documentation and templates
```

#### File 2: `docs/design/design-tokens.md`

Copy from the plugin template at `plugins/product/ui-designer/templates/design-tokens.md`.

If the file already exists, do not overwrite — leave it as-is.

### Step 3: Return manifest

After creating/merging all files, output a summary:

```
## Design Bootstrap Complete

### Files created
- `docs/design/_sections/ui-designer.md` — ui-designer's fragment of the design domain doc (assembled into `docs/design/CLAUDE.md` by the coordinator)
- `docs/design/design-tokens.md` — design token template

### Files merged
- (list any existing files where sections were appended)

### Next steps
- Populate `design-tokens.md` with project-specific token values
- Use `/ui-designer:component-spec` to spec new components
- Run `/ui-designer:accessibility-audit` on existing UI
```
