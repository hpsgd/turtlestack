# Image for web-snapshot.py — render a URL to PDF via shot-scraper/Playwright.
#
# Base: Microsoft's official Playwright Python image. It ships Chromium at
# /ms-playwright and configures PLAYWRIGHT_BROWSERS_PATH. shot-scraper sits
# on top of Playwright and picks up that browser automatically. The base is
# large (~1.5GB) — the first build pulls it once and caches it.
#
# Run model: Chromium's sandbox prefers root inside the container, so the
# image runs as root and the entrypoint chowns the output directory back to
# the host user's UID/GID (passed as RUN_AS_UID / RUN_AS_GID env vars) before
# exiting. On macOS Docker Desktop UID translation is automatic and the chown
# is a no-op.
#
# Build context: scripts/ directory (this dir).
#
# Build:
#   docker build -f Dockerfile -t turtlestack/web-snapshot:<tag> .

# Pin: the Playwright Python package version installed in the image must
# match the Chromium build baked into the base image. When bumping the base
# image tag below, bump the `playwright==` pin to the same x.y.z. Otherwise
# Playwright errors with "Executable doesn't exist at /ms-playwright/...".
FROM mcr.microsoft.com/playwright/python:v1.60.0-noble

ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    PIP_BREAK_SYSTEM_PACKAGES=1

RUN pip install --no-cache-dir --disable-pip-version-check \
    'playwright==1.60.0' shot-scraper

COPY web-snapshot.py /opt/turtlestack/web-snapshot.py
COPY entrypoint.sh /opt/turtlestack/entrypoint.sh
RUN chmod +x /opt/turtlestack/entrypoint.sh

WORKDIR /work
ENTRYPOINT ["/opt/turtlestack/entrypoint.sh"]
