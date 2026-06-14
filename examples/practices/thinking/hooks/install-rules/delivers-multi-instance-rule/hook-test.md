---
kind: hook
hook: plugins/practices/thinking/scripts/install-rules.sh
---

# Hook test: install-rules delivers the multi-instance rule

The SessionStart rule installer copies every enabled plugin's rules from the
marketplace cache into the project's rules dir. This proves the new
`multi-instance-dispatch` rule ships through that mechanism — staging a local
cache (the harness can't read an unreleased rule from the real cache, so we point
the installer at a cache built from the working tree) and asserting the rule lands
with the standard `<marketplace>--<plugin>--<version>--<file>` name.

## Setup

mkdir -p config/plugins/cache/turtlestack/thinking/9.9.9/rules
cp {repo_root}/plugins/practices/thinking/rules/*.md config/plugins/cache/turtlestack/thinking/9.9.9/rules/
mkdir -p project/.claude rules
cat > config/settings.json <<'JSON'
{"enabledPlugins": {"thinking@turtlestack": true}}
JSON

## Env

CLAUDE_PLUGIN_ROOT={workspace}/config/plugins/cache/turtlestack/thinking/9.9.9
CLAUDE_CONFIG_DIR={workspace}/config
CLAUDE_PROJECT_DIR={workspace}/project
RULES_DIR={workspace}/rules

## Assertions

- exit 0
- file exists: rules/turtlestack--thinking--9.9.9--multi-instance-dispatch.md
- file contains: rules/turtlestack--thinking--9.9.9--multi-instance-dispatch.md :: When you dispatch multiple instances
- file contains: rules/turtlestack--thinking--9.9.9--multi-instance-dispatch.md :: When you are a dispatched instance
