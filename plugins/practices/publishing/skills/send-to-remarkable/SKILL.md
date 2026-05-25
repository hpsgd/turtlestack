---
name: send-to-remarkable
description: "Upload a PDF to a reMarkable device (Paper Pro, rM2) wirelessly via the reMarkable cloud. Wraps the ddvk/rmapi CLI inside a Docker image — Docker is the only host requirement. Requires a one-time interactive pairing (--pair) before normal uploads work. Falls back to a manual-upload instruction if upload fails."
argument-hint: "<path to pdf> [<remote folder, default />]"
user-invocable: true
allowed-tools: Bash
---

# Send to reMarkable

Push a PDF to a reMarkable device via the cloud. The device picks it up next time it syncs over Wi-Fi. Works with Paper Pro and rM2 — the upload is via the cloud API, so it's device-agnostic.

This is a separate skill on purpose. Render with `/practices:write-document-pdf` (or any other PDF generator), then send with this. If you want them chained for a particular project, add a memory or learning to that repo saying "after generating a report, ask whether to send it to reMarkable."

## When to use

When the user has a PDF on disk and wants it on their reMarkable device without plugging in a USB cable. The device must be online (Wi-Fi connected to the reMarkable cloud) for the upload to land — rmapi pushes to the cloud immediately, but the device only sees it on its next sync.

Don't use this for the first-time setup of rmapi itself — pairing needs an interactive run. Tell the user to run `"${CLAUDE_PLUGIN_ROOT}/scripts/send-to-remarkable.sh" --pair` from their own terminal, where they can paste the one-time device code.

## Step 1: Resolve the PDF path to absolute

The first non-flag argument is the source PDF. Required, must exist.

```bash
ARG="<path>"
case "$ARG" in
  /*) ABS="$ARG" ;;
  *) ABS="$(pwd)/$ARG" ;;
esac
```

If the path doesn't exist or isn't a PDF (`.pdf` extension, magic bytes start with `%PDF`), stop and report.

## Step 2: Resolve the destination folder

Optional second argument. Default is `/` (root of My Files on the device). If the user names a sub-folder (e.g., `/Meetings`), the folder must already exist on the device — rmapi won't create it. If the destination is uncertain, default to `/` and let the user move it on-device.

## Step 3: Invoke the wrapper

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/send-to-remarkable.sh" <abs pdf path> [<remote folder>]
```

The wrapper builds (on first run) and runs an `rmapi` Docker image, bind-mounting `~/.config/rmapi/` from the host so the auth state persists across invocations. Capture stdout and stderr — both are useful, since rmapi prints upload progress on stdout and errors on stderr.

## Step 4: Handle failure modes

The fallback in every failure case is the same: tell the user the file is at `<absolute path>` and they can upload it manually via the reMarkable mobile app or desktop app. Don't retry automatically — failures here are usually structural (auth expired, network, protocol migration) and a retry won't help.

Specific exit codes from the wrapper:

- **64** — usage error (wrong number of arguments, or `--pair` invoked non-interactively). Programming bug, fix the call. For `--pair`, tell the user to run it from their own terminal.
- **66** — PDF file missing. Stop, report path.
- **69** — Docker not installed. Tell the user to install Docker Desktop (macOS/Windows) or the docker engine (Linux). The wrapper has no offline fallback.
- **75** — rmapi has not been paired yet. Tell the user to run `"${CLAUDE_PLUGIN_ROOT}/scripts/send-to-remarkable.sh" --pair` from their own terminal and paste the one-time code from https://my.remarkable.com/device/browser.
- **non-zero from rmapi itself** — most likely auth (re-pair via `--pair`), sync protocol breakage (the sync15 migration occasionally breaks `put`; check https://github.com/ddvk/rmapi/issues for current state), or network. Surface the rmapi error verbatim, then offer the manual fallback.

## Step 5: Confirm

On success, report which device folder the PDF was uploaded to and remind the user it'll appear on the device when it next syncs.

## Evidence requirements (non-negotiable)

Every claim about upload status must be grounded in actual command output. The skill MUST:

1. Show the literal command run, including the wrapper path and arguments.
2. Show the captured stdout and stderr from the wrapper (or, if `rmapi` was checked directly first, show that output too).
3. Quote the exit code.

Never assert "the upload succeeded" or "rmapi was found" without showing the underlying tool output. If the test or runtime environment makes the tool unavailable, the wrapper's exit-69 path produces the install instructions — surface those verbatim rather than imagining a happier outcome.

## Rules

- **Never modify the source PDF.** Read-only.
- **Don't bump rmapi inside the Dockerfile silently.** The `RMAPI_REF` build-arg pins the upstream version. When the sync protocol breaks, the maintainer publishes a new tag — bump the pin in `scripts/Dockerfile.remarkable` and let the image hash change to trigger a rebuild.
- **Don't try to set up rmapi auth in the script.** Pairing requires a one-time code from a browser — needs to be interactive with the user. Tell them to run `--pair` from their own terminal and stop.
- **Don't claim the file is on the device.** Claim it's been uploaded to the cloud. The device picks it up on next sync, which depends on the device being online and on Wi-Fi.

## Output format

On success:

```
Uploaded <pdf basename> to reMarkable cloud at <dest folder>.
Will appear on device next time it syncs over Wi-Fi.
```

On failure: the rmapi error verbatim, then:

```
Manual fallback: open the reMarkable mobile/desktop app and upload <abs pdf path>.
```

## Related skills

- `/practices:write-document-pdf` — generate the PDF in the first place.
- `/coordinator:write-meeting-pdf` — purpose-built meeting notes PDF for the Paper Pro form factor.

## Background

`rmapi` is the community-maintained CLI that talks to the reMarkable cloud. The original juruen/rmapi was archived in July 2024; the active fork is ddvk/rmapi (https://github.com/ddvk/rmapi). reMarkable is mid-migration to a new sync protocol ("sync15") which has occasionally broken uploads — the maintainer turns these around quickly but expect the odd outage where the manual fallback is needed. The Dockerfile builds rmapi from source at a pinned tag so the plugin doesn't depend on the user having a release binary on PATH.

The reasons we use this path rather than alternatives:

- **USB Web Interface (`http://10.11.99.1`)** — works on Paper Pro and is officially supported, but needs the device plugged in. No good for "render and send while the device is in another room."
- **OneDrive / Google Drive / Dropbox integrations** — not automated. The device-side integration browses cloud folders for manual import; there's no folder-watch.
- **SSH/scp** — needs Developer Mode, which on Paper Pro requires a factory reset to enable. Too costly.
- **Email-to-device** — no official path; third-party relays are fragile.
