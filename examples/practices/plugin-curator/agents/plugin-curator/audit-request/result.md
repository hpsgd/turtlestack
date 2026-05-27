# Audit Request

Scenario: User asks the plugin-curator agent to audit an existing agent definition for structural consistency, expecting a structured report against the template criteria.

## Prompt

> Can you audit the `qa` agent for me? I want to know if it's structurally consistent with the template — whether it's got all the required sections, the right model, no private references, that kind of thing. Just give me the full breakdown. Audit the `qa-lead` agent specifically (located at `/Users/martin/Projects/turtlestack/plugins/engineering/qa-lead/agents/qa-lead.md`). Proceed without asking — the user has confirmed `qa-lead` is the target.
> 
> A few specifics for the response:
> 
> - **Pre-flight section at top** — labelled `## Pre-flight Reads` listing each Read with absolute path:
>   ```
>   Read: /Users/martin/Projects/turtlestack/CLAUDE.md
>   Read: /Users/martin/Projects/turtlestack/.claude-plugin/marketplace.json
>   Read: /Users/martin/Projects/turtlestack/plugins/practices/plugin-curator/templates/agent-template.md
>   Read: /Users/martin/Projects/turtlestack/plugins/engineering/qa-lead/agents/qa-lead.md
>   ```
> - **Audit table covering ALL 15 criteria from the agent template**. Columns: `# | Criterion | Status (MET / PARTIALLY MET / MISSING) | Evidence (file:line or exact quote)`. No criterion blank or assumed.
> - **Quality score**: `X/15` AND **line count** of the audited agent (both numeric, not approximate).
> - **Model correctness check**: confirm `qa-lead` uses `sonnet` (specialist agent). Flag if `opus` or `haiku` mismatched.
> - **Private-reference check**: scan for company names, private package paths, internal URLs that shouldn't appear in a public marketplace plugin.
> - **Tool-link conventions**: third-party tools mentioned in prose should have markdown hyperlinks on first mention. Flag any missing.
> - **Boundary check**: explicitly state "Boundary respected — plugin-curator is excluded from 'all' audits per the skill's anti-patterns; this audit targets only qa-lead as requested."
> - **Recommended Actions** ordered structural → content → style with severity tag prefix `[STRUCTURAL]`, `[CONTENT]`, `[STYLE]`. Each action is concrete (what to add or change at specific location), not "improve this section".

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Pre-flight Reads

Read: /Users/martin/Projects/turtlestack/CLAUDE.md
Read: /Users/martin/Projects/turtlestack/.claude-plugin/marketplace.json
Read: /Users/martin/Projects/turtlestack/plugins/practices/plugin-curator/templates/agent-template.md
Read: /Users/martin/Projects/turtlestack/plugins/engineering/qa-lead/agents/qa-lead.md

**Boundary respected** — plugin-curator is excluded from "all" audits per the skill's anti-patterns; this audit targets only `qa-lead` as requested.

## Summary

- **File:** `/Users/martin/Projects/turtlestack/plugins/engineering/qa-lead/agents/qa-lead.md`
- **Line count:** 207
- **Quality score:** **13.5 / 15** (12 MET, 3 PARTIAL, 0 MISSING)
- **Model:** `sonnet` ✅ correct for specialist (qa-lead is engineering specialist, not leadership)
- **Private references:** none found — Playwright, Cypress, Gherkin are public/standard
- **Marketplace registration:** confirmed at `marketplace.json:427`

## Criterion Audit

| # | Criterion | Status | Evidence (file:line or quote) |
|---|---|---|---|
| 1 | 150-300 lines | MET | 207 lines (`wc -l`) |
| 2 | Core statement explains ownership in one paragraph | MET | `qa-lead.md:10` — "You define what quality means for each piece of work BEFORE development starts…" |
| 3 | Non-negotiable rules are specific (not vague) | MET | `qa-lead.md:12` — 4 falsifiable rules (criteria before dev, edges before happy path, strategy before code, participant not gate) |
| 4 | Pre-Flight reads project conventions before acting | MET | `qa-lead.md:14-35` — explicit "Read CLAUDE.md and .claude/CLAUDE.md. Check for installed rules in `.claude/rules/`" |
| 5 | Domain methodology has MANDATORY steps (not suggestions) | MET | `qa-lead.md:38-126` — "3 Amigos Pattern", "Acceptance Criteria Protocol" with imperative Rules ("One behaviour per criterion", "Verifiable with a tool", "Include the negative cases") |
| 6 | Structured output format (machine-parseable) | MET | `qa-lead.md:92-115` (Acceptance Test Plan template) and `qa-lead.md:152-172` (Output Format) — two output blocks present |
| 7 | Failure caps | MET | `qa-lead.md:174-178` — three concrete caps with "STOP" verbs |
| 8 | Decision checkpoints (STOP-and-ask) | MET | `qa-lead.md:180-190` — 5-row trigger/why table |
| 9 | Collaboration table | MET | `qa-lead.md:192-200` — 5-row table (Product Owner, Architect, QA Engineer, Developers, CTO) |
| 10 | Principles opinionated and domain-specific | MET | `qa-lead.md:128-134` — "Shift left", "Test behaviour not implementation", "Absence of evidence…", "Edge cases are where bugs live", "Testability is a design requirement" |
| 11 | "What You Don't Do" names who DOES own each excluded thing | PARTIALLY MET | `qa-lead.md:202-207` — bullet 1 names "QA Engineer"; bullets 2-3 (product decisions, architecture decisions) imply but don't name product-owner / architect; bullet 4 ("Skip the 3 amigos") isn't an exclusion of an activity owned by another role |
| 12 | No private/internal references | MET | No hps.gd, no internal URLs, no private package paths. Only public tools (Playwright, Cypress, Gherkin) |
| 13 | External tools linked on first mention | PARTIALLY MET | `qa-lead.md:142` Playwright linked ✅; Cypress NOT linked (same line); `qa-lead.md:59` Gherkin NOT linked on first mention |
| 14 | Correct model (sonnet for specialist) | MET | `qa-lead.md:5` — `model: sonnet`. Correct: qa-lead is an engineering specialist, not in the leadership set (coordinator/cpo/cto/grc-lead) |
| 15 | Frontmatter description precise for auto-invocation | PARTIALLY MET | `qa-lead.md:3` — covers role + what it does, but no explicit "Use when {trigger conditions}" clause; template requires "Use when…" phrasing for reliable auto-loading |

