# plugin-curator scripts

Tooling for evaluating Claude Code skills and agents end-to-end against rubric-style tests.

## What's here

| File | Purpose |
|---|---|
| `run-test.py` | Run a single test: invoke the skill/agent in headless mode, snapshot artifacts, judge against criteria, write `result.md` |
| `judge-prompt.md` | System prompt the judge model uses when scoring captured output |
| `check-result-verdict.py` | PostToolUse hook that validates `result.md` verdicts match their scores |

## How testing works

`run-test.py` does five things in order:

1. **Parse** `test.md` into scenario, prompt, and criteria
2. **Spawn** an isolated tmp workspace (git-initialised, with path env overrides set)
3. **Invoke** `claude -p --plugin-dir <plugin> --output-format json <prompt>` against the workspace
4. **Snapshot** every file the target wrote into the override dirs
5. **Judge** by invoking a second `claude -p` with `judge-prompt.md` as system prompt and the criteria + chat response + artifacts as input

The judge returns strict JSON. The runner converts that to a `result.md` with verdict, score, per-criterion evidence, and the captured output.

## Prerequisites

- `claude` CLI in PATH (`claude --version`)
- Python 3.10+
- `git` for workspace seeding
- A working Claude Code auth (keychain, `ANTHROPIC_API_KEY`, or `apiKeyHelper`)

## Quick start

Run one skill test:

```bash
plugins/practices/plugin-curator/scripts/run-test.py \
  --test-dir examples/practices/thinking/skills/handoff \
  --plugin-dir plugins/practices/thinking
```

The result lands at `examples/practices/thinking/skills/handoff/result.md` and a JSON summary prints to stdout.

Override the target or judge model for an ad-hoc run:

```bash
plugins/practices/plugin-curator/scripts/run-test.py \
  --test-dir examples/.../skills/foo \
  --plugin-dir plugins/.../foo-plugin \
  --target-model claude-sonnet-4-6
```

Without `--target-model`, the runner uses the test's own preference (`target-model:` in `test.md` frontmatter — see [Test.md format](#testmd-format)) and falls back to a hardcoded default. Same for `--judge-model`. The chosen model is logged to stderr at start, recorded in `result.md`'s metadata table, and included in the JSON summary.

Keep the workspace for debugging:

```bash
plugins/practices/plugin-curator/scripts/run-test.py \
  --test-dir ... --plugin-dir ... --keep-workspace
```

Test a plugin that declares dependencies on other plugins (e.g. `manda` depends on `analyst@turtlestack`):

Two ways to satisfy the dep, depending on whether the dep declaration is qualified by marketplace.

**Unqualified deps** — pass the dependency directory as another `--plugin-dir`:

```bash
plugins/practices/plugin-curator/scripts/run-test.py \
  --test-dir examples/research/manda/skills/company-assessment/partnership-eval \
  --plugin-dir plugins/research/manda \
  --plugin-dir ../turtlestack/plugins/research/analyst
```

**Marketplace-qualified deps** (`"dependencies": ["analyst@turtlestack"]`) — `--plugin-dir` loads plugins as `@inline`, which doesn't satisfy `@turtlestack`-qualified deps. Use `--isolate-plugins` to set up a per-run isolated plugin cache, then point `--marketplace-source` at the upstream source for each marketplace referenced. The runner reads `dependencies` from each `--plugin-dir`'s `plugin.json`, registers each marketplace in the isolated cache, and installs the deps before invoking the test:

```bash
.../run-test.py \
  --test-dir examples/research/manda/skills/company-assessment/partnership-eval \
  --plugin-dir plugins/research/manda \
  --isolate-plugins \
  --marketplace-source turtlestack=hpsgd/turtlestack
```

The isolated cache lives under the workspace and is torn down with it. Nothing under `~/.claude/plugins/` is touched. Auth still works through keychain — no `ANTHROPIC_API_KEY` needed because `CLAUDE_CONFIG_DIR` is left alone.

## Arguments

