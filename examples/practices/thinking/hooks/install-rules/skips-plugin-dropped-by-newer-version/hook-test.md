---
kind: hook
hook: plugins/practices/thinking/scripts/install-rules.sh
---

# Hook test: install-rules doesn't bring back rules a newer version dropped

4.0.0 moved some plugins' rules into skills, so a 4.0.0 install leaves no rule file for them. When a
3.7.1 profile runs against that project, it finds no newer file for those plugins in particular and
would reinstall their old rules. Here the project holds `mp--alpha--4.0.0--style.md` only; the 3.7.1
cache ships rules for alpha and beta. Neither 3.7.1 rule may be written, and the 4.0.0 file stays.

## Setup

mkdir -p config/plugins/cache/mp/alpha/3.7.1/rules config/plugins/cache/mp/beta/3.7.1/rules rules
cat > config/plugins/cache/mp/alpha/3.7.1/rules/style.md <<'MD'
Old alpha rule body.
MD
cat > config/plugins/cache/mp/beta/3.7.1/rules/research.md <<'MD'
Old beta rule body that 4.0.0 moved into a skill.
MD
cat > rules/mp--alpha--4.0.0--style.md <<'MD'
New 4.0.0 rule body.
MD
mkdir -p project/.claude
cat > config/settings.json <<'JSON'
{"enabledPlugins": {"alpha@mp": true, "beta@mp": true}}
JSON

## Env

CLAUDE_PLUGIN_ROOT={workspace}/config/plugins/cache/mp/alpha/3.7.1
CLAUDE_CONFIG_DIR={workspace}/config
CLAUDE_PROJECT_DIR={workspace}/project
RULES_DIR={workspace}/rules

## Assertions

- exit 0
- file contains: rules/mp--alpha--4.0.0--style.md :: New 4.0.0 rule body.
- file not exists: rules/mp--beta--3.7.1--research.md
- file not exists: rules/mp--alpha--3.7.1--style.md
