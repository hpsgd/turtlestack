# Bootstrap

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/ai/_sections/ai-engineer.md` fragment containing a user-authored section. The ai-engineer bootstrap skill should preserve that user content while appending the template's missing sections (with a merge marker), and should create the two files the fixture is missing — `prompt-library.md` and `eval-suite-template.md`. The ai-engineer never writes `docs/ai/CLAUDE.md` directly — the coordinator assembles it from the fragments in `_sections/`. The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

> The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/ai/_sections/ai-engineer.md` fragment is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.
> 
> Read the ai-engineer bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/engineering/ai-engineer/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.
> 
> After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## AI Engineer Bootstrap Complete

### Files created
- `docs/ai/_sections/ai-engineer.md` — ai-engineer fragment (coordinator assembles `docs/ai/CLAUDE.md` from it)
- `docs/ai/prompt-library.md` — prompt catalogue template
- `docs/ai/eval-suite-template.md` — model evaluation suite template

### Files merged
- `docs/ai/_sections/ai-engineer.md` — appended bootstrap sections (v0.1.0) while preserving user's "Custom team notes" section with `USER-EDIT-SENTINEL-DO-NOT-STRIP` sentinel

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

#### `work/docs/ai/_sections/ai-engineer.md`

```
<!-- ai-engineer fragment of the ai domain doc. Assembled into docs/ai/CLAUDE.md by the coordinator. -->

## Custom team notes

USER-EDIT-SENTINEL-DO-NOT-STRIP

This section was written by the team and must survive any bootstrap re-run.
It exists to test the safe-merge contract: the bootstrap skill must not
overwrite or remove user-authored content.

<!-- Merged from ai-engineer bootstrap v0.1.0 -->

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

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 11.5/11.5 (100%) |
| Evaluated | 2026-06-15 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 47800 ms |
| Target cost | $0.0954 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | After bootstrap, `docs/ai/_sections/ai-engineer.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim | PASS | Artifact shows '## Custom team notes\n\nUSER-EDIT-SENTINEL-DO-NOT-STRIP\n\nThis section was written by the team...' intact at top of merged file. |
| c2 | After bootstrap, `docs/ai/_sections/ai-engineer.md` contains the safe-merge marker `<!-- Merged from ai-engineer bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged | PASS | Artifact contains exactly '<!-- Merged from ai-engineer bootstrap v0.1.0 -->' between the preserved user section and the appended template content. |
| c3 | After bootstrap, `docs/ai/_sections/ai-engineer.md` contains the appended template sections — at minimum the "Prompt Engineering Conventions" and "Model Evaluation" headings now appear alongside the preserved user content | PASS | Artifact contains '## Prompt Engineering Conventions' and '## Model Evaluation' headings below the merge marker, alongside the preserved user content. |
| c4 | The ai-engineer fragment is authored at H2 and below — it does not introduce a `# AI Domain` H1 (the coordinator generates that when it assembles `docs/ai/CLAUDE.md`) | PASS | All headings in the artifact are H2 (`##`). No H1 (`#`) heading is present anywhere in `work/docs/ai/_sections/ai-engineer.md`. |
| c5 | The skill does NOT write `docs/ai/CLAUDE.md` directly — that file is the coordinator's to assemble from `_sections/` | PASS | Only three artifacts listed: `prompt-library.md`, `eval-suite-template.md`, and `_sections/ai-engineer.md`. No `docs/ai/CLAUDE.md` artifact exists. |
| c6 | After bootstrap, `docs/ai/prompt-library.md` exists and contains a `## Prompt Registry` heading | PASS | Artifact `work/docs/ai/prompt-library.md` exists and contains '## Prompt Registry' with a table beneath it. |
| c7 | After bootstrap, `docs/ai/eval-suite-template.md` exists and contains a `## Metrics` heading | PASS | Artifact `work/docs/ai/eval-suite-template.md` exists and contains '## Metrics' with a metrics table beneath it. |
| c8 | The created `eval-suite-template.md` contains an AI-specific metrics row referencing RAGAS (e.g. `Faithfulness (RAGAS)`) or `## Failure Analysis` | PASS | Artifact contains both '\| Faithfulness (RAGAS) \| >= 0.8 \|' and '\| Relevancy (RAGAS) \| >= 0.8 \|' rows, plus a '## Failure Analysis' section. |
| c9 | Chat output includes a manifest summary that distinguishes files created (`prompt-library.md`, `eval-suite-template.md`) from files merged (`_sections/ai-engineer.md`) | PASS | Chat output has separate '### Files created' and '### Files merged' sections; merged section explicitly calls out `_sections/ai-engineer.md` with sentinel preservation noted. |
| c10 | Output names each created and merged file individually — a bare "bootstrap complete" without the per-file manifest is not enough | PASS | Each file is listed individually: `docs/ai/_sections/ai-engineer.md`, `docs/ai/prompt-library.md`, `docs/ai/eval-suite-template.md` with per-file descriptions. |
| c11 | Output does not claim it overwrote or replaced `docs/ai/_sections/ai-engineer.md` — the language reflects merge, not replacement | PASS | Chat output says 'appended bootstrap sections (v0.1.0) while preserving user's "Custom team notes" section' — no overwrite/replace language used. |
| c12 | Output points the reader at next steps (using `/ai-engineer:model-evaluation` or `/ai-engineer:rag-pipeline`) consistent with the skill's documented manifest | PARTIAL | Chat output '### Next steps' lists both 'Create eval suites for each prompt using `/ai-engineer:model-evaluation`' and 'Design RAG pipelines using `/ai-engineer:rag-pipeline`'. |

### Notes

All criteria met cleanly. The minor anomaly of `ai-engineer.md` appearing in both 'Files created' and 'Files merged' sections is slightly redundant but does not obscure the required distinction, and c9 scores PASS since the merge/created separation is unambiguous.
