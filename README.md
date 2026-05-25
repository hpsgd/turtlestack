# Turtlestack

A plugin marketplace for Claude Code. Agents, skills, rules, and conventions that work together as a virtual team.

<p align="center">
  <img src="assets/logo.png" alt="Turtlestack logo" width="256">
</p>

- [Quick start](#quick-start)
  - [Customisation](#customisation)
  - [JSON shortcut](#json-shortcut)
  - [Bootstrap a project](#bootstrap-a-project)
- [Thinking and learning](#thinking-and-learning)
- [Plugins](#plugins)
  - [Practices](#practices)
    - [Coding Standards](#coding-standards)
    - [Plugin Curator](#plugin-curator)
    - [Publishing](#publishing)
    - [Security Compliance](#security-compliance)
    - [Technology Stacks](#technology-stacks)
    - [Thinking](#thinking)
    - [Tooling](#tooling)
    - [Writing Style](#writing-style)
  - [Research](#research)
    - [Analyst](#analyst)
    - [Investigator](#investigator)
    - [Dossier](#dossier)
    - [Web Tools](#web-tools)
  - [Leadership](#leadership)
    - [Coordinator](#coordinator)
    - [CPO](#cpo)
    - [CTO](#cto)
    - [GRC Lead](#grc-lead)
  - [Product](#product)
    - [Customer Success](#customer-success)
    - [Developer Docs Writer](#developer-docs-writer)
    - [GTM](#gtm)
    - [Internal Docs Writer](#internal-docs-writer)
    - [Product Owner](#product-owner)
    - [Support](#support)
    - [UI Designer](#ui-designer)
    - [User Docs Writer](#user-docs-writer)
    - [UX Researcher](#ux-researcher)
  - [Engineering](#engineering)
    - [AI Engineer](#ai-engineer)
    - [Architect](#architect)
    - [Billing Engineer](#billing-engineer)
    - [Code Reviewer](#code-reviewer)
    - [Data Engineer](#data-engineer)
    - [DevOps](#devops)
    - [.NET Developer](#net-developer)
    - [Performance Engineer](#performance-engineer)
    - [PHP Developer](#php-developer)
    - [Python Developer](#python-developer)
    - [QA Engineer](#qa-engineer)
    - [QA Lead](#qa-lead)
    - [React Developer](#react-developer)
    - [Release Manager](#release-manager)
    - [Security Engineer](#security-engineer)
- [Under the hood](#under-the-hood)
  - [How rules and skills work](#how-rules-and-skills-work)
  - [The learning system (technical detail)](#the-learning-system-technical-detail)
  - [Evaluation framework](#evaluation-framework)
  - [Creating a new plugin](#creating-a-new-plugin)
  - [Troubleshooting](#troubleshooting)
- [Complementary plugins](#complementary-plugins)
- [Acknowledgements](#acknowledgements)

## Quick start

### Requirements

Most plugins need nothing beyond Claude Code itself. A few — `publishing`, `coordinator`'s meeting PDF skill, and `web-tools` — shell out to native tools (PDF rendering, headless Chromium, `rmapi`). Those wrap the tooling in Docker images that build on first run. If you plan to use any of them, install Docker Desktop (macOS/Windows) or the docker engine (Linux). No other host dependencies — no `pip install`, no `shot-scraper install`, no manual binary downloads.

### 1. Add the marketplace

```
/plugin marketplace add hpsgd/turtlestack
```

### 2. Install what you need

Start with the core plugins (rules, thinking skills, and code review), then add agents for your stack:

```
/plugin install coding-standards@turtlestack
/plugin install writing-style@turtlestack
/plugin install security-compliance@turtlestack
/plugin install thinking@turtlestack
/plugin install tooling@turtlestack
/plugin install code-reviewer@turtlestack
/plugin install ai-engineer@turtlestack
```

Add a technology stack if relevant:

```
/plugin install dotnet-stack@turtlestack
/plugin install nextjs-stack@turtlestack
/plugin install php-stack@turtlestack
/plugin install python-stack@turtlestack
```

Then reload:

```
/reload-plugins
```

Browse the full [plugin list](#plugins) below to see what else is available.

### Customisation

**Per-project overrides.** Create your own `.claude/rules/` files. Project-level rules take precedence over marketplace rules.

**Disabling a plugin.** Set it to `false` in `.claude/settings.json`:

```json
{
  "enabledPlugins": {
    "writing-style@turtlestack": false
  }
}
```

**Local overrides (not committed).** Use `.claude/settings.local.json` for personal preferences that shouldn't affect the team.

### JSON shortcut

<details>
<summary>Copy this to install everything at once</summary>

```json
{
  "enabledPlugins": {
    "coding-standards@turtlestack": true,
    "writing-style@turtlestack": true,
    "security-compliance@turtlestack": true,
    "thinking@turtlestack": true,
    "tooling@turtlestack": true,
    "code-reviewer@turtlestack": true,
    "dotnet-stack@turtlestack": true,
    "nextjs-stack@turtlestack": true,
    "php-stack@turtlestack": true,
    "python-stack@turtlestack": true,
    "plugin-curator@turtlestack": true,
    "publishing@turtlestack": true,
    "coordinator@turtlestack": true,
    "cpo@turtlestack": true,
    "product-owner@turtlestack": true,
    "ui-designer@turtlestack": true,
    "ux-researcher@turtlestack": true,
    "user-docs-writer@turtlestack": true,
    "developer-docs-writer@turtlestack": true,
    "internal-docs-writer@turtlestack": true,
    "gtm@turtlestack": true,
    "support@turtlestack": true,
    "customer-success@turtlestack": true,
    "grc-lead@turtlestack": true,
    "cto@turtlestack": true,
    "architect@turtlestack": true,
    "billing-engineer@turtlestack": true,
    "react-developer@turtlestack": true,
    "dotnet-developer@turtlestack": true,
    "php-developer@turtlestack": true,
    "python-developer@turtlestack": true,
    "ai-engineer@turtlestack": true,
    "qa-lead@turtlestack": true,
    "qa-engineer@turtlestack": true,
    "release-manager@turtlestack": true,
    "performance-engineer@turtlestack": true,
    "devops@turtlestack": true,
    "security-engineer@turtlestack": true,
    "data-engineer@turtlestack": true,
    "analyst@turtlestack": true,
    "investigator@turtlestack": true,
    "web-tools@turtlestack": true
  }
}
```

</details>

### Bootstrap a project

After installing plugins, scaffold your project with domain-specific docs:

```
/coordinator:bootstrap-project my-project
```

This delegates to each installed agent's bootstrap skill, creating a `docs/` structure with per-domain documentation and conventions. Safe to re-run after adding new plugins.

## Thinking and learning

The `thinking` plugin is the one to install first. It gives Claude structured ways to reason through problems and a learning loop that gets better the more you use it.

**Reasoning skills** help with specific situations. `/thinking:first-principles` when you're stuck on a design decision. `/thinking:council` when you need multiple perspectives on a trade-off. `/thinking:red-team` to stress-test a plan before committing. `/thinking:isc` at the start of any task to make sure nothing gets missed. Claude auto-invokes these when the context matches, or you can call them directly.

**The learning loop** watches how you work across sessions. When you correct Claude ("no, not like that" or "stop doing X"), the system spots the pattern. After enough evidence, it writes a rule so the same mistake doesn't happen again. Run `/thinking:retrospective` to review what it's learned, or let it run automatically at the start of each session.

**Wisdom frames** are the long-term version. Patterns that have held up across many sessions get crystallised into reusable knowledge via `/thinking:wisdom`. Think of it as the difference between "I learned this yesterday" and "I've seen this enough times to trust it."

See the [thinking plugin](#thinking) section below for the full skill list, or the [technical detail](#the-learning-system-technical-detail) for how the hooks and classifiers work.

## Plugins

### Practices

#### Coding Standards

TypeScript, .NET, Python conventions, git workflow, testing, architecture, AI steering. Installed as rules that apply to every session.

```
/plugin install coding-standards@turtlestack
```

**Rules:**

| Rule | Description |
|---|---|
| [ai-steering](plugins/practices/coding-standards/rules/ai-steering.md) | Behavioral rules for how Claude should approach work |
| [architecture](plugins/practices/coding-standards/rules/architecture.md) | General architecture principles |
| [dotnet](plugins/practices/coding-standards/rules/dotnet.md) | .NET / C# language conventions and project patterns |
| [event-sourcing](plugins/practices/coding-standards/rules/event-sourcing.md) | Event Sourcing, CQRS, and DDD patterns |
| [git-and-ci](plugins/practices/coding-standards/rules/git-and-ci.md) | Git workflow, branching, CI/CD, and commit conventions |
| [php](plugins/practices/coding-standards/rules/php.md) | PHP language conventions and engineering standards |
| [python](plugins/practices/coding-standards/rules/python.md) | Python language conventions and engineering standards |
| [spec-driven-development](plugins/practices/coding-standards/rules/spec-driven-development.md) | Specs before code, acceptance criteria before implementation |
| [strict-validation](plugins/practices/coding-standards/rules/strict-validation.md) | Strict validation principles |
| [review-conventions](plugins/practices/coding-standards/rules/review-conventions.md) | Review workflow conventions and inline decision markers |
| [testing](plugins/practices/coding-standards/rules/testing.md) | General testing principles |
| [typescript](plugins/practices/coding-standards/rules/typescript.md) | TypeScript coding conventions |

| Skill | Description | Example |
|---|---|---|
| [review-typescript](plugins/practices/coding-standards/skills/review-typescript/SKILL.md) | TypeScript/Next.js code review | [TS review](examples/practices/coding-standards/skills/review-typescript/result.md) |
| [review-dotnet](plugins/practices/coding-standards/skills/review-dotnet/SKILL.md) | .NET/C# code review | [.NET review](examples/practices/coding-standards/skills/review-dotnet/result.md) |
| [review-python](plugins/practices/coding-standards/skills/review-python/SKILL.md) | Python code review | [Python review](examples/practices/coding-standards/skills/review-python/result.md) |
| [review-php](plugins/practices/coding-standards/skills/review-php/SKILL.md) | PHP code review | [PHP review](examples/practices/coding-standards/skills/review-php/result.md) |
| [review-git](plugins/practices/coding-standards/skills/review-git/SKILL.md) | Git conventions review | [Git review](examples/practices/coding-standards/skills/review-git/result.md) |
| [review-go](plugins/practices/coding-standards/skills/review-go/SKILL.md) | Go code review | — |
| [review-standards](plugins/practices/coding-standards/skills/review-standards/SKILL.md) | Cross-cutting quality review | [Standards review](examples/practices/coding-standards/skills/review-standards/result.md) |

#### [Plugin Curator](plugins/practices/plugin-curator/agents/plugin-curator.md)

Marketplace maintenance. Creates agents and skills from templates, audits for structural consistency, runs the evaluation framework. See [audit request example](examples/practices/plugin-curator/agents/plugin-curator/audit-request/result.md).

Also includes the [evaluator](plugins/practices/plugin-curator/agents/evaluator.md) agent, which runs test cases against plugin definitions and produces pass/fail verdicts.

```
/plugin install plugin-curator@turtlestack
```

**Rules:**

| Rule | Description |
|---|---|
| [hook-design](plugins/practices/plugin-curator/rules/hook-design.md) | Hook design principles: structural checks, silent on pass, actionable on block |

| Skill | Description | Example |
|---|---|---|
| [create-agent](plugins/practices/plugin-curator/skills/create-agent/SKILL.md) | Create agent from template | [Agent creation](examples/practices/plugin-curator/skills/create-agent/result.md) |
| [create-skill](plugins/practices/plugin-curator/skills/create-skill/SKILL.md) | Create skill from template | [Skill creation](examples/practices/plugin-curator/skills/create-skill/result.md) |
| [audit-agent](plugins/practices/plugin-curator/skills/audit-agent/SKILL.md) | Audit agent against template | [Agent audit](examples/practices/plugin-curator/skills/audit-agent/result.md) |
| [audit-skill](plugins/practices/plugin-curator/skills/audit-skill/SKILL.md) | Audit skill against template | [Skill audit](examples/practices/plugin-curator/skills/audit-skill/result.md) |
| [evaluate](plugins/practices/plugin-curator/skills/evaluate/SKILL.md) | Run test cases against plugin definitions | N/A |

#### Publishing

Brand-styled markdown-to-PDF rendering for reports, assessments, and briefs. A4 with hps.gd typography (Mona Sans, Inter) and palette. Optional cover page from YAML frontmatter. Pure-Python toolchain (xhtml2pdf + python-markdown), no system libraries required.

```
/plugin install publishing@turtlestack
```

**Skills:**

| Skill | Description |
|---|---|
| [write-document-pdf](plugins/practices/publishing/skills/write-document-pdf/SKILL.md) | Render a markdown file as a brand-styled A4 PDF. Use `--style <name>` for a bundled stylesheet or `--css <path>` for a project-specific CSS file. |

The brand fonts and logos under `plugins/practices/publishing/assets/` are the single source of truth for hps.gd brand assets across PDF renderers — `/coordinator:write-meeting-pdf` reads from the same location.

#### Security Compliance

Security baseline rules and deep audit capability.

```
/plugin install security-compliance@turtlestack
```

**Rules:**

| Rule | Description |
|---|---|
| [security-baseline](plugins/practices/security-compliance/rules/security-baseline.md) | Security baseline — always-on rules for writing secure code |

| Skill | Description | Example |
|---|---|---|
| [security-audit](plugins/practices/security-compliance/skills/security-audit/SKILL.md) | Security compliance audit | [Security audit](examples/practices/security-compliance/skills/security-audit/result.md) |

#### Technology Stacks

Framework-specific conventions. Install what matches your project.

```
/plugin install dotnet-stack@turtlestack    # JasperFx (Wolverine/Marten) on .NET
/plugin install nextjs-stack@turtlestack    # Next.js, React, Vercel
/plugin install php-stack@turtlestack       # EventSauce + symfony/messenger
/plugin install python-stack@turtlestack    # Django, python-eventsourcing
```

**dotnet-stack rules:**

| Rule | Description |
|---|---|
| [jasperfx](plugins/practices/dotnet-stack/rules/jasperfx.md) | JasperFx ecosystem conventions — Wolverine command bus and Marten event store |

**nextjs-stack rules:**

| Rule | Description |
|---|---|
| [nextjs](plugins/practices/nextjs-stack/rules/nextjs.md) | Next.js and React conventions |

**php-stack rules:**

| Rule | Description |
|---|---|
| [eventsauce-and-messenger](plugins/practices/php-stack/rules/eventsauce-and-messenger.md) | EventSauce + symfony/messenger conventions for event-sourced PHP |

#### Thinking

Structured reasoning, learning system, project health checks. See [Thinking and learning](#thinking-and-learning) for the overview.

```
/plugin install thinking@turtlestack
```

**Rules:**

| Rule | Description |
|---|---|
| [session-discipline](plugins/practices/thinking/rules/session-discipline.md) | Session focus, scope-drift detection, and deferred work markers |
| [mechanism-design](plugins/practices/thinking/rules/mechanism-design.md) | Design recurring actions as mechanisms with triggers and failure handling |

| Skill | Description | Example |
|---|---|---|
| [algorithm](plugins/practices/thinking/skills/algorithm/SKILL.md) | Seven-phase systematic execution | [Algorithm run](examples/practices/thinking/skills/algorithm/result.md) |
| [isc](plugins/practices/thinking/skills/isc/SKILL.md) | Decompose into verifiable criteria | [ISC decomposition](examples/practices/thinking/skills/isc/result.md) |
| [first-principles](plugins/practices/thinking/skills/first-principles/SKILL.md) | Deconstruct to fundamentals and rebuild | [First principles](examples/practices/thinking/skills/first-principles/result.md) |
| [council](plugins/practices/thinking/skills/council/SKILL.md) | Multi-expert structured debate | [Council debate](examples/practices/thinking/skills/council/result.md) |
| [red-team](plugins/practices/thinking/skills/red-team/SKILL.md) | Adversarial stress-testing | [Red team](examples/practices/thinking/skills/red-team/result.md) |
| [creative](plugins/practices/thinking/skills/creative/SKILL.md) | Divergent ideation | [Creative ideation](examples/practices/thinking/skills/creative/result.md) |
| [iterative-depth](plugins/practices/thinking/skills/iterative-depth/SKILL.md) | Multi-lens analysis | [Multi-lens analysis](examples/practices/thinking/skills/iterative-depth/result.md) |
| [scientific-method](plugins/practices/thinking/skills/scientific-method/SKILL.md) | Hypothesis-driven investigation | [Scientific method](examples/practices/thinking/skills/scientific-method/result.md) |
| [retrospective](plugins/practices/thinking/skills/retrospective/SKILL.md) | Session analysis and learning extraction | [Retrospective](examples/practices/thinking/skills/retrospective/result.md) |
| [learning](plugins/practices/thinking/skills/learning/SKILL.md) | Capture a learning manually | [Learning capture](examples/practices/thinking/skills/learning/result.md) |
| [wisdom](plugins/practices/thinking/skills/wisdom/SKILL.md) | Crystallised pattern library | [Wisdom frame](examples/practices/thinking/skills/wisdom/result.md) |
| [health-check](plugins/practices/thinking/skills/health-check/SKILL.md) | Project setup audit | [Health check](examples/practices/thinking/skills/health-check/result.md) |
| [review-settings](plugins/practices/thinking/skills/review-settings/SKILL.md) | Settings.json audit | [Settings audit](examples/practices/thinking/skills/review-settings/result.md) |
| [reconcile-rules](plugins/practices/thinking/skills/reconcile-rules/SKILL.md) | Deduplicate learned vs marketplace rules | [Rule reconciliation](examples/practices/thinking/skills/reconcile-rules/result.md) |
| [propose-improvement](plugins/practices/thinking/skills/propose-improvement/SKILL.md) | PR against marketplace from learned pattern | [Improvement PR](examples/practices/thinking/skills/propose-improvement/result.md) |
| [handoff](plugins/practices/thinking/skills/handoff/SKILL.md) | Write or resume a session handoff doc | — |

#### Tooling

Organisational tooling conventions. Ensures agents reference the correct tools.

```
/plugin install tooling@turtlestack
```

**Rules:**

| Rule | Description |
|---|---|
| [tooling-conventions](plugins/practices/tooling/rules/tooling-conventions.md) | Organisational tooling conventions — which tool for which function |

#### Writing Style

AI tell avoidance, banned vocabulary, sentence structure, markdown formatting, personal voice.

```
/plugin install writing-style@turtlestack
```

**Rules:**

| Rule | Description |
|---|---|
| [tone-and-voice](plugins/practices/writing-style/rules/tone-and-voice.md) | Writing rules and AI tell avoidance |
| [personal-voice](plugins/practices/writing-style/rules/personal-voice.md) | Personal writing voice patterns and habits |
| [markdown-formatting](plugins/practices/writing-style/rules/markdown-formatting.md) | Markdown formatting conventions and GFM compliance |

| Skill | Description | Example |
|---|---|---|
| [style-guide](plugins/practices/writing-style/skills/style-guide/SKILL.md) | Writing style review and rewrite | [Style review](examples/practices/writing-style/skills/style-guide/result.md) |

### Research

#### Analyst

Web research, company analysis, content analysis. Three agents in one plugin.

```
/plugin install analyst@turtlestack
```

**Rules:**

| Rule | Description |
|---|---|
| [source-citations](plugins/research/analyst/rules/source-citations.md) | Source citation quality — every cited source must be verifiable |

**[Open-source researcher](plugins/research/analyst/agents/open-source-researcher.md)** — web research with source attribution (see [topic research example](examples/research/analyst/agents/open-source-researcher/topic-research/result.md)):

| Skill | Description | Example |
|---|---|---|
| [web-research](plugins/research/analyst/skills/web-research/SKILL.md) | Topic research with sources | [Web research](examples/research/analyst/skills/web-research/result.md) |
| [deep-research](plugins/research/analyst/skills/deep-research/SKILL.md) | Multi-pass deep research | [Deep research](examples/research/analyst/skills/deep-research/result.md) |

**[Business analyst](plugins/research/analyst/agents/business-analyst.md)** — company and market research (see [boundary individual example](examples/research/analyst/agents/business-analyst/boundary-individual/result.md)):

| Skill | Description | Example |
|---|---|---|
| [company-lookup](plugins/research/analyst/skills/company-lookup/SKILL.md) | Company profile from public sources | [Company lookup](examples/research/analyst/skills/company-lookup/result.md) |
| [competitive-analysis](plugins/research/analyst/skills/competitive-analysis/SKILL.md) | Competitive landscape mapping | [Competitive mapping](examples/research/analyst/skills/competitive-analysis/result.md) |
| [market-sizing](plugins/research/analyst/skills/market-sizing/SKILL.md) | TAM/SAM/SOM market sizing | [Market sizing](examples/research/analyst/skills/market-sizing/result.md) |

**[Content analyst](plugins/research/analyst/agents/content-analyst.md)** — content analysis and framing assessment (see [content evaluation example](examples/research/analyst/agents/content-analyst/content-evaluation/result.md)):

| Skill | Description | Example |
|---|---|---|
| [content-analysis](plugins/research/analyst/skills/content-analysis/SKILL.md) | Article/document analysis | [Content analysis](examples/research/analyst/skills/content-analysis/result.md) |
| [source-credibility](plugins/research/analyst/skills/source-credibility/SKILL.md) | Source credibility assessment | [Source credibility](examples/research/analyst/skills/source-credibility/result.md) |

#### Investigator

OSINT investigation with mandatory ethical authorisation gates.

```
/plugin install investigator@turtlestack
```

**Rules:**

| Rule | Description |
|---|---|
| [source-citations](plugins/research/investigator/rules/source-citations.md) | Source citation quality — every cited source must be verifiable |

**[OSINT analyst](plugins/research/investigator/agents/osint-analyst.md)** — domain and infrastructure intelligence (see [domain investigation example](examples/research/investigator/agents/osint-analyst/domain-investigation/result.md)):

| Skill | Description | Example |
|---|---|---|
| [domain-intel](plugins/research/investigator/skills/domain-intel/SKILL.md) | Domain/DNS investigation | [Domain intel](examples/research/investigator/skills/domain-intel/result.md) |
| [ip-intel](plugins/research/investigator/skills/ip-intel/SKILL.md) | IP and infrastructure analysis | [IP intel](examples/research/investigator/skills/ip-intel/result.md) |
| [entity-footprint](plugins/research/investigator/skills/entity-footprint/SKILL.md) | Entity digital footprint | [Entity footprint](examples/research/investigator/skills/entity-footprint/result.md) |

**[Investigator](plugins/research/investigator/agents/investigator.md)** — people and entity investigation, authorisation required (see [legitimate investigation example](examples/research/investigator/agents/investigator/legitimate-investigation/result.md)):

| Skill | Description | Example |
|---|---|---|
| [people-lookup](plugins/research/investigator/skills/people-lookup/SKILL.md) | People search from public sources | [People lookup](examples/research/investigator/skills/people-lookup/result.md) |
| [identity-verification](plugins/research/investigator/skills/identity-verification/SKILL.md) | Identity verification | [Identity check](examples/research/investigator/skills/identity-verification/result.md) |
| [social-media-footprint](plugins/research/investigator/skills/social-media-footprint/SKILL.md) | Social media presence mapping | [Social footprint](examples/research/investigator/skills/social-media-footprint/result.md) |
| [public-records](plugins/research/investigator/skills/public-records/SKILL.md) | Public records search | [Public records](examples/research/investigator/skills/public-records/result.md) |
| [corporate-ownership](plugins/research/investigator/skills/corporate-ownership/SKILL.md) | Beneficial ownership investigation | [Ownership trace](examples/research/investigator/skills/corporate-ownership/result.md) |

#### Dossier

End-to-end research campaigns and report consolidation. Drives multiple research skills against a single target, then compiles the outputs into a single brand-styled PDF.

```
/plugin install dossier@turtlestack
```

**[Dossier driver](plugins/research/dossier/agents/dossier.md)** — orchestrates an end-to-end campaign on one target (person, company, or domain), dispatches the right research skills, then consolidates their reports.

| Skill | Description | Example |
|---|---|---|
| [consolidate](plugins/research/dossier/skills/consolidate/SKILL.md) | Gather every conforming research report under an engagement directory into one `DOSSIER.md` plus brand-styled PDF | — |

`dossier` and the other research plugins (`analyst`, `investigator`) share `research-conventions` as an internal dependency — installed automatically; you don't install it directly.

#### Web Tools

Tools for fetching and archiving web content during research. Used by research skills and agents that need page content (for analysis) or PDF snapshots (for evidence).

```
/plugin install web-tools@turtlestack
```

| Skill | Description | Example |
|---|---|---|
| [content-retrieval](plugins/research/web-tools/skills/content-retrieval/SKILL.md) | Four-tier URL retrieval (WebFetch → curl → Playwright → human escalation) — returns page text/HTML for analysis | [URL retrieval](examples/research/web-tools/skills/content-retrieval/result.md) |
| [web-snapshot](plugins/research/web-tools/skills/web-snapshot/SKILL.md) | Save a page as a rendered PDF using Playwright/Chromium (runs in Docker) — for evidence archival in sources registers | — |

### Leadership

#### [Coordinator](plugins/leadership/coordinator/agents/coordinator.md)

CEO/founder proxy. Decomposes cross-team initiatives, coordinates CPO and CTO, resolves conflicts, defines OKRs. Produces dispatch plans rather than doing the work directly. See [initiative decomposition example](examples/leadership/coordinator/agents/coordinator/initiative-decomposition/result.md).

```
/plugin install coordinator@turtlestack
```

**Rules:**

| Rule | Description |
|---|---|
| [delegate-first](plugins/leadership/coordinator/rules/delegate-first.md) | Before starting any non-trivial work, determine which specialist agent should handle it and delegate |
| [coordination-rule](plugins/leadership/coordinator/rules/coordination-rule.md) | Delegate non-trivial work to specialist agents instead of doing it yourself |

The coordinator owns the org structure:

```
Human (CEO/Founder)
└── Coordinator
    ├── CPO (product, design, content, GTM, support, customer-success)
    ├── CTO (architecture, development, QA, DevOps, security, data)
    ├── GRC Lead (governance, risk, compliance)
    └── Research (cross-cutting)
```

| Skill | Description | Example |
|---|---|---|
| [decompose-initiative](plugins/leadership/coordinator/skills/decompose-initiative/SKILL.md) | Break an initiative into team workstreams with dependencies | [Initiative breakdown](examples/leadership/coordinator/skills/decompose-initiative/result.md) |
| [define-okrs](plugins/leadership/coordinator/skills/define-okrs/SKILL.md) | Company OKRs cascading to team objectives | [OKR definition](examples/leadership/coordinator/skills/define-okrs/result.md) |
| [write-spec](plugins/leadership/coordinator/skills/write-spec/SKILL.md) | Cross-team spec with Gherkin acceptance criteria | [Spec authoring](examples/leadership/coordinator/skills/write-spec/result.md) |
| [write-meeting-agenda](plugins/leadership/coordinator/skills/write-meeting-agenda/SKILL.md) | Synthesise the session discussion into a structured meeting agenda | [Agenda writing](examples/leadership/coordinator/skills/write-meeting-agenda/result.md) |
| [write-meeting-qanda](plugins/leadership/coordinator/skills/write-meeting-qanda/SKILL.md) | Expand an agenda into a Q-and-A document with talking points, questions, notes capture | [Q-and-A writing](examples/leadership/coordinator/skills/write-meeting-qanda/result.md) |
| [write-meeting-pdf](plugins/leadership/coordinator/skills/write-meeting-pdf/SKILL.md) | Render the Q-and-A document as a printable PDF for tablet note-taking (Remarkable Paper Pro) | [PDF rendering](examples/leadership/coordinator/skills/write-meeting-pdf/result.md) |
| [bootstrap-project](plugins/leadership/coordinator/skills/bootstrap-project/SKILL.md) | Scaffold docs via installed agents | [Bootstrap project](examples/leadership/coordinator/skills/bootstrap-project/result.md) |

#### [CPO](plugins/leadership/cpo/agents/cpo.md)

Coordinates product, design, content, GTM, and support teams. Routes work to the right specialist. No skills — coordination only. See [product prioritisation example](examples/leadership/cpo/agents/cpo/product-prioritisation/result.md).

```
/plugin install cpo@turtlestack
```

#### [CTO](plugins/leadership/cto/agents/cto.md)

Coordinates architecture, development, QA, DevOps, security, and data engineering. Routes technical work. No skills — coordination only. See [technical decision example](examples/leadership/cto/agents/cto/technical-decision/result.md).

```
/plugin install cto@turtlestack
```

#### [GRC Lead](plugins/leadership/grc-lead/agents/grc-lead.md)

Governance, risk management, regulatory compliance, AI governance, audit readiness. See [compliance scoping example](examples/leadership/grc-lead/agents/grc-lead/compliance-scope/result.md).

```
/plugin install grc-lead@turtlestack
```

| Skill | Description | Example |
|---|---|---|
| [risk-assessment](plugins/leadership/grc-lead/skills/risk-assessment/SKILL.md) | Risk register entries with likelihood/impact scoring | [Risk scoring](examples/leadership/grc-lead/skills/risk-assessment/result.md) |
| [compliance-audit](plugins/leadership/grc-lead/skills/compliance-audit/SKILL.md) | Compliance gap analysis against a framework | [Gap analysis](examples/leadership/grc-lead/skills/compliance-audit/result.md) |
| [ai-governance-review](plugins/leadership/grc-lead/skills/ai-governance-review/SKILL.md) | AI system governance assessment | [AI governance](examples/leadership/grc-lead/skills/ai-governance-review/result.md) |
| [write-dpia](plugins/leadership/grc-lead/skills/write-dpia/SKILL.md) | Data protection impact assessment | [DPIA authoring](examples/leadership/grc-lead/skills/write-dpia/result.md) |

### Product

#### [Customer Success](plugins/product/customer-success/agents/customer-success.md)

Health monitoring, churn prevention, expansion, onboarding quality. See [account review example](examples/product/customer-success/agents/customer-success/account-review/result.md).

```
/plugin install customer-success@turtlestack
```

| Skill | Description | Example |
|---|---|---|
| [health-assessment](plugins/product/customer-success/skills/health-assessment/SKILL.md) | Customer health score assessment | [Health scoring](examples/product/customer-success/skills/health-assessment/result.md) |
| [churn-analysis](plugins/product/customer-success/skills/churn-analysis/SKILL.md) | Churn risk analysis | [Churn analysis](examples/product/customer-success/skills/churn-analysis/result.md) |
| [expansion-plan](plugins/product/customer-success/skills/expansion-plan/SKILL.md) | Account expansion plan | [Expansion plan](examples/product/customer-success/skills/expansion-plan/result.md) |
| [write-qbr](plugins/product/customer-success/skills/write-qbr/SKILL.md) | Quarterly business review | [QBR authoring](examples/product/customer-success/skills/write-qbr/result.md) |
| [write-onboarding-playbook](plugins/product/customer-success/skills/write-onboarding-playbook/SKILL.md) | Customer onboarding playbook | [Onboarding playbook](examples/product/customer-success/skills/write-onboarding-playbook/result.md) |

#### [Developer Docs Writer](plugins/product/developer-docs-writer/agents/developer-docs-writer.md)

API references, SDK guides, integration tutorials, code examples. See [API documentation example](examples/product/developer-docs-writer/agents/developer-docs-writer/api-documentation/result.md).

```
/plugin install developer-docs-writer@turtlestack
```

| Skill | Description | Example |
|---|---|---|
| [write-api-docs](plugins/product/developer-docs-writer/skills/write-api-docs/SKILL.md) | API reference documentation | [API docs](examples/product/developer-docs-writer/skills/write-api-docs/result.md) |
| [write-sdk-guide](plugins/product/developer-docs-writer/skills/write-sdk-guide/SKILL.md) | SDK getting-started guide | [SDK guide](examples/product/developer-docs-writer/skills/write-sdk-guide/result.md) |
| [write-integration-guide](plugins/product/developer-docs-writer/skills/write-integration-guide/SKILL.md) | Third-party integration guide | [Integration guide](examples/product/developer-docs-writer/skills/write-integration-guide/result.md) |
| [write-migration-guide](plugins/product/developer-docs-writer/skills/write-migration-guide/SKILL.md) | Version migration guide | [Migration guide](examples/product/developer-docs-writer/skills/write-migration-guide/result.md) |

#### [GTM](plugins/product/gtm/agents/gtm.md)

Positioning, launch strategy, competitive analysis, battle cards. See [launch strategy example](examples/product/gtm/agents/gtm/launch-strategy/result.md).

```
/plugin install gtm@turtlestack
```

| Skill | Description | Example |
|---|---|---|
| [positioning](plugins/product/gtm/skills/positioning/SKILL.md) | Product positioning statement | [Positioning statement](examples/product/gtm/skills/positioning/result.md) |
| [launch-plan](plugins/product/gtm/skills/launch-plan/SKILL.md) | Launch plan with timeline | [Launch planning](examples/product/gtm/skills/launch-plan/result.md) |
| [competitive-analysis](plugins/product/gtm/skills/competitive-analysis/SKILL.md) | Competitive landscape analysis | [Competitive mapping](examples/product/gtm/skills/competitive-analysis/result.md) |
| [write-battle-card](plugins/product/gtm/skills/write-battle-card/SKILL.md) | Sales battle card | [Battle card](examples/product/gtm/skills/write-battle-card/result.md) |

#### [Internal Docs Writer](plugins/product/internal-docs-writer/agents/internal-docs-writer.md)

Architecture docs, runbooks, changelogs, post-mortems. See [runbook creation example](examples/product/internal-docs-writer/agents/internal-docs-writer/runbook-creation/result.md).

```
/plugin install internal-docs-writer@turtlestack
```

| Skill | Description | Example |
|---|---|---|
| [write-runbook](plugins/product/internal-docs-writer/skills/write-runbook/SKILL.md) | Operational runbook | [Runbook](examples/product/internal-docs-writer/skills/write-runbook/result.md) |
| [write-changelog](plugins/product/internal-docs-writer/skills/write-changelog/SKILL.md) | Release changelog | [Changelog](examples/product/internal-docs-writer/skills/write-changelog/result.md) |
| [write-architecture-doc](plugins/product/internal-docs-writer/skills/write-architecture-doc/SKILL.md) | Architecture overview document | [Architecture doc](examples/product/internal-docs-writer/skills/write-architecture-doc/result.md) |

#### [Product Owner](plugins/product/product-owner/agents/product-owner.md)

Requirements, user stories, acceptance criteria, backlog prioritisation. See [backlog prioritisation example](examples/product/product-owner/agents/product-owner/backlog-prioritisation/result.md).

```
/plugin install product-owner@turtlestack
```

| Skill | Description | Example |
|---|---|---|
| [write-prd](plugins/product/product-owner/skills/write-prd/SKILL.md) | Product requirements document | [PRD authoring](examples/product/product-owner/skills/write-prd/result.md) |
| [groom-backlog](plugins/product/product-owner/skills/groom-backlog/SKILL.md) | Backlog grooming and prioritisation | [Backlog grooming](examples/product/product-owner/skills/groom-backlog/result.md) |
| [write-user-story](plugins/product/product-owner/skills/write-user-story/SKILL.md) | User stories with acceptance criteria | [User story](examples/product/product-owner/skills/write-user-story/result.md) |
| [write-jtbd](plugins/product/product-owner/skills/write-jtbd/SKILL.md) | Jobs-to-be-done canvas | [JTBD canvas](examples/product/product-owner/skills/write-jtbd/result.md) |
| [write-story-map](plugins/product/product-owner/skills/write-story-map/SKILL.md) | User story mapping | [Story map](examples/product/product-owner/skills/write-story-map/result.md) |

#### [Support](plugins/product/support/agents/support.md)

Ticket triage, feedback synthesis, knowledge base, bug escalation. See [ticket handling example](examples/product/support/agents/support/ticket-handling/result.md).

```
/plugin install support@turtlestack
```

| Skill | Description | Example |
|---|---|---|
| [write-kb-article](plugins/product/support/skills/write-kb-article/SKILL.md) | Knowledge base article from ticket patterns | [KB article](examples/product/support/skills/write-kb-article/result.md) |
| [feedback-synthesis](plugins/product/support/skills/feedback-synthesis/SKILL.md) | Aggregate feedback into themes | [Feedback themes](examples/product/support/skills/feedback-synthesis/result.md) |
| [triage-tickets](plugins/product/support/skills/triage-tickets/SKILL.md) | Ticket triage and routing | [Ticket triage](examples/product/support/skills/triage-tickets/result.md) |

#### [UI Designer](plugins/product/ui-designer/agents/designer.md)

Visual design, design system, component specifications, accessibility. See [component design example](examples/product/ui-designer/agents/designer/component-design/result.md).

```
/plugin install ui-designer@turtlestack
```

| Skill | Description | Example |
|---|---|---|
| [component-spec](plugins/product/ui-designer/skills/component-spec/SKILL.md) | Component specification | [Component spec](examples/product/ui-designer/skills/component-spec/result.md) |
| [accessibility-audit](plugins/product/ui-designer/skills/accessibility-audit/SKILL.md) | WCAG accessibility review | [A11y audit](examples/product/ui-designer/skills/accessibility-audit/result.md) |
| [design-review](plugins/product/ui-designer/skills/design-review/SKILL.md) | Design system compliance review | [Design review](examples/product/ui-designer/skills/design-review/result.md) |
| [design-tokens](plugins/product/ui-designer/skills/design-tokens/SKILL.md) | Design token definitions | [Token definitions](examples/product/ui-designer/skills/design-tokens/result.md) |

#### [User Docs Writer](plugins/product/user-docs-writer/agents/user-docs-writer.md)

User guides, tutorials, KB articles, onboarding content. See [help article example](examples/product/user-docs-writer/agents/user-docs-writer/help-article/result.md).

```
/plugin install user-docs-writer@turtlestack
```

| Skill | Description | Example |
|---|---|---|
| [write-user-guide](plugins/product/user-docs-writer/skills/write-user-guide/SKILL.md) | Step-by-step user guide | [User guide](examples/product/user-docs-writer/skills/write-user-guide/result.md) |
| [write-kb-article](plugins/product/user-docs-writer/skills/write-kb-article/SKILL.md) | Knowledge base article | [KB article](examples/product/user-docs-writer/skills/write-kb-article/result.md) |
| [write-onboarding](plugins/product/user-docs-writer/skills/write-onboarding/SKILL.md) | Onboarding content | [Onboarding content](examples/product/user-docs-writer/skills/write-onboarding/result.md) |
| [content-strategy](plugins/product/user-docs-writer/skills/content-strategy/SKILL.md) | Documentation content strategy | [Content strategy](examples/product/user-docs-writer/skills/content-strategy/result.md) |

#### [UX Researcher](plugins/product/ux-researcher/agents/ux-researcher.md)

Customer journeys, personas, usability assessment, information architecture. See [research plan example](examples/product/ux-researcher/agents/ux-researcher/research-plan/result.md).

```
/plugin install ux-researcher@turtlestack
```

| Skill | Description | Example |
|---|---|---|
| [journey-map](plugins/product/ux-researcher/skills/journey-map/SKILL.md) | Customer journey map | [Journey map](examples/product/ux-researcher/skills/journey-map/result.md) |
| [usability-review](plugins/product/ux-researcher/skills/usability-review/SKILL.md) | Heuristic usability assessment | [Usability review](examples/product/ux-researcher/skills/usability-review/result.md) |
| [persona-definition](plugins/product/ux-researcher/skills/persona-definition/SKILL.md) | User persona with goals and frustrations | [Persona definition](examples/product/ux-researcher/skills/persona-definition/result.md) |
| [usability-test-plan](plugins/product/ux-researcher/skills/usability-test-plan/SKILL.md) | Usability testing protocol | [Test plan](examples/product/ux-researcher/skills/usability-test-plan/result.md) |
| [service-blueprint](plugins/product/ux-researcher/skills/service-blueprint/SKILL.md) | Service blueprint | [Service blueprint](examples/product/ux-researcher/skills/service-blueprint/result.md) |

### Engineering

The engineering plugins share `engineering-conventions` as an internal dependency (spec-first implementation, definition of ready) — installed automatically with `ai-engineer`, `data-engineer`, `devops`, `python-developer`, `qa-engineer`, `react-developer`, and `security-engineer`. You don't install it directly.

#### [AI Engineer](plugins/engineering/ai-engineer/agents/ai-engineer.md)

Prompt engineering, model evaluation, RAG pipelines, embeddings. See [RAG design example](examples/engineering/ai-engineer/agents/ai-engineer/rag-design/result.md).

```
/plugin install ai-engineer@turtlestack
```

**Rules:**

| Rule | Description |
|---|---|
| [spec-first](plugins/engineering/ai-engineer/rules/spec-first.md) | Check for a spec before starting implementation |

| Skill | Description | Example |
|---|---|---|
| [prompt-design](plugins/engineering/ai-engineer/skills/prompt-design/SKILL.md) | Production prompt template | [Prompt design](examples/engineering/ai-engineer/skills/prompt-design/result.md) |
| [model-evaluation](plugins/engineering/ai-engineer/skills/model-evaluation/SKILL.md) | Model comparison and selection | [Model evaluation](examples/engineering/ai-engineer/skills/model-evaluation/result.md) |
| [rag-pipeline](plugins/engineering/ai-engineer/skills/rag-pipeline/SKILL.md) | RAG pipeline design | [RAG pipeline](examples/engineering/ai-engineer/skills/rag-pipeline/result.md) |

#### [Architect](plugins/engineering/architect/agents/architect.md)

System design, ADRs, technology evaluation, API strategy. See [system design example](examples/engineering/architect/agents/architect/system-design-request/result.md).

```
/plugin install architect@turtlestack
```

| Skill | Description | Example |
|---|---|---|
| [write-adr](plugins/engineering/architect/skills/write-adr/SKILL.md) | Architecture decision record | [ADR authoring](examples/engineering/architect/skills/write-adr/result.md) |
| [evaluate-technology](plugins/engineering/architect/skills/evaluate-technology/SKILL.md) | Technology evaluation with scoring | [Tech evaluation](examples/engineering/architect/skills/evaluate-technology/result.md) |
| [system-design](plugins/engineering/architect/skills/system-design/SKILL.md) | System design document | [System design](examples/engineering/architect/skills/system-design/result.md) |
| [api-design](plugins/engineering/architect/skills/api-design/SKILL.md) | API contract design | [API design](examples/engineering/architect/skills/api-design/result.md) |

#### [Billing Engineer](plugins/engineering/billing-engineer/agents/billing-engineer.md)

Subscription billing logic, invoicing, payment gateway integration (Stripe, PayPal), dunning management, and revenue recognition workflows. See [payment processing example](examples/engineering/billing-engineer/agents/billing-engineer/payment-processing/result.md).

```
/plugin install billing-engineer@turtlestack
```

| Skill | Description | Example |
|---|---|---|
| [payment-integration](plugins/engineering/billing-engineer/skills/payment-integration/SKILL.md) | Payment gateway integration design | Coming soon |
| [dunning-workflow](plugins/engineering/billing-engineer/skills/dunning-workflow/SKILL.md) | Dunning and retry strategy | Coming soon |
| [revenue-recognition](plugins/engineering/billing-engineer/skills/revenue-recognition/SKILL.md) | Revenue recognition mapping | Coming soon |

#### [Code Reviewer](plugins/engineering/code-reviewer/agents/code-reviewer.md)

Multi-pass code review with quality scoring and adversarial analysis. See [review with issues example](examples/engineering/code-reviewer/agents/code-reviewer/review-with-issues/result.md).

```
/plugin install code-reviewer@turtlestack
```

| Skill | Description | Example |
|---|---|---|
| [code-review](plugins/engineering/code-reviewer/skills/code-review/SKILL.md) | Multi-pass code review | [Code review](examples/engineering/code-reviewer/skills/code-review/result.md) |
| [pr-create](plugins/engineering/code-reviewer/skills/pr-create/SKILL.md) | PR with conventional commit title | [PR creation](examples/engineering/code-reviewer/skills/pr-create/result.md) |

#### [Data Engineer](plugins/engineering/data-engineer/agents/data-engineer.md)

Data pipelines, analytics, event tracking, metrics, data lineage. See [pipeline design example](examples/engineering/data-engineer/agents/data-engineer/pipeline-design/result.md).

```
/plugin install data-engineer@turtlestack
```

**Rules:**

| Rule | Description |
|---|---|
| [spec-first](plugins/engineering/data-engineer/rules/spec-first.md) | Check for a spec before starting implementation |

| Skill | Description | Example |
|---|---|---|
| [event-tracking-plan](plugins/engineering/data-engineer/skills/event-tracking-plan/SKILL.md) | Event tracking specification | [Event tracking](examples/engineering/data-engineer/skills/event-tracking-plan/result.md) |
| [write-query](plugins/engineering/data-engineer/skills/write-query/SKILL.md) | Analytics query | [Query authoring](examples/engineering/data-engineer/skills/write-query/result.md) |
| [data-model](plugins/engineering/data-engineer/skills/data-model/SKILL.md) | Data model design | [Data modelling](examples/engineering/data-engineer/skills/data-model/result.md) |

#### [DevOps](plugins/engineering/devops/agents/devops.md)

Infrastructure-as-code, CI/CD, deployment, monitoring, incident response. See [deployment strategy example](examples/engineering/devops/agents/devops/deployment-strategy/result.md).

```
/plugin install devops@turtlestack
```

**Rules:**

| Rule | Description |
|---|---|
| [spec-first](plugins/engineering/devops/rules/spec-first.md) | Check for a spec before starting implementation |
| [pulumi](plugins/engineering/devops/rules/pulumi.md) | Pulumi infrastructure-as-code patterns and conventions |
| [moonrepo](plugins/engineering/devops/rules/moonrepo.md) | Moon monorepo manager conventions |
| [sonarcloud](plugins/engineering/devops/rules/sonarcloud.md) | SonarCloud code quality enforcement and configuration |

| Skill | Description | Example |
|---|---|---|
| [write-pipeline](plugins/engineering/devops/skills/write-pipeline/SKILL.md) | CI/CD pipeline configuration | [Pipeline config](examples/engineering/devops/skills/write-pipeline/result.md) |
| [write-dockerfile](plugins/engineering/devops/skills/write-dockerfile/SKILL.md) | Production Dockerfile | [Dockerfile](examples/engineering/devops/skills/write-dockerfile/result.md) |
| [incident-response](plugins/engineering/devops/skills/incident-response/SKILL.md) | Incident response runbook | [Incident response](examples/engineering/devops/skills/incident-response/result.md) |
| [write-iac](plugins/engineering/devops/skills/write-iac/SKILL.md) | Infrastructure-as-code module | [IaC module](examples/engineering/devops/skills/write-iac/result.md) |
| [write-slo](plugins/engineering/devops/skills/write-slo/SKILL.md) | SLO definition | [SLO definition](examples/engineering/devops/skills/write-slo/result.md) |

#### [.NET Developer](plugins/engineering/dotnet-developer/agents/dotnet-developer.md)

.NET/C# with Wolverine, Marten, event sourcing, CQRS, Alba testing. See [endpoint implementation example](examples/engineering/dotnet-developer/agents/dotnet-developer/endpoint-implementation/result.md).

```
/plugin install dotnet-developer@turtlestack
```

| Skill | Description | Example |
|---|---|---|
| [write-endpoint](plugins/engineering/dotnet-developer/skills/write-endpoint/SKILL.md) | Wolverine HTTP endpoint | [Endpoint authoring](examples/engineering/dotnet-developer/skills/write-endpoint/result.md) |
| [write-handler](plugins/engineering/dotnet-developer/skills/write-handler/SKILL.md) | Wolverine message handler | [Handler authoring](examples/engineering/dotnet-developer/skills/write-handler/result.md) |

#### [Performance Engineer](plugins/engineering/performance-engineer/agents/performance-engineer.md)

Load testing, profiling, capacity planning, performance budgets. See [bottleneck investigation example](examples/engineering/performance-engineer/agents/performance-engineer/bottleneck-investigation/result.md).

```
/plugin install performance-engineer@turtlestack
```

| Skill | Description | Example |
|---|---|---|
| [load-test-plan](plugins/engineering/performance-engineer/skills/load-test-plan/SKILL.md) | Load test plan | [Load test plan](examples/engineering/performance-engineer/skills/load-test-plan/result.md) |
| [performance-profile](plugins/engineering/performance-engineer/skills/performance-profile/SKILL.md) | Performance profiling report | [Perf profiling](examples/engineering/performance-engineer/skills/performance-profile/result.md) |
| [capacity-plan](plugins/engineering/performance-engineer/skills/capacity-plan/SKILL.md) | Capacity planning analysis | [Capacity plan](examples/engineering/performance-engineer/skills/capacity-plan/result.md) |

#### [PHP Developer](plugins/engineering/php-developer/agents/php-developer.md)

Framework-agnostic modern PHP 8.4+ with PHPStan level 9, PHP-CS-Fixer (PER-CS), Pest + Behat, Infection mutation testing, readonly value objects, and event-sourced aggregates via EventSauce dispatched through symfony/messenger. See [aggregate implementation example](examples/engineering/php-developer/agents/php-developer/aggregate-implementation/result.md).

```
/plugin install php-developer@turtlestack
```

| Skill | Description | Example |
|---|---|---|
| [write-feature-spec](plugins/engineering/php-developer/skills/write-feature-spec/SKILL.md) | Behat feature specification | [Feature spec](examples/engineering/php-developer/skills/write-feature-spec/result.md) |
| [write-aggregate](plugins/engineering/php-developer/skills/write-aggregate/SKILL.md) | Event-sourced aggregate (EventSauce) | [Aggregate authoring](examples/engineering/php-developer/skills/write-aggregate/result.md) |
| [write-handler](plugins/engineering/php-developer/skills/write-handler/SKILL.md) | symfony/messenger command/query/event handler | [Handler authoring](examples/engineering/php-developer/skills/write-handler/result.md) |

#### [Python Developer](plugins/engineering/python-developer/agents/python-developer.md)

Python with Ruff, mypy strict, BDD (pytest-bdd), Hypothesis, DDD. See [feature implementation example](examples/engineering/python-developer/agents/python-developer/feature-implementation/result.md).

```
/plugin install python-developer@turtlestack
```

**Rules:**

| Rule | Description |
|---|---|
| [spec-first](plugins/engineering/python-developer/rules/spec-first.md) | Check for a spec before starting implementation |

| Skill | Description | Example |
|---|---|---|
| [write-feature-spec](plugins/engineering/python-developer/skills/write-feature-spec/SKILL.md) | BDD feature specification | [Feature spec](examples/engineering/python-developer/skills/write-feature-spec/result.md) |
| [write-schema](plugins/engineering/python-developer/skills/write-schema/SKILL.md) | Pydantic schema definition | [Schema definition](examples/engineering/python-developer/skills/write-schema/result.md) |

#### [QA Engineer](plugins/engineering/qa-engineer/agents/qa-engineer.md)

Test automation, E2E acceptance tests, coverage analysis, bug investigation. See [test planning example](examples/engineering/qa-engineer/agents/qa-engineer/test-planning/result.md).

```
/plugin install qa-engineer@turtlestack
```

**Rules:**

| Rule | Description |
|---|---|
| [spec-first](plugins/engineering/qa-engineer/rules/spec-first.md) | Check for a spec before starting implementation |

| Skill | Description | Example |
|---|---|---|
| [generate-tests](plugins/engineering/qa-engineer/skills/generate-tests/SKILL.md) | Generate test suite from spec | [Test generation](examples/engineering/qa-engineer/skills/generate-tests/result.md) |
| [write-bug-report](plugins/engineering/qa-engineer/skills/write-bug-report/SKILL.md) | Structured bug report | [Bug report](examples/engineering/qa-engineer/skills/write-bug-report/result.md) |

#### [QA Lead](plugins/engineering/qa-lead/agents/qa-lead.md)

Test strategy, acceptance criteria, 3 amigos, edge case identification. See [strategy review example](examples/engineering/qa-lead/agents/qa-lead/strategy-review/result.md).

```
/plugin install qa-lead@turtlestack
```

| Skill | Description | Example |
|---|---|---|
| [test-strategy](plugins/engineering/qa-lead/skills/test-strategy/SKILL.md) | Test strategy document | [Test strategy](examples/engineering/qa-lead/skills/test-strategy/result.md) |
| [write-acceptance-criteria](plugins/engineering/qa-lead/skills/write-acceptance-criteria/SKILL.md) | Gherkin acceptance criteria | [Acceptance criteria](examples/engineering/qa-lead/skills/write-acceptance-criteria/result.md) |

#### [React Developer](plugins/engineering/react-developer/agents/react-developer.md)

React/Next.js with TypeScript, Tailwind, content-collections, Vitest. See [component implementation example](examples/engineering/react-developer/agents/react-developer/component-implementation/result.md).

```
/plugin install react-developer@turtlestack
```

**Rules:**

| Rule | Description |
|---|---|
| [spec-first](plugins/engineering/react-developer/rules/spec-first.md) | Check for a spec before starting implementation |

| Skill | Description | Example |
|---|---|---|
| [component-from-spec](plugins/engineering/react-developer/skills/component-from-spec/SKILL.md) | Build component from design spec | [Component build](examples/engineering/react-developer/skills/component-from-spec/result.md) |
| [performance-audit](plugins/engineering/react-developer/skills/performance-audit/SKILL.md) | Frontend performance audit | [Perf audit](examples/engineering/react-developer/skills/performance-audit/result.md) |

#### [Release Manager](plugins/engineering/release-manager/agents/release-manager.md)

Release coordination, go/no-go, rollback decisions, deployment scheduling. See [release coordination example](examples/engineering/release-manager/agents/release-manager/release-coordination/result.md).

```
/plugin install release-manager@turtlestack
```

| Skill | Description | Example |
|---|---|---|
| [release-plan](plugins/engineering/release-manager/skills/release-plan/SKILL.md) | Release plan with gates | [Release plan](examples/engineering/release-manager/skills/release-plan/result.md) |
| [rollback-assessment](plugins/engineering/release-manager/skills/rollback-assessment/SKILL.md) | Rollback risk assessment | [Rollback assessment](examples/engineering/release-manager/skills/rollback-assessment/result.md) |

#### Security Engineer

Threat modelling, security audits, CVSS scoring, vulnerability management. Includes a separate [prompt-injection-tester](plugins/engineering/security-engineer/agents/prompt-injection-tester.md) agent for adversarial LLM testing (see [LLM testing example](examples/engineering/security-engineer/agents/prompt-injection-tester/test-llm-endpoint/result.md)).

```
/plugin install security-engineer@turtlestack
```

**Rules:**

| Rule | Description |
|---|---|
| [spec-first](plugins/engineering/security-engineer/rules/spec-first.md) | Check for a spec before starting implementation |

**[Security engineer](plugins/engineering/security-engineer/agents/security-engineer.md)** skills (see [vulnerability assessment example](examples/engineering/security-engineer/agents/security-engineer/vulnerability-assessment/result.md)):

| Skill | Description | Example |
|---|---|---|
| [threat-model](plugins/engineering/security-engineer/skills/threat-model/SKILL.md) | STRIDE threat model | [Threat modelling](examples/engineering/security-engineer/skills/threat-model/result.md) |
| [security-review](plugins/engineering/security-engineer/skills/security-review/SKILL.md) | Security code review | [Security review](examples/engineering/security-engineer/skills/security-review/result.md) |
| [dependency-audit](plugins/engineering/security-engineer/skills/dependency-audit/SKILL.md) | Dependency vulnerability audit | [Dependency audit](examples/engineering/security-engineer/skills/dependency-audit/result.md) |
| [supply-chain-audit](plugins/engineering/security-engineer/skills/supply-chain-audit/SKILL.md) | Supply chain security review | [Supply chain audit](examples/engineering/security-engineer/skills/supply-chain-audit/result.md) |
| [recon](plugins/engineering/security-engineer/skills/recon/SKILL.md) | External reconnaissance | [Recon](examples/engineering/security-engineer/skills/recon/result.md) |
| [web-assessment](plugins/engineering/security-engineer/skills/web-assessment/SKILL.md) | Web application security assessment | [Web assessment](examples/engineering/security-engineer/skills/web-assessment/result.md) |

## Under the hood

### How rules and skills work

Claude Code plugins support tools, agents, skills, and output styles. Team instructions (coding standards, security rules, writing guidelines) use two approaches:

**Rules** are `.md` files in each plugin's `rules/` directory. Claude Code auto-installs them into `.claude/rules/` with a version prefix (e.g., `1.7.5--typescript.md`). They're always active.

**Skills** are context-specific. Claude auto-invokes them when the situation matches (e.g., a code review skill activates when reviewing code), or you call them directly with `/plugin:skill-name`.

| Scenario | Approach |
|---|---|
| "Always follow these TypeScript conventions" | Rule |
| "When reviewing code, check for X" | Skill |
| "Use this tone in all communications" | Rule |
| "When working on API files, follow these patterns" | Skill with `paths:` filter |

### The learning system (technical detail)

The thinking plugin hooks into every session:

- **`UserPromptSubmit` (async)** — classifies every message via regex. Catches corrections, praise, and approach changes. Queues ambiguous messages for Claude to classify during `/thinking:retrospective`.
- **`SessionStart`** — analyses the previous session's transcript, detects patterns, generates metrics, and injects recent learnings into context.

Learnings flow through two paths:

1. **Local (immediate):** Rules written to `.claude/rules/learned--*.md` take effect next session.
2. **Shared (upstream):** When patterns recur (5+ instances), `/thinking:propose-improvement` proposes a PR against the marketplace repo with evidence.

The regex classifier self-evolves. Each retrospective that classifies an ambiguous message extracts a new regex pattern and writes it to `.claude/learnings/signals/patterns.json`, which the classifier loads on every subsequent message.

### Evaluation framework

Every plugin definition is tested against a calibrated [evaluator agent](plugins/practices/plugin-curator/agents/evaluator.md). Each test has a [realistic prompt, criteria, captured output, and per-criterion evaluation](examples/). The Example column in each plugin table links to the evaluated output.

Run evaluations via the [evaluate skill](plugins/practices/plugin-curator/skills/evaluate/SKILL.md):

```
/evaluate                          # all tests
/evaluate examples/research        # one category
/evaluate examples/research/analyst/skills/company-lookup  # single test
```

The skill prints a summary table to the chat. Per-test `result.md` files in each test directory carry the full output and judge breakdown — those are linked from the Example column in every plugin table above.

The 23 per-agent `bootstrap` skills don't appear in the skill tables (they're not user-invocable — `/coordinator:bootstrap-project` delegates to them), but each one has its own rubric test under `examples/<category>/<plugin>/skills/bootstrap/result.md`. The safe-merge contract — preserving user-edited sections while appending missing template sections — is exercised against a synthetic project fixture for every bootstrap.

### Creating a new plugin

1. Create the plugin directory under the appropriate category:

   ```
   plugins/<category>/<name>/
   ├── .claude-plugin/plugin.json   # Required
   ├── skills/                      # Optional
   │   └── my-skill/SKILL.md
   ├── agents/                      # Optional
   │   └── my-agent.md
   ├── rules/                       # Optional: auto-installed by Claude Code
   │   └── my-rules.md
   └── templates/                   # Optional: reference templates
   ```

2. Register in `.claude-plugin/marketplace.json` and update this README.

### Troubleshooting

**marketplace.json source paths** must be prefixed with `./plugins/` (the full relative path from the repo root). Do NOT use `pluginRoot` in metadata.

```json
{
  "name": "my-plugin",
  "source": "./plugins/engineering/my-plugin"
}
```

**Skills not available via `/` slash commands.** Plugin skills are invoked by Claude automatically or by asking Claude to use them. The `/plugin-name:skill-name` syntax may not work for all plugin-provided skills. This is a Claude Code limitation.

## Complementary plugins

These external marketplaces provide capabilities that complement ours:

- [obra/superpowers](https://github.com/obra/superpowers) — TDD enforcement, systematic debugging, parallel agent dispatch
- [anthropics/skills](https://github.com/anthropics/skills) — Official skill standards, document creation (docx, pdf, pptx, xlsx)
- [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) — Official Anthropic reference plugins
- [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin) — Research agents, multi-lens code review, design sync
- [mintmcp/agent-security](https://github.com/mintmcp/agent-security) — Secrets scanning hooks (pre-submission credential blocking)

## Acknowledgements

This marketplace incorporates concepts and methodologies from:

- [PAI (Personal AI Infrastructure)](https://github.com/danielmiessler/Personal_AI_Infrastructure) by Daniel Miessler — ISC methodology, algorithm phases, first principles, council, red team, creative skills, AI steering rules, writing style rules
- [romiluz13/cc10x](https://github.com/romiluz13/cc10x) — Phase contracts, proof reconciliation, multi-signal quality scoring, failure caps, scenario contracts, evidence arrays
- [obra/superpowers](https://github.com/obra/superpowers) — TDD iron law, systematic debugging methodology, parallel agent dispatch protocol
- [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin) — Multi-lens review patterns, adversarial analysis, confidence calibration, design iteration
- [shinpr/claude-code-workflows](https://github.com/shinpr/claude-code-workflows) — Technical designer gates, agreement-first pattern, task decomposition, work planning
- [rsmdt/the-startup](https://github.com/rsmdt/the-startup) — Constitution governance, 3Cs validation framework, NEEDS CLARIFICATION markers, drift detection
- [withzombies/hyperpowers](https://github.com/withzombies/hyperpowers) — Parallel agent orchestration protocol, markdown-first state management
- [Equilateral-AI/equilateral-agents-open-core](https://github.com/Equilateral-AI/equilateral-agents-open-core) — Standards injection, knowledge harvest methodology
- [adrianpuiu/specification-document-generator](https://github.com/adrianpuiu/specification-document-generator) — Anti-slop protocol, evidence-based architecture, citation trails
- [christophecapel/claude-mechanisms](https://github.com/christophecapel/claude-mechanisms) — Session discipline, mechanism design principles, hook design patterns, cascade tracing, review-in-artifact conventions
