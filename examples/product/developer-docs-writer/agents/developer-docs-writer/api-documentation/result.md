# Api Documentation

Scenario: A developer needs docs written for a REST API that handles webhook delivery, including authentication and rate limiting behaviour.

## Prompt

> Write documentation for our webhooks API. Here's what it does:
> 
> - POST /v1/webhooks — register a new webhook endpoint
> - GET /v1/webhooks — list all registered webhooks
> - DELETE /v1/webhooks/{id} — remove a webhook
> - POST /v1/webhooks/{id}/test — send a test event to verify the endpoint works
> 
> Auth: Bearer token in Authorization header. All tokens are scoped — you need `webhooks:write` scope to register/delete, `webhooks:read` to list.
> 
> Rate limits: 100 requests/minute per token. Returns 429 with Retry-After header when exceeded.
> 
> Webhook payloads are signed with HMAC-SHA256 using a secret we provide at registration. Customers must verify the signature or we recommend rejecting the payload.
> 
> Output requirements:
> 
> - **Every endpoint section MUST include**:
>   - **Complete request example** with ALL required headers (`Authorization: Bearer <token>`, `Content-Type: application/json`, `Idempotency-Key: <uuid>` for POSTs).
>   - **Success response example** AND **error response examples** for at minimum **400, 401, 403, 404, 409, 422, 429**. Show the exact JSON body shape per status.
>   - **Required scope** explicitly: POST/DELETE → `webhooks:write`, GET → `webhooks:read`.
> - **All code examples are syntactically correct and copy-pasteable** — no `<...>` placeholders without convention, no `# ...` ellipsis. Use `<YOUR_TOKEN>` / `<WEBHOOK_ID>` placeholders with a "Replace with..." note on first use.
> - **Code examples in 3 languages**: `curl`, JavaScript (`fetch`), Python (`requests`). Each fully runnable.
> - **HMAC verification example** in 3 languages with the exact algorithm: `hmac.new(secret, body, hashlib.sha256).hexdigest()` (Python), `crypto.createHmac('sha256', secret).update(body).digest('hex')` (Node), `openssl dgst -sha256 -hmac "$SECRET"` (curl/shell). Compare against the `X-Signature` header.
> - **Rate-limit section** documenting the response: 429 status, `Retry-After: <seconds>` header, `X-RateLimit-Remaining`, `X-RateLimit-Reset` headers.
> - **Pagination section** for `GET /v1/webhooks`: `limit`, `cursor`, response includes `next_cursor` + `has_more`.
> - **Webhooks-specific Quality Checklist** at end:
>   ```
>   - [ ] Every example was executed against staging before publication
>   - [ ] HMAC verification example tested with a known signature pair
>   - [ ] All 429-Retry-After examples include the header
>   - [ ] All scoped endpoints document the required scope
>   ```
> 
> A few specifics for the response:
> 
> - Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
> - Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
> - For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
> - When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
> - Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

The documentation is written to `docs/webhooks-api.md`. Here it is in full:

---

# Webhooks API Reference

> **Assumptions documented inline:** Base URL uses `api.example.com` — replace with your actual domain. Token scopes follow `resource:action` format. Webhook IDs use a `wh_<uuid>` prefix. Signing secrets are 64-character hex strings returned once at registration. Default page size is 20; maximum is 100. `Idempotency-Key` is required on all POST requests. The `X-Signature` header carries the HMAC-SHA256 hex digest.

---

## Base URL

```
Production:  https://api.example.com/v1
Staging:     https://api-staging.example.com/v1
```

Versioning strategy: path-based (`/v1/`). Breaking changes are released under a new version prefix; the prior version remains available for a deprecation window.

---

## Authentication

### Bearer token

All endpoints require a Bearer token in the `Authorization` header:

```
Authorization: Bearer <YOUR_TOKEN>
```

> **Replace `<YOUR_TOKEN>`** with the token issued in your dashboard under **Settings → API Tokens**. All subsequent examples use this placeholder.

#### Token scopes

| Scope | Grants |
|---|---|
| `webhooks:read` | List registered webhooks |
| `webhooks:write` | Register new webhooks, delete webhooks, send test events |

**Authentication failure (401):**

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Missing or invalid Bearer token"
  }
}
```

**Insufficient scope (403):**

```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Token does not have the required scope: webhooks:write"
  }
}
```

---

## Rate Limiting

**Limit:** 100 requests per minute, per token.

When the limit is exceeded the API responds with:

```
HTTP/1.1 429 Too Many Requests
Retry-After: 42
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1716825060
```

```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Rate limit exceeded. Retry after 42 seconds."
  }
}
```

| Header | Type | Description |
|---|---|---|
| `X-RateLimit-Remaining` | integer | Requests remaining in the current 60-second window |
| `X-RateLimit-Reset` | integer (Unix timestamp) | UTC timestamp when the window resets and the counter returns to 100 |
| `Retry-After` | integer (seconds) | How long to wait before retrying. Present only on 429 responses. |

All successful responses also include `X-RateLimit-Remaining` and `X-RateLimit-Reset` so you can monitor headroom proactively without waiting for a 429.

---

## Pagination

`GET /v1/webhooks` uses **cursor-based pagination**.

**Request:**

```
GET /v1/webhooks?limit=20&cursor=d2ViaG9va19leGFtcGxlMjAyNjA1Mjc
```

**Response:**

```json
{
  "data": [ "..." ],
  "next_cursor": "d2ViaG9va19leGFtcGxlMjAyNjA1Mjc",
  "has_more": true
}
```

| Field | Type | Description |
|---|---|---|
| `data` | array | Page of webhook objects |
| `next_cursor` | string \| null | Opaque cursor for the next page. `null` when there are no further results. |
| `has_more` | boolean | `true` if more pages exist beyond this one |

| Parameter | Type | Default | Maximum | Description |
|---|---|---|---|---|
| `limit` | integer | 20 | 100 | Results per page |
| `cursor` | string | — | — | Value from a previous response's `next_cursor` |

**Detecting last page:** `has_more: false` or `next_cursor: null`.

Total count is not returned. Cursors are stable across concurrent mutations — items will not appear twice or be skipped if webhooks are added or deleted during pagination.

---

## Error Format

All error responses share a common shape:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable description of what went wrong",
    "details": [
      {
        "field": "url",
        "message": "Must be a valid HTTPS URL"
      }
    ]
  }
}
```

`details` is present only on `400` and `422` responses where field-level information is available.

### Error Code Reference

| HTTP Status | Code | Meaning | Common Cause |
|---|---|---|---|
| 400 | `VALIDATION_ERROR` | Request body or parameters are invalid | Missing required field, wrong type, invalid format |
| 401 | `UNAUTHORIZED` | Authentication failed or missing | Expired token, missing `Authorization` header |
| 403 | `FORBIDDEN` | Authenticated but insufficient permissions | Token missing required scope |
| 404 | `NOT_FOUND` | Resource does not exist | Invalid webhook ID, already deleted |
| 409 | `CONFLICT` | Request conflicts with current state | Webhook URL already registered |
| 422 | `UNPROCESSABLE_ENTITY` | Request is well-formed but semantically invalid | URL is HTTP (not HTTPS), unrecognised event type, endpoint unreachable |
| 429 | `RATE_LIMITED` | Too many requests | Exceeded 100 req/min per token |
| 500 | `INTERNAL_ERROR` | Server error | Bug — contact support |

