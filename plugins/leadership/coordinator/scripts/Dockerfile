# Image for render-meeting-pdf.py — meeting Q&A → Remarkable Paper Pro PDF.
#
# The script reaches across plugins to read brand fonts/logos from the
# publishing plugin's assets/ directory (resolved via parents[3] of the
# script path). To make that path resolution work inside the container we
# mirror the plugin tree under /opt/turtlestack/plugins.
#
# Build context: the marketplace's plugins/ directory.
#
# Build:
#   docker build -f leadership/coordinator/scripts/Dockerfile \
#     -t turtlestack/coordinator-meeting-pdf:<tag> \
#     plugins
#
# Run via the wrapper render-meeting-pdf.sh — it computes the tag from a hash
# of the Dockerfile + script + publishing assets and only builds on cache miss.

FROM python:3.12-slim

RUN pip install --no-cache-dir --disable-pip-version-check reportlab

# Mirror enough of the plugin layout so the script's parents[3] resolution
# lands on /opt/turtlestack/plugins and picks up publishing/assets.
COPY leadership/coordinator/scripts/render-meeting-pdf.py \
     /opt/turtlestack/plugins/leadership/coordinator/scripts/render-meeting-pdf.py
COPY practices/publishing/assets \
     /opt/turtlestack/plugins/practices/publishing/assets

WORKDIR /work
ENTRYPOINT ["python3", "/opt/turtlestack/plugins/leadership/coordinator/scripts/render-meeting-pdf.py"]
