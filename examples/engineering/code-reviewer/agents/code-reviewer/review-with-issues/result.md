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

Here is the full review of `views.py`.

---

## Code Review — `views.py`: `request_password_reset`

**Verdict: BLOCK** — one SQL injection blocker prevents approval regardless of other findings.

---

## Findings

**Finding 1**
**Severity**: BLOCKER | **Confidence**: HIGH | **File:Line**: `views.py:15`
**Evidence**: `cursor.execute(f"SELECT id, username FROM auth_user WHERE email = '{email}'")`
**Impact**: Attacker submits `' OR '1'='1` as email, returns the first row in the table. Submit `'; DROP TABLE auth_user; --` for full DDL access (database-user permitting). No exploit chaining required — this is directly reachable from the public internet.
**Fix**:
```python
# Option A — parameterised raw SQL
cursor.execute("SELECT id, username FROM auth_user WHERE email = %s", [email])

# Option B — preferred: drop the raw query entirely
try:
    user = User.objects.get(email=email)
except User.DoesNotExist:
    user = None
```

---

**Finding 2**
**Severity**: CRITICAL | **Confidence**: HIGH | **File:Line**: `views.py:19`
**Evidence**: `return JsonResponse({'error': 'Email not found'}, status=404)`
**Impact**: A 404 vs 200 distinction lets an attacker enumerate valid accounts silently — no rate limit needed, just `curl` with a wordlist.
**Fix**:
```python
# Return 200 regardless — don't reveal whether the email exists
if not row:
    return JsonResponse({'message': 'If an account exists for this email, a reset link has been sent'})
```

---

**Finding 3**
**Severity**: CRITICAL | **Confidence**: HIGH | **File:Line**: `views.py:7` (entire function)
**Evidence**: No rate-limiting decorator or middleware present.
**Impact**: 1,000 req/s from one IP floods any linked-profile inboxes, and iterates the account-enumeration check for free.
**Fix**:
```python
from django_ratelimit.decorators import ratelimit

@ratelimit(key='post:email', rate='5/h', block=True)
@ratelimit(key='ip', rate='20/h', block=True)
def request_password_reset(request):
    ...
```
Key on `post:email` as well as IP to prevent distributed enumeration with rotating addresses.

---

**Finding 4**
**Severity**: HIGH | **Confidence**: HIGH | **File:Line**: `views.py:27–28`
**Evidence**:
```python
for profile in user.linkedprofile_set.all():
    profile.reset_token = token
    profile.save()
```
**Impact**: N+1 writes — one `UPDATE` per profile. With 50 linked profiles this is 50 round-trips inside a single HTTP request.
**Fix**:
```python
user.linkedprofile_set.all().update(reset_token=hashed_token, reset_token_expires_at=expiry)
```
Keep the loop only for `send_reset_email` calls after the bulk update.

---

**Finding 5**
**Severity**: HIGH | **Confidence**: HIGH | **File:Line**: `views.py:27`
**Evidence**: `profile.reset_token = token` — raw token written to the column.
**Impact**: A DB dump, a rogue DBA, or a SQL injection read (`UNION SELECT reset_token FROM ...`) hands the attacker a live, redeemable token that takeovers every linked account.
**Fix**:
```python
import hashlib
hashed = hashlib.sha256(token.encode()).hexdigest()
# store hashed; return raw token in the email only
profile.reset_token = hashed
```
On redemption: `hashlib.sha256(submitted_token.encode()).hexdigest() == profile.reset_token`.

---

**Finding 6**
**Severity**: HIGH | **Confidence**: HIGH | **File:Line**: `views.py:27`
**Evidence**: No `reset_token_expires_at` field assigned.
**Impact**: A token stolen from the DB (or from an old email) remains valid forever. Standard threat model: tokens must be single-use and time-bounded.
**Fix**:
```python
from django.utils import timezone
from datetime import timedelta

expiry = timezone.now() + timedelta(hours=1)
LinkedProfile.objects.filter(user=user).update(
    reset_token=hashed_token,
    reset_token_expires_at=expiry,
)
```
Or use Django's built-in `PasswordResetTokenGenerator`, which encodes expiry and invalidates after use by incorporating the password hash.

---

