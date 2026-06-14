# Hook test result: Hook test: install-rules delivers the multi-instance rule

| Field | Value |
|---|---|
| Verdict | PASS |
| Checks | 4/4 |
| Hook | `/Users/martin/Projects/turtlestack/plugins/practices/thinking/scripts/install-rules.sh` |
| Hook exit | 0 |

## Assertions

| Result | Assertion | Evidence |
|---|---|---|
| PASS | exit 0 | actual exit 0 |
| PASS | file exists: rules/turtlestack--thinking--9.9.9--multi-instance-dispatch.md | exists: /var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/hooktest-060a2c8d-1dt35s9a/rules/turtlestack--thinking--9.9.9--multi-instance-dispatch.md |
| PASS | file contains: rules/turtlestack--thinking--9.9.9--multi-instance-dispatch.md :: When you dispatch multiple instances | found in /var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/hooktest-060a2c8d-1dt35s9a/rules/turtlestack--thinking--9.9.9--multi-instance-dispatch.md: 'When you dispatch multiple instances' |
| PASS | file contains: rules/turtlestack--thinking--9.9.9--multi-instance-dispatch.md :: When you are a dispatched instance | found in /var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/hooktest-060a2c8d-1dt35s9a/rules/turtlestack--thinking--9.9.9--multi-instance-dispatch.md: 'When you are a dispatched instance' |

## Captured stdout

```
<learning-context>
Installed 4 new/updated rules from 1 plugins (turtlestack)
</learning-context>
```
