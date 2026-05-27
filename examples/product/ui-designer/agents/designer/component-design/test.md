---
# Match the model the agent declares (sonnet) in
# plugins/product/ui-designer/agents/designer.md. The runner otherwise
# falls back to the harness default (Haiku), which is not what the
# agent is designed to run on.
target-model: claude-sonnet-4-6
---

# Test: Component design

Scenario: A product team needs a multi-step onboarding wizard designed for their B2B SaaS product. The designer agent is asked to produce a component specification.

## Prompt


We need to design a multi-step onboarding wizard for Clearpath, our B2B project management tool. New users need to:
1. Set up their workspace (name, logo, timezone)
2. Invite team members (up to 5 emails)
3. Connect their first integration (GitHub, Jira, or Slack — or skip)
4. Create their first project from a template

We have a design system with existing Input, Button, Avatar, and Card components. The wizard should work on desktop and tablet. Can you design this?

Output structure:

- **Existing component reuse table** at top with columns `Component | Decision (REUSE / EXTEND / CREATE) | Rationale`. Cover Input (REUSE), Button (REUSE), Avatar (REUSE — for invited team members), Card (REUSE — for integration tiles), Stepper/ProgressIndicator (decide REUSE / EXTEND / CREATE — most likely CREATE since it's not in the existing system).
- **8 component states for EVERY new component** — not just one diagram, repeat for each new component. The 8 states: Default, Hover (cursor over interactive area), Focus (keyboard focus ring), Active (pressed/clicked), Disabled, Loading (async work in progress), Error (validation failure or operation error), Empty (no data yet — e.g. no team members invited).
- **Per-step error states** explicitly: Step 1 (workspace name validation: empty, too long, duplicate), Step 2 (invalid email format, duplicate email, too many invites), Step 3 (integration auth failure, network timeout, scope-denied), Step 4 (template fetch failure, project name conflict).
- **ARIA + keyboard navigation**: each new component documents `role`, `aria-label` / `aria-labelledby`, `tabindex`, and which keys advance/retreat (Tab, Shift+Tab, Enter, Esc).
- **Step indicator decision**: explicitly state REUSE/EXTEND/CREATE for the progress component. If CREATE, document the 8 states for it too.

A few specifics for the response:

- Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
- Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
- For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
- When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
- Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Criteria


- [ ] PASS: Checks the existing design system first and explicitly identifies which existing components (Input, Button, Avatar, Card) can be reused versus what needs to be created
- [ ] PASS: Documents all 8 required component states for the wizard: Default, Hover, Focus, Active, Disabled, Loading, Error, Empty
- [ ] PASS: Specifies ARIA roles, labels, and keyboard navigation requirements — not deferred to a future accessibility pass
- [ ] PASS: Addresses the step indicator / progress component as either a Reuse, Extend, or Create decision with justification
- [ ] PASS: Specifies responsive behaviour for both desktop and tablet breakpoints
- [ ] PASS: Documents the error state for each step (e.g. invalid email format in team invite, workspace name taken)
- [ ] PARTIAL: Specifies loading states for async operations — partial credit if loading state is mentioned but not fully specified for each async step (integration connection, form submission)
- [ ] PASS: Produces output in a structured component specification format with named sections, not a prose description

## Output expectations

- [ ] PASS: Output addresses each of the 4 wizard steps from the prompt explicitly — workspace setup, team invite, integration connection, project from template — with the relevant inputs / interactions per step
- [ ] PASS: Output's design-system reuse decisions are explicit per primitive — Input (reuse for workspace name, email fields), Button (reuse for navigation), Avatar (reuse for team-member preview), Card (reuse for template selection) — and identifies what NEEDS to be created (step indicator / progress component)
- [ ] PASS: Output's progress / step-indicator component is decided explicitly as Reuse / Extend / Create with reasoning — likely Create with justification that no existing primitive serves this layout
- [ ] PASS: Output documents all 8 component states for the wizard shell — Default, Hover (on next/back), Focus (keyboard focus on inputs), Active (during click), Disabled (next button before required fields filled), Loading (during async like integration auth), Error (validation failures), Empty (initial state of integration step before selection)
- [ ] PASS: Output's accessibility specification covers ARIA roles (e.g. `role="region"` on each step, `aria-current="step"` on the active indicator), labels, and keyboard navigation (Tab through fields, Enter to advance, Esc to abandon)
- [ ] PASS: Output addresses the team-invite step's email validation — what counts as valid format, max 5 emails, duplicate email handling, malformed entry handling — with error states designed
- [ ] PASS: Output addresses the integration step's "or skip" branch explicitly — designed as a primary "Connect" path AND a secondary "Skip for now" link, with deferred re-engagement (e.g. nudge in onboarding email Day 7)
- [ ] PASS: Output specifies responsive behaviour for desktop AND tablet — including how the wizard layout reflows (single-column on tablet vs two-column on desktop) and where the step indicator sits at each breakpoint
- [ ] PASS: Output addresses can-skip vs cannot-skip per step — workspace setup is required, team invite can be skipped (don't trap a solo user), integration is optional, first project from template is required (so they end the wizard with something usable)
- [ ] PARTIAL: Output addresses the loading state for the integration step specifically — OAuth roundtrip can take 5-15 seconds, requires a clear "Connecting to GitHub..." indicator with a fallback message if it stalls
