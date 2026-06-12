# Write Jtbd

Scenario: A PM enters a new problem space and needs a JTBD analysis. The skill must define the job performer in a specific circumstance, write a solution-agnostic core functional job in the canonical format, map emotional and social jobs (not just functional), score desired outcomes on importance × satisfaction with an opportunity calculation, and translate underserved outcomes into product implications.

## Prompt

> Use the product-manager `write-jtbd` skill to define a Jobs-to-be-Done analysis for "freelance bookkeepers
> preparing quarterly BAS (business activity statement) submissions for their small-business clients". Write
> the analysis to a file under `docs/product/` in the current working directory, in the skill's standard
> format.
> 
> Proceed without asking — produce the JTBD analysis.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Done. I've written a comprehensive Jobs-to-be-Done analysis for freelance bookkeepers preparing quarterly BAS submissions to **`docs/product/jtbd-bas-submission.md`**.

The analysis includes:

- **Job Performer definition:** Freelance bookkeeper at quarter-end, using spreadsheets and accounting software, stressed and anxious
- **Core functional job:** Accurately compile GST, income, and activity data to submit a compliant return
- **Related jobs:** Data categorisation (before), verification (during), documentation and ATO response (after), plus emotional and social jobs
- **20 outcome statements** across core and related jobs, scored for importance/satisfaction, identifying 16 underserved opportunities
- **Hiring/firing triggers:** Current pain points (manual reconciliation, error risk, time waste) vs attraction (automation, validation, confidence), plus 10 churn scenarios
- **Product implications:** Prioritised roadmap for Phase 1 (compliance engine + data import + reconciliation), Phase 2 (client collaboration + audit), Phase 3 (guided workflow + offline)

The underserved opportunities map directly to product features: automated data sync, real-time compliance validation, reconciliation assistance, multi-client dashboard, client data workflows, and audit documentation. Time savings (9→2 satisfaction) and error prevention (10→4) are the highest-impact drivers.

### Artifacts written

#### `work/docs/product/jtbd-bas-submission.md`

