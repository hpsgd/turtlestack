#!/usr/bin/env bash
# Wrapper for web-snapshot.py that runs the snapshot script inside a Docker
# image based on Microsoft's Playwright Python image. The only host
# requirement is Docker.
#
# Image resolution order:
#   1. local hash tag    — preserves dev iteration on Dockerfile changes
#   2. local registry tag — already pulled from ghcr.io
#   3. docker pull        — first run on a fresh host (~3.9GB; minutes)
#   4. docker build       — offline, fork, or image-missing fallback
#                           (local build also pulls the Playwright base)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PLUGIN_ROOT="$(cd "$SKILL_ROOT/../.." && pwd)"
DOCKERFILE="$SCRIPT_DIR/Dockerfile"
SCRIPT="$SCRIPT_DIR/web-snapshot.py"
ENTRYPOINT="$SCRIPT_DIR/entrypoint.sh"
PLUGIN_JSON="$PLUGIN_ROOT/.claude-plugin/plugin.json"

if ! command -v docker >/dev/null 2>&1; then
  echo "error: docker not found on PATH. Install Docker Desktop or the docker engine." >&2
  exit 69
fi

hash_inputs() {
  cat "$DOCKERFILE" "$SCRIPT" "$ENTRYPOINT" | shasum -a 256 | cut -c1-12
}

plugin_version() {
  [ -f "$PLUGIN_JSON" ] || return 0
  grep -E '"version"[[:space:]]*:' "$PLUGIN_JSON" | head -1 \
    | sed -E 's/.*"version"[[:space:]]*:[[:space:]]*"([^"]+)".*/\1/'
}

VERSION="$(plugin_version)"
IMAGE_HASH_TAG="turtlestack/web-snapshot:$(hash_inputs)"
IMAGE_REGISTRY_TAG="ghcr.io/hpsgd/turtlestack-web-snapshot:${VERSION}"

if docker image inspect "$IMAGE_HASH_TAG" >/dev/null 2>&1; then
  IMAGE_TAG="$IMAGE_HASH_TAG"
elif [ -n "$VERSION" ] && docker image inspect "$IMAGE_REGISTRY_TAG" >/dev/null 2>&1; then
  IMAGE_TAG="$IMAGE_REGISTRY_TAG"
elif [ -n "$VERSION" ] && docker pull --quiet "$IMAGE_REGISTRY_TAG" >/dev/null 2>&1; then
  IMAGE_TAG="$IMAGE_REGISTRY_TAG"
else
  echo "Building $IMAGE_HASH_TAG locally (registry image unavailable; pulls Playwright base, ~1.5GB)..." >&2
  docker build --quiet \
    -f "$DOCKERFILE" \
    -t "$IMAGE_HASH_TAG" \
    "$SCRIPT_DIR" >/dev/null
  IMAGE_TAG="$IMAGE_HASH_TAG"
fi

# Chromium's sandbox wants root inside the container, so we don't pass --user.
# Instead the entrypoint chowns the output dir back to the host UID/GID on
# exit (Linux only; macOS Docker Desktop maps ownership already).
docker_args=(
  --rm
  -v "$HOME:$HOME"
  -v "/tmp:/tmp"
  -w "$PWD"
  -e HOME="$HOME"
  -e RUN_AS_UID="$(id -u)"
  -e RUN_AS_GID="$(id -g)"
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
