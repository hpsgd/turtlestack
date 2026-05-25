#!/usr/bin/env bash
# Upload a PDF to a reMarkable device via the reMarkable cloud, using the
# community-maintained ddvk/rmapi CLI built inside a Docker image. The only
# host requirement is Docker.
#
# Auth state lives on the host at ~/.config/rmapi/ — it's bind-mounted into
# the container so pairing persists. First-time pairing is interactive and
# requires running the script in --pair mode first:
#
#   send-to-remarkable.sh --pair                  # one-time interactive pairing
#   send-to-remarkable.sh <pdf-path> [<folder>]   # normal upload
#
# Default remote folder is "/" (root of My Files). The folder must already
# exist on the device.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DOCKERFILE="$SCRIPT_DIR/Dockerfile.remarkable"
CONFIG_DIR="$HOME/.config/rmapi"
LEGACY_CONFIG_DIR="$HOME/.rmapi"

if ! command -v docker >/dev/null 2>&1; then
  echo "error: docker not found on PATH. Install Docker Desktop or the docker engine." >&2
  exit 69
fi

hash_inputs() {
  cat "$DOCKERFILE" | shasum -a 256 | cut -c1-12
}

IMAGE_TAG="turtlestack/remarkable:$(hash_inputs)"

if ! docker image inspect "$IMAGE_TAG" >/dev/null 2>&1; then
  echo "Building $IMAGE_TAG (one-off, ~60-120s)..." >&2
  docker build --quiet \
    -f "$DOCKERFILE" \
    -t "$IMAGE_TAG" \
    "$SCRIPT_DIR" >/dev/null
fi

# Ensure the auth dir exists on the host so the bind-mount creates a directory
# (not a file) inside the container.
mkdir -p "$CONFIG_DIR"

# rmapi looks at $HOME/.config/rmapi/ first; map host's config dir there.
# We deliberately use a fixed in-container HOME (/home/rmapi) so the bind-
# mount target is stable regardless of host UID.
common_mounts=(
  -v "$CONFIG_DIR:/home/rmapi/.config/rmapi"
  -e HOME=/home/rmapi
  -u "$(id -u):$(id -g)"
)

# Surface legacy ~/.rmapi state if the user has an older install — rmapi falls
# back to it for some commands. Mount only if it exists; harmless otherwise.
if [ -d "$LEGACY_CONFIG_DIR" ]; then
  common_mounts+=(-v "$LEGACY_CONFIG_DIR:/home/rmapi/.rmapi")
fi

case "${1:-}" in
  --pair)
    if [ ! -t 0 ]; then
      echo "error: --pair requires an interactive terminal (stdin must be a TTY)." >&2
      echo "       Run this in your terminal, then re-run normal uploads non-interactively." >&2
      exit 64
    fi
    echo "Starting interactive pair. Get a one-time code from https://my.remarkable.com/device/browser" >&2
    # `rmapi ls` requires auth — on an unpaired host it triggers the device-
    # code prompt; on a paired host it lists files (also fine — confirms auth
    # still works). Bare `rmapi` with no subcommand just prints help.
    exec docker run --rm -it "${common_mounts[@]}" "$IMAGE_TAG" ls
    ;;
  -h|--help|"")
    cat <<EOF
usage: $(basename "$0") --pair                  # interactive device pairing (one-time)
       $(basename "$0") <pdf-path> [<folder>]   # upload PDF to reMarkable cloud
EOF
    exit 64
    ;;
esac

PDF="$1"
DEST="${2:-/}"

if [ ! -f "$PDF" ]; then
  echo "error: file not found: $PDF" >&2
  exit 66
fi

# Fail fast if pairing hasn't happened yet — otherwise rmapi prints a cryptic
# auth error and the user blames Docker.
if [ ! -f "$CONFIG_DIR/rmapi.conf" ] && [ ! -f "$LEGACY_CONFIG_DIR/rmapi.conf" ]; then
  echo "error: rmapi is not paired with your device yet." >&2
  echo "       Run: $(basename "$0") --pair" >&2
  echo "       You'll need a one-time code from https://my.remarkable.com/device/browser" >&2
  exit 75
fi

# Resolve PDF to an absolute path so the bind-mount and the in-container
# argument refer to the same file.
PDF_ABS="$(cd "$(dirname "$PDF")" && pwd)/$(basename "$PDF")"

upload_mounts=("${common_mounts[@]}" -v "$PDF_ABS:$PDF_ABS:ro")

exec docker run --rm "${upload_mounts[@]}" "$IMAGE_TAG" put "$PDF_ABS" "$DEST"