---

## Endpoints

---

### Register a Webhook

Registers a new endpoint to receive webhook events. Returns the webhook record including the signing secret used to verify payloads. **The `secret` is returned only in this response — store it immediately.**

```
POST /v1/webhooks
```

#### Authentication

Requires Bearer token with **`webhooks:write`** scope.

#### Request Body

```
Content-Type: application/json
```

| Field | Type | Required | Description |
|---|---|---|---|
| `url` | string | Yes | HTTPS URL to receive webhook event POSTs. Maximum 2048 characters. Must use `https://`. |
| `events` | array of strings | Yes | Event types to subscribe to. Each must be a recognised event name (e.g., `"payment.succeeded"`, `"invoice.created"`). Pass `["*"]` to subscribe to all current and future event types. |
| `description` | string | No | Human-readable label for this webhook. Maximum 255 characters. |

**Example request body:**

```json
{
  "url": "https://app.example.com/webhooks/inbound",
  "events": ["payment.succeeded", "payment.failed"],
  "description": "Production payment handler"
}
```

#### Response

**Success: `201 Created`**

```json
{
  "id": "wh_4f8a1b2c-3d4e-5f6a-7b8c-9d0e1f2a3b4c",
  "url": "https://app.example.com/webhooks/inbound",
  "events": ["payment.succeeded", "payment.failed"],
  "description": "Production payment handler",
  "secret": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2",
  "status": "active",
  "created_at": "2026-05-27T09:00:00Z"
}
```

> **The `secret` field is only present in this creation response.** Store it securely — it cannot be retrieved later. Use it to verify the `X-Signature` header on every incoming payload.

**Errors:**

| Status | Code | When |
|---|---|---|
| 400 | `VALIDATION_ERROR` | Missing `url` or `events`, invalid field types |
| 401 | `UNAUTHORIZED` | Missing or invalid Bearer token |
| 403 | `FORBIDDEN` | Token lacks `webhooks:write` scope |
| 409 | `CONFLICT` | This URL is already registered as a webhook |
| 422 | `UNPROCESSABLE_ENTITY` | URL uses HTTP instead of HTTPS, or an event name in `events` is unrecognised |
| 429 | `RATE_LIMITED` | Rate limit exceeded |

**400 example:**

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      { "field": "url", "message": "url is required" },
      { "field": "events", "message": "events must be a non-empty array" }
    ]
  }
}
```

**401 example:**

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Missing or invalid Bearer token"
  }
}
```

**403 example:**

```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Token does not have the required scope: webhooks:write"
  }
}
```

**409 example:**

```json
{
  "error": {
    "code": "CONFLICT",
    "message": "A webhook for https://app.example.com/webhooks/inbound already exists"
  }
}
```

**422 example:**

```json
{
  "error": {
    "code": "UNPROCESSABLE_ENTITY",
    "message": "Unrecognised event type",
    "details": [
      { "field": "events[1]", "message": "payment.bounced is not a valid event type" }
    ]
  }
}
```

**429 example:**

```
HTTP/1.1 429 Too Many Requests
Retry-After: 38
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1716825060
```

```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Rate limit exceeded. Retry after 38 seconds."
  }
}
```

#### Example

**curl:**

```bash
curl -X POST https://api.example.com/v1/webhooks \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000" \
  -d '{
    "url": "https://app.example.com/webhooks/inbound",
    "events": ["payment.succeeded", "payment.failed"],
    "description": "Production payment handler"
  }'
```

> Replace `<YOUR_TOKEN>` with your API token. Replace the `Idempotency-Key` UUID with a unique value per distinct request to prevent duplicate registrations on retry.

**JavaScript (fetch):**

```javascript
const response = await fetch('https://api.example.com/v1/webhooks', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer <YOUR_TOKEN>',
    'Content-Type': 'application/json',
    'Idempotency-Key': crypto.randomUUID(),
  },
  body: JSON.stringify({
    url: 'https://app.example.com/webhooks/inbound',
    events: ['payment.succeeded', 'payment.failed'],
    description: 'Production payment handler',
  }),
});

const webhook = await response.json();
// Store webhook.secret immediately — it will not be returned again
console.log('Secret (save this now):', webhook.secret);
```

**Python (requests):**

```python
import uuid
import requests

response = requests.post(
    'https://api.example.com/v1/webhooks',
    headers={
        'Authorization': 'Bearer <YOUR_TOKEN>',
        'Content-Type': 'application/json',
        'Idempotency-Key': str(uuid.uuid4()),
    },
    json={
        'url': 'https://app.example.com/webhooks/inbound',
        'events': ['payment.succeeded', 'payment.failed'],
        'description': 'Production payment handler',
    },
)

webhook = response.json()
# Store webhook['secret'] immediately — it will not be returned again
print('Secret (save this now):', webhook['secret'])
```

#### Notes

- **Idempotency:** Supplying the same `Idempotency-Key` on a retry within 24 hours returns the original `201` response without creating a duplicate webhook.
- **Secret storage:** The `secret` is shown exactly once at registration. If lost, delete this webhook and register a new one to receive a fresh secret.
- Creating a webhook does not send a test event automatically. Use `POST /v1/webhooks/{id}/test` to verify connectivity and signature handling.

---

### List Webhooks

Returns all webhooks registered under the authenticated token's account, ordered by `created_at` descending (most recent first).

```
GET /v1/webhooks
```

#### Authentication

Requires Bearer token with **`webhooks:read`** scope.

#### Query Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `limit` | integer | No | 20 | Number of results per page. Range: 1–100. |
| `cursor` | string | No | — | Opaque pagination cursor from a previous response's `next_cursor` field. Omit for the first page. |

#### Response

**Success: `200 OK`**

```json
{
  "data": [
    {
      "id": "wh_4f8a1b2c-3d4e-5f6a-7b8c-9d0e1f2a3b4c",
      "url": "https://app.example.com/webhooks/inbound",
      "events": ["payment.succeeded", "payment.failed"],
      "description": "Production payment handler",
      "status": "active",
      "created_at": "2026-05-27T09:00:00Z"
    },
    {
      "id": "wh_9c8b7a6f-5e4d-3c2b-1a0f-9e8d7c6b5a4f",
      "url": "https://staging.example.com/webhooks/inbound",
      "events": ["*"],
      "description": "Staging all-events handler",
      "status": "active",
      "created_at": "2026-05-20T14:30:00Z"
    }
  ],
  "next_cursor": "d2ViaG9va19leGFtcGxlMjAyNjA1Mjc",
  "has_more": true
}
```

> The `secret` field is **not** returned in list responses. It is present only in the `201` response from webhook registration.

**Errors:**

| Status | Code | When |
|---|---|---|
| 400 | `VALIDATION_ERROR` | `limit` is not an integer, out of range, or `cursor` is malformed |
| 401 | `UNAUTHORIZED` | Missing or invalid Bearer token |
| 403 | `FORBIDDEN` | Token lacks `webhooks:read` scope |
| 429 | `RATE_LIMITED` | Rate limit exceeded |

**400 example:**

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      { "field": "limit", "message": "limit must be an integer between 1 and 100" }
    ]
  }
}
```

**401 example:**

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Missing or invalid Bearer token"
  }
}
```

