# Image for render-document-pdf.py — markdown → A4 PDF via xhtml2pdf.
#
# Build context: plugin root (plugins/practices/publishing/) so the image can
# copy in the assets/ directory the script expects at PLUGIN_ROOT/assets.
#
# Build:
#   docker build -f scripts/Dockerfile -t turtlestack/publishing-document-pdf:<tag> \
#     plugins/practices/publishing
#
# Run via the wrapper render-document-pdf.sh — it computes the tag from a hash
# of the Dockerfile + constraints + script and only builds on cache miss.

FROM python:3.12-slim

WORKDIR /opt/turtlestack

COPY scripts/constraints.txt /opt/turtlestack/constraints.txt
RUN pip install --no-cache-dir --disable-pip-version-check \
    --constraint /opt/turtlestack/constraints.txt \
    xhtml2pdf markdown

COPY scripts/render-document-pdf.py /opt/turtlestack/scripts/render-document-pdf.py
COPY assets /opt/turtlestack/assets

# render-document-pdf.py resolves PLUGIN_ROOT as parents[1] of the script,
# i.e. /opt/turtlestack — so /opt/turtlestack/assets is where it looks for
# styles and fonts. Keep the layout matching that expectation.

WORKDIR /work
ENTRYPOINT ["python3", "/opt/turtlestack/scripts/render-document-pdf.py"]
