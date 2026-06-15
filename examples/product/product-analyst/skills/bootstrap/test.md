# Test: bootstrap scaffolds the product-analytics documentation structure

Scenario: A contributor sets up product-analytics documentation for a new project. The skill must create `docs/analytics/` with the product-analyst fragment, a metric-tree template, and an instrumentation-spec template, leave empty placeholder rows rather than inventing metric values, and return a manifest — without overwriting any existing file. The product-analyst never writes `docs/analytics/CLAUDE.md` directly; the coordinator assembles it from the fragments in `_sections/`.

## Prompt

Use the product-analyst `bootstrap` skill to set up the product-analytics documentation structure for a project called "Cadence". Create the structure under `docs/analytics/` relative to the current working directory and return the bootstrap manifest in the skill's standard format.

Proceed without asking — create the files and return the manifest.

## Criteria

- [ ] PASS: Creates the `docs/analytics/` directory (the one canonical path — not `docs/product-analytics/` or a variant) with a `_sections/` subdirectory for the domain fragment
- [ ] PASS: Writes `docs/analytics/_sections/product-analyst.md` as the domain fragment
- [ ] PASS: The fragment is authored at H2 and below — it does not introduce a `# Analytics Domain` H1 (the coordinator generates that when it assembles `docs/analytics/CLAUDE.md`)
- [ ] PASS: The skill does NOT write `docs/analytics/CLAUDE.md` directly — that file is the coordinator's to assemble from `_sections/`
- [ ] PASS: Writes `docs/analytics/metric-tree.md` (North Star + metric-hierarchy template) and `docs/analytics/instrumentation-spec.md` (data-engineer hand-off template)
- [ ] PASS: The fragment states the ownership boundary — the product-analyst defines what to measure and why; the data-engineer builds how data flows (pipelines, warehouse, dashboards)
- [ ] PASS: The fragment states the metric-definition standard (question it answers, definition, calculation, granularity, filters, time window, Goodhart risk, owner)
- [ ] PASS: The fragment states conventions — North Star measures customer value not company revenue, Goodhart check on every metric, vanity/cumulative totals are never a North Star
- [ ] PASS: Does not invent metric values during bootstrap — templates ship with empty placeholder rows, not fabricated North Star or input metrics for "Cadence"
- [ ] PASS: Returns a manifest listing files created, files merged (or "none"), and next steps — not arbitrary prose

## Output expectations

- [ ] PASS: `docs/analytics/_sections/product-analyst.md` exists and lists the available product-analyst skills (define-north-star, design-metric-hierarchy, write-instrumentation-spec, cohort-analysis, design-experiment)
- [ ] PASS: `docs/analytics/metric-tree.md` and `docs/analytics/instrumentation-spec.md` exist with template structure and empty placeholder rows, not invented data
- [ ] PASS: The manifest names the created files and a "Next steps" section pointing at define-north-star and design-metric-hierarchy
- [ ] PARTIAL: The manifest reports a "Files merged" line as "none" given a clean project (idempotency awareness)
