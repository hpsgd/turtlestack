# Bootstrap

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/design/CLAUDE.md` containing a user-authored section. The ux-researcher bootstrap skill should preserve that user content while appending the UX research conventions (with a merge marker), and should create the two template files the fixture is missing — `persona-template.md` and `journey-map-template.md`. The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

> The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/design/CLAUDE.md` is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.
> 
> Read the ux-researcher bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/product/ux-researcher/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.
> 
> After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## UX Research Bootstrap Complete

### Files created
- `docs/design/persona-template.md` — persona card template
- `docs/design/journey-map-template.md` — journey map template

### Files merged
- `docs/design/CLAUDE.md` — appended UX research conventions (safe merge: preserved existing "Custom team notes" section with USER-EDIT-SENTINEL)

### Next steps
- Create initial personas using `/ux-researcher:persona-definition`
- Map critical user journeys using `/ux-researcher:journey-map`
- Run `/ux-researcher:usability-review` on existing interfaces

### Artifacts written

#### `work/docs/design/journey-map-template.md`

```
# Journey Map — {{journey_name}}

| Field          | Value              |
|----------------|--------------------|
| User type      | {{persona or segment}} |
| Journey        | {{journey_name}}   |
| Author         | {{author}}         |
| Last updated   | {{date}}           |

## Scope

| Dimension    | Value |
|-------------|-------|
| Start point | {{e.g. "User realises they have a problem"}} |
| End point   | {{e.g. "User achieves first value milestone"}} |
| Success metric | {{e.g. activation rate, time-to-value}} |
| Time span   | {{typical elapsed time from start to end}} |

## Journey stages

### Stage 1: {{stage_name — e.g. Awareness}}

| Dimension | Detail |
|-----------|--------|
| Touchpoints | {{e.g. blog post, peer recommendation, ad}} |
| Actions | {{what the user does}} |
| Thinking | {{internal questions or considerations}} |
| Feeling | {{emotional state — e.g. curious, frustrated, hopeful}} |
| Pain points | {{friction or obstacles}} |
| Opportunities | {{how we could improve this stage}} |
| Drop-off risk | {{low / medium / high}} |

### Stage 2: {{stage_name — e.g. Evaluation}}

| Dimension | Detail |
|-----------|--------|
| Touchpoints | {{e.g. website, docs, competitor comparison}} |
| Actions | {{what the user does}} |
| Thinking | {{internal questions}} |
| Feeling | {{emotional state}} |
| Pain points | {{friction}} |
| Opportunities | {{improvements}} |
| Drop-off risk | {{low / medium / high}} |

### Stage 3: {{stage_name — e.g. Onboarding}}

| Dimension | Detail |
|-----------|--------|
| Touchpoints | {{e.g. signup flow, welcome email, first-run wizard}} |
| Actions | {{what the user does}} |
| Thinking | {{internal questions}} |
| Feeling | {{emotional state}} |
| Pain points | {{friction}} |
| Opportunities | {{improvements}} |
| Drop-off risk | {{low / medium / high}} |

### Stage 4: {{stage_name — e.g. First value}}

| Dimension | Detail |
|-----------|--------|
| Touchpoints | {{e.g. core feature, integration, dashboard}} |
| Actions | {{what the user does}} |
| Thinking | {{internal questions}} |
| Feeling | {{emotional state}} |
| Pain points | {{friction}} |
| Opportunities | {{improvements}} |
| Drop-off risk | {{low / medium / high}} |

### Stage 5: {{stage_name — e.g. Habit / Expansion}}

| Dimension | Detail |
|-----------|--------|
| Touchpoints | {{e.g. advanced features, team invite, billing}} |
| Actions | {{what the user does}} |
| Thinking | {{internal questions}} |
| Feeling | {{emotional state}} |
| Pain points | {{friction}} |
| Opportunities | {{improvements}} |
| Drop-off risk | {{low / medium / high}} |

> Add or remove stages to match the actual journey.

## Critical moments

| Moment | Stage | Why it matters | Current experience | Desired experience |
|--------|-------|---------------|-------------------|-------------------|
| {{moment_1}} | {{stage}} | {{impact on conversion/retention}} | {{current state}} | {{target state}} |
| {{moment_2}} | {{stage}} | {{impact}} | {{current}} | {{desired}} |

## Journey health summary

| Stage | Conversion / completion | Satisfaction | Biggest gap |
|-------|------------------------|-------------|-------------|
| {{stage_1}} | {{rate}} | {{high/med/low}} | {{gap}} |
| {{stage_2}} | {{rate}} | {{satisfaction}} | {{gap}} |
| {{stage_3}} | {{rate}} | {{satisfaction}} | {{gap}} |
| {{stage_4}} | {{rate}} | {{satisfaction}} | {{gap}} |
| {{stage_5}} | {{rate}} | {{satisfaction}} | {{gap}} |

## Recommendations

| Priority | Recommendation | Stage | Expected impact | Effort |
|----------|---------------|-------|----------------|--------|
| 1 | {{recommendation}} | {{stage}} | {{impact}} | {{S/M/L}} |
| 2 | {{recommendation}} | {{stage}} | {{impact}} | {{effort}} |
| 3 | {{recommendation}} | {{stage}} | {{impact}} | {{effort}} |

## Change log

| Date | Change | Author |
|------|--------|--------|
|      |        |        |

```

