# Coach Refinement

Scenario: A product owner runs a live refinement event over a groomed candidate queue for a 5-developer two-week sprint. The queue contains a clean story, an over-large story that must be split by behaviour, a story that depends on the over-large one, a story with a non-atomic acceptance criterion and an external legal blocker, and a second clean story. The skill must set a 10% capacity budget, INVEST-check each item, surface dependencies, gate against the Definition of Ready, and produce a clean Ready / back-to-refinement / Blocked split.

## Prompt

> The groomed candidate queue for the Sprint 14 refinement event is on disk at `{workspace}/work/groomed-queue.md`. Read it.
> 
> /product-owner:coach-refinement {workspace}/work/groomed-queue.md
> 
> Run the full refinement event. Set the capacity budget first (the team is 5 developers on a two-week sprint), INVEST-check every candidate, surface dependencies, run the Definition of Ready gate on each, and produce the event summary using the skill's Output Format. Write the summary back to the backlog file at the path above and reply with that path.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Refinement event complete. Summary written to:

**`/private/var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/eval-1781284036-22a2ce8c/work/groomed-queue.md`**

### Event outcome:

**Ready for planning (8 points):**
- User can reset their password via email link (3 pts)
- User can enable TOTP two-factor authentication (5 pts)

**Returned to refinement:**
- Account settings overhaul — split into 5 behaviour-based child stories (failed Small and Estimable as a single item)

**Blocked:**
- Show last-login timestamp — sequencing dependency (waits on Account settings security tab)
- Export account data to PDF — legal sign-off required on field list scope (external blocker, GRC/Legal owner)

**Capacity:** 8 of 50 points Ready; 42 points remain for the sprint. The team has headroom for additional work if Item 2's child stories are refined and prioritized before sprint planning.

### Artifacts written

#### `work/groomed-queue.md`

```
# Refinement Event — Sprint 14 (2026-06-13)

## Capacity budget
- Team sprint capacity: 5 developers × 10 days = 50 developer-days (~400 hours)
- Refinement budget (~10%): ~40 hours total for sprint
- This event: 3 hours allocated
- Items in scope: 5 candidates

## Item results

| Item | INVEST | Dependencies | DoR | Outcome |
|------|--------|--------------|-----|---------|
| Password reset via email link | ✅✅✅✅✅✅ | None | 6/6 | **Ready** |
| Account settings overhaul | ✅✅✅❌❌✅ | None identified | 4/6 | **Back to refinement** — split by behaviour (fails Small, Estimable) |
| Show last-login timestamp | ✅✅✅✅✅✅ | depends on Item 2 | — | **Blocked** — sequencing (security tab prerequisite) |
| Export account data to PDF | ✅✅✅❌✅❌ | external | 3/6 | **Blocked** — legal sign-off on field list required |
| TOTP 2FA | ✅✅✅✅✅✅ | None | 6/6 | **Ready** |

## INVEST detail by item

### Item 1: User can reset their password via email link (3 points)

| Criterion | Result | Reason |
|-----------|--------|--------|
| **I**ndependent | ✅ | No dependencies on other work |
| **N**egotiable | ✅ | Approach is open — email provider, link format, backend implementation flexible |
| **V**aluable | ✅ | Delivers user-visible value independently — users regain account access |
| **E**stimable | ✅ | Team estimated 3 points confidently; groom pass included 3 amigos review |
| **S**mall | ✅ | 3 points fits comfortably in 50-point sprint |
| **T**estable | ✅ | Clear, atomic acceptance criteria |

**Gate result: READY FOR PLANNING** (all DoR boxes checked)

---

### Item 2: Account settings overhaul (20+ points)

| Criterion | Result | Reason |
|-----------|--------|--------|
| **I**ndependent | ✅ | No blocking dependencies |
| **N**egotiable | ✅ | Approach open |
| **V**aluable | ✅ | Delivers user-visible value |
| **E**stimable | ❌ | "maybe 20+ points, hard to say" — uncertainty too high; team cannot commit with confidence |
| **S**mall | ❌ | 20+ points exceeds sprint capacity; groom pass flagged as "likely too large for one sprint" |
| **T**estable | ⚠️ | Five separate concerns bundled into one story makes acceptance criteria unwieldy |

**Gate result: BACK TO REFINEMENT — split by behaviour required**

**Proposed child stories (to refine separately):**
1. **User can manage profile information** — update name, email, avatar, timezone
2. **User can configure notification preferences** — digest frequency, notification channels
3. **User can manage connected apps** — view, revoke, re-auth
4. **User can view and update billing details** — payment method, billing address, invoice history
5. **User can view and manage security settings** — password, 2FA, last login, active sessions

Each child re-enters INVEST and DoR in follow-up refinement event.

---

### Item 3: Show last-login timestamp on the security tab (2 points)

| Criterion | Result | Reason |
|-----------|--------|--------|
| **I**ndependent | ❌ | **Hard prerequisite on Item 2's security tab** — cannot start until security tab is built |
| **N**egotiable | ✅ | Implementation approach is open |
| **V**aluable | ✅ | Delivers value once security tab exists |
| **E**stimable | ✅ | 2 points, clear scope |
| **S**mall | ✅ | 2 points fits |
| **T**estable | ✅ | Clear acceptance criteria |

**Gate result: BLOCKED — sequencing dependency**

**Escalation:** Move to next refinement event once Item 2's security-tab child story is Ready.

---

### Item 4: Export account data to PDF for compliance requests (5 points)

| Criterion | Result | Reason |
|-----------|--------|--------|
| **I**ndependent | ✅ | No upstream story dependencies |
| **N**egotiable | ✅ | Format and transport approach open |
| **V**aluable | ✅ | Delivers user-visible value |
| **E**stimable | ❌ | "5 points, but the legal team hasn't confirmed which fields are in scope" — estimate assumes unknown scope |
| **S**mall | ✅ | 5 points fits |
| **T**estable | ❌ | Acceptance criteria incomplete until legal clarifies field list; tester cannot verify completeness |

**Gate result: BLOCKED — external dependency**

**Escalation:** 
- **Owner:** GRC/Legal lead
- **Impact of delay:** Cannot start development until field scope is confirmed
- **Next step:** Product owner to request legal sign-off; bring revised story (with confirmed field list + updated AC) to next refinement event

---

### Item 5: User can enable TOTP two-factor authentication (5 points)

| Criterion | Result | Reason |
|-----------|--------|--------|
| **I**ndependent | ✅ | No blocking dependencies |
| **N**egotiable | ✅ | Implementation details open (QR standard, recovery code format, session timing) |
| **V**aluable | ✅ | Delivers user-visible security feature with direct value |
| **E**stimable | ✅ | 5 points, team reviewed with confidence in groom pass |
| **S**mall | ✅ | 5 points fits |
| **T**estable | ✅ | Clear atomic acceptance criteria |

**Gate result: READY FOR PLANNING** (all DoR boxes checked)

---

## Dependency map

```
Item 1 (password reset)
  └─ No dependencies

