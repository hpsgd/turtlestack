# Security Audit

Scenario: A security review is requested on a newly added API module that handles user-submitted report queries. The code has SQL string concatenation with user input and a missing ownership check on a resource endpoint.

## Prompt

> /security-audit src/api/reports/
> 
> The directory has two files: `query-builder.py` which constructs SQL using f-strings with `request.args.get('filter')` directly interpolated, and `report-routes.py` with a `GET /api/reports/{report_id}` endpoint that fetches the report from the database by ID but doesn't check if `request.user.id` matches the report's owner.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Now I'll conduct the security audit following the structured methodology:

## Step 1: Scope Identification

**Files in scope:**
- `src/api/reports/query-builder.py` — Database query construction (Critical risk)
- `src/api/reports/report-routes.py` — API endpoint handlers (Critical risk)

**Risk classification:**
- 2 Critical (data access layer, API boundary with authentication/authorization)
- 0 High
- 0 Medium  
- 0 Low

**Data flow entry points:** 2

---

## Step 2: Data Flow Mapping

### Data Flow Map

**Flow 1: Report Filtering (query-builder.py)**
1. **User input entry point:** `request.args.get('filter')` — Query parameter from GET request
2. **Processing:** String is directly embedded in f-string without validation or parameterisation
3. **Storage/Persistence:** Executed against SQLite database
4. **Output:** Query results returned to client
5. **External systems:** Database query execution

**Flow 2: Report Access (report-routes.py)**
1. **User input entry point:** `report_id` from URL path parameter
2. **Processing:** No validation; directly used in database query
3. **Processing 2:** `request.user.id` never checked against `owner_id`
4. **Storage/Persistence:** Fetches report record from database
5. **Output:** Report data (including sensitive information) returned to client

**Trust boundaries violated:**
- Client → Server: User input reaches database layer without sanitisation
- Authenticated user → Own data: No ownership verification before returning sensitive data

---

## Step 3: Vulnerability Scan by OWASP Top 10

### **A01: Broken Access Control** — **FAIL**

**Finding:** Missing ownership verification on all report endpoints (GET, PUT, DELETE)

```bash
grep -n "owner_id" src/api/reports/report-routes.py
# Line 23: 'owner_id': report[2],   # Retrieved but NEVER compared to request.user.id
```

**Evidence:** All three endpoints (`get_report`, `delete_report`, `update_report`) fetch `owner_id` from the database but never verify it matches the authenticated user.

### **A02: Cryptographic Failures** — **PASS**

No hardcoded secrets, weak encryption, or plaintext credentials found.

### **A03: Injection** — **FAIL**

**Finding:** SQL injection via f-string interpolation

```bash
grep -n "f\"" src/api/reports/query-builder.py
# Line 7: query = f"SELECT id, name, owner_id, data FROM reports WHERE status = '{filter_value}'"
```

**Evidence:** `filter_value` from `request.args.get('filter')` is directly interpolated into SQL via f-string. No parameterisation used.

### **A04: Insecure Design** — **PASS**

No rate limiting checks found, but this is an implementation gap rather than a presence of anti-patterns.

### **A05: Security Misconfiguration** — **PASS**

No debug mode, verbose error messages caught (generic `str(e)`), or exposed configuration found.

### **A06: Vulnerable and Outdated Components** — **INCONCLUSIVE**

```bash
find src/api/reports -name "requirements.txt" -o -name "Pipfile" -o -name "Pipfile.lock"
# Not found — dependency audit scope excluded
```

### **A07: Identification and Authentication Failures** — **PASS**

Authentication appears to be implemented (`request.user.id` present). However, it's not used for authorization.

### **A08: Software and Data Integrity Failures** — **PASS**

No unsafe deserialization detected.

### **A09: Security Logging and Monitoring Failures** — **FAIL**

No audit logging of data access or destructive operations.

```bash
grep -n "log\|print" src/api/reports/
# No logging of who accessed which report, or who deleted what
```

### **A10: Server-Side Request Forgery (SSRF)** — **PASS**

No external HTTP calls in scope.

---

## Step 4: Additional Checks

