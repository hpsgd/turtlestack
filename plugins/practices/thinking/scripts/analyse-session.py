#!/usr/bin/env python3
"""Analyse a Claude Code session transcript (JSONL) for learnings.

Extracts corrections, reversals, approach changes, and successes from
the conversation transcript. Outputs structured JSON for the
retrospective skill to interpret.

Usage:
    python3 analyse-session.py <transcript.jsonl> [--project-dir <path>] [--global-dir <path>]
"""

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

# --- Seed patterns (hardcoded baseline) ---
# The retrospective skill adds learned patterns to
# .claude/<marketplace>/learnings/signals/patterns.json at runtime.

SEED_CORRECTION = [
    # Explicit rejection
    r"\bno[,.]?\s+(not |don't |that's not |wrong)",
    r"^no[,.\s-]",
    r"\bthat's not (right|correct|what i)",
    r"\bwrong\b",
    r"\bstop\b.*(doing|that)",
    r"\bdon'?t\s+(do|use|add|create|write|generate|suggest)",
    # Redirection
    r"\binstead[,.]?\s",
    r"\bactually[,.]?\s",
    r"\brather\b",
    r"\bi('d| would) prefer",
    r"\blet'?s (try|do|go with|use|take)",
    r"\bnot that",
    r"\bnot what i (asked|meant|wanted)",
    # Frustration / repetition
    r"\bi (already|just) (said|told|asked|mentioned)",
    r"\bas i said",
    r"\bagain[,:]",
    # Learned from session ca9272e6 (2026-04-03):
    r"\b(feels?|seems?) (arbitrary|wrong|off|unnecessary|forced|weird)\b",
    r"\bi think (we|you)'?re (underestimating|overestimating|missing|ignoring)",
    r"\bi think (both|all|neither)\b.{0,20}(need|want|should|important)",
]

SEED_APPROACH_CHANGE = [
    r"\bdifferent approach",
    r"\bchange (of |in )?direction",
    r"\bslight change",
    r"\bpivot\b",
    r"\bscrap (that|this)",
    r"\bstart over",
    r"\bforget (that|what i said)",
    r"\bon second thought",
    # Learned from session ca9272e6 (2026-04-03):
    r"\bi think (it'?s|that'?s|this is) deeper",
    r"\byou'?re underestimating",
]

SEED_ACCEPTANCE = [
    r"^(ok|okay|good|great|perfect|nice|done|thanks|yep|yes|y|lgtm|ship it)",
    r"\bthat('s| is) (good|great|perfect|right|correct|fine|exactly)",
    r"\bkeep going",
    r"\blet'?s (commit|continue|move on|proceed)",
    r"\bnext\b",
]


def load_analysis_patterns(project_dir: str | None) -> dict[str, list[re.Pattern]]:
    """Load seed patterns + any learned patterns from the project.

    Learned patterns live at .claude/<marketplace>/learnings/signals/patterns.json
    (written by the retrospective skill). The marketplace segment is globbed so
    the script stays marketplace-agnostic; $LEARNINGS_DIR overrides for tests.
    """
    learned = {"correction": [], "approach_change": [], "acceptance": []}

    candidates: list[Path] = []
    env_dir = os.environ.get("LEARNINGS_DIR")
    if env_dir:
        candidates.append(Path(env_dir) / "signals" / "patterns.json")
    if project_dir:
        candidates.extend(sorted(Path(project_dir).glob(".claude/*/learnings/signals/patterns.json")))

    for patterns_file in candidates:
        if patterns_file.exists():
            try:
                with open(patterns_file) as f:
                    data = json.load(f)
                for key in learned:
                    for p in data.get(key, []):
                        try:
                            re.compile(p, re.IGNORECASE)
                            learned[key].append(p)
                        except re.error:
                            pass
            except (json.JSONDecodeError, OSError):
                pass

    return {
        "correction": [re.compile(p, re.IGNORECASE) for p in SEED_CORRECTION + learned["correction"]],
        "approach_change": [re.compile(p, re.IGNORECASE) for p in SEED_APPROACH_CHANGE + learned["approach_change"]],
        "acceptance": [re.compile(p, re.IGNORECASE) for p in SEED_ACCEPTANCE + learned["acceptance"]],
    }


def parse_jsonl(path: str) -> list[dict]:
    """Parse JSONL file, skipping malformed lines."""
    entries = []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass  # Skip malformed lines
    return entries


