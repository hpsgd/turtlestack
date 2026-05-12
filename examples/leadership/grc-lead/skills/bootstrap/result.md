# Bootstrap

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/governance/CLAUDE.md` containing a user-authored section. The grc-lead bootstrap skill should preserve that user content while appending the template's missing sections (with a merge marker), and should create the three files the fixture is missing — `risk-register.md`, `compliance-checklist.md`, and `ai-governance-policy.md`. The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

> The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/governance/CLAUDE.md` is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.
> 
> Read the grc-lead bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/leadership/grc-lead/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.
> 
> After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## GRC Lead Bootstrap Complete

### Files created
- `docs/governance/risk-register.md` — risk register template
- `docs/governance/compliance-checklist.md` — compliance checklist template
- `docs/governance/ai-governance-policy.md` — AI governance policy template

### Files merged
- `docs/governance/CLAUDE.md` — appended missing sections (What This Domain Covers, Risk Management, Compliance Frameworks, AI Governance, DPIA Process, Audit Readiness, Tooling, Available Skills, Conventions) while preserving user-authored "Custom team notes" section with sentinel

### Next steps
- Conduct initial risk assessment using `/grc-lead:risk-assessment`
- Determine applicable compliance frameworks in `compliance-checklist.md`
- Classify AI systems using `/grc-lead:ai-governance-review`
- Complete DPIAs for high-risk data processing using `/grc-lead:write-dpia`

### Artifacts written

#### `work/docs/governance/ai-governance-policy.md`

```
# AI Governance Policy

> Governs the development, deployment, and operation of AI/ML systems.

## Scope

This policy applies to all AI/ML systems developed or deployed by the project, including:
- Large language model (LLM) integrations
- Machine learning models (classification, prediction, recommendation)
- Automated decision-making systems

## AI System Inventory

| System | Risk Level | Purpose | Model | Owner | Last Review |
|--------|-----------|---------|-------|-------|-------------|
| | Minimal / Limited / High | | | | |

## Principles

1. **Transparency** — users know when they are interacting with AI
2. **Fairness** — systems are tested for bias before deployment
3. **Accountability** — every AI system has a named owner
4. **Safety** — guardrails prevent harmful outputs
5. **Privacy** — personal data is minimised and protected

## Review Requirements

| Risk Level | Review Type | Frequency |
|------------|------------|-----------|
| High | Full AI governance review + DPIA | Before deployment, then annually |
| Limited | Transparency assessment | Before deployment, then annually |
| Minimal | Self-assessment | Annually |

## Incident Response

AI-specific incidents (harmful output, bias detected, data leak via AI):
1. Disable or restrict the AI system immediately
2. Notify the AI system owner and GRC lead
3. Investigate root cause and impact
4. Remediate and document in incident report
5. Update guardrails and eval suites

> Review this policy annually and after any AI-related incident.

```

#### `work/docs/governance/compliance-checklist.md`

```
# Compliance Checklist

> Track compliance status against applicable frameworks. Update during quarterly reviews.

## Framework Applicability

| Framework | Applicable | Maturity Target | Current Status |
|-----------|-----------|-----------------|----------------|
| SOC 2 Type II | Yes / No | | Not started / In progress / Compliant |
| ISO 27001 | Yes / No | | Not started / In progress / Certified |
| GDPR | Yes / No | | Not started / In progress / Compliant |
| Essential Eight | Yes / No | ML2 / ML3 | Not started / In progress / Assessed |
| NIST CSF 2.0 | Yes / No | | Not started / In progress / Aligned |

## Control Mapping

| Control ID | Description | SOC 2 | ISO 27001 | GDPR | Essential Eight | Evidence |
|-----------|-------------|-------|-----------|------|-----------------|----------|
| | | | | | | |

## Open Gaps

| Gap ID | Framework | Control | Gap Description | Remediation | Owner | Due Date |
|--------|-----------|---------|----------------|-------------|-------|----------|
| | | | | | | |

> Map controls across frameworks to reduce duplicate effort. One control can satisfy multiple frameworks.

```

#### `work/docs/governance/risk-register.md`

```
# Risk Register

> Track all identified risks, their ratings, treatments, and owners.

## Active Risks

| ID | Risk Description | Category | Likelihood | Consequence | Rating | Treatment | Owner | Review Date |
|----|-----------------|----------|-----------|-------------|--------|-----------|-------|-------------|
| R-001 | | | | | | | | |

## Risk Categories

| Category | Examples |
|----------|---------|
| Strategic | Market changes, competitive threats |
| Operational | Process failures, resource constraints |
| Technical | System failures, security vulnerabilities |
| Compliance | Regulatory changes, audit findings |
| Financial | Budget overruns, revenue impact |

## Closed / Accepted Risks

| ID | Risk Description | Rating | Disposition | Closed Date |
|----|-----------------|--------|-------------|-------------|
| | | | Accepted / Mitigated / Avoided | |

> Review all active risks quarterly. Update ratings and treatments as context changes.

```