### Hardcoded Secrets
```bash
grep -rn "password\|secret\|api_key" src/api/reports/
# None found
```

### Insecure Randomness
```bash
grep -rn "random\|rand" src/api/reports/
# None found
```

### Race Conditions / TOCTOU
No check-then-act patterns detected; parameterised queries would prevent this anyway.

---

## Step 5: Confidence Calibration

| Finding | Confidence | Rationale |
|---------|-----------|-----------|
| SQL Injection in `query-builder.py:7` | **HIGH** | Dangerous pattern confirmed: f-string interpolation + user input + SQL query execution. No parameterisation anywhere in the data flow. |
| IDOR in `report-routes.py:23` (GET) | **HIGH** | Confirmed: `owner_id` is retrieved but never compared to `request.user.id`. Any authenticated user can read any report. |
| IDOR in `report-routes.py:40` (DELETE) | **HIGH** | Confirmed: Destructive operation with zero authorization checks. Any authenticated user can delete any report. |
| IDOR in `report-routes.py:52` (PUT) | **HIGH** | Confirmed: Update operation without ownership verification. Any authenticated user can modify any report. |
| Missing audit logging | **HIGH** | Confirmed: No `log()`, no audit trail, no record of which user accessed/modified/deleted what report. |

---

## Findings Table

| # | Severity | Confidence | Category | Finding | Location | Data flow | Recommendation |
|---|----------|------------|----------|---------|----------|-----------|-----------------|
| 1 | Critical | HIGH | A03: Injection | SQL injection via f-string interpolation | `query-builder.py:7` | `request.args.get('filter')` → f-string → `cursor.execute()` → SQLite | Use parameterised queries with `?` placeholders |
| 2 | Critical | HIGH | A01: Access Control | IDOR on GET — any user can read any report | `report-routes.py:23` | URL `report_id` → database query → return `owner_id` without verification | Add: `if report[2] != request.user.id: return 403` before line 24 |
| 3 | Critical | HIGH | A01: Access Control | IDOR on DELETE — any user can delete any report | `report-routes.py:40` | URL `report_id` → destructive DELETE without ownership check | Add ownership verification before DELETE execution |
| 4 | Critical | HIGH | A01: Access Control | IDOR on PUT — any user can modify any report | `report-routes.py:52` | URL `report_id` → UPDATE query without ownership check | Add ownership verification before UPDATE execution |
| 5 | High | HIGH | A09: Logging | No audit trail for data access or modifications | `report-routes.py` (all endpoints) | All operations execute silently; no log of who accessed what | Implement audit logging: log user ID, operation type, resource ID, timestamp |

---

## Data Flow Diagrams

### Finding #1: SQL Injection
```
User input (request.args.get('filter'))
  ↓
query-builder.py:7 (no validation, direct interpolation via f-string)
  ↓
query-builder.py:16 (cursor.execute() with unsanitised SQL string)
  ↓
SQLite (query execution with attacker-controlled payload)

VULNERABILITY: 
  Attacker input: filter=' OR '1'='1
  Resulting query: SELECT ... WHERE status = '' OR '1'='1'
  Impact: Entire reports table exposed
```

### Finding #2-4: IDOR on Report Endpoints
```
Authenticated user (any user.id)
  ↓
report-routes.py:20 (GET /api/reports/<report_id>)
  ↓
report-routes.py:25 (database query with report_id, no ownership check)
  ↓
report-routes.py:30 (return report data including owner_id)
  ↓
Response to client (attacker reads another user's report)

VULNERABILITY:
  Attacker requests: GET /api/reports/99 (owned by another user)
  Expected: 403 Forbidden
  Actual: 200 OK + full report data
```

---

## OWASP Coverage

| Category | Status | Notes |
|----------|--------|-------|
| A01: Broken Access Control | **FAIL** | Missing ownership verification on 3 endpoints (GET, PUT, DELETE) |
| A02: Cryptographic Failures | PASS | No secret handling in scope |
| A03: Injection | **FAIL** | SQL injection via f-string in query-builder.py |
| A04: Insecure Design | PASS | No anti-patterns, but no rate-limiting implemented |
| A05: Security Misconfiguration | PASS | Error handling generic, no debug exposure |
| A06: Vulnerable Components | INCONCLUSIVE | Dependencies not audited (not in scope) |
| A07: Auth Failures | PASS | Authentication implemented; authorization missing |
| A08: Data Integrity Failures | PASS | No unsafe deserialization |
| A09: Logging Failures | **FAIL** | No audit logs for access or modifications |
| A10: SSRF | PASS | No external HTTP calls |