**403 example:**

```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Token does not have the required scope: webhooks:read"
  }
}
```

**429 example:**

```
HTTP/1.1 429 Too Many Requests
Retry-After: 15
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1716825120
```

```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Rate limit exceeded. Retry after 15 seconds."
  }
}
```

#### Example

**curl — first page:**

```bash
curl -X GET "https://api.example.com/v1/webhooks?limit=20" \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

**curl — subsequent page:**

```bash
curl -X GET "https://api.example.com/v1/webhooks?limit=20&cursor=d2ViaG9va19leGFtcGxlMjAyNjA1Mjc" \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

**JavaScript (fetch) — iterate all pages:**

```javascript
async function listAllWebhooks(token) {
  const webhooks = [];
  let cursor = null;

  do {
    const url = new URL('https://api.example.com/v1/webhooks');
    url.searchParams.set('limit', '100');
    if (cursor) url.searchParams.set('cursor', cursor);

    const response = await fetch(url.toString(), {
      headers: { 'Authorization': `Bearer ${token}` },
    });

    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    const page = await response.json();
    webhooks.push(...page.data);
    cursor = page.has_more ? page.next_cursor : null;
  } while (cursor);

  return webhooks;
}
```

**Python (requests) — iterate all pages:**

```python
import requests

def list_all_webhooks(token):
    webhooks = []
    cursor = None

    while True:
        params = {'limit': 100}
        if cursor:
            params['cursor'] = cursor

        response = requests.get(
            'https://api.example.com/v1/webhooks',
            headers={'Authorization': f'Bearer {token}'},
            params=params,
        )
        response.raise_for_status()
        page = response.json()
        webhooks.extend(page['data'])

        if not page['has_more']:
            break
        cursor = page['next_cursor']

    return webhooks
```

#### Notes

- Secrets are omitted from list responses. Record the secret at registration time.
- Pagination cursors are stable — adding or deleting webhooks during iteration does not cause items to appear twice or be skipped.
- There is no total count field. Iterate until `has_more` is `false`.

---

### Delete a Webhook

Permanently removes a registered webhook. No further events will be delivered to its URL after deletion succeeds.

```
DELETE /v1/webhooks/{id}
```

#### Authentication

Requires Bearer token with **`webhooks:write`** scope.

#### Path Parameters

| Parameter | Type | Description |
|---|---|---|
| `id` | string | The webhook's unique identifier. Format: `wh_<uuid>`. Returned from the Register Webhook endpoint. |

#### Response

**Success: `204 No Content`**

No response body.

**Errors:**

| Status | Code | When |
|---|---|---|
| 401 | `UNAUTHORIZED` | Missing or invalid Bearer token |
| 403 | `FORBIDDEN` | Token lacks `webhooks:write` scope |
| 404 | `NOT_FOUND` | No webhook with this ID exists, or it belongs to a different account |
| 429 | `RATE_LIMITED` | Rate limit exceeded |

**401 example:**

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Missing or invalid Bearer token"
  }
}
```

**403 example:**

```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Token does not have the required scope: webhooks:write"
  }
}
```

**404 example:**

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Webhook wh_4f8a1b2c-3d4e-5f6a-7b8c-9d0e1f2a3b4c not found"
  }
}
```

**429 example:**

```
HTTP/1.1 429 Too Many Requests
Retry-After: 5
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1716825180
```

```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Rate limit exceeded. Retry after 5 seconds."
  }
}
```

#### Example

**curl:**

```bash
curl -X DELETE https://api.example.com/v1/webhooks/<WEBHOOK_ID> \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

> Replace `<WEBHOOK_ID>` with the `id` returned when the webhook was registered (e.g., `wh_4f8a1b2c-3d4e-5f6a-7b8c-9d0e1f2a3b4c`).

**JavaScript (fetch):**

```javascript
const webhookId = 'wh_4f8a1b2c-3d4e-5f6a-7b8c-9d0e1f2a3b4c';

const response = await fetch(`https://api.example.com/v1/webhooks/${webhookId}`, {
  method: 'DELETE',
  headers: {
    'Authorization': 'Bearer <YOUR_TOKEN>',
  },
});

if (response.status === 204) {
  console.log('Webhook deleted successfully');
}
```

**Python (requests):**

```python
import requests

webhook_id = 'wh_4f8a1b2c-3d4e-5f6a-7b8c-9d0e1f2a3b4c'

response = requests.delete(
    f'https://api.example.com/v1/webhooks/{webhook_id}',
    headers={'Authorization': 'Bearer <YOUR_TOKEN>'},
)

if response.status_code == 204:
    print('Webhook deleted successfully')
```

#### Notes

- Deletion is **permanent and immediate**. Events already queued before deletion may still be delivered, but no new events will be dispatched.
- To update a webhook URL, delete the existing record and register a new one (you will receive a new secret).
- A `404` is returned whether the ID never existed or belongs to a different account — this prevents enumeration.

---

### Send a Test Event

Delivers a synthetic `webhook.test` event to the registered endpoint URL. Use this after registration to confirm your server is reachable, parses the payload correctly, and successfully verifies the HMAC signature.

```
POST /v1/webhooks/{id}/test
```

#### Authentication

Requires Bearer token with **`webhooks:write`** scope.

#### Path Parameters

| Parameter | Type | Description |
|---|---|---|
| `id` | string | The webhook's unique identifier. Format: `wh_<uuid>`. |

#### Request Body

No request body is required. You may omit it or send an empty JSON object (`{}`).

#### Response

**Success: `200 OK`**

A `200` from this endpoint means the API successfully attempted delivery — check `delivered: true` to confirm your server accepted it.

```json
{
  "delivered": true,
  "status_code": 200,
  "response_body": "ok",
  "duration_ms": 143,
  "sent_at": "2026-05-27T09:15:00Z"
}
```

If your endpoint returned a non-2xx status:

```json
{
  "delivered": false,
  "status_code": 401,
  "response_body": "Signature verification failed",
  "duration_ms": 87,
  "sent_at": "2026-05-27T09:15:00Z"
}
```

**Errors:**

| Status | Code | When |
|---|---|---|
| 400 | `VALIDATION_ERROR` | Request is malformed |
| 401 | `UNAUTHORIZED` | Missing or invalid Bearer token |
| 403 | `FORBIDDEN` | Token lacks `webhooks:write` scope |
| 404 | `NOT_FOUND` | No webhook with this ID exists |
| 422 | `UNPROCESSABLE_ENTITY` | Endpoint URL is unreachable (DNS failure, connection refused, timeout) |
| 429 | `RATE_LIMITED` | Rate limit exceeded |

**401 example:**

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Missing or invalid Bearer token"
  }
}
```

**403 example:**

```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Token does not have the required scope: webhooks:write"
  }
}
```

**404 example:**

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Webhook wh_4f8a1b2c-3d4e-5f6a-7b8c-9d0e1f2a3b4c not found"
  }
}
```

**422 example:**

```json
{
  "error": {
    "code": "UNPROCESSABLE_ENTITY",
    "message": "Could not reach endpoint: connection refused at https://app.example.com/webhooks/inbound"
  }
}
```

**429 example:**

```
HTTP/1.1 429 Too Many Requests
Retry-After: 22
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1716825240
```

```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Rate limit exceeded. Retry after 22 seconds."
  }
}
```

#### Example

**curl:**

```bash
curl -X POST https://api.example.com/v1/webhooks/<WEBHOOK_ID>/test \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: 7c9e6679-7425-40de-944b-e07fc1f90ae7"
```

**JavaScript (fetch):**

```javascript
const webhookId = 'wh_4f8a1b2c-3d4e-5f6a-7b8c-9d0e1f2a3b4c';

