# Test: five-forces skill (Porter, judgment not box-tick)

Scenario: A well-funded startup is deciding whether to enter the Australian SMB cloud accounting software market aimed at micro-businesses. They want a Porter's Five Forces read that concludes on attractiveness for a NEW ENTRANT, working from a staged industry brief.

## Prompt

Work entirely from the staged industry brief — do NOT perform any live web research (no WebSearch, no WebFetch). The structural facts you need are on disk.

/analyst:five-forces AU SMB cloud accounting software — decision: should a new entrant (Orchid) enter aimed at micro-businesses? {workspace}/work/orchid

Read `{workspace}/work/orchid/industry-brief.md` first — it states the decision and the structural facts (players, rivalry, buyers, suppliers, entry barriers, substitutes).

The deliverable is a written report file on disk under `{workspace}/work/orchid/five-forces/`, not a chat answer. Write the conforming report to that path with the Write tool, then reply with the absolute path. Do not produce the analysis only in the chat reply.

Requirements for the report:

- Frame the decision explicitly at the top (new-entrant lens, micro-business segment) — the forces have no reference point without it.
- Assess all five forces, rating intensity AND the direction each points for profitability, with the specific evidence from the brief behind each rating.
- Do NOT stop at five independent ratings. Identify the ONE or TWO forces that dominate this decision and explain why they outweigh the others — that is the core judgment.
- Conclude with a clear position on attractiveness for the new entrant: enter / don't / conditional on a specific move. "Moderate across the board" is not acceptable.
- Note where the static model is weak for this market and what to use instead.

## Criteria

- [ ] PASS: Skill writes a conforming report to disk under `orchid/five-forces/` (see ARTIFACTS WRITTEN — at least one .md file there)
- [ ] PASS: The written file opens with YAML frontmatter including title, date, author=five-forces, category (per report-conventions)
- [ ] PASS: The decision is framed explicitly at the top as a NEW-ENTRANT decision in the micro-business segment — not a neutral industry description
- [ ] PASS: All five forces are assessed, each with an intensity rating AND a direction for profitability, each backed by specific evidence from the staged brief
- [ ] FAIL-IF-MECHANICAL: The report does NOT simply rate every force "moderate" and stop — a flat five-box grid with no dominant force identified must NOT pass this criterion
- [ ] PASS: The report identifies the ONE or TWO dominant forces (e.g. threat-of-new-entrants via the accountant-channel moat, and rivalry) and explains why they outweigh the others
- [ ] PASS: The report reaches a clear VERDICT on structural attractiveness for the new entrant — enter / don't enter / conditional on a stated move — not a balanced non-conclusion
- [ ] PASS: Supplier power is correctly read as LOW (commoditised cloud hosting, non-scarce talent) rather than mechanically rated "moderate" to fill the box
- [ ] PASS: The report notes a limit of the static Five Forces model for this market (e.g. channel dynamics / evolution) and what to use instead
- [ ] PASS: The skill did NOT perform live web research — it applied the framework to the staged brief
- [ ] PASS: Chat response includes the absolute path to the written report

## Output expectations

- [ ] FAIL-IF-MECHANICAL: A purely mechanical filled-in grid (all five forces present but no stated position on what dominates or whether to enter) would FAIL — the output must take a position, and it does
- [ ] PASS: The dominant-force judgment is substantive — it names the structural reason the entry barrier (accountant channel moat + rivalry against entrenched incumbents) is the binding constraint for THIS entrant decision, not just that some force is "high"
