---
name: security-audit
description: Perform a security-focused audit of code changes or a specific area of the codebase.
argument-hint: "[file path, directory, or git diff range]"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Skill
---

Perform a focused security audit on the specified code. If no argument is provided, audit staged changes (`git diff --staged`). Follow every step below — skipping steps leads to missed vulnerabilities.

## Step 0 — Native review first (diff-scoped audits only)

When the scope is a diff or the current branch's pending changes, run Claude Code's bundled security review first and collect its findings as input:

```
Skill(skill="security-review")
```

The native review covers generic vulnerability classes on the branch diff. The steps below then add what it can't know — the org's security baseline (installed `security-baseline` rules), data-flow mapping across the wider codebase, and the team's report format. Skip this step for directory- or area-scoped audits (the native review only covers pending branch changes) and when the bundled skill is unavailable — the rest of the audit is self-contained either way.

## Step 1 — Scope identification

Determine exactly what code is in scope:

```bash
# If argument is a directory:
find $TARGET -type f -name "*.{js,ts,py,go,java,rb,php,rs}" | head -200

# If argument is a git range:
git diff --name-only $RANGE

# If argument is a file:
# Just that file
```

For each file in scope, classify it:

| Classification | Risk level | Examples |
|---|---|---|
| **Auth / Identity** | Critical | Login, registration, password reset, session management, token handling |
| **Data access** | Critical | Database queries, ORM usage, data retrieval, API data endpoints |
| **API boundary** | High | Request handlers, input parsing, response formatting, middleware |
| **Infrastructure** | High | Deployment configs, environment variables, secrets management, Docker |
| **Business logic** | Medium | Workflow logic, state machines, calculations, rule engines |
| **UI / Frontend** | Medium | Template rendering, client-side JS, form handling |
| **Utilities / Helpers** | Low | String manipulation, date formatting, logging |
| **Tests** | Low | Test files (but check they don't contain hardcoded secrets) |

Focus the deepest analysis on Critical and High files. Do not skip Low files — scan them quickly for secrets and obvious issues.

## Step 2 — Data flow mapping

Before looking for vulnerabilities, understand how data moves through the code:

```
### Data flow map

1. **User input entry points:**
   - [file:line] — [what input, how it enters (form, API, file upload, URL param)]

2. **Processing / transformation:**
   - [file:line] — [what happens to the input (validation, parsing, transformation)]

3. **Storage / persistence:**
   - [file:line] — [where data is stored (database, file, cache, session)]

4. **Output / rendering:**
   - [file:line] — [where data is displayed or returned (HTML, API response, logs)]

5. **External system calls:**
   - [file:line] — [what external systems are called with this data]
```

Identify trust boundaries:
- Client to server
- Server to database
- Service to external API
- Authenticated to unauthenticated

Every vulnerability is a data flow problem — untrusted input reaching a sensitive operation without adequate validation or sanitisation. The data flow map tells you where to look.

## Step 3 — Vulnerability scan by OWASP Top 10

For each OWASP category, search the scoped code using the specified patterns. Document what you find.

### A01: Broken Access Control

**What to look for:** Missing authorisation checks, IDOR (insecure direct object references), privilege escalation, CORS misconfiguration.

**Search patterns:**
```bash
# Missing auth middleware
grep -rn "router\.\(get\|post\|put\|delete\)" --include="*.{js,ts}" | grep -v "auth\|middleware\|protect"

# Direct object references without ownership check
grep -rn "params\.\(id\|userId\|accountId\)" --include="*.{js,ts,py}"
grep -rn "request\.args\.get\|request\.form\.get" --include="*.py"

# CORS configuration
grep -rn "Access-Control-Allow-Origin\|cors\|CORS" --include="*.{js,ts,py,go}"

# Admin/role checks
grep -rn "isAdmin\|role\s*[=!]=\|hasPermission\|authorize" --include="*.{js,ts,py,go}"
```

**Check:** For every endpoint that accesses a resource by ID, verify that the code checks whether the authenticated user owns or has access to that resource.

### A02: Cryptographic Failures

**What to look for:** Plaintext secrets, weak encryption, missing HTTPS, improper key management.

**Search patterns:**
```bash
# Hardcoded secrets
grep -rn "password\s*=\s*['\"]" --include="*.{js,ts,py,go,java,rb}"
grep -rn "secret\s*=\s*['\"]" --include="*.{js,ts,py,go,java,rb}"
grep -rn "api[_-]key\s*=\s*['\"]" --include="*.{js,ts,py,go,java,rb}"
grep -rn "BEGIN\s\(RSA\|DSA\|EC\)\sP" --include="*.{js,ts,py,go,java,rb,pem}"

# Weak crypto
grep -rn "MD5\|SHA1\|sha1\|md5\|DES\|RC4" --include="*.{js,ts,py,go,java}"
grep -rn "Math\.random\|random\.random" --include="*.{js,ts,py}"

# HTTP (not HTTPS)
grep -rn "http://" --include="*.{js,ts,py,go,java,rb}" | grep -v "localhost\|127\.0\.0\.1\|http://$"
```

### A03: Injection

**What to look for:** SQL injection, NoSQL injection, OS command injection, LDAP injection, template injection.

**Search patterns:**
```bash
# SQL string concatenation (most dangerous)
grep -rn "SELECT.*+\|INSERT.*+\|UPDATE.*+\|DELETE.*+" --include="*.{js,ts,py,go,java}"
grep -rn "f\".*SELECT\|f\".*INSERT\|f\".*UPDATE\|f\".*DELETE" --include="*.py"
grep -rn '`.*\$\{.*\}.*SELECT\|`.*\$\{.*\}.*INSERT' --include="*.{js,ts}"

# Command execution
grep -rn "exec(\|system(\|popen(\|subprocess\|child_process\|spawn(" --include="*.{js,ts,py,go,java,rb}"
grep -rn "eval(\|Function(" --include="*.{js,ts}"

# NoSQL injection
grep -rn "\$where\|\$regex\|\$gt\|\$lt\|\$ne" --include="*.{js,ts,py}"

# Template injection
grep -rn "render_template_string\|Jinja2\|Template(" --include="*.py"
grep -rn "dangerouslySetInnerHTML\|innerHTML\s*=" --include="*.{js,ts,jsx,tsx}"
```

### A04: Insecure Design

**What to look for:** Missing rate limiting, lack of abuse prevention, no account lockout, missing CAPTCHA on sensitive operations.

**Search patterns:**
```bash
# Rate limiting presence
grep -rn "rateLimit\|rate.limit\|throttle\|RateLimiter" --include="*.{js,ts,py,go}"

# Account lockout
grep -rn "lockout\|max.*attempts\|failed.*login\|brute" --include="*.{js,ts,py,go}"
```

**Check:** Are login, registration, password reset, and payment endpoints rate-limited?

### A05: Security Misconfiguration

**What to look for:** Debug mode in production, default credentials, verbose error messages, missing security headers.

**Search patterns:**
```bash
# Debug mode
grep -rn "DEBUG\s*=\s*True\|debug:\s*true\|NODE_ENV.*development" --include="*.{js,ts,py,go,json,yaml,yml}"

# Default credentials
grep -rn "admin:admin\|root:root\|password:password\|default.*password" --include="*.{js,ts,py,go,json,yaml,yml}"

# Security headers
grep -rn "X-Frame-Options\|X-Content-Type-Options\|Strict-Transport-Security\|Content-Security-Policy" --include="*.{js,ts,py,go}"

# Verbose errors
grep -rn "stack.*trace\|stackTrace\|traceback\|e\.message\|err\.message" --include="*.{js,ts,py,go}"
```

### A06: Vulnerable and Outdated Components

**Search patterns:**
```bash
# Check for lockfiles and dependency manifests
ls package-lock.json yarn.lock requirements.txt Pipfile.lock go.sum Gemfile.lock 2>/dev/null

# If npm/yarn:
npm audit --json 2>/dev/null | head -50

# If pip:
pip audit 2>/dev/null | head -50
```

### A07: Identification and Authentication Failures

**What to look for:** Weak password policies, missing MFA, insecure session management, credential exposure in URLs.

**Search patterns:**
```bash
# Password validation
grep -rn "password.*length\|minLength.*password\|password.*min" --include="*.{js,ts,py,go}"

# Session configuration
grep -rn "session.*secret\|session.*expire\|cookie.*secure\|httpOnly\|sameSite" --include="*.{js,ts,py,go}"

# JWT handling
grep -rn "jwt\.\|jsonwebtoken\|JWT_SECRET\|decode.*jwt\|verify.*jwt" --include="*.{js,ts,py,go}"
grep -rn "algorithm.*none\|alg.*none" --include="*.{js,ts,py,go}"
```

### A08: Software and Data Integrity Failures

**What to look for:** Insecure deserialization, missing integrity checks, unsigned updates.

**Search patterns:**
```bash
# Deserialization
grep -rn "pickle\.load\|yaml\.load\|unserialize\|deserialize\|JSON\.parse" --include="*.{js,ts,py,go,java,rb,php}"
grep -rn "ObjectInputStream\|readObject" --include="*.java"

# Integrity checks
grep -rn "checksum\|integrity\|verify.*signature\|hmac" --include="*.{js,ts,py,go}"
```

### A09: Security Logging and Monitoring Failures

**What to look for:** Missing audit logs for security events, sensitive data in logs, no alerting.

**Search patterns:**
```bash
# Logging of sensitive data
grep -rn "log.*password\|log.*token\|log.*secret\|log.*key\|console\.log.*auth" --include="*.{js,ts,py,go}"

# Security event logging
grep -rn "login.*log\|auth.*log\|failed.*log\|audit.*log" --include="*.{js,ts,py,go}"
```

### A10: Server-Side Request Forgery (SSRF)

**What to look for:** User-controlled URLs in server-side requests, missing URL validation.

**Search patterns:**
```bash
# URL from user input used in requests
grep -rn "fetch(\|axios\.\|requests\.\|http\.Get\|urllib" --include="*.{js,ts,py,go}"
grep -rn "url.*=.*req\.\|url.*=.*request\.\|url.*=.*params\." --include="*.{js,ts,py,go}"
```

## Step 4 — Additional checks

Beyond OWASP Top 10, check for:

### Hardcoded secrets and API keys
```bash
# Common patterns
grep -rn "AKIA[0-9A-Z]{16}" .  # AWS access keys
grep -rn "sk-[a-zA-Z0-9]{48}" .  # OpenAI keys
grep -rn "ghp_[a-zA-Z0-9]{36}" .  # GitHub tokens
grep -rn "xoxb-\|xoxp-\|xoxo-" .  # Slack tokens
grep -rn "['\"]eyJ[a-zA-Z0-9]" .  # JWT tokens
```

### Insecure randomness
```bash
grep -rn "Math\.random\|random\.random\|rand()\|mt_rand" --include="*.{js,ts,py,php}"
```
Flag any use for: token generation, session IDs, password reset tokens, cryptographic operations.

### Race conditions
```bash
# Check-then-act patterns (TOCTOU)
grep -rn "if.*exists.*then\|check.*then.*update\|find.*then.*create" --include="*.{js,ts,py,go}"
```

### Missing input validation at API boundaries
For every API endpoint found in Step 1, verify:
- Input types are validated (string is string, number is number)
- Input lengths are bounded
- Enums are checked against allowed values
- File uploads are restricted by type and size

## Step 5 — Confidence calibration

For every finding, assign a confidence level:

| Confidence | Meaning | Threshold |
|---|---|---|
| **HIGH** | The vulnerability is confirmed — the code path is exploitable as written | Dangerous pattern found AND no mitigating control in the data flow |
| **MODERATE** | The pattern is concerning but a mitigating control may exist elsewhere | Dangerous pattern found AND mitigating control is possible but not confirmed in scope |
| **LOW** | The pattern is a code smell but exploitation requires additional conditions | Pattern matches but context suggests it may be safe; needs manual review |

Rules for confidence:
- If a SQL query uses string concatenation AND the input comes from user input AND there is no parameterisation or sanitisation in the path: HIGH
- If a SQL query uses string concatenation BUT the input comes from an internal source: MODERATE (internal sources can still be tainted)
- If `eval()` is called BUT only with hardcoded strings: LOW
- When in doubt, rate MODERATE and explain what additional investigation would confirm or deny the finding
- Never rate something HIGH based on grep alone — you must trace the data flow

## Step 6 — Output

### Scope summary

```
Files analysed: [N]
Risk classification: [N] Critical, [N] High, [N] Medium, [N] Low
Data flow entry points: [N]
```

### Findings table

| # | Severity | Confidence | Category | Finding | Location | Data flow | Recommendation |
|---|---|---|---|---|---|---|---|
| 1 | Critical | HIGH | A03: Injection | SQL query built with string concatenation using user input | `app/db.py:45` | Request param -> query builder -> database | Use parameterised queries |
| 2 | High | MODERATE | A01: Access Control | Endpoint accesses resource by ID without ownership check | `routes/api.js:122` | URL param -> database lookup -> response | Add authorisation middleware |

Sort by: Severity (Critical first), then Confidence (HIGH first).

### Data flow diagram

For any Critical or High finding, show the data flow:

```
User input (request.params.id)
  -> routes/api.js:122 (no validation)
  -> db/queries.js:45 (string concatenation into SQL)
  -> PostgreSQL (query execution)

VULNERABILITY: User-controlled input reaches SQL query without parameterisation
```

### OWASP coverage

| Category | Status | Notes |
|---|---|---|
| A01: Broken Access Control | PASS / FAIL / N/A | |
| A02: Cryptographic Failures | PASS / FAIL / N/A | |
| A03: Injection | PASS / FAIL / N/A | |
| A04: Insecure Design | PASS / FAIL / N/A | |
| A05: Security Misconfiguration | PASS / FAIL / N/A | |
| A06: Vulnerable Components | PASS / FAIL / N/A | |
| A07: Auth Failures | PASS / FAIL / N/A | |
| A08: Data Integrity Failures | PASS / FAIL / N/A | |
| A09: Logging Failures | PASS / FAIL / N/A | |
| A10: SSRF | PASS / FAIL / N/A | |

### Summary and priorities

```
### Overall security posture: [Good / Needs attention / Concerning / Critical]

**Top priorities (fix these first):**
1. [Finding #N] — [why this is urgent] — [estimated effort]
2. [Finding #N] — [why this is urgent] — [estimated effort]
3. [Finding #N] — [why this is urgent] — [estimated effort]

**Positive findings:**
- [What's done well — acknowledge good security practices]

**Systemic issues:**
- [Any patterns that suggest a broader problem — e.g., "No input validation library is used anywhere"]

**What was NOT checked:**
- [Explicitly state what's out of scope — dependencies not audited, infrastructure not reviewed, etc.]
```

## Rules

- Never declare code "secure." State what was checked, what was found, and what was not checked. Security is the absence of found vulnerabilities, not a positive assertion.
- Trace data flows for every Critical and High finding. A grep match alone is not a vulnerability — it's a lead. Follow the data from input to operation.
- False positives are better than false negatives. Report uncertain findings with MODERATE or LOW confidence rather than silently dropping them.
- Check for defence in depth. Even if input validation exists at the API boundary, verify that the database layer also uses parameterised queries. One layer of defence is not enough.
- Explicitly state what was NOT audited. The "What was NOT checked" section is mandatory — it prevents dangerous overconfidence in the audit's coverage.
- If you find a Critical/HIGH finding, check the rest of the codebase for the same pattern. One SQL injection usually means there are more.
- Never include exploitation details in the report beyond what's needed to understand and fix the issue. This report may be shared broadly.
- Acknowledge good practices. If auth is solid, say so. Audits that only report negatives are demoralising and get ignored.

## Related Skills

- `/security-engineer:threat-model` — for threat modelling before or alongside the security audit.
- `/security-engineer:dependency-audit` — for auditing third-party dependencies specifically.
- `/coding-standards:review-standards` — for code quality checks that complement security findings.
