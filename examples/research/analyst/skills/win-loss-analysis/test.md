# Test: win-loss-analysis skill (buyer-vs-rep gap)

Scenario: A sales leader doesn't trust the CRM close-reasons for a batch of Q2 mid-market losses to a competitor (Pinnacle). They want a win/loss analysis that surfaces the gap between what reps reported and what buyers actually said, working from staged deal records.

## Prompt

Work entirely from the staged deal records — do NOT perform any live web research (no WebSearch, no WebFetch). The deal set, the sales-reported reasons, and the buyer-reported reasons are already on disk.

/analyst:win-loss-analysis losses to Pinnacle (Q2 mid-market) {workspace}/work/deals

Read `{workspace}/work/deals/q2-deal-records.md` first — it holds the deal set context (window, segment, win/loss mix) and, for each deal, the SALES-reported close reason and the BUYER-reported reason from post-close interviews.

Requirements for the response:

- Scope the deal set explicitly (window, segment, win/loss mix) and note the 7-14 day post-close interview discipline.
- Put the sales-reported reason next to the buyer-reported reason for each deal — and make the BUYER-VS-REP GAP the headline, near the top. Where reps systematically say "price" but buyers say something else, name it as a messaging/sales-process problem wearing a product-problem costume.
- Extract PATTERNS across the set (a pattern needs two or more deals): e.g. unclear differentiation, slow follow-up misfiled as feature gaps, hidden decision-makers (security / procurement vetoes), migration-trust gaps. A single deal is an anecdote, not a pattern.
- Include the WINS — say what they tell you to protect (discovery + migration confidence + painless buying), not just what to fix.
- Recommend specific owned actions, separating fix-the-product from fix-the-messaging from fix-the-sales-process.

## Criteria

- [ ] PASS: Skill writes a conforming report to disk under `deals/win-loss-analysis/` (see ARTIFACTS WRITTEN — at least one .md file there)
- [ ] PASS: The written file opens with YAML frontmatter including title, date, author=win-loss-analysis, category (per report-conventions)
- [ ] PASS: The deal set is scoped explicitly (window, mid-market segment, win/loss mix) with the post-close interview-timing discipline noted
- [ ] PASS: The buyer-vs-rep GAP is the headline near the top — sales-reported reasons placed against buyer-reported reasons
- [ ] PASS: The report names the systematic divergence — reps repeatedly report "price" while buyers report unclear differentiation / security veto / migration distrust — and reads it as a messaging/sales-process issue, not a product-price issue
- [ ] PASS: Patterns are extracted across two or more deals each (unclear differentiation; slow follow-up misfiled as feature gap; hidden decision-makers; migration trust) — not one-off anecdotes
- [ ] PASS: Hidden decision-makers (security veto on Borealis, procurement on Evergreen) are surfaced as a pattern distinct from the stated reasons
- [ ] PASS: The wins are included and used to say what to PROTECT (discovery, migration confidence, painless buying) — not a losses-only fix-list
- [ ] PASS: Recommendations separate fix-the-product from fix-the-messaging from fix-the-sales-process
- [ ] PASS: The skill did NOT perform live web research — it analysed the staged records
- [ ] PASS: Chat response includes the absolute path to the written report

## Output expectations

- [ ] PASS: The single most useful output is the buyer-vs-rep gap, not a deal catalogue — the report makes the divergence measurable (reps say price, buyers say differentiation/trust/veto)
- [ ] PASS: The analysis distinguishes a genuine product gap from a sales-execution or value-communication failure wearing a product-problem costume
