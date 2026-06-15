---
name: bootstrap
bootstrap-phase: stack
description: "Bootstrap the AI/ML documentation structure for a project. Creates docs/ai/, generates initial templates, and writes the ai-engineer fragment of the ai domain doc (the coordinator assembles docs/ai/CLAUDE.md). Idempotent — merges missing sections into existing files without overwriting."
argument-hint: "[project name]"
user-invocable: false
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Bootstrap AI Documentation

Bootstrap the AI/ML documentation structure for **$ARGUMENTS**.

## Process

### Step 1: Check and create domain directory

```bash
mkdir -p docs/ai docs/ai/_sections
```

### Step 2: Create or merge files

For each file below, apply the safe merge pattern:
- If file does not exist -> create from template
- If file exists -> read both, find sections in template missing from file, append missing sections with `<!-- Merged from ai-engineer bootstrap v0.1.0 -->`

#### Fragment: `docs/ai/_sections/ai-engineer.md`

`docs/ai/CLAUDE.md` is **assembled by the coordinator** from the fragments in `_sections/` — no plugin writes
it directly. Write the ai-engineer's contribution as this fragment. It starts at H2 (the coordinator generates
the `# AI Domain` H1 and a one-line intro — the `domain-title` hint below gives it the acronym). Create it
with this content:

```markdown
<!-- domain-title: AI -->
## What This Domain Covers

- **Prompt engineering** — design patterns, versioning, and testing
- **Model evaluation** — benchmarks, metrics, and regression testing
- **RAG pipelines** — retrieval-augmented generation architecture
- **AI safety** — guardrails, content filtering, and risk mitigation
- **Cost management** — token budgets, model selection, and caching
- **Experiment tracking** — reproducible AI experiments

## Prompt Engineering Conventions

Follow the [Anthropic prompt engineering guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) as the baseline.

### Prompt structure

1. **System prompt** — role, constraints, output format
2. **Context** — relevant documents, data, or prior conversation
3. **Task** — specific instruction with clear success criteria
4. **Examples** — few-shot examples for complex tasks

### Prompt versioning

- Store prompts in `prompts/` directory, not inline in code
- Version prompts with semantic versioning (same as code)
- Every prompt change requires an eval run before deployment
- Track prompt → model → output triples for reproducibility

### Prompt testing

- Unit test: does the prompt parse correctly and include required sections?
- Eval test: does the output meet quality thresholds on the eval suite?
- Regression test: does the new prompt maintain quality on previous test cases?

## Model Evaluation

### RAG evaluation (RAGAS)

Use [RAGAS](https://docs.ragas.io/) metrics for RAG pipeline quality:

| Metric | Measures | Target |
|--------|----------|--------|
| Faithfulness | Are answers grounded in retrieved context? | > 0.8 |
| Answer relevancy | Does the answer address the question? | > 0.8 |
| Context precision | Is retrieved context relevant? | > 0.7 |
| Context recall | Is all needed context retrieved? | > 0.7 |

### General evaluation (HELM)

Use [HELM](https://crfm.stanford.edu/helm/) framework principles for general model evaluation:
- Accuracy, calibration, robustness, fairness, efficiency
- Evaluate on domain-specific test sets, not just public benchmarks

### Eval suite conventions

- Store eval datasets in `evals/` directory
- Minimum 50 test cases per eval suite
- Run evals in CI on prompt or model changes
- Track eval scores over time for regression detection

## AI Safety (OWASP LLM Top 10)

Address the [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/):

| Risk | Mitigation |
|------|------------|
| Prompt injection | Input validation, system prompt hardening |
| Insecure output handling | Output sanitisation, type checking |
| Training data poisoning | Data provenance tracking |
| Denial of service | Token limits, rate limiting, timeouts |
| Supply chain vulnerabilities | Model provenance, dependency audit |
| Sensitive information disclosure | PII filtering, output guardrails |
| Insecure plugin design | Least-privilege tool access |
| Excessive agency | Human-in-the-loop for high-risk actions |
| Overreliance | Confidence scoring, citation requirements |
| Model theft | Access controls, API key rotation |

## Cost Management

- Set per-request token budgets (input + output)
- Use cheaper models for simple tasks, capable models for complex tasks
- Cache identical or near-identical requests
- Monitor daily/weekly spend and alert on anomalies
- Log token usage per feature for cost attribution

## Tooling

| Tool | Purpose |
|------|---------|
| [OpenRouter](https://openrouter.ai) | Model access and routing |
| [GitHub Actions](https://docs.github.com/en/actions) | Eval suite in CI on prompt/model changes |
| [Perplexity](https://perplexity.ai) | AI research and literature review |

## Available Skills

| Skill | Purpose |
|-------|---------|
| `/ai-engineer:prompt-design` | Design and optimise prompts |
| `/ai-engineer:model-evaluation` | Create model evaluation suites |
| `/ai-engineer:rag-pipeline` | Design RAG pipeline architecture |

## Conventions

- Every prompt is version-controlled and eval-tested before deployment
- Model changes require eval regression testing
- AI safety review for any user-facing LLM feature
- Cost budgets are set per feature and monitored weekly
- RAG pipelines are evaluated with RAGAS metrics before release
- Experiment results are logged for reproducibility
```

