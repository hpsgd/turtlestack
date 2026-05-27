# Rag Design

Scenario: User wants to build a RAG pipeline so employees can ask natural language questions against the company's internal documentation corpus (~2,000 Confluence pages and ~500 PDF runbooks).

## Prompt

> We want to let our support and engineering teams search our internal docs using natural language. We have about 2,000 Confluence pages (mostly Markdown/HTML) and ~500 PDF runbooks, totalling roughly 800MB. Documents are updated a few times a week. Questions are things like "what's the rollback procedure for the payments service?" or "which team owns the authentication microservice?". We need citations so users know where answers came from. Budget is $500/month for AI costs. Can you design this RAG pipeline?
> 
> A few specifics for the response:
> 
> - Open with an "Evaluation Targets" section UPFRONT (before any implementation): Precision@5, Recall@10, MRR, Faithfulness, P95 latency targets — these define success.
> - List 20 concrete example queries (10 procedural like "rollback procedure for payments", 10 ownership like "which team owns auth") with the expected source document for each — this is the retrieval gold set.
> - Cover BOTH fallback cases explicitly: model/provider unavailability AND insufficient context.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

# RAG Pipeline Design: Internal Documentation Search

---

## Evaluation Targets

These are the success criteria. Do not declare the pipeline production-ready until all targets are met on the gold set below.

| Metric | Target | Rationale |
|---|---|---|
| **Precision@5** | ≥ 0.80 | 4 of 5 retrieved chunks must be relevant; any lower and generation gets polluted context |
| **Recall@10** | ≥ 0.75 | 75% of all relevant docs for a query must appear in the top 10; lower means answers are incomplete |
| **MRR** | ≥ 0.82 | The single best result must land near position 1; ownership queries in particular fail badly if the right doc is buried |
| **Faithfulness** | ≥ 0.97 | Near-zero hallucination tolerance — a wrong rollback procedure has operational consequences |
| **P95 latency** | ≤ 3 000 ms | Measured end-to-end from query receipt to streamed first token; retrieval ≤ 400 ms, generation ≤ 2 600 ms |

Measure retrieval metrics first. Do not touch prompt engineering until retrieval meets its targets.

---

## Retrieval Gold Set — 20 Queries

These are the ground-truth query/document pairs that drive embedding evaluation, retrieval tuning, and regression testing. All 20 must be curated from real documents before the first embed run.

### Procedural (10)

| # | Query | Expected Source Document |
|---|---|---|
| P1 | What is the rollback procedure for the payments service? | `runbooks/payments-service-runbook.pdf` |
| P2 | How do I restart the authentication service after a crash? | `runbooks/auth-service-ops.pdf` |
| P3 | What are the steps to deploy a hotfix to production? | `confluence/eng/hotfix-deployment-guide.md` |
| P4 | How do I rotate database credentials for the user service? | `runbooks/user-service-secrets-rotation.pdf` |
| P5 | What is the incident response procedure for a P1 outage? | `confluence/ops/incident-response-playbook.md` |
| P6 | How do I scale up the order processing workers? | `runbooks/order-processing-scaling.pdf` |
| P7 | What are the steps to restore the search index after corruption? | `runbooks/search-index-recovery.pdf` |
| P8 | How do I enable or disable a feature flag in the mobile app? | `confluence/mobile/feature-flag-management.md` |
| P9 | What is the process for requesting elevated database access? | `confluence/sec/db-access-review-process.md` |
| P10 | How do I run a canary deployment for the recommendation engine? | `confluence/eng/canary-deployment-guide.md` |

### Ownership (10)

