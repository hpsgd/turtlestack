# Migration: namespace marketplace state under `.claude/<marketplace>/`

Status: implemented in turtlestack v1.17.0+
Drafted: 2026-05-08
Implemented: 2026-05-08

The marketplace-side code now writes to namespaced paths. Consuming projects need to run the migration snippet below once after updating to v1.17.0 or later. Project-scoped state stays in the project; global learnings move to `~/.claude/turtlestack/learnings/`.

## Why

Right now turtlestack writes state into half a dozen different paths under a consuming project's `.claude/`:

| Path | Owner |
|---|---|
| `.claude/learnings/` | turtlestack (thinking plugin) |
| `.claude/handoff/` | turtlestack (thinking plugin) |
| `.claude/plugin-updates-<marketplace>.md` | turtlestack (thinking plugin) |
| `.claude/scheduled_tasks.lock` | schedule plugin (confirm before moving — may be a separate marketplace's) |
| `.claude/rules/` | Claude Code reads, turtlestack writes |
| `.claude/settings.json` | Claude Code, user-edited |
| `.claude/settings.local.json` | Claude Code |

Three problems with this:

1. Every new marketplace artefact requires retrospectively patching the consuming project's `.gitignore`. Easy to forget.
2. No clean ownership boundary. If a user wants to add their own `.claude/.gitignore` they may collide with marketplace-managed entries.
3. Cleanup is impossible to express. "Wipe turtlestack's state" requires knowing every path it writes.

## What changes

Move marketplace-owned state under a per-marketplace namespace:

| Old path | New path |
|---|---|
| `.claude/learnings/` | `.claude/<marketplace>/learnings/` |
| `.claude/handoff/` | `.claude/<marketplace>/handoff/` |
| `.claude/plugin-updates-<marketplace>.md` | `.claude/<marketplace>/plugin-updates.md` |
| `.claude/scheduled_tasks.lock` (if turtlestack-owned) | `.claude/<marketplace>/scheduled_tasks.lock` |

`<marketplace>` is the actual marketplace name (e.g. `turtlestack`). The path is derived in scripts the same way `install-rules.sh` does it — from `CLAUDE_PLUGIN_ROOT`.

Three things stay put:

| Path | Why it stays |
|---|---|
| `.claude/rules/` | Claude Code reads from this exact path. Each rule file is already prefixed `<marketplace>--<plugin>--<version>--<filename>.md`, so ownership is visible. |
| `.claude/settings.json` | Claude Code's. User-owned, committed. |
| `.claude/settings.local.json` | Claude Code's. Per-machine. |

After the move, the consuming project's `.gitignore` can collapse to:

```gitignore
# Marketplace-managed transient state
.claude/turtlestack/
# (add other marketplaces here as they're enabled)
```

Plus the existing Claude Code lines:

```gitignore
.claude/settings.local.json
.claude/rules/
```

## Marketplace-side changes (done in v1.17.0)

Marketplace name is derived dynamically in shell scripts that run as hooks (from `CLAUDE_PLUGIN_ROOT` — same approach `install-rules.sh` already uses). For Python scripts, `classify-message.py` reads `CLAUDE_PLUGIN_ROOT` from env via a `_marketplace_name()` helper; CLI-invoked scripts (`detect-patterns.py`, `generate-metrics.py`) hardcode `turtlestack` in their argparse defaults since this code lives in turtlestack's repo. Test override env vars (`LEARNINGS_DIR`, `GLOBAL_LEARNINGS_DIR`, `HANDOFF_DIR`) are unchanged — they bypass the namespace logic entirely.

Files updated:

- `plugins/practices/thinking/scripts/learning-hook.sh` — writes signals/sessions
- `plugins/practices/thinking/scripts/learning-readback.sh` — reads from `$PROJECT_DIR/.claude/learnings`
- `plugins/practices/thinking/scripts/classify-message.py` — writes to signals
- `plugins/practices/thinking/scripts/analyse-session.py` — writes session analysis
- `plugins/practices/thinking/scripts/detect-patterns.py` — writes patterns
- `plugins/practices/thinking/scripts/generate-metrics.py` — writes metrics
- `plugins/practices/thinking/scripts/check-plugin-versions.sh` — writes drift file
- `plugins/practices/thinking/skills/handoff/SKILL.md` — writes handoff docs
- `plugins/practices/thinking/skills/retrospective/SKILL.md` — reads sessions/signals
- `plugins/practices/thinking/skills/reconcile-rules/SKILL.md` — reads rules (this one may not need changing if it only reads `.claude/rules/`)
- `plugins/practices/thinking/skills/propose-improvement/SKILL.md` — reads patterns
- `plugins/practices/coding-standards/rules/ai-steering.md` — references `.claude/learnings` in prose; update example paths

No shared `lib.sh` helper was added — derivation is short enough (3 lines) that inlining was clearer than a sourced helper. Three of the five scripts that need it already had inline derivation.

Tests using `LEARNINGS_DIR`/`GLOBAL_LEARNINGS_DIR`/`HANDOFF_DIR` env overrides keep working unchanged — those overrides bypass marketplace namespacing entirely.

## Consumer-side migration (per-project)

Run once per project after the marketplace change ships and the user has run `claude plugin update thinking@turtlestack` and restarted.

> [!IMPORTANT]
> The SessionStart hooks under v1.17.0 populate the new namespaced paths the first time you start a session, so by the time you run this migration `.claude/turtlestack/learnings/` already exists with placeholder data from one session. The snippets below handle that collision: they treat the **old path** as authoritative (it has full history) and replace the placeholder new-path data with it. If you've been running v1.17.0 for many sessions before migrating and want to keep the new-path data, do a manual `rsync -a` instead of the `rm -rf`.

```bash
# Per-project state — run from project root
cd <project-root>
mkdir -p .claude/turtlestack

# Learnings: old path has full history; new path has fresh placeholder.
# Replace the placeholder with the historical data.
if [ -d .claude/learnings ]; then
    rm -rf .claude/turtlestack/learnings
    mv .claude/learnings .claude/turtlestack/learnings
fi

# Handoff: new path holds the live handoff queue; old path may hold
# resumed/. Move resumed across, then drop the empty old dir.
if [ -d .claude/handoff/resumed ]; then
    mkdir -p .claude/turtlestack/handoff
    mv .claude/handoff/resumed .claude/turtlestack/handoff/resumed
fi
[ -d .claude/handoff ] && rmdir .claude/handoff 2>/dev/null

# Regenerable — safe to delete; the hook will recreate where needed
[ -f .claude/scheduled_tasks.lock ] && mv .claude/scheduled_tasks.lock .claude/turtlestack/ 2>/dev/null
rm -f .claude/plugin-updates-*.md
```

```bash
# Global state — run once per machine. Same pattern: old wins.
mkdir -p ~/.claude/turtlestack
if [ -d ~/.claude/learnings ]; then
    rm -rf ~/.claude/turtlestack/learnings
    mv ~/.claude/learnings ~/.claude/turtlestack/learnings
fi
```

Then update the project's `.gitignore`:

```diff
- .claude/learnings/sessions/
- .claude/learnings/signals/
- .claude/learnings/patterns/
- .claude/learnings/metrics/
- .claude/learnings/manifest.json
- .claude/handoff/
- .claude/scheduled_tasks.lock
- .claude/plugin-updates-*.md
+ .claude/turtlestack/
```

Keep:

```gitignore
.claude/settings.local.json
.claude/rules/
```

Restart Claude Code. The thinking plugin's SessionStart hook will write into the new paths. Verify the drift file appears at `.claude/turtlestack/plugin-updates.md` (if drift exists) or not at all (if everything's in sync).

