# Metrics Strategy Review

Scenario: Leadership wants a cumulative vanity metric as the North Star and wants to force a product change based on a correlation treated as cause. The agent must anchor to the customer value moment, reject the vanity metric, propose a value-based North Star, run a Goodhart check, expose the correlation-not-causation error and demand an experiment, build a leading/lagging hierarchy, and stay in its lane (hand offs to data-engineer and product-manager) using its structured deliverable format.

## Prompt

> Use the product-analyst agent to handle this, and respond in its standard measurement methodology and deliverable format.
> 
> We're the team behind Northstar Notes, a personal note-taking app. Two things came down from leadership this week and we want your read before we commit:
> 
> 1. The CEO wants to make "total registered users" our official North Star Metric — it only ever goes up and looks great in the board deck.
> 2. Our data team found that users who join a shared "Spaces" group retain about 3x better than users who don't, so the growth team wants to force every new user into a Spaces group during onboarding to lift retention.
> 
> Give us your read on the metrics strategy: what our North Star should be, how to structure the supporting metrics, and what to do about the Spaces finding.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## North Star: Northstar Notes

---

### 1. Critique: Why "Total Registered Users" must be rejected

**Total registered users is the canonical vanity metric.** The skill methodology has one hard rule: never propose a cumulative metric as a North Star. Here's why this one specifically fails every test:

| Failure mode | What it means for Northstar Notes |
|---|---|
| **Cumulative — only goes up** | Provides zero signal about product health. A product whose entire user base has churned still shows an increasing North Star. The CEO is right that it looks great in the board deck — that's the problem. |
| **Measures acquisition, not value** | Registration measures the marketing funnel, not the product. A user who signed up three years ago and never took a note is counted identically to a daily power user. |
| **Goodhart failure** | Optimising for total registrations incentivises buying low-quality users, reducing signup friction for unqualified leads, and ignoring everything that happens after registration. All of this harms long-term product health. |
| **Lags problems catastrophically** | If retention collapses, total registered users keeps climbing for months before anyone notices. The alarm is silenced precisely when it should be loudest. |
| **No causal link to revenue or sustainability** | A board deck metric that never goes down tells leadership nothing about whether the business is working. |

---

### Customer value moment

> "A customer of Northstar Notes gets value when they return to their notes and actively write, organise, or retrieve information that helps them think, remember, or collaborate."

The observable event is **a note being created, edited, or meaningfully accessed in a session**. Registration is not a value moment. Onboarding completion is not a value moment. The value moment is the recurring act of using notes.

---

### North Star Metric

**Weekly Note-Active Users (WNAU)**

| Field | Definition |
|---|---|
| **Question** | How many users are getting recurring value from Northstar Notes this week? |
| **Definition** | Distinct users who create, edit, or actively access ≥1 note in the trailing 7 days |
| **Calculation** | `COUNT(DISTINCT user_id WHERE note_action_event IN last_7_days AND session_depth >= threshold)` |
| **Granularity** | Weekly cadence, tracked on a rolling 7-day basis |
| **Filters** | Exclude bot/internal accounts; exclude users within 24h of signup (signup-day exploration is not habit); exclude auto-created or system-generated note touches |
| **Time window** | Rolling 7-day window, reported weekly |
| **Owner** | Product + Data team |

This is the right shape because Northstar Notes is an engagement product — value is delivered through **repeated use**, not through a single transaction. The North Star must capture the habit loop, not the acquisition funnel.

---

### Goodhart check

**Gaming scenario:** The growth team pushes aggressive re-engagement push notifications that drive users to open the app and tap a single note. The metric rises; actual engagement is hollow. Alternatively, onboarding auto-creates a "starter note" on the user's behalf, inflating WNAU with zero user intent.

**Verdict: Counter-metric required**

The definition is tightened by requiring `session_depth >= threshold` (e.g., ≥30 seconds of active session, or ≥1 substantive action beyond a bare open). Two counter-metrics must be tracked alongside WNAU and must not be allowed to fall while WNAU climbs:

| Counter-metric | Guardrail purpose |
|---|---|
| **Average notes per WNAU** | Detects inflation via empty/trivial interactions — if WNAU rises but average note depth falls, the team is gaming |
| **WNAU 30-day retention** | Detects dark-pattern re-engagement — if WNAU rises but fewer users return the following month, the activation was forced not genuine |

