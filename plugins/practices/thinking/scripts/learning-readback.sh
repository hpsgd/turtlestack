#!/bin/bash
# Learning readback — runs on SessionStart (sync).
# Reads recent learnings and outputs them to stdout for context injection.
# Output appears as system context in the conversation.
#
# Budget: <2000 characters to avoid context bloat.

set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"

# Derive marketplace name from CLAUDE_PLUGIN_ROOT to namespace learning state.
# Falls back to "turtlestack" if not running as a hook.
MARKETPLACE=""
if [ -n "${CLAUDE_PLUGIN_ROOT:-}" ]; then
    cache_path="${CLAUDE_PLUGIN_ROOT%/}"
    cache_path=$(dirname "$cache_path")  # strip version
    cache_path=$(dirname "$cache_path")  # strip plugin name
    MARKETPLACE=$(basename "$cache_path")
    [ "$MARKETPLACE" = "cache" ] && MARKETPLACE=""
fi
MARKETPLACE="${MARKETPLACE:-turtlestack}"

# LEARNINGS_DIR / GLOBAL_LEARNINGS_DIR can be overridden via env var (used by
# test harnesses to redirect outside permission-gated .claude/ paths).
PROJECT_LEARNINGS="${LEARNINGS_DIR:-$PROJECT_DIR/.claude/$MARKETPLACE/learnings}"
GLOBAL_LEARNINGS="${GLOBAL_LEARNINGS_DIR:-$HOME/.claude/$MARKETPLACE/learnings}"

output=""

# --- Recent session learnings ---
for learnings_dir in "$PROJECT_LEARNINGS/sessions" "$GLOBAL_LEARNINGS/sessions"; do
    [ -d "$learnings_dir" ] || continue

    # Find the 2 most recent analysis files
    RECENT=$(ls -t "$learnings_dir"/*.json 2>/dev/null | head -2)
    for f in $RECENT; do
        SUMMARY=$(python3 -c "
import json, sys
try:
    with open('$f') as fh:
        d = json.load(fh)
    m = d.get('metrics', {})
    c = m.get('corrections', {})
    total_c = c.get('total', 0)
    if total_c > 0:
        print(f'Session {d[\"session_id\"][:8]}...: {total_c} corrections (rate: {m.get(\"correction_rate\", 0):.0%})')
        for evt in d.get('events', [])[:2]:
            if evt.get('type') in ('immediate_correction', 'approach_change'):
                print(f'  - {evt.get(\"user_said\", \"\")[:100]}')
except: pass
" 2>/dev/null)

        if [ -n "$SUMMARY" ]; then
            output="$output$SUMMARY\n"
        fi
    done
done

# --- High-confidence wisdom ---
for wisdom_dir in "$PROJECT_DIR/.claude/wisdom" "$HOME/.claude/wisdom"; do
    [ -d "$wisdom_dir" ] || continue

    WISDOM=$(python3 -c "
import os, re
wisdom_dir = '$wisdom_dir'
principles = []
for f in os.listdir(wisdom_dir):
    if not f.endswith('.md'): continue
    with open(os.path.join(wisdom_dir, f)) as fh:
        for line in fh:
            m = re.search(r'\[CRYSTAL\s+(\d+)%\]\s+(.*)', line)
            if m and int(m.group(1)) >= 85:
                principles.append(f'  - [{f.replace(\".md\",\"\")}] {m.group(2).strip()} ({m.group(1)}%)')
if principles:
    print('High-confidence wisdom:')
    for p in principles[:5]:
        print(p)
" 2>/dev/null)

    if [ -n "$WISDOM" ]; then
        output="$output$WISDOM\n"
    fi
done

# --- Plugin version change detection ---
# Check if any installed plugin versions have changed since last reconciliation
RECONCILE_SNAPSHOT="$GLOBAL_LEARNINGS/reconcile-snapshot.json"
LEARNED_RULES_EXIST=false
for dir in "$HOME/.claude/rules" "$PROJECT_DIR/.claude/rules"; do
    if ls "$dir"/learned--*.md >/dev/null 2>&1; then
        LEARNED_RULES_EXIST=true
        break
    fi
done

if [ "$LEARNED_RULES_EXIST" = true ]; then
    VERSION_CHANGED=$(python3 -c "
import json, os, glob

# Build current plugin version map from installed rules (plugin name from prefix)
current_rules = set()
for d in ['$HOME/.claude/rules', '$PROJECT_DIR/.claude/rules']:
    for f in glob.glob(os.path.join(d, '*.md')):
        basename = os.path.basename(f)
        if not basename.startswith('learned--'):
            # Extract plugin name from prefix (e.g., 'coding-standards' from 'coding-standards--python.md')
            parts = basename.split('--', 1)
            if len(parts) == 2:
                current_rules.add(parts[0])

# Compare against snapshot
snapshot_file = '$RECONCILE_SNAPSHOT'
if not os.path.exists(snapshot_file):
    # No snapshot yet — if there are both learned and marketplace rules, nudge
    if current_rules:
        print('new')
else:
    try:
        with open(snapshot_file) as f:
            snapshot = json.load(f)
        old_rules = set(snapshot.get('marketplace_plugins', []))
        if current_rules != old_rules:
            print('changed')
    except:
        print('new')
" 2>/dev/null)

    if [ -n "$VERSION_CHANGED" ]; then
        # The nudge fires in every live session until someone reconciles (which updates the
        # snapshot). reconcile-rules deletes from a shared global dir, so if several sessions all
        # act on this nudge at once they can race. When other sessions are live, steer to a
        # single-session run rather than fanning the cleanup out. Same signal as the skill's 4a guard.
        CLAUDE_SESSIONS=$(pgrep -x claude 2>/dev/null | wc -l | tr -d ' ')
        if [ "${CLAUDE_SESSIONS:-1}" -gt 1 ]; then
            output="${output}Plugin rules have changed since last reconciliation. Run /thinking:reconcile-rules to check for superseded learned rules — but other Claude sessions are live, so run it in a single session (close the others first) to avoid a concurrent-delete race.\n"
        else
            output="${output}Plugin rules have changed since last reconciliation. Run /thinking:reconcile-rules to check if any learned rules are now superseded.\n"
        fi
    fi
fi

# Only output if we have something (keep context clean)
if [ -n "$output" ]; then
    echo "<learning-context>"
    echo -e "$output" | head -c 1900  # Hard budget limit
    echo "</learning-context>"
fi
