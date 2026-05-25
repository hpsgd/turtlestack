# Image for fetch-rendered.py — Playwright-based HTML fetcher used at Tier 3
# of the content-retrieval skill (JS-rendered pages).
#
# Pin: the Playwright Python package version must match the Chromium build in
# the base image. When bumping the base tag below, bump the playwright== pin
# to the same x.y.z. Otherwise Playwright errors with "Executable doesn't
# exist at /ms-playwright/...".
#
# Build context: this scripts/ directory.

FROM mcr.microsoft.com/playwright/python:v1.60.0-noble

ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    PIP_BREAK_SYSTEM_PACKAGES=1

RUN pip install --no-cache-dir --disable-pip-version-check 'playwright==1.60.0'

COPY fetch-rendered.py /opt/turtlestack/fetch-rendered.py

WORKDIR /work
ENTRYPOINT ["python3", "/opt/turtlestack/fetch-rendered.py"]