---

### Coherence across customer types

| Customer type | Is WNAU-up good for them? |
|---|---|
| Solo note-taker (personal capture, retrieval) | Good — their value action is measured directly |
| Collaborative Spaces user (shared notes, group work) | Good — any note interaction in a Space counts |
| Read-heavy Spaces member (consumes shared notes, rarely writes) | Good — "actively accesses" is included in the definition, capturing readers |

**Verdict: Coherent.** WNAU covers both solo and collaborative modes. The inclusion of note access (not just writes) ensures Spaces readers who derive value without authoring are counted. If read-only usage in Spaces grows significantly, revisit whether a weighted interaction score is warranted.

---

### Input metrics

These are the 5 levers teams can move this week that lead WNAU:

| Input metric | Definition | Leading? | Owner |
|---|---|---|---|
| **New user activation rate** | % of new signups who create their first note within 7 days | Yes — activations this week feed WNAU next week | Growth / Onboarding |
| **D7 note retention** | % of users who return and take a note action on day 7 after first note | Yes — predicts whether the habit loop is forming | Retention / Core product |
| **Notes per active user per week** | Average notes created or edited per WNAU (depth signal) | Yes — depth in week N predicts retention in week N+2 | Core product |
| **Spaces join rate (organic)** | % of active users who voluntarily join or create a Spaces group within 30 days | Yes — see Spaces section below; organic adoption, not forced | Collaboration / Growth |
| **Re-engagement rate** | % of lapsed users (no note action in 14+ days) who return and take a note action within 7 days of a re-engagement touchpoint | Yes — retention recovery lever | Growth / CRM |

---

### The Spaces finding: correlation, not (yet proven) causation

**The growth team's instinct is directionally right but the proposed tactic is wrong.**

The 3× retention finding is almost certainly **heavily confounded**. Users who voluntarily join a Spaces group are not a random sample:

- They are more engaged to begin with (selection bias — the kind of user who seeks out collaboration features is already invested)
- They likely have existing collaborators on the platform (network effect — their retention is driven by others pulling them back, not the feature itself)
- They may have more mature use cases that make the app inherently stickier

**Forcing all new users into a Spaces group will not capture the same 3× lift** because the causal mechanism — whatever it is — operated on self-selected, socially-motivated users. Forcing an unconnected new user into an empty or stranger-filled Space replicates the treatment condition superficially while eliminating the mechanism.

Worse: a bad forced-onboarding experience (feeling pushed into something with no context or payoff) is a documented churn driver. You may actively suppress the retention you're trying to lift.

**Recommended course of action:**

1. **Do not ship the forced-Spaces onboarding** — at minimum, not until Step 2 is complete.

2. **Run a causal experiment.** Randomly assign new users to three cohorts:
   - **Control:** standard onboarding, no Spaces prompt
   - **Nudge:** prominent Spaces invitation with clear value framing, opt-in
   - **Forced:** automatically added to a Spaces group, no opt-in
   
   Measure D7, D30, and D90 retention plus note depth. This will decompose the 3× signal into its components.

3. **Investigate the mechanism before designing the intervention.** The most valuable question is not "how do we get users into Spaces?" but "**what about Spaces drives retention?**" Hypotheses to test:
   - Is it social accountability (others can see your notes)?
   - Is it network pull (colleagues are already there)?
   - Is it the use case (Spaces users have a project/team context that makes note-taking inherently stickier)?
   - Is it simply that power users self-select into Spaces?
   
   The answer determines whether the right lever is onboarding flow, invite mechanics, templates, or something else entirely.

4. **If the nudge arm wins,** design an onboarding step that helps users discover a genuine collaborative use case — a real person to invite, a real project to start — rather than a hollow structural placement.

---

### Link to OKRs

