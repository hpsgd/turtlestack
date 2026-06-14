# Hook test result: Hook test: shows unseen notices on first run (show mode)

| Field | Value |
|---|---|
| Verdict | PASS |
| Checks | 6/6 |
| Hook | `/Users/martin/Projects/turtlestack/plugins/practices/thinking/scripts/show-notices.sh` |
| Hook exit | 0 |

## Assertions

| Result | Assertion | Evidence |
|---|---|---|
| PASS | exit 0 | actual exit 0 |
| PASS | stdout contains: SessionStart | present: 'SessionStart' |
| PASS | stdout contains: Breaking change to rule install | present: 'Breaking change to rule install' |
| PASS | stdout contains: Action needed on config | present: 'Action needed on config' |
| PASS | file exists: config/turtlestack/notices-seen.json | exists: /var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/hooktest-974b3b04-a89q146b/config/turtlestack/notices-seen.json |
| PASS | file contains: config/turtlestack/notices-seen.json :: test-action | found in /var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/hooktest-974b3b04-a89q146b/config/turtlestack/notices-seen.json: 'test-action' |

## Captured stdout

```
{"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "<turtlestack-notices>\nChange notices for this marketplace. Help the user action each one:\n- [breaking] (9.9.9) Breaking change to rule install: Re-run bootstrap to pick up the new path.\n- [action] (9.9.9) Action needed on config: Add the new key to settings.json.\n</turtlestack-notices>"}, "systemMessage": "\u26d4 Breaking change to rule install\n\u26a0 Action needed on config"}
```
