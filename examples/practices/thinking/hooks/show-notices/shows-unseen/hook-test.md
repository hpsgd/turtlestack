---
kind: hook
hook: plugins/practices/thinking/scripts/show-notices.sh
---

# Hook test: shows unseen notices on first run (show mode)

With `NOTICES_FIRST_RUN=show`, a fresh machine surfaces every eligible notice
once — a SessionStart additionalContext block plus a one-line systemMessage per
notice. A fixture notices.json under a `cache/turtlestack/thinking/<ver>/`
structure makes the marketplace derivation deterministic (the shipped
notices.json is intentionally empty).

## Setup

mkdir -p cache/turtlestack/thinking/9.9.9
cat > cache/turtlestack/thinking/9.9.9/notices.json <<'JSON'
{"notices": [
  {"id": "test-breaking", "version": "9.9.9", "severity": "breaking", "title": "Breaking change to rule install", "message": "Re-run bootstrap to pick up the new path."},
  {"id": "test-action", "version": "9.9.9", "severity": "action", "title": "Action needed on config", "message": "Add the new key to settings.json."}
]}
JSON
mkdir -p config

## Env

CLAUDE_PLUGIN_ROOT={workspace}/cache/turtlestack/thinking/9.9.9
CLAUDE_CONFIG_DIR={workspace}/config
NOTICES_FIRST_RUN=show

## Assertions

- exit 0
- stdout contains: SessionStart
- stdout contains: Breaking change to rule install
- stdout contains: Action needed on config
- file exists: config/turtlestack/notices-seen.json
- file contains: config/turtlestack/notices-seen.json :: test-action
