#!/usr/bin/env bash
# check-plugin-versions.sh — Detect plugin version drift on session start.
#
# Iterates every installed marketplace under ~/.claude/plugins/marketplaces/
# and compares each installed plugin's version against the cached marketplace's
# current version. Per-marketplace drift files are written under
# .claude/<marketplace>/plugin-updates.md with ready-to-paste
# `claude plugin update` commands; a single consolidated context line points
# at all of them.
#
# Silent on no drift. Fails silent on errors (never blocks session start).

set -uo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-}"
CONFIG_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
INSTALLED="$CONFIG_DIR/plugins/installed_plugins.json"
MARKETPLACES_DIR="$CONFIG_DIR/plugins/marketplaces"

[[ ! -f "$INSTALLED" || ! -d "$MARKETPLACES_DIR" ]] && exit 0

drift_target_dir() {
    local marketplace="$1"
    if [[ -n "$PROJECT_DIR" ]]; then
        echo "${PROJECT_DIR}/.claude/${marketplace}"
    else
        echo "${CONFIG_DIR}/${marketplace}"
    fi
}

display_path() {
    local path="$1"
    if [[ -n "$PROJECT_DIR" && "$path" == "$PROJECT_DIR"/* ]]; then
        echo "${path#$PROJECT_DIR/}"
    else
        echo "$path"
    fi
}

summary_lines=()
total_count=0
drift_paths=()
display_paths=()

shopt -s nullglob
for mp_path in "$MARKETPLACES_DIR"/*/; do
    MARKETPLACE=$(basename "$mp_path")
    MARKETPLACE_JSON="${mp_path}.claude-plugin/marketplace.json"
    DRIFT_FILE="$(drift_target_dir "$MARKETPLACE")/plugin-updates.md"

    if [[ ! -f "$MARKETPLACE_JSON" ]]; then
        [[ -f "$DRIFT_FILE" ]] && rm -f "$DRIFT_FILE"
        continue
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
        continue
    fi

    count=$(printf '%s\n' "$drift" | wc -l | tr -d ' ')
    total_count=$((total_count + count))
    summary_lines+=("${count} ${MARKETPLACE}")
    drift_paths+=("$DRIFT_FILE")
    display_paths+=("$(display_path "$DRIFT_FILE")")

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
done

[[ $total_count -eq 0 ]] && exit 0

python3 - "$total_count" "${#summary_lines[@]}" "${summary_lines[@]}" "${drift_paths[@]}" "${display_paths[@]}" <<'PY'
import json, sys

total = sys.argv[1]
n = int(sys.argv[2])
summaries = sys.argv[3 : 3 + n]
paths = sys.argv[3 + n : 3 + 2 * n]
displays = sys.argv[3 + 2 * n : 3 + 3 * n]

breakdown = ", ".join(summaries)
detail = "; ".join(f"{label} -> {path}" for label, path in zip(summaries, paths))

context = (
    f"<plugin-version-drift>{total} plugin(s) out of date across "
    f"{n} marketplace(s) ({breakdown}). Details: {detail}"
    "</plugin-version-drift>"
)
message = f"⚠  {total} plugin(s) out of date — see {', '.join(displays)}"
print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": context,
    },
    "systemMessage": message,
}))
PY
