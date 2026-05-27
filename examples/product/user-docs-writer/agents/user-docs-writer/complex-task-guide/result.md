# Complex Task Guide

Scenario: A user asks the help-article agent to write a help article for a complex multi-step SSO setup that spans two systems and includes troubleshooting for known failure modes. The audience is IT admins, not developers.

## Prompt

> Write a help article for setting up SSO (SAML 2.0) with Azure AD in our platform. This involves configuring both sides (Azure portal and our admin panel), testing the connection, and troubleshooting common failures like certificate mismatches and attribute mapping errors. Our users are IT admins, not developers.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

The article has been written to `sso-azure-ad-saml-setup.md`. Here's a summary of what it covers:

**Structure**
- **Title**: Phrased as a user search query — "How do I set up single sign-on (SSO) with Azure AD using SAML 2.0?"
- **Short answer**: Self-contained 2-sentence summary for scanners
- **Prerequisites**: Roles in both Azure and our platform, plan tier, domain verification

**16 numbered steps across 3 parts**
- Part 1 (Steps 1–8): Azure portal — enterprise app creation, Basic SAML Configuration, attribute/claims mapping, certificate download, user assignment
- Part 2 (Steps 9–13): Admin panel — metadata import, certificate upload, attribute mapping, save without enabling
- Part 3 (Steps 14–16): Test with a non-admin account before going live

**6 troubleshooting entries** covering the problems you specified:
- ACS/Reply URL mismatch
- Certificate mismatch (including post-rotation scenario)
- User not assigned to Azure app
- Attribute mapping gaps (with tip on inspecting the raw SAML response)
- Clock skew / redirect loop
- Missing SSO settings (wrong role or wrong plan)

**Related articles** grouped as next steps, related topics, and background — all flagged [To be created] since no existing articles were found in the repo.

### Artifacts written

#### `work/sso-azure-ad-saml-setup.md`

```
# How do I set up single sign-on (SSO) with Azure AD using SAML 2.0?

You can connect Azure Active Directory to our platform so your users sign in through your organisation's Azure AD credentials. This guide walks you through configuring both Azure and our admin panel, testing the connection, and resolving the most common problems.

---

## Short answer

Create an enterprise application in the Azure portal, download the SAML signing certificate and metadata, then paste them into **Admin Panel > Security > Single Sign-On**. Once both sides are configured and saved, use the **Test SSO** button to verify the connection before enabling it for all users.

---

## Prerequisites

- **Role in Azure AD**: Global Administrator or Cloud Application Administrator
- **Role in our platform**: Organisation Owner or Administrator
- **Plan tier**: SSO is available on Business and Enterprise plans only
- **Prior steps**: Your organisation's domain must be verified in Azure AD before proceeding

---

## Step-by-step instructions

### Part 1 — Configure Azure AD

1. **Open the Azure portal and navigate to Azure Active Directory**
   Go to [portal.azure.com](https://portal.azure.com), sign in as a Global Administrator or Cloud Application Administrator, then select **Azure Active Directory** from the left navigation.

   Expected result: The Azure Active Directory overview page opens.

2. **Create a new enterprise application**
   Select **Enterprise applications** from the left menu, then click **+ New application** at the top of the page. On the Browse Azure AD Gallery page, click **+ Create your own application**.

   Expected result: A panel opens on the right side of the screen.

3. **Name the application and choose the non-gallery option**
   Enter a name for the application (for example, *Our Platform SSO*). Select **Integrate any other application you don't find in the gallery (Non-gallery)**, then click **Create**.

   Expected result: Azure creates the application and opens its overview page. This may take a few seconds.

4. **Open the SAML configuration**
   In the application's left menu, select **Single sign-on**, then click the **SAML** tile.

   Expected result: The Set up Single Sign-On with SAML page opens, showing five numbered sections.

5. **Enter the Basic SAML Configuration values**
   Click the **Edit** button (pencil icon) in the **Basic SAML Configuration** section. Enter the following values — you can find these in our admin panel under **Admin Panel > Security > Single Sign-On > Setup instructions**:

   - **Identifier (Entity ID)**: Paste the Entity ID shown in our admin panel (example: `https://app.ourplatform.com/saml/metadata`)
   - **Reply URL (Assertion Consumer Service URL)**: Paste the ACS URL shown in our admin panel (example: `https://app.ourplatform.com/saml/acs`)
   - **Sign on URL**: Leave blank unless your users sign in from within Azure. If required, enter `https://app.ourplatform.com/login`

   Click **Save**.

   Expected result: Azure validates and saves the values. If you see a red error banner, check that the URLs are complete and begin with `https://`.

