# Test: health-check full project setup audit

Scenario: A developer starts getting Claude Code's "instruction files add up to more than the 150k-char limit" warning and runs a health check to see what is loading, what is duplicated, and what else in the setup needs attention.

## Prompt

/health-check

Treat the following as the actual filesystem state for this health-check (the workspace is sandboxed; substitute these values for the real Glob/ls/wc results):

```
CLAUDE_CONFIG_DIR                                 → ~/.claude-work
~/.claude-work/rules/                             → 20 files, 40,000 chars (all learned--*.md)
~/.claude/rules/                                  → 20 files, 40,000 chars, byte-identical to ~/.claude-work/rules/ (loaded as an ANCESTOR of the project, which lives under ~)
.claude/rules/                                    → 25 files: 22 marketplace (turtlestack--*), 3 learned; 95,000 chars always-on, plus 4 path-scoped files (paths: frontmatter) totalling 12,000 chars
  largest: turtlestack--writing-style--3.7.1--tone-and-voice.md 38,000 chars; turtlestack--coding-standards--3.7.1--ai-steering.md 9,000 chars
CLAUDE.md (project root)                          → present, 5,000 chars
~/.claude-work/settings.json                      → no claudeMdExcludes key
.claude/settings.json                             → ABSENT
.claude/settings.local.json                       → ABSENT
~/.claude-work/projects/-<hash>/memory/           → 14 files (MEMORY.md index + 6 feedback, 5 project, 2 reference); newest 2 days ago; 1 references src/legacy/auth.ts, which no longer exists
Enabled plugins                                   → 8 plugins enabled including thinking
```

A few specifics for the response:

- **Instruction budget first**: compute the always-on total (180,000 chars: 40k + 40k + 95k + 5k), state it against the 150,000 limit, and exclude the 4 path-scoped files from the total.
- **Duplicate load**: identify that `~/.claude/rules/` duplicates `~/.claude-work/rules/` because the project sits under `~`, and name `claudeMdExcludes` in `~/.claude-work/settings.json` as the fix.
- **Two-bucket rule reporting**: marketplace and learned rules reported separately, global and project separately.
- **Memory**: report counts by type and freshness, and flag the stale reference to `src/legacy/auth.ts` without quoting memory contents.

## Criteria

- [ ] PASS: Skill measures the instruction budget with tool calls (wc / ls), not assumptions
- [ ] PASS: Reported always-on total excludes path-scoped rule files
- [ ] PASS: The `~/.claude/rules/` duplicate is identified as an ancestor-directory load, with `claudeMdExcludes` as the fix
- [ ] PASS: Report distinguishes marketplace rules from learned rules with counts for each
- [ ] PASS: Each section reports what IS found; recommendations go in a separate section
- [ ] PASS: Missing project-level settings.json is reported as "none found" — section is not skipped
- [ ] PASS: Report uses the defined output format with a summary header then per-section details
- [ ] PARTIAL: Recommendations name the largest always-on files as candidates to move into skills

## Output expectations

- [ ] PASS: Summary header states the instruction budget as a number against 150,000 (180,000 / 150,000, over by 30,000)
- [ ] PASS: Output names `tone-and-voice` (38,000 chars) as the largest always-on file
- [ ] PASS: Output says removing the duplicate load alone brings the total to 140,000, under the limit
- [ ] PASS: Output reports memory as 14 files with the per-type breakdown and flags the stale `src/legacy/auth.ts` reference
- [ ] PASS: Output reports CLAUDE.md as PRESENT and project-level `settings.json` as ABSENT
- [ ] PASS: Recommendations are specific actions tied to findings (e.g. "add `claudeMdExcludes: [\"~/.claude/rules/**\"]` to `~/.claude-work/settings.json`") — not "consider reviewing"
- [ ] PARTIAL: Output notes that the thinking plugin (the rule installer) is enabled