**Finding 7**
**Severity**: HIGH | **Confidence**: MEDIUM | **File:Line**: `views.py:25`
**Evidence**: Raw SQL on line 15 → ORM `User.objects.get(id=user_id)` on line 25 — two separate DB round-trips with no transaction boundary.
**Impact**: If the user row is hard-deleted between lines 16 and 25 (another request, admin action, cascade delete), `User.DoesNotExist` propagates as an unhandled 500. MEDIUM confidence because concurrent deletes are uncommon, but the failure mode is a crash, not a graceful error.
**Fix**: Eliminate the raw SQL entirely (see Finding 1 Fix Option B) and issue a single ORM call wrapped in `try/except User.DoesNotExist`.

---

**Finding 8**
**Severity**: HIGH | **Confidence**: HIGH | **File:Line**: `views.py:26–30`
**Evidence**:
```python
for profile in user.linkedprofile_set.all():
    ...
    send_reset_email(profile.email, token)
```
**Impact**: The same raw token is emailed to every linked profile. Any single compromised inbox — an old employer's account, a defunct alias — gives full access to the primary account. Users with many linked profiles have a much larger attack surface than they know.
**Fix**: Design intent needs clarification (see Questions below), but at minimum: each profile should receive its own token, or only the primary/verified profile should receive the reset link.

---

**Finding 9**
**Severity**: MEDIUM | **Confidence**: HIGH | **File:Line**: `views.py:7`
**Evidence**: No `@csrf_protect` decorator; no `@require_POST` or DRF permission class.
**Impact**: A third-party page can silently POST to this endpoint on behalf of a logged-in user if `SameSite` cookie settings are lax. Django's global CSRF middleware covers session-authenticated views but is commonly disabled on APIs.
**Fix**:
```python
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

@csrf_protect
@require_POST
def request_password_reset(request):
    ...
```
If this is an API endpoint with token auth, document the explicit exemption.

---

**Finding 10**
**Severity**: MEDIUM | **Confidence**: HIGH | **File:Line**: `views.py:30`
**Evidence**: `send_reset_email(profile.email, token)` — called synchronously inside the request handler.
**Impact**: If the mail server is slow or unreachable, the HTTP response blocks until timeout. No retry on transient failures. Under load, this exhausts worker threads.
**Fix**:
```python
send_reset_email.delay(profile.email, token)  # Celery task
```
Or Django-Q / RQ equivalent. The view returns immediately; delivery retries are the task queue's responsibility.

---

**Finding 11**
**Severity**: MEDIUM | **Confidence**: HIGH | **File:Line**: `views.py:15, 21`
**Evidence**: SQL selects `username` → unpacked as `user_id, username = row` → `username` is never referenced again.
**Impact**: Dead variable. If the raw SQL is ever partially edited (e.g. column renamed), silent mismatch — the unpacking will silently pick the wrong column. Confusion for the next reader.
**Fix**: Remove the dead select; use only `SELECT id FROM auth_user WHERE email = %s`, or better, the ORM (see Finding 1).

---

**Finding 12**
**Severity**: LOW | **Confidence**: HIGH | **File:Line**: `views.py:11`
**Evidence**: `email = request.POST.get('email', '')`
**Impact**: An empty string `''` passes through to the SQL query (and post-fix, to the ORM). Django's `User.objects.get(email='')` won't raise for empty emails if any user has an empty email field. Add basic format validation to fail fast.
**Fix**:
```python
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

email = request.POST.get('email', '').strip()
try:
    validate_email(email)
except ValidationError:
    return JsonResponse({'error': 'Invalid email'}, status=400)
```

---

## Quality Score Table

| Dimension | Score (0–10) | Rationale |
|---|---|---|
| **Security** | 0/10 | SQL injection blocker alone floors this. Plus: enumeration, no rate-limit, plaintext tokens, no expiry, CSRF. |
| **Correctness** | 3/10 | Race condition between raw SQL and ORM; silent no-op when `linkedprofile_set` is empty (returns 200 but sends nothing); dead `username` variable. |
| **Performance** | 3/10 | N+1 writes in the profile loop; synchronous email blocks the thread; two separate DB round-trips where one would do. |
| **Maintainability** | 4/10 | Raw SQL for something the ORM handles natively adds needless complexity; mixed raw-SQL + ORM pattern is confusing; no type hints; no docstring on a security-sensitive function. |
| **Overall** | 0/10 | `min(security)` = 0. No other dimension can raise the floor while the blocker is open. |

