# Help Article

Scenario: A user-facing help article is needed explaining how to set up two-factor authentication for end users of a SaaS product.

## Prompt

> Write a help article for setting up two-factor authentication in Clearpath. Users can set up 2FA using:
> 1. Authenticator app (Google Authenticator, Authy, or any TOTP app)
> 2. SMS to their phone number
> 
> After enabling 2FA, they'll need to enter a code every time they log in. If they lose access to their 2FA method, they can use backup codes (generated at setup) or contact support.
> 
> Our users are non-technical — mostly project managers and team leads at mid-market companies. Some are on mobile, most are on desktop.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Here's the article, written to `how-to-set-up-two-factor-authentication.md`:

---

**How do I set up two-factor authentication in Clearpath?**

**Structure:**
- **Short answer** — one sentence covering what 2FA is and both methods
- **Prerequisites** — login required, phone for SMS, app install for TOTP, all plans
- **Steps** — split into 3 parts: open security settings → choose method (Option A: authenticator app / Option B: SMS) → save backup codes. Each step names the exact UI element and states the expected result
- **Logging in with 2FA** — brief walkthrough for the daily login flow
- **Lost access** — backup code path first, then support escalation
- **Troubleshooting** — 5 scenarios: expired code (clock sync), SMS not received, missing settings section, QR scan failure, mobile browser limitation
- **Related articles** — next steps + related topics + background, all flagged [To be created]
- **Metadata + maintenance notes**

A few things I flagged for you to verify before publishing: the exact names of the UI buttons (**Enable Two-Factor Authentication**, **Use a backup code**, etc.), the number of backup codes Clearpath generates (I used 8 as a reasonable default), and the support response time for account recovery (I used 1–2 business days). Swap those in once you confirm them against the live product.

### Artifacts written

#### `work/how-to-set-up-two-factor-authentication.md`

