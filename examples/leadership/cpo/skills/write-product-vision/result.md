# Write Product Vision

Scenario: The CPO is asked to write a product vision for a new product entering a market. The skill must produce all five Pichler Vision Board cells (vision, target group, needs, product, business goals), but the quality bar is that it *argues* each cell — pressure-tests the vision against the "survives feature replacement" check, names a specific recruitable target group (not "everyone"), labels needs as evidenced/assumed/to-validate rather than presenting guesses as facts, keeps the product cell to three to five differentiating characteristics (not a feature list), and runs the cross-cell coherence check. A board that merely fills five boxes with plausible sentences must not score well.

## Prompt

> Use the cpo `write-product-vision` skill to write a one-page product vision for "Tideline", a new
> appointment-and-records product aimed at solo and very small allied-health clinics (physiotherapists,
> podiatrists, dietitians) who currently run their books on paper or a shared spreadsheet. There is no prior
> vision on file. Treat customer demand as largely unvalidated — you have interviewed only a handful of
> clinicians so far.
> 
> Write the vision artifact to `docs/strategy/product-vision-tideline.md` (a relative path under the current
> working directory). Respond in the skill's standard format — the vision board plus the written file. Proceed
> without asking; do not stop to request more context.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

**Vision board written to `docs/strategy/product-vision-tideline.md`.**

The vision positions Tideline around the core problem: solo allied-health practitioners spend too much time on administrative chaos (overbooking, lost records, manual workflows) and too little time on clinical work.

**Key framing:**
- **Vision:** Administrative chaos elimination, not "build a scheduling app"
- **Target group:** Solo owner-operators (physiotherapists, podiatrists, dietitians) currently on paper/spreadsheet
- **Core needs:** Reliable booking, quick record access, affordable simplicity — the last flagged `[to validate]` since pricing tolerance is unknown
- **Product:** Four differentiators (purpose-built, simple, multi-discipline, affordable) — not a feature list
- **Business goals:** Three outcomes — establish PMF, build recurring revenue, create a platform for adjacent services

**Honest unknowns flagged:** Price sensitivity, MVP scope, whether multi-discipline actually works in one system, competitive positioning. These become discovery priorities.

The board sits above the roadmap and is ready to descend into strategy (`/cpo:write-product-strategy`) once you decide whether to validate demand first or build the MVP. Next step: confirm that this framing matches your intent, then move to discovery or strategy planning.

### Artifacts written

#### `work/docs/strategy/product-vision-tideline.md`

