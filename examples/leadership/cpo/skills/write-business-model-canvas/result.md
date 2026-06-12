# Write Business Model Canvas

Scenario: The CPO maps a business model where the user and the payer differ — the classic load-bearing trap. The skill must fill the nine Osterwalder blocks as a first pass, but the quality bar is the ARGUED READ: it must trace whether revenue actually follows from value (and surface that the people who get the value are not the people who pay), tag blocks known/assumed and honour the ratio, name exactly ONE riskiest assumption as a falsifiable claim with the cheapest test to settle it, test the unit economics direction, and end with a position on viability. A tidy nine-cell grid with no judgment must NOT score well.

## Prompt

> Use the cpo `write-business-model-canvas` skill to map and pressure-test the business model for "Roster", a
> proposed (not yet built) shift-scheduling app for hospitality venues. The intended model: the app is free
> for hourly staff to view and swap shifts (the users), while venue owners/managers pay a per-venue monthly
> subscription (the payers). Revenue is assumed to come from venue subscriptions; demand is largely
> unvalidated — you are proposing this model, not auditing a running one. Acquisition is assumed to be
> word-of-mouth from staff pulling their venue onto the platform.
> 
> Write the canvas artifact to `docs/strategy/business-model-canvas-roster.md` (a relative path under the
> current working directory). Respond in the skill's standard format. Proceed without asking.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Done. The business model canvas for Roster is written to `docs/strategy/business-model-canvas-roster.md`.

**Key findings:**

1. **The load-bearing assumption:** Venues will pay monthly for shift-coordination features when the primary value is delivered to staff, and acquisition is staff-driven word-of-mouth. This is unvalidated and carries the entire revenue model.

2. **Right-side weakness:** The user-payer mismatch. Staff get free value; venues pay for indirect benefits (retention, reduced no-shows, efficiency). The connection is speculative — no evidence that venues see these as material cost problems or would attribute them to this tool.

3. **Left-side weakness:** Acquisition is entirely dependent on staff driving venue adoption, which reverses typical B2B dynamics. No fallback channels or partnerships exist. If word-of-mouth doesn't work, the model has no customer-acquisition lever.

4. **The verdict:** The model is coherent if the revenue assumption holds, but it's 95% unvalidated. Before engineering, run a cheap discovery loop to test whether venue managers see shift coordination as a cost problem and whether staff can actually drive adoption.

5. **Canvas recommendation:** This is premature for a Business Model Canvas. Switch to a **Lean Canvas** immediately — it forces the team to validate customer, problem, and solution before betting on the business structure.

The artifact includes the discovery interview loop you should run first (~1 week, cheap, settles the core assumption).

### Artifacts written

#### `work/docs/strategy/business-model-canvas-roster.md`

