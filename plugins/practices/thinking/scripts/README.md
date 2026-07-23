# thinking scripts

Most scripts here are internal to the thinking plugin's hooks (session analysis, metrics,
learning readback). One is a **supported cross-marketplace entry point**: `install-rules.sh`.

## `install-rules.sh` — rule installer (public entry point)

Installs a marketplace's plugin rule files into a consuming project's `.claude/rules/`. It runs
as thinking's own SessionStart hook, but it is **not** turtlestack-specific: it derives the
marketplace from `CLAUDE_PLUGIN_ROOT` and installs rules for that marketplace's enabled plugins.
A downstream marketplace can reuse this exact script by exec'ing it with `CLAUDE_PLUGIN_ROOT`
pointing at one of its own plugins — no fork required.

This is a **supported contract**. The path and the behaviour below won't change without a major
version bump of the thinking plugin and a migration note. Downstream marketplaces may depend on it.

### How a downstream marketplace uses it

The canonical installed copy lives at:

```
<config>/plugins/cache/turtlestack/thinking/<version>/scripts/install-rules.sh
```

(`<config>` is `$CLAUDE_CONFIG_DIR`, default `~/.claude`.) A downstream SessionStart hook locates
that script and execs it with `CLAUDE_PLUGIN_ROOT` still pointing at the *downstream* plugin, so the
canonical installs the downstream marketplace's rules. Glob the `<version>` segment — don't pin it.

### Inputs (environment)

| Var | Required | Meaning |
|---|---|---|
| `CLAUDE_PLUGIN_ROOT` | yes | The calling plugin's cache or source root. The marketplace name is derived from this — both the cache form (`.../plugins/cache/<marketplace>/<plugin>/<version>`) and the source form (`.../plugins/marketplaces/<marketplace>/...`) are recognised. |
| `CLAUDE_PROJECT_DIR` | yes | The consuming project. Empty → no-op `exit 0` (global session, nothing to install). |
| `CLAUDE_CONFIG_DIR` | no | Where the plugin cache and global `settings.json` live. Defaults to `~/.claude`. |
| `RULES_DIR` | no | Where rules are written. Defaults to `$CLAUDE_PROJECT_DIR/.claude/rules`. Test harnesses override this to dodge the `.claude/` write gate. |

### Behaviour

- Reads `enabledPlugins` from both project (`$CLAUDE_PROJECT_DIR/.claude/settings.json`) and global
  (`$CLAUDE_CONFIG_DIR/settings.json`) settings, keeping the keys suffixed `@<marketplace>`.
- For each enabled plugin of that marketplace, finds the highest-version cache dir and copies every
  `rules/*.md` into `RULES_DIR` as `<marketplace>--<plugin>--<version>--<file>.md`.
- Writes atomically (temp file then move) and skips files whose content is unchanged.
- Prunes older cached version dirs (never the one currently executing).
- Removes stale `<marketplace>--*.md` rules that are no longer shipped by an enabled plugin.
- Sweeps orphan `<marketplace>--*.md` files left at the user level by an older scheme.
- Prints a `<learning-context>` summary to stdout **only when something changed**; silent otherwise.

### Stability promise

The script path, the four input env vars, and the `<marketplace>--<plugin>--<version>--<file>.md`
naming convention are stable. Breaking any of them requires a major version bump and a migration note.
The cross-marketplace contract is regression-guarded by
`examples/practices/thinking/hooks/install-rules/installs-downstream-marketplace-rule/`.

## Other scripts

`analyse-session.py`, `classify-message.py`, `detect-patterns.py`, `generate-metrics.py`,
`learning-hook.sh`, `learning-readback.sh`, `show-notices.sh` are
internal to thinking's hooks and carry no cross-marketplace stability promise.
