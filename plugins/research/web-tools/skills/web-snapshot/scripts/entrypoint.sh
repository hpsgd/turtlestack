#!/usr/bin/env bash
# Entrypoint for the web-snapshot image. Runs the snapshot script as root
# (Chromium needs that inside the container) and chowns the output directory
# back to the host UID/GID afterwards so the resulting PDFs aren't owned by
# root on the host filesystem.
#
# Host UID/GID are passed as RUN_AS_UID / RUN_AS_GID environment variables
# by the wrapper script; if absent, no chown happens (Docker Desktop on
# macOS already maps file ownership and these are unset there).

set -euo pipefail

cleanup() {
  if [ -n "${RUN_AS_UID:-}" ] && [ -n "${RUN_AS_GID:-}" ] && [ -n "${OUT_DIR:-}" ]; then
    if [ -d "$OUT_DIR" ]; then
      chown -R "$RUN_AS_UID:$RUN_AS_GID" "$OUT_DIR" 2>/dev/null || true
    fi
  fi
}
trap cleanup EXIT

# Sniff --out from the args so we know what to chown. Default matches the
# script's own default.
OUT_DIR="./web-snapshots"
prev=""
for arg in "$@"; do
  if [ "$prev" = "--out" ]; then
    OUT_DIR="$arg"
  fi
  prev="$arg"
done

exec python3 /opt/turtlestack/web-snapshot.py "$@"
