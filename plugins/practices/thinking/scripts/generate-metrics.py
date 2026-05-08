#!/usr/bin/env python3
"""Aggregate session metrics into daily and summary reports.

Reads session analysis files and produces:
- Per-day metrics (corrections, successes, correction rate, tokens)
- Rolling averages (7-day, 30-day, all-time)
- Trend detection (improving, stable, declining)

Usage:
    python3 generate-metrics.py [--project-dir <path>] [--global-dir <path>] [--json]
"""

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


def load_session_analyses(dirs: list[str]) -> list[dict]:
    """Load all session analysis JSON files."""
    analyses = []
    for base_dir in dirs:
        sessions_dir = Path(base_dir) / "sessions"
        if not sessions_dir.exists():
            continue
        for f in sessions_dir.glob("*.json"):
            try:
                with open(f) as fh:
                    data = json.load(fh)
                if "metrics" in data:
                    analyses.append(data)
            except (json.JSONDecodeError, OSError):
                pass
    return analyses


def load_signals(dirs: list[str]) -> list[dict]:
    """Load all pending signals from JSONL files."""
    signals = []
    for base_dir in dirs:
        signals_file = Path(base_dir) / "signals" / "pending.jsonl"
        if not signals_file.exists():
            continue
        try:
            with open(signals_file) as f:
                for line in f:
                    line = line.strip()
                    if line:
                        signals.append(json.loads(line))
        except (json.JSONDecodeError, OSError):
            pass
    return signals


def extract_date(timestamp: str) -> str:
    """Extract YYYY-MM-DD from an ISO timestamp."""
    if not timestamp:
        return "unknown"
    try:
        return timestamp[:10]
    except (IndexError, TypeError):
        return "unknown"


def aggregate_daily(analyses: list[dict]) -> dict[str, dict]:
    """Aggregate metrics by day."""
    daily = defaultdict(lambda: {
        "sessions": 0,
        "duration_minutes": 0,
        "user_turns": 0,
        "assistant_turns": 0,
        "corrections_immediate": 0,
        "corrections_approach": 0,
        "corrections_reversals": 0,
        "corrections_total": 0,
        "successes": 0,
        "input_tokens": 0,
        "output_tokens": 0,
    })

    for analysis in analyses:
        date = extract_date(analysis.get("analysed_at", ""))
        m = analysis.get("metrics", {})
        c = m.get("corrections", {})
        t = m.get("tokens_used", {})

        d = daily[date]
        d["sessions"] += 1
        d["duration_minutes"] += m.get("duration_minutes", 0)
        d["user_turns"] += m.get("total_user_turns", 0)
        d["assistant_turns"] += m.get("total_assistant_turns", 0)
        d["corrections_immediate"] += c.get("immediate", 0)
        d["corrections_approach"] += c.get("approach_changes", 0)
        d["corrections_reversals"] += c.get("delayed_reversals", 0)
        d["corrections_total"] += c.get("total", 0)
        d["successes"] += m.get("successes", 0)
        d["input_tokens"] += t.get("input", 0)
        d["output_tokens"] += t.get("output", 0)

    return dict(daily)


def compute_rolling(daily: dict[str, dict], window: int) -> dict:
    """Compute rolling average over the most recent N days."""
    sorted_dates = sorted(daily.keys(), reverse=True)
    recent = sorted_dates[:window]

    if not recent:
        return {"window": window, "days_available": 0}

    totals = defaultdict(float)
    for date in recent:
        for key, val in daily[date].items():
            totals[key] += val

    n = len(recent)
    return {
        "window": window,
        "days_available": n,
        "avg_sessions_per_day": round(totals["sessions"] / n, 1),
        "avg_corrections_per_day": round(totals["corrections_total"] / n, 1),
        "avg_successes_per_day": round(totals["successes"] / n, 1),
        "avg_correction_rate": round(
            totals["corrections_total"] / max(totals["user_turns"], 1), 4
        ),
        "avg_duration_minutes": round(totals["duration_minutes"] / max(totals["sessions"], 1)),
        "total_tokens": {
            "input": int(totals["input_tokens"]),
            "output": int(totals["output_tokens"]),
        },
    }


