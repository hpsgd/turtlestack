---
kind: hook
hook: plugins/practices/thinking/scripts/install-rules.sh
---

# Hook test: install-rules keeps newer rules installed by another profile

Two Claude Code profiles can share one project directory. Here the project already holds
`mp--alpha--4.0.0--style.md`, written by a profile on 4.0.0, and the installer runs from a profile
whose cache only has alpha 3.7.1. It must keep the 4.0.0 file, write no 3.7.1 file, and print a
one-line warning. Before the fix it wrote the 3.7.1 file and deleted the 4.0.0 one as stale.

## Setup

mkdir -p config/plugins/cache/mp/alpha/3.7.1/rules rules
cat > config/plugins/cache/mp/alpha/3.7.1/rules/style.md <<'MD'
Old 3.7.1 rule body.
MD
cat > rules/mp--alpha--4.0.0--style.md <<'MD'
New 4.0.0 rule body.
MD
mkdir -p project/.claude
cat > config/settings.json <<'JSON'
{"enabledPlugins": {"alpha@mp": true}}
JSON

## Env

CLAUDE_PLUGIN_ROOT={workspace}/config/plugins/cache/mp/alpha/3.7.1
CLAUDE_CONFIG_DIR={workspace}/config
CLAUDE_PROJECT_DIR={workspace}/project
RULES_DIR={workspace}/rules

## Assertions

- exit 0
- file contains: rules/mp--alpha--4.0.0--style.md :: New 4.0.0 rule body.
- file not exists: rules/mp--alpha--3.7.1--style.md
- stdout contains: kept mp 4.0.0 rules