const response = await fetch(`https://api.example.com/v1/webhooks/${webhookId}/test`, {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer <YOUR_TOKEN>',
    'Content-Type': 'application/json',
    'Idempotency-Key': crypto.randomUUID(),
  },
});

const result = await response.json();
console.log('Delivered:', result.delivered);
console.log('Your endpoint returned:', result.status_code);
```

**Python (requests):**

```python
import uuid
import requests

webhook_id = 'wh_4f8a1b2c-3d4e-5f6a-7b8c-9d0e1f2a3b4c'

response = requests.post(
    f'https://api.example.com/v1/webhooks/{webhook_id}/test',
    headers={
        'Authorization': 'Bearer <YOUR_TOKEN>',
        'Content-Type': 'application/json',
        'Idempotency-Key': str(uuid.uuid4()),
    },
)

result = response.json()
print('Delivered:', result['delivered'])
print('Your endpoint returned:', result['status_code'])
```

#### Notes

- The test payload uses event type `webhook.test` with a synthetic body — it does not reflect real account data.
- If `delivered: false`, inspect `response_body` — the most common cause is a failed or missing signature check.
- The test event is signed with the same secret as live events — your signature verification code works against it unchanged.

---

## Verifying Webhook Signatures

Every event payload includes an `X-Signature` header:

```
X-Signature: a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2
```

This is an **HMAC-SHA256 hex digest** of the raw request body, keyed with the secret returned at registration. Your handler must verify this before processing any payload.

**Algorithm:** `HMAC-SHA256(secret, raw_request_body).hexdigest()`

> **Critical:** Compute the HMAC over the **raw request body bytes** — not a parsed or re-serialised form. Re-serialising JSON may change key order and produce a different digest, causing legitimate events to fail verification.

**Why this matters:** Without signature verification an attacker can POST arbitrary payloads to your endpoint and trigger your business logic with forged data.

### Python

```python
import hashlib
import hmac

def verify_webhook_signature(secret: str, body: bytes, signature_header: str) -> bool:
    expected = hmac.new(
        secret.encode('utf-8'),
        body,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, signature_header)


# Flask example — read raw bytes before any JSON parsing
from flask import Flask, request, abort

app = Flask(__name__)
WEBHOOK_SECRET = 'a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2'

@app.route('/webhooks/inbound', methods=['POST'])
def handle_webhook():
    body = request.get_data()  # raw bytes — before any parsing
    sig = request.headers.get('X-Signature', '')

    if not verify_webhook_signature(WEBHOOK_SECRET, body, sig):
        abort(401)

    event = request.get_json()
    # process event ...
    return 'ok', 200
```

### Node.js

```javascript
const crypto = require('crypto');

function verifyWebhookSignature(secret, body, signatureHeader) {
  const expected = crypto
    .createHmac('sha256', secret)
    .update(body)
    .digest('hex');
  return crypto.timingSafeEqual(
    Buffer.from(expected),
    Buffer.from(signatureHeader),
  );
}

// Express example — must parse body as raw Buffer, not JSON
const express = require('express');
const app = express();

const WEBHOOK_SECRET = 'a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2';

app.post(
  '/webhooks/inbound',
  express.raw({ type: 'application/json' }), // keeps body as Buffer
  (req, res) => {
    const sig = req.headers['x-signature'] || '';

    if (!verifyWebhookSignature(WEBHOOK_SECRET, req.body, sig)) {
      return res.status(401).send('Invalid signature');
    }

    const event = JSON.parse(req.body);
    // process event ...
    res.status(200).send('ok');
  },
);
```

### Shell / curl

Verify a captured payload file against a known signature:

```bash
SECRET="a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2"
BODY_FILE="payload.json"
RECEIVED_SIG="<value from X-Signature header>"

COMPUTED=$(cat "$BODY_FILE" | openssl dgst -sha256 -hmac "$SECRET" | awk '{print $2}')

if [ "$COMPUTED" = "$RECEIVED_SIG" ]; then
  echo "Signature valid"
else
  echo "Signature INVALID — reject this request"
fi
```

### Timing-safe comparison

Always use a timing-safe equality function — a naive `==` comparison leaks timing information that can be exploited to forge valid signatures byte by byte.

| Language | Function |
|---|---|
| Python | `hmac.compare_digest(a, b)` |
| Node.js | `crypto.timingSafeEqual(Buffer.from(a), Buffer.from(b))` |
| Go | `subtle.ConstantTimeCompare([]byte(a), []byte(b))` |

---

## Webhooks-Specific Quality Checklist

```
- [ ] Every example was executed against staging before publication
- [ ] HMAC verification example tested with a known signature pair
- [ ] All 429-Retry-After examples include the header
- [ ] All scoped endpoints document the required scope
```

---

File is at `docs/webhooks-api.md`. A few assumptions I documented inline that you'll want to verify before publication:

- **Base URL** — `api.example.com` used as placeholder
- **Webhook ID prefix** — assumed `wh_<uuid>`; adjust if your IDs use a different format
- **Secret format** — assumed 64-char hex; confirm this matches what registration actually returns
- **Idempotency-Key window** — assumed 24 hours; confirm with your implementation
- **`X-Signature` header name** — confirm the exact casing your server sends
- **`events: ["*"]` wildcard** — assumed supported; remove if it isn't

### Artifacts written

#### `work/docs/webhooks-api.md`

```
# Webhooks API Reference

> **Assumptions documented inline:** Base URL uses `api.example.com` — replace with your actual domain. Token scopes follow `resource:action` format. Webhook IDs use a `wh_<uuid>` prefix. Signing secrets are 64-character hex strings returned once at registration. Default page size is 20; maximum is 100. `Idempotency-Key` is required on all POST requests. The `X-Signature` header carries the HMAC-SHA256 hex digest.

---

## Base URL

```
Production:  https://api.example.com/v1
Staging:     https://api-staging.example.com/v1
```

Versioning strategy: path-based (`/v1/`). Breaking changes are released under a new version prefix; the prior version remains available for a deprecation window.

---

## Authentication

### Bearer token

All endpoints require a Bearer token in the `Authorization` header:

```
Authorization: Bearer <YOUR_TOKEN>
```

> **Replace `<YOUR_TOKEN>`** with the token issued in your dashboard under **Settings → API Tokens**. All subsequent examples use this placeholder.

#### Token scopes

| Scope | Grants |
|---|---|
| `webhooks:read` | List registered webhooks |
| `webhooks:write` | Register new webhooks, delete webhooks, send test events |

