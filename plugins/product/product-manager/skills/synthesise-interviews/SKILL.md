---
name: synthesise-interviews
description: "Pattern-code a window of discovery interviews into themes, update opportunity solution tree nodes, and flag theme saturation. Produces a synthesis that turns raw interview notes into discovery decisions. Use after running several interviews to convert conversation into opportunity nodes."
argument-hint: "[the set of interviews or the time window to synthesise]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Synthesise the interviews in $ARGUMENTS.

Discovery without synthesis is just conversation. This skill turns a window of interviews into themes, maps
those themes onto the [Opportunity Solution Tree](https://www.producttalk.org/opportunity-solution-trees/),
and flags when themes have saturated — the point where new interviews stop yielding new themes. It is the
analysis counterpart to the generative interview (`/product-manager:write-interview-guide`) and switch
interview (`/product-manager:switch-interview`) skills.

Follow every step. The output is a synthesis with updated OST nodes and a saturation call.

## Step 1: Assemble the interview window

Gather the interviews to synthesise — typically the last three to four, matching the OST update cadence, or
a defined window from `docs/product/discovery-log.md`. List participant, segment, interview type, and date.
This step is complete when the window is listed.

## Step 2: Pattern-code the notes

Read every interview and tag recurring observations. Code at the level of customer need and behaviour, not
solution requests:

- A customer saying "I wish it had a bulk button" → code the underlying need: "reconciling records one at a
  time is too slow at their volume", not "wants a bulk button"
- Tag each coded observation with the participant it came from, so a theme's support is traceable

Group codes into themes. A theme is a pattern seen across multiple participants, not a single strong quote.
This step is complete when observations are coded and grouped into candidate themes.

## Step 3: Test each theme for support and disconfirmation

For each theme, count how many participants support it and actively look for disconfirming evidence — a
participant who didn't have the problem, or solved it differently. A theme every participant supports with
zero discards is a warning: it may be a confirmation-bias artifact of leading questions rather than a real
pattern. Note the discard rate. This step is complete when every theme has a support count and a
disconfirmation check.

## Step 4: Update the opportunity solution tree

Map themes onto the OST (`/product-manager:write-opportunity-solution-tree`). For each theme that meets the
branch criteria (connected to the outcome, surfaced by research, specific enough to act on):

- New pattern → add an opportunity node, citing the interviews
- Strengthened pattern → note the added evidence on the existing node
- Contradicted pattern → flag the node for review; don't silently keep it

This step is complete when the OST reflects the window's evidence and every change cites its interviews.

## Step 5: Call theme saturation

Compare this window's themes to prior windows. If new interviews are producing themes already on the tree
and few or no new ones, the segment is approaching saturation (typically 20-30 interviews across a
homogeneous segment reaches 90-95%). State whether to:

- **Continue** in this segment (still finding new themes)
- **Saturated** — move to a new segment or shift from generative to evaluative/concept testing

This step is complete when a saturation call is recorded.

## Rules

- **Code needs, not feature requests.** A customer's proposed solution is data about their need, not a
  requirement. Always translate up to the underlying job.
- **A theme needs multiple participants.** One vivid quote is an anecdote. A pattern across participants is
  a theme. Don't promote anecdotes.
- **Actively seek disconfirmation.** A zero-discard synthesis means the interviews were confirmatory. Note
  who didn't fit the theme.
- **Every OST change cites its interviews.** An opportunity node with no source is an assumption wearing a
  research costume.
- **Saturation is a decision, not a feeling.** Base it on the rate of new themes, and write the call down.
- **Don't synthesise toward your prior plan.** If every theme conveniently supports what you already wanted
  to build, re-examine the coding.

## Output Format

Write to `docs/product/synthesis-[window].md`:

```markdown
# Interview synthesis: [window]

## Window
| Participant | Segment | Type | Date |
|-------------|---------|------|------|
| ... | ... | generative / switch | ... |

## Themes
| Theme (need-level) | Participants supporting | Disconfirming | Discard rate |
|--------------------|-------------------------|---------------|--------------|
| ... | 4/5 | 1 | 20% |

## OST updates
| Change | Node | Source interviews |
|--------|------|-------------------|
| Added opportunity | ... | ... |
| Strengthened | ... | ... |
| Flagged (contradicted) | ... | ... |

## Saturation call
[Continue in segment / Saturated — move to next segment] — [reasoning based on rate of new themes]
```

## Related Skills

- `/product-manager:write-interview-guide` — the generative interviews this synthesises.
- `/product-manager:switch-interview` — switch interviews also feed this synthesis.
- `/product-manager:write-opportunity-solution-tree` — the artifact this skill updates.
- `/product-manager:strategic-voc-synthesis` — validates synthesised hypotheses against broader VoC signal.
