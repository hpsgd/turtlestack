---
kind: hook
hook: plugins/practices/thinking/scripts/install-rules.sh
---

# Hook test: install-rules keeps one plugin's newer rules when plugins version independently

In a marketplace whose plugins carry their own versions, the newest version overall can match
between two profiles while one plugin differs. The project holds alpha 2.0.0 and beta 1.6.0; this
profile's cache has alpha 2.0.0 and beta 1.5.0. Alpha installs as normal, beta's 1.6.0 rule is kept,
no 1.5.0 file is written, and one warning line names beta.

## Setup

mkdir -p config/plugins/cache/mp/alpha/2.0.0/rules config/plugins/cache/mp/beta/1.5.0/rules rules
cat > config/plugins/cache/mp/alpha/2.0.0/rules/a.md <<'MD'
Alpha 2.0.0 rule body.
MD
cat > config/plugins/cache/mp/beta/1.5.0/rules/b.md <<'MD'
Beta 1.5.0 rule body.
MD
cp config/plugins/cache/mp/alpha/2.0.0/rules/a.md rules/mp--alpha--2.0.0--a.md
cat > rules/mp--beta--1.6.0--b.md <<'MD'
Beta 1.6.0 rule body.
MD
mkdir -p project/.claude
cat > config/settings.json <<'JSON'
{"enabledPlugins": {"alpha@mp": true, "beta@mp": true}}
JSON

## Env

CLAUDE_PLUGIN_ROOT={workspace}/config/plugins/cache/mp/alpha/2.0.0
CLAUDE_CONFIG_DIR={workspace}/config
CLAUDE_PROJECT_DIR={workspace}/project
RULES_DIR={workspace}/rules

## Assertions

- exit 0
- file contains: rules/mp--alpha--2.0.0--a.md :: Alpha 2.0.0 rule body.
- file contains: rules/mp--beta--1.6.0--b.md :: Beta 1.6.0 rule body.
- file not exists: rules/mp--beta--1.5.0--b.md
- stdout contains: kept newer project rules for beta
