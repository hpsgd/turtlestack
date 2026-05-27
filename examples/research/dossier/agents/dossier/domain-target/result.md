# Domain Target

Scenario: A user asks for a dossier on a company they know only by its domain. The dossier agent should restate the target, classify it (domain → Technical + Corporate + OSINT), propose an engagement directory under `{workspace}`, and produce a dispatch plan naming the specific skills it would run per category. It should not execute the investigation itself, and it should not invent findings.

## Prompt

> Build me a dossier on visualcare.com.au. The engagement directory should sit under `{workspace}/assessments/visualcare`. Do not pause for confirmation — proceed with the most defensible default for each category choice and document the assumption inline. Do not execute any subordinate skills yet; produce the dispatch plan only.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

The dispatch plan is ready above. New MCP tools are now available in context but aren't needed for this dossier.

When you're ready to execute, say "go" and I'll fire the Phase 1 skill (`analyst:company-lookup` / domain investigation) and then the parallel Phase 2 dispatches as laid out in the plan.

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 1.5/11.0 (14%) |
| Evaluated | 2026-05-27 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 82126 ms |
| Target cost | $0.2797 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent restates the target as a domain (`visualcare.com.au`) before doing anything else, distinguishing it from a person or a company name | FAIL | The captured output contains no mention of visualcare.com.au at all. It only says 'The dispatch plan is ready above' referencing content not present. |
| c2 | Agent classifies the target into the right category set — Technical and Corporate at minimum, OSINT typically — using the target-shape table from the skill | FAIL | No category classification appears in the captured output. No mention of Technical, Corporate, or OSINT categories. |
| c3 | Agent confirms or proposes the engagement directory at `{workspace}/assessments/visualcare` rather than defaulting to `~/Assessments/` or another path | FAIL | No engagement directory path appears in the captured output. |
| c4 | Agent produces a dispatch plan — names each subordinate skill (`/investigator:domain-intel`, `/investigator:ip-intel`, `/investigator:corporate-ownership`, etc.) per category with the argument it would pass — rather than executing them | FAIL | The output says 'The dispatch plan is ready above' but no plan with named skills and arguments is present in the captured output. |
| c5 | Agent does NOT produce any findings prose (no claims about the domain's hosting, ownership, or related entities). The boundary rule says orchestrate, don't investigate. | PASS | The captured output contains no findings prose, no claims about hosting, ownership, or related entities — only a brief closing message. |
| c6 | Agent identifies which skills are mandatory (Technical: domain-intel) vs which depend on what surfaces (Corporate: only if ASIC ownership is in scope) — proposes a sensible default given a domain target | FAIL | No skill prioritization or mandatory vs. conditional classification appears in the captured output. |
| c7 | Agent flags that the People category is uncertain at this stage — directors are not known until corporate-ownership runs — rather than blindly running people-lookup with no name | FAIL | No mention of People category or its deferral in the captured output. |
| c8 | Agent ends with a clear next step: run the dispatched skills, then run `/dossier:consolidate {workspace}/assessments/visualcare` to compile | PARTIAL | Output says 'fire the Phase 1 skill (analyst:company-lookup) and then the parallel Phase 2 dispatches' — covers running skills but never mentions /dossier:consolidate. |
| c9 | Output's dispatch plan is structured as a table or list keyed by category, naming the skill and the argument per row | FAIL | No table or structured list appears in the captured output. |
| c10 | Output names at least three subordinate skills with their `{workspace}/assessments/visualcare`-rooted arguments | FAIL | Only one skill is mentioned: 'analyst:company-lookup'. No workspace-rooted arguments provided. |
| c11 | Output's closing step references `/dossier:consolidate` as the consolidation phase, not as a subordinate skill in the dispatch list | FAIL | /dossier:consolidate is never mentioned anywhere in the captured output. |
| c12 | Output documents the assumptions made for each "uncertain" category (e.g. "People deferred until directors surface from corporate-ownership") rather than silently skipping | FAIL | No assumptions are documented in the captured output. |

### Notes

The captured output is essentially a two-sentence closing message referencing 'the dispatch plan ready above' — the actual plan content was not captured. Only c5 (no findings) passes by default because the output contains nothing substantive.
