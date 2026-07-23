#!/usr/bin/env bash
# show-notices.sh — Surface unseen change notices on session start.
#
# Reads notices shipped in the plugin (notices.json), compares them against a
# per-machine seen-marker, and shows any the user hasn't seen yet exactly once.
# Emits a visible systemMessage (one line per notice) plus model
# additionalContext so the model can help action each notice. Records shown ids
# in the seen-marker so they don't reappear.
#
# Silent on no-op, writes a per-marketplace detail file on overflow, derives
# paths from env.
#
# Silent when nothing is unseen. Fails silent on errors (never blocks session
# start — every error path exits 0).

set -uo pipefail

# No plugin root → can't locate notices.json. Nothing to do.
[[ -z "${CLAUDE_PLUGIN_ROOT:-}" ]] && exit 0

CONFIG_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-}"

# Derive marketplace name from CLAUDE_PLUGIN_ROOT to namespace notice state,
# exactly as learning-readback.sh does (strip version, strip plugin, basename;
# fall back to "turtlestack" if not running as an installed hook).
MARKETPLACE=""
cache_path="${CLAUDE_PLUGIN_ROOT%/}"
cache_path=$(dirname "$cache_path")  # strip version
cache_path=$(dirname "$cache_path")  # strip plugin name
MARKETPLACE=$(basename "$cache_path")
[ "$MARKETPLACE" = "cache" ] && MARKETPLACE=""
MARKETPLACE="${MARKETPLACE:-turtlestack}"

# Installed plugin version is the basename of CLAUDE_PLUGIN_ROOT, which contains
# the version when running as an installed hook. Recorded as baseline_version in
# the seen-marker on first run.
INSTALLED_VERSION=$(basename "${CLAUDE_PLUGIN_ROOT%/}")

NOTICES_CONFIG_DIR="$CONFIG_DIR" \
NOTICES_PROJECT_DIR="$PROJECT_DIR" \
NOTICES_MARKETPLACE="$MARKETPLACE" \
NOTICES_PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT%/}" \
NOTICES_INSTALLED_VERSION="$INSTALLED_VERSION" \
NOTICES_FIRST_RUN="${NOTICES_FIRST_RUN:-auto}" \
python3 - <<'PY' 2>/dev/null
import glob, json, os, sys
from datetime import datetime, timezone

CONFIG_DIR = os.environ["NOTICES_CONFIG_DIR"]
PROJECT_DIR = os.environ.get("NOTICES_PROJECT_DIR", "")
MARKETPLACE = os.environ["NOTICES_MARKETPLACE"]
PLUGIN_ROOT = os.environ["NOTICES_PLUGIN_ROOT"]
INSTALLED_VERSION = os.environ.get("NOTICES_INSTALLED_VERSION", "")
FIRST_RUN_MODE = os.environ.get("NOTICES_FIRST_RUN") or "auto"

STATE_DIR = os.path.join(CONFIG_DIR, MARKETPLACE)
SEEN_PATH = os.path.join(STATE_DIR, "notices-seen.json")
DEBUG_LOG = os.path.join(STATE_DIR, "notices-debug.log")
INSTALLED_PLUGINS = os.path.join(CONFIG_DIR, "plugins", "installed_plugins.json")
NOTICES_PATH = os.path.join(PLUGIN_ROOT, "notices.json")

# Detail file: project scope when a project dir is set, user scope otherwise.
DETAIL_DIR = os.path.join(PROJECT_DIR, ".claude", MARKETPLACE) if PROJECT_DIR else STATE_DIR
DETAIL_FILE = os.path.join(DETAIL_DIR, "notices.md")

BUDGET = 1900
GLYPH = {"breaking": "⛔", "action": "⚠", "info": "ℹ"}
ORDER = {"breaking": 0, "action": 1, "info": 2}


def log_debug(msg):
    try:
        os.makedirs(STATE_DIR, exist_ok=True)
        with open(DEBUG_LOG, "a") as f:
            f.write(f"{datetime.now(timezone.utc).isoformat()} {msg}\n")
    except Exception:
        pass


def display_path(path):
    if PROJECT_DIR and path.startswith(PROJECT_DIR + os.sep):
        return path[len(PROJECT_DIR) + 1:]
    return path


# --- Load notices (missing/malformed -> silent) ---
try:
    with open(NOTICES_PATH) as f:
        data = json.load(f)
    raw = data.get("notices", [])
    if not isinstance(raw, list):
        sys.exit(0)
except Exception:
    sys.exit(0)

valid = []
for n in raw:
    if not isinstance(n, dict):
        continue
    nid, ver = n.get("id"), n.get("version")
    title, msg = n.get("title"), n.get("message")
    if not (nid and ver and title and msg):
        continue
    sev = n.get("severity", "info")
    if sev not in GLYPH:
        sev = "info"
    valid.append({
        "id": nid,
        "version": str(ver),
        "severity": sev,
        "plugin": n.get("plugin"),
        "title": title,
        "message": msg,
    })

if not valid:
    sys.exit(0)

all_ids = [n["id"] for n in valid]

# --- Installed plugins (for plugin-scoped notices) ---
installed_names = set()
try:
    with open(INSTALLED_PLUGINS) as f:
        ip = json.load(f)
    for key in ip.get("plugins", {}).keys():
        installed_names.add(key.split("@", 1)[0])
