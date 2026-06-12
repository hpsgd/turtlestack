---
name: team-health-scan
description: "Run a team-health scan: an Edmondson-style psychological-safety questionnaire, a working-norms review, and a Tuckman-stage assessment on reteaming. Produces a health report distinguishing what to act on from what to surface. Use to establish a safety baseline, after reteaming, or when a team feels off."
argument-hint: "[team name]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Team Health Scan

Run a team-health scan for **$ARGUMENTS**. Psychological safety is a precondition for almost every agile practice —
a retrospective on an unsafe team produces only safe-to-say data, and a standup where developers fear surfacing
blockers becomes a performance. This scan reads safety, norms, and team-stage so you coach the real problem rather
than polishing ceremonies on top of fear. Reference:
[Amy Edmondson](https://amycedmondson.com/psychological-safety/), *The Fearless Organization* (2018), and
[Tuckman's stages](https://en.wikipedia.org/wiki/Tuckman%27s_stages_of_group_development).

## Step 1: Run the psychological-safety questionnaire

Use an Edmondson-style anonymous questionnaire. The seven classic items (agree/disagree, 1-5):

1. If you make a mistake on this team, it is often held against you. *(reverse-scored)*
2. Members of this team are able to bring up problems and tough issues.
3. People on this team sometimes reject others for being different. *(reverse-scored)*
4. It is safe to take a risk on this team.
5. It is difficult to ask other members of this team for help. *(reverse-scored)*
6. No one on this team would deliberately act to undermine my efforts.
7. Working with members of this team, my unique skills and talents are valued and utilised.

Run it anonymously. Raw responses are never attributed — attribution destroys the safety the scan measures. Report
the distribution, not individuals.

Reverse-scoring is where this step goes wrong most often. Items 1, 3, and 5 are negatively worded: agreement means
*less* safety. Convert each reverse-scored item to a safety-aligned value with `safety = 6 − raw` (on a 1-5 scale)
before averaging, so every item points the same way (higher = safer). Apply it to all three negative items, never
just one or two.

Worked example: raw item 1 = 4.1 → 6 − 4.1 = **1.9** (a poor signal — people agree mistakes are held against them).
Raw item 5 = 3.9 → 6 − 3.9 = **2.1** (a poor signal — people agree it's hard to ask for help). Positively worded
items (2, 4, 6, 7) are used as-is: raw item 4 = 2.1 stays **2.1** (a poor signal — it's not felt safe to take
risks). After converting, the lowest safety-aligned values are the real concerns regardless of how the item was
worded.

Output: a safety score and the distribution, with all three reverse-scored items converted via `6 − raw` and the
lowest converted values named as the concerns.

## Step 2: Review working norms

Read the team's working agreements (`docs/coaching/working-agreements.md`). Check whether they're being followed,
whether they're specific enough to be testable, and whether any are quietly ignored. A norm that's violated with no
consequence is an authority gap, not a norms gap — note which it is.

## Step 3: Assess the Tuckman stage (especially after reteaming)

Every reteaming event resets safety and disrupts norms. Assess where the team sits:

| Stage | Signals | Coaching implication |
|-------|---------|---------------------|
| Forming | Polite, cautious, low conflict | Establish norms and safety; don't expect peak output |
| Storming | Open conflict, friction over how to work | Coach conflict surfacing; this is healthy, not broken |
| Norming | Agreements forming, conflict resolving | Reinforce agreements; let the team own more |
| Performing | High autonomy, self-correcting | Stay focused and light-touch; protect what works |

If the team reteamed recently (new joiner, split, merge, switch — see
[Dynamic Reteaming](https://www.heidihelfand.com/dynamic-reteaming/)), expect a reset and set expectations
accordingly. The org-level failure mode: constant reorganisation means the team never reaches norming before the
next change arrives.

## Step 4: Separate act-on from surface

Not everything the scan reveals is yours to fix. Sort findings:

- **Act on** — within the team's process: low safety in retros, vague norms, skipped agreements.
- **Surface** — beyond process coaching: serious interpersonal harm, a manager creating fear, structural
  reteaming churn. These go to the team's lead (CTO or CPO) or the coordinator, not into a coaching action item.

## Rules

- Always run the questionnaire anonymously. Attributed safety data is a contradiction in terms and will poison the
  next scan.
- Report distributions, never individuals. The scan measures the team, not people.
- Handle reverse-scored items correctly. Items 1, 3, and 5 are negatively worded — a "1" there is a *good* signal.
- Never assert safety exists when the data says otherwise. Reading high when it's low is the most damaging error a
  coach can make.
- Surface, don't bury, serious harm. Psychological-safety damage from a person is an escalation, not a retro item.

## Output Format

```markdown
---
title: Team Health Scan — [team]
date: YYYY-MM-DD
author: agile-coach
category: Coaching
confidence: [0-4]
---

## Psychological safety
- Score: [aggregate, 1-5]
- Distribution: [spread across items]
- Lowest-scoring items: [which, and what they suggest]

## Working norms
- Followed: [...]
- Vague or ignored: [...] (norms gap vs authority gap)

## Tuckman stage
- Assessed stage: [forming/storming/norming/performing]
- Recent reteaming: [yes/no — pattern]

## Act on (process coaching)
1. [...]

## Surface to lead / coordinator (beyond process)
1. [...]
```
