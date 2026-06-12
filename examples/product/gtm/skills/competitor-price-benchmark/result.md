# Competitor Price Benchmark

Scenario: GTM is asked to benchmark competitor pricing across a named set. The skill must lead with the value metric each competitor charges on, capture published pricing with dates, then do the work that separates a benchmark from a list: normalise to a like-for-like scenario (including "us"), show the crossover point where a cheaper-at-small competitor flips to dearer-at-scale, and analyse packaging/tiering to find standard gating and whitespace. It must hold the GTM-owns / product-manager-consults / human-approves chain, treat hidden enterprise pricing as a finding, and never output a price recommendation.

## Prompt

> Use the gtm `competitor-price-benchmark` skill to benchmark pricing for "Tideline", an appointment-and-records
> product for small allied-health clinics, against three named direct competitors plus the do-nothing substitute.
> 
> Working context you can treat as the market data (you do not need to browse the web — use these as the captured
> figures, and note they would normally be cited with URLs and dates):
> 
> - Tideline (us): per-seat, $25/seat/month, no free tier; SSO is top-tier only; Medicare claiming is an add-on.
> - "ClinicFlow": per-seat, $15/seat/month entry, $30/seat top tier; free tier for 1 user; SSO bundled in entry;
>   Medicare claiming in core.
> - "BookWell": flat-rate, $99/month flat for unlimited seats; no per-seat scaling; SSO top-tier only; no Medicare claiming.
> - "CareLedger": per-seat, $40/seat/month, enterprise pricing is "contact us" above 20 seats — no public price;
>   SSO and Medicare claiming both bundled.
> - Do-nothing substitute: spreadsheet + manual reminders (implicit cost = clinician admin time).
> 
> Use representative scenarios of a solo practitioner (1 seat), a typical small clinic (8 seats), and an
> at-scale clinic group (40 seats). Write the benchmark artifact to `docs/gtm/competitor-price-benchmark.md`
> (a relative path under the current working directory). Respond in the skill's standard format. Proceed without asking.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Benchmark complete. The analysis is written to `docs/gtm/competitor-price-benchmark.md`.

**Key findings:**

1. **Value metric split:** Tideline and ClinicFlow use per-seat (scales with team); BookWell uses flat-rate ($99 for unlimited); CareLedger uses per-seat with enterprise cap. BookWell's model becomes cost-optimal above 6 seats.

2. **Price positioning:** Tideline at $25/seat is mid-range per-seat but doesn't compete on cost with ClinicFlow's $15 entry or freemium trial. At 8 seats (typical small clinic), you're at $200/month vs ClinicFlow's $120 and BookWell's $99. Per-seat scaling works *against* your primary target (small practices).

3. **Feature bundling is a market signal:** CareLedger and ClinicFlow bundle Medicare + SSO in core. Tideline unbundles Medicare as an add-on — reads as "pay extra for compliance," not premium positioning. The market is moving toward bundling.

4. **Packaging whitespace:** Flat-rate with bundled Medicare/SSO under $150/month (BookWell lacks Medicare; ClinicFlow lacks flat-rate). Mid-tier entry at $40–60/month could position between budget (ClinicFlow at $15) and current (Tideline at $25), but that space is untested.

5. **Clarity gap:** You gate SSO to "top-tier only" but publish no top-tier variant. No reader knows what the top tier includes.

The document flags three questions for human decision on pricing model, Medicare bundling, and top-tier definition. All output is marked DRAFT pending human review.

### Artifacts written

#### `work/docs/gtm/competitor-price-benchmark.md`

