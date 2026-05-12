# Test: consolidate engagement reports into a single dossier

Scenario: An engagement directory under `{workspace}/work/visualcare/` contains three conforming research reports across two categories (one People, two Technical). The fixtures are pre-staged by the harness from `fixtures/visualcare/`. The consolidate skill should detect them, group them by category, produce a `DOSSIER.md` with each report embedded under its category, and render a brand-styled PDF.

The skill's design is "terse chat + rich artifact": the chat output is intentionally a short completion summary (report count, output paths), with every per-file detail captured inside the written `DOSSIER.md`. Criteria below evaluate the artifact as the primary source of truth, treating the chat as a confirmation surface, not a verbose progress log.

## Prompt

The engagement directory at `{workspace}/work/visualcare/` already contains three research reports staged by the test harness:

- `people-lookup/graves-michael.md` (category: People)
- `domain-intel/visualcare-com-au.md` (category: Technical)
- `ip-intel/52-12-34-56.md` (category: Technical)

Run `/dossier:consolidate {workspace}/work/visualcare` to produce the dossier. Do not pause for confirmation — proceed with all defaults.

## Criteria

- [ ] PASS: Skill resolves the engagement directory to the absolute path under `{workspace}` — evidence may be the absolute path appearing in chat output paths, an explicit confirmation line, or both
- [ ] PASS: Skill detects all three fixture files — evidence may be a per-file enumeration in chat OR all three reports appearing in the written `DOSSIER.md`. A count summary in chat ("3 reports across 2 categories") is acceptable when the per-file detail is present in the artifact.
- [ ] PASS: Skill orders reports by category — People reports first, then Technical (per the skill's category-ordering rule) — sorted within category by subject then date
- [ ] PASS: Skill writes `DOSSIER.md` to the engagement directory with the three source reports embedded inline, each as its own h1 page break
- [ ] PASS: Skill renders a PDF of the dossier (skill output names the rendered PDF path, and a `.pdf` file lands in the engagement directory) — OR — if rendering is unavailable in the test environment, the skill stops cleanly and reports that rendering would be the next step rather than silently skipping
- [ ] PASS: Each embedded report's body content is preserved verbatim — no body rewriting. Frontmatter stripping is intentional per the skill's template; titles become h1 page breaks.
- [ ] PARTIAL: Skill flags any body `h1` violations from the source reports — explicitly stating "no body-h1 warnings" when the fixture is clean. Silence is acceptable when no warnings exist, but an explicit statement is preferred.
- [ ] PASS: A re-run of consolidate against the same directory does not ingest the previous `DOSSIER.md` (`category: Dossier` is excluded) — evidence may be the `category: Dossier` line in the generated artifact's frontmatter, which is the exclusion mechanism. A demonstrated re-run is not required.

## Output expectations

- [ ] PASS: Output's `DOSSIER.md` orders reports People first then Technical, with each report's title rendered as h1 (per the page-break-per-report rule)
- [ ] PASS: Output's category ordering is stable — sorted reports within each category by subject then date — re-running on the same inputs produces the same ordering
- [ ] PASS: Output reports the file path of the generated `DOSSIER.md` (and the PDF if rendering succeeded) so the user can open the result without searching
- [ ] PARTIAL: Chat output identifies the three input files individually — either by listing them before consolidating or by naming them in a per-file summary line. A bare count ("3 reports") satisfies a PARTIAL ceiling here, since the per-file detail is recoverable from `DOSSIER.md` itself.
