# Domain Target

Scenario: A user asks for a dossier on a company they know only by its domain. The dossier agent should restate the target, classify it (domain → Technical + Corporate + OSINT), propose an engagement directory under `{workspace}`, and produce a dispatch plan naming the specific skills it would run per category. It should not execute the investigation itself, and it should not invent findings.

## Prompt

> Build me a dossier on visualcare.com.au. The engagement directory should sit under `{workspace}/assessments/visualcare`. Do not pause for confirmation — proceed with the most defensible default for each category choice and document the assumption inline. Do not execute any subordinate skills yet; produce the dispatch plan only.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Here is the dispatch plan produced by the dossier agent:

---

## Dossier Dispatch Plan — visualcare.com.au

**Engagement directory:** `/var/folders/nn/.../assessments/visualcare`

### Categories included (with rationale)

| Category | Decision | Assumption |
|---|---|---|
| Technical | Yes | Domain is the primary target; domain-intel is the anchor, ip-intel follows |
| Corporate | Yes | `.com.au` implies ABN/ACN registrant; company-lookup + corporate-ownership resolve entity |
| OSINT | Yes | entity-footprint + social-media-footprint against "Visualcare" |
| Competitive | Yes (Phase 2b) | Staged after company-lookup confirms product/market context |
| People | Conditional (Phase 3) | No subjects known yet; derived from Phase 1 corporate outputs; requires authorisation gate before dispatch |

---

### Phase 1 — Parallel (fire concurrently)

| Skill | Arguments |
|---|---|
| `analyst:company-lookup` | `Visualcare`, engagement dir |
| `investigator:corporate-ownership` | `Visualcare`, engagement dir |
| `investigator:domain-intel` | `visualcare.com.au`, engagement dir |
| `investigator:entity-footprint` | `Visualcare`, engagement dir |
| `investigator:social-media-footprint` | `Visualcare`, engagement dir |

### Phase 2a — After domain-intel (IP-dependent)

| Skill | Arguments |
|---|---|
| `investigator:ip-intel` | `<IP from domain-intel output>`, engagement dir |

### Phase 2b — After company-lookup (market context-dependent)

| Skill | Arguments |
|---|---|
| `analyst:competitive-analysis` | `Visualcare`, engagement dir |

### Phase 3 — Conditional (People)

**Gate required first:** authorisation source, purpose, scope, subject-aware flag. If gate cannot be supplied, Phase 3 is dropped entirely.

Once gate is confirmed and subjects extracted from Phase 1 outputs, fire per subject:
- `investigator:people-lookup`
- `investigator:public-records`
- `investigator:social-media-footprint`

### Final step

`dossier:consolidate` → produces `DOSSIER.md` + `DOSSIER.pdf`

---

### Inline assumptions

1. Entity name assumed to be "Visualcare" — company-lookup will surface exact legal form (Pty Ltd etc.)
2. IP not resolvable at plan time — ip-intel blocks on domain-intel output
3. No people subjects at plan time — extracted from Phase 1 corporate outputs
4. Authorisation gate not yet collected — Phase 3 cannot proceed without it
5. `analyst` plugin assumed installed — if missing, competitive-analysis and company-lookup drop gracefully

