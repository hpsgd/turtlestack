#!/usr/bin/env bash
# Wrapper for web-snapshot.py that runs the snapshot script inside a Docker
# image based on Microsoft's Playwright Python image. The only host
# requirement is Docker.
#
# First run pulls the Playwright base (~1.5GB, several minutes on a slow
# connection) and builds the wrapper image. Subsequent runs reuse the cached
# image (~2s overhead per invocation).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DOCKERFILE="$SCRIPT_DIR/Dockerfile"
SCRIPT="$SCRIPT_DIR/web-snapshot.py"
ENTRYPOINT="$SCRIPT_DIR/entrypoint.sh"

if ! command -v docker >/dev/null 2>&1; then
  echo "error: docker not found on PATH. Install Docker Desktop or the docker engine." >&2
  exit 69
fi

hash_inputs() {
  cat "$DOCKERFILE" "$SCRIPT" "$ENTRYPOINT" | shasum -a 256 | cut -c1-12
}

IMAGE_TAG="turtlestack/web-snapshot:$(hash_inputs)"

if ! docker image inspect "$IMAGE_TAG" >/dev/null 2>&1; then
  echo "Building $IMAGE_TAG (first run pulls Playwright base, ~1.5GB)..." >&2
  docker build --quiet \
    -f "$DOCKERFILE" \
    -t "$IMAGE_TAG" \
    "$SCRIPT_DIR" >/dev/null
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