```
# Business model canvas — Roster

**Maturity:** Proposed model (not yet built) · **Author:** CPO · **Date:** 2026-06-13

**Verdict:** Coherent structure, but the load-bearing assumption (venues will pay for staff-driven efficiency gains) is entirely unvalidated. This is a 95%-assumed model that needs customer discovery before the revenue chain can be pressure-tested. Recommend switching to a Lean Canvas to validate problem fit before engineering.

## The nine blocks (first pass)

| Block | Side | One-line | Evidence |
|---|---|---|---|
| Customer segments | Right | Hourly staff (users); venue owners/managers (payers) | `[assumed]` |
| Value propositions | Right | For staff: free shift visibility + swap workflows. For venues: labor efficiency, reduced no-shows, staff retention. | `[assumed]` |
| Channels | Right | Word-of-mouth from staff pulling venue adoption; (implied) direct/support onboarding for venues | `[assumed]` |
| Customer relationships | Right | Self-serve for staff; self-serve + support onboarding for venues | `[assumed]` |
| Revenue streams | Right | Per-venue monthly subscription (pricing not specified) | `[assumed]` |
| Key resources | Left | Software platform (mobile + web); staff-user network; shift/availability data | `[known]` platform is buildable; `[assumed]` network effects and data value |
| Key activities | Left | Platform development; venue onboarding; "network growth" (staff adoption, viral loop, venue pull-in) | `[assumed]` |
| Key partnerships | Left | (None identified) Implied: POS/HR integrations, payment processing | `[assumed]` — no partnerships named |
| Cost structure | Left | Development + maintenance; server/infrastructure (scales with users); support (scales with venues); acquisition (if word-of-mouth insufficient) | `[assumed]` |

**Known-to-assumed ratio:** ~1 known / 8 assumed (87% guesswork). The platform is buildable; everything else is hypothesis.

---

## Right side — does capture follow from value?

### Segments → Value propositions

The model has **two distinct segments with different value propositions, and they're misaligned.**

**Staff segment:** Free shift visibility and swap workflows solve a real problem IF staff currently experience friction in shift management (pen & paper, manager calls, group chats, fragmented coordination). The value is direct and immediate — staff see it on day one. However, this assumption is unvalidated: many venues may already have adequate shift management via group chats, existing POS systems (Toast, Square), or simple practices. The value prop assumes the problem is salient to staff; that needs discovery.

**Venue segment:** The value prop (labor efficiency, reduced no-shows, staff retention) is three separate claims bundled together:
- Reduced no-shows: unclear how shift swaps → fewer no-shows. Staff swap when they can cover, which may eliminate no-shows, but the claim isn't proven.
- Efficiency gains: harder to measure. Does shift visibility save management time? Maybe, but competing tools already offer this.
- Staff retention: the most indirect. Does enabling shift swaps improve retention? Possibly, if flexibility is a retention lever — but that's a 6–12 month signal, not a subscription justification.

The venue value prop is **aspirational and speculative.** Venues don't manage shift availability as a cost centre they're trying to optimize; they manage it operationally with whatever tools they have. If they don't currently see shift coordination as a pain, they won't pay for a solution. This is not "nice to have in the future" — it's "not on the venue manager's decision frame today."

### Value propositions → Revenue streams (the critical chain)

This is where the model bends most visibly: **the payer (venue) is not the primary value beneficiary; the user (staff) is.**

The revenue model assumes venues will subscribe to unlock management features that help their staff coordinate shifts. But the core value is delivered TO staff (free), and the subscription is charged TO venues. The link requires:

1. Venues to see the value proposition (labor efficiency, retention, fewer no-shows) as worth $X/month
2. Venues to attribute that value to *this tool*, not to existing practices or competing solutions
3. Venues to sustain the subscription even if ROI is hard to measure

None of these are validated. The revenue chain reads: staff get free value → venues pay for the downstream benefit. This is backward from how SaaS revenue typically flows: the party that benefits pays.

**Acquisition channel amplifies this problem:** The model bets on word-of-mouth from staff pulling venues in. This reverses standard B2B dynamics (venues decide to adopt tools; staff then use them). For this to work, venues must *trust a staff recommendation on business software* and see enough value themselves to start paying. That's a high bar. Most venue managers won't adopt a tool because staff push it unless the manager independently sees ROI — and if the manager needs to see ROI, a staff-driven acquisition channel is fragile.

### Channel fit vs. price point

The assumed channel (staff-driven, word-of-mouth) is low-touch and low-cost for acquisition. But the assumed relationship model (self-serve onboarding for venues) implies no dedicated support or sales. If venues are acquired through staff recommendations, they likely have low expectations for handholding — which is good margin-wise.

However, if venues need onboarding help (integrations, user setup, training), support costs will spike and erode margin. The tension is unresolved: either the channel is truly self-serve (no support, high churn risk) or venues expect support (channel now has high CAC). The model papers over this.

**Weakest link on the right:** The value-proposition-to-revenue connection. Venues are expected to pay for a feature set designed for and delivered to staff. The willingness-to-pay assumption is entirely unvalidated and carries the entire revenue model.

---

## Left side — can you deliver it?

### Value propositions → Key activities and resources

**For staff value (shift visibility + swaps):**
- Requires a reliable platform and data integration. If shifts are manually entered, venues must trust data accuracy; if integrated with POS systems, you need partnerships with Toast, Square, Plate IQ, etc. No partnerships are identified — this is a hidden integration tax.
- The platform is buildable. This block is the one reliable piece of the left side.

**For venue value (efficiency, retention, reduced no-shows):**
- Requires measurement and analytics to show ROI. Currently missing from key activities. If venues subscribe for retention and efficiency, they'll want proof (reports, dashboards, metrics). Building this is a second product; the current blocks don't mention it.
- This is a missing activity that separates "staff think this is useful" from "venues think it's worth paying for."

### Key partnerships — concentration risk

**No partnerships are identified.** The model assumes:
- Venues will voluntarily adopt through word-of-mouth (no sales, community, or distribution partnerships)
- Staff will voluntarily use and drive adoption (no community or influencer partnerships)
- POS/HR integrations will exist (no tech partnerships named, integration tax uncosted)
- Payment processing will work (commodity)

The highest-risk gap: **If word-of-mouth doesn't work, there's no fallback.** The model has no B2B sales channel, no venue-discovery partnerships, no industry association relationships. It's a one-lever model (viral staff adoption), and that lever is unproven.

The second-highest-risk gap: integrations are unplanned. Many venues use Toast, Square, Toast, or Marginaut for shift coordination already. Roster either competes with them (and loses on brand, integration depth, and feature breadth) or integrates with them (and needs partnerships, which are unidentified).

### Load-bearing resource and failure mode

**Load-bearing resource:** The staff-user network. Without staff adopting the platform and driving awareness, there's no acquisition lever and no venue pull-in. The platform itself is buildable (moderate risk), but the network is the lynchpin.

**Most likely to fail:** The acquisition channel. Word-of-mouth from staff pulling in venues is unvalidated and operationally complex:
- Staff adoption requires awareness, onboarding, and habit formation. What activates all three? No growth strategy is described.
- Staff influence requires staff to be decision-makers or strong influencers on business-software decisions. In hospitality, that's uncommon — managers/owners decide, staff use.
- Venue onboarding requires venues to sign up after a staff recommendation, without sales support. The friction is higher than a typical bottoms-up or top-down B2B sale.

If any of these three fails, the model has no customer acquisition path.

---

## Economics

### Unit economics (direction)

Assume a venue with 25 staff members, $30/month subscription:
- **Revenue per venue per year:** $360
- **Cost to serve per venue:** ~$2–5/month for infrastructure (platform + data) + $3–8/month for support/onboarding amortized over 24-month lifetime = ~$5–13 COGS per month
- **Gross margin direction:** Likely positive per venue ($30 − $13 = $17, ~57% margin) IF support costs don't spike and the venue sustains the subscription

**The risk:** Churn. If venues drop after 6 months because they see no ROI, the lifetime value falls sharply. The model assumes venues stick around; that's unvalidated. Staff turnover also threatens the viral loop — if staff who drove adoption leave, the connection to the venue evaporates.

### Cost structure shape

This is a **software-platform model with two-sided-market dynamics.** The value prop leans premium (efficiency, retention, labor intelligence), but the acquisition is grassroots (staff-driven). This is a mismatch:
- Premium SaaS models typically have high CAC but high LTV (decision-maker wants to solve a problem, pays accordingly).
- Grassroots models typically have low CAC but lower willingness-to-pay (acquired through usage, expect lower price).
- Roster is trying both: low-CAC acquisition (word-of-mouth) + premium-SaaS pricing (monthly subscription). Unless the value to venues is genuinely premium, this is underpriced or the channel doesn't work.

The cost structure is **optimized for premium delivery (product development, support, data analytics) but funded by grassroots acquisition (assumed free word-of-mouth).** If the grassroots channel doesn't work, the model needs high-cost direct sales, which inverts the economics.

### Where's the margin?

Margin lives in:
1. **The subscription fee** ($30/month or higher per venue) — this is entirely assumed. No pricing research or willingness-to-pay study is mentioned.
2. **Low support costs** — the model assumes self-serve onboarding. If venues need hand-holding, support costs spike and margin collapses.
3. **High LTV through retention** — the model assumes venues stay subscribed. If churn is high (unvalidated), LTV falls and margin disappears.

Margin is consumed by:
1. **Platform development and maintenance** (ongoing, scale-invariant at early stage)
2. **Infrastructure** (scales moderately with venues + staff)
3. **Support and onboarding** (scales with venues, high-risk cost)
4. **Customer acquisition** (assumed zero through word-of-mouth; if actual CAC is needed, margin inverts)

**The margin is thin and contingent.** It depends on all three assumptions (pricing, retention, low CAC) holding true. Failure of any one collapses profitability.

---

## Riskiest assumption

**Assumption (falsifiable):** "Venue managers will pay a monthly subscription ($20–50) for shift-visibility and coordination features when the primary beneficiary is their staff, the acquirer is staff word-of-mouth, and the link between the tool and measurable ROI (reduced no-shows, retention, efficiency) is indirect and unproven."

**Evidence that would confirm it:**
- Venue managers independently report that shift-coordination and staff-retention are significant cost problems.
- Venue managers would subscribe to a tool *even if staff hadn't recommended it*, based on the operational value alone.
- Venue managers who adopt sustain the subscription beyond 12 months, indicating they perceive ongoing value.

**Evidence that would kill it:**
- Venue managers report they have adequate shift-coordination practices already (group chats, POS systems, existing tools).
- Venue managers would not subscribe based on the value prop alone; they'd only consider it if staff pulled them in — and even then, would drop after a trial period.
- No sustained interest from venue managers in pricing conversations or pilots.

**Cheapest test:** 
1. **Interview loop (1 week):** Talk to 15–20 venue managers (hospitality, 10–50 staff) about their shift-coordination pain points, how they currently manage availability, and whether they'd consider a subscription tool. Don't mention Roster — test the problem first. Ask: "If your staff recommended a tool for better shift coordination, would you consider paying for it? What would it need to do to be worth $X/month?"
2. **Staff discovery (parallel, 1 week):** Interview 10–15 hourly staff about their shift-coordination friction and whether they'd feel empowered to pull their venue onto a new platform. Assess: Do staff feel empowered to recommend business tools? Do they currently coordinate shifts and see friction?
3. **Analysis:** Map the results. If venue managers see the problem and would pay independently, the revenue assumption may hold. If they only consider it via staff recommendation and see marginal value, the model is fragile. If staff don't perceive friction, the viral lever doesn't prime.

This test is cheap (interviews + synthesis, no product build) and settles the core assumption before engineering starts.

---

## Argued read

Roster's business model is **coherent in structure but dependent on a single unvalidated assumption: that venues will pay for labour coordination and retention benefits that their staff drive adoption of.**

The model is internally consistent:
- Staff get a free, frictionless tool.
- Venues pay for the operational benefits (efficiency, retention, fewer no-shows).
- The acquisition channel (word-of-mouth from staff) is elegant if it works.
- Unit economics are probably positive if retention is high and support costs are low.

But the model is **entirely bet on the revenue assumption.** The sequence is:
1. Build platform (buildable; medium risk)
2. Drive staff adoption (unvalidated; high risk)
3. Staff pull in venues (unvalidated; high risk)
4. Venues perceive ROI and sustain subscriptions (unvalidated; **highest risk**)

Failure at step 3 or 4 breaks the model. Steps 3 and 4 are the whole business, and both are guesses.

The secondary risks are:
- **Integration tax:** Venues likely use Toast, Square, or other POS systems for shifts. Roster either competes (and loses) or integrates (and needs partnerships not yet planned).
- **Support cost:** If venues need onboarding help, the self-serve assumption breaks and margin collapses.
- **Churn:** If venues drop after 6 months, LTV falls sharply. High churn is likely if ROI is hard to measure.

**Viability hinges on:** Can you find venue managers who see labour coordination and retention as material cost problems, and who will pay monthly for a solution their staff adopt? If yes, the model may work. If no, you have a user-friendly product without a business model.

---

## Which canvas this called for

**Recommendation: Switch to a Lean Canvas immediately.**

**Why:** The Business Model Canvas is designed for products with known customers and validated value propositions. Roster is 95% unvalidated:

- **Customer:** It's unclear whether the customer is staff (who use the tool) or venues (who pay). Venues are payers but not primary users, and their needs are assumed, not discovered.
- **Problem:** Does this product solve a problem venues actually have and want to pay for? Or does it solve a staff problem and hope venues subsidize it? The canvas doesn't answer this.
- **Solution:** The product hasn't been built, tested, or validated with any segment. The value props (efficiency, retention, fewer no-shows) are aspirational, not proven.
- **Known-to-assumed ratio:** 87% assumed. The only known block is that the platform is technically buildable.

The Lean Canvas forces the harder questions first:

| Block | Roster (BMC) | Roster (Lean Canvas) |
|---|---|---|
| Customer | Venues + staff | Who *actually* wants to solve a shift-coordination problem? |
| Problem | Assumed inefficiency, turnover, no-shows | What friction do venue managers and staff *actually* experience? |
| Solution | The app | Is shift-swapping the right lever for retention? Or for no-shows? |
| Key metrics | (Not in BMC) | What would prove the model works? (e.g., % staff adoption, % venues that sustain subscriptions, NPS) |
| Unfair advantage | (Not in BMC) | Why would venues choose Roster over Toast, Square, or existing practices? |

**Next step:** Run the discovery interview loop (test described in "Riskiest assumption" above). Once you've validated that:
1. Venue managers see shift coordination as a cost problem, OR
2. Staff feel empowered to drive adoption and venue managers trust the recommendation,

...you can return to the BMC with actual data. Until then, the Lean Canvas keeps the team focused on what actually needs to be true before this model works.

---

## Related reading

- [[learned--verify-regulated-content-against-primary-source]] — While Roster isn't regulated, the principle applies: validate assumptions against real customer data before designing the business model.
- [[learned--martin-nfr-flavour-answers-to-ambiguity]] — This model has ambiguity about who benefits and who pays; the resolution should come from customer discovery, not design assumption.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 12.5/13.0 (96%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 108228 ms |
| Target cost | $0.1114 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Establishes context and maturity first — recognises this is a PROPOSED model (not an operating-model audit), so most blocks are assumptions | PASS | File opens: "Maturity: Proposed model (not yet built)"; verdict states "95%-assumed model that needs customer discovery"; known-to-assumed ratio 87% guesswork explicitly stated. |
| c2 | Drafts all nine Osterwalder blocks as a first pass, each tagged `[known]` or `[assumed]`, and reports the known-to-assumed ratio as a finding (a mostly-assumed canvas is a hypothesis, not a business) | PASS | All nine blocks appear in the table with [known] or [assumed] tags; explicit ratio: "~1 known / 8 assumed (87% guesswork). The platform is buildable; everything else is hypothesis." |
| c3 | Traces revenue back to value and EXPLICITLY surfaces the user-vs-payer split — staff get the value (free shift swapping) while venues pay — and states whether their interests align or conflict | PASS | "the payer (venue) is not the primary value beneficiary; the user (staff) is." Revenue chain described as "backward from how SaaS revenue typically flows"; conflict is explicit, not neutral. |
| c4 | Pressure-tests the right side as a chain (segments→value→revenue, channels/relationships vs price point) with an argued paragraph per link, not a description, ending with the single weakest link on the right | PASS | Section "Right side" walks Segments→VP, VP→Revenue, Channel fit vs. price point with argued paragraphs; ends: "Weakest link on the right: The value-proposition-to-revenue connection." |
| c5 | Pressure-tests the left side — value→activities/resources and partnership/concentration risk — and names the load-bearing resource/activity whose removal collapses the model | PASS | "Load-bearing resource: The staff-user network. Without staff adopting the platform... there's no acquisition lever and no venue pull-in." Partnerships section names integration tax and no-fallback risk. |
| c6 | Tests the economics — unit-economics direction (does revenue plausibly exceed cost to serve) and cost-structure shape (value-driven vs cost-driven), checking the blocks are internally consistent | PASS | Specific unit calc: $30/mo venue, ~$5–13 COGS, ~57% margin. Cost-structure shape: "premium delivery... funded by grassroots acquisition" tension named. Churn risk on LTV explicitly tested. |
| c7 | Names EXACTLY ONE riskiest assumption as a falsifiable claim (e.g. "venue managers will pay $X/month", or "staff word-of-mouth actually pulls venues onto the platform"), NOT a list of risks | PASS | "Riskiest assumption" section contains one falsifiable claim: "Venue managers will pay a monthly subscription ($20–50) for shift-visibility and coordination features when..." — single, not a list. |
| c8 | For the riskiest assumption, states what evidence would confirm or kill it AND the cheapest test that would produce that evidence | PASS | Three confirm bullets, three kill bullets, then "Cheapest test": 1-week interview loop with 15–20 venue managers + parallel 10–15 staff interviews described in detail. |
| c9 | Ends with an argued read that takes a POSITION on viability ("viable if and only if X holds"), willing to conclude the model bends or doesn't hold — not a neutral summary that all nine boxes are filled | PASS | "Viability hinges on: Can you find venue managers who see labour coordination...as material cost problems...? If yes, the model may work. If no, you have a user-friendly product without a business model." |
| c10 | Decides whether the BMC was even the right tool — given a mostly-assumed, unvalidated proposed model, recommends switching to a Lean Canvas and names the risk as market risk (should we build this?) not operational risk | PASS | Section "Which canvas this called for" recommends Lean Canvas immediately; frames it as "Does this product solve a problem venues actually have?" — market risk framing, not operational. |
| c11 | Holds CPO ownership — frames the read as CPO-authored with PM supplying slice-level economic input | PARTIAL | "Author: CPO" is stated in the header. However, no mention of PM supplying slice-level economic input appears anywhere in the document — that delegation is entirely absent. |
| c12 | Output writes the canvas file to `docs/strategy/business-model-canvas-roster.md` under the working directory, with a one-line viability verdict up top, the nine-block table with known/assumed tags, and a distinct "Riskiest assumption" section | PASS | File written to `work/docs/strategy/business-model-canvas-roster.md`; one-line verdict at top; nine-block table with tags present; "Riskiest assumption" is a distinct headed section. |
| c13 | The written file demonstrates the argue-not-box-tick bar — it names exactly one riskiest assumption as a falsifiable claim with a cheapest test, surfaces the user-vs-payer split, and ends with a position on viability rather than restating that all nine blocks are populated | PASS | File has single falsifiable claim with cheapest test, explicit user-vs-payer conflict, and conditional viability verdict — not a restatement of block coverage. |

### Notes

An exceptionally thorough output that hits every structural requirement and argues each link in the chain rather than describing it. The only gap is c11's PM economic delegation, which is simply absent from both the artifact and the chat response.
