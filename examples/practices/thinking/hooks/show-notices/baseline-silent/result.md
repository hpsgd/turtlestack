# Hook test result: Hook test: baseline mode seeds the marker silently

| Field | Value |
|---|---|
| Verdict | PASS |
| Checks | 4/4 |
| Hook | `/Users/martin/Projects/turtlestack/plugins/practices/thinking/scripts/show-notices.sh` |
| Hook exit | 0 |

## Assertions

| Result | Assertion | Evidence |
|---|---|---|
| PASS | exit 0 | actual exit 0 |
| PASS | stdout empty | stdout empty |
| PASS | file exists: config/turtlestack/notices-seen.json | exists: /var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/hooktest-5b5fc960-nwm1pqkf/config/turtlestack/notices-seen.json |
| PASS | file contains: config/turtlestack/notices-seen.json :: test-action | found in /var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/hooktest-5b5fc960-nwm1pqkf/config/turtlestack/notices-seen.json: 'test-action' |

## Captured stdout

```
(empty)
```