**Authentication failure (401):**

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Missing or invalid Bearer token"
  }
}
```

**Insufficient scope (403):**

```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Token does not have the required scope: webhooks:write"
  }
}
```

---

## Rate Limiting

**Limit:** 100 requests per minute, per token.

When the limit is exceeded the API responds with:

```
HTTP/1.1 429 Too Many Requests
Retry-After: 42
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1716825060
```

```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Rate limit exceeded. Retry after 42 seconds."
  }
}
```

| Header | Type | Description |
|---|---|---|
| `X-RateLimit-Remaining` | integer | Requests remaining in the current 60-second window |
| `X-RateLimit-Reset` | integer (Unix timestamp) | UTC timestamp when the window resets and the counter returns to 100 |
| `Retry-After` | integer (seconds) | How long to wait before retrying. Present only on 429 responses. |

All successful responses also include `X-RateLimit-Remaining` and `X-RateLimit-Reset` so you can monitor headroom proactively without waiting for a 429.

---

## Pagination

`GET /v1/webhooks` uses **cursor-based pagination**.

**Request:**

```
GET /v1/webhooks?limit=20&cursor=d2ViaG9va19leGFtcGxlMjAyNjA1Mjc
```

**Response:**

```json
{
  "data": [ "..." ],
  "next_cursor": "d2ViaG9va19leGFtcGxlMjAyNjA1Mjc",
  "has_more": true
}
```

| Field | Type | Description |
|---|---|---|
| `data` | array | Page of webhook objects |
| `next_cursor` | string \| null | Opaque cursor for the next page. `null` when there are no further results. |
| `has_more` | boolean | `true` if more pages exist beyond this one |

| Parameter | Type | Default | Maximum | Description |
|---|---|---|---|---|
| `limit` | integer | 20 | 100 | Results per page |
| `cursor` | string | — | — | Value from a previous response's `next_cursor` |

**Detecting last page:** `has_more: false` or `next_cursor: null`.

Total count is not returned. Cursors are stable across concurrent mutations — items will not appear twice or be skipped if webhooks are added or deleted during pagination.

---

## Error Format

All error responses share a common shape:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable description of what went wrong",
    "details": [
      {
        "field": "url",
        "message": "Must be a valid HTTPS URL"
      }
    ]
  }
}
```

`details` is present only on `400` and `422` responses where field-level information is available.

### Error Code Reference

| HTTP Status | Code | Meaning | Common Cause |
|---|---|---|---|
| 400 | `VALIDATION_ERROR` | Request body or parameters are invalid | Missing required field, wrong type, invalid format |
| 401 | `UNAUTHORIZED` | Authentication failed or missing | Expired token, missing `Authorization` header |
| 403 | `FORBIDDEN` | Authenticated but insufficient permissions | Token missing required scope |
| 404 | `NOT_FOUND` | Resource does not exist | Invalid webhook ID, already deleted |
| 409 | `CONFLICT` | Request conflicts with current state | Webhook URL already registered |
| 422 | `UNPROCESSABLE_ENTITY` | Request is well-formed but semantically invalid | URL is HTTP (not HTTPS), unrecognised event type, endpoint unreachable |
| 429 | `RATE_LIMITED` | Too many requests | Exceeded 100 req/min per token |
| 500 | `INTERNAL_ERROR` | Server error | Bug — contact support |

---

## Endpoints

---

### Register a Webhook

Registers a new endpoint to receive webhook events. Returns the webhook record including the signing secret used to verify payloads. **The `secret` is returned only in this response — store it immediately.**

```
POST /v1/webhooks
```

#### Authentication

Requires Bearer token with **`webhooks:write`** scope.

#### Request Body

```
Content-Type: application/json
```

| Field | Type | Required | Description |
|---|---|---|---|
| `url` | string | Yes | HTTPS URL to receive webhook event POSTs. Maximum 2048 characters. Must use `https://`. |
| `events` | array of strings | Yes | Event types to subscribe to. Each must be a recognised event name (e.g., `"payment.succeeded"`, `"invoice.created"`). Pass `["*"]` to subscribe to all current and future event types. |
| `description` | string | No | Human-readable label for this webhook. Maximum 255 characters. |

**Example request body:**

```json
{
  "url": "https://app.example.com/webhooks/inbound",
  "events": ["payment.succeeded", "payment.failed"],
  "description": "Production payment handler"
}
```

#### Response

**Success: `201 Created`**

```json
{
  "id": "wh_4f8a1b2c-3d4e-5f6a-7b8c-9d0e1f2a3b4c",
  "url": "https://app.example.com/webhooks/inbound",
  "events": ["payment.succeeded", "payment.failed"],
  "description": "Production payment handler",
  "secret": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2",
  "status": "active",
  "created_at": "2026-05-27T09:00:00Z"
}
```

> **The `secret` field is only present in this creation response.** Store it securely — it cannot be retrieved later. Use it to verify the `X-Signature` header on every incoming payload. See [Verifying Webhook Signatures](#verifying-webhook-signatures).

**Errors:**

| Status | Code | When |
|---|---|---|
| 400 | `VALIDATION_ERROR` | Missing `url` or `events`, invalid field types |
| 401 | `UNAUTHORIZED` | Missing or invalid Bearer token |
| 403 | `FORBIDDEN` | Token lacks `webhooks:write` scope |
| 409 | `CONFLICT` | This URL is already registered as a webhook |
| 422 | `UNPROCESSABLE_ENTITY` | URL uses HTTP instead of HTTPS, or an event name in `events` is unrecognised |
| 429 | `RATE_LIMITED` | Rate limit exceeded |

**400 example:**

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      { "field": "url", "message": "url is required" },
      { "field": "events", "message": "events must be a non-empty array" }
    ]
  }
}
```

**401 example:**

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Missing or invalid Bearer token"
  }
}
```

**403 example:**

```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Token does not have the required scope: webhooks:write"
  }
}
```

**409 example:**

```json
{
  "error": {
    "code": "CONFLICT",
    "message": "A webhook for https://app.example.com/webhooks/inbound already exists"
  }
}
```

**422 example:**

```json
{
  "error": {
    "code": "UNPROCESSABLE_ENTITY",
    "message": "Unrecognised event type",
    "details": [
      { "field": "events[1]", "message": "payment.bounced is not a valid event type" }
    ]
  }
}
```

**429 example:**

```
HTTP/1.1 429 Too Many Requests
Retry-After: 38
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1716825060
```

```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Rate limit exceeded. Retry after 38 seconds."
  }
}
```

#### Example

**curl:**

```bash
curl -X POST https://api.example.com/v1/webhooks \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000" \
  -d '{
    "url": "https://app.example.com/webhooks/inbound",
    "events": ["payment.succeeded", "payment.failed"],
    "description": "Production payment handler"
  }'
```

> Replace `<YOUR_TOKEN>` with your API token. Replace the `Idempotency-Key` UUID with a unique value per distinct request to prevent duplicate registrations on retry.

**JavaScript (fetch):**

```javascript
const response = await fetch('https://api.example.com/v1/webhooks', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer <YOUR_TOKEN>',
    'Content-Type': 'application/json',
    'Idempotency-Key': crypto.randomUUID(),
  },
  body: JSON.stringify({
    url: 'https://app.example.com/webhooks/inbound',
    events: ['payment.succeeded', 'payment.failed'],
    description: 'Production payment handler',
  }),
});

const webhook = await response.json();
// Store webhook.secret immediately — it will not be returned again
console.log('Secret (save this now):', webhook.secret);
```

**Python (requests):**

