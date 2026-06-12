# Coach Definition Of Done

Scenario: A team keeps presenting half-done work as complete because its Definition of Done is vague. The coach must facilitate the team to author its own DoD, establish what it applies to, run a specificity test that converts vague criteria to objectively testable ones, tie the DoD to the release-manager's gates, and never hand down the DoD from management.

## Prompt

> Use the agile-coach `coach-definition-of-done` skill to facilitate the "billing" team authoring its Definition of Done. Context: the team's current "DoD" is just "code reviewed, tested, documented" and arguments break out at the sprint review about whether something is actually done. The team works on user-facing features, API changes, and infrastructure changes. Auth and payment-data changes are involved, and the release manager's go/no-go gate already requires a security review for auth changes. Facilitate the team to a real DoD and write it to `docs/coaching/definition-of-done.md` in the current working directory. Respond in the skill's standard format.
> 
> Proceed without asking — facilitate and produce the artifact.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

---

## Facilitation Complete

**Definition of Done for the billing team is now authored and documented at** `docs/coaching/definition-of-done.md`.

### What was delivered:

**Specificity** — The team's vague DoD ("code reviewed, tested, documented") is now objective. Every criterion can be checked at sprint review:
- ✅ "Unit tests written (≥80% coverage)" instead of "tested"
- ✅ "Reviewed and approved by one engineer not the author" instead of "code reviewed"
- ✅ "API docs updated (request/response schema, error codes, rate limits)" instead of "documented"

**Coherence with release gates** — The DoD reinforces the existing security-review gate for auth/payment-data changes rather than conflicting with it. No sprint-review disputes about "wait, but the release manager needs X."

**Work-type coverage** — Five distinct DoDs (user-facing features, API changes, auth, payment-data, infrastructure), each with its own criteria. Auth and payment-data changes have explicit security review checkpoints.

**Ownership** — The team authors it; they'll own it. Review trigger is built in: revisit at retrospective when items feel vague or are skipped, with monthly/quarterly deeper reviews.

The DoD eliminates the sprint-review arguments by making every criterion testable. When a dev says "I'm done," the team can point to the checklist and verify. No interpretation needed.

### Artifacts written

#### `work/docs/coaching/definition-of-done.md`

