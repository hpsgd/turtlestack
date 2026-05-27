---
# Match the model the agent declares (sonnet) in
# plugins/research/dossier/agents/dossier.md. The runner otherwise
# falls back to the harness default (Haiku), which is not what the
# agent is designed to run on.
target-model: claude-sonnet-4-6
---

# Test: dossier driver categorises a domain target and proposes the right skills

Scenario: A user asks for a dossier on a company they know only by its domain. The dossier agent should restate the target, classify it (domain → Technical + Corporate + OSINT), propose an engagement directory under `{workspace}`, and produce a dispatch plan naming the specific skills it would run per category. It should not execute the investigation itself, and it should not invent findings.

## Prompt

Build me a dossier on visualcare.com.au. The engagement directory should sit under `{workspace}/assessments/visualcare`. Do not pause for confirmation — proceed with the most defensible default for each category choice and document the assumption inline. Do not execute any subordinate skills yet; produce the dispatch plan only.

## Criteria

- [ ] PASS: Agent restates the target as a domain (`visualcare.com.au`) before doing anything else, distinguishing it from a person or a company name
- [ ] PASS: Agent classifies the target into the right category set — Technical and Corporate at minimum, OSINT typically — using the target-shape table from the skill
- [ ] PASS: Agent confirms or proposes the engagement directory at `{workspace}/assessments/visualcare` rather than defaulting to `~/Assessments/` or another path
- [ ] PASS: Agent produces a dispatch plan — names each subordinate skill (`/investigator:domain-intel`, `/investigator:ip-intel`, `/investigator:corporate-ownership`, etc.) per category with the argument it would pass — rather than executing them
- [ ] PASS: Agent does NOT produce any findings prose (no claims about the domain's hosting, ownership, or related entities). The boundary rule says orchestrate, don't investigate.
- [ ] PASS: Agent identifies which skills are mandatory (Technical: domain-intel) vs which depend on what surfaces (Corporate: only if ASIC ownership is in scope) — proposes a sensible default given a domain target
- [ ] PARTIAL: Agent flags that the People category is uncertain at this stage — directors are not known until corporate-ownership runs — rather than blindly running people-lookup with no name
- [ ] PASS: Agent ends with a clear next step: run the dispatched skills, then run `/dossier:consolidate {workspace}/assessments/visualcare` to compile

## Output expectations

- [ ] PASS: Output's dispatch plan is structured as a table or list keyed by category, naming the skill and the argument per row
- [ ] PASS: Output names at least three subordinate skills with their `{workspace}/assessments/visualcare`-rooted arguments
- [ ] PASS: Output's closing step references `/dossier:consolidate` as the consolidation phase, not as a subordinate skill in the dispatch list
- [ ] PARTIAL: Output documents the assumptions made for each "uncertain" category (e.g. "People deferred until directors surface from corporate-ownership") rather than silently skipping