except Exception:
    installed_names = set()


def plugin_eligible(n):
    p = n.get("plugin")
    return True if not p else p in installed_names


def has_footprint():
    # Evidence that this marketplace has done work on this machine before.
    # Only analysed session records count — NOT directory existence and NOT
    # .claude/rules/ (install-rules.sh writes rules on every first run and would
    # false-positive a fresh install). The script's own files (notices-seen.json,
    # notices.md, notices-debug.log) live directly under <marketplace>/ and are
    # never on these learnings paths, so they're naturally excluded.
    scopes = [STATE_DIR]
    if PROJECT_DIR:
        scopes.append(os.path.join(PROJECT_DIR, ".claude", MARKETPLACE))
    for base in scopes:
        if glob.glob(os.path.join(base, "learnings", "sessions", "*.json")):
            return True
    return False


# --- Seen-marker ---
seen = set()
baseline_version = INSTALLED_VERSION
marker_exists = os.path.exists(SEEN_PATH)
if marker_exists:
    try:
        with open(SEEN_PATH) as f:
            m = json.load(f)
        seen = set(m.get("seen", []))
        baseline_version = m.get("baseline_version", INSTALLED_VERSION)
    except Exception:
        # Corrupt marker: treat as a fresh machine and re-baseline rather than
        # risk dumping the whole backlog.
        marker_exists = False
        seen = set()

to_show = []
new_seen = set(seen)

if not marker_exists:
    # First run on this machine. Decide whether to show the backlog or seed it
    # silently, based on the mode and the prior-work footprint.
    baseline_version = INSTALLED_VERSION
    if FIRST_RUN_MODE == "baseline":
        show_first_run = False
    elif FIRST_RUN_MODE == "show":
        show_first_run = True
    else:  # auto (default): existing user (footprint) sees it, fresh install doesn't.
        show_first_run = has_footprint()

    if show_first_run:
        # Existing user: show eligible notices, record them seen, baseline.
        # Plugin-ineligible notices stay unseen so they can surface once the
        # plugin is installed (same rule as a normal run).
        to_show = [n for n in valid if plugin_eligible(n)]
    else:
        # Fresh install: seed everything as seen, show nothing.
        new_seen = set(all_ids)
        to_show = []
else:
    # Normal run: unseen and plugin-eligible.
    to_show = [n for n in valid if n["id"] not in seen and plugin_eligible(n)]

need_write = (not marker_exists) or bool(to_show)


def write_marker():
    try:
        os.makedirs(STATE_DIR, exist_ok=True)
        with open(SEEN_PATH, "w") as f:
            json.dump({"seen": sorted(new_seen), "baseline_version": baseline_version}, f, indent=2)
            f.write("\n")
        return True
    except Exception as e:
        log_debug(f"failed to write seen-marker {SEEN_PATH}: {e}")
        return False


if not to_show:
    # Silent. Still seed the marker on first run.
    if need_write:
        write_marker()
    sys.exit(0)

# Order by severity (breaking, action, info); stable within a tier.
to_show.sort(key=lambda n: ORDER.get(n["severity"], 2))

for n in to_show:
    new_seen.add(n["id"])

# --- Build output ---
context_lines = [
    "<turtlestack-notices>",
    "Change notices for this marketplace. Help the user action each one:",
]
for n in to_show:
    context_lines.append(f"- [{n['severity']}] ({n['version']}) {n['title']}: {n['message']}")
context_lines.append("</turtlestack-notices>")
context_full = "\n".join(context_lines)

msg_lines = [f"{GLYPH[n['severity']]} {n['title']}" for n in to_show]


def write_detail():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        os.makedirs(DETAIL_DIR, exist_ok=True)
        with open(DETAIL_FILE, "w") as f:
            f.write(f"# Change notices — {MARKETPLACE}\n\n")
            f.write(f"Generated: {now}\n\n")
            f.write(f"{len(to_show)} unseen notice(s).\n\n")
            for n in to_show:
                f.write(f"## {GLYPH[n['severity']]} {n['title']}\n\n")
                f.write(f"- id: {n['id']}\n")
                f.write(f"- version: {n['version']}\n")
                f.write(f"- severity: {n['severity']}\n")
                if n.get("plugin"):
                    f.write(f"- plugin: {n['plugin']}\n")
                f.write(f"\n{n['message']}\n\n")
        return True
    except Exception as e:
        log_debug(f"failed to write detail file {DETAIL_FILE}: {e}")
        return False


if len(context_full) > BUDGET:
    if write_detail():
        disp = display_path(DETAIL_FILE)
        msg_lines.append(f"Full details: {disp}")
        context = (
            f"<turtlestack-notices>{len(to_show)} change notice(s) — "
            f"full text written to {DETAIL_FILE}</turtlestack-notices>"
        )
    else:
        context = context_full[:BUDGET]
else:
    context = context_full

# Record shown notices as seen. A write failure here means the notices re-show
# next session (annoying, not harmful) — we still show them now.
write_marker()

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": context,
    },
    "systemMessage": "\n".join(msg_lines),
}))
PY

exit 0
