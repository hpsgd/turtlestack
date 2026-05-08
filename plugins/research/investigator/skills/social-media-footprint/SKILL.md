---
name: social-media-footprint
description: "Map publicly visible social media presence for a person or organisation across platforms. Public content only — no access to locked, private, or friends-gated content. Writes a conforming report (per report-conventions) to <engagement_dir>/social-media-footprint/<subject-slug>.md."
argument-hint: "<person or organisation name> [engagement_dir]"
user-invocable: true
allowed-tools: WebSearch, WebFetch, Read, Write, Bash
---

Map the public social media footprint of the named subject and write the findings to a deterministic file path.

> [!IMPORTANT]
> For people (not organisations): this skill requires the investigator agent's full authorisation gate before invocation. The gate stays in the session record — it is not embedded in the report file.

## Step 0: Resolve arguments

Parse `$ARGUMENTS` as `<subject name> [engagement_dir]`. Trailing path-shaped token is the engagement directory; otherwise default to `pwd`. Resolve to an absolute path.

Decide whether the subject is a person or an organisation — affects the slug, the category in frontmatter, and whether the gate applies.

## Step 1: Compute the output path

Subject slug:

| Subject type | Slug |
|---|---|
| Person | `<lastname>-<firstname>`, kebab-case, lowercase, ASCII |
| Organisation | full name, kebab-case, lowercase, ASCII, no legal-suffix punctuation |

Examples:

- `Michael Graves` → `graves-michael`
- `Acme Corp Pty Ltd` → `acme-corp-pty-ltd`

Output path: `$ENG/social-media-footprint/<slug>.md`

If a file already exists at that path, ask before overwriting.

## Step 2: Stage the report from the template

```bash
mkdir -p "$ENG/social-media-footprint"
cp "${CLAUDE_PLUGIN_ROOT}/templates/social-media-footprint.md" "$ENG/social-media-footprint/<slug>.md"
```

Replace placeholders in frontmatter:

| Placeholder | Replace with |
|---|---|
| `{SUBJECT}` | The subject name |
| `{SUBTITLE}` | Engagement directory basename, title-cased; drop the line if no useful inference |
| `{DATE}` | Today's ISO date |

If the subject is an organisation, also change `category: People` in the frontmatter to `category: OSINT` to reflect organisational scope.

## Step 3: Investigation

### Platform search

Search for the subject on each platform. For organisations, look for official accounts. For individuals, look for public profiles.

| Platform | Search method |
|---|---|
| LinkedIn | Name search; for organisations, company page search |
| Twitter/X | `twitter.com/search?q=[name]` or name search |
| Facebook | Name/page search — public content only |
| Instagram | Username search — public accounts only |
| TikTok | Username search |
| YouTube | Channel search |
| GitHub | Username or organisation search |
| Reddit | Username search (for individuals who post publicly under their name) |

Record per account: URL, handle, follower or subscriber count, account creation date if visible, posting cadence (active / occasional / dormant).

### Username patterns

Once a username is found on one platform, search the same username across others.

Tools: [Namechk](https://namechk.com) (public availability search), manual search on major platforms.

Consistent usernames across platforms are a strong identity signal. Inconsistent ones may indicate separate accounts for different contexts (professional vs personal).

### Content assessment

For each active account, review public posts to establish:

- Primary topics and themes
- Tone and audience (professional, community, personal expression)
- Posting frequency and recency
- Notable public statements or positions
- Engagement patterns (comments, shares, replies from others)

Public content only. Do not attempt to view locked, private, or friends-gated content by any means.

### Organisational accounts (organisations only)

For organisation investigations, map:

- Official verified accounts vs unofficial fan/community pages
- Employee accounts that post about work publicly
- Executive accounts (often the most informative signal of direction and culture)
- Product-specific sub-accounts

## Step 4: Finalise the report

- Confirm every section has either content or an explicit "none found / not on this platform" note.
- Replace placeholder source rows with actual sources, tagged with tier per source-quality.
- Set `status: Final` once complete.
- Optionally set `confidence: 0-4`.

## Rules

- Public content only. No access to locked, private, or friends-gated content — this is a hard limit with no exceptions.
- Don't screen-scrape, don't attempt to infer private content, don't attempt to bypass platform access controls.
- For individuals: scope to public professional presence unless the gate record explicitly expands to personal accounts.
- Content assessment produces observations, not character conclusions. "Posts frequently about [topic]" is an observation. "This person is [character judgement]" is not your call.
- A well-curated, private social presence is a finding. It means the subject is intentional about their public footprint.
- One file per invocation.

## Output

A single line: the absolute path to the written report.
