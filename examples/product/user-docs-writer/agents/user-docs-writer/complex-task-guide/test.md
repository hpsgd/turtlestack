---
# Match the model the agent declares (sonnet) in
# plugins/product/user-docs-writer/agents/user-docs-writer.md. The runner otherwise
# falls back to the harness default (Haiku), which is not what the
# agent is designed to run on.
target-model: claude-sonnet-4-6
---

# Test: user-docs-writer — complex task guide

Scenario: A user asks the help-article agent to write a help article for a complex multi-step SSO setup that spans two systems and includes troubleshooting for known failure modes. The audience is IT admins, not developers.

## Prompt

Write a help article for setting up SSO (SAML 2.0) with Azure AD in our platform. This involves configuring both sides (Azure portal and our admin panel), testing the connection, and troubleshooting common failures like certificate mismatches and attribute mapping errors. Our users are IT admins, not developers.

## Criteria

- [ ] PASS: Article provides separate labelled paths for each configuration side (Azure portal steps, platform admin steps)
- [ ] PASS: Recovery path is documented for each failure mode mentioned (certificate mismatch, attribute mapping)
- [ ] PASS: Steps are numbered with expected results after each step, not just instructions
- [ ] PASS: Technical jargon is explained or linked on first use (SAML, IdP, SP, assertion)
- [ ] PASS: A verification step confirms the SSO connection works before declaring success
- [ ] PARTIAL: Article includes a "before you start" prerequisites section with specific requirements (Azure AD tier, admin permissions, metadata URL)
- [ ] PASS: Troubleshooting section is structured as symptom → cause → fix, not a list of tips
- [ ] PASS: The article is written for IT admins (procedural, specific) not developers (no code samples unless necessary)

## Output expectations

- [ ] PASS: Output's structure has clearly labelled sections — Prerequisites, Configure Azure AD, Configure the platform, Test the connection, Troubleshooting — with the two configuration sections explicitly distinct (no interleaving)
- [ ] PASS: Output's Azure AD section steps are numbered with screenshots or specific path references — e.g. "1. Sign in to Azure portal at https://portal.azure.com. 2. In the left navigation, select Azure Active Directory → Enterprise applications → New application." — with expected result per step
- [ ] PASS: Output's platform side has matching numbered steps — taking the values copied from Azure (Identity Provider URL, Certificate, Entity ID) and pasting them into the corresponding fields in the platform admin panel — with field names exact
- [ ] PASS: Output explains technical jargon on first use — SAML 2.0 ("a standard for single sign-on"), IdP / SP ("Identity Provider, the system that authenticates users; Service Provider, our platform"), assertion ("the signed message Azure sends back confirming user identity") — without dumbing down for the IT-admin audience
- [ ] PASS: Output's verification step performs an actual end-to-end SSO login attempt — e.g. "open an incognito window, navigate to your platform login URL, click 'Sign in with SSO', enter an Azure-AD-managed test user; you should land on the platform dashboard logged in as that user"
- [ ] PASS: Output's troubleshooting section uses symptom → cause → fix structure for at least the two named failure modes — certificate mismatch (symptom: "SSO error: invalid signature"; cause: cert in platform doesn't match Azure's; fix: re-export and re-upload), attribute mapping (symptom: "user logged in but missing email/name"; cause: claim mappings; fix: configure Azure attribute claims for emailaddress, name)
- [ ] PASS: Output's prerequisites are explicit — Azure AD Premium tier (Free does not support custom SAML), Azure AD Global Administrator role, the platform admin role, the platform's metadata URL or values to provide to Azure
- [ ] PASS: Output's tone is procedural — single action per step, expected outcome stated, no "feel free to" or "you might want to" hedge language — but not condescending; treats the IT admin as a competent professional
- [ ] PASS: Output addresses the bidirectional nature explicitly — Azure has values that need to come INTO the platform, and the platform has values that need to go INTO Azure (entity ID / ACS URL); the order matters and is shown
- [ ] PARTIAL: Output addresses production cutover guidance — once tested in a staging or test SSO config, how to switch existing users to SSO without locking anyone out (allow password fallback during transition, then enforce SSO)
