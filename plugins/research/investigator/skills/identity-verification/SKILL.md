---
name: identity-verification
description: "Verify that a named individual is who they claim to be, or resolve ambiguity between people sharing a name. Anchors on verifiable claims and cross-references independently. Writes a conforming report (per report-conventions) to <engagement_dir>/identity-verification/<lastname>-<firstname>.md. Requires authorisation gate."
argument-hint: "<person name> claims to be <role/employer/credential> [engagement_dir]"
user-invocable: true
allowed-tools: WebSearch, WebFetch, Read, Write, Bash
---

Verify the identity of the named individual using public sources, and write a conforming report.

> [!IMPORTANT]
> This skill requires the investigator agent's full authorisation gate before invocation. The gate stays in the session record — it is not embedded in the report file.

## Step 0: Resolve arguments

Parse `$ARGUMENTS` as `<person name> claims to be <claims> [engagement_dir]`. The trailing token, if it looks like a path, is the engagement directory; otherwise default to `pwd`. Resolve to an absolute path.

The "claims to be" portion is the input to verify, not part of the subject identity.

## Step 1: Compute the output path

Subject slug: `<lastname>-<firstname>`, kebab-case, lowercase, ASCII (per report-conventions).

Output path: `$ENG/identity-verification/<slug>.md`

If a file already exists at that path, ask the user before overwriting (overwrite / write a `-2` sibling / abort).

## Step 2: Stage the report from the template

```bash
mkdir -p "$ENG/identity-verification"
cp "${CLAUDE_PLUGIN_ROOT}/templates/identity-verification.md" "$ENG/identity-verification/<slug>.md"
```

Replace placeholders in frontmatter:

| Placeholder | Replace with |
|---|---|
| `{SUBJECT}` | The personal name |
| `{SUBTITLE}` | Engagement directory basename, title-cased; drop the line if no useful inference |
| `{DATE}` | Today's ISO date |

## Step 3: Investigation

Write findings into the staged file as you go.

### Anchor on verifiable claims

Start with what the subject has claimed — not with a general search. List each claim explicitly in the report's "Claims to verify" section before verifying any of them. Unanchored searches produce noise; anchored searches produce evidence.

Claims to verify might include:

- Current employer and role
- Credentials and qualifications
- Publications or public work
- Location or operational base

### Verify each claim independently

For each claim:

**Employer verification:**

- Search the company's own website for the person (team pages, leadership, press releases, bylines)
- Check LinkedIn for consistency between the person's profile and the company's employee list
- Look for the person mentioned in company announcements or press coverage

**Credential verification:**

- Professional licensing boards (see people-lookup skill for the full AU/NZ/US registry list)
- Academic institutions for degree claims — faculty pages, alumni directories
- For specific accreditations: the issuing body's public registry or verification page
- AU health practitioners: [AHPRA](https://www.ahpra.gov.au)
- AU financial advisers: [ASIC Financial Advisers Register](https://moneysmart.gov.au/financial-advice/financial-advisers-register)

**Publication verification:**

- [Google Scholar](https://scholar.google.com), [ORCID](https://orcid.org), [ResearchGate](https://www.researchgate.net)
- The specific journal or publisher's website for the claimed work
- Conference proceedings for claimed conference presentations

### Cross-reference identifiers

Strong identity confirmation comes from consistent identifiers across independent sources:

- **Photo consistency** — does the same face appear on LinkedIn, company site, conference appearances?
- **Location consistency** — do professional history claims place the person in the same locations consistently?
- **Timeline consistency** — do claimed tenures line up? Are there unexplained gaps?
- **Writing style or patterns** — for authors, does the claimed work match a consistent voice or research area?

### Name disambiguation

If the name belongs to multiple people:

1. List all distinct individuals found with this name
1. Apply context anchors from the gate record (employer, location, field) to narrow
1. Document which individual is being confirmed — and note if disambiguation is uncertain

Failure condition: after 3 attempts with different context anchors, ambiguity persists. Stop and ask for additional context rather than guessing.

### Flag inconsistencies

Document any:

- Claims that couldn't be verified (not the same as disproved)
- Gaps in the professional timeline
- Credential claims that don't appear in the issuing body's registry
- Conflicting information across sources (different employers listed on different sites)

Distinguish clearly between "unverifiable" (no public evidence either way) and "contradicted" (evidence that the claim is false).

## Step 4: Finalise the report

- Set `status: Final` once content is complete; leave `Draft` if claims remain unverified or disambiguation is incomplete.
- Optionally set `confidence: 0-4` based on the verification evidence (per source-quality).
- Source list with tier tags.

## Rules

- Start from the subject's claims, not from an open search. You're verifying, not profiling.
- Never assert a claim is false unless you have a source that actively contradicts it. "Not found in registry" is not the same as "invalid credential."
- Disambiguation failures must be surfaced. Reporting on the wrong person is worse than reporting nothing.
- Photo comparison is visual only — note photo consistency across sources; don't speculate beyond what you can observe.
- One file per invocation.

## Output

A single line: the absolute path to the written report.
