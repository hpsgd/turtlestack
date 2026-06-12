# Test: write-product-vision pressure-tests the Pichler board, not just fills it

Scenario: The CPO is asked to write a product vision for a new product entering a market. The skill must
produce all five Pichler Vision Board cells (vision, target group, needs, product, business goals), but the
quality bar is that it *argues* each cell — pressure-tests the vision against the "survives feature
replacement" check, names a specific recruitable target group (not "everyone"), labels needs as
evidenced/assumed/to-validate rather than presenting guesses as facts, keeps the product cell to three to
five differentiating characteristics (not a feature list), and runs the cross-cell coherence check. A board
that merely fills five boxes with plausible sentences must not score well.

## Prompt

Use the cpo `write-product-vision` skill to write a one-page product vision for "Tideline", a new
appointment-and-records product aimed at solo and very small allied-health clinics (physiotherapists,
podiatrists, dietitians) who currently run their books on paper or a shared spreadsheet. There is no prior
vision on file. Treat customer demand as largely unvalidated — you have interviewed only a handful of
clinicians so far.

Write the vision artifact to `docs/strategy/product-vision-tideline.md` (a relative path under the current
working directory). Respond in the skill's standard format — the vision board plus the written file. Proceed
without asking; do not stop to request more context.

## Criteria

- [ ] PASS: Establishes context first — names scope (one product), a 2-5 year horizon, the trigger (new product / new market), and that prior evidence was checked — before filling any cell
- [ ] PASS: All five Pichler cells are present and named — vision, target group, needs, product, business goals — none collapsed or omitted
- [ ] PASS: The vision cell describes a change in the world (what it makes possible for the clinics), not a product description, and avoids "best / leading / world-class / seamless"
- [ ] PASS: Pressure-tests the vision — applies the "would survive replacing every current feature" / "still true if a competitor shipped the same product" check, not just asserting the statement
- [ ] PASS: Target group is specific and recruitable (e.g. "solo physios running bookings on paper/spreadsheet"), explicitly NOT "everyone"; distinguishes user from paying customer if they differ
- [ ] PASS: Needs are stated as customer problems (not features), limited to two or three core needs, and EACH is tagged `[evidenced]` / `[assumed]` / `[to validate]` — given demand is unvalidated, at least one need is honestly marked assumed or to-validate
- [ ] PASS: Product cell is three to five differentiating CHARACTERISTICS, explicitly not a feature/backlog list, and each characteristic is cross-checked against a stated need
- [ ] PASS: Business goals are stated as business outcomes (revenue, market position, retention), two to four of them, not vanity metrics like "acquire many users"
- [ ] PASS: Runs the cross-cell coherence check (target↔needs, needs↔product, product↔goals, above-roadmap altitude, evidence honesty) rather than checking each cell only in isolation
- [ ] PASS: Holds CPO ownership — frames the vision as CPO-authored with PM/discovery providing slice input, not delegated authoring
- [ ] PASS: Names what is unknown (open questions) rather than fabricating evidence to fill gaps

## Output expectations

- [ ] PASS: Output writes the vision file to `docs/strategy/product-vision-tideline.md` under the working directory, on one page, with the five board sections as named headings
- [ ] PASS: The written file's needs section carries explicit `[evidenced|assumed|to validate]` tags per need, and the product section lists characteristics not features — demonstrating the argue-not-box-tick bar