| # | Query | Expected Source Document |
|---|---|---|
| O1 | Which team owns the authentication microservice? | `confluence/ops/service-ownership-registry.md` |
| O2 | Who is the on-call contact for the payments platform? | `confluence/ops/oncall-roster.md` |
| O3 | Which squad is responsible for the data pipeline? | `confluence/eng/team-topology-map.md` |
| O4 | Who owns the mobile push notification service? | `confluence/ops/service-ownership-registry.md` |
| O5 | Which team maintains the API gateway? | `confluence/eng/api-gateway-ownership.md` |
| O6 | Who is the escalation contact for billing disputes? | `confluence/ops/escalation-paths.md` |
| O7 | Which engineering team owns the search service? | `confluence/ops/service-ownership-registry.md` |
| O8 | Who should I contact about GDPR data deletion requests? | `confluence/legal/data-privacy-procedures.md` |
| O9 | Which team is responsible for the CI/CD pipeline? | `confluence/eng/devops-team-responsibilities.md` |
| O10 | Who owns the customer identity platform? | `confluence/ops/service-ownership-registry.md` |

**Note on O1/O4/O7/O10:** All four map to `service-ownership-registry.md`. This is intentional — it stress-tests whether the registry is chunked such that each service section is independently retrievable, not buried in a monolithic chunk that matches nothing.

---

## Corpus Profile

| Property | Value |
|---|---|
| Document types | Confluence pages (HTML/Markdown), PDF runbooks |
| Volume | ~2,500 documents, ~800 MB |
| Estimated token count | ~50–80M tokens (text only, after stripping HTML/PDF scaffolding) |
| Update frequency | A few times per week — incremental indexing required |
| Language | English |
| Structure | Confluence: headings, tables, code blocks. PDFs: numbered steps, tables, section headers |
| Content quality | Confluence: clean structured HTML. PDFs: variable — check for scanned pages requiring OCR |

---

## Chunking Configuration

Different content types need different strategies. Apply them in a single ingestion pipeline with a content-type router.

### Confluence Pages

- **Strategy:** Semantic — split on H2/H3 headings first, then paragraph boundaries
- **Chunk size:** 512 tokens target, max 768 tokens hard cap
- **Overlap:** 64 tokens (one paragraph) at section boundaries only — not within a section
- **Atomic units:** Never split mid-table or mid-code-block; treat each as a single chunk even if it exceeds the soft cap
- **Special case for `service-ownership-registry.md`:** Each service entry is its own chunk. If the registry is one large table, split row-by-row and embed each row as `"[service-name]: owned by [team], on-call: [contact]"` to maximise ownership query recall

### PDF Runbooks

- **Strategy:** Paragraph-based with fallback to fixed-size
- **Chunk size:** 512 tokens, 20% overlap (PDFs lose heading structure after extraction; overlap compensates)
- **Preprocessing:** Strip headers/footers (page numbers, company name repeated on every page). Detect and handle multi-column layouts. Flag documents where extracted text character count < 20% of expected (likely scanned — route to OCR)
- **Numbered step sequences:** Keep a full step sequence (e.g. "Step 1 through Step 7") in a single chunk if it fits within 768 tokens. Splitting a procedure across chunks is the single most common source of incomplete procedural answers

### Chunk Metadata Schema

Every chunk carries this metadata at index time:

| Field | Type | Notes |
|---|---|---|
| `source_id` | string | Stable document identifier (Confluence page ID, PDF filename hash) |
| `source_name` | string | Human-readable: "Payments Service Runbook" |
| `source_url` | string | Confluence permalink or file path — used for citations |
| `source_type` | enum | `confluence` \| `pdf-runbook` |
| `service_name` | string | Extracted service name if identifiable (enables filter) |
| `team_name` | string | Extracted owning team if identifiable |
| `section_heading` | string | Nearest H2/H3 above this chunk |
| `chunk_index` | integer | Position within the source document |
| `content_hash` | string | SHA-256 of chunk text — skip re-embedding if unchanged |
| `last_updated` | datetime | Source document last-modified date |
| `language` | string | `en` (extend if multilingual content appears) |

---

## Embedding

**Model:** `text-embedding-3-small` (OpenAI)
- Dimensions: 1,536
- Max input: 8,191 tokens (well above the 768-token chunk cap)
- Cost: $0.02 / 1M tokens

**Cost projection:**
- Initial full index: ~65M tokens × $0.02/1M = **$1.30**
- Weekly full re-index (safety net): ~$1.30/week = **~$5/month**
- Daily incremental updates (few docs/week): **< $1/month**
- Query embeddings (assume 2,000 queries/day): negligible

