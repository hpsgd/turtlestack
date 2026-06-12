# Groomed candidate queue — Sprint 14 refinement

Output of a prior `groom-backlog` solo audit pass. Items are pre-classified and
RICE-ordered. This is the top of the ready/needs-refinement queue going into the
team refinement event.

Team context: 5 developers, two-week sprint. (Use this to set the capacity budget.)

## Candidate items (priority order from the groomed queue)

1. **[STORY] User can reset their password via email link**
   - As a user, I want to reset my password from the login screen so I can get back in if I forget it.
   - Acceptance criteria: request reset from login screen; receive email with a single-use link; link expires after 1 hour; set a new password meeting the policy.
   - Estimate: 3 points. Traces to PRD `auth-self-service` (success metric: reduce password-reset support tickets 40%).
   - 3 amigos: PO, engineer, QA all reviewed in groom pass. No open clarifications.

2. **[STORY] Account settings overhaul**
   - As a user, I want to manage my profile, notification preferences, connected apps, billing details, and security settings all from one redesigned settings area.
   - Estimate: "big — maybe 20+ points, hard to say." Traces to roadmap theme `account-management`.
   - Note from groom pass: flagged as likely too large for one sprint; candidate for a behaviour split.

3. **[STORY] Show last-login timestamp on the security tab**
   - As a user, I want to see when my account was last accessed so I can spot suspicious activity.
   - Acceptance criteria: last-login time shown on the security tab; shows "never" if no prior login.
   - Estimate: 2 points. Depends on the security tab existing — which is part of item 2 (Account settings overhaul).
   - Traces to PRD `auth-self-service`.

4. **[STORY] Export account data to PDF for compliance requests**
   - As a user, I want to export all my account data so I can respond to a data-access request.
   - Acceptance criteria: export produces a PDF AND a CSV AND emails it to the account owner.
   - Estimate: "5 points, but the legal team hasn't confirmed which fields are in scope for a data-access export."
   - Blocked-by note from groom pass: waiting on legal sign-off on the field list.

5. **[STORY] User can enable TOTP two-factor authentication**
   - As a user, I want to turn on two-factor auth with an authenticator app so my account is more secure.
   - Acceptance criteria: scan QR to enrol; verify with a 6-digit code; show recovery codes once; require a code at next login.
   - Estimate: 5 points. Traces to PRD `auth-self-service` (success metric: 25% of accounts on 2FA within 90 days).
   - 3 amigos reviewed. No open clarifications, no dependencies.
