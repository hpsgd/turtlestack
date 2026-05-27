---
# Match the model the agent declares (sonnet) in
# plugins/engineering/ai-engineer/agents/ai-engineer.md. The runner otherwise
# falls back to the harness default (Haiku), which is not what the
# agent is designed to run on.
target-model: claude-sonnet-4-6
---

# Test: RAG pipeline for internal documentation search

Scenario: User wants to build a RAG pipeline so employees can ask natural language questions against the company's internal documentation corpus (~2,000 Confluence pages and ~500 PDF runbooks).

## Prompt

We want to let our support and engineering teams search our internal docs using natural language. We have about 2,000 Confluence pages (mostly Markdown/HTML) and ~500 PDF runbooks, totalling roughly 800MB. Documents are updated a few times a week. Questions are things like "what's the rollback procedure for the payments service?" or "which team owns the authentication microservice?". We need citations so users know where answers came from. Budget is $500/month for AI costs. Can you design this RAG pipeline?

A few specifics for the response:

- Open with an "Evaluation Targets" section UPFRONT (before any implementation): Precision@5, Recall@10, MRR, Faithfulness, P95 latency targets — these define success.
- List 20 concrete example queries (10 procedural like "rollback procedure for payments", 10 ownership like "which team owns auth") with the expected source document for each — this is the retrieval gold set.
- Cover BOTH fallback cases explicitly: model/provider unavailability AND insufficient context.

## Criteria

- [ ] PASS: Agent defines evaluation criteria (retrieval precision/recall targets, faithfulness requirement, latency budget) BEFORE proposing implementation
- [ ] PASS: Agent analyses corpus properties (document types, volume, update frequency) before recommending chunking strategy
- [ ] PASS: Agent recommends evaluating embedding models on a 20-query test set from actual user queries — not choosing by benchmark alone
- [ ] PASS: Agent addresses citation requirements — every generated answer must reference source documents
- [ ] PASS: Agent defines a freshness/rebuild strategy given the weekly update cadence
- [ ] PASS: Agent includes fallback handling for model unavailability and cases where context is insufficient to answer
- [ ] PASS: Agent raises a decision checkpoint before choosing a model (cost/quality trade-off needs stakeholder input given $500/month budget)
- [ ] PARTIAL: Agent separates retrieval evaluation from generation evaluation and specifies testing retrieval first
- [ ] PASS: Output covers all pipeline stages: chunking config, metadata schema, embedding selection, retrieval strategy, prompt template, and evaluation plan

## Output expectations

- [ ] PASS: Output's chunking strategy distinguishes between Markdown/HTML Confluence pages and PDF runbooks, acknowledging that PDFs need OCR or layout-aware extraction before chunking
- [ ] PASS: Output proposes specific chunk size and overlap values (e.g. 512 tokens, 10-20% overlap) with reasoning tied to the corpus content (procedural runbooks vs reference documentation), not generic defaults
- [ ] PASS: Output's retrieval design addresses ownership/team queries (e.g. "which team owns X") via metadata filtering or hybrid retrieval — pure vector similarity will not reliably answer these
- [ ] PASS: Output's monthly cost calculation breaks down embedding cost (one-time + weekly re-embed of changed docs) plus per-query LLM generation cost, with a number that fits within the $500/month ceiling for the projected query volume
- [ ] PASS: Output's prompt template includes a citation instruction (e.g. "cite source document and section after each claim") and the response schema includes a citations array linking to source URLs or runbook IDs
- [ ] PASS: Output specifies an incremental indexing strategy (only re-embed changed Confluence pages or PDFs) rather than full re-indexing weekly, given the 800MB corpus and few-times-weekly update cadence
- [ ] PASS: Output's evaluation plan lists at least 10-20 example queries drawn from the prompt's domain (rollback procedures, service ownership) with expected source documents, not just abstract metrics
- [ ] PARTIAL: Output names specific embedding model candidates (e.g. text-embedding-3-small, voyage-3, BGE) and a specific generation model, with a justification tying each to the cost budget
- [ ] PARTIAL: Output addresses access control — internal docs may have permissions, and a RAG system that returns chunks the asking user shouldn't see is a leak vector
