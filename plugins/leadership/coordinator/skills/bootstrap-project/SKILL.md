---
name: bootstrap-project
description: "Bootstrap or update a project with domain-specific documentation, CLAUDE.md files, and governance artifacts. Delegates to each installed agent's bootstrap skill. Idempotent — safe to re-run after adding new plugins. Use at project kickoff or when adding new agents to an existing project."
argument-hint: "[project name, or 'update' to re-run for newly installed plugins]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Bootstrap Project

Orchestrate the bootstrapping (or updating) of project documentation and governance for $ARGUMENTS. This skill does not generate domain files itself — it delegates to each installed agent's `bootstrap` skill, coordinates execution order, and produces shared artifacts. It is idempotent: re-running after installing new plugins bootstraps only what is new or updated.

## Step 1: Discover Installed Plugins

Determine which agent plugins are **installed and enabled** for this project. The coordinator does not decide what is relevant — **if a plugin is installed, it participates**.

**How to find installed plugins:**

1. Read the project's `.claude/settings.local.json` and `.claude/settings.json`. Look for the `enabledPlugins` object. Each key is `"plugin-name@marketplace": true/false`.
2. Also read the global `~/.claude/settings.json` for globally-enabled plugins (same `enabledPlugins` format).
3. Merge both lists — a plugin is installed if it appears in either file with `true`.
4. **Only use enabled plugins.** Do NOT scan the plugin cache directory (`~/.claude/plugins/cache/`). The cache contains every plugin from the marketplace, not just installed ones.

For each enabled plugin:
1. Locate its plugin directory via the marketplace source path in settings.
2. Check for a `skills/bootstrap/SKILL.md` within that plugin. Only plugins with a bootstrap skill participate.
3. Read `.claude-plugin/plugin.json` to get `name` and `version`.
4. Read the bootstrap skill's frontmatter and extract its `bootstrap-phase` value (see Step 4). Record it now — this is what slots the plugin into the right execution phase without this skill knowing the plugin exists.

Build the **installed agents list**: `{ name, version, hasBootstrap, bootstrapPhase }`.

This discovery is marketplace-agnostic. Any enabled plugin with a bootstrap skill participates — whether it ships in this marketplace or a downstream one (e.g. tortoisestack). Phase comes from the skill's own frontmatter, never from a list held here.

**Output:** Table of installed plugins, their versions, declared phase, and whether they have a bootstrap skill. Clearly separate "will bootstrap" from "installed but no bootstrap skill".

## Step 2: Read or Initialise Manifest

The manifest tracks which agents have been bootstrapped, enabling idempotent re-runs.

1. Attempt to read `.claude/bootstrap-manifest.json`.
2. If it does not exist, initialise an empty manifest structure:

```json
{
  "schemaVersion": 1,
  "projectName": "[project name]",
  "lastRun": null,
  "agents": {}
}
```

Each entry in `agents` looks like:

```json
{
  "coding-standards": {
    "version": "1.2.0",
    "bootstrappedAt": "2026-04-02T10:30:00Z",
    "files": ["docs/coding-standards/CLAUDE.md", "docs/coding-standards/linting.md"]
  }
}
```

**Output:** Manifest state — new or loaded with N existing agent entries.

## Step 2.4: Establish project context and shape

Before deriving the stack, the bootstrap needs two things it cannot get from the project name. **Never infer what the project does from its name.** "TestProject", "atlas", "phoenix" tell you nothing — a bootstrap that invents a purpose from the name writes confident fiction into every domain doc.

Ask the user directly (skip anything already given in `$ARGUMENTS` or earlier in the session):

1. **What does this project do?** One or two sentences, if known. This is the *initial context* — it flows to every agent bootstrap (Step 4) so domain docs describe the real project, not a guess. If the user doesn't know yet, record `unknown` and bootstraps leave a marked placeholder rather than invent one.
2. **What shape(s) is it?** Any that apply: `web-frontend`, `backend-service`, `library`, `cli`, `mobile`, `data-pipeline`. A repo can be more than one (a web frontend plus a backend service).
3. **What layout?** `single-package` or `monorepo`.

