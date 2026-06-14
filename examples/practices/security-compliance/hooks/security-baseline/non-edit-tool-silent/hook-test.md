---
kind: hook
hook: plugins/practices/security-compliance/scripts/security-baseline-hook.sh
---

# Hook test: non-edit tools are ignored

The hook only scans Edit/Write/MultiEdit content. A Read tool event — even one
whose payload contains a secret-shaped string — is ignored and produces no output.

## Stdin

```json
{"tool_name": "Read", "tool_input": {"file_path": "AKIA1234567890ABCDEF.txt"}}
```

## Assertions

- exit 0
- stdout empty