This North Star serves the product-level objective: **"Northstar Notes becomes a daily-use habit for our users."** WNAU is the outcome measure. The five input metrics map directly to the key results: activation (onboarding), habit formation (D7 retention), depth (notes per user), collaboration (organic Spaces join), and recovery (re-engagement). The Spaces experiment is a discovery investment that should be scoped as its own key result before any forced-onboarding decision is committed to roadmap.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 12.0/12.0 (100%) |
| Evaluated | 2026-06-12 |
| Target model | claude-sonnet-4-6 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 96113 ms |
| Target cost | $0.1886 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Anchors to the customer value moment before proposing any number — names the observable moment a Northstar Notes user actually gets value (capturing / retrieving a note they rely on) | PASS | Dedicated 'Customer value moment' section precedes any metric: 'A customer of Northstar Notes gets value when they return to their notes and actively write, organise, or retrieve information...' |
| c2 | Rejects "total registered users" as a North Star, explicitly naming it a cumulative vanity metric that rises regardless of product quality | PASS | Section title 'Critique: Why Total Registered Users must be rejected'; 'Total registered users is the canonical vanity metric'; failure row 'Cumulative — only goes up'. |
| c3 | Proposes a North Star that measures delivered customer value (e.g. active users who capture and retrieve notes), not a company-convenience count, and treats revenue as a lagging result rather than the North Star | PASS | Proposes WNAU: 'users who create, edit, or actively access ≥1 note in the trailing 7 days.' Revenue is not the NSM; OKR section frames WNAU as outcome measure. |
| c4 | Runs a Goodhart check on its proposed North Star — names how optimising it could be gamed and whether that would hurt the user | PASS | Dedicated 'Goodhart check' section names two gaming scenarios: push notifications driving hollow opens and onboarding auto-creating starter notes. Proposes two counter-metrics. |
| c5 | Flags the "Spaces group → 3x retention" finding as correlation, NOT causation — points out those users were likely already more engaged — and recommends an experiment (A/B or holdout) before forcing everyone into Spaces | PASS | 'The 3× retention finding is almost certainly heavily confounded... selection bias... Forcing all new users into a Spaces group will not capture the same 3× lift.' Three-cohort RCT recommended. |
| c6 | Builds a metric hierarchy that distinguishes leading/input metrics (controllable this week) from the lagging North Star — not a single number | PASS | 'Input metrics' table with 5 entries, each marked 'Leading? Yes' with explanations like 'activations this week feed WNAU next week', explicitly contrasting with the lagging WNAU. |
| c7 | Distinguishes leading, lagging, and vanity metrics explicitly and keeps vanity metrics out of the tree | PASS | Total registered users labelled vanity and excluded from hierarchy; WNAU is the lagging NSM; 5 input metrics are leading. No vanity metrics appear in the structured metric tree. |
| c8 | Names the hand-offs — data-engineer implements instrumentation, product-manager owns OKRs — and stays within its own remit (does not rewrite OKRs or build pipelines) | PASS | Owner columns in NSM table ('Product + Data team') and input metrics table list named owners. OKRs section defers the Spaces experiment to 'its own key result' without rewriting them or specifying pipelines. |
| c9 | Hits a decision checkpoint — flags that changing an established North Star, or shipping an onboarding change that could degrade a segment's experience, needs product-manager / leadership sign-off | PARTIAL | Flags Spaces onboarding gate ('Do not ship...at minimum, not until Step 2 is complete') but does not explicitly require leadership/PM sign-off for the North Star change itself. |
| c10 | Output uses a structured deliverable format (type, customer question, deliverable, Goodhart/coherence check, hand-off) rather than freeform prose | PASS | Output has labelled sections: Customer value moment, North Star Metric (structured table), Goodhart check, Coherence check, Input metrics table, Spaces analysis, Link to OKRs — not freeform prose. |
| c11 | The Spaces recommendation is "run an experiment to establish causation," not "force everyone into Spaces" | PASS | 'Do not ship the forced-Spaces onboarding'; 'Run a causal experiment. Randomly assign new users to three cohorts: Control / Nudge / Forced.' |
| c12 | The proposed North Star is expressed as the customer's win as a number, with revenue treated as a downstream/lagging result | PASS | WNAU is 'COUNT(DISTINCT user_id WHERE note_action_event...)' — customer's active use as a count. Revenue not proposed as NSM; critique flags 'no causal link to revenue' as a failure of total registered users. |
| c13 | A Goodhart / coherence checklist is present and worked through, not just mentioned | PARTIAL | Goodhart section works through two gaming scenarios with specific counter-metrics. Coherence section evaluates three distinct user types with verdicts. Both worked through, not merely mentioned. |

### Notes

The output is exemplary — every major criterion is addressed with specificity and structure. The only gap is c9, where the decision-checkpoint for changing the North Star itself (requiring leadership/PM sign-off) is absent; the gate exists only for the Spaces onboarding change.
