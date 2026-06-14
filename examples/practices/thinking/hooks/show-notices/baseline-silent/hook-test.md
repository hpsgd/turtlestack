---
kind: hook
hook: plugins/practices/thinking/scripts/show-notices.sh
---

# Hook test: baseline mode seeds the marker silently

With `NOTICES_FIRST_RUN=baseline`, a fresh install seeds every notice id as
already-seen and shows nothing — so a real first install on a clean machine isn't
flooded with the backlog. The seen-marker is still written.

## Setup

mkdir -p cache/turtlestack/thinking/9.9.9
cat > cache/turtlestack/thinking/9.9.9/notices.json <<'JSON'
{"notices": [
  {"id": "test-action", "version": "9.9.9", "severity": "action", "title": "Action needed on config", "message": "Add the new key to settings.json."}
]}
JSON
mkdir -p config

## Env

CLAUDE_PLUGIN_ROOT={workspace}/cache/turtlestack/thinking/9.9.9
CLAUDE_CONFIG_DIR={workspace}/config
NOTICES_FIRST_RUN=baseline

## Assertions

- exit 0
- stdout empty
- file exists: config/turtlestack/notices-seen.json
- file contains: config/turtlestack/notices-seen.json :: test-action
