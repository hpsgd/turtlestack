---
name: bootstrap
bootstrap-phase: market
description: "Bootstrap the support and customer success documentation structure for a project. Creates docs/support/, generates initial templates, and writes the support fragment of the support domain doc (the coordinator assembles docs/support/CLAUDE.md). Idempotent — merges missing sections into existing files without overwriting."
argument-hint: "[project name]"
user-invocable: false
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Bootstrap Support & Customer Success Documentation

Bootstrap the support and customer success documentation structure for **$ARGUMENTS**.

This skill covers both support and customer success since they share the `docs/support/` domain.

## Process

### Step 1: Check and create domain directory

```bash
mkdir -p docs/support docs/support/_sections
```

### Step 2: Create or merge files

For each file below, apply the safe merge pattern:
- If file does not exist -> create from template
- If file exists -> read both, find sections in template missing from file, append missing sections with `<!-- Merged from support bootstrap v0.1.0 -->`

#### Fragment: `docs/support/_sections/support.md`

`docs/support/CLAUDE.md` is **assembled by the coordinator** from the fragments in `_sections/` — no plugin
writes it directly. Write the support and customer-success contribution as this fragment. It starts at H2 (the
coordinator generates the `# Support Domain` H1 and a one-line intro). Create it with this content:

```markdown
## What This Domain Covers

### Support
- **Ticket triage** — classification, priority, and routing
- **Knowledge base** — article lifecycle and templates
- **Escalation** — paths and playbooks for complex issues
- **Feedback synthesis** — turning support signals into product insights
- **SLA targets** — response and resolution time commitments

### Customer Success
- **Health scoring** — customer health indicators and thresholds
- **QBR process** — quarterly business review preparation
- **Onboarding** — customer onboarding playbooks
- **Churn analysis** — identifying and mitigating churn risk
- **Expansion** — upsell and cross-sell planning

## Ticket Triage Process

Tickets arrive via GitHub Issues. Triage within the SLA response window:

### Priority classification

| Priority | Criteria | Response SLA | Resolution SLA |
|----------|----------|-------------|----------------|
| P1 — Critical | Service down, data loss, security breach | 1 hour | 4 hours |
| P2 — High | Major feature broken, no workaround | 4 hours | 1 business day |
| P3 — Medium | Feature impaired, workaround available | 1 business day | 3 business days |
| P4 — Low | Minor issue, cosmetic, feature request | 2 business days | Best effort |

### Triage steps

1. **Classify** — assign priority based on impact and urgency
2. **Label** — add appropriate GitHub Issue labels (`bug`, `question`, `feature-request`)
3. **Route** — assign to the correct team or individual
4. **Acknowledge** — respond to the customer within SLA
5. **Track** — update issue with progress until resolved

## KB Article Lifecycle

### Article types

| Type | Purpose | Example |
|------|---------|---------|
| How-to | Step-by-step instructions | "How to configure SSO" |
| Troubleshooting | Diagnose and fix problems | "Fix: login timeout errors" |
| FAQ | Common questions | "What data is encrypted?" |
| Reference | Technical details | "API rate limits" |

### Lifecycle stages

1. **Draft** — author writes article from template
2. **Review** — peer review for accuracy and clarity
3. **Publish** — add to GitHub Wiki
4. **Maintain** — review quarterly, update when product changes
5. **Retire** — archive when no longer applicable

## Escalation Paths

| Level | Who | When | Action |
|-------|-----|------|--------|
| L1 | Support agent | Initial contact | Triage, known-issue resolution, KB lookup |
| L2 | Senior support / domain expert | L1 cannot resolve within SLA | Deep investigation, log analysis |
| L3 | Engineering team | Bug confirmed or requires code change | Fix, deploy, verify |
| Executive | Leadership | Customer escalation, SLA breach, churn risk | Direct engagement, remediation plan |

## Feedback Synthesis

Turn support signals into product insights:

1. **Collect** — tag tickets with feature areas and pain points
2. **Aggregate** — weekly summary of top themes by volume and severity
3. **Analyse** — identify patterns, correlate with churn and NPS
4. **Report** — monthly feedback synthesis to product team
5. **Close loop** — update customers when their feedback drives changes

## Customer Health Scoring

### Health indicators

| Indicator | Weight | Green | Yellow | Red |
|-----------|--------|-------|--------|-----|
| Product usage (DAU/MAU) | 30% | > 60% | 30–60% | < 30% |
| Support ticket volume | 20% | Decreasing | Stable | Increasing |
| Feature adoption | 20% | Adopting new features | Stagnant | Declining usage |
| NPS / CSAT | 15% | > 8 | 6–8 | < 6 |
| Contract / payment | 15% | On time, expanding | On time | Late, at risk |

### Health score thresholds

| Score | Status | Action |
|-------|--------|--------|
| 80–100 | Healthy | Expansion opportunity — nurture and upsell |
| 60–79 | Neutral | Monitor — proactive check-in |
| 40–59 | At risk | Intervention — success plan, executive sponsor |
| 0–39 | Critical | Save plan — immediate outreach, escalate |

## QBR Process

Quarterly Business Reviews demonstrate value and align on goals:

1. **Prepare** (2 weeks before) — gather usage data, health score, open tickets, ROI metrics
2. **Agenda** — achievements, usage trends, roadmap preview, customer goals for next quarter
3. **Deliver** — present to customer stakeholders
4. **Follow up** — action items with owners and deadlines

## Onboarding Playbook

Standard onboarding phases:

| Phase | Duration | Activities | Success Criteria |
|-------|----------|-----------|-----------------|
| Kickoff | Week 1 | Welcome, introductions, access setup | Account provisioned |
| Configuration | Weeks 1–2 | Initial setup, integrations, data migration | System configured |
| Training | Weeks 2–3 | User training, admin training, documentation | Users trained |
| Go-live | Week 3–4 | Launch, monitor adoption, resolve blockers | Active usage |
| Handoff | Week 4+ | Transition to ongoing support, schedule first QBR | Health score > 60 |

## Tooling

| Tool | Purpose |
|------|---------|
| [GitHub Issues](https://docs.github.com/en/issues) | Ticket triage and tracking |
| [GitHub Wiki](https://docs.github.com/en/communities/documenting-your-project-with-wikis) | KB article publishing |
| [Xero](https://www.xero.com) | Customer revenue data for CS health scoring |

## Available Skills

### Support Skills

| Skill | Purpose |
|-------|---------|
| `/support:triage-tickets` | Triage and classify support tickets |
| `/support:feedback-synthesis` | Synthesise support feedback into insights |
| `/support:write-kb-article` | Write a knowledge base article |

### Customer Success Skills

| Skill | Purpose |
|-------|---------|
| `/customer-success:health-assessment` | Assess customer health |
| `/customer-success:churn-analysis` | Analyse churn risk |
| `/customer-success:expansion-plan` | Plan account expansion |
| `/customer-success:write-qbr` | Prepare a quarterly business review |
| `/customer-success:write-onboarding-playbook` | Write a customer onboarding playbook |

## Conventions

- Every support ticket is triaged within SLA response time
- KB articles are reviewed quarterly — stale articles are updated or retired
- Customer health scores are updated monthly
- QBRs are conducted for all customers on annual or multi-year contracts
- Feedback synthesis is shared with product team monthly
- Escalation playbooks are tested quarterly during tabletop exercises
- Churn risk triggers automatic CS intervention at "At Risk" threshold
```