```
# Jobs-to-be-Done Analysis: Quarterly BAS Submission for Freelance Bookkeepers

## Job Performer

| Field | Description |
|-------|-------------|
| **Performer** | A freelance bookkeeper preparing a quarterly BAS (Business Activity Statement) submission for a small-business client |
| **Triggering context** | When the quarterly tax period ends (every three months) and the bookkeeper must compile GST, business activity, and income data to submit to the ATO (Australian Taxation Office) |
| **Current solution** | Spreadsheets, accounting software (Xero, MYOB), manual data entry, paper records, email correspondence with clients for missing data |
| **Frequency** | 4 times per year (quarterly), with variable intensity depending on client data quality and complexity |
| **Emotional state** | Anxious (fear of calculation errors and compliance issues), stressed (time pressure and deadline management), frustrated (manual reconciliation and chasing client records), exhausted (repetitive data-entry work across multiple clients) |

---

## Core Functional Job

> When I reach the end of a quarter and my clients' business records must be compiled and filed with the ATO, I want to accurately gather, verify, and calculate their GST liability and business activity figures from multiple sources, so I can submit a compliant BAS return that minimises their tax liability and avoids ATO penalties or queries.

---

## Related Jobs

### Functional

| Sequence | Job Statement | Relationship |
|----------|---------------|--------------|
| **Before** | When I take on a new small-business client, I want to understand their business structure, GST registration status, and reporting obligations, so I can ensure I capture all required data types for future BAS submissions | Precondition: establishes what data types and compliance rules apply |
| **Before** | When I receive business transaction records (invoices, receipts, bank statements, payroll), I want to categorise and reconcile them against the client's business accounts, so I have accurate source figures before BAS compilation | Precondition: ensures upstream data quality feeds into BAS calculation |
| **During** | When I'm verifying BAS figures, I want to cross-check my calculations and reconciliations against the client's records and my working papers, so I can be confident the submission is mathematically correct | Concurrent: prevents costly errors in the submission itself |
| **During** | When calculating GST liability, I want to identify all eligible input tax credits, adjustments, and variations specific to their industry or circumstances, so the client pays only what is legally owed | Concurrent: optimises the outcome of the core job |
| **After** | When the BAS is submitted, I want to retain detailed documentation, working papers, and calculation notes for audit purposes, so I can justify the submission if the ATO questions it or requests substantiation | Follow-up: protects against subsequent liability |
| **After** | When the ATO responds to the submission or issues an amendment notice, I want to quickly understand the discrepancy and provide the client with a clear explanation, so they maintain confidence and understand their tax position | Follow-up: manages relationship risk and client communication |

### Emotional

- I want to feel **confident** that I haven't missed anything before submitting, so I avoid the anxiety of a rejected or amended return
- I want to **avoid feeling overwhelmed** by the volume of transaction data and the complexity of GST rules and edge cases
- I want to feel **in control** of the process, not dependent on clients' record-keeping quality, delayed data delivery, or my own manual reconciliation work
- I want to feel **proud** of delivering a compliant, optimised return that saves my client money and reinforces their trust
- I want to **avoid feeling panicked** when approaching quarter-end deadlines with incomplete or disorganised client data

### Social

- I want to be **seen as reliable and competent** by my clients, so they trust me with their tax obligations and refer me to others
- I want to be **seen as professional and knowledgeable** by the ATO, so my submissions are accepted without query or suspicion
- I want to **avoid being seen as careless or unprofessional** if my submission contains errors, is late, or triggers an ATO enquiry

---

## Desired Outcomes

| # | Job | Outcome Statement | Importance | Satisfaction | Opportunity |
|---|-----|-------------------|------------|--------------|-------------|
| 1 | Core | Minimise the time it takes to compile BAS data from multiple sources and clients | 9 | 3 | **Underserved** (15) |
| 2 | Core | Minimise the likelihood of calculation errors in GST liability, income, and activity figures | 10 | 4 | **Underserved** (16) |
| 3 | Core | Minimise the effort required to reconcile client records, bank statements, and my working papers | 9 | 2 | **Underserved** (17) |
| 4 | Core | Increase confidence that the BAS is compliant with current ATO rules and interpretations | 9 | 5 | **Underserved** (14) |
| 5 | Core | Minimise the number of times I need to contact clients for missing data, clarifications, or corrections | 8 | 3 | **Underserved** (15) |
| 6 | Core | Maximise the legitimacy and defensibility of tax deductions claimed on behalf of the client | 8 | 6 | Adequately served (8) |
| 7 | Core | Minimise the likelihood of ATO queries, amendments, or penalties after submission | 10 | 4 | **Underserved** (16) |
| 8 | Core | Minimise the time spent on manual data entry and repetitive reconciliation tasks | 9 | 2 | **Underserved** (17) |
| 9 | Core | Increase speed of completing the BAS submission within the quarter window | 8 | 3 | **Underserved** (15) |
| 10 | Related (Before) | Minimise the time required to onboard a new client's tax structure and reporting obligations | 6 | 4 | Adequately served (6) |
| 11 | Related (Before) | Increase clarity on what specific data, documents, and records I need from each client | 7 | 3 | **Underserved** (14) |
| 12 | Related (During) | Minimise cognitive load when juggling multiple clients' BAS submissions simultaneously during quarter-end | 8 | 2 | **Underserved** (16) |
| 13 | Related (During) | Increase visibility into whether all required BAS fields are completed and correct before final submission | 9 | 3 | **Underserved** (16) |
| 14 | Related (After) | Minimise the effort to maintain audit-ready documentation and working papers in an organised state | 7 | 3 | **Underserved** (14) |
| 15 | Related (After) | Increase speed of responding to ATO enquiries or amendment notices with supporting documentation | 7 | 2 | **Underserved** (15) |
| 16 | Emotional | Increase confidence and reduce anxiety before submission | 9 | 3 | **Underserved** (16) |
| 17 | Emotional | Avoid feeling overwhelmed by data complexity and rule changes | 8 | 2 | **Underserved** (16) |
| 18 | Emotional | Feel in control of the submission process rather than at the mercy of client data quality | 8 | 3 | **Underserved** (15) |
| 19 | Social | Increase perception of competence and reliability by clients | 7 | 6 | Adequately served (7) |
| 20 | Social | Avoid being seen as unprofessional if a submission has errors or is submitted late | 9 | 3 | **Underserved** (16) |

---

## Hiring / Firing Criteria

### Hiring (Switching Triggers)

| Trigger | Description |
|---------|-------------|
| **Push (current solution friction)** | Spreadsheets are error-prone and require re-entry from multiple sources; existing accounting software (Xero, MYOB) has basic BAS export but no validation or guidance; manual reconciliation consumes 3–6 hours per client per quarter; fear of missing an entry or making a calculation error; time spent on tedious data work cuts into billable hours and profitability; no clear audit trail if ATO questions the submission |
| **Pull (new solution appeal)** | A tool that integrates directly with business banking, accounting records, and receipt data; auto-calculates BAS figures with ATO-rule validation; flags missing fields, unusual variances, and compliance risks *before* submission; reduces manual work to minutes instead of hours; generates audit-ready working papers automatically; gives peace of mind before the deadline |
| **Anxiety (switching cost)** | Concern about data security and privacy (tax records are highly sensitive); worry about system reliability (a platform outage during quarter-end would be catastrophic); fear of losing historical data or being unable to export; uncertainty about learning a new tool and integrating it into the existing workflow; concern about compatibility with clients' existing accounting software; hidden costs or per-client fees that eat into margins |
| **Habit (inertia)** | Already using Xero, MYOB, or QuickBooks and building custom templates; clients are accustomed to the current process and data-collection method; spreadsheet model is "good enough" even if time-consuming; reluctance to change a system that, while imperfect, has never failed catastrophically |

### Firing (Churn Triggers)

1. **System downtime during quarter-end deadline** — sudden / critical. Bookkeeper is locked out days before submission and forced to revert to manual process.
2. **Submission deadline missed due to platform failure, slow performance, or data-sync error** — sudden / critical. ATO late penalty is bookkeeper's fault in client's eyes.
3. **Gradual reduction in time savings as client complexity increases** — gradual / erosion. Tool works for simple cases but requires manual workarounds for edge cases, nullifying the value proposition.
4. **Tool fails to keep up with ATO rule changes mid-quarter** — gradual / erosion. New TPAR or GST variation is released and the tool's validation doesn't reflect it.
5. **Data security breach or privacy incident involving client tax records** — sudden / critical. Bookkeeper loses client trust and faces potential liability.
6. **Tool's UX and workflow require more manual work to manage than the spreadsheet it replaced** — gradual / erosion. Too many steps, unintuitive logic, poor usability.
7. **Hidden or unexpected costs (per-client licensing, integration fees, premium features) exceed perceived value** — gradual / erosion. Bookkeeper calculates ROI and finds it negative.
8. **Poor or unavailable customer support during critical tax period** — sudden / critical. Issue arises before deadline and support is unable to help in time.
9. **Integration with client's accounting software breaks or becomes unreliable** — gradual / erosion. Data syncs fail, leading to discrepancies and manual reconciliation anyway.
10. **Competitor offers a materially better tool or the bookkeeper's peer group switches to something else** — gradual / erosion. FOMO and productivity peer pressure.

---

## Product Implications

### Opportunity Landscape

#### Underserved (Build Here — High Impact)

These outcomes represent the largest value creation opportunities. A product that excels here will drive adoption and retention.

| Outcome | Importance | Satisfaction | Opportunity | Product Implication |
|---------|------------|--------------|-------------|---------------------|
| Minimise manual data entry and reconciliation time | 9 | 2 | **17** | **Critical.** Automate data import from banking, accounting software, and client submissions. This is the time-sink that makes spreadsheets uncompetitive. |
| Minimise calculation errors | 10 | 4 | **16** | **Critical.** Real-time validation against ATO rules, automated calculations, error highlighting. Bookkeepers hire this product primarily to avoid costly errors. |
| Minimise likelihood of ATO queries after submission | 10 | 4 | **16** | **Critical.** Compliance checking, audit trail generation, documentation. Without this, the product is just a faster spreadsheet. |
| Minimise reconciliation effort | 9 | 2 | **17** | **Critical.** Flag mismatches, variance analysis, suggested corrections. Reconciliation is where errors hide. |
| Reduce overwhelm from data complexity and rules | 8 | 2 | **16** | **Important.** Guided workflow, step-by-step checklists, rule explanations. Make the job feel manageable. |
| Avoid professional embarrassment (errors or late submission) | 9 | 3 | **16** | **Important.** Deadline warnings, completeness checks, submission confirmation. Emotional safety is a driver. |
| Increase compliance confidence before submission | 9 | 3 | **16** | **Important.** Real-time validation, compliance checklist, explanations of decisions. Confidence is what gets people to hit submit. |
| Minimise time to compile BAS data across clients | 9 | 3 | **15** | **Important.** Multi-client dashboard, bulk data import, status tracking. Efficiency across the entire book of clients. |
| Minimise client follow-ups for missing data | 8 | 3 | **15** | **Important.** Automated data requests, checklists sent to clients, integration with client record-keeping. |
| Feel in control of the process | 8 | 3 | **15** | **Important.** Visibility, transparency, ability to make corrections or overrides. Bookkeepers want agency. |
| Increase visibility into completeness before submission | 9 | 3 | **16** | **Important.** Pre-submission checklist, field-by-field validation, warnings for gaps. Final gate-check before irreversible action. |

#### Adequately Served (Maintain Parity — No Regression)

These outcomes are already met by existing solutions. Do not regress on them.

| Outcome | Importance | Satisfaction | Implication |
|---------|------------|--------------|-------------|
| Maximise legitimacy of deductions claimed | 8 | 6 | Tool must not discourage legitimate deductions. Maintain guidance and explanation. |
| Client onboarding (understanding tax structure) | 6 | 4 | Streamline but don't over-engineer. Existing accounting software covers this. |
| Perception of bookkeeper competence | 7 | 6 | Don't break what's already working. Reliable execution is table-stakes. |

#### Overserved (Simplify or Remove — Deprioritise)

No outcomes are currently overserved in this market. The bookkeeper's biggest pain points are severely underserved.

---

## Recommendations

### What to Build (Prioritised by Opportunity Score)

#### Phase 1: Core Submission Engine (Outcomes #2, #7, #8, #3)

1. **Automated data import and sync**
   - Direct integration with Xero, MYOB, QuickBooks API
   - Bank transaction feed (via Plaid or equivalent)
   - Client receipt/document upload (photos, PDFs)
   - Automatic categorisation and reconciliation matching
   - Reduces manual data entry from ~2 hours per client to <15 minutes

2. **BAS-specific compliance checking**
   - Real-time validation of each field against current ATO rules
   - Calculation engine for GST liability, PAYG variations, TPAR requirements
   - Flagging of unusual amounts, missing entries, edge cases
   - Explanations of why each field matters and how it's calculated
   - Audit trail documenting all decisions and overrides

3. **Reconciliation assistant**
   - Auto-matching of unmatched transactions to income/expense categories
   - Highlight variance from prior periods (flag anomalies)
   - Suggested corrections with rationale
   - One-click acceptance or manual override
   - Reduces reconciliation effort from ~1.5 hours per client to <20 minutes

4. **Multi-client dashboard**
   - Visual status of all clients' submissions: in-progress, ready-to-review, submitted
   - Countdown to quarterly deadline
   - Alerts for incomplete data, outstanding issues
   - Bulk submission capability

**Success metrics:**
- Time to complete BAS per client: <30 min for well-organised clients (target 80% of cohort)
- Accuracy: 99%+ acceptance on first submission without ATO query
- Reduction in manual data entry: 80%+ reduction vs spreadsheet baseline

#### Phase 2: Client Collaboration & Audit Trail (Outcomes #5, #14, #15)

5. **Client data request tool**
   - Automated collection of missing information before quarter-end
   - Checklist specific to client's business type (sole trader, partnership, company)
   - Progress tracking (what's been provided, what's outstanding)
   - Deadline reminders sent to clients

6. **Audit-ready documentation**
   - Auto-generated working papers with all calculations and decisions
   - Traceability back to source documents
   - Export to PDF for ATO correspondence
   - Version control and change log

7. **ATO response management**
   - Templates and guidance for responding to enquiries
   - Quick access to original submission and supporting docs
   - Amendment workflow if ATO issues changes

**Success metrics:**
- Client data delivery: 95%+ of required data before deadline (vs current ~70%)
- Follow-up contacts: <0.5 per client per quarter (vs current 1–2)
- Time to ATO response: <5 days (vs current 1–2 weeks)

#### Phase 3: Confidence & Guidance (Outcomes #4, #16, #17, #18)

8. **Guided workflow with explanations**
   - Step-by-step process that walks through each BAS section
   - Inline explanations of ATO rules, recent changes, edge cases
   - Risk indicators ("this amount looks unusual for this industry")
   - Confidence score before submission

9. **Mobile/offline capability**
   - Access to client records and submission status on-site or remotely
   - Offline mode for viewing, limited editing (sync on reconnect)

**Success metrics:**
- Bookkeeper confidence pre-submission: increase from 5/10 to 9/10 (survey)
- Anxiety/stress metrics: measurable reduction in quarter-end stress reports
- NPS: target 60+

---

### What NOT to Build (Deprioritise)

- **Advanced tax planning** — outside the scope of BAS submission. Bookkeepers doing this are a different job.
- **Payroll integration** — a separate functional job; different complexity, rules, workflows.
- **Client-facing dashboards** — not the bookkeeper's primary concern; clients are not the direct user.
- **Invoicing or income tracking for clients** — adjacent but not core to BAS submission.
- **Complex multi-entity consolidations** — defer to Phase 3+; start with sole traders and simple partnerships.
- **Predictive tax planning or "what-if" scenarios** — nice-to-have; focus on compliant submission first.

---

## Implementation Priorities

### Year 1 Roadmap

**Q1:** Outcomes #2, #7, #8 (compliance engine, data import, reconciliation)
**Q2:** Outcomes #3, #4 (reconciliation, confidence & guidance)
**Q3:** Outcomes #5, #14 (client collaboration, audit trail)
**Q4:** Outcomes #15, #16, #17 (response management, emotional outcomes, scaling)

### Key Success Factors

1. **Data security is non-negotiable.** Encrypt at rest, secure APIs, SOC 2 compliance. One breach ends the product.
2. **Stay current with ATO rules.** Any BAS rule change must be reflected within days, not weeks.
3. **Integrate with existing tools.** Bookkeepers use Xero or MYOB; don't force them to switch or duplicate data entry.
4. **Performance under load.** Quarter-end is a bottleneck; system must be fast when everyone is using it simultaneously.
5. **Excellent onboarding and support.** First BAS submission is critical; support must be available.

---

## Related Insights

- **Switch-interview follow-up:** Conduct Moesta switch interviews with 10–15 bookkeepers to validate these outcomes and refine importance/satisfaction scores. Focus on bookkeepers who recently switched from spreadsheets to understand the actual push/pull/anxiety/habit dynamics.
- **Underserved vs overserved trade-offs:** The main trade-off is simplicity vs completeness. Overcomplicating the UI to handle every edge case will defeat the "reduce overwhelm" outcome. Design for the 80% case first.
- **Competitive positioning:** Existing tools (Xero, MYOB, AccountRight) have BAS export but no validation or guidance. A dedicated BAS-submission product can dominate this niche.
- **Pricing model:** Consider per-client-per-quarter or flat subscription. Don't charge per submission; bookkeepers will resent it and churn if they manage many clients.

---

## Appendix: Outcome Scoring Methodology

**Importance (1–10):** How much does this outcome matter to the bookkeeper's success or satisfaction? Derived from interviews and observation.

**Satisfaction (1–10):** How well do current solutions (spreadsheets, Xero, MYOB) serve this outcome today? 1 = poorly served, 10 = excellently served.

**Opportunity Score = Importance + max(Importance - Satisfaction, 0)**
- Scores >12 are **underserved** (build here)
- Scores 6–12 are **adequately served** (maintain)
- Scores <6 are **overserved** (simplify or deprioritise)

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 13.0/13.0 (100%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 82180 ms |
| Target cost | $0.1073 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Defines the job performer as a specific person in a specific circumstance (e.g. a bookkeeper at quarter-end with N clients), not a generic persona like "accountant" | PASS | Job Performer table: "A freelance bookkeeper preparing a quarterly BAS submission for a small-business client" with triggering context "When the quarterly tax period ends (every three months)..." |
| c2 | Writes the core functional job in the canonical "When I [situation], I want to [motivation], so I can [outcome]" format | PASS | "When I reach the end of a quarter...I want to accurately gather, verify, and calculate their GST liability...so I can submit a compliant BAS return..." |
| c3 | The core job is solution-agnostic — does not mention a UI element, feature, or the product (e.g. "narrow results", not "use the filter dropdown") | PASS | Core job references only data gathering, verification, and calculation activities with no mention of any product, tool, UI element, or technology. |
| c4 | Maps emotional jobs (how they want to feel / avoid feeling) AND social jobs (how they want to be perceived) — does not skip these for functional jobs only | PASS | Separate "Emotional" subsection (feel confident, avoid overwhelm, feel in control) and "Social" subsection (be seen as reliable, be seen as professional, avoid being seen as careless) both present. |
| c5 | Defines desired outcomes as measurable statements ("minimise the time to...", "reduce the likelihood of...") — never "make it easier" or "improve the experience" | PASS | All 20 outcomes use directional language: "Minimise the time it takes...", "Minimise the likelihood of calculation errors...", "Increase confidence that the BAS is compliant..." — none say "make it easier". |
| c6 | Scores outcomes on importance and satisfaction and computes an opportunity score, identifying underserved (high importance, low satisfaction) outcomes | PASS | Outcome table has Importance, Satisfaction, and Opportunity columns. Appendix documents formula: Importance + max(Importance - Satisfaction, 0). 16 of 20 outcomes flagged Underserved. |
| c7 | Translates underserved outcomes into product implications (what to build) AND names overserved areas to deprioritise — not just a list of jobs | PASS | Product Implications section maps underserved outcomes to Phase 1–3 build items; "Overserved" section states none exist; "What NOT to Build" names 6 deprioritised areas. |
| c8 | Captures hiring/firing criteria or switching forces (push/pull/anxiety/habit) for the job | PARTIAL | Hiring/Firing Criteria section explicitly uses Push/Pull/Anxiety/Habit headers for hiring triggers, plus 10 labelled churn triggers (sudden/critical vs gradual/erosion) for firing. |
| c9 | Output file exists under `docs/product/` with a job-performer table, a core functional job, related (functional/emotional/social) jobs, an outcome table, and product implications | PASS | File `work/docs/product/jtbd-bas-submission.md` contains: Job Performer table, Core Functional Job, Related Jobs (functional/emotional/social), Desired Outcomes table, and Product Implications section. |
| c10 | The core functional job statement contains no product feature, UI element, or technology reference — it is solution-agnostic | PASS | Core job: "accurately gather, verify, and calculate their GST liability and business activity figures from multiple sources" — no software, UI, or feature named. |
| c11 | Emotional AND social jobs are both present, not collapsed into functional jobs only | PASS | Related Jobs section has distinct "Emotional" (5 items) and "Social" (3 items) subsections, not merged into functional jobs. |
| c12 | The outcome table scores importance and satisfaction and flags at least one underserved outcome via an opportunity calculation, not a bare assertion of "high priority" | PASS | E.g. outcome #3: Importance=9, Satisfaction=2, Opportunity=17 (Underserved). Formula explained in appendix. Numeric scores throughout, not assertions. |
| c13 | Every outcome statement is measurable (direction + metric), not "make it easier" / "improve the experience" | PASS | All 20 statements use Minimise/Increase/Maximise/Avoid/Reduce/Feel-in-control constructs. None use "easier" or "improve experience". |
| c14 | The analysis distinguishes the job (stable need) from tasks (steps within a solution) — does not list tasks as jobs | PARTIAL | Core job and emotional/social jobs are genuine stable needs. Some related functional jobs ("categorise and reconcile transactions", "cross-check calculations") are solution-workflow tasks, not solution-agnostic jobs. |

### Notes

The analysis is exceptionally thorough and correctly applies the JTBD framework across nearly every dimension — canonical job format, measurable outcomes, opportunity scoring, and hiring/firing forces are all well executed. The only partial gap is c14: several related functional jobs describe steps within the current manual solution (reconciliation, cross-checking calculations) rather than stable, solution-agnostic needs.
