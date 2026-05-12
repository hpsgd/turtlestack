---
name: create-agent
description: "Create a new agent plugin following the standard template. Handles directory structure, plugin.json, agent definition, marketplace.json, README, and RATSI updates."
argument-hint: "[agent name and brief description of its role]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Create a new agent plugin for $ARGUMENTS.

## Process (sequential — do not skip steps)

### Step 1: Read the templates and conventions

```
Read(file_path="${CLAUDE_PLUGIN_ROOT}/templates/agent-template.md")
Read(file_path="CLAUDE.md")
Read(file_path=".claude-plugin/marketplace.json")
```

The agent template defines the MANDATORY structure. CLAUDE.md defines the directory conventions. marketplace.json is the registry.

### Step 2: Research best practices

Before writing anything, research the established standards and frameworks for this agent's domain:

1. **Identify authoritative sources** — standards bodies, established practitioners, peer-reviewed frameworks (not blog posts)
2. **Document which standards are being adopted** — and why these over alternatives
3. **Plan domain-specific templates** — if the agent produces artefacts, design templates based on the research

The principle: **adopt existing standards, don't invent**. If a well-established framework exists, use it.

### Step 3: Determine category and create structure

Classify the agent:

| Category | Criteria | Examples |
|---|---|---|
| `leadership/` | Coordinates other agents, makes cross-cutting decisions | coordinator, cpo, cto, grc-lead |
| `product/` | Customer-facing, product, design, content, marketing, support | product-owner, ui-designer, gtm, support |
| `engineering/` | Builds, tests, deploys, secures, monitors | architect, developers, qa, devops, security |
| `practices/` | Standards, methodology, cross-cutting rules | coding-standards, writing-style, thinking |

Create the directory structure:

```bash
mkdir -p plugins/{category}/{agent-name}/.claude-plugin
mkdir -p plugins/{category}/{agent-name}/agents
mkdir -p plugins/{category}/{agent-name}/skills
mkdir -p plugins/{category}/{agent-name}/templates  # if agent produces artefacts
```

### Step 4: Write plugin.json

```json
{
  "name": "{agent-name}",
  "description": "{Role} — {domain summary}.",
  "version": "0.1.0",
  "author": {
    "name": "[author or organisation name]"
  },
  "repository": "[repository URL]",
  "license": "Unlicense",
  "keywords": [
    "{keyword1}",
    "{keyword2}"
  ]
}
```

Pretty-printed JSON with 2-space indent. Keywords are lowercase, hyphen-separated.

### Step 5: Write the agent definition

File: `plugins/{category}/{agent-name}/agents/{agent-name}.md`

Follow the agent template EXACTLY. Every section is mandatory:

**Frontmatter:**

```yaml
---
name: {kebab-case — matches directory}
description: "{Role} — {domain summary}. Use when {trigger conditions}."
tools: {minimal set needed}
model: {sonnet for specialists, opus for leadership}
---
```

**Body sections (all mandatory for implementation agents):**

| Section | Purpose | Key requirements |
|---|---|---|
| **Core statement** | What the agent owns | One paragraph, second person ("You own...") |
| **Non-negotiable** | Absolute rules | Specific, falsifiable (not "do good work") |
| **Pre-Flight** | Read before acting | Step 1: CLAUDE.md + .claude/CLAUDE.md + rules. Step 2: understand patterns. Step 3: classify work |
| **Domain methodology** | The expertise | MANDATORY steps, not suggestions. Opinionated decisions |
| **Output format** | What the agent produces | Structured markdown template, all fields defined |
| **Failure caps** | When to stop | 3 consecutive failures → stop. 10 min without progress → stop |
| **Decision checkpoints** | When to ask | Table of triggers where human input is needed |
| **Collaboration** | Who they work with | Table: role, how you work together |
| **Principles** | Domain philosophy | 5–10 opinionated, domain-specific, falsifiable |
| **What You Don't Do** | Boundaries | Each exclusion names who DOES own it |

**Quality targets:**
- 150–300 lines
- Opinionated — "Use X because Y" not "Consider X"
- Domain-specific — not generic advice applicable to any agent
- External tools hyperlinked on first mention

### Step 6: Update marketplace.json

Add the plugin entry to `.claude-plugin/marketplace.json`:

```json
{
  "name": "{agent-name}",
  "source": "{category}/{agent-name}",
  "description": "{one-line description}",
  "version": "0.1.0",
  "category": "{leadership|product|engineering|practices}",
  "tags": ["{tag1}", "{tag2}"]
}
```

