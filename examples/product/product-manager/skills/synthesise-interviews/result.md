# Synthesise Interviews

Scenario: A PM has run several interviews and must synthesise them. The skill must pattern-code observations at the need level (not feature requests), require multiple participants per theme (one quote is an anecdote), actively look for disconfirming evidence and report the discard rate, map themes onto OST changes that cite their interviews, and make an explicit saturation call. Raw interview notes are staged as a fixture.

## Prompt

> Use the product-manager `synthesise-interviews` skill to synthesise the discovery interviews for the
> "activation" slice. The raw interview notes are at `{workspace}/work/docs/product/interviews/` (five files) —
> read them all. The desired outcome is to lift week-one activation. Write the synthesis to a file under
> `docs/product/` in the current working directory, in the skill's standard format.
> 
> Proceed without asking — produce the synthesis.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Done. I've synthesised the five activation interviews and written the synthesis to `docs/product/synthesis-activation-window-1.md`.

**Key findings:**

**Two clear themes blocking week-one activation:**

1. **Mobile-responsive bank feed connection** (2/5 support, segment-specific) — Priya and Sam, both mobile-first, abandoned onboarding when forced to desktop for bank auth. Falls back to legacy spreadsheets.

2. **Post-action confirmation gap** (2/5 support, 20% discard rate) — Marco and Lena both completed data imports but had no confirmation they'd succeeded. Marco duplicated the import three times; Lena kept exploring looking for a "next step" signal.

3. **Feature discoverability** (1/5 anecdote, not yet a theme) — Dana assumed the invite feature was paid-only and gave up. Needs another case to establish as a pattern.

**Saturation call:** Shift to concept testing rather than more generative discovery in this segment. The window has surfaced enough distinct themes to guide fix directions (mobile auth UX, success confirmation, clearer free/paid boundaries). Further interviews in this same segment will likely repeat these patterns rather than surface new ones.

The synthesis is ready for your product roadmap and OST updates.

### Artifacts written

#### `work/docs/product/synthesis-activation-window-1.md`

