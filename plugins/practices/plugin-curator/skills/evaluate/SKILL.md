---
name: evaluate
description: "Run rubric-style tests against skill and agent plugins by invoking them headlessly, capturing real output and artifacts, and judging against test criteria. Replaces the prior simulation-based evaluator. Use to verify a single test, a directory of tests, or every test in the marketplace."
argument-hint: "[test path or directory; default: all of examples/]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Evaluate

Run rubric tests against plugin definitions. Each run invokes the skill or agent in a real headless `claude -p` session, captures the chat response and any files written, then asks a judge model to score against the test's criteria.

This skill **does not simulate**. Earlier versions wrote `result.md` files containing imagined output. That was unreliable — fixes against simulated weaknesses didn't always change real-run behaviour. The runner now executes targets for real.

## Modes

`$ARGUMENTS` selects the scope:

| Mode | Trigger | Action |
|---|---|---|
| Empty / `all` | `/evaluate` | Run every `test.md` under `examples/` |
| Directory | `/evaluate examples/research` | Run every `test.md` under that subtree |
| Single test | `/evaluate examples/practices/thinking/skills/handoff` | Run only that one test |

## Step 1: Resolve runner

The runner script lives at:

```bash
RUNNER="${CLAUDE_PLUGIN_ROOT}/scripts/run-test.py"
```

If the script doesn't exist, stop and tell the user to install or update the `plugin-curator` plugin.

## Step 2: Discover tests

Find every `test.md` under the requested scope:

```bash
SCOPE="${ARGUMENTS:-examples}"
find "$SCOPE" -type f -name 'test.md' 2>/dev/null | sort
```

If `$SCOPE` is itself a test directory (contains `test.md`), use that single test.

If no `test.md` files exist, report that plainly and stop.

## Step 3: Resolve plugin source per test

For each `test.md`, derive the plugin under test:

- **Skill test:** path matches `examples/<category>/<plugin>/skills/<name>/test.md` → plugin source is `plugins/<category>/<plugin>` (the directory containing `.claude-plugin/plugin.json`)
- **Agent test:** path matches `examples/<category>/<plugin>/agents/<role>/<scenario>/test.md` → plugin source is `plugins/<category>/<plugin>`

Verify the plugin source has `.claude-plugin/plugin.json` before invoking the runner. If missing, skip the test and record `missing-plugin` in the report.

## Step 4: Invoke the runner

For each (test, plugin) pair, run:

```bash
"$RUNNER" \
  --test-dir "<test_dir>" \
  --plugin-dir "<plugin_dir>"
```

The runner picks the target model from (in order) the `--target-model` flag, a `target-model:` entry in the test's frontmatter, or its hardcoded default. Same precedence for `--judge-model`. Only pass `--target-model` / `--judge-model` for ad-hoc overrides; otherwise let the test or the default decide.

The runner emits a JSON summary on stdout (including the `target_model` and `judge_model` that ran). Capture that. The runner also writes `result.md` to `<test_dir>` for inspection.

Exit code reflects the verdict:

- `0` PASS (≥ 80%)
- `1` PARTIAL (≥ 60%)
- `2` FAIL (< 60%)
- `3` infrastructure error (workspace setup, claude crash, judge response unparseable)
- `4` target API error — the target invocation returned a structured error response (content-filter block, `invalid_request_error`, rate limit). Not an infra failure: the runner did its job, the API rejected the call. The error message includes the API error text and `request_id`.

Treat exit codes ≥ 3 as failures of the harness, not the skill — record them as `infra-error` (3) or `api-error` (4) in the report and continue. For exit 4, capture the API error message and `request_id` so the operator can decide whether to retry, soften the prompt, switch model, or escalate to Anthropic.

For long batches, run sequentially. Parallel runs are safe in principle (each gets its own tmp workspace) but cost-of-debugging outweighs the speed-up for now.

### Plugin dependencies and isolation

If the plugin under test declares marketplace-qualified dependencies (any `"dependencies"` entry of the form `name@marketplace`), the runner cannot resolve them against the operator's local plugin cache — tests are meant to run hermetically. Pass `--isolate-plugins` so the runner sets up a per-run isolated plugin cache, and one `--marketplace-source <name>=<source>` per marketplace referenced:

```bash
"$RUNNER" \
  --test-dir "<test_dir>" \
  --plugin-dir "<plugin_dir>" \
  --isolate-plugins \
  --marketplace-source turtlestack=hpsgd/turtlestack
```

Without `--isolate-plugins`, claude's plugin loader silently refuses to register a plugin whose declared dependencies aren't installed — meaning the plugin's slash commands (and skills, agents) never become available to the target session. The target invocation returns `Unknown command: /<ns>:<skill>` in tens of milliseconds with zero model cost. Every criterion then scores FAIL, which looks identical to a skill regression but is actually harness misconfiguration.

This applies to any plugin with marketplace-qualified deps — even when a single test happens to "just work" because the dep is rules-only and contributes no commands.

### Test prompt conventions

Test prompts may pass an output directory to the skill (some skills accept an artifact destination as an argument). Use the literal token `{workspace}` for that destination — the runner substitutes the resolved per-run workspace path before invoking the target:

```
/recon:technical-recon canva.com {workspace}/assessments/canva
```

The runner captures everything written under the workspace and feeds it to the judge as artifacts. Anything written *outside* the workspace (e.g. `~/Assessments/canva` or `/tmp/foo`) is invisible to the judge — it only sees the chat summary, which is deliberately terse, and criteria that depend on the artifact will FAIL even when the skill produced it correctly. Symptom: plausible overall score but specific criteria FAIL with "no mention in chat" while the actual report file looks fine.

