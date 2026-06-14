---
kind: hook
hook: plugins/practices/thinking/scripts/install-rules.sh
---

# Hook test: install-rules installs a downstream marketplace's rule

The installer derives the marketplace from `CLAUDE_PLUGIN_ROOT`, so a downstream marketplace can
reuse this exact script by exec'ing it with `CLAUDE_PLUGIN_ROOT` pointing at one of its own plugins.
This pins that cross-marketplace contract: stage a synthetic marketplace `downstreammp` shipping a
plugin (`recon`) with one rule, point the installer at it, and assert the rule lands with the
`downstreammp--recon--<version>--<file>` name — proving the marketplace prefix follows the plugin
root, not turtlestack. A synthetic marketplace name keeps `@<marketplace>` suffix matching from
picking up any real enabled plugins, and `CLAUDE_CONFIG_DIR` is pinned to the workspace for full
isolation from the operator's `~/.claude`.

## Setup

mkdir -p config/plugins/cache/downstreammp/recon/2.1.0/rules
cat > config/plugins/cache/downstreammp/recon/2.1.0/rules/recon-baseline.md <<'MD'
# Recon baseline

Downstream marketplace rule body. Proves cross-marketplace install.
MD
mkdir -p project/.claude rules
cat > config/settings.json <<'JSON'
{"enabledPlugins": {"recon@downstreammp": true}}
JSON

## Env

CLAUDE_PLUGIN_ROOT={workspace}/config/plugins/cache/downstreammp/recon/2.1.0
CLAUDE_CONFIG_DIR={workspace}/config
CLAUDE_PROJECT_DIR={workspace}/project
RULES_DIR={workspace}/rules

## Assertions

- exit 0
- file exists: rules/downstreammp--recon--2.1.0--recon-baseline.md
- file contains: rules/downstreammp--recon--2.1.0--recon-baseline.md :: Downstream marketplace rule body
- stdout contains: downstreammp
- stdout not contains: turtlestack