```
# Interview synthesis: activation (window 1)

## Window

| Participant | Segment | Type | Date |
|---|---|---|---|
| Priya | Mobile-first freelancer | generative | 2026-05-12 |
| Marco | Desktop ops lead (2-person team) | generative | 2026-05-14 |
| Dana | Desktop freelancer | generative | 2026-05-19 |
| Sam | Mobile-first bookkeeper | generative | 2026-05-21 |
| Lena | Desktop ops manager (mid-market) | generative | 2026-05-26 |

## Themes

| Theme (need-level) | Participants supporting | Disconfirming | Discard rate |
|---|---|---|---|
| Mobile-responsive bank feed connection required for mobile-first segment | 2/5 (Priya, Sam) | 3/5 (Marco, Dana, Lena—all desktop, no mobile issue) | 60% |
| Post-action confirmation + sense of completion required after data import | 2/5 (Marco, Lena) | 1/5 (Dana—completed, saw data appear, no confusion) | 20% |
| Feature discoverability: users unsure which features are free vs paid-only | 1/5 (Dana) | 0/5 explicit disconfirmation | 0% |

## Pattern notes

**Theme 1: Mobile responsiveness**
- Priya (INT-01): Bank feed connection opened "tiny window that didn't work on mobile." Abandoned account setup. Fell back to spreadsheet for that client. Quote: "I wish it just worked on mobile like everything else does."
- Sam (INT-04): Bank feed connection "bounced me to some screen that clearly expected a desktop browser—button half off the edge." Abandoned setup. Quote: "Everything else I run my business on works on my phone. This one step didn't, so it stalled."
- **Code:** Mobile-first users need the primary onboarding action (bank connection) to work on their device of choice. Forcing desktop breaks their workflow expectation and triggers abandonment.

**Theme 2: Post-action feedback gap**
- Marco (INT-02): CSV import provided no success signal. "I honestly couldn't tell if it had worked, so I uploaded it again. And again. Then I had three copies of every transaction and spent an hour cleaning it up." Quote: "There was no 'you're done, this worked' moment. I was flying blind."
- Lena (INT-05): Data loaded successfully, but dashboard appeared empty with no completion signal. "I had no sense of whether I'd set it up right or whether something was still missing. I kept poking around expecting a 'next step'." Quote: "It loaded, but I had no idea if I'd actually finished setting it up."
- **Dana disconfirms:** She connected her bank feed, "saw her data appear" on the dashboard—no confusion about completion.
- **Code:** Users who complete an import/data-load action need explicit confirmation that the action succeeded AND a clear signal that their next step is defined (not "keep exploring"). Without it, they doubt the product and/or duplicate actions.

**Theme 3: Feature discoverability** (single case, not yet a theme)
- Dana (INT-03): "I went looking for where to add Jess and couldn't find it. I assumed it was one of those things you only get if you pay more, so I left it." Quote: "I couldn't find the invite thing, figured it was a paid feature, gave up."
- **Code:** Unclear or hidden feature locations trigger negative assumptions (paywall) and abandonment. Needs 1+ additional case to become a theme.

## OST updates

Assuming the current OST has a root outcome of "new user successfully onboards team + connects data by end of week one":

| Change | Node | Source interviews | Evidence |
|---|---|---|---|
| Add opportunity | **Mobile-first users can complete bank feed connection on their phone** | INT-01 (Priya), INT-04 (Sam) | Two mobile-first freelancers abandoned setup when forced to desktop for bank feed auth. Both cited mobile-first workflow expectations. Both fell back to legacy systems. Activation blocker for this segment. |
| Add opportunity | **User receives explicit confirmation that data import/load succeeded + knows their next step** | INT-02 (Marco), INT-05 (Lena) | Two users completed the technical action but had high doubt about success. Marco duplicated the import three times due to absent feedback. Lena explored the dashboard looking for a "next step" signal. Adds friction and disengagement risk post-onboarding. |
| Monitor | Feature discoverability (free vs paid assumption) | INT-03 (Dana) | Single case. Dana assumed invite feature was paid-only and abandoned it. Needs 1+ additional case to establish as a pattern. Flag for next window. |

## Saturation call

**Status: Continue → targeted concept testing rather than more generative discovery**

**Reasoning:**
- 5 interviews across a mixed-segment window (2 mobile-first, 3 desktop) have surfaced 2 clear, distinct themes (mobile connection, confirmation feedback) with strong, traceable participant support
- The 60% discard rate on mobile responsiveness is expected and healthy: it's a segment-specific blocker (mobile-first segment only), not a universal activation issue
- The 20% discard rate on post-action feedback is minimal (Dana is the only user who completed without confusion, and she did see her data appear—the confirmation came implicitly)
- Theme 3 (discoverability) remains a single-case anecdote. It's worth tracking but doesn't yet warrant design action
- Further generative interviews in this same "freelancer/ops team" segment are unlikely to yield new themes; repeats of the mobile and confirmation issues are likely
- **Next move:** Shift to concept testing. Validate fix directions for mobile responsiveness (responsive auth flow? native bank auth options?) and post-action feedback (success toast? dashboard education? next-step prompt?). Return to generative discovery only if concept testing uncovers new constraints or reveals unmet needs in a different segment (e.g., larger enterprises, specific verticals, accountant-vs-bookkeeper differences).

```

#### `work/docs/product/interviews/int-03-dana.md`

```
# Interview INT-03 — Dana

| Field | Value |
|-------|-------|
| Participant | Dana, sole-trader accountant |
| Segment | Desktop freelancer |
| Type | generative |
| Date | 2026-05-19 |

## Notes

Dana set up on desktop and connected her bank feed without trouble — "that part was fine, took a couple of
minutes." Her issue was inviting her business partner: "I went looking for where to add Jess and couldn't
find it. I assumed it was one of those things you only get if you pay more, so I left it."

Quote: "I couldn't find the invite thing, figured it was a paid feature, gave up."

Note: Dana did NOT report any mobile or import-confirmation problem — she connected fine on desktop and saw
her data appear. This is a disconfirming case for the mobile-connection theme (she's desktop) and she had no
confirmation complaint.

```