Record the answers — shape and layout drive which defaults apply in Step 2.5; context and shape are passed to every bootstrap in Step 4.

| Field | Value | Source |
|---|---|---|
| Context | [one-line description, or `unknown`] | user |
| Shape | [one or more of: web-frontend, backend-service, library, cli, mobile, data-pipeline] | user |
| Layout | [single-package / monorepo] | user |

**Output:** Project context, shape, and layout — confirmed with the user.

## Step 2.5: Assemble Tech Context

Derive the project's technology stack from two sources: installed agents (primary) and existing project files (override).

### Agent-to-stack mapping

Use this lookup table to derive defaults from installed language/framework agents:

| Installed agent | Languages | Test framework | Linter/formatter | Type checker | Frameworks |
|---|---|---|---|---|---|
| react-developer | TypeScript | Vitest | ESLint, Prettier | TypeScript strict | Next.js, Tailwind |
| python-developer | Python | pytest | Ruff | mypy strict | Pydantic |
| dotnet-developer | C# | xUnit | CSharpier | Roslyn analysers | Wolverine, Marten |
| php-developer | PHP | Pest | PHP-CS-Fixer | PHPStan | — |
| ai-engineer | (adds to above) | + LLM eval tests | — | — | OpenRouter |
| data-engineer | (adds to above) | + data pipeline tests | — | — | — |

If no language agents are installed, the tech context is empty — skip this step.

### Project file overrides

For existing projects (or `bootstrap update`), scan for files that indicate different choices:

| File | Signal | Override |
|---|---|---|
| `package.json` with `"jest"` | Jest installed | Test framework → Jest (not Vitest) |
| `package.json` with `"cypress"` | Cypress installed | E2E framework → Cypress (not Playwright) |
| `jest.config.*` | Jest config present | Test framework → Jest |
| `vitest.config.*` | Vitest config present | Test framework → Vitest (confirms default) |
| `pytest.ini` or `[tool.pytest]` in pyproject.toml | pytest config | Confirms default |
| `.github/workflows/*.yml` | CI exists | Note existing CI — don't duplicate |

Project file signals take precedence over agent defaults.

### Shape-conditional defaults

Org tooling conventions supply defaults, but a default only flows in when the project's **shape** (Step 2.4) calls for it. A backend service, a library, or a CLI has no frontend to host and no browser to drive — seeding its stack with Vercel and Playwright is the spurious assumption this gate exists to stop.

| Category | Default | Applies when | Source |
|---|---|---|---|
| CI/CD | GitHub Actions | always | tooling conventions |
| Code quality | SonarCloud | always | tooling conventions |
| Frontend hosting | Vercel | shape includes `web-frontend` | tooling conventions |
| E2E framework | Playwright | shape includes `web-frontend` and react-developer installed | react-developer |
| Monorepo task runner | Moon | layout is `monorepo` | devops (if installed) |

GitHub Actions and SonarCloud are org-wide for any repo, so they stay universal. Everything else is gated — if a gated default's condition isn't met, leave it out, don't list it "for completeness".

### Assemble the context table

Combine agent defaults, project overrides, and common defaults into a single table:

```markdown
### Tech Context

| Category | Value | Source |
|---|---|---|
| Languages | Python, TypeScript | python-developer, react-developer |
| Test frameworks | pytest, Vitest | python-developer, react-developer |
| E2E framework | Playwright | react-developer |
| Linters | Ruff, ESLint | python-developer, react-developer |
| Type checkers | mypy, TypeScript strict | python-developer, react-developer |
| Frameworks | Next.js, Pydantic | react-developer, python-developer |
| CI/CD | GitHub Actions | tooling conventions |
| Code quality | SonarCloud | tooling conventions |
```

**Output:** Tech context table ready for user confirmation in Step 3.

## Step 3: Determine Work Plan

Compare the installed agents list (Step 1) against the manifest (Step 2) to classify each agent:

| Classification | Condition | Action |
|---|---|---|
| **New** | Agent has a bootstrap skill but is not in the manifest | Run bootstrap skill |
| **Updated** | Agent is in the manifest but installed version > manifest version | Run bootstrap skill in **merge mode** |
| **Current** | Agent is in the manifest at the same version | **Skip** (unless user passed `--force`) |
| **No bootstrap** | Agent has no bootstrap skill | Skip — note in summary |

