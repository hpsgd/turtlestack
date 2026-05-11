# Test: market-sizing skill

Scenario: A startup founder needs a defensible TAM estimate for the Australian aged care technology market to include in a Series A pitch deck.

## Prompt

/analyst:market-sizing Australian aged care technology — SaaS tools for residential aged care providers, current year

## Criteria

- [ ] PASS: Skill writes a file to disk at `<pwd>/market-sizing/<market-slug>.md` (see ARTIFACTS WRITTEN — at least one .md file under `market-sizing/` exists)
- [ ] PASS: The written file opens with YAML frontmatter (title, date, author=market-sizing, category=Commercial, subject) per report-conventions
- [ ] PASS: Chat response includes the absolute path to the written report (verbatim, copyable)
- [ ] PASS: Skill defines the market before producing any figures — buyer type, purchase unit, geography (AU), and time horizon are all stated
- [ ] PASS: Both top-down and bottom-up estimates are attempted — if one genuinely can't be done, the reason is explained
- [ ] PASS: Top-down estimate cites a specific report title, year, and figure — not a generic reference to "analysts"
- [ ] PASS: Bottom-up estimate shows the calculation explicitly (N customers × $X avg spend × Y% penetration = $Z)
- [ ] PASS: Where top-down and bottom-up figures diverge by more than 2x, skill diagnoses the gap rather than averaging them
- [ ] PASS: All estimates are labelled as estimates — none presented as established facts
- [ ] PASS: AU-specific sources are used where available (ABS, IBISWorld AU, ACSA) before defaulting to global analyst reports
- [ ] PARTIAL: Confidence rating is provided with reasoning — not just asserted without evidence

## Output expectations

- [ ] PASS: Output's market definition specifies — buyer (residential aged care provider), purchase unit (subscription / per-bed pricing typical), geography (Australia), time horizon (current year)
- [ ] PASS: Output's top-down estimate cites specific reports — IBISWorld Australia "Aged Care SaaS" or sector adjacent, government data (Department of Health and Aged Care), Aged Care Industry Association reports — with title, year, and figure
- [ ] PASS: Output's bottom-up estimate shows the math — N residential aged care providers in AU × average-bed count × % currently using SaaS × $X per-bed-per-month × 12 — with each input source-cited
- [ ] PASS: Output reconciles top-down and bottom-up — if they differ by >2x, the gap is diagnosed (different segment definitions, different penetration assumptions, one excludes hardware) rather than averaged
- [ ] PASS: Output uses AU-specific sources first — Aged Care Quality and Safety Commission, ABS Health Services data, ACSA (Aged & Community Services Australia), AFR / Australian sector press — before defaulting to global analyst reports
- [ ] PARTIAL: Output's TAM / SAM / SOM breakdown is shown — TAM (all residential aged care SaaS), SAM (the addressable subset given product fit), SOM (realistic capture given competitive set and team) — with reasoning per layer
- [ ] PASS: Output labels EVERY estimate as "estimate" — not "the market is $X" but "estimated at $X based on Y inputs from Z sources"
- [ ] PARTIAL: Output's confidence rating is shown with reasoning — overall or per-estimate confidence with explanation of why (e.g., source robustness, recency, definition clarity)
