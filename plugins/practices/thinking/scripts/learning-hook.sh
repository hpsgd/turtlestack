#!/bin/bash
# Learning hook — runs on SessionStart to analyse the previous session.
# Called by the thinking plugin's SessionStart hook.
#
# Finds the most recently completed session transcript for this project
# and runs analyse-session.py on it if not already analysed.

set -euo pipefail

PLUGIN_ROOT="${1:-}"
PROJECT_DIR="${2:-$(pwd)}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ANALYSE_SCRIPT="$SCRIPT_DIR/analyse-session.py"

# Derive marketplace name from PLUGIN_ROOT
# (e.g. ~/.claude/plugins/cache/turtlestack/thinking/1.16.0 -> turtlestack).
# Used to namespace learning state under .claude/<marketplace>/learnings.
MARKETPLACE=""
if [ -n "$PLUGIN_ROOT" ]; then
    cache_path="${PLUGIN_ROOT%/}"
    cache_path=$(dirname "$cache_path")  # strip version
    cache_path=$(dirname "$cache_path")  # strip plugin name
    MARKETPLACE=$(basename "$cache_path")
    [ "$MARKETPLACE" = "cache" ] && MARKETPLACE=""
fi
MARKETPLACE="${MARKETPLACE:-turtlestack}"

# Determine transcript directories for this project and its worktrees.
# Claude stores transcripts at ~/.claude/projects/-{PATH_HASH}/ where
# PATH_HASH replaces all non-alphanumeric chars with -.
CLAUDE_PROJECTS_DIR="$HOME/.claude/projects"

if [ ! -d "$CLAUDE_PROJECTS_DIR" ]; then
    exit 0
fi

path_to_hash() {
    echo "$1" | sed 's|^/||; s|[^a-zA-Z0-9]|-|g'
}

# Collect transcript dirs: current project + worktrees (active and removed).
#
# Active worktrees come from git worktree list. Removed worktrees are
# discovered via breadcrumb files: each worktree session writes a
# "parent-project" file to its transcript dir on SessionStart. The
# learning hook scans all transcript dirs for breadcrumbs pointing to
# this project, so deleted worktree transcripts are still found.
TRANSCRIPT_DIRS=()
MAIN_HASH=$(path_to_hash "$PROJECT_DIR")
MAIN_HASH_DIR="$CLAUDE_PROJECTS_DIR/-$MAIN_HASH"
[ -d "$MAIN_HASH_DIR" ] && TRANSCRIPT_DIRS+=("$MAIN_HASH_DIR")

# Write breadcrumb for the current session so future runs can find it.
# For the main project this is redundant but harmless.
if [ -d "$MAIN_HASH_DIR" ]; then
    echo "$PROJECT_DIR" > "$MAIN_HASH_DIR/parent-project"
fi

# Active worktrees (git worktree list)
if command -v git >/dev/null 2>&1 && git -C "$PROJECT_DIR" rev-parse --git-dir >/dev/null 2>&1; then
    while IFS= read -r wt_path; do
        wt_hash=$(path_to_hash "$wt_path")
        wt_dir="$CLAUDE_PROJECTS_DIR/-$wt_hash"
        [ -d "$wt_dir" ] && [ "$wt_dir" != "$MAIN_HASH_DIR" ] && TRANSCRIPT_DIRS+=("$wt_dir")
    done < <(git -C "$PROJECT_DIR" worktree list --porcelain | sed -n 's/^worktree //p')
fi

# Removed worktrees (breadcrumb scan). Resolve the main project path
# to handle symlinks/trailing slashes consistently.
RESOLVED_PROJECT=$(cd "$PROJECT_DIR" 2>/dev/null && pwd -P)
for breadcrumb in "$CLAUDE_PROJECTS_DIR"/*/parent-project; do
    [ -f "$breadcrumb" ] || continue
    bc_dir=$(dirname "$breadcrumb")
    # Skip dirs we already have
    [[ " ${TRANSCRIPT_DIRS[*]} " == *" $bc_dir "* ]] && continue
    bc_project=$(cat "$breadcrumb")
    RESOLVED_BC=$(cd "$bc_project" 2>/dev/null && pwd -P 2>/dev/null || echo "$bc_project")
    [ "$RESOLVED_BC" = "$RESOLVED_PROJECT" ] && TRANSCRIPT_DIRS+=("$bc_dir")
done

if [ ${#TRANSCRIPT_DIRS[@]} -eq 0 ]; then
    exit 0
fi

# Find the most recent JSONL file across all transcript dirs that is
# NOT the current session (skip files modified in the last 60 seconds)
CURRENT_TIME=$(date +%s)
LATEST_JSONL=""
LATEST_MTIME=0

for hash_dir in "${TRANSCRIPT_DIRS[@]}"; do
    for jsonl in "$hash_dir"/*.jsonl; do
        [ -f "$jsonl" ] || continue
        MTIME=$(stat -f %m "$jsonl" 2>/dev/null || stat -c %Y "$jsonl" 2>/dev/null || echo 0)
        AGE=$((CURRENT_TIME - MTIME))

        if [ "$AGE" -lt 60 ]; then
            continue
        fi

        if [ "$MTIME" -gt "$LATEST_MTIME" ]; then
            LATEST_MTIME=$MTIME
            LATEST_JSONL=$jsonl
        fi
    done
done

if [ -z "$LATEST_JSONL" ]; then
    exit 0
fi

# Check if already analysed
SESSION_ID=$(basename "$LATEST_JSONL" .jsonl)
# LEARNINGS_DIR / GLOBAL_LEARNINGS_DIR can be overridden via env var (used by
# test harnesses to redirect outside permission-gated .claude/ paths).
PROJECT_LEARNINGS="${LEARNINGS_DIR:-$PROJECT_DIR/.claude/$MARKETPLACE/learnings}"
GLOBAL_LEARNINGS="${GLOBAL_LEARNINGS_DIR:-$HOME/.claude/$MARKETPLACE/learnings}"

if [ -f "$PROJECT_LEARNINGS/sessions/$SESSION_ID.json" ] || \
   [ -f "$GLOBAL_LEARNINGS/sessions/$SESSION_ID.json" ]; then
    exit 0  # Already analysed
fi

# Run analysis
if [ -f "$ANALYSE_SCRIPT" ]; then
    python3 "$ANALYSE_SCRIPT" "$LATEST_JSONL" \
        --project-dir "$PROJECT_LEARNINGS" \
        --global-dir "$GLOBAL_LEARNINGS" \
        >/dev/null 2>&1 || true
fi

# Run pattern detection (scans all accumulated sessions)
PATTERNS_SCRIPT="$SCRIPT_DIR/detect-patterns.py"
if [ -f "$PATTERNS_SCRIPT" ]; then
    python3 "$PATTERNS_SCRIPT" \
        --project-dir "$PROJECT_LEARNINGS" \
        --global-dir "$GLOBAL_LEARNINGS" \
        >/dev/null 2>&1 || true
fi

# Generate metrics summary
METRICS_SCRIPT="$SCRIPT_DIR/generate-metrics.py"
if [ -f "$METRICS_SCRIPT" ]; then
    python3 "$METRICS_SCRIPT" \
        --project-dir "$PROJECT_LEARNINGS" \
        --global-dir "$GLOBAL_LEARNINGS" \
        >/dev/null 2>&1 || true
fi
