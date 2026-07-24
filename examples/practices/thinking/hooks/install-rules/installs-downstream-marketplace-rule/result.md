# Hook test result: Hook test: install-rules installs a downstream marketplace's rule

| Field | Value |
|---|---|
| Verdict | PASS |
| Checks | 5/5 |
| Hook | `/Users/martin/Projects/turtlestack/plugins/practices/thinking/scripts/install-rules.sh` |
| Hook exit | 0 |

## Assertions

| Result | Assertion | Evidence |
|---|---|---|
| PASS | exit 0 | actual exit 0 |
| PASS | file exists: rules/downstreammp--recon--2.1.0--recon-baseline.md | exists: /var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/hooktest-d05ce7c6-ui3ssf2l/rules/downstreammp--recon--2.1.0--recon-baseline.md |
| PASS | file contains: rules/downstreammp--recon--2.1.0--recon-baseline.md :: Downstream marketplace rule body | found in /var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/hooktest-d05ce7c6-ui3ssf2l/rules/downstreammp--recon--2.1.0--recon-baseline.md: 'Downstream marketplace rule body' |
| PASS | stdout contains: downstreammp | present: 'downstreammp' |
| PASS | stdout not contains: turtlestack | absent: 'turtlestack' |

## Captured stdout

```
<learning-context>
Installed 1 new/updated rules from 1 plugins (downstreammp)
</learning-context>
```