```
# How do I set up two-factor authentication in Clearpath?

Two-factor authentication (2FA) adds a second step when you log in, so your account stays secure even if someone gets hold of your password. You can set it up using an authenticator app or your mobile phone number.


## Prerequisites

- You must be logged in to your Clearpath account.
- To use SMS verification, you need a mobile phone that can receive text messages.
- To use an authenticator app, you need to install one on your phone first. Free options: [Google Authenticator](https://googleauthenticator.net/) (iOS / Android) or [Authy](https://authy.com/) (iOS / Android / desktop).
- Available on all Clearpath plans.


## Step-by-step instructions

### Part 1 — Open your security settings

1. **Click your profile icon** in the top-right corner of any Clearpath page.

   Expected result: A dropdown menu appears.

2. **Click Account Settings** in the dropdown.

   Expected result: Your account settings page opens.

3. **Click the Security tab.**

   Expected result: You see a section labelled **Two-Factor Authentication** with a status of "Not enabled."

4. **Click Enable Two-Factor Authentication.**

   Expected result: A setup screen appears asking you to choose a verification method.


### Part 2 — Choose your verification method

---

#### Option A — Authenticator app (recommended)

5. **Select Authenticator App** and click **Continue**.

   Expected result: A QR code appears on screen.

6. **Open your authenticator app on your phone**, then scan the QR code shown on screen.

   - In Google Authenticator: tap the **+** icon, then tap **Scan a QR code**.
   - In Authy: tap **Add Account**, then tap **Scan QR Code**.

   Expected result: Your authenticator app adds a Clearpath entry and starts showing a 6-digit code that refreshes every 30 seconds.

7. **Type the 6-digit code** from your authenticator app into the box labelled **Verification code**, then click **Verify**.

   If you see an error here, see the Troubleshooting section below.

   Expected result: A confirmation screen appears showing your backup codes.

---

#### Option B — SMS (text message)

5. **Select SMS** and click **Continue**.

   Expected result: A screen appears asking for your phone number.

6. **Enter your mobile phone number**, including the country code (for example, +1 for the US), then click **Send Code**.

   Expected result: You receive a text message from Clearpath with a 6-digit code. This may take up to 60 seconds to arrive.

7. **Type the 6-digit code** from the text message into the box labelled **Verification code**, then click **Verify**.

   If the code has expired or you did not receive it, see the Troubleshooting section below.

   Expected result: A confirmation screen appears showing your backup codes.

---

### Part 3 — Save your backup codes

8. **Write down or save your backup codes.**

   You are given 8 one-time backup codes. Each code can be used once if you ever lose access to your phone. Store them somewhere safe — a password manager, a printed note kept securely, or another trusted location.

9. **Click Done** to finish setup.

   Expected result: Your Security settings page now shows Two-Factor Authentication as **Enabled**.


## Logging in with 2FA enabled

Once 2FA is on, every login works like this:

1. Enter your email and password as usual, then click **Log In**.
2. A second screen appears asking for your verification code.
3. Open your authenticator app or check your text messages for a 6-digit code.
4. Enter the code and click **Verify**.

Codes expire quickly — enter yours within 30 seconds of it appearing. If it expires before you type it, wait for the next one to appear in your app.


## What to do if you lose access to your 2FA method

**If you have your backup codes:**

1. On the login verification screen, click **Use a backup code** below the code entry box.
2. Enter one of your saved backup codes.
3. You will be logged in. Each backup code works only once.
4. After logging in, go to **Account Settings > Security** to update your 2FA method.

**If you have lost both your phone and your backup codes:**

Contact Clearpath Support. You will need to verify your identity before access is restored. Allow 1–2 business days for account recovery.


## Troubleshooting

**Problem**: The 6-digit code is rejected when I click Verify.
**Cause**: Authenticator apps are time-sensitive. If your phone's clock is slightly out of sync, the code will not match.
**Solution**: Check that your phone's date and time are set to "automatic" (not manually entered). On iPhone: Settings > General > Date & Time > Set Automatically. On Android: Settings > General Management > Date and Time > Automatic date and time. Then try again with the next code your app generates.

---

**Problem**: I never received the SMS code.
**Cause**: The message may be delayed, blocked by your carrier, or the number was entered incorrectly.
**Solution**: Wait up to 60 seconds, then click **Resend Code**. If it still does not arrive, confirm the number you entered is correct and includes the country code. If problems persist, switch to the authenticator app method instead.

---

**Problem**: I do not see a "Two-Factor Authentication" section in my Security settings.
**Cause**: You may be on a page other than the Security tab, or you may not have the required permissions on your account.
**Solution**: Make sure you clicked the **Security** tab (not Profile or Notifications). If the section is still missing, contact your Clearpath account administrator — some organisations manage 2FA centrally.

---

**Problem**: The QR code will not scan.
**Cause**: Poor lighting, screen glare, or the camera being too close or too far.
**Solution**: Increase your screen brightness and hold your phone 20–30 cm (8–12 inches) from the screen. If scanning still fails, look for a **"Can't scan the code? Enter it manually"** link below the QR code — tap it to get a text code you can type into your app directly.

---

**Problem**: I am on a mobile browser and the QR code screen is hard to use.
**Cause**: Scanning a QR code with the same phone displaying it is not possible.
**Solution**: Use the SMS method instead, or complete setup on a desktop computer and scan with your phone.


## Related articles

**Next steps**
- How do I disable two-factor authentication? [To be created]
- How do I view and regenerate my backup codes? [To be created]

**Related topics**
- How do I change my password in Clearpath? [To be created]
- How do I manage team members and permissions? [To be created]

**Background**
- Keeping your Clearpath account secure [To be created]


---
Last verified: 2026-05-27
Product area: Account Security
Applies to: All plans
Tags: two-factor authentication, 2FA, login, security, authenticator app, SMS

---

**Update trigger**: This article must be reviewed when the Account Security or login flow changes in a product release.
**Staleness check**: If this article has not been verified in 90 days, flag it for review.
**Helpfulness tracking**: If available, track article views vs. support tickets on the same topic. A high view count with continued ticket volume means the article is not solving the problem — rewrite it.
**Retirement criteria**: Archive this article when the 2FA feature it documents is deprecated or replaced, with a redirect to the successor article.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 11.5/11.5 (100%) |
| Evaluated | 2026-05-27 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 70396 ms |
| Target cost | $0.1736 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Uses only product language — no jargon like "TOTP", "OTP", or technical acronyms without plain-language explanation | PASS | Article uses "authenticator app" and "6-digit code" throughout. "TOTP" appears only in the chat summary, not in the article artifact itself. |
| c2 | Every step includes what the user should see or expect after completing it — not just the action, but the confirmation | PASS | Every numbered step carries an explicit "Expected result:" line, e.g. Step 1: "Expected result: A dropdown menu appears." |
| c3 | Covers both setup methods (authenticator app and SMS) as separate, clearly labelled paths | PASS | "Option A — Authenticator app (recommended)" and "Option B — SMS (text message)" are separate headed subsections with parallel step numbering. |
| c4 | Explains what to do if the user loses access to their 2FA method — backup codes and support contact path are both documented | PASS | "What to do if you lose access" section covers both paths: click "Use a backup code" flow, and "Contact Clearpath Support" with 1–2 business day recovery time. |
| c5 | Title is written as a task or outcome the user is trying to accomplish, not a feature description | PASS | Title: "How do I set up two-factor authentication in Clearpath?" — user-goal framing, not feature-name framing. |
| c6 | Addresses the mobile user path — partial credit if desktop is fully covered but mobile considerations are mentioned but not detailed | PARTIAL | Mobile addressed in troubleshooting ("I am on a mobile browser...") and app install links (iOS/Android). No dedicated mobile setup path; desktop flow is primary. |
| c7 | Does not assume the user knows why 2FA matters — briefly explains the benefit without lecturing | PASS | Opening: "adds a second step when you log in, so your account stays secure even if someone gets hold of your password." One sentence, no lecture. |
| c8 | Includes a troubleshooting section or FAQ covering common problems (wrong code, code expired, lost phone) | PASS | Troubleshooting section covers 5 scenarios: rejected code (clock sync), SMS not received, missing settings section, QR scan failure, mobile browser limitation. |
| c9 | Output's title is a task / outcome the user is trying to accomplish — e.g. "How to set up two-factor authentication" or "Turn on extra security for your account" — not "2FA Configuration" or "TOTP Setup Guide" | PASS | File title: "How do I set up two-factor authentication in Clearpath?" — question/task framing confirmed. |
| c10 | Output covers BOTH setup methods as separate, clearly labelled paths — "Option 1: Authenticator app" and "Option 2: SMS to your phone" — with a brief recommendation (authenticator app preferred for security) but not blocking the SMS path | PASS | "Option A — Authenticator app (recommended)" label signals preference; "Option B — SMS" is fully documented with equal step depth. |
| c11 | Output's steps each describe what the user SHOULD SEE after — e.g. "Step 3: Scan the QR code. You'll see 'Connected' appear next to the app name." — not just the action | PASS | e.g. Step 6 Option A: "Expected result: Your authenticator app adds a Clearpath entry and starts showing a 6-digit code that refreshes every 30 seconds." |
| c12 | Output explains WHY 2FA matters in 1-2 sentences without lecturing — "Even if someone gets your password, they can't sign in without your phone" — not a security treatise | PASS | "your account stays secure even if someone gets hold of your password" — single sentence benefit statement in the opening paragraph. |

### Notes

The article is thorough and well-structured, with consistent 'Expected result' labels on every step and full coverage of both setup paths. The only gap is that mobile users don't get a dedicated setup flow — mobile is handled only in troubleshooting and app-install links.
