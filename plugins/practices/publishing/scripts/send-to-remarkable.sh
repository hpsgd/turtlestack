#!/usr/bin/env bash
# Upload a PDF to a reMarkable device via the cloud, using the community-maintained
# ddvk/rmapi CLI. The binary is treated as an external dependency so it can be
# updated independently of this plugin.
#
# Install: download the prebuilt binary for your platform from
# https://github.com/ddvk/rmapi/releases and put it on PATH. (`go install
# github.com/ddvk/rmapi@latest` does not work — ddvk's go.mod has replace
# directives that go install refuses. The io41/tap homebrew formula exists but
# tends to lag upstream by several versions, which matters because the cloud
# sync protocol breaks `put` on older releases.)
#
# First run requires `rmapi` interactively to pair the device (one-time code
# from https://my.remarkable.com/device/browser).
#
# Usage: send-to-remarkable.sh <pdf-path> [<remote-folder>]
#
# Default remote folder is "/" (root of My Files). Pass "/Meetings" or similar
# to drop into a sub-folder; the folder must already exist on the device.

set -euo pipefail

if [ $# -lt 1 ] || [ $# -gt 2 ]; then
  echo "usage: $(basename "$0") <pdf-path> [<remote-folder>]" >&2
  exit 64
fi

PDF="$1"
DEST="${2:-/}"

if [ ! -f "$PDF" ]; then
  echo "error: file not found: $PDF" >&2
  exit 66
fi

if ! command -v rmapi >/dev/null 2>&1; then
  cat >&2 <<'EOF'
error: rmapi not found on PATH

Install ddvk/rmapi (the active community fork — original juruen/rmapi is archived).
Download the prebuilt binary for your platform from:

  https://github.com/ddvk/rmapi/releases

Place it on your PATH (e.g. /opt/homebrew/bin on macOS, ~/.local/bin on Linux if
that's on your PATH).

Then run `rmapi` once interactively to pair with your device using a one-time
code from https://my.remarkable.com/device/browser. After that this script will
work non-interactively.

Note: `go install github.com/ddvk/rmapi@latest` does NOT work — ddvk's go.mod
has replace directives that go install refuses. Use the release binary.
EOF
  exit 69
fi

# rmapi's `put` reads from the local PDF and uploads to the cloud. The device
# syncs next time it's online. Output goes to stdout/stderr from rmapi directly
# so any failure (auth expired, sync15 protocol mismatch, network) surfaces.
exec rmapi put "$PDF" "$DEST"
