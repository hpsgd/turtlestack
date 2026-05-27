# Review With Issues

Scenario: A developer asks the code reviewer agent to review a Python Django view that handles user password reset. The code contains a SQL injection risk, an N+1 query, and missing rate limiting on the endpoint.

## Prompt

> Can you review this code? It's the password reset handler in our Django app.
> 
> ```python
> # views.py
> from django.http import JsonResponse
> from django.contrib.auth.models import User
> from django.db import connection
> import secrets
> 
> def request_password_reset(request):
>     if request.method != 'POST':
>         return JsonResponse({'error': 'Method not allowed'}, status=405)
> 
>     email = request.POST.get('email', '')
> 
>     # Find user by email
>     with connection.cursor() as cursor:
>         cursor.execute(f"SELECT id, username FROM auth_user WHERE email = '{email}'")
>         row = cursor.fetchone()
> 
>     if not row:
>         return JsonResponse({'error': 'Email not found'}, status=404)
> 
>     user_id, username = row
>     token = secrets.token_urlsafe(32)
> 
>     # Save token and send to all user's linked accounts
>     user = User.objects.get(id=user_id)
>     for profile in user.linkedprofile_set.all():
>         profile.reset_token = token
>         profile.save()
>         # Send email for each linked account
>         send_reset_email(profile.email, token)
> 
>     return JsonResponse({'message': 'Reset email sent'})
> ```
> 
> A few specifics for the response (the file is `views.py`; cite `views.py:line` on every finding):
> 
> - **Findings list (8 minimum)** — each with `**Severity**: BLOCKER/CRITICAL/HIGH/MEDIUM/LOW | **Confidence**: HIGH/MEDIUM/LOW | **File:Line**: views.py:N | **Evidence**: \`code snippet\` | **Fix**: [concrete code]`:
>   1. **BLOCKER, HIGH confidence** — SQL injection at `views.py:14` via f-string interpolation `f"SELECT id, email FROM auth_user WHERE email = '{email}'"`. Fix: parameterised query `cursor.execute("SELECT id, email FROM auth_user WHERE email = %s", [email])` OR Django ORM `User.objects.get(email=email)`.
>   2. **CRITICAL** — N+1 query in the `for profile in user.linkedprofile_set.all()` loop at `views.py:~34`. Each iteration triggers a save. Fix: `select_related('user')` on the queryset and bulk update with `LinkedProfile.objects.filter(user=user).update(reset_token=token)`.
>   3. **CRITICAL** — Missing rate limiting on the password-reset endpoint. Fix: add `django-ratelimit` decorator `@ratelimit(key='ip', rate='5/h', block=True)` or equivalent middleware. WHY: unbounded password-reset attempts allow account-enumeration probing and email flooding.
>   4. **HIGH** — User enumeration via 404 on unknown email at `views.py:~22`. Returning a different status for unknown vs known emails leaks account existence. Fix: return 200 with a generic message ("If an account exists for this email, a reset link has been sent") regardless.
>   5. **HIGH** — Reset token stored in plaintext on `profile.reset_token`. Fix: store `hashlib.sha256(token.encode()).hexdigest()` at rest; compare hashed value on redemption. Plaintext tokens in the DB = full account takeover if DB leaks.
>   6. **HIGH** — No token expiry / TTL on the reset token. Fix: add `reset_token_expires_at = models.DateTimeField()` with a 1-hour TTL; reject expired tokens at redemption. Use Django's built-in `PasswordResetTokenGenerator` which handles expiry and single-use invalidation.
>   7. **MEDIUM** — Missing CSRF protection (no `@csrf_protect` or DRF auth/permission decorator) on the view.
>   8. **MEDIUM** — Synchronous `send_reset_email()` inside the request handler blocks the response and provides no retry. Fix: offload to a Celery / RQ background task.
>   9. **MEDIUM** — Race condition between raw SQL `SELECT` and `User.objects.get(id=user_id)` ORM call — if the user row is deleted between these two queries, `DoesNotExist` raises an unhandled 500. Use a single ORM call.
> - **Quality Score Table** with at least four dimensions: `| Dimension | Score (0-10) | Rationale |` — Security (0/10 — SQL injection blocker), Correctness, Performance, Maintainability. Overall confidence = `min(HARD signals)` so Security=0 means overall confidence floor is 0.
> - **Verdict**: explicit `Verdict: REQUEST_CHANGES` (or `BLOCK` given the SQL injection blocker). Not approve.
> - **Adversarial analysis section**: explicitly consider "what happens if this endpoint is called 1000×/sec from one IP?" and "what if the email is `' OR 1=1 --`?" and "what if `linkedprofile_set` is empty?". Each as a separate sub-finding.
> - **Confidence levels per finding** (HIGH/MEDIUM/LOW) — not just severity. SQL injection = HIGH confidence; race condition = MEDIUM (requires concurrent delete).
> - **"Positive Observations" or "Questions for the Author" section at end** (per the agent's defined output format), not only findings.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Code Review — `views.py` — Password Reset Handler

---

## Findings

---

**Finding 1**
**Severity**: BLOCKER | **Confidence**: HIGH | **File:Line**: `views.py:15`
**Evidence**: `cursor.execute(f"SELECT id, username FROM auth_user WHERE email = '{email}'")`
**Description**: Direct f-string interpolation of user-supplied input into a raw SQL query. An attacker can inject arbitrary SQL — dump tables, bypass authentication, or escalate to OS-level commands if `xp_cmdshell` is available.
**Fix**:
```python
# Option A — parameterised raw query
cursor.execute("SELECT id, username FROM auth_user WHERE email = %s", [email])

# Option B (preferred) — eliminate the raw query entirely
try:
    user = User.objects.get(email=email)
except User.DoesNotExist:
    user = None
```

---

**Finding 2**
**Severity**: CRITICAL | **Confidence**: HIGH | **File:Line**: `views.py:26–28`
**Evidence**: `for profile in user.linkedprofile_set.all(): profile.reset_token = token; profile.save()`
**Description**: N+1 write pattern. Each loop iteration fires a separate `UPDATE` — one per linked profile. For a user with 100 linked profiles, this issues 100 round-trips to the database inside a single HTTP request.
**Fix**:
```python
from django.utils import timezone

# Single bulk UPDATE — one query regardless of profile count
user.linkedprofile_set.all().update(
    reset_token=token,
    reset_token_expires_at=timezone.now() + timedelta(hours=1),
)
```

---

**Finding 3**
**Severity**: CRITICAL | **Confidence**: HIGH | **File:Line**: `views.py:7` (function entry)
**Evidence**: No rate-limiting decorator or middleware on the view.
**Description**: The endpoint accepts unlimited POST requests. An attacker can call it in a tight loop to: (a) enumerate valid email addresses via timing differences or status codes, (b) flood targets with reset emails, (c) saturate the email-sending pipeline. No cost to the attacker.
**Fix**:
```python
from django_ratelimit.decorators import ratelimit

@ratelimit(key='post:email', rate='3/h', block=True)
@ratelimit(key='ip', rate='20/h', block=True)
def request_password_reset(request):
    ...
```
Or enforce at the reverse-proxy/WAF layer if `django-ratelimit` is not available.

---

**Finding 4**
**Severity**: HIGH | **Confidence**: HIGH | **File:Line**: `views.py:18–19`
**Evidence**: `return JsonResponse({'error': 'Email not found'}, status=404)`
**Description**: Returning HTTP 404 for an unknown email and HTTP 200 for a known one leaks account existence. An attacker can silently enumerate your entire user base by submitting email addresses and observing the status code.
**Fix**:
```python
# Return 200 with a generic message regardless of whether the email exists
if not user:
    return JsonResponse({'message': 'If an account exists for this email, a reset link has been sent'})
# continue with token generation ...
return JsonResponse({'message': 'If an account exists for this email, a reset link has been sent'})
```

---

**Finding 5**
**Severity**: HIGH | **Confidence**: HIGH | **File:Line**: `views.py:27`
**Evidence**: `profile.reset_token = token`
**Description**: The raw token is stored in the database. If the database is breached (SQL dump, replica misconfiguration, backup leak), every token is immediately usable for account takeover — no additional cracking step required.
**Fix**:
```python
import hashlib

hashed = hashlib.sha256(token.encode()).hexdigest()
profile.reset_token = hashed  # store only the hash

# At redemption time:
submitted_hash = hashlib.sha256(submitted_token.encode()).hexdigest()
if profile.reset_token != submitted_hash:
    return JsonResponse({'error': 'Invalid token'}, status=400)
```
Alternatively, use Django's built-in `PasswordResetTokenGenerator`, which handles hashing, expiry, and single-use invalidation.

---

**Finding 6**
**Severity**: HIGH | **Confidence**: HIGH | **File:Line**: `views.py:22–28`
**Evidence**: `token = secrets.token_urlsafe(32)` … `profile.reset_token = token` — no expiry field set.
**Description**: Tokens never expire. A token issued today is valid indefinitely, broadening the attack window for phishing-intercepted or forwarded reset emails. It also prevents single-use enforcement.
**Fix**:
```python
from datetime import timedelta
from django.utils import timezone

RESET_TTL = timedelta(hours=1)

# When issuing:
profile.reset_token = hashed_token
profile.reset_token_expires_at = timezone.now() + RESET_TTL
profile.save()

# At redemption:
if profile.reset_token_expires_at < timezone.now():
    return JsonResponse({'error': 'Token expired'}, status=400)
```
Or delegate entirely to `django.contrib.auth.forms.PasswordResetForm`, which handles expiry via `PasswordResetTokenGenerator`.

---

**Finding 7**
**Severity**: MEDIUM | **Confidence**: HIGH | **File:Line**: `views.py:7`
**Evidence**: No `@csrf_protect` decorator; no DRF `permission_classes`; no `@login_required`.
**Description**: The view is not CSRF-protected. A forged cross-site POST from a malicious page can trigger a password-reset flow on behalf of an authenticated user. Django's `CsrfViewMiddleware` only applies if it's in `MIDDLEWARE` and the view isn't exempt — custom views that handle `POST` directly should be explicit.
**Fix**:
```python
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def request_password_reset(request):
    ...
```
Or, if this is a JSON API consumed by a SPA, use DRF with `SessionAuthentication` (which enforces CSRF) or token-based auth.

---

**Finding 8**
**Severity**: MEDIUM | **Confidence**: HIGH | **File:Line**: `views.py:30`
**Evidence**: `send_reset_email(profile.email, token)`
**Description**: Email sending is synchronous inside the request handler. SMTP latency (typically 100–500 ms per message) multiplied across N linked profiles can hold the HTTP connection open for seconds. If the mail server is down, the entire request fails with an unhandled exception and no retry.
**Fix**:
```python
# Celery example
from myapp.tasks import send_reset_email_task

send_reset_email_task.delay(profile.email, token)

# Or Django-Q / RQ equivalent
from django_rq import enqueue
enqueue(send_reset_email, profile.email, token)
```
If a task queue is unavailable, at minimum wrap in a `try/except` and log failures rather than propagating a 500.

---

**Finding 9**
**Severity**: MEDIUM | **Confidence**: MEDIUM | **File:Line**: `views.py:14–15` and `views.py:25`
**Evidence**: Raw SQL at line 15 yields `user_id`; `User.objects.get(id=user_id)` at line 25 re-fetches by that id.
**Description**: Two separate database reads for the same row with no transaction isolation. If a concurrent request deletes the user between lines 16 and 25, `User.objects.get()` raises `User.DoesNotExist`, which is unhandled — the view returns HTTP 500. This is also an unnecessary double-query: the ORM can retrieve the user in one call.
**Fix**:
```python
try:
    user = User.objects.prefetch_related('linkedprofile_set').get(email=email)
except User.DoesNotExist:
    return JsonResponse({'message': 'If an account exists ...'})
# raw SQL block removed entirely
```

---

## Quality Score Table

| Dimension | Score (0–10) | Rationale |
|---|---|---|
| Security | 0 / 10 | SQL injection BLOCKER present; enumeration, plaintext tokens, no rate-limit, no CSRF — every OWASP A01–A07 category touched |
| Correctness | 3 / 10 | Succeeds in the happy path only; unhandled `DoesNotExist` on race, silent failure if `linkedprofile_set` is empty, no error handling on email dispatch |
| Performance | 2 / 10 | N+1 write loop; two DB round-trips for same user; synchronous SMTP blocking request thread |
| Maintainability | 3 / 10 | Bypasses Django ORM for no reason, re-invents password-reset machinery Django already ships, no type hints, `send_reset_email` undefined in snippet |
| **Overall** | **0 / 10** | Floor is `min(HARD signals)` — Security=0 sets the overall score |

---

## Verdict

**Verdict: BLOCK**

The SQL injection at `views.py:15` is a BLOCKER. This code must not be merged or deployed in its current state. The combination of SQL injection, plaintext token storage, no rate-limiting, and user enumeration represents a full account-takeover attack surface on a security-critical endpoint.

---

## Adversarial Analysis

### Scenario A — 1,000 req/sec from one IP

No rate limiting exists (`views.py:7`). Every request reaches the database and (on a hit) the mail server. At 1,000 req/sec against a valid email:
- **Database**: 1,000 raw SQL executions/sec against `auth_user`, bypassing the ORM query cache.
- **Mail server**: Up to 1,000 reset emails/sec to the target address — effective email-flooding DoS against the victim.
- **SMTP connection pool**: `send_reset_email` is synchronous; request threads pile up waiting for SMTP handshakes, exhausting the Django worker pool within seconds.
- **No circuit-breaker**: the view returns HTTP 200 on every hit — no signal to the caller or monitoring that abuse is occurring.

**Blast radius**: service degradation for all users, not just the targeted account.

---

### Scenario B — Email input is `' OR 1=1 --`

`views.py:15` becomes:
```sql
SELECT id, username FROM auth_user WHERE email = '' OR 1=1 --'
```
`1=1` is always true; `--` comments out the closing quote. `fetchone()` returns the **first row in the table** (typically the superuser). The attacker receives a password-reset token for that account. With plaintext token storage (`views.py:27`), they own the account the moment the email arrives (or if they can read DB contents via a second injection).

More dangerous variants: `UNION SELECT`-based data exfiltration, `'; DROP TABLE auth_user; --` on PostgreSQL with `autocommit`, or `'; UPDATE auth_user SET password='...' WHERE id=1; --`.

---

### Scenario C — `linkedprofile_set` is empty

`views.py:26`: the `for` loop body never executes. `token` is generated (`views.py:22`) but stored nowhere and no email is sent. The view returns HTTP 200 `{'message': 'Reset email sent'}` — a **lie**. The user receives no email and cannot reset their password, but the UI tells them to check their inbox.

Additionally, the raw SQL query may return a valid `user_id` for a user who has a `User` row but zero `LinkedProfile` rows — so `User.objects.get(id=user_id)` at `views.py:25` succeeds, silently discards the token, and returns success. This silent failure is untestable without a user fixture that has no linked profiles.

---

## Positive Observations

- `secrets.token_urlsafe(32)` (`views.py:22`) is the correct CSPRNG — `random` or `uuid4` would be weaker.
- The method guard at `views.py:8–9` (405 on non-POST) is present and correct.
- The code is short enough to reason about completely, which makes the full fix tractable.

---

## Questions for the Author

1. **Why raw SQL?** `User.objects.get(email=email)` covers this case in one line with no injection risk. Was there a performance or join reason for dropping to raw SQL here?
2. **What is `LinkedProfile`?** Does a `User` always have at least one `LinkedProfile`? If not, the silent-success bug in Scenario C is a known user-facing defect.
3. **Is `send_reset_email` tested?** It's called but not imported or defined in the snippet — is it a stub, or does it actually send? If it raises, the view 500s after the token has already been written.
4. **Is there a redemption view?** If so, does it validate token expiry and invalidate on use? The issues in this view (plaintext, no TTL) are load-bearing there too.
5. **Is Django's built-in `PasswordResetView` a viable replacement?** It handles token generation, hashing, expiry, single-use invalidation, and CSRF out of the box. The custom implementation here re-invents that machinery with several gaps — is there a specific reason for the custom path (e.g. multi-profile model, custom token format)?

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 13.0/14.0 (93%) |
| Evaluated | 2026-05-27 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 81276 ms |
| Target cost | $0.1885 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent identifies the SQL injection vulnerability (f-string interpolation into the raw SQL query) as a blocker with specific file:line reference | PASS | Finding 1: 'Severity: BLOCKER \| Confidence: HIGH \| File:Line: views.py:15' with evidence quoting the f-string interpolation. |
| c2 | Agent identifies the N+1 query in the loop over linkedprofile_set as a performance finding, with a specific fix (select_related or prefetch_related) | PASS | Finding 2 flags the N+1 write pattern at views.py:26–28 with bulk UPDATE fix; Finding 9 fix includes `prefetch_related('linkedprofile_set')`. |
| c3 | Agent flags the missing rate limiting on the password reset endpoint as a security finding | PASS | Finding 3 (CRITICAL): 'No rate-limiting decorator or middleware on the view' with django-ratelimit decorator fix. |
| c4 | Agent produces a quality score table covering at least Security, Correctness, Performance, and Maintainability dimensions | PASS | Quality Score Table has Security (0/10), Correctness (3/10), Performance (2/10), Maintainability (3/10), and Overall (0/10). |
| c5 | Agent gives a verdict of REQUEST CHANGES or BLOCK (not APPROVE) given the SQL injection blocker | PASS | 'Verdict: BLOCK' — 'SQL injection at views.py:15 is a BLOCKER. This code must not be merged or deployed.' |
| c6 | Agent runs adversarial analysis — considers what happens if the endpoint is called 1000 times in rapid succession | PASS | Adversarial Analysis 'Scenario A — 1,000 req/sec from one IP' covers DB exhaustion, email flooding, and SMTP thread starvation. |
| c7 | Agent notes that the 404 response on unknown email leaks account existence information (user enumeration) and recommends returning 200 regardless | PARTIAL | Finding 4 (HIGH): 'Returning HTTP 404 for unknown email... leaks account existence' with fix returning generic 200 message. |
| c8 | Every finding cites a specific location in the code and includes a concrete suggested fix | PASS | All 9 findings include File:Line (e.g. views.py:15, views.py:26–28) and concrete code fixes with actual Python snippets. |
| c9 | Output recommends parameterised queries (e.g. `cursor.execute("SELECT ... WHERE email = %s", [email])`) or the Django ORM (`User.objects.filter(email=email).first()`) as the fix for the SQL injection, not just "sanitise input" | PASS | Finding 1 Fix: 'Option A — cursor.execute("SELECT id, username FROM auth_user WHERE email = %s", [email])' and 'Option B — User.objects.get(email=email)'. |
| c10 | Output assigns confidence levels (HIGH / MODERATE / LOW or numeric 0-100) to individual findings, not only an overall confidence | PASS | All 9 findings carry explicit Confidence labels: Findings 1–8 = HIGH, Finding 9 = MEDIUM. |
| c11 | Output's Security score is 0 (or otherwise reflects that a HARD signal hit zero) given the SQL injection, and the overall confidence reflects `min(HARD signals)` rather than averaging the issue away | PASS | Security: '0/10'; Overall: '0/10 — Floor is min(HARD signals) — Security=0 sets the overall score'. |
| c12 | Output flags the unconditional `User.objects.get(id=user_id)` as a correctness or robustness issue (raises `DoesNotExist` if the row vanishes between the raw query and the ORM lookup, or if `linkedprofile_set` is empty no token is ever persisted to the user) | PASS | Finding 9 flags the race condition DoesNotExist risk. Scenario C covers empty linkedprofile_set: token generated but stored nowhere, silent 200 lie. |
| c13 | Output identifies that the same reset token is reused across every linked profile and recommends per-profile token generation (or explains why a single token is acceptable) — a token-handling concern beyond the SQL/N+1/rate-limit trio | FAIL | No finding, adversarial scenario, or observation mentions the single-token-shared-across-all-profiles concern. The bulk-update fix in Finding 2 continues the same-token pattern without comment. |
| c14 | Output notes that `reset_token` appears to be stored in plaintext on the profile and recommends hashing the token at rest (storing only a hash, comparing on redemption) | PARTIAL | Finding 5 (HIGH): 'The raw token is stored in the database' with hashlib.sha256 fix showing hashing at write and comparison at redemption. |
| c15 | Output flags the absence of a token expiry / time-to-live on the reset token as a security concern | PARTIAL | Finding 6 (HIGH): 'Tokens never expire. A token issued today is valid indefinitely' with timezone.now() + timedelta(hours=1) fix. |
| c16 | Output calls out that emails are sent synchronously inside the request handler (blocking the response, no retry) and suggests offloading to a background task or queue | PARTIAL | Finding 8 (MEDIUM): 'Email sending is synchronous inside the request handler' with Celery (.delay()) and Django-RQ (enqueue) fixes. |
| c17 | Output includes a "Positive Observations" or "Questions for the Author" section consistent with the agent's defined output format, not only findings | PARTIAL | Both 'Positive Observations' (3 items including secrets.token_urlsafe praise) and 'Questions for the Author' (5 questions) sections are present. |

### Notes

The review is thorough and well-structured, correctly identifying all major security flaws with precise citations and concrete fixes. The only miss is c13: the output never flags that one token is shared across all linked profiles, and its own bulk-update fix perpetuates the pattern without comment.
