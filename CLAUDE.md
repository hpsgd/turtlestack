# Turtlestack — Contributor Guide

## Structure

This repo is a Claude Code marketplace. Plugins are organised by function:

```
plugins/
├── leadership/          # Coordinator, CPO, CTO, GRC Lead
├── product/             # Product owner, UI designer, UX researcher, technical writer, GTM, support, customer success
├── engineering/          # Architect, developers, QA, DevOps, security, data engineering, workflow tools
├── practices/           # Coding standards, writing style, security compliance, thinking, technology stack
└── research/            # Business analyst, content analyst, open-source researcher, investigator, OSINT analyst
```

Each plugin follows this layout:

```
plugins/<category>/<name>/
├── .claude-plugin/plugin.json   # Required: plugin metadata
├── skills/                      # Optional: skills (invokable or auto-triggered)
│   └── <skill-name>/SKILL.md
├── agents/                      # Optional: subagent definitions
│   └── <agent-name>.md
├── rules/                       # Optional: instruction files (installed by thinking plugin hook)
│   └── <topic>.md
├── hooks/                       # Optional: lifecycle hooks
│   └── hooks.json
└── templates/                   # Optional: template files
```

## Key conventions

- Never put anything except `plugin.json` (and `marketplace.json` at root) inside `.claude-plugin/`
- Skills, agents, hooks, rules, and templates go at the plugin root level
- Rules in `rules/` are instruction files installed into `.claude/rules/` by the thinking plugin's SessionStart hook
- Skills in `skills/` are for context-specific guidance that Claude auto-invokes
- Register every new plugin in `.claude-plugin/marketplace.json`
- Use `leadership/` for coordination and C-level agents
- Use `product/` for customer-facing and product-related agents
- Use `engineering/` for technical implementation agents
- Use `practices/` for standards, conventions, and methodologies
- Use `research/` for research, analysis, and investigation agents
- The `thinking` plugin's SessionStart hook installs rules from all enabled plugins into `.claude/rules/` as `<marketplace>--<plugin>--<version>--<filename>.md`
- **`thinking` must be enabled** for any plugin's rules to be installed — it is the rule delivery mechanism for the marketplace
- A plugin that contributes to project bootstrap puts a `skills/bootstrap/SKILL.md` at its root. That skill's frontmatter **must declare `bootstrap-phase`** — `/coordinator:bootstrap-project` reads it to sequence the bootstrap. Valid phases: `foundations`, `delivery`, `engineering`, `stack`, `product`, `content`, `market`, `governance`. The coordinator never hardcodes which plugin runs in which phase — it reads this field, so plugins from any marketplace (including downstream ones built on this convention) slot in without editing the coordinator. A bootstrap skill with no `bootstrap-phase` still runs, in a default slot before governance, with a warning.
- **A bootstrap skill never writes a domain `CLAUDE.md` — it writes only its own fragment.** Every domain doc is assembled by the coordinator from fragments at `docs/<domain>/_sections/<plugin>.md` (authored at H2 and below, no H1), whether the domain has one contributing plugin or five. The coordinator assembles `docs/<domain>/CLAUDE.md` from the fragments — the same way it assembles the top-level `docs/CLAUDE.md` index. This makes write-collisions impossible by construction: no shared file, no ordering rules, no after-the-fact merge. A single-plugin domain is just a domain with one fragment; adding a plugin to a domain is one more fragment. A fragment may carry a `<!-- domain-title: X -->` hint as its first line to set the assembled H1's display name (e.g. `GTM`, `AI`) — without it the coordinator title-cases the directory name. This uniform model replaced the old split where single-plugin bootstraps wrote a `CLAUDE.md` directly (the surprise placeholder problem).
- **A bootstrap never guesses the project's purpose from its name.** `/coordinator:bootstrap-project` collects initial context, shape, and layout from the user up front and passes them to every bootstrap. Where the context is unknown, a bootstrap leaves a clearly marked placeholder rather than inventing a purpose. Org tooling defaults (Vercel, Playwright, Moon) are gated on shape — they flow in only when the project actually has a frontend or a monorepo, and `docs/tooling-register.md` is the per-project source of truth the tooling-conventions rule defers to.

## Adding a new plugin

1. Create `plugins/<category>/<name>/.claude-plugin/plugin.json`
2. Add skills, agents, rules, and hooks as needed
3. Add an entry to `.claude-plugin/marketplace.json` with `source` pointing to the nested path (e.g., `./plugins/engineering/architect`)
4. Update `README.md` with usage instructions
5. If the plugin scaffolds project docs, add a `skills/bootstrap/SKILL.md` declaring `bootstrap-phase` in its frontmatter (see Key conventions)
