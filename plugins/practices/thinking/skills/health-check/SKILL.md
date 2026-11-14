---
name: health-check
description: "Generate a health report of the current project's Claude Code setup — the always-on instruction budget, installed rules, enabled plugins, CLAUDE.md coverage and memory state."
argument-hint: "[optional: specific area to check, e.g. 'budget', 'rules', 'memory']"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

Generate a health report for the current project's Claude Code setup. If $ARGUMENTS specifies an area, focus on that; otherwise report on everything.

## What to Check

### 1. Instruction budget

Claude Code warns when always-on instruction files (every CLAUDE.md and every `rules/*.md` without a `paths:` scope) add up to more than 150,000 characters. Over that, adherence drops and every session pays the cost. Measure it:

```bash
CONFIG_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
# Candidate sources: user config, every ancestor directory's .claude/ and CLAUDE.md, the project
{
  ls "$CONFIG_DIR"/CLAUDE.md "$CONFIG_DIR"/rules/*.md 2>/dev/null
  d="$PWD"; while [ "$d" != "/" ]; do
    ls "$d"/CLAUDE.md "$d"/CLAUDE.local.md "$d"/.claude/CLAUDE.md "$d"/.claude/rules/*.md 2>/dev/null
    d=$(dirname "$d")
  done
} | sort -u | while read -r f; do
  grep -q '^paths:' "$f" && continue      # path-scoped: loads only when matching files are touched
  printf '%8d %s\n' "$(wc -c < "$f")" "$f"
done | sort -rn > /tmp/instruction-budget.txt
awk '{t+=$1} END {printf "TOTAL %d chars across %d files (limit 150000)\n", t, NR}' /tmp/instruction-budget.txt
head -10 /tmp/instruction-budget.txt
```

Then check:
- **Duplicates.** The same file content loaded from two paths (`cmp`), most often a second Claude config dir picked up as an *ancestor* of the project (e.g. `~/.claude/rules/` while `CLAUDE_CONFIG_DIR` points elsewhere). The fix is `claudeMdExcludes` in that profile's `settings.json`.
- **Exclusions.** Subtract anything matched by `claudeMdExcludes` in the settings files. The total above is an upper bound until you do.
- **The biggest files.** Anything over ~5k that only matters for some work is a candidate to become a skill.

Report: total vs limit, headroom, the top five files, duplicates found.

### 2. Installed Rules

Scan **both** global and project-level rules:

```bash
CONFIG_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
ls -la "$CONFIG_DIR"/rules/ 2>/dev/null   # global (all projects)
ls -la .claude/rules/ 2>/dev/null          # project
```

Check global (`$CLAUDE_CONFIG_DIR/rules/`, default `~/.claude/rules/`) **first**, then project-level (`.claude/rules/`). For each rule file:
- Which plugin installed it (from the namespace prefix, e.g., `coding-standards--`)
- Whether it's a learned rule (`learned--` prefix)
- When it was last updated (file modification time)
- Whether the source rule in the plugin is newer than the installed copy

Report: total count, breakdown by source (marketplace vs learned), global vs project-level, any stale copies.

### 3. Project Configuration

Check `.claude/settings.json` and `.claude/settings.local.json`:
- Which plugins are enabled
- Any custom permissions
- Any hooks configured
- MCP servers

Report: enabled plugins, custom configuration.

### 4. CLAUDE.md Coverage

Check for project documentation:
- Root `CLAUDE.md` or `.claude/CLAUDE.md` — does it exist? How comprehensive?
- `.claude/rules/` — any project-specific (non-marketplace) rules?
- Sub-project CLAUDE.md files — are workspaces documented?

Report: documentation coverage, gaps.

### 5. Memory Health

Check the native auto memory directory (`$CLAUDE_CONFIG_DIR/projects/-<project-path-hash>/memory/`, with `MEMORY.md` as its index):
- Total memory files
- Memory types (user, feedback, project, reference)
- Most recent memory (is the system actively learning?)
- Any stale memories (referenced files that no longer exist)

Report: memory count by type, freshness.

## Output Format

```
## Project Health Report

### Summary
- Instruction budget: X / 150,000 chars (Y files, Z duplicates)
- Rules: X installed (Y from marketplace, Z project-specific)
- Plugins: X enabled
- Documentation: [good/gaps identified]
- Memory: X files (Y feedback, Z project decisions)

### Details
[per-section details as above]

### Recommendations
[specific actions to improve coverage]
```

## Anti-Patterns

See Rules below — health-check is diagnostic, not procedural, so anti-patterns are expressed as rules rather than a separate list.

## Rules

- **Check, don't assume.** Every health-check item must be verified with a tool call (ls, grep, read). Do not report based on memory of what was installed.
- **Report what IS, not what SHOULD BE.** A health check describes current state. Recommendations go in a separate section, not mixed with findings.
- **Never fabricate coverage.** If a section has no data (e.g., no memory directory exists), report "none found" — do not skip the section.
- **Staleness is a finding.** A rule installed 6 months ago with no updates is worth flagging. A memory referencing a deleted file is worth flagging.
- **Quantify everything.** "Some rules installed" is not a finding. "7 rules installed (5 from marketplace, 2 project-specific, 1 stale)" is.
- **Privacy-aware.** Memory files may contain user preferences or feedback. Report counts and types, not contents, unless the user asks for detail.

## Related Skills

- `/thinking:reconcile-rules` — removes learned rules the marketplace now covers. Run it when the budget is tight.
- `/thinking:retrospective` — writes learned rules; it checks the budget before adding one.