#### `work/docs/design/persona-template.md`

```
# Persona Card — {{archetype_name}}

| Field          | Value            |
|----------------|------------------|
| Archetype      | {{archetype_name}} |
| Segment        | {{segment — e.g. mid-market engineering managers}} |
| Author         | {{author}}       |
| Last updated   | {{date}}         |

## Evidence base

| Source | Count | Recency |
|--------|-------|---------|
| User interviews | {{n}} | {{date range}} |
| Survey responses | {{n}} | {{date}} |
| Analytics cohort | {{n users}} | {{period}} |
| Support tickets | {{n}} | {{period}} |

**Confidence:** {{high / medium / low — based on evidence volume and recency}}

## Context

| Dimension | Description |
|-----------|-------------|
| Role | {{e.g. Senior backend engineer}} |
| Organisation size | {{e.g. 50-200 employees}} |
| Tech sophistication | {{low / medium / high / expert}} |
| Decision authority | {{end user / influencer / budget holder / decision maker}} |
| Time pressure | {{low / medium / high — how urgent is their need}} |
| Tool landscape | {{key tools they already use}} |

## Goals (ranked)

| Priority | Goal | Frequency |
|----------|------|-----------|
| 1 | {{primary goal}} | {{daily / weekly / ad-hoc}} |
| 2 | {{secondary goal}} | {{frequency}} |
| 3 | {{tertiary goal}} | {{frequency}} |

## Frustrations (ranked)

| Priority | Frustration | Severity | Current workaround |
|----------|------------|----------|-------------------|
| 1 | {{frustration_1}} | {{high/med/low}} | {{workaround}} |
| 2 | {{frustration_2}} | {{severity}} | {{workaround}} |
| 3 | {{frustration_3}} | {{severity}} | {{workaround}} |

## Behaviour patterns

| Pattern | Description |
|---------|-------------|
| Discovery | {{How they find new tools — e.g. peer recommendations, Hacker News, vendor outreach}} |
| Evaluation | {{How they assess options — e.g. free trial, POC, read docs first}} |
| Decision trigger | {{What makes them decide to adopt — e.g. hits pain threshold, team request, mandate}} |
| Learning style | {{e.g. reads docs end-to-end, learns by doing, watches videos}} |
| Collaboration | {{How they work with others — async, pairing, delegates}} |

## Success criteria

> How does this persona define "success" with our product?

- {{criterion_1 — e.g. "reduced deploy time from 30 min to 5 min"}}
- {{criterion_2}}
- {{criterion_3}}

## Anti-persona signals

> Indicators that someone is NOT this persona (avoid targeting them as such):

- {{signal_1 — e.g. "No engineering background"}}
- {{signal_2 — e.g. "Organisation < 10 people"}}
- {{signal_3}}

## Representative quote

> "{{A real or composite quote that captures this persona's mindset.}}"

## Change log

| Date | Change | Author |
|------|--------|--------|
|      |        |        |

```

#### `work/docs/design/CLAUDE.md`

