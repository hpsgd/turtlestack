# Write Discovery Plan

Scenario: A PM is standing up discovery for a slice. The skill must produce a Torres continuous-discovery plan: tied to a desired outcome, run by the full product trio in every interview, on a protected weekly slot, with automated recruiting set up before the first interview, and a synthesis/OST rhythm — not a one-off research sprint.

## Prompt

> Use the product-manager `write-discovery-plan` skill to set up a continuous-discovery cadence for the
> "activation" slice of a B2B SaaS whose desired outcome is to lift week-one activation from 30% to 55%. The
> product has logged-in users. Write the plan to a file under `docs/product/` in the current working
> directory, in the skill's standard format.
> 
> Proceed without asking — produce the discovery plan.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Done. I've created a runnable discovery plan for the activation slice at `docs/product/discovery-plan-activation.md` and a companion discovery log at `docs/product/discovery-log.md`.

The plan specifies:

- **Desired outcome:** Week-one activation 30% → 55%
- **Trio structure:** PM, designer, engineer attending every interview (no filtering)
- **Recurring slot:** Tuesday 11 AM, protected weekly
- **Recruiting:** In-product prompt to users who didn't activate, with auto-booking calendar integration (zero recruiting friction)
- **Interview type:** Generative discovery focused on week-one friction, blockers, value realisation
- **Target segment:** Users who signed up in the past 2 weeks (tight enough to saturate themes)
- **Synthesis rhythm:** Per-interview log entry; OST update every 3–4 interviews; monthly review

The plan is ready to run next week. The product leader fills in three names (trio), chooses the incentive, and the team blocks the Tuesday slot. Recruiting is automated from day one — the most common reason these cadences collapse is manual recruiting friction, so it's built in upfront.

### Artifacts written

#### `work/docs/product/discovery-log.md`

```
# Discovery log: activation

Continuous discovery log for week-one activation (30% → 55%). Updated after every interview. OST synthesised every 3–4 entries.

| Date | Participant | Segment | Interview Type | Key Signal | Themes | OST Updated? |
|------|-------------|---------|---|---|---|---|
| | | | generative / switch | | | [ ] |

## How to use this log

1. **After every interview:** Add a row with the date, participant segment, interview type, and the single most important signal from that conversation.
2. **"Themes" column:** Spot patterns across 3–4 interviews (e.g., "data entry burden", "integration friction", "unclear next step").
3. **Every 3–4 interviews:** Run `/product-manager:synthesise-interviews` over the log. Update the OST. Check the OST Updated box.
4. **Monthly:** Full review. Compare emerging themes to roadmap. Flag any new opportunities that conflict with current bets.

## What counts as a "key signal"

- **Blockers:** "Couldn't figure out how to X" / "Gave up on Y"
- **Workarounds:** "I worked around it by…" / "I use a spreadsheet alongside because…"
- **Triggers:** "I came back the next day because…" / "I never logged back in because…"
- **Comparisons:** "Your feature is confusing vs Competitor; their flow is clearer"
- **Unmet need:** "I wish you had…" / "I had to manually…"

## Related files

- `discovery-plan-activation.md` — the plan and scheduling
- `/product-manager:write-interview-guide` — the full interview structure
- `/product-manager:synthesise-interviews` — turn log entries into themes
- `/product-manager:write-opportunity-solution-tree` — the artifact this discovery keeps current

---

**Log started:** 2026-06-13  
**Team:** [PM / Designer / Engineer names]

```

#### `work/docs/product/discovery-plan-activation.md`