## Verification

After migration, in the project:

- `ls .claude/turtlestack/` shows learnings/, handoff/, and any drift/lock files
- `ls .claude/` no longer shows learnings/ or handoff/ at the top level
- `git status` shows no untracked turtlestack-managed files (the `.claude/turtlestack/` line catches them)
- Start a fresh Claude Code session — the SessionStart hooks should run without error
- `cat .claude/turtlestack/plugin-updates.md` (if drift exists) shows the right commands

## Edge cases

- **Schedule lock ownership**: confirm whether `.claude/scheduled_tasks.lock` is written by a turtlestack plugin or by Claude Code / another marketplace. If it's not turtlestack's, leave it alone.
- **Multi-marketplace projects**: a project enabling tortoisestack as well gets a parallel `.claude/tortoisestack/` dir. Add a second `.gitignore` line. Each marketplace's hook should namespace by its own derived `MARKETPLACE` value, never hardcode "turtlestack".
- **In-flight sessions during migration**: if a session is running when the user updates the plugin, the old session may still write to old paths. Tell the user to close Claude Code before running the migration shell snippet.
- **Old learnings still useful**: don't delete `.claude/learnings/` — move it. Session signals are evidence behind learned rules.
- **Existing `.gitignore` already commits old paths**: if `.claude/learnings/` was accidentally committed in a prior version of the project, `git rm -r --cached .claude/learnings` before the move so git stops tracking them. Do this carefully — the user will see a large diff.

## Sequencing

1. ✅ Marketplace-side path change shipped in v1.17.0
2. ✅ This doc's status updated
3. Consumers: per-project migration when they next update the plugin. Each session that picks up the new plugin version can use this doc as the recipe.

## When this is done

Future marketplace artefacts default to `.claude/<marketplace>/<thing>` from the start. The pattern is self-perpetuating. The root `.claude/` only ever holds Claude Code's own files.
