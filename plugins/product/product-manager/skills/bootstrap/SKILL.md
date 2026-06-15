---
name: bootstrap
bootstrap-phase: product
description: "Bootstrap the product-management documentation structure for a project. Creates docs/product/, generates discovery and roadmap templates, and writes the product-manager fragment of the product domain doc. Idempotent — merges missing sections into existing files without overwriting."
argument-hint: "[project name]"
user-invocable: false
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Bootstrap Product-Management Documentation

Bootstrap the product-management documentation structure for **$ARGUMENTS**.

This sets up the home for discovery artifacts, roadmaps, JTBD canvases, and PRDs that the other product-manager skills (`write-discovery-plan`, `write-roadmap`, `write-prd`, `write-jtbd`, and the rest) write into.

## Step 1: Check and create the domain directory

```bash
mkdir -p docs/product/_sections
```

This step is complete when `docs/product/_sections/` exists.

## Step 2: Create or merge files

For each file below, apply the safe merge pattern:

- If the file does not exist → create from the template
- If the file exists → read both, find sections in the template missing from the file, append only the missing sections with a marker comment `<!-- Merged from product-manager bootstrap v0.1.0 -->`

Never overwrite an existing file wholesale. This step is complete when both files below exist and contain at least the template sections.

### Fragment: `docs/product/_sections/product-manager.md`

`docs/product/CLAUDE.md` is **assembled by the coordinator** from the fragments in `_sections/` — no plugin
writes it directly, so the product-manager and product-owner never collide on it. Write the
product-management contribution as this fragment. It starts at H2 (the coordinator generates the
`# Product Domain` H1):

```markdown
## Product management (PM lens)

This section holds product-management work: problem validation, continuous discovery, JTBD analysis,
the roadmap, and PRDs.

### What this lens covers

- **Discovery** — continuous customer interviews, opportunity solution trees, switch interviews
- **Validation** — assumption maps, pretotypes, experiment design before any build commitment
- **Jobs to Be Done** — functional, emotional, and social jobs; outcome scoring
- **Roadmap** — outcome-shaped Now/Next/Later or GIST, never a feature timeline
- **PRDs** — specced problems handed to the product-owner for execution
- **Voice of customer** — the PM's VoC lens, validated against discovery hypotheses

### The sequence that does not reverse

Problem validation → solution validation → market validation. No PRD is written for a problem
discovery has not confirmed.

### Discovery cadence

- Weekly customer contact, protected on the calendar
- The product trio (PM + designer + engineer) attends every interview
- Recruiting is automated so the cadence is self-sustaining
- The opportunity solution tree updates as evidence arrives — monthly minimum

### Roadmap conventions

A roadmap states the change in customer behaviour expected, not a list of features with dates.

- **Now** — in active discovery or delivery
- **Next** — validated enough to commit to soon
- **Later** — directionally important, not yet validated

### PRD conventions

Every problem larger than ~1 sprint gets a PRD before development. A PRD includes problem
validation, target user, RICE score, success metrics (leading, lagging, guardrail), scope
(in/out/anti-requirements), edge cases, and open questions.

### RICE scoring

RICE = (Reach × Impact × Confidence) / Effort. Show the calculation — never assert "high
priority" without the numbers.

### Tooling

| Tool | Purpose |
|------|---------|
| GitHub Issues | Backlog and roadmap items (owned by product-owner) |
| GitHub Discussions | PRD review, roadmap input, discovery findings |
| useMotion | Discovery cadence and interview scheduling |
| MS 365 | Stakeholder documentation |

### Available skills

| Skill | Purpose |
|-------|---------|
| `/product-manager:write-discovery-plan` | Set up a Torres continuous-discovery cadence |
| `/product-manager:write-interview-guide` | Mom Test generative interview guide |
| `/product-manager:switch-interview` | Moesta four-forces switch interview |
| `/product-manager:write-opportunity-solution-tree` | Build/maintain an OST |
| `/product-manager:synthesise-interviews` | Pattern-code an interview window into OST updates |
| `/product-manager:assumption-map` | Knowledge × impact assumption map |
| `/product-manager:design-pretotype` | Savoia pretotype + MEH hypothesis |
| `/product-manager:write-jtbd` | JTBD analysis (Ulwick + Christensen) |
| `/product-manager:write-roadmap` | Outcome-shaped Now/Next/Later or GIST roadmap |
| `/product-manager:write-prd` | Product Requirements Document |
| `/product-manager:strategic-voc-synthesis` | Validate hypotheses against VoC signal |
| `/product-manager:define-icp` | Firmographic + behavioural ICP |

### Conventions

- No bet reaches the roadmap without problem evidence
- No PRD is written for an unvalidated problem
- Discovery runs weekly; the OST updates monthly
- Pricing and packaging are GTM's call — the PM consults and stays aware
- Strategy authoring is the CPO's — the PM provides slice-level input
```

### File 2: `docs/product/discovery-log.md`

Create with this content:

```markdown
# Discovery log

A running record of customer contact so the team never loses the thread. One row per interview.

## Cadence

| Field | Value |
|-------|-------|
| Recurring slot | [e.g. Tuesdays 11:00] |
| Trio | [PM / designer / engineer names] |
| Recruiting source | [in-product prompt / CS / panel] |
| Desired outcome | [the metric this discovery serves] |

## Interview log

| Date | Participant (segment) | Type (generative / switch) | Key signal | OST node touched |
|------|-----------------------|----------------------------|------------|------------------|
| | | | | |

## Theme saturation

Track when new interviews stop producing new themes — that is your saturation signal.

| Theme | First seen | Times confirmed | Saturated? |
|-------|------------|-----------------|------------|
| | | | |
```

## Step 3: Return a manifest

After creating or merging the files, output:

```
## Product-Manager Bootstrap Complete

### Files created
- `docs/product/_sections/product-manager.md` — product-manager's fragment of the product domain doc (assembled into `docs/product/CLAUDE.md` by the coordinator)
- `docs/product/discovery-log.md` — running discovery record

### Files merged
- [list any existing files where sections were appended, or "none"]

### Next steps
- Set up a discovery cadence with `/product-manager:write-discovery-plan`
- Frame the problem space with `/product-manager:write-jtbd`
- Stand up an opportunity solution tree with `/product-manager:write-opportunity-solution-tree`
```

## Rules

- **Write only your own fragment.** `docs/product/CLAUDE.md` is assembled by the coordinator; this skill writes `docs/product/_sections/product-manager.md` and nothing else. The product-owner writes its own fragment — there is no shared file to clobber.
- **Safe-merge the fragment, idempotent by design.** If the fragment exists, preserve user-authored content and append only missing template sections with the merge marker — never overwrite. Running twice produces no duplicate sections.
- **Don't invent project specifics.** Leave bracketed placeholders for the team to fill — don't guess the trio's names or the recurring slot.

## Output Format

The manifest in Step 3 is the output. Report files created, files merged, and next steps. Nothing else.
