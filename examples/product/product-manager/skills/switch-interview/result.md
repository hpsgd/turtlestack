# Switch Interview

Scenario: A PM wants to understand a real B2B purchase. The skill must run a Moesta switch interview: pick a real recent switch, reconstruct the timeline as a documentary (first thought → passive looking → active looking → decision) with specifics, code the four forces (push, pull, anxiety, habit) from quotes, and extract the demand-side insight including the real competition — not run an evaluative feature-feedback interview.

## Prompt

> Use the product-manager `switch-interview` skill to design a switch interview for "Dana, an ops lead at a
> mid-market logistics firm who switched from a spreadsheet to our reconciliation product six weeks ago". Write
> the interview design and force-coding structure to a file under `docs/product/` in the current working
> directory, in the skill's standard format. Use plausible illustrative quotes to populate the timeline and
> force coding.
> 
> Proceed without asking — produce the switch interview.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Done. Switch interview for Dana written to `docs/product/switch-interview-dana.md`.

The interview reconstructs her actual timeline from first pain (March month-end close took 3 days + $14k error caught too late) through executive pressure from her finance director, passive awareness of alternatives, active research, and the deciding moment (product demo on April 24 that proved integration with regional banks could work).

Force coding reveals:
- **Push:** Error risk + time burden (8–10 hrs/week on variance hunting)
- **Pull:** Speed (200 transactions matched in 3 seconds vs. hours manual)
- **Anxiety:** Regional bank API integration (the blocker — resolved in demo)
- **Habit:** Excel templates + 4-year muscle memory (addressed by parallel trial approach)

The demand-side insight names the real job: *error prevention at scale + time recovery* — not cloud modernization. The decisive anxiety (integration fit) and how it was overcome (explicit demo proof) show why the purchase happened that day, not "eventually."

### Artifacts written

#### `work/docs/product/switch-interview-dana.md`

