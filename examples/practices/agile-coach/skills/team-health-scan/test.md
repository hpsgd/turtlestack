# Test: team-health-scan reads safety, norms, and Tuckman stage correctly

Scenario: A coach runs a health scan on a team that recently merged with another team. The skill must run an Edmondson-style anonymous psychological-safety questionnaire (handling reverse-scored items), review the working norms against what's actually followed, assess the Tuckman stage given the reteaming, and separate what to act on from what to surface to the lead.

## Prompt

Use the agile-coach `team-health-scan` skill to run a team-health scan for the "billing" team. The team's working agreements (with notes on which are followed) are at `docs/coaching/working-agreements.md` (relative to the current working directory). The team merged with the invoicing team three weeks ago and two new developers joined. Read the agreements, design the scan, and produce the health report in the skill's standard format. Write the report to `docs/coaching/health/` in the current working directory.

For the psychological-safety questionnaire, assume the following aggregated anonymous responses (1-5 scale, seven Edmondson items in order): item 1 = 4.1, item 2 = 2.3, item 3 = 3.8, item 4 = 2.1, item 5 = 3.9, item 6 = 3.2, item 7 = 2.8. Interpret these correctly, including the reverse-scored items.

Proceed without asking — design the scan and produce the report.

## Criteria

- [ ] PASS: Uses an Edmondson-style anonymous psychological-safety questionnaire with the seven classic items, and states the responses are anonymous / never attributed
- [ ] PASS: Handles reverse-scored items (1, 3, 5) correctly — recognises a high raw number on a negatively-worded item is a poor safety signal and adjusts the interpretation accordingly
- [ ] PASS: Identifies the genuinely low safety signals from the supplied data — items 2 ("able to bring up problems", 2.3) and 4 ("safe to take a risk", 2.1) — as the weak spots, not the reverse-scored items read naively
- [ ] PASS: Reviews the working norms against what's actually followed, and classifies the ignored "pair on the payments gateway" agreement as an authority/ownership gap (violated with no consequence), not a norms-wording gap
- [ ] PASS: Assesses the Tuckman stage given the three-week-old merge and two new joiners — recognises a reteaming reset (likely Forming/Storming) rather than assuming Performing
- [ ] PASS: Separates findings into act-on (within the team's process) and surface (beyond process coaching — to the lead/coordinator)
- [ ] PARTIAL: Notes the org-level reteaming-churn failure mode — constant reorganisation prevents a team ever reaching Norming

## Output expectations

- [ ] PASS: Output is a structured health report with a psychological-safety section (score + distribution + lowest items), a working-norms section, a Tuckman-stage section, and an act-on vs surface split
- [ ] PASS: The safety section correctly flags items 2 and 4 as the lowest-scoring concerns and does not misread the reverse-scored items as the problem
- [ ] PASS: Output classifies the ignored gateway-pairing agreement as an authority gap (no consequence for violation) distinct from a vague-wording norms gap
- [ ] PASS: Output assigns a Tuckman stage consistent with a recent merge (Forming or Storming) and ties the assessment to the reteaming event
- [ ] PASS: Output routes serious / beyond-process findings to the team's lead or coordinator rather than turning them into a coaching action item
- [ ] PARTIAL: Output states that the questionnaire is anonymous and reports distributions, never individuals