def extract_conversation_turns(entries: list[dict]) -> list[dict]:
    """Extract user/assistant message pairs in chronological order."""
    turns = []
    for entry in entries:
        entry_type = entry.get("type")
        if entry_type not in ("user", "assistant"):
            continue

        msg = entry.get("message", {})
        content = msg.get("content", "")
        is_meta = entry.get("isMeta", False)

        # Skip meta messages (system injections, skill preambles)
        if is_meta and entry_type == "user":
            continue

        # Extract text content
        text = ""
        if isinstance(content, str):
            text = content
        elif isinstance(content, list):
            has_tool_result = False
            for block in content:
                if isinstance(block, dict):
                    if block.get("type") == "text":
                        text += block.get("text", "") + "\n"
                    elif block.get("type") == "tool_result":
                        has_tool_result = True
                        # Tool results are not user speech — skip
            # If the message is ONLY tool results with no text, skip entirely
            if has_tool_result and not text.strip():
                continue

        # Skip empty messages
        text = text.strip()
        if not text:
            continue

        # Strip XML tags from user messages (command wrappers, caveats)
        if entry_type == "user":
            clean = re.sub(r"<[^>]+>", " ", text).strip()
            clean = re.sub(r"\s+", " ", clean)
            if not clean or len(clean) < 3:
                continue
            # Skip messages that look like tool output, file paths, or IDs
            if re.match(r"^(toolu_|/private/|/tmp/|/Users/|[a-f0-9]{8,})", clean):
                continue
            # Skip messages that are mostly non-word characters (JSON, paths)
            word_chars = len(re.findall(r"[a-zA-Z]", clean))
            if word_chars < len(clean) * 0.4:
                continue
            text = clean

        turns.append({
            "type": entry_type,
            "text": text[:2000],  # Truncate very long messages
            "uuid": entry.get("uuid", ""),
            "timestamp": entry.get("timestamp", ""),
            "parent_uuid": entry.get("parentUuid", ""),
        })

    return turns


def extract_tool_uses(entries: list[dict]) -> list[dict]:
    """Extract all tool use events."""
    tool_uses = []
    for entry in entries:
        if entry.get("type") != "assistant":
            continue
        msg = entry.get("message", {})
        content = msg.get("content", [])
        if not isinstance(content, list):
            continue
        for block in content:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                tool_uses.append({
                    "name": block.get("name", ""),
                    "input": block.get("input", {}),
                    "timestamp": entry.get("timestamp", ""),
                    "uuid": entry.get("uuid", ""),
                })
    return tool_uses


def extract_file_modifications(tool_uses: list[dict]) -> dict[str, list[dict]]:
    """Track which files were modified and when."""
    file_mods = defaultdict(list)
    for tu in tool_uses:
        name = tu["name"]
        inp = tu.get("input", {})
        path = None

        if name in ("Write", "Edit"):
            path = inp.get("file_path", "")
        elif name == "Bash":
            # Detect git add, mv, rm in bash commands
            cmd = inp.get("command", "")
            if ">" in cmd or "mv " in cmd or "rm " in cmd:
                # Too noisy to parse reliably — skip
                pass

        if path:
            file_mods[path].append({
                "tool": name,
                "timestamp": tu["timestamp"],
                "uuid": tu["uuid"],
            })

    return dict(file_mods)


def detect_corrections(turns: list[dict], patterns: dict[str, list[re.Pattern]]) -> list[dict]:
    """Find user messages that correct the assistant."""
    corrections = []

    for i, turn in enumerate(turns):
        if turn["type"] != "user":
            continue

        text = turn["text"]

        # Find the preceding assistant message
        prev_assistant = None
        for j in range(i - 1, -1, -1):
            if turns[j]["type"] == "assistant":
                prev_assistant = turns[j]
                break

        if not prev_assistant:
            continue

        # Check for correction signals
        is_correction = any(p.search(text) for p in patterns["correction"])
        is_approach_change = any(p.search(text) for p in patterns["approach_change"])

        if is_correction:
            corrections.append({
                "type": "immediate_correction",
                "severity": "HIGH",
                "user_said": text[:500],
                "assistant_said": prev_assistant["text"][:500],
                "user_uuid": turn["uuid"],
                "assistant_uuid": prev_assistant["uuid"],
                "timestamp": turn["timestamp"],
            })
        elif is_approach_change:
            corrections.append({
                "type": "approach_change",
                "severity": "MEDIUM",
                "user_said": text[:500],
                "assistant_said": prev_assistant["text"][:500],
                "user_uuid": turn["uuid"],
                "assistant_uuid": prev_assistant["uuid"],
                "timestamp": turn["timestamp"],
            })

    return corrections