The runner warns on stderr if a test prompt references absolute or home-relative paths that aren't `{workspace}`-rooted. Ignore the warning only if the path is genuinely required (Docker volume mount, system cache).

### Fixture files

When a test needs files on disk before the target runs (an engagement directory, a code sample, a config file), put them under `<test_dir>/fixtures/`. The runner copies the entire tree into `{workspace}/work/` before invoking the target. Test prompts can then reference `{workspace}/work/<subpath>` directly without asking the model to write the fixtures itself — embedding fixture content in the prompt is unreliable, especially for smaller target models that often misparse nested code blocks or heredocs.

The fixture tree mirrors the layout you want under `work/`. For example:

```
examples/<cat>/<plug>/skills/<skill>/
├── test.md
└── fixtures/
    └── visualcare/
        ├── people-lookup/graves-michael.md
        ├── domain-intel/visualcare-com-au.md
        └── ip-intel/52-12-34-56.md
```

After the runner stages those, the target sees them at `{workspace}/work/visualcare/...`.

## Troubleshooting

| Signal | Likely cause |
|---|---|
| `target_duration_ms < 100` and `target_cost_usd == 0`, every criterion FAIL | Slash command never registered. Plugin under test has marketplace deps that need `--isolate-plugins` + `--marketplace-source`. |
| Plausible overall score but criteria FAIL with "no mention in chat" / "not found in output" while the skill clearly produced the artifact | Skill wrote files to a path outside the workspace (e.g. `~/Assessments/...` taken from the test prompt). Update the test prompt to use `{workspace}/<subpath>` so the runner can capture them. |

## Step 5: Build the summary

For directory or all-tests mode, collect the per-test JSON summaries into a table for chat output. Don't write this to a file — each test's `result.md` already carries the full record on disk; an aggregate snapshot just goes stale between runs.

Use this shape:

```markdown
| Field | Value |
|---|---|
| Run date | <YYYY-MM-DD> |
| Total | N tests |
| Passed | N |
| Partial | N |
| Failed | N |
| Infra errors | N |
| Score range | X%–Y% |
| Average | Z% |
| Median | M% |
| Total cost | $X.XX |
| Total duration | XmYs |

| Test | Type | Verdict | Score | Cost | Duration |
|---|---|---|---|---|---|
| <relative-path> | skill\|agent | PASS\|PARTIAL\|FAIL | X/Y (Z%) | $0.XX | XX s |
```

Sort the results table by score ascending so the lowest-scoring tests surface first. Verdicts under PASS deserve attention before the high scorers.

For single-test mode, skip the table and just print the runner's JSON output along with the `result.md` path.

## Step 6: Report back

Print a summary table and flag anything that needs attention:

- Tests with `FAIL` verdict
- Tests with `infra-error`
- Tests with `PARTIAL` that previously passed (regression)
- Tests where target cost or duration is significantly above the median (suggests the skill is wandering)

Don't suggest fixes here — that's a separate workflow. Just surface the data.

## Argument matrix

| Argument | Behaviour |
|---|---|
| (empty) | Run every `test.md` under `examples/`, print summary table to chat |
| `examples/research` | Run every `test.md` under that subtree, print summary table to chat |
| `examples/practices/thinking/skills/handoff` | Run that single test, print its result.md path |
| `path/that/doesnt/exist` | Report missing path, stop |
| Anything else | Treat as a path, glob for `test.md` underneath |

## Rules

- **Real execution only.** Never write a `result.md` containing simulated output. If the runner can't fire (e.g. `claude` not in PATH, no auth), report the infrastructure failure — don't fabricate a score.
- **One test, one workspace.** The runner creates a fresh tmp workspace per test. Never reuse workspaces across tests — cross-contamination invalidates results.
- **Sort by score ascending.** The bottom of the table is what matters. Don't bury low scorers.
- **Don't tune until you've measured.** If a test scores below 80%, surface it. Don't immediately edit the skill — first confirm the gap is real (re-run if judge variance is plausible), then fix.
- **Treat infra errors as bugs in the harness, not the skill.** Don't downgrade a skill verdict because the runner couldn't authenticate or the workspace got wedged. Fix the harness first.

## Output format

### Single-test mode

```markdown
## Evaluated: <test path>

**Verdict:** <PASS|PARTIAL|FAIL>
**Score:** X/Y (Z%)
**Target cost:** $0.XX
**Target duration:** XX s
**Result file:** `<test_dir>/result.md`

<one paragraph summary of any criteria that didn't pass, or notes from the judge>
```

### Multi-test mode

Print the summary block and results table from Step 5 directly to chat, followed by:

```markdown
N tests — X passed, Y partial, Z failed. Total cost $X.XX, total duration XmYs.

<sub-90% tests listed inline so they're impossible to miss>
```

Per-test `result.md` files on disk hold the full output and judge reasoning for any test the user wants to drill into.

## Related skills

- `/plugin-curator:create-skill` — scaffolds new skills with a `test.md` ready to evaluate
- `/plugin-curator:audit-skill` — structural audit (separate from rubric evaluation)
- `/plugin-curator:audit-agent` — same, for agents

## Downstream usage

The runner is portable and has no marketplace-specific assumptions. To use the same harness in a downstream repo, copy `scripts/run-test.py` and `scripts/judge-prompt.md` into the target project. See `${CLAUDE_PLUGIN_ROOT}/scripts/README.md` for full vendoring instructions.