If `$ARGUMENTS` contains `--force`, treat all agents with bootstrap skills as **New**.

Present the tech context (from Step 2.5) and work plan together for user confirmation:

```markdown
### Tech Context (derived from installed agents + project files)

| Category | Value | Source |
|---|---|---|
| Languages | Python, TypeScript | python-developer, react-developer |
| Test frameworks | pytest, Vitest | python-developer, react-developer |
| E2E framework | Playwright | react-developer |
| Linters | Ruff, ESLint | python-developer, react-developer |
| CI/CD | GitHub Actions | tooling conventions |
| ... | ... | ... |

### Work Plan

| Agent | Status | Action |
|---|---|---|
| coding-standards | New | Bootstrap |
| architect | v1.0 → v1.2 | Merge update |
| qa-lead | v2.0 (current) | Skip |
| ... | ... | ... |

Proceed with this context and work plan? (Y / adjust / n)
```

If the user says **adjust**, ask what to change in the tech context table. Use their adjusted version for all subsequent steps. If they say **Y**, proceed with the derived context.

**Output:** Confirmed tech context + classified work plan. Wait for user confirmation before proceeding.

## Step 4: Delegate to Agent Bootstraps

Invoke each agent's `bootstrap` skill grouped by its declared **bootstrap phase**. Phases execute in sequence; agents within a phase may execute in any order.

### Phase is declared, not hardcoded

Every bootstrap skill declares which phase it belongs to in its frontmatter:

```yaml
---
name: bootstrap
bootstrap-phase: product
---
```

You already captured each plugin's `bootstrap-phase` in Step 1. Group the work plan by that value. **Never maintain a plugin→phase list in this skill.** A plugin — from this marketplace or a downstream one — controls its own placement through its frontmatter. This is the whole reason a new plugin (or a new marketplace like tortoisestack) needs no edit here to bootstrap correctly.

### Canonical phase order

This ordered list is the single source of sequencing truth. It names phases, not plugins:

| Order | Phase | Rationale |
|---|---|---|
| 1 | `foundations` | Standards and architecture inform everything else |
| 2 | `delivery` | Delivery and agile process scaffolding (RAID, ceremonies, working agreements) |
| 3 | `engineering` | Core engineering practices depend on foundations |
| 4 | `stack` | Language/framework implementations depend on standards and practices |
| 5 | `product` | Product work builds on the engineering foundation |
| 6 | `content` | Documentation follows product and engineering decisions |
| 7 | `market` | Go-to-market and support build on product definition |
| 8 | `governance` | Governance wraps around everything else |

Sort the work plan by each agent's phase rank. Run phase 1 fully, then phase 2, and so on.

### Undeclared or unknown phases (fail visibly, never drop)

A plugin must never be silently skipped because its phase is missing or unrecognised — that is the exact drift this mechanism exists to prevent. Two cases, both run, both warn:

- **No `bootstrap-phase` declared** (an older or downstream bootstrap skill predating this convention): run it in a default slot ranked **between `market` and `governance`** (so it still follows the main build and precedes governance), and print: `⚠ <plugin>: bootstrap skill declares no bootstrap-phase — running in the default slot. Add 'bootstrap-phase:' to its frontmatter to control ordering.`
- **Unrecognised `bootstrap-phase`** (declares a phase not in the canonical list — e.g. a downstream marketplace added one): run it in that same default slot, ordered alphabetically among other unknowns, and print: `⚠ <plugin>: unknown bootstrap-phase '<value>' — running in the default slot. Add '<value>' to the canonical phase order in /coordinator:bootstrap-project to place it.`

`governance` always runs last, after the default slot. The warnings are the signal that the canonical list needs a maintainer's attention — a downstream phase should be promoted into the table above.

### Passing tech context

Include the confirmed tech context table (from Step 3) in every agent bootstrap invocation. Add it as context at the start of the invocation:

