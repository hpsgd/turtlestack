---
# Match the model the agent declares (sonnet) in
# plugins/product/gtm/agents/gtm.md. The runner otherwise
# falls back to the harness default (Haiku), which is not what the
# agent is designed to run on.
target-model: claude-sonnet-4-6
---

# Test: Launch strategy

Scenario: A GTM manager needs a go-to-market plan for a new analytics feature being added to a B2B project management tool.

## Prompt


We're launching "Clearpath Analytics" next month — a new analytics module for our project management tool. Key capabilities:

- Real-time project health dashboard (RAG status across all projects)
- Resource utilisation reports (who's overloaded, who's under-utilised)
- On-time delivery rate trends by team and project type
- Executive summary reports (PDF/email, weekly)

Target customers: Existing Clearpath customers with 50+ seats (we have 340 of them). New pricing: $15/seat/month add-on. We think mid-market operations directors and PMOs are the buyers.

Main competitors: Asana's reporting, Monday.com dashboards. We think we're better at the executive summary piece specifically.

Can you help me build the launch strategy?

Output structure:

- **Customer-problem-led messaging** at the top: lead with the problem (blind spots in project health, late deliveries discovered too late, hidden over-utilisation) BEFORE the product capability list. The product features are the answer to the problem, not the headline.
- **TWO distinct GTM motions** explicitly named and separated:
  1. **Existing customer expansion** (340 Pro accounts, ~50+ seats) — in-product upsell, account-team-led, no acquisition cost. Target: 30% attach rate by Q4.
  2. **New customer acquisition** ("Analytics" as differentiated landing) — content marketing, paid search on PM-reporting keywords, demo-led sales. Target: 50 net-new logos.
- **Post-launch review plan** with measurable success metrics + cadence: T+30, T+60, T+90 reviews. Specific metrics: attach rate, MRR contribution, NPS for the module, support ticket volume by category.
- **Competitive positioning**: name the differentiator (executive summary report PDF/email weekly) explicitly and compare with Asana reporting + Monday.com dashboards on this specific dimension.

A few specifics for the response:

- Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
- Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
- For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
- When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
- Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Criteria


- [ ] PASS: All marketing copy, messaging, and campaign content is labelled DRAFT and flagged for human review before use
- [ ] PASS: Applies positioning work before tactics — identifies the competitive alternative (Asana/Monday reporting), differentiator (executive summaries), and target segment (operations directors/PMOs at 50+ seat accounts) before writing messages
- [ ] PASS: Leads messaging with the customer problem (e.g. blind spots in project health, lack of exec visibility) rather than feature descriptions
- [ ] PASS: Recommends a launch tier (given 340 existing customers and $15/seat add-on, this is likely a Tier 2 or Tier 1 launch — not a silent rollout)
- [ ] PASS: Distinguishes between the existing customer expansion play (340 accounts) and any net-new motion — these require different approaches
- [ ] PARTIAL: Includes a post-launch review plan with success metrics — partial credit if metrics are named but no review timeline or owner is specified
- [ ] PASS: Produces a structured launch plan with phases and owners, not a list of marketing ideas

## Output expectations

- [ ] PASS: Output sizes the existing-customer revenue opportunity — 340 accounts × 50+ seats × $15/seat/month — yielding the upper-bound ARR (~$3M+) and a realistic conversion target (e.g. "30% adoption in year 1 → ~$900K ARR uplift")
- [ ] PASS: Output's positioning anchors against Asana / Monday native reporting as the competitive alternatives, with the executive summary as the named differentiator — not a generic feature list
- [ ] PASS: Output's customer-problem framing leads with the operations director / PMO pain — e.g. "execs ask 'how are projects tracking?' and you spend half a day pulling a manual report" — not "we have a new analytics module"
- [ ] PASS: Output classifies this as Tier 1 or Tier 2 launch given 340 existing customers, $15/seat ARR uplift, and a 3-year-customer-base activation event — explicitly NOT a silent rollout
- [ ] PASS: Output separates the existing-customer expansion motion (CSM-led, in-product upsell, QBR conversations) from any net-new acquisition motion — different channels, different messaging, different sales process
- [ ] PASS: Output's launch plan has phases with owners and dates — Pre-launch (weeks -4 to 0): readiness checklist, sales enablement, beta close-out; Launch week: announcements, in-product, customer comms; Post-launch (weeks 1-12): adoption tracking, expansion plays, feedback loops
- [ ] PASS: Output's marketing copy and messaging examples are labelled DRAFT — explicitly flagged for human review before publication
- [ ] PASS: Output's post-launch review plan names success metrics (e.g. trial signups, paid conversions, % of 340-base activated, $ ARR uplift), a review date (e.g. "Day 30, Day 60, Day 90 reviews"), and a review owner
- [ ] PASS: Output addresses internal readiness alongside external launch — sales enablement (battle cards, demo scripts), CSM enablement (expansion playbooks), support training, docs ready before announce
- [ ] PARTIAL: Output addresses pricing communication carefully — $15/seat add-on for existing customers may need grandfathering for early adopters or volume discounting at the 340 mid-market scale