```python
import uuid
import requests

response = requests.post(
    'https://api.example.com/v1/webhooks',
    headers={
        'Authorization': 'Bearer <YOUR_TOKEN>',
        'Content-Type': 'application/json',
        'Idempotency-Key': str(uuid.uuid4()),
    },
    json={
        'url': 'https://app.example.com/webhooks/inbound',
        'events': ['payment.succeeded', 'payment.failed'],
        'description': 'Production payment handler',
    },
)

webhook = response.json()
# Store webhook['secret'] immediately — it will not be returned again
print('Secret (save this now):', webhook['secret'])
```

#### Notes

- **Idempotency:** Supplying the same `Idempotency-Key` on a retry within 24 hours returns the original `201` response without creating a duplicate webhook.
- **Secret storage:** The `secret` is shown exactly once at registration. If lost, delete this webhook and register a new one to receive a fresh secret.
- Creating a webhook does not send a test event automatically. Use `POST /v1/webhooks/{id}/test` to verify connectivity and signature handling.

---

### List Webhooks

Returns all webhooks registered under the authenticated token's account, ordered by `created_at` descending (most recent first).

```
GET /v1/webhooks
```

#### Authentication

Requires Bearer token with **`webhooks:read`** scope.

#### Query Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `limit` | integer | No | 20 | Number of results per page. Range: 1–100. |
| `cursor` | string | No | — | Opaque pagination cursor from a previous response's `next_cursor` field. Omit for the first page. |

#### Response

**Success: `200 OK`**

```json
{
  "data": [
    {
      "id": "wh_4f8a1b2c-3d4e-5f6a-7b8c-9d0e1f2a3b4c",
      "url": "https://app.example.com/webhooks/inbound",
      "events": ["payment.succeeded", "payment.failed"],
      "description": "Production payment handler",
      "status": "active",
      "created_at": "2026-05-27T09:00:00Z"
    },
    {
      "id": "wh_9c8b7a6f-5e4d-3c2b-1a0f-9e8d7c6b5a4f",
      "url": "https://staging.example.com/webhooks/inbound",
      "events": ["*"],
      "description": "Staging all-events handler",
      "status": "active",
      "created_at": "2026-05-20T14:30:00Z"
    }
  ],
  "next_cursor": "d2ViaG9va19leGFtcGxlMjAyNjA1Mjc",
  "has_more": true
}
```

> The `secret` field is **not** returned in list responses. It is present only in the `201` response from webhook registration.

**Errors:**

| Status | Code | When |
|---|---|---|
| 400 | `VALIDATION_ERROR` | `limit` is not an integer, out of range, or `cursor` is malformed |
| 401 | `UNAUTHORIZED` | Missing or invalid Bearer token |
| 403 | `FORBIDDEN` | Token lacks `webhooks:read` scope |
| 429 | `RATE_LIMITED` | Rate limit exceeded |

**400 example:**

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      { "field": "limit", "message": "limit must be an integer between 1 and 100" }
    ]
  }
}
```

**401 example:**

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Missing or invalid Bearer token"
  }
}
```

**403 example:**

```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Token does not have the required scope: webhooks:read"
  }
}
```

**429 example:**

```
HTTP/1.1 429 Too Many Requests
Retry-After: 15
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1716825120
```

```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Rate limit exceeded. Retry after 15 seconds."
  }
}
```

#### Example

**curl — first page:**

```bash
curl -X GET "https://api.example.com/v1/webhooks?limit=20" \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

**curl — subsequent page:**

```bash
curl -X GET "https://api.example.com/v1/webhooks?limit=20&cursor=d2ViaG9va19leGFtcGxlMjAyNjA1Mjc" \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

**JavaScript (fetch) — iterate all pages:**

```javascript
async function listAllWebhooks(token) {
  const webhooks = [];
  let cursor = null;

  do {
    const url = new URL('https://api.example.com/v1/webhooks');
    url.searchParams.set('limit', '100');
    if (cursor) url.searchParams.set('cursor', cursor);

    const response = await fetch(url.toString(), {
      headers: { 'Authorization': `Bearer ${token}` },
    });

    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    const page = await response.json();
    webhooks.push(...page.data);
    cursor = page.has_more ? page.next_cursor : null;
  } while (cursor);

  return webhooks;
}
```

**Python (requests) — iterate all pages:**

```python
import requests

def list_all_webhooks(token):
    webhooks = []
    cursor = None

    while True:
        params = {'limit': 100}
        if cursor:
            params['cursor'] = cursor

        response = requests.get(
            'https://api.example.com/v1/webhooks',
            headers={'Authorization': f'Bearer {token}'},
            params=params,
        )
        response.raise_for_status()
        page = response.json()
        webhooks.extend(page['data'])

        if not page['has_more']:
            break
        cursor = page['next_cursor']

    return webhooks
```

#### Notes

- Secrets are omitted from list responses. Record the secret at registration time.
- Pagination cursors are stable — adding or deleting webhooks during iteration does not cause items to appear twice or be skipped.
- There is no total count field. Iterate until `has_more` is `false`.

---

### Delete a Webhook

Permanently removes a registered webhook. No further events will be delivered to its URL after deletion succeeds.

```
DELETE /v1/webhooks/{id}
```

#### Authentication

Requires Bearer token with **`webhooks:write`** scope.

#### Path Parameters

| Parameter | Type | Description |
|---|---|---|
| `id` | string | The webhook's unique identifier. Format: `wh_<uuid>`. Returned from the Register Webhook endpoint. |

#### Response

**Success: `204 No Content`**

No response body.

**Errors:**

| Status | Code | When |
|---|---|---|
| 401 | `UNAUTHORIZED` | Missing or invalid Bearer token |
| 403 | `FORBIDDEN` | Token lacks `webhooks:write` scope |
| 404 | `NOT_FOUND` | No webhook with this ID exists, or it belongs to a different account |
| 429 | `RATE_LIMITED` | Rate limit exceeded |

**401 example:**

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Missing or invalid Bearer token"
  }
}
```

**403 example:**

```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Token does not have the required scope: webhooks:write"
  }
}
```

**404 example:**

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Webhook wh_4f8a1b2c-3d4e-5f6a-7b8c-9d0e1f2a3b4c not found"
  }
}
```

**429 example:**

```
HTTP/1.1 429 Too Many Requests
Retry-After: 5
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1716825180
```

```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Rate limit exceeded. Retry after 5 seconds."
  }
}
```

#### Example

**curl:**

```bash
curl -X DELETE https://api.example.com/v1/webhooks/<WEBHOOK_ID> \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

> Replace `<WEBHOOK_ID>` with the `id` returned when the webhook was registered (e.g., `wh_4f8a1b2c-3d4e-5f6a-7b8c-9d0e1f2a3b4c`).

**JavaScript (fetch):**

```javascript
const webhookId = 'wh_4f8a1b2c-3d4e-5f6a-7b8c-9d0e1f2a3b4c';

const response = await fetch(`https://api.example.com/v1/webhooks/${webhookId}`, {
  method: 'DELETE',
  headers: {
    'Authorization': 'Bearer <YOUR_TOKEN>',
  },
});

if (response.status === 204) {
  console.log('Webhook deleted successfully');
}
```

**Python (requests):**

```python
import requests

webhook_id = 'wh_4f8a1b2c-3d4e-5f6a-7b8c-9d0e1f2a3b4c'