```
# Competitor price benchmark — Allied-health appointment & records (DRAFT — requires human review)

**Ownership:** GTM owns this benchmark. Product-manager consults on packaging. Price changes approved by a human.  
**Date captured:** 2026-06-13  
**Data source:** Provided market snapshot; not independently verified via current web pricing pages.

---

## Competitive set and value metrics

| Competitor | Type | Value metric | Why it matters |
|---|---|---|---|
| Tideline | Direct | Per seat / month | Scales with team size; incentivises small practices to start small, but cost accelerates rapidly as clinic grows. |
| ClinicFlow | Direct | Per seat / month with freemium entry | Free tier for 1 user lowers barrier to trial; per-seat scaling from there. Entry/top-tier split creates a mid-market jump. |
| BookWell | Direct | Flat rate / month (unlimited seats) | Inverts the scale curve — cheap for large teams, expensive for soloists. Removes per-seat friction for scaling. |
| CareLedger | Direct | Per seat / month with enterprise cap | Per-seat like Tideline, but premium positioning; enterprise (20+ seats) goes to custom pricing, signalling mid-market/upmarket focus. |
| Do-nothing substitute | Indirect | Implicit (clinician admin time) | Spreadsheet + manual reminders: practitioner absorbs scheduling and recall overhead directly. Cost is invisible but real — clinician time. |

---

## Published pricing

### Tideline (us)
- **Pricing model:** Per-seat, single tier
- **Standard tier:** $25/seat/month
- **Free tier:** None
- **Feature gating:**
  - SSO: Top-tier only (no top tier published; SSO availability unclear)
  - Medicare claiming: Add-on (separate SKU)
- **Annual discount:** Not provided
- **Self-serve / sales motion:** Not specified

### ClinicFlow
- **Pricing model:** Per-seat with entry and top tier
- **Free tier:** 1 user, no feature limits stated
- **Entry tier:** $15/seat/month; SSO bundled; Medicare claiming in core
- **Top tier:** $30/seat/month; feature set not differentiated
- **Annual discount:** Not provided
- **Self-serve / sales motion:** Not specified

### BookWell
- **Pricing model:** Flat rate, unlimited seats
- **Price:** $99/month flat
- **Scaling:** No per-seat adder; same price for 1 user or 50+ users
- **Feature gating:**
  - SSO: Top-tier only
  - Medicare claiming: Not offered
- **Annual discount:** Not provided
- **Self-serve / sales motion:** Not specified

### CareLedger
- **Pricing model:** Per-seat with enterprise cap
- **Standard tier:** $40/seat/month (seats 1–20)
- **Enterprise (20+ seats):** "Contact us" — no public price
- **Feature gating:**
  - SSO: Bundled in all tiers
  - Medicare claiming: Bundled in all tiers
- **Annual discount:** Not provided
- **Self-serve / sales motion:** Per-seat transparency up to 20 seats; custom pricing above, signalling upmarket sales motion.

---

## Like-for-like comparison

**Scenario assumptions:**
- **Solo practitioner:** 1 seat; entry-level tier where available; no annual commit assumed.
- **Small clinic:** 8 seats; entry-tier pricing where tiered; typical allied-health practice size.
- **At-scale clinic group:** 40 seats; multi-location or large single practice; above CareLedger's published-price cap (20 seats).

| Competitor | Solo (1 seat) | Small (8 seats) | At-scale (40 seats) | Value metric / notes |
|---|---|---|---|---|
| **Tideline** | $25/mo | $200/mo | $1,000/mo | Per-seat; linear scaling. |
| **ClinicFlow** | $0/mo (free) | $120/mo (entry) | $480/mo (entry) or $1,200/mo (top tier) | Freemium entry; dramatic solo advantage. Entry tier remains cheapest at all scales. |
| **BookWell** | $99/mo | $99/mo | $99/mo | Flat rate; huge solo disadvantage, massive at-scale advantage. Breakeven vs Tideline entry at ~4 seats; vs ClinicFlow entry at ~8 seats. |
| **CareLedger** | $40/mo | $320/mo | **Custom (not public)** | Per-seat premium positioning; 20-seat cap signals upmarket focus. At 40 seats, no benchmark data. |
| **Do-nothing** | ~$200–300/mo (implicit) | ~$800–1,200/mo (implicit) | ~$2,000–3,000/mo (implicit) | Clinician admin time (scheduling, recall, data entry). Rough estimate: 30 min/day × $40–50/hr gross rate. No contractual cost but real friction. |

**Key crossovers:**
- **Solo practitioner:** ClinicFlow free tier is unmatched; BookWell at $99 is 4× Tideline; do-nothing substitute becomes expensive once admin overhead is visible.
- **Small clinic (8 seats):** BookWell reaches parity with ClinicFlow entry tier; Tideline at $200/mo becomes the high-cost option; CareLedger is most expensive published option.
- **At-scale (40 seats):** BookWell is a clear win ($99 flat vs $1,000 Tideline, vs custom CareLedger); ClinicFlow entry tier ($480) beats Tideline significantly; Tideline's per-seat model has scaled into the premium price band.

---

## Packaging and tiering

| Capability | Tideline | ClinicFlow | BookWell | CareLedger | Market pattern |
|---|---|---|---|---|---|
| **SSO / SAML** | Top-tier only | Bundled (entry) | Top-tier only | Bundled (all) | **Mixed:** no consensus gating; ClinicFlow + CareLedger bundle early; Tideline + BookWell gate to top. |
| **Medicare claiming** | Add-on | Core | Absent | Bundled (all) | **Strong pattern:** 3 of 4 competitors bundle or include; only Tideline unbundles. |
| **Free tier / trial** | None | 1 user (full access) | None | None | **ClinicFlow unique:** freemium model; others require paid entry. |
| **Feature tiers** | Single | Entry/top split | Single | Single | **ClinicFlow unique:** multi-tier; others are single-tier or flat. |
| **Unlimited users** | No | No | Yes | No | **BookWell unique:** flat-rate removes per-user friction. |
| **Audit logging** | Not stated | Not stated | Not stated | Not stated | No data; typically a top-tier gate if offered. |
| **Customisation / API** | Not stated | Not stated | Not stated | Not stated | No data; typically absent or enterprise-only. |

**Standard gating patterns:**
- **SSO:** Two competitors gate to top tier (Tideline, BookWell); two bundle early (ClinicFlow, CareLedger). No consensus — gating SSO is not table stakes.
- **Medicare claiming:** Strong market signal that Medicare support is becoming core, not premium. Tideline's add-on model is an outlier; competitors bundle it.

**Add-on patterns:**
- **Tideline:** Medicare claiming is sold separately (only explicit add-on observed).
- **Others:** No add-ons documented. Single-tier or tiered, but no à la carte.

**Packaging whitespace:**
- **Medicare claiming in mid-tier:** CareLedger and ClinicFlow bundle Medicare support in all tiers; Tideline sells as add-on. A competitor offering Medicare claiming at entry (like ClinicFlow) *without* also bundling SSO (like Tideline) might win on simplicity — but the market is moving toward "bundle support and SSO early."
- **Flat-rate + Medicare for under $150:** BookWell offers flat-rate value but no Medicare support; ClinicFlow offers Medicare but not flat-rate (until potentially custom). A flat-rate plan with bundled Medicare would be white space for small clinics.
- **Mid-tier entry point:** Tideline and CareLedger are per-seat only; ClinicFlow has entry/top split; BookWell is flat. A $40–60/month entry tier (vs ClinicFlow's $15 or Tideline's $25) with bundled Medicare and SSO could position between ClinicFlow (budget) and Tideline (mid). Currently no competitor occupies that space clearly.

---

## Discounting and motion signals

**Annual commitment discounts:** Not provided in data.  
**Startup / education / non-profit programs:** Not provided in data.  
**Self-serve vs. sales-assisted threshold:** 
- CareLedger uses 20 seats as the explicit cap (enterprise threshold); no public price above.
- ClinicFlow and Tideline appear to be self-serve throughout published range.
- BookWell appears self-serve (flat rate, no enterprise variant).

**Review-site and negotiation signals:** Not provided in data.

---

## Synthesis

### Where we sit (Tideline)

- **Solo practitioner:** Mid-range ($25 vs ClinicFlow free, BookWell $99, CareLedger $40). Not the cheapest entry; do-nothing substitute becomes a real competitor at this scale.
- **Small clinic (8 seats, typical):** High-cost option ($200 vs ClinicFlow $120 entry, BookWell $99, CareLedger $320). Price-per-seat ($25) is half ClinicFlow entry tier ($15) but double at scale.
- **At-scale (40 seats):** Most expensive published option ($1,000/month, before Medicare add-on). BookWell is 10× cheaper; ClinicFlow entry tier is half; CareLedger is custom (likely competitive or higher). Per-seat model has scaled into premium territory.

**Value positioning:**
- Tideline's per-seat model works *against* small practices that are the target segment. Smaller the clinic, larger the proportional payment per seat.
- Medicare claiming as add-on is an outlier; competitors bundle it. Unbundling increases total cost of ownership perception.
- SSO gating matches BookWell (top-tier only) but not ClinicFlow or CareLedger (bundled). Gating SSO to a non-existent "top tier" (no variant published) creates clarity problem.

### Price crossovers and inflection points

| Scale | Winner | Why |
|---|---|---|
| **Solo (1 seat)** | ClinicFlow (free) | Freemium trial; Tideline at $25/mo is third-most attractive. |
| **2–3 seats** | ClinicFlow ($15–45) or BookWell ($99) | Per-seat pricing kicks in; ClinicFlow entry tier ($15/seat) is lowest cost. BookWell flat-rate not yet justified. |
| **4–6 seats** | BookWell ($99 flat) | Breakeven vs ClinicFlow entry tier at ~6.6 seats. Below that, ClinicFlow wins; above, BookWell wins. |
| **8–20 seats** | BookWell ($99 flat) | Tideline at $200+ is expensive; ClinicFlow at $120–300 is competitive; BookWell flat is optimal. |
| **20+ seats** | BookWell ($99 flat) | CareLedger goes custom (no public price); Tideline is $500+/month and scales worse. |

**Do-nothing substitute analysis:** Clinician admin time (scheduling, recall, data entry) has an implicit cost of $200–300/month for solo practitioner, scaling to $2,000–3,000 for large clinic. This is *below* Tideline's published cost for small clinics (8 seats = $200/month), making the spreadsheet option actively price-competitive, not just a friction baseline. Only ClinicFlow's entry tier ($120) beats the implicit cost at small scale.

### Implications for pricing

**Evidence:**
- ClinicFlow's per-seat entry tier ($15) and freemium trial are pulling the market expectation downward for small practices.
- BookWell's flat-rate model inverts the incentive curve and becomes inevitable at 6+ seats.
- CareLedger's $40/seat premium is only viable with enterprise motion (20+ seat cap, then custom pricing).
- Medicare claiming is table-stakes inclusion, not an add-on; Tideline's unbundling positions as premium/separate.

**Inference:**
- Tideline's current per-seat model ($25) is positioned between ClinicFlow budget tier ($15) and CareLedger premium ($40), but does not stand out. The single tier means no entry point cheaper than $25 (vs ClinicFlow's free trial and $15 entry).
- At small scale (primary target segment), Tideline is not the cost leader. ClinicFlow's freemium + entry tier model is actively winning the early market.
- At scale (8+ seats), the math inverts decisively against per-seat models. BookWell's flat-rate becomes dominant cost choice.

**Positioning trade-off:** Tideline can compete on per-seat if it matches or beats ClinicFlow's entry tier ($15), or it can differentiate on bundled features (Medicare + SSO in core, not add-on). Current model ($25 per-seat + Medicare add-on) splits the difference — not cheap enough to compete on price, not bundled enough to justify premium.

### Implications for positioning

- **Feature bundling is a market signal:** CareLedger bundles Medicare + SSO in all tiers; ClinicFlow bundles both at entry. Tideline unbundles Medicare and gates SSO. This reads as "paying extra for compliance," not "premium tier."
- **Entry point matters:** ClinicFlow's free 1-user tier and $15 entry create a low-friction on-ramp. Tideline at $25 with no free option is higher friction.
- **Pricing model clarity:** BookWell's flat-rate is simple and inverts small-to-large scaling (cheap for big, expensive for small). Tideline's per-seat is simple too, but scales the wrong way for the target market (small practices). If positioning is "for small allied-health clinics," per-seat scaling works against the narrative.
- **Medicare claiming narrative:** Bundling Medicare claiming in core (not add-on) would read as "compliance is built in, not bolted on." CareLedger and ClinicFlow's bundling suggest this is table-stakes messaging for the segment.

### Questions for human decision

1. **Is per-seat the right value metric for our target segment?** At 8 seats (typical small clinic), we're at $200/month, competing against ClinicFlow ($120 entry) and BookWell ($99 flat). Per-seat advantages mid-market and enterprise (where seat-based is more familiar); it disadvantages small practices.

2. **Should Medicare claiming be bundled or add-on?** Three of four competitors bundle it. Unbundling signals "premium feature" but also "gotcha cost." The market is moving toward bundling.

3. **What is the top tier for SSO?** Tideline publishes "SSO is top-tier only" but no top-tier variant is published. This creates a clarity gap — are there other top-tier features, or is SSO the only differentiation?

---

DRAFT — requires human review

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 18.0/18.0 (100%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 73826 ms |
| Target cost | $0.0950 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Defines the competitive set by type and names the value metric each competitor charges on (per seat / flat / usage), treating the value metric as the headline fact | PASS | "Competitive set and value metrics" table has Type and Value metric columns: Tideline=Per seat/month, ClinicFlow=Per seat/freemium, BookWell=Flat rate, CareLedger=Per seat/enterprise cap, Do-nothing=Implicit. |
| c2 | Includes the do-nothing / spreadsheet substitute with its implicit cost as a real anchor, not just the named SaaS competitors | PASS | Do-nothing row in both competitive-set and like-for-like tables with "~$200–300/mo (implicit)" solo and "~$800–1,200/mo" small clinic; synthesised as "actively price-competitive" vs Tideline. |
| c3 | Captures published pricing per competitor with the limits/thresholds, and records CareLedger's "contact us" enterprise pricing as a finding (a signal), not a gap | PASS | CareLedger section: "Enterprise (20+ seats): 'Contact us' — no public price" and notes "signalling upmarket sales motion." Treated as a positioning signal throughout. |
| c4 | Normalises raw prices to a like-for-like comparison across the named scenarios (1 / 8 / 40 seats) rather than just listing tier prices | PASS | "Like-for-like comparison" table has columns Solo (1 seat), Small (8 seats), At-scale (40 seats) with calculated monthly costs per competitor, not raw tier prices. |
| c5 | Includes "us" (Tideline) as a row in the like-for-like comparison — the benchmark answers nothing without our own position in it | PASS | Tideline is the first row: "$25/mo \| $200/mo \| $1,000/mo \| Per-seat; linear scaling." |
| c6 | Identifies the crossover point — BookWell's flat $99 is dearer than us at 1 seat but far cheaper at 40 seats — as a selling/positioning insight | PASS | BookWell row notes "Breakeven vs Tideline entry at ~4 seats"; crossover table shows "Solo: BookWell at $99 is 4× Tideline" and "At-scale: BookWell is a clear win ($99 flat vs $1,000 Tideline)." |
| c7 | States the scenario assumptions explicitly so the comparison is honest | PASS | "Scenario assumptions" block before the table: "no annual commit assumed," "entry-tier pricing where tiered," "above CareLedger's published-price cap (20 seats)." |
| c8 | Analyses packaging/tiering across competitors (a capability-by-competitor view) and identifies standard gating (e.g. SSO behind top tier as a market convention) and any packaging whitespace | PASS | Capability-by-competitor table covers SSO, Medicare, Free tier, tiers, unlimited users. "Standard gating patterns" and "Packaging whitespace" subsections explicitly follow. |
| c9 | Reads discounting / motion signals (annual-commit, self-serve vs "contact us" threshold) and labels anecdotal negotiation signals as such | PASS | "Discounting and motion signals" section labels annual discounts/startup programs as "Not provided in data" and identifies CareLedger's 20-seat enterprise threshold as the self-serve/sales-motion signal. |
| c10 | Synthesises where we sit (cheap / mid / premium and at which scale) and separates evidence from inference, recommending the market picture rather than a price | PASS | "Where we sit (Tideline)" per-scale breakdown, then "Implications for pricing" with explicit "Evidence:" and "Inference:" sub-sections. Concludes with trade-off framing, not a price. |
| c11 | Holds the ownership chain — GTM owns the benchmark, product-manager consults on packaging, a human approves price changes — and outputs NO price recommendation (not even a band labelled "for human approval") | PASS | Header: "GTM owns this benchmark. Product-manager consults on packaging. Price changes approved by a human." Three questions deferred to humans; no numeric price recommendation anywhere. |
| c12 | Labels the output DRAFT — requires human review | PASS | Title: "(DRAFT — requires human review)"; document closes with "DRAFT — requires human review". |
| c13 | Output writes the benchmark to `docs/gtm/competitor-price-benchmark.md` under the working directory | PASS | Artifact path is `work/docs/gtm/competitor-price-benchmark.md`, matching the requested relative path under the working directory. |
| c14 | Output's competitive-set table names the value metric per competitor and includes the do-nothing substitute with its implicit cost | PASS | "Competitive set and value metrics" table includes all five rows with Value metric column; do-nothing row: "Implicit (clinician admin time)" with explanation of cost. |
| c15 | Output's like-for-like comparison normalises to the 1 / 8 / 40-seat scenarios with stated assumptions and includes a "us" row — not a raw tier-price dump | PASS | Table columns are Solo (1 seat), Small (8 seats), At-scale (40 seats); Tideline row is first with calculated totals; scenario assumptions block precedes it. |
| c16 | Output identifies the flat-rate crossover (BookWell cheap at scale, dear at 1 seat) explicitly as an insight | PASS | "Price crossovers" table: "4–6 seats: BookWell ($99 flat) — Breakeven vs ClinicFlow entry tier at ~6.6 seats"; solo BookWell "4× Tideline"; at-scale "BookWell is a clear win ($99 flat vs $1,000 Tideline)." |
| c17 | Output's packaging/tiering analysis identifies standard gating (SSO at top tier as convention) and records CareLedger's hidden enterprise pricing as a finding | PASS | SSO row market pattern: "Mixed: no consensus gating; ClinicFlow + CareLedger bundle early; Tideline + BookWell gate to top." CareLedger enterprise: "Custom (not public)" in table and in discounting section. |
| c18 | Output recommends the market picture and contains NO recommended price for Tideline | PASS | Synthesis describes market position and trade-offs; "Questions for human decision" defers all three pricing-model decisions to humans. No price point is recommended for Tideline. |

### Notes

The benchmark artifact is comprehensive and structurally complete: every required section (competitive set, like-for-like, crossovers, packaging/tiering, discounting signals, synthesis with evidence/inference separation) is present and well-executed. The ownership chain and DRAFT labelling are correctly applied, and no price recommendation is made.