### Step 7: Update the coordinator's RATSI matrix

Determine whether the new agent is R (Responsible), A (Accountable), T (Tasked), S (Support), or I (Informed) for each activity. Then choose the right place to record it:

- **Public turtlestack plugins** — read `coordinator:agents/coordinator.md` and add the agent's column to relevant activity rows in the baseline matrix. This is the default path for any agent shipped in turtlestack.
- **Other marketplaces (private or third-party)** — ship a rule file in your plugin's `rules/` directory named `coordinator-ratsi.md`. It installs as `<marketplace>--<plugin>--<version>--coordinator-ratsi.md`, which the coordinator picks up at preflight as an authoritative extension to the baseline matrix. The rule states which baseline sub-section it extends, provides the rows in the same column structure, and includes skill routing for the added activities. See the "Marketplace-contributed extensions" section in the coordinator agent for the full contract.

The dual path keeps the public coordinator file free of private or domain-specific routing while still letting any marketplace contribute to the matrix.

### Step 8: Update the relevant lead's team listing

| Category | Lead to update |
|---|---|
| `engineering/` | CTO agent — add to team listing |
| `product/` | CPO agent — add to team listing |
| `leadership/` | Coordinator agent — add to peer listing |

### Step 9: Update README

Three places to update in `README.md`:

1. **Category install block** — add CLI install command to the relevant category section
2. **Everything install block** — add to the "install everything" command
3. **Agent table** — add row with agent name, description, skills, model

### Step 10: Verify

```bash
# All JSON valid
python3 -c "import json; json.load(open('plugins/{category}/{agent-name}/.claude-plugin/plugin.json'))"
python3 -c "import json; json.load(open('.claude-plugin/marketplace.json'))"

# Plugin count matches
echo "Dirs: $(find plugins -name 'plugin.json' | wc -l)"
echo "Registry: $(python3 -c "import json; print(len(json.load(open('.claude-plugin/marketplace.json'))['plugins']))")"

# No private references
grep -r "hps\.gd\|interstitium\|whns\.gd" --include="*.md" plugins/{category}/{agent-name}/
```

Run the agent audit criteria mentally:

- [ ] 150–300 lines
- [ ] Core statement explains ownership
- [ ] Non-negotiable rules are specific
- [ ] Pre-Flight reads conventions
- [ ] Mandatory methodology steps
- [ ] Structured output format (or N/A if leadership)
- [ ] Failure caps defined
- [ ] Decision checkpoints defined
- [ ] Collaboration table present
- [ ] Principles are opinionated
- [ ] "What You Don't Do" names owners
- [ ] No private references
- [ ] External tools linked
- [ ] Correct model
- [ ] Description precise enough for auto-invocation

## Anti-Patterns (NEVER do these)

- **Creating without researching** — agents must be grounded in established domain practices, not invented methodologies
- **Vague principles** — "Write quality code" applies to every agent and informs no decisions. "One migration per PR — compound migrations are a deployment risk" is specific and useful
- **Missing the registry chain** — creating the agent without updating marketplace.json, README, RATSI, and lead listing leaves it disconnected
- **Suggestions instead of decisions** — "You might consider using blue/green deployments" is weak. "Default to feature flags for user-facing changes" is a decision
- **Generic descriptions** — "Helps with code" triggers on everything. "React developer — component implementation, hooks, state management. Use when building React frontend features" triggers precisely
- **Forgetting model assignment** — leadership agents use opus (they make cross-cutting decisions). Specialists use sonnet (they execute within their domain)

## Output Format

After creation, report:

```markdown
## Created: {agent-name}

### Files Created
- `plugins/{category}/{agent-name}/.claude-plugin/plugin.json`
- `plugins/{category}/{agent-name}/agents/{agent-name}.md`
- `plugins/{category}/{agent-name}/skills/` (empty, ready for skills)
- `plugins/{category}/{agent-name}/templates/` (if applicable)

### Registry Updates
- marketplace.json: ✅ added
- README: ✅ install commands + agent table
- Coordinator RATSI: ✅ {activities added to}
- Lead ({cto/cpo}): ✅ team listing updated

### Quality Score
- **Lines:** {count}
- **Agent audit score:** {X}/15
- **Model:** {model}

### Verification
- JSON valid: ✅
- Plugin count matches: ✅
- No private refs: ✅
```
