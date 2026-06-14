---
kind: hook
hook: plugins/practices/security-compliance/scripts/security-baseline-hook.sh
---

# Hook test: inline nosec suppresses the finding

A secret on a line carrying a `# nosec` marker is suppressed — the hook stays
silent even though the pattern matches.

## Stdin

```json
{"tool_name": "Write", "tool_input": {"file_path": "fixture.py", "content": "FAKE_KEY = \"AKIA1234567890ABCDEF\"  # nosec\n"}}
```

## Assertions

- exit 0
- stdout empty
