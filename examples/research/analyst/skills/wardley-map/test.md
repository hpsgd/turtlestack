# Test: wardley-map skill (visibility x evolution)

Scenario: A product team for Helio (an AI meeting-notes product) wants a Wardley Map of their value chain to see where commoditisation is approaching and where to invest, working from a staged capability brief.

## Prompt

Work entirely from the staged capability brief — do NOT perform any live web research (no WebSearch, no WebFetch). The value chain and the market maturity evidence you need are on disk.

/analyst:wardley-map Manager gets accurate shareable meeting notes without taking them (Helio) {workspace}/work/helio

Read `{workspace}/work/helio/capability-brief.md` first — it states the user and need, the value-chain components, and market evidence on the maturity of each component.

Requirements for the response:

- Anchor on the user need in one sentence (the manager's outcome, not a feature).
- Build the value chain: list the components, place each on the VISIBILITY axis (high near the user, low for infrastructure), and show the dependency links.
- Place every component on the EVOLUTION axis (genesis / custom-built / product / commodity) from the market evidence in the brief, stating the basis — e.g. speech-to-text and LLM inference are commoditising; action-item extraction is still genesis/custom.
- Extract all three strategic signals: approaching commoditisation (and any Helio differentiation sitting on a commoditising component — the custom summariser), competitor over/under-investment (the competitor's custom speech-to-text), and a build/buy/partner call per component that matters.
- End with an investment call: where to invest and own, where to buy/rent rather than build.

## Criteria

- [ ] PASS: Skill writes a conforming report to disk under `helio/wardley-map/` (see ARTIFACTS WRITTEN — at least one .md file there)
- [ ] PASS: The written file opens with YAML frontmatter including title, date, author=wardley-map, category (per report-conventions)
- [ ] PASS: The map is anchored on the user NEED (manager getting shareable notes), stated as an outcome, not a feature
- [ ] PASS: A value chain is built with components placed on a VISIBILITY axis (user-facing high, infrastructure low) and dependency links shown
- [ ] PASS: Every component is placed on the EVOLUTION axis (genesis / custom / product / commodity) with the basis drawn from the staged market evidence
- [ ] PASS: Speech-to-text and LLM inference are correctly read as commoditising (commodity/utility direction), and action-item extraction as still genesis/custom differentiation — per the staged evidence, not arbitrary
- [ ] PASS: The "approaching commoditisation" signal flags Helio's custom summariser as differentiation sitting on a commoditising component (the erosion warning)
- [ ] PASS: The "competitor over/under-investment" signal flags the competitor custom-building speech-to-text that is now a commodity
- [ ] PASS: A build/buy/partner call is made per component that matters (own action-item extraction; buy/rent STT, LLM, compute)
- [ ] PASS: The skill ends with an investment position — where to invest, what to stop building — not just a diagram
- [ ] PASS: The skill did NOT perform live web research — it applied the framework to the staged brief
- [ ] PASS: Chat response includes the absolute path to the written report

## Output expectations

- [ ] PASS: Output uses the two Wardley axes correctly — visibility (vertical, user need at top) and evolution (horizontal, genesis to commodity) — not a generic 2x2 or maturity list
- [ ] PASS: The strategic read connects evolution placement to action — components heading to commodity should be bought not built; the differentiator (action-item extraction) is where to invest
