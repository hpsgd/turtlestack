---
name: audit-skill
description: "Audit a skill definition against the standard template. Reports structural gaps and recommended fixes."
argument-hint: "[skill name, parent agent, or 'all' to audit every skill]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Audit $ARGUMENTS against the skill template quality criteria.

## Process (sequential — do not skip steps)

### Step 1: Read the template

```
Read(file_path="${CLAUDE_PLUGIN_ROOT}/templates/skill-template.md")
```

The template defines the MANDATORY structure. The quality criteria at the bottom of the template are the audit checklist.

### Step 2: Find the skill(s) to audit

If `$ARGUMENTS` is "all", find every skill:
```bash
find plugins -name 'SKILL.md' | sort
```

Otherwise, locate the specific skill by name or agent.

### Step 3: Evaluate each quality criterion

For EACH skill, check all applicable criteria — 12 that apply to every skill, plus criterion 13 which applies only to `bootstrap` skills (N/A otherwise). Score as ✅ (met), ⚠️ (partially met — explain why), ❌ (missing), or N/A (not applicable).

**Criterion 1: Line count (100–500 lines)**

Count lines. Under 100 indicates a stub or skeleton. Over 500 indicates the skill is trying to be an agent and should be split.

| Lines | Score |
|---|---|
| 100–500 | ✅ |
| 50–99 | ⚠️ Short — lacks depth |
| < 50 | ❌ Stub — needs full rewrite |
| > 500 | ⚠️ Long — consider splitting |

**Criterion 2: Description specific enough for auto-invocation**

Read the `description` field in frontmatter. Claude uses this to decide whether to load the skill. Must include: (1) what it produces, (2) when to use it.

| Quality | Score |
|---|---|
| Specific task + trigger conditions | ✅ |
| Vague ("helps with X") | ❌ |

**Criterion 3: Self-contained**

The skill must work without reading the parent agent first. Check:
- Does it define its own methodology, or does it say "follow the process in the agent"?
- Does it include enough context to execute independently?
- A reader encountering this skill for the first time should understand what to do

**Criterion 4: Sequential mandatory steps**

Steps must be numbered, sequential, and blocking (cannot skip). Check:
- Are steps numbered with clear progression?
- Are steps framed as mandatory ("do this") not optional ("consider this")?
- Would skipping a step break the process?

**Criterion 5: Verifiable step outputs**

Each step should produce something verifiable — a table, a score, a file, a decision. Check:
- After completing each step, is there a concrete output?
- Can someone else verify the step was completed correctly?

**Criterion 6: Rules with anti-patterns**

Must have a rules or anti-patterns section with specific imperatives. Check:
- "Always X" / "Never Y" style rules (not suggestions)
- Anti-patterns explain what NOT to do and why
- Rules are domain-specific (not generic "write good code")

**Criterion 7: Structured output format**

Must include a template showing the exact output structure. Check:
- Markdown template with all fields defined
- Fields are specific (not "present your findings")
- Template is copy-pasteable as a starting point

**Criterion 8: Cross-references related skills**

Where a genuine workflow relationship exists, the skill references related skills. Check:
- Does the skill reference skills whose output feeds INTO this skill, or skills that consume THIS skill's output? (e.g., "define the schema first, then generate tests" is a real dependency)
- Sharing a parent plugin is NOT sufficient reason for cross-references. Two skills in the same plugin that serve independent purposes do not need to reference each other
- N/A if the skill has no workflow dependencies on other skills

**Criterion 9: Generic examples only**

No private company names, internal packages, or project-specific details. Check:
- Examples use generic names (Acme Corp, @org/ui, myservice)
- No internal URLs, private repo references, or proprietary tools

**Criterion 10: External tools linked**

External tools mentioned in prose should have markdown hyperlinks on first mention. Check:
- Tool names like k6, Locust, Lighthouse have `[tool](url)` links
- N/A if the skill doesn't mention specific external tools

**Criterion 11: Argument hint**

The `argument-hint` frontmatter field tells the user what to provide. Check:
- Present and wrapped in `[brackets]`
- Specific enough to guide the user

**Criterion 12: Frontmatter description precision**

The frontmatter `description` is the primary matching signal. Check:
- Would Claude match this description to the right user intent?
- Is it distinguishable from sibling skills?

**Criterion 13: Bootstrap phase declared (bootstrap skills only)**

Only applies when the skill is named `bootstrap` (i.e. `skills/bootstrap/SKILL.md`). For every other skill, mark this criterion N/A and skip it. A bootstrap skill must declare `bootstrap-phase` in its frontmatter — `/coordinator:bootstrap-project` reads it to sequence the project bootstrap, and a missing value forces it into a default slot with a warning. Check:
- Is `bootstrap-phase` present in the frontmatter?
- Is the value one of: `foundations`, `delivery`, `engineering`, `stack`, `product`, `content`, `market`, `governance`?

| State | Score |
|---|---|
| Present and a recognised phase | ✅ |
| Present but unrecognised value | ⚠️ Runs in the default slot — confirm the phase is intended |
| Missing | ❌ Add `bootstrap-phase` so the coordinator can order it |