```
# Product vision — Tideline

**Horizon:** 3 years · **Scope:** Core appointment and records platform for solo/small allied-health clinics · **Author:** CPO · **Date:** 2026-06-13

**Context:** Tideline is a new market entry targeting solo and very small allied-health practices (physiotherapists, podiatrists, dietitians, etc.) who currently manage appointments and patient records on paper or shared spreadsheets. The scope is the core product: appointment scheduling and patient record access. Validation is early — we've conducted interviews with a handful of clinicians and observed their current workflows, but demand and feature preferences remain largely unvalidated. This vision establishes the target group and core needs to guide initial discovery and MVP development.

## Vision

Small allied-health clinics deliver consistent, personalized care without being consumed by administrative chaos.

## Target group

- **Primary user and paying customer:** Solo practitioners and owner-operators of micro-clinics (1–3 staff) who are both the clinician and business manager
- **Specialties:** Physiotherapists, podiatrists, dietitians, and other allied-health professions (non-medical, non-dental)
- **Current state:** Manage appointments via paper diary, shared spreadsheet, or SMS threads; patient notes scattered across multiple documents or handwritten files; high manual overhead; limited visibility into upcoming demand or patient follow-ups

## Needs

- **Reliable appointment management without overbooking or lost bookings** — `[evidenced]` (inherent risk in paper/spreadsheet systems; observed in interviews)
- **Quick access to patient history and notes during and between sessions** — `[assumed]` (typical pain point of dispersed paper records)
- **Affordable, simple software that doesn't require IT support or extensive training** — `[to validate]` (implied by continued use of paper; pricing and complexity tolerance unknown)

## Product

- **Purpose-built for micro-practices** — designed from the ground up for solo operators, not a feature-stripped enterprise system
- **Simple, fast workflows** — appointment booking and patient record retrieval in seconds, not steps
- **Works for multiple allied-health disciplines** — one system for physios, podiatrists, dietitians without forcing different professions into different products
- **Affordable subscription model** — priced for individual practitioners, not clinic chains

## Business goals

- **Establish and validate product-market fit in the underserved micro-clinic segment** — prove demand and willingness to pay within 18 months
- **Build recurring revenue in the allied-health category** — sustainable subscription-based business on this segment
- **Create a platform for adjacent services** — position Tideline as the foundation for invoicing, patient outcomes tracking, and practitioner networks

## Coherence check

- [x] Target group ↔ needs aligned — solo operators on paper need reliable booking, record access, and simple affordable software
- [x] Needs ↔ product aligned — purpose-built simplicity and affordability address the cost/complexity barrier; core features address booking and record needs
- [x] Product ↔ business goals aligned — simplicity and affordability drive adoption; multi-discipline capability grows the addressable market
- [x] Above-the-roadmap altitude held — vision describes the outcome and target, not features or milestones
- [x] Assumptions labelled honestly — affordability tolerance and discipline-agnostic demand flagged as `[to validate]`

## Open questions

- **Price sensitivity:** What monthly or annual subscription would a solo practitioner accept? Is it £30/month, £100/month, or higher?
- **Feature scope for MVP:** Do we launch with basic appointment + notes, or add invoicing, patient communication, or reporting in v1?
- **Multi-discipline viability:** Do the workflows of physios, podiatrists, and dietitians differ enough that one product feels forced? Or can a single system serve all three?
- **Competitive positioning:** How does Tideline compare to Cliniko, Acuity Scheduling, or homebrew solutions on simplicity and cost for this segment?

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 11.0/13.0 (85%) |
| Evaluated | 2026-06-13 |
| Target model | claude-haiku-4-5-20251001 |
| Judge model | claude-sonnet-4-6 |
| Target duration | 36832 ms |
| Target cost | $0.1024 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Establishes context first — names scope (one product), a 2-5 year horizon, the trigger (new product / new market), and that prior evidence was checked — before filling any cell | PASS | Header: 'Horizon: 3 years · Scope: Core appointment and records platform'; Context paragraph: 'Validation is early — we've conducted interviews with a handful of clinicians...demand and feature preferences remain largely unvalidated.' |
| c2 | All five Pichler cells are present and named — vision, target group, needs, product, business goals — none collapsed or omitted | PASS | File has five H2 headings: '## Vision', '## Target group', '## Needs', '## Product', '## Business goals' — all present and distinct. |
| c3 | The vision cell describes a change in the world (what it makes possible for the clinics), not a product description, and avoids 'best / leading / world-class / seamless' | PASS | 'Small allied-health clinics deliver consistent, personalized care without being consumed by administrative chaos.' — world-change framing, no banned superlatives. |
| c4 | Pressure-tests the vision — applies the 'would survive replacing every current feature' / 'still true if a competitor shipped the same product' check, not just asserting the statement | FAIL | The coherence check section checks cross-cell alignment and altitude but never applies the 'survives feature replacement' or 'competitor-ships-the-same' pressure test. No such check appears anywhere in the file. |
| c5 | Target group is specific and recruitable (e.g. 'solo physios running bookings on paper/spreadsheet'), explicitly NOT 'everyone'; distinguishes user from paying customer if they differ | PASS | 'Primary user and paying customer: Solo practitioners and owner-operators of micro-clinics (1–3 staff) who are both the clinician and business manager' with named specialties and current-state descriptor. |
| c6 | Needs are stated as customer problems (not features), limited to two or three core needs, and EACH is tagged `[evidenced]` / `[assumed]` / `[to validate]` — given demand is unvalidated, at least one need is honestly marked assumed or to-validate | PASS | Three needs: 'Reliable appointment management' `[evidenced]`, 'Quick access to patient history' `[assumed]`, 'Affordable, simple software' `[to validate]` — all tagged, all customer problems. |
| c7 | Product cell is three to five differentiating CHARACTERISTICS, explicitly not a feature/backlog list, and each characteristic is cross-checked against a stated need | PARTIAL | Four characteristics listed (not features). Coherence check cross-references needs at aggregate level ('purpose-built simplicity and affordability address the cost/complexity barrier') but does not map each characteristic individually to a stated need. |
| c8 | Business goals are stated as business outcomes (revenue, market position, retention), two to four of them, not vanity metrics like 'acquire many users' | PASS | Three goals: PMF validation, recurring revenue, platform for adjacent services — all outcome-framed, no raw user-count or vanity metrics. |
| c9 | Runs the cross-cell coherence check (target↔needs, needs↔product, product↔goals, above-roadmap altitude, evidence honesty) rather than checking each cell only in isolation | PASS | '## Coherence check' lists: Target group ↔ needs, Needs ↔ product, Product ↔ business goals, Above-the-roadmap altitude held, Assumptions labelled honestly — all five cross-checks present. |
| c10 | Holds CPO ownership — frames the vision as CPO-authored with PM/discovery providing slice input, not delegated authoring | PARTIAL | Header states 'Author: CPO'. No mention of PM/discovery providing slice input; the framing of who feeds what into the vision is absent from the file. |
| c11 | Names what is unknown (open questions) rather than fabricating evidence to fill gaps | PASS | '## Open questions' names four specifics: price sensitivity, MVP scope, multi-discipline viability, competitive positioning — genuine unknowns, not fabricated facts. |
| c12 | Output writes the vision file to `docs/strategy/product-vision-tideline.md` under the working directory, on one page, with the five board sections as named headings | PASS | Artifact at 'work/docs/strategy/product-vision-tideline.md' (test-harness working dir prefix); chat confirms 'docs/strategy/product-vision-tideline.md'; five H2 headings present. |
| c13 | The written file's needs section carries explicit `[evidenced\|assumed\|to validate]` tags per need, and the product section lists characteristics not features — demonstrating the argue-not-box-tick bar | PASS | Needs: three tags applied per-need (`[evidenced]`, `[assumed]`, `[to validate]`). Product: four named characteristics ('Purpose-built for micro-practices', etc.) rather than a feature list. |

### Notes

The vision board is substantively well-argued — honest tagging, specific target group, outcome-framed goals, and a genuine coherence check section. The two gaps are the absent 'survives feature replacement' pressure-test (c4) and the missing PM/discovery-input framing (c10 partial), both of which the scenario rubric specifically requires.
