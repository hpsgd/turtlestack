#!/usr/bin/env bash
# security-baseline-hook.sh — Advisory PreToolUse scan of Edit/Write content.
#
# Regex-scans the content being written against patterns.json (the executable
# encoding of the security-baseline rule). On a match it emits an advisory
# additionalContext block plus a one-line systemMessage so the model fixes the
# finding this turn. It NEVER blocks: the tool call always proceeds.
#
# Pure local regex — no network, no LLM, no subprocess per pattern. Silent and
# instant when nothing matches.
#
# Contract:
#   - Reads the PreToolUse event JSON from stdin.
#   - Scans tool_input.content (Write) / new_string (Edit) / each
#     edits[].new_string (MultiEdit). Other tools / no content -> exit 0 silent.
#   - Kill switch: SECURITY_BASELINE_HOOK_DISABLE non-empty -> exit 0.
#   - Caps scanned content at 256 KB. Honours inline `# nosec` / `// nosec`
#     suppression on the matching line or the line above.
#   - EVERY path exits 0 (advisory, never blocks). Malformed/absent
#     patterns.json, oversized content, unreadable input: all silent, exit 0.

set -uo pipefail

# Kill switch — disabled entirely when set to any non-empty value.
[[ -n "${SECURITY_BASELINE_HOOK_DISABLE:-}" ]] && exit 0

# Locate patterns.json: prefer the plugin root (hook context), fall back to the
# script's sibling directory (so the script works when run directly in tests).
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd)"
if [[ -n "${CLAUDE_PLUGIN_ROOT:-}" && -f "${CLAUDE_PLUGIN_ROOT}/patterns.json" ]]; then
    PATTERNS_FILE="${CLAUDE_PLUGIN_ROOT}/patterns.json"
else
    PATTERNS_FILE="${SCRIPT_DIR}/../patterns.json"
fi

CONFIG_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
DEBUG_LOG="${CONFIG_DIR}/security-baseline-hook-debug.log"

# Capture the event JSON (may be large) to a temp file so the python heredoc can
# read it — the heredoc itself occupies python's stdin.
TMP_INPUT="$(mktemp 2>/dev/null)" || exit 0
trap 'rm -f "$TMP_INPUT"' EXIT
cat > "$TMP_INPUT"

SBH_PATTERNS="$PATTERNS_FILE" SBH_INPUT="$TMP_INPUT" SBH_DEBUG="$DEBUG_LOG" \
python3 - <<'PY' 2>/dev/null
import json, os, re, sys
from datetime import datetime, timezone

PATTERNS = os.environ["SBH_PATTERNS"]
INPUT = os.environ["SBH_INPUT"]
DEBUG = os.environ.get("SBH_DEBUG", "")

MAX_BYTES = 256 * 1024
EDIT_TOOLS = {"Edit", "Write", "MultiEdit"}
SEV_ORDER = {"high": 0, "medium": 1, "low": 2}
NOSEC = re.compile(r"(?:#|//)\s*nosec(?::\s*([A-Za-z0-9_-]+))?")


def log(msg):
    if not DEBUG:
        return
    try:
        os.makedirs(os.path.dirname(DEBUG), exist_ok=True)
        with open(DEBUG, "a") as f:
            f.write(f"{datetime.now(timezone.utc).isoformat()} {msg}\n")
    except Exception:
        pass


# --- Read the event (unreadable/malformed -> silent) ---
try:
    with open(INPUT, "rb") as f:
        event = json.loads(f.read().decode("utf-8", "replace"))
except Exception as e:
    log(f"unreadable event: {e}")
    sys.exit(0)

if not isinstance(event, dict):
    sys.exit(0)

tool = event.get("tool_name")
if tool not in EDIT_TOOLS:
    sys.exit(0)

ti = event.get("tool_input")
if not isinstance(ti, dict):
    sys.exit(0)

# --- Extract the content to scan ---
parts = []
if tool == "Write":
    c = ti.get("content")
    if isinstance(c, str):
        parts.append(c)
elif tool == "Edit":
    c = ti.get("new_string")
    if isinstance(c, str):
        parts.append(c)
elif tool == "MultiEdit":
    edits = ti.get("edits")
    if isinstance(edits, list):
        for e in edits:
            if isinstance(e, dict):
                ns = e.get("new_string")
                if isinstance(ns, str):
                    parts.append(ns)

content = "\n".join(parts)
if not content.strip():
    sys.exit(0)

# --- Bound the scan (slice, don't reject) ---
encoded = content.encode("utf-8", "replace")
if len(encoded) > MAX_BYTES:
    content = encoded[:MAX_BYTES].decode("utf-8", "ignore")

# --- Load patterns (malformed/absent -> silent) ---
try:
    with open(PATTERNS) as f:
        pdata = json.load(f)
    raw = pdata.get("patterns", [])
    if not isinstance(raw, list):
        sys.exit(0)
except Exception as e:
    log(f"patterns load failed: {e}")
    sys.exit(0)

compiled = []
for p in raw:
    if not isinstance(p, dict):
        continue
    pid, rx = p.get("id"), p.get("regex")
    if not (pid and rx):
        continue
    try:
        compiled.append((p, re.compile(rx, re.MULTILINE)))
    except Exception as e:
        log(f"bad regex {pid}: {e}")
        continue

if not compiled:
    sys.exit(0)

lines = content.splitlines()


def suppressed(line_idx, pid):
    # A finding is suppressed by a nosec marker on its own line or the line above.
    # Bare nosec suppresses anything; `nosec: <id>` scopes to one pattern.
    for idx in (line_idx, line_idx - 1):
        if idx < 0 or idx >= len(lines):
            continue
        m = NOSEC.search(lines[idx])
        if not m:
            continue
        scope = m.group(1)
        if scope is None or scope == pid:
            return True
    return False


# One finding per pattern id (deduped); first non-suppressed match wins.
findings = {}
for p, cre in compiled:
    pid = p["id"]
    for m in cre.finditer(content):
        line_idx = content.count("\n", 0, m.start())
        if suppressed(line_idx, pid):
            continue
        findings[pid] = p
        break

if not findings:
    sys.exit(0)

ordered = sorted(
    findings.values(),
    key=lambda p: (SEV_ORDER.get(p.get("severity"), 1), p["id"]),
)

ctx = ["<security-baseline-findings>"]
for p in ordered:
    ctx.append(
        f"[{p.get('severity', '?')}] {p['id']} "
        f"({p.get('baseline_ref', '?')}): {p.get('message', '')}"
    )
ctx.append("</security-baseline-findings>")

ids = ", ".join(p["id"] for p in ordered)
message = f"⚠ {len(ordered)} security finding(s): {ids}"

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "additionalContext": "\n".join(ctx),
    },
    "systemMessage": message,
}))
sys.exit(0)
PY

# Advisory hook: succeed regardless of what python did.
exit 0