```
# Design Domain

This directory contains design and UX research documentation.

## Custom team notes

USER-EDIT-SENTINEL-DO-NOT-STRIP

This section was written by the team and must survive any bootstrap re-run.
It exists to test the safe-merge contract: the bootstrap skill must not
overwrite or remove user-authored content.

<!-- UX Research section — added by ux-researcher bootstrap v0.1.0 -->

## UX Research

This section covers UX research methodology, persona definitions, journey maps, and usability review conventions.

### What UX Research Covers

- **Personas** — evidence-based user archetypes
- **Journey maps** — end-to-end user experience visualisation
- **Usability reviews** — heuristic evaluation of interfaces
- **Usability test plans** — structured testing protocols
- **Service blueprints** — front-stage and back-stage service mapping

### Research Methodology

#### Research types

| Type | When | Output |
|------|------|--------|
| **Discovery** | New product/feature area | Personas, JTBD canvases, opportunity map |
| **Evaluative** | Existing design or prototype | Usability findings, severity ratings |
| **Continuous** | Ongoing | Analytics insights, feedback synthesis |

#### Evidence hierarchy
1. **Behavioural data** — what users actually do (analytics, session recordings)
2. **Observation** — watching users attempt tasks (usability tests)
3. **Self-reported** — what users say they do (interviews, surveys)

Weight findings by evidence quality. Behavioural data trumps self-reported preferences.

### Persona Format

Personas describe behaviour, not demographics. Every persona must include:

| Section | Required | Purpose |
|---------|----------|---------|
| Evidence base | Yes | Sources, sample size, recency — establishes confidence |
| Context | Yes | Role, organisation size, tech sophistication, decision authority |
| Goals (ranked) | Yes | What they are trying to achieve, with frequency |
| Frustrations (ranked) | Yes | Current pain points with severity and workarounds |
| Behaviour patterns | Yes | Discovery, evaluation, decision trigger, learning style |
| Success criteria | Yes | How they define success with the product |
| Anti-persona signals | Recommended | Indicators someone is NOT this persona |

**Rule:** Never include age, gender, or stock photos. Personas are archetypes, not stereotypes.

### Usability Heuristics (Nielsen)

Use these 10 heuristics for usability reviews:

1. Visibility of system status
2. Match between system and real world
3. User control and freedom
4. Consistency and standards
5. Error prevention
6. Recognition rather than recall
7. Flexibility and efficiency of use
8. Aesthetic and minimalist design
9. Help users recognise, diagnose, and recover from errors
10. Help and documentation

Rate findings: **Critical** (blocks task) / **Major** (significant friction) / **Minor** (cosmetic or low-impact).

### Journey Mapping Process

1. **Define scope** — start point, end point, and success metric
2. **Identify stages** — typically 4–6 stages the user moves through
3. **Map dimensions** — for each stage: touchpoints, actions, thinking, feeling, pain points, opportunities
4. **Identify critical moments** — high-impact moments that affect conversion or retention
5. **Prioritise recommendations** — rank improvements by expected impact and effort

### UX Research Tooling

| Tool | Purpose |
|------|---------|
| GitHub Discussions | Research findings and synthesis |
| MS 365 | Research reports, presentation decks |
| Figma | Prototype testing (if applicable) |

### Available UX Research Skills

| Skill | Purpose |
|-------|---------|
| `/ux-researcher:persona-definition` | Create an evidence-based persona |
| `/ux-researcher:journey-map` | Map an end-to-end user journey |
| `/ux-researcher:usability-review` | Conduct a heuristic usability review |
| `/ux-researcher:usability-test-plan` | Create a usability test plan |
| `/ux-researcher:service-blueprint` | Create a service blueprint |

### UX Research Conventions

- Personas are living documents — update when new evidence contradicts existing assumptions
- Every persona must cite its evidence base (interviews, analytics, surveys)
- Journey maps start from user intent, not from the product's navigation
- Usability findings are rated by severity and mapped to heuristics
- Research findings are shared in GitHub Discussions for team visibility

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/8.5 (88%) |
| Evaluated | 2026-05-13 |
| Target duration | 42520 ms |
| Target cost | $0.1398 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | After bootstrap, `docs/design/CLAUDE.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim | PASS | Artifact shows '## Custom team notes\n\nUSER-EDIT-SENTINEL-DO-NOT-STRIP' intact in the merged CLAUDE.md. |
| c2 | After bootstrap, `docs/design/CLAUDE.md` contains the merge marker `<!-- Merged from ux-researcher bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged | FAIL | Artifact contains '<!-- UX Research section — added by ux-researcher bootstrap v0.1.0 -->' but not the exact required string '<!-- Merged from ux-researcher bootstrap v0.1.0 -->'. |
| c3 | After bootstrap, `docs/design/CLAUDE.md` contains the appended UX research sections — at minimum the `## UX Research` heading and `### Persona Format` heading now appear alongside the preserved user content | PASS | Artifact shows '## UX Research' and '### Persona Format' both present after the preserved user section. |
| c4 | After bootstrap, `docs/design/persona-template.md` exists and was copied from the plugin template (contains `# Persona Card` heading and `## Evidence base` section) | PASS | Artifact persona-template.md opens with '# Persona Card — {{archetype_name}}' and contains '## Evidence base' section. |
| c5 | After bootstrap, `docs/design/journey-map-template.md` exists and was copied from the plugin template (contains `# Journey Map` heading and `## Scope` section) | PASS | Artifact journey-map-template.md opens with '# Journey Map — {{journey_name}}' and contains '## Scope' section. |
| c6 | Chat output includes a manifest summary that distinguishes files created (`persona-template.md`, `journey-map-template.md`) from files merged (`CLAUDE.md`) | PASS | Chat response has distinct '### Files created' and '### Files merged' sections listing the correct files under each. |
| c7 | Output names each created and merged file individually — a bare "bootstrap complete" without the per-file manifest is not enough | PASS | Each file named individually: persona-template.md, journey-map-template.md under created; CLAUDE.md under merged. |
| c8 | Output does not claim it overwrote or replaced `docs/design/CLAUDE.md` — the language reflects merge or append, not replacement | PASS | Chat says 'appended UX research conventions (safe merge: preserved existing "Custom team notes" section with USER-EDIT-SENTINEL)' — no replacement language. |
| c9 | Output points the reader at next steps (using persona-definition and journey-map skills) consistent with the skill's documented manifest | PARTIAL | Chat lists '### Next steps' referencing /ux-researcher:persona-definition, /ux-researcher:journey-map, and /ux-researcher:usability-review. |

### Notes

The bootstrap executed correctly on all structural requirements — sentinel preserved, templates created, UX sections appended, manifest output clear. The only failure is c2: the actual merge comment ('added by') does not match the required exact string ('Merged from'), losing 1 point.