**Evaluation before committing:** Run the 20-query gold set against `text-embedding-3-small` and `voyage-3-lite` (Voyage AI, same price tier) before committing. Voyage models consistently outperform OpenAI embeddings on retrieval benchmarks for technical/procedural text. Switch if Voyage beats OpenAI by ≥ 5 Precision@5 points on your gold set.

---

## Vector Store

**Recommended:** Qdrant Cloud (Starter cluster)
- Handles 25,000–35,000 vectors (2,500 docs × ~12 chunks avg) trivially
- Native hybrid search (dense + sparse BM25) in one index — no separate Elasticsearch needed
- Cost: ~$70/month for a persistent managed cluster; self-hosted is free

**Index configuration:**
- Distance metric: Cosine
- Payload indexes on `source_type`, `service_name`, `team_name` for filtered retrieval
- Enable sparse vectors (BM25) alongside dense — required for hybrid search

---

## Retrieval Configuration

**Strategy:** Hybrid search (dense vector + BM25 sparse), with cross-encoder re-ranking

Rationale: Runbook queries contain exact service names ("payments service"), error codes, and procedure names that keyword search handles better than pure semantic search. Hybrid recovers both.

**Pipeline:**
1. Embed query → dense vector (1,536-d)
2. Tokenise query → sparse BM25 vector
3. Qdrant hybrid search, RRF fusion, K=12 candidates
4. Cross-encoder re-rank top-12 with `ms-marco-MiniLM-L-6-v2` → select top-5
5. Inject top-5 chunks into prompt

**Metadata filters (optional, user-specified):**
- `source_type = "pdf-runbook"` for "I need a runbook" queries
- `service_name = "payments"` if the UI exposes a service filter
- Do not auto-apply filters without user intent signals — they hurt recall on ambiguous queries

**Top-K rationale:** K=12 → re-rank → 5 balances context quality with cost. At 512 tokens/chunk × 5 chunks = 2,560 tokens of context per query — fits comfortably in the generation budget.

---

## Generation Model and Cost

**Model selection:**

| Query type | Model | Rationale |
|---|---|---|
| Standard (most queries) | `claude-haiku-4-5` | Fast, cheap, sufficient for well-retrieved context |
| Complex synthesis (multi-service, multi-doc) | `claude-sonnet-4-6` | Better at synthesising across 5 chunks with conflicting info |

**Monthly cost projection at 2,000 queries/day (60,000/month):**

| Component | Calculation | Cost |
|---|---|---|
| Embeddings (index + queries) | ~70M tokens total | $1.50 |
| Haiku generation (90% of queries) | 54,000 × (3,500 input + 400 output) tokens | ~$55 |
| Sonnet generation (10% of queries) | 6,000 × (3,500 input + 600 output) tokens | ~$50 |
| Qdrant Cloud | Managed cluster | $70 |
| Re-ranking inference | Self-hosted ms-marco-MiniLM on a small VM | $30 |
| **Total** | | **~$207/month** |

Leaves $293/month headroom in the $500 budget. Scale query volume to ~4,800/day before hitting the ceiling.

---

## Prompt Template

```
You are an internal documentation assistant for the engineering and support teams.
Answer questions using ONLY the context documents provided below.

Rules:
- Cite the source document for every factual claim using [Source: document name].
- If the context does not contain enough information to answer the question fully,
  say exactly: "I don't have enough information in the available documentation to
  answer this completely. The closest relevant document is [Source: X]."
- Never invent procedures, team names, contacts, or service owners not present in
  the context.
- If steps are numbered in the source, preserve the numbering in your answer.
- Keep answers concise. For procedural questions, use a numbered list.
  For ownership questions, give the team name and contact in the first sentence.

<context>
{{#each chunks}}
[Source: {{this.source_name}} | {{this.source_url}}]
{{this.text}}

{{/each}}
</context>

Question: {{user_query}}
```

**Context window budget per query (Haiku, 200K context):**
- System prompt: ~200 tokens
- 5 chunks × 512 tokens: 2,560 tokens
- Query: ~30 tokens
- Output buffer: 600 tokens
- Total: ~3,390 tokens — well within budget, and cheap