#### File 2: `docs/support/escalation-playbook.md`

Create with this content:

```markdown
# Escalation Playbook — [Issue Type]

> Copy this template for each common escalation scenario.

## Metadata

| Field | Value |
|-------|-------|
| Issue type | |
| Priority | P1 / P2 / P3 |
| Last updated | YYYY-MM-DD |
| Owner | |

## Symptoms

<!-- How does this issue present? What does the customer report? -->

- Symptom 1
- Symptom 2

## Initial Response (L1)

1. Acknowledge the customer within SLA
2. Gather information:
   - Customer name and account
   - Steps to reproduce
   - Impact (how many users, what functionality)
   - Screenshots or error messages
3. Check known issues in GitHub Wiki
4. Attempt standard resolution:
   - [ ] Resolution step 1
   - [ ] Resolution step 2

## Escalation Trigger

Escalate to L2 if:
- L1 resolution steps fail
- Issue is not in known issues database
- Customer requests escalation
- SLA resolution deadline approaching

## L2 Investigation

1. Review full ticket history and customer context
2. Reproduce the issue in staging
3. Check application logs and metrics
4. Determine root cause or escalate to L3

## L3 Engineering Handoff

Provide to engineering:
- Reproduction steps (verified)
- Relevant log entries
- Customer impact assessment
- Suggested priority

## Communication Template

```
Subject: [Priority] Update on your issue — [Brief description]

Hi [Customer name],

Thank you for your patience. Here's an update on [issue summary]:

**Status:** [Investigating / Fix identified / Fix deployed]
**Next step:** [What happens next]
**Expected timeline:** [When they can expect resolution]

[Your name]
```

> Review and update this playbook after each use. Track resolution times for SLA reporting.
```

#### File 3: `docs/support/kb-article-template.md`

Create with this content:

```markdown
# [Article Title]

> Use a clear, searchable title. Prefix with article type: "How to:", "Fix:", "FAQ:", or "Reference:".

## Metadata

| Field | Value |
|-------|-------|
| Type | How-to / Troubleshooting / FAQ / Reference |
| Product area | |
| Created | YYYY-MM-DD |
| Last reviewed | YYYY-MM-DD |
| Author | |

## Summary

<!-- 1–2 sentence overview of what this article covers -->

## Prerequisites

<!-- What the reader needs before starting (access, permissions, versions) -->

- Prerequisite 1
- Prerequisite 2

## Instructions

<!-- Step-by-step instructions (for how-to) or diagnostic steps (for troubleshooting) -->

### Step 1: [Action]

<!-- Detailed instructions with screenshots if applicable -->

### Step 2: [Action]

<!-- Continue as needed -->

## Expected Result

<!-- What the reader should see when successful -->

## Troubleshooting

<!-- Common issues encountered while following this article -->

| Problem | Solution |
|---------|----------|
| | |

## Related Articles

<!-- Links to related KB articles -->

- [Related article 1]()
- [Related article 2]()

> Review this article quarterly. Update when the product changes. Retire when no longer applicable.
```

### Step 3: Return manifest

After creating/merging all files, output a summary:

```
## Support & Customer Success Bootstrap Complete

### Files created
- `docs/support/_sections/support.md` — support + CS fragment (coordinator assembles `docs/support/CLAUDE.md` from it)
- `docs/support/escalation-playbook.md` — escalation playbook template
- `docs/support/kb-article-template.md` — knowledge base article template

### Files merged
- (list any existing files where sections were appended)

### Next steps
- Create escalation playbooks for common issue types
- Set up GitHub Wiki for KB articles
- Configure customer health scoring using `/customer-success:health-assessment`
- Triage existing tickets using `/support:triage-tickets`
```
