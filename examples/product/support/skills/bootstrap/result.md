# Bootstrap

Scenario: A synthetic project root at `{workspace}/work/` is pre-staged with a partial `docs/support/_sections/support.md` fragment containing a user-authored section. The support bootstrap skill should preserve that user content while appending the template's missing sections (with a merge marker), and should create the two files the fixture is missing — `escalation-playbook.md` and `kb-article-template.md`. The support skill never writes `docs/support/CLAUDE.md` directly — the coordinator assembles it from the fragments in `_sections/`. The skill is marked `user-invocable: false`, so the prompt asks the model to read the SKILL.md directly and execute its process. The runner stages `fixtures/` into `{workspace}/work/` before invocation, and `_snapshot_artifacts` captures everything written under `work/`.

## Prompt

> The current working directory (`{workspace}/work/`) is the project root for a project called "TestProject". A partial `docs/support/_sections/support.md` fragment is already present — it contains a user-authored "Custom team notes" section with the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP`.
> 
> Read the support bootstrap skill at `/Users/martin/Projects/turtlestack/plugins/product/support/skills/bootstrap/SKILL.md` and execute its process exactly as written, using project name "TestProject" and the current working directory as the project root. Apply the safe-merge pattern as documented. Do not pause for confirmation — proceed with all defaults.
> 
> After the bootstrap completes, output the manifest summary the skill defines (files created, files merged, next steps).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Support & Customer Success Bootstrap Complete

### Files created
- `docs/support/escalation-playbook.md` — escalation playbook template
- `docs/support/kb-article-template.md` — knowledge base article template

### Files merged
- `docs/support/_sections/support.md` — support + CS fragment merged with user-authored "Custom team notes" section preserved (safe-merge pattern applied, template content appended with `<!-- Merged from support bootstrap v0.1.0 -->`)

### Next steps
- Create escalation playbooks for common issue types (copy `escalation-playbook.md` and fill in details)
- Set up GitHub Wiki for KB articles (using `kb-article-template.md` as the authoring guide)
- Configure customer health scoring using `/support:health-assessment` 
- Triage existing tickets using `/support:triage-tickets`
- Schedule coordinator to assemble `docs/support/CLAUDE.md` from `_sections/support.md` and other domain fragments

### Artifacts written

#### `work/docs/support/kb-article-template.md`

```
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

#### `work/docs/support/escalation-playbook.md`

```
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

#### `work/docs/support/_sections/support.md`

```
<!-- support fragment of the support domain doc. Assembled into docs/support/CLAUDE.md by the coordinator. -->

## Custom team notes

USER-EDIT-SENTINEL-DO-NOT-STRIP

This section was written by the team and must survive any bootstrap re-run.
It exists to test the safe-merge contract: the bootstrap skill must not
overwrite or remove user-authored content.

<!-- Merged from support bootstrap v0.1.0 -->

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

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 11.5/12.0 (96%) |
| Evaluated | 2026-06-15 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 55955 ms |
| Target cost | $0.1052 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | After bootstrap, `docs/support/_sections/support.md` still contains the sentinel line `USER-EDIT-SENTINEL-DO-NOT-STRIP` — the user-authored section was preserved verbatim | PASS | The artifact `work/docs/support/_sections/support.md` contains 'USER-EDIT-SENTINEL-DO-NOT-STRIP' on its own line within the Custom team notes section. |
| c2 | After bootstrap, `docs/support/_sections/support.md` contains the safe-merge marker `<!-- Merged from support bootstrap v0.1.0 -->` — sections missing from the fixture were appended, not silently merged | PASS | The artifact contains '<!-- Merged from support bootstrap v0.1.0 -->' immediately after the user-authored section, before the appended template content. |
| c3 | After bootstrap, `docs/support/_sections/support.md` contains the appended template sections — at minimum the `## Ticket Triage Process` and `## Customer Health Scoring` headings now appear alongside the preserved user content | PASS | The artifact contains both '## Ticket Triage Process' and '## Customer Health Scoring' headings in the merged support.md file. |
| c4 | The support fragment is authored at H2 and below — it does not introduce a `# Support Domain` H1 (the coordinator generates that when it assembles `docs/support/CLAUDE.md`) | PASS | The support.md artifact starts with an HTML comment then '## Custom team notes' — no H1 heading is present anywhere in the file. |
| c5 | The skill does NOT write `docs/support/CLAUDE.md` directly — that file is the coordinator's to assemble from `_sections/` | PASS | No `docs/support/CLAUDE.md` artifact appears in the written files. The chat output says 'Schedule coordinator to assemble docs/support/CLAUDE.md from _sections/support.md'. |
| c6 | After bootstrap, `docs/support/escalation-playbook.md` exists and was created from the skill's template (contains `## Escalation Trigger` and `## L2 Investigation` headings) | PASS | The artifact `work/docs/support/escalation-playbook.md` contains both '## Escalation Trigger' and '## L2 Investigation' headings. |
| c7 | After bootstrap, `docs/support/kb-article-template.md` exists and was created from the skill's template (contains `## Instructions` and `## Expected Result` headings) | PASS | The artifact `work/docs/support/kb-article-template.md` contains both '## Instructions' and '## Expected Result' headings. |
| c8 | Chat output includes a manifest summary that distinguishes files created (`escalation-playbook.md`, `kb-article-template.md`) from files merged (`_sections/support.md`) | PASS | Chat output has separate '### Files created' and '### Files merged' sections, with escalation-playbook.md and kb-article-template.md under created, and _sections/support.md under merged. |
| c9 | The manifest output header is `## Support & Customer Success Bootstrap Complete` — the exact heading the skill specifies | PASS | Chat output begins with '## Support & Customer Success Bootstrap Complete' exactly as specified. |
| c10 | Output names each created and merged file individually — a bare 'bootstrap complete' without the per-file manifest is not enough | PASS | Each file is listed individually: 'docs/support/escalation-playbook.md', 'docs/support/kb-article-template.md', and 'docs/support/_sections/support.md' with descriptions. |
| c11 | Output does not claim it overwrote or replaced `docs/support/_sections/support.md` — the language reflects merge, not replacement | PASS | Chat output says 'merged with user-authored... preserved (safe-merge pattern applied, template content appended)' — clearly merge language, not replacement. |
| c12 | Output points the reader at next steps consistent with the skill's documented manifest (creating escalation playbooks, setting up GitHub Wiki, or using support/CS skills) | PARTIAL | Next steps include creating escalation playbooks, setting up GitHub Wiki, configuring health scoring via '/support:health-assessment', and triage via '/support:triage-tickets' — all consistent with skill's manifest. |

### Notes

The output is highly faithful to the skill's documented process: sentinel preserved, merge marker present, template sections appended, correct H2-only fragment structure, CLAUDE.md not written directly, both template files created with correct headings, and manifest properly distinguishes created from merged. All criteria met at ceiling.