> **Tech context for this project:**
>
> [paste the confirmed tech context table here]
>
> Use this to inform your framework and tooling choices. If a category is not listed, it is not relevant to this project.

Agents that don't use tech context (most domain bootstraps) will ignore it. Agents that do (qa-engineer, code-reviewer, devops, coding-standards) will use it to make informed decisions about which frameworks, linters, and CI jobs to scaffold.

### Passing project context

Along with the tech context, give every bootstrap the project context, shape, and layout from Step 2.4:

> **Project context:** [one-line description, or "unknown — do not invent one"]
> **Shape:** [shapes]   **Layout:** [layout]
>
> Author the domain docs for *this* project using the context above. **Do not infer what the project does from its name.** Where context is "unknown", leave any purpose-specific spot as a clearly marked placeholder (e.g. `[describe the project's purpose]`) rather than guessing one.

This is what stops a bootstrap turning a bare project name into invented product detail. Every domain bootstrap that writes narrative (architect, product-owner, security-engineer, the docs writers) gets the same directive, so the guess never happens in the first place.

### Invoking bootstraps

No two bootstraps write the same file — that is the design, not a thing the coordinator has to police.
No bootstrap writes a domain `CLAUDE.md` at all. Each plugin writes only its **own fragment** at
`docs/<domain>/_sections/<plugin>.md`, whether the domain has one contributing plugin or several. Those
paths are disjoint, so there is no collision to coordinate and no ordering constraint within a phase. The
coordinator assembles the domain `CLAUDE.md` from the fragments afterwards (see Step 4.5). Running
sequentially is still fine and is the simplest default, but it is no longer load-bearing for correctness.

For each agent that needs bootstrapping, in phase order:

1. **Skip** agents classified as "Current" or "No bootstrap".
2. **New agents:** Invoke the agent's `bootstrap` skill with the tech context. The agent writes only paths
   it exclusively owns — its own domain files, and its single domain fragment under
   `docs/<domain>/_sections/`. It never writes another plugin's file or the assembled domain `CLAUDE.md`.
3. **Updated agents (merge mode):** Invoke the agent's `bootstrap` skill with the tech context and a merge
   instruction. The agent reads its own files, adds missing sections, and **never overwrites or deletes**
   existing content — only appends or creates files it owns.
4. After each agent completes, record the files it created or modified (use `Glob` to diff before/after).

**Output:** Per-phase progress log showing which agents ran and what files they produced.

## Step 4.5: Assemble Shared Domain Docs

For every domain directory that contains a `_sections/` subdirectory, assemble its `CLAUDE.md` from the
fragments. This is the same pattern as the top-level `docs/CLAUDE.md` index (Step 5a) — disjoint pieces
combined by the coordinator — applied one level down, so no plugin ever has to own or merge a shared file.

For each `docs/<domain>/_sections/` found with `Glob`:

1. List the fragment files (`docs/<domain>/_sections/*.md`), sorted by filename. A numeric prefix
   (`10-architect.md`, `20-python-developer.md`) gives a deliberate order; plain `<plugin>.md` sorts
   alphabetically, which is fine when order does not matter.
2. **Before writing, guard against clobbering a hand-authored or directly-written file.** If
   `docs/<domain>/CLAUDE.md` already exists and does **not** contain the generated marker
   (`<!-- Generated by bootstrap-project from`), it was written by hand or by a plugin (possibly from another
   marketplace) that doesn't follow the fragment convention. Do not overwrite it. Print
   `⚠ <domain>: docs/<domain>/CLAUDE.md exists without the generated marker and was NOT assembled — a plugin or a person writes it directly. Resolve the conflict: convert that writer to a _sections/ fragment, or move its content into a fragment.` and skip assembly for this domain. This keeps a mixed local/downstream domain failing loudly instead of losing content.
