# Hook test result: Hook test: install-rules keeps one plugin's newer rules when plugins version independently

| Field | Value |
|---|---|
| Verdict | PASS |
| Checks | 5/5 |
| Hook | `/Users/martin/Projects/hps.gd/turtlestack/plugins/practices/thinking/scripts/install-rules.sh` |
| Hook exit | 0 |

## Assertions

| Result | Assertion | Evidence |
|---|---|---|
| PASS | exit 0 | actual exit 0 |
| PASS | file contains: rules/mp--alpha--2.0.0--a.md :: Alpha 2.0.0 rule body. | found in /var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/hooktest-67e2851b-tdf36baj/rules/mp--alpha--2.0.0--a.md: 'Alpha 2.0.0 rule body.' |
| PASS | file contains: rules/mp--beta--1.6.0--b.md :: Beta 1.6.0 rule body. | found in /var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/hooktest-67e2851b-tdf36baj/rules/mp--beta--1.6.0--b.md: 'Beta 1.6.0 rule body.' |
| PASS | file not exists: rules/mp--beta--1.5.0--b.md | absent: /var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/hooktest-67e2851b-tdf36baj/rules/mp--beta--1.5.0--b.md |
| PASS | stdout contains: kept newer project rules for beta | present: 'kept newer project rules for beta' |

## Captured stdout

```
install-rules: kept newer project rules for beta; this profile's versions are older. Update them with /plugin.
```