Item 2 (account settings overhaul)
  └─ No dependencies (but future children will sequence with Items 3, 5)

Item 3 (last-login timestamp)
  └─ BLOCKED BY Item 2 (security tab must exist first)

Item 4 (export account data)
  └─ BLOCKED BY external: legal sign-off on field list

Item 5 (TOTP 2FA)
  └─ No dependencies
```

**Cycles:** None detected.

---

## Ready for planning (priority order)

1. **User can reset their password via email link** — 3 points
2. **User can enable TOTP two-factor authentication** — 5 points

**Total sprint-ready from this event: 8 points**  
**Sprint capacity remaining: 42 points** (from 50-point budget)

---

## Returned to refinement

**Account settings overhaul** — split into 5 child stories for separate refinement:
1. User can manage profile information
2. User can configure notification preferences
3. User can manage connected apps
4. User can view and update billing details
5. User can view and manage security settings

Bring children to next refinement event with fresh INVEST and DoR checks.

---

## Blocked — escalation required

| Item | Blocker | Owner | Impact |
|------|---------|-------|--------|
| Show last-login timestamp | Item 2 child (security tab prerequisite) | PM/dev team | Sequence after Item 2 security tab story ships; no external escalation needed |
| Export account data to PDF | Legal sign-off on field list | GRC/Legal lead | No development can start until scope confirmed; product owner follow up with legal |

---

## Deferred (over capacity budget)

None. All 5 candidates fit within the event timebox.

---

## Notes for the agile-coach

1. **Item 2 split:** Account settings overhaul correctly failed on **Small** and **Estimable**. The groom-pass classification surfaced this early; the team's behaviour-based split (5 user-centric stories vs. technical layers) is the right decomposition. Watch the follow-up refinement to ensure each child is sized independently.

2. **External blocker visibility:** Item 4 (export data) has a hard legal dependency. This is unavoidable but impacts planning: 5 points are unavailable until legal clarifies scope. Product owner should flag this to the stakeholder — set expectation for when development can start (after legal sign-off).

3. **Sequencing dependency:** Item 3 (last-login) is technically Ready on INVEST and DoR but logically waits on Item 2's security-tab child. Once Item 2 child ships, Item 3 unblocks automatically. Good dependency visibility; no ceremony issue. This is a natural backlog sequencing, not a sprint blocker.

4. **Ready backlog headroom:** 2 stories Ready (8 points) leaves 42 points available in the sprint. Team has room for additional work if:
   - Item 2's split children are refined and prioritized before sprint planning, or
   - Higher-priority items emerge from the refinement queue

5. **Groom-pass effectiveness:** The solo groom-pass classification caught Item 2's size issue and Item 4's external blocker early. This event confirmed the classifications; minimal rework needed. Pattern is holding.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 11.5/12.5 (92%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 82976 ms |
| Target cost | $0.1211 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Sets a capacity budget before refining — states team sprint capacity in developer-hours and a refinement budget of ~10% of that capacity, with items-in-scope derived from it | PASS | "Team sprint capacity: 5 developers × 10 days = 50 developer-days (~400 hours)" and "Refinement budget (~10%): ~40 hours total" and "Items in scope: 5 candidates" |
| c2 | INVEST-checks every candidate item with explicit pass/fail per criterion (I/N/V/E/S/T) and a one-line reason, not a blanket 'looks fine' | PASS | Each of the 5 items has a full INVEST table with ✅/❌ per letter and a one-line reason column for every entry. |
| c3 | Flags the 'Account settings overhaul' item as failing Small and splits it by user behaviour (e.g. profile / notifications / billing / security as separate stories), never by technical layer | PASS | Item 2 INVEST shows S=❌ and E=❌; 5 child stories are "manage profile", "notification preferences", "connected apps", "billing details", "security settings" — all user-behaviour oriented. |
| c4 | Surfaces that 'Show last-login timestamp' depends on the security tab from the overhaul item — and sequences or reclassifies it rather than passing it as Ready | PASS | Item 3 I=❌ with reason "Hard prerequisite on Item 2's security tab"; Gate result: "BLOCKED — sequencing dependency". |
| c5 | Reclassifies the 'Export account data' item as Blocked (external legal sign-off on the field list) — not Ready — with owner and impact named | PASS | "BLOCKED — external dependency"; "Owner: GRC/Legal lead"; "Impact of delay: Cannot start development until field scope is confirmed". |
| c6 | Runs a Definition of Ready gate per item and only declares Ready the items that pass every box — 'mostly ready' is not Ready | PASS | Items 1 and 5 get 6/6 DoR → Ready; Item 2 gets 4/6 → back to refinement; Items 3 and 4 gated as Blocked. No partial-pass item declared Ready. |
| c7 | Catches the non-atomic acceptance criterion on the export item ('PDF AND CSV AND email' smuggles multiple criteria into one) against the ISC splitting test | FAIL | Item 4 Testable=❌ is explained solely as "Acceptance criteria incomplete until legal clarifies field list". No mention of PDF/CSV/email non-atomicity or ISC splitting test anywhere in the output. |
| c8 | The two clean stories (password reset, TOTP 2FA) pass INVEST and DoR and leave the event Ready for planning | PASS | Items 1 and 5 each show all-✅ INVEST and DoR 6/6; both appear under "Ready for planning" with point estimates (3 and 5 pts). |
| c9 | Does not re-prioritise the items against the roadmap during the event — readiness only, not re-ranking | PASS | No roadmap comparison, business value ranking, or priority reorder against strategy appears anywhere in the event summary. Notes section addresses ceremony only. |
| c10 | Keeps the agile-coach's ceremony-health lens distinct from the PO's readiness call — notes ceremony observations separately rather than conflating them | PARTIAL | "Notes for the agile-coach" section is explicitly separated from readiness tables and contains ceremony observations ("Pattern is holding", "groom-pass effectiveness"). |
| c11 | Output writes the refinement summary to the backlog file at the given path and reports that path — not only an inline chat answer | PASS | Chat response: "Summary written to: `/private/var/.../work/groomed-queue.md`"; artifact confirms file written with full refinement event content. |
| c12 | Output's item-results table follows the skill format (Item \| INVEST \| Dependencies \| DoR \| Outcome) and assigns every candidate a clear Outcome (Ready / back to refinement / Blocked) | PASS | Table header "\| Item \| INVEST \| Dependencies \| DoR \| Outcome \|" present; all 5 rows assigned one of Ready / Back to refinement / Blocked. |
| c13 | Output produces a dependency map showing the last-login → security-tab/overhaul relationship and the export → legal-sign-off blocker, with any unblocked items marked as startable immediately | PASS | "Dependency map" section: "Item 3 BLOCKED BY Item 2 (security tab)"; "Item 4 BLOCKED BY external: legal sign-off"; Items 1, 2, 5 marked "No dependencies". |

### Notes

The output is thorough and well-structured, correctly handling capacity budgeting, INVEST detail, dependency surfacing, DoR gating, and file output. The sole miss is c7: the non-atomic 'PDF AND CSV AND email' acceptance-criterion issue on the export story is completely absent — the Testable failure is pinned only to the legal blocker, not to the multi-output smuggling.
