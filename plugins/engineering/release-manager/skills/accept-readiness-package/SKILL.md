---
name: accept-readiness-package
description: "Accept and gate the delivery-manager's release-readiness package — validate it is complete (support briefed, GTM aligned, ops runbook drafted, governance approvals on file, customer comms planned), map each coordination item to a release-plan readiness gate, run the readiness assessment over the combined engineering + coordination picture, and produce a go/no-go input with explicit blockers. Use when a delivery-manager hands a release-readiness package to the release-manager. This is the formal entry of coordination into the release gates; a missing package item is a no-go, not a warning."
argument-hint: "[release name or version, and the release-readiness package from the delivery-manager]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Accept readiness package

Accept the delivery-manager's release-readiness package for $ARGUMENTS and run it through the release-manager's gates. This skill is the receiving half of a two-part hand-off. Upstream, the delivery-manager shepherds the organisational readiness — support briefed, GTM aligned, ops runbook drafted, governance approvals on file, customer comms planned — and assembles a release-readiness package (their `/delivery-manager:coordinate-release-readiness` skill). This skill ingests that package, validates it, maps it to the release-plan readiness gates, and feeds a gated go/no-go input.

The boundary is the point. The delivery-manager coordinates readiness; the release-manager gates. The delivery-manager cannot wave a release through — handing over a package is a request for assessment, not an approval. You own the gate decision. A package that arrives with open items is a no-go, returned to sender with the specific gaps named, not a release that ships on trust.

## Step 1: Receive and validate the package is complete

Read the package the delivery-manager handed over. It should carry six coordination items, each with a status, evidence, and owner:

| Coordination item | Expected evidence | Upstream owner |
|---|---|---|
| Support briefed | FAQ, known issues, escalation paths, briefing date | Support |
| GTM aligned | Launch plan, agreed timing, no clash with deploy window | GTM |
| Ops runbook drafted | Runbook link for the new behaviour, ops has seen it | DevOps / ops |
| Governance approvals | Sign-off references (security, legal, compliance, change board) | GRC Lead / relevant board |
| Customer comms planned | Comms plan: what, which channel, when relative to deploy | GTM / product |
| Gating dependencies cleared | RAID IDs, all On track or resolved | Delivery-manager |

Validate, do not assume. For each item, confirm the package actually carries evidence — a link, a date, a reference — not a bare "Confirmed". An item marked confirmed with no evidence is an unconfirmed item.

**If any item is missing, has no evidence, or is marked open:** stop. Return the package to the delivery-manager (return-to-sender) with the specific gaps named — which item, what is missing, what evidence is needed to close it. Do not proceed to the assessment. A package with open items is not a package you can gate.

Produce a validation result: package complete (proceed) or returned-to-sender (with the named gaps).

## Step 2: Map each coordination item to a release-plan readiness gate

The release-plan readiness assessment (the `/release-manager:release-plan` skill, Step 2) checks engineering, operational, and communication gates. The delivery-manager's coordination items feed the operational and communication gates. Map them explicitly so nothing is double-counted and nothing falls through:

| DM coordination item | Maps to release-plan gate | Gate category |
|---|---|---|
| Support briefed | Support team briefed (FAQ, known issues, escalation paths) | Operational |
| Ops runbook drafted | Monitoring and alerts in place / runbook ready | Operational |
| Customer comms planned | Customer communication prepared | Communication |
| GTM aligned | GTM team notified (launch activities) | Communication |
| Governance approvals | Security review / sign-offs on file (where applicable) | Operational / governance |
| Gating dependencies cleared | No blocking dependency in a known-bad state | Operational |

The coordination items do not cover the engineering gates. Definition of Done, verification tests pass in staging, no open critical bugs, migrations tested, performance benchmarks — those remain the release-manager's to assess directly. The package fills the operational and communication columns; you fill the engineering column yourself.

Record the mapping so the go/no-go input shows which gate each coordination item satisfied, and which gates the package did not touch.

## Step 3: Run the release-plan readiness assessment over the combined picture

Run the full release-plan readiness assessment (`/release-manager:release-plan`, Step 2) across both halves:

1. **Engineering gates** — assess directly from your own evidence (test output, review comments, migration logs, benchmark results). The package does not cover these.
2. **Operational and communication gates** — assess from the validated package evidence mapped in Step 2.

Check each gate against actual evidence, not against the fact that someone claimed it. A gate without evidence is a gate that has not passed. If a gate is genuinely not applicable (no migrations this release, no user-facing change so no customer comms), mark it N/A with the reason.

The combined picture is the release-plan readiness table with every gate filled: engineering from your assessment, operational and communication from the package. No empty cells — every gate is PASS, FAIL, or N/A with evidence or reason.

## Step 4: Produce the go/no-go input with explicit blockers

