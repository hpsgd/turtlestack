# Test: define-north-star resists a vanity metric on a two-sided marketplace

Scenario: Leadership wants a cumulative vanity count as the North Star for a two-sided marketplace. The skill must
anchor to the matched value exchange, reject the vanity metric, run a Goodhart check with a concrete gaming
scenario, run a multi-customer-type coherence check across both sides, and derive leading, controllable input
metrics — each with a real definition block.

## Prompt

/product-analyst:define-north-star Plotline — a two-sided marketplace that matches freelance video editors with content creators who need editing done. Leadership wants to make "total registered users" the North Star because the number only ever goes up and looks strong in board decks. Write the North Star canvas to {workspace}/work/docs/analytics/north-star.md.

## Criteria

- [ ] PASS: States a customer value moment anchored to an observable event — a completed, delivered editing job where both sides win — not a signup, a login, or a pageview
- [ ] PASS: Explicitly rejects "total registered users" as a North Star, naming it a cumulative vanity metric that rises regardless of product quality
- [ ] PASS: Proposes a North Star that captures the matched value exchange (a completed editing transaction), not one side's activity in isolation
- [ ] PASS: Runs a Goodhart check — writes out a concrete gaming scenario for the proposed metric and a verdict (survives / counter-metric added / rejected)
- [ ] PASS: Runs a multi-customer-type coherence check across BOTH sides (editors and creators), stating for each whether the metric going up is good
- [ ] PASS: Derives 3-5 input metrics, each leading (moves before the North Star) and controllable (a team can move it) — not lagging outcomes or reporting lines nobody can influence
- [ ] PASS: Every metric (North Star and each input) carries a definition block — at minimum calculation, granularity, filters, and time window — not just a name
- [ ] PARTIAL: Adds a counter-metric / guardrail when the Goodhart check surfaces a gaming risk

## Output expectations

- [ ] PASS: Output is structured as a North Star canvas — value moment, North Star with definition, Goodhart verdict, coherence table, input metrics
- [ ] PASS: The coherence table lists each customer type (editor and creator) with an explicit is-up-good verdict per side
- [ ] PASS: Filters/exclusions (bots, test accounts, internal users) are explicit in the definition block, not silently assumed
- [ ] PARTIAL: Links the North Star to an OKR owned by the product-manager rather than inventing or rewriting OKRs