def detect_file_reversals(file_mods: dict[str, list[dict]]) -> list[dict]:
    """Find files modified 3+ times (potential reversals)."""
    reversals = []
    for path, mods in file_mods.items():
        if len(mods) >= 3:
            reversals.append({
                "type": "delayed_reversal",
                "severity": "MEDIUM",
                "file_path": path,
                "modification_count": len(mods),
                "first_modified": mods[0]["timestamp"],
                "last_modified": mods[-1]["timestamp"],
                "timestamps": [m["timestamp"] for m in mods],
            })
    return reversals


def detect_successes(turns: list[dict], self_patterns: dict[str, list[re.Pattern]]) -> list[dict]:
    """Find assistant work that was accepted without correction."""
    successes = []
    seen_user_uuids = set()
    i = 0
    while i < len(turns):
        if turns[i]["type"] != "assistant":
            i += 1
            continue

        # Look for user acceptance after assistant message
        assistant_turn = turns[i]
        for j in range(i + 1, min(i + 3, len(turns))):
            if turns[j]["type"] == "user":
                user_uuid = turns[j]["uuid"]
                if user_uuid in seen_user_uuids:
                    break
                text = turns[j]["text"]
                is_accepted = any(p.search(text) for p in self_patterns["acceptance"])
                is_correction = any(p.search(text) for p in self_patterns["correction"])

                if is_accepted and not is_correction:
                    seen_user_uuids.add(user_uuid)
                    successes.append({
                        "type": "success",
                        "severity": "POSITIVE",
                        "assistant_said": assistant_turn["text"][:500],
                        "user_said": text[:200],
                        "timestamp": turns[j]["timestamp"],
                    })
                break
        i += 1

    return successes


def compute_metrics(entries: list[dict], turns: list[dict],
                    corrections: list[dict], reversals: list[dict],
                    successes: list[dict]) -> dict:
    """Compute session-level metrics."""
    user_turns = [t for t in turns if t["type"] == "user"]
    assistant_turns = [t for t in turns if t["type"] == "assistant"]

    # Extract token usage from assistant messages
    total_input_tokens = 0
    total_output_tokens = 0
    for entry in entries:
        if entry.get("type") == "assistant":
            usage = entry.get("message", {}).get("usage", {})
            total_input_tokens += usage.get("input_tokens", 0)
            total_output_tokens += usage.get("output_tokens", 0)

    # Session duration
    timestamps = [e.get("timestamp", "") for e in entries if e.get("timestamp")]
    duration_minutes = 0
    if len(timestamps) >= 2:
        try:
            start = datetime.fromisoformat(timestamps[0].replace("Z", "+00:00"))
            end = datetime.fromisoformat(timestamps[-1].replace("Z", "+00:00"))
            duration_minutes = int((end - start).total_seconds() / 60)
        except (ValueError, TypeError):
            pass

    immediate = sum(1 for c in corrections if c["type"] == "immediate_correction")
    approach = sum(1 for c in corrections if c["type"] == "approach_change")
    total_corrections = immediate + approach + len(reversals)
    total_interactions = len(user_turns)
    correction_rate = total_corrections / max(total_interactions, 1)

    return {
        "duration_minutes": duration_minutes,
        "total_user_turns": len(user_turns),
        "total_assistant_turns": len(assistant_turns),
        "corrections": {
            "immediate": immediate,
            "approach_changes": approach,
            "delayed_reversals": len(reversals),
            "total": total_corrections,
        },
        "successes": len(successes),
        "correction_rate": round(correction_rate, 4),
        "tokens_used": {
            "input": total_input_tokens,
            "output": total_output_tokens,
        },
    }


