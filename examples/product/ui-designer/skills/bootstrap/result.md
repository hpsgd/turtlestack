# Bootstrap

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/design/CLAUDE.md` containing a user-authored section. The ui-designer bootstrap skill should preserve that user content while appending the template's missing sections (with a merge marker), and should create the file the fixture is missing — `docs/design/design-tokens.md` — copied from the plugin template. The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

> The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/design/CLAUDE.md` is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.
> 
> Read the ui-designer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/product/ui-designer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.
> 
> After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Design Bootstrap Complete

### Files created
- `docs/design/design-tokens.md` — design token template with TestProject values

### Files merged
- `docs/design/CLAUDE.md` — appended design domain sections while preserving user custom notes

### Next steps
- Populate `design-tokens.md` with project-specific token values
- Use `/ui-designer:component-spec` to spec new components
- Run `/ui-designer:accessibility-audit` on existing UI

### Artifacts written

#### `work/docs/design/design-tokens.md`

```
# Design Tokens: TestProject

| Field | Value |
|---|---|
| **System** | TestProject |
| **Version** | 1.0.0 |
| **Last Updated** | 2026-05-13 |

## Colour Primitives

Reference only from semantic tokens, never directly in components.

| Token Name | Hex | Usage Notes |
|---|---|---|
| `color-blue-500` | `#3B82F6` | Primary blue |
| `color-neutral-0` | `#FFFFFF` | White |
| `color-neutral-900` | `#111827` | Near-black |
| `color-red-500` | `#EF4444` | Error red |
| `color-green-500` | `#22C55E` | Success green |
| `color-amber-500` | `#F59E0B` | Warning amber |

## Semantic Colour Tokens

Map primitives to usage. Override per theme.

| Token Name | Light Value | Dark Value | Usage |
|---|---|---|---|
| `color-text-primary` | `neutral-900` | `neutral-50` | Body text, headings |
| `color-text-secondary` | `neutral-600` | `neutral-400` | Supporting text |
| `color-bg-surface` | `neutral-0` | `neutral-900` | Card and panel backgrounds |
| `color-bg-page` | `neutral-50` | `neutral-950` | Page background |
| `color-border-default` | `neutral-200` | `neutral-700` | Default borders |
| `color-interactive-primary` | `blue-500` | `blue-400` | Buttons, links |
| `color-feedback-error` | `red-500` | `red-400` | Error states |
| `color-feedback-success` | `green-500` | `green-400` | Success states |

## Spacing Scale

| Token Name | Value | Usage |
|---|---|---|
| `space-1` | `0.25rem` (4px) | Tight inline spacing |
| `space-2` | `0.5rem` (8px) | Icon-to-label gap |
| `space-4` | `1rem` (16px) | Default padding, stack gap |
| `space-6` | `1.5rem` (24px) | Section padding |
| `space-8` | `2rem` (32px) | Card padding |
| `space-16` | `4rem` (64px) | Page-level spacing |

## Typography Scale

| Token Name | Font Family | Size | Weight | Line-Height | Letter-Spacing | Usage |
|---|---|---|---|---|---|---|
| `type-display` | `system-ui, -apple-system, sans-serif` | `2.25rem` | `700` | `1.2` | `-0.02em` | Hero headings |
| `type-heading-1` | `system-ui, -apple-system, sans-serif` | `1.5rem` | `600` | `1.3` | `-0.01em` | Page titles |
| `type-heading-2` | `system-ui, -apple-system, sans-serif` | `1.25rem` | `600` | `1.3` | `0` | Section headings |
| `type-body` | `system-ui, -apple-system, sans-serif` | `0.875rem` | `400` | `1.5` | `0` | Body text |
| `type-body-small` | `system-ui, -apple-system, sans-serif` | `0.75rem` | `400` | `1.5` | `0` | Captions, help text |
| `type-code` | `Monaco, 'Courier New', monospace` | `0.8125rem` | `400` | `1.6` | `0` | Code blocks |

## Border Radius

| Token Name | Value | Usage |
|---|---|---|
| `radius-sm` | `0.25rem` (4px) | Badges, tags |
| `radius-md` | `0.5rem` (8px) | Buttons, inputs |
| `radius-lg` | `0.75rem` (12px) | Cards, dialogs |
| `radius-full` | `9999px` | Avatars, pills |

## Shadow / Elevation