6. **Configure the attribute and claims mapping**
   Click **Edit** in the **Attributes & Claims** section. Verify or set the following required claims:

   | Claim name | Source attribute |
   |---|---|
   | `emailaddress` | `user.mail` |
   | `givenname` | `user.givenname` |
   | `surname` | `user.surname` |
   | `name` (Unique User Identifier) | `user.userprincipalname` |

   If any claim is missing, click **+ Add new claim**, fill in the **Name** and **Source attribute** fields, then click **Save**.

   Expected result: The claims list shows all four rows above. Changes save immediately.

7. **Download the SAML signing certificate**
   In the **SAML Signing Certificate** section, locate the row labelled **Certificate (Base64)** and click **Download**. Save the `.cer` file to your computer.

   Also click the **Copy** icon next to **App Federation Metadata Url** and paste it somewhere handy — you will need it in Part 2.

   Expected result: A `.cer` file downloads to your computer. The metadata URL is a long `https://login.microsoftonline.com/...` address.

8. **Assign users or groups to the application**
   In the application's left menu, select **Users and groups**, then click **+ Add user/group**. Search for and add the users or Azure AD groups who should be able to sign in with SSO.

   Click **Assign** to confirm.

   Expected result: The selected users or groups appear in the Users and groups list. Users not assigned here will be denied access when SSO is enabled.

---

### Part 2 — Configure our admin panel

9. **Open the SSO settings page**
   In our platform, click your organisation name in the top-right corner and select **Admin Panel**. Navigate to **Security > Single Sign-On**.

   Expected result: The Single Sign-On settings page opens, showing the current SSO status as **Disabled**.

10. **Enter the IdP metadata URL**
    In the **Identity Provider Configuration** section, paste the App Federation Metadata URL you copied in Step 7 into the **Metadata URL** field, then click **Import from URL**.

    Expected result: Our platform fetches the metadata automatically and fills in the **IdP Entity ID**, **SSO Login URL**, and **SSO Logout URL** fields. If the import fails, see the Troubleshooting section below.

11. **Upload the signing certificate**
    If the metadata import in Step 10 did not automatically populate the certificate, click **Upload Certificate** and select the `.cer` file you downloaded in Step 7.

    Expected result: A green tick and the certificate thumbprint appear next to the certificate field.

12. **Map the user attributes**
    In the **Attribute Mapping** section, confirm the following mappings match what you configured in Azure (Step 6):

    | Our platform field | Azure AD claim |
    |---|---|
    | Email | `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress` |
    | First name | `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname` |
    | Last name | `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname` |
    | Username | `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name` |

    Adjust any field that does not match, then click **Save attribute mapping**.

    Expected result: A confirmation message reads "Attribute mapping saved."

13. **Save the SSO configuration**
    Click **Save configuration** at the bottom of the page. Do not enable SSO for all users yet — test it first in the next step.

    Expected result: A banner reads "SSO configuration saved. SSO is currently disabled."

---

### Part 3 — Test the connection

14. **Run the built-in SSO test**
    On the **Security > Single Sign-On** page, click **Test SSO connection**.

    Expected result: A new browser tab or pop-up window opens and redirects to the Azure AD login page.

