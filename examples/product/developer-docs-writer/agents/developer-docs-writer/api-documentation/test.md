---
# Match the model the agent declares (sonnet) in
# plugins/product/developer-docs-writer/agents/developer-docs-writer.md. The runner otherwise
# falls back to the harness default (Haiku), which is not what the
# agent is designed to run on.
target-model: claude-sonnet-4-6
---

# Test: API documentation

Scenario: A developer needs docs written for a REST API that handles webhook delivery, including authentication and rate limiting behaviour.

## Prompt


Write documentation for our webhooks API. Here's what it does:

- POST /v1/webhooks — register a new webhook endpoint
- GET /v1/webhooks — list all registered webhooks
- DELETE /v1/webhooks/{id} — remove a webhook
- POST /v1/webhooks/{id}/test — send a test event to verify the endpoint works

Auth: Bearer token in Authorization header. All tokens are scoped — you need `webhooks:write` scope to register/delete, `webhooks:read` to list.

Rate limits: 100 requests/minute per token. Returns 429 with Retry-After header when exceeded.

Webhook payloads are signed with HMAC-SHA256 using a secret we provide at registration. Customers must verify the signature or we recommend rejecting the payload.

Output requirements:

- **Every endpoint section MUST include**:
  - **Complete request example** with ALL required headers (`Authorization: Bearer <token>`, `Content-Type: application/json`, `Idempotency-Key: <uuid>` for POSTs).
  - **Success response example** AND **error response examples** for at minimum **400, 401, 403, 404, 409, 422, 429**. Show the exact JSON body shape per status.
  - **Required scope** explicitly: POST/DELETE → `webhooks:write`, GET → `webhooks:read`.
- **All code examples are syntactically correct and copy-pasteable** — no `<...>` placeholders without convention, no `# ...` ellipsis. Use `<YOUR_TOKEN>` / `<WEBHOOK_ID>` placeholders with a "Replace with..." note on first use.
- **Code examples in 3 languages**: `curl`, JavaScript (`fetch`), Python (`requests`). Each fully runnable.
- **HMAC verification example** in 3 languages with the exact algorithm: `hmac.new(secret, body, hashlib.sha256).hexdigest()` (Python), `crypto.createHmac('sha256', secret).update(body).digest('hex')` (Node), `openssl dgst -sha256 -hmac "$SECRET"` (curl/shell). Compare against the `X-Signature` header.
- **Rate-limit section** documenting the response: 429 status, `Retry-After: <seconds>` header, `X-RateLimit-Remaining`, `X-RateLimit-Reset` headers.
- **Pagination section** for `GET /v1/webhooks`: `limit`, `cursor`, response includes `next_cursor` + `has_more`.
- **Webhooks-specific Quality Checklist** at end:
  ```
  - [ ] Every example was executed against staging before publication
  - [ ] HMAC verification example tested with a known signature pair
  - [ ] All 429-Retry-After examples include the header
  - [ ] All scoped endpoints document the required scope
  ```

A few specifics for the response:

- Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
- Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
- For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
- When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
- Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Criteria


- [ ] PASS: Every endpoint includes a complete request example with all required headers (Authorization, Content-Type) and a realistic request body
- [ ] PASS: Every endpoint documents both success responses and error responses — at minimum: 401 Unauthorized, 403 Forbidden (wrong scope), 429 Too Many Requests, and relevant 4xx for invalid input
- [ ] PASS: Documents the HMAC-SHA256 signature verification process with a working code example in at least one language
- [ ] PASS: Explains token scopes (webhooks:read vs webhooks:write) and which endpoints require which scope
- [ ] PASS: Documents rate limit behaviour including the Retry-After header and how clients should handle 429 responses
- [ ] PASS: Code examples are syntactically correct and copy-pasteable — not pseudocode or placeholder-heavy
- [ ] PARTIAL: Includes a quick-start or authentication section before the endpoint reference — partial credit if auth is documented inline per endpoint but not as a standalone overview
- [ ] PASS: Documents what a webhook payload looks like and how to verify the signature, not just that verification should happen

## Output expectations

- [ ] PASS: Output documents all four endpoints — POST `/v1/webhooks`, GET `/v1/webhooks`, DELETE `/v1/webhooks/{id}`, POST `/v1/webhooks/{id}/test` — with request/response examples per endpoint, not a generic CRUD template
- [ ] PASS: Output's request examples for POST endpoints include the full JSON body — endpoint URL, event types subscribed, custom metadata — not just `{"url": "..."}` placeholder
- [ ] PASS: Output documents 401 (missing/invalid token), 403 (wrong scope — e.g. `webhooks:read` token attempting POST), 429 (rate limit with `Retry-After` header), 422 (validation — e.g. invalid URL), and 404 (deleting a non-existent webhook)
- [ ] PASS: Output's HMAC signature verification example shows actual code in at least one language (Python or Node.js typical) — including extracting the signature from the header, computing HMAC-SHA256 using the secret, and constant-time comparison — runnable, not pseudocode
- [ ] PASS: Output explains the two scopes (`webhooks:read`, `webhooks:write`) and maps each endpoint to its required scope in a table — not just mentioning scopes in prose
- [ ] PASS: Output's rate-limit documentation includes the algorithm semantics (per-token, 100/minute), the response body shape on 429, the `Retry-After` header value semantics, and a recommended client backoff strategy
- [ ] PASS: Output documents the webhook payload structure delivered TO the customer's endpoint — not just the API request structure — including the signed body, the signature header name, and example event types
- [ ] PASS: Output's authentication section appears as an overview before the endpoint reference, explaining Bearer token format and where to obtain tokens — not only inline per endpoint
- [ ] PASS: Output's code examples are syntactically correct and copy-pasteable — no `<your_token_here>` ambiguity that doesn't match runtime expectations, no missing imports
- [ ] PARTIAL: Output addresses webhook delivery semantics — retry policy if the customer's endpoint returns non-2xx, timeout handling, and when a webhook is considered "failed" — important for customers building reliable receivers
