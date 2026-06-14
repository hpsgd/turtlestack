---
kind: hook
hook: plugins/practices/security-compliance/scripts/security-baseline-hook.sh
---

# Hook test: kill switch disables the scan

With `SECURITY_BASELINE_HOOK_DISABLE` set, the hook exits 0 immediately and
scans nothing — even content that would otherwise match.

## Env

SECURITY_BASELINE_HOOK_DISABLE=1

## Stdin

```json
{"tool_name": "Write", "tool_input": {"file_path": "deploy.py", "content": "AWS_KEY = \"AKIA1234567890ABCDEF\"\n"}}
```

## Assertions

- exit 0
- stdout empty
