#!/usr/bin/env bash
# Wrapper for fetch-rendered.py — fetches a URL with Playwright/Chromium
# inside a Docker image and prints rendered HTML to stdout. The only host
# requirement is Docker.
#
# First run pulls the Playwright base (~1.5GB). Shares layers with the
# web-snapshot image if that's already been built.
#
# Usage:
#   fetch-rendered.sh <url> [--wait-for <selector>] [--timeout <ms>] [--wait-after <ms>]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DOCKERFILE="$SCRIPT_DIR/Dockerfile"
SCRIPT="$SCRIPT_DIR/fetch-rendered.py"

if ! command -v docker >/dev/null 2>&1; then
  echo "error: docker not found on PATH. Install Docker Desktop or the docker engine." >&2
  exit 69
fi

hash_inputs() {
  cat "$DOCKERFILE" "$SCRIPT" | shasum -a 256 | cut -c1-12
}

IMAGE_TAG="turtlestack/content-retrieval-playwright:$(hash_inputs)"

if ! docker image inspect "$IMAGE_TAG" >/dev/null 2>&1; then
  echo "Building $IMAGE_TAG (first run pulls Playwright base, ~1.5GB)..." >&2
  docker build --quiet \
    -f "$DOCKERFILE" \
    -t "$IMAGE_TAG" \
    "$SCRIPT_DIR" >/dev/null
fi

exec docker run --rm "$IMAGE_TAG" "$@"