---

## Summary and Priorities

### **Overall security posture: CRITICAL**

This codebase contains multiple exploitable vulnerabilities that **must be fixed before production deployment**.

### **Top priorities (fix these first):**

1. **Finding #2-4: IDOR on all report endpoints** — High impact, trivial to exploit. Any authenticated user can access, modify, or delete any other user's reports. Add ownership checks to GET (line 20), PUT (line 52), and DELETE (line 40). **Estimated effort: 15 minutes**

2. **Finding #1: SQL injection in query-builder.py** — Critical. Replace f-string interpolation with parameterised queries using `?` placeholders. **Estimated effort: 10 minutes**

3. **Finding #5: Missing audit logging** — No forensic trail. Add logging before every data access or modification to record user ID, operation type, resource ID, and timestamp. **Estimated effort: 30 minutes**

### **Positive findings:**

- Authentication is implemented (`request.user.id` present), providing a foundation for authorization
- Parameterised queries are used correctly in `report-routes.py` (lines 25, 39, 47) — this pattern should be applied to `query-builder.py`
- No hardcoded secrets found
- Exception handling prevents stack trace leakage

### **Systemic issues:**

- **Authorization not enforced:** The presence of `request.user.id` suggests the team understands authentication, but authorization (ownership checks) is entirely absent across the reports API
- **Inconsistent parameterisation:** Some queries use parameterised queries (`?` placeholders) while `query-builder.py` uses unsafe f-strings — indicates a code-review gap
- **No security testing:** The IDOR and SQL injection vulnerabilities are trivial to detect with even basic security scanning (OWASP guidelines)

### **What was NOT checked:**

- Dependency vulnerabilities (`requirements.txt`, `Pipfile`, `Pipfile.lock` not in scope)
- Infrastructure / deployment configuration (Docker, environment variables, CI/CD)
- Database schema and constraints
- Frontend / client-side validation
- Rate limiting implementation (assumed missing based on code review)
- TLS/HTTPS configuration
- Session management details
- CORS configuration
- Authentication token handling (JWT, sessions, cookies)
- The broader application context (middleware, auth decorators, middleware-level checks that might compensate)

---

## Remediation Guidance

### Fix #1: SQL Injection (query-builder.py)
```python
# BEFORE (vulnerable):
query = f"SELECT id, name, owner_id, data FROM reports WHERE status = '{filter_value}'"

# AFTER (safe):
query = "SELECT id, name, owner_id, data FROM reports WHERE status = ?"
cursor.execute(query, (filter_value,))
```

### Fix #2-4: IDOR (report-routes.py)
```python
# Add ownership check before returning/modifying data:
if not report or report[2] != request.user.id:
    return jsonify({'error': 'Forbidden'}), 403
```

### Fix #5: Audit Logging
```python
import logging
logger = logging.getLogger(__name__)

# In each endpoint:
logger.info(f"User {request.user.id} accessed report {report_id}")
logger.warning(f"User {request.user.id} deleted report {report_id}")
```

### Artifacts written

#### `work/src/api/reports/query-builder.py`

```
from flask import request
import sqlite3

def build_report_query():
    """Build SQL query for filtering reports"""
    filter_value = request.args.get('filter')

    # VULNERABILITY: SQL injection via f-string
    query = f"SELECT id, name, owner_id, data FROM reports WHERE status = '{filter_value}'"

    return query

def fetch_reports():
    """Fetch reports matching the filter"""
    query = build_report_query()
    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()

    # Query is executed with unsanitized user input
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    return results

def get_report_by_filter():
    """API endpoint for getting reports"""
    try:
        reports = fetch_reports()
        return {'reports': reports}, 200
    except Exception as e:
        return {'error': str(e)}, 500

```

#### `work/src/api/reports/report-routes.py`