3. Otherwise write `docs/<domain>/CLAUDE.md` as: the generated marker, a generated `# <Domain> Domain` H1 and
   one-line intro, then each fragment's contents in order (fragments are authored at H2 and below — they never
   carry their own H1). Overwriting a file that already carries the marker is expected — it is a regenerate.
   - **Display name:** `<Domain>` is the domain's display name, not always a title-cased directory. If any
     fragment in `_sections/` begins with an HTML comment `<!-- domain-title: X -->`, use `X` (e.g. `GTM`, `AI`,
     `Product Analytics`); otherwise title-case the directory name. This keeps acronym and multi-word domains
     correct without the coordinator holding a name map — the display name is data the fragment carries, the
     same single-source-of-truth principle as `bootstrap-phase`. The hint comment is invisible in rendered
     output, so it may stay in the assembled file.
4. The assembled file is generated output. Customisation goes in the fragments, not here.

```markdown
<!-- Generated by bootstrap-project from docs/<domain>/_sections/. Edit the fragments, not this file. -->
# Product Domain

Domain conventions contributed by the installed product plugins. Each section below comes from one
plugin's bootstrap fragment in `_sections/`.

<!-- contents of _sections/product-owner.md -->

<!-- contents of _sections/product-manager.md -->
```

A domain with a single fragment assembles to that one fragment under the generated header — no special
case. A new plugin joining a shared domain just drops another fragment into `_sections/`; re-running
bootstrap picks it up with no coordinator change.

**Output:** List of assembled domain docs and the fragments each was built from.

## Step 5: Generate Shared Artifacts

After all agent bootstraps complete, the coordinator generates cross-cutting artifacts that no single agent owns.

### 5a. `docs/CLAUDE.md` — Domain Index

Auto-generate an index of all active domain directories. Scan `docs/*/CLAUDE.md` with `Glob` and build:

```markdown
<!-- Generated by bootstrap-project. Auto-regenerated on each run. -->
# Project Documentation Index

This file is auto-generated by `/coordinator:bootstrap-project`. It lists all active domain documentation directories. Each domain has its own `CLAUDE.md` with domain-specific instructions.

| Domain | Path | Description |
|---|---|---|
| Architecture | `docs/architecture/CLAUDE.md` | System design, ADRs, technology choices |
| Coding Standards | `docs/coding-standards/CLAUDE.md` | Linting, formatting, review conventions |
| ... | ... | ... |

> Re-run `/coordinator:bootstrap-project update` after adding or removing plugins to refresh this index.
```

### 5b. Root `CLAUDE.md` Integration

Read the project root `CLAUDE.md`. If it exists, ensure it contains a section pointing to `docs/CLAUDE.md`. If the section is missing, append it. If `CLAUDE.md` does not exist, create it with a minimal project header and the pointer section.

The section to add or verify:

```markdown
## Documentation Index

This project uses domain-specific documentation managed by agent plugins.
See [docs/CLAUDE.md](docs/CLAUDE.md) for the full index of all domain documentation.
```

Use `Edit` to merge — never overwrite the root `CLAUDE.md`.

### 5c. `docs/tooling-register.md`

This file is the project's single source of truth for tool choices. The `tooling-conventions` rule defers to it: org defaults apply only until the register records a choice. Seed it from the confirmed tech context (Step 3) and project shape (Step 2.4), not from the full org list — a register that lists Vercel for a backend service is the same spurious assumption Step 2.5 gates against.

If the file does not exist, create it:

```markdown
<!-- Generated by bootstrap-project. Review and customize. -->
# Tooling Register

| Field | Value |
|---|---|
| Project | [project name] |
| Context | [one-line description from Step 2.4, or `unknown`] |
| Shape | [shapes from Step 2.4] |
| Layout | [single-package / monorepo] |

## Tools

| Function | Tool | Version | Notes |
|---|---|---|---|
| Language | [from tech context] | | |
| Framework | [from tech context] | | |
| Package manager | [e.g. uv] | | |
| Linter | [from tech context] | | |
| Formatter | [from tech context] | | |
| Type checker | [from tech context] | | |
| Test runner | [from tech context] | | |
| CI/CD | GitHub Actions | | org default |
| Code quality | SonarCloud | | org default |
| Container runtime | [e.g. Docker] | | |
| Error tracking | [e.g. Sentry] | | |

> Add rows only for functions this project actually has. A non-frontend project omits the frontend-hosting row; a single-package repo omits the monorepo task-runner row. Populate with your actual tool choices and keep it updated as the stack evolves.
```