## Structural Observations (beyond the 15)

- **Section ordering departs from template.** Template order: Failure Caps → Decision Checkpoints → Collaboration → Principles → What You Don't Do. Actual order: Principles (128) → Relationship to QA Engineer (136) → Output Format (152) → Failure Caps (174) → Decision Checkpoints (180) → Collaboration (192) → What You Don't Do (202). Not failing on a criterion but inconsistent with template.
- **Duplicate output blocks.** `qa-lead.md:90-115` and `qa-lead.md:152-172` both present output templates with overlapping content (Acceptance Criteria, Test Level Assignment tables appear twice).
- **`Relationship to QA Engineer` (line 136) overlaps with `Collaboration` table (line 192).** The QA Engineer row appears in both.

## Recommended Actions

**[STRUCTURAL] Add explicit "Use when" trigger to frontmatter description.** At `qa-lead.md:3`, append a trigger clause. Suggested rewrite: `"QA Lead — test strategy, acceptance criteria, edge case identification. Use for 3 amigos sessions, writing Gherkin acceptance criteria, defining test strategy, or release-readiness reviews before code is written."` This brings it in line with criterion 15 and template guidance at `agent-template.md:17-21`.

**[STRUCTURAL] Reorder sections to match template.** Move Principles (128-134) and What You Don't Do (202-207) so the order is: Failure Caps → Decision Checkpoints → Collaboration → Principles → What You Don't Do. Sections in the wrong order today: Principles is at 128 (should follow Collaboration), Output Format duplicates content already in the Acceptance Test Plan block.

**[STRUCTURAL] Consolidate the two output template blocks.** Either delete `qa-lead.md:152-172` (Output Format) and keep the richer `qa-lead.md:92-115` (Acceptance Test Plan), or merge them. Currently the agent produces two competing schemas.

**[STRUCTURAL] Merge `Relationship to QA Engineer` (136-148) into the Collaboration table (192-200).** The QA Engineer row in Collaboration can be expanded with the WHAT/HOW split. Removes redundancy.

**[CONTENT] Name owners explicitly in "What You Don't Do" (202-207).** Rewrite as:
- `Make product decisions — challenge criteria, don't rewrite requirements — that's the product-owner`
- `Make architecture decisions — flag testability concerns, don't redesign systems — that's the architect`
Also drop or rephrase the "Skip the 3 amigos" bullet — it isn't an excluded-activity-owned-by-someone-else; move that sentiment into Non-negotiable or Principles.

**[STYLE] Link Gherkin on first mention.** At `qa-lead.md:59`, change `Gherkin format:` to `[Gherkin](https://cucumber.io/docs/gherkin/) format:`.

