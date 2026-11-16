# Hook test result: Hook test: install-rules still upgrades older rules

| Field | Value |
|---|---|
| Verdict | PASS |
| Checks | 4/4 |
| Hook | `/Users/martin/Projects/hps.gd/turtlestack/plugins/practices/thinking/scripts/install-rules.sh` |
| Hook exit | 0 |

## Assertions

| Result | Assertion | Evidence |
|---|---|---|
| PASS | exit 0 | actual exit 0 |
| PASS | file contains: rules/mp--alpha--4.0.0--style.md :: New 4.0.0 rule body. | found in /var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/hooktest-7b60876f-1qn3bery/rules/mp--alpha--4.0.0--style.md: 'New 4.0.0 rule body.' |
| PASS | file not exists: rules/mp--alpha--3.7.1--style.md | absent: /var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/hooktest-7b60876f-1qn3bery/rules/mp--alpha--3.7.1--style.md |
| PASS | stdout contains: Installed 1 new/updated rules | present: 'Installed 1 new/updated rules' |

## Captured stdout

```
<learning-context>
Installed 1 new/updated rules from 1 plugins (mp)
Removed 1 stale rules
</learning-context>
```