#### `work/docs/product/interviews/int-04-sam.md`

```
# Interview INT-04 — Sam

| Field | Value |
|-------|-------|
| Participant | Sam, mobile-first bookkeeper |
| Segment | Mobile-first freelancer |
| Type | generative |
| Date | 2026-05-21 |

## Notes

Sam started connecting a bank feed on his phone on the first day. "It bounced me to some screen that clearly
expected a desktop browser — there was a button half off the edge of the screen. I closed it and figured I'd
sort it out later." He hadn't, a fortnight on.

Quote: "Everything else I run my business on works on my phone. This one step didn't, so it stalled."

Asked about import confirmation: "I never got that far — couldn't connect the feed in the first place."

```

#### `work/docs/product/interviews/int-02-marco.md`

```
# Interview INT-02 — Marco

| Field | Value |
|-------|-------|
| Participant | Marco, ops lead (2-person finance team) |
| Segment | Desktop ops lead |
| Type | generative |
| Date | 2026-05-14 |

## Notes

Marco imported a CSV on day one from his desktop. The import "just sat there" with no confirmation. "I
honestly couldn't tell if it had worked, so I uploaded it again. And again. Then I had three copies of every
transaction and spent an hour cleaning it up."

Quote: "There was no 'you're done, this worked' moment. I was flying blind."

Asked what would have helped: "Just tell me it worked. A tick. Anything."

```

#### `work/docs/product/interviews/int-01-priya.md`

```
# Interview INT-01 — Priya

| Field | Value |
|-------|-------|
| Participant | Priya, freelance bookkeeper |
| Segment | Mobile-first freelancer |
| Type | generative |
| Date | 2026-05-12 |

## Notes

Priya signed up on her phone between client visits. On day one she tried to connect a client's bank feed.
"I got to the bit where it wanted me to log into the bank and it just... opened a tiny window that didn't
work on my phone. I told myself I'd do it later on the laptop." She never did — three weeks later the
account still had no data source connected.

Quote: "I wish it just worked on mobile like everything else does."

Asked what she did instead last time she needed the data: "I kept using my spreadsheet for that client. It's
annoying but at least it works on my phone."

```

#### `work/docs/product/interviews/int-05-lena.md`