def detect_trend(daily: dict[str, dict]) -> dict:
    """Detect whether correction rate is improving, stable, or declining."""
    sorted_dates = sorted(daily.keys())
    if len(sorted_dates) < 3:
        return {"trend": "insufficient_data", "days": len(sorted_dates)}

    # Compare first half vs second half
    mid = len(sorted_dates) // 2
    first_half = sorted_dates[:mid]
    second_half = sorted_dates[mid:]

    def avg_rate(dates):
        total_corrections = sum(daily[d]["corrections_total"] for d in dates)
        total_turns = sum(daily[d]["user_turns"] for d in dates)
        return total_corrections / max(total_turns, 1)

    rate_first = avg_rate(first_half)
    rate_second = avg_rate(second_half)

    if rate_second < rate_first * 0.8:
        trend = "improving"
    elif rate_second > rate_first * 1.2:
        trend = "declining"
    else:
        trend = "stable"

    return {
        "trend": trend,
        "first_half_rate": round(rate_first, 4),
        "second_half_rate": round(rate_second, 4),
        "change": round((rate_second - rate_first) / max(rate_first, 0.001), 2),
    }


def compute_signal_summary(signals: list[dict]) -> dict:
    """Summarise real-time signal classifications."""
    by_type = defaultdict(int)
    by_confidence = defaultdict(int)

    for s in signals:
        by_type[s.get("type", "unknown")] += 1
        by_confidence[s.get("confidence", "unknown")] += 1

    return {
        "total_signals": len(signals),
        "by_type": dict(by_type),
        "by_confidence": dict(by_confidence),
        "unclassified": by_type.get("unclassified", 0),
    }


def save_metrics(metrics: dict, dirs: list[str]):
    """Save metrics to all learnings directories."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    for base_dir in dirs:
        metrics_dir = Path(base_dir) / "metrics"
        metrics_dir.mkdir(parents=True, exist_ok=True)
        output_path = metrics_dir / f"{today}.json"
        with open(output_path, "w") as f:
            json.dump(metrics, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Generate learning metrics and trends")
    parser.add_argument("--project-dir",
                        default=os.environ.get("LEARNINGS_DIR", ".claude/turtlestack/learnings"),
                        help="Project learnings directory (default: $LEARNINGS_DIR or .claude/turtlestack/learnings)")
    parser.add_argument("--global-dir",
                        default=os.environ.get("GLOBAL_LEARNINGS_DIR", os.path.expanduser("~/.claude/turtlestack/learnings")),
                        help="Global learnings directory (default: $GLOBAL_LEARNINGS_DIR or ~/.claude/turtlestack/learnings)")
    parser.add_argument("--json", action="store_true",
                        help="Output raw JSON to stdout")
    args = parser.parse_args()

    dirs = [d for d in [args.project_dir, args.global_dir] if os.path.isdir(d)]

    if not dirs:
        if args.json:
            print(json.dumps({"error": "No learnings directories found"}))
        else:
            print("No learnings directories found.")
        sys.exit(0)

    analyses = load_session_analyses(dirs)
    signals = load_signals(dirs)
    daily = aggregate_daily(analyses)

    metrics = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sessions_total": len(analyses),
        "days_with_data": len(daily),
        "daily": {k: v for k, v in sorted(daily.items(), reverse=True)},
        "rolling_7d": compute_rolling(daily, 7),
        "rolling_30d": compute_rolling(daily, 30),
        "all_time": compute_rolling(daily, len(daily)),
        "trend": detect_trend(daily),
        "signals": compute_signal_summary(signals),
    }

    # Save to disk
    save_metrics(metrics, dirs)

    if args.json:
        print(json.dumps(metrics, indent=2))
    else:
        print(f"Sessions analysed: {len(analyses)}")
        print(f"Days with data: {len(daily)}")

        at = metrics["all_time"]
        if at.get("days_available", 0) > 0:
            print(f"\nAll-time averages:")
            print(f"  Sessions/day: {at['avg_sessions_per_day']}")
            print(f"  Corrections/day: {at['avg_corrections_per_day']}")
            print(f"  Successes/day: {at['avg_successes_per_day']}")
            print(f"  Correction rate: {at['avg_correction_rate']:.1%}")
            print(f"  Avg duration: {at['avg_duration_minutes']} min")

        t = metrics["trend"]
        if t["trend"] != "insufficient_data":
            direction = {"improving": "↓ improving", "declining": "↑ declining", "stable": "→ stable"}
            print(f"\nTrend: {direction.get(t['trend'], t['trend'])}")
            print(f"  First half correction rate: {t['first_half_rate']:.1%}")
            print(f"  Second half correction rate: {t['second_half_rate']:.1%}")
        else:
            print(f"\nTrend: insufficient data ({t['days']} days, need 3+)")

        s = metrics["signals"]
        if s["total_signals"] > 0:
            print(f"\nReal-time signals: {s['total_signals']} total")
            for stype, count in s["by_type"].items():
                print(f"  {stype}: {count}")
            if s["unclassified"] > 0:
                print(f"  ⚠ {s['unclassified']} unclassified (run /thinking:retrospective)")


if __name__ == "__main__":
    main()