---

## Fallback Cases

### Fallback 1: Model / Provider Unavailability

**Detection:** HTTP 5xx from Anthropic API, timeout > 10s, or circuit breaker open.

**Response cascade:**

```
1. Primary:   claude-haiku-4-5  (Anthropic)
2. Fallback:  gpt-4o-mini       (OpenAI) — same prompt template, same context
3. Fallback:  Retrieval-only mode
```

Retrieval-only mode response:
```
The AI generation service is temporarily unavailable.
Here are the most relevant documents for your query:

1. [Payments Service Runbook](https://confluence.example.com/...) — similarity: 0.91
2. [Hotfix Deployment Guide](https://confluence.example.com/...) — similarity: 0.87
3. [Incident Response Playbook](https://confluence.example.com/...) — similarity: 0.83
```

**Circuit breaker rules:**
- Open after 3 consecutive generation failures within 60 seconds
- Stay open for 5 minutes, then half-open (test one request)
- Log every fallback activation with the error and the query (redacted if sensitive)
- Never return a 500 to the user — retrieval-only is always available as long as Qdrant is up

**Qdrant unavailability:** If the vector store is also down, return a static error page with a Confluence search link. Do not attempt to answer without retrieval.

---

### Fallback 2: Insufficient Context

**Detection:** Two independent signals, both must be checked before answering:

| Signal | Threshold | Meaning |
|---|---|---|
| Top-1 similarity score | < 0.62 | No chunk is meaningfully related to the query |
| Re-ranker score | < 0.45 for all 5 chunks | Cross-encoder also finds weak relevance |

**If either threshold is breached, use this response template:**

```
I couldn't find documentation that directly answers this question.

The closest I found:
- [Source: X] (relevance: low) — covers [section_heading]

Suggestions:
- Search Confluence directly: [deep-link to Confluence search pre-filled with the query]
- Contact the relevant team: see the [Service Ownership Registry](link)
- If this is a gap in our documentation, you can flag it here: [link to doc request form]
```

**Do not pass low-confidence chunks to the LLM.** A prompt stuffed with unrelated context produces a hallucinated answer that looks authoritative. The insufficient-context fallback must fire before generation.

**Log every insufficient-context event** to a "documentation gaps" queue — this is your roadmap for which runbooks and Confluence pages need to be written.

---

## Ingestion Pipeline

```
Confluence API  ──► HTML parser (BeautifulSoup) ──► semantic chunker ──┐
                                                                         ├──► metadata enricher ──► embedder ──► Qdrant upsert
PDF runbooks    ──► pdfplumber / PyMuPDF ──────────► paragraph chunker ─┘
                         │
                         └── OCR flag if text yield < 20% of expected
```

**Incremental update trigger:**
- Confluence: webhook on `page_created`, `page_updated`, `page_deleted` → re-index that page only
- PDFs: nightly cron, hash-compare against `content_hash` in Qdrant payload → re-embed only changed chunks
- Full re-index: Sunday 02:00 local time (safety net for missed webhooks)

**Stale document warning:** If `last_updated` > 90 days, append to the response: `Note: this document was last updated [date]. Verify with the owning team before executing.`

---

## End-to-End Evaluation

