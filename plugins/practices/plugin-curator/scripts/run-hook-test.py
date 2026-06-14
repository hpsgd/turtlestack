#!/usr/bin/env python3
"""Deterministic hook tester — sibling of run-test.py.

Claude Code hooks are deterministic: given stdin (an event JSON) and environment,
they produce stdout (a JSON hook response, or silence) and an exit code. That
needs exact assertions, not an LLM judge — so hook tests live here, not in the
judge-based run-test.py.

A hook test is a `hook-test.md` file:

    ---
    kind: hook
    hook: plugins/practices/security-compliance/scripts/security-baseline-hook.sh
    ---

    # Hook test: <title>

    <scenario paragraph>

    ## Setup            (optional — bash run in the workspace before the hook)
    mkdir -p .claude/turtlestack

    ## Env              (optional — KEY=VALUE per line; tokens substituted)
    CLAUDE_PLUGIN_ROOT={plugin_dir}
    CLAUDE_CONFIG_DIR={workspace}/config

    ## Stdin            (optional — fenced block piped to the hook)
    ```json
    {"tool_name": "Write", "tool_input": {"content": "api_key = \"AKIA...\""}}
    ```

    ## Assertions       (required — one check per line)
    - exit 0
    - stdout contains: hardcoded-secret
    - stdout not contains: should-not-appear
    - stdout regex: PreToolUse
    - stdout empty
    - file exists: config/turtlestack/notices-seen.json
    - file contains: config/.../foo.md :: some text

Tokens usable in Env values, Setup, and file-path assertions:
  {workspace}  the per-run temp dir (cwd of the hook)
  {plugin_dir} the --plugin-dir (the plugin root holding the hook)
  {test_dir}   the test directory
  {repo_root}  the repo root (runner cwd)

Exit codes mirror run-test.py: 0 PASS, 2 FAIL, 3 infra error.
A JSON summary always prints to stdout; result.md is written to the test dir.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class HookTest:
    title: str
    hook: str
    env: list[tuple[str, str]] = field(default_factory=list)
    setup: str = ""
    stdin: str = ""
    assertions: list[str] = field(default_factory=list)


def _section(body: str, name: str) -> str | None:
    """Return the text of a `## <name>` section, or None if absent."""
    pat = re.compile(rf"^##\s+{re.escape(name)}\s*$", re.MULTILINE | re.IGNORECASE)
    m = pat.search(body)
    if not m:
        return None
    start = m.end()
    nxt = re.search(r"^##\s+", body[start:], re.MULTILINE)
    end = start + nxt.start() if nxt else len(body)
    return body[start:end].strip("\n")


def _strip_fence(text: str) -> str:
    """If the text is a single fenced code block, return its inner content."""
    t = text.strip()
    fence = re.match(r"^```[^\n]*\n(.*)\n```$", t, re.DOTALL)
    return fence.group(1) if fence else t


def parse_hook_test(path: Path) -> HookTest:
    raw = path.read_text()
    if not raw.startswith("---"):
        raise ValueError("hook-test.md must start with a YAML frontmatter block")
    end = raw.find("\n---", 3)
    if end == -1:
        raise ValueError("unterminated frontmatter block")
    fm_block = raw[3:end].strip()
    body = raw[end + 4:]

    fm: dict[str, str] = {}
    for line in fm_block.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"frontmatter line without ':' -> {line!r}")
        k, v = line.split(":", 1)
        fm[k.strip()] = v.strip()

    if fm.get("kind") != "hook":
        raise ValueError("frontmatter must declare `kind: hook`")
    if not fm.get("hook"):
        raise ValueError("frontmatter must declare `hook: <path>`")

    title_m = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else path.parent.name

    env: list[tuple[str, str]] = []
    env_sec = _section(body, "Env")
    if env_sec:
        for line in env_sec.splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env.append((k.strip(), v.strip()))

    setup = _strip_fence(_section(body, "Setup") or "")
    stdin = _strip_fence(_section(body, "Stdin") or "")

    assertions: list[str] = []
    a_sec = _section(body, "Assertions")
    if a_sec:
        for line in a_sec.splitlines():
            line = line.strip()
            if line.startswith("-"):
                line = line[1:].strip()
            if line:
                assertions.append(line)
    if not assertions:
        raise ValueError("hook test needs at least one assertion under `## Assertions`")

    return HookTest(title=title, hook=fm["hook"], env=env,
                    setup=setup, stdin=stdin, assertions=assertions)


def substitute(text: str, tokens: dict[str, str]) -> str:
    for k, v in tokens.items():
        text = text.replace("{" + k + "}", v)
    return text


@dataclass
class CheckResult:
    text: str
    passed: bool
    evidence: str


def evaluate_assertions(
    assertions: list[str], rc: int, out: str, err: str,
    workspace: Path, tokens: dict[str, str],
) -> list[CheckResult]:
    results: list[CheckResult] = []
    for a in assertions:
        results.append(_check_one(a, rc, out, err, workspace, tokens))
    return results


def _check_one(a: str, rc: int, out: str, err: str,
               workspace: Path, tokens: dict[str, str]) -> CheckResult:
    low = a.lower()

    if low.startswith("exit"):
        want = a.split(None, 1)[1].strip()
        ok = str(rc) == want
        return CheckResult(a, ok, f"actual exit {rc}")

    if low == "stdout empty":
        ok = out.strip() == ""
        return CheckResult(a, ok, "stdout empty" if ok else f"stdout had {len(out)} chars")

    if low == "stderr empty":
        ok = err.strip() == ""
        return CheckResult(a, ok, "stderr empty" if ok else f"stderr had {len(err)} chars")

    for prefix, stream, negate in (
        ("stdout contains:", out, False),
        ("stdout not contains:", out, True),
        ("stderr contains:", err, False),
    ):
        if low.startswith(prefix):
            needle = a[len(prefix):].strip()
            present = needle in stream
            ok = (not present) if negate else present
            return CheckResult(a, ok, f"{'present' if present else 'absent'}: {needle!r}")

    if low.startswith("stdout regex:"):
        pat = a[len("stdout regex:"):].strip()
        try:
            ok = re.search(pat, out) is not None
        except re.error as e:
            return CheckResult(a, False, f"bad regex: {e}")
        return CheckResult(a, ok, f"regex {'matched' if ok else 'no match'}: {pat!r}")

    if low.startswith("file exists:"):
        rel = substitute(a[len("file exists:"):].strip(), tokens)
        target = (workspace / rel) if not Path(rel).is_absolute() else Path(rel)
        ok = target.exists()
        return CheckResult(a, ok, f"{'exists' if ok else 'missing'}: {target}")

    if low.startswith("file contains:"):
        spec = a[len("file contains:"):].strip()
        if "::" not in spec:
            return CheckResult(a, False, "malformed `file contains:` (need `path :: text`)")
        rel, needle = (s.strip() for s in spec.split("::", 1))
        rel = substitute(rel, tokens)
        target = (workspace / rel) if not Path(rel).is_absolute() else Path(rel)
        if not target.exists():
            return CheckResult(a, False, f"missing file: {target}")
        ok = needle in target.read_text(errors="replace")
        return CheckResult(a, ok, f"{'found' if ok else 'not found'} in {target}: {needle!r}")

    return CheckResult(a, False, f"unrecognised assertion: {a!r}")


def write_result(test_dir: Path, ht: HookTest, hook_path: Path, rc: int,
                 out: str, err: str, checks: list[CheckResult], verdict: str) -> Path:
    passed = sum(1 for c in checks if c.passed)
    lines = [
        f"# Hook test result: {ht.title}",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Verdict | {verdict} |",
        f"| Checks | {passed}/{len(checks)} |",
        f"| Hook | `{hook_path}` |",
        f"| Hook exit | {rc} |",
        "",
        "## Assertions",
        "",
        "| Result | Assertion | Evidence |",
        "|---|---|---|",
    ]
    for c in checks:
        mark = "PASS" if c.passed else "FAIL"
        ev = c.evidence.replace("|", "\\|").replace("\n", " ")
        at = c.text.replace("|", "\\|")
        lines.append(f"| {mark} | {at} | {ev} |")
    lines += ["", "## Captured stdout", "", "```", out.rstrip() or "(empty)", "```", ""]
    if err.strip():
        lines += ["## Captured stderr", "", "```", err.rstrip(), "```", ""]
    path = test_dir / "result.md"
    path.write_text("\n".join(lines))
    return path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--test-dir", required=True, type=Path,
                    help="Directory containing hook-test.md")
    ap.add_argument("--plugin-dir", type=Path,
                    help="Plugin root holding the hook (sets {plugin_dir} token "
                         "and the default CLAUDE_PLUGIN_ROOT if the test references it)")
    ap.add_argument("--repo-root", type=Path, default=Path.cwd(),
                    help="Repo root for resolving the frontmatter `hook:` path (default: cwd)")
    ap.add_argument("--timeout", type=int, default=30,
                    help="Seconds to allow the hook to run (default 30)")
    ap.add_argument("--keep-workspace", action="store_true")
    ap.add_argument("--write-result", action="store_true", default=True)
    ap.add_argument("--no-write-result", dest="write_result", action="store_false")
    args = ap.parse_args()

    test_dir = args.test_dir.resolve()
    spec = test_dir / "hook-test.md"
    if not spec.exists():
        print(json.dumps({"verdict": "INFRA", "error": f"no hook-test.md in {test_dir}"}))
        return 3

    try:
        ht = parse_hook_test(spec)
    except ValueError as e:
        print(json.dumps({"verdict": "INFRA", "error": f"parse error: {e}"}))
        return 3

    repo_root = args.repo_root.resolve()
    hook_path = (repo_root / ht.hook).resolve()
    if not hook_path.exists():
        print(json.dumps({"verdict": "INFRA", "error": f"hook not found: {hook_path}"}))
        return 3

    plugin_dir = args.plugin_dir.resolve() if args.plugin_dir else hook_path.parent.parent

    workspace = Path(tempfile.mkdtemp(prefix=f"hooktest-{uuid.uuid4().hex[:8]}-"))
    tokens = {
        "workspace": str(workspace),
        "plugin_dir": str(plugin_dir),
        "test_dir": str(test_dir),
        "repo_root": str(repo_root),
    }

    try:
        if ht.setup:
            subprocess.run(["bash", "-c", substitute(ht.setup, tokens)],
                           cwd=workspace, check=True, timeout=args.timeout,
                           capture_output=True, text=True)

        import os
        env = os.environ.copy()
        # A hook test starts from a clean slate: don't inherit the operator's
        # plugin root or config dir unless the test sets them explicitly.
        env.pop("CLAUDE_PLUGIN_ROOT", None)
        for k, v in ht.env:
            env[k] = substitute(v, tokens)

        proc = subprocess.run(
            ["bash", str(hook_path)],
            input=ht.stdin,
            cwd=workspace,
            env=env,
            timeout=args.timeout,
            capture_output=True,
            text=True,
        )
        rc, out, err = proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        print(json.dumps({"verdict": "INFRA", "error": f"hook timed out after {args.timeout}s"}))
        if not args.keep_workspace:
            shutil.rmtree(workspace, ignore_errors=True)
        return 3
    except subprocess.CalledProcessError as e:
        print(json.dumps({"verdict": "INFRA", "error": f"setup failed: {e.stderr or e}"}))
        if not args.keep_workspace:
            shutil.rmtree(workspace, ignore_errors=True)
        return 3

    checks = evaluate_assertions(ht.assertions, rc, out, err, workspace, tokens)
    passed = sum(1 for c in checks if c.passed)
    verdict = "PASS" if passed == len(checks) else "FAIL"

    result_path = None
    if args.write_result:
        result_path = write_result(test_dir, ht, hook_path, rc, out, err, checks, verdict)

    if not args.keep_workspace:
        shutil.rmtree(workspace, ignore_errors=True)

    print(json.dumps({
        "test": str(test_dir),
        "title": ht.title,
        "verdict": verdict,
        "checks_passed": passed,
        "checks_total": len(checks),
        "hook_exit": rc,
        "result_md": str(result_path) if result_path else None,
        "failures": [c.text for c in checks if not c.passed],
    }))
    return 0 if verdict == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