```
# Switch interview: Dana — spreadsheet to reconciliation SaaS

| Field | Value |
|-------|-------|
| Switched | From manual Excel-based cash reconciliation → cloud reconciliation platform |
| When | 2026-04-24 |
| Interview date | 2026-06-08 |

## Timeline

| Moment | What happened (specific) |
|--------|--------------------------|
| **First thought** | Early April 2026. Month-end close for March took 3 days instead of the usual 2. Dana spent 8 hours manually cross-referencing variance reports across 3 Excel workbooks spanning 47 delivery centers. Found a $14,000 discrepancy in the petty cash reconciliation — three days *after* finance had already booked the ledger entries. Had to reverse and repost. |
| **Passive looking** | Mid-April. At a logistics industry roundtable, mentioned the close delays to another ops lead from a competitor. She said offhand: "We switched to some automated platform six months ago. Basically imports our bank feeds and flags the real variances." Dana filed it mentally but didn't act on it. |
| **Active looking** | April 22. Finance director David asked why the March close took three days. Pointed to the $14k error as the reason — we needed tighter controls. David said "Fix this by end of Q2. Budget's there if you need it." Dana spent that afternoon and the next morning researching: Google search ("cash reconciliation software logistics"), LinkedIn post from a colleague at FedEx logistics, two product websites, one Reddit thread from accountants. Made a list of four tools. |
| **The event / decision** | April 24, 9:30 AM. Scheduled a 30-minute demo with the platform. Product demo showed auto-matching of 200 transactions from their primary bank feed in under 3 seconds, flagged 4 real variances (vs. 47 flagged as false positives in her manual process). Showed integration with their regional bank APIs (the blocker Dana had worried about). By 11:00 AM same day, Dana approved a 90-day free trial and set up the staging environment with test data. "If this works the way it's showing, we cut our close time in half and catch errors *before* posting." |

## Force coding

| Force | Quote |
|-------|-------|
| **Push** | "We were losing variances in the shuffle. March close, I found $14k in discrepancies three days *after* we'd already booked the ledger. Can't do that. And I'm spending two days a week just reconciling. It's not sustainable." |
| **Pull** | "When I saw it auto-match 200 transactions in three seconds and actually flag the *real* variances — not the false positives my macros catch — I just... yeah. That's what I needed to see. No more digging through pivot tables at 10 PM." |
| **Anxiety** | "My biggest worry was: would it actually work with our weird bank feeds? Half our centers use regional banks without standard APIs. We've tried 'modern' tools before. They look great in the demo and then don't talk to your actual systems. This one showed it could handle it. That was the relief." |
| **Habit** | "The team knows Excel. We've got macros, templates, formulas that work. And I've been managing this way for four years — I know where everything is. Switching means retraining everyone, changing our month-end process. That was... I was worried about that." |

## Demand-side insight

- **Job hired for:** Reduce ops risk during month-end close by catching posting errors before they hit the ledger, and reclaim the 8–10 hours per week Dana was spending on manual reconciliation variance-hunting. Not primarily "automate" or "cloud modernize" — the job is *error prevention at scale* (47 centers, 200+ daily transactions) and *time recovery*.

- **Decisive anxiety:** Integration fit. Dana's worry that the tool wouldn't work with her regional bank feeds (the "weird banks") nearly prevented the trial. The product demo explicitly addressing this — showing it could handle regional APIs — was what tipped her from "interesting, maybe later" to "start the trial today."

- **Habit overcome:** Excel templates and macros (the team's institutional knowledge) plus Dana's four-year muscle memory of the manual process. The trial worked because it was positioned as *addition* (run both systems in parallel for 30 days) rather than *replacement* (throw out the old way). That lowered the perceived risk of the habit-breaking.

- **Real competition:** Not other SaaS reconciliation tools. The real competitor was: *the status quo, a spreadsheet workflow that kinda works, plus the belief that month-end risk is just "part of the job."* David's budget and deadline (executive pressure) broke the inertia. The product demo proved there was a way to do it that didn't require weeks of integration work or replacing the whole process.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 10.5/12.0 (88%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 52101 ms |
| Target cost | $0.0764 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Frames a real, recent, specific switch (Dana, spreadsheet → product, ~6 weeks ago) — not a hypothetical 'people who might buy' | PASS | File header: 'Switched \| From manual Excel-based cash reconciliation → cloud reconciliation platform \| When \| 2026-04-24 \| Interview date \| 2026-06-08' — ~6 weeks prior, concrete individual. |
| c2 | Reconstructs the timeline as a documentary across the four moments: first thought, passive looking, active looking, the event/decision — with specifics (when, where, who else) | PASS | Timeline table has all four labeled rows with dates, named people (David, competitor ops lead), locations (roundtable, 9:30 AM demo), and amounts ($14k, 47 centers). |
| c3 | Codes ALL FOUR Moesta forces by name — Push and Pull (drive the switch), Anxiety and Habit (resist it) | PASS | Force coding table rows: **Push**, **Pull**, **Anxiety**, **Habit** — each with a dedicated quote row. |
| c4 | Notes that the switch happens only when push + pull outweigh anxiety + habit | FAIL | Demand-side insight describes each force's resolution but never states the balance equation or frames it as 'switch occurs when push+pull > anxiety+habit'. |
| c5 | Codes forces from quotes (the customer's words), not from the interviewer's interpretation/inference | PASS | Each force row contains a first-person Dana quote, e.g. Push: 'We were losing variances in the shuffle... I'm spending two days a week just reconciling. It's not sustainable.' |
| c6 | Reconstructs the decision moment with documentary specifics (what tipped them, what happened right before) rather than abstract feature evaluation | PASS | 'April 24, 9:30 AM... by 11:00 AM same day, Dana approved a 90-day free trial' with the specific blocker resolved (regional bank API integration shown in demo). |
| c7 | Extracts the demand-side insight — the job hired for, the decisive anxiety, the habit overcome, and the real competition (often 'do nothing' / the spreadsheet) | PASS | Four bullet points labeled exactly: 'Job hired for', 'Decisive anxiety', 'Habit overcome', 'Real competition: Not other SaaS... real competitor was the status quo.' |
| c8 | Distinguishes the switch interview (retrospective, post-purchase) from generative discovery (prospective) | PARTIAL | Structure is inherently retrospective (Interview date 6 weeks post-switch, timeline reconstructs past events), but no explicit methodological note contrasting it with prospective discovery. |
| c9 | Output file exists under `docs/product/` with a timeline table (first thought → passive → active → decision) and a four-force coding table | PASS | File at `work/docs/product/switch-interview-dana.md` contains both a Timeline table and a Force coding table with all required rows. |
| c10 | All four forces (push, pull, anxiety, habit) are present and correctly classified as drivers vs resistors | PASS | Demand-side insight: Anxiety 'nearly prevented the trial'; Habit's 'perceived risk... had to be lowered'; Push/Pull described as what drove the switch. |
| c11 | The force coding cites quotes rather than interviewer interpretation | PASS | All four force rows contain verbatim first-person quotes, e.g. Anxiety: 'My biggest worry was: would it actually work with our weird bank feeds?' |
| c12 | The demand-side insight names the job hired for, the decisive anxiety, and the real competition (e.g. the spreadsheet / status quo) | PASS | Explicit bullets: job = 'error prevention at scale + time recovery'; decisive anxiety = 'Integration fit'; real competition = 'the status quo, a spreadsheet workflow that kinda works'. |
| c13 | Output states the switch interview is retrospective, distinct from prospective generative discovery | FAIL | No explicit statement in the file distinguishing retrospective/post-purchase nature from prospective discovery. The structure implies it but never states it. |

### Notes

Strong output: all four timeline moments, all four forces with first-person quotes, and a complete four-element demand-side insight section. The two gaps are c4 (no explicit four-forces balance equation framing) and c13 (no stated retrospective vs. prospective distinction), both relatively minor structural omissions in an otherwise thorough artifact.
