# Hook test result: Hook test: install-rules doesn't bring back rules a newer version dropped

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
| PASS | file contains: rules/mp--alpha--4.0.0--style.md :: New 4.0.0 rule body. | found in /var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/hooktest-c913aa83-_m2rnta2/rules/mp--alpha--4.0.0--style.md: 'New 4.0.0 rule body.' |
| PASS | file not exists: rules/mp--beta--3.7.1--research.md | absent: /var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/hooktest-c913aa83-_m2rnta2/rules/mp--beta--3.7.1--research.md |
| PASS | file not exists: rules/mp--alpha--3.7.1--style.md | absent: /var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/hooktest-c913aa83-_m2rnta2/rules/mp--alpha--3.7.1--style.md |

## Captured stdout

```
install-rules: kept mp 4.0.0 rules; this profile's plugins are older (3.7.1). Update them with /plugin.
```
