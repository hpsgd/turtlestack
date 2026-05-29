#!/usr/bin/env bash
# Wrapper for render-meeting-pdf.py that runs the renderer inside a Docker
# image. The only host requirement is Docker.
#
# Image resolution order:
#   1. local hash tag    — preserves dev iteration on Dockerfile changes
#   2. local registry tag — already pulled from ghcr.io
#   3. docker pull        — first run on a fresh host
#   4. docker build       — offline, fork, or image-missing fallback
#
# Build context spans plugins/ because the script reads brand assets from
# the publishing plugin (cross-plugin asset dep). When falling back to a
# local build we need both plugins on disk; the registry image already
# bakes those assets in.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PLUGINS_ROOT="$(cd "$PLUGIN_ROOT/../.." && pwd)"
DOCKERFILE="$SCRIPT_DIR/Dockerfile"
SCRIPT="$SCRIPT_DIR/render-meeting-pdf.py"
PUBLISHING_ASSETS="$PLUGINS_ROOT/practices/publishing/assets"
PLUGIN_JSON="$PLUGIN_ROOT/.claude-plugin/plugin.json"

if ! command -v docker >/dev/null 2>&1; then
  echo "error: docker not found on PATH. Install Docker Desktop or the docker engine." >&2
  exit 69
fi

hash_inputs() {
  {
    cat "$DOCKERFILE" "$SCRIPT"
    find "$PUBLISHING_ASSETS" -type f -exec shasum -a 256 {} + | sort 2>/dev/null
  } | shasum -a 256 | cut -c1-12
}

plugin_version() {
  [ -f "$PLUGIN_JSON" ] || return 0
  grep -E '"version"[[:space:]]*:' "$PLUGIN_JSON" | head -1 \
    | sed -E 's/.*"version"[[:space:]]*:[[:space:]]*"([^"]+)".*/\1/'
}

VERSION="$(plugin_version)"
IMAGE_HASH_TAG="turtlestack/coordinator-meeting-pdf:$(hash_inputs)"
IMAGE_REGISTRY_TAG="ghcr.io/hpsgd/turtlestack-coordinator-meeting-pdf:${VERSION}"

if docker image inspect "$IMAGE_HASH_TAG" >/dev/null 2>&1; then
  IMAGE_TAG="$IMAGE_HASH_TAG"
elif [ -n "$VERSION" ] && docker image inspect "$IMAGE_REGISTRY_TAG" >/dev/null 2>&1; then
  IMAGE_TAG="$IMAGE_REGISTRY_TAG"
elif [ -n "$VERSION" ] && docker pull --quiet "$IMAGE_REGISTRY_TAG" >/dev/null 2>&1; then
  IMAGE_TAG="$IMAGE_REGISTRY_TAG"
else
  if [ ! -d "$PUBLISHING_ASSETS" ]; then
    echo "error: registry image unavailable and publishing plugin assets not found at $PUBLISHING_ASSETS." >&2
    echo "       The meeting-pdf renderer needs the publishing plugin installed alongside coordinator for the local-build fallback." >&2
    exit 70
  fi
  echo "Building $IMAGE_HASH_TAG locally (registry image unavailable)..." >&2
  docker build --quiet \
    -f "$DOCKERFILE" \
    -t "$IMAGE_HASH_TAG" \
    "$PLUGINS_ROOT" >/dev/null
  IMAGE_TAG="$IMAGE_HASH_TAG"
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
