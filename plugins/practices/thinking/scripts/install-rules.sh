#!/usr/bin/env bash
# install-rules.sh — Install plugin rule files into the consuming project's .claude/rules/
#
# Runs as a SessionStart hook from the thinking plugin.
# Installs rules for ALL enabled plugins in the marketplace, not just thinking.
#
# Naming convention: <marketplace>--<plugin>--<version>--<filename>.md
# Example: turtlestack--coding-standards--1.7.5--ai-steering.md

set -euo pipefail

# --- Inputs ---
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-}"
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-}"

# Skip if no project directory (global session)
if [[ -z "$PROJECT_DIR" ]]; then
  exit 0
fi

# --- Derive marketplace name and cache root ---
# PLUGIN_ROOT is e.g. ~/.claude/plugins/cache/turtlestack/thinking/1.7.5
# Walk up to find the marketplace name (parent of plugin name, child of "cache")
cache_path="${PLUGIN_ROOT}"
# Strip trailing slashes
cache_path="${cache_path%/}"
# Go up: version -> plugin -> marketplace -> cache
version_dir=$(basename "$cache_path")
cache_path=$(dirname "$cache_path")
plugin_dir=$(basename "$cache_path")
cache_path=$(dirname "$cache_path")
MARKETPLACE=$(basename "$cache_path")
CACHE_ROOT=$(dirname "$cache_path")/${MARKETPLACE}

if [[ -z "$MARKETPLACE" || "$MARKETPLACE" == "cache" ]]; then
  echo "Could not derive marketplace name from CLAUDE_PLUGIN_ROOT" >&2
  exit 1
fi

# --- Set up rules directory ---
# RULES_DIR can be overridden via env var (used by test harnesses to redirect
# writes outside the permission-gated .claude/ path). Default: project's .claude/rules.
if [[ -z "${RULES_DIR:-}" ]]; then
  RULES_DIR="${PROJECT_DIR}/.claude/rules"
fi
mkdir -p "$RULES_DIR"

# --- Collect enabled plugins ---
# Parse enabledPlugins from both project and global settings
# Extracts plugin names where the key ends with @<marketplace> and value is true
extract_plugins() {
  local settings_file="$1"
  if [[ ! -f "$settings_file" ]]; then
    return
  fi
  # Use python3 for reliable JSON parsing
  python3 -c "
import json, sys
try:
    with open('$settings_file') as f:
        data = json.load(f)
    plugins = data.get('enabledPlugins', {})
    suffix = '@${MARKETPLACE}'
    for key, val in plugins.items():
        if key.endswith(suffix) and val is True:
            print(key[:-len(suffix)])
except Exception:
    pass
" 2>/dev/null
}

# Merge project-level and global-level enabled plugins (deduplicated).
# Global config respects $CLAUDE_CONFIG_DIR (used by the test harness to
# isolate config under a workspace tmpdir), falling back to ~/.claude when
# the variable is unset.
GLOBAL_SETTINGS="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/settings.json"

enabled_plugins=()
while IFS= read -r plugin; do
  [[ -n "$plugin" ]] && enabled_plugins+=("$plugin")
done < <(
  {
    extract_plugins "${PROJECT_DIR}/.claude/settings.json"
    extract_plugins "$GLOBAL_SETTINGS"
  } | sort -u
)

if [[ ${#enabled_plugins[@]} -eq 0 ]]; then
  exit 0
fi

# --- Install rules from enabled plugins ---
installed_count=0
plugin_count=0
pruned_versions=0
installed_files=()  # Track what we install for cleanup

for plugin in "${enabled_plugins[@]}"; do
  plugin_cache="${CACHE_ROOT}/${plugin}"

  # Find the highest version directory (semver-aware sort)
  if [[ ! -d "$plugin_cache" ]]; then
    continue
  fi

  version=""
  while IFS= read -r d; do
    [[ -n "$d" ]] && version=$(basename "$d")
  done < <(find "$plugin_cache" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | sort -V)

  if [[ -z "$version" ]]; then
    continue
  fi

  # Prune older version directories from cache.
  # Safety: never prune the version dir we're currently executing from
  # (the running thinking plugin); subsequent hook scripts in this session
  # still need it on disk.
  for d in "$plugin_cache"/*/; do
    [[ -d "$d" ]] || continue
    other=$(basename "$d")
    if [[ "$other" == "$version" ]]; then
      continue
    fi
    if [[ "$plugin" == "$plugin_dir" && "$other" == "$version_dir" ]]; then
      continue
    fi
    rm -rf "$d"
    ((pruned_versions++)) || true
  done

  rules_source="${plugin_cache}/${version}/rules"
  if [[ ! -d "$rules_source" ]]; then
    continue
  fi

  plugin_installed=0
  for rule_file in "$rules_source"/*.md; do
    [[ -f "$rule_file" ]] || continue

    filename=$(basename "$rule_file")
    target_name="${MARKETPLACE}--${plugin}--${version}--${filename}"
    target_path="${RULES_DIR}/${target_name}"

    # Track this as an expected file
    installed_files+=("$target_name")

    # Only copy if content differs or file doesn't exist
    if [[ -f "$target_path" ]] && cmp -s "$rule_file" "$target_path"; then
      continue
    fi

    # Atomic write: temp file then move
    tmp_file=$(mktemp "${RULES_DIR}/.tmp.XXXXXX")
    cp "$rule_file" "$tmp_file"
    mv "$tmp_file" "$target_path"

    ((installed_count++)) || true
    plugin_installed=1
  done

  if [[ $plugin_installed -eq 1 ]] || ls "$rules_source"/*.md >/dev/null 2>&1; then
    ((plugin_count++)) || true
  fi
done

# --- Cleanup stale rules ---
# Remove any <marketplace>--* files that weren't just installed
removed_count=0
for existing in "$RULES_DIR"/${MARKETPLACE}--*.md; do
  [[ -f "$existing" ]] || continue

  existing_name=$(basename "$existing")

  # Check if this file is in our installed list
  found=0
  for expected in "${installed_files[@]}"; do
    if [[ "$expected" == "$existing_name" ]]; then
      found=1
      break
    fi
  done

  if [[ $found -eq 0 ]]; then
    rm "$existing"
    ((removed_count++)) || true
  fi
done

# --- Output summary ---
if [[ $installed_count -gt 0 || $removed_count -gt 0 || $pruned_versions -gt 0 ]]; then
  echo "<learning-context>"
  if [[ $installed_count -gt 0 ]]; then
    echo "Installed ${installed_count} new/updated rules from ${plugin_count} plugins (${MARKETPLACE})"
  fi
  if [[ $removed_count -gt 0 ]]; then
    echo "Removed ${removed_count} stale rules"
  fi
  if [[ $pruned_versions -gt 0 ]]; then
    echo "Pruned ${pruned_versions} old plugin version directories from cache"
  fi
  echo "</learning-context>"
fi