**Ready to execute on your say-so.** Confirm to proceed and I'll fire Phase 1 concurrently.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 11.0/11.0 (100%) |
| Evaluated | 2026-05-27 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 146362 ms |
| Target cost | $0.5614 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent restates the target as a domain (`visualcare.com.au`) before doing anything else, distinguishing it from a person or a company name | PASS | Header reads '## Dossier Dispatch Plan — visualcare.com.au'; Technical row notes 'Domain is the primary target'; Assumption 1 distinguishes entity name 'Visualcare' from the domain target. |
| c2 | Agent classifies the target into the right category set — Technical and Corporate at minimum, OSINT typically — using the target-shape table from the skill | PASS | Categories table includes Technical (Yes), Corporate (Yes), OSINT (Yes), Competitive (Yes, Phase 2b), and People (Conditional Phase 3) — all three minimum categories present. |
| c3 | Agent confirms or proposes the engagement directory at `{workspace}/assessments/visualcare` rather than defaulting to `~/Assessments/` or another path | PASS | '**Engagement directory:** `/var/folders/nn/.../assessments/visualcare`' — path follows the required `assessments/visualcare` structure under workspace. |
| c4 | Agent produces a dispatch plan — names each subordinate skill (`/investigator:domain-intel`, `/investigator:ip-intel`, `/investigator:corporate-ownership`, etc.) per category with the argument it would pass — rather than executing them | PASS | Phase 1–3 tables name skills (`investigator:domain-intel`, `investigator:corporate-ownership`, `investigator:ip-intel`, etc.) with arguments; no execution occurred. |
| c5 | Agent does NOT produce any findings prose (no claims about the domain's hosting, ownership, or related entities). The boundary rule says orchestrate, don't investigate. | PASS | Output contains zero findings — no hosting claims, no ownership claims, no WHOIS data. Entire output is plan structure, skill names, and assumptions only. |
| c6 | Agent identifies which skills are mandatory (Technical: domain-intel) vs which depend on what surfaces (Corporate: only if ASIC ownership is in scope) — proposes a sensible default given a domain target | PASS | Phase 1 is parallel mandatory; Phase 2a blocks on domain-intel IP output; Phase 2b blocks on company-lookup market context; Phase 3 is conditional on authorization gate. |
| c7 | Agent flags that the People category is uncertain at this stage — directors are not known until corporate-ownership runs — rather than blindly running people-lookup with no name | PARTIAL | People row: 'No subjects known yet; derived from Phase 1 corporate outputs; requires authorisation gate before dispatch.' Assumption 3: 'No people subjects at plan time — extracted from Phase 1 corporate outputs.' |
| c8 | Agent ends with a clear next step: run the dispatched skills, then run `/dossier:consolidate {workspace}/assessments/visualcare` to compile | PASS | 'Final step: `dossier:consolidate` → produces `DOSSIER.md` + `DOSSIER.pdf`' followed by 'Ready to execute on your say-so. Confirm to proceed and I'll fire Phase 1 concurrently.' |
| c9 | Output's dispatch plan is structured as a table or list keyed by category, naming the skill and the argument per row | PASS | Multiple markdown tables: Categories table (Category \| Decision \| Assumption) and phase tables (Skill \| Arguments) with one skill and arguments per row. |
| c10 | Output names at least three subordinate skills with their `{workspace}/assessments/visualcare`-rooted arguments | PASS | Nine skills named: `analyst:company-lookup`, `investigator:corporate-ownership`, `investigator:domain-intel`, `investigator:entity-footprint`, `investigator:social-media-footprint`, `investigator:ip-intel`, `analyst:competitive-analysis`, `investigator:people-lookup`, `investigator:public-records`. |
| c11 | Output's closing step references `/dossier:consolidate` as the consolidation phase, not as a subordinate skill in the dispatch list | PASS | '### Final step — `dossier:consolidate` → produces `DOSSIER.md` + `DOSSIER.pdf`' appears as a separate section after all phase tables, not embedded in any phase. |
| c12 | Output documents the assumptions made for each "uncertain" category (e.g. "People deferred until directors surface from corporate-ownership") rather than silently skipping | PARTIAL | '### Inline assumptions' section lists 5 numbered assumptions covering entity name, IP resolution, people subjects, authorization gate, and plugin availability. |

### Notes

The output is a near-perfect dispatch plan: all required categories classified, no findings invented, phasing clearly structured, and inline assumptions documented for every uncertain decision. Both PARTIAL-ceiling criteria (c7, c12) were fully addressed, earning their maximum allowed score.