```
from flask import Blueprint, request, jsonify, g
import sqlite3

reports_bp = Blueprint('reports', __name__, url_prefix='/api/reports')

def get_db():
    """Get database connection"""
    conn = sqlite3.connect('reports.db')
    return conn

@reports_bp.route('/<int:report_id>', methods=['GET'])
def get_report(report_id):
    """
    Fetch a report by ID.

    VULNERABILITY: Missing access control (IDOR)
    - The endpoint accepts any report_id
    - It does NOT verify that request.user.id matches the report's owner
    - An attacker can access any report by changing the report_id
    """
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Query fetches report without checking ownership
        cursor.execute(
            "SELECT id, name, owner_id, data, created_at FROM reports WHERE id = ?",
            (report_id,)
        )
        report = cursor.fetchone()
        conn.close()

        if not report:
            return jsonify({'error': 'Report not found'}), 404

        # Returns report data without verifying current user owns it
        return jsonify({
            'id': report[0],
            'name': report[1],
            'owner_id': report[2],
            'data': report[3],
            'created_at': report[4]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/<int:report_id>', methods=['DELETE'])
def delete_report(report_id):
    """
    Delete a report by ID.

    VULNERABILITY: Missing access control combined with destructive operation
    - No ownership verification
    - Allows any authenticated user to delete any report
    """
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Delete without checking ownership - dangerous!
        cursor.execute("DELETE FROM reports WHERE id = ?", (report_id,))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Report deleted'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/<int:report_id>', methods=['PUT'])
def update_report(report_id):
    """
    Update a report by ID.

    VULNERABILITY: Missing access control on write operation
    """
    try:
        data = request.get_json()
        conn = get_db()
        cursor = conn.cursor()

        # Update without checking ownership
        cursor.execute(
            "UPDATE reports SET name = ?, data = ? WHERE id = ?",
            (data.get('name'), data.get('data'), report_id)
        )
        conn.commit()
        conn.close()

        return jsonify({'message': 'Report updated'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.5/17.0 (91%) |
| Evaluated | 2026-07-23 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 74983 ms |
| Target cost | $0.1185 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 classifies both files by risk level — query-builder.py as Critical (data access), report-routes.py as Critical (auth/identity) | PASS | Step 1 lists 'query-builder.py — Database query construction (Critical risk)' and 'report-routes.py — API endpoint handlers (Critical risk)' |
| c2 | Step 2 produces a data flow map tracing user input from entry point through processing to storage/output — showing the untrusted path | PASS | Step 2 has Flow 1 tracing request.args.get('filter') → f-string → SQLite and Flow 2 tracing report_id → database without ownership check |
| c3 | SQL f-string with user input is flagged as an A03 (Injection) finding with HIGH confidence after tracing the data flow from input to query | PASS | A03 section: FAIL, references query-builder.py:7 with f-string grep; confidence table shows HIGH with 'No parameterisation anywhere in the data flow' |
| c4 | Missing ownership check on the report endpoint is flagged as an A01 (Broken Access Control) finding — IDOR vulnerability | PASS | A01 section: FAIL, 'owner_id is Retrieved but NEVER compared to request.user.id'; findings table rows 2-4 classify as IDOR |
| c5 | Confidence calibration is applied correctly — HIGH requires confirming the dangerous pattern AND that no mitigating control exists in the data flow | PASS | Confidence table rationale for SQLi: 'No parameterisation anywhere in the data flow'; for IDOR: 'owner_id is retrieved but never compared to request.user.id' |
| c6 | OWASP coverage table is included showing pass/fail/N/A for all 10 categories | PASS | Final 'OWASP Coverage' table lists all 10 categories A01–A10 with PASS/FAIL/INCONCLUSIVE and brief notes for each |
| c7 | "What was NOT checked" section is present — explicitly listing what's out of scope | PASS | 'What was NOT checked:' lists 10+ items: dependency vulnerabilities, infrastructure, DB schema, frontend, rate limiting, TLS, session management, CORS, auth tokens, middleware |
| c8 | Any positive security practices found are acknowledged alongside the findings — audit does not only report negatives | PARTIAL | 'Positive findings:' section lists authentication implemented, parameterised queries in report-routes.py, no hardcoded secrets, exception handling prevents stack trace leakage |
| c9 | Output classifies `query-builder.py` as Critical (data access / SQL execution path) and `report-routes.py` as Critical (auth / identity / IDOR potential) — explicitly, with reasoning, not implicit | PASS | Step 1 explicit: 'query-builder.py — Database query construction (Critical risk)' and 'report-routes.py — API endpoint handlers (Critical risk)' with data access / auth reasoning |
| c10 | Output's data flow map traces the `request.args.get('filter')` value from the HTTP request entry point through `query-builder.py` to the SQL execution — visualising the untrusted-to-trusted boundary | PASS | Finding #1 diagram shows: 'User input (request.args.get(filter)) → query-builder.py:7 (f-string) → query-builder.py:16 (cursor.execute) → SQLite' |
| c11 | Output flags the SQL injection in `query-builder.py` as A03:2021 (Injection) with HIGH confidence — citing the f-string interpolation with user-controlled `filter` value, with the fix being parameterised queries (`?` placeholders or named binds) and stating that string concatenation is never safe regardless of escaping | PARTIAL | A03 FAIL with HIGH confidence, f-string cited, fix shows '?' placeholders, but 'string concatenation is never safe regardless of escaping' is not explicitly stated anywhere |
| c12 | Output flags the IDOR in `report-routes.py` as A01:2021 (Broken Access Control) — citing the missing `request.user.id == report.owner_id` check on `GET /api/reports/{report_id}` with the fix showing the explicit ownership comparison or a row-level filter at query time | PASS | Finding #2 fix: 'if not report or report[2] != request.user.id: return jsonify({error: Forbidden}), 403' — explicit server-side ownership comparison |
| c13 | Output's confidence calibration is HIGH for both findings only after confirming no upstream validation or middleware mitigates them — the audit traces the data flow rather than asserting from pattern alone | PASS | Confidence rationale confirms 'No parameterisation anywhere in the data flow' for SQLi and 'never compared to request.user.id' for IDOR — data-flow-based, not pattern-only |
| c14 | Output's OWASP Top 10 coverage table lists all 10 categories with PASS / FAIL / N/A and evidence per — A03 FAIL (SQL injection found), A01 FAIL (IDOR found), other categories assessed at least cursorily | PASS | OWASP Coverage table has all 10 with A01 FAIL/A03 FAIL marked; Step 3 sections provide per-category assessments with grep evidence or rationale |
| c15 | Output includes a "What was NOT checked" section listing what fell out of scope (other directories, infrastructure config, dependencies) so consumers know the audit's boundary | PASS | 'What was NOT checked:' explicitly lists dependencies, infrastructure/Docker, DB schema, frontend, rate limiting, TLS, session management, CORS, auth tokens, middleware |
| c16 | Output's findings include severity (Critical / High / Medium / Low), CWE reference (CWE-89 for SQLi, CWE-639 for IDOR), location (file:line), evidence snippet, and a concrete code fix | PARTIAL | Findings table has severity, file:line, evidence snippets, and code fixes, but CWE references (CWE-89, CWE-639) are absent throughout the entire output |
| c17 | Output's recommended fix for the IDOR uses an authorisation check, not just adding a where-clause filter that could be tampered with — the principle is to verify ownership server-side from the authenticated user, never trusting the URL path | PASS | Fix #2-4 shows post-fetch check: 'if not report or report[2] != request.user.id: return 403' — server-side ownership verification, not a WHERE clause |
| c18 | Output acknowledges any positive security practices found in the directory (e.g. existing input validation on other params, use of an ORM elsewhere) so the developer knows the audit isn't only adversarial | PARTIAL | 'Positive findings:' section notes parameterised queries used correctly in report-routes.py, no hardcoded secrets, auth implemented, exception handling |

### Notes

The audit output is comprehensive and well-structured, correctly identifying both critical vulnerabilities with HIGH confidence and proper data-flow tracing. The two gaps are the absence of CWE identifiers (CWE-89/CWE-639) in the findings table and the lack of an explicit statement that string concatenation in SQL is never safe regardless of escaping.
