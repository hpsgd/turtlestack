# Capability brief — Helio AI meeting-notes product

Use this brief as your evidence base. Do NOT live-research; build the Wardley Map from the facts
below: anchor on the user need, place each component on visibility and evolution, and read the
strategic signals.

## User and need

User: a busy team manager. Need: walk out of every meeting with accurate, shareable notes and
action items without taking notes themselves.

## Value chain components (what's required to deliver the need)

- **Meeting capture UX** (the manager's surface — join a call, see live notes). High visibility.
- **Action-item extraction** (Helio's proprietary model that pulls owners + due dates from
  transcript). This is Helio's claimed differentiation today.
- **Summarisation** (condense transcript into notes). Helio built a custom summariser 2 years ago.
- **Speech-to-text transcription** (turn audio into text).
- **Large language model inference** (the general LLM that powers summarisation/extraction).
- **Audio ingestion / streaming** (pull audio from Zoom/Meet/Teams).
- **Compute / hosting** (servers the whole thing runs on).

## Market evidence on maturity (use this to place evolution)

- **Compute / hosting:** fully commoditised — AWS/Azure/GCP utility pricing. Nobody differentiates.
- **Speech-to-text:** now a commodity cloud service — multiple providers (cloud STT APIs,
  open-source Whisper) at near-utility pricing. Two years ago this was a custom build; today it's
  off-the-shelf.
- **LLM inference:** rapidly evolving from product toward commodity — many interchangeable API
  providers, prices falling monthly. Custom-built summarisation on top is increasingly redundant as
  general LLMs summarise well out of the box.
- **Summarisation:** Helio's custom summariser is now matched by generic LLM summarisation — the
  thing they custom-built is drifting to commodity beneath them.
- **Action-item extraction:** still genuinely ahead of off-the-shelf — bespoke, accurate, the real
  differentiator. Genesis/custom territory.
- **Meeting capture UX:** product-stage; competitors have comparable polished UX.
- **Audio ingestion:** product/commodity — standard SDKs from each meeting platform.

## Competitor note

A large competitor still pours engineering into its own custom speech-to-text stack — even though
commodity cloud STT is now as good and far cheaper.
