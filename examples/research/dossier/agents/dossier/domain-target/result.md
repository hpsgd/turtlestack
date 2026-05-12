# Domain Target

Scenario: A user asks for a dossier on a company they know only by its domain. The dossier agent should restate the target, classify it (domain → Technical + Corporate + OSINT), propose an engagement directory under `{workspace}`, and produce a dispatch plan naming the specific skills it would run per category. It should not execute the investigation itself, and it should not invent findings.

## Prompt

> Build me a dossier on visualcare.com.au. The engagement directory should sit under `{workspace}/assessments/visualcare`. Do not pause for confirmation — proceed with the most defensible default for each category choice and document the assumption inline. Do not execute any subordinate skills yet; produce the dispatch plan only.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Here's the dispatch plan the dossier agent produced:

---

## Dispatch plan — visualcare.com.au

**Engagement dir:** `/var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/eval-1778593403-b1872d77/assessments/visualcare`

### Assumptions (documented inline)

- **People excluded** — no named subjects provided; the authorisation gate (purpose, scope, subject awareness) can't be completed without them. Can be added if you supply names + gate answers.
- **Commercial excluded as standalone** — `company-lookup` covers the registry angle; no full competitive-analysis scope was requested.
- **Legal entity name** — inferred as `Visualcare` from the domain; confirmed from `domain-intel` output before `corporate-ownership` is dispatched.

### Sequencing

**Batch 1 — run first (solo):**

| # | Skill | Subject | Why first |
|---|---|---|---|
| 1 | `domain-intel` | `visualcare.com.au` | Anchor. Resolves IPs (feeds row 2) and registrant entity name (feeds row 3). |

**Batch 2 — run in parallel after Batch 1:**

| # | Skill | Subject | Notes |
|---|---|---|---|
| 2 | `ip-intel` | `<IP from domain-intel>` | One run per distinct hosting IP; drops CDN/shared addresses |
| 3 | `corporate-ownership` | `<confirmed legal name>` | ABN/ACN, directors, beneficial owners, related entities |
| 4 | `company-lookup` | `Visualcare` | Commercial registry + market data; dropped if `analyst` plugin absent |
| 5 | `entity-footprint` | `Visualcare` | Broad OSINT sweep — social, press, breach exposure, domain history |

**Final step (after all skills complete):**

`dossier:consolidate` → PDF

---

Say the word and I'll execute Batch 1, or if you want to add People scope first, supply the names and authorisation context.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 9.5/11.0 (86%) |
| Evaluated | 2026-05-12 |
| Target duration | 54811 ms |
| Target cost | $0.3448 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent restates the target as a domain (`visualcare.com.au`) before doing anything else, distinguishing it from a person or a company name | PASS | Heading reads '## Dispatch plan — visualcare.com.au' and Batch 1 table shows subject 'visualcare.com.au' for domain-intel as the anchor skill. |
| c2 | Agent classifies the target into the right category set — Technical and Corporate at minimum, OSINT typically — using the target-shape table from the skill | PARTIAL | Skills chosen map correctly (domain-intel/ip-intel=Technical, corporate-ownership/company-lookup=Corporate, entity-footprint=OSINT) but category labels are never stated explicitly; grouped by batch instead. |
| c3 | Agent confirms or proposes the engagement directory at `{workspace}/assessments/visualcare` rather than defaulting to `~/Assessments/` or another path | PASS | '**Engagement dir:** `/var/folders/.../T/eval-1778593403-b1872d77/assessments/visualcare`' — workspace substituted, path matches the requested pattern. |
| c4 | Agent produces a dispatch plan — names each subordinate skill (`/investigator:domain-intel`, `/investigator:ip-intel`, `/investigator:corporate-ownership`, etc.) per category with the argument it would pass — rather than executing them | PASS | Tables list domain-intel, ip-intel, corporate-ownership, company-lookup, entity-footprint with subjects; output ends 'Say the word and I'll execute Batch 1' — no execution. |
| c5 | Agent does NOT produce any findings prose (no claims about the domain's hosting, ownership, or related entities). The boundary rule says orchestrate, don't investigate. | PASS | Entire output is sequencing tables, assumption notes, and a closing prompt. No hosting IPs, ownership claims, or entity details appear. |
| c6 | Agent identifies which skills are mandatory (Technical: domain-intel) vs which depend on what surfaces (Corporate: only if ASIC ownership is in scope) — proposes a sensible default given a domain target | PASS | domain-intel is solo in Batch 1 labelled 'Anchor'; ip-intel and corporate-ownership are Batch 2 with explicit dependency notes; company-lookup flagged 'dropped if analyst plugin absent'. |
| c7 | Agent flags that the People category is uncertain at this stage — directors are not known until corporate-ownership runs — rather than blindly running people-lookup with no name | PARTIAL | Assumptions: 'People excluded — no named subjects provided; the authorisation gate can't be completed without them.' Flagged but framed as auth-gate gap, not as 'directors surface from corporate-ownership'. |
| c8 | Agent ends with a clear next step: run the dispatched skills, then run `/dossier:consolidate {workspace}/assessments/visualcare` to compile | PASS | 'Final step (after all skills complete): `dossier:consolidate` → PDF' and closing line 'Say the word and I'll execute Batch 1'. |
| c9 | Output's dispatch plan is structured as a table or list keyed by category, naming the skill and the argument per row | PARTIAL | Two markdown tables with Skill and Subject columns, but keyed by batch (Batch 1 / Batch 2) rather than by category (Technical / Corporate / OSINT) as the criterion specifies. |
| c10 | Output names at least three subordinate skills with their `{workspace}/assessments/visualcare`-rooted arguments | PARTIAL | Five skills named (domain-intel, ip-intel, corporate-ownership, company-lookup, entity-footprint) but arguments shown are subjects/targets only; no workspace-rooted output-path arguments per skill. |
| c11 | Output's closing step references `/dossier:consolidate` as the consolidation phase, not as a subordinate skill in the dispatch list | PASS | 'Final step (after all skills complete): `dossier:consolidate` → PDF' — placed after all batch rows, clearly separated from the dispatch list. |
| c12 | Output documents the assumptions made for each "uncertain" category (e.g. "People deferred until directors surface from corporate-ownership") rather than silently skipping | PARTIAL | Assumptions section covers People (auth gate), Commercial (no competitive scope requested), and entity name inference. OSINT category rationale not explicitly stated. |

### Notes

The output is a well-structured dispatch plan that correctly selects skills, defers execution, and documents key assumptions. Its main gaps are omitting explicit category labels (Technical/Corporate/OSINT) in the table headers and not providing workspace-rooted output-path arguments per skill invocation.