Include the shape-gated rows (frontend hosting → Vercel, E2E → Playwright, monorepo task runner → Moon) only when Step 2.4's shape/layout called them in.

If the file already exists, skip.

### 5d. `docs/okrs/period-1-okrs.md`

If the file does not exist, create the placeholder:

```markdown
<!-- Generated by bootstrap-project. Review and customize. -->
# OKRs — [Project Name] — Period 1

## Objective 1: Establish project foundations

| Key Result | Target | Current | Status |
|---|---|---|---|
| KR1: CI/CD pipeline deployed and green | 100% | 0% | Not started |
| KR2: Core domain model defined and reviewed | Complete | — | Not started |
| KR3: First feature spec written and approved | Complete | — | Not started |

## Objective 2: Deliver initial value

| Key Result | Target | Current | Status |
|---|---|---|---|
| KR1: [placeholder] | [target] | — | Not started |
| KR2: [placeholder] | [target] | — | Not started |

> Customize these OKRs with the team. Use `/coordinator:define-okrs` for detailed OKR facilitation.
```

If the file exists, skip.

### 5e. `SECURITY.md`

If the file does not exist at the project root, create it following [GitHub security policy conventions](https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository):

```markdown
<!-- Generated by bootstrap-project. Review and customize. -->
# Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| latest | Yes |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **Do not** open a public issue.
2. Email [security contact] with a description of the vulnerability.
3. Include steps to reproduce, impact assessment, and any suggested fix.
4. You will receive an acknowledgement within **48 hours**.
5. We aim to provide a fix or mitigation within **7 days** for critical issues.

## Security Practices

- Dependencies are monitored for known vulnerabilities.
- Security-sensitive changes require review by the security engineer.
- See `docs/security/CLAUDE.md` for detailed security engineering practices (if available).
```

If the file exists, skip.

### 5f. `CHANGELOG.md`

