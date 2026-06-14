# Hook test result: Hook test: flags a hardcoded AWS access key

| Field | Value |
|---|---|
| Verdict | PASS |
| Checks | 4/4 |
| Hook | `/Users/martin/Projects/turtlestack/plugins/practices/security-compliance/scripts/security-baseline-hook.sh` |
| Hook exit | 0 |

## Assertions

| Result | Assertion | Evidence |
|---|---|---|
| PASS | exit 0 | actual exit 0 |
| PASS | stdout contains: aws-access-key | present: 'aws-access-key' |
| PASS | stdout contains: PreToolUse | present: 'PreToolUse' |
| PASS | stdout contains: security-baseline-findings | present: 'security-baseline-findings' |

## Captured stdout

```
{"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": "<security-baseline-findings>\n[high] aws-access-key (security-baseline.md:L26): Hardcoded AWS access key id. Use an env var or a secrets manager.\n</security-baseline-findings>"}, "systemMessage": "\u26a0 1 security finding(s): aws-access-key"}
```
