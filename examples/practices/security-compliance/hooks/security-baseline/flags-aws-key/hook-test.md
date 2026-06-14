---
kind: hook
hook: plugins/practices/security-compliance/scripts/security-baseline-hook.sh
---

# Hook test: flags a hardcoded AWS access key

A Write tool call carrying a hardcoded AWS access key should produce an advisory
finding (the `aws-access-key` pattern) with a PreToolUse additionalContext block,
while still exiting 0 (advisory, never blocks).

## Stdin

```json
{"tool_name": "Write", "tool_input": {"file_path": "deploy.py", "content": "AWS_KEY = \"AKIA1234567890ABCDEF\"\n"}}
```

## Assertions

- exit 0
- stdout contains: aws-access-key
- stdout contains: PreToolUse
- stdout contains: security-baseline-findings