Produce the gated go/no-go input. This is not the deployment and not the final release sign-off ceremony — it is the readiness verdict that the release-plan go/no-go decision consumes.

- **GO input:** every engineering, operational, and communication gate passes with evidence (or is N/A with reason). The package was complete and mapped clean.
- **NO-GO input:** any engineering gate fails, OR the package was returned-to-sender, OR any operational/communication gate the package was meant to satisfy has no evidence. List every blocker with its owner and the action to clear it.
- **CONDITIONAL GO input:** a non-engineering gate carries a known, documented, acceptable risk — escalate to the CTO for approval before this becomes a go. Engineering gate failures are never conditionally acceptable. A missing package item is never a conditional go; it is a no-go until the delivery-manager closes it.

The delivery-manager's hand-off does not lower the bar. If the package is thin, the verdict is no-go and the gap goes back to the delivery-manager to close, then re-hand.

## Rules

- You own the gate decision. The delivery-manager coordinates readiness and hands over a package; handing over is a request for assessment, not an approval. The delivery-manager cannot wave a release through.
- A missing or evidence-free package item is a no-go, not a warning. Don't downgrade a gap to "minor" to keep the release moving — return the package to sender with the specific gap named.
- Validate evidence, never assume. "Support briefed: Confirmed" with no briefing doc or date is unconfirmed. Treat a bare status as an open item.
- Don't re-coordinate the package yourself. If support is not briefed, that is the delivery-manager's gap to close — return it, don't quietly brief support and proceed. Re-coordinating blurs the boundary the hand-off exists to keep sharp.
- Don't let the package substitute for the engineering gates. Tests, migrations, performance, and the security review of the change itself are yours to assess directly — the package does not cover them and a complete package does not make them pass.
- Map every coordination item to exactly one gate. Don't double-count a single item across two gates to make the table look fuller, and don't leave a gate the package was meant to satisfy unmapped.
- Record the return-to-sender. If you reject a package, the rejection, the named gaps, and the date are recorded so the re-hand is traceable. A verbal "it's not ready" leaves no audit trail.

## Output Format

```markdown
## Readiness Package Acceptance: [release name / version]

### Package Validation
- Source: delivery-manager (`coordinate-release-readiness`)
- Received: [date]
- Result: Complete / Returned-to-sender

| Coordination item | Evidence present | Status |
|---|---|---|
| Support briefed | [link/date or MISSING] | OK / Gap |
| GTM aligned | [link or MISSING] | OK / Gap |
| Ops runbook | [link or MISSING] | OK / Gap |
| Governance approvals | [refs or MISSING] | OK / Gap |
| Customer comms planned | [plan or MISSING] | OK / Gap |
| Gating dependencies | [RAID IDs or MISSING] | OK / Gap |

Named gaps (if returned-to-sender): [item — what is missing — evidence needed — owner]

### Gate Mapping + Combined Assessment
| Gate | Category | Source | Status | Evidence |
|---|---|---|---|---|
| Definition of Done | Engineering | RM direct | PASS/FAIL | [evidence] |
| Verification tests (staging) | Engineering | RM direct | PASS/FAIL | [command + exit code] |
| No open critical/high bugs | Engineering | RM direct | PASS/FAIL | [tracker] |
| Migrations tested | Engineering | RM direct | PASS/FAIL/N-A | [staging log] |
| Performance baseline | Engineering | RM direct | PASS/FAIL/N-A | [benchmark] |
| Support briefed | Operational | DM package | PASS/FAIL | [briefing doc + date] |
| Ops runbook / monitoring | Operational | DM package | PASS/FAIL | [runbook link] |
| Governance sign-offs | Operational | DM package | PASS/FAIL/N-A | [sign-off refs] |
| Gating dependencies clear | Operational | DM package | PASS/FAIL | [RAID IDs] |
| Customer comms prepared | Communication | DM package | PASS/FAIL/N-A | [comms plan] |
| GTM notified | Communication | DM package | PASS/FAIL/N-A | [launch plan] |

### Go/No-Go Input: [GO / NO-GO / CONDITIONAL GO]
Reasoning: [why, citing gate results and package validation]

Blockers (if any):
| Blocker | Gate | Owner | Action to clear |
|---|---|---|---|
| [description] | [gate] | [owner] | [action] |

Next: feed this input to `/release-manager:release-plan` Step 6 for the go/no-go decision. If returned-to-sender, the delivery-manager closes the named gaps and re-hands.
```

## Related skills

- `/delivery-manager:coordinate-release-readiness` — the upstream producer. The delivery-manager assembles the release-readiness package this skill ingests. This skill is the receiving, gating half of that hand-off.
- `/release-manager:release-plan` — the genuine workflow dependency. This skill runs the package through the release-plan readiness assessment (Step 2) and feeds its go/no-go decision (Step 6). The combined assessment here is the engineering + coordination input to that plan.
