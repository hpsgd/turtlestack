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
# PLUGIN_ROOT can be either:
#   - cache path:  ~/.claude/plugins/cache/<marketplace>/<plugin>/<version>
#   - source path: ~/.claude/plugins/marketplaces/<marketplace>/plugins/<category>/<plugin>
# The cache path is used when Claude Code finds an installed cache entry
# matching the current scope. The source path is used as a fallback when no
# matching install is found (e.g. project-scoped install for a different
# project) but the plugin is still enabled.
PLUGIN_ROOT_NORM="${PLUGIN_ROOT%/}"
running_from_cache=0
plugin_dir=""
version_dir=""

if [[ "$PLUGIN_ROOT_NORM" =~ /plugins/cache/([^/]+)/([^/]+)/([^/]+)$ ]]; then
  MARKETPLACE="${BASH_REMATCH[1]}"
  plugin_dir="${BASH_REMATCH[2]}"
  version_dir="${BASH_REMATCH[3]}"
  running_from_cache=1
elif [[ "$PLUGIN_ROOT_NORM" =~ /plugins/marketplaces/([^/]+)(/|$) ]]; then
  MARKETPLACE="${BASH_REMATCH[1]}"
else
  echo "Could not derive marketplace name from CLAUDE_PLUGIN_ROOT=$PLUGIN_ROOT" >&2
  exit 1
fi

# Cache root is at a fixed location regardless of which path the running
# plugin was loaded from.
CONFIG_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
CACHE_ROOT="${CONFIG_DIR}/plugins/cache/${MARKETPLACE}"

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
    if [[ $running_from_cache -eq 1 && "$plugin" == "$plugin_dir" && "$other" == "$version_dir" ]]; then
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

# --- Sweep orphan user-level rule files ---
# The current architecture writes rule files only to PROJECT_DIR/.claude/rules.
# Any <marketplace>-- prefixed file at user level (CONFIG_DIR/rules) is an
# orphan from before this scheme. Sweep for every marketplace currently
# installed on the machine, so a single hook run cleans up everything
# regardless of which marketplace's thinking plugin fired.
user_rules_dir="${CONFIG_DIR}/rules"
user_swept_count=0
if [[ -d "$user_rules_dir" && "$user_rules_dir" != "$RULES_DIR" ]]; then
  marketplaces_dir="${CONFIG_DIR}/plugins/marketplaces"
  if [[ -d "$marketplaces_dir" ]]; then
    for mp_dir in "$marketplaces_dir"/*/; do
      [[ -d "$mp_dir" ]] || continue
      mp_name=$(basename "$mp_dir")
      for existing in "$user_rules_dir"/${mp_name}--*.md; do
        [[ -f "$existing" ]] || continue
        rm "$existing"
        ((user_swept_count++)) || true
      done
    done
  fi
fi

# --- Output summary ---
if [[ $installed_count -gt 0 || $removed_count -gt 0 || $pruned_versions -gt 0 || $user_swept_count -gt 0 ]]; then
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
  if [[ $user_swept_count -gt 0 ]]; then
    echo "Swept ${user_swept_count} orphan rule file(s) from ${user_rules_dir}"
  fi
  echo "</learning-context>"
fi