| Flag | Default | Purpose |
|---|---|---|
| `--test-dir` | required | Test directory containing `test.md` |
| `--plugin-dir` | required | Plugin under test (the dir holding `.claude-plugin/plugin.json`). Repeatable — pass once for the plugin under test, again for any dependencies it declares. |
| `--target-model` | from test frontmatter, else `claude-haiku-4-5-20251001` | Model that runs the skill/agent. CLI flag wins over `target-model:` in test.md frontmatter, which wins over the hardcoded default. |
| `--judge-model` | from test frontmatter, else `claude-sonnet-4-6` | Model that scores the output. Same resolution order as `--target-model`. |
| `--judge-prompt` | `judge-prompt.md` (sibling) | Override the judge system prompt |
| `--workspace-root` | `$TMPDIR` | Where per-run workspaces are created |
| `--keep-workspace` | off | Don't delete the workspace after the run |
| `--env KEY=VALUE` | none | Extra env var for the target run (repeatable) |
| `--timeout` | 300 | Seconds per invocation (target and judge) |
| `--isolate-config` | off | Set `CLAUDE_CONFIG_DIR` to the workspace. Requires `ANTHROPIC_API_KEY` (keychain auth doesn't resolve through the redirect) |
| `--isolate-plugins` | off | Set `CLAUDE_CODE_PLUGIN_CACHE_DIR` to a workspace subdir, isolating marketplaces and plugin installs from `~/.claude/plugins`. Auth keeps working via keychain. The runner pre-populates the isolated cache from each `--plugin-dir`'s declared deps. |
| `--marketplace-source NAME=SOURCE` | none | Map a marketplace name to its source for `claude plugin marketplace add` (e.g. `turtlestack=hpsgd/turtlestack`). Repeatable. Required under `--isolate-plugins` for each marketplace referenced in deps. |
| `--project-dir` | tmp workspace | Run the target with this directory as cwd, so project-scoped plugins from that project apply (default: a fresh workspace dir) |
| `--no-write-result` | off | Skip writing `result.md`; still emits JSON to stdout |

## Test.md format

```markdown
---
target-model: claude-sonnet-4-6
---

# Test: <short title>

<Scenario paragraph — what's being tested and why>

## Prompt

<verbatim prompt that will be sent to the skill or agent>

## Criteria

- [ ] PASS: <criterion the skill definition must address>
- [ ] PARTIAL: <criterion capped at 0.5 points>
- [ ] SKIP: <criterion excluded from scoring>

## Output expectations

- [ ] PASS: <criterion about what the captured output must contain>
```

Both `## Criteria` and `## Output expectations` are optional but at least one must be present. The `PASS:` / `PARTIAL:` / `SKIP:` prefix sets the **scoring ceiling**, not the expected outcome — see `judge-prompt.md`.

### Frontmatter (optional)

A leading YAML block fenced by `---` lines lets a test declare per-test config. Currently supported keys:

| Key | Effect |
|---|---|
| `target-model` | Model to invoke for the skill/agent under test. Overridden by `--target-model` on the CLI; otherwise used in place of the hardcoded default. |
| `judge-model` | Model to invoke for scoring. Overridden by `--judge-model` on the CLI; otherwise used in place of the hardcoded default. |

A malformed frontmatter block (missing closing `---`, line without `:`) fails the run loudly rather than silently falling through — a typo in a model name must not cause the wrong model to run. Tests without frontmatter are unchanged; the runner just sees no preference and falls back to the default.

## Path env overrides

The runner sets these automatically before invoking the target so skills write into the workspace, not into permission-gated `.claude/` paths:

| Env var | Default | Affects |
|---|---|---|
| `HANDOFF_DIR` | workspace `handoff/` | thinking/handoff skill |
| `LEARNINGS_DIR` | workspace `learnings/` | thinking learnings ecosystem |
| `RULES_DIR` | workspace `rules/` | learned rule writes |
| `GLOBAL_LEARNINGS_DIR` | workspace `global-learnings/` | universal learnings |
| `GLOBAL_RULES_DIR` | workspace `global-rules/` | universal learned rules |

Skills that don't read these env vars fall back to their hardcoded defaults — and may then hit Claude Code's `.claude/` write protection. If a new skill writes to `.claude/`, add a path override to its definition (see `plugins/practices/thinking/skills/handoff/SKILL.md` for the pattern).

Add more overrides for the target via `--env`:

```bash
run-test.py ... --env DOCS_DIR=/tmp/docs --env CUSTOM_PATH=/tmp/custom
```

## Artifact snapshotting

After the target finishes, the runner reads every file under the workspace's override dirs (handoff, learnings, rules, etc) plus any new files in the work tree. These are passed to the judge under `## ARTIFACTS WRITTEN` so it can score against actual file contents, not just the chat response. Without this, a skill that writes a 200-line doc and prints a one-line confirmation would be judged on the confirmation alone.

Files over 50KB are truncated. `.git/` and pre-existing files are excluded.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | PASS (≥ 80%) |
| 1 | PARTIAL (≥ 60%) |
| 2 | FAIL (< 60%) |
| 3+ | Infrastructure error (workspace setup, claude invocation, judge response unparseable) |

JSON summary always prints to stdout; progress lines go to stderr. Pipe stdout into `jq` for batch processing:

```bash
run-test.py --test-dir ... --plugin-dir ... | jq '.score_pct'
```

## Costs

Per test, with default models (Haiku target, Sonnet judge):

- Target: ~$0.05 (haiku, 30–60s)
- Judge: ~$0.05 (sonnet, 5–15s)
- Total: ~$0.10 per test

Running all 172 turtlestack tests: ~$17.

## Vendoring into a downstream project

The runner has no turtlestack-specific dependencies. To use it elsewhere:

1. Copy `run-test.py` and `judge-prompt.md` into your repo (e.g. `scripts/eval/`)
2. Adopt the `test.md` format above for your tests
3. Point `--test-dir` and `--plugin-dir` at your own paths
4. Optionally override `--judge-prompt` to enforce house-specific scoring rules

The runner makes no assumptions about your test/plugin layout — there's no `examples/ ↔ plugins/` mirror requirement. As long as `--plugin-dir` points to a valid Claude Code plugin (with `.claude-plugin/plugin.json`) and `--test-dir` contains a `test.md`, it works.

## Caveats

- **Auth and config bleed:** without `--isolate-config` or `--isolate-plugins`, the test session inherits the user's global `~/.claude/` rules and enabled plugins. This can colour skill behaviour. `--isolate-plugins` keeps plugin state hermetic without touching auth (no API key needed) — usually what you want. `--isolate-config` is heavier (full vanilla state) but requires `ANTHROPIC_API_KEY` because `CLAUDE_CONFIG_DIR` redirects break keychain auth.
- **Permission gates on `.claude/`:** Claude Code hard-blocks writes to `.claude/` even under `--dangerously-skip-permissions`. The path env overrides exist specifically to dodge this. New skills that write state should adopt the same override pattern.
- **Judge non-determinism:** the judge is a model call, not a deterministic checker. Re-runs vary by ±2–3 percentage points. The runner does not currently re-run for stability — that's left to the caller.
- **Hooks fire during runs:** `--plugin-dir` loads SessionStart hooks too. If a hook writes to `.claude/`, it will silently fail without an env override. Add overrides to the hook scripts as needed.