def analyse_session(jsonl_path: str, project_dir: str | None = None) -> dict:
    """Main analysis function."""
    entries = parse_jsonl(jsonl_path)
    if not entries:
        return {"error": "No entries found in transcript"}

    # Load seed + learned patterns
    # Infer project dir from the transcript's cwd if not provided
    if not project_dir:
        for entry in entries:
            cwd = entry.get("cwd")
            if cwd:
                project_dir = cwd
                break

    patterns = load_analysis_patterns(project_dir)

    # Extract session metadata
    session_id = None
    for entry in entries:
        sid = entry.get("sessionId")
        if sid:
            session_id = sid
            break

    turns = extract_conversation_turns(entries)
    tool_uses = extract_tool_uses(entries)
    file_mods = extract_file_modifications(tool_uses)

    corrections = detect_corrections(turns, patterns)
    reversals = detect_file_reversals(file_mods)
    successes = detect_successes(turns, patterns)
    metrics = compute_metrics(entries, turns, corrections, reversals, successes)

    # Combine all events
    events = corrections + reversals + successes

    return {
        "session_id": session_id,
        "jsonl_path": jsonl_path,
        "analysed_at": datetime.now(timezone.utc).isoformat(),
        "metrics": metrics,
        "events": events,
        "files_modified": {
            path: len(mods) for path, mods in file_mods.items()
        },
    }


def save_results(results: dict, project_dir: str | None, global_dir: str | None):
    """Save analysis results to project and/or global learnings directories."""
    session_id = results.get("session_id", "unknown")

    for base_dir in [project_dir, global_dir]:
        if not base_dir:
            continue

        sessions_dir = Path(base_dir) / "sessions"
        sessions_dir.mkdir(parents=True, exist_ok=True)

        output_path = sessions_dir / f"{session_id}.json"

        # Don't overwrite existing analysis
        if output_path.exists():
            continue

        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)

    # Update manifest
    for base_dir in [project_dir, global_dir]:
        if not base_dir:
            continue

        manifest_path = Path(base_dir) / "manifest.json"
        manifest = {}
        if manifest_path.exists():
            with open(manifest_path) as f:
                manifest = json.load(f)

        if "analysed_sessions" not in manifest:
            manifest["analysed_sessions"] = {}

        manifest["analysed_sessions"][session_id] = {
            "analysed_at": results["analysed_at"],
            "correction_count": results["metrics"]["corrections"]["total"],
            "success_count": results["metrics"]["successes"],
        }

        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Analyse a Claude Code session transcript")
    parser.add_argument("jsonl_path", help="Path to the session JSONL file")
    parser.add_argument("--project-dir",
                        default=os.environ.get("LEARNINGS_DIR"),
                        help="Project learnings directory (default: $LEARNINGS_DIR or .claude/turtlestack/learnings/)")
    parser.add_argument("--global-dir",
                        default=os.environ.get("GLOBAL_LEARNINGS_DIR"),
                        help="Global learnings directory (default: $GLOBAL_LEARNINGS_DIR or ~/.claude/turtlestack/learnings/)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON to stdout")
    args = parser.parse_args()

    if not os.path.exists(args.jsonl_path):
        print(json.dumps({"error": f"File not found: {args.jsonl_path}"}))
        sys.exit(1)

    results = analyse_session(args.jsonl_path)

    if args.project_dir or args.global_dir:
        save_results(results, args.project_dir, args.global_dir)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        # Human-readable summary
        m = results["metrics"]
        print(f"Session: {results['session_id']}")
        print(f"Duration: {m['duration_minutes']} minutes")
        print(f"Turns: {m['total_user_turns']} user, {m['total_assistant_turns']} assistant")
        print(f"Corrections: {m['corrections']['immediate']} immediate, "
              f"{m['corrections']['approach_changes']} approach changes, "
              f"{m['corrections']['delayed_reversals']} reversals")
        print(f"Successes: {m['successes']}")
        print(f"Correction rate: {m['correction_rate']:.1%}")
        print(f"Files modified: {len(results['files_modified'])}")
        print(f"Tokens: {m['tokens_used']['input']:,} in / {m['tokens_used']['output']:,} out")

        if results["events"]:
            print(f"\n--- Events ({len(results['events'])}) ---")
            for event in results["events"]:
                etype = event["type"]
                severity = event.get("severity", "")
                if etype in ("immediate_correction", "approach_change"):
                    print(f"\n[{severity}] {etype}")
                    print(f"  User: {event['user_said'][:120]}")
                elif etype == "delayed_reversal":
                    print(f"\n[{severity}] {etype}: {event['file_path']} "
                          f"({event['modification_count']} modifications)")
                elif etype == "success":
                    print(f"\n[{severity}] {etype}")
                    print(f"  User: {event['user_said'][:120]}")


if __name__ == "__main__":
    main()
