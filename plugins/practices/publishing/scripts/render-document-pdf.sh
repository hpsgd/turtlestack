#!/usr/bin/env bash
# Wrapper for render-document-pdf.py that runs the renderer inside a Docker
# image built from scripts/Dockerfile. The only host requirement is Docker.
#
# On first run (or when the Dockerfile / constraints / script change) the
# image is built locally (~30-60s). Subsequent runs reuse the cached image
# (~1s overhead per invocation).
#
# All paths the user passes must live under $HOME — the wrapper bind-mounts
# $HOME read-write into the container at the same path. Output PDF and any
# referenced CSS/markdown files therefore resolve identically inside and
# outside the container.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DOCKERFILE="$SCRIPT_DIR/Dockerfile"
SCRIPT="$SCRIPT_DIR/render-document-pdf.py"
CONSTRAINTS="$SCRIPT_DIR/constraints.txt"
ASSETS_DIR="$PLUGIN_ROOT/assets"

if ! command -v docker >/dev/null 2>&1; then
  echo "error: docker not found on PATH. Install Docker Desktop or the docker engine." >&2
  exit 69
fi

hash_inputs() {
  {
    cat "$DOCKERFILE" "$CONSTRAINTS" "$SCRIPT"
    find "$ASSETS_DIR" -type f -exec shasum -a 256 {} + | sort
  } | shasum -a 256 | cut -c1-12
}

IMAGE_TAG="turtlestack/publishing-document-pdf:$(hash_inputs)"

if ! docker image inspect "$IMAGE_TAG" >/dev/null 2>&1; then
  echo "Building $IMAGE_TAG (one-off, ~30-60s)..." >&2
  docker build --quiet \
    -f "$DOCKERFILE" \
    -t "$IMAGE_TAG" \
    "$PLUGIN_ROOT" >/dev/null
fi

# Mount $HOME and /tmp so most user-supplied absolute paths resolve identically
# inside the container. Run as the host user so output files have correct
# ownership on Linux; on macOS Docker Desktop the UID is translated already.
# For unusual paths outside $HOME and /tmp, set TURTLESTACK_DOCKER_MOUNTS as
# a colon-separated list of host paths to bind-mount at the same path.
docker_args=(
  --rm
  -v "$HOME:$HOME"
  -v "/tmp:/tmp"
  -w "$PWD"
  -u "$(id -u):$(id -g)"
  -e HOME="$HOME"
)

# Add $PWD mount only if it's not already covered by $HOME or /tmp.
case "$PWD/" in
  "$HOME/"*|/tmp/*) ;;
  *) docker_args+=(-v "$PWD:$PWD") ;;
esac

if [ -n "${TURTLESTACK_DOCKER_MOUNTS:-}" ]; then
  IFS=':' read -ra extra_mounts <<< "$TURTLESTACK_DOCKER_MOUNTS"
  for m in "${extra_mounts[@]}"; do
    [ -n "$m" ] && docker_args+=(-v "$m:$m")
  done
fi

exec docker run "${docker_args[@]}" "$IMAGE_TAG" "$@"
