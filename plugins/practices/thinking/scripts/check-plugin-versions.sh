#!/usr/bin/env bash
# check-plugin-versions.sh — Detect plugin version drift on session start.
#
# Compares each installed plugin's version against the cached marketplace's
# current version. If drift exists, writes a markdown file with ready-to-paste
# `claude plugin update` commands and prints a one-line summary pointing at it.
# If no drift, removes any stale file from a previous session.
#
# Silent on no drift. Fails silent on errors (never blocks session start).

set -uo pipefail

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-}"
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-}"

# Derive marketplace name from CLAUDE_PLUGIN_ROOT
# (e.g. ~/.claude/plugins/cache/turtlestack/thinking/1.15.0 -> turtlestack)
[[ -z "$PLUGIN_ROOT" ]] && exit 0
cache_path="${PLUGIN_ROOT%/}"
cache_path=$(dirname "$cache_path")  # strip version
cache_path=$(dirname "$cache_path")  # strip plugin name
MARKETPLACE=$(basename "$cache_path")
[[ -z "$MARKETPLACE" || "$MARKETPLACE" == "cache" ]] && exit 0

CONFIG_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
INSTALLED="$CONFIG_DIR/plugins/installed_plugins.json"
MARKETPLACE_JSON="$CONFIG_DIR/plugins/marketplaces/$MARKETPLACE/.claude-plugin/marketplace.json"

# Drift file lives with the project so project-scoped drift travels with the
# project. Fall back to global config dir for sessions with no project.
if [[ -n "$PROJECT_DIR" ]]; then
    DRIFT_FILE="${PROJECT_DIR}/.claude/${MARKETPLACE}/plugin-updates.md"
else
    DRIFT_FILE="${CONFIG_DIR}/${MARKETPLACE}/plugin-updates.md"
fi

if [[ ! -f "$INSTALLED" || ! -f "$MARKETPLACE_JSON" ]]; then
    [[ -f "$DRIFT_FILE" ]] && rm -f "$DRIFT_FILE"
    exit 0
fi

drift=$(python3 - "$INSTALLED" "$MARKETPLACE_JSON" "$MARKETPLACE" "${PROJECT_DIR:-}" <<'PY' 2>/dev/null
import json, sys

installed_path, marketplace_path, marketplace, project_dir = sys.argv[1:5]

try:
    with open(installed_path) as f:
        installed = json.load(f)
    with open(marketplace_path) as f:
        catalog = json.load(f)
except Exception:
    sys.exit(0)

latest = {p["name"]: p.get("version") for p in catalog.get("plugins", []) if p.get("name")}

suffix = f"@{marketplace}"
drifted = []

for key, entries in installed.get("plugins", {}).items():
    if not key.endswith(suffix):
        continue
    name = key[: -len(suffix)]
    if name not in latest:
        continue
    target = latest[name]
    if not target:
        continue
    if not isinstance(entries, list):
        entries = [entries]
    for entry in entries:
        scope = entry.get("scope", "user")
        if scope == "project":
            if not project_dir or entry.get("projectPath") != project_dir:
                continue
        current = entry.get("version")
        if current and current != target:
            drifted.append((name, scope, current, target))

for name, scope, current, target in drifted:
    print(f"{name}\t{scope}\t{current}\t{target}")
PY
)

if [[ -z "$drift" ]]; then
    [[ -f "$DRIFT_FILE" ]] && rm -f "$DRIFT_FILE"
    exit 0
fi

count=$(printf '%s\n' "$drift" | wc -l | tr -d ' ')

mkdir -p "$(dirname "$DRIFT_FILE")"
{
    echo "# Plugin updates — ${MARKETPLACE}"
    echo
    echo "Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo
    echo "${count} plugin(s) out of sync with the cached marketplace catalog."
    echo "Run the commands below, then restart Claude Code for the new versions to load."
    echo
    echo '```bash'
    while IFS=$'\t' read -r name scope current target; do
        [[ -z "$name" ]] && continue
        echo "claude plugin update ${name}@${MARKETPLACE} --scope ${scope}    # ${current} -> ${target}"
    done <<< "$drift"
    echo '```'
} > "$DRIFT_FILE"

python3 - "$count" "$MARKETPLACE" "$DRIFT_FILE" <<'PY'
import json, sys
count, marketplace, drift_file = sys.argv[1:4]
context = f"<plugin-version-drift>{count} {marketplace} plugin(s) out of date — see {drift_file}</plugin-version-drift>"
message = f"⚠  {count} {marketplace} plugin(s) out of date — see {drift_file}"
print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": context,
    },
    "systemMessage": message,
}))
PY
