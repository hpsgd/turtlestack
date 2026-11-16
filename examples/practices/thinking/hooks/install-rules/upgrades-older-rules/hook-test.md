---
kind: hook
hook: plugins/practices/thinking/scripts/install-rules.sh
---

# Hook test: install-rules still upgrades older rules

The downgrade guard must not block the normal upgrade. The project holds
`mp--alpha--3.7.1--style.md`; the cache has alpha 4.0.0. The 4.0.0 rule is installed and the 3.7.1
file is removed as stale.

## Setup

mkdir -p config/plugins/cache/mp/alpha/4.0.0/rules rules
cat > config/plugins/cache/mp/alpha/4.0.0/rules/style.md <<'MD'
New 4.0.0 rule body.
MD
cat > rules/mp--alpha--3.7.1--style.md <<'MD'
Old 3.7.1 rule body.
MD
mkdir -p project/.claude
cat > config/settings.json <<'JSON'
{"enabledPlugins": {"alpha@mp": true}}
JSON

## Env

CLAUDE_PLUGIN_ROOT={workspace}/config/plugins/cache/mp/alpha/4.0.0
CLAUDE_CONFIG_DIR={workspace}/config
CLAUDE_PROJECT_DIR={workspace}/project
RULES_DIR={workspace}/rules

## Assertions

- exit 0
- file contains: rules/mp--alpha--4.0.0--style.md :: New 4.0.0 rule body.
- file not exists: rules/mp--alpha--3.7.1--style.md
- stdout contains: Installed 1 new/updated rules
