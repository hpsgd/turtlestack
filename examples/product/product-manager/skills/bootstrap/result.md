# Bootstrap

Scenario: A contributor sets up product-management documentation for a new project. The skill must create `docs/product/` with its own fragment `docs/product/_sections/product-manager.md` and a discovery log, leave bracketed placeholders rather than inventing project specifics, and return a manifest — without writing the shared `docs/product/CLAUDE.md` (the coordinator assembles that from the fragments).

## Prompt

> Use the product-manager `bootstrap` skill to set up the product-management documentation structure for a
> project called "Cadence". Create the structure under `docs/product/` relative to the current working
> directory and return the bootstrap manifest in the skill's standard format.
> 
> Proceed without asking — create the files and return the manifest.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Product-Manager Bootstrap Complete

### Files created
- `docs/product/_sections/product-manager.md` — product-manager's fragment of the product domain doc (assembled into `docs/product/CLAUDE.md` by the coordinator)
- `docs/product/discovery-log.md` — running discovery record

### Files merged
- none

### Next steps
- Set up a discovery cadence with `/product-manager:write-discovery-plan`
- Frame the problem space with `/product-manager:write-jtbd`
- Stand up an opportunity solution tree with `/product-manager:write-opportunity-solution-tree`

### Artifacts written

#### `work/docs/product/discovery-log.md`

```
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

#### `work/docs/product/_sections/product-manager.md`

```
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

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 13.5/13.5 (100%) |
| Evaluated | 2026-06-15 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 32612 ms |
| Target cost | $0.0693 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Creates the `docs/product/_sections/` directory and writes its fragment `docs/product/_sections/product-manager.md` | PASS | Artifact `work/docs/product/_sections/product-manager.md` is present and contains the full PM fragment. |
| c2 | The fragment starts at an H2 heading — it contains no `# ` H1 (the coordinator generates the `# Product Domain` H1 when it assembles `docs/product/CLAUDE.md`) | PASS | Fragment opens with `## Product management (PM lens)` — no H1 present anywhere in the file. |
| c3 | The skill does NOT write `docs/product/CLAUDE.md` directly — that file is assembled by the coordinator from `_sections/` | PASS | Only two artifacts listed: discovery-log.md and _sections/product-manager.md. No CLAUDE.md artifact exists. |
| c4 | Writes a `docs/product/discovery-log.md` with a cadence block, an interview log table, and a theme-saturation table | PASS | discovery-log.md contains a Cadence table, an Interview log table, and a Theme saturation table — all three present. |
| c5 | The fragment states the non-reversing sequence: problem validation → solution validation → market validation | PASS | Section `### The sequence that does not reverse`: "Problem validation → solution validation → market validation." |
| c6 | The fragment states roadmap convention as outcome-shaped Now/Next/Later (change in customer behaviour), not a feature timeline | PASS | "A roadmap states the change in customer behaviour expected, not a list of features with dates." with Now/Next/Later definitions. |
| c7 | The fragment states the boundaries — pricing/packaging is GTM's call (PM consults), strategy authoring is the CPO's (PM gives slice-level input) | PASS | Conventions section: "Pricing and packaging are GTM's call — the PM consults" and "Strategy authoring is the CPO's — the PM provides slice-level input." |
| c8 | Leaves bracketed placeholders (e.g. recurring slot, trio names) rather than inventing project specifics like real names or times | PASS | discovery-log.md uses `[e.g. Tuesdays 11:00]`, `[PM / designer / engineer names]`, `[in-product prompt / CS / panel]`, `[the metric this discovery serves]`. |
| c9 | Returns a manifest listing files created, files merged (or "none"), and next steps — not arbitrary prose | PASS | Chat response has structured sections: `### Files created`, `### Files merged` ("- none"), `### Next steps` with three items. |
| c10 | `docs/product/_sections/product-manager.md` exists and lists the available product-manager skills (discovery plan, interview guide, roadmap, PRD, JTBD, etc.) | PASS | Fragment has `### Available skills` table listing 12 skills including write-discovery-plan, write-jtbd, write-roadmap, write-prd, write-interview-guide. |
| c11 | `docs/product/discovery-log.md` exists with the cadence / interview-log / saturation structure | PASS | Artifact `work/docs/product/discovery-log.md` confirmed with all three sections: Cadence, Interview log, Theme saturation. |
| c12 | The manifest names both created files and a "Next steps" section pointing at write-discovery-plan, write-jtbd, or write-opportunity-solution-tree | PASS | Next steps: `/product-manager:write-discovery-plan`, `/product-manager:write-jtbd`, `/product-manager:write-opportunity-solution-tree` — all three present. |
| c13 | Output does not fabricate a trio, a recurring slot, or a desired outcome — placeholders remain bracketed | PASS | No real names, times, or outcomes appear anywhere. Trio field is `[PM / designer / engineer names]`, slot is `[e.g. Tuesdays 11:00]`. |
| c14 | The manifest reports a "Files merged" line as "none" given a clean project (idempotency awareness) | PARTIAL | Manifest has `### Files merged` with `- none` — idempotency awareness is explicit. |

### Notes

All criteria met perfectly. The skill produced well-structured artifacts with no fabricated specifics, correct H2-only fragment structure, no CLAUDE.md written, and a fully compliant manifest.
