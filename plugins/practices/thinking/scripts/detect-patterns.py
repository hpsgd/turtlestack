#!/usr/bin/env python3
"""Detect recurring patterns across session learnings.

Scans accumulated session analysis files from both project and global
learnings directories. Groups similar corrections by type and content,
flags patterns with 3+ instances, and writes pattern files.

Usage:
    python3 detect-patterns.py [--project-dir <path>] [--global-dir <path>] [--json]
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


def load_session_analyses(dirs: list[str]) -> list[dict]:
    """Load all session analysis JSON files from the given directories."""
    analyses = []
    for base_dir in dirs:
        sessions_dir = Path(base_dir) / "sessions"
        if not sessions_dir.exists():
            continue
        for f in sessions_dir.glob("*.json"):
            try:
                with open(f) as fh:
                    data = json.load(fh)
                if "events" in data:
                    analyses.append(data)
            except (json.JSONDecodeError, OSError):
                pass
    return analyses


def extract_corrections(analyses: list[dict]) -> list[dict]:
    """Extract all correction and approach_change events across sessions."""
    corrections = []
    for analysis in analyses:
        session_id = analysis.get("session_id", "unknown")
        analysed_at = analysis.get("analysed_at", "")
        for event in analysis.get("events", []):
            if event.get("type") in ("immediate_correction", "approach_change"):
                corrections.append({
                    "session_id": session_id,
                    "analysed_at": analysed_at,
                    "type": event["type"],
                    "severity": event.get("severity", "MEDIUM"),
                    "user_said": event.get("user_said", ""),
                    "assistant_said": event.get("assistant_said", ""),
                    "timestamp": event.get("timestamp", ""),
                })
    return corrections


def normalise_text(text: str) -> str:
    """Normalise text for similarity comparison."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def extract_keywords(text: str) -> set[str]:
    """Extract significant keywords from text (skip stop words)."""
    stop_words = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "can", "shall", "to", "of", "in", "for",
        "on", "with", "at", "by", "from", "as", "into", "through", "during",
        "before", "after", "above", "below", "between", "out", "off", "over",
        "under", "again", "further", "then", "once", "here", "there", "when",
        "where", "why", "how", "all", "each", "every", "both", "few", "more",
        "most", "other", "some", "such", "no", "nor", "not", "only", "own",
        "same", "so", "than", "too", "very", "just", "because", "but", "and",
        "or", "if", "that", "this", "it", "its", "i", "you", "we", "they",
        "me", "him", "her", "us", "them", "my", "your", "his",
    }
    words = set(normalise_text(text).split())
    return words - stop_words


def group_similar_corrections(corrections: list[dict]) -> dict[str, list[dict]]:
    """Group corrections by keyword overlap (simple similarity)."""
    groups = defaultdict(list)

    for correction in corrections:
        text = correction["user_said"]
        keywords = extract_keywords(text)

        if not keywords:
            groups["uncategorised"].append(correction)
            continue

        # Try to match to an existing group
        matched = False
        for group_key, group_items in groups.items():
            if group_key == "uncategorised":
                continue
            group_keywords = extract_keywords(group_items[0]["user_said"])
            overlap = keywords & group_keywords
            # If 30%+ keyword overlap, same group
            if len(overlap) >= max(2, len(keywords) * 0.3):
                groups[group_key].append(correction)
                matched = True
                break

        if not matched:
            # Create a new group keyed by the first 3 significant keywords
            sorted_kw = sorted(keywords)[:3]
            group_key = "-".join(sorted_kw) if sorted_kw else "misc"
            groups[group_key].append(correction)

    return dict(groups)


def detect_patterns(groups: dict[str, list[dict]], threshold: int = 3) -> list[dict]:
    """Identify groups that meet the pattern threshold."""
    patterns = []

    for group_key, items in groups.items():
        if len(items) < threshold:
            continue

        # Extract common thread
        all_keywords = set()
        for item in items:
            all_keywords |= extract_keywords(item["user_said"])

        # Find keywords that appear in most items
        keyword_freq = defaultdict(int)
        for item in items:
            for kw in extract_keywords(item["user_said"]):
                keyword_freq[kw] += 1

        common_keywords = [
            kw for kw, count in keyword_freq.items()
            if count >= len(items) * 0.5
        ]

        sessions = sorted(set(item["session_id"] for item in items))
        timestamps = [item["timestamp"] for item in items if item.get("timestamp")]

        pattern_id = f"pat-{group_key}"

        patterns.append({
            "pattern_id": pattern_id,
            "group_key": group_key,
            "count": len(items),
            "sessions": sessions,
            "first_seen": min(timestamps) if timestamps else "",
            "last_seen": max(timestamps) if timestamps else "",
            "common_keywords": common_keywords[:10],
            "description": f"Correction pattern ({len(items)} instances): {', '.join(common_keywords[:5])}",
            "instances": [
                {
                    "session_id": item["session_id"],
                    "user_said": item["user_said"][:200],
                    "timestamp": item["timestamp"],
                }
                for item in items
            ],
            "status": "detected",
        })

    return patterns