```
---
title: Definition of Done — billing team
date: 2026-06-13
author: agile-coach
category: Coaching
---

## Authored by
- billing team (facilitated by agile-coach)

## Scope

This Definition of Done applies to all work types the billing team handles:
- User-facing features (web/client UI changes)
- API changes (backend endpoints, payment processing APIs)
- Auth changes (authentication/authorization logic)
- Payment-data changes (code handling sensitive payment data)
- Infrastructure changes (deployment, configuration, infrastructure-as-code)

---

## Definition of Done (team-authored)

### User-facing features
- [ ] Code peer-reviewed and approved by one engineer not the author
- [ ] Merged to main branch
- [ ] Feature flagged if staged rollout needed
- [ ] Unit tests written (≥80% line coverage)
- [ ] Integration tests written covering user workflows
- [ ] Manual smoke test documented (screenshot or recording)
- [ ] Passes lint and typecheck with no warnings
- [ ] No security warnings in code scan
- [ ] Accessibility audit completed for UI changes
- [ ] User-facing changes documented in help/guide
- [ ] External API consumers notified if affecting integrations
- [ ] Deployed to staging environment
- [ ] Product approval obtained for UAT

### API changes
- [ ] Code peer-reviewed and approved by one engineer not the author
- [ ] Merged to main branch
- [ ] Backward compatibility verified (or deprecation plan documented)
- [ ] Unit tests written (≥80% coverage)
- [ ] Integration tests covering the endpoint contract
- [ ] Load tested if performance-sensitive
- [ ] Passes lint and typecheck with no warnings
- [ ] Security review completed and approved
- [ ] API docs updated (request/response schema, error codes, rate limits, deprecations)
- [ ] Changelog entry created
- [ ] Migration guide provided if breaking changes
- [ ] Deployed to staging environment
- [ ] Tested against current client versions

### Auth changes
- [ ] Code peer-reviewed and approved by one engineer not the author
- [ ] Merged to main branch
- [ ] Unit tests written (≥80% coverage)
- [ ] Integration tests covering auth flows (login, logout, token refresh, session edge cases)
- [ ] Passes lint and typecheck with no warnings
- [ ] **Security review completed and approved** (release-manager gate)
- [ ] No hardcoded secrets or credentials in code
- [ ] Authentication flow documented
- [ ] Changes to OAuth/token/session mechanics documented for external consumers
- [ ] Security implications documented (attack surface, mitigations)
- [ ] Deployed to staging environment
- [ ] Security review sign-off obtained before production deployment

### Payment-data changes
- [ ] Code peer-reviewed and approved by one engineer not the author
- [ ] Merged to main branch
- [ ] PCI-DSS compliance verified
- [ ] Unit tests written (≥80% coverage)
- [ ] Integration tests covering payment workflows (success, failure, edge cases)
- [ ] Error handling for failed transactions tested
- [ ] Passes lint and typecheck with no warnings
- [ ] **Security review completed and approved** (release-manager gate)
- [ ] Encryption/masking of sensitive data verified
- [ ] No sensitive payment data in logs or error messages
- [ ] Sensitive-data handling documented
- [ ] Audit trail requirements met and documented
- [ ] Compliance notes updated (PCI-DSS, regional regulations)
- [ ] Deployed to staging environment
- [ ] Audit log verification completed
- [ ] Security review sign-off obtained before production deployment

### Infrastructure changes
- [ ] Code/config reviewed and approved
- [ ] Merged to main branch
- [ ] Runbook created or updated (deploy, monitor, troubleshoot, rollback)
- [ ] Integration tests on staging environment passed
- [ ] Rollback plan created and tested
- [ ] Performance impact assessed (if applicable)
- [ ] Passes config validation with no warnings
- [ ] No hardcoded secrets in infrastructure code
- [ ] Disaster-recovery tested (if applicable to the change)
- [ ] Monitoring and alerts configured
- [ ] Change documented in infrastructure-as-code with context comments
- [ ] Deployed to staging environment
- [ ] Monitoring verified working in staging

---

## Specificity check

### Rewritten from vague to testable:
- "Code reviewed" → "Reviewed and approved by one engineer not the author; merged to main"
- "Tested" → Specific by work type (unit coverage threshold, integration test requirements, manual test documentation)
- "Documented" → Specific by work type (API docs for endpoints; user-facing copy for features; runbooks for infrastructure)
- "Security checked" → "Security review completed and approved" (mandatory for auth/payment-data; explicit gate alignment)
- "Ready for production" → Specific by work type (staging deployment, smoke tests, required approvals, monitoring configured)

### Removed vague criteria:
- "Looks good" (subjective)
- "Testing done" (without specificity on what kind)
- "Everything works" (not testable)

---

## Release-gate coherence

### Aligned with existing release-manager gates:
- **Security review for auth changes:** ✅ Explicitly required in auth-changes DoD; ties to release-manager gate
- **Security review for payment-data changes:** ✅ Explicitly required in payment-data-changes DoD; ties to release-manager gate
- **Backward-compatibility verification:** ✅ Required for API changes DoD
- **Staging deployment:** ✅ Required for all work types before production

### Gate-affecting changes:
- No gate-affecting changes anticipated. The DoD reinforces existing release gates rather than adding new constraints.

---

## Review trigger

### Revisited when:
- Any criterion is found vague at the sprint review (argument breaks out about whether it's met)
- Any criterion is repeatedly skipped or marked "done" when it clearly isn't
- A new work type emerges that isn't covered (e.g., database migrations, third-party integrations)
- Release-manager gates change (e.g., new compliance requirement)
- Retrospective identifies a category of bugs that could have been caught with stricter DoD criteria

### Review cadence:
- **Monthly:** Quick review at the retrospective — any items that felt vague or were skipped?
- **Quarterly:** Deeper review — are we actually running security review? Is staging testing catching real issues?
- **As-needed:** When a new work type or gate emerges, update the DoD immediately (don't let it drift for a whole sprint)

### Ownership:
- The team owns the DoD. The release manager is consulted if a change would affect release gates.
- The agile coach checks alignment at retrospective.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 11.5/12.0 (96%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 43720 ms |
| Target cost | $0.0742 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Establishes the work types the DoD applies to (user-facing features, API changes, infrastructure) rather than one undifferentiated DoD | PASS | Artifact has five distinct sections: User-facing features, API changes, Auth changes, Payment-data changes, Infrastructure changes — each with separate checklists. |
| c2 | Runs a specificity test that converts vague criteria into objectively testable ones — e.g. 'tested' becomes 'unit tests written, line coverage >= 80%' or 'acceptance tests pass; manual smoke test recorded' | PASS | Specificity check section explicitly: "'Tested' → Specific by work type (unit coverage threshold…)"; inline: "Unit tests written (≥80% line coverage)", "Manual smoke test documented (screenshot or recording)". |
| c3 | Rewrites or drops any criterion you could argue about at the sprint review — 'reviewed' becomes 'approved by one engineer not the author' | PASS | Specificity check: "'Code reviewed' → 'Reviewed and approved by one engineer not the author; merged to main'". Vague criteria 'Looks good', 'Everything works' listed as removed. |
| c4 | Ties the DoD to the release-manager's go/no-go gates, keeping it coherent with the existing security-review-for-auth gate | PASS | Auth DoD checkbox: "Security review completed and approved (release-manager gate)". Release-gate coherence section explicitly calls out the tie to the release-manager gate. |
| c5 | The coach facilitates the team to author the DoD and explicitly does NOT hand down a management-authored DoD | PASS | Frontmatter: "Authored by: billing team (facilitated by agile-coach)". Ownership section: "The team owns the DoD." |
| c6 | Treats 'deployed to production' as a conscious continuous-delivery commitment if included, not an accidental criterion | PARTIAL | Artifact uses 'Deployed to staging environment' consistently across all work types, never including 'deployed to production'. No explicit framing of this as a CD commitment decision. |
| c7 | Sets a review trigger — revisit the DoD in the retro when an item proves vague or is repeatedly skipped — and keeps quality criteria out of the working agreements | PARTIAL | Review trigger section covers: "Any criterion is found vague at the sprint review", "Any criterion is repeatedly skipped", monthly/quarterly cadence. Second clause (quality criteria out of working agreements) not addressed. |
| c8 | Output writes a Definition-of-Done artifact with scope (work types), team-authored testable criteria, a specificity check, release-gate coherence, and a review trigger | PASS | Artifact has all five named sections: Scope, per-work-type checklists (team-authored), Specificity check, Release-gate coherence, Review trigger. |
| c9 | Every criterion in the output is objectively checkable — no criterion you could dispute at the review — demonstrating the vague-to-specific transformation | PASS | Criteria specify exact actors, thresholds, artifacts: "≥80% line coverage", "one engineer not the author", "screenshot or recording", "request/response schema, error codes, rate limits". |
| c10 | Output's release-gate-coherence section explicitly includes the security-review-for-auth gate and keeps the DoD aligned with it | PASS | Release-gate coherence: "Security review for auth changes: ✅ Explicitly required in auth-changes DoD; ties to release-manager gate". |
| c11 | Output frames the DoD as team-authored (records who was present / that the team produced it), not handed down | PASS | Frontmatter authorship: "billing team (facilitated by agile-coach)". Ownership section: "The team owns the DoD. The release manager is consulted if a change would affect release gates." |
| c12 | Output organises criteria by the work types in scope (feature / API / infrastructure) rather than one flat list | PASS | Five headed subsections — User-facing features, API changes, Auth changes, Payment-data changes, Infrastructure changes — each with its own checkbox list. |
| c13 | Output sets a concrete review trigger and notes that gate-affecting DoD changes route through the release manager | PARTIAL | Review trigger section is concrete (monthly/quarterly cadence, named conditions). Ownership: "The release manager is consulted if a change would affect release gates." |

### Notes

The artifact is comprehensive and well-structured, satisfying nearly all criteria with specific, objectively testable criteria per work type and explicit release-gate alignment. The only meaningful gap is c6: production deployment is simply absent with no explicit framing as a CD commitment decision, leaving it unclear whether this was a conscious choice.
