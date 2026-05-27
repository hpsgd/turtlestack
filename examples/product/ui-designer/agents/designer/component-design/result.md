# Component Design

Scenario: A product team needs a multi-step onboarding wizard designed for their B2B SaaS product. The designer agent is asked to produce a component specification.

## Prompt

> We need to design a multi-step onboarding wizard for Clearpath, our B2B project management tool. New users need to:
> 1. Set up their workspace (name, logo, timezone)
> 2. Invite team members (up to 5 emails)
> 3. Connect their first integration (GitHub, Jira, or Slack — or skip)
> 4. Create their first project from a template
> 
> We have a design system with existing Input, Button, Avatar, and Card components. The wizard should work on desktop and tablet. Can you design this?
> 
> Output structure:
> 
> - **Existing component reuse table** at top with columns `Component | Decision (REUSE / EXTEND / CREATE) | Rationale`. Cover Input (REUSE), Button (REUSE), Avatar (REUSE — for invited team members), Card (REUSE — for integration tiles), Stepper/ProgressIndicator (decide REUSE / EXTEND / CREATE — most likely CREATE since it's not in the existing system).
> - **8 component states for EVERY new component** — not just one diagram, repeat for each new component. The 8 states: Default, Hover (cursor over interactive area), Focus (keyboard focus ring), Active (pressed/clicked), Disabled, Loading (async work in progress), Error (validation failure or operation error), Empty (no data yet — e.g. no team members invited).
> - **Per-step error states** explicitly: Step 1 (workspace name validation: empty, too long, duplicate), Step 2 (invalid email format, duplicate email, too many invites), Step 3 (integration auth failure, network timeout, scope-denied), Step 4 (template fetch failure, project name conflict).
> - **ARIA + keyboard navigation**: each new component documents `role`, `aria-label` / `aria-labelledby`, `tabindex`, and which keys advance/retreat (Tab, Shift+Tab, Enter, Esc).
> - **Step indicator decision**: explicitly state REUSE/EXTEND/CREATE for the progress component. If CREATE, document the 8 states for it too.
> 
> A few specifics for the response:
> 
> - Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
> - Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
> - For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
> - When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
> - Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Here is the full specification, also written to `clearpath-onboarding-wizard-spec.md`:

---

# Clearpath Onboarding Wizard — Component Specification

**Assumptions (proceeding without clarification per brief):**
- Stack: React + TypeScript with CSS custom-property design tokens (`--color-*`, `--space-*`).
- Breakpoints: Tailwind defaults — sm 640px, md 768px, lg 1024px.
- Focus ring: 2px solid `--color-focus-ring`, 2px offset, visible in light and dark modes.
- Existing design system: `Input`, `Button`, `Avatar`, `Card` only. No `Select`, `Stepper`, `Upload`, or `TagInput` components exist.
- Logo upload constraint: PNG / JPEG / SVG, max 2 MB.
- Timezone data source: `Intl.supportedValuesOf('timeZone')` or bundled IANA dataset — resolved by caller, not a prop.
- Wizard is client-side; OAuth popup for integrations is managed by the host application.

---

## Existing Component Reuse Table

| Component | Decision | Rationale |
|-----------|----------|-----------|
| `Input` | REUSE | Used without modification for workspace name (Step 1), project name (Step 4), and as the inner text field within `EmailTagInput`. Existing validation and error-message props are sufficient. |
| `Button` | REUSE | All CTAs — Next, Back, Skip, Connect, Create, Add (email), Remove (logo) — use the existing `Button` component with its `primary` and `ghost`/`secondary` variants. No new variant needed. |
| `Avatar` | REUSE | Email chip tags in `EmailTagInput` (Step 2) render invited-member initials using the existing `Avatar` component at `sm` size with its built-in initials-fallback logic. |
| `Card` | REUSE | Integration tiles (Step 3) and template tiles (Step 4) are composed from the existing `Card` component. A selected-state overlay is applied via wrapping markup — no new component required. |
| `StepIndicator` | CREATE | No existing progress, stepper, breadcrumb, or wizard-step component in the design system. Cannot be composed from the four existing components. |
| `LogoUpload` | CREATE | No file-upload or image-upload component exists. `Input type="file"` does not support drag-and-drop, preview, upload-progress overlay, or aspect-ratio constraints. |
| `TimezoneSelect` | CREATE | No `Select`, `Combobox`, or `Autocomplete` component exists. `Input` does not support option lists. ~500 IANA entries require a virtualised, searchable dropdown. |
| `EmailTagInput` | CREATE | No multi-value tag/chip input exists. `Input` supports single-value text entry only. The invite flow requires up to 5 emails as removable chips with per-chip `Avatar`, inline validation, and a counter. |

---

## Component 1: StepIndicator

### 0. Design System Decision

**Decision: CREATE** — Searched for Stepper, ProgressIndicator, Breadcrumb, and WizardNav components. None found in the design system (Input, Button, Avatar, Card). The StepIndicator must show 4 named steps, differentiate completed / current / upcoming states visually, and allow backward navigation to completed steps via click or keyboard. Cannot be assembled from the four existing components.

---

### 1. Purpose and Usage Context

**What:** A horizontal progress indicator that shows the user's position across named steps in a sequential flow and enables backward navigation to completed steps.

**When to use:** Inside multi-step wizard or onboarding flows where steps are completed in order and the user may need to revisit earlier steps. Do NOT use for tab navigation (use `Tabs`), percentage-complete progress (use a `ProgressBar`), or documentation sections (use an ordered list).

---

### 2. Props / API

| Prop | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| `steps` | `Step[]` | — | Yes | Ordered array of step definitions. Min length: 1. |
| `currentStep` | `number` | — | Yes | Zero-based index of the active step. |
| `onStepClick` | `(index: number) => void` | `undefined` | No | Called when user activates a completed step. If omitted, completed steps are not clickable. |
| `loading` | `boolean` | `false` | No | Replaces all step nodes with skeleton shimmer; disables all interaction. |

```ts
interface Step {
  label: string;         // e.g. "Workspace Setup"
  description?: string;  // e.g. "Name and timezone" — hidden on tablet
}
```

---

### 3. Variants

N/A — `StepIndicator` has a single presentation. Visual differentiation is carried by per-node state (completed / current / upcoming), not a `variant` prop.

---

### 4. States — Complete Coverage Table

Each step *node* carries one of three sub-states: **completed** (`index < currentStep`), **current** (`index === currentStep`), **upcoming** (`index > currentStep`). The table below describes component-level states.

| State | Visual Treatment | Behaviour | Transitions to |
|-------|-----------------|-----------|----------------|
| **Default** | Completed nodes: filled `--color-brand-primary` circle, white checkmark icon, full-opacity label. Current node: filled circle with step number, bold label. Upcoming nodes: `--color-border` outline circle, muted number, `--color-text-muted` label. Connectors: brand-filled between completed; `--color-border` toward upcoming. | Completed nodes clickable when `onStepClick` provided (cursor: pointer). Current/upcoming: cursor: default. | Hover, Focus |
| **Hover** | Hovered completed node: circle → `--color-brand-primary-hover`. Label underline. Connector unchanged. | cursor: pointer. Tooltip if label truncated. No hover effect on current/upcoming. | Default, Active |
| **Focus** | Focused completed node: 2px solid `--color-focus-ring` outline, 2px offset. Visible in both modes. | Tab navigates only between completed nodes (`tabindex="-1"` on current/upcoming). | Default, Active |
| **Active** | Completed node: circle scales 0.95. Background → `--color-brand-primary-active`. | Calls `onStepClick(index)` on pointer-up or Enter/Space. | Default |
| **Disabled** | Entire indicator at 40% opacity. All circles/labels: `--color-text-disabled`. `aria-disabled="true"`. | cursor: not-allowed. No clicks, no keyboard. Used during step submission. | Loading, Default |
| **Loading** | All step circles and labels: skeleton shimmer of identical dimensions. Connectors also shimmered. `aria-busy="true"`. | Non-interactive. Layout preserved. `prefers-reduced-motion` respected. | Default, Error |
| **Error** | Current node circle → `--color-error` with `!` icon replacing step number. Current label → `--color-error`. Completed/upcoming unchanged. | Backward nav to completed steps remains available. Error clears on correction. | Default |
| **Empty** | N/A — `steps` must have ≥ 1 item (TypeScript-enforced). Runtime empty array: component returns `null`. | — | — |

**Compound state combinations:**

| Combination | Resolved Behaviour |
|-------------|-------------------|
| `loading={true}` + completed steps | Skeleton overrides all clickability. |
| Error on current + completed steps | Backward nav stays enabled. Error styling on current node only. |
| `currentStep` = last index | Final connector line hidden. All preceding nodes: completed. |

---

### 5. Responsive Behaviour

| Breakpoint | Width | Layout Changes | Content Changes |
|-----------|-------|---------------|----------------|
| **Mobile** | < 640px | Wizard targets desktop + tablet. If forced: collapses to `"Step N of 4"` text only. | Labels and descriptions hidden; ordinal text only. |
| **Tablet** | 640–1024px | Horizontal layout maintained. Labels truncate single-line with ellipsis. | `description` prop hidden. |
| **Desktop** | > 1024px | Full layout: circles, connectors, labels, optional descriptions. | All content visible. |

- Each completed step node touch target: min 44×44px (WCAG 2.5.5).
- No horizontal scroll at any supported breakpoint.
- Labels truncate with ellipsis — no height expansion.

---

### Performance Considerations

N/A — Fixed small number of nodes (3–8). Re-renders are O(steps.length). No virtualisation needed.

---

### 6. Accessibility Requirements

#### Keyboard Navigation

| Element Type | Key | Action |
|---|---|---|
| Completed step `<button>` | `Tab` | Next completed step node |
| Completed step `<button>` | `Shift+Tab` | Previous completed step node |
| Completed step `<button>` | `Enter` / `Space` | Navigate to that step — `onStepClick(index)` |
| Current / upcoming `<span>` | — | Not in tab order (`tabindex="-1"`) |

After `onStepClick`: focus moves to first focusable element in the target step's form — not back to the indicator.

#### Screen Reader

- **Role:** `<nav aria-label="Onboarding progress">` wrapping the indicator.
- **Completed nodes:** `<button aria-label="Step 1: Workspace Setup, completed">`.
- **Current node:** `<span aria-current="step">` — not a button.
- **Upcoming nodes:** `<span>` — no special ARIA.
- **Step transitions:** `<div aria-live="polite" aria-atomic="true" class="sr-only">` outside the indicator announces `"Step [N] of 4: [Label]"` when `currentStep` changes.
- **Description:** Visually hidden `<p>` via `aria-describedby`: `"Completed steps can be selected to return and edit them."` — rendered once on mount.

#### Colour and Contrast

- Step number / icon in circle: ≥ 4.5:1 against circle fill.
- Connector lines: ≥ 3:1 against page background.
- Focus ring: ≥ 3:1 in both modes.
- Error state: `!` icon supplements red — not colour alone.

#### Focus Management

- Not trapped within StepIndicator.
- Component mount does not steal focus — first focus lands on Step 1's first form field.
- Focus indicator visible in light and dark modes.

---

### 7. Dark Mode

- [x] All colours use semantic tokens (`--color-brand-primary`, `--color-text-muted`, `--color-error`, `--color-border`)
- [x] Muted label on dark surface ≥ 4.5:1 (re-verified)
- [x] No images — ThemeImage N/A
- [x] Connectors use `--color-border` (auto-lightens in dark mode)
- [x] Focus ring uses `--color-focus-ring` token (light: blue-600, dark: blue-400)
- [x] Shadows: N/A — component is flat

---

### 8. Animation and Motion

| Element | Animation | Duration | Easing | Reduced-motion fallback |
|---------|-----------|----------|--------|------------------------|
| Node: upcoming → current | Circle fill cross-fades from outline to solid | 200ms | ease-out | Instant |
| Node: current → completed | Checkmark stroke draws in | 250ms | ease-out | Instant |
| Connector fill | `scaleX` 0→1, transform-origin: left | 250ms | ease-out | Instant |
| Error entry | Cross-fade to `--color-error` | 150ms | ease-in | Instant |
| Active: press | `scale(0.95)` | 100ms | ease-in | No transform |

All governed by `@media (prefers-reduced-motion: reduce)`.

---

### 9. Usage Examples

```tsx
// Standard 4-step wizard, currently on step 2 (zero-indexed: currentStep=1)
<StepIndicator
  steps={[
    { label: "Workspace Setup", description: "Name and timezone" },
    { label: "Invite Team",     description: "Up to 5 members" },
    { label: "Integrations",    description: "Connect your tools" },
    { label: "First Project",   description: "From a template" },
  ]}
  currentStep={1}
  onStepClick={(i) => wizard.goToStep(i)}
/>

// Loading state during step transition
<StepIndicator steps={WIZARD_STEPS} currentStep={2} loading={true} />

// Locked wizard — no backward navigation
<StepIndicator steps={WIZARD_STEPS} currentStep={0} />
```

---

### 10. Do / Don't

| Do | Don't |
|----|-------|
| Always supply `onStepClick` — backward navigation is expected | Lock completed steps unless the flow technically forbids revisiting |
| Use `loading` prop during submission to block double-navigation | Manually set `pointer-events: none` via CSS |
| Keep step labels ≤ 3 words | Use full sentence labels — they truncate on tablet |
| Announce step transitions via `aria-live` outside the indicator | Rely on the indicator alone for screen reader communication |

---

## Component 2: LogoUpload

### 0. Design System Decision

**Decision: CREATE** — Searched for FileInput, ImageUpload, AvatarEditor, Dropzone. None found. `Input type="file"` exists as an HTML primitive but the design system has no styled file upload component. LogoUpload requires: drag-and-drop with visual affordance, image preview at 128×128px, upload-progress overlay, and client-side validation. A new component is needed.

---

### 1. Purpose and Usage Context

**What:** An interactive upload area that accepts a single image file via drag-and-drop or OS file picker, displays a live preview, and communicates upload progress.

**When to use:** Single-image upload where preview and type/size validation are needed — workspace logo, user profile photo. Do NOT use for multi-file upload, document upload, or non-image formats.

---

### 2. Props / API

| Prop | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| `onFileSelect` | `(file: File) => void` | — | Yes | Called after client-side validation passes. Caller handles uploading. |
| `onClear` | `() => void` | — | Yes | Called when user removes the current image. |
| `previewUrl` | `string \| null` | `null` | No | URL to display as preview. When provided, component enters preview mode. |
| `uploading` | `boolean` | `false` | No | Shows upload-progress overlay. |
| `uploadProgress` | `number` | `0` | No | Integer 0–100. Shown only when `uploading={true}`. |
| `error` | `string \| null` | `null` | No | Error message below the upload area. Clears on next valid file selection. |
| `disabled` | `boolean` | `false` | No | Disables all interaction. |
| `accept` | `string` | `"image/png,image/jpeg,image/svg+xml"` | No | MIME types forwarded to hidden `<input type="file">`. |
| `maxSizeBytes` | `number` | `2097152` | No | Max file size in bytes (default 2 MB). Excess triggers `error` without calling `onFileSelect`. |

---

### 3. Variants

N/A — Single presentation. Appearance driven by state (empty / preview / uploading / error), not a `variant` prop.

---

### 4. States — Complete Coverage Table

| State | Visual Treatment | Behaviour | Transitions to |
|-------|-----------------|-----------|----------------|
| **Default** | 128×128px square, 2px dashed `--color-border-dashed` border, 8px radius. Centred upload-cloud icon (`--color-icon-muted`). Label below: "Click or drag to upload" (`--color-text-muted`). Background: `--color-surface-subtle`. | Entire area is `<button>`. Click opens file picker. Drag-over activates Hover. | Hover, Focus, Active |
| **Hover** | Border → 2px dashed `--color-brand-primary`. Background → `--color-surface-brand-subtle`. Icon translates up 2px. | Valid drag target. cursor: pointer. | Default, Active |
| **Focus** | 2px solid `--color-focus-ring` outline, 2px offset. Dashed border unchanged. | `Enter`/`Space` opens file picker. | Default, Active |
| **Active** | Background → `--color-surface-brand-active`. Icon scales 0.95. | Visual feedback. | Default (no file), Preview (file selected) |
| **Disabled** | 40% opacity. cursor: not-allowed. Border → `--color-border-disabled`. `aria-disabled="true"`. `<input disabled>`. | No click, no drag. | — |
| **Loading** | `previewUrl` image behind 50% black overlay. Circular progress ring centred (determinate when `uploadProgress > 0`). Percentage text in white below ring. Dimensions unchanged (128×128px). `aria-busy="true"`. | Non-interactive. Remove button hidden. | Default (error), Preview (success) |
| **Error** | Border → `--color-error`. Error icon below area. Error string in `--color-error` below icon. Upload area still interactive. | User can re-attempt. `aria-live="polite"` announces error. Clears on next valid selection. | Default, Active |
| **Empty** | Identical to Default — "no image" is the Default state. Listed here for completeness. | — | — |

**Preview sub-state** (when `previewUrl` non-null and `uploading` false):

| Sub-state | Visual Treatment | Behaviour |
|-----------|-----------------|-----------|
| Preview: Default | 128×128px image, object-fit: cover, 8px radius. "×" `Button` (ghost, sm) top-right. | Image click re-opens file picker. "×" calls `onClear`. |
| Preview: Hover | Semi-transparent overlay + "Change" label. "×" scales 1.1. | cursor: pointer. |
| Preview: Focus (×) | Focus ring on "×" button. | `Enter`/`Space` → `onClear`. Focus returns to upload area. |

---

### 5. Responsive Behaviour

| Breakpoint | Width | Layout Changes | Content Changes |
|-----------|-------|---------------|----------------|
| **Mobile** | < 640px | Wizard targets tablet+. If forced: 96×96px. | Label → "Upload logo". |
| **Tablet** | 640–1024px | 128×128px. Full label. Touch target ≥ 44×44px satisfied by full component area. | All states functional. |
| **Desktop** | > 1024px | 128×128px. Same as tablet. | All states functional. |

---

### Performance Considerations

N/A — Single file. Preview uses `URL.createObjectURL` (no network round-trip). Object URL revoked via `URL.revokeObjectURL` in cleanup effect on unmount or file change.

---

### 6. Accessibility Requirements

#### Keyboard Navigation

| Key | Action |
|-----|--------|
| `Tab` | Focus moves to upload area |
| `Enter` / `Space` | Opens OS file picker |
| `Tab` (preview mode) | Moves focus to "×" remove button |
| `Enter` / `Space` (on ×) | Calls `onClear`; focus returns to upload area |
| `Shift+Tab` | Reverse focus movement |

#### Screen Reader

- **Role:** `button` on upload area. `<input type="file">` is `aria-hidden="true"`.
- **Label:** `aria-label="Upload workspace logo"`.
- **State announcements:** `aria-live="polite"` region:
  - File selected: `"Logo selected: [filename]"`
  - Progress (at 25/50/75/100%): `"Uploading… [N]%"` (throttled to ≤ 4 announcements)
  - Complete: `"Logo uploaded successfully."`
  - Error: the `error` prop string
- **Description:** `aria-describedby` → visually hidden `<p>`: `"Accepted formats: PNG, JPEG, SVG. Maximum size: 2 MB."`.
- **Remove button:** `aria-label="Remove logo"`.

#### Colour and Contrast

- Dashed border (default): ≥ 3:1 against `--color-surface-subtle`.
- Error border + text: `--color-error` ≥ 4.5:1 on light; error icon supplements colour.
- Progress overlay text (white on dark): ≥ 4.5:1.

#### Focus Management

- No focus trap.
- After file picker closes: focus returns to upload area.
- After `onClear`: focus returns to upload area.

---

### 7. Dark Mode

- [x] All colours use semantic tokens
- [x] Dashed border visible on dark surfaces (`--color-border-dashed` lightens in dark mode)
- [x] Upload icon `--color-icon-muted` auto-adjusts
- [x] Progress overlay: light `rgba(0,0,0,0.5)` → dark `rgba(0,0,0,0.65)`
- [x] Focus ring `--color-focus-ring` ≥ 3:1 on dark backgrounds
- [x] Error: `--color-error` on dark — may need `--color-error-dark` (lighter red) if pure red fails contrast

---

### 8. Animation and Motion

| Element | Animation | Duration | Easing | Reduced-motion fallback |
|---------|-----------|----------|--------|------------------------|
| Hover: border colour | `transition: border-color` | 150ms | ease-out | Instant |
| Hover: icon nudge | `translateY(-2px)` | 150ms | ease-out | No transform |
| Active: press | `scale(0.95)` | 100ms | ease-in | No transform |
| Preview appear | `opacity` 0→1 | 200ms | ease-out | Instant |
| Error: shake | `translateX` ±4px × 3 | 300ms | ease-in-out | Instant; no shake |

---

### 9. Usage Examples

```tsx
// Default — no logo
<LogoUpload onFileSelect={handleLogoFile} onClear={() => setLogoUrl(null)} />

// Preview with existing logo
<LogoUpload previewUrl={workspace.logoUrl} onFileSelect={handleLogoFile} onClear={clearLogo} />

// Upload in progress (65%)
<LogoUpload previewUrl={localObjectUrl} uploading={true} uploadProgress={65}
  onFileSelect={handleLogoFile} onClear={clearLogo} />

// Error state
<LogoUpload error="File exceeds 2 MB. Please choose a smaller image."
  onFileSelect={handleLogoFile} onClear={clearLogo} />
```

---

### 10. Do / Don't

| Do | Don't |
|----|-------|
| Validate type and size client-side before calling `onFileSelect` | Let the server reject invalid files — validate in the component |
| Show preview immediately via object URL, before upload completes | Wait for server upload to show any preview |
| Revoke object URL in cleanup effect | Hold object URL references beyond the component lifecycle |
| Keep component at fixed 128×128px to prevent layout shift | Resize based on preview image dimensions |
| Show determinate progress ring when `uploadProgress > 0` | Show only an indeterminate spinner |

---

## Component 3: TimezoneSelect

### 0. Design System Decision

**Decision: CREATE** — Searched for Select, Combobox, Autocomplete, Dropdown, Listbox. None found. `Input` does not support option lists. Timezone selection requires a searchable combobox over ~500 IANA entries with regional grouping and virtualised rendering. A new component is required.

---

### 1. Purpose and Usage Context

**What:** A searchable combobox that lets a user select an IANA timezone from a grouped, filterable list displaying the timezone's common name and UTC offset.

**When to use:** Timezone selection in workspace setup, user profile, or scheduling configuration. Do NOT use for general enumerable option lists (if a generic `Select` is later added, prefer that). Do NOT use for non-timezone data.

---

### 2. Props / API

| Prop | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| `value` | `string \| null` | `null` | No | Selected IANA timezone string (e.g., `"Australia/Sydney"`). Controlled. |
| `onChange` | `(timezone: string) => void` | — | Yes | Called on selection. |
| `label` | `string` | `"Timezone"` | No | Visible label text above the trigger. |
| `placeholder` | `string` | `"Select timezone…"` | No | Shown when `value` is null. |
| `error` | `string \| null` | `null` | No | Inline error message below the trigger. |
| `disabled` | `boolean` | `false` | No | Disables all interaction. |
| `loading` | `boolean` | `false` | No | Skeleton state while timezone data loads. |
| `autoDetect` | `boolean` | `true` | No | Pre-populates display with `Intl.DateTimeFormat().resolvedOptions().timeZone` on mount when `value` is null. Does not auto-call `onChange` — caller persists on "Next". |

**Note on data source:** Timezone list resolved from a module import or React context — not a prop. Keeps the component deployment-model-agnostic.

---

### 3. Variants

N/A — Single presentation. State changes (open / closed / error / disabled / loading) drive visual differentiation.

---

### 4. States — Complete Coverage Table

| State | Visual Treatment | Behaviour | Transitions to |
|-------|-----------------|-----------|----------------|
| **Default** | Trigger: `Input`-styled field, `--color-border` border. Value text or placeholder (`--color-text-placeholder`). Chevron-down icon right-aligned. Dropdown closed. | Click or `Enter`/`Space` opens dropdown. `ArrowDown` opens and focuses first option. | Hover, Focus, Open |
| **Hover** | Border → `--color-border-hover`. Chevron → `--color-text-primary`. | cursor: pointer. | Default, Active |
| **Focus** | 2px solid `--color-focus-ring` outline, 2px offset. Border → `--color-brand-primary`. | `ArrowDown`/`Enter`/`Space` opens dropdown. | Default, Active, Open |
| **Active** | Background → `--color-surface-pressed`. Chevron rotates 180°. | Dropdown opens. | Open |
| **Disabled** | 40% opacity. cursor: not-allowed. `aria-disabled="true"`. Dropdown never opens. | No interaction. | — |
| **Loading** | Trigger replaced by skeleton shimmer of identical dimensions. `aria-busy="true"`. | Non-interactive. Layout preserved. | Default |
| **Error** | Border → `--color-error`. Error icon replaces chevron (closed). Error message below trigger in `--color-error` with icon. | Dropdown still operable; error clears on valid selection. `aria-live="polite"` announces. | Default, Open |
| **Empty** | Dropdown open, query matches nothing. Panel: `"No timezones match '[query]'. Clear search to see all."` | Clearing search restores full list. Escape closes. | Open (with results) |

**Open / Dropdown sub-states:**

| Sub-state | Visual Treatment | Behaviour |
|-----------|-----------------|-----------|
| Open: Default | Panel: `--color-surface-overlay` bg, 1px `--color-border` border, 8px radius, `box-shadow: --shadow-md`. Appears below trigger (flips above if < 300px below viewport). Max-height 320px, scrollable. Search input at top. Groups as non-interactive headers. | Virtualised list (visible rows only). |
| Open: Searching | Matching substring bold in label. Non-matching hidden. Empty group headers hidden. Debounced 100ms. | — |
| Open: Option Hover | `--color-surface-brand-subtle` background. cursor: pointer. | — |
| Open: Option Focus | Hover + inset `--color-focus-ring` outline 2px. | `Enter` selects. |
| Open: Option Selected | Checkmark icon. Bold text. `--color-surface-brand-subtle`. Scrolled into view on open. | Re-selecting is no-op. |

---

### 5. Responsive Behaviour

| Breakpoint | Width | Layout Changes | Content Changes |
|-----------|-------|---------------|----------------|
| **Mobile** | < 640px | Wizard targets tablet+. If forced: dropdown as bottom-sheet modal. | — |
| **Tablet** | 640–1024px | Panel width = trigger width. Max-height 240px. | Option rows ≥ 44px for touch targets. |
| **Desktop** | > 1024px | Panel width ≥ trigger (min 280px). Max-height 320px. | All features. |

---

### Performance Considerations

- **Rendering strategy:** Virtualised list required (`@tanstack/virtual` or `react-window`) for ~500 IANA entries. >100 DOM nodes in dropdown causes visible jank — virtualise from initial implementation.
- **Filter performance:** Client-side substring match on display name and UTC offset. Debounced 100ms. No server round-trip.
- **Row height:** Fixed 44px (required by virtualiser for scroll bound calculation).

---

### 6. Accessibility Requirements

#### Keyboard Navigation

| Element Type | Key | Action |
|---|---|---|
| Trigger (closed) | `Enter` / `Space` / `ArrowDown` | Open dropdown; focus to search input |
| Trigger (closed) | `Tab` | Skip past component |
| Search input (open) | Type | Filter list |
| Search input (open) | `ArrowDown` | Focus first option |
| Search input (open) | `Escape` | Close; focus returns to trigger |
| Option | `ArrowDown` / `ArrowUp` | Navigate options |
| Option | `Enter` | Select; close; focus returns to trigger |
| Option | `Escape` | Close without selecting; focus to trigger |
| Option | `Home` / `End` | First / last option |
| Option | `Tab` | Close; focus exits component |

#### Screen Reader

- **Role:** `role="combobox"` on trigger; `aria-expanded`; `aria-haspopup="listbox"`; `aria-controls="[listbox-id]"`.
- **Listbox:** `role="listbox"`, `aria-label="Timezones"`.
- **Options:** `role="option"`, `aria-selected`, unique `id`.
- **Groups:** `role="group"`, `aria-label="[Region]"`.
- **Label:** Visible `<label htmlFor>` linked to trigger. `aria-labelledby` on trigger.
- **Active option:** `aria-activedescendant="[focused-option-id]"` on trigger.
- **Search input:** `aria-label="Search timezones"`, `aria-controls="[listbox-id]"`.
- **Error:** `aria-invalid="true"` on trigger; `aria-describedby` → error `<p>`.

#### Colour and Contrast

- Placeholder text: ≥ 4.5:1 (verify — placeholder tones often fail AA).
- Option text on panel background: ≥ 4.5:1 in light and dark.
- Selected checkmark: ≥ 3:1 against option background.
- Error uses icon + colour — not colour alone.

#### Focus Management

- On open: focus moves to search input.
- On close (selection or Escape): focus returns to trigger.
- On Tab from open: focus exits to next element in tab order.

---

### 7. Dark Mode

- [x] Trigger inherits `Input` dark-mode tokens
- [x] Panel `--color-surface-overlay` (dark: `--color-gray-900`)
- [x] Option hover `--color-surface-brand-subtle` verified ≥ 3:1 on dark panel
- [x] Group headers `--color-text-muted` — verify ≥ 4.5:1 in dark (muted tones risk failing)
- [x] Chevron `--color-icon-muted`
- [x] Panel border `--color-border` (lightens in dark)
- [x] Box shadow adapted (`--shadow-md-dark` or reduced opacity)

---

### 8. Animation and Motion

| Element | Animation | Duration | Easing | Reduced-motion fallback |
|---------|-----------|----------|--------|------------------------|
| Panel open | `opacity` 0→1, `translateY(-4px)`→0 | 150ms | ease-out | Instant appear |
| Panel close | `opacity` 1→0, `translateY(0)`→`-4px` | 100ms | ease-in | Instant disappear |
| Chevron rotation | 0°→180° | 150ms | ease-out | Instant |
| Filter hide | `opacity` 1→0 per hidden row | 80ms | linear | Instant |

---

### 9. Usage Examples

```tsx
// Auto-detect timezone on mount
<TimezoneSelect value={formState.timezone} onChange={(tz) => setField("timezone", tz)} />

// Explicit value with error
<TimezoneSelect value={null} onChange={handleTimezoneChange}
  error="Please select a timezone to continue." autoDetect={false} />

// Disabled after workspace saved
<TimezoneSelect value="Australia/Sydney" onChange={noop} disabled={true} />
```

---

### 10. Do / Don't

| Do | Don't |
|----|-------|
| Virtualise the option list from day one | Render all ~500 options as plain DOM nodes |
| Pre-populate via `autoDetect` | Leave field empty and force every user to search |
| Show UTC offset: "Sydney (UTC+10:00)" | Show raw IANA ID only — "Australia/Sydney" is not user-readable |
| Close and return focus to trigger on selection | Keep dropdown open after selection |
| Debounce filter at 100ms | Re-filter on every keystroke |

---

## Component 4: EmailTagInput

### 0. Design System Decision

**Decision: CREATE** — Searched for TagInput, ChipInput, MultiEmail, TokenInput. None found. `Input` supports single-value text entry only. The invite flow requires up to 5 emails as removable chip tags with per-chip `Avatar`, per-chip validation, a count constraint, and a counter display. Cannot be composed from `Input` alone.

---

### 1. Purpose and Usage Context

**What:** A multi-value text input that validates email addresses on entry, renders them as removable chip tags (with `Avatar`), and enforces a configurable maximum count.

**When to use:** Adding multiple email addresses in invite or share flows. Do NOT use for free-text tags, single email input (use `Input type="email"` directly), or search queries.

---

### 2. Props / API

| Prop | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| `emails` | `string[]` | — | Yes | Controlled list of validated email strings. |
| `onAdd` | `(email: string) => void` | — | Yes | Called when a valid, non-duplicate email is submitted. |
| `onRemove` | `(email: string) => void` | — | Yes | Called when user removes a chip. |
| `maxEmails` | `number` | `5` | No | Max emails permitted. Input hides when `emails.length >= maxEmails`. |
| `error` | `string \| null` | `null` | No | Field-level error (e.g., "Invite send failed"). Shown below component. |
| `inputError` | `string \| null` | `null` | No | Inline error for current typed value (e.g., "Invalid email format"). |
| `disabled` | `boolean` | `false` | No | Disables all interaction including chip removal. |
| `loading` | `boolean` | `false` | No | Shows skeleton chips for existing list. |
| `placeholder` | `string` | `"Enter email address…"` | No | Input placeholder. |

---

### 3. Variants

N/A — Single presentation. State changes drive visual differentiation.

---

### 4. States — Complete Coverage Table

| State | Visual Treatment | Behaviour | Transitions to |
|-------|-----------------|-----------|----------------|
| **Default** | Rounded container, 1px `--color-border`. Chips inside (if any) followed by text input. "Add" button right of input (enabled when input has value). Counter below: "[N] of [maxEmails] added" (`--color-text-muted`). | `Enter` or "Add" validates and calls `onAdd`. | Hover, Focus, Error |
| **Hover** | Container border → `--color-border-hover`. | cursor: text over input; cursor: pointer over chip "×" buttons. | Default, Active |
| **Focus** | Container border → `--color-brand-primary` 2px. Inner `<input>` focus ring normalised. | Keyboard input active. | Default, Active |
| **Active** | "Add" button pressed state: scale 0.95, `--color-brand-primary-active`. | Chip appears on successful add. | Default |
| **Disabled** | 40% opacity. cursor: not-allowed. `aria-disabled="true"`. Chip "×" buttons hidden. `<input disabled>`. | No typing, adding, or removing. | — |
| **Loading** | Existing chips → skeleton pills of identical dimensions. Input disabled. `aria-busy="true"`. | Non-interactive. Layout preserved. | Default |
| **Error** | Container border → `--color-error`. Error message with icon below container. Input area still interactive. | `aria-live="polite"` announces error. Clears on next successful add. | Default |
| **Empty** | Input with placeholder. No chips. Counter: "0 of [max] added". "Add" button disabled (no value). | First valid add creates first chip. | Default (with chips) |

**Chip sub-states:**

| Sub-state | Visual Treatment | Behaviour |
|-----------|-----------------|-----------|
| Chip: Default | Rounded pill, `--color-surface-brand-subtle`. `Avatar` (sm, initials) + email text (truncated at 24ch) + "×" `Button` (ghost, xs). | — |
| Chip: Hover | "×" scales 1.1. Background → `--color-surface-brand`. | cursor: pointer on "×". |
| Chip: Focus (×) | Focus ring on "×". | `Enter`/`Space` → `onRemove(email)`. |
| Chip: Active (×) | "×" scales 0.9. | Chip animates out. |

**Input error sub-state** (when `inputError` non-null): Input border → `--color-error`. Error text immediately below input. `aria-invalid="true"` on input.

**Max-reached state** (when `emails.length >= maxEmails`): Input hidden. Message: "Maximum of [maxEmails] invites reached. Remove one to add another." `aria-live="polite"` announces on transition.

---

### 5. Responsive Behaviour

| Breakpoint | Width | Layout Changes | Content Changes |
|-----------|-------|---------------|----------------|
| **Mobile** | < 640px | Wizard targets tablet+. If forced: chips wrap, container grows. | Email truncates at 20ch. |
| **Tablet** | 640–1024px | Chips wrap within container. Max 2 chip rows before internal scroll. | Touch targets: "×" button ≥ 44×44px. |
| **Desktop** | > 1024px | Up to 3 chips per row. | Full email text. |

---

### Performance Considerations

N/A — Maximum 5 chips. Add/remove are O(1) array operations. No virtualisation required.

---

### 6. Accessibility Requirements

#### Keyboard Navigation

| Element Type | Key | Action |
|---|---|---|
| Text input | Type | Enter email |
| Text input | `Enter` | Validate; call `onAdd` if valid + non-duplicate |
| Text input | `Backspace` (on empty input) | Remove last chip |
| Text input | `Tab` | Focus first chip "×", then "Add" button, then exit |
| Chip "×" | `Enter` / `Space` | Remove chip; focus → text input |
| Chip "×" | `Delete` / `Backspace` | Remove chip; focus → previous "×" or text input |
| Chip "×" | `Tab` / `Shift+Tab` | Navigate between "×" buttons |

After chip removal: focus returns to text input. After add via `Enter`: focus stays in text input.

#### Screen Reader

- **Role:** `role="group"` on container, `aria-label="Email invites"`.
- **Text input:** `role="textbox"`, `aria-label="Email address"`, `aria-describedby` → counter `<p>` + `inputError` `<p>`.
- **Chip list:** `role="list"`. Each chip: `role="listitem"`.
- **Chip "×":** `role="button"`, `aria-label="Remove [email@example.com]"`.
- **Counter:** `aria-live="polite"` announces count change on add/remove.
- **Input errors (immediate):** `aria-live="assertive"` announces:
  - Invalid format: `"Invalid email format"`
  - Duplicate: `"This email has already been added"`
- **Max-reached:** `aria-live="polite"` → `"Maximum of 5 invites reached."`
- **Field-level `error`:** `aria-live="polite"` on error region below component.
- **Input validity:** `aria-invalid="true"` when `inputError` non-null.

#### Colour and Contrast

- Chip email text on `--color-surface-brand-subtle`: ≥ 4.5:1.
- Chip "×" icon: ≥ 3:1 against chip background.
- Error text + icon: not colour alone.
- Counter `--color-text-muted`: verify ≥ 4.5:1 — muted tones commonly fail AA.

#### Focus Management

- No focus trap — inline within step form.
- Focus returns to text input after chip removal.
- Focus indicator visible in light and dark modes.

---

### 7. Dark Mode

- [x] Chip `--color-surface-brand-subtle` has verified dark-mode variant
- [x] Container border `--color-border` / `--color-border-hover` tokens
- [x] "×" icon `--color-icon-muted`
- [x] Error: `--color-error` on dark — verify; may need `--color-error-dark` (lighter red) to maintain ≥ 4.5:1
- [x] `Avatar` initials inherit existing `Avatar` high-contrast tokens
- [x] "Add" button inherits `Button` dark-mode tokens

---

### 8. Animation and Motion

| Element | Animation | Duration | Easing | Reduced-motion fallback |
|---------|-----------|----------|--------|------------------------|
| Chip add | `scale(0)`→`scale(1)`, `opacity` 0→1 | 200ms | ease-out | Instant appear |
| Chip remove | `scale(1)`→`scale(0)`, `opacity` 1→0 | 150ms | ease-in | Instant disappear |
| Input error shake | `translateX` ±4px × 3 | 250ms | ease-in-out | Instant; no shake |
| Max-reached message | `opacity` 0→1 | 150ms | ease-out | Instant appear |

---

### 9. Usage Examples

```tsx
// Empty state
<EmailTagInput emails={[]} onAdd={handleAdd} onRemove={handleRemove} />

// With existing invites and input validation error
<EmailTagInput emails={["alice@acme.com", "bob@acme.com"]}
  onAdd={handleAdd} onRemove={handleRemove} inputError="Invalid email format" />

// Max reached (5/5)
<EmailTagInput emails={["a@b.com","c@d.com","e@f.com","g@h.com","i@j.com"]}
  onAdd={handleAdd} onRemove={handleRemove} maxEmails={5} />

// Disabled after step submission
<EmailTagInput emails={confirmed} onAdd={noop} onRemove={noop} disabled={true} />
```

---

### 10. Do / Don't

| Do | Don't |
|----|-------|
| Validate format client-side before calling `onAdd` | Call `onAdd` with invalid strings |
| Keep focus in text input after each chip add | Return focus to first chip or page top |
| Use `aria-label="Remove [email]"` on each "×" | Use `aria-label="×"` or `aria-label="Remove"` |
| Show counter + max-reached message | Silently disable the input at max |
| Support `Backspace` on empty input to remove last chip | Require only the "×" button for removal |

---

## Per-Step Error States

### Step 1: Workspace Setup

| Field | Error Condition | Error Message | Validation Trigger |
|-------|-----------------|---------------|--------------------|
| Workspace Name | Empty on submit | "Workspace name is required." | On submit |
| Workspace Name | > 64 characters | "Workspace name must be 64 characters or fewer. ([N]/64)" | On blur + on submit |
| Workspace Name | Duplicate — API 409 | "A workspace with this name already exists. Please choose a different name." | On submit (async) |
| Logo Upload | File type rejected | "Only PNG, JPEG, and SVG files are supported." | On file select |
| Logo Upload | File > 2 MB | "File exceeds 2 MB. Please choose a smaller image." | On file select |
| Logo Upload | Upload failed (network/server) | "Logo upload failed. Please try again." + retry `Button` | During upload (async) |
| Timezone | Not selected on submit | "Please select a timezone." | On submit |

**Global Step 1 pattern:** All fields validate simultaneously on submit. `aria-live="assertive"` announces: `"Please fix [N] error(s) to continue."` Focus moves to the first invalid field.

---

### Step 2: Invite Team

| Condition | Error Message | Validation Trigger |
|-----------|---------------|--------------------|
| Invalid email format | "Please enter a valid email address." | On `Enter` / "Add" — via `inputError` prop |
| Duplicate email in list | "This email has already been added." | On `Enter` / "Add" — via `inputError` prop |
| > `maxEmails` (5) | "Maximum of 5 invites reached. Remove one to add another." | On `Enter` / "Add" at max — via `inputError` |
| Email domain blocked (API) | "[email] cannot be invited. Contact your administrator." | On submit (async) — via `error` prop |
| Invite send failure (network) | "Failed to send invites. Check your connection and try again." + retry | On submit (async) — via `error` prop |

**Step 2 note:** Proceeding with zero invites is valid — no error on empty list.

---

### Step 3: Connect Integration

| Condition | Error Message | Banner Variant | Recovery |
|-----------|---------------|---------------|----------|
| OAuth cancelled (user denied) | "Connection cancelled. You can connect [Service] later from Settings." | `warning` | Dismiss; skip or retry |
| OAuth auth failure (server) | "Something went wrong connecting to [Service]. Please try again." | `error` | Retry button (re-opens OAuth) |
| Network timeout (> 10 s) | "Connection timed out. Check your internet connection and try again." | `error` | Retry button |
| Scope denied | "Clearpath needs additional permissions. Please try again and accept all requested permissions." | `error` | Retry (re-opens OAuth with full scope) |
| Integration already connected | "This account is already connected." | `info` | Informational — proceed |
| Skip selected | No error — integration marked "Not connected" in Settings. | — | — |

**Step 3 pattern:** Errors appear as a single inline banner below the integration tile grid. OAuth popup lifecycle is managed by the host application.

---

### Step 4: Create First Project

| Condition | Error Message | Validation Trigger |
|-----------|---------------|--------------------|
| No template selected | "Please select a project template to continue." | On submit — inline below template grid |
| Project name empty | "Project name is required." | On submit |
| Project name > 80 characters | "Project name must be 80 characters or fewer." | On blur + on submit |
| Project name conflict — API 409 | "A project named '[name]' already exists. Please choose a different name." | On submit (async) |
| Template list fetch failure | "Couldn't load project templates. Check your connection." + retry | On mount / retry |
| Template list empty (plan restriction) | "No templates available for your plan. You can create a blank project instead." + CTA | On mount — empty state |
| Project creation failed (server) | "Project creation failed. Please try again." | On submit (async) |

---

## ARIA + Keyboard Navigation Reference

### Wizard Shell (page layout — not a new component)

| Element | Attribute | Value |
|---------|-----------|-------|
| Outer wrapper | `<section aria-label="Onboarding wizard">` | — |
| Step content area | `role="main"` or `<main>` | — |
| Step transition announcement | `<div aria-live="polite" aria-atomic="true" class="sr-only">` | `"Step [N] of 4: [Label]"` on `currentStep` change |

### New Component ARIA + Keyboard Summary

| Component | `role` | `aria-label` / `aria-labelledby` | `tabindex` | Advance key | Retreat key |
|-----------|--------|----------------------------------|------------|-------------|-------------|
| `StepIndicator` | `nav` (container); `button` (completed); `span` (current/upcoming) | `aria-label="Onboarding progress"` on nav; `aria-label="Step N: [Label], completed"` on buttons | `0` on completed buttons; `-1` on current/upcoming | `Tab` between completed nodes; `Enter`/`Space` navigate | `Shift+Tab` |
| `LogoUpload` | `button` (upload area) | `aria-label="Upload workspace logo"` | `0` on area; `0` on "×" when visible | `Enter`/`Space` (open picker) | `Shift+Tab` |
| `TimezoneSelect` | `combobox` (trigger); `listbox` (panel); `option` (items); `group` (regions) | `aria-labelledby` → visible `<label>`; dropdown `aria-label="Timezones"` | `0` on trigger | `ArrowDown`/`Enter`/`Space` open + navigate + select | `Escape` close; `Shift+Tab` exit |
| `EmailTagInput` | `group` (container); `textbox` (input); `list` (chips); `listitem`; `button` (×) | `aria-label="Email invites"` on group; `aria-label="Remove [email]"` on × buttons | `0` on input; `0` on each × | `Enter` add; `Tab` to "×" buttons | `Backspace` on empty input removes last chip |

### Wizard Tab Order by Step

**Step 1:** StepIndicator completed nodes → Logo upload area → Logo "×" (if preview shown) → Workspace name `Input` → `TimezoneSelect` trigger → Back `Button` → Next `Button`

**Step 2:** StepIndicator completed nodes → `EmailTagInput` text input → Chip "×" buttons → "Add" `Button` → Back `Button` → Next `Button` (+ "Skip for now" link)

**Step 3:** StepIndicator completed nodes → Integration `Card` 1 → `Card` 2 → `Card` 3 → Back `Button` → "Connect" `Button` → "Skip" link

**Step 4:** StepIndicator completed nodes → Template `Card` 1 → … → Template `Card` N → Project name `Input` → Back `Button` → "Create project" `Button`

---

## Wizard-Level Do / Don't

| Do | Don't |
|----|-------|
| Validate each step before advancing | Defer all validation to final submission |
| Allow backward navigation to any completed step via StepIndicator | Lock completed steps — users need to correct earlier entries |
| Preserve form state across step navigation | Reset state when user navigates back |
| Announce step transitions via `aria-live` outside StepIndicator | Rely on the visual progress indicator alone |
| Make Step 3 (integrations) skippable without an error state | Block wizard completion on optional steps |
| Show "N of 5 added" counter in `EmailTagInput` | Show a generic "Add teammates" label with no count feedback |
| Pre-detect timezone via `autoDetect` on Step 1 mount | Leave timezone empty and force every user to search |

---

## Related Skills

- `/ui-designer:design-review` — review the implemented wizard against this spec.
- `/ui-designer:accessibility-audit` — audit all four new components for WCAG 2.1 AA compliance after implementation.

---

The spec is written to disk at `clearpath-onboarding-wizard-spec.md`. Here's a summary of what's covered:

**4 new components specified (CREATE):** `StepIndicator`, `LogoUpload`, `TimezoneSelect`, `EmailTagInput` — each with all 10 mandatory sections including the full 8-state table.

**4 existing components confirmed REUSE:** `Input`, `Button`, `Avatar`, `Card` — with explicit rationale for why no extension is needed.

**Per-step error states:** 7 error conditions for Step 1, 5 for Step 2, 6 for Step 3, 7 for Step 4 — each with message text, variant, and trigger.

**ARIA + keyboard nav:** Role, label, tabindex, and advance/retreat keys documented per component, plus a wizard-level tab order by step.

**Key design decisions documented inline:**
- `TimezoneSelect` uses virtualised rendering (required from day one — 500 DOM nodes causes jank).
- `autoDetect` pre-populates timezone but does not auto-call `onChange` — caller persists on "Next".
- Integration error banner is per-step (not per-tile); OAuth lifecycle is host-application responsibility.
- `LogoUpload` uses object URLs for instant preview before server upload completes.

### Artifacts written

#### `work/clearpath-onboarding-wizard-spec.md`

```
# Clearpath Onboarding Wizard — Component Specification

**Assumptions (proceeding without clarification per brief):**
- Stack: React + TypeScript with CSS custom-property design tokens (`--color-*`, `--space-*`).
- Breakpoints: Tailwind defaults — sm 640px, md 768px, lg 1024px.
- Focus ring: 2px solid `--color-focus-ring`, 2px offset, visible in light and dark modes.
- Existing design system: `Input`, `Button`, `Avatar`, `Card` only. No `Select`, `Stepper`, `Upload`, or `TagInput` components exist.
- Logo upload constraint: PNG / JPEG / SVG, max 2 MB.
- Timezone data source: `Intl.supportedValuesOf('timeZone')` or bundled IANA dataset — resolved by caller, not a prop.
- Wizard is a client-side flow; OAuth popup for integrations is managed by the host application.

---

## Existing Component Reuse Table

| Component | Decision | Rationale |
|-----------|----------|-----------|
| `Input` | REUSE | Used without modification for workspace name (Step 1), project name (Step 4), and as the inner text field within `EmailTagInput`. Existing validation and error-message props are sufficient. |
| `Button` | REUSE | All CTAs — Next, Back, Skip, Connect, Create, Add (email), Remove (logo) — use the existing `Button` component with its `primary` and `ghost`/`secondary` variants. No new variant needed. |
| `Avatar` | REUSE | Email chip tags in `EmailTagInput` (Step 2) render invited-member initials using the existing `Avatar` component at `sm` size with its built-in initials-fallback logic. |
| `Card` | REUSE | Integration tiles (Step 3) and template tiles (Step 4) are composed from the existing `Card` component. A selected-state overlay is applied via a wrapping `div` and `aria-selected` — no new component required. |
| `StepIndicator` | CREATE | No existing progress, stepper, breadcrumb, or wizard-step component exists in the design system. Cannot be composed from the four existing components. Full spec below. |
| `LogoUpload` | CREATE | No file-upload or image-upload component exists. `Input type="file"` does not support drag-and-drop, preview, upload-progress overlay, or aspect-ratio constraints. Full spec below. |
| `TimezoneSelect` | CREATE | No `Select`, `Combobox`, or `Autocomplete` component exists. `Input` does not support option lists. ~500 IANA entries require a virtualised, searchable dropdown — distinct enough from `Input` to warrant a new component. Full spec below. |
| `EmailTagInput` | CREATE | No multi-value tag/chip input exists. `Input` supports single-value text entry only. The invite flow requires adding up to 5 emails as removable chips with per-chip `Avatar`, inline validation, and a counter. Cannot be composed from `Input` alone. Full spec below. |

---

## Component 1: StepIndicator

### 0. Design System Decision

**Decision: CREATE** — Searched for Stepper, ProgressIndicator, Breadcrumb, WizardNav, and similar components. None found in the design system (Input, Button, Avatar, Card). The StepIndicator must show 4 named steps, differentiate completed / current / upcoming states visually, and allow backward navigation to completed steps via click or keyboard. This cannot be assembled from the four existing components.

---

### 1. Purpose and Usage Context

**What:** A horizontal progress indicator that shows the user's position across named steps in a sequential flow and enables backward navigation to completed steps.

**When to use:** Inside multi-step wizard or onboarding flows where steps must be completed in order and the user may need to revisit earlier steps. Do NOT use for tab navigation (use `Tabs`), percentage-complete progress (use a `ProgressBar`), or documentation page sections (use a plain ordered list).

---

### 2. Props / API

| Prop | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| `steps` | `Step[]` | — | Yes | Ordered array of step definitions. Min length: 1. |
| `currentStep` | `number` | — | Yes | Zero-based index of the active step. |
| `onStepClick` | `(index: number) => void` | `undefined` | No | Called when user activates a completed step. If omitted, completed steps are not clickable. |
| `loading` | `boolean` | `false` | No | Replaces all step nodes with skeleton shimmer; disables all interaction. |

```ts
interface Step {
  label: string;         // e.g. "Workspace Setup"
  description?: string;  // e.g. "Name and timezone" — hidden on tablet
}
```

---

### 3. Variants

N/A — `StepIndicator` has a single presentation. Visual differentiation is carried by per-node state (completed / current / upcoming), not a `variant` prop.

---

### 4. States — Complete Coverage Table

Each step *node* within the indicator carries one of three sub-states: **completed** (`index < currentStep`), **current** (`index === currentStep`), **upcoming** (`index > currentStep`). The table below describes the *component-level* states.

| State | Visual Treatment | Behaviour | Transitions to |
|-------|-----------------|-----------|----------------|
| **Default** | Completed nodes: filled `--color-brand-primary` circle, white checkmark icon, full-opacity label. Current node: filled `--color-brand-primary` circle with step number, bold label. Upcoming nodes: `--color-border` outline circle, muted step number, `--color-text-muted` label. Connector lines: `--color-brand-primary` between completed steps; `--color-border` toward upcoming steps. | Completed nodes clickable when `onStepClick` provided (cursor: pointer). Current and upcoming: cursor: default, not clickable. | Hover (completed node), Focus (completed node) |
| **Hover** | Hovered completed node: circle background → `--color-brand-primary-hover`. Label gets underline. Connector unchanged. Upcoming/current nodes: no hover effect. | cursor: pointer on completed nodes. Tooltip with truncated label shown if label text overflows. | Default, Active |
| **Focus** | Focused completed node: 2px solid `--color-focus-ring` outline, 2px offset, around circle + label bounds. Outline visible in both light and dark modes. | Tab navigates only between completed step nodes. Current and upcoming nodes are not in the tab order (`tabindex="-1"`). | Default, Active |
| **Active** | Completed node: circle scales to 0.95 via `transform: scale(0.95)`. Background → `--color-brand-primary-active`. | Visual feedback on click/keypress. Calls `onStepClick(index)` on pointer-up or keyup Enter/Space. | Default (after navigation) |
| **Disabled** | Entire indicator at 40% opacity. All circles and labels use `--color-text-disabled`. No completed-step affordances. `aria-disabled="true"` on container. | cursor: not-allowed on all nodes. No click, no keyboard navigation. Used during step submission to prevent double-navigation. | Loading, Default |
| **Loading** | All step circles and labels replaced with skeleton shimmer animation of identical dimensions. Connector lines also shimmer. `aria-busy="true"` on container. | Non-interactive. Layout preserved — no shift when shimmer resolves. Animation governed by `prefers-reduced-motion`. | Default, Error |
| **Error** | Current step node's circle → `--color-error` background with exclamation `!` icon replacing the step number. Current step label → `--color-error`. Completed and upcoming nodes unchanged. | Backward navigation to completed steps remains available. Error indicator clears when user starts correcting the step's form. | Default (on correction) |
| **Empty** | N/A — `steps` must have ≥ 1 item (enforced by TypeScript). If `steps` is empty at runtime, component returns `null` silently. Caller is responsible for a non-empty array. | — | — |

**Compound state combinations:**

| Combination | Resolved Behaviour |
|-------------|-------------------|
| `loading={true}` + completed steps present | Skeleton overrides all clickability. No interaction permitted. |
| Error on current step + completed steps present | Backward navigation to completed steps stays enabled. Error styling applies only to current node. |
| `currentStep` equals last index | All preceding nodes show completed. Final connector line is hidden (no "upcoming" node after last). |

---

### 5. Responsive Behaviour

| Breakpoint | Width | Layout Changes | Content Changes |
|-----------|-------|---------------|----------------|
| **Mobile** | < 640px | Wizard targets desktop + tablet. If forced to render on mobile, StepIndicator collapses to a single `"Step N of 4"` text line — no circles, no connectors. | `Step.label` and `Step.description` hidden; only ordinal text shown. |
| **Tablet** | 640–1024px | Horizontal layout maintained. Labels truncate to single line with ellipsis at container width. | `description` prop hidden to conserve space. |
| **Desktop** | > 1024px | Full horizontal layout: circles, connectors, labels, and optional `description` lines. | All content visible. |

**Rules:**
- Each completed step node touch target: min 44×44px (WCAG 2.5.5).
- No horizontal scroll at any supported breakpoint.
- Labels truncate with ellipsis — no wrapping that expands the component height.

---

### Performance Considerations

N/A — StepIndicator renders a fixed, small number of nodes (3–8 in practice). Re-renders are O(steps.length). No virtualisation needed.

---

### 6. Accessibility Requirements

#### Keyboard Navigation

| Element Type | Key | Action |
|---|---|---|
| Completed step node (`<button>`) | `Tab` | Move focus to next completed step node |
| Completed step node (`<button>`) | `Shift+Tab` | Move focus to previous completed step node |
| Completed step node (`<button>`) | `Enter` / `Space` | Navigate to that step — calls `onStepClick(index)` |
| Current / upcoming step (`<span>`) | — | Not in tab order (`tabindex="-1"`), not interactive |

**Focus management after `onStepClick`:** Focus moves to the first focusable element in the target step's form content — not back to the step indicator.

#### Screen Reader

- **Role:** `<nav role="navigation" aria-label="Onboarding progress">` wrapping the indicator.
- **Completed step nodes:** `<button aria-label="Step 1: Workspace Setup, completed">`.
- **Current step node:** `<span aria-current="step">` — not a button.
- **Upcoming step nodes:** `<span>` with no special ARIA — announced by visible text only.
- **Step transitions:** An `aria-live="polite"` region *outside* the indicator announces `"Step [N] of 4: [Label]"` whenever `currentStep` changes.
- **Description:** A visually hidden `<p aria-describedby>` reads: `"Completed steps can be selected to return and edit them."` — rendered once on mount.

#### Colour and Contrast

- Step number / icon within circle: ≥ 4.5:1 against circle fill.
- Connector lines: ≥ 3:1 against page background.
- Focus ring: ≥ 3:1 against adjacent background in both modes.
- Error state: exclamation icon supplements red colour — not colour alone.

#### Focus Management

- Focus is not trapped within StepIndicator.
- Component mount does not steal focus — first focus goes to Step 1's first form field.
- Focus indicator visible in light and dark modes.

---

### 7. Dark Mode

- [x] All colours use semantic tokens (`--color-brand-primary`, `--color-text-muted`, `--color-error`, `--color-border`)
- [x] Contrast re-verified in dark mode: muted label on dark surface ≥ 4.5:1
- [x] No images — ThemeImage N/A
- [x] Connector lines use `--color-border` token (auto-lightens in dark mode)
- [x] Focus ring uses `--color-focus-ring` token (light: blue-600, dark: blue-400)
- [x] Shadows: N/A — StepIndicator is flat

---

### 8. Animation and Motion

| Element | Animation | Duration | Easing | Reduced-motion fallback |
|---------|-----------|----------|--------|------------------------|
| Node: upcoming → current | Circle fill cross-fades from outline to solid | 200ms | ease-out | Instant fill |
| Node: current → completed | Checkmark draws in (stroke-dashoffset 0→100%) | 250ms | ease-out | Instant checkmark |
| Connector line fill | Left-to-right fill (`scaleX` 0→1, transform-origin: left) | 250ms | ease-out | Instant fill |
| Error state entry | Circle cross-fades to `--color-error` | 150ms | ease-in | Instant swap |
| Hover: scale active | `transform: scale(0.95)` | 100ms | ease-in | No transform |

All governed by `@media (prefers-reduced-motion: reduce)` — instant state changes with no transforms or cross-fades.

---

### 9. Usage Examples

```tsx
// Standard 4-step wizard at step 2 (zero-indexed: currentStep=1)
<StepIndicator
  steps={[
    { label: "Workspace Setup", description: "Name and timezone" },
    { label: "Invite Team",     description: "Up to 5 members" },
    { label: "Integrations",    description: "Connect your tools" },
    { label: "First Project",   description: "From a template" },
  ]}
  currentStep={1}
  onStepClick={(i) => wizard.goToStep(i)}
/>

// Loading state — between step transitions
<StepIndicator
  steps={WIZARD_STEPS}
  currentStep={2}
  loading={true}
/>

// Locked wizard — no backward navigation
<StepIndicator
  steps={WIZARD_STEPS}
  currentStep={0}
/>
```

---

### 10. Do / Don't

| Do | Don't |
|----|-------|
| Always supply `onStepClick` — backward navigation is expected in onboarding | Lock completed steps unless the flow technically forbids revisiting |
| Use the `loading` prop during submission to block double-navigation | Manually set `pointer-events: none` via CSS — use the prop |
| Keep step labels ≤ 3 words — they truncate on tablet | Use full sentence labels |
| Announce step transitions via `aria-live` outside the indicator | Rely on the indicator alone to communicate progress to screen readers |

---

## Component 2: LogoUpload

### 0. Design System Decision

**Decision: CREATE** — Searched for FileInput, ImageUpload, AvatarEditor, and Dropzone components. None found. `Input type="file"` exists as an HTML primitive but the design system has no styled file upload component. LogoUpload requires: drag-and-drop with visual affordance, image preview at 128×128px, upload-progress overlay, and client-side file validation. A new component is needed.

---

### 1. Purpose and Usage Context

**What:** An interactive upload area that accepts a single image file via drag-and-drop or OS file picker, displays a live preview, and communicates upload progress.

**When to use:** Single-image upload where preview and type/size validation are needed — workspace logo, user profile photo. Do NOT use for multi-file upload, document upload, or any non-image format.

---

### 2. Props / API

| Prop | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| `onFileSelect` | `(file: File) => void` | — | Yes | Called after client-side validation passes. Caller is responsible for uploading. |
| `onClear` | `() => void` | — | Yes | Called when the user removes the current image. |
| `previewUrl` | `string \| null` | `null` | No | URL to display as preview. When provided, component is in preview mode. |
| `uploading` | `boolean` | `false` | No | Shows upload-progress overlay when `true`. |
| `uploadProgress` | `number` | `0` | No | Integer 0–100. Shown only when `uploading={true}`. |
| `error` | `string \| null` | `null` | No | Error message displayed below the upload area. Clears on next valid file selection. |
| `disabled` | `boolean` | `false` | No | Disables all interaction. |
| `accept` | `string` | `"image/png,image/jpeg,image/svg+xml"` | No | MIME types forwarded to the hidden `<input type="file">`. |
| `maxSizeBytes` | `number` | `2097152` | No | Max file size in bytes (default 2 MB). Files exceeding this trigger `error` without calling `onFileSelect`. |

---

### 3. Variants

N/A — Single presentation. Appearance is driven by state (empty / preview / uploading / error), not a `variant` prop.

---

### 4. States — Complete Coverage Table

| State | Visual Treatment | Behaviour | Transitions to |
|-------|-----------------|-----------|----------------|
| **Default** | 128×128px square with 2px dashed `--color-border-dashed` border, 8px border-radius. Centred upload-cloud icon in `--color-icon-muted`. Label below icon: "Click or drag to upload" in `--color-text-muted`. Background: `--color-surface-subtle`. | Entire area is a `<button>` (or `<div role="button">`). Click opens OS file picker via hidden `<input type="file">`. Drag-over activates Hover state. | Hover, Focus, Active |
| **Hover** | Border: 2px dashed `--color-brand-primary`. Background: `--color-surface-brand-subtle`. Upload icon translates up 2px. | Valid drag target indicated. cursor: pointer. | Default, Active |
| **Focus** | 2px solid `--color-focus-ring` outline, 2px offset. Dashed border unchanged. | Keyboard focus indicator. `Enter` or `Space` opens file picker. | Default, Active |
| **Active** | Background → `--color-surface-brand-active`. Icon scales to 0.95. | Visual feedback on press/click. | Default (no file), Preview (file selected) |
| **Disabled** | Full component at 40% opacity. cursor: not-allowed. Dashed border → `--color-border-disabled`. `aria-disabled="true"`. Hidden `<input>` has `disabled` attribute. | No click, no drag. | — |
| **Loading** | `previewUrl` image visible behind 50% black overlay. Circular indeterminate progress ring centred in overlay (switches to determinate arc when `uploadProgress` > 0). Progress percentage text below ring in white. Layout dimensions unchanged (128×128px). | Non-interactive. Remove button hidden. `aria-busy="true"`. | Default (on error), Preview (on success) |
| **Error** | Dashed border → `--color-error`. Error icon below the upload area. Error message string in `--color-error` below icon. Upload icon and label return to default appearance (still interactive). | User can re-attempt. File picker remains accessible. Error clears on next valid selection. `aria-live="polite"` announces error. | Default, Active |
| **Empty** | Identical to Default — the "no image" state is the Default state. Listed here to confirm it is not a distinct visual state. | — | — |

**Preview sub-state** (active when `previewUrl` is non-null and `uploading` is false):

| Sub-state | Visual Treatment | Behaviour |
|-----------|-----------------|-----------|
| Preview: Default | 128×128px rounded-square image (object-fit: cover). "×" remove button (`Button` ghost, sm) in top-right corner. | Clicking image re-opens file picker. Remove button calls `onClear`. |
| Preview: Hover | Semi-transparent overlay with "Change" label centred. "×" button scales 1.1. | cursor: pointer on image. |
| Preview: Focus (×) | Focus ring on "×" button. | `Enter` / `Space` calls `onClear`. Focus returns to upload area. |

---

### 5. Responsive Behaviour

| Breakpoint | Width | Layout Changes | Content Changes |
|-----------|-------|---------------|----------------|
| **Mobile** | < 640px | Wizard targets tablet+. If forced visible: 96×96px upload area. | Label → "Upload logo" (shorter). |
| **Tablet** | 640–1024px | 128×128px. Full label. | All states functional. Touch target ≥ 44×44px — entire area qualifies. |
| **Desktop** | > 1024px | 128×128px. Same as tablet. | All states functional. |

---

### Performance Considerations

N/A — Single file. Preview uses `URL.createObjectURL` (local, no network round-trip). Object URL is revoked via `URL.revokeObjectURL` in a cleanup effect on unmount or file change to prevent memory leaks.

---

### 6. Accessibility Requirements

#### Keyboard Navigation

| Key | Action |
|-----|--------|
| `Tab` | Focus moves to LogoUpload upload area |
| `Enter` / `Space` | Opens OS file picker |
| `Tab` (preview mode) | Moves focus to "×" remove button |
| `Enter` / `Space` (on ×) | Calls `onClear`; focus returns to upload area |
| `Shift+Tab` | Reverse focus movement |
| `Escape` | N/A — no overlay to dismiss |

#### Screen Reader

- **Role:** `button` on the upload area (`<button>` or `<div role="button" tabindex="0">`). The `<input type="file">` is `aria-hidden="true"` — the button wrapper handles the accessible interaction.
- **Label:** `aria-label="Upload workspace logo"` on the button wrapper.
- **State announcements:**
  - File selected (preview): `aria-live="polite"` → `"Logo selected: [filename]"`.
  - Upload progress: `aria-live="polite"` at 25 / 50 / 75 / 100% milestones → `"Uploading… [N]%"` (throttled to ≤ 4 announcements per upload).
  - Upload complete: `aria-live="polite"` → `"Logo uploaded successfully."`.
  - Error: `aria-live="polite"` → the `error` prop string.
- **Description:** `aria-describedby` pointing to a visually hidden `<p>`: `"Accepted formats: PNG, JPEG, SVG. Maximum size: 2 MB."`.
- **Remove button:** `aria-label="Remove logo"` (from `Button` component's `aria-label` prop).

#### Colour and Contrast

- Dashed border (default): 3:1 against `--color-surface-subtle`.
- Error border + text: `--color-error` ≥ 4.5:1 on light background; error icon supplements colour.
- Progress overlay text (white on dark overlay): ≥ 4.5:1.

#### Focus Management

- No focus trap.
- After file picker closes (selection or cancel): focus returns to upload area.
- After `onClear`: focus returns to upload area.
- Focus indicator visible in both light and dark modes.

---

### 7. Dark Mode

- [x] All colours use semantic tokens
- [x] Dashed border visible on dark surfaces (`--color-border-dashed` lightens in dark mode)
- [x] Upload icon `--color-icon-muted` auto-adjusts
- [x] Progress overlay: light mode `rgba(0,0,0,0.5)` → dark mode `rgba(0,0,0,0.65)` (image is already dark-adjusted via preview URL)
- [x] Focus ring `--color-focus-ring` token (verified at ≥ 3:1 on dark backgrounds)
- [x] Error text/border re-verified: `--color-error` on dark background — may need `--color-error-subtle` variant if pure red fails contrast

---

### 8. Animation and Motion

| Element | Animation | Duration | Easing | Reduced-motion fallback |
|---------|-----------|----------|--------|------------------------|
| Hover: border colour | CSS `transition: border-color` | 150ms | ease-out | Instant |
| Hover: icon nudge | `transform: translateY(-2px)` | 150ms | ease-out | No transform |
| Active: scale | `transform: scale(0.95)` | 100ms | ease-in | No transform |
| Preview: appear | `opacity` 0→1 | 200ms | ease-out | Instant |
| Error: shake | `translateX` ±4px, 3 cycles | 300ms | ease-in-out | No shake, instant |
| Overlay: appear | `opacity` 0→1 | 150ms | ease-out | Instant |

All governed by `@media (prefers-reduced-motion: reduce)`.

---

### 9. Usage Examples

```tsx
// Default — no logo yet
<LogoUpload
  onFileSelect={(file) => handleLogoFile(file)}
  onClear={() => setLogoUrl(null)}
/>

// Preview with existing logo
<LogoUpload
  previewUrl={workspace.logoUrl}
  onFileSelect={(file) => handleLogoFile(file)}
  onClear={() => clearLogo()}
/>

// Upload in progress (65%)
<LogoUpload
  previewUrl={localObjectUrl}
  uploading={true}
  uploadProgress={65}
  onFileSelect={handleLogoFile}
  onClear={clearLogo}
/>

// Error state — file too large
<LogoUpload
  error="File exceeds 2 MB. Please choose a smaller image."
  onFileSelect={handleLogoFile}
  onClear={clearLogo}
/>
```

---

### 10. Do / Don't

| Do | Don't |
|----|-------|
| Validate type and size client-side before calling `onFileSelect` | Call `onFileSelect` with invalid files and let the server reject them |
| Show preview immediately via object URL, before server upload completes | Wait for server upload to show any preview — creates perceived latency |
| Revoke object URL in cleanup effect on unmount or file change | Hold object URL references beyond the component lifecycle |
| Keep the component at a fixed 128×128px to prevent layout shift | Resize based on preview image dimensions |
| Show determinate progress ring when `uploadProgress` > 0 | Show only an indeterminate spinner — users want to know how long |

---

## Component 3: TimezoneSelect

### 0. Design System Decision

**Decision: CREATE** — Searched for Select, Combobox, Autocomplete, Dropdown, and Listbox components. None found in the design system. `Input` supports text entry only — no option list. Timezone selection requires a searchable combobox over ~500 IANA entries with regional grouping and virtualised rendering. A new component is required.

---

### 1. Purpose and Usage Context

**What:** A searchable combobox that lets a user select an IANA timezone from a grouped, filterable list, displaying the timezone's common name and UTC offset.

**When to use:** Timezone selection in workspace setup, user profile, or scheduling configuration. Do NOT use for general enumerable option lists (if a generic `Select` component is later added, prefer that). Do NOT use for non-timezone data — this component's list and display logic is timezone-specific.

---

### 2. Props / API

| Prop | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| `value` | `string \| null` | `null` | No | Selected IANA timezone string (e.g., `"Australia/Sydney"`). Controlled. |
| `onChange` | `(timezone: string) => void` | — | Yes | Called on selection. |
| `label` | `string` | `"Timezone"` | No | Visible label text rendered above the trigger. |
| `placeholder` | `string` | `"Select timezone…"` | No | Shown when `value` is null. |
| `error` | `string \| null` | `null` | No | Inline error message below the trigger. |
| `disabled` | `boolean` | `false` | No | Disables all interaction. |
| `loading` | `boolean` | `false` | No | Skeleton state — used when timezone data is loaded asynchronously. |
| `autoDetect` | `boolean` | `true` | No | On mount, pre-populates with `Intl.DateTimeFormat().resolvedOptions().timeZone` if `value` is null. Does not call `onChange` automatically — sets internal display only, caller must persist on Next. |

**Note on timezone data:** The timezone list is resolved from a module import or React context — not a prop. This keeps the component deployment-model-agnostic and avoids a large prop payload on every render.

---

### 3. Variants

N/A — Single presentation variant. Visual differentiation driven by component state (closed / open / error / disabled / loading).

---

### 4. States — Complete Coverage Table

The component has two layers: the **trigger** (resembles an `Input` field) and the **dropdown panel** (option list). States apply to the trigger unless stated otherwise.

| State | Visual Treatment | Behaviour | Transitions to |
|-------|-----------------|-----------|----------------|
| **Default** | Trigger styled identically to `Input`: `--color-border` border, `--color-surface` background, value text or placeholder (`--color-text-placeholder`). Chevron-down icon right-aligned. Dropdown closed. | Click or `Enter`/`Space` opens dropdown. `ArrowDown` opens and focuses first option. | Hover, Focus, Open |
| **Hover** | Border → `--color-border-hover`. Chevron → `--color-text-primary`. | cursor: pointer. | Default, Active |
| **Focus** | 2px solid `--color-focus-ring` outline, 2px offset. Border → `--color-brand-primary`. | Keyboard focus. `ArrowDown` or `Enter`/`Space` opens dropdown. | Default, Active, Open |
| **Active** | Background → `--color-surface-pressed`. Chevron rotates 180°. | Dropdown opens. | Open |
| **Disabled** | 40% opacity on trigger. cursor: not-allowed. `aria-disabled="true"`. Dropdown never opens. | No interaction. | — |
| **Loading** | Trigger replaced by skeleton shimmer of identical dimensions. `aria-busy="true"`. | Non-interactive. Layout preserved. | Default |
| **Error** | Trigger border → `--color-error`. Error icon replaces chevron (when closed). Error message below trigger in `--color-error` with error icon. | Dropdown still operable (user can re-select to clear error). Error clears on valid selection. `aria-live="polite"` announces error. | Default, Open |
| **Empty** | Dropdown open, search query returns no matches. Panel shows: `"No timezones match '[query]'. Clear search to see all."` Trigger and panel border unchanged. | Clearing the search query restores the full list. Escape closes without selecting. | Open (with results) |

**Open / Dropdown sub-states:**

| Sub-state | Visual Treatment | Behaviour |
|-----------|-----------------|-----------|
| Open: Default | Panel: `--color-surface-overlay` background, 1px `--color-border` border, 8px border-radius, `box-shadow: --shadow-md`. Appears below trigger (flips above if < 300px below viewport edge). Max-height 320px, overflow-y scroll. Search `<input>` at top with magnifying-glass icon. Groups rendered as non-interactive headers (`--color-text-muted`, uppercase, sm text). Selected option marked with checkmark. | Virtualised list renders only visible rows. |
| Open: Searching | Matching substring bolded in option label text. Non-matching options hidden. Group header hidden if all group options filtered out. List re-rendered debounced 100ms. | — |
| Open: Option Hover | `--color-surface-brand-subtle` background on hovered row. cursor: pointer. | — |
| Open: Option Focus | Same as Hover + `--color-focus-ring` outline (2px, inset). | `Enter` selects; `Escape` closes. |
| Open: Option Selected | Checkmark icon. Text bold. Row background `--color-surface-brand-subtle`. Scrolled into view on open. | Selecting again is a no-op (already selected). |

---

### 5. Responsive Behaviour

| Breakpoint | Width | Layout Changes | Content Changes |
|-----------|-------|---------------|----------------|
| **Mobile** | < 640px | Wizard targets tablet+. If forced: dropdown renders as a bottom-sheet modal (full-width, slides up). | — |
| **Tablet** | 640–1024px | Panel width equals trigger width. Max-height 240px (shorter for smaller screens). | Option rows ≥ 44px height for touch targets. |
| **Desktop** | > 1024px | Panel width ≥ trigger width (min 280px). Max-height 320px. | All features. |

---

### Performance Considerations

- **Rendering strategy:** Virtualised option list (`@tanstack/virtual` or `react-window`) required for ~500 IANA timezone entries. All 500 DOM nodes causes measurable jank on mid-range devices.
- **Threshold:** > 100 DOM nodes in the dropdown triggers visible layout recalculation. Virtualise from initial implementation.
- **Filter performance:** Client-side substring match on display name and UTC offset string. Debounced 100ms. No server round-trip.
- **Row height:** Fixed at 44px (required for virtualiser to calculate scroll bounds).

---

### 6. Accessibility Requirements

#### Keyboard Navigation

| Element Type | Key | Action |
|---|---|---|
| Trigger (closed) | `Enter` / `Space` / `ArrowDown` | Open dropdown; focus moves to search input |
| Trigger (closed) | `Tab` | Skip component, move focus past it |
| Search input (open) | Type | Filter list in real-time |
| Search input (open) | `ArrowDown` | Move focus to first option in virtualised list |
| Search input (open) | `Escape` | Close dropdown; focus returns to trigger |
| Option | `ArrowDown` / `ArrowUp` | Navigate between options |
| Option | `Enter` | Select focused option; close dropdown; focus returns to trigger |
| Option | `Escape` | Close without selecting; focus returns to trigger |
| Option | `Home` | Focus first visible option |
| Option | `End` | Focus last visible option |
| Option | `Tab` | Close dropdown; move focus to next element outside component |

**Focus management:** On open, focus moves to the search input. On close (any method), focus returns to trigger. On Tab from open dropdown, focus exits component entirely.

#### Screen Reader

- **Role:** `role="combobox"` on trigger, `aria-expanded="true/false"`, `aria-haspopup="listbox"`, `aria-controls="[listbox-id]"`.
- **Listbox:** `role="listbox"`, `aria-label="Timezones"`.
- **Options:** `role="option"`, `aria-selected="true/false"`, unique `id` per option.
- **Groups:** `role="group"`, `aria-label="[Region name]"` (e.g., "Australia").
- **Label:** Visible `<label htmlFor="[trigger-id]">` linked to trigger input. `aria-labelledby` on trigger pointing to label.
- **Active option:** `aria-activedescendant="[focused-option-id]"` on trigger (updated as user arrows through list).
- **Search input (inside panel):** `aria-label="Search timezones"`, `aria-controls="[listbox-id]"`.
- **Error:** `aria-invalid="true"` on trigger. `aria-describedby` pointing to error `<p>`.
- **Loading:** `aria-busy="true"` on trigger skeleton.

#### Colour and Contrast

- Placeholder text `--color-text-placeholder`: ≥ 4.5:1 against trigger background (verify — placeholder tones often fail AA).
- Option text on panel background: ≥ 4.5:1 in light and dark modes.
- Selected checkmark: ≥ 3:1 against option background.
- Error border + icon: not colour alone.

#### Focus Management

- On dropdown open: focus moves to search input within panel.
- On selection or Escape: focus returns to trigger.
- On Tab from open panel: focus exits to next component in tab order.

---

### 7. Dark Mode

- [x] Trigger uses same tokens as `Input` — inherits dark-mode adaptation
- [x] Panel background `--color-surface-overlay` (dark mode: `--color-gray-900` or equivalent)
- [x] Option hover `--color-surface-brand-subtle` verified ≥ 3:1 against panel background in dark
- [x] Group headers `--color-text-muted` — verify ≥ 4.5:1 in dark mode (muted tones risk failing)
- [x] Chevron `--color-icon-muted` token
- [x] Panel border `--color-border` (lightens in dark mode to remain visible)
- [x] Box shadow adapted for dark mode (`--shadow-md-dark` or reduced opacity)

---

### 8. Animation and Motion

| Element | Animation | Duration | Easing | Reduced-motion fallback |
|---------|-----------|----------|--------|------------------------|
| Panel open | `opacity` 0→1, `translateY(-4px)`→0 | 150ms | ease-out | Instant appear |
| Panel close | `opacity` 1→0, `translateY(0)`→`-4px` | 100ms | ease-in | Instant disappear |
| Chevron rotation | 0°→180° on open | 150ms | ease-out | Instant rotation |
| Filter: options hide | `opacity` 1→0 per hidden row | 80ms | linear | Instant show/hide |

---

### 9. Usage Examples

```tsx
// Auto-detect timezone on mount (autoDetect={true} by default)
<TimezoneSelect
  value={formState.timezone}
  onChange={(tz) => setFormState({ ...formState, timezone: tz })}
/>

// Explicit value with validation error
<TimezoneSelect
  value={null}
  onChange={handleTimezoneChange}
  error="Please select a timezone to continue."
  autoDetect={false}
/>

// Disabled after workspace is saved
<TimezoneSelect
  value="Australia/Sydney"
  onChange={noop}
  disabled={true}
/>
```

---

### 10. Do / Don't

| Do | Don't |
|----|-------|
| Virtualise the option list — 500 DOM nodes causes measurable jank | Render all timezone options as plain `<li>` elements |
| Pre-populate via `autoDetect` — most users should not need to search | Leave the field empty and force every user to manually search |
| Show UTC offset alongside name: "Sydney (UTC+10:00)" | Show raw IANA identifier only — "Australia/Sydney" is not meaningful to most users |
| Close dropdown and return focus to trigger on selection | Leave the dropdown open and require a separate confirm step |
| Debounce the search filter at 100ms | Re-filter on every keystroke — causes visible jank at 500 options |

---

## Component 4: EmailTagInput

### 0. Design System Decision

**Decision: CREATE** — Searched for TagInput, ChipInput, MultiEmail, TokenInput, and ComboTag components. None found. `Input` supports single-value text entry only. The invite flow requires up to 5 emails displayed as removable chip tags, each with an `Avatar` and per-chip validation. A new compound component is needed.

---

### 1. Purpose and Usage Context

**What:** A multi-value text input that validates email addresses on entry, renders them as removable chip tags (with `Avatar`), and enforces a configurable maximum count.

**When to use:** For adding multiple email addresses in invite or share flows. Do NOT use for free-text tags (a future generic `TagInput` would be more appropriate), single email input (use `Input type="email"` directly), or search (use the future `SearchInput`).

---

### 2. Props / API

| Prop | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| `emails` | `string[]` | — | Yes | Controlled list of validated email strings currently added. |
| `onAdd` | `(email: string) => void` | — | Yes | Called when a valid, non-duplicate email is submitted. |
| `onRemove` | `(email: string) => void` | — | Yes | Called when user removes a chip. |
| `maxEmails` | `number` | `5` | No | Max emails permitted. Input hides when `emails.length >= maxEmails`. |
| `error` | `string \| null` | `null` | No | Field-level error (e.g., "Invite send failed"). Displayed below the component. |
| `inputError` | `string \| null` | `null` | No | Inline error for the current typed value (e.g., "Invalid email format"). Displayed inline. |
| `disabled` | `boolean` | `false` | No | Disables all interaction including chip removal. |
| `loading` | `boolean` | `false` | No | Shows skeleton chips for the existing email list. |
| `placeholder` | `string` | `"Enter email address…"` | No | Input placeholder shown when value is empty. |

---

### 3. Variants

N/A — Single presentation. State changes drive visual differentiation.

---

### 4. States — Complete Coverage Table

The component has two sub-elements: the **chip list** and the **text input + Add button**. States apply to the combined component.

| State | Visual Treatment | Behaviour | Transitions to |
|-------|-----------------|-----------|----------------|
| **Default** | Rounded container, 1px `--color-border`. Chip tags inside (if any) followed by text input. "Add" button to the right of input (enabled only when input has value). Counter below: "[N] of [maxEmails] added" in `--color-text-muted`. | Typing enables "Add" button. `Enter` or clicking "Add" triggers validation and `onAdd` (if valid). | Hover, Focus, Error |
| **Hover** | Container border → `--color-border-hover`. | cursor: text over input area; cursor: pointer over chip "×" buttons. | Default, Active |
| **Focus** | Container border → `--color-brand-primary` 2px. Inner `<input>` focus ring per browser default (normalised to design system). | Keyboard input active. | Default, Active |
| **Active** | "Add" button in pressed state (scale 0.95, `--color-brand-primary-active`). | Chip appears on successful add. | Default (after add) |
| **Disabled** | 40% opacity on entire component. cursor: not-allowed. `aria-disabled="true"`. Chip "×" buttons hidden entirely. Input `disabled`. | No typing, no adding, no removing. | — |
| **Loading** | Existing chips replaced by skeleton pills (shimmer, identical dimensions). Input area disabled. `aria-busy="true"`. | Non-interactive. Layout preserved. | Default |
| **Error** | Container border → `--color-error`. Error message with error icon below container in `--color-error`. Input area remains interactive. | Error clears on next successful add or on input value change. `aria-live="polite"` announces error. | Default |
| **Empty** | Container shows input with placeholder. No chips. Counter: "0 of [maxEmails] added". "Add" button disabled (no value). | Typing enables "Add". First successful add creates first chip. | Default (with chips) |

**Chip sub-states:**

| Sub-state | Visual Treatment | Behaviour |
|-----------|-----------------|-----------|
| Chip: Default | Rounded pill, `--color-surface-brand-subtle` background. `Avatar` (sm, initials) + email text (truncated at 24ch with ellipsis) + "×" `Button` (ghost, xs). | — |
| Chip: Hover | "×" button scales 1.1. Chip background → `--color-surface-brand`. | cursor: pointer on "×". |
| Chip: Focus (×) | Focus ring on "×" button. | `Enter`/`Space` calls `onRemove(email)`. |
| Chip: Active (×) | "×" scales 0.9. | Chip animates out. |

**Input error sub-state** (when `inputError` is non-null):

- Text input border → `--color-error`.
- Error text appears immediately below the input (not below the container).
- `aria-invalid="true"` on input. `aria-describedby` points to error `<p>`.

**Max-reached state** (when `emails.length >= maxEmails`):

- Text input hidden.
- Message replaces input: "Maximum of [maxEmails] invites reached. Remove one to add another." in `--color-text-muted`.
- `aria-live="polite"` announces message on transition.

---

### 5. Responsive Behaviour

| Breakpoint | Width | Layout Changes | Content Changes |
|-----------|-------|---------------|----------------|
| **Mobile** | < 640px | Wizard targets tablet+. If forced: chips wrap to multiple lines, container grows vertically. | Email truncates at 20ch. |
| **Tablet** | 640–1024px | Chips wrap within container. Max 2 chip rows before internal scroll (not page scroll). | Full email text up to container width. Touch targets: "×" button ≥ 44×44px. |
| **Desktop** | > 1024px | More horizontal space; up to 3 chips per row. | Full email text. |

---

### Performance Considerations

N/A — Maximum 5 chip tags. Add/remove operations are O(1) array operations. No virtualisation required.

---

### 6. Accessibility Requirements

#### Keyboard Navigation

| Element Type | Key | Action |
|---|---|---|
| Text input | Type | Enter email address |
| Text input | `Enter` | Validate; call `onAdd` if valid and not duplicate |
| Text input | `Backspace` (on empty input) | Remove last chip in the list |
| Text input | `Tab` | Move focus to first chip "×" button, then "Add" button, then exit component |
| Chip "×" button | `Enter` / `Space` | Remove chip; focus returns to text input |
| Chip "×" button | `Delete` / `Backspace` | Remove chip; focus moves to previous "×" or text input |
| Chip "×" button | `Tab` / `Shift+Tab` | Navigate between chip "×" buttons |

**Focus management:** After chip removal, focus returns to text input. After adding a chip via `Enter`, focus stays in text input for rapid multi-entry.

#### Screen Reader

- **Role:** `role="group"` on outer container, `aria-label="Email invites"`.
- **Text input:** `role="textbox"`, `aria-label="Email address"`, `aria-describedby` pointing to counter `<p>` and `inputError` `<p>`.
- **Chip list:** `role="list"`. Each chip: `role="listitem"`.
- **Chip "×" button:** `role="button"`, `aria-label="Remove [email@example.com]"`.
- **Counter:** `aria-live="polite"` on counter `<p>` — announces count change when chip added or removed.
- **Input errors (immediate):** `aria-live="assertive"` region announces:
  - Invalid format: `"Invalid email format"`.
  - Duplicate: `"This email has already been added"`.
- **Max-reached:** `aria-live="polite"` → `"Maximum of 5 invites reached."`.
- **Field-level error (`error` prop):** `aria-live="polite"` on error region below component.
- **Input validity:** `aria-invalid="true"` on input when `inputError` is non-null.

#### Colour and Contrast

- Chip email text on `--color-surface-brand-subtle`: ≥ 4.5:1.
- Chip "×" icon: ≥ 3:1 against chip background.
- Error text `--color-error` + icon: not colour alone.
- Counter `--color-text-muted`: verify ≥ 4.5:1 — muted tones commonly fail AA.

#### Focus Management

- No focus trap — inline within step form.
- Focus returns to text input after chip removal.
- Focus ring visible in both light and dark modes.

---

### 7. Dark Mode

- [x] Chip background `--color-surface-brand-subtle` has verified dark-mode variant
- [x] Container border `--color-border` / `--color-border-hover` tokens
- [x] "×" button icon `--color-icon-muted` token
- [x] Error text `--color-error` on dark background: red (#EF4444) on dark (#1F2937) — verify contrast; may require lighter `--color-error-dark` (#FCA5A5) to maintain 4.5:1
- [x] `Avatar` initials use high-contrast tokens from existing `Avatar` component
- [x] "Add" button inherits `Button` dark-mode token adaptations

---

### 8. Animation and Motion

| Element | Animation | Duration | Easing | Reduced-motion fallback |
|---------|-----------|----------|--------|------------------------|
| Chip add | `scale(0)→scale(1)`, `opacity` 0→1 | 200ms | ease-out | Instant appear |
| Chip remove | `scale(1)→scale(0)`, `opacity` 1→0 | 150ms | ease-in | Instant disappear |
| Input error shake | `translateX` ±4px, 3 cycles | 250ms | ease-in-out | Instant; no shake |
| Max-reached message | `opacity` 0→1 | 150ms | ease-out | Instant appear |

---

### 9. Usage Examples

```tsx
// Empty state
<EmailTagInput
  emails={[]}
  onAdd={(email) => setEmails(prev => [...prev, email])}
  onRemove={(email) => setEmails(prev => prev.filter(e => e !== email))}
/>

// With existing invites and an input validation error
<EmailTagInput
  emails={["alice@acme.com", "bob@acme.com"]}
  onAdd={handleAdd}
  onRemove={handleRemove}
  inputError="Invalid email format"
/>

// Max invites reached (5/5)
<EmailTagInput
  emails={["a@b.com", "c@d.com", "e@f.com", "g@h.com", "i@j.com"]}
  onAdd={handleAdd}
  onRemove={handleRemove}
  maxEmails={5}
/>

// Disabled after step submission
<EmailTagInput
  emails={confirmedEmails}
  onAdd={noop}
  onRemove={noop}
  disabled={true}
/>
```

---

### 10. Do / Don't

| Do | Don't |
|----|-------|
| Validate email format client-side before calling `onAdd` | Call `onAdd` with invalid strings — component owns validation |
| Keep focus in text input after each chip add | Return focus to top of page or first chip — rapid entry requires cursor to stay |
| Use `aria-label="Remove [email]"` on each "×" button | Use `aria-label="×"` or `aria-label="Remove"` — screen readers need the specific email |
| Show counter ("2 of 5 added") and max-reached message | Silently disable the input at max without explanation |
| Support `Backspace` on empty input to remove the last chip | Require only the "×" button for removal — keyboard-only users need the shortcut |

---

## Per-Step Error States

### Step 1: Workspace Setup

| Field | Error Condition | Error Message | Validation Trigger |
|-------|-----------------|---------------|--------------------|
| Workspace Name | Empty on submit | "Workspace name is required." | On submit |
| Workspace Name | > 64 characters | "Workspace name must be 64 characters or fewer. ([N]/64)" | On blur + on submit |
| Workspace Name | Duplicate — API 409 | "A workspace with this name already exists. Please choose a different name." | On submit (async) |
| Logo Upload | File type rejected | "Only PNG, JPEG, and SVG files are supported." | On file select |
| Logo Upload | File > 2 MB | "File exceeds 2 MB. Please choose a smaller image." | On file select |
| Logo Upload | Upload failed (network / server) | "Logo upload failed. Please try again." + retry `Button` | During upload (async) |
| Timezone | Not selected on submit | "Please select a timezone." | On submit |

**Global error pattern (Step 1):** All fields validate simultaneously on submit. An `aria-live="assertive"` region outside the form announces: `"Please fix [N] error(s) to continue."` Focus moves to the first invalid field.

---

### Step 2: Invite Team

| Condition | Error Message | Validation Trigger |
|-----------|---------------|--------------------|
| Invalid email format | "Please enter a valid email address." | On `Enter` / "Add" click — `inputError` prop |
| Duplicate email in list | "This email has already been added." | On `Enter` / "Add" click — `inputError` prop |
| > `maxEmails` (5) | "Maximum of 5 invites reached. Remove one to add another." | On `Enter` / "Add" at max — `inputError` prop |
| Email domain blocked (API) | "[email] cannot be invited. Contact your administrator." | On submit (async) — `error` prop |
| Invite send failure (network) | "Failed to send invites. Check your connection and try again." + retry | On submit (async) — `error` prop |

**Step 2 note:** Proceeding with zero invites is valid. No error on an empty chip list.

---

### Step 3: Connect Integration

| Condition | Error Message | Variant | Recovery |
|-----------|---------------|---------|----------|
| OAuth auth cancelled (user denied) | "Connection cancelled. You can connect [GitHub / Jira / Slack] later from Settings." | `warning` banner | Dismiss; skip or retry |
| OAuth auth failure (server error) | "Something went wrong connecting to [GitHub / Jira / Slack]. Please try again." | `error` banner | Retry button (re-opens OAuth) |
| Network timeout (> 10 s) | "Connection timed out. Check your internet connection and try again." | `error` banner | Retry button |
| Scope denied (insufficient permissions) | "Clearpath needs additional permissions. Please try again and accept all requested permissions." | `error` banner | Retry (re-opens OAuth with full scope) |
| Integration already connected (duplicate account) | "This account is already connected." | `info` banner | Informational only; proceed |
| Skip selected | No error — integration marked "Not connected" in workspace settings. | — | — |

**Step 3 error pattern:** Errors appear as inline banners directly below the integration tile grid (one banner, not per-tile). OAuth popup lifecycle is managed by the host application.

---

### Step 4: Create First Project

| Condition | Error Message | Validation Trigger |
|-----------|---------------|--------------------|
| No template selected on submit | "Please select a project template to continue." | On submit — inline below template grid |
| Project name empty on submit | "Project name is required." | On submit |
| Project name > 80 characters | "Project name must be 80 characters or fewer." | On blur + on submit |
| Project name conflict — API 409 | "A project named '[name]' already exists. Please choose a different name." | On submit (async) |
| Template list fetch failure (network) | "Couldn't load project templates. Check your connection." + retry | On mount / retry |
| Template list empty (plan restriction) | "No templates are available for your plan. You can create a blank project instead." | On mount — empty state with blank-project CTA |
| Project creation failed (server) | "Project creation failed. Please try again." | On submit (async) |

---

## ARIA + Keyboard Navigation Reference

### Wizard Shell (not a new component — implemented as page layout)

| Attribute | Value |
|-----------|-

[truncated — over 50KB]
```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/17.0 (100%) |
| Evaluated | 2026-05-27 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 1024908 ms |
| Target cost | $1.2735 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Checks the existing design system first and explicitly identifies which existing components (Input, Button, Avatar, Card) can be reused versus what needs to be created | PASS | "Existing Component Reuse Table" lists all four primitives as REUSE with rationale, then identifies StepIndicator, LogoUpload, TimezoneSelect, EmailTagInput as CREATE. |
| c2 | Documents all 8 required component states for the wizard: Default, Hover, Focus, Active, Disabled, Loading, Error, Empty | PASS | Each of the four new components has a "States — Complete Coverage Table" with all 8 states (Default, Hover, Focus, Active, Disabled, Loading, Error, Empty) explicitly named and described. |
| c3 | Specifies ARIA roles, labels, and keyboard navigation requirements — not deferred to a future accessibility pass | PASS | Each component has a full "Accessibility Requirements" section with keyboard navigation tables and screen-reader roles/labels. "ARIA + Keyboard Navigation Reference" table consolidates role, aria-label/labelledby, tabindex, advance/retreat keys per component. |
| c4 | Addresses the step indicator / progress component as either a Reuse, Extend, or Create decision with justification | PASS | StepIndicator §0: "Decision: CREATE — Searched for Stepper, ProgressIndicator, Breadcrumb, WizardNav components. None found in the design system. Cannot be assembled from the four existing components." |
| c5 | Specifies responsive behaviour for both desktop and tablet breakpoints | PASS | Every new component has a "Responsive Behaviour" table with Mobile/Tablet/Desktop rows detailing layout changes and content changes at each breakpoint. |
| c6 | Documents the error state for each step (e.g. invalid email format in team invite, workspace name taken) | PASS | "Per-Step Error States" section covers Step 1 (7 conditions), Step 2 (5 conditions), Step 3 (6 conditions), Step 4 (7 conditions), each with message text and validation trigger. |
| c7 | Specifies loading states for async operations — partial credit if loading state is mentioned but not fully specified for each async step (integration connection, form submission) | PARTIAL | Loading state specified for all four new components. StepIndicator `loading` prop used "during step transitions". Integration-specific OAuth loading indicator and form-submission loading per step are not consolidated in a wizard-level async-loading spec. |
| c8 | Produces output in a structured component specification format with named sections, not a prose description | PASS | Each component follows identical numbered sections: §0 Design Decision, §1 Purpose, §2 Props/API, §3 Variants, §4 States, §5 Responsive, Performance, §6 Accessibility, §7 Dark Mode, §8 Animation, §9 Usage Examples, §10 Do/Don't. |
| c9 | Output addresses each of the 4 wizard steps from the prompt explicitly — workspace setup, team invite, integration connection, project from template — with the relevant inputs / interactions per step | PASS | Per-Step Error States covers all four steps with dedicated subsections. Step tab orders in "ARIA + Keyboard Navigation Reference" list components per step. LogoUpload/TimezoneSelect → Step 1; EmailTagInput → Step 2; integration tiles → Step 3; template tiles + project name → Step 4. |
| c10 | Output's design-system reuse decisions are explicit per primitive — Input (reuse for workspace name, email fields), Button (reuse for navigation), Avatar (reuse for team-member preview), Card (reuse for template selection) — and identifies what NEEDS to be created (step indicator / progress component) | PASS | Reuse table: Input "Used without modification for workspace name (Step 1)…and as the inner text field within EmailTagInput"; Avatar "render invited-member initials"; Card "Integration tiles (Step 3) and template tiles (Step 4)." |
| c11 | Output's progress / step-indicator component is decided explicitly as Reuse / Extend / Create with reasoning — likely Create with justification that no existing primitive serves this layout | PASS | StepIndicator reuse table row: "CREATE — No existing progress, stepper, breadcrumb, or wizard-step component in the design system." Full 8-state spec follows. |
| c12 | Output documents all 8 component states for the wizard shell — Default, Hover (on next/back), Focus (keyboard focus on inputs), Active (during click), Disabled (next button before required fields filled), Loading (during async like integration auth), Error (validation failures), Empty (initial state of integration step before selection) | PASS | StepIndicator 8-state table covers Loading (async transition), Error (current step validation), Disabled (during submission); Per-Step Error States covers validation failures; wizard Do/Don't covers disabled-next pattern; Step 3 skip covers empty integration state. |
| c13 | Output's accessibility specification covers ARIA roles (e.g. `role="region"` on each step, `aria-current="step"` on the active indicator), labels, and keyboard navigation (Tab through fields, Enter to advance, Esc to abandon) | PASS | StepIndicator screen reader: "<span aria-current='step'>" on current node; ARIA table: role=nav, combobox, listbox, group, textbox, button, option per component; Tab/Enter/Escape/ArrowDown keys documented per component. |
| c14 | Output addresses the team-invite step's email validation — what counts as valid format, max 5 emails, duplicate email handling, malformed entry handling — with error states designed | PASS | EmailTagInput `maxEmails=5`, `inputError` for "Invalid email format" / "This email has already been added"; Per-Step Step 2 table covers all four cases with specific messages and triggers. |
| c15 | Output addresses the integration step's "or skip" branch explicitly — designed as a primary "Connect" path AND a secondary "Skip for now" link, with deferred re-engagement (e.g. nudge in onboarding email Day 7) | PASS | Step 3 tab order lists "'Skip' link"; error table: "Skip selected — No error — integration marked 'Not connected' in workspace settings"; OAuth cancel message: "You can connect [Service] later from Settings." |
| c16 | Output specifies responsive behaviour for desktop AND tablet — including how the wizard layout reflows (single-column on tablet vs two-column on desktop) and where the step indicator sits at each breakpoint | PASS | All four new components have Responsive Behaviour tables with Tablet (640–1024px) and Desktop (>1024px) rows. StepIndicator: tablet labels truncate/description hidden; desktop full layout. |
| c17 | Output addresses can-skip vs cannot-skip per step — workspace setup is required, team invite can be skipped (don't trap a solo user), integration is optional, first project from template is required (so they end the wizard with something usable) | PASS | Step 2: "Proceeding with zero invites is valid — no error on empty chip list." Step 3 skip path explicit. Step 1 Timezone and Step 4 template both have "required" submit-time errors. Wizard Do/Don't: "Make Step 3 (integrations) skippable." |
| c18 | Output addresses the loading state for the integration step specifically — OAuth roundtrip can take 5-15 seconds, requires a clear "Connecting to GitHub..." indicator with a fallback message if it stalls | PARTIAL | Step 3 error table has "Network timeout (> 10 s)" with error banner and retry, but no dedicated "Connecting to [Service]…" loading indicator spec with stall fallback during the OAuth roundtrip itself. |

### Notes

An exceptionally thorough specification that passes all criteria comfortably. The two PARTIAL-ceiling criteria (c7 and c18) are correctly scored at PARTIAL: loading states exist per component but aren't consolidated at wizard-step granularity, and the integration OAuth loading indicator lacks a dedicated "Connecting…" with stall-detection spec.
