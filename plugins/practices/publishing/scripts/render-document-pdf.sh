#!/usr/bin/env bash
# Wrapper for render-document-pdf.py that runs the renderer inside a Docker
# image. The only host requirement is Docker.
#
# Image resolution order:
#   1. local hash tag    — preserves dev iteration on Dockerfile changes
#   2. local registry tag — already pulled from ghcr.io
#   3. docker pull        — first run on a fresh host
#   4. docker build       — offline, fork, or image-missing fallback
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
PLUGIN_JSON="$PLUGIN_ROOT/.claude-plugin/plugin.json"

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

plugin_version() {
  [ -f "$PLUGIN_JSON" ] || return 0
  grep -E '"version"[[:space:]]*:' "$PLUGIN_JSON" | head -1 \
    | sed -E 's/.*"version"[[:space:]]*:[[:space:]]*"([^"]+)".*/\1/'
}

VERSION="$(plugin_version)"
IMAGE_HASH_TAG="turtlestack/publishing-document-pdf:$(hash_inputs)"
IMAGE_REGISTRY_TAG="ghcr.io/hpsgd/turtlestack-publishing-document-pdf:${VERSION}"

if docker image inspect "$IMAGE_HASH_TAG" >/dev/null 2>&1; then
  IMAGE_TAG="$IMAGE_HASH_TAG"
elif [ -n "$VERSION" ] && docker image inspect "$IMAGE_REGISTRY_TAG" >/dev/null 2>&1; then
  IMAGE_TAG="$IMAGE_REGISTRY_TAG"
elif [ -n "$VERSION" ] && docker pull --quiet "$IMAGE_REGISTRY_TAG" >/dev/null 2>&1; then
  IMAGE_TAG="$IMAGE_REGISTRY_TAG"
else
  echo "Building $IMAGE_HASH_TAG locally (registry image unavailable)..." >&2
  docker build --quiet \
    -f "$DOCKERFILE" \
    -t "$IMAGE_HASH_TAG" \
    "$PLUGIN_ROOT" >/dev/null
  IMAGE_TAG="$IMAGE_HASH_TAG"
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
