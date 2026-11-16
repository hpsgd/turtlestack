# Hook test result: Hook test: install-rules keeps newer rules installed by another profile

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
| PASS | file contains: rules/mp--alpha--4.0.0--style.md :: New 4.0.0 rule body. | found in /var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/hooktest-4f35982c-yojm9fxn/rules/mp--alpha--4.0.0--style.md: 'New 4.0.0 rule body.' |
| PASS | file not exists: rules/mp--alpha--3.7.1--style.md | absent: /var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/hooktest-4f35982c-yojm9fxn/rules/mp--alpha--3.7.1--style.md |
| PASS | stdout contains: kept mp 4.0.0 rules | present: 'kept mp 4.0.0 rules' |

## Captured stdout

```
install-rules: kept mp 4.0.0 rules; this profile's plugins are older (3.7.1). Update them with /plugin.
```
