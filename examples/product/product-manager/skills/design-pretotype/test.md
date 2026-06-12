# Test: design-pretotype states an MEH in XYZ form and measures skin-in-the-game

Scenario: A PM wants to test demand for a bet cheaply before any build. The skill must state a Market
Engagement Hypothesis in XYZ form (X% of Y will do Z) with a threshold committed before running, pick the
cheapest pretotype that yields behavioural data, define a skin-in-the-game metric (likes/verbal enthusiasm
score zero), specify the run, and pre-commit the proceed/kill decision.

## Prompt

Use the product-manager `design-pretotype` skill to design a pretotype experiment to test whether there's
real demand for a "bulk-retry-and-reconcile" view before we build it. The product has logged-in users.
Write the experiment to a file under `docs/product/` in the current working directory, in the skill's
standard format.

Proceed without asking — produce the pretotype design.

## Criteria

- [ ] PASS: States a Market Engagement Hypothesis in XYZ form — "X% of Y will do Z" — specific on audience, behaviour, and threshold
- [ ] PASS: Commits the X threshold BEFORE running, and says so explicitly (a threshold chosen after seeing results proves nothing)
- [ ] PASS: Picks a specific pretotype (e.g. fake door / smoke test / concierge / Wizard of Oz) and justifies why it fits this hypothesis — the cheapest one that yields behavioural data
- [ ] PASS: Defines a skin-in-the-game metric — a real action (clicks, email entry, money, time) — and explicitly rejects likes / verbal enthusiasm / "would you use it" as zero-signal
- [ ] PASS: Specifies the run: audience (matching Y), sample size, duration, and stop condition — small and fast
- [ ] PASS: Pre-commits the decision rule — above threshold → proceed; below → kill or pivot — written before running
- [ ] PASS: If a fake door is used, handles the dead end gracefully (a "coming soon / notify me" rather than a broken page) and avoids running at trust-eroding scale
- [ ] PARTIAL: Distinguishes pretotype (should we build it) from prototype (can we build it right); flags any ad/tool spend

## Output expectations

- [ ] PASS: Output file exists under `docs/product/` with an MEH in "X% of Y will Z" form and the threshold marked as pre-committed
- [ ] PASS: A specific pretotype type is chosen with a fit rationale, not a generic "run an experiment"
- [ ] PASS: The measured metric is a behaviour (an action taken), and stated intent / likes are explicitly excluded as evidence
- [ ] PASS: The run spec includes audience, sample size, duration, and stop condition
- [ ] PASS: A pre-committed proceed/kill decision rule is recorded against the threshold
- [ ] PARTIAL: Any paid tool / ad spend is flagged, and pretotype-vs-prototype is distinguished