---

## Adversarial Analysis

**Scenario A — 1,000 req/s from one IP**
No rate limit → all requests reach the DB. Each request that hits a real email triggers N profile saves + N synchronous `send_reset_email` calls. At scale: DB write pressure from N+1 saves, mail-server saturation from unbounded outbound volume, and thread exhaustion from synchronous send. The endpoint becomes a self-DoS amplifier: one external attacker causes internal resource collapse. The fix chain is: rate-limit → async email → bulk update.

**Scenario B — Email is `' OR 1=1 --`**
The f-string produces:
```sql
SELECT id, username FROM auth_user WHERE email = '' OR 1=1 --'
```
`fetchone()` returns the first row in `auth_user` — typically the oldest or lowest-ID account (often an admin). The code then generates a reset token for that account, stores it across all of that account's linked profiles, and emails it. The attacker gets a valid password-reset link for an account they never knew existed, without knowing any credentials. Full account takeover in one unauthenticated POST.

**Scenario C — `linkedprofile_set` is empty**
The `for` loop body never executes. No token is stored anywhere. No email is sent. The function returns `{'message': 'Reset email sent'}` — a lie. The user sees a success message, waits for an email that never arrives, and has no recourse. Depending on UX expectations this is a silent failure masquerading as success. Fix: check `profiles.exists()` before the loop, or handle the zero-profile case explicitly.

---

## Positive Observations

1. `secrets.token_urlsafe(32)` is the right primitive — cryptographically secure, correct entropy, correct module. Good call avoiding `random` or `uuid4`.
2. The method guard (`if request.method != 'POST'`) is present, which is a correct baseline (though `@require_POST` is cleaner).
3. The overall structure — find user, generate token, store, notify — is a sensible skeleton. The security properties around each step are the problem, not the flow itself.

---

## Questions for the Author

