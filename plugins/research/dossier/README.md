# Dossier

Build a single brand-styled PDF dossier from research outputs that conform to the report frontmatter contract. Two modes:

- **`/dossier:consolidate`** — back end. Scan an engagement directory, group conforming reports by category, produce `DOSSIER.md` + `DOSSIER.pdf`. Use this when reports already exist (you ran individual skills or wrote them by hand).
- **`/dossier:dossier`** (agent, drive mode) — front end. Name a target ("dossier on visualcare.com.au"), the agent asks what kind of investigation is wanted, dispatches the right skills with consistent arguments, then calls consolidate.

## What counts as a conforming report

Any markdown file inside the engagement directory whose YAML frontmatter declares all four required fields: `title`, `date`, `author`, `category`. See the `report-conventions.md` rule for the full contract.

The dossier doesn't care which plugin produced the file. Investigator outputs, analyst outputs, reports written by hand — all picked up if they conform. Files that don't conform are listed separately so the user can fix them or accept exclusion.

## Quick start — consolidate an existing engagement

```
/dossier:consolidate ~/Assessments/visualcare
```

The skill scans the directory, lists eligible files grouped by category, asks for any exclusions, then writes `DOSSIER.md` and renders `DOSSIER.pdf`.

## Quick start — drive a fresh campaign

Invoke the dossier agent and name a target. The agent walks you through:

1. What kind of target it is (domain, company, person, mixed)
2. Which engagement directory to use (default: `~/Assessments/<slug>/`)
3. Which categories to investigate (People, Corporate, Technical, Commercial, OSINT)
4. Which subjects under each category
5. Authorisation gate (if any People-category subjects)

It then dispatches skills, gathers outputs, and runs consolidate at the end.

## Engagement directory layout

```
~/Assessments/visualcare/
├── people-lookup/
│   ├── graves-michael.md
│   └── lau-susan.md
├── domain-intel/
│   └── visualcare-com-au.md
├── corporate-ownership/
│   └── visual-data-solutions-pty-ltd.md
├── DOSSIER.md           # produced by consolidate
└── DOSSIER.pdf          # rendered from DOSSIER.md
```

Each skill writes one file per invocation under `<engagement_dir>/<skill-name>/<subject-slug>.md`. The consolidate skill produces `DOSSIER.md` at the engagement root and renders the PDF alongside it.

## Dependencies

- **`/publishing:write-document-pdf`** — the renderer. If not installed, consolidate will produce the markdown but skip the PDF and tell you.
- **The `report-conventions.md` rule** — installed automatically when the dossier plugin is enabled (the rule also lives in `analyst` and `investigator`; any of those installs is sufficient).

## When not to use this

- You only need one report. Just run the relevant skill directly.
- The reports you want to consolidate don't conform to the report-conventions rule and you can't fix them. Either fix the producer (preferred) or write the dossier markdown by hand.
- You want a slim "synopsis-only" dossier. The current consolidate skill embeds full content. A separate skill would handle the slim case if there's demand.
