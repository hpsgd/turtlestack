#!/usr/bin/env bash
# Wrapper for render-meeting-pdf.py that runs the renderer inside a Docker
# image built from scripts/Dockerfile. The only host requirement is Docker.
#
# On first run (or when the Dockerfile / script / publishing assets change)
# the image is built locally (~30-60s). Subsequent runs reuse the cached
# image (~1s overhead per invocation).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PLUGINS_ROOT="$(cd "$PLUGIN_ROOT/../.." && pwd)"
DOCKERFILE="$SCRIPT_DIR/Dockerfile"
SCRIPT="$SCRIPT_DIR/render-meeting-pdf.py"
PUBLISHING_ASSETS="$PLUGINS_ROOT/practices/publishing/assets"

if ! command -v docker >/dev/null 2>&1; then
  echo "error: docker not found on PATH. Install Docker Desktop or the docker engine." >&2
  exit 69
fi

if [ ! -d "$PUBLISHING_ASSETS" ]; then
  echo "error: publishing plugin assets not found at $PUBLISHING_ASSETS." >&2
  echo "       The meeting-pdf renderer reads brand fonts/logos from there." >&2
  exit 70
fi

hash_inputs() {
  {
    cat "$DOCKERFILE" "$SCRIPT"
    find "$PUBLISHING_ASSETS" -type f -exec shasum -a 256 {} + | sort
  } | shasum -a 256 | cut -c1-12
}

IMAGE_TAG="turtlestack/coordinator-meeting-pdf:$(hash_inputs)"

if ! docker image inspect "$IMAGE_TAG" >/dev/null 2>&1; then
  echo "Building $IMAGE_TAG (one-off, ~30-60s)..." >&2
  docker build --quiet \
    -f "$DOCKERFILE" \
    -t "$IMAGE_TAG" \
    "$PLUGINS_ROOT" >/dev/null
fi

docker_args=(
  --rm
  -v "$HOME:$HOME"
  -v "/tmp:/tmp"
  -w "$PWD"
  -u "$(id -u):$(id -g)"
  -e HOME="$HOME"
)

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
