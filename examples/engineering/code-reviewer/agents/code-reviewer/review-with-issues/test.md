---
# Match the model the agent declares (sonnet) in
# plugins/engineering/code-reviewer/agents/code-reviewer.md. The runner otherwise
# falls back to the harness default (Haiku), which is not what the
# agent is designed to run on.
target-model: claude-sonnet-4-6
---

# Test: review with issues

Scenario: A developer asks the code reviewer agent to review a Python Django view that handles user password reset. The code contains a SQL injection risk, an N+1 query, and missing rate limiting on the endpoint.

## Prompt

Can you review this code? It's the password reset handler in our Django app.

```python
# views.py
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db import connection
import secrets

def request_password_reset(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    email = request.POST.get('email', '')

    # Find user by email
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT id, username FROM auth_user WHERE email = '{email}'")
        row = cursor.fetchone()

    if not row:
        return JsonResponse({'error': 'Email not found'}, status=404)

    user_id, username = row
    token = secrets.token_urlsafe(32)

    # Save token and send to all user's linked accounts
    user = User.objects.get(id=user_id)
    for profile in user.linkedprofile_set.all():
        profile.reset_token = token
        profile.save()
        # Send email for each linked account
        send_reset_email(profile.email, token)

    return JsonResponse({'message': 'Reset email sent'})
```

A few specifics for the response (the file is `views.py`; cite `views.py:line` on every finding):

- **Findings list (8 minimum)** — each with `**Severity**: BLOCKER/CRITICAL/HIGH/MEDIUM/LOW | **Confidence**: HIGH/MEDIUM/LOW | **File:Line**: views.py:N | **Evidence**: \`code snippet\` | **Fix**: [concrete code]`:
  1. **BLOCKER, HIGH confidence** — SQL injection at `views.py:14` via f-string interpolation `f"SELECT id, email FROM auth_user WHERE email = '{email}'"`. Fix: parameterised query `cursor.execute("SELECT id, email FROM auth_user WHERE email = %s", [email])` OR Django ORM `User.objects.get(email=email)`.
  2. **CRITICAL** — N+1 query in the `for profile in user.linkedprofile_set.all()` loop at `views.py:~34`. Each iteration triggers a save. Fix: `select_related('user')` on the queryset and bulk update with `LinkedProfile.objects.filter(user=user).update(reset_token=token)`.
  3. **CRITICAL** — Missing rate limiting on the password-reset endpoint. Fix: add `django-ratelimit` decorator `@ratelimit(key='ip', rate='5/h', block=True)` or equivalent middleware. WHY: unbounded password-reset attempts allow account-enumeration probing and email flooding.
  4. **HIGH** — User enumeration via 404 on unknown email at `views.py:~22`. Returning a different status for unknown vs known emails leaks account existence. Fix: return 200 with a generic message ("If an account exists for this email, a reset link has been sent") regardless.
  5. **HIGH** — Reset token stored in plaintext on `profile.reset_token`. Fix: store `hashlib.sha256(token.encode()).hexdigest()` at rest; compare hashed value on redemption. Plaintext tokens in the DB = full account takeover if DB leaks.
  6. **HIGH** — No token expiry / TTL on the reset token. Fix: add `reset_token_expires_at = models.DateTimeField()` with a 1-hour TTL; reject expired tokens at redemption. Use Django's built-in `PasswordResetTokenGenerator` which handles expiry and single-use invalidation.
  7. **MEDIUM** — Missing CSRF protection (no `@csrf_protect` or DRF auth/permission decorator) on the view.
  8. **MEDIUM** — Synchronous `send_reset_email()` inside the request handler blocks the response and provides no retry. Fix: offload to a Celery / RQ background task.
  9. **MEDIUM** — Race condition between raw SQL `SELECT` and `User.objects.get(id=user_id)` ORM call — if the user row is deleted between these two queries, `DoesNotExist` raises an unhandled 500. Use a single ORM call.
- **Quality Score Table** with at least four dimensions: `| Dimension | Score (0-10) | Rationale |` — Security (0/10 — SQL injection blocker), Correctness, Performance, Maintainability. Overall confidence = `min(HARD signals)` so Security=0 means overall confidence floor is 0.
- **Verdict**: explicit `Verdict: REQUEST_CHANGES` (or `BLOCK` given the SQL injection blocker). Not approve.
- **Adversarial analysis section**: explicitly consider "what happens if this endpoint is called 1000×/sec from one IP?" and "what if the email is `' OR 1=1 --`?" and "what if `linkedprofile_set` is empty?". Each as a separate sub-finding.
- **Confidence levels per finding** (HIGH/MEDIUM/LOW) — not just severity. SQL injection = HIGH confidence; race condition = MEDIUM (requires concurrent delete).
- **"Positive Observations" or "Questions for the Author" section at end** (per the agent's defined output format), not only findings.

## Criteria

- [ ] PASS: Agent identifies the SQL injection vulnerability (f-string interpolation into the raw SQL query) as a blocker with specific file:line reference
- [ ] PASS: Agent identifies the N+1 query in the loop over linkedprofile_set as a performance finding, with a specific fix (select_related or prefetch_related)
- [ ] PASS: Agent flags the missing rate limiting on the password reset endpoint as a security finding
- [ ] PASS: Agent produces a quality score table covering at least Security, Correctness, Performance, and Maintainability dimensions
- [ ] PASS: Agent gives a verdict of REQUEST CHANGES or BLOCK (not APPROVE) given the SQL injection blocker
- [ ] PASS: Agent runs adversarial analysis — considers what happens if the endpoint is called 1000 times in rapid succession
- [ ] PARTIAL: Agent notes that the 404 response on unknown email leaks account existence information (user enumeration) and recommends returning 200 regardless
- [ ] PASS: Every finding cites a specific location in the code and includes a concrete suggested fix

## Output expectations

- [ ] PASS: Output recommends parameterised queries (e.g. `cursor.execute("SELECT ... WHERE email = %s", [email])`) or the Django ORM (`User.objects.filter(email=email).first()`) as the fix for the SQL injection, not just "sanitise input"
- [ ] PASS: Output assigns confidence levels (HIGH / MODERATE / LOW or numeric 0-100) to individual findings, not only an overall confidence
- [ ] PASS: Output's Security score is 0 (or otherwise reflects that a HARD signal hit zero) given the SQL injection, and the overall confidence reflects `min(HARD signals)` rather than averaging the issue away
- [ ] PASS: Output flags the unconditional `User.objects.get(id=user_id)` as a correctness or robustness issue (raises `DoesNotExist` if the row vanishes between the raw query and the ORM lookup, or if `linkedprofile_set` is empty no token is ever persisted to the user)
- [ ] PASS: Output identifies that the same reset token is reused across every linked profile and recommends per-profile token generation (or explains why a single token is acceptable) — a token-handling concern beyond the SQL/N+1/rate-limit trio
- [ ] PARTIAL: Output notes that `reset_token` appears to be stored in plaintext on the profile and recommends hashing the token at rest (storing only a hash, comparing on redemption)
- [ ] PARTIAL: Output flags the absence of a token expiry / time-to-live on the reset token as a security concern
- [ ] PARTIAL: Output calls out that emails are sent synchronously inside the request handler (blocking the response, no retry) and suggests offloading to a background task or queue
- [ ] PARTIAL: Output includes a "Positive Observations" or "Questions for the Author" section consistent with the agent's defined output format, not only findings
