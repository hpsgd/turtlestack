#!/usr/bin/env bash
# Wrapper for fetch-rendered.py — fetches a URL with Playwright/Chromium
# inside a Docker image and prints rendered HTML to stdout. The only host
# requirement is Docker.
#
# Image resolution order:
#   1. local hash tag    — preserves dev iteration on Dockerfile changes
#   2. local registry tag — already pulled from ghcr.io
#   3. docker pull        — first run on a fresh host (~3.9GB; minutes)
#   4. docker build       — offline, fork, or image-missing fallback
#                           (local build also pulls the Playwright base)
#
# Shares the Playwright base layer with the web-snapshot image — if either
# is cached locally, the other is much faster to obtain.
#
# Usage:
#   fetch-rendered.sh <url> [--wait-for <selector>] [--timeout <ms>] [--wait-after <ms>]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PLUGIN_ROOT="$(cd "$SKILL_ROOT/../.." && pwd)"
DOCKERFILE="$SCRIPT_DIR/Dockerfile"
SCRIPT="$SCRIPT_DIR/fetch-rendered.py"
PLUGIN_JSON="$PLUGIN_ROOT/.claude-plugin/plugin.json"

if ! command -v docker >/dev/null 2>&1; then
  echo "error: docker not found on PATH. Install Docker Desktop or the docker engine." >&2
  exit 69
fi

hash_inputs() {
  cat "$DOCKERFILE" "$SCRIPT" | shasum -a 256 | cut -c1-12
}

plugin_version() {
  [ -f "$PLUGIN_JSON" ] || return 0
  grep -E '"version"[[:space:]]*:' "$PLUGIN_JSON" | head -1 \
    | sed -E 's/.*"version"[[:space:]]*:[[:space:]]*"([^"]+)".*/\1/'
}

VERSION="$(plugin_version)"
IMAGE_HASH_TAG="turtlestack/content-retrieval-playwright:$(hash_inputs)"
IMAGE_REGISTRY_TAG="ghcr.io/hpsgd/turtlestack-content-retrieval-playwright:${VERSION}"

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

exec docker run --rm "$IMAGE_TAG" "$@"