**Criterion 14: Writes a domain fragment, never the domain `CLAUDE.md` (bootstrap skills only)**

Only applies to `bootstrap` skills; N/A otherwise. A bootstrap skill must never write a domain `CLAUDE.md` directly — the coordinator assembles every one from fragments. The skill writes its contribution as a fragment at `docs/<domain>/_sections/<plugin>.md` (H2 and below, no H1), whether the domain has one contributing plugin or several. A sole owner is not an exception: a single-plugin domain is just a domain with one fragment. Check the skill's file-write instructions:
- Does it create or append any `docs/<domain>/CLAUDE.md`? That is the defect — even for a domain no other plugin touches.
- Does it correctly write a fragment under `_sections/` and refer to the domain `CLAUDE.md` only as the coordinator-assembled output?

Writing the project-root `SECURITY.md` or `CHANGELOG.md` is fine — those are not domain docs. A `See docs/<domain>/CLAUDE.md` pointer is fine — that references the assembled file, it doesn't write it.

| State | Score |
|---|---|
| Writes a `_sections/<plugin>.md` fragment; refers to the domain `CLAUDE.md` only as coordinator-assembled | ✅ |
| Creates or appends any domain `docs/<domain>/CLAUDE.md` directly (even as sole owner) | ❌ Convert to a `_sections/<plugin>.md` fragment |

### Step 4: Classify findings

For each skill, classify the overall state:

| State | Criteria | Action needed |
|---|---|---|
| **Complete** | 10+ criteria passing, no ❌ | None — minor tweaks at most |
| **Needs expansion** | 6–9 criteria passing, structure exists | Expand missing sections |
| **Stub** | < 6 criteria passing or < 50 lines | Full rewrite needed |

### Step 5: Produce the report

**Single skill audit** — full detail for the one skill.

**"All" audit** — summary table first, then detail for non-passing skills only.

## Anti-Patterns (NEVER do these)

- **Passing stubs** — a 9-line skill with correct frontmatter is still ❌ on most criteria. Frontmatter alone is not a skill
- **Vague findings** — "needs improvement" is not a finding. "Missing structured output format — skill ends with prose description instead of a markdown template" is a finding
- **Ignoring edge cases** — thinking skills and plugin-curator skills have different structures than domain skills. Adapt criteria (e.g., thinking skills may not need argument-hint or anti-patterns in the same way)
- **Counting comments as content** — HTML comments and template instructions don't count toward line count
- **Scoring without reading** — every criterion requires evidence from the actual file content. Don't score based on the skill name or assumptions
- **Penalising redirect headings** — if a section heading exists but redirects to another section (e.g., "## Anti-Patterns" with "See Rules below"), score as ✅. The heading is present and visible; the content is covered elsewhere in the document

## Output Format

### Single skill

```markdown
## Skill Audit: {skill-name} ({parent-agent})

### Summary
- **Lines:** {count} (target: 100–500)
- **Quality score:** {X}/12 criteria met
- **State:** Complete / Needs expansion / Stub

### Criteria

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Line count (100–500) | ✅/⚠️/❌ | {count} lines |
| 2 | Description for auto-invocation | ✅/⚠️/❌ | {quote or issue} |
| 3 | Self-contained | ✅/⚠️/❌ | {evidence} |
| 4 | Sequential mandatory steps | ✅/⚠️/❌ | {step count, structure} |
| 5 | Verifiable step outputs | ✅/⚠️/❌ | {evidence} |
| 6 | Rules with anti-patterns | ✅/⚠️/❌ | {evidence} |
| 7 | Structured output format | ✅/⚠️/❌ | {evidence} |
| 8 | Cross-references | ✅/⚠️/❌/N/A | {evidence} |
| 9 | Generic examples | ✅/⚠️/❌ | {evidence} |
| 10 | Tool links | ✅/⚠️/❌/N/A | {evidence} |
| 11 | Argument hint | ✅/⚠️/❌ | {value or missing} |
| 12 | Description precision | ✅/⚠️/❌ | {evidence} |

### Recommended Actions
1. {highest priority fix with specific guidance}
2. {second priority}
```

### All skills

```markdown
## Skill Audit: All Skills

### Summary
- **Total skills:** {count}
- **Complete (10+/12):** {count}
- **Needs expansion (6–9/12):** {count}
- **Stubs (<6/12 or <50 lines):** {count}

### Results

| Agent | Skill | Lines | Score | State | Top issue |
|---|---|---|---|---|---|
| {parent} | {name} | {N} | {X}/12 | Complete/Expand/Stub | {primary gap} |

Sort by agent name, then skill name within each agent.

### Stubs (need full rewrite)
| Agent | Skill | Lines |
|---|---|---|
| {parent} | {name} | {N} |

### Needs Expansion (prioritised)
| Agent | Skill | Lines | Score | Missing criteria |
|---|---|---|---|---|
| {parent} | {name} | {N} | {X}/12 | {list of ❌ criteria} |
```