If the file does not exist at the project root, create it in [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
<!-- Generated by bootstrap-project. Review and customize. -->
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project bootstrap with documentation structure.
```

If the file exists, skip.

## Step 6: Update Manifest

After all work is complete, update `.claude/bootstrap-manifest.json`:

1. For each agent that ran, record or update its entry with the current version, timestamp, and list of files created/modified.
2. Set `lastRun` to the current ISO 8601 timestamp.
3. Write the manifest using `Write`.

Ensure the `.claude/` directory exists before writing (create with `mkdir -p` if needed).

## Step 7: Output Summary

Present the final summary:

```markdown
## Bootstrap Summary — [Project Name]

### Agent Execution

| Agent | Phase | Action | Files Created | Files Merged |
|---|---|---|---|---|
| coding-standards | foundations | Bootstrapped | 3 | 0 |
| architect | foundations | Merge update | 0 | 2 |
| qa-lead | engineering | Skipped (current) | — | — |
| security-engineer | engineering | Bootstrapped | 4 | 0 |
| ... | ... | ... | ... | ... |

### Shared Artifacts

| File | Action |
|---|---|
| `docs/CLAUDE.md` | Created / Updated |
| `docs/tooling-register.md` | Created / Skipped (exists) |
| `docs/okrs/period-1-okrs.md` | Created / Skipped (exists) |
| `SECURITY.md` | Created / Skipped (exists) |
| `CHANGELOG.md` | Created / Skipped (exists) |
| `.claude/bootstrap-manifest.json` | Updated |

### Next Steps

1. Review every generated document — they are starting points, not final artifacts.
2. Populate `docs/tooling-register.md` with your actual tool choices.
3. Customise `docs/okrs/period-1-okrs.md` with the team — or run `/coordinator:define-okrs`.
4. Run `/coordinator:decompose-initiative` to break down the first initiative.
5. Update `SECURITY.md` with your actual security contact and supported versions.
6. Add newly installed plugins and re-run `/coordinator:bootstrap-project update` to bootstrap them.
```

**Output:** Summary table with next steps.

## Rules

- **Delegate, don't generate.** The coordinator never creates domain-specific files itself. Each agent's `bootstrap` skill is responsible for its own domain directory and `CLAUDE.md`. The coordinator only produces shared cross-cutting artifacts (listed in Step 5).
- **Plugin installation determines participation.** If a plugin is installed, it participates. If it is not installed, it does not. The user controls relevance by installing and uninstalling plugins.
- **Tech context flows downward.** The coordinator assembles tech context from installed agents and project files, confirms it with the user, and passes it to every agent bootstrap. Agents use it or ignore it as appropriate.
- **Never guess the project from its name.** Establish initial context, shape, and layout with the user (Step 2.4) before deriving anything. The name is a label, not a description — pass the real context down (Step 4) and have bootstraps leave a marked placeholder when context is `unknown`, never an invented purpose.
- **Defaults are shape-gated, not universal.** Only org defaults the project's shape calls for flow into the tech context and tooling register. Vercel and Playwright need a `web-frontend`; Moon needs a `monorepo`. GitHub Actions and SonarCloud are the only universal defaults. The tooling register, seeded from shape, is the per-project source of truth the conventions rule defers to.
- **Idempotent by default.** The manifest tracks what has been done. Re-runs only process new or updated agents. Use `--force` to re-run everything. Never duplicate work.
- **Safe merge, never overwrite.** When updating existing files, review existing content and merge in missing sections. Never clobber existing files. Existing content represents decisions already made.
- **Every coordinator-generated file gets the marker comment.** `<!-- Generated by bootstrap-project. Review and customize. -->` at the top. Agent-generated files follow their own conventions.
- **Respect phase order, read it from the skill.** Sequence by each bootstrap skill's declared `bootstrap-phase`, ordered by the canonical phase list in Step 4. Foundations first, governance last, so later agents can reference earlier artifacts. Never hardcode which plugin belongs to which phase — that membership lives in the plugin's own frontmatter, which is what keeps downstream marketplaces working without editing this skill.
- **Never silently skip a bootstrap.** A plugin with a missing or unknown `bootstrap-phase` still runs (in the default slot before governance) and emits a warning. Absence of a phase is a prompt to fix the frontmatter, not a reason to drop the plugin.
- **No plugin writes a domain `CLAUDE.md`; the coordinator assembles every one.** Each bootstrap writes only its own fragment under `docs/<domain>/_sections/<plugin>.md` — disjoint paths, whether the domain has one contributing plugin or five. The coordinator assembles the domain `CLAUDE.md` from the fragments in Step 4.5. There is no shared write to race on, so bootstraps need no ownership rules, no sequencing for safety, and no after-the-fact content merge. A single-plugin domain is just a domain with one fragment; adding a plugin to a domain is one more fragment. This uniformity is what removed the surprise placeholder `CLAUDE.md` files that single-plugin bootstraps used to write directly.
- **CHANGELOG.md uses [Keep a Changelog](https://keepachangelog.com/) format.** Sections: Added, Changed, Deprecated, Removed, Fixed, Security. Start with `## [Unreleased]`.
- **SECURITY.md follows [GitHub conventions](https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository).** Include supported versions, reporting process, and expected response time.
- **Always confirm the work plan.** Present the classified agent table and wait for user confirmation before executing. This prevents unexpected changes.
- **This is a starting point.** Say it in the summary. Say it in the marker comments. Every generated doc needs team review before it becomes authoritative.

## Output Format

1. Installed plugins table (Step 1).
2. Project context, shape, and layout — confirmed with the user (Step 2.4).
3. Tech context table derived from installed agents and project files (Step 2.5).
3. Combined tech context + work plan — wait for user confirmation (Step 3).
4. Per-phase execution log (Step 4).
5. Summary table of all files created/merged, agent execution results, and numbered next steps (Step 7).

## Related Skills

- `/coordinator:decompose-initiative` — after bootstrap, decompose the first initiative into workstreams.
- `/coordinator:define-okrs` — customise the generated OKR template with the team.
- `/qa-lead:test-strategy` — expand the generated test strategy with detailed test plans.
- `/architect:write-adr` — record architecture decisions as the project progresses.
- `/security-engineer:threat-model` — develop threat models referenced by the security bootstrap.
