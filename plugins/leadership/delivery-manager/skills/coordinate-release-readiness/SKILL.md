---
name: coordinate-release-readiness
description: "Coordinate the upstream pieces a release needs before the release-manager's gates — support briefed, GTM aligned, ops runbook drafted, governance approvals lined up, customer comms planned. Assembles a release-readiness package and hands it to the release-manager. Use ahead of a release to get the team ready to be ready; this does NOT execute the release or own the engineering gates."
argument-hint: "[release name or version being prepared]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Coordinate release readiness

Coordinate release readiness for $ARGUMENTS. This skill sits upstream of the release-manager's gates. The delivery-manager coordinates getting ready to be ready — the cross-team and organisational pieces that must be in place before a release can be assessed. The release-manager owns the engineering gates, deployment strategy, and rollback. The output of this skill is a release-readiness package that is handed to the release-manager; it is not a go/no-go decision and it is not a deployment.

The boundary matters. You confirm support is briefed and governance approvals are on file; the release-manager confirms tests pass and the rollback works. Do not absorb the engineering gates, and do not let the release-manager's gates substitute for the coordination this skill covers.

## Step 1: Confirm the release scope with the owners

Read the release scope from the product-owner and the release-manager's release plan if one exists. You are coordinating readiness for a defined scope, not deciding what ships. Confirm the scope is stable before coordinating around it — coordinating readiness for a moving target wastes the effort.

## Step 2: Work the readiness checklist

Coordinate each upstream piece. For each, your job is to confirm it is genuinely in place, with evidence — not to assume someone did it.

| Readiness item | Confirm | Owner |
|---|---|---|
| Support briefed | FAQ, known issues, escalation paths handed to support ahead of release | Support |
| GTM aligned | Launch timing agreed, announcements drafted, no clash with the deployment window | GTM |
| Ops runbook drafted | Runbook for the new behaviour exists and ops has seen it | DevOps / ops |
| Governance approvals | Any required sign-offs (security, legal, compliance, change board) on file | GRC Lead / relevant board |
| Customer comms planned | What customers are told, by which channel, and when relative to deployment | GTM / product |
| Dependencies cleared | Any RAID dependencies that gate this release are On track or resolved | Delivery-manager |

Support is briefed before deployment, never after. Customer comms go out after the release is verified stable, never before — but the plan is prepared now.

## Step 3: Chase the gaps

Any item not in place is a gap. Coordinate to close it: name the owner, name the action, name the date. An item you cannot close before the release window is a blocker — raise it in the RAID log and the status report, and flag it to the release-manager. Do not present a package with open items as complete (decision checkpoint).

## Step 4: Assemble the release-readiness package

When the checklist is complete, assemble the package:

```markdown
## Release-Readiness Package: [release name / version]

| Readiness item | Status | Evidence | Owner |
|---|---|---|---|
| Support briefed | Confirmed | [briefing doc + date] | Support |
| GTM aligned | Confirmed | [launch plan link] | GTM |
| Ops runbook | Confirmed | [runbook link] | DevOps |
| Governance approvals | Confirmed | [sign-off references] | GRC Lead |
| Customer comms planned | Confirmed | [comms plan link] | GTM |
| Gating dependencies | Cleared | [RAID IDs] | Delivery-manager |

Open items: [none / list with owner and date]
```

## Step 5: Hand off to the release-manager

Pass the package to the release-manager, who runs it through the release-plan readiness assessment and owns the go/no-go. Your coordination role ends at the hand-off. Record the hand-off date. If the release-manager finds the package incomplete, that is your gap to close — take it back, close the item, re-hand.

## Rules

- Coordinate readiness; never execute the release. The deployment, the gates, the rollback are the release-manager's.
- Confirm each item with evidence, not assumption. "I think support knows" is not "support is briefed".
- Support is briefed before deployment. Customer comms are planned now but go out only after the release is verified stable.
- Never hand over a package with open items presented as complete. An incomplete package presented as ready compounds release risk.
- Gating dependencies must be cleared in the RAID log before the package is complete — a release that ships on an at-risk dependency inherits that risk.
- Don't duplicate the release-manager's engineering gates here. Tests, performance, migrations, security review of the change itself — those are theirs.

## Output Format

The release-readiness package from Step 4, plus a hand-off note:

```markdown
## Release-Readiness Hand-off: [release] → release-manager

- Package status: Complete / Incomplete
- Open items: [none / list]
- Handed to release-manager: [date]
- Next: release-manager runs release-plan readiness assessment and owns go/no-go
```

## Related skills

- `/delivery-manager:write-dependency-map` — the gating dependencies this package depends on are tracked here. A release cannot be ready while a gating dependency is at risk or blocked.
- `/delivery-manager:write-status-report` — any open readiness item that cannot be closed before the release window is raised as a risk in the weekly status.
- `/release-manager:release-plan` — the downstream owner. The release-manager runs this package through its readiness assessment and owns the go/no-go. Your role ends at the hand-off.