| Token Name | Value | Usage |
|---|---|---|
| `shadow-sm` | `0 1px 2px rgba(0,0,0,0.05)` | Cards at rest |
| `shadow-md` | `0 4px 6px rgba(0,0,0,0.07)` | Dropdowns, hover |
| `shadow-lg` | `0 10px 15px rgba(0,0,0,0.1)` | Modals, popovers |

## Breakpoints

| Token Name | Min-Width | Usage |
|---|---|---|
| `bp-sm` | `640px` | Large phones |
| `bp-md` | `768px` | Tablets |
| `bp-lg` | `1024px` | Desktops |
| `bp-xl` | `1280px` | Wide screens |

## Motion / Duration

| Token Name | Duration | Easing | Usage |
|---|---|---|---|
| `motion-fast` | `100ms` | `ease-out` | Hover, focus, micro-interactions |
| `motion-normal` | `200ms` | `ease-in-out` | Expand/collapse, fade |
| `motion-slow` | `350ms` | `ease-in-out` | Slide-in panels, modals |
| `motion-reduced` | `0ms` | -- | When `prefers-reduced-motion` is set |

## Usage Rules

1. **Never use primitives directly in components.** Always reference semantic tokens.
2. **Extending**: Add primitives first, then semantic mappings. Get design-system review before merging.
3. **Naming**: `{category}-{property}-{variant}` (e.g., `color-bg-surface`, `space-4`).
4. **Dark mode**: All semantic colour tokens must define both light and dark values.
5. **Accessibility**: All text/background pairings must meet WCAG 2.1 AA (4.5:1 body, 3:1 large text).

```

#### `work/docs/design/CLAUDE.md`

```
# Design Domain

This directory contains design documentation for the project.

## Custom team notes

USER-EDIT-SENTINEL-DO-NOT-STRIP

This section was written by the team and must survive any bootstrap re-run.
It exists to test the safe-merge contract: the bootstrap skill must not
overwrite or remove user-authored content.

<!-- Merged from ui-designer bootstrap v0.1.0 -->

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

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/7.5 (100%) |
| Evaluated | 2026-05-13 |
| Target duration | 48350 ms |
| Target cost | $0.1669 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | After bootstrap, `docs/design/CLAUDE.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim | PASS | Artifact shows `USER-EDIT-SENTINEL-DO-NOT-STRIP` on its own line under `## Custom team notes`, with surrounding user text intact. |
| c2 | After bootstrap, `docs/design/CLAUDE.md` contains the safe-merge marker `<!-- Merged from ui-designer bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged | PASS | Artifact contains `<!-- Merged from ui-designer bootstrap v0.1.0 -->` immediately before the appended template sections. |
| c3 | After bootstrap, `docs/design/CLAUDE.md` contains the appended template sections — at minimum the "Design Token Architecture" and "WCAG 2.2 Accessibility Requirements" headings now appear alongside the preserved user content | PASS | Artifact contains `## Design Token Architecture` and `## WCAG 2.2 Accessibility Requirements` headings, both appearing after the merge marker and user section. |
| c4 | After bootstrap, `docs/design/design-tokens.md` exists and was created from the plugin template (contains `## Colour Primitives` and `## Semantic Colour Tokens` headings) | PASS | Artifact `work/docs/design/design-tokens.md` contains both `## Colour Primitives` and `## Semantic Colour Tokens` headings with full token tables. |
| c5 | Chat output includes a manifest summary that distinguishes files created (`design-tokens.md`) from files merged (`CLAUDE.md`) | PASS | Chat response has separate `### Files created` and `### Files merged` sections, each listing the respective file. |
| c6 | Output names each created and merged file individually — a bare "bootstrap complete" without the per-file manifest is not enough | PASS | `docs/design/design-tokens.md` named under created; `docs/design/CLAUDE.md` named under merged, each with a description. |
| c7 | Output does not claim it overwrote or replaced `docs/design/CLAUDE.md` — the language reflects merge, not replacement | PASS | Output says "appended design domain sections while preserving user custom notes" — no overwrite/replace language anywhere. |
| c8 | Output points the reader at next steps (populating `design-tokens.md`, using `/ui-designer:component-spec`) consistent with the skill's documented manifest | PARTIAL | Next steps list "Populate `design-tokens.md`", "Use `/ui-designer:component-spec`", and "/ui-designer:accessibility-audit" — fully matches the skill manifest. |

### Notes

All eight criteria are met; the skill correctly preserved user content, applied the merge marker, appended template sections, and created the missing file from the template. The manifest summary is well-structured and distinguishes created from merged files.
