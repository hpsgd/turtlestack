---
kind: hook
hook: plugins/practices/thinking/scripts/install-rules.sh
---

# Hook test: install-rules warns instead of installing into a folder of repos

A session started in a folder that holds repos but isn't one (like `~/Projects/hps.gd`) would write
rules to `<folder>/.claude/rules/`. Claude Code loads that as an ancestor of every repo below it, so
each repo gets the rules twice. The installer must write nothing there and print one warning line.
`RULES_DIR` is left unset so the default `<project>/.claude/rules` path is what's checked.

## Setup

mkdir -p config/plugins/cache/mp/alpha/1.0.0/rules parent/repo-a/.git parent/repo-b/.git
cat > config/plugins/cache/mp/alpha/1.0.0/rules/style.md <<'MD'
Alpha rule body.
MD
cat > config/settings.json <<'JSON'
{"enabledPlugins": {"alpha@mp": true}}
JSON

## Env

CLAUDE_PLUGIN_ROOT={workspace}/config/plugins/cache/mp/alpha/1.0.0
CLAUDE_CONFIG_DIR={workspace}/config
CLAUDE_PROJECT_DIR={workspace}/parent
RULES_DIR=

## Assertions

- exit 0
- file not exists: parent/.claude/rules
- stdout contains: contains git repos but is not one
