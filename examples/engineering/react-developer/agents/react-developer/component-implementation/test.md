---
# Match the model the agent declares (sonnet) in
# plugins/engineering/react-developer/agents/react-developer.md. The runner otherwise
# falls back to the harness default (Haiku), which is not what the
# agent is designed to run on.
target-model: claude-sonnet-4-6
---

# Test: Data table component implementation

Scenario: User asks the React developer to build a reusable data table component with server-side sorting, filtering, and pagination. The app uses Next.js App Router with TypeScript and Tailwind CSS.

## Prompt

I need a `DataTable` component for our Next.js app. It should support:
- Columns defined via a config prop (label, key, sortable flag)
- Server-side sorting (clicking a column header updates URL params and triggers a server refetch)
- A text filter input that debounces and updates a `?q=` URL param
- Pagination controls (previous/next, page number display) using `?page=` URL param
- Loading skeleton that matches the table layout
- Empty state when there are no rows

The table will be used on the `/admin/orders` and `/admin/users` pages, so it needs to be in the shared components. We use Tailwind for styling.

Do not ask for clarification — proceed using the information provided. Use reasonable defaults for anything not specified (e.g. assume App Router, TypeScript strict, clsx for class composition) and state your assumptions.

A few specifics for the response:

- **Recon first**: show `find src/components -name "*.tsx" 2>/dev/null` and `cat CLAUDE.md 2>/dev/null` results (or "no existing components / no CLAUDE.md found, greenfield"). Include a one-line **Decision Checkpoint**: "Checked for existing Table primitive in shadcn/ui, Radix UI — none found in this project; building from scratch." (state explicitly even if synthetic).
- **TDD with exit codes**: write the failing Vitest test FIRST, run `npx vitest run DataTable`, show **exit code 1 (RED)**. Then implementation, run again, show **exit code 0 (GREEN)**. Tests cover at minimum: renders with data, renders empty state, renders skeleton when loading, sort click updates URL.
- **Export ONE `DataTableProps<T>` type** — exported from the component file, used everywhere. No separate inline definition that diverges from the exported one.
- **URL state via `router.replace`** with `scroll: false` — NOT `router.push` (avoid history entries on every sort/filter/page change).
- **Accessibility for sortable headers**: `<th aria-sort="ascending|descending|none">` with `role="button"`, `tabIndex={0}`, AND `onKeyDown` handling Space/Enter to activate sort. Add `aria-label` on `<table>`.
- **Output structure**: end with a `## TDD Evidence` section (RED command + exit 1, GREEN command + exit 0) AND a `## Checklist` section enumerating completed items.

## Criteria

- [ ] PASS: Agent reads CLAUDE.md and scans existing components before writing any code
- [ ] PASS: Agent identifies that sorting, filtering, and pagination state must live in URL search params (not useState)
- [ ] PASS: Agent writes a failing Vitest test first (RED) before implementing the component
- [ ] PASS: Agent defines a typed `DataTableProps` interface with exported type
- [ ] PASS: Agent handles all required states: loading (skeleton), empty, and populated
- [ ] PASS: Agent uses `clsx` for conditional class composition, not string concatenation
- [ ] PASS: Agent flags the decision checkpoint for adding a new shared component (checks UI library for existing primitives)
- [ ] PARTIAL: Agent covers accessibility requirements — keyboard navigation for sortable headers, appropriate ARIA attributes
- [ ] PASS: Output includes TDD Evidence (RED/GREEN commands with exit codes) and a Checklist section

## Output expectations

- [ ] PASS: Output places `DataTable` in the shared components folder (e.g. `components/ui/data-table.tsx` or `components/shared/`), not co-located with `/admin/orders` or `/admin/users`, since the prompt says it's used on both
- [ ] PASS: Output's `DataTableProps` is a typed and exported interface with at least: `columns: ColumnConfig[]`, `data: T[]`, `loading?: boolean`, `total?: number`, with a generic `<T>` type parameter so consumers get typed row data
- [ ] PASS: Output stores sort, filter, and page state in URL search params using `useSearchParams` / `usePathname` from `next/navigation` (App Router) and updates them via `router.replace` with `scroll: false` — NOT in component-local `useState`
- [ ] PASS: Output's text filter uses a debounce (e.g. 300-500ms) before updating the URL `?q=` param, preventing a navigation per keystroke — and the debounce is implemented in the component or via a hook, not via an external library if a hook will do
- [ ] PASS: Output's column header click handler toggles sort direction (asc → desc → unset, or asc ↔ desc) and updates the URL `?sort=` and `?dir=` params — not in-place sorting of the data array
- [ ] PASS: Output renders three distinct UI states — loading skeleton (matches column layout, not generic shimmer), empty state (when data.length === 0 and not loading), populated table — with clear conditional rendering
- [ ] PASS: Output uses `clsx` (or `cn` wrapper) for conditional classNames — never string concatenation like `` `${base} ${active ? 'bg-blue-500' : ''}` ``
- [ ] PASS: Output writes the failing Vitest test first — RED command with exit code 1 shown — then implements, then GREEN with exit code 0; tests cover at minimum: renders with data, renders empty state, renders skeleton when loading, sort click updates URL
- [ ] PASS: Output addresses accessibility — sortable headers use `<th aria-sort>` with `ascending`/`descending`/`none` values, are keyboard-activatable (button or proper role), and the table has appropriate ARIA labels
- [ ] PARTIAL: Output checks the project's existing UI library (shadcn/ui, Material UI, or custom) for an existing Table primitive before building from scratch — flagged as a decision checkpoint