```
# Interview INT-05 — Lena

| Field | Value |
|-------|-------|
| Participant | Lena, ops manager (mid-market) |
| Segment | Desktop ops manager |
| Type | generative |
| Date | 2026-05-26 |

## Notes

Lena got through import on desktop without an issue technically — the data loaded. But: "the dashboard was
just empty-looking afterwards. I had no sense of whether I'd set it up right or whether something was still
missing. I kept poking around expecting a 'next step'."

Quote: "It loaded, but I had no idea if I'd actually finished setting it up."

No mobile issue (she's desktop). Her complaint is about the lack of a post-setup confirmation / sense of
completion — same underlying need as Marco, different surface symptom.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 13.0/13.0 (100%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 59856 ms |
| Target cost | $0.0928 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Reads the staged interview notes and assembles the window (participant, segment, type, date) | PASS | Window table lists all 5 participants with segment (e.g. 'Mobile-first freelancer'), type ('generative'), and date (e.g. 2026-05-12) for each. |
| c2 | Codes at the NEED/behaviour level, not feature requests — translates "I wish it had a bulk button" up to the underlying need | PASS | Each pattern has a 'Code:' line elevating to need: 'Mobile-first users need the primary onboarding action to work on their device of choice' and 'Users who complete an import need explicit confirmation that the action succeeded.' |
| c3 | Promotes a pattern to a theme only when multiple participants support it — a single vivid quote is an anecdote, not a theme | PASS | Themes 1 and 2 both have 2/5 support; Theme 3 (Dana) is explicitly labelled '(single case, not yet a theme)' in the pattern notes. |
| c4 | Actively seeks disconfirming evidence and reports a discard rate — flags a zero-discard theme as a possible confirmation-bias artifact | PASS | Themes table has 'Disconfirming' and 'Discard rate' columns: Theme 1 60%, Theme 2 20%, Theme 3 0%. No confirmed theme has 0% discard — the 0% case is already an unconfirmed anecdote. |
| c5 | Correctly distinguishes the cross-participant themes (mobile bank-feed failure; no setup confirmation) from the single-participant anecdote (invite discoverability) | PASS | Themes 1 (Priya, Sam) and 2 (Marco, Lena) are confirmed themes; Dana's discoverability issue is explicitly '(single case, not yet a theme)' and listed as 'Monitor' in OST. |
| c6 | Maps themes onto OST changes — add / strengthen / flag-contradicted — each change citing the interviews it came from | PASS | OST updates table uses 'Add opportunity' (citing INT-01/INT-04, INT-02/INT-05) and 'Monitor' (INT-03 Dana) — each entry has a 'Source interviews' column and 'Evidence' column. |
| c7 | Makes an explicit saturation call (continue vs saturated) based on the rate of new themes, not a feeling | PASS | 'Saturation call' section: 'Continue → targeted concept testing... Further generative interviews in this same segment are unlikely to yield new themes; repeats of the mobile and confirmation issues are likely.' |
| c8 | Notes the mixed segment as a reason themes may not be saturating, recommending a narrower segment | PARTIAL | Saturation call notes '2 mobile-first, 3 desktop' mix and that mobile theme is 'segment-specific'. Future generative discovery in 'a different segment (e.g. larger enterprises)' is mentioned as conditional, not as a primary recommendation. |
| c9 | Output file exists under `docs/product/` with a window table, a themes table (with participant support counts and discard rate), an OST-updates table, and a saturation call | PASS | File `work/docs/product/synthesis-activation-window-1.md` contains all four required sections: window table, themes table with support counts and discard rates, OST-updates table, and saturation call. |
| c10 | Themes are need-level, and each cites the participants/interviews supporting it | PASS | Themes table column 'Participants supporting' lists names and IDs. OST table 'Source interviews' cites INT-01/INT-04 and INT-02/INT-05 by ID and name. |
| c11 | The single-participant invite-discoverability signal is treated as an anecdote to watch, not promoted to a confirmed theme | PASS | Saturation call: 'Theme 3 (discoverability) remains a single-case anecdote. It's worth tracking but doesn't yet warrant design action.' OST action is 'Monitor', not 'Add opportunity'. |
| c12 | A discard rate / disconfirmation check appears for the themes — not an all-confirming synthesis | PASS | Themes table has explicit 'Disconfirming' column (e.g. '3/5 (Marco, Dana, Lena—all desktop)') and 'Discard rate' column (60%, 20%, 0%). Dana's disconfirming case for Theme 2 is called out in pattern notes. |
| c13 | The saturation call is stated as a decision with reasoning (rate of new themes), not omitted | PASS | 'Status: Continue → targeted concept testing rather than more generative discovery' followed by 5 bullet reasoning points including likelihood of repeats and theme count. |
| c14 | OST changes cite source interviews rather than appearing as unsourced assertions | PARTIAL | OST table has 'Source interviews' column (e.g. 'INT-01 (Priya), INT-04 (Sam)') and 'Evidence' column with per-row rationale. Citations are present and traceable. |

### Notes

The synthesis is exceptionally well-executed: every structural element (window table, need-level coding, disconfirmation column with discard rates, OST mapping, saturation call) is present and correctly populated. The only partial is c8, where the mixed-segment observation is noted but the recommendation to specifically pursue a narrower-segment generative window is stated conditionally rather than as a primary next step.
