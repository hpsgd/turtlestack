# Test: bootstrap scaffolds the product-management documentation structure

Scenario: A contributor sets up product-management documentation for a new project. The skill must create
`docs/product/` with a domain CLAUDE.md and a discovery log, leave bracketed placeholders rather than
inventing project specifics, and return a manifest — without overwriting any existing file.

## Prompt

Use the product-manager `bootstrap` skill to set up the product-management documentation structure for a
project called "Cadence". Create the structure under `docs/product/` relative to the current working
directory and return the bootstrap manifest in the skill's standard format.

Proceed without asking — create the files and return the manifest.

## Criteria

- [ ] PASS: Creates the `docs/product/` directory and writes a `docs/product/CLAUDE.md` domain file
- [ ] PASS: Writes a `docs/product/discovery-log.md` with a cadence block, an interview log table, and a theme-saturation table
- [ ] PASS: The domain CLAUDE.md states the non-reversing sequence: problem validation → solution validation → market validation
- [ ] PASS: The domain CLAUDE.md states roadmap convention as outcome-shaped Now/Next/Later (change in customer behaviour), not a feature timeline
- [ ] PASS: The domain CLAUDE.md states the boundaries — pricing/packaging is GTM's call (PM consults), strategy authoring is the CPO's (PM gives slice-level input)
- [ ] PASS: Leaves bracketed placeholders (e.g. recurring slot, trio names) rather than inventing project specifics like real names or times
- [ ] PASS: Returns a manifest listing files created, files merged (or "none"), and next steps — not arbitrary prose

## Output expectations

- [ ] PASS: `docs/product/CLAUDE.md` exists and lists the available product-manager skills (discovery plan, interview guide, roadmap, PRD, JTBD, etc.)
- [ ] PASS: `docs/product/discovery-log.md` exists with the cadence / interview-log / saturation structure
- [ ] PASS: The manifest names both created files and a "Next steps" section pointing at write-discovery-plan, write-jtbd, or write-opportunity-solution-tree
- [ ] PASS: Output does not fabricate a trio, a recurring slot, or a desired outcome — placeholders remain bracketed
- [ ] PARTIAL: The manifest reports a "Files merged" line as "none" given a clean project (idempotency awareness)
