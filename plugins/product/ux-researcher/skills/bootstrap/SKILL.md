---
name: bootstrap
bootstrap-phase: product
description: "Bootstrap the UX research documentation structure for a project. Writes the ux-researcher fragment of the design domain doc and copies persona/journey-map templates. Idempotent — merges missing sections into existing files without overwriting."
argument-hint: "[project name]"
user-invocable: false
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Bootstrap UX Research Documentation

Bootstrap the UX research documentation structure for **$ARGUMENTS**.

## Process

### Step 1: Check and create domain directory

```bash
mkdir -p docs/design/_sections
```

### Step 2: Create or merge files

For each file below, apply the safe merge pattern:
- If file does not exist → create from template
- If file exists → read both, find sections in template missing from file, append missing sections with `<!-- Merged from ux-researcher bootstrap v0.1.0 -->`

#### Fragment: `docs/design/_sections/ux-researcher.md`

`docs/design/CLAUDE.md` is **assembled by the coordinator** from the fragments in `_sections/` — no plugin
writes it directly, so the ux-researcher and ui-designer never collide on it. Write the UX research
contribution as this fragment. It starts at H2 (the coordinator generates the `# Design Domain` H1):

```markdown
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

#### File 2: `docs/design/persona-template.md`

Copy from the plugin template at `plugins/product/ux-researcher/templates/persona.md`.

If the file already exists, do not overwrite — leave it as-is.

#### File 3: `docs/design/journey-map-template.md`

Copy from the plugin template at `plugins/product/ux-researcher/templates/journey-map.md`.

If the file already exists, do not overwrite — leave it as-is.

### Step 3: Return manifest

After creating/merging all files, output a summary:

```
## UX Research Bootstrap Complete

### Files created
- `docs/design/_sections/ux-researcher.md` — ux-researcher's fragment of the design domain doc (assembled into `docs/design/CLAUDE.md` by the coordinator)
- `docs/design/persona-template.md` — persona card template
- `docs/design/journey-map-template.md` — journey map template

### Files merged
- (list any existing files where sections were appended)

### Next steps
- Create initial personas using `/ux-researcher:persona-definition`
- Map critical user journeys using `/ux-researcher:journey-map`
- Run `/ux-researcher:usability-review` on existing interfaces
```

## Rules

- **Write only your own fragment.** `docs/design/CLAUDE.md` is assembled by the coordinator; this skill writes `docs/design/_sections/ux-researcher.md` and nothing else. The ui-designer writes its own fragment — there is no shared file to clobber.
- **Safe-merge the fragment, idempotent by design.** If the fragment exists, preserve user-authored content and append only missing template sections with the merge marker — never overwrite. Running twice produces no duplicate sections.
- **Don't overwrite the templates.** If `persona-template.md` or `journey-map-template.md` already exist, leave them as-is.

## Output Format

The manifest in Step 3 is the output. Report files created, files merged, and next steps. Nothing else.