#### `work/docs/governance/CLAUDE.md`

```
# Governance Domain

This directory contains governance, risk, and compliance documentation: risk registers, compliance checklists, AI governance policies, and audit artefacts.

## Custom team notes

USER-EDIT-SENTINEL-DO-NOT-STRIP

This section was written by the team and must survive any bootstrap re-run.
It exists to test the safe-merge contract: the bootstrap skill must not
overwrite or remove user-authored content.

<!-- Merged from grc-lead bootstrap v0.1.0 -->

## What This Domain Covers

- **Risk management** — ISO 31000 risk assessment and treatment
- **Compliance frameworks** — SOC 2, ISO 27001, GDPR, Essential Eight, NIST CSF
- **AI governance** — NIST AI RMF, EU AI Act compliance
- **Privacy** — Data Protection Impact Assessments (DPIAs)
- **Audit readiness** — evidence collection and control mapping

## Risk Management (ISO 31000)

### Risk assessment process

1. **Establish context** — scope, stakeholders, risk criteria
2. **Identify risks** — what can happen, how, and why
3. **Analyse risks** — likelihood and consequence assessment
4. **Evaluate risks** — compare against risk criteria, prioritise
5. **Treat risks** — avoid, mitigate, transfer, or accept

### Risk rating matrix

| Likelihood / Consequence | Insignificant | Minor | Moderate | Major | Catastrophic |
|--------------------------|---------------|-------|----------|-------|-------------|
| Almost certain | Medium | High | High | Extreme | Extreme |
| Likely | Medium | Medium | High | High | Extreme |
| Possible | Low | Medium | Medium | High | High |
| Unlikely | Low | Low | Medium | Medium | High |
| Rare | Low | Low | Low | Medium | Medium |

### Risk treatment options

| Option | When to Use |
|--------|------------|
| Avoid | Eliminate the activity that creates the risk |
| Mitigate | Reduce likelihood or consequence with controls |
| Transfer | Share risk via insurance, contracts, or outsourcing |
| Accept | Risk is within appetite — monitor and review |

## Compliance Frameworks

### SOC 2 Type II

Trust service criteria: Security, Availability, Processing Integrity, Confidentiality, Privacy. Maintain evidence of controls operating effectively over the audit period.

### ISO 27001

Information security management system (ISMS). Requires: risk assessment, Statement of Applicability, continuous improvement cycle (Plan-Do-Check-Act).

### GDPR

For EU personal data: lawful basis, data minimisation, storage limitation, data subject rights, breach notification (72 hours), DPIAs for high-risk processing.

### Essential Eight (ACSC)

Australian Cyber Security Centre maturity model. Target Maturity Level 2 minimum:
1. Application control 2. Patch applications 3. Configure MS Office macros 4. User application hardening 5. Restrict admin privileges 6. Patch operating systems 7. Multi-factor authentication 8. Regular backups

### NIST Cybersecurity Framework (CSF) 2.0

Six functions: Govern, Identify, Protect, Detect, Respond, Recover. Map controls to CSF categories for cross-framework alignment.

## AI Governance

### NIST AI Risk Management Framework (AI RMF)

Four functions: Govern, Map, Measure, Manage. Apply to all AI/ML systems:
- **Govern** — policies, roles, accountability for AI systems
- **Map** — context, intended use, risk identification
- **Measure** — evaluation metrics, bias testing, performance monitoring
- **Manage** — risk treatment, incident response, decommissioning

### EU AI Act

Classify AI systems by risk level:

| Risk Level | Examples | Requirements |
|------------|----------|-------------|
| Unacceptable | Social scoring, real-time biometric ID | Prohibited |
| High | HR screening, credit scoring, safety systems | Conformity assessment, human oversight |
| Limited | Chatbots, deepfakes | Transparency obligations |
| Minimal | Spam filters, AI-assisted games | No specific requirements |

## DPIA Process

Conduct a Data Protection Impact Assessment when processing is likely to result in high risk to individuals:

1. **Describe processing** — purpose, scope, data flows
2. **Assess necessity** — proportionality, lawful basis
3. **Identify risks** — to individuals' rights and freedoms
4. **Mitigations** — measures to address risks
5. **Sign-off** — DPO review and approval

## Audit Readiness

- Maintain a control register mapping controls to frameworks
- Evidence collection: automated where possible (CI logs, access reviews)
- Review cadence: quarterly internal review, annual external audit
- Gap analysis: track remediation items with owners and deadlines

## Tooling

| Tool | Purpose |
|------|---------|
| [MS 365 SharePoint](https://www.microsoft.com/en-au/microsoft-365) | Policy storage and stakeholder access |
| [GitHub](https://github.com) | Governance docs versioned in repo |

## Available Skills

| Skill | Purpose |
|-------|---------|
| `/grc-lead:risk-assessment` | Conduct an ISO 31000 risk assessment |
| `/grc-lead:compliance-audit` | Audit compliance against a framework |
| `/grc-lead:ai-governance-review` | Review AI system governance |
| `/grc-lead:write-dpia` | Write a Data Protection Impact Assessment |

## Conventions

- Every identified risk is recorded in the risk register with an owner
- Compliance evidence is collected continuously, not just before audits
- AI systems are classified per EU AI Act risk levels before deployment
- DPIAs are completed before any new high-risk personal data processing
- Policies are reviewed annually and after significant changes
- All governance documents are version-controlled in this repository

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 9.5/9.5 (100%) |
| Evaluated | 2026-05-13 |
| Target duration | 49202 ms |
| Target cost | $0.1597 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | After bootstrap, `docs/governance/CLAUDE.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim | PASS | work/docs/governance/CLAUDE.md contains '## Custom team notes\n\nUSER-EDIT-SENTINEL-DO-NOT-STRIP' with full surrounding text intact |
| c2 | After bootstrap, `docs/governance/CLAUDE.md` contains the safe-merge marker `<!-- Merged from grc-lead bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged | PASS | Artifact contains exactly '<!-- Merged from grc-lead bootstrap v0.1.0 -->' between the user section and the appended template sections |
| c3 | After bootstrap, `docs/governance/CLAUDE.md` contains the appended template sections — at minimum the "Risk Management (ISO 31000)" and "Compliance Frameworks" headings now appear alongside the preserved user content | PASS | '## Risk Management (ISO 31000)' and '## Compliance Frameworks' both present in CLAUDE.md artifact, following the merge marker |
| c4 | After bootstrap, `docs/governance/risk-register.md` exists and was created from the skill's template (contains an "Active Risks" table with column headers) | PASS | work/docs/governance/risk-register.md exists with '## Active Risks' and table headers: ID, Risk Description, Category, Likelihood, Consequence, Rating, Treatment, Owner, Review Date |
| c5 | After bootstrap, `docs/governance/compliance-checklist.md` exists and was created from the skill's template (contains a "Framework Applicability" table) | PASS | work/docs/governance/compliance-checklist.md exists with '## Framework Applicability' table listing SOC 2, ISO 27001, GDPR, Essential Eight, NIST CSF 2.0 |
| c6 | After bootstrap, `docs/governance/ai-governance-policy.md` exists and was created from the skill's template (contains an "AI System Inventory" table and "Principles" section) | PASS | work/docs/governance/ai-governance-policy.md contains '## AI System Inventory' table and '## Principles' section with 5 numbered principles |
| c7 | Chat output includes a manifest summary headed `## GRC Lead Bootstrap Complete` that distinguishes files created from files merged | PASS | Chat response opens with '## GRC Lead Bootstrap Complete' and contains distinct '### Files created' and '### Files merged' subsections |
| c8 | Output names each created and merged file individually — a bare "bootstrap complete" without the per-file manifest is not enough | PASS | Each file listed by path: risk-register.md, compliance-checklist.md, ai-governance-policy.md under created; CLAUDE.md under merged with per-section detail |
| c9 | Output does not claim it overwrote or replaced `docs/governance/CLAUDE.md` — the language reflects merge, not replacement | PASS | Output says 'appended missing sections...while preserving user-authored "Custom team notes" section with sentinel' — merge language throughout, no replacement claim |
| c10 | Output points the reader at next steps (conducting a risk assessment, determining applicable compliance frameworks, classifying AI systems) consistent with the skill's documented manifest | PARTIAL | Next steps section lists: risk-assessment skill, compliance-checklist.md for frameworks, ai-governance-review skill, and write-dpia skill — all three specified items present |

### Notes

All ten criteria are fully met. The safe-merge contract was executed correctly: sentinel preserved, merge marker present, template sections appended, three new files created with correct structure, and chat manifest is complete and accurate.
