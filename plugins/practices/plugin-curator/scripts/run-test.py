#!/usr/bin/env python3
"""Run a single skill/agent test end-to-end and write result.md.

Pipeline:

  1. Parse test.md (scenario, prompt, criteria, output expectations)
  2. Spawn an isolated workspace under $TMPDIR with vanilla CLAUDE_CONFIG_DIR
  3. Invoke `claude -p --plugin-dir <plugin>` with the test prompt
  4. Capture the result
  5. Invoke a second `claude -p` instance with judge-prompt.md as the system prompt,
     feeding it the criteria and captured output
  6. Parse the judge's JSON response
  7. Write result.md to the test directory

Designed to be portable — no turtlestack-specific paths or assumptions.
Downstream projects can vendor this script and use it against their own
plugin/test layout.

Exit codes:
  0  PASS (>= 80%)
  1  PARTIAL (>= 60%)
  2  FAIL (< 60%)
  3  infrastructure error (workspace setup, claude crash, judge failure)
  4  target API error (content filter block, invalid_request_error, rate limit) —
     the target invocation produced a structured error response, not an
     infra crash. Distinct so callers can decide whether to retry, soften
     the prompt, or escalate to Anthropic.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path

EXIT_PASS = 0
EXIT_PARTIAL = 1
EXIT_FAIL = 2
EXIT_INFRA = 3
EXIT_TARGET_API_ERROR = 4

DEFAULT_TARGET_MODEL = "claude-haiku-4-5-20251001"
DEFAULT_JUDGE_MODEL = "claude-sonnet-4-6"


class TargetAPIError(RuntimeError):
    """Target claude invocation returned a structured error response (e.g. content
    filter block, rate limit, invalid request). Distinct from a runner-side
    infrastructure failure — the runner did its job, the API rejected the call."""


@dataclass
class TestCase:
    scenario: str
    prompt: str
    criteria: list[str]
    output_expectations: list[str]
    test_dir: Path
    frontmatter: dict[str, str] = field(default_factory=dict)

    @property
    def all_criteria(self) -> list[str]:
        return self.criteria + self.output_expectations


@dataclass
class TargetRun:
    result_text: str
    duration_ms: int
    cost_usd: float
    tool_uses: int
    permission_denials: list[dict]
    raw_json: dict
    artifacts: dict[str, str] = field(default_factory=dict)
    binary_artifacts: dict[str, bytes] = field(default_factory=dict)
    """Binary files captured during the run (by workspace-relative path).
    Written next to result.md by write_result_md and linked from there."""


@dataclass
class JudgeOutput:
    verdict: str
    score_points: float
    score_max: float
    score_pct: float
    criteria: list[dict]
    notes: str
    raw_text: str


@dataclass
class RunConfig:
    test_dir: Path
    plugin_dirs: list[Path]
    target_model: str
    judge_model: str
    judge_prompt_path: Path
    extra_env: dict[str, str] = field(default_factory=dict)
    workspace_root: Path | None = None
    keep_workspace: bool = False
    timeout_sec: int = 300
    isolate_config: bool = False
    isolate_plugins: bool = False
    marketplace_sources: dict[str, str] = field(default_factory=dict)
    project_dir: Path | None = None


def parse_test_md(test_dir: Path) -> TestCase:
    test_path = test_dir / "test.md"
    if not test_path.exists():
        raise FileNotFoundError(f"test.md not found at {test_path}")
    text = test_path.read_text()

    frontmatter, body = _split_frontmatter(text, test_path)

    sections: dict[str, str] = {}
    current = "_preamble"
    buf: list[str] = []
    for line in body.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            sections[current] = "\n".join(buf).strip()
            current = m.group(1).strip().lower()
            buf = []
        else:
            buf.append(line)
    sections[current] = "\n".join(buf).strip()

    scenario = sections.get("_preamble", "").strip()
    scenario_lines = [line for line in scenario.splitlines() if line.strip() and not line.startswith("#")]
    scenario_text = " ".join(scenario_lines).strip()

    prompt = sections.get("prompt", "").strip()

    criteria = _extract_checkboxes(sections.get("criteria", ""))
    output_expectations = _extract_checkboxes(sections.get("output expectations", ""))

    if not prompt:
        raise ValueError(f"test.md at {test_path} is missing a ## Prompt section")
    if not (criteria or output_expectations):
        raise ValueError(
            f"test.md at {test_path} has no checkbox criteria under ## Criteria or ## Output expectations"
        )

    return TestCase(
        scenario=scenario_text,
        prompt=prompt,
        criteria=criteria,
        output_expectations=output_expectations,
        test_dir=test_dir,
        frontmatter=frontmatter,
    )


def _split_frontmatter(text: str, test_path: Path) -> tuple[dict[str, str], str]:
    """Detect a leading YAML-style frontmatter block fenced by `---` lines and
    return (parsed_dict, remaining_body). When the file has no frontmatter,
    returns ({}, text) unchanged. Malformed frontmatter fails loudly rather
    than silently falling through — a typo in a model name must not cause the
    wrong model to run."""
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        return {}, text
    lines = text.splitlines(keepends=True)
    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.rstrip() == "---":
            end_idx = i
            break
    if end_idx is None:
        raise ValueError(
            f"test.md at {test_path} starts with `---` but the frontmatter block is unterminated "
            "(expected a closing `---` line)"
        )
    fm: dict[str, str] = {}
    for raw in lines[1:end_idx]:
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            raise ValueError(
                f"test.md at {test_path} has malformed frontmatter line (expected `key: value`): {stripped!r}"
            )
        key, _, value = stripped.partition(":")
        key = key.strip()
        value = value.strip()
        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]
        if not key:
            raise ValueError(f"test.md at {test_path} has frontmatter line with empty key: {stripped!r}")
        fm[key] = value
    body = "".join(lines[end_idx + 1:])
    return fm, body


def _resolve_model(cli_value: str | None, frontmatter_value: str | None, default: str) -> tuple[str, str]:
    """Pick the effective model and report where it came from. CLI flag always wins,
    then test.md frontmatter, then the hardcoded fallback."""
    if cli_value is not None:
        return cli_value, "from CLI flag"
    if frontmatter_value:
        return frontmatter_value, "from test.md frontmatter"
    return default, "default"


def _extract_checkboxes(section: str) -> list[str]:
    items: list[str] = []
    for line in section.splitlines():
        m = re.match(r"^\s*-\s*\[\s*[ xX~]?\s*\]\s*(.+?)\s*$", line)
        if m:
            items.append(m.group(1).strip())
    return items


def make_workspace(root: Path | None) -> Path:
    base = root or Path(os.environ.get("TMPDIR", "/tmp"))
    base.mkdir(parents=True, exist_ok=True)
    runid = f"eval-{int(time.time())}-{uuid.uuid4().hex[:8]}"
    ws = base / runid
    (ws / "work").mkdir(parents=True)
    (ws / "config").mkdir()
    (ws / "learnings").mkdir()
    (ws / "rules").mkdir()
    (ws / "global-learnings").mkdir()
    (ws / "global-rules").mkdir()
    (ws / "handoff").mkdir()

    work = ws / "work"
    subprocess.run(["git", "init", "-q"], cwd=work, check=True)
    (work / "README.md").write_text("# eval workspace\n")
    subprocess.run(["git", "add", "."], cwd=work, check=True)
    subprocess.run(
        ["git", "-c", "user.email=eval@local", "-c", "user.name=eval",
         "-c", "commit.gpgsign=false",
         "commit", "-qm", "initial"],
        cwd=work, check=True,
    )
    return ws


def env_for_run(
    workspace: Path,
    extra: dict[str, str],
    isolate_config: bool,
    isolate_plugins: bool,
) -> dict[str, str]:
    env = os.environ.copy()
    # CLAUDE_CONFIG_DIR isolates the global ~/.claude state — but it also
    # isolates auth (keychain reads target the real path, the redirect breaks
    # auth resolution). Only enable when ANTHROPIC_API_KEY is set or the user
    # has explicitly opted in via --isolate-config.
    if isolate_config:
        env["CLAUDE_CONFIG_DIR"] = str(workspace / "config")
    # CLAUDE_CODE_PLUGIN_CACHE_DIR isolates only plugin state (marketplaces +
    # installed_plugins.json + plugin code). Auth stays where it is, so
    # keychain-based subscription auth keeps working without an API key.
    if isolate_plugins:
        env["CLAUDE_CODE_PLUGIN_CACHE_DIR"] = str(workspace / "plugins")
    env["LEARNINGS_DIR"] = str(workspace / "learnings")
    env["RULES_DIR"] = str(workspace / "rules")
    env["GLOBAL_LEARNINGS_DIR"] = str(workspace / "global-learnings")
    env["GLOBAL_RULES_DIR"] = str(workspace / "global-rules")
    env["HANDOFF_DIR"] = str(workspace / "handoff")
    env.update(extra)
    return env


def _read_plugin_deps(plugin_dirs: list[Path]) -> list[str]:
    """Collect marketplace-qualified dependencies (`name@marketplace`) from each
    --plugin-dir's plugin.json. Skip entries without an `@` qualifier — they're
    not marketplace deps and don't need an install step."""
    deps: list[str] = []
    seen: set[str] = set()
    for plugin_dir in plugin_dirs:
        plugin_json = plugin_dir / ".claude-plugin" / "plugin.json"
        if not plugin_json.exists():
            continue
        try:
            data = json.loads(plugin_json.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        for dep in data.get("dependencies") or []:
            if isinstance(dep, str) and "@" in dep and dep not in seen:
                seen.add(dep)
                deps.append(dep)
    return deps


def setup_isolated_plugins(cfg: RunConfig, workspace: Path) -> None:
    """When --isolate-plugins is set, populate the isolated plugin cache with
    the marketplace deps declared in the plugin-under-test's plugin.json.

    Steps:
      1. Read marketplace-qualified deps from each --plugin-dir/plugin.json.
      2. For each unique marketplace name, look up the source in
         cfg.marketplace_sources and run `claude plugin marketplace add`.
      3. Run `claude plugin install` for each dep.
      4. Verify by reading installed_plugins.json — `claude plugin install`
         exits 0 even on failure, so exit code is not enough.

    Raises RuntimeError on any setup failure."""
    if not cfg.isolate_plugins:
        return

    cache_dir = workspace / "plugins"
    cache_dir.mkdir(exist_ok=True)

    deps = _read_plugin_deps(cfg.plugin_dirs)
    if not deps:
        print("[run-test] --isolate-plugins: no marketplace deps detected, "
              "skipping setup", file=sys.stderr)
        return

    marketplaces = sorted({dep.split("@", 1)[1] for dep in deps})
    missing = [m for m in marketplaces if m not in cfg.marketplace_sources]
    if missing:
        raise RuntimeError(
            f"--isolate-plugins detected marketplace deps that have no "
            f"--marketplace-source mapping: {', '.join(missing)}. "
            f"Detected deps: {deps}. "
            f"Pass --marketplace-source <name>=<source> for each."
        )

    env = os.environ.copy()
    env["CLAUDE_CODE_PLUGIN_CACHE_DIR"] = str(cache_dir)

    for name in marketplaces:
        source = cfg.marketplace_sources[name]
        print(f"[run-test] --isolate-plugins: marketplace add {name}={source}",
              file=sys.stderr)
        proc = subprocess.run(
            ["claude", "plugin", "marketplace", "add", source],
            env=env, capture_output=True, text=True, timeout=180,
        )
        if proc.returncode != 0:
            raise RuntimeError(
                f"marketplace add failed for {name}={source} (exit "
                f"{proc.returncode})\nstdout: {proc.stdout[:500]}\n"
                f"stderr: {proc.stderr[:500]}"
            )

    for dep in deps:
        print(f"[run-test] --isolate-plugins: plugin install {dep}",
              file=sys.stderr)
        proc = subprocess.run(
            ["claude", "plugin", "install", dep],
            env=env, capture_output=True, text=True, timeout=180,
        )
        # Exit code is unreliable — verify via installed_plugins.json below.
        if proc.returncode != 0:
            raise RuntimeError(
                f"plugin install failed for {dep} (exit {proc.returncode})\n"
                f"stdout: {proc.stdout[:500]}\nstderr: {proc.stderr[:500]}"
            )

    installed_path = cache_dir / "installed_plugins.json"
    if not installed_path.exists():
        raise RuntimeError(
            f"plugin install left no installed_plugins.json at {installed_path}"
        )
    try:
        installed_data = json.loads(installed_path.read_text())
    except (json.JSONDecodeError, OSError) as e:
        raise RuntimeError(f"could not read {installed_path}: {e}")
    installed_keys = set(installed_data.get("plugins", {}).keys())
    missing_after = [d for d in deps if d not in installed_keys]
    if missing_after:
        raise RuntimeError(
            f"plugin install reported success but these deps are not in "
            f"installed_plugins.json: {missing_after}. Installed: "
            f"{sorted(installed_keys)}"
        )


_ABS_PATH_TOKEN = re.compile(
    r"(?:(?<=\s)|^)(~/[^\s'\"]+|/[A-Za-z][^\s'\":]*/[^\s'\"]+)"
)
"""Token that looks like an absolute path the operator may have meant as an
artifact destination. Requires at least one more `/` after the leading one
(or a `~/` prefix) so slash commands like `/recon:technical-recon` and
`/foo:bar` don't match. Excludes `:` from the first path segment so namespaced
slash commands are filtered even when followed by a `/`-suffixed argument."""


def warn_external_paths_in_prompt(test: TestCase) -> None:
    """Warn when a test prompt contains absolute or home-relative paths that
    aren't {workspace}-rooted. Skills that write artifacts to such paths bypass
    _snapshot_artifacts, leaving the judge with only the chat summary to
    score against. Symptom: plausible overall score but criteria FAIL with
    "no mention in chat" while the skill clearly produced the artifact.
    """
    tokens = _ABS_PATH_TOKEN.findall(test.prompt)
    suspect = [t for t in tokens if not t.startswith("{workspace}")]
    if not suspect:
        return
    unique = sorted(set(suspect))
    print(
        "[run-test] WARNING: test prompt references absolute / home-relative "
        f"paths that bypass the workspace: {unique}",
        file=sys.stderr,
    )
    print(
        "[run-test] WARNING: artifacts written outside the workspace are "
        "invisible to the judge (it sees only the chat summary). Use "
        "{workspace}/<subpath> in the prompt so the runner can capture "
        "them. Ignore this warning only if the path is genuinely required "
        "(e.g. a Docker volume mount).",
        file=sys.stderr,
    )


def stage_fixtures(test_dir: Path, workspace: Path) -> None:
    """If `<test_dir>/fixtures/` exists, copy its tree into `<workspace>/work/`
    before the target runs.

    The runner's `_snapshot_artifacts` later captures everything under
    `workspace/work/**`, so anything dropped here will be visible to the judge
    as a starting condition. Use this for test scenarios that need real files
    on disk (engagement directories, code samples, config files) — embedding
    them in the prompt is unreliable for smaller target models.

    The fixture tree is rooted at `workspace/work/` so test prompts can
    reference paths like `{workspace}/work/<subpath>` consistently.
    """
    fixtures_dir = test_dir / "fixtures"
    if not fixtures_dir.is_dir():
        return
    work_dir = workspace / "work"
    work_dir.mkdir(exist_ok=True)
    file_count = 0
    for src in fixtures_dir.rglob("*"):
        if not src.is_file():
            continue
        rel = src.relative_to(fixtures_dir)
        dst = work_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        file_count += 1
    if file_count:
        print(
            f"[run-test] staged {file_count} fixture file(s) from "
            f"{fixtures_dir} into {work_dir}",
            file=sys.stderr,
        )


def substitute_workspace_in_prompt(prompt: str, workspace: Path) -> str:
    """Replace `{workspace}` in a test prompt with the resolved workspace path.

    Operators write test prompts with `{workspace}/<subpath>` to tell the
    skill where to write artifacts; the runner substitutes the literal
    workspace path at invocation time. The chosen brace syntax doesn't
    collide with shell variable expansion — prompts are passed as a single
    subprocess argument, not through a shell, so $-style would also be safe,
    but braces read as a template placeholder rather than an env var.
    """
    return prompt.replace("{workspace}", str(workspace))


def warn_unresolved_marketplace_deps(cfg: RunConfig) -> None:
    """When the plugin-under-test declares marketplace-qualified deps but
    --isolate-plugins is not set, claude's plugin loader silently refuses to
    register the parent plugin — slash commands fail with "Unknown command"
    and every criterion scores FAIL. Surface that diagnosis up front so
    operators don't chase a phantom skill regression.

    Tests are designed to run hermetically — the operator's local plugin cache
    is not consulted, so any declared marketplace dep is unresolved unless
    --isolate-plugins + --marketplace-source are provided. We therefore warn
    on every marketplace-qualified dep when --isolate-plugins is off, without
    inspecting the host cache.
    """
    if cfg.isolate_plugins:
        return
    deps = _read_plugin_deps(cfg.plugin_dirs)
    if not deps:
        return
    print(
        "[run-test] WARNING: plugin-under-test declares marketplace-qualified "
        f"dependencies but --isolate-plugins was not set: {deps}",
        file=sys.stderr,
    )
    print(
        "[run-test] WARNING: claude's plugin loader will refuse to register "
        "the parent plugin if these deps aren't installed in the test "
        "workspace. Slash commands may fail with 'Unknown command' (target "
        "duration <100ms, cost $0). Re-run with --isolate-plugins and "
        "--marketplace-source <name>=<source> per referenced marketplace.",
        file=sys.stderr,
    )


def _resolve_plugin_dirs(cfg: RunConfig, test: TestCase) -> list[Path]:
    """Return the list of --plugin-dir paths to pass to claude.

    Each entry in cfg.plugin_dirs is processed independently:
      - If the entry has .claude-plugin/plugin.json, use it as-is.
      - Otherwise (marketplace root), try to derive the specific plugin
        from the test path: examples/<category>/<plugin>/... ->
        <root>/<category>/<plugin>. Keep the root too so marketplace.json /
        settings-based plugins still apply alongside the derived plugin.

    Multiple --plugin-dir entries let a test load a plugin plus its
    declared dependencies (e.g. a downstream plugin and its upstream).
    """
    resolved: list[Path] = []
    for plugin_dir in cfg.plugin_dirs:
        plugin_json = plugin_dir / ".claude-plugin" / "plugin.json"
        if plugin_json.exists():
            resolved.append(plugin_dir)
            continue

        # Root-style path: try to find the specific plugin from test path
        parts = test.test_dir.parts
        derived = None
        for i, part in enumerate(parts):
            if part == "examples" and i + 2 < len(parts):
                candidate = plugin_dir / parts[i + 1] / parts[i + 2]
                if (candidate / ".claude-plugin" / "plugin.json").exists():
                    derived = candidate
                break

        resolved.append(plugin_dir)
        if derived is not None:
            resolved.append(derived)

    # Preserve order, drop duplicates
    seen: set[Path] = set()
    out: list[Path] = []
    for p in resolved:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


def run_target(cfg: RunConfig, test: TestCase, workspace: Path) -> TargetRun:
    plugin_dirs = _resolve_plugin_dirs(cfg, test)
    plugin_dir_args: list[str] = []
    for pd in plugin_dirs:
        plugin_dir_args += ["--plugin-dir", str(pd)]

    effective_prompt = substitute_workspace_in_prompt(test.prompt, workspace)
    cmd = [
        "claude", "-p",
        *plugin_dir_args,
        "--output-format", "json",
        "--dangerously-skip-permissions",
        "--add-dir", str(workspace / "handoff"),
        "--add-dir", str(workspace / "learnings"),
        "--add-dir", str(workspace / "rules"),
        "--model", cfg.target_model,
        effective_prompt,
    ]
    work = cfg.project_dir if cfg.project_dir is not None else workspace / "work"
    env = env_for_run(workspace, cfg.extra_env, cfg.isolate_config, cfg.isolate_plugins)

    proc = subprocess.run(
        cmd, cwd=work, env=env,
        capture_output=True, text=True, timeout=cfg.timeout_sec,
    )

    # Persist raw stdout/stderr unconditionally — most useful exactly when the
    # invocation failed and the operator needs to see what claude returned.
    # Survives only if --keep-workspace is set; the inline error message below
    # is the primary signal for the cleanup-on-exit case.
    debug_dir = workspace / "target-debug"
    debug_dir.mkdir(exist_ok=True)
    (debug_dir / "stdout.json").write_text(proc.stdout or "")
    (debug_dir / "stderr.txt").write_text(proc.stderr or "")

    # Parse stdout BEFORE checking exit code. claude reports API/policy errors
    # (content filter blocks, invalid_request_error, rate limits) as structured
    # JSON in stdout while exiting non-zero. Checking returncode first hides
    # these as opaque "infrastructure errors" and discards the actionable detail.
    data: dict | None = None
    parse_err: json.JSONDecodeError | None = None
    if proc.stdout.strip():
        try:
            data = json.loads(proc.stdout)
        except json.JSONDecodeError as e:
            parse_err = e

    if data is not None and data.get("is_error"):
        result = data.get("result", "") or "(no result text in response)"
        request_id = data.get("request_id") or "unknown"
        raise TargetAPIError(
            f"target returned an error response (exit {proc.returncode}, "
            f"request_id={request_id}): {result[:1500]}\n"
            f"raw stdout/stderr saved to {debug_dir} "
            "(use --keep-workspace to retain after run)"
        )

    if proc.returncode != 0:
        # No structured error from the target — genuine runner-side failure
        # (claude crashed, bad flags, missing binary, etc.).
        stdout_state = "empty" if not proc.stdout.strip() else "unparseable JSON"
        msg = (
            f"claude target invocation failed (exit {proc.returncode}); "
            f"stdout was {stdout_state}\n"
            f"stderr: {proc.stderr[:2000]}\n"
            f"raw stdout/stderr saved to {debug_dir} "
            "(use --keep-workspace to retain after run)"
        )
        if parse_err is not None:
            msg += f"\nstdout parse error: {parse_err}"
        raise RuntimeError(msg)

    if data is None:
        raise RuntimeError(
            f"target returned non-JSON output ({parse_err})\n"
            f"raw stdout saved to {debug_dir / 'stdout.json'} "
            "(use --keep-workspace to retain after run)"
        )

    text_artifacts, binary_artifacts = _snapshot_artifacts(workspace)

    return TargetRun(
        result_text=data.get("result", ""),
        duration_ms=int(data.get("duration_ms", 0)),
        cost_usd=float(data.get("total_cost_usd", 0.0)),
        tool_uses=int(data.get("num_turns", 0)),
        permission_denials=data.get("permission_denials", []),
        raw_json=data,
        artifacts=text_artifacts,
        binary_artifacts=binary_artifacts,
    )


_BINARY_EXTENSIONS = {
    ".pdf", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".bmp", ".tiff",
    ".zip", ".tar", ".gz", ".bz2", ".xz", ".7z", ".rar",
    ".woff", ".woff2", ".ttf", ".otf", ".eot",
    ".mp3", ".mp4", ".mov", ".avi", ".webm", ".wav", ".ogg",
    ".pyc", ".so", ".dylib", ".exe", ".bin", ".o", ".a",
}
"""File extensions treated as binary artifacts. These get copied next to
result.md and linked from it, instead of being embedded as garbled text in
the artifacts section. Add new extensions here as new artifact types appear."""


_HOOK_ARTIFACT_PATHS = {
    "rules",
    "global-rules",
    "learnings/signals",
    "learnings/sessions",
    "global-learnings/signals",
    "global-learnings/sessions",
}
"""Workspace-relative paths populated entirely by hooks, not by skills.

- `rules/` and `global-rules/` come from the SessionStart rule installer (~20 files per session)
- `learnings/signals/patterns.json` holds learned detection regexes read by the analyser
- `learnings/sessions/<SESSION_ID>.json` comes from the SessionStart learning analyser

Including these in snapshots adds ~1500 lines of noise to every result.md and obscures the skill's actual output. Skill output to learnings/global-learnings goes to other paths (memory files written by the /thinking:learning skill), which we still capture."""


def _snapshot_artifacts(workspace: Path) -> tuple[dict[str, str], dict[str, bytes]]:
    """Read every file the target wrote into the workspace's path-override dirs.

    Returns a (text_artifacts, binary_artifacts) pair. Text artifacts get
    embedded inline in result.md; binary artifacts (PDFs, images, archives)
    get written next to result.md and linked from it.

    Files written by hooks (rule installer, learning analyser) are excluded —
    they're session bootstrap, not skill output.
    """
    text_artifacts: dict[str, str] = {}
    binary_artifacts: dict[str, bytes] = {}

    def _capture(path: Path, rel: Path) -> None:
        rel_str = str(rel)
        if path.suffix.lower() in _BINARY_EXTENSIONS:
            try:
                binary_artifacts[rel_str] = path.read_bytes()
            except OSError:
                pass
            return
        try:
            text = path.read_text(errors="replace")
            text = text.replace("\x00", "")
        except (UnicodeDecodeError, OSError):
            return
        if len(text) > 50_000:
            text = text[:50_000] + "\n\n[truncated — over 50KB]"
        text_artifacts[rel_str] = text

    for sub in ("handoff", "learnings", "global-learnings"):
        root = workspace / sub
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(workspace)
            rel_str = str(rel)
            if any(rel_str == hp or rel_str.startswith(hp + "/") for hp in _HOOK_ARTIFACT_PATHS):
                continue
            _capture(path, rel)

    _SKIP_DIRS = {".git", ".claude", ".venv", "venv", "node_modules", "__pycache__",
                  ".tox", ".pytest_cache", "dist", "build", ".mypy_cache",
                  "bin", "obj", ".nuget", "packages", ".gradle", "target"}
    for path in (workspace / "work").rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(workspace)
        if any(p in rel.parts for p in _SKIP_DIRS):
            continue
        if rel.name == "README.md" and rel.parent.name == "work":
            continue
        _capture(path, rel)

    return text_artifacts, binary_artifacts


def run_judge(cfg: RunConfig, test: TestCase, target: TargetRun, workspace: Path) -> JudgeOutput:
    judge_system = cfg.judge_prompt_path.read_text()

    criteria_lines = []
    for i, c in enumerate(test.all_criteria, start=1):
        criteria_lines.append(f"c{i}. {c}")
    criteria_block = "\n".join(criteria_lines)

    artifacts_block = ""
    if target.artifacts or target.binary_artifacts:
        parts = ["## ARTIFACTS WRITTEN\n"]
        parts.append(
            "Files the target wrote to disk during execution. Judge against these "
            "where the criterion asks about file contents — not just the chat response.\n"
        )
        for path, text in target.artifacts.items():
            parts.append(f"\n### `{path}`\n\n```\n{text}\n```\n")
        for path, data in target.binary_artifacts.items():
            size_kb = len(data) // 1024
            parts.append(
                f"\n### `{path}` (binary, {size_kb}KB)\n\n"
                "Binary file — contents not shown. Treat its existence and size as evidence; "
                "do not judge structural details that would require reading the binary.\n"
            )
        artifacts_block = "\n".join(parts) + "\n"

    user_msg = (
        "## TEST\n\n"
        f"**Scenario:** {test.scenario}\n\n"
        f"**Prompt:**\n\n```\n{test.prompt}\n```\n\n"
        "## CAPTURED OUTPUT (chat response)\n\n"
        f"```\n{target.result_text}\n```\n\n"
        f"{artifacts_block}"
        "## CRITERIA TO SCORE\n\n"
        f"{criteria_block}\n\n"
        "Score every criterion. Return only the JSON object specified in your system prompt."
    )

    # We deliberately don't use --bare here — bare mode requires
    # ANTHROPIC_API_KEY/apiKeyHelper for auth and fails without them.
    # Plain headless mode keeps keychain auth and is enough for a single
    # judge call.
    cmd = [
        "claude", "-p",
        "--append-system-prompt", judge_system,
        "--output-format", "json",
        "--model", cfg.judge_model,
    ]
    judge_workspace = workspace / "judge"
    judge_workspace.mkdir(exist_ok=True)
    judge_env = os.environ.copy()
    if cfg.isolate_config:
        judge_env["CLAUDE_CONFIG_DIR"] = str(workspace / "config")
    if cfg.isolate_plugins:
        judge_env["CLAUDE_CODE_PLUGIN_CACHE_DIR"] = str(workspace / "plugins")

    proc = subprocess.run(
        cmd, cwd=judge_workspace, env=judge_env,
        input=user_msg,
        capture_output=True, text=True, timeout=cfg.timeout_sec,
    )
    debug_dir = judge_workspace / "debug"
    if proc.returncode != 0:
        debug_dir.mkdir(exist_ok=True)
        (debug_dir / "stdout.json").write_text(proc.stdout)
        (debug_dir / "stderr.txt").write_text(proc.stderr)
        raise RuntimeError(
            f"judge invocation failed (exit {proc.returncode}) — "
            f"raw stdout/stderr saved to {debug_dir}"
        )
    try:
        outer = json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        debug_dir.mkdir(exist_ok=True)
        (debug_dir / "stdout.json").write_text(proc.stdout)
        raise RuntimeError(
            f"judge returned non-JSON wrapper ({e}) — "
            f"raw stdout saved to {debug_dir / 'stdout.json'}"
        ) from e

    raw_text = outer.get("result", "").strip()
    inner_json = _extract_json_block(raw_text)
    if inner_json is None:
        debug_dir.mkdir(exist_ok=True)
        (debug_dir / "stdout.json").write_text(proc.stdout)
        (debug_dir / "result.txt").write_text(raw_text)
        # If the raw text doesn't end with a closing brace, the judge response
        # was almost certainly cut off by the model's output token cap — flag
        # that explicitly so the failure mode is recognisable.
        truncated = not raw_text.rstrip().endswith("}")
        hint = (
            " (response does not end with '}' — likely truncated by output token cap; "
            "consider shortening evidence per criterion or splitting criteria into batches)"
            if truncated else ""
        )
        raise RuntimeError(
            f"judge response did not contain a JSON object{hint} — "
            f"raw output saved to {debug_dir}"
        )

    return JudgeOutput(
        verdict=inner_json["verdict"],
        score_points=float(inner_json["score_points"]),
        score_max=float(inner_json["score_max"]),
        score_pct=float(inner_json["score_pct"]),
        criteria=inner_json["criteria"],
        notes=inner_json.get("notes", ""),
        raw_text=raw_text,
    )


def _extract_json_block(text: str) -> dict | None:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*\n?", "", text)
        text = re.sub(r"\n?```\s*$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            return None
    return None


def write_result_md(cfg: RunConfig, test: TestCase, target: TargetRun, judge: JudgeOutput) -> Path:
    result_path = test.test_dir / "result.md"
    today = time.strftime("%Y-%m-%d")

    # Resolve binary artifact filenames up-front — same scheme used below when
    # writing them to disk. Lets us surface the links prominently near the top
    # of result.md (above the long prompt blockquote) so readers landing here
    # from the README can click straight through to the produced files.
    binary_targets: dict[str, str] = {}
    used_names: set[str] = set()
    for path, data in target.binary_artifacts.items():
        base = Path(path).name
        target_name = base
        counter = 1
        while target_name in used_names:
            stem = Path(base).stem
            suffix = Path(base).suffix
            target_name = f"{stem}-{counter}{suffix}"
            counter += 1
        used_names.add(target_name)
        binary_targets[path] = target_name

    lines: list[str] = []
    title = test.test_dir.name.replace("-", " ").title()
    lines.append(f"# {title}")
    lines.append("")
    if test.scenario:
        lines.append(test.scenario)
        lines.append("")
    if binary_targets:
        # GitHub renders PDFs and images inline when the link target is a blob,
        # so a markdown link here is directly clickable on the rendered page.
        labels = []
        for path, target_name in binary_targets.items():
            data = target.binary_artifacts[path]
            size_kb = max(1, len(data) // 1024)
            labels.append(f"[{target_name}](./{target_name}) ({size_kb}KB)")
        lines.append("**Output files:** " + " · ".join(labels))
        lines.append("")
    lines.append("## Prompt")
    lines.append("")
    lines.append("> " + test.prompt.replace("\n", "\n> "))
    lines.append("")
    lines.append("## Output")
    lines.append("")
    lines.append("Captured from a real headless invocation of the skill/agent.")
    lines.append("")
    lines.append("### Chat response")
    lines.append("")
    lines.append(target.result_text)
    lines.append("")
    if target.artifacts or target.binary_artifacts:
        lines.append("### Artifacts written")
        lines.append("")
        for path, text in target.artifacts.items():
            lines.append(f"#### `{path}`")
            lines.append("")
            lines.append("```")
            lines.append(text)
            lines.append("```")
            lines.append("")
        # Binary artifacts: write next to result.md, link rather than embed.
        # Filenames were resolved at the top of this function (see binary_targets)
        # so the same name is used in both the up-front summary and here.
        for path, target_name in binary_targets.items():
            data = target.binary_artifacts[path]
            (test.test_dir / target_name).write_bytes(data)
            size_kb = max(1, len(data) // 1024)
            lines.append(f"#### `{path}`")
            lines.append("")
            lines.append(f"Binary artifact ({size_kb}KB) — see [`{target_name}`](./{target_name})")
            lines.append("")
    lines.append("## Evaluation")
    lines.append("")
    lines.append("| Field | Value |")
    lines.append("|---|---|")
    lines.append(f"| Verdict | {judge.verdict} |")
    lines.append(f"| Score | {judge.score_points}/{judge.score_max} ({judge.score_pct:.0f}%) |")
    lines.append(f"| Evaluated | {today} |")
    lines.append(f"| Target model | {cfg.target_model} |")
    lines.append(f"| Judge model | {cfg.judge_model} |")
    lines.append(f"| Target duration | {target.duration_ms} ms |")
    lines.append(f"| Target cost | ${target.cost_usd:.4f} |")
    lines.append(f"| Permission denials | {len(target.permission_denials)} |")
    lines.append("")
    lines.append("### Criteria")
    lines.append("")
    lines.append("| # | Criterion | Result | Evidence |")
    lines.append("|---|---|---|---|")
    for c in judge.criteria:
        crit_text = c.get("text", "").replace("|", "\\|")
        evidence = c.get("evidence", "").replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {c.get('id', '')} | {crit_text} | {c.get('result', '')} | {evidence} |")
    lines.append("")
    if judge.notes:
        lines.append("### Notes")
        lines.append("")
        lines.append(judge.notes)
        lines.append("")

    result_path.write_text("\n".join(lines))
    return result_path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--test-dir", required=True, type=Path,
                   help="Path to a test directory (containing test.md)")
    p.add_argument("--plugin-dir", required=True, action="append", type=Path,
                   help="Path to a plugin directory to load for the test session "
                        "(contains .claude-plugin/plugin.json). Repeatable — "
                        "pass once for the plugin under test, again for any "
                        "dependencies it declares.")
    p.add_argument("--target-model", default=None,
                   help="Model to invoke for the skill/agent under test. When omitted, the runner "
                        "falls back to test.md frontmatter (`target-model: ...`), then to "
                        f"{DEFAULT_TARGET_MODEL}.")
    p.add_argument("--judge-model", default=None,
                   help="Model to invoke for scoring the captured output. When omitted, the runner "
                        "falls back to test.md frontmatter (`judge-model: ...`), then to "
                        f"{DEFAULT_JUDGE_MODEL}.")
    p.add_argument("--judge-prompt", type=Path,
                   default=Path(__file__).resolve().parent / "judge-prompt.md",
                   help="Judge system prompt template")
    p.add_argument("--workspace-root", type=Path,
                   help="Override base directory for the per-run workspace")
    p.add_argument("--keep-workspace", action="store_true",
                   help="Don't delete the workspace after the run")
    p.add_argument("--env", action="append", default=[],
                   metavar="KEY=VALUE",
                   help="Extra environment variable for the target run (repeatable)")
    p.add_argument("--timeout", type=int, default=1200,
                   help="Timeout in seconds for both target and judge invocations. "
                        "Default 1200s (20 min) — research skills that do multiple "
                        "WebFetches and follow follow-on routing can legitimately run "
                        "5-10 minutes. Previous 300s and 600s defaults cut OSINT "
                        "investigations off mid-run.")
    p.add_argument("--isolate-config", action="store_true",
                   help="Set CLAUDE_CONFIG_DIR to the workspace (full vanilla global state). "
                        "Requires ANTHROPIC_API_KEY in the environment — keychain auth "
                        "will not resolve through the redirected config dir.")
    p.add_argument("--isolate-plugins", action="store_true",
                   help="Set CLAUDE_CODE_PLUGIN_CACHE_DIR to a workspace subdir, "
                        "isolating marketplaces and plugin installs from ~/.claude/plugins. "
                        "Auth still works via keychain (no API key needed). When enabled, "
                        "the runner reads marketplace-qualified deps from each --plugin-dir's "
                        "plugin.json and pre-populates the isolated cache via `claude plugin "
                        "marketplace add` + `claude plugin install`. Requires "
                        "--marketplace-source for each marketplace name referenced.")
    p.add_argument("--marketplace-source", action="append", default=[],
                   metavar="NAME=SOURCE",
                   help="Map a marketplace name to its source for `claude plugin "
                        "marketplace add` (e.g., turtlestack=hpsgd/turtlestack). Repeatable. "
                        "Required for each unique marketplace referenced in the deps of "
                        "any --plugin-dir under --isolate-plugins.")
    p.add_argument("--project-dir", type=Path,
                   help="Run the target with this directory as cwd (default: a tmp "
                        "workspace dir). Use to pick up project-scoped plugins from "
                        "the marketplace under test, so the test session sees the "
                        "plugins you've installed against that project.")
    p.add_argument("--write-result", action="store_true", default=True,
                   help="Write result.md to the test directory (default: true)")
    p.add_argument("--no-write-result", dest="write_result", action="store_false",
                   help="Skip writing result.md (still emits JSON to stdout)")
    return p.parse_args()


def main() -> int:
    args = parse_args()

    extra_env = {}
    for kv in args.env:
        if "=" not in kv:
            print(f"Invalid --env value (expected KEY=VALUE): {kv}", file=sys.stderr)
            return EXIT_INFRA
        k, v = kv.split("=", 1)
        extra_env[k.strip()] = v

    marketplace_sources: dict[str, str] = {}
    for kv in args.marketplace_source:
        if "=" not in kv:
            print(f"Invalid --marketplace-source value (expected NAME=SOURCE): {kv}",
                  file=sys.stderr)
            return EXIT_INFRA
        k, v = kv.split("=", 1)
        marketplace_sources[k.strip()] = v.strip()

    test_dir = args.test_dir.resolve()
    print(f"[run-test] reading {test_dir}/test.md", file=sys.stderr)
    test = parse_test_md(test_dir)
    print(f"[run-test] {len(test.all_criteria)} criteria parsed", file=sys.stderr)

    target_model, target_source = _resolve_model(
        args.target_model, test.frontmatter.get("target-model"), DEFAULT_TARGET_MODEL,
    )
    judge_model, judge_source = _resolve_model(
        args.judge_model, test.frontmatter.get("judge-model"), DEFAULT_JUDGE_MODEL,
    )
    print(f"[run-test] target-model: {target_model} ({target_source})", file=sys.stderr)
    print(f"[run-test] judge-model: {judge_model} ({judge_source})", file=sys.stderr)

    cfg = RunConfig(
        test_dir=test_dir,
        plugin_dirs=[p.resolve() for p in args.plugin_dir],
        target_model=target_model,
        judge_model=judge_model,
        judge_prompt_path=args.judge_prompt.resolve(),
        extra_env=extra_env,
        workspace_root=args.workspace_root.resolve() if args.workspace_root else None,
        keep_workspace=args.keep_workspace,
        timeout_sec=args.timeout,
        isolate_config=args.isolate_config,
        isolate_plugins=args.isolate_plugins,
        marketplace_sources=marketplace_sources,
        project_dir=args.project_dir.resolve() if args.project_dir else None,
    )

    workspace = make_workspace(cfg.workspace_root)
    print(f"[run-test] workspace: {workspace}", file=sys.stderr)

    try:
        setup_isolated_plugins(cfg, workspace)
        warn_unresolved_marketplace_deps(cfg)
        warn_external_paths_in_prompt(test)
        stage_fixtures(cfg.test_dir, workspace)

        print("[run-test] invoking target...", file=sys.stderr)
        target = run_target(cfg, test, workspace)
        print(f"[run-test] target done in {target.duration_ms}ms, "
              f"${target.cost_usd:.4f}, denials={len(target.permission_denials)}",
              file=sys.stderr)

        print("[run-test] invoking judge...", file=sys.stderr)
        judge = run_judge(cfg, test, target, workspace)
        print(f"[run-test] judge: {judge.verdict} {judge.score_points}/{judge.score_max} "
              f"({judge.score_pct:.0f}%)", file=sys.stderr)

        if args.write_result:
            result_path = write_result_md(cfg, test, target, judge)
            print(f"[run-test] wrote {result_path}", file=sys.stderr)

        summary = {
            "test_dir": str(cfg.test_dir),
            "verdict": judge.verdict,
            "score_points": judge.score_points,
            "score_max": judge.score_max,
            "score_pct": judge.score_pct,
            "target_model": cfg.target_model,
            "judge_model": cfg.judge_model,
            "target_duration_ms": target.duration_ms,
            "target_cost_usd": target.cost_usd,
            "target_denials": len(target.permission_denials),
            "result_md": str(cfg.test_dir / "result.md") if args.write_result else None,
        }
        print(json.dumps(summary, indent=2))
    finally:
        if not cfg.keep_workspace:
            shutil.rmtree(workspace, ignore_errors=True)
            print(f"[run-test] cleaned up {workspace}", file=sys.stderr)
        else:
            print(f"[run-test] kept workspace at {workspace}", file=sys.stderr)

    if judge.verdict == "PASS":
        return EXIT_PASS
    if judge.verdict == "PARTIAL":
        return EXIT_PARTIAL
    return EXIT_FAIL


if __name__ == "__main__":
    try:
        sys.exit(main())
    except TargetAPIError as e:
        print(f"[run-test] target API error: {e}", file=sys.stderr)
        sys.exit(EXIT_TARGET_API_ERROR)
    except Exception as e:
        print(f"[run-test] infrastructure error: {e}", file=sys.stderr)
        sys.exit(EXIT_INFRA)