15. **Sign in with a test Azure AD account**
    Sign in using an Azure AD account that is assigned to the enterprise application (from Step 8). Use a non-administrator test account if possible.

    Expected result: After signing in, the pop-up closes and a green banner on the SSO settings page reads "Test successful. SSO is working correctly." If you see an error, do not proceed — see the Troubleshooting section below.

16. **Enable SSO for your organisation**
    Once the test passes, toggle **Enable SSO for all users** to **On**, then click **Save configuration**.

    Expected result: The status indicator changes to **Enabled**. Users will now be redirected to Azure AD when they sign in to our platform.

---

## Troubleshooting

**Problem**: "Metadata import failed" when pasting the App Federation Metadata URL
**Cause**: The metadata URL is inaccessible from our servers, or it was copied with extra whitespace.
**Solution**: Re-copy the URL directly from the Azure portal (Step 7). Ensure there are no leading or trailing spaces. If your network restricts outbound connections, download the metadata XML file directly from Azure (go to the SAML page, click **Download** next to **Federation Metadata XML**) and use the **Upload metadata file** option instead.

---

**Problem**: Test SSO fails with "AADSTS50011: The reply URL specified in the request does not match the reply URLs configured for the application"
**Cause**: The ACS (Reply) URL entered in Azure (Step 5) does not exactly match the value expected by our platform.
**Solution**: Return to the Azure portal, open the enterprise application, go to **Single sign-on > Basic SAML Configuration**, and compare the **Reply URL** field against the ACS URL shown in **Admin Panel > Security > Single Sign-On > Setup instructions**. They must be identical, including `https://`, trailing slashes, and capitalisation. Click **Save** after correcting the value.

---

**Problem**: Test SSO fails with "SAML token signature cannot be validated" or "Certificate mismatch"
**Cause**: The certificate uploaded to our platform does not match the certificate Azure used to sign the SAML assertion. This commonly happens when Azure has rotated its signing certificate.
**Solution**: In the Azure portal, go to the enterprise application, select **Single sign-on**, and check the **SAML Signing Certificate** section. Download the current **Certificate (Base64)** and re-upload it in **Admin Panel > Security > Single Sign-On > Upload Certificate**. If Azure shows multiple active certificates, download the one marked **Active**. Click **Save configuration** after uploading.

---

**Problem**: Users receive a "Your account is not assigned to this application" error in Azure
**Cause**: The user signing in has not been added to the enterprise application in Azure AD (Step 8).
**Solution**: In the Azure portal, open the enterprise application, go to **Users and groups**, and add the user or their group. Assignment changes take effect within 1–2 minutes. If users are in a group, confirm the group assignment is visible in the **Users and groups** list.

---

**Problem**: Attribute mapping error — users can sign in but their name or email is blank in our platform
**Cause**: The claim names in Azure (Step 6) do not match the attribute mapping configured in our admin panel (Step 12). This often happens if Azure sends claims using shortened names rather than the full URI format.
**Solution**: In the Azure portal, open the enterprise application and go to **Single sign-on > Attributes & Claims**. Check the **Name** column for each claim. If Azure is using short names (e.g., `emailaddress` instead of the full URI), update the **Attribute Mapping** in our admin panel to match. Use the exact string Azure sends. You can inspect the exact claim names by running the test (Step 14–15) and clicking **View raw SAML response** in the result window.

---

**Problem**: SSO redirects loop continuously without completing sign-in
**Cause**: Clock skew — a time difference greater than 5 minutes between our servers and the Azure AD servers can cause SAML assertions to appear expired or not yet valid.
**Solution**: Verify that the computer you are testing on has its system clock synchronised. For server-level clock skew, contact your network administrator to confirm NTP is correctly configured on any on-premises components in the authentication path. You do not need to adjust anything in Azure or our platform — this is a time-sync issue on the network.

---