response = requests.delete(
    f'https://api.example.com/v1/webhooks/{webhook_id}',
    headers={'Authorization': 'Bearer <YOUR_TOKEN>'},
)

if response.status_code == 204:
    print('Webhook deleted successfully')
```

#### Notes

- Deletion is **permanent and immediate**. Events already queued before deletion may still be delivered to your endpoint, but no new events will be dispatched.
- To update a webhook URL, delete the existing record and register a new one (you will receive a new secret).
- A `404` is returned whether the ID never existed or belongs to a different account — this prevents enumeration.

---

### Send a Test Event

Delivers a synthetic `webhook.test` event to the registered endpoint URL. Use this after registration to confirm your server is reachable, parses the payload correctly, and successfully verifies the HMAC signature.

```
POST /v1/webhooks/{id}/test
```

#### Authentication

Requires Bearer token with **`webhooks:write`** scope.

#### Path Parameters

| Parameter | Type | Description |
|---|---|---|
| `id` | string | The webhook's unique identifier. Format: `wh_<uuid>`. |

#### Request Body

No request body is required. You may omit it or send an empty JSON object (`{}`).

#### Response

**Success: `200 OK`**

The response reflects what your endpoint returned. A `200` from this endpoint means the API successfully attempted delivery — check `delivered: true` to confirm your server accepted it.

```json
{
  "delivered": true,
  "status_code": 200,
  "response_body": "ok",
  "duration_ms": 143,
  "sent_at": "2026-05-27T09:15:00Z"
}
```

If your endpoint returned a non-2xx status:

```json
{
  "delivered": false,
  "status_code": 401,
  "response_body": "Signature verification failed",
  "duration_ms": 87,
  "sent_at": "2026-05-27T09:15:00Z"
}
```

**Errors:**

| Status | Code | When |
|---|---|---|
| 400 | `VALIDATION_ERROR` | Request is malformed |
| 401 | `UNAUTHORIZED` | Missing or invalid Bearer token |
| 403 | `FORBIDDEN` | Token lacks `webhooks:write` scope |
| 404 | `NOT_FOUND` | No webhook with this ID exists |
| 422 | `UNPROCESSABLE_ENTITY` | Endpoint URL is unreachable (DNS failure, connection refused, timeout) |
| 429 | `RATE_LIMITED` | Rate limit exceeded |

**401 example:**

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Missing or invalid Bearer token"
  }
}
```

**403 example:**

```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Token does not have the required scope: webhooks:write"
  }
}
```

**404 example:**

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Webhook wh_4f8a1b2c-3d4e-5f6a-7b8c-9d0e1f2a3b4c not found"
  }
}
```

**422 example:**

```json
{
  "error": {
    "code": "UNPROCESSABLE_ENTITY",
    "message": "Could not reach endpoint: connection refused at https://app.example.com/webhooks/inbound"
  }
}
```

**429 example:**

```
HTTP/1.1 429 Too Many Requests
Retry-After: 22
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1716825240
```

```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Rate limit exceeded. Retry after 22 seconds."
  }
}
```

#### Example

**curl:**

```bash
curl -X POST https://api.example.com/v1/webhooks/<WEBHOOK_ID>/test \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: 7c9e6679-7425-40de-944b-e07fc1f90ae7"
```

**JavaScript (fetch):**

```javascript
const webhookId = 'wh_4f8a1b2c-3d4e-5f6a-7b8c-9d0e1f2a3b4c';

const response = await fetch(`https://api.example.com/v1/webhooks/${webhookId}/test`, {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer <YOUR_TOKEN>',
    'Content-Type': 'application/json',
    'Idempotency-Key': crypto.randomUUID(),
  },
});

const result = await response.json();
console.log('Delivered:', result.delivered);
console.log('Your endpoint returned:', result.status_code);
```

**Python (requests):**

```python
import uuid
import requests

webhook_id = 'wh_4f8a1b2c-3d4e-5f6a-7b8c-9d0e1f2a3b4c'

response = requests.post(
    f'https://api.example.com/v1/webhooks/{webhook_id}/test',
    headers={
        'Authorization': 'Bearer <YOUR_TOKEN>',
        'Content-Type': 'application/json',
        'Idempotency-Key': str(uuid.uuid4()),
    },
)

result = response.json()
print('Delivered:', result['delivered'])
print('Your endpoint returned:', result['status_code'])
```

#### Notes

- The test payload uses event type `webhook.test` with a synthetic body — it does not reflect real account data.
- If `delivered: false`, inspect `response_body` — it usually contains your server's error message. The most common cause is a failed or missing signature check.
- The test event is signed with the same secret as live events — your signature verification code will work against it unchanged.

---

## Verifying Webhook Signatures

Every event payload we POST to your endpoint includes an `X-Signature` header:

```
X-Signature: a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2
```

This is an **HMAC-SHA256 hex digest** of the raw request body, keyed with the secret returned at webhook registration. Your handler must verify this signature and reject any request where it does not match.

**Algorithm:**

```
signature = HMAC-SHA256(secret, raw_request_body).hexdigest()
```

> **Critical:** Compute the HMAC over the **raw request body bytes** — not a parsed or re-serialised form. Re-serialising JSON (even with the same data) may change key order and produce a different digest, causing legitimate events to be rejected.

**Why this matters:** Without signature verification an attacker can POST arbitrary payloads to your endpoint and trigger your business logic with forged data.

### Python

```python
import hashlib
import hmac

def verify_webhook_signature(secret: str, body: bytes, signature_header: str) -> bool:
    expected = hmac.new(
        secret.encode('utf-8'),
        body,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, signature_header)


# Flask example — read raw bytes before any JSON parsing
from flask import Flask, request, abort

app = Flask(__name__)
WEBHOOK_SECRET = 'a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2'

@app.route('/webhooks/inbound', methods=['POST'])
def handle_webhook():
    body = request.get_data()  # raw bytes — before any parsing
    sig = request.headers.get('X-Signature', '')

    if not verify_webhook_signature(WEBHOOK_SECRET, body, sig):
        abort(401)

    event = request.get_json()
    # process event ...
    return 'ok', 200
```

### Node.js

```javascript
const crypto = require('crypto');

function verifyWebhookSignature(secret, body, signatureHeader) {
  const expected = crypto
    .createHmac('sha256', secret)
    .update(body)
    .digest('hex');
  return crypto.timingSafeEqual(
    Buffer.from(expected),
    Buffer.from(signatureHeader),
  );
}

// Express example — must parse body as raw Buffer, not JSON
const express = require('express');
const app = express();

const WEBHOOK_SECRET = 'a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2';

app.post(
  '/webhooks/inbound',
  express.raw({ type: 'application/json' }), // keeps body as Buffer
  (req, res) => {
    const sig = req.headers['x-signature'] || '';

    if (!verifyWebhookSignature(WEBHOOK_SECRET, req.body, sig)) {
      return res.status(401).send('Invalid signature');
    }

    const event = JSON.parse(req.body);
    // process event ...
    res.status(200).send('ok');
  },
);
```

### Shell / curl

Verify a captured payload file against a known signature:

```bash
SECRET="a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2"
BODY_FILE="payload.json"
RECEIVED_SIG="<value from X-Signature header>"

COMPUTED=$(cat "$BODY_FILE" | openssl dgst -sha256 -hmac "$SECRET" | awk '{print $2}')

