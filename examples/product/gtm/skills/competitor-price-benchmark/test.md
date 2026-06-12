# Test: competitor-price-benchmark normalises to like-for-like and analyses packaging/tiering

Scenario: GTM is asked to benchmark competitor pricing across a named set. The skill must lead with the value
metric each competitor charges on, capture published pricing with dates, then do the work that separates a
benchmark from a list: normalise to a like-for-like scenario (including "us"), show the crossover point where
a cheaper-at-small competitor flips to dearer-at-scale, and analyse packaging/tiering to find standard gating
and whitespace. It must hold the GTM-owns / product-manager-consults / human-approves chain, treat hidden
enterprise pricing as a finding, and never output a price recommendation.

## Prompt

Use the gtm `competitor-price-benchmark` skill to benchmark pricing for "Tideline", an appointment-and-records
product for small allied-health clinics, against three named direct competitors plus the do-nothing substitute.

Working context you can treat as the market data (you do not need to browse the web — use these as the captured
figures, and note they would normally be cited with URLs and dates):

- Tideline (us): per-seat, $25/seat/month, no free tier; SSO is top-tier only; Medicare claiming is an add-on.
- "ClinicFlow": per-seat, $15/seat/month entry, $30/seat top tier; free tier for 1 user; SSO bundled in entry;
  Medicare claiming in core.
- "BookWell": flat-rate, $99/month flat for unlimited seats; no per-seat scaling; SSO top-tier only; no Medicare claiming.
- "CareLedger": per-seat, $40/seat/month, enterprise pricing is "contact us" above 20 seats — no public price;
  SSO and Medicare claiming both bundled.
- Do-nothing substitute: spreadsheet + manual reminders (implicit cost = clinician admin time).

Use representative scenarios of a solo practitioner (1 seat), a typical small clinic (8 seats), and an
at-scale clinic group (40 seats). Write the benchmark artifact to `docs/gtm/competitor-price-benchmark.md`
(a relative path under the current working directory). Respond in the skill's standard format. Proceed without asking.

## Criteria

- [ ] PASS: Defines the competitive set by type and names the value metric each competitor charges on (per seat / flat / usage), treating the value metric as the headline fact
- [ ] PASS: Includes the do-nothing / spreadsheet substitute with its implicit cost as a real anchor, not just the named SaaS competitors
- [ ] PASS: Captures published pricing per competitor with the limits/thresholds, and records CareLedger's "contact us" enterprise pricing as a finding (a signal), not a gap
- [ ] PASS: Normalises raw prices to a like-for-like comparison across the named scenarios (1 / 8 / 40 seats) rather than just listing tier prices
- [ ] PASS: Includes "us" (Tideline) as a row in the like-for-like comparison — the benchmark answers nothing without our own position in it
- [ ] PASS: Identifies the crossover point — BookWell's flat $99 is dearer than us at 1 seat but far cheaper at 40 seats — as a selling/positioning insight
- [ ] PASS: States the scenario assumptions explicitly so the comparison is honest
- [ ] PASS: Analyses packaging/tiering across competitors (a capability-by-competitor view) and identifies standard gating (e.g. SSO behind top tier as a market convention) and any packaging whitespace
- [ ] PASS: Reads discounting / motion signals (annual-commit, self-serve vs "contact us" threshold) and labels anecdotal negotiation signals as such
- [ ] PASS: Synthesises where we sit (cheap / mid / premium and at which scale) and separates evidence from inference, recommending the market picture rather than a price
- [ ] PASS: Holds the ownership chain — GTM owns the benchmark, product-manager consults on packaging, a human approves price changes — and outputs NO price recommendation (not even a band labelled "for human approval")
- [ ] PASS: Labels the output DRAFT — requires human review

## Output expectations

- [ ] PASS: Output writes the benchmark to `docs/gtm/competitor-price-benchmark.md` under the working directory
- [ ] PASS: Output's competitive-set table names the value metric per competitor and includes the do-nothing substitute with its implicit cost
- [ ] PASS: Output's like-for-like comparison normalises to the 1 / 8 / 40-seat scenarios with stated assumptions and includes a "us" row — not a raw tier-price dump
- [ ] PASS: Output identifies the flat-rate crossover (BookWell cheap at scale, dear at 1 seat) explicitly as an insight
- [ ] PASS: Output's packaging/tiering analysis identifies standard gating (SSO at top tier as convention) and records CareLedger's hidden enterprise pricing as a finding
- [ ] PASS: Output recommends the market picture and contains NO recommended price for Tideline
