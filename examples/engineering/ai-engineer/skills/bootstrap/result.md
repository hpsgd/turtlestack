# Bootstrap

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/ai/CLAUDE.md` containing a user-authored section. The ai-engineer bootstrap skill should preserve that user content while appending the template's missing sections (with a merge marker), and should create the two files the fixture is missing — `prompt-library.md` and `eval-suite-template.md`. The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

> The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/ai/CLAUDE.md` is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.
> 
> Read the ai-engineer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/engineering/ai-engineer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.
> 
> After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## AI Engineer Bootstrap Complete

### Files created
- `docs/ai/prompt-library.md` — prompt catalogue template
- `docs/ai/eval-suite-template.md` — model evaluation suite template

### Files merged
- `docs/ai/CLAUDE.md` — domain conventions and skill reference (user-authored "Custom team notes" section preserved; missing sections appended with merge marker)

### Next steps
- Register production prompts in `prompt-library.md`
- Create eval suites for each prompt using `/ai-engineer:model-evaluation`
- Design RAG pipelines using `/ai-engineer:rag-pipeline`
- Review AI safety checklist for user-facing features

### Artifacts written

#### `work/docs/ai/prompt-library.md`

```
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

```

#### `work/docs/ai/eval-suite-template.md`

```
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

#### `work/docs/ai/CLAUDE.md`

```
# AI Domain

This directory contains AI/ML documentation for the project.

## Custom team notes

USER-EDIT-SENTINEL-DO-NOT-STRIP

This section was written by the team and must survive any bootstrap re-run.
It exists to test the safe-merge contract: the bootstrap skill must not
overwrite or remove user-authored content.

<!-- Merged from ai-engineer bootstrap v0.1.0 -->

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

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 9.5/9.5 (100%) |
| Evaluated | 2026-05-13 |
| Target duration | 38797 ms |
| Target cost | $0.1079 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | After bootstrap, `docs/ai/CLAUDE.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim | PASS | CLAUDE.md artifact contains `USER-EDIT-SENTINEL-DO-NOT-STRIP` within the preserved '## Custom team notes' section. |
| c2 | After bootstrap, `docs/ai/CLAUDE.md` contains the safe-merge marker `<!-- Merged from ai-engineer bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged | PASS | CLAUDE.md artifact contains `<!-- Merged from ai-engineer bootstrap v0.1.0 -->` immediately after the user-authored section. |
| c3 | After bootstrap, `docs/ai/CLAUDE.md` contains the appended template sections — at minimum the "Prompt Engineering Conventions" and "Model Evaluation" headings now appear alongside the preserved user content | PASS | CLAUDE.md contains `## Prompt Engineering Conventions` and `## Model Evaluation` headings following the merge marker and user content. |
| c4 | After bootstrap, `docs/ai/prompt-library.md` exists and contains a `## Prompt Registry` heading | PASS | `work/docs/ai/prompt-library.md` artifact exists and contains `## Prompt Registry` heading with a table. |
| c5 | After bootstrap, `docs/ai/eval-suite-template.md` exists and contains a `## Metrics` heading | PASS | `work/docs/ai/eval-suite-template.md` artifact exists and contains `## Metrics` heading with a metrics table. |
| c6 | The created `eval-suite-template.md` contains an AI-specific metrics row referencing RAGAS (e.g. `Faithfulness (RAGAS)`) or `## Failure Analysis` | PASS | eval-suite-template.md contains both `Faithfulness (RAGAS)` and `Relevancy (RAGAS)` rows in the Metrics table, plus `## Failure Analysis` section. |
| c7 | Chat output includes a manifest summary that distinguishes files created (`prompt-library.md`, `eval-suite-template.md`) from files merged (`CLAUDE.md`) | PASS | Chat output has distinct `### Files created` and `### Files merged` sections listing the respective files. |
| c8 | Output names each created and merged file individually — a bare "bootstrap complete" without the per-file manifest is not enough | PASS | Each file is named individually: `docs/ai/prompt-library.md`, `docs/ai/eval-suite-template.md`, `docs/ai/CLAUDE.md` with per-file descriptions. |
| c9 | Output does not claim it overwrote or replaced `docs/ai/CLAUDE.md` — the language reflects merge, not replacement | PASS | Output says CLAUDE.md was 'merged' with 'user-authored section preserved; missing sections appended with merge marker' — no overwrite/replace language. |
| c10 | Output points the reader at next steps (using `/ai-engineer:model-evaluation` or `/ai-engineer:rag-pipeline`) consistent with the skill's documented manifest | PARTIAL | Next steps explicitly mention `/ai-engineer:model-evaluation` and `/ai-engineer:rag-pipeline` as recommended follow-on skills. |

### Notes

The skill executed flawlessly: sentinel preserved, merge marker present, template sections appended, both missing files created with correct content including RAGAS metrics, and the manifest summary clearly distinguished created vs merged files. All criteria met at ceiling.
