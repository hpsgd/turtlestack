---
description: "Hook design principles: structural checks, silent on pass, actionable on block"
---

# Hook Design

## Structural checks use hooks, not behavioral rules

If a check is structural (a file exists, a section is present, a keyword appears in the diff, a naming convention is followed), enforce it with a hook. Behavioral rules depend on the model remembering to apply them under cognitive load. They fail when the session is complex, the context is long, or the task is unfamiliar.

Hooks fire mechanically. They don't forget. They don't get distracted. If the check can be expressed as "does X exist / match / contain Y," write a hook.

Reserve behavioral rules for judgment calls: "is this the right approach," "should we split this PR," "does this naming make sense." Those require context a hook can't evaluate.

## Pick the hook type by check shape

Claude Code hooks come in several types. Choose by the shape of the check, not by habit:

| Type | What it is | Use for |
|---|---|---|
| `command` | Local script, no LLM | Structural checks — regex, file existence, arithmetic. Fast, deterministic, free. The default |
| `prompt` | Single-turn LLM evaluation of the event | A bounded judgment call on the event's content ("is this commit message conventional in spirit, not just format?") where regex false-positives too much |
| `agent` | Agentic verifier with Read/Grep/Glob (experimental) | A judgment call that needs to look beyond the event payload — cross-file consistency, "does this edit contradict the spec" |
| `http` / `mcp_tool` | Remote endpoint or MCP tool | Delegating the check to an existing external service |

`prompt` and `agent` hooks cost latency and tokens on every firing — a `command` hook that does the job is always preferable. Reach for them only when the check genuinely needs judgment AND matters enough to pay for on every matching event. Both existing marketplace hooks (security-baseline scan, result-verdict check) are structural and stay `command` deliberately.

Useful modifiers: `once: true` (skill-frontmatter hooks only) fires a hook once per session; `async: true` doesn't block the tool call; `asyncRewake` runs in the background and wakes Claude on exit code 2.

## Silent on pass, detailed on block

Hook output goes to `additionalContext` and is fed to the model on every turn. Verbose green-path output is a token tax paid on every interaction, measured across 30 sessions at a median of 7s hook time. The rule:

- **Pass:** print nothing, exit 0
- **Block:** print full actionable detail (what failed, what to fix, where to look), exit non-zero
- **Warn:** one short line maximum, exit 0

Never print "All checks passed!" or "Everything looks good." Silence is the signal that things are fine. Noise drowns out the messages that matter.
