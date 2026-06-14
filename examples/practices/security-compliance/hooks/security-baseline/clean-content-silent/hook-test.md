---
kind: hook
hook: plugins/practices/security-compliance/scripts/security-baseline-hook.sh
---

# Hook test: clean content is silent

A Write tool call with no matching pattern must produce no output and exit 0.
Silence is the signal that nothing was found.

## Stdin

```json
{"tool_name": "Write", "tool_input": {"file_path": "greet.py", "content": "def greet(name):\n    return f\"hello {name}\"\n"}}
```

## Assertions

- exit 0
- stdout empty