if [ "$COMPUTED" = "$RECEIVED_SIG" ]; then
  echo "Signature valid"
else
  echo "Signature INVALID — reject this request"
fi
```

### Timing-safe comparison

Always use a timing-safe equality function:

| Language | Function |
|---|---|
| Python | `hmac.compare_digest(a, b)` |
| Node.js | `crypto.timingSafeEqual(Buffer.from(a), Buffer.from(b))` |
| Go | `subtle.ConstantTimeCompare([]byte(a), []byte(b))` |

A naive `==` comparison leaks timing information that can be exploited to forge valid signatures byte by byte.

---

## Webhooks-Specific Quality Checklist

```
- [ ] Every example was executed against staging before publication
- [ ] HMAC verification example tested with a known signature pair
- [ ] All 429-Retry-After examples include the header
- [ ] All scoped endpoints document the required scope
```

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.5/17.0 (91%) |
| Evaluated | 2026-05-27 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 372362 ms |
| Target cost | $0.6146 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Every endpoint includes a complete request example with all required headers (Authorization, Content-Type) and a realistic request body | PASS | All four endpoints have curl/JS/Python examples with Authorization, Content-Type, and Idempotency-Key headers. POST /v1/webhooks body includes url, events, description. |
| c2 | Every endpoint documents both success responses and error responses — at minimum: 401 Unauthorized, 403 Forbidden (wrong scope), 429 Too Many Requests, and relevant 4xx for invalid input | PASS | Every endpoint has explicit 401/403/429 examples with JSON bodies. POST adds 400/409/422; DELETE adds 404; test endpoint adds 400/404/422. |
| c3 | Documents the HMAC-SHA256 signature verification process with a working code example in at least one language | PASS | "Verifying Webhook Signatures" section provides full working examples in Python (hmac.new + Flask), Node.js (crypto.createHmac + Express), and Shell (openssl dgst -sha256 -hmac). |
| c4 | Explains token scopes (webhooks:read vs webhooks:write) and which endpoints require which scope | PASS | Authentication section has a scope table; each endpoint section states "Requires Bearer token with `webhooks:write`/`webhooks:read` scope" explicitly. |
| c5 | Documents rate limit behaviour including the Retry-After header and how clients should handle 429 responses | PASS | Dedicated Rate Limiting section shows 429 with Retry-After, X-RateLimit-Remaining, X-RateLimit-Reset headers plus JSON error body. Every endpoint repeats 429 example with headers. |
| c6 | Code examples are syntactically correct and copy-pasteable — not pseudocode or placeholder-heavy | PASS | All curl/JS/Python examples have correct syntax, proper imports (uuid, requests, hashlib, hmac), and placeholders like `<YOUR_TOKEN>` explained on first use. |
| c7 | Includes a quick-start or authentication section before the endpoint reference — partial credit if auth is documented inline per endpoint but not as a standalone overview | PARTIAL | "## Authentication" section appears before "## Endpoints", shows Bearer token format, scope table, and notes "under Settings → API Tokens" — a standalone overview. |
| c8 | Documents what a webhook payload looks like and how to verify the signature, not just that verification should happen | PASS | "Verifying Webhook Signatures" shows X-Signature header value, HMAC-SHA256 algorithm, raw-body requirement, full code in 3 languages extracting header and comparing digest. |
| c9 | Output documents all four endpoints — POST `/v1/webhooks`, GET `/v1/webhooks`, DELETE `/v1/webhooks/{id}`, POST `/v1/webhooks/{id}/test` — with request/response examples per endpoint, not a generic CRUD template | PASS | All four endpoints have dedicated sections with unique request/response examples, success codes (201, 200, 204, 200), and endpoint-specific error scenarios. |
| c10 | Output's request examples for POST endpoints include the full JSON body — endpoint URL, event types subscribed, custom metadata — not just `{"url": "..."}` placeholder | PASS | POST body includes `url`, `events: ["payment.succeeded", "payment.failed"]`, and `description: "Production payment handler"` across all three languages. |
| c11 | Output documents 401 (missing/invalid token), 403 (wrong scope — e.g. `webhooks:read` token attempting POST), 429 (rate limit with `Retry-After` header), 422 (validation — e.g. invalid URL), and 404 (deleting a non-existent webhook) | PASS | All five statuses present: 401/403 on every endpoint; 429 with Retry-After on every endpoint; 422 on POST/test; 404 on DELETE and test endpoints with JSON examples. |
| c12 | Output's HMAC signature verification example shows actual code in at least one language (Python or Node.js typical) — including extracting the signature from the header, computing HMAC-SHA256 using the secret, and constant-time comparison — runnable, not pseudocode | PASS | Python: `request.headers.get('X-Signature')`, `hmac.new(...).hexdigest()`, `hmac.compare_digest`. Node.js: `createHmac('sha256',secret).update(body).digest('hex')`, `crypto.timingSafeEqual`. |
| c13 | Output explains the two scopes (`webhooks:read`, `webhooks:write`) and maps each endpoint to its required scope in a table — not just mentioning scopes in prose | PASS | Authentication section has a scope table mapping `webhooks:read`→list, `webhooks:write`→register/delete/test. Each endpoint also explicitly declares its required scope. |
| c14 | Output's rate-limit documentation includes the algorithm semantics (per-token, 100/minute), the response body shape on 429, the `Retry-After` header value semantics, and a recommended client backoff strategy | PARTIAL | Covers per-token/100/min semantics, 429 body shape, Retry-After semantics. Missing: explicit recommended client backoff strategy (exponential backoff, jitter not mentioned). |
| c15 | Output documents the webhook payload structure delivered TO the customer's endpoint — not just the API request structure — including the signed body, the signature header name, and example event types | PARTIAL | X-Signature header name shown, raw-body signing explained, event types mentioned (`webhook.test`, `payment.succeeded`). Missing: actual JSON payload structure delivered to customer endpoint. |
| c16 | Output's authentication section appears as an overview before the endpoint reference, explaining Bearer token format and where to obtain tokens — not only inline per endpoint | PASS | "## Authentication" before "## Endpoints": shows `Authorization: Bearer <YOUR_TOKEN>` format, notes "Settings → API Tokens" for obtaining tokens, plus scope table. |
| c17 | Output's code examples are syntactically correct and copy-pasteable — no `<your_token_here>` ambiguity that doesn't match runtime expectations, no missing imports | PASS | Python has `import uuid, requests, hashlib, hmac`. JS uses `crypto.randomUUID()`. Placeholders `<YOUR_TOKEN>` and `<WEBHOOK_ID>` are explained on first use with replacement instructions. |
| c18 | Output addresses webhook delivery semantics — retry policy if the customer's endpoint returns non-2xx, timeout handling, and when a webhook is considered "failed" — important for customers building reliable receivers | FAIL | Output only mentions `delivered: true/false` in test endpoint response. No retry policy for non-2xx, no timeout handling, no failure/dead-letter semantics documented anywhere. |

### Notes

The output is exceptionally thorough, covering all four endpoints with complete examples in three languages, full error coverage, HMAC verification in three languages, and a well-structured standalone auth overview. The main gaps are the absence of actual webhook payload JSON structure (c15), missing client backoff strategy in rate-limit docs (c14), and no delivery retry/timeout semantics (c18).
