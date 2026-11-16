# Hook test result: Hook test: install-rules warns instead of installing into a folder of repos

| Field | Value |
|---|---|
| Verdict | PASS |
| Checks | 3/3 |
| Hook | `/Users/martin/Projects/hps.gd/turtlestack/plugins/practices/thinking/scripts/install-rules.sh` |
| Hook exit | 0 |

## Assertions

| Result | Assertion | Evidence |
|---|---|---|
| PASS | exit 0 | actual exit 0 |
| PASS | file not exists: parent/.claude/rules | absent: /var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/hooktest-a17c048d-lfvniifi/parent/.claude/rules |
| PASS | stdout contains: contains git repos but is not one | present: 'contains git repos but is not one' |

## Captured stdout

```
install-rules: skipped /var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/hooktest-a17c048d-lfvniifi/parent: it contains git repos but is not one itself. Start the session inside a repo.
```
