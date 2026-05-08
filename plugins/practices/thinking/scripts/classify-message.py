#!/usr/bin/env python3
"""Classify a user message for sentiment/correction signals.

Reads hook payload from stdin (UserPromptSubmit event).
Uses fast regex for obvious cases (corrections, praise).
Queues ambiguous messages for later classification by Claude
during the retrospective analysis (which runs inside Claude
and doesn't need an external API).

Writes to .claude/<marketplace>/learnings/signals/pending.jsonl
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# --- Seed patterns (hardcoded baseline) ---
# These are the starting set. The retrospective skill adds learned
# patterns to .claude/<marketplace>/learnings/signals/patterns.json at runtime.

SEED_NOT_CORRECTION = [
    r"^(ok|okay|yes|y|yep|yeah|sure|go ahead|lgtm|ship it|commit|push|done|thanks|good|great|perfect|nice)\b",
    r"^/",  # Slash commands
    r"^!",  # Shell escapes
]

SEED_CORRECTION = [
    r"^no[,.\s]",
    r"\bthat'?s (not |wrong|incorrect)",
    r"\bstop (doing|that|it)",
    r"\bdon'?t (do|use|add|create|write|delete|remove|change)",
    r"\bnot what i (asked|meant|wanted|said)",
    r"\bi (already|just) (said|told|asked)",
    r"\bwhy (did you|are you|is it)\b.*\?",
    r"\bwrong\b",
    r"\bnot that\b",
    # Learned from session ca9272e6 (2026-04-03):
    r"\b(feels?|seems?) (arbitrary|wrong|off|unnecessary|forced|weird)\b",
    r"\bi think (we|you)'?re (underestimating|overestimating|missing|ignoring)",
    r"\bi think (both|all|neither)\b.{0,20}(need|want|should|important)",
    r"\bcan'?t we\b.{0,30}\binstead\b",
    r"\brather than\b.{0,30}\bwhy not\b",
]

SEED_PRAISE = [
    r"\b(excellent|brilliant|amazing|awesome|fantastic|wonderful)\b",
    r"\bthat'?s (exactly|precisely|perfect)",
    r"\bgreat (work|job)\b",
    r"\bwell done\b",
    r"\blove (it|this|that)\b",
]

SEED_APPROACH_CHANGE = [
    r"\bdifferent approach",
    r"\bchange (of |in )?direction",
    r"\bslight change",
    r"\bscrap (that|this)",
    r"\bstart over",
    r"\bon second thought",
    r"\bactually[,.]?\s+(let'?s|i think|i'?d)",
    # Learned from session ca9272e6 (2026-04-03):
    r"\bi think (it'?s|that'?s|this is) deeper",
    r"\byou'?re underestimating",
]


def load_patterns(project_dir: str) -> dict[str, list[re.Pattern]]:
    """Load seed patterns + any learned patterns from the project.

    Learned patterns live in .claude/<marketplace>/learnings/signals/patterns.json:
    {
        "correction": ["\\bfeels (arbitrary|wrong)\\b", ...],
        "praise": [...],
        "approach_change": [...],
        "not_correction": [...]
    }
    """
    learned = {"correction": [], "praise": [], "approach_change": [], "not_correction": []}

    patterns_file = _learnings_dir(project_dir) / "signals" / "patterns.json"
    if patterns_file.exists():
        try:
            with open(patterns_file) as f:
                data = json.load(f)
            for key in learned:
                for p in data.get(key, []):
                    try:
                        re.compile(p, re.IGNORECASE)  # Validate before using
                        learned[key].append(p)
                    except re.error:
                        pass  # Skip invalid patterns
        except (json.JSONDecodeError, OSError):
            pass

    # Combine seed + learned, compile
    return {
        "not_correction": [re.compile(p, re.IGNORECASE) for p in SEED_NOT_CORRECTION + learned["not_correction"]],
        "correction": [re.compile(p, re.IGNORECASE) for p in SEED_CORRECTION + learned["correction"]],
        "praise": [re.compile(p, re.IGNORECASE) for p in SEED_PRAISE + learned["praise"]],
        "approach_change": [re.compile(p, re.IGNORECASE) for p in SEED_APPROACH_CHANGE + learned["approach_change"]],
    }


def classify(prompt: str, patterns: dict[str, list[re.Pattern]]) -> dict | None:
    """Fast regex classification. Returns result or None if ambiguous."""
    if any(p.search(prompt) for p in patterns["not_correction"]):
        return None  # Clearly not interesting — don't record at all

    if any(p.search(prompt) for p in patterns["correction"]):
        return {"rating": 3, "type": "correction", "confidence": "regex"}

    if any(p.search(prompt) for p in patterns["praise"]):
        return {"rating": 9, "type": "praise", "confidence": "regex"}

    if any(p.search(prompt) for p in patterns["approach_change"]):
        return {"rating": 4, "type": "approach_change", "confidence": "regex"}

    # Ambiguous — queue for Claude to classify during retrospective
    if len(prompt) > 20:  # Skip very short messages
        return {"rating": 5, "type": "unclassified", "confidence": "needs_review"}

    return None


def _marketplace_name() -> str:
    """Derive marketplace name from CLAUDE_PLUGIN_ROOT, fall back to turtlestack."""
    plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT", "").rstrip("/")
    if plugin_root:
        # ~/.claude/plugins/cache/<marketplace>/<plugin>/<version>
        parts = plugin_root.split(os.sep)
        if len(parts) >= 3 and parts[-3] != "cache":
            return parts[-3]
    return "turtlestack"


def _learnings_dir(project_dir: str) -> Path:
    """Resolve the learnings directory, honouring LEARNINGS_DIR env override."""
    override = os.environ.get("LEARNINGS_DIR")
    if override:
        return Path(override)
    return Path(project_dir) / ".claude" / _marketplace_name() / "learnings"


def write_signal(signal: dict, project_dir: str):
    """Append a classified signal to the pending signals file."""
    signals_dir = _learnings_dir(project_dir) / "signals"
    signals_dir.mkdir(parents=True, exist_ok=True)

    signals_file = signals_dir / "pending.jsonl"
    with open(signals_file, "a") as f:
        f.write(json.dumps(signal) + "\n")


def main():
    # Read hook payload from stdin
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    prompt = payload.get("prompt", "").strip()
    session_id = payload.get("session_id", "")
    cwd = payload.get("cwd", os.getcwd())

    # Skip very short messages and commands
    if len(prompt) < 4 or prompt.startswith("/") or prompt.startswith("!"):
        sys.exit(0)

    # Skip system-generated messages (XML tags)
    if prompt.startswith("<") and ">" in prompt[:50]:
        sys.exit(0)

    # Load seed + learned patterns
    patterns = load_patterns(cwd)

    result = classify(prompt, patterns)

    if result is None:
        sys.exit(0)  # Not interesting or clearly positive — skip

    signal = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": session_id,
        "type": result["type"],
        "rating": result["rating"],
        "confidence": result["confidence"],
        "prompt_preview": prompt[:300],
    }
    write_signal(signal, cwd)


if __name__ == "__main__":
    main()