1. **Intent of linked profiles**: Should a password reset invalidate *all* linked profiles' tokens or only the one whose email was submitted? Sending one token to all inboxes looks like it conflates "notify all" with "reset all" — what's the intended UX?
2. **`send_reset_email` defined where?** It's not imported in the snippet. Is it synchronous SMTP, or is there already a task queue in the project that it wraps?
3. **`LinkedProfile.reset_token` schema**: Is this an existing column or a new one? If existing, what is its current length — a 43-character `token_urlsafe(32)` output won't fit in a `VARCHAR(32)` column.
4. **Is this endpoint public?** If it's behind authentication it narrows the SQL injection blast radius; if it's fully unauthenticated (typical for password resets) the BLOCKER is maximum severity.
5. **Django version + `PasswordResetTokenGenerator`**: Django ships a battle-tested token generator that handles expiry, single-use invalidation, and secure comparison. Was there a reason to roll a custom one rather than subclassing it?

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.5/14.5 (100%) |
| Evaluated | 2026-07-23 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 94914 ms |
| Target cost | $0.1919 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent identifies the SQL injection vulnerability (f-string interpolation into the raw SQL query) as a blocker with specific file:line reference | PASS | Finding 1: 'Severity: BLOCKER \| Confidence: HIGH \| File:Line: views.py:15' with evidence showing the exact f-string interpolation. |
| c2 | Agent identifies the N+1 query in the loop over linkedprofile_set as a performance finding, with a specific fix (select_related or prefetch_related) | PASS | Finding 4 at views.py:27-28 identifies N+1 writes; fix uses bulk update: 'user.linkedprofile_set.all().update(reset_token=hashed_token, ...)'. |
| c3 | Agent flags the missing rate limiting on the password reset endpoint as a security finding | PASS | Finding 3: 'Severity: CRITICAL \| File:Line: views.py:7 (entire function)' with @ratelimit decorator fix keyed on both IP and post:email. |
| c4 | Agent produces a quality score table covering at least Security, Correctness, Performance, and Maintainability dimensions | PASS | Quality Score Table has Security (0/10), Correctness (3/10), Performance (3/10), Maintainability (4/10), and Overall (0/10) rows. |
| c5 | Agent gives a verdict of REQUEST CHANGES or BLOCK (not APPROVE) given the SQL injection blocker | PASS | 'Verdict: BLOCK — one SQL injection blocker prevents approval regardless of other findings.' at the top of the review. |
| c6 | Agent runs adversarial analysis — considers what happens if the endpoint is called 1000 times in rapid succession | PASS | Scenario A: '1,000 req/s from one IP' — discusses DB write pressure, mail-server saturation, thread exhaustion, and self-DoS amplification. |
| c7 | Agent notes that the 404 response on unknown email leaks account existence information (user enumeration) and recommends returning 200 regardless | PARTIAL | Finding 2 at views.py:19: '404 vs 200 distinction lets an attacker enumerate valid accounts silently' with fix returning 200 generic message. |
| c8 | Every finding cites a specific location in the code and includes a concrete suggested fix | PASS | All 12 findings include File:Line references and concrete code fixes; e.g. Finding 12 at views.py:11 with validate_email snippet. |
| c9 | Output recommends parameterised queries (e.g. `cursor.execute("SELECT ... WHERE email = %s", [email])`) or the Django ORM (`User.objects.filter(email=email).first()`) as the fix for the SQL injection, not just "sanitise input" | PASS | Finding 1 Fix: 'Option A — cursor.execute("SELECT id, username FROM auth_user WHERE email = %s", [email])' and 'Option B — User.objects.get(email=email)'. |
| c10 | Output assigns confidence levels (HIGH / MODERATE / LOW or numeric 0-100) to individual findings, not only an overall confidence | PASS | Every finding header includes e.g. 'Confidence: HIGH' or 'Confidence: MEDIUM'; Finding 7 uses MEDIUM to note race condition rarity. |
| c11 | Output's Security score is 0 (or otherwise reflects that a HARD signal hit zero) given the SQL injection, and the overall confidence reflects `min(HARD signals)` rather than averaging the issue away | PASS | Security: 0/10; Overall: 0/10 with explicit note 'min(security) = 0. No other dimension can raise the floor while the blocker is open.' |
| c12 | Output flags the unconditional `User.objects.get(id=user_id)` as a correctness or robustness issue (raises `DoesNotExist` if the row vanishes between the raw query and the ORM lookup, or if `linkedprofile_set` is empty no token is ever persisted to the user) | PASS | Finding 7 flags DoesNotExist crash risk; Scenario C addresses empty linkedprofile_set returning false success 'Reset email sent'. |
| c13 | Output identifies that the same reset token is reused across every linked profile and recommends per-profile token generation (or explains why a single token is acceptable) — a token-handling concern beyond the SQL/N+1/rate-limit trio | PASS | Finding 8: 'The same raw token is emailed to every linked profile... each profile should receive its own token, or only the primary/verified profile.' |
| c14 | Output notes that `reset_token` appears to be stored in plaintext on the profile and recommends hashing the token at rest (storing only a hash, comparing on redemption) | PARTIAL | Finding 5: 'raw token written to the column' with hashlib.sha256 fix and redemption comparison instructions. |
| c15 | Output flags the absence of a token expiry / time-to-live on the reset token as a security concern | PARTIAL | Finding 6: 'No reset_token_expires_at field assigned... A token stolen from the DB... remains valid forever.' with 1-hour TTL fix. |
| c16 | Output calls out that emails are sent synchronously inside the request handler (blocking the response, no retry) and suggests offloading to a background task or queue | PARTIAL | Finding 10 at views.py:30: 'called synchronously inside the request handler' blocking workers; fix: 'send_reset_email.delay(profile.email, token)  # Celery task'. |
| c17 | Output includes a "Positive Observations" or "Questions for the Author" section consistent with the agent's defined output format, not only findings | PARTIAL | Both '## Positive Observations' (3 items praising secrets.token_urlsafe, method guard, skeleton) and '## Questions for the Author' (5 items) are present. |

### Notes

The output is comprehensive and exceeds all criteria — 12 findings versus the required 8, adversarial scenarios covering all three requested cases, a min-signal quality table, and both end-sections. No criterion was missed or only partially addressed beyond the PARTIAL ceilings set by the test author.