#### File 2: `docs/ai/prompt-library.md`

Create with this content:

````markdown
# Prompt Library

> Central catalogue of production prompts. Each prompt is version-controlled and eval-tested.

## Prompt Registry

| Prompt ID | Version | Model | Purpose | Eval Score | Owner |
|-----------|---------|-------|---------|------------|-------|
| | | | | | |

## Prompt Template

### `{prompt_id}` — v{version}

**Model:** {model name and version}
**Temperature:** {0.0–1.0}
**Max tokens:** {limit}

#### System Prompt

```
[System prompt content here]
```

#### User Prompt Template

```
[User prompt with {variables} marked]
```

#### Variables

| Variable | Type | Description | Required |
|----------|------|-------------|----------|
| | | | |

#### Examples

**Input:**
```
[Example input]
```

**Expected output:**
```
[Example output]
```

#### Eval Results

| Eval Suite | Score | Date | Notes |
|------------|-------|------|-------|
| | | | |

> Add new prompts here before implementing in code. Every prompt must have at least one eval run.
````

#### File 3: `docs/ai/eval-suite-template.md`

Create with this content:

```markdown
# Eval Suite — [Feature/Prompt Name]

> Template for creating model evaluation suites. Copy for each new eval.

## Metadata

| Field | Value |
|-------|-------|
| Prompt ID | |
| Model | |
| Created | YYYY-MM-DD |
| Last run | YYYY-MM-DD |
| Owner | |

## Test Cases

| # | Input | Expected Output | Criteria | Pass/Fail |
|---|-------|----------------|----------|-----------|
| 1 | | | | |
| 2 | | | | |

## Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Accuracy | >= % | % | |
| Faithfulness (RAGAS) | >= 0.8 | | |
| Relevancy (RAGAS) | >= 0.8 | | |
| Latency (p95) | <= ms | ms | |
| Cost per request | <= $ | $ | |

## Failure Analysis

| Test # | Failure Mode | Root Cause | Action |
|--------|-------------|------------|--------|
| | | | |

## History

| Date | Version | Score | Model | Notes |
|------|---------|-------|-------|-------|
| | | | | |

> Minimum 50 test cases per eval suite. Run evals in CI on every prompt change.
```

### Step 3: Return manifest

After creating/merging all files, output a summary:

```
## AI Engineer Bootstrap Complete

### Files created
- `docs/ai/_sections/ai-engineer.md` — ai-engineer fragment (coordinator assembles `docs/ai/CLAUDE.md` from it)
- `docs/ai/prompt-library.md` — prompt catalogue template
- `docs/ai/eval-suite-template.md` — model evaluation suite template

### Files merged
- (list any existing files where sections were appended)

### Next steps
- Register production prompts in `prompt-library.md`
- Create eval suites for each prompt using `/ai-engineer:model-evaluation`
- Design RAG pipelines using `/ai-engineer:rag-pipeline`
- Review AI safety checklist for user-facing features
```
