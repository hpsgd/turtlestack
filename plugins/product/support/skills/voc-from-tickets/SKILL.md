---
name: voc-from-tickets
description: Extract Voice-of-Customer product themes from support tickets — code ticket text into product themes, separate UX-failure signal from doc-gap signal, weight themes by frequency × severity, and surface a ranked theme list for the roadmap. Use when support-ticket volume needs to feed product decisions, not just be resolved.
argument-hint: "[path to support tickets, a triaged batch, or 'recent' to scan the issue tracker]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

# Voice of customer from tickets

Extract product themes from the support tickets in $ARGUMENTS. This is the support team's Voice-of-Customer lens: support sits closest to the user's words at the moment something goes wrong, and that raw signal carries product intelligence that triage and resolution alone throw away. The marketplace runs a distributed-VoC model — each role (support, customer-success, UX research, GTM) holds its own VoC lens, and the overlap is deliberate. A theme this skill surfaces from tickets may also appear in churn signal or review mining; conflict between those lenses is information, not error.

This skill is the ticket-theme-extraction lens specifically. It is narrower than `/support:feedback-synthesis`, which synthesises across all feedback channels (tickets, reviews, surveys, NPS, social). Run this skill to turn a ticket corpus into product themes; hand its output to feedback-synthesis when those themes need merging with non-ticket sources. It is distinct from `/support:triage-tickets`, which routes individual tickets reactively — triage answers "who fixes this ticket now," this skill answers "what is the ticket corpus telling product to build."

## Step 1 — Assemble the ticket corpus

Read every ticket in scope. If pointed at files or a directory, use `Glob` and `Read`; if pointed at an issue tracker export, parse it; if given inline tickets, parse directly. Tickets already triaged by `/support:triage-tickets` are the ideal input — reuse their category and severity rather than re-deriving.

Record the corpus boundary before coding anything:

- **Ticket count** — total tickets in scope
- **Date range** — earliest to latest (or "undated" where absent)
- **Source** — which queue, product area, or tracker the tickets came from
- **Segment data available** — plan tier, tenure, role, if present

A corpus under 30 tickets is a small sample. Note it now and caveat every conclusion later. Do not invent tickets to reach a threshold.

## Step 2 — Code each ticket into a product theme

Coding means assigning each ticket a theme drawn from the user's own words, not internal jargon. Read the ticket body, not just its subject line — the subject is often the user's guess at the cause, while the body holds the actual behaviour.

For each ticket capture:

- **Ticket ID** — reuse the existing ID or assign a sequential one
- **Verbatim phrase** — the exact words that name the problem (do not paraphrase)
- **Theme** — a short user-language label (e.g. "can't find where to cancel," "export silently drops rows")
- **Product area** — the feature or surface the ticket touches

Theme-naming rules:

- Use what the user said. "Can't find the cancel button" — not "cancellation discoverability gap."
- One ticket, one primary theme. If a ticket genuinely raises two distinct problems, split it into two coded entries.
- Keep themes specific. "Billing is confusing" is too broad to act on; "doesn't understand proration on mid-cycle upgrade" is a theme product can fix.

## Step 3 — Classify the signal type

This is the core discrimination this skill exists to make. A ticket where the user couldn't do the thing can mean two very different product actions, and conflating them sends work to the wrong place. For every coded ticket, assign exactly one signal type:

| Signal type | The user... | Tell-tale phrasing | Product action |
|---|---|---|---|
| **UX failure** | could not complete the task because the product made it hard, hidden, or error-prone | "I clicked everywhere," "there's no button for," "it let me save an invalid," "I assumed X would happen and it didn't" | Redesign the flow, surface, or affordance — owned by product/design |
| **Doc gap** | could have completed the task but did not know how; the capability exists and works | "how do I," "is it possible to," "where is the setting for," "I didn't realise you could" | Write or improve docs/onboarding — owned by docs/support |
| **Missing capability** | wanted something the product does not do at all | "it would be great if," "can you add," "I wish it could" | Feature request — feeds the roadmap |
| **Defect** | hit something genuinely broken against documented behaviour | error messages, crashes, data loss, "it worked yesterday" | Bug fix — owned by engineering |

The hard call is UX-failure versus doc-gap. The discriminator is whether the capability exists and works:

- If the user fought the interface to do something the product supports, it is a **UX failure** even if a help article would have rescued them. A flow that needs a help article to be usable is a design defect, not a docs defect.
- If the user simply did not know a working, discoverable-once-known feature existed, it is a **doc gap**.
- When the same theme produces both signals across different tickets (some users found it confusing, some just didn't know), record the split count — that split is itself a finding (e.g. "12 tickets: 8 UX-failure, 4 doc-gap" means fix the flow first, then the docs).

Anti-pattern: defaulting confusing-experience tickets to "doc gap" because writing an article is cheaper than redesigning a flow. That buries a UX failure behind a help article and the tickets keep coming.

## Step 4 — Cluster and count themes

Group coded tickets into themes. A theme needs 2+ tickets; a single ticket is an outlier, listed separately. For each theme record:

- **Ticket count** and **percentage of corpus**
- **Signal-type breakdown** — how many UX-failure / doc-gap / missing-capability / defect tickets
- **Segment concentration** — is the theme concentrated in one segment (e.g. "9 of 11 from trial users in week one")? Note it; absence of concentration is also worth stating.
- **Trend** — if dates exist, is the theme increasing, stable, or decreasing across the window? If not, state "trend unknown."

## Step 5 — Weight by frequency × severity

Rank themes so product reads them in priority order. Score each theme:

**Theme weight = Frequency × Severity × Segment factor**

Where:

- **Frequency** = the ticket count for the theme (use the raw count).
- **Severity** = the worst user-impact in the theme: Blocks core task (4), Forces a painful workaround (3), Slows the user down (2), Annoyance only (1). Severity is about user impact, not ticket volume — a 3-ticket theme that blocks signup can outweigh a 20-ticket cosmetic theme.
- **Segment factor** = paid/enterprise concentration (1.5×), mixed or unknown (1.0×). Justify any non-1.0 factor with the segment data from Step 4 — never apply it on a hunch.

Sort themes by weight, descending. Show the arithmetic for each so the ranking is auditable, not asserted.

## Step 6 — Surface themes for the roadmap

Produce the ranked output below. For the top themes, write a roadmap-ready line: the theme, the signal type (which determines who owns it), the evidence, and the reach. Stop at the themes that clear a weight worth a product conversation — do not pad the list to a round number.

Hand-off rules:

- UX-failure and missing-capability themes go to product/the product-owner for roadmap consideration.
- Doc-gap themes go to docs/support — and where a doc-gap theme is large, flag a `/support:write-kb-article` candidate.
- Defect themes go to engineering via `/support:triage-tickets`' bug-report path; do not re-document them here.
- Cross-pollinate: name where this corpus agrees or conflicts with another VoC lens (churn signal, reviews) if that data is to hand. Surface the conflict; do not resolve it.

## Rules

- Code from the ticket body, not the subject line. The subject is the user's diagnosis; the body is the evidence.
- Never collapse UX-failure signal into doc-gap signal to make the fix cheaper. If the flow needs an article to be usable, the flow is the defect.
- Preserve verbatim phrases. The moment you paraphrase "it just spins forever" into "performance concern," you have destroyed the signal that made it a VoC artifact.
- Severity is user impact, not ticket count. Frequency already carries volume; don't double-count it as severity.
- Don't manufacture themes from a thin corpus. Under 30 tickets, present findings as directional and say so explicitly.
- Report what users said, not what the roadmap wants to hear. A theme that contradicts a planned direction is exactly the theme product needs to see.
- Keep this lens to tickets. When the question needs reviews, surveys, or NPS folded in, that is `/support:feedback-synthesis`' job — hand off rather than reaching outside the ticket corpus.

## Output Format

```
## VoC from tickets — [source / product area]

### Corpus
- Tickets analysed: [N]
- Date range: [earliest] to [latest]
- Source: [queue / tracker / product area]
- Sample caveat: [none | "small sample (<30) — directional only"]

### Theme table (ranked by weight)

| Rank | Theme (user language) | Signal mix | Count | % | Severity | Segment | Weight | Trend |
|---|---|---|---|---|---|---|---|---|
| 1 | "..." | UX 8 / Doc 4 | 12 | 24% | 4 | trial wk1 | 72 | rising |

### Signal-type split

- UX failure: [N] tickets across [N] themes
- Doc gap: [N] tickets across [N] themes
- Missing capability: [N] tickets across [N] themes
- Defect: [N] tickets across [N] themes

### Roadmap-ready themes

For each theme worth a product conversation:

#### [Rank]. [Theme in user language]
- Signal type: [UX failure | doc gap | missing capability] → owner: [product | docs | engineering]
- Evidence: [2-3 verbatim phrases with ticket IDs]
- Reach: [N tickets / N% of corpus], concentrated in [segment or "broad"]
- Weight: [frequency] × [severity] × [segment factor] = [score]
- Recommended action: [specific — "redesign the cancel flow to surface the button on the billing page," not "improve cancellation UX"]

### Hand-offs
- To product (roadmap): [themes]
- To docs (`/support:write-kb-article` candidates): [doc-gap themes]
- To engineering (`/support:triage-tickets`): [defect themes]
- To `/support:feedback-synthesis`: [themes needing merge with reviews/surveys/NPS]

### Cross-lens notes
[Where this ticket corpus agrees with or contradicts another VoC lens — churn signal, review mining. Surface conflict; do not resolve it.]

### Outliers
[Single-ticket signals worth watching — novel requests, early warnings — that didn't form a theme.]
```

## Related Skills

- `/support:feedback-synthesis` — the broader synthesis lens. This skill extracts themes from tickets only; feedback-synthesis merges theme output with reviews, surveys, NPS, and social. Run this first when the input is tickets, then hand themes upward.
- `/support:triage-tickets` — reactive, per-ticket routing. Triage feeds this skill (its category/severity are reusable input); this skill is the retrospective product-signal pass over a triaged batch.
- `/support:write-kb-article` — the destination for large doc-gap themes surfaced in Step 6.