**Problem**: The SSO settings page is missing or greyed out in our admin panel
**Cause**: Your account does not have the Owner or Administrator role, or your organisation is on a plan that does not include SSO.
**Solution**: Ask an Organisation Owner to grant you the Administrator role under **Admin Panel > Team > Roles**. If SSO is still not visible, contact our support team to confirm your plan includes SSO — it is available on Business and Enterprise plans only.

---

## Related articles

**Next steps**
- How do I configure SCIM provisioning to sync users from Azure AD automatically? [To be created]
- How do I enforce SSO so users cannot bypass it with a password? [To be created]

**Related topics**
- How do I set up SSO with Okta? [To be created]
- How do I set up SSO with Google Workspace? [To be created]

**Background**
- What is SAML 2.0 and how does SSO work? [To be created]
- How do I manage user roles and permissions? [To be created]

---

```
Last verified: 2026-05-27
Product area: Security / Authentication
Applies to: Business and Enterprise plans
Tags: SSO, SAML, Azure AD, single sign-on, authentication
```

---

**Update trigger**: This article must be reviewed when the SSO configuration UI or the SAML attribute mapping fields change in a product release.
**Staleness check**: If this article has not been verified in 90 days, flag it for review.
**Helpfulness tracking**: If available, track article views vs. support tickets on the same topic. A high view count with continued ticket volume means the article is not solving the problem — rewrite it.
**Retirement criteria**: Archive this article when the feature it documents is deprecated, replaced by a redirect to the successor article.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.5/17.0 (85%) |
| Evaluated | 2026-05-27 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 93580 ms |
| Target cost | $0.2509 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Article provides separate labelled paths for each configuration side (Azure portal steps, platform admin steps) | PASS | "Part 1 — Configure Azure AD" (Steps 1–8) and "Part 2 — Configure our admin panel" (Steps 9–13) are explicitly labelled and non-interleaved. |
| c2 | Recovery path is documented for each failure mode mentioned (certificate mismatch, attribute mapping) | PASS | Dedicated troubleshooting entries for "SAML token signature cannot be validated" and "users can sign in but their name or email is blank" both include cause + fix. |
| c3 | Steps are numbered with expected results after each step, not just instructions | PASS | Every step ends with "Expected result:" — e.g. Step 1: "Expected result: The Azure Active Directory overview page opens." |
| c4 | Technical jargon is explained or linked on first use (SAML, IdP, SP, assertion) | PARTIAL | SSO defined as "single sign-on" in title; ACS spelled out as "Assertion Consumer Service URL" in Step 5. SAML, IdP, SP, and assertion-as-concept are not defined or linked. |
| c5 | A verification step confirms the SSO connection works before declaring success | PASS | Part 3 "Test the connection" Steps 14–15: click "Test SSO connection", sign in with a test Azure AD account; expected result is a "Test successful" green banner before Step 16 enables SSO. |
| c6 | Article includes a "before you start" prerequisites section with specific requirements (Azure AD tier, admin permissions, metadata URL) | PARTIAL | Prerequisites section lists Azure AD and platform admin roles and platform plan tier. Azure AD Premium tier requirement and platform metadata URL are absent. |
| c7 | Troubleshooting section is structured as symptom → cause → fix, not a list of tips | PASS | All six troubleshooting entries use explicit "Problem" / "Cause" / "Solution" labels — e.g., the certificate mismatch entry follows this structure exactly. |
| c8 | The article is written for IT admins (procedural, specific) not developers (no code samples unless necessary) | PASS | Procedural numbered steps with portal navigation paths; only URLs like "https://app.ourplatform.com/saml/metadata" appear as illustrative examples, not code. |
| c9 | Output's structure has clearly labelled sections — Prerequisites, Configure Azure AD, Configure the platform, Test the connection, Troubleshooting — with the two configuration sections explicitly distinct (no interleaving) | PASS | Sections: Prerequisites, Part 1 (Azure AD), Part 2 (admin panel), Part 3 (test), Troubleshooting — all clearly delimited with no interleaving between the two config parts. |
| c10 | Output's Azure AD section steps are numbered with screenshots or specific path references — e.g. "1. Sign in to Azure portal at https://portal.azure.com. 2. In the left navigation, select Azure Active Directory → Enterprise applications → New application." — with expected result per step | PASS | Step 1 references portal.azure.com with left-nav path; Step 2 gives exact menu sequence; every step has an "Expected result:" line. |
| c11 | Output's platform side has matching numbered steps — taking the values copied from Azure (Identity Provider URL, Certificate, Entity ID) and pasting them into the corresponding fields in the platform admin panel — with field names exact | PASS | Step 10: paste metadata URL into "Metadata URL" field; Step 11: upload .cer into "Upload Certificate"; Step 12: map attributes with full claim URI strings — all exact field names. |
| c12 | Output explains technical jargon on first use — SAML 2.0 ("a standard for single sign-on"), IdP / SP ("Identity Provider, the system that authenticates users; Service Provider, our platform"), assertion ("the signed message Azure sends back confirming user identity") — without dumbing down for the IT-admin audience | FAIL | None of the specified definitions appear. SAML is used without explanation; IdP appears in Step 10 without a gloss; SP and assertion-as-concept are never defined. |
| c13 | Output's verification step performs an actual end-to-end SSO login attempt — e.g. "open an incognito window, navigate to your platform login URL, click 'Sign in with SSO', enter an Azure-AD-managed test user; you should land on the platform dashboard logged in as that user" | PASS | Steps 14–15: click Test SSO connection → Azure AD login page opens → sign in with an assigned Azure AD test account → expected result is "Test successful" banner completing the full SAML round-trip. |
| c14 | Output's troubleshooting section uses symptom → cause → fix structure for at least the two named failure modes — certificate mismatch (symptom: "SSO error: invalid signature"; cause: cert in platform doesn't match Azure's; fix: re-export and re-upload), attribute mapping (symptom: "user logged in but missing email/name"; cause: claim mappings; fix: configure Azure attribute claims for emailaddress, name) | PASS | Certificate mismatch entry: Problem/Cause/Solution with cert rotation scenario. Attribute mapping entry: Problem "name or email is blank", Cause claim name mismatch, Solution check Azure claims and update mapping. |
| c15 | Output's prerequisites are explicit — Azure AD Premium tier (Free does not support custom SAML), Azure AD Global Administrator role, the platform admin role, the platform's metadata URL or values to provide to Azure | PARTIAL | Global Administrator role and platform admin role are listed. Azure AD Premium tier requirement is entirely absent; metadata URL/values are described in Step 5 but not as a prerequisite. |
| c16 | Output's tone is procedural — single action per step, expected outcome stated, no "feel free to" or "you might want to" hedge language — but not condescending; treats the IT admin as a competent professional | PASS | Steps use imperative voice ("Click", "Enter", "Navigate"); no hedge language found; "Use a non-administrator test account if possible" is the mildest qualifier. |
| c17 | Output addresses the bidirectional nature explicitly — Azure has values that need to come INTO the platform, and the platform has values that need to go INTO Azure (entity ID / ACS URL); the order matters and is shown | PASS | Step 5 sends platform Entity ID/ACS URL → Azure. Steps 10–11 send Azure metadata URL/certificate → platform. Part ordering (Azure first, platform second) encodes the dependency. |
| c18 | Output addresses production cutover guidance — once tested in a staging or test SSO config, how to switch existing users to SSO without locking anyone out (allow password fallback during transition, then enforce SSO) | FAIL | Step 16 simply toggles "Enable SSO for all users" on. No password fallback, no staged rollout, no lock-out risk guidance. Related articles reference "How do I enforce SSO" as [To be created]. |

### Notes

The article is well-structured and thorough on procedural steps, bidirectional configuration flow, and troubleshooting format. The two main gaps are jargon definitions (SAML, IdP, SP, assertion are never explained) and the absence of Azure AD Premium tier as a prerequisite and any production cutover/lock-out guidance.