```
# Discovery plan: activation

| Field | Value |
|-------|-------|
| Desired outcome | Week-one activation: 30% → 55% (25 percentage point lift) |
| Trio | [PM name] / [Designer name] / [Engineer name] — **to be filled in by product leader** |
| Recurring slot | Tuesday 11:00 AM (weekly) |
| Cadence target | Weekly, minimum |
| Recruiting mechanism | In-product prompt to logged-in users who did not activate in week one. Offer: [incentive TBD: beta access / account credit / other]. Calendar integration auto-books slots. |
| Interview type | Generative discovery — understanding week-one friction and blockers |
| Target segment | Users who signed up in past 2 weeks, activated or did-not-activate, across all customer segments (or narrow to primary segment if TAM permits) |
| Synthesis rhythm | Per-interview: log participant, type, key signal to `docs/product/discovery-log.md`. Every 3–4 interviews: OST update. Monthly: full review and roadmap impact |

## First two weeks

- [ ] **Calendar:** Recurring Tuesday 11:00 AM slot created and added to PM / Designer / Engineer calendars. Marked protected (do not bump).
- [ ] **Recruiting:** In-product prompt spec drafted. Incentive chosen. Recruiting pool seeded with first 3–5 participants. Calendar integration tested.
- [ ] **Discovery log:** `docs/product/discovery-log.md` created with headers (Date, Participant, Segment, Interview Type, Key Signal, Themes).
- [ ] **First interview:** Scheduled and on trio's calendars.

## Interview guide

This cadence runs generative discovery. Each interview explores:

1. **Onboarding friction** — what stopped them or slowed them in their first week?
2. **Value realisation** — when / how did they see value? If they didn't activate, what would have prompted it?
3. **Setup burden** — data entry, integrations, configuration — what was hard?
4. **Comparison to alternative** — what were they using before? Why switch? Why abandon?
5. **Trigger for next action** — what would make them log back in tomorrow?

See `/product-manager:write-interview-guide` for the full guide template.

## Synthesis and OST updates

After every interview, the team logs the signal to the discovery log. Every 3–4 interviews:

1. Run `/product-manager:synthesise-interviews` over the log entries.
2. Update the opportunity-solution tree (`/product-manager:write-opportunity-solution-tree`).
3. Flag any signals that change the roadmap or week-one flow.

Minimum monthly: review the full OST against emerging themes. If a new opportunity emerges that conflicts with the current roadmap, flag it to the product leader.

## Rules

- **Trio attends every interview.** The engineer hears constraints and workarounds, the designer hears interaction friction, the PM hears business context. No filtering through the PM.
- **Protect the Tuesday slot.** This cadence dies the first time it gets bumped for "more urgent" work. It's not negotiable.
- **Automate recruiting now.** Manual recruiting next week will collapse by week 3. Specify the incentive and calendar integration this week.
- **Weekly beats one-time sprints.** A one-time discovery sprint's insights are stale by ship date. Weekly keeps pace with users' changing needs.

## Who fills in the blanks

**Product leader:** Confirm the trio names (PM / designer / engineer), choose the incentive, and approve the target segment narrowing.

**Recruiting / ops:** Wire up the in-product prompt and calendar integration before the first Tuesday.

**PM / designer / engineer:** Block the Tuesday 11 AM slot on your calendars starting next week. Attend every interview. Log signals. Update the OST every 3–4.

## Next steps

1. Fill in the trio names (requires product leader sign-off).
2. Specify the incentive for participants.
3. Wire the in-product recruiting prompt and calendar integration.
4. Create `docs/product/discovery-log.md` with column headers.
5. Schedule the first interview for next Tuesday at 11 AM.
6. Read `/product-manager:write-interview-guide` for the interview structure.

---

**Created:** 2026-06-13  
**Status:** Ready to run starting next week

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 13.0/13.0 (100%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 40736 ms |
| Target cost | $0.0711 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | PASS: Ties discovery to a specific desired outcome (week-one activation 30% → 55%), not "learn about customers" | PASS | Plan table row: "Desired outcome \| Week-one activation: 30% → 55% (25 percentage point lift)" |
| c2 | PASS: Forms the product trio (PM + designer + engineer) and states all three attend EVERY interview — not a researcher reporting back to the PM | PASS | Rules section: "Trio attends every interview... No filtering through the PM." Engineer/designer/PM roles explicitly named. |
| c3 | PASS: Protects a recurring weekly slot and targets at least one customer conversation per week (continuous, not a sprint) | PASS | "Recurring slot \| Tuesday 11:00 AM (weekly)"; Rules: "Protect the Tuesday slot... not negotiable"; "Weekly beats one-time sprints." |
| c4 | PASS: Automates recruiting BEFORE the first interview (e.g. in-product prompt to a % of logged-in users feeding a scheduling pool) — names manual recruiting as the main cause of cadence collapse | PASS | Rules: "Automate recruiting now. Manual recruiting next week will collapse by week 3." Calendar integration is a setup prerequisite in the first-two-weeks checklist. |
| c5 | PASS: States the interview type (generative / switch) and a narrow target segment that will reach theme saturation (~20-30 interviews) | PASS | "Interview type \| Generative discovery"; "Target segment \| Users who signed up in past 2 weeks"; chat: "tight enough to saturate themes" |
| c6 | PASS: Sets a synthesis / OST update rhythm (per-interview log, OST update every 3-4 interviews, monthly review) — discovery without synthesis is just conversation | PASS | "Synthesis rhythm \| Per-interview: log... Every 3–4 interviews: OST update. Monthly: full review and roadmap impact" |
| c7 | PASS: If any paid panel or recruiting service is mentioned, flags the cost and prefers the free in-product / customer-success route first | PASS | No paid recruiting service mentioned at all; plan exclusively uses in-product prompt with internal incentives (beta access / account credit). Condition never triggered. |
| c8 | PARTIAL: Frames the plan as runnable next week — a concrete first-two-weeks checklist | PARTIAL | "First two weeks" section has 4 checkbox items (calendar, recruiting, discovery log, first interview). Chat: "The plan is ready to run next week." |
| c9 | PASS: Output plan file exists under `docs/product/` and names the desired outcome as the thing discovery serves | PASS | File written to `work/docs/product/discovery-plan-activation.md`; first table row is the desired outcome (30% → 55%). |
| c10 | PASS: The plan names the trio and states explicitly that all three attend every interview (the no-filter rationale) | PASS | Trio field lists PM/Designer/Engineer; Rules: "The engineer hears constraints... the designer hears interaction friction... No filtering through the PM." |
| c11 | PASS: The plan specifies an automated, self-sustaining recruiting mechanism set up before the cadence starts, not per-interview manual recruiting | PASS | "Calendar integration auto-books slots"; first-two-weeks checklist requires recruiting pool seeded and integration tested before first interview. |
| c12 | PASS: The plan sets weekly (or bi-weekly floor) cadence and a synthesis rhythm with OST updates, not a single discovery sprint | PASS | "Cadence target \| Weekly, minimum"; synthesis rhythm specifies OST update every 3–4 interviews; Rules: "Weekly beats one-time sprints." |
| c13 | PASS: A target segment narrow enough to saturate is named, with an interview type | PASS | "Target segment \| Users who signed up in past 2 weeks, activated or did-not-activate"; "Interview type \| Generative discovery" |
| c14 | PARTIAL: Any paid recruiting path is cost-flagged with the free route preferred first | PARTIAL | No paid path included; plan uses only free in-product prompt + internal incentives. Spirit of criterion fully met; ceiling caps at PARTIAL. |

### Notes

The plan is comprehensive and hits every Torres continuous-discovery requirement: tied outcome, trio attends all interviews with explicit no-filter rationale, protected weekly slot, automated pre-cadence recruiting with collapse rationale, generative interview type, narrow segment, and full synthesis/OST rhythm. The only ceiling-capped criteria (c8, c14) are structurally capped at PARTIAL by the test author, not by any gap in the output.