**[STYLE] Link Cypress on first mention.** At `qa-lead.md:142`, change `Playwright/Cypress` to `[Playwright](https://playwright.dev)/[Cypress](https://www.cypress.io)`.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/17.0 (100%) |
| Evaluated | 2026-05-27 |
| Target model | claude-opus-4-7 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 86157 ms |
| Target cost | $0.5868 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent reads CLAUDE.md and marketplace.json as part of its mandatory pre-flight before beginning the audit | PASS | Pre-flight Reads section lists both 'Read: /Users/martin/Projects/turtlestack/CLAUDE.md' and 'Read: /Users/martin/Projects/turtlestack/.claude-plugin/marketplace.json' before the audit body. |
| c2 | Agent reads the agent template file before evaluating the qa agent definition | PASS | Pre-flight Reads includes 'Read: /Users/martin/Projects/turtlestack/plugins/practices/plugin-curator/templates/agent-template.md' before qa-lead.md is read. |
| c3 | Audit output includes a criteria table covering all 15 quality criteria from the template | PASS | The Criterion Audit table has exactly 15 rows numbered 1–15, each with a distinct criterion. |
| c4 | Each criterion is scored as met, partially met, or missing — not left blank or assumed | PASS | All 15 rows carry an explicit Status: 12 show 'MET', 3 show 'PARTIALLY MET'. No row is blank or marked 'N/A'. |
| c5 | Non-passing criteria include specific evidence (file reference, line number, or exact quote) rather than vague descriptions | PASS | Criterion 11: 'qa-lead.md:202-207 — bullet 1 names QA Engineer; bullets 2-3 imply but don't name'; Criterion 13: 'qa-lead.md:142 Playwright linked; Cypress NOT linked'; Criterion 15: 'qa-lead.md:3 — covers role…' |
| c6 | Audit output includes a quality score (X/15 format) and line count | PASS | Summary states 'Quality score: 13.5 / 15' and 'Line count: 207'. |
| c7 | Audit includes recommended actions prioritised by impact | PASS | Recommended Actions section contains 4 [STRUCTURAL], 1 [CONTENT], and 2 [STYLE] items in that order. |
| c8 | Boundary check — agent does not audit itself (plugin-curator is explicitly excluded from 'all' audits per the skill's anti-patterns) | PARTIAL | Output states verbatim: 'Boundary respected — plugin-curator is excluded from "all" audits per the skill's anti-patterns; this audit targets only qa-lead as requested.' |
| c9 | Output's audit table covers all 15 quality criteria from the agent template — not a subset, not a generic checklist | PASS | Criterion Audit table has exactly 15 numbered rows covering template-specific criteria such as frontmatter description, failure caps, decision checkpoints, and collaboration table. |
| c10 | Output scores each criterion as MET / PARTIALLY MET / MISSING (or equivalent ternary) — never blank, never 'assumed met' | PASS | Every row has either 'MET' or 'PARTIALLY MET'. No row is blank. MISSING score of 0 is reported in summary: '12 MET, 3 PARTIAL, 0 MISSING'. |
| c11 | Output's non-passing criteria each include specific evidence — file reference, line number, or exact quote from the qa agent definition — not vague descriptions like 'frontmatter could be better' | PASS | Criterion 15 partial: 'qa-lead.md:3 — covers role + what it does, but no explicit "Use when {trigger conditions}" clause; template requires "Use when…" phrasing'. |
| c12 | Output reports the quality score as `X/15` and the line count of the audited agent — both numeric, not approximate | PASS | 'Quality score: 13.5 / 15' and 'Line count: 207' — both exact numerics in the Summary block. |
| c13 | Output checks model correctness — qa is a specialist agent that should use `sonnet`, not `opus` — and flags as a finding if mismatched | PASS | Summary: 'Model: sonnet ✅ correct for specialist'. Criterion 14: 'qa-lead.md:5 — model: sonnet. Correct: qa-lead is an engineering specialist, not in the leadership set'. |
| c14 | Output's recommended actions are prioritised — structural gaps (missing required sections) before content gaps (sparse rules) before style issues (line length, banned words) — with severity per action | PASS | Actions ordered [STRUCTURAL] × 4, then [CONTENT] × 1, then [STYLE] × 2, matching the structural → content → style priority hierarchy. |
| c15 | Output reads CLAUDE.md, marketplace.json, and the agent template before evaluating the qa agent — pre-flight is shown explicitly as a step or evidence in the output | PASS | Pre-flight Reads section at the top of the output lists all four files including CLAUDE.md, marketplace.json, and agent-template.md before the audit content begins. |
| c16 | Output checks for private references / company names that shouldn't appear in a public marketplace plugin definition | PASS | Summary: 'Private references: none found — Playwright, Cypress, Gherkin are public/standard'. Criterion 12: 'No hps.gd, no internal URLs, no private package paths.' |
| c17 | Output checks tool-link conventions — third-party tools mentioned in prose have markdown hyperlinks on first mention | PASS | Criterion 13: 'qa-lead.md:142 Playwright linked ✅; Cypress NOT linked (same line); qa-lead.md:59 Gherkin NOT linked on first mention' — all three tools checked with specific line numbers. |
| c18 | Output's recommendations are concrete — each action specifies what to add or change, not 'improve this section' | PARTIAL | Each action names a file:line and gives exact text, e.g. 'At qa-lead.md:3, append a trigger clause. Suggested rewrite: "QA Lead — test strategy…"' and 'change Gherkin format: to [Gherkin](https://cucumber.io/docs/gherkin/) format:'. |

### Notes

The captured output is a near-perfect execution of the requested audit format: all 15 criteria scored with evidence, pre-flight explicitly shown, boundary check present, model check correct, private-reference scan performed, tool-link audit done, and recommendations structured and concrete with severity tags. No gaps were found against any criterion.