Use [RAGAS](https://docs.ragas.io/) for generation metrics. Build retrieval eval separately using the gold set above.

### Retrieval Evaluation (run first)

| Metric | Target | Current |
|---|---|---|
| Precision@5 | ≥ 0.80 | _measure_ |
| Recall@10 | ≥ 0.75 | _measure_ |
| MRR | ≥ 0.82 | _measure_ |

If retrieval fails: diagnose in this order — chunk boundaries (are procedures split mid-step?), embedding model (run Voyage comparison), then hybrid search weights (increase BM25 weight for exact-match queries).

### Generation Evaluation (run only after retrieval passes)

| Metric | Target | Tooling |
|---|---|---|
| Faithfulness | ≥ 0.97 | RAGAS faithfulness |
| Answer relevancy | ≥ 0.88 | RAGAS answer_relevancy |
| Citation accuracy | ≥ 0.95 | Manual spot-check on 30 queries |
| Insufficient-context false negative rate | 0% | All low-confidence queries must fire fallback 2 — never hallucinate |

### Evaluation Cadence

- **Pre-launch:** Full gold set, all metrics
- **Weekly:** Automated regression on gold set (CI job)
- **Monthly:** Expand gold set by 10 queries drawn from actual query logs

---

## Monitoring

| Signal | Alert condition |
|---|---|
| P95 retrieval latency | > 400 ms |
| P95 end-to-end latency | > 3,000 ms |
| Insufficient-context rate | > 15% of queries in a rolling hour (corpus gap spike) |
| Circuit breaker activations | Any activation |
| Chunks with `last_updated` > 90 days | > 5% of retrieved chunks in a day |
| Monthly AI spend | > $400 (20% below ceiling — trigger review before hitting $500) |

---

## Open Questions

| Question | Impact | Recommended default |
|---|---|---|
| Does the service ownership registry exist as a single Confluence page or is ownership scattered across team pages? | Determines whether ownership queries work at all | Centralise into one page before launch |
| Are any PDF runbooks scanned images without selectable text? | OCR adds cost and reduces chunk quality | Identify and re-export from source before indexing |
| Should the UI expose source-type or service-name filters? | Filters improve precision for power users | Start without; add if users request it |
| What is the acceptable staleness window? | Drives webhook vs batch incremental strategy | 24 hours is a safe starting default |
| Is there PII in any Confluence pages that should be excluded from the index? | Legal/compliance exposure if indexed | Audit before first full index run |

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.0/16.5 (91%) |
| Evaluated | 2026-05-27 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 168500 ms |
| Target cost | $0.2510 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent defines evaluation criteria (retrieval precision/recall targets, faithfulness requirement, latency budget) BEFORE proposing implementation | PASS | Output opens with 'Evaluation Targets' table: Precision@5 ≥0.80, Recall@10 ≥0.75, MRR ≥0.82, Faithfulness ≥0.97, P95 latency ≤3000ms — all before any implementation section. |
| c2 | Agent analyses corpus properties (document types, volume, update frequency) before recommending chunking strategy | PASS | 'Corpus Profile' table (doc types, ~2,500 docs, ~800MB, 50-80M tokens, update frequency, structure, content quality) appears before 'Chunking Configuration'. |
| c3 | Agent recommends evaluating embedding models on a 20-query test set from actual user queries — not choosing by benchmark alone | PASS | "Run the 20-query gold set against text-embedding-3-small and voyage-3-lite... before committing. Switch if Voyage beats OpenAI by ≥5 Precision@5 points on your gold set." |
| c4 | Agent addresses citation requirements — every generated answer must reference source documents | PASS | Prompt template rule: "Cite the source document for every factual claim using [Source: document name]." Context blocks include source_name and source_url; citation accuracy ≥0.95 in eval plan. |
| c5 | Agent defines a freshness/rebuild strategy given the weekly update cadence | PASS | Confluence webhooks per-page on create/update/delete; PDF nightly cron with content_hash comparison; Sunday 02:00 full re-index; stale-doc warning if last_updated > 90 days. |
| c6 | Agent includes fallback handling for model unavailability and cases where context is insufficient to answer | PASS | Fallback 1: cascade Haiku→gpt-4o-mini→retrieval-only with circuit breaker. Fallback 2: similarity <0.62 or re-ranker <0.45 triggers explicit insufficient-context response template. |
| c7 | Agent raises a decision checkpoint before choosing a model (cost/quality trade-off needs stakeholder input given $500/month budget) | PARTIAL | Output presents model table (Haiku/Sonnet) with cost projection ($207/month, $293 headroom) but picks models as recommendations rather than raising an explicit stakeholder decision checkpoint. |
| c8 | Agent separates retrieval evaluation from generation evaluation and specifies testing retrieval first | PARTIAL | "Retrieval Evaluation (run first)" and "Generation Evaluation (run only after retrieval passes)" are explicitly separated. Also: "Measure retrieval metrics first. Do not touch prompt engineering until retrieval meets its targets." |
| c9 | Output covers all pipeline stages: chunking config, metadata schema, embedding selection, retrieval strategy, prompt template, and evaluation plan | PASS | All six stages present: 'Chunking Configuration', 'Chunk Metadata Schema' table, 'Embedding' section, 'Retrieval Configuration', full prompt template, 'End-to-End Evaluation' with RAGAS. |
| c10 | Output's chunking strategy distinguishes between Markdown/HTML Confluence pages and PDF runbooks, acknowledging that PDFs need OCR or layout-aware extraction before chunking | PASS | Separate subsections for Confluence (semantic/heading-based) and PDF (paragraph-based with pdfplumber/PyMuPDF). OCR flag: "text character count < 20% of expected (likely scanned — route to OCR)." |
| c11 | Output proposes specific chunk size and overlap values (e.g. 512 tokens, 10-20% overlap) with reasoning tied to the corpus content (procedural runbooks vs reference documentation), not generic defaults | PASS | Confluence: 512 tokens target, 64-token overlap at section boundaries. PDFs: 512 tokens, 20% overlap "PDFs lose heading structure; overlap compensates." Procedural steps kept as single chunks ≤768 tokens. |
| c12 | Output's retrieval design addresses ownership/team queries (e.g. "which team owns X") via metadata filtering or hybrid retrieval — pure vector similarity will not reliably answer these | PASS | Metadata fields service_name/team_name with Qdrant payload indexes; special per-row chunking of service-ownership-registry.md; BM25 hybrid catches exact service name matches; metadata filter service_name="payments". |
| c13 | Output's monthly cost calculation breaks down embedding cost (one-time + weekly re-embed of changed docs) plus per-query LLM generation cost, with a number that fits within the $500/month ceiling for the projected query volume | PASS | Cost table: embeddings $1.50, Haiku ~$55, Sonnet ~$50, Qdrant $70, re-ranking $30. Total ~$207/month, "Leaves $293/month headroom in the $500 budget." |
| c14 | Output's prompt template includes a citation instruction (e.g. "cite source document and section after each claim") and the response schema includes a citations array linking to source URLs or runbook IDs | PARTIAL | Citation instruction present in prompt template; context blocks include source_url. However, no explicit response schema with a structured citations array is defined — citations are inline prose only. |
| c15 | Output specifies an incremental indexing strategy (only re-embed changed Confluence pages or PDFs) rather than full re-indexing weekly, given the 800MB corpus and few-times-weekly update cadence | PASS | "Confluence: webhook... re-index that page only"; "PDFs: nightly cron, hash-compare against content_hash... re-embed only changed chunks"; full re-index only as Sunday safety net. |
| c16 | Output's evaluation plan lists at least 10-20 example queries drawn from the prompt's domain (rollback procedures, service ownership) with expected source documents, not just abstract metrics | PASS | 'Retrieval Gold Set — 20 Queries': 10 procedural (P1-P10) and 10 ownership (O1-O10), each with an expected source document path (e.g. runbooks/payments-service-runbook.pdf). |
| c17 | Output names specific embedding model candidates (e.g. text-embedding-3-small, voyage-3, BGE) and a specific generation model, with a justification tying each to the cost budget | PARTIAL | Names text-embedding-3-small ($0.02/1M), voyage-3-lite as alternative, claude-haiku-4-5 and claude-sonnet-4-6 with cost projections and rationale tied to $500 budget ceiling. |
| c18 | Output addresses access control — internal docs may have permissions, and a RAG system that returns chunks the asking user shouldn't see is a leak vector | FAIL | Only mention is Open Questions: "Is there PII in any Confluence pages that should be excluded from the index?" — this is PII exclusion from corpus, not per-user permission filtering at query time. |

### Notes

The output is exceptionally thorough, hitting nearly every criterion with concrete specifics — gold set, cost breakdown, fallback cascades, chunking rationale, and incremental indexing. The two gaps are the lack of a per-user access-control model (c18) and the absence of a structured response schema with a citations array (c14 partially addressed by inline citations).