def load_existing_patterns(dirs: list[str]) -> dict[str, dict]:
    """Load existing pattern files."""
    existing = {}
    for base_dir in dirs:
        patterns_dir = Path(base_dir) / "patterns"
        if not patterns_dir.exists():
            continue
        for f in patterns_dir.glob("*.json"):
            try:
                with open(f) as fh:
                    data = json.load(fh)
                pid = data.get("pattern_id", f.stem)
                existing[pid] = data
            except (json.JSONDecodeError, OSError):
                pass
    return existing


def save_patterns(patterns: list[dict], dirs: list[str]):
    """Save new/updated patterns to all learnings directories."""
    for base_dir in dirs:
        patterns_dir = Path(base_dir) / "patterns"
        patterns_dir.mkdir(parents=True, exist_ok=True)

        for pattern in patterns:
            pid = pattern["pattern_id"]
            output_path = patterns_dir / f"{pid}.json"

            # Merge with existing if present
            if output_path.exists():
                try:
                    with open(output_path) as f:
                        existing = json.load(f)
                    # Keep the existing status if it's been progressed
                    if existing.get("status") in ("pending_review", "pr_submitted", "resolved"):
                        pattern["status"] = existing["status"]
                    # Merge instances (dedup by session_id + timestamp)
                    existing_keys = {
                        (i["session_id"], i.get("timestamp", ""))
                        for i in existing.get("instances", [])
                    }
                    for inst in pattern.get("instances", []):
                        key = (inst["session_id"], inst.get("timestamp", ""))
                        if key not in existing_keys:
                            existing.setdefault("instances", []).append(inst)
                    pattern["instances"] = existing.get("instances", pattern["instances"])
                    pattern["count"] = len(pattern["instances"])
                except (json.JSONDecodeError, OSError):
                    pass

            pattern["updated_at"] = datetime.now(timezone.utc).isoformat()

            with open(output_path, "w") as f:
                json.dump(pattern, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Detect recurring patterns in session learnings")
    parser.add_argument("--project-dir",
                        default=os.environ.get("LEARNINGS_DIR", ".claude/turtlestack/learnings"),
                        help="Project learnings directory (default: $LEARNINGS_DIR or .claude/turtlestack/learnings)")
    parser.add_argument("--global-dir",
                        default=os.environ.get("GLOBAL_LEARNINGS_DIR", os.path.expanduser("~/.claude/turtlestack/learnings")),
                        help="Global learnings directory (default: $GLOBAL_LEARNINGS_DIR or ~/.claude/turtlestack/learnings)")
    parser.add_argument("--threshold", type=int, default=3,
                        help="Minimum instances to qualify as a pattern")
    parser.add_argument("--json", action="store_true",
                        help="Output raw JSON to stdout")
    args = parser.parse_args()

    dirs = [d for d in [args.project_dir, args.global_dir] if os.path.isdir(d)]

    if not dirs:
        if args.json:
            print(json.dumps({"patterns": [], "message": "No learnings directories found"}))
        else:
            print("No learnings directories found.")
        sys.exit(0)

    # Load all session analyses
    analyses = load_session_analyses(dirs)
    if not analyses:
        if args.json:
            print(json.dumps({"patterns": [], "sessions_scanned": 0}))
        else:
            print("No session analyses found.")
        sys.exit(0)

    # Extract and group corrections
    corrections = extract_corrections(analyses)
    groups = group_similar_corrections(corrections)
    patterns = detect_patterns(groups, threshold=args.threshold)

    # Save patterns
    if patterns:
        save_patterns(patterns, dirs)

    # Output
    if args.json:
        print(json.dumps({
            "sessions_scanned": len(analyses),
            "total_corrections": len(corrections),
            "groups_found": len(groups),
            "patterns_detected": len(patterns),
            "patterns": patterns,
        }, indent=2))
    else:
        print(f"Sessions scanned: {len(analyses)}")
        print(f"Total corrections: {len(corrections)}")
        print(f"Groups found: {len(groups)}")
        print(f"Patterns detected (>={args.threshold} instances): {len(patterns)}")

        if patterns:
            print(f"\n--- Patterns ---")
            for p in patterns:
                print(f"\n[{p['pattern_id']}] {p['count']} instances across {len(p['sessions'])} sessions")
                print(f"  Keywords: {', '.join(p['common_keywords'][:5])}")
                print(f"  First: {p['first_seen'][:10] if p['first_seen'] else '?'}")
                print(f"  Last: {p['last_seen'][:10] if p['last_seen'] else '?'}")
                print(f"  Status: {p['status']}")
                for inst in p["instances"][:3]:
                    print(f"    - {inst['user_said'][:100]}")

        # Show groups below threshold
        below = {k: v for k, v in groups.items() if len(v) < args.threshold and len(v) >= 2}
        if below:
            print(f"\n--- Emerging (2 instances, watching) ---")
            for k, items in below.items():
                print(f"  [{k}] {len(items)} instances")


if __name__ == "__main__":
    main()
