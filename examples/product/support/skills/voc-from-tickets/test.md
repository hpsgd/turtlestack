# Test: Voice of customer from tickets

Scenario: A support team has a month of tickets and wants them to feed product decisions, not just be resolved. The corpus contains a cancel-discoverability theme (users fought the interface — UX failure), an onboarding empty-state theme (UX failure, concentrated in trial week-one users), a CSV-export-silently-drops-rows theme (data-loss defect, concentrated in paid tiers), several how-to questions about features that exist and work (doc gaps), and assorted feature requests (missing capability). The skill must code the tickets, discriminate UX-failure from doc-gap signal, weight themes by frequency × severity, and surface a ranked roadmap-ready list.

## Prompt

A month of support tickets is on disk at `{workspace}/work/tickets/support-tickets-may.md`. Read it.

/support:voc-from-tickets {workspace}/work/tickets/support-tickets-may.md

Run the full skill: assemble the corpus, code each ticket into a product theme from the user's own words, classify the signal type (UX failure / doc gap / missing capability / defect), cluster and count themes, weight each by frequency × severity (× segment factor), and surface the ranked roadmap-ready themes with hand-offs. Use the skill's Output Format.

## Criteria

- [ ] PASS: Records the corpus boundary first — ticket count, date range, source — before coding any themes
- [ ] PASS: Codes tickets from the body using user-language theme labels (e.g. "can't find where to cancel"), preserving verbatim phrases, not internal jargon
- [ ] PASS: Classifies the cancel-discoverability tickets as UX failure (users "clicked everywhere", the affordance is hidden) — NOT collapsed into a doc gap because an article would have rescued them
- [ ] PASS: Classifies the SSO / recurring-tasks / PDF-export how-to tickets as doc gaps — the capability exists and works, the user just didn't know how — distinct from the UX-failure tickets
- [ ] PASS: Classifies the CSV-export-drops-rows tickets as a defect (silent data loss against expected behaviour), not as a doc gap or feature request
- [ ] PASS: Classifies the feature requests (dark mode, calendar view, API rate-limit headers, bulk delete) as missing capability, routed to the roadmap
- [ ] PASS: Weights themes by frequency × severity (severity = user impact, not ticket volume) so a high-impact theme can outrank a higher-volume low-impact one — and shows the arithmetic
- [ ] PASS: Applies a paid/enterprise segment factor where justified by the segment data (e.g. the export-data-loss theme concentrated in paid tiers) rather than on a hunch
- [ ] PASS: Notes segment concentration where present — onboarding-confusion in trial week-one users, export-data-loss in paid tiers
- [ ] PASS: Treats this as the support ticket lens — hands defect themes to engineering and large doc-gap themes toward write-kb-article, rather than absorbing all feedback channels
- [ ] PARTIAL: For a theme that splits across signal types (some UX-failure, some doc-gap tickets), records the split count rather than forcing one classification

## Output expectations

- [ ] PASS: Output follows the skill's Output Format — corpus block, ranked theme table (with signal mix, count, %, severity, weight), signal-type split, roadmap-ready themes, and hand-offs
- [ ] PASS: Output's ranked theme table shows the frequency × severity (× segment) arithmetic per theme so the ranking is auditable, and routes each theme by signal type to the correct owner (product / docs / engineering)
